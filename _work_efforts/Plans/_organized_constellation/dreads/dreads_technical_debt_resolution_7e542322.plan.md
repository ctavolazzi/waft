---
name: Technical Debt Resolution
overview: "Comprehensive plan to address all three technical debt items: JavaScript extraction, CSS modularization, and font loading optimization. This will improve maintainability, performance, and developer experience."
todos:
  - id: js-extract
    content: "Phase 1: Extract inline JavaScript to assets/js/main.js - Move all JS from _layouts/default.html to external file for browser caching"
    status: pending
  - id: js-modularize
    content: "Phase 2: Modularize JavaScript - Split main.js into logical modules (sounds, achievements, settings, components, easter-eggs, ui)"
    status: pending
  - id: fonts-optimize
    content: "Phase 3: Optimize font loading - Combine requests, lazy load optional fonts, audit font weights"
    status: pending
  - id: css-modularize
    content: "Phase 4: Modularize CSS - Convert to Sass/SCSS with organized partials in _sass/ directory"
    status: pending
  - id: testing
    content: Comprehensive testing - Functional, performance (Lighthouse), cross-browser, regression testing after each phase
    status: pending
  - id: documentation
    content: Update documentation - Mark technical debt items as resolved, update file structure docs, create migration notes
    status: pending

category: dreads
confidence: 0.83
constellation_date: 2026-01-14
---

# Technical Debt Resolution Plan

## Overview

This plan addresses three major technical debt items identified in the codebase audit:

1. **JavaScript Extraction** - Extract ~1,100+ lines of inline JS from `_layouts/default.html` to external files
2. **CSS Modularization** - Split 9,841-line monolithic CSS file into organized modules
3. **Font Loading Optimization** - Optimize 11+ Google Fonts loading strategy

## Current State Analysis

### JavaScript (`_layouts/default.html`)

- **Location**: Lines ~230-3299 (single `<script>` tag)
- **Size**: ~1,100+ lines inline
- **Structure**: Well-organized with clear section comments:

- Simple Dark Mode (~15 lines)
- Void Corruption Check (~15 lines)
- Sound Effects System (~150 lines)
- Achievement System (~120 lines)
- Konami Code (~35 lines)
- Button Sound Hooks (~40 lines)
- Achievement Panel UI (~70 lines)

- Easter Egg Hunt (~50 lines)
- Code Snippet Copy (~25 lines)
- Search Clear (~15 lines)
- Tabs Functionality (~30 lines)
- Toast System (~100 lines)
- Slider/Rating/Color (~50 lines)
- File Upload (~20 lines)

- Settings Widget (~400 lines)
- FAB Bar (~300 lines)
- Various component handlers

### CSS (`assets/css/main.css`)

- **Size**: 9,841 lines, 224KB
- **Structure**: 

- CSS Variables/Tokens (~100 lines)
- Dark mode themes (~100 lines)
- Base/Reset (~100 lines)
- Components (~7,000+ lines)
- Utilities (~500 lines)
- Responsive (~500 lines)

### Font Loading (`_layouts/default.html` lines 9-12)

- **Current**: Two separate Google Fonts requests
- **Fonts**: 11+ font families loaded on every page
- **Always used**: Inter, JetBrains Mono
- **Optional**: 9 fonts only used via settings widget

## Implementation Strategy

### Phase 1: JavaScript Extraction (Quick Win - 1-2 hours)

**Goal**: Move all JavaScript from inline `<script>` to external file for browser caching.

#### Step 1.1: Create Main JavaScript File

- Create `assets/js/main.js`

- Extract entire script block from `_layouts/default.html` (lines ~230-3299)
- Replace with: `<script src="{{ site.baseurl }}/assets/js/main.js"></script>`
- Test all functionality works identically

#### Step 1.2: Verify Functionality

- Test dark mode toggle
- Test sound effects
- Test achievement system
- Test settings widget
- Test FAB bar

- Test all interactive components
- Verify localStorage persistence

**Files to modify:**

- `_layouts/default.html` - Remove inline script, add external script tag
- `assets/js/main.js` - New file with all extracted JavaScript

**Benefits**: Browser caching, cleaner layout file, no functional changes---

### Phase 2: JavaScript Modularization (1-2 days)

**Goal**: Split monolithic JavaScript into logical modules for better maintainability.

#### Step 2.1: Create Module Structure

Create `assets/js/` directory structure:

