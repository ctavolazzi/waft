# LaTeX Alternatives Evaluation

**Date:** 2026-01-16  
**Work Effort:** WE-260116-5exf  
**Purpose:** Comprehensive evaluation of modern LaTeX alternatives for WAFT's typesetting needs

---

## Executive Summary

This document evaluates modern typesetting alternatives to LaTeX, comparing Typst, ConTeXt, Quarto, and Pandoc against WAFT's existing LaTeX infrastructure and other PDF generation systems (WeasyPrint, FPDF2).

**Key Findings:**
- **Typst**: Most promising modern alternative with simpler syntax and faster compilation
- **ConTeXt**: Better consistency but still TeX-based, less ecosystem support
- **Quarto**: Excellent for reproducible research but overkill for general templates
- **Pandoc**: Good for Markdown workflows but limited template control
- **Recommendation**: Continue with LaTeX for existing templates, consider Typst for new templates

---

## Current WAFT PDF Generation Systems

### 1. LaTeX System (Production)
**Location:** `src/waft/templates/latex/`
- **Compiler:** `LaTeXCompiler` class using `pdflatex`/`xelatex`
- **Registry:** `LaTeXTemplateRegistry` with auto-discovery
- **Templates:** 9+ wrapper modules (formal_letter, essay, presentation, etc.)
- **Status:** ✅ Production, actively used

**Strengths:**
- Professional typography
- Extensive template library
- Well-established ecosystem
- Auto-discovery system

**Weaknesses:**
- Slow compilation (multiple runs needed)
- Complex syntax
- Package dependency management
- Large installation footprint

### 2. WeasyPrint + HTML + Jinja2 (Production)
**Location:** `src/waft/templates/`
- **Technology:** HTML/CSS to PDF conversion
- **Status:** ✅ Production, proven

**Strengths:**
- Beautiful output
- Automatic formatting
- Flexible layouts
- Familiar web syntax

**Weaknesses:**
- System dependencies (Cairo, Pango)
- Requires HTML knowledge
- Less suitable for academic documents

### 3. FPDF2 (Production)
**Location:** `src/waft/foundation.py`
- **Technology:** Pure Python PDF generation
- **Status:** ✅ Production

**Strengths:**
- Pure Python (no system deps)
- Simple API
- Lightweight

**Weaknesses:**
- Manual positioning
- Basic typography
- Limited automatic layout

---

## System Evaluations

### Typst

**Overview:**
Modern typesetting system written in Rust, designed as a LaTeX alternative with simpler syntax, faster compilation, and better error messages.

**Key Features:**
- Simpler syntax (Markdown-like with extensions)
- Fast compilation (single pass, no multiple runs)
- Built-in scripting language
- Better error messages
- Modern tooling (CLI, web editor)

**Syntax Example:**
```typst
#set page(margin: 2cm)
#set text(font: "Linux Libertine", size: 11pt)

= Introduction
This is a paragraph with *bold* and _italic_ text.

#figure(
  image("diagram.png"),
  caption: [Diagram showing the process]
)
```

**Python Integration:**
- ✅ CLI available (`typst compile input.typ output.pdf`)
- ✅ Can be called via subprocess (similar to LaTeXCompiler)
- ✅ JSON API available for programmatic access
- ⚠️ No native Python library (yet)

**Compilation Speed:**
- **Typst:** Single pass, typically < 1 second for typical documents
- **LaTeX:** Multiple passes (2-3 runs), typically 2-5 seconds

**Feature Completeness:**
- ✅ Math support (similar to LaTeX)
- ✅ Tables, figures, cross-references
- ✅ Bibliography support (via packages)
- ✅ Custom functions and scripting
- ⚠️ Smaller package ecosystem than LaTeX

**Template System Compatibility:**
- Can generate Typst source from Python (similar to LaTeX)
- Template registry could be extended to support Typst
- Would need new `TypstCompiler` class

