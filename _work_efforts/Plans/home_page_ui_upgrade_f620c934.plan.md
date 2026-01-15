# Home Page UI Upgrade

## Current State

- 13 wiki pages in `_wiki/` with only `title` and `order` in frontmatter
- Basic card grid on [index.html](index.html) using [_includes/card.html](_includes/card.html)
- Search component exists at [_includes/components/search.html](_includes/components/search.html) but unused
- Warm theme CSS with cream/coral-red palette

## Changes

### 1. Add Categories to Wiki Pages

Update frontmatter in all 13 wiki pages with `category` field:

- **Getting Started**: `getting-started`
- **Equipment Guide, Lab Status**: `equipment`
- **Team**: `community`
- **Brand Standards, CSS Library, Component Showcase, Button Playground, API Reference**: `development`
- **CFL Kiosk, CFL Task Dashboard**: `projects`
- **GitHub Rulesets**: `guides`
- **The Void**: `fun`

### 2. Update Home Page Layout ([index.html](index.html))

```
Hero Section (keep as-is)
        ↓
┌─────────────────────────────────┐
│  Search Bar (centered)          │
│  ┌───────────────────────────┐  │
│  │ 🔍 Search wiki pages...   │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
        ↓
┌─────────────────────────────────┐
│  Category Pills (horizontal)    │
│  [All] [Equipment] [Guides] ... │
└─────────────────────────────────┘
        ↓
┌─────────────────────────────────┐
│  Upgraded Card Grid             │
│  ┌─────┐ ┌─────┐ ┌─────┐       │
│  │Card │ │Card │ │Card │       │
│  └─────┘ └─────┘ └─────┘       │
└─────────────────────────────────┘
```

### 3. Upgrade Card Design ([_includes/card.html](_includes/card.html))

New card features:

- Category badge (colored pill)
- Icon based on category
- Subtle gradient header accent
- Improved hover animation (lift + shadow)
- Better typography hierarchy

### 4. Add JavaScript for Search/Filter

Client-side filtering in [_layouts/default.html](_layouts/default.html):

- Filter cards by search input (title + excerpt)
- Filter cards by category pill click
- Show "No results" state when empty
- Animate card transitions

### 5. CSS Updates ([assets/css/main.css](assets/css/main.css))

- New `.wiki-search` section styles
- Category pill buttons (`.category-pill`)
- Enhanced `.wiki-card` with gradient, shadows, animations
- "No results" empty state
- Mobile-responsive adjustments

## Files to Modify

| File | Changes |

|------|---------|

| `_wiki/*.mkd` (13 files) | Add `category` frontmatter |

| `index.html` | Add search bar, category pills, data attributes |

| `_includes/card.html` | Upgraded card markup with category badge, icon |

| `_layouts/default.html` | Add search/filter JavaScript |

| `assets/css/main.css` | New styles for search, pills, upgraded cards |