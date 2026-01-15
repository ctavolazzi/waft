---
category: dreads
confidence: 0.62
constellation_date: 2026-01-14
original_file: fix_directory_browser_clicks_and_add_search_35cb492e.plan.md
---

# Fix Directory Browser Clicks and Add Search

## Problems Identified

1. **Clicks not working**: Click handlers are set up but may have event propagation issues or CSS cursor issues
2. **No search functionality**: Missing search input to filter directories
3. **Confusing selection behavior**: Folders with work efforts auto-select on single click
4. **Missing features**: No breadcrumbs, loading states, error handling, or ability to select folders without work efforts

## Solution

### 1. Fix Click Handlers - Single Click Navigate, Double Click Select

**File**: `mcp-servers/dashboard/public/app.js`

- **Single-click**: Navigate into ANY folder (whether it has work efforts or not)
- **Double-click**: Select the folder (closes browser, fills form, user clicks "Add Repository")
- Add proper event handling with `stopPropagation()` and `preventDefault()`
- Add visual feedback (cursor pointer, hover states)

**Changes**:

- Update `browsePath()` click handler: single-click always navigates
- Add double-click handler: selects folder and calls `selectDirectory()`
- Make `selectDirectory()` work for ANY folder (not just ones with work efforts)
- Add `cursor: pointer` CSS
- Add `user-select: none` to prevent text selection

### 2. Add Search Functionality

**File**: `mcp-servers/dashboard/public/app.js`

- Add search input field in browser toolbar (next to path input)
- Filter directory list in real-time as user types
- Search filters by directory name (case-insensitive)
- Clear search button (X icon) to reset filter
- Search persists when navigating into folders

**Changes**:

- Add search input to `openDirectoryBrowser()` HTML
- Store full items list in `browsePath()` before filtering
- Add `filterDirectories(searchTerm, items)` method
- Bind search input to filter on `input` event with debounce
- Update rendering to show filtered results
- Add search icon/clear button styling

### 3. Add Breadcrumb Navigation

**File**: `mcp-servers/dashboard/public/app.js`

- Show clickable breadcrumb trail above directory list
- Format: `Code > active > waft` (each segment clickable)
- Clicking breadcrumb navigates to that path
- Highlight current directory in breadcrumbs

**Changes**:

- Add `renderBreadcrumbs(path)` method that splits path and creates clickable segments
- Add breadcrumb HTML to browser toolbar area
- Bind breadcrumb clicks to navigate to that path
- Style breadcrumbs with separators and hover states

### 4. Add Loading States

**File**: `mcp-servers/dashboard/public/app.js`

- Show loading spinner when clicking folders (before API call completes)
- Disable click handlers during loading
- Show "Loading..." text in browser list
- Add visual feedback on folder click (highlight briefly)

**Changes**:

- Add loading state flag in `browsePath()`
- Show spinner/loading message immediately on click
- Disable all browser-item clicks during loading
- Re-enable after API response

### 5. Improve Error Handling

**File**: `mcp-servers/dashboard/public/app.js`

- Show clear error messages if navigation fails
- Handle network errors gracefully
- Show toast notifications for errors
- Allow retry on error

**Changes**:

- Wrap API calls in try-catch with specific error messages
- Show user-friendly error text (not just "Failed to load")
- Add retry button on error state
- Log errors to console for debugging

### 6. Allow Selecting Any Folder

**File**: `mcp-servers/dashboard/public/app.js`

- Remove restriction that only folders with work efforts can be selected
- Double-click ANY folder to select it
- Visual indicator for folders with work efforts (keep the green highlight)
- But allow selection of any folder

**Changes**:

- Update `selectDirectory()` to work for any folder
- Remove `has-work-efforts` check from selection logic
- Keep visual highlighting for folders with work efforts (informational only)
- Update hint text to reflect that any folder can be selected

## Implementation Details

### Click Handler Fix

```javascript
// In browsePath(), after setting innerHTML:
browserList.querySelectorAll('.browser-item').forEach(item => {
  item.style.cursor = 'pointer';

  // Single-click: navigate
  item.addEventListener('click', (e) => {
    e.stopPropagation();
    const itemPath = item.dataset.path;
    this.browsePath(itemPath); // Always navigate
  });

  // Double-click: select
  item.addEventListener('dblclick', (e) => {
    e.stopPropagation();
    e.preventDefault();
    this.selectDirectory(item.dataset.path, item.dataset.name);
  });
});
```



### Search Implementation

```javascript
// Add to openDirectoryBrowser() HTML toolbar:
<input type="text"
       class="browser-search"
       id="browserSearch"
       placeholder="🔍 Search directories...">
<button class="browser-clear-search" id="browserClearSearch" title="Clear">×</button>

// Store full items and filter:
this.browserItems = data.items; // Store full list
const searchTerm = this.browserSearchTerm || '';
const filteredItems = this.filterDirectories(searchTerm, this.browserItems);

// Filter method:
filterDirectories(searchTerm, items) {
  if (!searchTerm.trim()) return items;
  const term = searchTerm.toLowerCase();
  return items.filter(item =>
    item.name.toLowerCase().includes(term)
  );
}
```



### Breadcrumbs

```javascript
renderBreadcrumbs(currentPath) {
  const parts = currentPath.split('/').filter(p => p);
  const segments = [];
  let accumulatedPath = '';

  parts.forEach((part, index) => {
    accumulatedPath += (accumulatedPath ? '/' : '') + part;
    segments.push({
      name: part,
      path: '/' + accumulatedPath,
      isLast: index === parts.length - 1
    });
  });

  return segments.map(s =>
    `<span class="breadcrumb-segment ${s.isLast ? 'active' : ''}"
            data-path="${s.path}">${s.name}</span>`
  ).join('<span class="breadcrumb-separator"> > </span>');
}
```



### Loading State

```javascript
async browsePath(dirPath) {
  this.isLoading = true;
  this.updateBrowserLoadingState(true);

  try {
    // ... API call ...
    this.isLoading = false;
    this.updateBrowserLoadingState(false);
  } catch (error) {
    this.isLoading = false;
    this.updateBrowserLoadingState(false);
    this.showBrowserError(error);
  }
}
```



## CSS Updates

**File**: `mcp-servers/dashboard/public/styles.css`

- Add `cursor: pointer` to `.browser-item`
- Add `user-select: none` to `.browser-item`
- Style search input to match toolbar
- Style breadcrumbs with hover states
- Add loading spinner styles
- Add error state styles

## Testing Checklist

- [ ] Single-click any folder → Navigates into it
- [ ] Double-click any folder → Selects it and closes browser
- [ ] Search filters list in real-time
- [ ] Breadcrumbs show current path
- [ ] Clicking breadcrumb navigates to that path
- [ ] Loading spinner shows when clicking folders
- [ ] Error messages are clear and helpful
- [ ] Can select folders without work efforts
- [ ] Folders with work efforts are visually highlighted (but still navigable)

## Files to Modify

1. `mcp-servers/dashboard/public/app.js` - All functionality