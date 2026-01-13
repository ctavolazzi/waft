# WeasyPrint vs ReportLab: Quick Reference

**Side-by-side code comparison for common tasks**

---

## 1. Basic Document

### WeasyPrint
```python
from weasyprint import HTML

html = """<!DOCTYPE html>
<html><body>
<h1>Title</h1>
<p>Content here</p>
</body></html>"""

HTML(string=html).write_pdf("output.pdf")
```

### ReportLab
```python
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("output.pdf")
styles = getSampleStyleSheet()
story = [
    Paragraph("Title", styles['Heading1']),
    Paragraph("Content here", styles['BodyText'])
]
doc.build(story)
```

---

## 2. Styling

### WeasyPrint (CSS)
```python
html = f"""<html>
<head><style>
body {{ font-family: Georgia; font-size: 11pt; }}
h1 {{ color: #2c3e50; font-size: 18pt; }}
</style></head>
<body>{content}</body></html>"""
```

### ReportLab (Python)
```python
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor

style = ParagraphStyle(
    'Custom',
    fontName='Georgia',
    fontSize=11,
    textColor=HexColor('#2c3e50')
)
```

---

## 3. Tables

### WeasyPrint (HTML)
```python
html = f"""
<table>
    <tr><th>Name</th><th>Value</th></tr>
    <tr><td>Item 1</td><td>100</td></tr>
</table>
"""
```

### ReportLab (Python)
```python
from reportlab.platypus import Table
from reportlab.lib import colors

data = [['Name', 'Value'], ['Item 1', '100']]
table = Table(data)
table.setStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
])
```

---

## 4. Markdown → PDF

### WeasyPrint
```python
import markdown
from weasyprint import HTML

html = markdown.markdown(md_content)
HTML(string=wrap_html(html)).write_pdf("output.pdf")
```
**Lines**: ~5  
**Time**: 2 minutes

### ReportLab
```python
# Must parse markdown manually
lines = md_content.split('\n')
story = []
for line in lines:
    if line.startswith('# '):
        story.append(Paragraph(line[2:], styles['Heading1']))
    # ... 50+ more lines
doc.build(story)
```
**Lines**: ~60  
**Time**: 30 minutes

---

## 5. Images

### WeasyPrint
```python
html = f'<img src="image.png" style="width: 200px;">'
```

### ReportLab
```python
from reportlab.platypus import Image
story.append(Image("image.png", width=200))
```

---

## 6. Page Breaks

### WeasyPrint (CSS)
```python
css = """
.page-break { page-break-after: always; }
"""
html = '<div class="page-break"></div>'
```

### ReportLab
```python
from reportlab.platypus import PageBreak
story.append(PageBreak())
```

---

## 7. Headers/Footers

### WeasyPrint (CSS @page)
```python
css = """
@page {
    @top-center { content: "Header Text"; }
    @bottom-center { content: "Page " counter(page); }
}
"""
```

### ReportLab (Python functions)
```python
def add_header(canvas, doc):
    canvas.saveState()
    canvas.drawString(72, 750, "Header Text")
    canvas.restoreState()

doc.build(story, onFirstPage=add_header, onLaterPages=add_header)
```

---

## 8. Multi-column Layout

### WeasyPrint (CSS)
```python
css = """
.columns { column-count: 2; column-gap: 20px; }
"""
html = '<div class="columns">Content...</div>'
```

### ReportLab (Frames)
```python
from reportlab.platypus import Frame, PageTemplate

frame1 = Frame(72, 72, 250, 700)
frame2 = Frame(330, 72, 250, 700)
page_template = PageTemplate(frames=[frame1, frame2])
doc.addPageTemplates([page_template])
```

---

## 9. Conditional Formatting

### WeasyPrint (CSS)
```python
css = """
tr:nth-child(even) { background-color: #f0f0f0; }
.highlight { background-color: yellow; }
"""
```

### ReportLab (Python)
```python
for i, row in enumerate(data):
    if i % 2 == 0:
        table.setStyle([('BACKGROUND', (0, i), (-1, i), colors.lightgrey)])
```

---

## 10. External Stylesheet

### WeasyPrint
```python
HTML(string=html, base_url='.').write_pdf("output.pdf")
# CSS file referenced in <link> tag
```

### ReportLab
```python
# Must load CSS and convert to Python styles manually
# No direct CSS file support
```

---

## Quick Decision Guide

**Use WeasyPrint when**:
- ✅ HTML/CSS content
- ✅ Markdown → PDF
- ✅ Web → PDF
- ✅ Template-based
- ✅ Rapid development

**Use ReportLab when**:
- ✅ Programmatic generation
- ✅ Small file sizes
- ✅ Precise typography
- ✅ No system deps
- ✅ Production systems

---

**See**: `WEASYPRINT_VS_REPORTLAB_DEEP_COMPARISON.md` for full analysis
