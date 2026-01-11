# WAFT Scientific Document Generator - Roadmap to World-Class

**Goal:** Transform WAFT into a professional scientific document generation system capable of producing publication-quality papers, technical reports, and research documents.

---

## Phase 1: LaTeX Math & Equations (FOUNDATION)

**Priority:** CRITICAL - This is the #1 feature for scientific documents

### Features:
1. Inline math: `$E = mc^2$` renders within text
2. Display math: Block equations centered on page
3. Equation numbering: `(1)`, `(2)`, etc.
4. Equation references: "As shown in Equation (3)..."
5. Chemical formulas: `$\ce{H2O}$`, `$\ce{CO2}$`

### Implementation:
```python
# New classes in foundation.py

class MathInline(ContentBlock):
    """Inline LaTeX equation: $E = mc^2$"""
    def __init__(self, latex: str):
        self.latex = latex

    def to_html(self) -> str:
        return f'<span class="math-inline">{self.latex}</span>'

    def to_latex(self) -> str:
        return f"${self.latex}$"

class MathDisplay(ContentBlock):
    """Display LaTeX equation: $$\int_0^\infty e^{-x} dx = 1$$"""
    def __init__(self, latex: str, numbered: bool = True, label: str = None):
        self.latex = latex
        self.numbered = numbered
        self.label = label

    def to_html(self) -> str:
        return f'<div class="math-display">{self.latex}</div>'

    def to_latex(self) -> str:
        if self.numbered:
            return f"\\begin{{equation}}\n{self.latex}\n\\end{{equation}}"
        return f"$$\n{self.latex}\n$$"

class EquationRef(ContentBlock):
    """Reference to numbered equation"""
    def __init__(self, label: str):
        self.label = label
```

### Integration with WeasyPrint:
- Use **MathJax** for HTML rendering
- Add MathJax CDN to HTML template
- Equations render as beautiful typeset math

### Timeline: 2-3 days

---

## Phase 2: Citations & Bibliography

**Priority:** HIGH - Essential for academic papers

### Features:
1. In-text citations: `[1]`, `(Smith et al., 2024)`
2. Multiple citation styles (APA, IEEE, Nature, Chicago)
3. Bibliography generation at end of document
4. BibTeX file import
5. DOI/URL handling

### Implementation:
```python
class Citation(ContentBlock):
    """Citation reference: [1] or (Smith, 2024)"""
    def __init__(self, key: str, style: str = "numeric"):
        self.key = key
        self.style = style

class Bibliography(Section):
    """Auto-generated bibliography from citations"""
    def __init__(self, bibtex_file: str = None, style: str = "ieee"):
        self.bibtex_file = bibtex_file
        self.style = style
        self.entries = []
```

### Libraries:
- `pybtex` - BibTeX parsing
- `citeproc-py` - CSL style processing

### Timeline: 3-4 days

---

## Phase 3: Figures & Tables

**Priority:** HIGH - Core scientific content

### Features:
1. Automatic figure numbering (Figure 1, 2, 3...)
2. Captions with formatting
3. Cross-references: "See Figure 3"
4. List of figures at document start
5. Image embedding (PNG, JPG, SVG, PDF)
6. Multi-panel figures (A, B, C)
7. Table formatting with professional styling
8. Table captions and numbering

### Implementation:
```python
class Figure(ContentBlock):
    """Scientific figure with caption and numbering"""
    def __init__(
        self,
        image_path: str,
        caption: str,
        label: str = None,
        width: str = "100%"
    ):
        self.image_path = image_path
        self.caption = caption
        self.label = label
        self.width = width
        self.number = None  # Auto-assigned

class FigureRef(ContentBlock):
    """Reference to figure: 'Figure 3'"""
    def __init__(self, label: str):
        self.label = label

class Table(ContentBlock):
    """Scientific table with caption"""
    def __init__(
        self,
        data: List[List[str]],
        headers: List[str],
        caption: str,
        label: str = None
    ):
        self.data = data
        self.headers = headers
        self.caption = caption
        self.label = label
```

### Timeline: 3-4 days

---

## Phase 4: Code Blocks & Syntax Highlighting

**Priority:** MEDIUM - Important for technical docs

### Features:
1. Syntax highlighting (Python, JavaScript, C++, etc.)
2. Line numbering
3. Code captions/labels
4. Multiple color themes (light/dark)
5. Copy-friendly formatting

