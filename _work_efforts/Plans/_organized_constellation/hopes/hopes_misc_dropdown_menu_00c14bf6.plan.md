---
name: Misc Dropdown Menu
overview: Add a new "LAB" dropdown menu to the navigation that opens on click and contains a link to a new Component Library page showcasing all UI components.
todos:
  - id: nav-dropdown
    content: Add LAB dropdown HTML to generateNavHeader() in build.js
    status: pending
  - id: dropdown-css
    content: Add dropdown CSS styles to navigation.css (reuse theme-picker pattern)
    status: pending
  - id: dropdown-js
    content: Add LabPicker toggle logic to nav.js
    status: pending
  - id: component-page
    content: Create src/lab/components.html with live component examples
    status: pending
  - id: build-config
    content: Update build.js to process lab/*.html files
    status: pending

category: hopes
confidence: 1.00
constellation_date: 2026-01-14
---

# Misc/Experiments Dropdown Menu

## Summary

Add a click-activated "LAB" dropdown to the main navigation containing a Component Library link, plus create a new `/lab/components.html` page that showcases all UI components.

## Architecture

```mermaid
flowchart LR
    subgraph Navigation
        NAV[Main Nav] --> LAB[LAB Dropdown]
        LAB --> COMP[Component Library]
        LAB --> FUTURE[Future Items...]
    end
    
    subgraph Pages
        COMP --> PAGE[/lab/components.html]
    end
```

## Files to Modify

1. **[scripts/build.js](scripts/build.js)** - Add LAB dropdown to `generateNavHeader()` function
2. **[src/css/navigation.css](src/css/navigation.css)** - Add dropdown styling (reuse theme-picker pattern)
3. **[src/js/nav.js](src/js/nav.js)** - Add `LabPicker` toggle logic (similar to `ThemePicker`)

## Files to Create

1. **src/lab/components.html** - Component Library showcase page with live examples of all UI components

## Implementation Details

### Navigation Dropdown
- Position: Between PRICING and CONTACT in the nav
- Label: "LAB" with a beaker/flask icon
- Click behavior: Toggle dropdown visibility (same pattern as theme picker)
- Dropdown contains: "Component Library" link initially, expandable for future items

### Component Library Page
- Shows live, interactive examples of all components documented in `_docs/30-39_reference/components_category/components.01_ui_component_reference.md`
- Organized by category: Navigation, Content, Interactive, Grid, etc.
- Each component shows: live preview + code snippet

### Mobile Support
- Add "LAB" section to mobile drawer with same items
- Dropdown closes when clicking outside (existing pattern)
