# PDF/PNG Conversion

**Complete guide for converting between PDF and PNG formats in WAFT.**

---

## Overview

The PDF/PNG conversion system provides bidirectional conversion between PDF documents and PNG images, with support for multiple backends, configurable DPI, and standard page sizes.

---

## Features

- **PDF → PNG**: Convert PDF pages to individual PNG images
- **PNG → PDF**: Combine PNG images into a PDF binder
- **Multiple Backends**: Automatic fallback chain (pdf2image → ImageMagick → PyMuPDF)
- **Configurable DPI**: Choose resolution or use auto-selection
- **Standard Page Sizes**: Support for Letter, A4, Legal, and custom sizes
- **Automatic Integration**: Optional PNG conversion in one-pager workflow

---

## Installation

### Required Dependencies

Install at least one of the following backends:

```bash
# Option 1: pdf2image (recommended - best quality)
pip install pdf2image
# Also requires poppler-utils:
# macOS: brew install poppler
# Ubuntu: sudo apt-get install poppler-utils

# Option 2: ImageMagick
# macOS: brew install imagemagick
# Ubuntu: sudo apt-get install imagemagick

# Option 3: PyMuPDF (fallback)
pip install pymupdf

# Required for PNG → PDF conversion
pip install pillow
```

---

## Basic Usage

### Convert PDF to PNG Images

```python
from pathlib import Path
from src.waft.evolution.pdf_image_converter import pdf_to_pngs

# Basic conversion
png_paths = pdf_to_pngs("document.pdf", dpi=300)
print(f"Created {len(png_paths)} PNG images")

# Custom output directory
png_paths = pdf_to_pngs("document.pdf", output_dir=Path("output/pages"), dpi=300)

# Auto-select DPI based on file size
png_paths = pdf_to_pngs("document.pdf", dpi="auto")
```

### Convert PNG Images to PDF

```python
from pathlib import Path
from src.waft.evolution.pdf_image_converter import pngs_to_pdf, PageSize

# Use standard page size
png_list = [Path("page_1.png"), Path("page_2.png")]
pdf_path = pngs_to_pdf(png_list, "output.pdf", page_size=PageSize.LETTER)
```

---

## Automatic Integration (v0.5.2+)

**All PDF generators automatically create PNG screenshots:**

```python
from src.waft.evolution.pdf_generator import generate_pdf

# PNG conversion happens automatically
pdf_path = generate_pdf(
    content=content,
    title=title,
    style="clinical_standard"
    # convert_to_png=True is default
    # png_dpi=300 is default
)
# PNG screenshot saved at pdf_path.with_suffix('.png')
```

---

## DPI Recommendations

| Use Case | Recommended DPI | Notes |
|----------|----------------|-------|
| Web display | 150 | Fast loading, good for previews |
| Standard print | 300 | Default, balanced quality/speed |
| High quality print | 600 | Detailed graphics, slower conversion |
| Screen viewing | 150-300 | Depends on display resolution |

---

## Backend Fallback Chain

The system tries backends in this order:

1. **pdf2image** (best quality, recommended)
2. **ImageMagick** (via subprocess, good quality)
3. **PyMuPDF** (fallback, acceptable quality)

**Graceful degradation**: If one backend fails, the system automatically tries the next. PDF generation never fails due to PNG conversion issues.

---

## Troubleshooting

### "No PDF conversion library available"

**Solution**: Install at least one backend:
```bash
pip install pdf2image  # Recommended
# OR
pip install pymupdf   # Always works
```

### PNG conversion is slow

**Solution**: Use lower DPI for faster conversion:
```python
pdf_to_pngs("document.pdf", dpi=150)  # Faster than 300
```

### PNG files are large

**Solution**: Use lower DPI or compress images:
```python
pdf_to_pngs("document.pdf", dpi=150)  # Smaller files
```

---

## Related Documentation

- **[Evolutionary Iteration Process](Evolutionary-Iteration-Process)** - Visual verification workflow
- **[PDF Generation Guide](PDF-Generation-Guide)** - PDF creation
- **[API Reference](API-Reference)** - Complete API documentation

---

**Convert between PDF and PNG formats with automatic fallback in WAFT.**
