---
name: CSS Overflow Investigation
overview: Investigate and fix CSS overflow issues caused by conflicting dual CSS systems (legacy styles.css and V3 modular CSS) that result in elements appearing outside their container bounds.
todos:
  - id: audit-selectors
    content: Audit conflicting CSS selectors between styles.css and V3 CSS
    status: pending
  - id: fix-stats-grid
    content: Fix stats-section grid overflow with proper minmax constraints
    status: pending
  - id: fix-buttons
    content: Add max-width and overflow control to test/demo buttons
    status: pending
  - id: fix-stat-values
    content: Add responsive font-size and overflow handling to stat values
    status: pending
  - id: fix-queue-indicators
    content: Fix queue indicator box-shadow overflow with padding or reduced spread
    status: pending
  - id: add-overflow-control
    content: Add overflow:hidden and min-width:0 to containers throughout
    status: pending
  - id: migrate-legacy
    content: Migrate conflicting legacy CSS sections to V3 component files
    status: pending

category: dreads
confidence: 0.82
constellation_date: 2026-01-14
---

# CSS Overflow Issues Investigation Plan

## Problem Summary

Elements are overflowing their containers on the dashboard:
- Test System and Live Demo buttons outside their stat-card bounds
- Stat numbers outside card bounds
- Queue indicator lights outside queue-item bounds

## Root Cause Analysis

The dashboard has a **dual CSS system conflict**:

1. **Legacy [`styles.css`](mcp-servers/dashboard-v3/public/styles.css)** (5,045 lines) - loaded first
2. **V3 Modular CSS** ([`main.css`](mcp-servers/dashboard-v3/public/styles/main.css) + components) - loaded second to override

Both systems define the same classes with conflicting properties. The cascade order and specificity battles are causing unpredictable results.

---

## Specific Issues Identified

### 1. Stats Section Grid Overflow

**Legacy CSS (lines 1175-1180):**
```css
.stats-section {
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}
```
The `minmax(200px, 1fr)` creates a 200px minimum width per cell. When the container is narrower, cards overflow horizontally.

**V3 CSS ([cards.css](mcp-servers/dashboard-v3/public/styles/components/cards.css) lines 136-181):**
Uses fixed column counts per breakpoint, but legacy rules may override due to specificity/order.

---

### 2. Test/Demo Button Overflow

**Legacy CSS (lines 3505-3518, 3698-3727):**
```css
.test-btn, .demo-btn {
  padding: var(--space-md) var(--space-lg);  /* ~14px ~20px */
}
```
These buttons have no `max-width` constraint. Combined with the `minmax(200px)` grid, buttons can exceed their parent `.stat-card` container.

**Missing from both systems:**
- `max-width: 100%` on buttons
- `overflow: hidden` on `.stat-card.test-card` and `.stat-card.demo-card`

---

### 3. Stat Value (Numbers) Overflow

**Legacy CSS (lines 1230-1236):**
```css
.stat-value {
  font-size: 2rem;
  font-weight: 700;
  line-height: 1;
}
```
No overflow control. Large numbers (e.g., triple digits) can exceed container width.

**Fix needed:**
- Add `overflow: hidden; text-overflow: ellipsis;` or `font-size: clamp()` for responsive sizing

---

### 4. Queue Indicator Lights Overflow

**Legacy CSS (lines 1352-1364):**
```css
.queue-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}
.queue-indicator.active {
  box-shadow: 0 0 8px var(--status-active);
}
.queue-indicator.in_progress {
  animation: indicatorPulse 1.5s infinite;
}
```
The `box-shadow` (8-12px spread) extends visually beyond the element bounds. The animation can cause visual jitter.

**Fix options:**
- Add `overflow: visible` on parent with proper padding
- OR reduce shadow spread radius
- OR use `filter: drop-shadow()` instead

---

## Architectural Issues

### CSS Loading Order (from [index.html](mcp-servers/dashboard-v3/public/index.html) lines 14-19):
```html
<!-- Legacy styles (loaded first, will be gradually removed) -->
<link rel="stylesheet" href="styles.css">
<!-- V3 Modular CSS (loaded last to override legacy) -->
<link rel="stylesheet" href="styles/main.css">
```

This creates:
1. **Specificity battles** - Same selectors in both files
2. **Unpredictable inheritance** - Some legacy rules win, some V3 rules win
3. **Container queries not working** - Legacy layout breaks V3 container query assumptions

---

## Investigation Steps

### Phase 1: Audit Conflicting Selectors
1. List all selectors that appear in both `styles.css` and V3 CSS
2. Compare specificity and identify which rules win
3. Document which legacy rules need `!important` overrides or deletion

### Phase 2: Fix Immediate Overflow Issues
1. **Stats grid**: Override legacy `minmax(200px)` with `minmax(min(100%, 150px), 1fr)`
2. **Buttons**: Add `max-width: 100%; box-sizing: border-box;` to `.test-btn`, `.demo-btn`
3. **Stat values**: Add responsive `font-size: clamp(1rem, 4vw, 2rem)`
4. **Queue indicators**: Add padding to parent or reduce `box-shadow` spread

### Phase 3: Structural Cleanup
1. Move critical legacy styles to V3 component files
2. Add `overflow: hidden` to card containers
3. Add `min-width: 0` to flex children throughout
4. Ensure all containers have explicit `max-width: 100%`

---

## Recommended Fix Strategy

**Option A: Surgical Override (Quick Fix)**
Add a new CSS file `styles/overrides.css` loaded last with high-specificity fixes:
```css
.stats-section.stats-section {
  grid-template-columns: repeat(2, 1fr);
  overflow: hidden;
}
@media (min-width: 640px) {
  .stats-section.stats-section {
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 140px), 1fr));
  }
}
```

**Option B: Legacy Removal (Recommended)**
Systematically remove conflicting sections from `styles.css` as they are migrated to V3 components, starting with:
1. Stats section (lines 1171-1244)
2. Queue item (lines 1321-1440)
3. Test/Demo buttons (lines 3484-3916)

---

## Files to Modify

| File | Action |
|------|--------|
| [`styles.css`](mcp-servers/dashboard-v3/public/styles.css) | Remove duplicate selectors after migration |
| [`cards.css`](mcp-servers/dashboard-v3/public/styles/components/cards.css) | Add overflow control, fix grid |
| [`layout.css`](mcp-servers/dashboard-v3/public/styles/layout.css) | Ensure `min-width: 0` on flex children |
| [`main.css`](mcp-servers/dashboard-v3/public/styles/main.css) | Add missing overflow handling |
