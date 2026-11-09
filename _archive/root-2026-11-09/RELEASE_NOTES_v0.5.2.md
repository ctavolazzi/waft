# WAFT v0.5.2 Release Notes

**Release Date**: January 11, 2026  
**Version**: 0.5.2  
**Type**: Minor Release (Feature Addition)

---

## 🎉 What's New

### Evolutionary Iteration Process - PNG Integration

**The biggest change in v0.5.2**: All PDF generators now automatically create PNG screenshots for visual verification, enabling the **evolutionary iteration process** (Generate → Visualize → Inspect → Iterate).

This release establishes visual verification as the standard workflow for all document generation and styling work in WAFT.

---

## ✨ Key Features

### 1. Automatic PNG Conversion

**All PDF generators now create PNG screenshots by default:**

- ✅ `PDFGenerator` - Base generator with PNG support
- ✅ `ScientificPDFGenerator` - Scientific PDFs with PNG screenshots
- ✅ `ComponentPDFGenerator` - Component-based PDFs with PNG screenshots
- ✅ `DocumentEvolutionEngine` - Evolved documents with PNG screenshots

**Usage:**
```python
from src.waft.evolution.pdf_generator import generate_pdf

# PNG conversion happens automatically (default: convert_to_png=True)
pdf_path = generate_pdf(
    content="# My Document\n\nContent...",
    title="My Document",
    style="clinical_standard"
)
# PNG screenshot automatically created at pdf_path.with_suffix('.png')
```

### 2. Robust Fallback Chain

**Three-level fallback ensures PNG conversion always works:**

1. **pdf2image** (Primary) - Best quality, recommended
2. **ImageMagick** (Fallback 1) - Good quality via subprocess
3. **PyMuPDF** (Fallback 2) - Always available, acceptable quality

**Graceful degradation**: If dependencies are missing, the system automatically tries the next backend. PDF generation never fails due to PNG conversion issues.

### 3. Evolutionary Iteration Workflow

**Core process for evidence-based debugging:**

```
Generate PDF → Convert to PNG → Visual Inspection → Identify Issues → Fix → Repeat
```

**Key Principle**: "See Before You Fix" - Visual verification is essential for evidence-based debugging and continuous improvement.

### 4. Work Effort Tooling

**New tools for data generation and experimentation:**

- `tools/generate_test_pdfs.py` - Generate test PDFs with PNGs for comparison
- `tools/status.py` - Quick status check for work efforts

**Enables**:
- Hypothesis-driven development
- Data generation for experimentation
- Before/after comparisons
- Visual verification workflows

---

## 📊 Impact

### For Users

- **Visual Verification**: See actual PDF output before committing changes
- **Evidence-Based Debugging**: Fix based on what you see, not assumptions
- **Iterative Improvement**: Compare before/after visually
- **Workflow Enhancement**: PNG screenshots created automatically

### For Developers

- **Consistent API**: All generators support PNG conversion uniformly
- **Backward Compatible**: Existing code continues to work (PNG conversion is optional)
- **Robust**: Fallback chain ensures reliability
- **Extensible**: Easy to add PNG conversion to new generators

---

## 🔧 Technical Details

### API Changes

**New Parameters** (all generators):
- `convert_to_png: bool = True` - Enable PNG conversion (default: True)
- `png_dpi: int = 300` - DPI for PNG conversion (default: 300)

**Backward Compatibility**: ✅ Maintained
- Existing code without PNG parameters works unchanged
- PNG conversion is opt-out (set `convert_to_png=False` to disable)

### Files Changed

- `src/waft/evolution/pdf_generator.py` - Base generator with PNG support
- `src/waft/evolution/scientific_pdf_generator.py` - Scientific generator updated
- `src/waft/evolution/component_generator.py` - Component generator updated
- `src/waft/evolution/document_evolution_engine.py` - Evolution engine updated
- `pyproject.toml` - Version updated to 0.5.2
- `src/waft/__init__.py` - Version updated to 0.5.2

### Dependencies

**No new dependencies required** - Uses existing:
- `pillow>=10.0.0` (already in dependencies)
- `pypdf>=3.0.0` (already in dependencies)

**Optional dependencies** (for best quality):
- `pdf2image` (recommended)
- `ImageMagick` (system package)

---

## 📚 Documentation

### New Documentation

- `docs/EVOLUTIONARY_ITERATION_PROCESS.md` - Complete guide to the iteration workflow
- `docs/PDF_PNG_CONVERSION.md` - PDF/PNG conversion usage guide
- Work effort documentation in `_work_efforts/WE-260111-dr0f/`

### Updated Documentation

- API documentation updated with PNG conversion parameters
- Usage examples include PNG conversion
- Best practices guide updated

---

## 🐛 Bug Fixes

- **Version Consistency**: Fixed version mismatch between `pyproject.toml` (0.5.1) and `__init__.py` (0.5.2)
  - Both now consistently use 0.5.2

---

## 🔄 Migration Guide

### From v0.5.1

**No migration required** - This is a backward-compatible feature addition.

**If you want to disable PNG conversion:**
```python
# Disable PNG conversion
pdf_path = generate_pdf(
    content=content,
    title=title,
    convert_to_png=False  # Disable automatic PNG conversion
)
```

**If you want custom DPI:**
```python
# Custom DPI
pdf_path = generate_pdf(
    content=content,
    title=title,
    png_dpi=150  # Lower DPI for faster conversion
)
```

---

## 🚀 What's Next

### Planned for v0.5.3

- **Automated Screenshot Comparison Tools** - Side-by-side and diff comparisons
- **Styling Genome Fitness Function** - Visual appeal metrics for evolution
- **Batch Testing with Visual Comparison** - Systematic testing workflows

---

## 📦 Installation

```bash
# Install latest version
uv tool install waft

# Or upgrade existing installation
uv tool upgrade waft
```

---

## 🙏 Acknowledgments

This release establishes the **evolutionary iteration process** as a core WAFT workflow, enabling evidence-based debugging and continuous improvement through visual verification.

**Special thanks** to the WAFT community for feedback and contributions.

---

## 📝 Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete list of changes.

---

**Download**: [GitHub Releases](https://github.com/ctavolazzi/waft/releases/tag/v0.5.2)  
**Documentation**: [docs/](docs/)  
**Issues**: [GitHub Issues](https://github.com/ctavolazzi/waft/issues)
