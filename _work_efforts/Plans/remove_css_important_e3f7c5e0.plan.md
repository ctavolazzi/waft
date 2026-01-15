---
name: Remove CSS Important
overview: Remove all 41 `!important` declarations from main.css by fixing the underlying specificity issues through proper CSS cascade restructuring.
todos:
  - id: progress-demo
    content: Remove 14 !important from progress bar demo animation (lines 1045-1101)
    status: pending
  - id: toggle-display
    content: Remove 1 !important from toggle display property (line 1870)
    status: pending
  - id: toggle-before
    content: Remove 2 !important from toggle ::before and consolidate with line 404 rules
    status: pending
  - id: toggle-track
    content: Remove 6 !important from toggle track sizes (lines 1911-1925)
    status: pending
  - id: toggle-thumb-where
    content: Add :where() wrapper for thumb base positioning (lines 1927-1935)
    status: pending
  - id: toggle-thumb-sizes
    content: Remove 10 !important from toggle thumb sizes (lines 1937-1958)
    status: pending
  - id: toggle-checked
    content: Remove 3 !important from toggle checked transform (lines 1967-1978)
    status: pending
  - id: settings-hidden
    content: Remove 2 !important from settings hidden state using double-class selector
    status: pending
  - id: verify
    content: Verify all 41 !important removed and components still work
    status: pending
---

# Remove All !important Declarations from CSS

## Problem Analysis

Found **41 `!important` declarations** in [`assets/css/main.css`](assets/css/main.css), grouped into 3 categories:

| Category | Count | Lines | Root Cause |

|----------|-------|-------|------------|

| Progress bar demo animation | 14 | 1047-1098 | Unnecessary - demo mode already omits inline widths |

| Toggle component | 24 | 1870-1977 | Base thumb positioning and pseudo-element conflicts |

| Settings panel hidden | 2 | 4990, 5086 | Ensuring `[hidden]` overrides display rules |

---

## Fix 1: Progress Bar Demo Animation (14 removals)

**Current code (lines 1045-1098):**

```css
.cfl-progress--demo .cfl-progress__bar {
    width: 0% !important;
    animation: progress-fill-cycle 4s ... infinite !important;
}
@keyframes progress-fill-cycle {
    0% { width: 0% !important; }
    /* ... 9 more keyframe steps with !important */
}
```

**Solution:** Simply remove `!important` - the demo component template already renders bars WITHOUT inline `width` styles:

```14:15:_includes/components/progress.html
    {% if demo %}
    <div class="cfl-progress__bar cfl-progress__bar--{{ variant }}..."></div>
```

No inline style means no specificity battle. Keyframes never need `!important`.

---

## Fix 2: Toggle Component (24 removals)

### 2a. Display flex (line 1870)

**Current:**

```css
label.cfl-toggle, .cfl-toggle {
    display: inline-flex !important;
}
```

**Solution:** Remove `!important`. The selector `label.cfl-toggle` (specificity 0,1,1) is already specific enough. No competing rules set a different `display` value.

---

### 2b. ::before removal (lines 1883-1884)

**Current:**

```css
label.cfl-toggle::before, .cfl-toggle::before {
    content: none !important;
    display: none !important;
}
```

**Root cause:** Global `li` styling at line 410 and markdown rendering can add list markers.

**Solution:** Consolidate with existing `main` scoped rules at lines 404-408:

```css
/* Already exists at line 404 - just ensure it's the authoritative rule */
main label.cfl-toggle::before,
main .cfl-toggle::before,
label.cfl-toggle::before,
.cfl-toggle::before {
    content: none;
    display: none;
}
```

Remove duplicate rules with `!important` since list-style-type doesn't apply to non-list elements anyway.

---

### 2c. Track sizes (lines 1911-1925) - 6 removals

**Current:**

```css
.cfl-toggle--sm .cfl-toggle__track { width: 28px !important; height: 16px !important; }
.cfl-toggle--md .cfl-toggle__track { width: 48px !important; height: 26px !important; }
.cfl-toggle--lg .cfl-toggle__track { width: 72px !important; height: 38px !important; }
```

**Solution:** Remove `!important`. The base `.cfl-toggle__track` (line 1899) sets no width/height - only relative properties. These are the ONLY rules defining track dimensions.

---

### 2d. Thumb sizes and positions (lines 1937-1958) - 10 removals

**Current:**

```css
.cfl-toggle--sm .cfl-toggle__thumb { width: 12px !important; height: 12px !important; top: 2px !important; left: 2px !important; }
/* Similar for --md and --lg */
```

**Root cause:** Base `.cfl-toggle__thumb` at line 1928-1930 sets `top: 3px; left: 3px`.

**Solution:** Wrap base positioning in `:where()` to lower its specificity:

```css
.cfl-toggle__thumb {
    position: absolute;
    background-color: #fff;
    border-radius: 50%;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2), 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* Use :where() for default positioning - zero specificity */
:where(.cfl-toggle__thumb) {
    top: 3px;
    left: 3px;
}
```

Then variant selectors naturally override without `!important`.

---

### 2e. Checked transform (lines 1967-1978) - 3 removals

**Current:**

```css
.cfl-toggle--sm .cfl-toggle__input:checked + .cfl-toggle__track .cfl-toggle__thumb {
    transform: translateX(12px) !important;
}
```

**Solution:** Remove `!important`. These selectors are unique - nothing else sets transform on checked state.

---

## Fix 3: Settings Panel Hidden (2 removals)

**Current (lines 4989-4991, 5085-5087):**

```css
.cfl-settings__scrim[hidden] { display: none !important; }
.cfl-settings__panel[hidden] { display: none !important; }
```

**Solution:** Use repeated class selector for higher specificity without `!important`:

```css
.cfl-settings__scrim.cfl-settings__scrim[hidden] { display: none; }
.cfl-settings__panel.cfl-settings__panel[hidden] { display: none; }
```

This creates specificity 0,3,0 vs the base 0,1,0 rules.

---

## Summary of Changes

```
 assets/css/main.css
 ├── Lines 1045-1101: Remove 14 !important from progress demo
 ├── Line 1870: Remove 1 !important from toggle display
 ├── Lines 1881-1885: Remove 2 !important from toggle ::before (consolidate with line 404)
 ├── Lines 1911-1925: Remove 6 !important from toggle track sizes
 ├── Lines 1927-1935: Add :where() wrapper for thumb defaults
 ├── Lines 1937-1958: Remove 10 !important from toggle thumb sizes
 ├── Lines 1967-1978: Remove 3 !important from toggle checked transform
 └── Lines 4989-5087: Remove 2 !important from settings hidden (add double-class)
```

## Testing Checklist

After changes, verify these still work correctly:

1. Progress bars with `demo=true` animate correctly
2. Progress bars with inline widths display correctly
3. Toggle components in all sizes (sm/md/lg) render correctly
4. Toggle checked/unchecked states transition smoothly
5. Toggles inside markdown lists don't show bullets
6. Settings panel shows/hides properly with `[hidden]` attribute