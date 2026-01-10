# PDF/Document Generation Libraries - Comparison & Recommendations

## Current Implementation: fpdf2

**What we're using now:**
```python
from fpdf import FPDF
```

**Pros:**
- ✅ Pure Python (no external dependencies)
- ✅ Simple API
- ✅ Lightweight
- ✅ Good for basic PDFs

**Cons:**
- ❌ Manual positioning required
- ❌ Limited advanced layout features
- ❌ No automatic text flow
- ❌ Basic typography support
- ❌ No CSS/template support

---

## Better Alternatives for Foundation V3

### 1. ReportLab (Recommended for Foundation V3)

**The industry standard for professional PDF generation**

```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Create document
doc = SimpleDocTemplate("output.pdf", pagesize=letter)
styles = getSampleStyleSheet()

# Build content
story = []
story.append(Paragraph("Executive Summary", styles['Heading1']))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("Body text with automatic flow...", styles['BodyText']))

# Automatic layout
doc.build(story)
```

**Why ReportLab?**
- ✅ **Platypus framework** - Automatic text flow and page breaks
- ✅ **Flowables** - Content blocks that know how to position themselves
- ✅ **Stylesheets** - Separate content from formatting
- ✅ **Professional typography** - Kerning, leading, tracking
- ✅ **Advanced tables** - Spanning cells, conditional formatting
- ✅ **Canvas API** - Low-level control when needed
- ✅ **Production proven** - Used by major companies

**Perfect for:**
- Clinical Standard documents
- Multi-page reports with automatic pagination
- Complex tables and data
- Professional publishing

**Installation:**
```bash
pip install reportlab
```

**Learning curve:** Medium (1-2 days)

---

### 2. WeasyPrint (Recommended for HTML-based workflows)

**Write HTML/CSS, get beautiful PDFs**

```python
from weasyprint import HTML, CSS

html_content = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Times New Roman', serif; }
        h1 { font-family: 'Helvetica', sans-serif; font-size: 18pt; }
        .metadata { background: #f0f0f0; padding: 10px; }
    </style>
</head>
<body>
    <h1>Executive Summary</h1>
    <div class="metadata">
        <strong>Subject ID:</strong> 991-DELTA<br>
        <strong>Timeline:</strong> 001-ORIGIN-TAM
    </div>
    <p>Body text with automatic flow and professional typography...</p>
</body>
</html>
"""

HTML(string=html_content).write_pdf('output.pdf')
```

**Why WeasyPrint?**
- ✅ **Modern web standards** - HTML5 + CSS3
- ✅ **Excellent typography** - Uses HarfBuzz for text shaping
- ✅ **Familiar syntax** - If you know CSS, you're done
- ✅ **Automatic pagination** - CSS Paged Media support
- ✅ **Print-ready** - Professional typesetting
- ✅ **Template engines** - Works with Jinja2, etc.

**Perfect for:**
- Teams with web development background
- Template-based document generation
- Complex layouts with CSS Grid/Flexbox
- Beautiful typography out of the box

**Installation:**
```bash
pip install weasyprint
```

**Dependencies:** Requires Cairo, Pango (system-level)

**Learning curve:** Low (if you know HTML/CSS)

---

### 3. Borb (Modern alternative)

**A more modern Python PDF library**

```python
from borb.pdf import Document, Page, Paragraph, PDF
from decimal import Decimal

# Create document
doc = Document()
page = Page()
doc.add_page(page)

# Add content
layout = PageLayout(page)
layout.add(Paragraph("Executive Summary",
                     font_size=Decimal(18),
                     font="Helvetica-Bold"))
layout.add(Paragraph("Body text..."))

# Save
with open("output.pdf", "wb") as pdf_file:
    PDF.dumps(pdf_file, doc)
```

**Why Borb?**
- ✅ **Modern API** - Cleaner than ReportLab
- ✅ **Read AND write** - Can modify existing PDFs
- ✅ **Type hints** - Full type safety
- ✅ **Good documentation** - Well-maintained
- ✅ **Active development** - Regular updates

**Perfect for:**
- New projects wanting modern Python
- Reading/modifying existing PDFs
- Type-safe document generation

**Installation:**
```bash
pip install borb
```

**Learning curve:** Medium

---

### 4. Jinja2 + WeasyPrint (Template-based approach)

**Separate content from layout completely**

```python
from jinja2 import Template
from weasyprint import HTML

# Define template
template = Template("""
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="clinical_standard.css">
</head>
<body>
    <h1>{{ title }}</h1>

    <div class="metadata-rail">
        <h2>{{ metadata.title }}</h2>
        {% for key, value in metadata.data.items() %}
        <div class="kv-pair">
            <span class="key">{{ key }}:</span>
            <span class="value">{{ value }}</span>
        </div>
        {% endfor %}
    </div>

    {% for section in sections %}
    <section>
        <h2>{{ section.title }}</h2>
        <p>{{ section.content }}</p>
    </section>
    {% endfor %}
</body>
</html>
""")

# Render with data
html = template.render(
    title="Research Report",
    metadata={
        'title': 'Subject Information',
        'data': {
            'Subject ID': '991-DELTA',
            'Timeline': '001-ORIGIN-TAM'
        }
    },
    sections=[
        {'title': 'Executive Summary', 'content': '...'},
        {'title': 'Methodology', 'content': '...'},
    ]
)

# Generate PDF
HTML(string=html).write_pdf('output.pdf')
```

