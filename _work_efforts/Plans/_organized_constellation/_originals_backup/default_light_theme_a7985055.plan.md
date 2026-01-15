---
name: Default Light Theme
overview: Change the default theme from system-preference-aware to always-light for first-time visitors. Users who explicitly toggle to dark mode will have their preference saved and respected.
todos:
  - id: update-index-html
    content: Update theme logic in src/index.html to default to light
    status: completed
  - id: update-404-html
    content: Update theme logic in src/404.html to default to light
    status: completed
  - id: update-theme-js
    content: Update theme logic in src/js/theme.js to default to light
    status: completed
  - id: rebuild-test
    content: Run npm run build and verify the change works
    status: completed
---

# Default to Light Mode

## Changes Required

Three files need identical logic updates to remove system preference detection:

### 1. [src/index.html](src/index.html) (lines 48-57)

**Before:**
```javascript
if (localTheme === 'dark' || (!localTheme && supportDarkMode)) {
    document.documentElement.setAttribute('data-theme', 'dark');
} else {
    document.documentElement.setAttribute('data-theme', 'light');
}
```

**After:**
```javascript
document.documentElement.setAttribute('data-theme', localTheme || 'light');
```

The `supportDarkMode` variable can also be removed since it's no longer used.

### 2. [src/404.html](src/404.html) (lines 10-19)

Same change as above - simplify to use saved preference or default to light.

### 3. [src/js/theme.js](src/js/theme.js) (lines 10-13)

**Before:**
```javascript
const saved = localStorage.getItem(this.STORAGE_KEY);
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
const theme = saved || (prefersDark ? 'dark' : 'light');
```

**After:**
```javascript
const theme = localStorage.getItem(this.STORAGE_KEY) || 'light';
```

### 4. Rebuild and test

Run `npm run build` to regenerate `dist/` files with the updated logic.

## Result

- First-time visitors: Light mode
- Users who toggle to dark: Dark mode (saved in localStorage)
- Users who toggle back to light: Light mode (saved in localStorage)