---
name: QoL Improvements - Top 5 Quick Wins
overview: "Implement 5 quick quality-of-life improvements: SEO meta tags, image lazy loading, script defer optimization, custom 404 page, and reading time estimates. These are low-effort, high-impact enhancements that improve SEO, performance, and user experience."
todos:
  - id: seo-meta
    content: Add SEO meta tags - Create _includes/seo.html with meta description, Open Graph, and Twitter Card tags, integrate into layout
    status: completed
  - id: image-lazy
    content: Implement image lazy loading - Add loading="lazy" to card and avatar component images
    status: completed
  - id: script-defer
    content: Add defer to scripts - Add defer attribute to fonts.js and main.js script tags for better performance
    status: completed
  - id: 404-page
    content: Create custom 404 page - Build helpful 404.html with search, popular links, and site branding
    status: completed
  - id: reading-time
    content: Add reading time estimates - Create _includes/reading-time.html and display on wiki pages
    status: completed

category: hopes
confidence: 0.70
constellation_date: 2026-01-14
---

# QoL Impro

vements - Top 5 Quick Wins

## Overview

This plan implements 5 quick quality-of-life improvements that provide immediate benefits:

1. **SEO Meta Tags** - Improve search engine visibility and social sharing
2. **Image Lazy Loading** - Reduce initial page load time
3. **Script Defer** - Improve page load performance

4. **Custom 404 Page** - Better user experience for broken links
5. **Reading Time** - Help users estimate reading time for wiki pages

## Current State Analysis

### SEO Meta Tags

- **Current**: Only basic `<title>` tag, no meta description, no Open Graph, no Twitter Cards
- **Location**: `_layouts/default.html` lines 1-14
- **Impact**: Poor social sharing previews, lower SEO scores

### Image Loading

- **Current**: Images load immediately without lazy loading
- **Files**: 
- `_includes/components/card.html` line 15: `<img src="{{ image }}" alt="{{ title | escape }}">`

- `_includes/components/avatar.html` line 11: `<img src="{{ src }}" alt="{{ alt | escape }}" class="cfl-avatar__image">`
- Wiki pages use markdown images: `![alt](url)`

- **Impact**: All images load on initial page load, slowing down performance

### Script Loading

- **Current**: Scripts load without defer attribute

- **Location**: `_layouts/default.html` line 228-229
- **Files**: `assets/js/fonts.js`, `assets/js/main.js`
- **Impact**: Scripts block rendering, even though they're at end of body

### 404 Page

- **Current**: No custom 404 page exists
- **Impact**: Users see generic GitHub Pages 404, poor UX

### Reading Time

- **Current**: No reading time estimates

- **Impact**: Users can't estimate how long content will take to read

## Implementation Plan

### 1. SEO Meta Tags (30 minutes)

**Goal**: Add comprehensive meta tags for SEO and social sharing.

#### Step 1.1: Create SEO Include File

Create `_includes/seo.html` with meta tags:

- Meta description (from page front matter or auto-generated)
- Open Graph tags (og:title, og:description, og:image, og:url, og:type)

- Twitter Card tags (twitter:card, twitter:title, twitter:description)
- Canonical URL

- Site name and description from `_config.yml`

#### Step 1.2: Auto-generate Descriptions

- Use `page.description` from front matter if available

- Fallback: Extract first paragraph from `page.content` (strip HTML, truncate to 160 chars)
- Fallback: Use site description from `_config.yml`

#### Step 1.3: Add to Layout

Include `_includes/seo.html` in `_layouts/default.html` `<head>` section after title tag.

#### Step 1.4: Add Site Description to Config

Add `description` field to `_config.yml`:

```yaml
description: "Community makerspace wiki for Chico Fab Lab - tools, projects, and resources"
```

**Files to create:**

- `_includes/seo.html` - SEO meta tags include

**Files to modify:**

- `_layouts/default.html` - Add seo.html include
- `_config.yml` - Add site description

**Benefits**: Better SEO, improved social sharing previews, higher Lighthouse scores---

### 2. Image Lazy Loading (15 minutes)

**Goal**: Defer loading of images until they're about to enter viewport.

#### Step 2.1: Update Card Component

Add `loading="lazy"` to `<img>` tag in `_includes/components/card.html`:

```liquid
<img src="{{ image }}" alt="{{ title | escape }}" loading="lazy">
```



#### Step 2.2: Update Avatar Component

Add `loading="lazy"` to `<img>` tag in `_includes/components/avatar.html`:

```liquid
<img src="{{ src }}" alt="{{ alt | escape }}" class="cfl-avatar__image" loading="lazy">
```



#### Step 2.3: Add Width/Height to Prevent Layout Shift

For card images, add width/height attributes if available in front matter, or use CSS aspect ratio.

**Note**: Markdown images in wiki pages will need a Jekyll plugin or post-processing. For now, focus on component images.**Files to modify:**

- `_includes/components/card.html` - Add loading="lazy"
- `_includes/components/avatar.html` - Add loading="lazy"

