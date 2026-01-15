---
name: Component Library Architecture
overview: Build a strategic component library by extending the patterns from the Detail View Overhaul PR, fixing dashboard overflow issues, and creating reusable, well-documented components.
todos:
  - id: fix-overflow-quick
    content: Fix immediate dashboard overflow issues (stats grid, buttons, indicators)
    status: completed
  - id: create-buttons-css
    content: Create buttons.css component file with all button variants
    status: completed
  - id: create-indicators-css
    content: Create indicators.css component file for status dots and badges
    status: completed
  - id: refactor-cards-bem
    content: Refactor cards.css with BEM naming convention
    status: completed
  - id: delete-legacy-sections
    content: Delete migrated sections from legacy styles.css
    status: completed
  - id: consolidate-tokens
    content: Consolidate design tokens into single tokens.css source
    status: completed
  - id: create-component-docs
    content: Create component documentation in docs/components/
    status: completed
  - id: build-demo-page
    content: Build visual component showcase page
    status: completed

category: dreads
confidence: 0.42
constellation_date: 2026-01-14
---

# Component Library Architecture Plan

## Context: Building on PR #16

The recent Detail View Overhaul established excellent patterns:

- Modular CSS in [`detail-view-improvements.css`](mcp-servers/dashboard-v3/public/styles/detail-view-improvements.css)
- Semantic HTML with ARIA labels
- Action button variants (`.action-primary`, `.action-success`, `.action-warning`)
- Responsive touch targets (44-64px minimum)
- Accessibility compliance

**Goal:** Extend these patterns into a full component library and fix the remaining dashboard overflow issues.---

## Phase 1: Foundation - Design Tokens and Reset

### 1.1 Consolidate Design Tokens

Current state: Tokens split between legacy `styles.css` and V3 `tokens.css`**Action:** Merge into single source of truth in [`tokens.css`](mcp-servers/dashboard-v3/public/styles/tokens.css):

```javascript
tokens.css
├── Colors (backgrounds, text, status, accents)
├── Typography (fonts, sizes, weights, line-heights)
├── Spacing (fluid clamp values)
├── Layout (sidebar, topbar, breakpoints)
├── Shadows & Effects
├── Z-index scale
├── Border radii
├── Transitions & Animations
└── Component-specific tokens (NEW)
    ├── --btn-height-sm: 36px
    ├── --btn-height-md: 44px
    ├── --btn-height-lg: 56px
    ├── --card-padding: var(--space-md)
    └── --indicator-size: 12px
```



### 1.2 Remove Legacy Conflicts

From `styles.css`, **delete** these sections (already in V3 or being migrated):

- Lines 1171-1244: Stats Section (move to `cards.css`)
- Lines 1321-1440: Queue Item (move to `cards.css`)
- Lines 3484-3916: Test/Demo buttons (move to `buttons.css`)
- Lines 4572-5044: Responsive (already in V3 `layout.css`)

---

## Phase 2: Component Library Structure

### 2.1 Directory Organization

```javascript
styles/
├── tokens.css              # Design tokens (single source)
├── reset.css               # Modern CSS reset
├── typography.css          # Font definitions, text utilities
├── layout.css              # Grid system, containers
├── main.css                # Imports all (load order matters)
│
├── components/
│   ├── buttons.css         # NEW: All button variants
│   ├── cards.css           # Stat cards, queue cards, panel cards
│   ├── indicators.css      # NEW: Status dots, badges, progress
│   ├── forms.css           # NEW: Inputs, selects, search
│   ├── nav.css             # Navigation, breadcrumbs
│   ├── sidebar.css         # Sidebar/drawer
│   ├── modals.css          # NEW: Modals, overlays, panels
│   ├── toast.css           # NEW: Toast notifications
│   └── command-center.css  # Command center specific
│
├── views/
│   ├── dashboard.css       # NEW: Dashboard view layout
│   └── detail.css          # Renamed from detail-view-improvements.css
│
└── utilities.css           # NEW: Utility classes (flex, grid, spacing)
```



### 2.2 Component Naming Convention

Use **BEM-like** naming with semantic prefixes:

```css
/* Block */
.card { }

/* Block--Modifier */
.card--stat { }
.card--queue { }
.card--action { }

/* Block__Element */
.card__icon { }
.card__content { }
.card__title { }
.card__value { }

/* State */
.card.is-active { }
.card.is-loading { }
.card.is-highlighted { }
```

---

## Phase 3: Core Components

### 3.1 Buttons (`components/buttons.css`)

**Variants:**

| Class | Purpose | Height |

|-------|---------|--------|

| `.btn` | Base button | 44px |

| `.btn--primary` | Primary action (accent color) | 44px |

| `.btn--secondary` | Secondary action (outline) | 44px |

| `.btn--success` | Success/complete (green) | 44px |

