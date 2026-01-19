# FHICT Document Template Documentation

**Template**: `@preview/unofficial-fhict-document-template:1.2.1`  
**Work Effort**: WE-260119-4nh6  
**Date**: 2026-01-19

---

## Overview

The FHICT (Fontys University of Applied Sciences ICT) document template is a comprehensive Typst template designed for academic and technical documentation. It provides extensive customization options for creating professional documents with proper formatting, citations, and organizational features.

## Installation

```bash
typst init @preview/unofficial-fhict-document-template:1.2.1
```

This creates a new directory with `main.typ` as the entry point.

## Template Structure

```
unofficial-fhict-document-template/
└── main.typ          # Main template file
```

## Core Features

### 1. Document Metadata

```typst
#show: fhict-doc.with(
  title: "Your Document Title",
  subtitle: "Optional Subtitle",
)
```

### 2. Authors and Assessors

```typst
authors-title: "Authors",
authors: (
  (
    name: "John Doe",
  ),
  (
    name: "Jane Smith",
  ),
),

assessors-title: "Assessors",
assessors: (
  (
    title: "Dr.",
    name: "Professor Name",
  ),
),
```

### 3. Multi-Language Support

Supports multiple languages with built-in translations:
- English (`en`)
- Dutch (`nl`)
- German (`de`)
- French (`fr`)
- Spanish (`es`)

```typst
language: "en",
available-languages: ("en", "nl", "de", "fr", "es"),
```

### 4. Version History

Track document versions with detailed change logs:

```typst
version-history: (
  (
    version: "1.0",
    date: "2026-01-19",
    author: "John Doe",
    changes: "Initial release",
  ),
  (
    version: "1.1",
    date: "2026-01-20",
    author: "Jane Smith",
    changes: "Added chapter 2",
  ),
),
```

### 5. Bibliography Support

Supports BibTeX bibliography files with various citation styles:

```typst
bibliography-file: bibliography("my-sources.bib"),
citation-style: "ieee",  // Options: ieee, apa, etc.
```

### 6. Table of Contents

Configurable table of contents with depth control:

```typst
toc-depth: 3,           // How many heading levels to include
disable-toc: false,     // Enable/disable TOC
```

### 7. Additional Tables

Generate tables for figures, listings, and tables:

```typst
table-of-figures: false,
table-of-listings: true,
table-of-tables: true,
```

### 8. Glossary Support

Add glossary terms with optional front placement:

```typst
// First, define terms in a separate file
#import "./terms.typ": term-list

// Then use in template
glossary-terms: term-list,
glossary-front: false,  // Place glossary at front or back
```

### 9. Chapter Formatting

Control chapter behavior:

```typst
chapter-on-new-page: true,           // Start chapters on new pages
disable-chapter-numbering: false,    // Show/hide chapter numbers
```

### 10. Pre-TOC and Appendix

Add content before table of contents or appendices:

```typst
pre-toc: [#include "./pre-toc.typ"],
appendix: [#include "./appendix.typ"],
```

### 11. Visual Options

```typst
watermark: none,              // Add watermark (or none)
line-numbering: false,        // Enable line numbers
print-extra-white-page: false, // Add extra blank page
```

### 12. Multi-Organization Support

Support for secondary organization branding:

```typst
secondary-organisation-color: none,
secondary-organisation-logo: none,
secondary-organisation-logo-height: 6%,
```

### 13. Index Generation

Generate document index:

```typst
enable-index: false,
index-columns: 2,  // Number of columns in index
```

### 14. Censorship Mode

Redact sensitive information:

```typst
censored: 0,  // Number of censored sections
```

## Usage Example

```typst
#import "@preview/unofficial-fhict-document-template:1.2.1": *

#show: fhict-doc.with(
  title: "My Academic Paper",
  subtitle: "A Comprehensive Study",
  
  authors: (
    (name: "John Doe"),
    (name: "Jane Smith"),
  ),
  
  language: "en",
  toc-depth: 3,
  bibliography-file: bibliography("sources.bib"),
  citation-style: "ieee",
)

= Introduction

This is the introduction chapter.

== Background

Background information here.

= Methodology

Methodology details.

= Results

Results and analysis.

= Conclusion

Final conclusions.
```

## Compilation

```bash
# Watch mode (auto-recompile on changes)
typst watch main.typ

# Single compilation
typst compile main.typ output.pdf
```

## Integration with WAFT

### Potential Use Cases

1. **Academic Reports**: Generate academic-style reports for research findings
2. **Technical Documentation**: Create comprehensive technical documentation
3. **Thesis/Dissertation**: Support for long-form academic documents
4. **Multi-language Documents**: Generate documents in multiple languages

### Integration Points

- **Template Registry**: Add to WAFT's Typst template registry
- **Document Generator**: Create wrapper class similar to existing LaTeX wrappers
- **Metadata Mapping**: Map WAFT document metadata to FHICT template parameters
- **Bibliography Integration**: Connect with WAFT's citation management

### Example WAFT Integration

```python
from waft.templates.typst import FHICTTemplate

template = FHICTTemplate(
    title="Research Report",
    authors=["John Doe", "Jane Smith"],
    language="en",
    toc_depth=3,
)

template.add_chapter("Introduction", content="...")
template.add_bibliography("sources.bib")
pdf = template.compile()
```

## Configuration Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | String | Required | Document title |
| `subtitle` | String | Optional | Document subtitle |
| `authors-title` | String | "Authors" | Label for authors section |
| `authors` | Array | [] | List of author objects |
| `assessors-title` | String | "Assessors" | Label for assessors section |
| `assessors` | Array | [] | List of assessor objects |
| `language` | String | "en" | Document language |
| `available-languages` | Array | All | Available language options |
| `version-history` | Array | [] | Version tracking entries |
| `chapter-on-new-page` | Boolean | true | Start chapters on new pages |
| `bibliography-file` | Bibliography | None | BibTeX bibliography file |
| `citation-style` | String | "ieee" | Citation style |
| `table-of-figures` | Boolean | false | Generate figure list |
| `table-of-listings` | Boolean | false | Generate listing list |
| `table-of-tables` | Boolean | false | Generate table list |
| `glossary-terms` | Array | [] | Glossary term definitions |
| `glossary-front` | Boolean | false | Place glossary at front |
| `toc-depth` | Integer | 3 | Table of contents depth |
| `disable-toc` | Boolean | false | Disable table of contents |
| `disable-chapter-numbering` | Boolean | false | Hide chapter numbers |
| `watermark` | Watermark/None | none | Document watermark |
| `line-numbering` | Boolean | false | Enable line numbers |
| `censored` | Integer | 0 | Number of censored sections |
| `print-extra-white-page` | Boolean | false | Add extra blank page |
| `secondary-organisation-color` | Color/None | none | Secondary org color |
| `secondary-organisation-logo` | Image/None | none | Secondary org logo |
| `secondary-organisation-logo-height` | Percentage | 6% | Logo height |
| `enable-index` | Boolean | false | Generate document index |
| `index-columns` | Integer | 2 | Index column count |

## Resources

- **Template Package**: `@preview/unofficial-fhict-document-template:1.2.1`
- **Typst Documentation**: https://typst.app/docs/
- **Work Effort**: [WE-260119-4nh6](../WE-260119-4nh6_fhict_document_template_typst_initialization/WE-260119-4nh6_index.md)

## Notes

- Template size: 221.0 KiB
- Requires Typst 0.10.0 or later
- Supports BibTeX bibliography format
- Multi-language support is built-in
- Extensive customization options for academic use cases
