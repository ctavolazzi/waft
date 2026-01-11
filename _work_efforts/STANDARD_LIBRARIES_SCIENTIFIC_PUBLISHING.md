# Standard Libraries for Scientific Document Generation

**Reference guide for building world-class scientific publishing systems**

These are the **standard, battle-tested libraries** used in professional scientific document generation projects like Jupyter Book, Quarto, Sphinx, and others.

---

## 📊 Core Document Generation

### 1. **WeasyPrint** ✓ *Already Using*
**Purpose:** HTML/CSS to PDF conversion
**Why:** Best Python solution for print-quality PDFs from web technologies
**Install:** `pip install weasyprint`

```python
from weasyprint import HTML
HTML(string=html_content).write_pdf('output.pdf')
```

**Pros:**
- Excellent CSS support (flexbox, grid, @page rules)
- Automatic pagination
- Professional typography
- Handles complex layouts

**Cons:**
- Requires system dependencies (cairo, pango)
- Limited interactive features

---

### 2. **Jinja2** ✓ *Already Using*
**Purpose:** Template engine
**Why:** Industry standard for Python templating
**Install:** `pip install jinja2`

```python
from jinja2 import Template
template = Template('<h1>{{ title }}</h1>')
output = template.render(title="My Document")
```

**Used by:** Flask, Django, Ansible, Sphinx, Quarto

---

### 3. **ReportLab**
**Purpose:** Low-level PDF generation (alternative to FPDF)
**Why:** More powerful and maintained than FPDF
**Install:** `pip install reportlab`

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

c = canvas.Canvas("doc.pdf", pagesize=letter)
c.drawString(100, 750, "Hello World")
c.save()
```

**Pros:**
- Very mature (20+ years)
- Full PDF control
- Good documentation
- Commercial support available

**Consider:** If WeasyPrint doesn't work for your use case

---

## 🔢 Math & Equations

### 4. **MathJax** (JavaScript)
**Purpose:** Render LaTeX equations in HTML/PDF
**Why:** Industry standard for web-based math rendering
**Install:** CDN link in HTML

```html
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

<p>Inline: \(E = mc^2\)</p>
<p>Display: $$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$</p>
```

**Used by:** Jupyter, Stack Overflow, Wikipedia, arXiv

**WeasyPrint Integration:**
- MathJax can render to SVG/HTML that WeasyPrint can handle
- Use `mathjax-node-cli` for server-side rendering

---

### 5. **SymPy**
**Purpose:** Symbolic mathematics in Python
**Why:** Generate LaTeX from Python expressions
**Install:** `pip install sympy`

```python
from sympy import Symbol, integrate, latex

x = Symbol('x')
expr = integrate(x**2, x)
latex_code = latex(expr)  # Returns: "\frac{x^{3}}{3}"
```

**Use case:** Programmatically generate equations

---

### 6. **latex2mathml**
**Purpose:** Convert LaTeX to MathML
**Why:** MathML is better for accessibility
**Install:** `pip install latex2mathml`

```python
from latex2mathml.converter import convert
mathml = convert(r'\frac{1}{2}')
```

---

## 📚 Citations & Bibliography

### 7. **pybtex**
**Purpose:** BibTeX parsing and formatting
**Why:** Standard Python BibTeX library
**Install:** `pip install pybtex`

```python
from pybtex.database import parse_file

bib_data = parse_file('references.bib')
for entry in bib_data.entries.values():
    print(entry.fields['title'])
```

**Features:**
- Parse `.bib` files
- Format citations in multiple styles
- Generate bibliographies

---

### 8. **citeproc-py**
**Purpose:** Citation Style Language (CSL) processor
**Why:** Support 1000+ citation styles (APA, MLA, Chicago, IEEE, Nature, etc.)
**Install:** `pip install citeproc-py`

```python
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import Citation, CitationItem
from citeproc.source.json import CiteProcJSON

# Load CSL style (e.g., IEEE, APA)
style = CitationStylesStyle('ieee')
bib = CitationStylesBibliography(style, source)

# Generate citation
citation = Citation([CitationItem('smith2024')])
formatted = bib.format_citation(citation)
```

**CSL Styles:** https://github.com/citation-style-language/styles

**Used by:** Zotero, Mendeley, Paperpile

---

### 9. **crossrefapi**
**Purpose:** Look up DOI metadata from CrossRef
**Why:** Auto-populate citations from DOIs
**Install:** `pip install crossrefapi`

```python
from crossref.restful import Works

