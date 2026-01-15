# /within-reason - Special Character Escaping for PDF Titles

**Purpose:** Ensure any special character can be rendered properly in PDF titles (within reason).

**Usage:** Built into PDF generation systems automatically

---

## Overview

The "within reason" system ensures that special characters in PDF titles are properly escaped for HTML/PDF rendering while preserving characters that should render as-is.

**What's Escaped:**
- HTML special characters: `< > & " '` → `&lt; &gt; &amp; &quot; &#x27;`

**What's Preserved (renders as-is):**
- Path separators: `/ \`
- Punctuation: `- _ . : ( ) [ ] { }`
- Operators: `+ = * ? ! @ # $ % ^ | ~ \``
- All other printable ASCII and Unicode characters

---

## How It Works

### Automatic Escaping

All PDF generation systems automatically escape titles:

1. **BriefDocument** (`src/waft/brief.py`):
   - Automatically escapes titles using `escape_title_for_pdf()`
   - Preserves special characters like `/`, `-`, `_`, etc.
   - Escapes HTML special characters (`< > & " '`)

2. **Case File PDFs** (`scripts/generate_case_pdf.py`):
   - Uses `generate_headline_title()` for headline-style titles
   - Escapes titles automatically before PDF generation
   - Handles special characters properly

3. **Template System** (`src/waft/templates/brief.py`):
   - Jinja2 template uses `|e` filter for explicit escaping
   - All template variables properly escaped

### Utility Functions

**Location:** `src/waft/utils/title_escape.py`

**Functions:**
- `escape_title_for_pdf(title)` - Escapes for HTML/PDF (preserves special chars)
- `escape_title_for_filename(title)` - Escapes for filesystem (replaces unsafe chars)
- `generate_headline_title(claim, verdict)` - Generates headline-style titles

---

## Examples

### Special Characters in Titles

**Input:**
```
"pantheon/ is the central database"
"File: /path/to/file.txt"
"X < Y & Z"
"Component (v1.0) - Status Report"
```

**Output (in PDF):**
```
"pantheon/ is the central database"  ✅ Renders correctly
"File: /path/to/file.txt"            ✅ Renders correctly
"X < Y & Z"                          ✅ Renders as "X < Y & Z"
"Component (v1.0) - Status Report"    ✅ Renders correctly
```

### HTML Escaping

**Input:**
```
"Title with <script>alert('XSS')</script>"
```

**Output (in PDF):**
```
"Title with <script>alert('XSS')</script>"  ✅ Escaped safely
```

---

## Integration

This system is built into:

1. **BriefDocument** - All brief PDFs
2. **Case File PDFs** - All proof case PDFs
3. **PDF Generator** - All PDF generation
4. **Template System** - All HTML templates

**No manual escaping needed** - it's automatic!

---

## Technical Details

### HTML Escaping

Uses Python's `html.escape()` which escapes:
- `<` → `&lt;`
- `>` → `&gt;`
- `&` → `&amp;`
- `"` → `&quot;`
- `'` → `&#x27;`

### Special Characters Preserved

These characters are **not** escaped and render as-is:
- `/` (forward slash)
- `\` (backslash)
- `-` (hyphen)
- `_` (underscore)
- `.` (period)
- `:` (colon)
- `(` `)` (parentheses)
- `[` `]` (brackets)
- `{` `}` (braces)
- `+ = * ? ! @ # $ % ^ | ~ \`` (operators and symbols)

### Filename Escaping

For filenames, unsafe characters are replaced:
- `/` → `_`
- `\` → `_`
- `:` → `-`
- `* ? " < > |` → `_`

---

## Usage

**Automatic** - No action needed! All PDF generation automatically handles special characters.

**Manual (if needed):**
```python
from waft.utils.title_escape import escape_title_for_pdf

title = "pantheon/ is central database"
escaped = escape_title_for_pdf(title)  # Ready for PDF
```

---

## "Within Reason" Definition

**Within reason** means:
- ✅ All printable ASCII characters
- ✅ Common Unicode characters (letters, numbers, punctuation)
- ✅ Path separators (`/`, `\`)
- ✅ Mathematical operators (`+`, `-`, `*`, `/`, `=`)
- ✅ Brackets and parentheses
- ✅ Special symbols (`@`, `#`, `$`, `%`, `^`, `&`, `*`, etc.)

**Not included:**
- ❌ Control characters (non-printable)
- ❌ Zero-width characters
- ❌ Extreme Unicode (rare scripts, emoji in titles)

---

## Testing

To test special character handling:

```python
from waft.utils.title_escape import escape_title_for_pdf

test_titles = [
    "pantheon/ is central database",
    "File: /path/to/file.txt",
    "X < Y & Z",
    "Component (v1.0) - Status",
    "Title with 'quotes' and \"double quotes\"",
    "Special: @#$%^&*()[]{}"
]

for title in test_titles:
    escaped = escape_title_for_pdf(title)
    print(f"{title} → {escaped}")
```

---

## Related

- **`/pdf-me`** - PDF generation command (uses this system)
- **`/case-file`** - Case file generation (uses this system)
- **BriefDocument** - Brief PDF generation (uses this system)

---

**Status**: ✅ Built into all PDF generation systems

**No manual action needed** - special characters are automatically handled properly!

--- End Command ---
