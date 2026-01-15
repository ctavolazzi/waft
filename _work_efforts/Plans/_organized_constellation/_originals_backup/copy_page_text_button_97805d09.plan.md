---
name: Copy Page Text Button
overview: Add a copy button in the navigation controls that extracts and copies all unique page text content, excluding navigation and footer elements, with toast feedback.
todos:
  - id: create-copy-module
    content: Create src/js/copy-page-text.js module with text extraction and clipboard functionality
    status: completed
  - id: add-button-to-nav
    content: Add copy-page-text button with SVG icon and tooltip to generateNavHeader() in scripts/build.js
    status: completed
  - id: style-button
    content: Add .copy-page-text-btn styles to src/css/navigation.css matching nav control pattern
    status: completed
    dependencies:
      - add-button-to-nav
  - id: bundle-copy-js
    content: Add copy-page-text.js to JS_FILES array in scripts/build.js for bundling
    status: completed
    dependencies:
      - create-copy-module
  - id: test-functionality
    content: Test copy functionality on different page types (index, wiki, etc.)
    status: completed
    dependencies:
      - create-copy-module
      - add-button-to-nav
      - style-button
  - id: deploy
    content: Build and deploy to Cloudflare Pages
    status: in_progress
    dependencies:
      - test-functionality
---

# Copy

Page Text Button Implementation

## Overview

Add a copy-to-clipboard button in the navigation bar that extracts all unique text content from the page, excluding navigation elements, footers, and other repeated UI components.

## Implementation Details

### 1. Create Copy Module (`src/js/copy-page-text.js`)

- New JavaScript module following the existing pattern (similar to `toast.js`, `nav.js`)

- Module name: `CopyPageText` (descriptive and accurate)

- Function to extract text from page content:

- Target: `main#main-content` or `.wiki-main` (main content areas)

- Exclude:

    - `.nav-wrapper` and all navigation elements

    - `footer[role="contentinfo"]`, `.wiki-footer`, `.wiki-index-footer`

    - `.skip-link`, elements with `aria-hidden="true"`

    - Hidden elements (display:none, visibility:hidden)

    - `.mobile-drawer`, `.wiki-sidebar`

- Extract text using `textContent` or `innerText`

- Clean up whitespace (normalize multiple spaces/newlines)

- Use Clipboard API (`navigator.clipboard.writeText()`)

- Show success/error toast feedback using existing `Toast` module

- Export as `window.CopyPageText` for global access

### 2. Add Button to Navigation (`scripts/build.js`)

- Modify `generateNavHeader()` function

- Add copy button in `.nav-controls` div (after theme picker, before menu toggle)

- Use inline SVG clipboard icon (similar to wiki icons pattern)

- Button naming: Use descriptive class name `copy-page-text-btn`

- Button structure with tooltip:
  ```html
    <button
        class="copy-page-text-btn"
        onclick="CopyPageText.copy()"
        aria-label="Copy all page text to clipboard"
        title="Copy all page text (excluding navigation and footer)">
        <span class="copy-icon" aria-hidden="true">
            <!-- SVG clipboard icon -->
        </span>
    </button>
  ```

- Tooltip: Use `title` attribute for native browser tooltip explaining the button copies all page text excluding navigation and footer elements

### 3. Style the Button (`src/css/navigation.css`)

- Add `.copy-page-text-btn` styles matching theme picker pattern

- Icon size: ~20px to match theme picker icon

- Hover/focus states consistent with other nav controls

- Responsive: visible on mobile (in nav controls area)

### 4. Initialize Module (`src/js/main.js`)

- Add `CopyPageText.init()` call in `App.init()` if needed

- Ensure module loads with other scripts

- Module may not need explicit initialization if it's just a function call

### 5. SVG Clipboard Icon

- Create inline SVG following existing icon pattern

- Use `viewBox="0 0 24 24"` with `stroke="currentColor"`

- Simple clipboard/clipboard-copy icon design

- Match stroke-width and styling of other icons

## Files to Modify

1. **`src/js/copy-page-text.js`** (NEW) - Copy functionality module

2. **`scripts/build.js`** - Add button to `generateNavHeader()` function with tooltip

3. **`src/css/navigation.css`** - Add `.copy-page-text-btn` button styles

4. **`src/js/main.js`** - Initialize copy module (if needed)

5. **`scripts/build.js`** - Add `copy-page-text.js` to JS_FILES array for bundling

## Text Extraction Logic

The copy function should:

1. Find main content container (`main#main-content` or `.wiki-main`)

2. Clone the element to avoid modifying DOM

3. Remove excluded elements from clone:

- Navigation wrappers

- Footer elements

- Hidden/aria-hidden elements

- Skip links

4. Extract text content

5. Normalize whitespace (trim, collapse multiple spaces/newlines)

6. Copy to clipboard

7. Show toast notification

## Testing Considerations

- Test on different page types:

- Main pages (index.html, about.html, etc.)

- Wiki pages (wiki template)

- Wiki index page

- Verify footer/navigation text is excluded

- Verify unique content is included

- Test clipboard API fallback (if needed)

- Verify toast feedback appears

