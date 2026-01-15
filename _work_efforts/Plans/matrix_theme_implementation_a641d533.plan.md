---
name: Matrix Theme Implementation
overview: Add an animated Matrix-themed fourth theme to FogSift featuring falling digital rain as a canvas background, green phosphor color palette, monospace typography, and CRT-style glow effects.
todos:
  - id: create-matrix-rain-js
    content: Create src/js/matrix-rain.js with canvas-based falling code animation
    status: pending
  - id: create-matrix-theme-css
    content: Create src/css/matrix-theme.css with green phosphor palette and CRT effects
    status: pending
  - id: update-tokens-css
    content: Add [data-theme="matrix"] variable block to tokens.css
    status: pending
  - id: update-theme-js
    content: Add 'matrix' to THEMES array and THEME_LABELS in theme.js
    status: pending
  - id: update-build-js
    content: "Update build.js: VALID_THEMES, CSS_FILES, JS_FILES, nav template"
    status: pending
  - id: test-and-verify
    content: Test theme switching, animation performance, and accessibility
    status: pending
---

# Matrix Theme Implementation

## Overview

Add a new "Matrix" theme to FogSift featuring the iconic green falling code aesthetic with animated digital rain background. The theme will integrate seamlessly with the existing 3-theme system (Light, Dark, Industrial).

## Architecture

```mermaid
flowchart TB
    subgraph ThemeSystem [Theme System Updates]
        ThemeJS[theme.js] --> |"Add 'matrix' to THEMES array"| Dropdown
        Dropdown[Theme Picker UI] --> |"New option with icon"| Selection
        BuildJS[build.js] --> |"Update VALID_THEMES"| FOUC[FOUC Prevention]
    end

    subgraph MatrixCode [Matrix Rain Effect]
        Canvas[matrix-rain.js] --> |"Renders to"| CanvasEl[Canvas Element]
        CanvasEl --> |"z-index: -1"| Background
        CSS[matrix-theme.css] --> |"Styles overlay"| Components
    end

    subgraph ColorPalette [Matrix Palette]
        BG["#0D0208 (near-black)"]
        Primary["#00FF41 (phosphor green)"]
        Glow["#003B00 (dark green)"]
        Text["#00FF41 / #008F11"]
    end

    ThemeSystem --> MatrixCode
```

## Files to Create/Modify

### New Files
1. **`src/js/matrix-rain.js`** - Canvas-based falling code animation
   - Self-contained module that creates/destroys canvas on theme change
   - Configurable speed, density, character set (katakana + ASCII)
   - Performance-optimized with requestAnimationFrame
   - Responds to Theme.subscribe() events

2. **`src/css/matrix-theme.css`** - Theme-specific styles
   - Green phosphor color palette with CSS variables
   - CRT scanline overlay effect (subtle)
   - Text glow/shadow effects
   - Component overrides matching industrial-theme.css pattern

### Modified Files
1. **[`src/js/theme.js`](src/js/theme.js)** - Add 'matrix' to THEMES array and THEME_LABELS
2. **[`scripts/build.js`](scripts/build.js)** - Add 'matrix' to VALID_THEMES, add new files to CSS_FILES/JS_FILES arrays, update nav template
3. **[`src/css/tokens.css`](src/css/tokens.css)** - Add `[data-theme="matrix"]` variable block

## Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| `--cream` | `#0D0208` | Near-black background |
| `--chocolate` | `#00FF41` | Primary phosphor green text |
| `--burnt-orange` | `#00FF41` | CTA buttons (same green) |
| `--accent` | `#008F11` | Secondary green |
| `--highlight` | `#39FF14` | Bright neon green accents |
| `--glow` | `0 0 10px #00FF41` | Text/element glow effect |

## Matrix Rain Implementation

The canvas effect will use these techniques:
- Characters: Mix of half-width katakana (U+FF66-U+FF9D) and ASCII
- Columns calculated from viewport width / font size
- Each column drops at slightly randomized speeds
- Characters fade from bright green to dark green as they fall
- Occasional "bright flash" characters for visual interest

## Theme Picker UI Update

Add new option to theme picker dropdown:
```html
<button class="theme-picker-option" data-theme="matrix" role="option" onclick="ThemePicker.select('matrix')">
    <span class="theme-option-icon">▓</span>
    <span class="theme-option-label">Matrix</span>
    <span class="theme-option-check" aria-hidden="true">✓</span>
</button>
```

## Accessibility Considerations

- Reduced motion: Disable rain animation when `prefers-reduced-motion: reduce`
- High contrast: Ensure sufficient contrast ratios (green on black passes WCAG AA)
- Canvas is decorative only (aria-hidden="true")