works = Works()
paper = works.doi('10.1038/nature12373')
print(paper['title'])
print(paper['author'])
```

**Use case:** User pastes DOI, system fetches full citation

---

## 📊 Tables & Data

### 10. **pandas**
**Purpose:** Data manipulation and analysis
**Why:** Industry standard for tabular data
**Install:** `pip install pandas`

```python
import pandas as pd

df = pd.DataFrame({
    'Name': ['Alice', 'Bob'],
    'Score': [95, 87]
})

# Export to HTML table
html_table = df.to_html()

# Export to LaTeX table
latex_table = df.to_latex()
```

**Used by:** Everyone in scientific Python

---

### 11. **tabulate**
**Purpose:** Pretty-print tabular data
**Why:** Easy ASCII/HTML/LaTeX table generation
**Install:** `pip install tabulate`

```python
from tabulate import tabulate

data = [['Alice', 95], ['Bob', 87]]
headers = ['Name', 'Score']

print(tabulate(data, headers, tablefmt='grid'))
# ┌───────┬───────┐
# │ Name  │ Score │
# ├───────┼───────┤
# │ Alice │    95 │
# │ Bob   │    87 │
# └───────┴───────┘
```

**Formats:** grid, pipe, html, latex, github markdown

---

## 📈 Figures & Plotting

### 12. **matplotlib**
**Purpose:** Plotting library
**Why:** Standard Python plotting
**Install:** `pip install matplotlib`

```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [1, 4, 9])
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
```

**Output:** High-quality PNG, PDF, SVG for documents

---

### 13. **seaborn**
**Purpose:** Statistical plotting
**Why:** Beautiful plots with less code
**Install:** `pip install seaborn`

```python
import seaborn as sns

sns.set_style('whitegrid')
sns.lineplot(x=[1,2,3], y=[1,4,9])
plt.savefig('plot.png', dpi=300)
```

**Use case:** Scientific visualizations

---

### 14. **plotly**
**Purpose:** Interactive plots
**Why:** Modern, interactive visualizations
**Install:** `pip install plotly`

```python
import plotly.graph_objects as go

fig = go.Figure(data=go.Scatter(x=[1,2,3], y=[1,4,9]))
fig.write_image('plot.png')  # Static image
fig.write_html('plot.html')  # Interactive HTML
```

**Use case:** Web-based interactive documents

---

### 15. **Pillow (PIL)**
**Purpose:** Image processing
**Why:** Load, resize, manipulate images
**Install:** `pip install Pillow`

```python
from PIL import Image

img = Image.open('photo.jpg')
img_resized = img.resize((800, 600))
img_resized.save('photo_small.jpg', quality=95)
```

**Use case:** Optimize images for PDF inclusion

---

## 💻 Code Highlighting

### 16. **Pygments**
**Purpose:** Syntax highlighting for 500+ languages
**Why:** Industry standard
**Install:** `pip install pygments`

```python
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

code = "def hello(): print('world')"
highlighted = highlight(code, PythonLexer(), HtmlFormatter())
```

**Output:** HTML/LaTeX with syntax colors

**Used by:** GitHub, Sphinx, Jupyter

---

## 📄 Document Conversion

### 17. **pypandoc**
**Purpose:** Universal document converter (Python wrapper for Pandoc)
**Why:** Convert between formats (Markdown ↔ LaTeX ↔ HTML ↔ DOCX)
**Install:** `pip install pypandoc`

```python
import pypandoc

# Markdown to LaTeX
output = pypandoc.convert_text('# Hello', 'latex', format='md')

# Markdown to DOCX
pypandoc.convert_file('input.md', 'docx', outputfile='output.docx')
```

**Pandoc supports:** 40+ formats

**Use case:** Export to Word, LaTeX, etc.

---

## 🔧 PDF Utilities

### 18. **PyPDF2** (or **pypdf**)
**Purpose:** PDF manipulation (merge, split, rotate)
**Why:** Useful for combining generated PDFs
**Install:** `pip install pypdf`

```python
from pypdf import PdfMerger

merger = PdfMerger()
merger.append('doc1.pdf')
merger.append('doc2.pdf')
merger.write('combined.pdf')
```

**Use case:** Merge multiple documents into one binder

---

### 19. **pdfrw**
**Purpose:** Low-level PDF reading/writing
**Why:** Modify PDFs, add metadata, watermarks
**Install:** `pip install pdfrw`

```python
from pdfrw import PdfReader, PdfWriter

pdf = PdfReader('input.pdf')
pdf.Info.Title = 'My Document'
PdfWriter('output.pdf', trailer=pdf).write()
```

---

## 🖋️ Typography

### 20. **fonttools** ✓ *Already Installed*
**Purpose:** Font manipulation
**Why:** Embed fonts, convert formats
**Install:** `pip install fonttools`

```python
from fontTools.ttLib import TTFont

