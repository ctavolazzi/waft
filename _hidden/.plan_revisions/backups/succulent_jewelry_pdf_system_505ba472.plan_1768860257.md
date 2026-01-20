# Succulent Jewelry PDF Generation System

## Project Overview

Create a streamlined system for generating PDF guides that complement your succulent jewelry casting videos. The system will produce professional, topic-flexible PDFs ready for Gumroad sales, supporting your relaxed creative workflow.

## Project Structure

Create a new directory: `succulent_jewelry_pdfs/`

```
succulent_jewelry_pdfs/
├── templates/              # PDF templates
│   ├── guide_template.py   # Flexible guide template (based on field_guide)
│   └── poetry_template.py  # Spoken word/video essay template
├── content/                # Source content (markdown/HTML)
│   ├── guides/            # Guide content files
│   └── poetry/            # Poetry/video essay content
├── generated/             # Output PDFs (ready for Gumroad)
│   ├── guides/
│   └── poetry/
├── scripts/               # Automation scripts
│   ├── generate_guide.py  # Generate single guide from content
│   ├── batch_generate.py  # Generate multiple guides
│   └── gumroad_prep.py    # Prepare PDFs for Gumroad upload
├── config/                # Configuration files
│   ├── guide_config.json  # Default guide settings
│   └── gumroad_metadata.json  # Gumroad product metadata template
└── README.md              # Usage instructions
```

## Implementation Steps

### 1. Create Flexible Guide Template

**File:** `succulent_jewelry_pdfs/templates/guide_template.py`

- Adapt the existing `field_guide` template from `src/waft/templates/field_guide.py`
- Make it flexible for various topics (jewelry casting, succulent care, music-themed guides, etc.)
- Include customizable sections:
  - Cover page with topic-specific imagery placeholders
  - Introduction section
  - Step-by-step procedures
  - Tips and warnings
  - Resources/references
  - Back cover with Gumroad link placeholder

**Key Features:**
- Clean, readable design suitable for how-to guides
- Support for images (succulent photos, jewelry examples)
- Flexible content structure (not locked to specific topic)
- Professional appearance for paid products

### 2. Create Poetry/Video Essay Template

**File:** `succulent_jewelry_pdfs/templates/poetry_template.py`

- More ornate, artistic design for spoken word performances
- Support for:
  - Poem formatting (stanzas, line breaks)
  - Video essay transcripts
  - Visual elements (backgrounds, borders)
  - Performance notes

### 3. Build Guide Generation Script

**File:** `succulent_jewelry_pdfs/scripts/generate_guide.py`

**Functionality:**
- Accept markdown or HTML content file
- Accept metadata (title, topic, sponsor info, etc.)
- Generate PDF using guide template
- Apply topic-specific styling
- Output to `generated/guides/` with proper naming

**Usage:**
```bash
python scripts/generate_guide.py \
  --content content/guides/jewelry_casting_basics.md \
  --title "Vacuum Casting Basics" \
  --topic "jewelry" \
  --output generated/guides/
```

### 4. Create Batch Generation Script

**File:** `succulent_jewelry_pdfs/scripts/batch_generate.py`

- Process multiple content files at once
- Read from a manifest file (CSV or JSON) with guide metadata
- Generate all PDFs in one run
- Useful for preparing multiple guides for a video series

### 5. Gumroad Preparation Script

**File:** `succulent_jewelry_pdfs/scripts/gumroad_prep.py`

**Functionality:**
- Generate Gumroad-ready metadata for each PDF
- Create product descriptions
- Set pricing suggestions
- Generate cover images (if needed)
- Create upload checklist/manifest

**Output:**
- `gumroad_products.json` - All product metadata in one file
- Individual product description files
- Upload checklist

### 6. Configuration Files

**File:** `succulent_jewelry_pdfs/config/guide_config.json`

Default settings for guides:
```json
{
  "series": "SUCCULENT JEWELRY GUIDE",
  "default_style": "field_guide",
  "printer_friendly": false,
  "include_gumroad_link": true,
  "author": "Your Name",
  "default_topics": ["jewelry", "succulents", "music", "casting"]
}
```

**File:** `succulent_jewelry_pdfs/config/gumroad_metadata.json`

Template for Gumroad product info:
```json
{
  "title_template": "{title} - Succulent Jewelry Guide",
  "description_template": "A helpful guide about {topic}...",
  "tags": ["jewelry", "succulents", "how-to"],
  "pricing_tiers": {
    "basic": 5.00,
    "premium": 10.00
  }
}
```

### 7. Example Content Templates

**File:** `succulent_jewelry_pdfs/content/guides/template.md`

Markdown template showing structure:
- Title
- Introduction
- Sections with headers
- Step-by-step instructions
- Tips/warnings
- Resources

### 8. Integration with WAFT System

**Leverage existing WAFT PDF system:**
- Use `PDF.from_template()` from `src/waft/pdf.py`
- Register new templates in template registry
- Reuse existing styling and formatting systems

**File:** `succulent_jewelry_pdfs/scripts/generate_guide.py` will import:
```python
from src.waft import PDF
from src.waft.templates.guide_template import generate_guide
```

## Workflow Integration

### Typical Workflow:

1. **Create Content** (markdown file in `content/guides/`)
2. **Generate PDF** (`python scripts/generate_guide.py --content ...`)
3. **Review PDF** (check `generated/guides/`)
4. **Prepare for Gumroad** (`python scripts/gumroad_prep.py`)
5. **Upload to Gumroad** (manual upload using generated metadata)

### For Video Series:

1. Create content for each video's guide
2. Use `batch_generate.py` to create all PDFs at once
3. Use `gumroad_prep.py` to prepare all products
4. Upload to Gumroad in batch

## Design Considerations

### Guide Template Design:
- **Clean and readable** - Easy to follow instructions
- **Visual-friendly** - Space for photos of succulents, jewelry pieces
- **Professional** - Looks worth paying for
- **Branded** - Subtle branding that doesn't overwhelm content
- **Print-friendly option** - Can generate printer-friendly versions

### Topic Flexibility:
- Template adapts to different topics automatically
- Music-themed guides can have different styling
- Jewelry casting guides emphasize step-by-step procedures
- Succulent care guides can include care charts/tables

## Files to Create

1. `succulent_jewelry_pdfs/templates/guide_template.py` - Main guide template
2. `succulent_jewelry_pdfs/templates/poetry_template.py` - Poetry template
3. `succulent_jewelry_pdfs/scripts/generate_guide.py` - Single guide generator
4. `succulent_jewelry_pdfs/scripts/batch_generate.py` - Batch generator
5. `succulent_jewelry_pdfs/scripts/gumroad_prep.py` - Gumroad preparation
6. `succulent_jewelry_pdfs/config/guide_config.json` - Configuration
7. `succulent_jewelry_pdfs/config/gumroad_metadata.json` - Gumroad template
8. `succulent_jewelry_pdfs/content/guides/template.md` - Content template
9. `succulent_jewelry_pdfs/README.md` - Usage documentation

## Next Steps After Implementation

1. Create first guide content (e.g., "Vacuum Casting Basics")
2. Generate test PDF
3. Refine template based on first output
4. Create content for video series
5. Generate all PDFs
6. Upload to Gumroad

## Technical Notes

- Uses existing WAFT PDF generation system (no new dependencies)
- Templates based on proven `field_guide` template
- Markdown → HTML → PDF pipeline
- Supports images, tables, lists, code blocks
- Outputs print-ready PDFs suitable for digital distribution