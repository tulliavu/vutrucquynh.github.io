# Quynh Tu Lai — GitHub Pages Personal Site

A clean, modern personal website for showcasing your Master's research on electric vehicle charging station siting optimization.

## Setup Instructions

### 1. Create a GitHub Pages Repository

1. Go to GitHub and create a new repository named `tulliavu.github.io`
2. Clone it to your local machine:
   ```bash
   git clone https://github.com/tulliavu/tulliavu.github.io.git
   cd tulliavu.github.io
   ```

### 2. Add the Website Files

Copy all files from this project into your repository:
- `index.html` - Main page
- `css/style.css` - Stylesheet
- `js/main.js` - Navigation scripts
- `images/` - Directory for your images (see below)

### 3. Add Images

Create an `images/` directory and add:

**avatar.png** (or .jpg)
- Your profile photo
- Size: 148x148 pixels (will be displayed as circular)
- Can be larger; it will be cropped to a circle

**favicon.svg** (optional)
- A small icon that appears in browser tabs
- You can use an SVG or replace with a .ico file

### 4. Update Your Information

Edit `index.html` and customize:

- **Email**: Update the email link in the hero section
- **Social links**: Modify URLs for GitHub, LinkedIn, etc.
- **Research description**: Update the intro paragraph
- **Tags**: Change your research keywords
- **Education dates**: Update your program dates
- **Supervisors**: Add links to your advisor profiles
- **Skills**: Modify the skill list in the Experience section

### 5. Customize Colors (Optional)

To change the accent color (currently blue `#0066cc`), edit `css/style.css`:

```css
:root {
  --accent: #0066cc;  /* Change this color */
  --accent-dark: #0052a3;  /* Darker version for hover */
}
```

Some suggestions:
- Green (sustainability): `#10b981`
- Teal (modern): `#0891b2`
- Purple (academic): `#8b5cf6`

### 6. Deploy to GitHub

```bash
git add .
git commit -m "Initial website commit"
git push origin main
```

Your site will be live at: `https://tulliavu.github.io`

## Features

✨ **Responsive Design** - Looks great on mobile, tablet, and desktop
🌙 **Dark Mode Support** - Automatically adapts to system preferences
📱 **Mobile Navigation** - Hamburger menu for small screens
♿ **Accessible** - Semantic HTML and ARIA labels
🎨 **Modern Styling** - Clean, professional aesthetic

## File Structure

```
tulliavu.github.io/
├── index.html
├── css/
│   └── style.css
├── js/
│   └── main.js
├── images/
│   ├── avatar.png
│   └── favicon.svg
└── README.md
```

## Customizing Sections

### Add Publications

Edit the publications section in `index.html`:

```html
<div class="pub-item">
  <h3>Your Paper Title</h3>
  <p class="pub-meta">Authors · <span class="pub-journal">Journal Name</span>, 2025</p>
  <p style="color: var(--text-muted);">Brief description of the paper.</p>
</div>
```

### Add News/Updates

Uncomment or add to the news section to show latest updates about your research.

### Modify Navigation

Edit the navigation links in the `<header>` section if you want to add more pages (Publications, Talks, etc.). Each needs a corresponding `<section id="...">` in the HTML.

## Tips

- **Keep it updated**: Update your site regularly with new publications and achievements
- **Profile picture**: Use a professional, well-lit headshot for your avatar
- **Mobile testing**: Test on your phone to ensure it looks good
- **Links**: Double-check all external links work correctly

## Additional Pages

To add more pages (e.g., publications.html, talks.html):

1. Create the new HTML file with the same header and footer
2. Copy the same CSS and JS files to maintain consistent styling
3. Link to it from the navigation in all pages

## License

This template is provided as-is for personal use.

---

**Questions?** Feel free to check the original template at [EricJin73.github.io](https://ericjin73.github.io/) for more ideas.
