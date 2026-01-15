---
name: Dashboard Navigation System
overview: Add a unified navigation system across dashboard and docs, solving the two-hamburger problem by integrating site nav into the dashboard's existing mobile sidebar, while giving docs its own mobile dropdown.
todos:
  - id: add-site-nav-css
    content: Add site navigation CSS to styles.css (~80 lines)
    status: completed
  - id: update-dashboard
    content: Add site nav to index.html, add nav links to sidebar, simplify header, adjust heights
    status: completed
    dependencies:
      - add-site-nav-css
  - id: update-docs
    content: Add site nav to docs/index.html, add fonts link, update colors to amber
    status: completed
    dependencies:
      - add-site-nav-css
  - id: test-desktop
    content: "Test both pages on desktop: nav links, active states, layout"
    status: completed
    dependencies:
      - update-dashboard
      - update-docs
  - id: test-mobile
    content: "Test both pages at 768px and below: hamburger behavior, touch targets"
    status: completed
    dependencies:
      - update-dashboard
      - update-docs

category: hopes
confidence: 0.39
constellation_date: 2026-01-14
---

# Mission Control Site Navigation (Final Revision)

## Critical Issues Addressed

| Issue | Solution |
|-------|----------|
| Two hamburger menus on mobile | Dashboard: site nav links go INTO sidebar; Docs: separate dropdown |
| Over-engineering | Keep docs inline styles, only add shared nav CSS |
| Font mismatch | Add Google Fonts link to docs page |
| Inconsistent breakpoints | Standardize on 768px everywhere |

## Mobile Strategy

```
DASHBOARD MOBILE:
┌─────────────────────────────┐
│ [☰] ◈ _pyrite               │  ← Single hamburger (existing)
├─────────────────────────────┤
│ ┌─ Sidebar ──────────────┐  │
│ │ Dashboard  Docs  ●API  │  │  ← Site nav links AT TOP of sidebar
│ │ ─────────────────────  │  │
│ │ Search...              │  │
│ │ Repository tree...     │  │
│ └────────────────────────┘  │
└─────────────────────────────┘

DOCS PAGE MOBILE:
┌─────────────────────────────┐
│ ◈ _pyrite              [☰] │  ← Site nav with its own hamburger
├─────────────────────────────┤
│ ┌─ Dropdown ─────────────┐  │
│ │ Dashboard              │  │
│ │ Docs ✓                 │  │
│ │ ● API Online           │  │
│ └────────────────────────┘  │
└─────────────────────────────┘
```

This means: **ONE hamburger per page, consistent behavior.**

## Desktop Layout

```
DASHBOARD:
┌────────────────────────────────────────────────────────────┐
│ ◈ _pyrite    [Dashboard]  [Docs]  [●API]                   │  ← Site nav (48px)
├────────────────────────────────────────────────────────────┤
│ SIDEBAR     │  TOPBAR: breadcrumb, notifs, view toggle     │
│ (simplified │  ───────────────────────────────────────────  │
│  no brand)  │  Main content area...                        │
└────────────────────────────────────────────────────────────┘

DOCS PAGE:
┌────────────────────────────────────────────────────────────┐
│ ◈ _pyrite    [Dashboard]  [Docs ✓]  [●API]  [Copy AI Docs] │  ← Site nav
├────────────────────────────────────────────────────────────┤
│                                                            │
│     Centered docs content (existing layout)...             │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Files to Modify

| File | Lines Changed | Changes |
|------|---------------|---------|
| [`styles.css`](mcp-servers/dashboard/public/styles.css) | +80 | Site nav styles only |
| [`index.html`](mcp-servers/dashboard/public/index.html) | +15, -10 | Add site nav, move nav links to sidebar for mobile |
| [`docs/index.html`](mcp-servers/dashboard/public/docs/index.html) | +40, -10 | Add site nav, Google Fonts, keep inline styles |

**No new JS file needed** - we'll add minimal toggle logic inline (< 10 lines each page).

## Implementation Details

### 1. Site Nav CSS (add to styles.css)

```css
/* ============================================================
   Site Navigation - Shared Header
   ============================================================ */
