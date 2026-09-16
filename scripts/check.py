#!/usr/bin/env python3
"""Check the site before publishing.

Catches the mistakes that are easy to make by hand and invisible until the
page is live: a mistyped class or id, a nav link pointing at a section that
was renamed, a photo referenced under the wrong filename, an unescaped & in
a query string, a stray brace in the stylesheet.

    python3 scripts/check.py
"""

import html.parser
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "source", "track", "wbr"}

problems = []


def fail(message):
    problems.append(message)


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.open_tags = []
        self.ids = []
        self.fragments = []
        self.labelledby = []
        self.local_assets = []

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if "id" in attr:
            self.ids.append(attr["id"])
        if "aria-labelledby" in attr:
            self.labelledby.append(attr["aria-labelledby"])
        for key in ("href", "src"):
            value = attr.get(key, "")
            if value.startswith("#"):
                self.fragments.append(value[1:])
            elif value and not re.match(r"(https?:|mailto:|data:|//)", value):
                self.local_assets.append(value.split("?")[0].split("#")[0])
        if tag not in VOID:
            self.open_tags.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if not self.open_tags:
            fail(f"index.html: stray </{tag}> at line {self.getpos()[0]}")
            return
        name, pos = self.open_tags.pop()
        if name != tag:
            fail(f"index.html: </{tag}> at line {self.getpos()[0]} closes "
                 f"<{name}> opened at line {pos[0]}")


source = (ROOT / "index.html").read_text()
parser = Parser()
parser.feed(source)

for name, pos in parser.open_tags:
    fail(f"index.html: <{name}> at line {pos[0]} is never closed")

for anchor_id in sorted({i for i in parser.ids if parser.ids.count(i) > 1}):
    fail(f"index.html: id=\"{anchor_id}\" is used more than once")

for fragment in parser.fragments:
    if fragment not in parser.ids:
        fail(f"index.html: link to #{fragment}, but nothing has that id")

for target in parser.labelledby:
    if target not in parser.ids:
        fail(f"index.html: aria-labelledby=\"{target}\" has no matching id")

for asset in sorted(set(parser.local_assets)):
    if not (ROOT / asset).is_file():
        fail(f"index.html: references {asset}, which does not exist")

# An unescaped & inside an attribute silently truncates query strings.
body = source.split("</script>")[-1]
stray = len(re.findall(r"&(?!#|\w{2,8};)", body))
if stray:
    fail(f"index.html: {stray} unescaped & in the page body, write &amp;")

# House style: plain hyphens only. Em and en dashes read as machine-written.
for glyph, name in (("\u2014", "em dash"), ("\u2013", "en dash")):
    count = source.count(glyph) + source.count("&mdash;" if name == "em dash"
                                               else "&ndash;")
    if count:
        fail(f"index.html: {count} {name}(s) - use a plain hyphen instead")

block = re.search(r'<script type="application/ld\+json">(.*?)</script>',
                  source, re.S)
if not block:
    fail("index.html: no JSON-LD block")
else:
    try:
        json.loads(block.group(1))
    except json.JSONDecodeError as error:
        fail(f"index.html: JSON-LD is not valid JSON: {error}")

css = (ROOT / "css" / "style.css").read_text()
if css.count("{") != css.count("}"):
    fail(f"style.css: {css.count('{')} opening braces, {css.count('}')} closing")

for declared in sorted(set(re.findall(r"var\((--[\w-]+)\)", css))):
    if not re.search(rf"^\s*{re.escape(declared)}\s*:", css, re.M):
        fail(f"style.css: uses {declared}, which is never defined")

# Every class in the stylesheet should be on the page, and the other way round.
# A renamed section otherwise leaves a rule styling nothing.
used = set()
for match in re.finditer(r'class="([^"]+)"', source):
    used.update(match.group(1).split())
declared = set(re.findall(r"\.([a-zA-Z][\w-]*)",
                          re.sub(r"/\*.*?\*/", "", css, flags=re.S)))
