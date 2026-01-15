---
name: Button Padding Fix
overview: Fix buttons having zero padding due to size class rendering as "3" instead of "md"
todos:
  - id: fix-liquid-template
    content: Change single quotes to double quotes in button.html size default
    status: completed
  - id: add-fallback-padding
    content: Add default padding to base .cfl-btn class as safety net
    status: completed
---

# Fix Button Padding - Root Cause Found

## Problem

The rendered HTML shows `cfl-btn--3` instead of `cfl-btn--md`:

```html
<a class="cfl-btn cfl-btn--primary cfl-btn--3" href="#">Primary</a>
```

There is NO CSS for `.cfl-btn--3`, so buttons get `padding: 0` from the global reset on line 35.

## Solution (Two Parts)

### 1. Fix the Liquid template (likely root cause)

In [_includes/components/button.html](_includes/components/button.html) line 3, change single quotes to double quotes:

```liquid
<!-- Before -->
{% assign size = include.size | default: 'md' %}

<!-- After -->
{% assign size = include.size | default: "md" %}
```

### 2. Add fallback padding to base class (safety net)

In [assets/css/main.css](assets/css/main.css) around line 608, add padding to base `.cfl-btn`:

```css
.cfl-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    font-family: system-ui, -apple-system, sans-serif;
    font-weight: 600;
    text-decoration: none;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.15s ease;
    white-space: nowrap;
    padding: 0.6rem 1.5rem;  /* ADD THIS LINE */
}
```

This ensures buttons always have padding even if size class fails.