---
name: Clean Code Audit
overview: Comprehensive audit of the howtowincapitalism codebase against Codacy's 9 clean code principles, identifying violations across hard-coded values, DRY, and code organization.
todos:
  - id: fix-base-tokens
    content: Remove duplicate design token definitions from Base.astro - import custom.css instead
    status: pending
  - id: fix-aside-colors
    content: Replace inline color objects in Aside.astro with CSS classes using design tokens
    status: pending
  - id: fix-tabs-colors
    content: "Replace hard-coded colors (#ccc, #f8f9fa, #eee) in Tabs.astro with CSS variables"
    status: pending
  - id: fix-steps-color
    content: "Replace #0645ad in Steps.astro with var(--color-link)"
    status: pending
  - id: fix-collapsible-color
    content: "Replace #fef0cc in Collapsible.astro with CSS variable"
    status: pending
  - id: fix-index-color
    content: "Replace #666 in index.astro with var(--color-text-muted)"
    status: pending
  - id: add-dm-constants
    content: Add named constants for magic numbers in decision-matrix.ts (thresholds, multipliers)
    status: pending
  - id: create-storage-helper
    content: Create src/lib/storage.ts to extract shared localStorage pattern from Favorites and CompletenessMeter
    status: pending

category: dreads
confidence: 0.82
constellation_date: 2026-01-14
---

# Clean Code Audit - How To Win Capitalism

## Overall Assessment: B-

Your codebase has good architecture (atomic design) and TypeScript practices, but suffers from **inconsistent design token usage** and **duplicated patterns**.

---

## Principle 1: Avoid Hard-Coded Numbers

### CRITICAL: Duplicated Design System in Base.astro

`src/layouts/Base.astro` re-defines the entire design token system that already exists in `src/styles/custom.css`:

```162:213:src/layouts/Base.astro
<style is:global>
  :root {
    /* Colors */
    --color-bg: #ffffff;
    --color-text: #202122;
    --color-text-muted: #666;
    ...
  }
```

This duplicates `custom.css` lines 6-68 and creates **maintenance risk** - tokens can diverge.

**Fix:** Import or reference `custom.css` instead of re-declaring tokens.

---

### CRITICAL: Inline Hard-Coded Colors

**src/components/simple/Aside.astro** - Uses inline styles with hard-coded colors:

```12:22:src/components/simple/Aside.astro
const colors = {
  note: { bg: '#eaf3ff', border: '#36c', icon: 'ℹ️' },
  tip: { bg: '#e6f6e6', border: '#2a2', icon: '💡' },
  caution: { bg: '#fef6e7', border: '#fc3', icon: '⚠️' },
  danger: { bg: '#ffebec', border: '#c00', icon: '🚨' },
};
...
<aside style={`background: ${style.bg}; border-color: ${style.border};`}>
```

**Fix:** Use CSS classes with CSS variables instead of inline styles.

---

**src/components/simple/Tabs.astro** - Hard-coded colors:

```11:35:src/components/simple/Tabs.astro
.tabs {
  border: 1px solid #ccc;
  ...
}
.tabs :global(summary) {
  background: #f8f9fa;
}
.tabs :global(summary:hover) {
  background: #eee;
}
```

**Fix:** Replace `#ccc`, `#f8f9fa`, `#eee` with `var(--color-border)`, `var(--color-surface)`, etc.

---

**src/components/simple/Steps.astro** - Hard-coded color:

```35:src/components/simple/Steps.astro
background: #0645ad;
```

**Fix:** Use `var(--color-link)`.

---

**src/components/atoms/Collapsible.astro** - One outlier:

```154:src/components/atoms/Collapsible.astro
background: #fef0cc;
```

**Fix:** Add `--color-warning-bg-hover` to custom.css or use existing token.

---

**src/pages/index.astro** - Hard-coded color:

```43:src/pages/index.astro
color: #666;
```

**Fix:** Use `var(--color-text-muted)`.

---

