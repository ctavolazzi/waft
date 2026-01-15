# Unified PDF Class - Consolidation Complete

**Date**: 2026-01-12  
**Status**: ✅ Implemented

---

## Problem: Too Many Heads (Hydra)

WAFT had **10+ different classes** handling PDF production:

1. **PDFGenerator** - Evolution system (ChatDistiller + StylingGenome)
2. **DocumentBuilder** - Template system (WeasyPrint + Jinja2)
3. **DocumentEngine** (foundation.py) - Foundation V1 (FPDF2 blocks)
4. **DocumentEngine** (foundation_v2.py) - Foundation V2 (better typography)
5. **TwoPageGenerator** - Two-page constraint enforcement
6. **ScientificPDFGenerator** - Scientific papers
7. **ComponentPDFGenerator** - Component-based generation
8. **FlexiblePDFGenerator** - Flexible generation
9. **LaTeXGenerator** - LaTeX generation
10. **GoldenTriangle** - Simple markdown/HTML to PDF

**Result**: Confusion, code duplication, inconsistent APIs, hard to maintain.

---

## Solution: One Class, Many Methods

Created unified `PDF` class that consolidates all approaches:

```python
from waft import PDF

# All generation approaches in one class:
PDF.from_template(...)      # Template system
PDF.from_content(...)       # Evolution system
PDF.from_blocks(...)        # Foundation system
PDF.from_markdown(...)      # Simple markdown
PDF.from_html(...)          # Simple HTML
PDF.scientific_paper(...)   # Scientific papers
PDF.two_page(...)           # Two-page constraint
PDF.latex(...)              # LaTeX generation
PDF.from_file(...)          # Auto-detect from file
PDF.from_pdf(...)           # Analyze and recreate
```

---

## API Reference

### Template-Based Generation

```python
# Professional documents with consistent formatting
PDF.from_template(
    template="field_guide",
    title="My Guide",
    content="<h2>Introduction</h2><p>Content here</p>",
    printer_friendly=True
).save("output.pdf")
```

**Best for**: Professional documents, consistent formatting, template-based layouts.

**Uses**: DocumentBuilder + Template Registry + WeasyPrint

---

### Evolution-Based Generation

```python
# Markdown/text with automatic idea extraction
PDF.from_content(
    content="# My Document\n\nContent here...",
    title="My Document",
    style="clinical_standard",
    author="John Doe"
).save("output.pdf", open_pdf=True)
```

**Best for**: Markdown content, automatic idea extraction, styling presets.

**Uses**: PDFGenerator + ChatDistiller + StylingGenome + TwoPageGenerator

**Styles**: `clinical_standard`, `premium`, `professional`

---

### Foundation-Based Generation

```python
# Programmatic document construction
from waft.foundation import SectionHeader, TextBlock

PDF.from_blocks(
    title="My Report",
    blocks=[
        SectionHeader("Introduction"),
        TextBlock("Content here...")
    ],
    use_foundation_v2=True  # Better typography
).save("output.pdf")
```

**Best for**: Programmatic construction, precise control, block-based layouts.

**Uses**: DocumentEngine (Foundation V1 or V2) + FPDF2

---

### Simple Generation

```python
# Quick markdown/HTML to PDF
PDF.from_markdown("# Title\n\nContent").save("output.pdf")
PDF.from_html("<h1>Title</h1><p>Content</p>").save("output.pdf")
```

**Best for**: Quick conversions, simple documents.

**Uses**: GoldenTriangle

---

### Scientific Papers

```python
# Academic papers
PDF.scientific_paper(
    title="Research Paper",
    abstract="Abstract text...",
    content="<h2>Introduction</h2>...",
    authors=["John Doe", "Jane Smith"],
    affiliations=["University A", "University B"],
    references=["Ref 1", "Ref 2"]
).save("paper.pdf")
```

**Best for**: Academic papers, research documents.

**Uses**: ScientificPDFGenerator or academic_paper template

---

### Two-Page Constraint

```python
# Strict 2-page documents
PDF.two_page(
    content="# Title\n\nContent...",
    title="Two Page Doc",
    style="clinical_standard"
).save("two_page.pdf")
```

**Best for**: One-pagers, summaries, executive briefs.

**Uses**: TwoPageGenerator with adaptive constraint enforcement

---

### LaTeX Generation

```python
# LaTeX documents
PDF.latex(
    title="LaTeX Doc",
    content="\\section{Introduction}\n\\paragraph{Content}",
    compile_pdf=True  # Requires LaTeX installation
).save("latex.pdf")
```

**Best for**: Complex mathematical documents, academic papers.

**Uses**: LaTeXGenerator

---

### File-Based Generation

```python
# Auto-detect format
PDF.from_file("document.md", style="clinical_standard").save("output.pdf")
PDF.from_file("document.html", template="field_guide").save("output.pdf")
PDF.from_file("source.pdf").save("recreated.pdf")  # Analyze and recreate
```

**Best for**: Converting existing files, PDF recreation.

---

## Migration Guide

### Before (Many Classes)

```python
# Template system
from waft import DocumentBuilder
doc = DocumentBuilder.field_guide(title="Guide", content="...")
doc.save("output.pdf")

# Evolution system
from waft.evolution.pdf_generator import PDFGenerator
gen = PDFGenerator.from_content(content="...", title="Doc", style="clinical_standard")
gen.save("output.pdf")

# Foundation system
from waft.foundation import DocumentEngine, SectionHeader, TextBlock
engine = DocumentEngine(config)
engine.add(SectionHeader("Title"))
engine.add(TextBlock("Content"))
engine.render(Path("output.pdf"))
```

### After (One Class)

```python
from waft import PDF

# Template system
PDF.from_template("field_guide", "Guide", "...").save("output.pdf")

# Evolution system
PDF.from_content("...", "Doc", style="clinical_standard").save("output.pdf")

# Foundation system
PDF.from_blocks("Doc", [SectionHeader("Title"), TextBlock("Content")]).save("output.pdf")
```

---

## Benefits

1. **Single Entry Point**: One class for all PDF generation
2. **Consistent API**: Same pattern across all methods
3. **Easy to Use**: Clear method names indicate use case
4. **Maintainable**: One place to update, not 10+
5. **Discoverable**: All methods in one class, easy to find
6. **Flexible**: Can still use underlying systems directly if needed

---

## Implementation Details

- **Location**: `src/waft/pdf.py`
- **Backend Routing**: Automatically routes to appropriate backend based on method used
- **Configuration**: Unified `PDFConfig` dataclass for all options
- **Backward Compatible**: Underlying classes still available for advanced use cases

---

## Next Steps

1. ✅ Create unified `PDF` class
2. ⏳ Update examples to use unified class
3. ⏳ Update scripts to use unified class
4. ⏳ Add to main exports (`waft/__init__.py`)
5. ⏳ Create migration guide for existing code
6. ⏳ Deprecate old classes (with warnings)

---

**One class, many methods - the hydra is tamed! 🎯**