.site-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 48px;
  padding: 0 var(--space-md);
  background: var(--bg-deep);
  border-bottom: 1px solid var(--border);
  position: relative;
  z-index: 200;
}

.site-nav-brand { /* ... */ }
.site-nav-links { /* ... */ }
.site-nav-link { /* ... */ }
.site-nav-link-active { /* ... */ }
.site-nav-status { /* ... */ }
.site-nav-toggle { display: none; } /* Hidden on desktop */

@media (max-width: 768px) {
  /* Dashboard: hide site nav links (they're in sidebar) */
  .has-sidebar .site-nav-links { display: none; }
  .has-sidebar .site-nav-toggle { display: none; }
  
  /* Docs: show mobile toggle, hide links until opened */
  .docs-page .site-nav-toggle { display: flex; }
  .docs-page .site-nav-links { /* dropdown styles */ }
  .docs-page .site-nav-links.open { display: flex; }
}
```

### 2. Dashboard Changes (index.html)

**Add at top of body:**
```html
<body class="has-sidebar">
  <nav class="site-nav">
    <a href="/" class="site-nav-brand">
      <span class="site-nav-gem">◈</span>
      <span class="site-nav-text">_pyrite</span>
    </a>
    <ul class="site-nav-links">
      <li><a href="/" class="site-nav-link site-nav-link-active">Dashboard</a></li>
      <li><a href="/docs/" class="site-nav-link">Docs</a></li>
      <li class="site-nav-status"><span class="status-dot"></span>API</li>
    </ul>
  </nav>
  <!-- existing .app container -->
```

**Add to sidebar (for mobile):**
```html
<div class="sidebar-nav-links">
  <a href="/" class="sidebar-nav-link active">Dashboard</a>
  <a href="/docs/" class="sidebar-nav-link">Docs</a>
</div>
```

**Simplify sidebar header:** Remove duplicate `_pyrite MISSION CONTROL` text, keep gem icon.

**Adjust .app height:**
```css
.app {
  height: calc(100vh - 48px); /* Account for site nav */
}
```

**Remove:** Topbar "📚 Docs" link (line 115), footer docs link.

### 3. Docs Page Changes (docs/index.html)

**Add to head:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../styles.css">
```

**Update body:**
```html
<body class="docs-page">
  <nav class="site-nav">
    <!-- Same structure, but Docs link has active class -->
    <button class="site-nav-toggle" id="navToggle">☰</button>
  </nav>
  
  <div class="container">
    <!-- existing content, move header content here -->
```

**Keep inline styles** but update colors:
```css
:root {
  --accent: #ff9d3d;      /* Was #22d3ee */
  --accent-dim: #b36d2a;  /* Was #0891b2 */
  /* ... other amber values */
}
```

**Add toggle script at bottom:**
```html
<script>
  document.getElementById('navToggle')?.addEventListener('click', function() {
    document.querySelector('.site-nav-links').classList.toggle('open');
  });
</script>
```

## Breakpoint Standardization

All responsive behavior uses **768px** consistently:
- Site nav mobile toggle: 768px
- Dashboard sidebar collapse: 768px  
- Docs page responsive: 768px

## Testing Checklist

- [ ] Dashboard desktop: site nav visible with all links
- [ ] Dashboard mobile: single hamburger, nav links in sidebar
- [ ] Docs desktop: site nav visible, "Docs" highlighted as active
- [ ] Docs mobile: hamburger opens dropdown with nav links
- [ ] Navigation works: Dashboard → Docs → Dashboard
- [ ] API status dot shows green (fetches /api/health)
- [ ] Fonts consistent between pages
- [ ] No layout jumps at 768px breakpoint
- [ ] Existing dashboard functionality unbroken