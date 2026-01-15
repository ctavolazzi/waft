---
name: Starlight Architecture Audit
overview: Comprehensive audit of the howtowincapitalism Starlight project, starting with site architecture and design philosophy analysis, then evaluating configuration compliance and identifying necessary adjustments.
todos:
  - id: decision-sidebar
    content: "DECISION REQUIRED: Choose sidebar strategy (A: keep hidden, B: enable, C: use splash template)"
    status: completed
  - id: decision-header
    content: "DECISION REQUIRED: Header override file - register it or delete it?"
    status: completed
  - id: fix-tagline
    content: Remove invalid `tagline` option from astro.config.mjs
    status: completed
  - id: fix-description
    content: Add global `description` to starlight config
    status: completed
  - id: fix-viewport
    content: Remove redundant viewport meta tag
    status: completed
  - id: fix-dns-prefetch
    content: Remove unnecessary dns-prefetch for Google Fonts
    status: completed
  - id: fix-sidebar-slug
    content: "Consider: Update sidebar to use `slug` instead of `link`"
    status: completed
  - id: verify-build
    content: Run build and verify all changes
    status: completed

category: dreams
confidence: 0.50
constellation_date: 2026-01-14
---

# Starlight Site Architecture & Configuration Audit

## Part 1: Site Design & Architecture Analysis

### 1.1 Site Type Classification

**Your Site Type:** Wikipedia-style financial wiki (not traditional documentation)

| Aspect | Traditional Docs Site | Your Site |

|--------|----------------------|-----------|

| Purpose | Software documentation | Educational wiki |

| Navigation | Sidebar-driven | Minimal header nav |

| Design | Default Starlight | Custom Wikipedia aesthetic |

| Theme | Light/dark toggle | Light-only |

| Layout | Sidebar + TOC + content | Content-focused, no sidebar |

**Assessment:** You're using Starlight as a foundation but heavily customizing it for a wiki-style experience. This is a valid but unconventional use case.

---

### 1.2 Starlight Feature Usage Matrix

| Starlight Feature | Status | Implementation |

|-------------------|--------|----------------|

| Content Collections | USING | `docsLoader()` + `docsSchema()` with extensions |

| Sidebar Navigation | DISABLED | Hidden via CSS, custom header nav instead |

| Table of Contents | USING | Enabled on content pages |

| Search (Pagefind) | USING | Default search in header |

| Theme Toggle | DISABLED | Overridden with `ForceLightTheme.astro` |

| Pagination | DISABLED | `pagination: false` |

| Last Updated | DISABLED | `lastUpdated: false` |

| Edit Links | NOT CONFIGURED | Could enable for contributions |

| i18n | NOT USING | Single language (English) |

| Built-in Components | PARTIALLY USING | Steps, Tabs, Aside imported |

| Hero Component | USING | On index page via frontmatter |

---

### 1.3 Component Override Analysis

**Currently Overridden:**

| Component | Override | Purpose |

|-----------|----------|---------|

| `ThemeProvider` | `ForceLightTheme.astro` | Force light-only mode |

| `ThemeSelect` | `Empty.astro` | Hide theme toggle |

| `Footer` | Custom `Footer.astro` | Wikipedia-style footer |

**Exists But NOT Registered:**

| Component | Location | Status |

|-----------|----------|--------|

| `Header` | `src/components/overrides/Header.astro` | File exists but NOT in config |

**Question:** Should the Header override be activated, or is it legacy code?

---

### 1.4 CSS Architecture Analysis

**Approach:** Custom CSS overriding Starlight's design system

**What's Being Overridden:**

```css
/* Color system - forcing light mode colors for both themes */
:root, :root[data-theme="light"], :root[data-theme="dark"] {
  --sl-color-white: #ffffff;
  --sl-color-gray-1: #f8f9fa;
  /* ... Wikipedia-inspired palette ... */
}

/* Layout - hiding Starlight's sidebar */
nav[aria-label="Main"], .sidebar {
  display: none;
}
```

**Implications:**

- Sidebar is hidden globally via CSS (not conditionally)
- Both light and dark themes forced to same colors
- Typography uses serif fonts (Wikipedia style)

---

### 1.5 Content Architecture

**Directory Structure:**

```
src/content/docs/
├── index.mdx              # Homepage (splash template)
├── protocol/              # Core concepts (10 pages)
├── field-notes/           # Updates & guides (4 pages)
└── reports/               # Templates & checklists (4 pages)
```

**Frontmatter Patterns:**

```yaml
# Extended schema fields (custom)
category: concept | tool | framework | guide | reference
difficulty: beginner | intermediate | advanced
readTime: "6 min"

# Standard Starlight fields
title: Required
description: Used for SEO
sidebar:
  order: 1
  badge: New
template: splash  # Only on index
```

---

## Part 2: Architecture Decision Evaluation

### 2.1 Is Starlight the Right Tool?

| Requirement | Starlight Fit | Notes |

|-------------|---------------|-------|

| Static site generation | Excellent | Built for this |

| Markdown/MDX content | Excellent | Core feature |

| Built-in search | Good | Pagefind works well |