**Dependencies:**
- Single binary executable (~10MB)
- No system dependencies
- Easy installation: `cargo install typst-cli` or download binary

**Ecosystem:**
- Growing community
- Active development
- Package system (but smaller than LaTeX)

**Migration Path:**
- **Effort:** Medium (2-3 days per template)
- **Process:** Convert LaTeX syntax to Typst syntax
- **Compatibility:** Most features have Typst equivalents
- **Risk:** Medium (new syntax to learn)

**Pros:**
- ✅ Much faster compilation
- ✅ Simpler syntax (easier to learn)
- ✅ Better error messages
- ✅ Built-in scripting
- ✅ Single binary (easy deployment)
- ✅ Modern tooling

**Cons:**
- ❌ Smaller ecosystem than LaTeX
- ❌ Less mature (newer project)
- ❌ Some LaTeX packages don't have equivalents
- ❌ Migration effort for existing templates

**WAFT Integration Feasibility:** ⭐⭐⭐⭐ (High)
- Can integrate similar to LaTeXCompiler
- Would need TypstCompiler class
- Template wrappers can generate Typst source
- Registry can be extended

---

### ConTeXt

**Overview:**
Powerful TeX variant offering more control and consistency out-of-the-box, with less reliance on external packages than LaTeX.

**Key Features:**
- Everything included (fewer package dependencies)
- Consistent configuration syntax
- Better control over layout
- Unified interface for all features

**Syntax Example:**
```context
\starttext
\section[title={Introduction}]
This is a paragraph with \bold{bold} and \em{italic} text.

\placefigure[here][fig:diagram]
  {\externalfigure[diagram.png][width=8cm]}
  {Diagram showing the process}

\stoptext
```

**Python Integration:**
- ✅ CLI available (`context input.tex`)
- ✅ Can be called via subprocess
- ⚠️ Similar to LaTeX (TeX-based)

**Compilation Speed:**
- Similar to LaTeX (multiple passes)
- Slightly faster due to better caching

**Feature Completeness:**
- ✅ Excellent math support
- ✅ Advanced layout control
- ✅ Built-in features (no packages needed)
- ✅ Better consistency than LaTeX

**Template System Compatibility:**
- Would need ConTeXtCompiler class
- Different syntax from LaTeX (not compatible)
- Would require new template wrappers

**Dependencies:**
- Full TeX Live distribution (large, ~4GB)
- Or ConTeXt standalone (~200MB)
- System dependencies similar to LaTeX

**Ecosystem:**
- Smaller community than LaTeX
- Less widely adopted
- Good documentation but fewer examples

**Migration Path:**
- **Effort:** High (3-5 days per template)
- **Process:** Complete rewrite (different syntax)
- **Compatibility:** Not compatible with LaTeX
- **Risk:** High (significant learning curve)

**Pros:**
- ✅ More consistent than LaTeX
- ✅ Better layout control
- ✅ Everything included (fewer packages)
- ✅ Professional output

**Cons:**
- ❌ Different syntax (not LaTeX-compatible)
- ❌ Smaller ecosystem
- ❌ Less widely adopted
- ❌ Similar compilation speed to LaTeX
- ❌ Large installation

**WAFT Integration Feasibility:** ⭐⭐⭐ (Medium)
- Can integrate but requires new compiler class
- Templates need complete rewrite
- Less ecosystem support than LaTeX

---

### Quarto

**Overview:**
Modern, reproducible technical publishing system combining Markdown with powerful code execution and output.

**Key Features:**
- Markdown-based (familiar syntax)
- Code execution (R, Python, Julia, etc.)
- Multiple output formats (PDF, HTML, DOCX, etc.)
- Reproducible research workflows
- Built on Pandoc

**Syntax Example:**
```markdown
---
title: "Document Title"
format: pdf
---

# Introduction

This is a paragraph with **bold** and *italic* text.

```{python}
import matplotlib.pyplot as plt
plt.plot([1, 2, 3])
plt.show()
```

![Diagram](diagram.png)
```

