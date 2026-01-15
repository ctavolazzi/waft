---
name: Who is FogSift Section
overview: Add a "Who is FogSift" personnel section under the Intel dropdown navigation, featuring Christopher as owner with placeholder slots for future team members. Process the provided badge image to 250x250px WebP format.
todos:
  - id: create-work-effort
    content: Create work effort via MCP work-efforts server
    status: completed
  - id: process-image
    content: Convert badge image to 250x250px WebP format
    status: completed
    dependencies:
      - create-work-effort
  - id: create-images-dir
    content: Create src/images/team/ directory structure
    status: completed
    dependencies:
      - create-work-effort
  - id: add-css-styles
    content: Add team section CSS to components.css
    status: completed
    dependencies:
      - create-images-dir
  - id: add-html-section
    content: Add team section HTML and navigation links
    status: completed
    dependencies:
      - add-css-styles
      - process-image
  - id: update-work-effort
    content: Update work effort with completion status
    status: completed
    dependencies:
      - add-html-section

category: hopes
confidence: 1.00
constellation_date: 2026-01-14
---

# Who is FogSift Personnel Section

## Summary

Add a new "Who is FogSift" section featuring personnel cards with profile images. The section will be accessible via the Intel dropdown menu and showcase Christopher (Owner) plus placeholder slots for future team members.

## Image Processing

- Convert the provided circular badge image to **250x250px WebP format**
- Save to `src/images/team/christopher-badge.webp`
- Create `src/images/team/` directory structure for future personnel images

## HTML Changes - [src/index.html](src/index.html)

1. **Add navigation link** in Intel dropdown (line ~103-106):

```html
<a href="#team" class="dropdown-link">The Team <span>Who is FogSift</span></a>
```

2. **Add mobile drawer link** (around line 82)
3. **Add new section** after the Secure Assets section (~line 330), including:
   - Section with `id="team"` and `data-crumb="INTEL / TEAM"`
   - Personnel grid with profile cards
   - Christopher card with image, name, role, and brief bio
   - 2 placeholder cards for future team members

## CSS Changes - [src/css/components.css](src/css/components.css)

Add new styles for the team section:
- `.team-grid` - responsive grid layout for personnel cards
- `.team-card` - individual card styling (consistent with site aesthetic)
- `.team-avatar` - circular profile image container (250px max, responsive)
- `.team-name`, `.team-role`, `.team-bio` - typography styles

## Work Effort & Documentation

Using MCP work-efforts server:
- Create work effort `00.05_who-is-fogsift-section.md` in `_work_efforts_/00-09_site_improvements/00_ui_ux/`
- Update the index file with link to new work effort
- Document progress and completion

## Implementation Order

1. Create work effort via MCP
2. Process and save image (250x250px WebP)
3. Create `src/images/team/` directory
4. Add CSS styles for team section
5. Add HTML section and navigation updates
6. Update work effort with completion status

## Design Notes

- Team cards will follow the existing brutalist/industrial aesthetic with:
  - Hard shadows (`var(--shadow-hard)`)
  - Monospace labels (`var(--font-mono)`)
  - Copper/electric accent colors
  - Border styling consistent with `.theatre-card`
- Placeholder cards will have a dashed border and muted styling to indicate "coming soon"