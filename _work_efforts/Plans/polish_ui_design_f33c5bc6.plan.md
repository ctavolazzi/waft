---
name: Polish UI Design
overview: Polish the existing Wikipedia-inspired design by refining typography, spacing, form inputs, and visual hierarchy - starting with auth pages and then updating app-wide styles.
todos:
  - id: polish-login-form
    content: Polish LoginForm component - refined inputs, shadows, focus states, button styling
    status: completed
  - id: update-login-page
    content: Update login page container styling - better card shadow and spacing
    status: completed
  - id: update-auth-pages
    content: Apply same polish to RegisterForm and ForgotPasswordForm
    status: completed
  - id: add-design-tokens
    content: Add shadow scale and refined surface colors to Base.astro
    status: completed
  - id: polish-header-footer
    content: Refine header and footer styling - subtle shadows, improved hover states
    status: completed
  - id: update-custom-css
    content: Update custom.css with any additional polish and typography refinements
    status: completed
---

# Polish UI Design

## Current State

The app has a functional Wikipedia-inspired look that needs refinement:
- Basic form inputs with minimal styling
- Limited visual hierarchy
- Simple borders without depth
- Functional but plain buttons

## Approach

Keep the Wikipedia aesthetic (serif headings, clean layout, blue links) but add polish through:
- Better typography scale and spacing
- Refined input styling with subtle shadows
- Improved visual hierarchy with cards
- Smoother transitions and focus states

## Phase 1: Auth Pages (Login, Register, Forgot Password)

### 1.1 Improve Login Page Container

Update [src/pages/login/index.astro](src/pages/login/index.astro) and [src/components/auth/LoginForm.astro](src/components/auth/LoginForm.astro):

- Add subtle card shadow for depth
- Improve header spacing
- Refine typography scale
- Better mobile responsiveness

### 1.2 Polish Form Inputs

Update LoginForm styling:
- Add subtle inner shadow on inputs
- Better focus ring (spread, color)
- Improved placeholder styling
- Refined label typography

### 1.3 Button Refinements

- Add subtle hover lift effect
- Better disabled state
- Improved loading state indicator

## Phase 2: App-Wide Polish

### 2.1 Update Base Layout Variables

In [src/layouts/Base.astro](src/layouts/Base.astro):

- Refine color palette (slightly warmer grays)
- Add shadow scale CSS variables
- Improve spacing consistency
- Add subtle surface shadows

### 2.2 Header Polish

- Add subtle bottom shadow on scroll
- Better hamburger menu shadow
- Improved site title hover state

### 2.3 Footer Refinement

- Cleaner disclaimer box styling
- Better visual separation
- Improved link hover states

### 2.4 Component Updates

- Polish WikiBox component
- Refine TopicCard hover states
- Improve Hero section typography

## Key Design Tokens to Add

```css
/* Shadows */
--shadow-xs: 0 1px 2px rgba(0,0,0,0.04);
--shadow-sm: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
--shadow-md: 0 4px 6px rgba(0,0,0,0.05), 0 2px 4px rgba(0,0,0,0.04);

/* Refined surfaces */
--color-surface-elevated: #ffffff;
--color-border-subtle: #e4e7eb;
```

## Files to Modify

1. `src/components/auth/LoginForm.astro` - Form styling
2. `src/pages/login/index.astro` - Page container
3. `src/components/auth/RegisterForm.astro` - Match login styling
4. `src/components/auth/ForgotPasswordForm.astro` - Match login styling
5. `src/layouts/Base.astro` - Global design tokens
6. `src/styles/custom.css` - Additional polish

## Visual Direction

```
Before: Flat, stark borders
After:  Subtle shadows, gentle depth
```

```
Before: #a2a9b1 borders everywhere
After:  Lighter borders (#e4e7eb), shadows for depth
```