---
name: Fogsift v2.0.0 Build
overview: Replace the current Hello World site with the full Fogsift v2.0.0 build from the manifest, then deploy to Cloudflare Pages.
todos:
  - id: create-index
    content: Replace dist/index.html with Fogsift v2.0.0 SPA
    status: completed
  - id: create-404
    content: Create dist/404.html failsafe page
    status: completed
  - id: create-robots
    content: Create dist/robots.txt bot control file
    status: completed
  - id: create-sitemap
    content: Create dist/sitemap.xml
    status: completed
  - id: deploy
    content: Deploy to Cloudflare Pages
    status: completed
---

# Fogsift v2.0.0 Implementation

## Files to Create

All files go in the existing `dist/` directory:

| File | Status |
|------|--------|
| `index.html` | Replace existing with full SPA (provided) |
| `404.html` | Create (provided) |
| `robots.txt` | Create (provided) |
| `sitemap.xml` | Create (provided) |
| `favicon.png` | MISSING - placeholder needed |
| `og-image.png` | MISSING - placeholder needed |

## Implementation Steps

1. Replace [dist/index.html](dist/index.html) with the complete Fogsift v2.0.0 code
2. Create `dist/404.html` with the failsafe page
3. Create `dist/robots.txt` with bot controls
4. Create `dist/sitemap.xml` with site map
5. Create placeholder assets (favicon.png, og-image.png) - note these need real designs later
6. Deploy to Cloudflare Pages via `npx wrangler pages deploy dist`

## Missing Assets Note

The manifest specifies two image assets that need to be created separately:
- `favicon.png` - 64x64px, copper geometric shape
- `og-image.png` - 1200x630px, social share card

I'll create simple placeholders so the site functions, but these should be replaced with proper designs.