---
name: Design Overhaul
overview: Transform the CFL Wiki into a visually striking, feature-rich site with animated marquee, card layouts, micro-interactions, and modern design patterns.
todos:
  - id: create-marquee
    content: Create animated marquee banner with recent pages
    status: completed
  - id: create-cards
    content: Build card-based wiki listing with hover effects
    status: completed
    dependencies:
      - create-marquee
  - id: add-hero
    content: Add hero section to homepage
    status: completed
    dependencies:
      - create-cards
  - id: micro-interactions
    content: Add animations and micro-interactions
    status: completed
    dependencies:
      - add-hero
  - id: enhance-nav-footer
    content: Sticky nav, enhanced footer with social links
    status: completed
    dependencies:
      - micro-interactions
  - id: test-commit
    content: Test all features and commit
    status: completed
    dependencies:
      - enhance-nav-footer
---

# CFL Wiki Design Overhaul

## New Features

### 1. Animated Marquee Banner
- Scrolling ticker at the top showing recently updated pages
- Uses Jekyll's `site.wiki | sort: 'date' | reverse` to get recent changes
- CSS animation for smooth infinite scroll
- Click to navigate to page

### 2. Card-Based Wiki Listing
- Replace boring `<ul>` list with visual cards
- Each card shows: title, description (first 100 chars), last updated date
- Hover effect with subtle lift and glow
- Grid layout that adapts to screen size

### 3. Hero Section (Homepage)
- Large welcome banner with gradient background
- CFL logo/branding
- Quick stats (number of wiki pages, etc.)
- Call-to-action button

### 4. Micro-Interactions
- Link hover: underline animation slides in
- Button hover: slight scale + glow
- Card hover: lift shadow + border glow
- Page load: content fades in with stagger

### 5. Enhanced Navigation
- Sticky header on scroll
- Active page indicator
- Animated hamburger menu on mobile

### 6. Visual Enhancements
- Gradient accents (orange to amber)
- Subtle grid/dot pattern background
- Better code syntax highlighting colors
- Smooth scroll behavior

### 7. Footer Upgrade
- Social links (Discord, GitHub)
- Quick links section
- "Built with Jekyll" badge

## Files to Create/Modify

| File | Changes |
|------|---------|
| `_layouts/default.html` | Add marquee, hero, sticky nav, footer links |
| `_includes/marquee.html` | New - reusable marquee component |
| `_includes/card.html` | New - wiki page card component |
| `assets/css/main.css` | Animations, cards, gradients, micro-interactions |
| `index.html` | Hero section, card grid layout |

## Technical Notes

- Pure CSS animations (no JS dependencies for marquee)
- CSS Grid for card layout
- CSS custom properties for easy theming
- `@keyframes` for marquee scroll
- `transition` for hover effects
- `animation-delay` for staggered entrance