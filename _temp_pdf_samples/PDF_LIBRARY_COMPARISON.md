# PDF Library Comparison Study

**Date**: January 12, 2026  
**Source**: `session_recap_2026-01-12.md`  
**Purpose**: Compare 3 different PDF generation approaches

---

## Generated PDFs

1. **ReportLab** → `session_recap_reportlab.pdf` (9.0 KB)
2. **WeasyPrint** → `session_recap_weasyprint.pdf` (153 KB)
3. **Jinja2 + WeasyPrint** → `session_recap_jinja.pdf` (161 KB)

---

## Library Comparison

### 1. ReportLab (Direct PDF Generation)

**Approach**: Direct PDF generation using Platypus framework

**Pros**:
- ✅ Smallest file size (9 KB)
- ✅ Pure Python, no external dependencies
- ✅ Professional typography control
- ✅ Automatic page breaks and flow
- ✅ Production-proven (used by major companies)
- ✅ Low-level control when needed (Canvas API)

**Cons**:
- ❌ Manual markdown parsing required
- ❌ More code for complex layouts
- ❌ Limited CSS support (must use ReportLab styles)
- ❌ Steeper learning curve

**Best For**:
- Professional documents with precise typography
- Data-heavy reports with tables
- When file size matters
- When you need programmatic control

**Code Location**: `examples/generate_pdf_reportlab.py`

---

### 2. WeasyPrint (HTML → PDF)

**Approach**: Convert markdown → HTML → PDF using CSS styling

**Pros**:
- ✅ CSS-based styling (familiar web technologies)
- ✅ Automatic HTML rendering
- ✅ Good typography and layout
- ✅ Handles complex HTML/CSS
- ✅ Automatic page breaks
- ✅ Good for web-to-PDF workflows

**Cons**:
- ❌ Larger file size (153 KB)
- ❌ System dependencies (Cairo, Pango)
- ❌ Less control over PDF internals
- ❌ CSS print media quirks

**Best For**:
- HTML/CSS-based workflows
- Web content conversion
- When you want CSS styling
- Rapid prototyping

**Code Location**: `examples/generate_pdf_weasyprint.py`

---

### 3. Jinja2 + WeasyPrint (Template-Based)

**Approach**: Markdown → HTML → Jinja2 template → WeasyPrint → PDF

**Pros**:
- ✅ Template-based (reusable, maintainable)
- ✅ Separation of content and presentation
- ✅ Dynamic content generation
- ✅ Professional document structure
- ✅ Easy to customize headers/footers
- ✅ Best for document generation systems

**Cons**:
- ❌ Largest file size (161 KB)
- ❌ Most complex setup
- ❌ Requires understanding both Jinja2 and WeasyPrint
- ❌ System dependencies

**Best For**:
- Document generation systems
- Templates with dynamic content
- When you need reusable document structures
- Professional document workflows

**Code Location**: `examples/generate_pdf_jinja.py`

---

## File Size Comparison

| Library | File Size | Ratio |
|---------|-----------|-------|
| ReportLab | 9.0 KB | 1x (baseline) |
| WeasyPrint | 153 KB | 17x |
| Jinja2+WeasyPrint | 161 KB | 18x |

**Note**: File size differences are due to:
- ReportLab: Direct PDF generation, minimal overhead
- WeasyPrint: HTML/CSS rendering, includes font metrics
- Jinja2+WeasyPrint: Same as WeasyPrint + template overhead

---

## Code Complexity Comparison

### ReportLab
- **Lines of Code**: ~150
- **Complexity**: Medium (manual markdown parsing)
- **Dependencies**: reportlab, markdown

### WeasyPrint
- **Lines of Code**: ~100
- **Complexity**: Low (HTML/CSS styling)
- **Dependencies**: weasyprint, markdown

### Jinja2 + WeasyPrint
- **Lines of Code**: ~120
- **Complexity**: Medium (template + styling)
- **Dependencies**: jinja2, weasyprint, markdown

---

## Use Case Recommendations

### Choose ReportLab When:
- ✅ File size is critical
- ✅ You need precise typography control
- ✅ You're generating data-heavy reports
- ✅ You want programmatic PDF generation
- ✅ You need low-level PDF control

### Choose WeasyPrint When:
- ✅ You have HTML/CSS content
- ✅ You want CSS-based styling
- ✅ You're converting web content
- ✅ You want rapid prototyping
- ✅ File size isn't critical

### Choose Jinja2 + WeasyPrint When:
- ✅ You need template-based generation
- ✅ You have dynamic content
- ✅ You want reusable document structures
- ✅ You're building a document generation system
- ✅ You need professional document layouts

---

## Technical Details

### ReportLab Implementation
- Uses `SimpleDocTemplate` for document structure
- `Paragraph` objects for text with HTML-like tags
- `Spacer` for vertical spacing
- Custom styles via `getSampleStyleSheet()`
- Manual markdown parsing line-by-line

### WeasyPrint Implementation
- Markdown → HTML conversion using `markdown` library
- Full HTML document with embedded CSS
- `@page` rules for page layout
- CSS print media styling
- Direct HTML → PDF conversion

### Jinja2 + WeasyPrint Implementation
- Markdown → HTML conversion
- Jinja2 template for document structure
- Template variables: `title`, `date`, `content`
- CSS styling in template
- Rendered HTML → PDF via WeasyPrint

---

## Conclusion

All three approaches successfully generate PDFs from markdown:

1. **ReportLab**: Best for file size and typography control
2. **WeasyPrint**: Best for HTML/CSS workflows
3. **Jinja2 + WeasyPrint**: Best for template-based systems

**Recommendation**: Choose based on your specific needs:
- **Small files + control** → ReportLab
- **HTML/CSS familiarity** → WeasyPrint
- **Template systems** → Jinja2 + WeasyPrint

---

**Generated**: January 12, 2026  
**Source Code**: `examples/generate_pdf_*.py`