### Implementation:
```python
class CodeBlock(ContentBlock):
    """Syntax-highlighted code block"""
    def __init__(
        self,
        code: str,
        language: str = "python",
        line_numbers: bool = True,
        caption: str = None,
        label: str = None
    ):
        self.code = code
        self.language = language
        self.line_numbers = line_numbers
        self.caption = caption
```

### Libraries:
- `Pygments` - Syntax highlighting

### Timeline: 2 days

---

## Phase 5: Document Templates

**Priority:** MEDIUM - Makes system user-friendly

### Templates:
1. **Academic Paper** (IEEE, ACM, Nature format)
2. **Technical Report** (Government/corporate style)
3. **Thesis/Dissertation** (University format)
4. **White Paper** (Business/consulting style)
5. **Lab Report** (Scientific method format)
6. **Preprint** (arXiv style)

### Implementation:
```python
# templates/academic_paper.py

class AcademicPaper(Document):
    """IEEE-style academic paper template"""
    def __init__(self, title: str, authors: List[Author], abstract: str):
        super().__init__(title)
        self.add_title_page(authors)
        self.add_abstract(abstract)
        self.set_columns(2)  # Two-column layout
```

### Timeline: 4-5 days

---

## Phase 6: Advanced Features

**Priority:** LOW - Nice to have

### Features:
1. Multi-column layouts
2. Footnotes/endnotes
3. Glossary generation
4. Index generation
5. Appendices with separate numbering
6. PDF bookmarks/navigation
7. Hyperlinks (internal and external)
8. Watermarks
9. Track changes (diff between versions)

### Timeline: 5-7 days

---

## Phase 7: Full LaTeX Backend (Optional)

**Priority:** OPTIONAL - Alternative to WeasyPrint

### Why?
- Some journals require LaTeX submission
- Maximum typographic quality
- Native equation support

### Implementation:
- Add LaTeX exporter to Document class
- Generate .tex files
- Shell out to `pdflatex` for compilation
- Handle LaTeX packages and dependencies

### Timeline: 5-7 days

---

## Total Timeline Estimate

- **Phase 1 (Math):** 2-3 days
- **Phase 2 (Citations):** 3-4 days
- **Phase 3 (Figures/Tables):** 3-4 days
- **Phase 4 (Code):** 2 days
- **Phase 5 (Templates):** 4-5 days
- **Phase 6 (Advanced):** 5-7 days (optional)
- **Phase 7 (LaTeX):** 5-7 days (optional)

**Core Features (Phases 1-4):** ~12-15 days
**Full System (Phases 1-6):** ~20-27 days

---

## Competitive Analysis

### Similar Tools:
1. **Typst** - Modern LaTeX alternative (Rust-based)
2. **Quarto** - Pandoc-based scientific publishing
3. **Jupyter Book** - Python notebooks to books
4. **Sphinx** - Python documentation (used for scientific docs)
5. **R Markdown** - R-based scientific documents

### WAFT Advantages:
- ✅ Pure Python (no external compilers)
- ✅ Multiple output formats (PDF, HTML, Markdown)
- ✅ Programmatic generation (not just markup)
- ✅ Template system for reusable documents
- ✅ Custom styling per document type
- ✅ Integration with Python scientific stack (NumPy, Pandas, Matplotlib)

---

## Recommended First Step

**Start with Phase 1: LaTeX Math Support**

This is the single most important feature for scientific documents. Without it, the system can't handle most research papers or technical reports.

### Quick Win Implementation:
1. Add MathJax to WeasyPrint template (2 hours)
2. Create `MathInline` and `MathDisplay` classes (2 hours)
3. Test with sample equations (1 hour)
4. Update LIGHTCONE documents to use math rendering (2 hours)

**Total:** 1 day to add basic math support!

---

## Questions for You

1. **What's your primary use case?**
   - Academic papers for publication?
   - Technical reports for work?
   - Documentation?
   - All of the above?

2. **Which output format is most important?**
   - PDF only?
   - HTML (for web viewing)?
   - LaTeX (for journal submission)?

3. **Do you need collaboration features?**
   - Multiple authors?
   - Track changes?
   - Comments/reviews?

4. **Timeline preference?**
   - Build core features first (Phases 1-3)?
   - Or complete everything (all phases)?

5. **Target audience?**
   - Researchers/academics?
   - Engineers/technical writers?
   - General business users?

---

## Next Action

**Let me know:**
1. Should I start with Phase 1 (LaTeX math)?
2. Any other features you consider critical?
3. Do you want to see a proof-of-concept first?

I can have basic math rendering working in the LIGHTCONE documents within a few hours!