### MEDIUM: Magic Numbers in decision-matrix.ts

```743:src/lib/tools/decision-matrix.ts
if (winnerScore > runnerUpScore * 1.1) {  // 10% better
```
```788:794:src/lib/tools/decision-matrix.ts
const normalizedConf = Math.min(100, normalizedGap * 2.5);
return (relativeConf * 0.4) + (normalizedConf * 0.6);
...
return Math.min(100, relativeConf * 1.5);
```
```807:813:src/lib/tools/decision-matrix.ts
if (confidence > 55) {
  ...
} else if (confidence > 30) {
```

**Fix:** Add named constants at top of file:

```typescript
const ADVANTAGE_THRESHOLD = 1.1;  // 10% better
const CONFIDENCE_HIGH = 55;
const CONFIDENCE_MODERATE = 30;
const NORMALIZED_MULTIPLIER = 2.5;
const RELATIVE_WEIGHT = 0.4;
const NORMALIZED_WEIGHT = 0.6;
```

---

## Principle 5: DRY (Don't Repeat Yourself)

### CRITICAL: Duplicated localStorage Pattern

Both `Favorites.astro` and `CompletenessMeter.astro` implement identical patterns:

```168:176:src/components/molecules/Favorites.astro
const DEBUG = import.meta.env?.DEV || localStorage.getItem('debug') === 'true';
const log = DEBUG
  ? (...args: unknown[]) => console.log('🔍 [favorites]', ...args)
  : () => {};
const STORAGE_KEY = 'htwc-favorites';
```
```224:232:src/components/molecules/CompletenessMeter.astro
const DEBUG = import.meta.env?.DEV || localStorage.getItem('debug') === 'true';
const log = DEBUG
  ? (...args) => console.log('🔍 [completeness-meter]', ...args)
  : () => {};
const STORAGE_KEY = 'htwc-visited-pages';
```

**Fix:** Create `src/lib/storage.ts`:

```typescript
export function createStorageHelper<T>(key: string, moduleName: string) {
  const DEBUG = import.meta.env?.DEV;
  const log = DEBUG ? (...args) => console.log(`🔍 [${moduleName}]`, ...args) : () => {};
  
  return {
    get: (): T[] => { ... },
    set: (data: T[]): void => { ... },
    log,
  };
}
```

---

## What You're Doing Well

| Principle | Grade | Notes |

|-----------|-------|-------|

| 2. Meaningful Names | A | `calculateStrengthsWeaknesses`, `sanitizeUrl`, clear interfaces |

| 3. Comments | A | JSDoc on modules, explains "why" not "what" |

| 4. Short Functions (SRP) | B+ | Most functions focused; some analysis methods could be smaller |

| 6. Code Standards | A | Consistent TypeScript, proper naming conventions |

| 7. Encapsulate Conditionals | A | No deeply nested logic |

| 8. Refactor Continuously | B+ | Component registry shows active management |

| 9. Version Control | A | Git with proper .gitignore |

---

## Files with No Violations

These components properly use CSS variables throughout:

- `src/components/molecules/DecisionMatrix.astro`
- `src/components/molecules/SeeAlso.astro`
- `src/components/atoms/WikiBox.astro`
- `src/components/organisms/Footer.astro`
- `src/lib/debug.ts`
- `src/lib/constants.ts`

---

## Priority Fix List

| Priority | File | Issue | Effort |

|----------|------|-------|--------|

| 1 | Base.astro | Remove duplicate design tokens | Medium |

| 2 | Aside.astro | Replace inline color objects with CSS classes | Low |

| 3 | Tabs.astro | Replace hard-coded colors | Low |

| 4 | Steps.astro | Replace #0645ad with var | Trivial |

| 5 | Collapsible.astro | Replace #fef0cc with var | Trivial |

| 6 | index.astro | Replace #666 with var | Trivial |

| 7 | decision-matrix.ts | Add named constants for magic numbers | Low |

| 8 | Create storage.ts | Extract shared localStorage helper | Medium |