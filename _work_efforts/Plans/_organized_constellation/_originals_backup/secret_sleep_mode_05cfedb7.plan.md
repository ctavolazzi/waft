---
name: Secret Sleep Mode
overview: Add a hidden "sleep mode" easter egg that activates after 5 minutes of page time plus 30 seconds of inactivity, featuring retro 70s/80s-themed animations with a flying toaster homage and pixel art aesthetic. Users click anywhere to wake the site up.
todos:
  - id: create-sleep-js
    content: Create src/js/sleep.js with timer logic, canvas toasters, and overlay
    status: completed
  - id: add-sleep-css
    content: Add sleep mode CSS animations and overlay styles to components.css
    status: completed
  - id: integrate-main
    content: Add SleepMode.init() call to main.js App.init()
    status: completed
---

# Secret Sleep Mode Easter Egg

## Feature Summary

A hidden sleep mode that triggers after 5 minutes total page time + 30 seconds idle. Features a retro 70s/80s screensaver aesthetic with:

- Flying toasters (classic Mac screensaver homage) rendered in pixel art style
- Gentle "static TV" scanlines overlay
- Floating "Z Z Z" letters in the retro orange palette
- Site dims to 30% opacity with a warm sepia tone
- Console message easter egg when activated

## Implementation

### 1. New JavaScript Module: `sleep.js`

Create [`src/js/sleep.js`](src/js/sleep.js) with:

- `SleepMode` object tracking:
- `pageLoadTime` - timestamp when page loaded
- `lastActivityTime` - updated on mouse/keyboard/scroll
- `isAsleep` - current state
- Timer logic: Check every 5 seconds if conditions are met (5 min total + 30s idle)
- DOM injection for overlay with canvas-based flying toasters
- Pixel-art toaster sprites drawn via canvas (no external images needed)
- Click handler to dismiss and reset timers

### 2. CSS for Sleep Overlay

Add to [`src/css/components.css`](src/css/components.css):

- Full-screen overlay with `z-index: 9999`
- CSS animations for floating Zs (keyframes)
- Scanline effect via repeating linear gradient
- Smooth fade-in/out transitions
- Respects `prefers-reduced-motion`

### 3. Integration in Main

Update [`src/js/main.js`](src/js/main.js):

- Call `SleepMode.init()` in `App.init()`
- Console easter egg message when sleep activates

## Animation Details

**Flying Toasters**: 8-bit style toasters with wings, moving diagonally across screen in classic screensaver pattern. Drawn via canvas for performance.**Floating Zs**: 3 sizes of "Z" letters in burnt-orange, drifting upward with slight rotation. CSS-only animation.**Scanlines**: Subtle CRT-style horizontal lines overlay for authentic retro feel.**Wake-up**: Click anywhere triggers a "TV turning on" flash effect, then smooth fade-out.

## Files to Modify/Create

| File | Action ||------|--------|| [`src/js/sleep.js`](src/js/sleep.js) | Create - main sleep mode logic |