```javascript
assets/js/
├── main.js              # Entry point, initializes all modules
├── core/
│   ├── storage.js       # safeGet, safeSet, safeRemove, safeParse
│   └── config.js        # CFL_CONFIG initialization
├── dark-mode.js         # Simple dark mode toggle
├── sounds.js            # Web Audio API sound effects
├── achievements.js      # Gamification system
├── settings.js          # Settings widget (largest module)
├── components/
│   ├── tabs.js
│   ├── search.js
│   ├── forms.js         # Slider, rating, color, file upload
│   ├── code-copy.js
│   └── toast.js
├── easter-eggs/
│   ├── konami.js
│   ├── void.js
│   └── eggs.js
└── ui/
    ├── fab-bar.js
    └── achievement-panel.js
```



#### Step 2.2: Extract Modules Using IIFE Pattern

Each module uses revealing module pattern:

```javascript
// sounds.js
window.CFL = window.CFL || {};
CFL.sounds = (function() {
    // Private variables
    var audioContext = null;
    var enabled = true;
    
    // Public API
    return {
        click: function() { /* ... */ },
        magic: function() { /* ... */ },
        // ... etc
    };
})();
```



#### Step 2.3: Update main.js

- Import all modules in correct initialization order
- Maintain DOMContentLoaded wrapper
- Ensure CFL global namespace is properly initialized

#### Step 2.4: Test Each Module

- Verify each module works independently
- Test module interactions
- Verify localStorage persistence
- Test all user interactions

**Files to create:**

- `assets/js/main.js` - Entry point

- `assets/js/core/storage.js`
- `assets/js/core/config.js`
- `assets/js/dark-mode.js`
- `assets/js/sounds.js`
- `assets/js/achievements.js`
- `assets/js/settings.js`
- `assets/js/components/tabs.js`

- `assets/js/components/search.js`
- `assets/js/components/forms.js`
- `assets/js/components/code-copy.js`
- `assets/js/components/toast.js`
- `assets/js/easter-eggs/konami.js`

- `assets/js/easter-eggs/void.js`
- `assets/js/easter-eggs/eggs.js`
- `assets/js/ui/fab-bar.js`
- `assets/js/ui/achievement-panel.js`

**Files to modify:**

- `_layouts/default.html` - Update script tag to point to main.js

**Benefits**: Better maintainability, testability, code organization---

### Phase 3: Font Loading Optimization (30 min - 4 hours)

**Goal**: Reduce render-blocking font requests and only load fonts when needed.

#### Step 3.1: Combine Font Requests (Quick Win - 30 min)

- Merge two Google Fonts `<link>` tags into one

- Keep `display=swap` parameter
- Maintain preconnect hints

#### Step 3.2: Lazy Load Optional Fonts (2-4 hours)

- Keep Inter and JetBrains Mono in initial load (always used)
- Create `assets/js/fonts.js` module for lazy loading
- Load optional fonts only when:

- User opens settings widget for first time, OR
- User has previously selected a font (check localStorage)
- Implement `loadFont(fontName)` function:
  ```javascript
    function loadFont(fontName) {
        if (document.querySelector(`link[data-font="${fontName}"]`)) return;
        var link = document.createElement('link');
        link.rel = 'stylesheet';
        link.dataset.font = fontName;
        link.href = `https://fonts.googleapis.com/css2?family=${fontName}&display=swap`;
        document.head.appendChild(link);
    }
  ```




#### Step 3.3: Optimize Font Weights

- Audit which font weights are actually used in CSS
- Remove unused weights from requests
- Document which weights are needed

**Files to modify:**

- `_layouts/default.html` - Update font loading strategy

- `assets/js/fonts.js` - New module for font management
- `assets/js/settings.js` - Integrate lazy font loading

**Benefits**: Faster initial page load, reduced render blocking---

### Phase 4: CSS Modularization (1-3 days)

**Goal**: Split 9,841-line CSS file into organized, maintainable modules.

#### Step 4.1: Audit and Map CSS Sections

- Review entire `assets/css/main.css`
- Document all sections with line numbers

- Identify dependencies between sections
- Create section map

#### Step 4.2: Choose Approach

**Recommended**: Use Jekyll's Sass support (Option C from tech debt doc)

Create `_sass/` directory structure:

```javascript
_sass/
├── _variables.scss      # CSS custom properties
├── _reset.scss          # Normalize/reset
├── _typography.scss     # Font styles
├── _layout.scss         # Grid, containers
├── components/
│   ├── _buttons.scss
│   ├── _cards.scss
│   ├── _forms.scss
│   ├── _alerts.scss
│   ├── _badges.scss
│   ├── _callouts.scss
│   ├── _tabs.scss
│   ├── _tables.scss
│   ├── _progress.scss
│   ├── _spinners.scss
│   ├── _stats.scss
│   ├── _avatars.scss
│   ├── _tooltips.scss
│   ├── _breadcrumbs.scss
│   ├── _settings.scss
│   └── _fab-bar.scss
├── _utilities.scss      # Helper classes
├── _fun.scss            # Easter eggs, achievements, animations
└── _responsive.scss     # Media queries
```



#### Step 4.3: Create Main SCSS File

Create `assets/css/main.scss`:

```scss
---
---

