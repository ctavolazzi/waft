---
name: Full Tech Debt Pass
overview: A comprehensive cleanup pass addressing open tech debt items, removing dead code, consolidating magic numbers, fixing inconsistencies, and improving code quality across the FogSift codebase.
todos:
  - id: remove-dead-code
    content: Remove test marker and dead code from index.html
    status: completed
  - id: fix-version
    content: Remove hardcoded version from main.js
    status: completed
  - id: magic-numbers
    content: Add TIMING constants to toast.js and modal.js
    status: completed
  - id: nav-cleanup
    content: Add comment to empty Nav.init() for clarity
    status: completed
  - id: toast-aria
    content: Fix Toast container to include ARIA attributes
    status: completed
  - id: wiki-theme-dedupe
    content: Remove duplicate theme init from wiki-template.html
    status: completed
  - id: css-cleanup
    content: Remove unused CSS variables from tokens.css
    status: completed
  - id: module-pattern
    content: Add explicit window.X exports to toast, modal, nav modules
    status: completed
  - id: update-tech-debt
    content: Update TECH_DEBT.md with completed items
    status: completed

category: dreads
confidence: 0.84
constellation_date: 2026-01-14
---

# Full Tech Debt Pass

Based on the `TECH_DEBT.md` inventory and codebase exploration, this pass addresses open items TD-015, TD-011, and general code quality improvements.

---

## 1. Remove Dead Code and Test Artifacts

**Files:** [`src/index.html`](src/index.html)

- Remove MCP test marker comment on line 2
- This is leftover from workflow testing (WE-251227-giok)

---

## 2. Fix Version Hardcoding (TD-015 related)

**Files:** [`src/js/main.js`](src/js/main.js)

- Currently `version: '0.0.5'` is hardcoded
- The build script already replaces `{{VERSION}}` in HTML
- Change `main.js` to not duplicate version, or accept it gets stale
- Simplest fix: Remove version from `main.js` since footer already shows it

---

## 3. Consolidate Magic Numbers (TD-015)

**Files:** [`src/js/toast.js`](src/js/toast.js), [`src/js/modal.js`](src/js/modal.js)

Create a timing constants pattern similar to `sleep.js`:

```javascript
// toast.js
const Toast = {
    TIMING: {
        DEFAULT_DURATION: 2500,
        ERROR_DURATION: 5000,
        FADE_DURATION: 200
    },
    // ...
};
```

---

## 4. Clean Empty/Unused Code

**Files:** [`src/js/nav.js`](src/js/nav.js)

- `Nav.init()` is empty (just a comment) - either add meaningful init or remove the method
- Since it's called from `main.js`, keep it but add a comment explaining it's a no-op placeholder

---

## 5. Fix Toast Container ARIA Attributes

**Files:** [`src/js/toast.js`](src/js/toast.js)

`getContainer()` recreates the container without ARIA attributes that exist in HTML:

```javascript
// Current: just creates div with id
// Fix: add role="status" aria-live="polite" aria-atomic="true"
```

---

## 6. Remove Duplicate Theme Init from Wiki Template

**Files:** [`src/wiki-template.html`](src/wiki-template.html)

Lines 26-32 have inline theme init, but wiki pages also load `app.js` which includes the full Theme module. The inline script is redundant since `app.js` handles theme on load.

- Remove the inline `<script>` block (lines 26-32)
- The build script's `{{THEME_INIT}}` injection handles FOUC prevention properly

---

## 7. Clean Unused CSS Variables

**Files:** [`src/css/tokens.css`](src/css/tokens.css)

Remove or comment legacy/unused variables:
- `--breadcrumb-height: 0px` (breadcrumbs removed)
- `--bar-*` variables (kept "for transition" but transition is done)

---

## 8. Gate Console.log Behind Debug Mode

**Files:** [`src/js/main.js`](src/js/main.js), [`src/js/sleep.js`](src/js/sleep.js)

The boot messages and easter egg console logs should use the Debug module:

```javascript
// Instead of: console.log('%c FOGSIFT v...')
// Use: if (Debug.enabled) console.log(...)
// Or keep branding logs as-is (they're styled, intentional)
```

Per TECH_DEBT.md: "TD-012: Console graffiti - Reviewed - only styled branding remains" - these are intentional.

**Decision:** Keep styled branding logs, but gate debug-style logs through Debug module.

---

## 9. Standardize Module Pattern

**Files:** [`src/js/toast.js`](src/js/toast.js), [`src/js/modal.js`](src/js/modal.js), [`src/js/nav.js`](src/js/nav.js)

Currently mixed patterns:
- `cache.js`, `debug.js` use IIFE with `window.X = X`
- `toast.js`, `modal.js`, `nav.js` use plain object literals (implicitly global)

Standardize to explicit global assignment for consistency:

```javascript
// At end of each module
window.Toast = Toast;
```

---

## 10. Update TECH_DEBT.md

Mark items addressed and update audit date.

---

## Summary of Changes

| File | Changes |
|------|---------|
| `src/index.html` | Remove test marker comment |
| `src/js/main.js` | Remove hardcoded version, add timing constants |
| `src/js/toast.js` | Add TIMING constants, fix ARIA attrs, add `window.Toast` |
| `src/js/modal.js` | Add TIMING constants, add `window.Modal` |
| `src/js/nav.js` | Add explanatory comment to empty init, add `window.Nav` |
| `src/wiki-template.html` | Remove duplicate inline theme init |
| `src/css/tokens.css` | Remove unused `--bar-*` and `--breadcrumb-height` variables |
| `TECH_DEBT.md` | Update status of addressed items |

---

## Out of Scope (for future work)

- TD-017/TD-020: Splitting large CSS files (significant refactor)
- TD-018: Splitting sleep.js (functional, just large)
- TD-019: Adding tests (requires test framework setup)
- TD-008: Analytics (requires service decision)
- TD-016: CI integration for ESLint