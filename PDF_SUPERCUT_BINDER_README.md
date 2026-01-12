# PDF Supercut Binder Generator

**Created**: 2026-01-11  
**Purpose**: Generate a comprehensive binder PDF showcasing all WAFT PDF generation capabilities

---

## Overview

The `generate_pdf_supercut_binder.py` script creates a single binder PDF containing samples from every PDF generator in the WAFT system. This provides a complete visual reference of all available capabilities.

---

## What Gets Generated

The binder includes samples from:

### 1. PDFGenerator (3 styles)
- **clinical_standard**: Times New Roman, 1-inch margins, academic style
- **premium**: Minion Pro/Palatino, generous spacing, deep blue accent
- **professional**: Georgia serif, comfortable spacing, professional gray-blue

### 2. ScientificPDFGenerator
- Scientific mode with research tools
- Self-examination features
- Metrics collection demonstration

### 3. ComponentPDFGenerator
- Component-based adaptive generation
- One-pager format demonstration

### 4. LaTeXGenerator
- LaTeX document generation (generates .tex files)

### 5. Template System
- **Field Guide**: Two-column, operational manual style
- **Lab Notes**: Scientific notebook format
- **Technical Memo**: Professional memo format

### 6. Foundation System
- FPDF2-based block generation
- Content-agnostic document engine

### 7. Cover Page
- Premium style cover with binder overview

---

## Usage

### Basic Usage

```bash
# Generate binder with default settings
python3 scripts/generate_pdf_supercut_binder.py
```

This creates `pdf_supercut_binder.pdf` in the current directory.

### Custom Output Path

```bash
# Specify custom output path
python3 scripts/generate_pdf_supercut_binder.py -o my_binder.pdf
```

### Keep Sample PDFs

```bash
# Keep individual sample PDFs after creating binder
python3 scripts/generate_pdf_supercut_binder.py --keep-samples
```

Sample PDFs will be saved in `_temp_pdf_samples/` directory.

### Custom Temp Directory

```bash
# Use custom temp directory for samples
python3 scripts/generate_pdf_supercut_binder.py --temp-dir my_samples/
```

---

## Output Structure

```
pdf_supercut_binder.pdf
├── Cover Page (Premium style)
├── PDFGenerator - Clinical Standard
├── PDFGenerator - Premium
├── PDFGenerator - Professional
├── ScientificPDFGenerator - Standard
├── ComponentPDFGenerator - One-Pager
├── Template - Field Guide
├── Template - Lab Notes
├── Template - Technical Memo
└── Foundation System - FPDF2
```

---

## Requirements

### Python Packages
- `weasyprint` - For PDF generation
- `PyPDF2` - For combining PDFs (optional, falls back to image conversion)
- `fpdf2` - For Foundation system
- Standard WAFT dependencies

### System Dependencies
- WeasyPrint system dependencies (Cairo, Pango)
- LaTeX (optional, for LaTeXGenerator)

---

## How It Works

1. **Generate Samples**: Creates individual PDFs from each generator/style
2. **Create Cover**: Generates a premium-style cover page
3. **Combine PDFs**: Merges all PDFs into a single binder using:
   - PyPDF2 (if available) - Fast, direct PDF merging
   - Image conversion fallback - Converts to PNGs then back to PDF
4. **Cleanup**: Removes temporary files (unless `--keep-samples`)

---

## Error Handling

The script gracefully handles:
- Missing generators (skips with warning)
- Import errors (continues with available generators)
- PDF generation failures (logs error, continues)
- Missing dependencies (uses fallback methods)

---

## Troubleshooting

### "PyPDF2 not available"
- **Solution**: Script automatically falls back to image conversion method
- **Note**: Image conversion is slower but produces same result

### "WeasyPrint not available"
- **Solution**: Install WeasyPrint dependencies:
  ```bash
  # macOS
  brew install cairo pango
  
  # Ubuntu/Debian
  sudo apt-get install python3-cairo python3-pango
  ```

### "Generator not available"
- **Solution**: Some generators may have additional dependencies
- **Note**: Script continues with available generators

### "No PDFs were generated"
- **Check**: Ensure at least one generator is working
- **Verify**: Check error messages for specific issues

---

## Example Output

```
🎬 WAFT PDF Supercut Binder Generator
============================================================
Output: pdf_supercut_binder.pdf
Temp dir: _temp_pdf_samples

📄 Generating PDFGenerator samples...
   - clinical_standard style
   - premium style
   - professional style
📄 Generating ScientificPDFGenerator samples...
   - Scientific mode (standard)
📄 Generating ComponentPDFGenerator samples...
   - One-pager component
📄 Generating LaTeXGenerator samples...
   - LaTeX document (.tex file)
📄 Generating template system samples...
   - Field Guide template
   - Lab Notes template
   - Technical Memo template
📄 Generating Foundation system samples...
   - Foundation document

✅ Generated 8 sample PDFs

📄 Creating cover page...
   ✅ Cover page: 00_cover.pdf

📚 Creating binder PDF from 9 PDFs...
   - Adding: 00_cover.pdf
   - Adding: 01_pdfgenerator_clinical_standard.pdf
   - Adding: 01_pdfgenerator_premium.pdf
   - Adding: 01_pdfgenerator_professional.pdf
   - Adding: 02_scientific_standard.pdf
   - Adding: 03_component_onepager.pdf
   - Adding: 05_template_field_guide.pdf
   - Adding: 06_template_lab_notes.pdf
   - Adding: 07_template_technical_memo.pdf
   - Adding: 08_foundation_document.pdf

✅ Binder PDF created: pdf_supercut_binder.pdf
   - Total pages: 45
   - Source PDFs: 9

🧹 Cleaning up temp directory: _temp_pdf_samples

📖 Opening binder PDF...

✅ Complete! Binder PDF: pdf_supercut_binder.pdf
```

---

## Integration

This script can be integrated into:
- CI/CD pipelines for documentation generation
- Release processes for showcasing features
- Development workflows for testing generators
- Documentation builds for user guides

---

## Related Files

- `PDF_GENERATOR_FILES_INVENTORY.md` - Complete list of all PDF generator files
- `docs/PDF_GENERATOR_API.md` - API documentation
- `WIKI_PDF_Generation_Guide.md` - User guide
- `scripts/pngs_to_pdf_binder.py` - PNG to PDF binder utility

---

## Notes

- LaTeXGenerator creates `.tex` files, not PDFs (requires pdflatex to compile)
- Some generators may require additional setup or configuration
- The binder automatically opens in your default PDF viewer (macOS/Linux/Windows)
- Sample PDFs are numbered for consistent ordering in the binder

---

**Status**: ✅ Ready to use
