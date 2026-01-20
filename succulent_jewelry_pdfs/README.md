# Succulent Jewelry PDF Generation System

A streamlined system for generating professional PDF guides that complement your succulent jewelry casting videos. Create topic-flexible PDFs ready for Gumroad sales.

## Features

- **Flexible Templates**: Guide template for how-to guides, poetry template for spoken word/video essays
- **Security First**: Path validation, input sanitization, and comprehensive error handling
- **Quality Validation**: Automatic PDF quality checks and validation
- **Batch Processing**: Generate multiple PDFs from a manifest file
- **Gumroad Ready**: Automatic metadata generation for Gumroad uploads

## Quick Start

### 1. Install Dependencies

```bash
pip install weasyprint markdown bleach PyPDF2
```

**System Dependencies** (for WeasyPrint):
- macOS: `brew install cairo pango`
- Ubuntu/Debian: `sudo apt-get install python3-cairo python3-pango`
- See [WeasyPrint docs](https://weasyprint.org/) for other systems

### 2. Create Your First Guide

```bash
# Create content file
cat > content/guides/my_first_guide.md << 'EOF'
# My First Guide

## Introduction
This is my first guide!

## Content
Add your content here...
EOF

# Generate PDF
python scripts/generate_guide.py \
  --content content/guides/my_first_guide.md \
  --title "My First Guide" \
  --topic "jewelry" \
  --output generated/guides/
```

### 3. Prepare for Gumroad

```bash
python scripts/gumroad_prep.py --pdf-dir generated/guides/
```

This generates:
- `gumroad_products.json` - All product metadata
- `gumroad_descriptions/` - Individual description files
- `gumroad_upload_checklist.md` - Upload checklist

## Project Structure

```
succulent_jewelry_pdfs/
├── templates/              # PDF templates
│   ├── guide_template.py   # Guide template
│   └── poetry_template.py  # Poetry/video essay template
├── content/                # Source content
│   ├── guides/            # Guide content files
│   └── poetry/            # Poetry/video essay content
├── generated/             # Output PDFs
│   ├── guides/
│   └── poetry/
├── scripts/               # Automation scripts
│   ├── generate_guide.py  # Single guide generator
│   ├── batch_generate.py  # Batch generator
│   ├── gumroad_prep.py    # Gumroad preparation
│   ├── security.py        # Security utilities
│   ├── validation.py      # PDF validation
│   └── resource_manager.py # Resource management
├── config/                # Configuration
│   ├── guide_config.json  # Guide settings
│   └── gumroad_metadata.json # Gumroad template
└── README.md              # This file
```

## Usage

### Generate Single Guide

```bash
python scripts/generate_guide.py \
  --content content/guides/jewelry_casting_basics.md \
  --title "Vacuum Casting Basics" \
  --topic "jewelry" \
  --subtitle "A Complete Guide" \
  --author "Your Name" \
  --output generated/guides/
```

### Batch Generate Multiple Guides

1. Create a manifest file (`manifest.json`):

```json
{
  "guides": [
    {
      "content": "content/guides/guide1.md",
      "title": "Guide 1",
      "topic": "jewelry"
    },
    {
      "content": "content/guides/guide2.md",
      "title": "Guide 2",
      "topic": "succulents"
    }
  ]
}
```

2. Run batch generation:

```bash
python scripts/batch_generate.py --manifest manifest.json
```

### Prepare for Gumroad

```bash
python scripts/gumroad_prep.py --pdf-dir generated/guides/
```

## Configuration

### Guide Configuration (`config/guide_config.json`)

```json
{
  "series": "SUCCULENT JEWELRY GUIDE",
  "default_style": "field_guide",
  "printer_friendly": false,
  "include_gumroad_link": true,
  "author": "Your Name",
  "default_topics": ["jewelry", "succulents", "music", "casting"],
  "max_content_size_mb": 10,
  "project_root": "."
}
```

### Gumroad Metadata (`config/gumroad_metadata.json`)

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

## Content Template

See `content/guides/template.md` for a complete example of guide structure.

Key features:
- Step-by-step procedures
- Tips and warnings
- Tables
- Images (with placeholder support)
- Resources section

### Adding Images

#### Using Placeholders

In your markdown, use placeholder syntax:
```markdown
![placeholder]
![placeholder:800:600]  # Custom size
![placeholder:picsum:800:600]  # Specific provider
![placeholder:pexels:800:600]  # Pexels (requires API key)
```

Then process with:
```bash
python scripts/add_images.py \
  --content content/guides/my_guide.md \
  --provider picsum \
  --width 800 \
  --height 600
```

#### Using Pexels (Real Photos)

1. Get API key from https://www.pexels.com/api/
2. Set environment variable: `export PEXELS_API_KEY=your_key`
3. Use in content:
```markdown
![placeholder:pexels:800:600]
```
4. Process with query:
```bash
python scripts/add_images.py \
  --content content/guides/my_guide.md \
  --provider pexels \
  --query "succulent" \
  --pexels-api-key $PEXELS_API_KEY
```

#### Direct Image URLs

You can also use direct image URLs in markdown:
```markdown
![Alt text](https://picsum.photos/800/600)
![Succulent](https://example.com/succulent.jpg)
```

## Security Features

- **Path Validation**: All file paths are validated to prevent path traversal attacks
- **Input Sanitization**: HTML content is sanitized to prevent XSS and code execution
- **File Size Limits**: Content files are limited to prevent DoS attacks
- **Error Handling**: Comprehensive error handling with graceful degradation

## Quality Validation

PDFs are automatically validated after generation:
- File size check
- PDF structure verification
- Page count validation
- Checksum generation

## Workflow

1. **Create Content**: Write markdown files in `content/guides/`
2. **Generate PDF**: Use `generate_guide.py` or `batch_generate.py`
3. **Review PDF**: Check `generated/guides/` for output
4. **Prepare for Gumroad**: Run `gumroad_prep.py` to generate metadata
5. **Upload**: Use the generated checklist to upload to Gumroad

## Troubleshooting

### WeasyPrint Import Error

If you get import errors for WeasyPrint, install system dependencies:
- macOS: `brew install cairo pango`
- Ubuntu: `sudo apt-get install python3-cairo python3-pango`

### Permission Errors

Make sure the `generated/` directory is writable:
```bash
chmod -R u+w generated/
```

### PDF Generation Fails

Check the logs for detailed error messages. Common issues:
- Missing dependencies
- Invalid content format
- File size too large
- Path validation errors

## Examples

### Jewelry Casting Guide

```bash
python scripts/generate_guide.py \
  --content content/guides/vacuum_casting.md \
  --title "Vacuum Casting Basics" \
  --topic "jewelry" \
  --subtitle "Complete Guide to Vacuum Casting"
```

### Succulent Care Guide

```bash
python scripts/generate_guide.py \
  --content content/guides/succulent_care.md \
  --title "Succulent Care Guide" \
  --topic "succulents" \
  --subtitle "Keep Your Succulents Thriving"
```

## License

This system is part of your succulent jewelry project. Use as needed.

## Support

For issues or questions, check the error logs and validation output for detailed information.