| Wikipedia-style design | Requires customization | Heavy CSS overrides needed |

| No sidebar | Against defaults | Hiding core navigation feature |

| Light-only theme | Requires override | Disabling core feature |

**Verdict:** Starlight CAN work for this use case, but you're fighting against several default behaviors. Two paths forward:

**Path A: Embrace Starlight Conventions**

- Use sidebar navigation (it's what Starlight does best)
- Enable light/dark theme
- Less custom CSS, more config

**Path B: Continue Custom Approach (Current)**

- Accept you're using ~40% of Starlight
- Maintain heavier customizations
- Consider if a simpler Astro template would be easier

---

### 2.2 Sidebar Strategy Decision

**Current Approach:**

- Sidebar hidden via CSS
- Custom header navigation with 4 links
- Config sidebar has 4 items (matching header)

**Problem:** The config sidebar (`astro.config.mjs` lines 64-69) isn't being displayed, so its configuration is partially wasted.

**Options:**

| Option | Pros | Cons |

|--------|------|------|

| A: Enable sidebar | Better navigation, Starlight-native | Changes site design significantly |

| B: Keep sidebar hidden | Maintains wiki aesthetic | Sidebar config serves limited purpose |

| C: Use `template: splash` on all pages | Proper way to hide sidebar | May affect other layout elements |

---

### 2.3 Theme Strategy Evaluation

**Current:** Force light-only via ThemeProvider override

**Is This Correct?**

- Your Wikipedia aesthetic is light-background focused
- Forcing light mode is a valid design choice
- Implementation works but is unconventional

**Alternative Approaches:**

| Approach | Implementation |

|----------|----------------|

| Current (ThemeProvider override) | Works, but hacky |

| CSS-only | Override `[data-theme="dark"]` to match light |

| Starlight config | No built-in "disable dark mode" option |

**Assessment:** Your current approach is reasonable given Starlight doesn't have a native "light-only" config option.

---

## Part 3: Visual/UI Issues (Priority)

### 3.0 Immediate Visual Problems

**Issue A: Blue Site Title**

- **Cause:** `custom.css` line 59-61 sets all links blue:
  ```css
  a {
    color: var(--color-link);
  }
  ```

- **Effect:** Site title in header is an `<a>` tag, becomes blue
- **Fix:** Add specific override for site title:
  ```css
  /* Site title should be dark, not link blue */
  .site-title a,
  header a[href="/"] {
    color: var(--sl-color-black);
  }
  ```


**Issue B: Nearly Invisible Search Icon**

- **Cause:** Search icon uses `--sl-color-gray-5` (`#72777d`) which has low contrast
- **Fix:** Increase search icon contrast:
  ```css
  /* Make search icon more visible */
  [data-search-modal] button,
  .search-button,
  starlight-search button {
    color: var(--sl-color-black);
  }
  ```


---

## Part 4: Configuration Issues

### 4.1 Invalid/Unnecessary Config

| Issue | Priority | Location | Fix |

|-------|----------|----------|-----|

| `tagline` not a valid option | Medium | `astro.config.mjs:22` | Remove line |

| Redundant viewport meta | Low | `astro.config.mjs:42` | Remove (Astro handles this) |

| DNS prefetch for unused resource | Low | `astro.config.mjs:32` | Remove (not using Google Fonts) |

### 3.2 Missing Recommended Config

| Setting | Current | Recommended | Why |

|---------|---------|-------------|-----|

| `description` | Not set | Add `SITE_DESCRIPTION` | Better SEO defaults |

### 3.3 Suboptimal Config

| Issue | Current | Better | Why |

|-------|---------|--------|-----|

| Sidebar items | Using `link` | Use `slug` | Better Starlight integration, auto-titles |

### 3.4 Dead/Unused Code

| Item | Location | Action |

|------|----------|--------|

| Header override | `src/components/overrides/Header.astro` | Either register in config OR delete |

---

## Part 4: Recommendations

### Critical Decision Required

Before implementing fixes, decide on **Sidebar Strategy**:

**Option A: Keep Current (Wiki-style, no sidebar)**

- Continue hiding sidebar via CSS
- Accept current limitations
- Apply only config fixes

**Option B: Embrace Sidebar**

- Remove CSS that hides sidebar
- Let Starlight show sidebar navigation
- Gains: better navigation, mobile menu, breadcrumbs
- Loses: Wikipedia minimalist aesthetic

**Option C: Use `template: splash` Properly**

- Add `template: splash` to all page frontmatters
- Properly disable sidebar per-page instead of CSS hack
- More Starlight-compliant approach

---

### Recommended Fixes (Regardless of Strategy)

1. Remove invalid `tagline` config option
2. Add global `description` to starlight config
3. Remove redundant viewport meta tag
4. Remove unnecessary dns-prefetch
5. Decide: Register Header override OR delete file
6. Consider: Change sidebar to use `slug` instead of `link`

---

## Part 5: Verification Checklist

After changes:

- [ ] `npm run build` completes without warnings
- [ ] All pages render correctly
- [ ] Search still works
- [ ] No duplicate meta tags in HTML source
- [ ] Navigation works on mobile
- [ ] Theme stays light-only