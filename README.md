# Personal site of Vu Truc Quynh

Static site, no build step and no JavaScript. GitHub Pages serves it straight
from the `main` branch.

Live at <https://tulliavu.github.io/vutrucquynh.github.io/>

```
index.html          the whole page, every section lives here
css/style.css       all styling, design tokens at the top
images/avatar.jpg   portrait, 675x900
images/favicon.svg  favicon
scripts/check.py    pre-publish checks, also run by CI
```

## Editing

Open `index.html` in any editor and change the text. To preview, open the file
in a browser, or, if the relative paths misbehave, serve the folder:

```bash
python3 -m http.server 4173
```

then visit <http://localhost:4173>.

See [QUICK_START.md](QUICK_START.md) for how to change the photo, colours and
sections.

## Publishing

Check first. This is faster than finding a broken link on the live site:

```bash
python3 scripts/check.py
```

Then:

```bash
git add -A && git commit -m "Update site" && git push origin main
```

GitHub rebuilds the page within a minute or two, and runs the same check.