@import "variables";
@import "reset";
@import "typography";
@import "layout";
@import "components/buttons";
@import "components/cards";
// ... etc
@import "utilities";
@import "fun";
@import "responsive";
```



#### Step 4.4: Migrate CSS Sections

- Extract each section to appropriate SCSS file
- Maintain exact CSS output (no functional changes)
- Test after each major section migration

- Use Sass features (variables, nesting) where beneficial

#### Step 4.5: Update Jekyll Config

- Ensure Jekyll processes SCSS files
- Verify `_sass/` directory is recognized
- Test build process

**Files to create:**

- `_sass/_variables.scss`
- `_sass/_reset.scss`
- `_sass/_typography.scss`
- `_sass/_layout.scss`
- `_sass/components/_buttons.scss` (and all other components)
- `_sass/_utilities.scss`
- `_sass/_fun.scss`

- `_sass/_responsive.scss`
- `assets/css/main.scss` (replaces main.css)

**Files to modify:**

- `_layouts/default.html` - Update CSS link (Jekyll will compile SCSS)
- `_config.yml` - Verify Sass processing

**Files to archive:**

- `assets/css/main.css` - Move to `assets/css/archive/` after migration

**Benefits**: Better maintainability, easier navigation, potential for code reuse---

## Testing Strategy

### After Each Phase

1. **Functional Testing**

- Test all interactive features

- Verify localStorage persistence
- Test dark mode toggle
- Test settings widget
- Test achievement system
- Test sound effects
- Test all components

2. **Performance Testing**

- Lighthouse scores (before/after)
- Network tab (check caching)
- First Contentful Paint (FCP)
- Largest Contentful Paint (LCP)

3. **Cross-browser Testing**

- Chrome/Edge
- Firefox
- Safari

4. **Regression Testing**

- Verify no visual changes
- Verify no functional regressions
- Check console for errors

## Implementation Order

**Recommended sequence:**

1. **Phase 1** (JavaScript Extraction) - Quick win, low risk
2. **Phase 3** (Font Optimization) - Performance boost, medium effort
3. **Phase 2** (JavaScript Modularization) - Better maintainability

4. **Phase 4** (CSS Modularization) - Largest refactor, do last

**Rationale**: Start with low-risk, high-reward changes. Build confidence before tackling larger refactors.

## Risk Mitigation

1. **Git Strategy**

- Create feature branch: `refactor/technical-debt`

- Commit after each phase completion
- Keep original files until migration verified

2. **Rollback Plan**

- Keep original `_layouts/default.html` script in comments initially
- Keep original `assets/css/main.css` until SCSS migration complete

- Tag commits for easy rollback

3. **Testing**

- Test locally with `jekyll serve`
- Test on GitHub Pages deployment
- Verify all features work before merging

## Success Criteria

- [ ] All JavaScript extracted to external files

- [ ] JavaScript modularized into logical components
- [ ] CSS split into maintainable SCSS modules
- [ ] Font loading optimized (lazy load optional fonts)
- [ ] All functionality works identically
- [ ] Performance metrics improved (Lighthouse scores)
- [ ] No visual regressions

- [ ] Code is more maintainable
- [ ] Documentation updated

## Documentation Updates

After completion, update:

- `docs/technical-debt/README.md` - Mark items as resolved
- `docs/README.md` - Update file structure documentation

- `README.md` - Update if needed
- Create migration notes if helpful

## Estimated Timeline

- **Phase 1**: 1-2 hours
- **Phase 2**: 1-2 days

- **Phase 3**: 30 min - 4 hours
- **Phase 4**: 1-3 days