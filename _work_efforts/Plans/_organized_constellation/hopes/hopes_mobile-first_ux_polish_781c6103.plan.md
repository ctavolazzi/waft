---
name: Mobile-First UX Polish
overview: Polish the mobile experience with touch-optimized targets, improved spacing, brand color consistency, and WCAG-compliant accessibility for colorblind users.
todos:
  - id: mobile-touch
    content: Implement 44px minimum touch targets for all interactive elements
    status: completed
  - id: mobile-spacing
    content: Optimize mobile spacing - remove label tilt, tighten margins
    status: completed
  - id: mobile-layout
    content: Fix mobile layouts - stack IO boxes, improve footer
    status: completed
  - id: color-cohesion
    content: Standardize brand colors - CTA orange, interactive teal, highlight gold
    status: completed
  - id: a11y-contrast
    content: Fix contrast ratios - muted text needs darker shade
    status: completed
  - id: a11y-focus
    content: Add focus-visible outlines and ARIA labels
    status: in_progress
  - id: a11y-colorblind
    content: Add non-color indicators for status (icons, patterns)
    status: pending
  - id: test-mobile
    content: Test on multiple mobile viewports and dark mode
    status: pending

category: hopes
confidence: 0.62
constellation_date: 2026-01-14
---

# Mobile-First UX Polish

## Priority Order
1. Mobile design optimization
2. Responsiveness improvements
3. Brand color cohesion
4. Accessibility (colorblind support)

---

## Issues Identified

### Mobile (Priority 1)
| Issue | Location | Fix |
|-------|----------|-----|
| Touch targets too small | Menu button, theme toggle, checkboxes | Min 44x44px tap areas |
| Label tilt looks awkward | All `.label` elements | Remove rotation on mobile |
| Excessive section spacing | Between sections | Tighter mobile-specific margins |
| Breadcrumb text too small | `.breadcrumb-bar` | Larger touch-friendly text |
| CTA button padding | `.hotline-button` | More vertical padding on mobile |

### Responsiveness (Priority 2)
| Issue | Location | Fix |
|-------|----------|-----|
| IO boxes cramped | `.io-box` | Stack vertically on mobile |
| Pricing cards | `.pricing-cards` | Better card spacing |
| Footer columns | `.footer-grid` | Stack cleanly on mobile |

### Brand Color Cohesion (Priority 3)
| Issue | Fix |
|-------|-----|
| Inconsistent accent usage | Standardize teal for interactive, orange for CTAs |
| Shadow colors vary | Use consistent shadow palette |
| Hover states inconsistent | Unified hover treatment |

### Accessibility - Colorblind (Priority 4)
| Issue | Fix |
|-------|-----|
| Orange/green distinction | Add secondary indicators (icons, patterns) |
| Contrast ratios | Ensure 4.5:1 minimum for all text |
| Focus indicators | High-contrast focus rings |
| Status indicators | Never rely on color alone |

---

## Implementation Plan

### Phase 1: Mobile Touch Optimization
**File:** [src/css/components.css](src/css/components.css)

```css
/* Minimum touch targets */
.theme-toggle, .mobile-toggle, .check-item { min-height: 44px; min-width: 44px; }

/* Remove label tilt on mobile */
@media (max-width: 800px) { .label { transform: none; } }

/* Larger mobile CTA */
@media (max-width: 800px) { .hotline-button { padding: 1.25rem 1.5rem; } }
```

### Phase 2: Mobile Spacing and Layout
**File:** [src/css/base.css](src/css/base.css)

- Reduce section margins on mobile
- Stack IO boxes vertically
- Improve footer layout

### Phase 3: Brand Color Consistency
**File:** [src/css/tokens.css](src/css/tokens.css)

- Define clear color roles (CTA = orange, interactive = teal, highlight = gold)
- Consistent shadow colors
- Standardized hover states

### Phase 4: Accessibility Enhancements
**Files:** [src/css/components.css](src/css/components.css), [src/index.html](src/index.html)

- Add focus-visible outlines with 3px offset
- Add aria-labels to interactive elements
- Ensure price tags have icons not just color
- Add checkmark icon to checked items (not just color change)

---

## WCAG Contrast Check

| Element | Current | Required | Status |
|---------|---------|----------|--------|
| Body text (#71717a on #fafafa) | 5.1:1 | 4.5:1 | PASS |
| Muted text (#a1a1aa on #fafafa) | 3.0:1 | 4.5:1 | FAIL - needs fix |
| Orange CTA (#c2410c on #fff) | 5.4:1 | 3:1 | PASS |
| Teal accent (#0d9488 on #fff) | 3.9:1 | 3:1 | PASS |

---

## Files to Modify

| File | Changes |
|------|---------|
| [src/css/tokens.css](src/css/tokens.css) | Color role definitions, fix muted contrast |
| [src/css/base.css](src/css/base.css) | Mobile spacing, focus styles |
| [src/css/components.css](src/css/components.css) | Touch targets, mobile layouts, hover states |
| [src/index.html](src/index.html) | ARIA labels, semantic improvements |

---

## Estimated Time
| Phase | Time |
|-------|------|
| Mobile touch optimization | 20 min |
| Mobile spacing/layout | 25 min |
| Brand color consistency | 15 min |
| Accessibility | 30 min |
| Testing | 20 min |
| **Total** | **~2 hrs** |