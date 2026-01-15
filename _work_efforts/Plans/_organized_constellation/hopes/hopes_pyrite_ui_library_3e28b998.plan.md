---
name: _pyrite UI Library
overview: Formalize the existing Mission Control dashboard styles and components into a documented, reusable "_pyrite-ui" library with organized CSS modules, JavaScript utilities, and usage documentation.
todos:
  - id: setup-structure
    content: Create pyrite-ui directory structure with tokens.css and base.css
    status: pending
  - id: extract-components
    content: Extract 8 component CSS modules from styles.css
    status: pending
    dependencies:
      - setup-structure
  - id: create-ui-js
    content: Create ui.js with toast, modal, confirm, notify helpers
    status: pending
    dependencies:
      - extract-components
  - id: build-catalog
    content: Create docs/index.html component catalog page
    status: pending
    dependencies:
      - extract-components
  - id: write-readme
    content: Write docs/README.md with usage and API reference
    status: pending
    dependencies:
      - create-ui-js
  - id: integrate-dashboard
    content: Update dashboard to use new pyrite-ui imports
    status: pending
    dependencies:
      - extract-components
      - create-ui-js

category: hopes
confidence: 0.50
constellation_date: 2026-01-14
---

# _pyrite UI Library Formalization Plan

Create a modular, documented UI library extracted from the existing Mission Control dashboard. The library will live in `mcp-servers/dashboard/lib/pyrite-ui/` and be consumable by future dashboards or tools.

---

## Architecture

```mermaid
graph TD
    subgraph pyrite_ui [pyrite-ui Library]
        Tokens[tokens.css]
        Base[base.css]
        Components[components/]
        Utils[ui.js]
        Docs[docs/]
    end
    
    subgraph components [Component CSS Modules]
        Buttons[buttons.css]
        Cards[cards.css]
        Modals[modals.css]
        Toasts[toasts.css]
        Sidebar[sidebar.css]
        Forms[forms.css]
        Nav[navigation.css]
        Charts[charts.css]
    end
    
    Components --> Buttons
    Components --> Cards
    Components --> Modals
    Components --> Toasts
    Components --> Sidebar
    Components --> Forms
    Components --> Nav
    Components --> Charts
    
    Tokens --> Base
    Base --> Components
    Utils --> Components
```

---

## Directory Structure

```
mcp-servers/dashboard/lib/pyrite-ui/
├── pyrite-ui.css          # Main entry (imports all)
├── tokens.css             # Design tokens (colors, spacing, etc.)
├── base.css               # Reset, typography, utilities
├── components/
│   ├── buttons.css
│   ├── cards.css
│   ├── modals.css
│   ├── toasts.css
│   ├── sidebar.css
│   ├── forms.css
│   ├── navigation.css
│   └── charts.css
├── ui.js                  # JS helpers (createToast, openModal, etc.)
└── docs/
    ├── index.html         # Component catalog/preview page
    └── README.md          # Usage documentation
```

---

## Phase 1: Design Tokens Extraction

Extract CSS variables from [styles.css](mcp-servers/dashboard/public/styles.css) lines 1-69 into `tokens.css`:

- Color palette (backgrounds, text, accents, status colors)
- Typography (font families, sizes)
- Spacing scale
- Border radii
- Shadows
- Motion/transitions

---

## Phase 2: Base Styles

Create `base.css` with:

- CSS reset (already have box-sizing, margin/padding reset)
- Typography defaults
- Utility classes (`.hidden`, `.truncate`, `.visually-hidden`)
- Animation keyframes (pulse, slide-in, fade, etc.)

---

## Phase 3: Component Modules

Extract and organize by component type:

| Module | Source Lines (approx) | Key Classes |
|--------|----------------------|-------------|
| `buttons.css` | ~100 lines | `.btn`, `.action-btn`, `.filter-btn`, `.status-btn` |
| `cards.css` | ~150 lines | `.stat-card`, `.queue-item`, `.panel-section` |
| `modals.css` | ~200 lines | `.modal-overlay`, `.modal`, `.modal-header/body/footer` |
| `toasts.css` | ~100 lines | `.toast-container`, `.toast`, `.toast-success/error/info` |
| `sidebar.css` | ~300 lines | `.sidebar`, `.tree-nav`, `.tree-item`, `.brand` |
| `forms.css` | ~80 lines | `.search-box`, input styles, select styles |
| `navigation.css` | ~150 lines | `.site-nav`, `.topbar`, `.breadcrumb`, `.tabs` |
| `charts.css` | ~100 lines | `.chart-container`, progress rings, sparklines |

---

## Phase 4: JavaScript Utilities

Create `ui.js` with programmatic helpers:

```javascript
// Example API
const PyUI = {
  toast(message, type = 'info', duration = 4000),
  modal(options),           // { title, body, actions }
  confirm(message),         // returns Promise<boolean>
  notify(title, message),   // notification panel
  loading(show = true),     // global loading state
};
```

Extract from current [app.js](mcp-servers/dashboard/public/app.js) toast/modal logic.

---

## Phase 5: Documentation

Create `docs/index.html` - a live component catalog showing:

- Color swatches
- Typography samples  
- Button variants
- Card layouts
- Modal examples
- Toast demos

Plus `README.md` with:

- Installation/usage
- CSS variable customization
- JavaScript API reference

---

## Migration Path

After library is created:

1. Update `public/index.html` to import `pyrite-ui.css` instead of `styles.css`
2. Move existing `styles.css` to backup
3. Keep page-specific overrides in a slim `dashboard.css`

---

## Estimated Effort

| Phase | Time |
|-------|------|
| Tokens extraction | 30 min |
| Base styles | 30 min |
| Component modules (8) | 2-3 hours |
| JS utilities | 1 hour |
| Documentation | 1-2 hours |
| **Total** | **5-7 hours** |

---

## Key Files to Modify/Create

**Create:**
- `mcp-servers/dashboard/lib/pyrite-ui/` (entire directory)

**Modify:**
- [public/index.html](mcp-servers/dashboard/public/index.html) - update CSS imports
- [public/app.js](mcp-servers/dashboard/public/app.js) - extract UI helpers

**Preserve:**
- [public/styles.css](mcp-servers/dashboard/public/styles.css) - keep as backup initially