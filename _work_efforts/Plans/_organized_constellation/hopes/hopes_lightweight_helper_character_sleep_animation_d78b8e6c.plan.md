---
name: Lightweight Helper Character Sleep Animation
overview: Replace the heavy canvas-based flying toaster animation with a lightweight CSS-animated helper character that runs around the screen interacting with UI elements, dramatically reducing system load while keeping the cute aesthetic.
todos:
  - id: design-character
    content: Design and implement the helper character (emoji, CSS, or SVG)
    status: pending
  - id: css-movement
    content: Create CSS keyframe animation path for character movement
    status: pending
  - id: element-interactions
    content: Add CSS animations for when helper 'adjusts' elements
    status: pending
  - id: refactor-sleep-js
    content: Remove canvas/toaster code from sleep.js, add helper creation
    status: pending
  - id: timing-coordination
    content: Coordinate JS class toggles with CSS animation timing for interactions
    status: pending
  - id: test-performance
    content: Verify reduced CPU/GPU usage compared to current implementation
    status: pending

category: hopes
confidence: 0.40
constellation_date: 2026-01-14
---

# Lightweight Helper Character Sleep Animation

## Current Problem
The existing sleep mode uses a canvas-based flying toaster animation that runs `requestAnimationFrame` at 60fps, continuously drawing multiple toasters. This is CPU-intensive and drains battery on mobile.

## Proposed Solution
Replace canvas animation with a single CSS-animated "helper" character that moves around using GPU-accelerated CSS transforms. The character will visit and interact with UI elements (buttons, cards) in a choreographed sequence.

---

## Implementation

### 1. Character Design

Create a simple helper character using CSS/emoji/SVG:

```css
/* Little pixel-art helper (CSS-based) */
.sleep-helper {
  width: 32px;
  height: 32px;
  position: fixed;
  z-index: 10001;
  /* Character appearance via emoji or SVG */
}
```

**Character options:**
- Emoji-based: A little worker/builder character (e.g., construction worker, mechanic)
- CSS pixel-art sprite (like the current toaster but simpler)
- Small SVG mascot

### 2. Movement System

Use CSS keyframe animations instead of JavaScript canvas:

```css
@keyframes helperPath {
  0%   { left: 10%;  top: 80%; }
  15%  { left: 25%;  top: 20%; }  /* Visit header */
  30%  { left: 60%;  top: 35%; }  /* Visit a card */
  /* ... continues visiting elements */
  100% { left: 10%;  top: 80%; }
}
```

This is dramatically lighter because:
- CSS transforms are GPU-accelerated
- No JavaScript per-frame execution
- Single DOM element vs. canvas redraw

### 3. Element Interactions

When the helper "reaches" an element, trigger CSS animations:

```css
.being-adjusted {
  animation: elementWobble 0.5s ease-in-out;
}

@keyframes elementWobble {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-3deg) scale(1.02); }
  75% { transform: rotate(3deg) scale(1.02); }
}
```

### 4. Files to Modify

| File | Changes |
|------|---------|
| [`src/css/sleep.css`](src/css/sleep.css) | Add helper character styles, movement keyframes, interaction animations |
| [`src/js/sleep.js`](src/js/sleep.js) | Remove canvas/toaster code, add helper element creation, coordinate element interactions with CSS animation timing |

### 5. What Gets Removed

- `initToasters()` - No more flying toasters
- `drawToaster()` - No more pixel drawing
- `startAnimation()` with `requestAnimationFrame` - No more JS animation loop
- Canvas element creation

### 6. What Gets Added

- Single `.sleep-helper` DOM element
- CSS keyframe path animation
- Timed class toggles for element interactions
- Optional: Multiple "poses" for the helper (walking, carrying, adjusting)

---

## Performance Comparison

| Metric | Current (Canvas) | Proposed (CSS) |
|--------|-----------------|----------------|
| JS execution | Every frame (60/sec) | Initial setup only |
| GPU utilization | Low (canvas is CPU) | High (CSS transforms) |
| Power consumption | High | Low |
| Animation smoothness | Depends on CPU | Consistent 60fps |

---

## Open Questions

1. **Character appearance:** Should the helper be an emoji (simplest), CSS pixel-art, or SVG sprite?
2. **Interaction style:** Should the helper literally "carry" buttons/elements, or just trigger wobble animations when nearby?
3. **Path complexity:** Simple loop visiting a few elements, or randomized visits?
