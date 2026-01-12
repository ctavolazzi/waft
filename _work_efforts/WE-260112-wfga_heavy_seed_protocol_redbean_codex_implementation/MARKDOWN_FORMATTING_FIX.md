# Markdown Formatting Fix for PDF Generation

**Date**: 2026-01-12 15:20  
**Issue**: Markdown formatting errors in PDF conversion  
**Status**: ✅ Fixed

---

## Problem

The `_clean_markdown` method in `two_page_generator.py` was **stripping** markdown formatting instead of **converting** it to HTML. This caused:

- Headers removed (##, ###)
- Bold/italic removed (**text**, *text*)
- Code blocks removed (```, `)
- Lists removed (-, *, 1.)
- Links converted to plain text

**Result**: PDFs showed plain text without any formatting, making them hard to read and losing important structure.

---

## Root Cause

**Location**: `src/waft/evolution/two_page_generator.py`

**Method**: `_clean_markdown()` (line 813)

**Problem**: Method was designed to "clean" markdown by removing all formatting, but it should have been converting markdown to HTML for proper rendering.

---

## Solution

### 1. Created New Method: `_markdown_to_html()`

**Purpose**: Properly convert markdown to HTML instead of stripping it

**Implementation**:
- **Primary**: Uses `markdown` library if available (best quality)
  - Extensions: `fenced_code`, `tables`, `nl2br`, `extra`
- **Fallback**: Manual conversion using regex (if library not available)
  - Headers: `##` → `<h2>`, `###` → `<h3>`, etc.
  - Bold: `**text**` → `<strong>text</strong>`
  - Italic: `*text*` → `<em>text</em>`
  - Code: `` `code` `` → `<code>code</code>`
  - Code blocks: ` ```...``` ` → `<pre><code>...</code></pre>`
  - Links: `[text](url)` → `<a href="url">text</a>`
  - Lists: `- item` → `<ul><li>item</li></ul>`
  - Ordered lists: `1. item` → `<ol><li>item</li></ol>`

### 2. Updated Template to Render HTML Safely

**Changes**:
- Changed `{{ idea.content }}` to `{{ idea.content|safe }}` in template
- Changed `<p class="idea-content">` to `<div class="idea-content">` (allows block-level HTML)
- Updated both page_1_ideas and page_2_ideas sections

**Why `|safe`**: Jinja2 auto-escapes HTML by default. Since we're now generating HTML, we need to use the `|safe` filter to prevent double-escaping.

### 3. Added Markdown Library to Dependencies

**File**: `pyproject.toml`

**Change**: Added `"markdown>=3.4.0"` to dependencies

**Purpose**: Provides high-quality markdown-to-HTML conversion with proper handling of edge cases, tables, code blocks, etc.

### 4. Kept Backward Compatibility

**Method**: `_clean_markdown()` now calls `_markdown_to_html()`

**Purpose**: Any existing code that calls `_clean_markdown()` will still work, but now properly converts markdown instead of stripping it.

---

## Files Modified

1. **`src/waft/evolution/two_page_generator.py`**:
   - Added `_markdown_to_html()` method (proper conversion)
   - Updated `_clean_markdown()` to call `_markdown_to_html()` (backward compatibility)
   - Updated template: `{{ idea.content }}` → `{{ idea.content|safe }}`
   - Updated template: `<p>` → `<div>` for idea-content containers

2. **`pyproject.toml`**:
   - Added `"markdown>=3.4.0"` to dependencies

---

## Testing

**To Test**:
1. Install dependencies: `pip install markdown>=3.4.0`
2. Generate PDF using PDFGenerator
3. Verify markdown formatting is preserved:
   - Headers appear as headers
   - Bold text appears bold
   - Code blocks appear in monospace
   - Lists appear as proper lists
   - Links are clickable

**Expected Result**: PDFs now show proper formatting with headers, bold, italic, code blocks, lists, and links rendered correctly.

---

## Impact

**Before**: 
- Markdown stripped → Plain text → Poor readability
- Lost structure (headers, lists, code blocks)
- No visual hierarchy

**After**:
- Markdown converted to HTML → Proper formatting → Better readability
- Structure preserved (headers, lists, code blocks)
- Visual hierarchy maintained
- Professional appearance

---

## Notes

- The `markdown` library provides the best conversion quality
- Fallback manual conversion handles basic cases if library unavailable
- Template uses `|safe` filter to prevent HTML escaping
- Backward compatibility maintained via `_clean_markdown()` wrapper

---

**Fix Complete**: 2026-01-12 15:20  
**Status**: ✅ Ready for testing
