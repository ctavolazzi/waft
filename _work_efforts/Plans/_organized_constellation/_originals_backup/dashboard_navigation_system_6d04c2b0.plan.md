---
name: Dashboard Navigation System
overview: Add a consistent navigation bar across the Mission Control dashboard and docs page, integrating carefully with the existing layout and using a shared JavaScript module for mobile toggle behavior.
todos:
  - id: add-nav-css
    content: Add site nav and docs page styles to styles.css (~300 lines)
    status: pending
  - id: create-nav-js
    content: Create nav.js with mobile toggle and API status check
    status: pending
  - id: update-dashboard-html
    content: Add site nav, simplify sidebar, remove duplicate docs links, adjust .app height
    status: pending
    dependencies:
      - add-nav-css
      - create-nav-js
  - id: update-docs-html
    content: "Restructure docs page: external CSS, site nav, body class, remove inline styles"
    status: pending
    dependencies:
      - add-nav-css
      - create-nav-js
  - id: test-browser
    content: Test both pages in browser for layout, navigation, and responsiveness
    status: pending
    dependencies:
      - update-dashboard-html
      - update-docs-html
---

# Mission Control Site Navigation (Revised)

## Problem Statement

Currently, there's no way to navigate between pages:
- Dashboard at `/` has links to docs but docs has no way back
- No consistent header/branding across pages
- Docs page uses a different color theme (cyan vs amber)

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Nav placement | Above `.app` container | Keeps existing layout intact, just needs height adjustment |
| Sidebar branding | Simplify to gem icon only | Avoids duplicate branding with site nav |
| Docs styling | Move to `styles.css` with `.docs-page` scoping | Single source of truth, easier maintenance |
| API Status link | Visual indicator only, no link | Page doesn't exist yet; indicator shows server is running |
| Mobile toggle | Shared `nav.js` file | DRY principle |
| Active state | CSS class `.nav-link-active` set in HTML | Simple, no JS needed |

## Layout Integration

### Current Dashboard Structure
```
body
└── .app (flex, 100vh)
    ├── .sidebar
    └── .main-content
```

### New Structure
```
body
├── .site-nav (height: 48px, fixed or static)
└── .app (flex, calc(100vh - 48px))
    ├── .sidebar
    └── .main-content
```

## Files to Modify

| File | Changes |
|------|---------|
| [`styles.css`](mcp-servers/dashboard/public/styles.css) | Add site nav CSS (~100 lines), add docs page styles (~200 lines), adjust .app height |
| [`index.html`](mcp-servers/dashboard/public/index.html) | Add site nav, simplify sidebar header, remove topbar/footer docs links |
| [`docs/index.html`](mcp-servers/dashboard/public/docs/index.html) | Complete restructure: link to `../styles.css`, add site nav, add `.docs-page` body class |
| [`nav.js`](mcp-servers/dashboard/public/nav.js) | New file: mobile toggle logic (~30 lines) |

## Implementation Details

### 1. Site Navigation HTML

```html
<nav class="site-nav">
  <a href="/" class="site-nav-brand">
    <span class="site-nav-gem">◈</span>
    <span class="site-nav-text">_pyrite</span>
  </a>
  
  <ul class="site-nav-links" id="siteNavLinks">
    <li><a href="/" class="site-nav-link site-nav-link-active">Dashboard</a></li>
    <li><a href="/docs/" class="site-nav-link">Docs</a></li>
    <li>
      <span class="site-nav-status" title="Server Status">
        <span class="site-nav-status-dot" id="apiStatusDot"></span>
        <span class="site-nav-status-text">API</span>
      </span>
    </li>
  </ul>
  
  <button class="site-nav-toggle" id="siteNavToggle" aria-label="Toggle navigation">
    <span class="site-nav-toggle-icon">☰</span>
  </button>
</nav>
```

### 2. CSS Architecture

Add to `styles.css`:

```css
/* Site Navigation - Shared across all pages */
.site-nav { ... }

/* Docs Page Specific Styles */
.docs-page .container { ... }
.docs-page .server-card { ... }
/* etc. */
```

Key CSS considerations:
- Site nav uses existing `--bg-primary`, `--accent`, `--border` variables
- 48px height to match topbar visual weight
- Mobile breakpoint at 640px (consistent with existing responsive design)
- Status dot animates to show API health (fetch on load)

### 3. Sidebar Header Simplification

**Before:**
```html
<div class="brand">
  <div class="brand-logo">
    <span class="brand-gem">◈</span>
  </div>
  <div class="brand-text">
    <span class="brand-prefix">_pyrite</span>
    <span class="brand-name">MISSION CONTROL</span>
  </div>
</div>
```

**After:**
```html
<div class="sidebar-brand">
  <span class="sidebar-gem">◈</span>
</div>
```

The tagline "Work Effort Command Center" moves to site nav or is removed.

### 4. Docs Page Migration

The docs page needs significant restructuring:

1. Remove all inline `<style>` content
2. Add `<link rel="stylesheet" href="../styles.css">`
3. Add `class="docs-page"` to `<body>`
4. Add site nav at top
5. Move "Copy AI Docs" button into a toolbar below nav

Color migration from cyan to amber:
- `--accent: #22d3ee` → `--accent: #ff9d3d`
- `--accent-dim: #0891b2` → `--accent-dim: rgba(255, 157, 61, 0.15)`
- All button hovers, badges, and highlights update automatically via variables

### 5. Mobile Behavior

```
Desktop (>640px):     [◈ _pyrite]  [Dashboard] [Docs] [●API]
Mobile (≤640px):      [◈ _pyrite]                      [☰]
                       ┌─────────────────┐
Mobile expanded:       │ Dashboard       │
                       │ Docs            │
                       │ ● API Online    │
                       └─────────────────┘
```

### 6. nav.js Implementation

```javascript
// Mobile nav toggle
const toggle = document.getElementById('siteNavToggle');
const links = document.getElementById('siteNavLinks');
toggle?.addEventListener('click', () => {
  links.classList.toggle('site-nav-links-open');
  toggle.setAttribute('aria-expanded', 
    links.classList.contains('site-nav-links-open'));
});

// API status check
fetch('/api/health')
  .then(r => r.ok ? 'online' : 'offline')
  .catch(() => 'offline')
  .then(status => {
    document.getElementById('apiStatusDot')
      ?.classList.add(`status-${status}`);
  });
```

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Breaking dashboard layout | Test height calc on multiple viewport sizes |
| CSS specificity conflicts | Use `.docs-page` scoping for doc styles |
| Missing functionality after restructure | Keep all existing JS includes |
| Theme inconsistency | Use CSS variables exclusively |

## Testing Checklist

- [ ] Dashboard loads correctly with nav
- [ ] Docs page loads correctly with nav  
- [ ] Nav links work in both directions
- [ ] Mobile toggle works on both pages
- [ ] API status dot shows green when server running
- [ ] All existing dashboard functionality still works
- [ ] Responsive at 640px, 768px, 1024px breakpoints