for name in sorted(declared - used):
    fail(f"style.css: .{name} is styled but never used in index.html")
for name in sorted(used - declared):
    fail(f"index.html: class=\"{name}\" has no rule in style.css")


def root_token(name, block):
    found = re.search(rf"{name}:\s*(#\w+)", block)
    return found.group(1) if found else None


light_block = re.search(r":root \{(.*?)\}", css, re.S)
dark_block = re.search(r"@media \(prefers-color-scheme: dark\) \{\s*:root \{(.*?)\}",
                       css, re.S)
if light_block and dark_block:
    # The browser paints its own chrome from theme-color, so a stale value
    # shows as a seam above the page on a phone.
    themes = {scheme: colour for colour, scheme in re.findall(
        r'<meta name="theme-color" content="(#\w+)" media="\(prefers-color-scheme: (\w+)\)">',
        source)}
    for scheme, block in (("light", light_block), ("dark", dark_block)):
        token = root_token("--bg", block.group(1))
        if themes.get(scheme) != token:
            fail(f"index.html: theme-color for {scheme} is {themes.get(scheme)}, "
                 f"but --bg is {token}")

    favicon = (ROOT / "images" / "favicon.svg").read_text()
    strokes = re.findall(r"stroke:\s*(#\w+)", favicon)
    for scheme, block, stroke in (("light", light_block, strokes[0] if strokes else None),
                                  ("dark", dark_block, strokes[1] if len(strokes) > 1 else None)):
        token = root_token("--ink", block.group(1))
        if stroke != token:
            fail(f"favicon.svg: {scheme} stroke is {stroke}, but --ink is {token}")

# Nav links must run in the same order as the sections, or the page reads as
# one order and navigates as another.
nav = re.search(r'<nav aria-label="Sections">(.*?)</nav>', source, re.S)
if nav:
    linked = re.findall(r'href="#([\w-]+)"', nav.group(1))
    sections = re.findall(r'<section id="([\w-]+)"', source)
    if linked != [s for s in sections if s in linked]:
        fail(f"index.html: nav order {linked} does not follow section order "
             f"{sections}")


def jpeg_size(path):
    """Width and height from the JPEG SOF marker, without a image library."""
    data = path.read_bytes()
    offset = 2
    while offset + 9 < len(data):
        if data[offset] != 0xFF:
            return None
        marker = data[offset + 1]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            return (int.from_bytes(data[offset + 7:offset + 9], "big"),
                    int.from_bytes(data[offset + 5:offset + 7], "big"))
        offset += 2 + int.from_bytes(data[offset + 2:offset + 4], "big")
    return None


photo = ROOT / "images" / "avatar.jpg"
if photo.is_file():
    if photo.stat().st_size > 500_000:
        fail(f"images/avatar.jpg is {photo.stat().st_size // 1024} KB, "
             f"compress it (see QUICK_START.md) so the page loads quickly")

    # Wrong width/height attributes make the page jump as the photo loads;
    # wrong og:image dimensions make the link preview crop badly.
    real = jpeg_size(photo)
    tag = re.search(r'class="portrait"[^>]*width="(\d+)" height="(\d+)"', source)
    meta_size = (re.search(r'og:image:width" content="(\d+)"', source),
                 re.search(r'og:image:height" content="(\d+)"', source))
    if real and tag and (int(tag.group(1)), int(tag.group(2))) != real:
        fail(f"index.html: portrait is tagged {tag.group(1)}x{tag.group(2)}, "
             f"but the file is {real[0]}x{real[1]}")
    if real and all(meta_size) and (int(meta_size[0].group(1)),
                                    int(meta_size[1].group(1))) != real:
        fail(f"index.html: og:image is {meta_size[0].group(1)}x"
             f"{meta_size[1].group(1)}, but the file is {real[0]}x{real[1]}")

if problems:
    for problem in problems:
        print(f"✗ {problem}")
    sys.exit(1)

print("✓ all checks passed")