**Python Integration:**
- ✅ CLI available (`quarto render document.qmd`)
- ✅ Python execution support
- ✅ Can be called via subprocess
- ✅ Python API available (`quarto.render()`)

**Compilation Speed:**
- Uses Pandoc (which uses LaTeX for PDF)
- Similar speed to LaTeX (multiple passes)

**Feature Completeness:**
- ✅ Excellent for research documents
- ✅ Code execution and output
- ✅ Multiple output formats
- ✅ Bibliography support
- ⚠️ Less control over typography than LaTeX

**Template System Compatibility:**
- Different paradigm (Markdown + YAML frontmatter)
- Would need QuartoCompiler class
- Templates would be Markdown-based

**Dependencies:**
- Quarto CLI (~100MB)
- Requires LaTeX or ConTeXt for PDF output
- Python/R/Julia for code execution

**Ecosystem:**
- Growing rapidly
- Strong focus on reproducible research
- Good documentation

**Migration Path:**
- **Effort:** High (3-4 days per template)
- **Process:** Convert to Markdown + YAML
- **Compatibility:** Different paradigm
- **Risk:** Medium-High (paradigm shift)

**Pros:**
- ✅ Excellent for reproducible research
- ✅ Markdown syntax (familiar)
- ✅ Code execution built-in
- ✅ Multiple output formats
- ✅ Modern tooling

**Cons:**
- ❌ Overkill for simple documents
- ❌ Less typography control than LaTeX
- ❌ Still requires LaTeX for PDF
- ❌ Different paradigm (not template-based)
- ❌ Learning curve for advanced features

**WAFT Integration Feasibility:** ⭐⭐⭐ (Medium)
- Good for research documents
- Less suitable for general templates
- Would require paradigm shift
- Better for specific use cases (scientific reports)

---

### Pandoc

**Overview:**
Universal document converter, excellent for Markdown-to-PDF workflows.

**Key Features:**
- Markdown input
- Multiple output formats
- Template system
- Bibliography support
- Extensible filters

**Syntax Example:**
```markdown
---
title: "Document Title"
author: "Author Name"
---

# Introduction

This is a paragraph with **bold** and *italic* text.

![Diagram](diagram.png)
```

**Python Integration:**
- ✅ CLI available (`pandoc input.md -o output.pdf`)
- ✅ Can be called via subprocess
- ✅ Python library available (`pypandoc`)

**Compilation Speed:**
- Uses LaTeX/ConTeXt for PDF (similar speed)
- Fast for simple documents

**Feature Completeness:**
- ✅ Good Markdown support
- ✅ Template system
- ✅ Bibliography support
- ⚠️ Limited typography control
- ⚠️ Less suitable for complex layouts

**Template System Compatibility:**
- Can use Pandoc templates
- Would need PandocCompiler class
- Templates would be Markdown-based

**Dependencies:**
- Pandoc binary (~50MB)
- Requires LaTeX/ConTeXt for PDF output
- System dependencies

**Ecosystem:**
- Very mature
- Widely used
- Good documentation

**Migration Path:**
- **Effort:** Medium (2-3 days per template)
- **Process:** Convert to Markdown
- **Compatibility:** Different format
- **Risk:** Medium (simpler but less control)

**Pros:**
- ✅ Simple Markdown syntax
- ✅ Multiple output formats
- ✅ Mature and stable
- ✅ Good for simple documents
- ✅ Template system

**Cons:**
- ❌ Less typography control
- ❌ Still requires LaTeX for PDF
- ❌ Limited for complex layouts
- ❌ Less suitable for academic documents

**WAFT Integration Feasibility:** ⭐⭐⭐ (Medium)
- Good for Markdown workflows
- Less suitable for complex templates
- Would complement existing systems
- Better for simple document generation

---

## Comparison Matrix

