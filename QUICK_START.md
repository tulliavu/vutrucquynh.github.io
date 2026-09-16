# How to edit this site

Everything is in two files: `index.html` for content, `css/style.css` for
design. There is no build step: save the file, reload the browser.

## Replace the photo

The site loads `images/avatar.jpg`. Keep it small: the old 7.6 MB PNG took so
long to load that the page looked broken. Anything under ~300 KB is fine.

On a Mac you can resize and compress in one command:

```bash
sips -s format jpeg -s formatOptions 80 -Z 900 my-photo.jpg --out images/avatar.jpg
```

`-Z 900` caps the longest side at 900 px. If you use a different filename,
update the `src` and the `width`/`height` attributes on the `<img class="portrait">`
tag in `index.html`.

The photo is displayed in a 3:4 portrait box and cropped from the centre, so a
vertical shot with your face near the middle works best.

## Change the colours and type

All design decisions live in the `:root` block at the top of `css/style.css`:

```css
--serif:  /* body text and headings */
--sans:   /* small labels: nav, dates, section titles */
--bg:     /* page background */
--ink:    /* main text */
--ink-soft: /* secondary text: dates, captions */
--rule:   /* hairline rules and underlines */
--measure: /* how wide a line of text gets */
--gutter:  /* the left column holding section labels */
```

Dark mode repeats those same names inside the
`@media (prefers-color-scheme: dark)` block just below. Change a colour in one
place, change it in the other too.

The design deliberately has no accent colour. If you want one, the natural
place is link underlines:

```css
a:hover { text-decoration-color: #0f766e; }
```

## Edit a section

Every section follows the same shape. The `<h2>` sits in the left margin, the
`.body` holds the content:

```html
<section id="talks">
  <h2>Talks</h2>
  <div class="body">
    <div class="entry">
      <p class="years">Mar 2026</p>
      <h3>Title of the talk</h3>
      <p class="meta">Conference name, city</p>
      <p>One or two sentences about it.</p>
    </div>
  </div>
</section>
```

Then add it to the navigation at the top of `index.html`:

```html
<a href="#talks">Talks</a>
```

Useful classes:

- `.entry`: one item, with spacing below it
- `.years`: small date line above a heading
- `.meta`: small grey line below a heading
- `.plain`: a list with no bullets (used by the Methods section)

To remove a section, delete the whole `<section>` block and its `<a>` in the
navigation.

## Preview before publishing

```bash
python3 -m http.server 4173
```

Open <http://localhost:4173>, and check it at phone width too. The layout
drops to a single column below 46rem (736 px).

Then run the checker:

```bash
python3 scripts/check.py
```

It catches the things that are invisible until the page is live: a nav link
pointing at a section you renamed, a photo referenced under the wrong
filename, a duplicated `id`, an unescaped `&` in a URL, a stray brace or an
undefined variable in the CSS, and a photo large enough to slow the page
down. The same script runs on GitHub after every push.

## Publish

```bash
git add -A
git commit -m "Update site"
git push origin main
```

GitHub rebuilds within a minute or two.

## Troubleshooting

**Changes not showing.** Hard-refresh (Cmd+Shift+R). GitHub Pages also caches
for a short while.

**Image not loading.** Filenames are case-sensitive on the server:
`Avatar.jpg` and `avatar.jpg` are different files.

**`tulliavu.github.io` shows 404.** That address only works if the repository
is named `tulliavu.github.io`. This one is named `vutrucquynh.github.io`, so
the site lives at `tulliavu.github.io/vutrucquynh.github.io/`. Renaming the
repository in Settings would move it to the short address.
