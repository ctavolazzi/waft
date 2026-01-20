# WAFT Example: Teleport Massive Case File

This document describes a comprehensive example of WAFT's document generation capabilities.

## Quick Links

- **Work Effort**: `_work_efforts/WE-260119-ejtx_teleport_massive_official_guide_to_scint_traversal/`
- **One-Shot Prompt**: See `ONE_SHOT_PROMPT.md` in the work effort directory
- **Capability Documentation**: See `WAFT_CAPABILITY_EXAMPLE.md` in the work effort directory

## What This Example Demonstrates

This project showcases WAFT's ability to create a complete corporate "case file" containing:

1. **Multi-format document generation** (Typst reports, letters, invoices, business cards)
2. **Data-driven content** (JSON → multiple document types)
3. **PDF manipulation** (merging, assembly, booklet creation)
4. **Professional templates** (corporate branding, international standards)
5. **Automated workflows** (batch processing, script orchestration)
6. **Narrative integration** (interconnected documents telling a story)

## Key Statistics

- **Total Documents Created**: 15+ Typst files
- **Final Case File**: 138 pages
- **Team Members**: 9 founding team members
- **Business Cards**: 9 professional cards
- **Invoices**: 2 financial documents
- **Research Papers**: 7 papers compiled into booklet

## Typst Packages Used

- `@preview/s6t5-page-bordering:1.0.0` - Professional page borders
- `@preview/letterloom:1.0.0` - Professional letters
- `@preview/invoice-pro:0.1.1` - DIN 5008 compliant invoices
- `@preview/minimalbc:0.0.1` - Minimalist business cards

## Python Libraries Used

- `pypdf` - PDF merging
- `subprocess` - Typst compilation
- `json` - Data handling
- `pathlib` - File operations

## Use Cases

This example demonstrates WAFT's suitability for:

- Corporate documentation
- Research compilation
- Professional correspondence
- Financial documentation
- Marketing materials
- Complex document workflows

## Recreating This Example

See `ONE_SHOT_PROMPT.md` in the work effort directory for a complete prompt that can recreate this entire project in one session.