| Criterion | LaTeX | Typst | ConTeXt | Quarto | Pandoc | WeasyPrint | FPDF2 |
|-----------|-------|-------|---------|--------|--------|------------|-------|
| **Syntax Simplicity** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Compilation Speed** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Typography Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **Math Support** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐ |
| **Template Control** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Ecosystem** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Python Integration** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Installation Size** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Learning Curve** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **WAFT Integration** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## Integration Feasibility Analysis

### Typst Integration

**Feasibility:** High ⭐⭐⭐⭐

**Implementation Approach:**
1. Create `TypstCompiler` class (similar to `LaTeXCompiler`)
2. Extend `LaTeXTemplateRegistry` to support Typst templates
3. Create Typst template wrappers (convert from LaTeX syntax)
4. Add Typst template discovery

**Code Structure:**
```python
# src/waft/templates/typst/compiler.py
class TypstCompiler:
    def compile(self, typst_content: str, output_path: Path) -> Path:
        # Call typst CLI via subprocess
        subprocess.run(["typst", "compile", input_file, output_path])
```

**Effort Estimate:** 2-3 days
- Compiler class: 4 hours
- Registry extension: 4 hours
- Template conversion: 1-2 days (per template)

**Pros:**
- Similar integration pattern to LaTeX
- Faster compilation
- Simpler syntax

**Cons:**
- New syntax to learn
- Smaller ecosystem

---

### ConTeXt Integration

**Feasibility:** Medium ⭐⭐⭐

**Implementation Approach:**
1. Create `ConTeXtCompiler` class
2. Create new template wrappers (different syntax)
3. Extend registry for ConTeXt templates

**Effort Estimate:** 3-5 days per template
- Complete rewrite needed
- Different syntax paradigm

**Pros:**
- Better consistency
- Professional output

**Cons:**
- High migration effort
- Smaller ecosystem
- Similar speed to LaTeX

---

### Quarto Integration

**Feasibility:** Medium ⭐⭐⭐

**Implementation Approach:**
1. Create `QuartoCompiler` class
2. Convert templates to Markdown + YAML
3. Support code execution

**Effort Estimate:** 3-4 days per template
- Paradigm shift to Markdown
- Code execution setup

**Pros:**
- Excellent for research
- Markdown syntax

**Cons:**
- Overkill for simple templates
- Still requires LaTeX
- Different paradigm

---

### Pandoc Integration

**Feasibility:** Medium ⭐⭐⭐

**Implementation Approach:**
1. Create `PandocCompiler` class
2. Convert templates to Markdown
3. Use Pandoc templates

**Effort Estimate:** 2-3 days per template
- Simpler conversion
- Less control

**Pros:**
- Simple Markdown
- Mature tool

**Cons:**
- Less typography control
- Still requires LaTeX
- Limited for complex layouts

---

## Migration Effort Estimates

### From LaTeX to Typst

**Per Template:** 2-3 days
- Syntax conversion: 1-2 days
- Testing and refinement: 1 day

**Total (9 templates):** 18-27 days

**Process:**
1. Convert LaTeX syntax to Typst
2. Test compilation
3. Adjust formatting
4. Update wrapper functions

**Example Conversion:**
```latex
% LaTeX
\documentclass[11pt]{article}
\usepackage{geometry}
\geometry{margin=1in}
\begin{document}
\section{Introduction}
Content here.
\end{document}
```

```typst
// Typst
#set page(margin: 1in)
#set text(size: 11pt)

= Introduction
Content here.
```

---

### From LaTeX to ConTeXt

**Per Template:** 3-5 days
- Complete rewrite: 2-3 days
- Testing: 1-2 days

**Total (9 templates):** 27-45 days

**Process:**
1. Rewrite in ConTeXt syntax
2. Test compilation
3. Adjust layout
4. Update wrapper functions

---

### From LaTeX to Quarto

