# Foundation V3 Roadmap - Better PDF Generation

> **Note**: This roadmap will be expanded to include the [Unified Genesis Protocol](UNIFIED_GENESIS_PROTOCOL.md) challenge system architecture.

> **Related**: See [LaTeX Alternatives Evaluation](../docs/LATEX_ALTERNATIVES_EVALUATION.md) for evaluation of Typst, ConTeXt, Quarto, and Pandoc as alternatives to LaTeX for template-based PDF generation.

## Current State: Foundation V2 ✅

**Status:** Shipped and tested
**Backend:** fpdf2
**Quality:** Grade A (90%+ code quality)
**Limitations:**
- Manual text positioning
- Basic typography
- No automatic pagination
- Limited table support

---

## The Opportunity: Foundation V3

We can dramatically improve output quality while keeping the same API by switching to a better backend.

### Option 1: ReportLab (Recommended)

**What it gives us:**
```python
# Same API you love
from waft.foundation_v3 import DocumentEngine, DocumentConfig

config = DocumentConfig.clinical_standard()
engine = DocumentEngine(config)
engine.add(CoverPage(...))  # Same blocks
engine.add(MetadataRail(...))  # Same API
engine.render(output_path)  # Same fluent interface
```

**What changes under the hood:**
- ✅ Automatic text flow (no more manual positioning)
- ✅ Professional typography (kerning, leading, tracking)
- ✅ Automatic pagination (smart page breaks)
- ✅ Advanced tables (spanning cells, conditional formatting)
- ✅ Better spacing and layout
- ✅ Production-grade output

**Migration effort:** 2-3 days
**New dependency:** `reportlab` (25 MB, pure Python)

---

### Option 2: WeasyPrint (Template-based)

**Complete paradigm shift to HTML/CSS:**
```python
from waft.foundation_v3 import TemplateEngine

# Define template once (HTML/CSS)
engine = TemplateEngine(template="clinical_standard.html")

# Generate many documents from data
engine.render(
    output="report.pdf",
    data={'subject': subject, 'measurements': data}
)
```

**What it gives us:**
- ✅ Write HTML/CSS, get beautiful PDFs
- ✅ Excellent typography (HarfBuzz text shaping)
- ✅ Familiar syntax (if you know web dev)
- ✅ Preview in browser before PDF
- ✅ Non-programmers can edit templates

**Migration effort:** 1 week (paradigm shift)
**New dependencies:** `weasyprint`, Cairo, Pango (system-level)

---

### Option 3: Hybrid Approach (Both!)

**Keep both APIs:**
```python
# Code-based (for programmers)
from waft.foundation_v3.code import DocumentEngine

engine = DocumentEngine(...)
engine.add(CoverPage(...))
engine.render(...)

# Template-based (for designers/content)
from waft.foundation_v3.templates import TemplateEngine

engine = TemplateEngine(template="clinical.html")
engine.render(data={...})
```

**Best of both worlds:**
- ✅ Programmers: Use block-based API
- ✅ Designers: Use HTML/CSS templates
- ✅ Maximum flexibility

**Migration effort:** 2 weeks
**Dependencies:** Both ReportLab and WeasyPrint

---

## Phased Roadmap

### Phase 1: ✅ DONE (Foundation V2)
- [x] Ship fpdf2-based system
- [x] Block-based API
- [x] Clinical Standard preset
- [x] Comprehensive testing
- [x] Documentation

### Phase 2: 🔄 IN PROGRESS (Evaluation)
- [x] Research alternatives (ReportLab, WeasyPrint, Borb)
- [x] Create comparison document
- [x] Create ReportLab POC
- [ ] Run POC and compare outputs
- [ ] Make decision on backend

### Phase 3: 📅 NEXT (Foundation V3)
**If choosing ReportLab:**
- [ ] Create `foundation_v3_reportlab.py`
- [ ] Port all ContentBlock classes
- [ ] Maintain same API surface
- [ ] Add new features (TOC, charts, cross-refs)
- [ ] Migration guide
- [ ] Deprecate V2 gradually

**If choosing WeasyPrint:**
- [ ] Create `foundation_v3_templates.py`
- [ ] Design HTML/CSS templates
- [ ] Create template engine
- [ ] Migration guide
- [ ] Keep V2 for code-based workflows

**If choosing Hybrid:**
- [ ] Both of the above
- [ ] Unified configuration
- [ ] Shared stylesheet system

