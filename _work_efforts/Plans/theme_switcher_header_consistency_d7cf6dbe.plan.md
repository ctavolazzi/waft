---
name: Theme Switcher Header Consistency
overview: ""
todos:
  - id: update-index-html
    content: Update index.html header structure and remove theme from drawer
    status: completed
  - id: update-navigation-css
    content: Adjust CSS for mobile-visible theme dropdown
    status: completed
  - id: update-wiki-templates
    content: Apply same changes to wiki-template.html and wiki-index-template.html
    status: completed
  - id: verify-themes
    content: Test all three themes on desktop and mobile viewports
    status: completed
---

# Theme Switcher Always Visible in Header

Move the theme dropdown to be always visible in the header across all viewports, removing it from the mobile drawer.

## Current State
- **Desktop**: Theme dropdown visible in header (right side)
- **Mobile**: Theme dropdown hidden in mobile drawer

## Target State
- **All viewports**: Theme dropdown always visible in header, next to hamburger menu on mobile

## Files to Modify

| File | Changes |
|------|---------|
| [`src/index.html`](src/index.html) | Move theme dropdown outside of mobile-hidden nav, remove from mobile drawer |
| [`src/css/navigation.css`](src/css/navigation.css) | Ensure dropdown visible on mobile, adjust positioning |
| [`src/wiki-template.html`](src/wiki-template.html) | Same changes for wiki pages |
| [`src/wiki-index-template.html`](src/wiki-index-template.html) | Same changes for wiki index |

## Implementation

1. **Header structure change**: Position theme dropdown after nav links but before hamburger button, or after hamburger - visible at all breakpoints

2. **CSS adjustments**: 
   - Remove `display: none` on mobile for theme dropdown
   - Add proper spacing/sizing for mobile touch targets (44px min)
   - Ensure dropdown doesn't overlap other elements

3. **Mobile drawer cleanup**:
   - Remove the "Theme" label and dropdown from mobile nav drawer
   - Simplify drawer to just navigation links

## Layout Mockup

```
Desktop:  [Logo]  [Nav Links...]  [Theme ▼]
Mobile:   [Logo]                  [Theme ▼] [☰]
```