font = TTFont('myfont.ttf')
print(font['name'].names)
```

**Use case:** Ensure fonts embed correctly in PDFs

---

## 📐 Layout & Styling

### 21. **python-bidi**
**Purpose:** Bidirectional text (Arabic, Hebrew)
**Why:** Support right-to-left languages
**Install:** `pip install python-bidi`

```python
from bidi.algorithm import get_display

arabic_text = "مرحبا"
display_text = get_display(arabic_text)
```

**Use case:** International scientific publishing

---

## 🔬 Scientific Computing (Context)

These aren't document libraries, but are often used alongside them:

### 22. **NumPy**
```bash
pip install numpy
```
Numerical arrays, used for data in figures/tables

### 23. **SciPy**
```bash
pip install scipy
```
Scientific computing (stats, optimization, signal processing)

### 24. **scikit-learn**
```bash
pip install scikit-learn
```
Machine learning (generate results for papers)

---

## 🎯 Recommended Stack for WAFT

**Tier 1: Core (Implement First)**
1. ✅ WeasyPrint - PDF generation
2. ✅ Jinja2 - Templates
3. 🔲 MathJax - Equations
4. 🔲 Pygments - Code highlighting
5. 🔲 pybtex - Citations

**Tier 2: Enhanced Features**
6. 🔲 matplotlib - Figures
7. 🔲 pandas - Tables
8. 🔲 citeproc-py - Citation styles
9. 🔲 tabulate - Simple tables

**Tier 3: Advanced**
10. 🔲 pypandoc - Multi-format export
11. 🔲 pypdf - PDF manipulation
12. 🔲 SymPy - Symbolic math
13. 🔲 crossrefapi - DOI lookups

**Tier 4: Optional**
14. 🔲 plotly - Interactive plots
15. 🔲 python-bidi - International text
16. 🔲 latex2mathml - Accessibility

---

## 📦 Installation Command

Install core scientific stack:

```bash
pip install weasyprint jinja2 pygments pybtex matplotlib pandas tabulate pillow
```

Install enhanced stack:

```bash
pip install citeproc-py pypandoc pypdf sympy crossrefapi seaborn plotly
```

---

## 🏆 What Makes WAFT Competitive?

**Existing strengths:**
- ✅ Pure Python (no LaTeX compiler needed)
- ✅ Multiple output formats
- ✅ Programmatic generation
- ✅ Template system

**Add these for world-class:**
- 🎯 MathJax integration → equations
- 🎯 Pygments integration → code
- 🎯 pybtex integration → citations
- 🎯 matplotlib integration → figures
- 🎯 pandas integration → tables

**Result:** System competitive with Quarto, Jupyter Book, Sphinx

---

## 🔍 Comparison to Other Systems

| Feature | WAFT | Quarto | Jupyter Book | Sphinx |
|---------|------|--------|--------------|--------|
| **Pure Python** | ✅ | ❌ (Lua) | ✅ | ✅ |
| **No LaTeX Required** | ✅ | ❌ | ✅ | ✅ |
| **Programmatic** | ✅ | ❌ | 🟡 | 🟡 |
| **Templates** | ✅ | ✅ | 🟡 | ✅ |
| **Equations** | 🔲 | ✅ | ✅ | ✅ |
| **Citations** | 🔲 | ✅ | ✅ | ✅ |
| **Code Highlighting** | 🔲 | ✅ | ✅ | ✅ |
| **Multi-format Export** | ✅ | ✅ | ✅ | ✅ |

**Legend:**
- ✅ Fully supported
- 🟡 Partially supported
- 🔲 Planned
- ❌ Not supported

---

## 📖 References

- **WeasyPrint:** https://weasyprint.org/
- **Jinja2:** https://jinja.palletsprojects.com/
- **Pygments:** https://pygments.org/
- **pybtex:** https://pybtex.org/
- **MathJax:** https://www.mathjax.org/
- **CSL Styles:** https://citationstyles.org/
- **Pandoc:** https://pandoc.org/

---

## ✅ Next Steps for WAFT

1. **Test simple template** - Verify it works (DONE ✓)
2. **Add MathJax** - Equations are critical
3. **Add Pygments** - Code highlighting
4. **Add pybtex** - Basic citations
5. **Integrate matplotlib** - Figure generation
6. **Create examples** - Show off capabilities

**Timeline:** Core features (MathJax, Pygments, pybtex) = 3-5 days

---

**Ready to proceed?** Let me know which library to integrate first!
