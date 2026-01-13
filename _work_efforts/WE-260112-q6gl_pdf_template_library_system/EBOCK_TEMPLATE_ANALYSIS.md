# eBook-Template Repository Analysis

**Date:** 2026-01-12  
**Repository:** https://github.com/akosma/eBook-Template.git  
**Status:** Archived (May 22, 2025)  
**Purpose:** Compare Asciidoctor-based eBook generation with WAFT's PDF systems

---

## Executive Summary

The **eBook-Template** repository provides a comprehensive Asciidoctor-based workflow for generating multiple eBook formats (PDF, ePub, Kindle, HTML5, Unix man pages) from a single source. While WAFT already has robust PDF generation capabilities, this template offers valuable patterns for multi-format output and structured document organization.

**Key Insight:** WAFT focuses on PDF generation with rich templating, while eBook-Template focuses on multi-format output from a single source. These are complementary approaches.

---

## Architecture Comparison

### eBook-Template Architecture

```
master.adoc (main file)
├── chapters/ (individual chapter files)
├── images/ (PNG images)
├── code/ (code samples)
├── data/ (XML, CSV data)
├── _conf/ (configuration files)
├── _resources/ (styles, templates)
└── Makefile (build orchestration)
```

**Technology Stack:**
- **Asciidoctor** - Document processor (Ruby-based)
- **Asciidoctor-PDF** - PDF backend
- **Asciidoctor-EPUB3** - ePub backend
- **PlantUML** - UML diagram generation
- **Mathematical** - LaTeX math rendering
- **Rouge** - Syntax highlighting

**Build Process:**
```makefile
make all          # Generates all formats
make pdf          # PDF only
make epub         # ePub only
make kindle       # Kindle (.mobi) only
make html         # HTML5 only
make clean        # Clean build artifacts
```

### WAFT Architecture

```
src/waft/templates/
├── field_guide.py
├── academic_paper.py
├── lab_notes.py
├── personal_memo.py
└── tm_report.py

src/waft/document_builder.py (unified API)
src/waft/foundation_v2.py (FPDF2 alternative)
```

**Technology Stack:**
- **WeasyPrint** - HTML to PDF conversion (primary)
- **FPDF2** - Pure Python PDF generation (alternative)
- **Jinja2** - Template engine
- **Markdown** - Content format (via markdown library)

**Build Process:**
```python
from waft import DocumentBuilder

# Template-based (production)
DocumentBuilder.field_guide(
    title="Guide",
    content=markdown_content
).generate()

# Foundation-based (experimental)
from waft.foundation_v2 import DocumentEngine
engine = DocumentEngine()
# ... block-based API
```

---

## Feature Comparison

| Feature | eBook-Template | WAFT |
|--------|----------------|------|
| **PDF Generation** | ✅ Asciidoctor-PDF | ✅ WeasyPrint (primary), FPDF2 (alt) |
| **ePub Generation** | ✅ Native support | ❌ Not supported |
| **Kindle (.mobi)** | ✅ Native support | ❌ Not supported |
| **HTML5 Output** | ✅ Self-contained HTML | ✅ Via WeasyPrint |
| **Multi-file Support** | ✅ Asciidoctor includes | ✅ Via DocumentBuilder |
| **Syntax Highlighting** | ✅ Rouge (Swift, Kotlin, etc.) | ✅ Via markdown extensions |
| **UML Diagrams** | ✅ PlantUML integration | ❌ Not supported |
| **Math Rendering** | ✅ LaTeX via Mathematical | ❌ Not supported |
| **Template System** | ⚠️ Asciidoctor attributes | ✅ Jinja2 templates |
| **Version Control** | ✅ Plain text (AsciiDoc) | ✅ Markdown/HTML |
| **Build System** | ✅ Makefile | ✅ Python scripts |
| **Template Library** | ❌ Single template | ✅ Multiple templates (5+) |
| **Template Registry** | ❌ Not applicable | ✅ TemplateRegistry system |

---

## Strengths & Weaknesses

### eBook-Template Strengths

1. **Multi-Format Output** ⭐
   - Single source generates PDF, ePub, Kindle, HTML
   - Consistent styling across formats
   - Industry-standard formats for eBook distribution

2. **Structured Organization**
   - Clear separation: chapters/, images/, code/, data/
   - Master file with includes
   - Version-control friendly (plain text)

3. **Rich Features**
   - PlantUML for diagrams
   - Mathematical for LaTeX equations
   - Syntax highlighting for many languages
   - Cross-references and TOC generation

4. **Mature Toolchain**
   - Asciidoctor is well-established
   - Good documentation
   - Active community

### eBook-Template Weaknesses

1. **Ruby Dependencies**
   - Requires Ruby, gems, system libraries
   - Complex installation (especially on macOS)
   - Docker option available but adds complexity

2. **Limited Template Variety**
   - Single template structure
   - Customization via Asciidoctor attributes
   - Less flexible than Jinja2 templates

3. **Archived Project**
   - No longer maintained (archived May 2025)
   - May have compatibility issues with newer tools

4. **Python Integration**
   - Not Python-native
   - Would require subprocess calls
   - Less seamless than WAFT's Python-first approach

### WAFT Strengths

1. **Python-Native** ⭐
   - Pure Python workflow
   - Easy integration with existing code
   - No external dependencies (except WeasyPrint system libs)

2. **Template Library System**
   - Multiple templates (field guide, academic, lab notes, etc.)
   - TemplateRegistry for discovery
   - Easy to add new templates

3. **Flexible Templating**
   - Jinja2 provides powerful templating
   - CSS-based styling
   - Easy customization

