---
name: Mission Control V3 Rewrite
overview: Comprehensive responsive rewrite of Mission Control with parallel dev server (port 3848) for side-by-side comparison. Phase 1 covers analysis, foundation, layout, and stats cards.
todos:
  - id: setup-v3-server
    content: "TKT-001: Create V3 dev environment on port 3848"
    status: completed
  - id: css-audit
    content: "TKT-002: Audit current 5044-line styles.css"
    status: completed
    dependencies:
      - setup-v3-server
  - id: html-audit
    content: "TKT-003: Audit HTML structure for responsive needs"
    status: completed
    dependencies:
      - setup-v3-server
  - id: design-tokens
    content: "TKT-004: Create enhanced fluid design tokens"
    status: completed
    dependencies:
      - css-audit
  - id: css-reset
    content: "TKT-005: Implement CSS reset and base"
    status: completed
    dependencies:
      - design-tokens
  - id: fluid-typography
    content: "TKT-006: Implement fluid typography scale"
    status: completed
    dependencies:
      - design-tokens
  - id: breakpoint-system
    content: "TKT-007: Implement breakpoint system"
    status: completed
    dependencies:
      - design-tokens
  - id: layout-shell
    content: "TKT-008: Build CSS Grid layout shell"
    status: completed
    dependencies:
      - breakpoint-system
      - css-reset
  - id: responsive-nav
    content: "TKT-009: Build responsive navigation"
    status: completed
    dependencies:
      - layout-shell
  - id: sidebar-drawer
    content: "TKT-010: Build sidebar/drawer system"
    status: completed
    dependencies:
      - layout-shell
  - id: main-content
    content: "TKT-011: Build main content zone"
    status: completed
    dependencies:
      - layout-shell
  - id: stats-card
    content: "TKT-012: Build stats card component"
    status: completed
    dependencies:
      - fluid-typography
  - id: stats-grid
    content: "TKT-013: Build responsive stats grid"
    status: completed
    dependencies:
      - stats-card
      - main-content
  - id: js-breakpoints
    content: "TKT-014: Add JS breakpoint detection"
    status: completed
    dependencies:
      - breakpoint-system
  - id: js-drawer
    content: "TKT-015: Add drawer/toggle JS logic"
    status: completed
    dependencies:
      - sidebar-drawer
      - js-breakpoints
  - id: test-breakpoints
    content: "TKT-016: Test all breakpoints systematically"
    status: completed
    dependencies:
      - stats-grid
      - js-drawer
  - id: test-accessibility
    content: "TKT-017: Touch and accessibility audit"
    status: completed
    dependencies:
      - test-breakpoints
---

# Mission Control V3 - Responsive Rewrite (Revised)

## Overview

Ground-up CSS architecture rewrite with mobile-first responsive design. Run V3 on port 3848 alongside V2 (port 3847) for live comparison.

## Current Codebase Analysis

| File | Lines | Notes |
|------|-------|-------|
| `styles.css` | 5,044 | Monolithic, needs modularization |
| `index.html` | 604 | Complex structure, needs audit |
| `app.js` | 2,940 | May need responsive-aware logic |

### Existing CSS Tokens (to preserve/enhance)
- Color system: 20+ custom properties (keep)
- Fixed spacing: `--space-xs` through `--space-2xl` (make fluid)
- Layout: `--sidebar-width: 280px`, `--topbar-height: 56px` (make responsive)
- Typography: JetBrains Mono + Space Grotesk (keep)
- Motion: transition timing (keep)

### HTML Structure (current)
```
body.has-sidebar
├── #site-nav (injected by nav.js)
├── .app
│   ├── aside.sidebar
│   │   ├── .sidebar-header (brand + toggle)
│   │   ├── .brand-tagline
│   │   ├── .search-container
│   │   ├── nav.tree-nav
│   │   └── .sidebar-footer
│   └── main.main-content
│       ├── header.topbar
│       ├── .command-center (dashboard view)
│       └── .detail-view (work effort detail)
├── .toast-container
└── modals...
```

---

## Development Setup

### Parallel Servers
| Version | Port | Purpose |
|---------|------|---------|
| V2 (current) | 3847 | Reference, production |
| V3 (new) | 3848 | Development, comparison |

### V3 Server Setup
1. Copy `mcp-servers/dashboard/` to `mcp-servers/dashboard-v3/`
2. Update `config.json` to use port 3848
3. Run both servers simultaneously

