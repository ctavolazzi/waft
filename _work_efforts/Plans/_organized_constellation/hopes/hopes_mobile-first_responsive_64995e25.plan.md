---
name: Mobile-First Responsive
overview: Upgrade the CSS to a mobile-first responsive design that looks great on phones, tablets, and desktops.
todos:
  - id: rewrite-css
    content: Rewrite main.css with mobile-first responsive design
    status: completed
  - id: test-mobile
    content: Test on mobile viewport sizes
    status: completed
    dependencies:
      - rewrite-css
  - id: commit-push
    content: Commit and push changes
    status: completed
    dependencies:
      - test-mobile

category: hopes
confidence: 1.00
constellation_date: 2026-01-14
---

# Mobile-First Responsive Design

## Approach

Rewrite CSS using mobile-first methodology: base styles for mobile, then use `min-width` media queries to enhance for larger screens.

## Changes to `assets/css/main.css`

**Mobile Base (default):**

- Single column layout, full width
- Larger tap targets (44px min)
- Readable font sizes (16px base)
- Stacked navigation
- Full-width images
- Comfortable padding

**Tablet (min-width: 600px):**

- Increased max-width container
- Horizontal nav links
- Slightly larger headings

**Desktop (min-width: 900px):**

- Max-width 900px centered
- More generous spacing
- Larger typography scale

## Key Improvements

| Element | Mobile | Desktop |
|---------|--------|---------|
| Nav | Stacked vertical | Horizontal inline |
| Body padding | 1rem | 2rem |
| H1 size | 1.75rem | 2.5rem |
| Images | Full bleed | Rounded corners |
| Footer | Compact | Spacious |

## Files to Modify

- [`assets/css/main.css`](assets/css/main.css) - Complete responsive rewrite