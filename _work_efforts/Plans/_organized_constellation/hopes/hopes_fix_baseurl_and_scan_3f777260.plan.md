---
name: Fix baseurl and scan
overview: Change baseurl for GitHub Pages, create API Reference page, add navigation link, and scan for remaining issues.
todos:
  - id: fix-baseurl
    content: Update _config.yml with correct baseurl for GitHub Pages
    status: completed
  - id: create-api-page
    content: Create _wiki/api-reference.mkd with component params and CSS variables docs
    status: completed
  - id: add-nav-link
    content: Add API link to navigation in _data/navigation.yml (near CSS)
    status: completed
  - id: update-button
    content: Update component-showcase button to link to new API reference page
    status: completed
  - id: scan-wiki
    content: Scan all _wiki/*.mkd files for hardcoded paths
    status: completed
  - id: fix-issues
    content: Fix any remaining hardcoded paths found
    status: completed
  - id: commit-push
    content: Commit all changes and push to GitHub
    status: completed

category: hopes
confidence: 0.38
constellation_date: 2026-01-14
---

# Fix baseurl, Create API Reference, and Comprehensive Scan

## Problem Summary

1. Site is configured for custom domain but user wants GitHub Pages URL
2. Missing API Reference page (button at bottom of Component Library links to non-existent page)
3. No "API" link in main navigation

## Changes Required

### 1. Fix baseurl Configuration

Update `_config.yml`:

```yaml
baseurl: "/chicofablab.github.io"
url: "https://ctavolazzi.github.io"
```

### 2. Create API Reference Page

Create `_wiki/api-reference.mkd` containing:

**Component API Documentation:**

- `button.html` parameters (href, variant, size, icon, etc.)
- `card.html` parameters (title, body, image, href, badge, etc.)
- `avatar.html` parameters (src, size, initials, status, ring)
- `alert.html`, `badge.html`, `callout.html`, etc.

**CSS Variables Reference:**

- Design tokens (colors, spacing, typography)
- Component-specific CSS variables
- Theme customization options

### 3. Update Navigation

Add to `_data/navigation.yml` main section (after CSS):

```yaml
- label: API
  url: /wiki/api-reference
  icon: 📖
```

### 4. Update Component Showcase Button

Change button at bottom of `_wiki/component-showcase.mkd`:

```liquid
{% include components/button.html text="📚 Full API Reference" variant="primary" href="/wiki/api-reference" %}
```

### 5. Comprehensive Scan

Search for any remaining hardcoded paths in:

- `_wiki/*.mkd` files
- `_includes/` files
- `_layouts/` files

### 6. Commit and Deploy

- Commit all fixes
- Push to trigger GitHub Pages rebuild
- Verify at `ctavolazzi.github.io/chicofablab.github.io/`