**Why Jinja2 + WeasyPrint?**
- ✅ **Separation of concerns** - Content vs. presentation
- ✅ **Maintainable** - Non-programmers can edit templates
- ✅ **Reusable** - Same template, different data
- ✅ **Version control friendly** - Templates are text files
- ✅ **Preview in browser** - Debug HTML before PDF generation

**Perfect for:**
- Data-driven document generation
- Multiple document types from templates
- Non-technical content editors
- Organizations with design teams

---

## Comparison Matrix

| Feature | fpdf2 (V2) | ReportLab | WeasyPrint | Borb | Jinja2+Weasy |
|---------|------------|-----------|------------|------|--------------|
| **Ease of Use** | Medium | Medium | Easy | Medium | Easy |
| **Typography** | Basic | Advanced | Excellent | Good | Excellent |
| **Auto Layout** | Manual | Yes (Platypus) | Yes (CSS) | Yes | Yes (CSS) |
| **Templates** | No | Limited | Yes (HTML) | No | Yes (Jinja2) |
| **Dependencies** | None | Few | Many | Few | Many |
| **Performance** | Good | Excellent | Moderate | Good | Moderate |
| **Read PDFs** | No | Limited | No | Yes | No |
| **Learning Curve** | Low | Medium | Low* | Medium | Low* |
| **Production Ready** | Yes | Yes | Yes | Yes | Yes |
| **Cost** | Free | Free | Free | Free | Free |

*If you know HTML/CSS

---

## Recommendations for WAFT

### Immediate (Foundation V2.1): Keep fpdf2, Add Helpers

Stay with fpdf2 but add helper utilities:

```python
# Add automatic text flow
class AutoFlowText:
    """Automatically flow text across pages with word wrapping."""

# Add stylesheet support
class Stylesheet:
    """Define reusable text styles."""

# Add better table support
class SmartTable:
    """Tables with automatic column sizing."""
```

**Pros:** Incremental improvement, no new dependencies
**Cons:** Still limited by fpdf2's capabilities

---

### Short-term (Foundation V3): Migrate to ReportLab

Replace fpdf2 with ReportLab's Platypus framework:

```python
from waft.foundation_v3 import (
    DocumentEngine,  # Now wraps ReportLab
    ClinicalTemplate,
    Section,
    MetadataBox,
    # ... all the same blocks
)

# Same API, better output
engine = DocumentEngine(ClinicalTemplate())
engine.add(CoverPage(...))
engine.add(MetadataBox(...))
engine.render("output.pdf")
```

**Pros:**
- Keep our block-based API
- Get professional typography
- Automatic pagination
- Better tables
- Production-grade output

**Cons:**
- Migration effort (2-3 days)
- Slightly larger dependency

**Implementation strategy:**
1. Create `foundation_v3.py` using ReportLab
2. Keep same block API (transparent to users)
3. Add new features (better tables, charts, TOC)
4. Deprecate V2 gradually

---

### Long-term (Foundation V4): HTML/CSS Templates

Move to template-based generation:

```python
from waft.foundation_v4 import TemplateEngine

# Define template once
engine = TemplateEngine(template="clinical_standard.html")

# Generate many documents
for subject in subjects:
    engine.render(
        output=f"report_{subject.id}.pdf",
        data={
            'subject': subject,
            'timeline': subject.timeline,
            'measurements': subject.get_measurements(),
        }
    )
```

**Pros:**
- Non-programmers can edit templates
- CSS for styling (familiar to web devs)
- Preview in browser before PDF
- Easy to create multiple document types
- Version control friendly

**Cons:**
- Different paradigm (data + template vs. code)
- Requires system dependencies (Cairo)

---

## My Recommendation: Phased Approach

### Phase 1 (Now): Ship V2 with fpdf2
- ✅ You've already built this
- ✅ It works
- ✅ Zero external dependencies
- ✅ Gets you to production

### Phase 2 (Next sprint): Experiment with ReportLab
Create a parallel implementation:

```python
# src/waft/foundation_v3_reportlab.py
from reportlab.platypus import SimpleDocTemplate, Flowable

class ReportLabEngine:
    """ReportLab-based implementation with same API as V2."""

    def add(self, block):
        """Same fluent API."""
        return self
```

Test with same content, compare output quality.

### Phase 3 (After validation): Choose direction

**Option A:** Stick with fpdf2
- Good for: Simple documents, minimal dependencies
- Keep V2, add incremental improvements

**Option B:** Migrate to ReportLab
- Good for: Professional documents, complex layouts
- Port V2 API to ReportLab backend

**Option C:** Go template-based (Jinja2 + WeasyPrint)
- Good for: Multiple document types, design team
- Complete paradigm shift

