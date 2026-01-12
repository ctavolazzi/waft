# PDF Generator API - Composable PDF Generation

## Overview

The `PDFGenerator` class provides a simple, composable API for generating PDFs with minimal boilerplate. It uses WAFT's evolution system (ChatDistiller, StylingGenome, TwoPageGenerator) under the hood.

**Before**: ~600 lines of boilerplate code  
**After**: ~10 lines of code

---

## Quick Start

### Option 1: One-Liner Function

```python
from src.waft.evolution.pdf_generator import generate_pdf

generate_pdf(
    content="# My Document\n\nContent here...",
    title="My Document",
    style="clinical_standard",
    open_pdf=True
)
```

### Option 2: Builder Pattern

```python
from src.waft.evolution.pdf_generator import PDFGenerator

PDFGenerator.from_content(
    content="# My Document\n\nContent here...",
    title="My Document",
    style="clinical_standard"
).save("output.pdf", open_pdf=True)
```

### Option 3: From File

```python
from src.waft.evolution.pdf_generator import generate_pdf_from_file

generate_pdf_from_file(
    "content.md",
    style="premium",
    open_pdf=True
)
```

---

## Available Styles

### `clinical_standard` (Recommended)

- **Body Font**: Times New Roman (11pt) - academic weight
- **Header Font**: Helvetica Bold (16/14/12pt) - professional appearance
- **Margins**: 1 inch (25.4mm) - print-ready
- **Line Spacing**: 1.4x - optimized readability
- **Tone**: Authoritative, institutional

This is WAFT's own Clinical Standard preset from Foundation V2.

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

## Customization

### Override Preset Values

```python
PDFGenerator.from_content(
    content=content,
    title="My Document",
    style="clinical_standard",
    font_size=12,  # Override body font size
    margins=(30, 30, 30, 30),  # Override margins (top, right, bottom, left)
    line_height=1.5  # Override line height
).save("output.pdf")
```

### Add Custom CSS

```python
generator = PDFGenerator.from_content(
    content=content,
    title="My Document",
    style="clinical_standard"
)

generator.with_custom_css("""
<style>
    h1 { color: #0d47a1; }
    .note-box { border-left: 5pt solid #0d47a1; }
</style>
""").save("output.pdf")
```

### Change Style

```python
generator = PDFGenerator.from_content(
    content=content,
    title="My Document",
    style="clinical_standard"
)

# Switch to premium style
generator.with_style("premium").save("output_premium.pdf")
```

---

## Advanced Usage

### Builder Pattern with Chaining

```python
PDFGenerator.from_content(
    content=content,
    title="My Document",
    style="clinical_standard",
    font_size=12
).with_custom_css("""
    <style>
        h1 { border-bottom: 3pt solid #0d47a1; }
    </style>
""").save("output.pdf", open_pdf=True)
```

### Control Page Count

```python
generator = PDFGenerator.from_content(
    content=content,
    title="My Document",
    style="clinical_standard"
)

# Include all ideas (no page limit)
generator.save("output.pdf", include_all_ideas=True)

# Target specific page count
generator.save("output.pdf", target_pages=5)
```

---

## Comparison: Before vs After

### Before (Old Way)

```python
# ~600 lines of boilerplate:
from src.waft.evolution.chat_distiller import ChatDistiller
from src.waft.evolution.two_page_generator import TwoPageGenerator
from src.waft.evolution.styling_genome import (
    StylingGenome, StylingGenomeRegistry, StylingGene,
    FontGene, MarginGene, ColorGene, LayoutGene
)
from weasyprint import HTML

# Get content
content = get_session_content()

# Distill content
distiller = ChatDistiller()
distilled = distiller.distill_text(content, title="My Document")

# Create styling genome
registry = StylingGenomeRegistry(registry_dir=Path("_genetics/session_recaps"))
styling_genes = StylingGene(
    font=FontGene(
        family="'Times New Roman', 'Times', serif",
        size_body=11,
        size_h1=16,
        size_h2=14,
        size_h3=12,
        size_code=9,
        line_height=1.4
    ),
    margin=MarginGene(
        top=25.4, bottom=25.4, left=25.4, right=25.4,
        section_spacing=12, paragraph_spacing=8
    ),
    color=ColorGene(
        text="#000000", background="#FFFFFF", heading="#000000",
        accent="#000000", code_bg="#f5f5f5", code_text="#000000", border="#cccccc"
    ),
    layout=LayoutGene(columns=1, density="normal", toc_enabled=False,
                      page_numbers=True, header_enabled=True, footer_enabled=True),
    name="Clinical Standard"
)
genome = StylingGenome.from_genes(styling_genes)
registry.register(genome)

# Get all ideas
all_ideas = distilled.get_top_ideas(n=1000, min_importance=0.0)
mid_point = len(all_ideas) // 2
page_1_ideas = all_ideas[:mid_point]
page_2_ideas = all_ideas[mid_point:]

# Generate PDF
generator = TwoPageGenerator(weasyprint_available=True)
html_content = generator._render_html(
    distilled_chat=distilled,
    styling_genome=genome,
    page_1_ideas=page_1_ideas,
    page_2_ideas=page_2_ideas,
)

# Inject CSS, save HTML, generate PDF...
# ... many more lines ...
```

