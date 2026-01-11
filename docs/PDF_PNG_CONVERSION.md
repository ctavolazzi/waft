# PDF/PNG Conversion Guide

Complete guide for converting between PDF and PNG formats in the WAFT evolution system.

## Overview

The PDF/PNG conversion system provides bidirectional conversion between PDF documents and PNG images, with support for multiple backends, configurable DPI, and standard page sizes.

## Features

- **PDF → PNG**: Convert PDF pages to individual PNG images
- **PNG → PDF**: Combine PNG images into a PDF binder
- **Multiple Backends**: Automatic fallback chain (pdf2image → ImageMagick → PyMuPDF)
- **Configurable DPI**: Choose resolution or use auto-selection
- **Standard Page Sizes**: Support for Letter, A4, Legal, and custom sizes
- **Automatic Integration**: Optional PNG conversion in one-pager workflow

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

# Use A4 size
pdf_path = pngs_to_pdf(png_list, "output.pdf", page_size=PageSize.A4)

# Custom page size (width, height in inches)
pdf_path = pngs_to_pdf(png_list, "output.pdf", page_size=(10.0, 12.0))

# Scale instead of crop
pdf_path = pngs_to_pdf(png_list, "output.pdf", crop_to_size=False)
```

### Convenience Functions

```python
from src.waft.evolution.pdf_image_converter import (
    convert_pdf_to_images,
    convert_images_to_pdf,
    PageSize,
)

# PDF → PNG
png_paths = convert_pdf_to_images("document.pdf", dpi=300)

# PNG → PDF
pdf_path = convert_images_to_pdf(
    png_list,
    "output.pdf",
    page_size=PageSize.LETTER,
    dpi=300,
)
```

## Page Sizes

### Standard Page Sizes

```python
from src.waft.evolution.pdf_image_converter import PageSize

# Available sizes:
PageSize.LETTER   # 8.5 x 11.0 inches (US Letter)
PageSize.LEGAL    # 8.5 x 14.0 inches (US Legal)
PageSize.A4       # 8.27 x 11.69 inches (ISO A4)
PageSize.A3       # 11.69 x 16.54 inches (ISO A3)
PageSize.TABLOID  # 11.0 x 17.0 inches (US Tabloid)

# Use in conversion
pngs_to_pdf(png_list, "output.pdf", page_size=PageSize.A4)
```

### Custom Page Sizes

```python
# Custom size as (width, height) tuple in inches
pngs_to_pdf(png_list, "output.pdf", page_size=(10.0, 12.0))
```

## DPI Configuration

### Manual DPI Selection

```python
# Standard quality (recommended for most use cases)
png_paths = pdf_to_pngs("document.pdf", dpi=300)

# Fast previews (lower quality, smaller files)
png_paths = pdf_to_pngs("document.pdf", dpi=150)

# High quality (larger files, slower conversion)
png_paths = pdf_to_pngs("document.pdf", dpi=600)
```

### Auto DPI Selection

The system automatically selects DPI based on PDF file size:

- **Small files (< 1MB)**: 150 DPI (fast previews)
- **Medium files (1-10MB)**: 300 DPI (standard quality)
- **Large files (> 10MB)**: 300 DPI (high quality)

```python
# Auto-select DPI
png_paths = pdf_to_pngs("document.pdf", dpi="auto")
```

### DPI Recommendations

| Use Case | Recommended DPI | Notes |
|----------|----------------|-------|
| Web display | 150 | Fast loading, good for previews |
| Standard print | 300 | Default, balanced quality/speed |
| High quality print | 600 | Detailed graphics, slower conversion |
| Screen viewing | 150-300 | Depends on display resolution |

## Integration with One-Pager Workflow

### Automatic PNG Conversion

Enable automatic PNG conversion when generating one-pagers:

```python
from src.waft.evolution import TwoPageGenerator

generator = TwoPageGenerator(weasyprint_available=True)

result = generator.generate(
    distilled_chat=distilled,
    styling_genome=genome,
    output_path="output.pdf",
    convert_to_png=True,  # Enable PNG conversion
    png_dpi=300,          # DPI for PNG conversion
)

# Access PNG paths from result
if result.get("png_paths"):
    print(f"Created {len(result['png_paths'])} PNG images")
```

### Manual Conversion After Generation

```python
from src.waft.evolution.pdf_image_converter import convert_pdf_to_images

# After generating PDF
result = generator.generate(...)
pdf_path = result["pdf_path"]

# Convert to PNGs
png_paths = convert_pdf_to_images(pdf_path, dpi=300)
```

## Image Handling Options

### Crop vs Scale

When converting PNGs to PDF, you can choose how to handle images that don't match the page size:

```python
# Crop to page size (center crop) - default
pngs_to_pdf(png_list, "output.pdf", crop_to_size=True)

