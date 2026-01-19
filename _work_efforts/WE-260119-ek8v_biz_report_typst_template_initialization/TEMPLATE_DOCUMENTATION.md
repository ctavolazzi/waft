# Biz Report Template Documentation

**Template**: `@preview/biz-report:0.3.1`  
**Work Effort**: WE-260119-ek8v  
**Date**: 2026-01-19

---

## Overview

The Biz Report template is a professional business report template for Typst, designed for creating polished corporate documents with modern styling, customizable branding, and business-focused features like info boxes, author profiles, and document control tables.

## Installation

```bash
typst init @preview/biz-report:0.3.1
```

This creates a new directory with `example.typ` as the entry point and example assets.

## Template Structure

```
biz-report/
├── example.typ        # Main template file with examples
├── author.png         # Example author image
├── mylogo.svg         # Example logo
└── techimage.svg      # Example feature image
```

## Core Features

### 1. Report Configuration

The main report wrapper with branding and metadata:

```typst
#import "@preview/biz-report:0.3.1": report

#show: report.with(
  title: "Business Report",
  publishdate: "November 2025",
  mylogo: image("mylogo.svg", width: 25%),
  myfeatureimage: image("techimage.svg", height: 6cm),
  myvalues: "VALUE1 | VALUE2 | VALUE3 | VALUE4",
  mycolor: rgb("#1300a7"),
  myfont: "IBM Plex Sans"
)
```

**Configuration Options:**
- `title`: Report title
- `publishdate`: Publication date
- `mylogo`: Company/organization logo (image)
- `myfeatureimage`: Hero/feature image for cover
- `myvalues`: Core values displayed as pipe-separated list
- `mycolor`: Primary brand color (RGB hex)
- `myfont`: Font family name

### 2. Drop Cap Paragraphs

Elegant first-line styling with drop caps:

```typst
#import "@preview/biz-report:0.3.1": dropcappara

#dropcappara(firstline: "Welcome to this report.")[
  Your paragraph content here...
]
```

### 3. Author Wrap

Author profile section with image and caption:

```typst
#import "@preview/biz-report:0.3.1": authorwrap

#authorwrap(
  authorimage: image("author.png", height: 3cm), 
  authorcaption: "The Author, CXO"
)[
  Author bio or content here...
]
```

### 4. Info Boxes

Highlighted information boxes with icons:

```typst
#import "@preview/biz-report:0.3.1": infobox

# Simple info box
#infobox(icon: "warning")[
  Swimming when there is a thunderstorm is dangerous.
]

# Info box with formatted content
#infobox(icon: "laptop")[
  *List of problems:*
  
  - Problem 1.
  - Problem 2.
  - Problem 3.
]
```

**Available Icons:**
- `warning` - Warning/alert
- `laptop` - Technology/computing
- `app-store` - Applications/software
- `shield-virus` - Security/protection
- `database` - Data/storage
- (and more Typst icon options)

### 5. Tables

Professional table formatting with headers:

```typst
#align(center)[
  #table(
    columns: (auto, auto, auto, auto),
    table.header(
      [Version], [Date], [Authors], [Changes]
    ),
    "0.2",
    "November 2025",
    "Reviewers",
    "Formal review",
    "0.1",
    "October 2025",
    "Authors",
    "Initial draft",
  )
]
```

### 6. Document Control Table

Built-in version history table:

```typst
=== Document Control

#align(center)[
  #table(
    columns: (auto, auto, auto, auto),
    table.header(
      [Version], [Date], [Authors], [Changes]
    ),
    // Add version entries...
  )
]
```

### 7. Figures

Image figures with captions:

```typst
#figure(
  image("techimage.svg", width: 50%),
  caption: ["Technology Image"],
)
```

### 8. Multi-Level Headings

Support for chapters and sub-headings:

```typst
= Main Chapter Title

== Sub-heading

=== Sub-sub-heading
```

## Usage Example