### Phase 4: 📅 FUTURE (Advanced Features)
- [ ] Table of contents generation
- [ ] Cross-references
- [ ] Charts and graphs (matplotlib integration)
- [ ] Multi-column layouts
- [ ] Footnotes/endnotes
- [ ] PDF/X compliance (print shop ready)
- [ ] CMYK color support

---

## Decision Matrix

| Criterion | Stay V2 (fpdf2) | V3 (ReportLab) | V3 (WeasyPrint) | V3 (Hybrid) |
|-----------|-----------------|----------------|-----------------|-------------|
| **Effort** | None ✅ | 2-3 days | 1 week | 2 weeks |
| **Quality** | Good | Excellent ⭐ | Excellent ⭐ | Excellent ⭐ |
| **Typography** | Basic | Advanced ⭐ | Excellent ⭐ | Excellent ⭐ |
| **Auto Layout** | Manual | Yes ⭐ | Yes ⭐ | Yes ⭐ |
| **Dependencies** | Minimal ✅ | +1 pkg | +2 pkgs + system | +3 pkgs + system |
| **API Change** | None ✅ | None ✅ | Complete | Dual |
| **Templates** | No | Limited | Yes ⭐ | Yes ⭐ |
| **Learning Curve** | Done ✅ | Low | Medium | Medium |

---

## Recommendation

### Immediate (This Week)
**Test the POC:**
```bash
pip install reportlab
python experiments/reportlab_poc.py
open _work_efforts/REPORTLAB_POC_CLINICAL.pdf
```

Compare side-by-side:
- Foundation V2 output (fpdf2)
- Foundation V3 POC (ReportLab)

Evaluate:
- Typography quality
- Table rendering
- Page breaks
- Overall professional appearance

### Short-term (Next Sprint)
**If POC looks good → Build Foundation V3 with ReportLab**

Maintain API compatibility:
```python
# V2 code (current)
from waft.foundation_v2 import DocumentEngine

# V3 code (same API, better output)
from waft.foundation_v3 import DocumentEngine
# Everything else stays the same!
```

### Long-term (Future)
**Add template support for scaling**

When generating hundreds of reports:
```python
# Template-based workflow
engine = TemplateEngine("clinical_standard.html")

for subject in subjects:
    engine.render(
        output=f"report_{subject.id}.pdf",
        data=subject.get_data()
    )
```

---

## Code Example: V2 → V3 Migration

### Before (Foundation V2 - fpdf2)
```python
from waft.foundation_v2 import DocumentEngine, DocumentConfig, CoverPage

config = DocumentConfig.clinical_standard()
engine = DocumentEngine(config)
engine.add(CoverPage(...))
engine.add(SectionHeader("Title", level=1))
engine.add(TextBlock("Content..."))
engine.render(Path("output.pdf"))
```

### After (Foundation V3 - ReportLab)
```python
from waft.foundation_v3 import DocumentEngine, DocumentConfig, CoverPage
# Same import, different backend

config = DocumentConfig.clinical_standard()
engine = DocumentEngine(config)
engine.add(CoverPage(...))  # Same blocks
engine.add(SectionHeader("Title", level=1))  # Same API
engine.add(TextBlock("Content..."))  # Same interface
engine.render(Path("output.pdf"))  # Same method

# BUT: Better typography, auto layout, professional output!
```

**Migration:** Just change the import path. Everything else stays the same.

---

## Success Metrics

Foundation V3 should deliver:
- ✅ **Same API** - No breaking changes for users
- ✅ **Better output** - Professional typography and layout
- ✅ **Automatic features** - Text flow, pagination, spacing
- ✅ **More features** - TOC, charts, cross-refs
- ✅ **Same quality** - Maintain Grade A code quality
- ✅ **Good docs** - Migration guide and examples

---

## Files Created

1. **docs/PDF_LIBRARY_COMPARISON.md** - Comprehensive analysis
2. **experiments/reportlab_poc.py** - Working proof of concept
3. **docs/FOUNDATION_V3_ROADMAP.md** - This document

---

## Next Actions

1. **Install and test POC:**
   ```bash
   pip install reportlab
   python experiments/reportlab_poc.py
   ```

2. **Compare outputs:**
   - Visual quality
   - Typography
   - Professional appearance

3. **Make decision:**
   - Stick with V2 (fpdf2)?
   - Migrate to V3 (ReportLab)?
   - Go template-based (WeasyPrint)?

4. **Build V3** (if approved)

---

**Foundation V2 is great. Foundation V3 could be exceptional.**

*The infrastructure is ready. The API is proven. Now we can swap in a better engine.*