### After (New Way)

```python
from src.waft.evolution.pdf_generator import generate_pdf

generate_pdf(
    content=get_session_content(),
    title="My Document",
    style="clinical_standard",
    open_pdf=True
)
```

**That's it!** 10 lines vs 600 lines.

---

## API Reference

### `generate_pdf(content, title, ...)`

Quick function to generate a PDF.

**Parameters:**
- `content` (str): Content (markdown/text)
- `title` (str): Document title
- `output_path` (Path, optional): Output path (auto-generated if None)
- `style` (str): Preset style ("clinical_standard", "premium", "professional")
- `open_pdf` (bool): Open PDF after generation
- `**kwargs`: Additional customization (font_size, margins, line_height, etc.)

**Returns:** Path to generated PDF

### `PDFGenerator.from_content(...)`

Create PDF generator from content string.

**Parameters:**
- `content` (str): Content
- `title` (str): Document title
- `style` (str): Preset style name
- `output_path` (Path, optional): Output path
- `registry_dir` (Path, optional): Styling genome registry directory
- `custom_css` (str, optional): Additional CSS
- `**overrides`: Override preset values

**Returns:** PDFGenerator instance

### `PDFGenerator.from_file(...)`

Create PDF generator from file.

**Parameters:**
- `file_path` (Path): Path to content file
- `title` (str, optional): Title (defaults to filename)
- `style` (str): Preset style name
- `**kwargs`: Additional arguments

**Returns:** PDFGenerator instance

### `generator.save(...)`

Generate and save PDF.

**Parameters:**
- `output_path` (Path, optional): Output path
- `open_pdf` (bool): Open PDF after generation
- `include_all_ideas` (bool): Include all ideas (no page limit)
- `target_pages` (int, optional): Target page count

**Returns:** Path to generated PDF

### `generator.with_custom_css(css)`

Add custom CSS to the generator.

**Returns:** Self (for chaining)

### `generator.with_style(style, **overrides)`

Change style preset.

**Returns:** New PDFGenerator instance

---

## Examples

### Session Recap

```python
from src.waft.evolution.pdf_generator import generate_pdf

generate_pdf(
    content=session_content,
    title="Session Recap: Karma Economy",
    style="clinical_standard",
    open_pdf=True
)
```

### Custom Styling

```python
from src.waft.evolution.pdf_generator import PDFGenerator

PDFGenerator.from_content(
    content=content,
    title="My Document",
    style="clinical_standard",
    font_size=12,
    margins=(30, 30, 30, 30)
).with_custom_css("""
    <style>
        h1 { color: #0d47a1; }
    </style>
""").save("output.pdf", open_pdf=True)
```

### From File

```python
from src.waft.evolution.pdf_generator import generate_pdf_from_file

generate_pdf_from_file(
    "my_content.md",
    style="premium",
    open_pdf=True
)
```

---

## Benefits

✅ **Much less boilerplate** - 10 lines vs 600 lines  
✅ **Preset styles** - clinical_standard, premium, professional  
✅ **Easy customization** - override any preset value  
✅ **Builder pattern** - chain methods for readability  
✅ **File-based generation** - from_file() convenience  
✅ **Automatic idea extraction** - ChatDistiller built-in  
✅ **Styling genome tracking** - automatic evolution tracking  

---

## Integration

The PDFGenerator uses WAFT's evolution system:
- **ChatDistiller**: Extracts structured ideas from content
- **StylingGenome**: Tracks styling evolution
- **TwoPageGenerator**: Generates PDFs with adaptive layout

All styling genomes are automatically registered and tracked for evolution.