4. **Active Development**
   - Currently maintained
   - Evolving template system
   - PDF recreation capabilities

### WAFT Weaknesses

1. **Single Format Focus**
   - PDF only (no ePub, Kindle)
   - Would need separate tooling for eBook formats

2. **No Diagram Support**
   - No PlantUML integration
   - Would need external diagram generation

3. **No Math Rendering**
   - No LaTeX equation support
   - Limited for academic/scientific documents

4. **Markdown Limitations**
   - Less structured than AsciiDoc
   - No native include mechanism (though can be added)

---

## Potential Integration Points

### 1. Multi-Format Output for WAFT

**Opportunity:** Add ePub/Kindle generation to WAFT

**Approach:**
- Use Asciidoctor as a backend for multi-format output
- Keep WeasyPrint for PDF (current system)
- Add `DocumentBuilder.epub()` and `DocumentBuilder.kindle()` methods
- Convert WAFT templates to AsciiDoc format when needed

**Implementation:**
```python
# Future API
DocumentBuilder.field_guide(
    title="Guide",
    content=markdown_content
).generate(format="pdf")    # Current
).generate(format="epub")   # New
).generate(format="kindle") # New
).generate(format="all")    # New - all formats
```

**Challenges:**
- Requires Ruby/Asciidoctor installation
- Template conversion (Jinja2 → AsciiDoc)
- Maintaining two template systems

### 2. Structured Document Organization

**Opportunity:** Adopt eBook-Template's folder structure

**Approach:**
- Organize WAFT documents with chapters/, images/, code/ folders
- Use master file pattern for long documents
- Support include mechanism in DocumentBuilder

**Implementation:**
```python
# Future API
DocumentBuilder.from_structure(
    master_file="master.md",
    chapters_dir="chapters/",
    images_dir="images/",
    code_dir="code/"
).generate()
```

### 3. Diagram and Math Support

**Opportunity:** Add PlantUML and LaTeX math to WAFT

**Approach:**
- Integrate PlantUML for UML diagrams
- Add LaTeX math rendering (via Mathematical or similar)
- Support in templates via special blocks

**Implementation:**
```python
# Future template support
content = """
# Chapter 1

[plantuml]
----
class User {
  +name: String
  +email: String
}
----

[math]
----
E = mc^2
----
"""
```

### 4. Build System Pattern

**Opportunity:** Add Makefile-based build for WAFT documents

**Approach:**
- Create Makefile templates for common WAFT workflows
- Support batch generation of multiple documents
- Clean build artifacts

**Implementation:**
```makefile
# Future WAFT Makefile
all: pdf html

pdf:
	python -m waft.cli generate --template field_guide --format pdf

html:
	python -m waft.cli generate --template field_guide --format html

clean:
	rm -rf _build/
```

---

## Recommendations

### Short-Term (Keep Current Approach)

1. **Continue with WeasyPrint + Jinja2**
   - Production-ready and working
   - Python-native
   - Flexible templating

2. **Enhance Template Library**
   - Add more templates
   - Improve TemplateRegistry
   - Better template discovery

3. **Document Best Practices**
   - Multi-file document organization
   - Image/code asset management
   - Template customization guide

### Medium-Term (Consider Integration)

1. **Add Multi-Format Support**
   - Evaluate Asciidoctor for ePub/Kindle
   - Or use alternative Python libraries (ebooklib, etc.)
   - Keep PDF generation with WeasyPrint

2. **Structured Document Support**
   - Add include mechanism to DocumentBuilder
   - Support master file pattern
   - Organize assets in folders

3. **Diagram Support**
   - Integrate PlantUML (Python library available)
   - Add diagram blocks to templates
   - Support in markdown processing

### Long-Term (Full Integration)

1. **Hybrid Approach**
   - Use WAFT templates for PDF (current)
   - Use Asciidoctor for multi-format eBooks
   - Shared content source (Markdown → AsciiDoc conversion)

2. **Unified Build System**
   - Makefile for batch operations
   - Python CLI for programmatic use
   - Docker support for consistent builds

3. **Complete Feature Parity**
   - Math rendering
   - Diagram generation
   - Multi-format output
   - Structured organization

---

## Conclusion

The **eBook-Template** repository offers valuable patterns for multi-format document generation and structured organization. However, WAFT's current Python-native approach with WeasyPrint and Jinja2 templates is well-suited for its primary use case (PDF generation).

**Key Takeaways:**
1. **Different Focus:** eBook-Template = multi-format eBooks, WAFT = rich PDF templates
2. **Complementary:** Could integrate Asciidoctor for ePub/Kindle while keeping WeasyPrint for PDF
3. **Patterns to Adopt:** Structured folder organization, master file pattern, build system
4. **Features to Consider:** PlantUML diagrams, LaTeX math, multi-format output

**Recommendation:** Continue with WAFT's current approach, but consider adding:
- Multi-format output (ePub/Kindle) via Asciidoctor or Python alternatives
- Structured document organization patterns
- Diagram and math support for academic/scientific documents

---

## References

- **eBook-Template Repository:** https://github.com/akosma/eBook-Template
- **Asciidoctor Documentation:** https://asciidoctor.org/
- **WAFT Template System:** `src/waft/templates/`
- **WAFT DocumentBuilder:** `src/waft/document_builder.py`
- **WAFT Template Registry:** `src/waft/templates/registry.py`

---

**Analysis Date:** 2026-01-12  
**Analyst:** AI Assistant (Claude)  
**Work Effort:** WE-260112-q6gl (PDF Template Library System)