---

## Code Example: Same API, Different Backend

Here's how you could keep the same API but swap backends:

```python
# foundation_v3_reportlab.py
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class DocumentEngine:
    """ReportLab backend with V2-compatible API."""

    def __init__(self, config):
        self.config = config
        self.story = []
        self.styles = getSampleStyleSheet()

    def add(self, block):
        """Same fluent API as V2."""
        flowable = block.to_reportlab_flowable(self.styles)
        self.story.append(flowable)
        return self

    def render(self, output_path):
        doc = SimpleDocTemplate(str(output_path))
        doc.build(self.story)
        return output_path

class SectionHeader:
    """Same block API as V2."""

    def __init__(self, title, level=1):
        self.title = title
        self.level = level

    def to_reportlab_flowable(self, styles):
        """Backend-specific conversion."""
        style = styles[f'Heading{self.level}']
        return Paragraph(self.title, style)

# Usage: IDENTICAL to V2
from waft.foundation_v3_reportlab import DocumentEngine, DocumentConfig

config = DocumentConfig.clinical_standard()
engine = DocumentEngine(config)
engine.add(SectionHeader("Title", level=1))
engine.add(TextBlock("Content..."))
engine.render(Path("output.pdf"))
```

---

## Quick Decision Matrix

**Choose fpdf2 (current V2) if:**
- ✅ You need minimal dependencies
- ✅ Documents are simple (< 10 pages)
- ✅ You want to ship NOW
- ✅ You're okay with manual layout

**Choose ReportLab if:**
- ✅ You need professional typography
- ✅ Documents are complex (20+ pages)
- ✅ You want automatic pagination
- ✅ You need advanced tables/charts
- ✅ You're building a production system

**Choose WeasyPrint if:**
- ✅ Your team knows HTML/CSS
- ✅ You want template-based workflow
- ✅ You need beautiful typography
- ✅ You're okay with system dependencies
- ✅ You want to preview in browser

**Choose Borb if:**
- ✅ You want modern Python APIs
- ✅ You need to read/modify PDFs
- ✅ You value type safety
- ✅ You're starting fresh

---

## Next Steps for WAFT

1. **Immediate:** Ship Foundation V2 with fpdf2 ✅ (done)

2. **This week:** Create proof-of-concept with ReportLab
   ```bash
   pip install reportlab
   python experiments/reportlab_poc.py
   ```

3. **Next week:** Compare outputs
   - Generate same document with V2 (fpdf2) and POC (ReportLab)
   - Evaluate typography, pagination, tables
   - Measure performance

4. **Decision point:** Choose backend for V3

5. **Future:** Consider template-based V4 for scaling

---

## Sample Migration Script

```python
"""
Proof of Concept: Foundation V2 API with ReportLab backend
"""

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

# Define Clinical Standard styles
def create_clinical_styles():
    styles = getSampleStyleSheet()

    # H1: Helvetica Bold 16pt
    styles.add(ParagraphStyle(
        name='ClinicalH1',
        fontName='Helvetica-Bold',
        fontSize=16,
        spaceAfter=12,
        textColor=colors.black,
    ))

    # Body: Times 11pt
    styles.add(ParagraphStyle(
        name='ClinicalBody',
        fontName='Times-Roman',
        fontSize=11,
        leading=15.4,  # 1.4x line spacing
        spaceAfter=8,
    ))

    return styles

# Generate document
doc = SimpleDocTemplate("clinical_poc.pdf")
styles = create_clinical_styles()
story = []

# Cover page
story.append(Paragraph("INSTITUTE FOR ADVANCED ONTOLOGICAL STUDIES",
                      styles['Title']))
story.append(Spacer(1, 0.5*inch))
story.append(PageBreak())

# Content
story.append(Paragraph("Executive Summary", styles['ClinicalH1']))
story.append(Paragraph("This demonstrates ReportLab with Clinical Standard styling...",
                      styles['ClinicalBody']))

# Table
data = [
    ['Parameter', 'Value', 'Unit', 'Status'],
    ['Coherence', '0.87', 'ratio', 'NORMAL'],
    ['Karma', '0', 'units', 'BASELINE'],
]
t = Table(data)
t.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
]))
story.append(t)

# Build
doc.build(story)
print("✅ Generated: clinical_poc.pdf")
```

---

## Resources

**ReportLab:**
- Docs: https://www.reportlab.com/docs/reportlab-userguide.pdf
- GitHub: https://github.com/MrBitBucket/reportlab-mirror

**WeasyPrint:**
- Docs: https://doc.courtbouillon.org/weasyprint/
- GitHub: https://github.com/Kozea/WeasyPrint

**Borb:**
- Docs: https://borb-pdf.readthedocs.io/
- GitHub: https://github.com/jorisschellekens/borb

**Jinja2:**
- Docs: https://jinja.palletsprojects.com/
- GitHub: https://github.com/pallets/jinja

---

*Foundation V2 is excellent with fpdf2. ReportLab would make it exceptional.*