- Test on mobile viewport

## Deployment

After implementation:

1. Build the project (`npm run build`)

2. Test locally

name: Copy Page Text Button

overview: Add a copy button in the navigation controls that extracts and copies all unique page text content, excluding navigation and footer elements, with toast feedback.

todos:

  - id: create-copy-module

content: Create src/js/copy-page-content.js module with text extraction and clipboard functionality

status: pending

  - id: add-button-to-nav

content: Add copy-page-content button with SVG icon and tooltip to generateNavHeader() in scripts/build.js

status: pending

  - id: style-button

content: Add .copy-page-content-btn styles to src/css/navigation.css matching nav control pattern

status: pending

dependencies:

      - add-button-to-nav
  - id: bundle-copy-js

content: Add copy-page-content.js to JS_FILES array in scripts/build.js for bundling

status: pending

dependencies:

      - create-copy-module
  - id: test-functionality

content: Test copy functionality on different page types (index, wiki, etc.)

status: pending

dependencies:

      - create-copy-module
      - add-button-to-nav
      - style-button
  - id: deploy

content: Build and deploy to Cloudflare Pages

status: pending

dependencies:

      - test-functionality

---

# Copy

Page Text Button Implementation

## Overview

Add a copy-to-clipboard button in the navigation bar that extracts all unique text content from the page, excluding navigation elements, footers, and other repeated UI components.

## Implementation Details

### 1. Create Copy Module (`src/js/copy-page-text.js`)

- New JavaScript module following the existing pattern (similar to `toast.js`, `nav.js`)

- Module name: `CopyPageText` (descriptive and accurate)

- Function to extract text from page content:

- Target: `main#main-content` or `.wiki-main` (main content areas)

- Exclude:

    - `.nav-wrapper` and all navigation elements

    - `footer[role="contentinfo"]`, `.wiki-footer`, `.wiki-index-footer`

    - `.skip-link`, elements with `aria-hidden="true"`

    - Hidden elements (display:none, visibility:hidden)

    - `.mobile-drawer`, `.wiki-sidebar`

- Extract text using `textContent` or `innerText`

- Clean up whitespace (normalize multiple spaces/newlines)

- Use Clipboard API (`navigator.clipboard.writeText()`)

- Show success/error toast feedback using existing `Toast` module

- Export as `window.CopyPageText` for global access

### 2. Add Button to Navigation (`scripts/build.js`)

- Modify `generateNavHeader()` function

- Add copy button in `.nav-controls` div (after theme picker, before menu toggle)

- Use inline SVG clipboard icon (similar to wiki icons pattern)

- Button naming: Use descriptive class name `copy-page-text-btn`

- Button structure with tooltip:
  ```html
    <button
        class="copy-page-text-btn"
        onclick="CopyPageText.copy()"
        aria-label="Copy all page text to clipboard"
        title="Copy all page text (excluding navigation and footer)">
        <span class="copy-icon" aria-hidden="true">
            <!-- SVG clipboard icon -->
        </span>
    </button>
  ```

- Tooltip: Use `title` attribute for native browser tooltip explaining the button copies all page text excluding navigation and footer elements

### 3. Style the Button (`src/css/navigation.css`)

- Add `.copy-page-text-btn` styles matching theme picker pattern

- Icon size: ~20px to match theme picker icon

- Hover/focus states consistent with other nav controls

- Responsive: visible on mobile (in nav controls area)

### 4. Initialize Module (`src/js/main.js`)

- Add `CopyPageText.init()` call in `App.init()` if needed

- Ensure module loads with other scripts

- Module may not need explicit initialization if it's just a function call

### 5. SVG Clipboard Icon

- Create inline SVG following existing icon pattern

- Use `viewBox="0 0 24 24"` with `stroke="currentColor"`

- Simple clipboard/clipboard-copy icon design

- Match stroke-width and styling of other icons

## Files to Modify

1. **`src/js/copy-page-text.js`** (NEW) - Copy functionality module

2. **`scripts/build.js`** - Add button to `generateNavHeader()` function with tooltip

3. **`src/css/navigation.css`** - Add `.copy-page-text-btn` button styles

4. **`src/js/main.js`** - Initialize copy module (if needed)

5. **`scripts/build.js`** - Add `copy-page-text.js` to JS_FILES array for bundling

## Text Extraction Logic

The copy function should:

1. Find main content container (`main#main-content` or `.wiki-main`)

2. Clone the element to avoid modifying DOM

3. Remove excluded elements from clone:

- Navigation wrappers

- Footer elements

- Hidden/aria-hidden elements

- Skip links

4. Extract text content

5. Normalize whitespace (trim, collapse multiple spaces/newlines)

6. Copy to clipboard

7. Show toast notification

## Testing Considerations

- Test on different page types:

- Main pages (index.html, about.html, etc.)

- Wiki pages (wiki template)

- Wiki index page

- Verify footer/navigation text is excluded

- Verify unique content is included

- Test clipboard API fallback (if needed)

- Verify toast feedback appears

- Test on mobile viewport

## Deployment

After implementation:

1. Build the project (`npm run build`)

2. Test locally