# Scale to fit (maintains aspect ratio, adds white borders)
pngs_to_pdf(png_list, "output.pdf", crop_to_size=False)
```

### Image Format Support

- **Input**: PNG, JPEG (for PNG → PDF)
- **Output**: PNG (for PDF → PNG)
- **PDF**: RGB format (non-RGB images are automatically converted)

## Backend Fallback Chain

The system tries backends in this order:

1. **pdf2image** (best quality, recommended)
2. **ImageMagick** (via subprocess, good quality)
3. **PyMuPDF** (fallback, acceptable quality)

If all backends fail, you'll get a helpful error message with installation instructions.

## Round-Trip Conversion

You can convert PDF → PNG → PDF to verify quality:

```python
from src.waft.evolution.pdf_image_converter import (
    pdf_to_pngs,
    pngs_to_pdf,
    PageSize,
)

# PDF → PNG
png_paths = pdf_to_pngs("original.pdf", dpi=300)

# PNG → PDF
round_trip_pdf = pngs_to_pdf(
    png_paths,
    "round_trip.pdf",
    page_size=PageSize.LETTER,
    dpi=300,
)
```

## Troubleshooting

### "No PDF conversion library available"

**Problem**: None of the backends are installed.

**Solution**: Install at least one backend:

```bash
# Option 1: pdf2image (recommended)
pip install pdf2image
brew install poppler  # macOS
# or: sudo apt-get install poppler-utils  # Ubuntu

# Option 2: ImageMagick
brew install imagemagick  # macOS
# or: sudo apt-get install imagemagick  # Ubuntu

# Option 3: PyMuPDF (fallback)
pip install pymupdf
```

### "PDF not found" Error

**Problem**: The PDF file path is incorrect or file doesn't exist.

**Solution**: Check the file path:

```python
from pathlib import Path

pdf_path = Path("document.pdf")
if not pdf_path.exists():
    print(f"File not found: {pdf_path}")
    print(f"Current directory: {Path.cwd()}")
```

### Poor Image Quality

**Problem**: Images look blurry or pixelated.

**Solution**: Increase DPI:

```python
# Use higher DPI
png_paths = pdf_to_pngs("document.pdf", dpi=600)

# Or use auto-selection for optimal quality
png_paths = pdf_to_pngs("document.pdf", dpi="auto")
```

### Conversion is Slow

**Problem**: Large PDFs take a long time to convert.

**Solution**: 
- Use lower DPI for previews (150 instead of 300)
- Use pdf2image backend (usually fastest)
- Consider converting only specific pages

### Images Don't Fit Page Size

**Problem**: PNGs are cropped or scaled incorrectly.

**Solution**: Choose the right handling option:

```python
# Crop to fit (removes edges)
pngs_to_pdf(png_list, "output.pdf", crop_to_size=True)

# Scale to fit (maintains full image, adds borders)
pngs_to_pngs(png_list, "output.pdf", crop_to_size=False)
```

### "No valid images to convert to PDF"

**Problem**: All PNG files are missing or invalid.

**Solution**: Check PNG files exist and are valid:

```python
from pathlib import Path
from PIL import Image

for png_path in png_list:
    if not png_path.exists():
        print(f"Missing: {png_path}")
    else:
        try:
            img = Image.open(png_path)
            print(f"Valid: {png_path} ({img.size})")
        except Exception as e:
            print(f"Invalid: {png_path} - {e}")
```

## Performance Tips

1. **Use appropriate DPI**: 300 DPI is usually sufficient for most use cases
2. **Choose the right backend**: pdf2image is typically fastest and highest quality
3. **Batch processing**: Convert multiple PDFs in parallel if needed
4. **Cache results**: Save PNGs if you'll need them multiple times

## Examples

### Complete Workflow

```python
from pathlib import Path
from src.waft.evolution.pdf_image_converter import (
    pdf_to_pngs,
    pngs_to_pdf,
    PageSize,
)

# 1. Convert PDF to PNGs
pdf_path = Path("document.pdf")
png_paths = pdf_to_pngs(pdf_path, dpi=300)
print(f"Created {len(png_paths)} PNG images")

# 2. Process PNGs (e.g., add annotations, resize, etc.)
# ... your processing code ...

# 3. Convert back to PDF
output_pdf = pngs_to_pdf(
    png_paths,
    "processed_document.pdf",
    page_size=PageSize.LETTER,
    dpi=300,
)
print(f"Created PDF: {output_pdf}")
```

### One-Pager with PNG Conversion

```python
from src.waft.evolution import TwoPageGenerator, ChatDistiller, StylingGenome

# Generate one-pager
distiller = ChatDistiller()
distilled = distiller.distill_text(chat_content, title="My Session")

genome = StylingGenome.from_genes(...)
generator = TwoPageGenerator(weasyprint_available=True)

result = generator.generate(
    distilled_chat=distilled,
    styling_genome=genome,
    output_path="one_pager.pdf",
    convert_to_png=True,  # Enable PNG conversion
    png_dpi=300,
)

print(f"PDF: {result['pdf_path']}")
if result.get("png_paths"):
    print(f"PNGs: {len(result['png_paths'])} images")
```

## API Reference

See `src/waft/evolution/pdf_image_converter.py` for complete API documentation.

## Related Documentation

- [One-Pager Tool Guide](ONE_PAGER_TOOL.md)
- [Evolution System](EVOLUTION_SYSTEM.md)
- [Two-Page Generator](TWO_PAGE_GENERATOR.md)
