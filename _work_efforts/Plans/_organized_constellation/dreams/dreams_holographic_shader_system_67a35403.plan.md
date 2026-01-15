---
name: Holographic Shader System
overview: Create a universal CSS holographic shader system with utility classes that can be applied to text, buttons, containers, borders, and images.
todos:
  - id: add-holo-css
    content: Add holographic utility classes to assets/css/main.css
    status: completed
  - id: update-showcase
    content: Add Holographic Utilities section to component-showcase.mkd with examples
    status: completed

category: dreams
confidence: 0.48
constellation_date: 2026-01-14
---

# Universal Holographic Shader System

## Goal
Expand the existing button-only holographic effect into a versatile utility class system that works on any element.

## Current State
The holographic effect exists only for buttons at [assets/css/main.css](assets/css/main.css) lines 921-971, using:
- Rainbow gradient background with `background-size: 300%` for animation
- `::before` pseudo-element for shine sweep effect
- Two keyframe animations: `holo-shift` and `holo-shine`

## Technical Constraints Addressed

### 1. Positioning Context
The shine `::before` uses absolute positioning. Base classes MUST include `position: relative` and `overflow: hidden` to contain the effect.

### 2. Image Pseudo-Element Limitation
CSS pseudo-elements do NOT work on `<img>` tags (replaced elements). Solution: support both wrapper approach and background-image approach.

### 3. Border Radius + Gradient Conflict
`border-image` ignores `border-radius`. Solution: use double-background-clip trick with solid center fill.

### 4. Accessibility
Large animated gradients can trigger vestibular disorders. Solution: include `prefers-reduced-motion` media query.

## Implementation

### 1. Add CSS to `assets/css/main.css` (after line 971)

```css
/* === HOLOGRAPHIC UTILITY SYSTEM === */

/* Base holographic background */
.cfl-holo {
    background: linear-gradient(135deg, #ff6b6b 0%, #feca57 20%, #48dbfb 40%, #ff9ff3 60%, #54a0ff 80%, #ff6b6b 100%);
    background-size: 300% 300%;
    animation: holo-shift 4s ease infinite;
    position: relative;  /* REQUIRED: contain pseudo-elements */
    overflow: hidden;    /* REQUIRED: clip shine effect */
}

/* Shine sweep overlay - add to .cfl-holo elements */
.cfl-holo-shine::before {
    content: '';
    position: absolute;
    inset: -50%;
    background: linear-gradient(45deg, transparent 40%, rgba(255,255,255,0.4) 50%, transparent 60%);
    animation: holo-shine 3s linear infinite;
    pointer-events: none;
    z-index: 1;
}

/* Holographic text (gradient text fill) */
.cfl-holo-text {
    background: linear-gradient(135deg, #ff6b6b 0%, #feca57 20%, #48dbfb 40%, #ff9ff3 60%, #54a0ff 80%, #ff6b6b 100%);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent; /* fallback */
    animation: holo-shift 4s ease infinite;
}

/* Holographic border with solid center (supports border-radius) */
.cfl-holo-border {
    border: 3px solid transparent;
    background:
        linear-gradient(var(--cfl-bg-surface, #1a1a2e), var(--cfl-bg-surface, #1a1a2e)) padding-box,
        linear-gradient(135deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3, #54a0ff, #ff6b6b) border-box;
    background-size: 100% 100%, 300% 300%;
    animation: holo-border-shift 4s ease infinite;
}

@keyframes holo-border-shift {
    0% { background-position: 0 0, 0% 50%; }
    50% { background-position: 0 0, 100% 50%; }
    100% { background-position: 0 0, 0% 50%; }
}

/* Image wrapper approach - apply to div/figure containing img */
.cfl-holo-img {
    position: relative;
    overflow: hidden;
    display: inline-block;
}
.cfl-holo-img::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, #ff6b6b33, #feca5733, #48dbfb33, #ff9ff333, #54a0ff33, #ff6b6b33);
    background-size: 300% 300%;
    mix-blend-mode: overlay;
    animation: holo-shift 4s ease infinite;
    pointer-events: none;
}
.cfl-holo-img img {
    display: block;
    width: 100%;
    height: auto;
}

/* Background-image approach - image set via CSS */
.cfl-holo-bg {
    position: relative;
    overflow: hidden;
    background-size: cover;
    background-position: center;
}
.cfl-holo-bg::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, #ff6b6b33, #feca5733, #48dbfb33, #ff9ff333, #54a0ff33, #ff6b6b33);
    background-size: 300% 300%;
    mix-blend-mode: overlay;
    animation: holo-shift 4s ease infinite;
    pointer-events: none;
}

/* Speed modifiers */
.cfl-holo--fast, .cfl-holo--fast::before, .cfl-holo--fast::after { animation-duration: 1s !important; }
.cfl-holo--slow, .cfl-holo--slow::before, .cfl-holo--slow::after { animation-duration: 8s !important; }

/* Accessibility: respect reduced motion preference */
@media (prefers-reduced-motion: reduce) {
    .cfl-holo,
    .cfl-holo::before,
    .cfl-holo-shine::before,
    .cfl-holo-text,
    .cfl-holo-border,
    .cfl-holo-img::after,
    .cfl-holo-bg::after {
        animation: none !important;
        background-size: 100% 100% !important;
    }
}
```

### 2. Keep backward compatibility
The existing `.cfl-btn--holo` class remains unchanged.

### 3. Update component showcase
Add "Holographic Utilities" section to [_wiki/component-showcase.mkd](_wiki/component-showcase.mkd):
- Holographic text headings
- Holographic cards/containers with shine
- Holographic borders (with border-radius demo)
- Holographic images (wrapper approach)
- Speed variations
- Note about reduced-motion support

## Files to Modify
| File | Change |
|------|--------|
| `assets/css/main.css` | Add ~80 lines of holographic utility classes |
| `_wiki/component-showcase.mkd` | Add showcase section with usage examples |

## Class Reference

| Class | Use Case | Notes |
|-------|----------|-------|
| `.cfl-holo` | Rainbow gradient background | Base class, includes positioning context |
| `.cfl-holo-shine` | Sweeping shine effect | Combine with `.cfl-holo` |
| `.cfl-holo-text` | Rainbow gradient text | Uses background-clip |
| `.cfl-holo-border` | Rainbow border, solid center | Supports border-radius |
| `.cfl-holo-img` | Image overlay (wrapper) | Apply to div/figure containing img |
| `.cfl-holo-bg` | Image overlay (CSS bg) | Set background-image inline |
| `.cfl-holo--fast` | 1s animation | Modifier |
| `.cfl-holo--slow` | 8s animation | Modifier |

## Usage Examples

```html
<!-- Text -->
<h1 class="cfl-holo-text">Rainbow Heading</h1>

<!-- Card with shine -->
<div class="cfl-card cfl-holo cfl-holo-shine">Content</div>

<!-- Border only (works with rounded corners) -->
<div class="cfl-card cfl-holo-border" style="border-radius: 12px;">Content</div>

<!-- Image wrapper approach -->
<figure class="cfl-holo-img">
    <img src="photo.jpg" alt="Photo">
</figure>

<!-- Image background approach -->
<div class="cfl-holo-bg" style="background-image: url('photo.jpg'); height: 200px;"></div>
```