```typst
#import "@preview/biz-report:0.3.1": authorwrap, dropcappara, infobox, report

#show: report.with(
  title: "Q4 Business Report",
  publishdate: "January 2026",
  mylogo: image("logo.svg", width: 25%),
  myfeatureimage: image("hero.png", height: 6cm),
  myvalues: "Innovation | Quality | Integrity | Growth",
  mycolor: rgb("#0066cc"),
  myfont: "Inter"
)

= Executive Summary

#dropcappara(firstline: "This quarter showed significant growth.")[
  Detailed summary content here...
]

#authorwrap(
  authorimage: image("ceo.jpg", height: 3cm),
  authorcaption: "Jane Smith, CEO"
)[
  CEO message and insights...
]

= Key Findings

#infobox(icon: "warning")[
  *Important Notice:*
  
  Market conditions have changed significantly this quarter.
]

#infobox(icon: "laptop")[
  *Technology Updates:*
  
  - New platform launched
  - Infrastructure upgraded
  - Security enhancements completed
]

=== Financial Performance

#figure(
  image("chart.png", width: 80%),
  caption: ["Q4 Financial Performance"],
)

=== Document Control

#align(center)[
  #table(
    columns: (auto, auto, auto, auto),
    table.header(
      [Version], [Date], [Authors], [Changes]
    ),
    "1.0",
    "January 2026",
    "Finance Team",
    "Initial release",
  )
]
```

## Compilation

```bash
# Watch mode (auto-recompile on changes)
cd biz-report
typst watch example.typ

# Single compilation
typst compile example.typ output.pdf
```

## Integration with WAFT

### Potential Use Cases

1. **Business Reports**: Generate quarterly/annual business reports
2. **Executive Summaries**: Create executive-level document summaries
3. **Project Reports**: Document project progress and outcomes
4. **Client Presentations**: Professional client-facing documents
5. **Internal Documentation**: Corporate internal reports

### Integration Points

- **Template Registry**: Add to WAFT's Typst template registry
- **Document Generator**: Create wrapper class for business reports
- **Branding System**: Integrate with WAFT's branding/logo system
- **Metadata Mapping**: Map WAFT document metadata to biz-report parameters
- **Info Box System**: Create structured info box content from WAFT data

### Example WAFT Integration

```python
from waft.templates.typst import BizReportTemplate

template = BizReportTemplate(
    title="Q4 Business Report",
    publish_date="January 2026",
    logo_path="assets/logo.svg",
    brand_color="#0066cc",
    values=["Innovation", "Quality", "Integrity"],
)

template.add_chapter("Executive Summary", content="...")
template.add_info_box(icon="warning", content="Important notice...")
template.add_author_profile(
    image="ceo.jpg",
    caption="Jane Smith, CEO",
    bio="..."
)
pdf = template.compile()
```

## Configuration Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | String | Required | Report title |
| `publishdate` | String | Required | Publication date |
| `mylogo` | Image | Optional | Company logo |
| `myfeatureimage` | Image | Optional | Hero/feature image |
| `myvalues` | String | Optional | Pipe-separated values |
| `mycolor` | Color | Optional | Primary brand color (RGB hex) |
| `myfont` | String | Optional | Font family name |

## Component Reference

### `report`
Main report wrapper with branding configuration.

### `dropcappara`
Drop cap paragraph with elegant first-line styling.
- Parameter: `firstline` - First line text for drop cap

### `authorwrap`
Author profile section with image and caption.
- Parameter: `authorimage` - Author photo (image)
- Parameter: `authorcaption` - Author title/description

### `infobox`
Highlighted information box with icon.
- Parameter: `icon` - Icon name (warning, laptop, app-store, shield-virus, database, etc.)

## Resources

- **Template Package**: `@preview/biz-report:0.3.1`
- **Typst Documentation**: https://typst.app/docs/
- **Work Effort**: [WE-260119-ek8v](../WE-260119-ek8v_biz_report_typst_template_initialization/WE-260119-ek8v_index.md)

## Notes

- Template size: 219.1 KiB
- Includes example assets (author.png, mylogo.svg, techimage.svg)
- Business-focused design with modern styling
- Excellent for corporate and professional documents
- Customizable branding for different organizations
- Version 0.3.1 (may have updates available)

## Tips

1. **Branding**: Replace example assets with your own logo and images
2. **Colors**: Use your brand colors for `mycolor` parameter
3. **Icons**: Choose appropriate icons for info boxes based on content type
4. **Document Control**: Keep version history updated in the document control table
5. **Author Profiles**: Use high-quality author images for professional appearance
