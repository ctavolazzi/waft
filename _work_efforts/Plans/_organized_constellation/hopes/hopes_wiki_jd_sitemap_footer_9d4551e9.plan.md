---
name: Wiki JD Sitemap Footer
overview: Add a Johnny Decimal sitemap component to the footer of all wiki pages, displaying the full wiki structure with auto-assigned JD numbering (10-19 Documentation, 20-29 Concepts, etc.) styled to match the 70s retro aesthetic.
todos:
  - id: add-css
    content: Add .jd-sitemap CSS styles to wiki.css with 70s retro aesthetic
    status: completed
  - id: build-function
    content: Add generateJDSitemap() function in build.js with auto-numbering logic
    status: completed
  - id: update-templates
    content: Add {{JD_SITEMAP}} placeholder to both wiki templates
    status: completed
  - id: test-build
    content: Run build and verify sitemap renders correctly
    status: completed

category: hopes
confidence: 1.00
constellation_date: 2026-01-14
---

# Johnny Decimal Sitemap Footer Component

## What We're Building
A visually distinctive footer component that displays the entire wiki structure using Johnny Decimal numbering. This will appear on both the wiki index page and all individual wiki article pages.

## Auto-Assigned JD Numbering

| Range | Category | Pages |
|-------|----------|-------|
| 10-19 | Documentation | 10.01-10.04 |
| 20-29 | Concepts | 20.01-20.06 |
| 30-39 | Frameworks | 30.01-30.04 |
| 40-49 | Field Notes | 40.01-40.07 |
| 50-59 | Case Studies | 50.01-50.03 |
| 60-69 | Tools & Techniques | 60.01-60.04 |

## Files to Modify

1. **[src/css/wiki.css](src/css/wiki.css)** - Add new `.jd-sitemap` styles matching retro aesthetic
2. **[scripts/build.js](scripts/build.js)** - Add `generateJDSitemap()` function to build the component HTML with JD numbering
3. **[src/wiki-template.html](src/wiki-template.html)** - Add `{{JD_SITEMAP}}` placeholder in footer
4. **[src/wiki-index-template.html](src/wiki-index-template.html)** - Add `{{JD_SITEMAP}}` placeholder before existing footer

## Visual Design

The sitemap will use:
- Monospace font for JD numbers (JetBrains Mono)
- Orange accent color for category ranges
- Teal links matching existing wiki style
- Card-style layout with subtle borders
- Responsive grid (2-3 columns on desktop, 1 on mobile)

```
┌─────────────────────────────────────────────────┐
│  SITEMAP                                        │
├─────────────────────────────────────────────────┤
│  10-19 DOCUMENTATION    │  20-29 CONCEPTS       │
│  → 10.01 Getting Started│  → 20.01 Root Cause   │
│  → 10.02 How We Work    │  → 20.02 Mental Models│
│  ...                    │  ...                  │
└─────────────────────────────────────────────────┘
```

## Implementation Steps

1. Add CSS styles for the JD sitemap component
2. Add `generateJDSitemap()` function in build.js that auto-assigns numbers
3. Update both wiki templates with the placeholder
4. Inject the generated sitemap during build