**Per Template:** 3-4 days
- Markdown conversion: 2 days
- YAML frontmatter: 0.5 day
- Testing: 1-1.5 days

**Total (9 templates):** 27-36 days

---

### From LaTeX to Pandoc

**Per Template:** 2-3 days
- Markdown conversion: 1-2 days
- Template setup: 0.5 day
- Testing: 0.5-1 day

**Total (9 templates):** 18-27 days

---

## Recommendations

### Short-term (Current Templates)

**Recommendation:** Continue with LaTeX

**Rationale:**
- Existing templates are working
- Large ecosystem and community
- Professional output quality
- Integration already complete

**Action Items:**
- Maintain existing LaTeX templates
- Optimize compilation (caching, parallel builds)
- Document best practices

---

### Medium-term (New Templates)

**Recommendation:** Consider Typst for new templates

**Rationale:**
- Faster compilation
- Simpler syntax (easier to maintain)
- Modern tooling
- Good integration feasibility

**Action Items:**
1. Create TypstCompiler class
2. Convert 1-2 templates as proof of concept
3. Evaluate results
4. Decide on broader adoption

**Pilot Templates:**
- Simple document (e.g., essay)
- Complex document (e.g., project report)

---

### Long-term (Strategic)

**Recommendation:** Hybrid approach

**Rationale:**
- Different tools for different use cases
- Leverage strengths of each system

**Tool Selection Guide:**

| Use Case | Recommended Tool |
|----------|------------------|
| Academic papers | LaTeX or Typst |
| Simple documents | Pandoc or WeasyPrint |
| Research reports | Quarto |
| Business letters | LaTeX or Typst |
| Web-based templates | WeasyPrint |
| Programmatic generation | FPDF2 or ReportLab |

**Action Items:**
1. Maintain LaTeX for complex academic documents
2. Use Typst for new templates (faster, simpler)
3. Use WeasyPrint for web-style templates
4. Use Quarto for reproducible research
5. Use Pandoc for Markdown workflows

---

## Next Steps

1. **Immediate (This Week)**
   - ✅ Complete this evaluation document
   - Create TypstCompiler proof of concept
   - Test Typst with one simple template

2. **Short-term (Next Sprint)**
   - Evaluate TypstCompiler results
   - Document Typst integration approach
   - Create migration guide

3. **Medium-term (Next Quarter)**
   - Convert 1-2 templates to Typst
   - Compare output quality and speed
   - Make adoption decision

4. **Long-term (Future)**
   - Consider hybrid approach
   - Maintain multiple systems for different use cases
   - Document tool selection guidelines

---

## References

1. [Typesetting Comparison](https://jbirnick.net/posts/typesetting-comparison/)
2. [LaTeX Alternatives (TeX.SE)](https://tex.stackexchange.com/questions/120271/alternatives-to-latex)
3. [LaTeX Alternatives (Octree)](https://www.useoctree.com/blog/latex-alternatives-document-preparation-options)
4. [Typst Reddit Discussion](https://www.reddit.com/r/rust/comments/11xpg6e/typst_a_modern_latex_alternative_written_in_rust/)
5. [Typst YouTube Video](https://www.youtube.com/watch?v=NTGkb4FCLhM)
6. [Stack Overflow: LaTeX Alternatives](https://stackoverflow.com/questions/2705468/alternative-to-latex-a-way-to-typeset-good-looking-documents-from-java-to-pdf)

---

## Related Work

- `WE-260116-xkhg`: Formal letter template evaluation (chose LaTeX over ConTeXt/Typst)
- `docs/FOUNDATION_V3_ROADMAP.md`: ReportLab/WeasyPrint alternatives for Foundation system
- `WAFT-Mac-Shortcuts-Research/notes/pdf_systems_analysis.md`: Current PDF systems analysis

---

**Status:** Evaluation Complete  
**Last Updated:** 2026-01-16  
**Next Review:** After TypstCompiler proof of concept
