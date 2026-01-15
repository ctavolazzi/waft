---
name: Fix Footer Links
overview: Fix broken footer navigation links and standardize the home page auth script pattern. Quick win with high impact.
todos:
  - id: fix-footer-links
    content: Update navLinks and resourceLinks arrays in Footer.astro to point to correct routes
    status: completed
  - id: home-domcontentloaded
    content: Wrap auth check script in index.astro with DOMContentLoaded
    status: completed

category: dreads
confidence: 0.79
constellation_date: 2026-01-14
---

# Fix Footer Links and Home Page Pattern

## Problem

The footer component has broken navigation links pointing to non-existent routes. This causes 404 errors when users click footer links.

## Changes

### 1. Fix Footer Navigation Links

**File:** [`src/components/organisms/Footer.astro`](src/components/organisms/Footer.astro)

**Current (broken):**
```astro
const navLinks = [
  { label: 'Home', href: '/' },
  { label: 'Introduction', href: '/protocol/introduction/' },
  { label: 'Decision Matrix', href: '/protocol/decision-matrix/' },
  { label: 'Latest Updates', href: '/field-notes/latest/' },
  { label: 'Reports', href: '/reports/' },  // doesn't exist
];

const resourceLinks = [
  { label: 'About This Wiki', href: '/about/' },  // doesn't exist
  { label: 'Contributing', href: '/contributing/' },  // doesn't exist
  { label: 'Disclaimer', href: '/disclaimer/' },
];
```

**Fixed:**
```astro
const navLinks = [
  { label: 'Home', href: '/' },
  { label: 'Introduction', href: '/faq/introduction/' },
  { label: 'Decision Matrix', href: '/faq/decision-matrix/' },
  { label: 'Latest Updates', href: '/notes/latest/' },
];

const resourceLinks = [
  { label: 'Disclaimer', href: '/disclaimer/' },
  { label: 'Privacy', href: '/privacy/' },
  { label: 'Terms', href: '/terms/' },
];
```

### 2. Add DOMContentLoaded to Home Page (Consistency)

**File:** [`src/pages/index.astro`](src/pages/index.astro)

Wrap the auth check script in DOMContentLoaded for consistency with other components (works now by luck, but should follow established pattern).

## Scope

- Fix 5 broken links in footer
- Remove links to non-existent pages (About, Contributing, Reports)
- Add links to existing pages (Privacy, Terms)
- Apply DOMContentLoaded pattern to home page

## Not in Scope

- Creating missing pages (/about, /contributing, /reports) - separate task
- Any visual changes to footer layout