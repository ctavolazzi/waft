---
name: Full Code De-duplication Audit
overview: ""
todos:
  - id: js-audit
    content: Audit and document all JavaScript duplications with line numbers
    status: completed
  - id: css-audit
    content: Audit and document all CSS duplications and inconsistencies
    status: completed
  - id: wiki-js-consolidate
    content: Remove inline JS from wiki-template.html, use shared bundle
    status: completed
  - id: nav-css-dedup
    content: Remove duplicate .mobile-theme-selector in navigation.css
    status: completed
  - id: breakpoints-standardize
    content: Standardize responsive breakpoints across all CSS files
    status: completed
  - id: verify-build
    content: Run build and verify all pages work correctly
    status: completed

category: dreads
confidence: 1.00
constellation_date: 2026-01-14
---

# Full Code De-duplication Audit

## Overview
Systematic audit and consolidation of duplicate JavaScript and CSS code across the FogSift codebase. This will reduce maintenance burden, improve consistency, and decrease bundle size.

---

## JavaScript Duplications

### 1. Theme System (Critical - ~300 duplicated lines)

**Files Affected:**
- [src/js/theme.js](src/js/theme.js) - Full implementation (402 lines)
- [src/wiki-template.html](src/wiki-template.html) - Inline copy (lines 185-325)

**Duplication Details:**
| Component | theme.js | wiki-template.html |
|-----------|----------|-------------------|
| Theme object | 145 lines | 60 lines |
| ThemePicker object | 140 lines | 75 lines |
| Total | ~285 lines | ~135 lines |

**Consolidation Strategy:**
- Option A: Include `theme.js` in wiki pages via build (add to `app.js` bundle)
- Option B: Extract minimal shared theme core, inline only FOUC-prevention snippet
- Recommended: **Option A** - single source of truth, build handles wiki pages

### 2. Navigation Module (Moderate - ~15 duplicated lines)

**Files Affected:**
- [src/js/nav.js](src/js/nav.js) - Full module (38 lines)
- [src/wiki-template.html](src/wiki-template.html) - Inline copy (lines 328-343)

**Consolidation Strategy:**
- Include `nav.js` in wiki page bundle if going with Option A above

### 3. Toast System (Minor - ~10 duplicated lines)

**Files Affected:**
- [src/js/toast.js](src/js/toast.js) - Full module (85 lines)
- [src/wiki-template.html](src/wiki-template.html) - Minimal version (lines 415-425)

**Consolidation Strategy:**
- Include in shared bundle

---

## CSS Duplications

### 4. Inconsistent Responsive Breakpoints

**Files Affected:**
- [src/css/mobile.css](src/css/mobile.css) - Uses 768px, 375px, 769-1024px
- [src/css/components.css](src/css/components.css) - Uses 800px
- [src/css/base.css](src/css/base.css) - Uses 800px
- [src/css/wiki.css](src/css/wiki.css) - Uses 767px, 768px, 1023px, 1024px
- [src/css/navigation.css](src/css/navigation.css) - Uses 800px

**Consolidation Strategy:**
- Standardize on consistent breakpoints in `tokens.css`:
  - Mobile: 768px (or 767px max)
  - Tablet: 1024px (or 1023px max)
  - Desktop: 1024px+
- Update all files to use CSS custom properties for breakpoints

### 5. Duplicate `.mobile-theme-selector` Definition

**File:** [src/css/navigation.css](src/css/navigation.css)
- Lines 318-331: First definition
- Lines 420-443: Second definition (duplicate)
- Lines 471-473: `display: none` override

**Action:** Remove duplicate definition, keep single source

### 6. Similar Grid Patterns

Multiple files repeat similar grid layouts:
```css
grid-template-columns: repeat(3, 1fr);  /* desktop */
grid-template-columns: 1fr;              /* mobile */
```

**Consolidation Strategy:**
- Consider utility classes for common grid patterns
- OR keep as-is (low impact, explicit per-component)

### 7. Repeated Dark Mode Patterns

**Files:** wiki.css, navigation.css, tokens.css

Similar `[data-theme="dark"]` selector patterns for border-color adjustments.

**Consolidation Strategy:**
- Use CSS custom properties more consistently (already using `--line`)
- Ensure all components reference tokens, not hardcoded dark mode styles

---

## Execution Plan

### Phase 1: JavaScript Consolidation
1. Modify build system to include all JS modules in wiki pages
2. Remove inline JS from `wiki-template.html` (keep only FOUC-prevention)
3. Test wiki pages with shared bundle

### Phase 2: CSS Breakpoint Standardization
1. Define breakpoint variables in `tokens.css`
2. Update all CSS files to use consistent breakpoints
3. Remove duplicate `.mobile-theme-selector` in `navigation.css`

### Phase 3: Verification
1. Run build
2. Test main site and wiki pages
3. Verify theme switching, navigation, toasts work correctly

---

## Trade-offs to Consider

| Approach | Pros | Cons |
|----------|------|------|
| Shared JS bundle for wiki | Single source, smaller total size | Slightly larger initial load for wiki |
| Keep inline JS | Faster wiki page load | Maintenance burden, drift risk |

**Recommendation:** Go with shared bundle. The inline JS in wiki-template is already ~140 lines, so the overhead of including the full modules is minimal, and maintenance becomes much easier.

---

## Files to Modify

| File | Changes |
|------|---------|
| `src/wiki-template.html` | Remove inline Theme/ThemePicker/Nav/Toast, add script tag |
| `scripts/build.js` | Update to include JS in wiki pages |
| `src/css/navigation.css` | Remove duplicate `.mobile-theme-selector` (lines 420-443) |
| `src/css/tokens.css` | Add breakpoint CSS custom properties |
| `src/css/*.css` | Standardize breakpoints |