| `.btn--warning` | Warning/caution (orange) | 44px |

| `.btn--danger` | Destructive (red) | 44px |

| `.btn--ghost` | Text-only, no background | 44px |

| `.btn--icon` | Icon-only button | 44px x 44px |

| `.btn--sm` | Small size | 36px |

| `.btn--lg` | Large size | 56px |**Pattern (from detail-view-improvements.css):**

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-xs);
  min-height: var(--btn-height-md);
  padding: var(--space-sm) var(--space-md);
  font-size: var(--text-sm);
  font-weight: var(--fw-medium);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-elevated);
  color: var(--text-primary);
  cursor: pointer;
  transition: all var(--transition-fast);
  /* Prevent overflow */
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
```



### 3.2 Cards (`components/cards.css`)

**Variants:**

| Class | Purpose |

|-------|---------|

| `.card` | Base card container |

| `.card--stat` | Stat display (icon + value + label) |

| `.card--queue` | Queue item (indicator + info + badge) |

| `.card--action` | Clickable action card (test/demo buttons) |

| `.card--panel` | Panel section in detail view |**Fix for overflow:**

```css
.card {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--card-padding);
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  /* Prevent overflow */
  overflow: hidden;
  min-width: 0;
}

.card__value {
  font-family: var(--font-mono);
  font-size: clamp(1.25rem, 4vw, 2rem); /* Responsive! */
  font-weight: var(--fw-bold);
  overflow: hidden;
  text-overflow: ellipsis;
}
```



### 3.3 Indicators (`components/indicators.css`)

**Variants:**

| Class | Purpose |

|-------|---------|

| `.indicator` | Base status dot |

| `.indicator--active` | Active/in-progress (pulsing) |

| `.indicator--completed` | Completed (green) |

| `.indicator--pending` | Pending (gray) |

| `.indicator--blocked` | Blocked (red) |

| `.badge` | Text badge (status label) |**Fix for box-shadow overflow:**

```css
.indicator {
  --indicator-size: 12px;
  --indicator-glow: 4px; /* Reduced from 8-12px */
  
  width: var(--indicator-size);
  height: var(--indicator-size);
  border-radius: 50%;
  flex-shrink: 0;
}

.indicator--active {
  background: var(--status-active);
  box-shadow: 0 0 var(--indicator-glow) var(--status-active);
}

/* Parent needs padding to accommodate glow */
.queue-item {
  padding-left: calc(var(--space-md) + var(--indicator-glow));
}
```



### 3.4 Grid System (`layout.css` enhancement)

**Stats Grid Fix:**

```css
.stats-grid {
  display: grid;
  gap: var(--space-md);
  width: 100%;
  /* Safe minmax that won't overflow */
  grid-template-columns: repeat(2, 1fr);
}

@media (min-width: 640px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 900px) {
  .stats-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (min-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(6, 1fr);
  }
}
```

---

## Phase 4: Fix Dashboard Overflow Issues

### 4.1 Stats Section

- Replace `minmax(200px, 1fr)` with fixed column counts per breakpoint
- Add `overflow: hidden` to `.stats-section`
- Add responsive `font-size: clamp()` to `.stat-value`

### 4.2 Test/Demo Buttons

- Constrain buttons with `max-width: 100%`
- Add `overflow: hidden` to `.card--action`
- Use flex layout instead of fixed padding

### 4.3 Queue Indicators

- Reduce `box-shadow` spread from 8-12px to 4px
- Add padding to parent to accommodate glow
- Use `filter: drop-shadow()` as alternative

---

## Phase 5: Documentation

### 5.1 Component Documentation

Create `docs/components/` with:

- `buttons.md` - All button variants with examples
- `cards.md` - Card patterns and usage
- `indicators.md` - Status indicators
- `forms.md` - Form elements
- `layout.md` - Grid system

### 5.2 Storybook-like Demo Page

Create `public/docs/components.html`:

- Visual showcase of all components
- Interactive states (hover, focus, active)
- Responsive preview
- Copy-to-clipboard for HTML snippets

---

## Implementation Order

| Priority | Task | Files |

|----------|------|-------|

| 1 | Fix dashboard overflow (quick wins) | `cards.css`, `layout.css` |

| 2 | Create `buttons.css` component | New file |

| 3 | Create `indicators.css` component | New file |

| 4 | Refactor `cards.css` with BEM naming | Existing file |

| 5 | Delete legacy CSS sections | `styles.css` |

| 6 | Create component documentation | `docs/` |

| 7 | Build demo page | `public/docs/` |---

## Success Criteria

- [ ] No overflow on any screen size (320px - 2560px)
- [ ] All components use consistent naming (BEM-like)
- [ ] All interactive elements have 44px minimum touch targets
- [ ] Components are self-contained (no global style leakage)
- [ ] Documentation exists for each component