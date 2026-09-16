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

photo = ROOT / "images" / "avatar.jpg"
if photo.is_file() and photo.stat().st_size > 500_000:
    fail(f"images/avatar.jpg is {photo.stat().st_size // 1024} KB, "
         f"compress it (see QUICK_START.md) so the page loads quickly")

if problems:
    for problem in problems:
        print(f"✗ {problem}")
    sys.exit(1)

print("✓ all checks passed")
