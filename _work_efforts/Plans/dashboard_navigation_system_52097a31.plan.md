---
name: Dashboard Navigation System
overview: Add a consistent navigation bar across the Mission Control dashboard and docs page, using the amber/orange theme from the dashboard, with mobile-responsive hamburger menu support.
todos:
  - id: add-nav-css
    content: Add site navigation CSS to styles.css with responsive breakpoints
    status: pending
  - id: update-dashboard-html
    content: Add site nav to index.html, remove redundant docs link from topbar
    status: pending
  - id: update-docs-html
    content: Update docs/index.html to use shared styles and site nav, convert to amber theme
    status: pending
  - id: add-nav-js
    content: Add minimal JS for mobile menu toggle to both pages
    status: pending
  - id: test-navigation
    content: Test navigation on both pages in browser
    status: pending
---

# Mission Control Site Navigation

## Overview

Add a unified navigation system across the dashboard and docs pages using the existing amber/orange command center theme. The nav will appear at the top of both pages with consistent branding, links, and mobile responsiveness.

## Architecture

```mermaid
flowchart LR
    subgraph SharedNav[Shared Navigation]
        Logo[Brand Logo]
        NavLinks[Dashboard | Docs | Status]
        MobileToggle[Hamburger Menu]
    end
    
    subgraph Pages[Pages]
        Dashboard[index.html]
        Docs[docs/index.html]
        Future[Future Pages]
    end
    
    SharedNav --> Dashboard
    SharedNav --> Docs
    SharedNav --> Future
```

## Files to Modify

| File | Changes |
|------|---------|
| [`public/styles.css`](mcp-servers/dashboard/public/styles.css) | Add site nav styles (~80 lines) |
| [`public/index.html`](mcp-servers/dashboard/public/index.html) | Add site nav above `.app`, minor restructure |
| [`public/docs/index.html`](mcp-servers/dashboard/public/docs/index.html) | Replace inline header, link to `../styles.css`, add nav |

## Implementation Details

### 1. Site Navigation Structure (HTML)

Both pages will include this nav structure at the top of `<body>`:

```html
<nav class="site-nav">
  <div class="site-nav-inner">
    <a href="/" class="site-nav-brand">
      <span class="nav-gem">◈</span>
      <span class="nav-brand-text">_pyrite</span>
    </a>
    <button class="site-nav-toggle" aria-label="Toggle menu">☰</button>
    <ul class="site-nav-links">
      <li><a href="/" class="nav-link">Dashboard</a></li>
      <li><a href="/docs/" class="nav-link">Docs</a></li>
      <li><a href="/api/health" class="nav-link nav-status">
        <span class="nav-status-dot"></span>API
      </a></li>
    </ul>
  </div>
</nav>
```

### 2. CSS Additions to `styles.css`

Add site-nav styles using existing CSS variables:
- Fixed/sticky nav bar with `--bg-primary` background
- Brand logo with amber gem icon
- Nav links with hover states matching existing patterns
- Mobile hamburger toggle below 768px
- Smooth transitions using `--transition-fast`

### 3. Dashboard Changes (`index.html`)

- Add site nav before the `.app` container
- Remove redundant "Docs" link from topbar (line 115) since it's now in site nav
- Keep topbar for breadcrumbs, notifications, view toggles (contextual controls)
- Add `active` class to Dashboard nav link

### 4. Docs Page Changes (`docs/index.html`)

- Link to `../styles.css` for shared nav styles
- Keep doc-specific styles inline (code blocks, server cards, etc.)
- Replace standalone `<header>` with site nav
- Move "Copy AI Docs" button into page content area
- Add `active` class to Docs nav link
- Update color variables to match amber theme

### 5. Mobile Behavior

- Below 768px: hamburger icon replaces inline nav links
- Click toggles a dropdown menu
- Uses existing mobile overlay pattern from dashboard
- Touch-friendly 44px tap targets

## Visual Hierarchy

```
+----------------------------------------------------------+
| ◈ _pyrite     [Dashboard]  [Docs]  [●API]        [☰]     |  <- Site Nav (shared)
+----------------------------------------------------------+
| [◂] _pyrite MISSION CONTROL  |  Search...  |  + Add Repo |  <- Sidebar (dashboard only)
|     Work Effort Command...   |             |             |
|------------------------------|-------------|-------------|
|  Topbar: Breadcrumb          |  Notif  Doc |  View Toggle|  <- Topbar (dashboard only)
+----------------------------------------------------------+
```

## Key Decisions

1. **Keep topbar separate from site nav**: The topbar contains contextual controls (breadcrumbs, notifications, view toggle) that are dashboard-specific
2. **API Status link**: Points to `/api/health` with a live status dot indicator
3. **Docs theme update**: Docs page will adopt amber accent to match dashboard
4. **Minimal JS**: Toggle logic only, no complex state management
