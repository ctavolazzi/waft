---
name: Simplify Dark Mode
overview: Refactor the dark mode system from a complex multi-component architecture (37 references, multiple sync calls) to a minimal, fast, single-toggle approach using pure CSS transitions and minimal JavaScript.
todos:
  - id: remove-fab-toggle
    content: Remove dark mode toggle from FAB settings menu
    status: completed
  - id: simplify-js
    content: Replace CFLDarkMode manager with 15-line inline script
    status: completed
  - id: simplify-html
    content: Replace checkbox toggle with simple button
    status: completed
  - id: cleanup-css
    content: Remove duplicate toggle CSS, add theme-based icon styles
    status: completed
  - id: remove-debug
    content: Remove all debug console.log statements
    status: completed

category: dreads
confidence: 0.70
constellation_date: 2026-01-14
---

# Simplify Dark Mode System

## Current Problems

The console logs reveal excessive complexity:

- **6+ sync calls** on page load alone
- **2 separate toggles** (drawer + FAB menu) requiring sync logic
- **CFLDarkMode manager object** with 4 methods
- **~50 lines of dark mode JS** spread across multiple IIFEs
- **Slow transitions** due to JavaScript-driven state updates

## Proposed Architecture

### Before (Current)

```
User Click → JS Handler → CFLDarkMode.setDarkMode() → 
  → Set data-theme attribute
  → Save to localStorage  
  → syncToggles() → Find drawer switch → Set checked
                 → Find menu switch → Set checked
```

### After (Simplified)

```
User Click → Toggle checkbox (native) → CSS :checked handles visual
          → Single event listener → Toggle data-theme + localStorage
```

## Implementation Plan

### 1. Remove Duplicate Toggle

Keep only ONE dark mode toggle location - the settings drawer. Remove the FAB menu dark mode toggle entirely.

**Files:** `_layouts/default.html`

- Remove the Appearance section from FAB settings menu (lines ~1943-1958)
- Remove menu dark mode switch event handlers (lines ~2027-2045)

### 2. Simplify JavaScript to ~15 lines

Replace the CFLDarkMode manager with a simple inline script:

```javascript
// Dark mode - runs immediately (before DOMContentLoaded)
(function() {
  var KEY = 'cfl-dark-mode';
  var html = document.documentElement;
  
  // Apply saved preference or system preference
  var saved = localStorage.getItem(KEY);
  var prefersDark = saved === 'true' || 
    (saved === null && matchMedia('(prefers-color-scheme:dark)').matches);
  html.dataset.theme = prefersDark ? 'dark' : 'light';
  
  // Toggle handler (delegate to any .dark-mode-toggle click)
  document.addEventListener('click', function(e) {
    if (e.target.closest('.dark-mode-toggle')) {
      var isDark = html.dataset.theme === 'dark';
      html.dataset.theme = isDark ? 'light' : 'dark';
      localStorage.setItem(KEY, isDark ? 'false' : 'true');
    }
  });
})();
```

### 3. Simplify Toggle HTML

Replace the complex checkbox-based toggle with a simple button:

```html
<button class="dark-mode-toggle" aria-label="Toggle dark mode">
  <span class="dark-mode-toggle__icon"></span>
  Dark Mode
</button>
```

### 4. CSS-Only Toggle Animation

Use CSS to handle the visual state based on `[data-theme]`:

```css
/* Toggle icon changes based on theme */
[data-theme="light"] .dark-mode-toggle__icon::before { content: "☀️"; }
[data-theme="dark"] .dark-mode-toggle__icon::before { content: "🌙"; }

/* Instant color transitions */
:root { transition: none; } /* Remove transition delay */
```

### 5. Remove Debug Logging

Delete all `console.log('[CFL debug]...` and `console.log('[CFL DRAWER]...` statements.

## Benefits

| Metric | Before | After |

|--------|--------|-------|

| Lines of JS | ~80 | ~15 |

| Sync calls on load | 6+ | 0 |

| Toggle locations | 2 | 1 |

| Event listeners | 5+ | 1 (delegated) |

| Time to toggle | ~10ms | ~1ms |

## Files to Modify

1. **[_layouts/default.html](_layouts/default.html)** - Remove CFLDarkMode manager, FAB menu toggle, debug logs; add simple inline script
2. **[assets/css/main.css](assets/css/main.css)** - Simplify toggle styles, remove duplicate `.cfl-toggle` rules