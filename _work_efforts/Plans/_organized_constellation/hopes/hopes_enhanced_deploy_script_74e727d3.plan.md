---
name: Enhanced Deploy Script
overview: Create a comprehensive deploy script with pre-flight checks, file tree visualization, bundle size reporting, and deployment manifest generation before pushing to Cloudflare Pages.
todos:
  - id: commit-changes
    content: Stage and commit current changes, push to origin
    status: completed
  - id: create-deploy-script
    content: Create scripts/deploy.js with pre-flight checks, file tree, bundle report, manifest
    status: completed
    dependencies:
      - commit-changes
  - id: update-package-json
    content: Add quick-deploy and deploy:dry npm scripts
    status: completed
    dependencies:
      - create-deploy-script
  - id: run-deployment
    content: Execute deploy script to push to Cloudflare Pages
    status: completed
    dependencies:
      - update-package-json

category: hopes
confidence: 1.00
constellation_date: 2026-01-14
---

# Enhanced Quick Deploy Script

## Current State

- Uncommitted changes need to be committed first
- Existing deployment: `npm run deploy` via wrangler

## Plan

### Step 1: Commit Current Changes

```bash
git add -A
git commit -m "chore: update work efforts and team badge"
git push origin main
```



### Step 2: Create Enhanced Deploy Script

Create [`scripts/deploy.js`](scripts/deploy.js) with these features:**Pre-Flight Checks:**

1. Clean git working tree (fail if uncommitted changes)
2. Verify on `main` branch
3. Version bump warning (compare to last deploy)

**Build and Verify:**

4. Run build.js
5. Verify critical files exist:

- `dist/index.html`
- `dist/styles.css`
- `dist/app.js`
- `dist/favicon.png`
- `dist/manifest.json`

**Reporting (before deploy):**

6. **File Tree Map** - Print visual tree of `dist/` directory
7. **Bundle Size Report** - Show sizes of CSS, JS, HTML with color-coded warnings
8. **Deployment Summary** - Version, file count, total size

**Deployment:**

9. Support `--dry-run` flag to preview without deploying
10. Run `wrangler pages deploy dist`
11. **Generate Deployment Manifest** - Save `dist/.deploy-manifest.json` with:

    - Timestamp
    - Version
    - Git commit hash
    - File checksums
    - Bundle sizes

### Step 3: Update package.json

```json
"scripts": {
  "quick-deploy": "node scripts/deploy.js",
  "deploy:dry": "node scripts/deploy.js --dry-run"
}
```



### Step 4: Deploy

## Script Output Preview

```javascript
╔═══════════════════════════════════════════════════════════╗
║  FOGSIFT DEPLOY v0.0.1                                    ║
╚═══════════════════════════════════════════════════════════╝

✓ Pre-flight checks
  • Git working tree clean
  • On branch: main
  • Version: 0.0.1

✓ Build complete

📁 Deployment Tree (dist/)
├── index.html
├── styles.css
├── app.js
├── 404.html
├── assets/
│   ├── icon-512.png
│   ├── logo.png
│   └── logo-mono.png
├── content/
│   └── articles.json
└── images/
    └── team/
        └── christopher-badge.webp

📊 Bundle Report
  HTML:  index.html     12.4 KB
  CSS:   styles.css      8.2 KB
  JS:    app.js          6.1 KB
  ─────────────────────────────
  Total: 14 files       156.8 KB

🚀 Deploying to Cloudflare Pages...
✨ Deployed! https://fogsift.pages.dev
```



## Files Changed

- Create: `scripts/deploy.js` (~180 lines)