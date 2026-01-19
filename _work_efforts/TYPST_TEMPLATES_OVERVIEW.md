# Typst Templates Overview

**Date**: 2026-01-19  
**Status**: Active Exploration

---

## Summary

This document provides an overview of Typst templates initialized for potential integration into the WAFT document generation system.

## Templates

### 1. FHICT Document Template

**Package**: `@preview/unofficial-fhict-document-template:1.2.1`  
**Work Effort**: [WE-260119-4nh6](WE-260119-4nh6_fhict_document_template_typst_initialization/WE-260119-4nh6_index.md)  
**Location**: `unofficial-fhict-document-template/`  
**Size**: 221.0 KiB

**Best For:**
- Academic papers and reports
- Technical documentation
- Thesis/dissertation documents
- Multi-language documents
- Documents requiring extensive citations

**Key Features:**
- Multi-language support (en, nl, de, fr, es)
- Bibliography with citation styles (IEEE, APA, etc.)
- Table of contents, figures, listings, tables
- Version history tracking
- Glossary support
- Index generation

**Documentation**: [FHICT Template Documentation](WE-260119-4nh6_fhict_document_template_typst_initialization/TEMPLATE_DOCUMENTATION.md)

---

### 2. Biz Report Template

**Package**: `@preview/biz-report:0.3.1`  
**Work Effort**: [WE-260119-ek8v](WE-260119-ek8v_biz_report_typst_template_initialization/WE-260119-ek8v_index.md)  
**Location**: `biz-report/`  
**Size**: 219.1 KiB

**Best For:**
- Business reports
- Executive summaries
- Project reports
- Client presentations
- Corporate documentation

**Key Features:**
- Customizable branding (logo, colors, fonts)
- Drop cap paragraphs
- Author profiles with images
- Info boxes with icons
- Document control tables
- Professional business styling

**Documentation**: [Biz Report Template Documentation](WE-260119-ek8v_biz_report_typst_template_initialization/TEMPLATE_DOCUMENTATION.md)

---

## Comparison

| Feature | FHICT Template | Biz Report Template |
|---------|---------------|---------------------|
| **Primary Use** | Academic/Technical | Business/Corporate |
| **Language Support** | Multi-language (5) | Single language |
| **Citations** | ✅ BibTeX support | ❌ No built-in |
| **Branding** | Limited | ✅ Extensive |
| **Info Boxes** | ❌ No | ✅ Yes (with icons) |
| **Author Profiles** | ✅ Yes (structured) | ✅ Yes (visual) |
| **Version History** | ✅ Built-in | ✅ Table format |
| **Glossary** | ✅ Yes | ❌ No |
| **Index** | ✅ Yes | ❌ No |
| **Table of Contents** | ✅ Advanced | Basic |
| **Drop Caps** | ❌ No | ✅ Yes |
| **Document Control** | ✅ Structured | ✅ Table format |

## Integration Strategy

### Phase 1: Template Registry
- Add both templates to WAFT's Typst template registry
- Create wrapper classes for each template
- Implement metadata mapping

### Phase 2: Document Generators
- Build document generator classes
- Support for WAFT document metadata
- Integration with existing PDF generation pipeline

### Phase 3: Advanced Features
- Bibliography integration for FHICT template
- Branding system integration for Biz Report
- Template selection based on document type
- Custom template configuration

## Usage Recommendations

### Use FHICT Template When:
- Creating academic or technical documents
- Need extensive citation support
- Require multi-language support
- Need glossary or index
- Creating long-form documents (thesis, manuals)

### Use Biz Report Template When:
- Creating business or corporate documents
- Need strong branding customization
- Want visual author profiles
- Need info boxes for highlights
- Creating executive-level reports

## Next Steps

1. ✅ **Template Initialization** - Both templates initialized
2. ✅ **Documentation** - Comprehensive docs created
3. ⏳ **Template Testing** - Test compilation and output
4. ⏳ **WAFT Integration** - Create wrapper classes
5. ⏳ **Registry Integration** - Add to template registry
6. ⏳ **Example Generation** - Create sample documents

## Resources

- **Typst Documentation**: https://typst.app/docs/
- **FHICT Template**: `@preview/unofficial-fhict-document-template:1.2.1`
- **Biz Report Template**: `@preview/biz-report:0.3.1`
- **Work Efforts**: 
  - [WE-260119-4nh6](WE-260119-4nh6_fhict_document_template_typst_initialization/WE-260119-4nh6_index.md)
  - [WE-260119-ek8v](WE-260119-ek8v_biz_report_typst_template_initialization/WE-260119-ek8v_index.md)

---

**Last Updated**: 2026-01-19