**Benefits**: Faster initial page load, better Core Web Vitals (LCP), reduced bandwidth usage---

### 3. Script Defer Optimization (5 minutes)

**Goal**: Defer non-critical scripts to improve initial page render.

#### Step 3.1: Add Defer to Scripts

Update `_layouts/default.html` script tags:

```html
<script src="{{ site.baseurl }}/assets/js/fonts.js" defer></script>
<script src="{{ site.baseurl }}/assets/js/main.js" defer></script>
```



**Rationale**:

- Both scripts use `DOMContentLoaded` or check `document.readyState`
- They don't need to execute immediately

- Defer ensures scripts download in parallel but execute after HTML parsing

**Files to modify:**

- `_layouts/default.html` - Add defer attribute to script tags

**Benefits**: Faster First Contentful Paint (FCP), better perceived performance---

### 4. Custom 404 Page (30 minutes)

**Goal**: Create helpful 404 page that guides users back to content.

#### Step 4.1: Create 404.html

Create `404.html` in root directory with:

- Friendly error message
- Search functionality (reuse existing search component)
- Links to popular pages (Getting Started, Component Showcase, etc.)

- Link back to homepage
- Same layout and styling as rest of site

#### Step 4.2: Add Helpful Content

- "Page not found" message
- "Maybe you were looking for:" with links to:
- Getting Started
- Component Showcase
- Equipment Guide
- Homepage

- Search bar to help users find what they need
- Fun message that fits site personality

**Files to create:**

- `404.html` - Custom 404 error page

**Benefits**: Better UX for broken links, helps users find content, maintains site branding---

### 5. Reading Time Estimate (30 minutes)

**Goal**: Display estimated reading time for wiki pages.

#### Step 5.1: Create Reading Time Include

Create `_includes/reading-time.html` that:

- Calculates word count from `page.content`
- Assumes average reading speed: 200 words/minute
- Formats as "~X min read" or "Less than 1 min read"

- Handles edge cases (empty content, very short content)

#### Step 5.2: Add to Wiki Page Layout

Include reading time in `_layouts/default.html` for wiki pages:

- Display near page title or in page metadata
- Only show for wiki collection pages
- Style consistently with existing design

#### Step 5.3: Optional: Add to Card Component

Consider adding reading time to card previews on homepage (optional enhancement).**Calculation Logic:**

```liquid
{% assign words = page.content | number_of_words %}
{% assign reading_time = words | divided_by: 200.0 | ceil %}
{% if reading_time < 1 %}
  Less than 1 min read
{% else %}
  ~{{ reading_time }} min read
{% endif %}
```

**Files to create:**

- `_includes/reading-time.html` - Reading time calculation and display

**Files to modify:**

- `_layouts/default.html` - Add reading time display for wiki pages

**Benefits**: Helps users estimate time commitment, improves content discoverability---

## Implementation Order

1. **Script Defer** (5 min) - Quickest win
2. **Image Lazy Loading** (15 min) - Performance boost

3. **SEO Meta Tags** (30 min) - SEO improvement
4. **404 Page** (30 min) - UX improvement
5. **Reading Time** (30 min) - Content enhancement

**Total Estimated Time**: ~2 hours

## Testing Checklist

### SEO Meta Tags

- [ ] Meta description appears in page source
- [ ] Open Graph tags present (test with Facebook Debugger)

- [ ] Twitter Card tags present (test with Twitter Card Validator)
- [ ] Canonical URL correct
- [ ] Social sharing preview works correctly

### Image Lazy Loading

- [ ] Images have `loading="lazy"` attribute
- [ ] Images load as user scrolls (check Network tab)
- [ ] No layout shift when images load

- [ ] Above-the-fold images still load immediately (or use `loading="eager"`)

### Script Defer

- [ ] Scripts have `defer` attribute

- [ ] All functionality still works (sounds, achievements, settings, etc.)
- [ ] No console errors
- [ ] Page renders before scripts execute

### 404 Page

- [ ] Navigate to non-existent URL (e.g., `/wiki/nonexistent`)
- [ ] 404 page displays correctly
- [ ] Search works on 404 page
- [ ] Links to popular pages work

- [ ] Styling matches rest of site

### Reading Time

- [ ] Reading time displays on wiki pages
- [ ] Calculation is accurate (test with known word counts)

- [ ] Handles edge cases (very short/long pages)
- [ ] Styling is consistent
- [ ] Only shows on wiki pages (not homepage)

## Success Criteria

- [ ] All 5 improvements implemented
- [ ] No regressions in existing functionality
- [ ] Lighthouse performance score improved
- [ ] SEO score improved

- [ ] Social sharing previews work correctly
- [ ] 404 page is helpful and branded
- [ ] Reading time estimates are reasonable

## Future Enhancements (Out of Scope)

- Image optimization (WebP conversion, responsive images)

- Service Worker for offline support
- Auto-generated table of contents
- Breadcrumb auto-generation
- Print stylesheet
- Skip to main content link