---

## Phase 1 Tickets (Revised)

### Phase 1A: Setup and Analysis (3 tickets)

| ID | Title | Description |
|----|-------|-------------|
| TKT-001 | Create V3 Dev Environment | Copy dashboard, configure port 3848, verify parallel running |
| TKT-002 | CSS Audit and Inventory | Document all current styles, identify what to keep/refactor |
| TKT-003 | HTML Structure Audit | Map current structure, plan responsive modifications |

### Phase 1B: CSS Foundation (4 tickets)

| ID | Title | Description |
|----|-------|-------------|
| TKT-004 | Design Tokens (Enhanced) | Fluid spacing with clamp(), responsive breakpoints, preserve colors |
| TKT-005 | CSS Reset and Base | Modern reset, smooth scroll, base typography |
| TKT-006 | Fluid Typography Scale | Responsive font sizes, line heights, letter spacing |
| TKT-007 | Breakpoint System | Mobile-first media queries, container query setup |

### Phase 1C: Core Layout (4 tickets)

| ID | Title | Description |
|----|-------|-------------|
| TKT-008 | Layout Shell (CSS Grid) | Named grid areas, responsive reflow |
| TKT-009 | Navigation Bar | Hamburger on mobile, full menu on desktop |
| TKT-010 | Sidebar/Drawer | Full sidebar on desktop, drawer overlay on mobile |
| TKT-011 | Main Content Zone | Responsive padding, scroll behavior |

### Phase 1D: Stats Cards (2 tickets)

| ID | Title | Description |
|----|-------|-------------|
| TKT-012 | Stats Card Component | Touch-friendly, responsive sizing |
| TKT-013 | Stats Grid Layout | 4-col -> 2-col -> 1-col responsive |

### Phase 1E: JavaScript Integration (2 tickets)

| ID | Title | Description |
|----|-------|-------------|
| TKT-014 | Breakpoint Detection | JS media query listeners, state management |
| TKT-015 | Drawer/Toggle Logic | Touch events, swipe gestures, keyboard nav |

### Phase 1F: Testing (2 tickets)

| ID | Title | Description |
|----|-------|-------------|
| TKT-016 | Breakpoint Testing Matrix | Test at 320, 480, 640, 768, 1024, 1280, 1440px |
| TKT-017 | Touch/Accessibility Audit | 44px targets, focus states, ARIA labels |

---

## Responsive Breakpoints

```css
/* Mobile-first breakpoints */
:root {
  --bp-sm: 480px;   /* Large phones */
  --bp-md: 640px;   /* Small tablets */
  --bp-lg: 1024px;  /* Tablets/small laptops */
  --bp-xl: 1280px;  /* Desktops */
  --bp-2xl: 1440px; /* Large screens */
}

/* Usage (min-width, mobile-first) */
@media (min-width: 640px) { /* tablet and up */ }
@media (min-width: 1024px) { /* desktop and up */ }
```

---

## Layout Behavior by Breakpoint

| Breakpoint | Sidebar | Nav | Stats Grid | Detail Panel |
|------------|---------|-----|------------|--------------|
| < 640px | Hidden (drawer) | Hamburger | 1 column | Full screen |
| 640-1024px | Collapsed (icons) | Full | 2 columns | Bottom sheet |
| > 1024px | Full (280px) | Full | 4 columns | Side panel |

---

## File Structure (V3)

```
mcp-servers/dashboard-v3/
├── config.json              # Port 3848
├── server.js                # (copy from v2)
├── public/
│   ├── index.html           # Updated structure
│   ├── styles/
│   │   ├── tokens.css       # Design tokens
│   │   ├── reset.css        # Modern reset
│   │   ├── typography.css   # Fluid type
│   │   ├── layout.css       # Grid shell
│   │   ├── components/
│   │   │   ├── nav.css
│   │   │   ├── sidebar.css
│   │   │   ├── cards.css
│   │   │   └── ...
│   │   └── main.css         # Imports all
│   ├── app.js               # Updated with responsive logic
│   └── ...
```

---

## Success Criteria

- [ ] V3 runs on port 3848 alongside V2 on 3847
- [ ] Dashboard renders correctly at all breakpoints (320-1440px)
- [ ] Sidebar converts to drawer below 640px
- [ ] No horizontal scroll at any width
- [ ] Touch targets minimum 44px
- [ ] Fluid typography scales smoothly
- [ ] All V2 functionality preserved in V3