---
name: 70s Retro Visual Overhaul
overview: Transform the FogSift website from cold brutalist aesthetic to warm 70's/80's retro-modern style matching the logo and profile badge, with simplified structure and removed complexity.
todos:
  - id: phase1-tokens
    content: "Overhaul tokens.css: new color palette, typography, border system"
    status: completed
  - id: phase2-structure
    content: Simplify index.html to 5 sections, remove diagnostic/breadcrumbs
    status: completed
  - id: phase2-remove
    content: Remove floating CTA, progress bar, breadcrumb HTML
    status: completed
  - id: phase3-cards
    content: Create badge-style card components in components.css
    status: completed
  - id: phase3-nav
    content: Simplify navigation to minimal top bar
    status: completed
  - id: phase4-hero
    content: Design hero section with badge-style centered card
    status: completed
  - id: phase4-process
    content: Create 3-step process section with numbered badges
    status: completed
  - id: phase4-about
    content: Simplify about section to badge + bio
    status: completed
  - id: phase4-pricing
    content: Clean up pricing cards, remove emoji decorations
    status: completed
  - id: phase5-cleanup
    content: Remove dead CSS/JS code, simplify main.js
    status: completed
  - id: phase5-dark
    content: Update dark mode to match new palette
    status: completed
  - id: final-test
    content: Test on mobile, verify aesthetic matches logo/badge
    status: completed
---

# 70's/80's Retro-Modern Visual Overhaul

## Vision
Transform FogSift from cold brutalist tech aesthetic to warm, confident 70's/80's retro-modern style that matches the logo and profile badge.

---

## Phase 1: Foundation (Tokens and Box Model)

### 1.1 Color Palette Overhaul
**File:** `src/css/tokens.css`

Replace current palette with brand-derived colors:

```css
/* 70's/80's Retro Palette */
--cream: #f5f0e6;        /* Primary background */
--cream-dark: #e8e0d0;   /* Secondary background */
--chocolate: #4a2c2a;    /* Primary text, borders */
--chocolate-light: #6b4423; /* Secondary text */
--burnt-orange: #e07b3c; /* CTA, accents */
--rust: #c2410c;         /* Hover states */
--earth-mid: #8b5a2b;    /* Decorative */
--earth-dark: #5c3d2e;   /* Decorative */
```

### 1.2 Typography System
**File:** `src/css/tokens.css`

- Keep Inter but increase weight usage
- Add geometric display font option (Outfit or DM Sans)
- Bolder headings, confident letter-spacing

```css
--font-display: 'Outfit', 'Inter', sans-serif;
--text-headline: clamp(2.5rem, 6vw, 4rem);
--letter-spacing-tight: -0.02em;
--letter-spacing-wide: 0.1em; /* For labels */
```

### 1.3 Box Model / Border System
**File:** `src/css/tokens.css`

- Rounded corners (badge aesthetic)
- Softer shadows (no hard offset)
- Double-line borders (retro feel)

```css
--radius: 8px;
--radius-lg: 16px;
--radius-badge: 24px;
--border-width: 3px;
--shadow-soft: 0 4px 20px rgba(74, 44, 42, 0.1);
--shadow-card: 0 8px 30px rgba(74, 44, 42, 0.15);
```

---

## Phase 2: Structure (Wireframe and Sections)

### 2.1 Simplified Page Structure
**File:** `src/index.html`

Reduce to 5 clean sections:

```
┌─────────────────────────────────────┐
│            NAVIGATION               │  Minimal, logo left, links right
├─────────────────────────────────────┤
│              HERO                   │  Badge-style centered card
│   "Straight answers to complicated  │
│         questions."                 │
│         [Contact CTA]               │
├─────────────────────────────────────┤
│           THE PROCESS               │  3 horizontal steps, icon badges
│    [Deconstruct] [Trace] [Solve]    │
├─────────────────────────────────────┤
│             ABOUT                   │  Photo + bio in badge card
│     Christopher - Owner             │
├─────────────────────────────────────┤
│            PRICING                  │  3 tier cards, horizontal
│   [Call] [Deep Dive] [Engagement]   │
├─────────────────────────────────────┤
│             FOOTER                  │  Minimal, links + copyright
└─────────────────────────────────────┘
```

### 2.2 Remove Complexity
**Files:** `src/index.html`, `src/js/main.js`, `src/css/components.css`

**Remove:**
- Floating CTA button
- Progress bar
- Breadcrumb system
- Diagnostic checklist (move to copy)
- Complex timeline with IO boxes
- Tech stack tags
- Capabilities grid

**Keep:**
- Toast notifications (useful feedback)
- Theme toggle (user preference)
- Mobile hamburger menu (necessary)

---

## Phase 3: Component Design

### 3.1 Badge-Style Cards
Primary design pattern: rounded rectangles with cream backgrounds, chocolate borders

```css
.card {
  background: var(--cream);
  border: var(--border-width) solid var(--chocolate);
  border-radius: var(--radius-lg);
  padding: 2rem;
}
```

### 3.2 Section Dividers
Horizontal rules with decorative elements (matching logo underline)

```css
.section-divider {
  height: 4px;
  background: var(--chocolate);
  width: 60%;
  margin: 0 auto;
  border-radius: 2px;
}
```

### 3.3 CTA Button Style
Pill-shaped, bold, matches brand orange

```css
.cta-button {
  background: var(--burnt-orange);
  color: var(--cream);
  border-radius: var(--radius-badge);
  padding: 1rem 2.5rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
```

### 3.4 Navigation
Minimal top bar, logo left, few links right, no breadcrumbs

---

## Phase 4: Content Hydration

### 4.1 Hero Section
- Large badge-style card
- Headline in bold display font
- Single CTA button
- No subtext clutter

### 4.2 Process Section
- 3 numbered badges in a row
- Simple icon + title + one sentence
- No input/output boxes

### 4.3 About Section
- Christopher badge image (already perfect)
- Name, title, one-liner bio
- No tech stack, no capabilities grid

### 4.4 Pricing Section
- 3 clean cards
- Clear pricing
- No emoji decorations

---

## Phase 5: Polish and Cleanup

### 5.1 Remove Dead Code
- Delete floating CTA HTML/CSS/JS
- Delete progress bar
- Delete breadcrumb system
- Delete diagnostic checklist
- Delete unused CSS classes

### 5.2 Simplify JS
- Keep: Toast, Theme, Nav (mobile menu)
- Remove: Diagnostic counter, floating CTA observer, complex scroll handlers

### 5.3 Dark Mode Adaptation
Invert to dark chocolate background with cream text, keep orange accent

---

## Key Files to Modify

| File | Changes |
|------|---------|
| `src/css/tokens.css` | Complete palette and token overhaul |
| `src/css/base.css` | Typography, layout simplification |
| `src/css/components.css` | New card/badge components, remove old |
| `src/index.html` | Simplified 5-section structure |
| `src/js/main.js` | Remove floating CTA, diagnostic, progress |

---

## Success Criteria

1. Site matches logo/badge aesthetic (warm, retro, confident)
2. Fewer than 100 lines of JS
3. Single-page flow with 5 clear sections
4. No floating elements or complex interactions
5. Works perfectly on mobile
6. Fast load time (less CSS/JS)