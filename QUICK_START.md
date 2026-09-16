# Quick Start Guide

## 5-Minute Setup

### Step 1: Create GitHub Repository
1. Log in to [GitHub](https://github.com)
2. Click the **+** icon → **New repository**
3. Name it: `tulliavu.github.io` (replace with your username if different)
4. Click **Create repository**

### Step 2: Add Your Files
1. Clone the repo: `git clone https://github.com/tulliavu/tulliavu.github.io.git`
2. Copy all files from this project into that folder
3. Add your profile photo as `images/avatar.png` (148x148px or larger)

### Step 3: Personalize
Edit `index.html` and change:
- Line 6: Your name in the `<title>`
- Line 13: Meta description
- Line 37: Your email (line 54 in HTML)
- Line 59: GitHub link to your profile
- Line 63: LinkedIn link (or remove if not needed)
- Update the biography paragraph
- Update education dates and supervisor information

### Step 4: Deploy
```bash
cd tulliavu.github.io
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 5: Visit Your Site
Go to: `https://tulliavu.github.io`

(It may take 1-2 minutes for GitHub to build and deploy)

---

## Customization Tips

### Change the Color Scheme
Open `css/style.css` and find:
```css
--accent: #0066cc;  /* Blue - change this */
```

Replace with:
- **Green**: `#10b981` (environmental)
- **Teal**: `#0891b2` (modern)
- **Emerald**: `#059669` (sustainable)

### Add Your Photo
1. Take a professional headshot (face-on, good lighting)
2. Resize to at least 300x300px
3. Save as `images/avatar.png` or `.jpg`
4. If you save as `.jpg`, update the HTML: `src="images/avatar.jpg"`

### Update Social Links
In `index.html`, find the social links section and update URLs:
```html
<a href="mailto:your.email@example.com">Email</a>
<a href="https://github.com/your-username">GitHub</a>
<a href="https://linkedin.com/in/your-profile">LinkedIn</a>
```

### Add More Sections
To add sections like "Talks" or "Grants":
1. Copy one of the existing section blocks
2. Give it a unique `id` (e.g., `id="grants"`)
3. Add a link in the navigation: `<li><a href="#grants">Grants</a></li>`

---

## Troubleshooting

**Site not showing up after pushing?**
- Wait 2-3 minutes for GitHub to build
- Check repository settings: Settings → Pages → Should show "Your site is live at..."

**Favicon not showing?**
- Clear browser cache (Ctrl+Shift+Del)
- Hard refresh the page (Ctrl+F5)

**Images not loading?**
- Make sure images are in the `images/` folder
- Use correct filename (case-sensitive on Linux servers)
- Check that you used the right path: `images/avatar.png`

---

## Next Steps

- ✅ Add publications and research output
- ✅ Update with news and achievements  
- ✅ Add links to your papers and presentations
- ✅ Keep social links current
- ✅ Update education dates as you progress

---

## Useful Links
- [GitHub Pages Docs](https://docs.github.com/en/pages)
- [HTML Tutorial](https://www.w3schools.com/html/)
- [CSS Guide](https://www.w3schools.com/css/)
