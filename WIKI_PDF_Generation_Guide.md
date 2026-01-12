# PDF Generation Guide

**Complete guide to generating professional PDFs with WAFT.**

---

## Overview

WAFT provides multiple PDF generation systems, each optimized for different use cases:

1. **PDFGenerator** - Simple, composable API (recommended for most users)
2. **ScientificPDFGenerator** - Research tools and self-examination
3. **ComponentPDFGenerator** - Component-based adaptive generation
4. **DocumentEvolutionEngine** - Evolutionary document creation

---

## Quick Start

### Basic PDF Generation

```python
from src.waft.evolution.pdf_generator import generate_pdf

pdf_path = generate_pdf(
    content="# My Document\n\nContent here...",
    title="My Document",
    style="clinical_standard"
)
# PNG screenshot automatically created for visual verification
```

### Using the Builder Pattern

```python
from src.waft.evolution.pdf_generator import PDFGenerator

PDFGenerator.from_content(
    content="# My Document\n\nContent here...",
    title="My Document",
    style="clinical_standard"
).save("output.pdf", open_pdf=True)
```

---

## Available Styles

### `clinical_standard` (Recommended)

- **Body Font**: Times New Roman (11pt) - academic weight
- **Header Font**: Helvetica Bold (16/14/12pt) - professional appearance
- **Margins**: 1 inch (25.4mm) - print-ready
- **Line Spacing**: 1.4x - optimized readability
- **Tone**: Authoritative, institutional

### `premium`

- **Body Font**: Minion Pro/Palatino (13pt) - premium serif
- **Margins**: 40mm - generous, elegant spacing
- **Line Spacing**: 1.75x - luxurious spacing
- **Colors**: Deep blue accent (#0d47a1)
- **Tone**: Premium, sophisticated

### `professional`

- **Body Font**: Georgia (11pt) - professional serif
- **Margins**: 25mm - comfortable spacing
- **Line Spacing**: 1.6x - comfortable reading
- **Colors**: Professional gray-blue accent
- **Tone**: Professional, clean

---

## PNG Conversion (v0.5.2+)

**All generators automatically create PNG screenshots by default:**

```python
# PNG conversion is automatic (default: convert_to_png=True)
pdf_path = generate_pdf(
    content=content,
    title=title,
    convert_to_png=True,  # Default, can be omitted
    png_dpi=300            # Default DPI
)
```

**Disable PNG conversion:**
```python
pdf_path = generate_pdf(
    content=content,
    title=title,
    convert_to_png=False  # Disable PNG conversion
)
```

---

## Advanced Usage

### Custom Styling

```python
generator = PDFGenerator.from_content(
    content=content,
    title=title,
    style="clinical_standard",
    margins=(30, 30, 30, 30),  # Custom margins
    font_size=12                # Custom font size
)
pdf_path = generator.save("output.pdf")
```

### Scientific PDFs

```python
from src.waft.evolution.scientific_pdf_generator import ScientificPDFGenerator

generator = ScientificPDFGenerator.from_content(
    content=content,
    title="Research Document",
    scientific_mode=True
)

# Generate with self-examination
pdf_path = generator.save("research.pdf")
# Analysis saved to research.pdf.analysis.json
```

### Component-Based PDFs

```python
from src.waft.evolution.component_generator import ComponentPDFGenerator

generator = ComponentPDFGenerator()

result = generator.generate_one_pager(
    content=content,
    title="Component Document",
    allowed_pages=2,
    convert_to_png=True  # PNG conversion supported
)
```

---

## Best Practices

1. **Use Visual Verification**: Always check PNG screenshots before committing
2. **Choose Appropriate Style**: Use `clinical_standard` for research, `premium` for presentations
3. **Iterate Based on Visual Evidence**: Use the evolutionary iteration process
4. **Document Your Choices**: Note why you chose specific styles or settings

---

## Troubleshooting

### PNG Conversion Fails

**Solution**: The system automatically falls back to alternative backends. If all fail, PDF generation continues without PNG.

**Check dependencies:**
```bash
# Install recommended backend
pip install pdf2image
# Also requires poppler-utils:
# macOS: brew install poppler
# Ubuntu: sudo apt-get install poppler-utils
```

### PDF Looks Wrong

**Solution**: Use the evolutionary iteration process:
1. Generate PDF → PNG
2. Inspect PNG screenshot
3. Identify issues
4. Fix and regenerate
5. Compare before/after

---

## Related Documentation

- **[Evolutionary Iteration Process](Evolutionary-Iteration-Process)** - Visual verification workflow
- **[PDF/PNG Conversion](PDF-PNG-Conversion)** - Conversion details
- **[API Reference](API-Reference)** - Complete API documentation

---

**Generate professional PDFs with automatic visual verification in WAFT v0.5.2+**
