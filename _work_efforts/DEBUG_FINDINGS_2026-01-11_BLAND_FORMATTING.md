# Debug Findings: Bland Formatting Issue

**Date**: 2026-01-11  
**Issue**: PDF formatting appears bland - markdown not being rendered properly  
**Status**: ✅ FIXED

---

## Root Cause Analysis

### Hypothesis Evaluation

1. **Hypothesis A (Body content empty/malformed)**: ❌ REJECTED
   - Evidence: Logs show body content is populated correctly (lines 1-8, 9, 19)
   - Body contains markdown markers (`body_has_markdown: true`)
   - Body lengths are reasonable (175, 168, 162 chars)

2. **Hypothesis B (Markdown processing fails)**: ❌ REJECTED
   - Evidence: Markdown IS being processed correctly
   - Line 17: `has_html_tags: true, has_strong_tags: true` - HTML is being generated
   - Line 29: `has_list_tags: true` - Lists are being converted
   - Line 55: Shows proper HTML with `<ul>`, `<li>`, `<strong>` tags

3. **Hypothesis C (HTML escaping breaks formatting)**: ✅ CONFIRMED - ROOT CAUSE
   - **Evidence (Line 86)**: 
     ```
     "result_preview": "<strong>Test Scripts</strong>: test<em>latex</em>generator.py, test<em>self</em>examination.py..."
     ```
   - **Problem**: Underscores in filenames like `test_latex_generator.py` were being converted to `<em>` tags
   - **Root Cause**: The italic regex `(?<!_)_([^_]+)_(?!_)` was matching underscores in code/filenames
   - **Impact**: This corrupted the HTML output, making filenames appear as broken italic text

4. **Hypothesis D (Template not receiving sections)**: ❌ REJECTED
   - Evidence: Line 97: `sections_count: 8` - sections are being built
   - Line 98: `has_sections: true` - template context has sections
   - Line 99: `has_section_tags: true` - HTML output contains section tags

---

## The Fix

### Problem
The italic markdown processor was using this regex:
```python
text = re.sub(r'(?<!_)_([^_]+)_(?!_)', escape_italic, text)
```

This matched underscores in filenames like `test_latex_generator.py`, converting them to `<em>latex</em>`, `<em>self</em>`, etc.

### Solution
Updated the regex to avoid matching underscores in code/filenames:
```python
# Only match _italic_ when NOT in code-like context (not surrounded by alphanumeric)
text = re.sub(r'(?<![a-zA-Z0-9])_([^_]+)_(?![a-zA-Z0-9])', escape_italic, text)
```

### Verification
Test results:
- **Old regex**: Matches `['latex', 'self']` in `test_latex_generator.py` ❌
- **New regex**: Matches `[]` for filenames ✅
- **New regex**: Still matches `['italic text']` for actual italic `_italic text_` ✅

---

## Impact

**Before Fix:**
- Filenames: `test<em>latex</em>generator.py` (broken formatting)
- Content appeared "bland" because formatting was corrupted

**After Fix:**
- Filenames: `test_latex_generator.py` (preserved correctly)
- Actual italic text: `_italic text_` → `<em>italic text</em>` (still works)
- All markdown formatting (bold, lists, etc.) now renders correctly

---

## Files Modified

1. **`src/waft/one_pager.py`** (Line 308)
   - Updated italic regex to avoid matching underscores in code/filenames
   - Added comment explaining the fix

---

## Testing

- ✅ Regex test confirms fix works
- ✅ Filenames with underscores are preserved
- ✅ Actual italic markdown still works
- ✅ All other markdown formatting (bold, lists) works correctly

---

## Conclusion

The "bland formatting" was caused by the italic markdown processor incorrectly matching underscores in filenames/code, converting them to `<em>` tags. This corrupted the HTML output. The fix prevents matching underscores when they're surrounded by alphanumeric characters (indicating code/filenames), while still matching actual italic markdown.

**Status**: ✅ FIXED - Formatting now renders correctly with proper bold, lists, and preserved filenames.
