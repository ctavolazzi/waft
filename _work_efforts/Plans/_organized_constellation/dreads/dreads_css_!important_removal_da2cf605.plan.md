---
name: CSS !important Removal
overview: Refactor FogSift CSS to eliminate all 55 instances of `!important` across 5 files by using proper CSS specificity, cascade layers, and selector architecture.
todos:
  - id: wiki-active-nav
    content: Fix wiki.css .wiki-nav-active specificity (1 instance)
    status: completed
  - id: honeypot-field
    content: Refactor components.css honeypot field selectors (10 instances)
    status: completed
  - id: industrial-theme
    content: Fix industrial-theme.css rotating-highlight reset (7 instances)
    status: completed
  - id: sleep-animations
    content: Refactor sleep.css animation state selectors (25 instances)
    status: completed
  - id: print-styles
    content: Fix base.css print stylesheet specificity (12 instances)
    status: completed
  - id: verify-removal
    content: Verify zero !important declarations remain
    status: completed

category: dreads
confidence: 0.71
constellation_date: 2026-01-14
---

# CSS !important Elimination Plan

## Current State

**55 total `!important` declarations** across 5 CSS files:

| File | Count | Purpose |
|------|-------|---------|
| [sleep.css](src/css/sleep.css) | 25 | Animation state overrides |
| [base.css](src/css/base.css) | 12 | Print stylesheet |
| [components.css](src/css/components.css) | 10 | Honeypot anti-bot field |
| [industrial-theme.css](src/css/industrial-theme.css) | 7 | Theme reset for rotating highlight |
| [wiki.css](src/css/wiki.css) | 1 | Active nav link color |

## Root Cause Analysis

The `!important` declarations exist because:

1. **Print styles** - Need to override all screen styles
2. **Security (honeypot)** - Must ensure field stays hidden from bots
3. **Dynamic state classes** - JS adds `.sleepy-breathing`, `.startled` that must override existing animations
4. **Theme overrides** - Industrial theme needs to "reset" styles applied earlier in cascade
5. **Specificity conflicts** - Active nav link competing with other nav styles

## Solution Strategy

Use a **specificity hierarchy** and **CSS load order** to naturally override without `!important`.

```
┌─────────────────────────────────────────────────┐
│         CSS SPECIFICITY HIERARCHY               │
├─────────────────────────────────────────────────┤
│  Layer 1: Tokens + Reset        (0,0,1)        │
│  Layer 2: Base components       (0,1,0)        │
│  Layer 3: Theme overrides       (0,2,0+)       │
│  Layer 4: State classes         (0,2,1+)       │
│  Layer 5: Print/A11y            (0,3,0+)       │
└─────────────────────────────────────────────────┘
```

---

## File-by-File Changes

### 1. [base.css](src/css/base.css) - Print Styles (12 instances)

**Problem:** Print styles use `!important` to override screen styles.

**Solution:** Increase specificity with `html` prefix:

```css
/* BEFORE */
@media print {
    body {
        background: #fff !important;
    }
}

/* AFTER */
@media print {
    html body {
        background: #fff;
    }
    html .frame {
        box-shadow: none;
        /* ... */
    }
}
```

### 2. [components.css](src/css/components.css) - Honeypot (10 instances)

**Problem:** Security-critical field must stay hidden.

**Solution:** Use attribute selector + class for bulletproof specificity:

```css
/* BEFORE */
.hp-field {
    position: absolute !important;
    left: -9999px !important;
}

/* AFTER - Specificity: (0,2,0) */
.hp-field[aria-hidden="true"],
input.hp-field,
label.hp-field {
    position: absolute;
    left: -9999px;
    /* ... all properties without !important */
}
```

### 3. [industrial-theme.css](src/css/industrial-theme.css) - Theme Reset (7 instances)

**Problem:** Theme selector `[data-theme="industrial-punchcard"]` needs to override base component styles.

**Solution:** Add parent context selectors:

```css
/* BEFORE */
[data-theme="industrial-punchcard"] .rotating-highlight [data-words] {
    color: var(--primary) !important;
    background: transparent !important;
}

/* AFTER - Specificity: (0,3,0) */
[data-theme="industrial-punchcard"] .hero-badge .rotating-highlight,
[data-theme="industrial-punchcard"] .rotating-highlight [data-words],
[data-theme="industrial-punchcard"] .section-hero [data-words] {
    color: var(--primary);
    background: transparent;
    border: none;
    padding: 0;
    box-shadow: none;
    border-radius: 0;
}
```

### 4. [sleep.css](src/css/sleep.css) - Animation States (25 instances)

**Problem:** Dynamic JS classes must override existing animations.

**Solution:** Use `body.page-sleeping` parent selector for state scoping:

```css
/* BEFORE */
.sleepy-breathing {
    animation: breathe 3s ease-in-out infinite !important;
}

/* AFTER - Specificity: (0,2,0) */
body.page-sleeping .sleepy-breathing,
.sleepy.sleepy-breathing {
    animation: breathe 3s ease-in-out infinite;
}

/* For startled - waking state */
body.page-waking .startled,
.sleepy.startled {
    animation: startledJump 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
}
```

For reduced motion accessibility, use higher specificity:

```css
/* BEFORE */
@media (prefers-reduced-motion: reduce) {
    .sleepy-breathing {
        animation: none !important;
    }
}

/* AFTER */
@media (prefers-reduced-motion: reduce) {
    html body .sleepy-breathing,
    html body .startled,
    html body .sleep-z {
        animation: none;
        transition: none;
    }
}
```

### 5. [wiki.css](src/css/wiki.css) - Active Nav (1 instance)

**Problem:** Active nav link color competing with base nav link styles.

**Solution:** Add element selector for specificity:

```css
/* BEFORE */
.wiki-nav-active {
    color: var(--burnt-orange) !important;
}

/* AFTER - Specificity: (0,1,1) */
a.wiki-nav-active,
.menu-link.wiki-nav-active {
    color: var(--burnt-orange);
}
```

---

## Implementation Order

1. Start with lowest-risk changes (wiki.css - 1 instance)
2. Move to components.css honeypot (security-critical, needs testing)
3. Refactor industrial-theme.css (theme-specific)
4. Tackle sleep.css (most complex, requires body class coordination)
5. Finish with base.css print styles

## Testing Checklist

- [ ] Print preview works correctly (Chrome/Firefox)
- [ ] Honeypot field remains invisible (inspect element)
- [ ] Industrial theme displays correctly
- [ ] Sleep mode animations work (wait 3+ minutes idle)
- [ ] Wake-up startled animations trigger
- [ ] Reduced motion preference respected
- [ ] Wiki nav active state shows orange
- [ ] Mobile sleep animations work

## Verification

After changes, run:
```bash
grep -r "!important" src/css/
```
Expected output: (no results)