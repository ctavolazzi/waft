# Foundation V2: Professional PDF Generation System

## Overview

Foundation V2 is an enhanced PDF generation engine designed for professional scientific documentation, clinical reports, and institutional publishing. It maintains the elegant block-based architecture of V1 while adding advanced typography, sophisticated layout capabilities, and print-ready formatting.

## What's New in V2

### 1. Professional Typography System

**Font Families**:
- **Serif** (Times New Roman) - Academic weight, traditional, perfect for body text
- **Sans-Serif** (Helvetica/Arial) - Modern, clean, ideal for headers
- **Monospace** (Courier) - Technical data, code, logs

**Font Configuration**:
```python
config = FontConfig(
    serif_family="Times",
    serif_bold="Times-Bold",
    sans_family="Helvetica",
    sans_bold="Helvetica-Bold",
    mono_family="Courier",
    mono_bold="Courier-Bold",
)
```

### 2. The Clinical Standard Preset

The flagship preset for professional scientific documentation:

```python
config = DocumentConfig.clinical_standard(
    header="INSTITUTE FOR ADVANCED ONTOLOGICAL STUDIES",
    watermark=None,
)
```

**Features**:
- Times New Roman body text (11pt)
- Helvetica headers (16pt/14pt/12pt for H1/H2/H3)
- Professional 1-inch margins
- Line spacing: 1.4x
- Authoritative, institutional tone

**Visual Comparison**:

| Aspect | V1 (Typewriter) | V2 (Clinical Standard) |
|--------|-----------------|------------------------|
| Body Font | Courier 12pt | Times 11pt |
| Header Font | Courier Bold | Helvetica Bold |
| Aesthetic | Typewriter/Cyberpunk | Professional/Scientific |
| Line Spacing | 1.5x | 1.4x |
| Layout | Basic blocks | Advanced layout system |

### 3. Advanced Layout Blocks

#### CoverPage
Full professional cover page with institutional branding:

```python
engine.add(CoverPage(
    institution="INSTITUTE FOR ADVANCED ONTOLOGICAL STUDIES",
    division="Department of Computational Phenomenology",
    document_type="RESEARCH REPORT",
    document_number="Report No. 001-ALPHA",
    classification="INTERNAL USE ONLY",
))
```

#### MetadataRail
Styled metadata block with gray background (like a sidebar):

```python
engine.add(MetadataRail(
    title="Subject Information",
    metadata={
        "Subject ID": "991-DELTA",
        "Subject Name": "Fai Wei Tam",
        "Timeline": "001-ORIGIN-TAM",
        "Status": "DORMANT",
    }
))
```

#### RuleBlock
Horizontal rules for visual separation:

```python
engine.add(RuleBlock(
    thickness=0.5,
    width_percent=80,
))
```

#### TableBlock
Professional tables with headers:

```python
engine.add(TableBlock(
    headers=["Parameter", "Value", "Unit", "Status"],
    rows=[
        ["Coherence", "0.87", "ratio", "NORMAL"],
        ["Karma Balance", "0", "units", "BASELINE"],
    ],
))
```

### 4. Enhanced Existing Blocks

All V1 blocks have been enhanced with:
- Better page break handling (`_check_page_break`)
- Professional font selection
- Improved spacing and layout
- Color support

**SectionHeader** - Now uses proper header font (sans-serif by default):
```python
engine.add(SectionHeader("Executive Summary", level=1))  # H1
engine.add(SectionHeader("Methodology", level=2))  # H2
engine.add(SectionHeader("Data Collection", level=3))  # H3
```

**TextBlock** - Supports custom font families:
```python
engine.add(TextBlock("Body text in serif font"))
engine.add(TextBlock("Header text", font_family=FontFamily.SANS_SERIF, bold=True))
engine.add(TextBlock("Code", font_family=FontFamily.MONOSPACE))
```

### 5. Print Optimization

- Professional margins (1 inch / 72pt default)
- Better page break logic
- Consistent spacing throughout document
- PDF metadata (title, author, subject)
- Watermark support with proper color

## Complete Usage Example

### Generating a Clinical Report

```python
from pathlib import Path
from datetime import datetime
from waft.foundation_v2 import (
    DocumentEngine,
    DocumentConfig,
    CoverPage,
    MetadataRail,
    SectionHeader,
    TextBlock,
    RuleBlock,
    TableBlock,
    WarningBlock,
    SignatureBlock,
    LogBlock,
)

# Configure for Clinical Standard
config = DocumentConfig.clinical_standard(
    header="INSTITUTE FOR ADVANCED ONTOLOGICAL STUDIES",
    watermark=None,
)

# Initialize engine
engine = DocumentEngine(config)

# Set sensitive terms for auto-redaction
engine.add_sensitive_terms([
    "Fai Wei Tam",
    "991-DELTA",
    "San Francisco",
])

# Build document
engine.add(CoverPage(
    institution="INSTITUTE FOR ADVANCED ONTOLOGICAL STUDIES",
    division="Department of Computational Phenomenology",
    document_type="RESEARCH REPORT",
    document_number="Report No. 001-ALPHA",
    classification="INTERNAL USE ONLY",
))

engine.add(MetadataRail(
    title="Subject Information",
    metadata={
        "Subject ID": "991-DELTA",
        "Subject Name": "Fai Wei Tam",
        "Timeline": "001-ORIGIN-TAM",
        "Status": "DORMANT",
    }
))

engine.add(SectionHeader("Executive Summary", level=1))
engine.add(TextBlock(
    "This report documents the initial observations for Subject 991-DELTA "
    "within the WAFT framework. The subject has been successfully instantiated "
    "and is currently dormant pending activation."
))

engine.add(RuleBlock(thickness=0.5, width_percent=80))

engine.add(SectionHeader("Methodology", level=1))
engine.add(TextBlock(
    "All observations are conducted through non-invasive monitoring systems."
))

engine.add(TableBlock(
    headers=["Parameter", "Value", "Unit", "Status"],
    rows=[
        ["Coherence", "0.87", "ratio", "NORMAL"],
        ["Karma Balance", "0", "units", "BASELINE"],
    ],
))

engine.add(WarningBlock(
    "CRITICAL: Subject must not access this documentation.",
    severity="CRITICAL"
))

engine.add(SignatureBlock(
    role="Principal Investigator",
    name="Dr. [REDACTED]",
    timestamp=datetime(2026, 1, 10),
))

# Render
output_path = Path("_work_efforts/CLINICAL_REPORT_001.pdf")
engine.render(output_path)
```

## Configuration Presets

### Clinical Standard (Recommended)
```python
config = DocumentConfig.clinical_standard(
    header="YOUR INSTITUTION",
    watermark=None,
)
```
- Times body, Helvetica headers
- Professional margins
- Authoritative tone

### Scientific Journal
```python
config = DocumentConfig.scientific_journal()
```
- Times body, Helvetica headers
- 1.6x line spacing
- "DRAFT" watermark

### Classified Dossier (V1 Style)
```python
config = DocumentConfig.classified_dossier(
    header="SITE-DELTA-9",
    watermark="INTERNAL USE ONLY",
)
```
- Courier monospace throughout
- Typewriter aesthetic
- SCP/Dossier style

## Migration from V1

Foundation V2 is **mostly backward compatible** with V1. Key differences:

1. **Import Path**:
   - V1: `from waft.foundation import DocumentEngine`
   - V2: `from waft.foundation_v2 import DocumentEngine`

2. **Font Configuration**:
   - V1: Dictionary-based font config
   - V2: `FontConfig` dataclass (cleaner, type-safe)

3. **New Blocks**: V2 adds CoverPage, MetadataRail, RuleBlock, TableBlock

4. **Font Families**: V2 uses `FontFamily` enum instead of string keys

### Quick Migration

Most V1 code will work with minimal changes:

```python
# V1 Code
from waft.foundation import DocumentEngine, DocumentConfig
config = DocumentConfig.classified_dossier()

# V2 Code (same)
from waft.foundation_v2 import DocumentEngine, DocumentConfig
config = DocumentConfig.classified_dossier()  # Still works!
```

To use new features:
```python
from waft.foundation_v2 import DocumentEngine, DocumentConfig

# Use the new Clinical Standard
config = DocumentConfig.clinical_standard()

# Add new layout blocks
engine.add(CoverPage(...))
engine.add(MetadataRail(...))
engine.add(RuleBlock())
engine.add(TableBlock(...))
```

## Typography Hierarchy

V2 implements a professional typographic hierarchy:

| Element | Font | Size | Weight | Spacing |
|---------|------|------|--------|---------|
| Cover Title | Sans | 22pt | Bold | 1.5x |
| H1 | Sans | 16pt | Bold | 1.8x |
| H2 | Sans | 14pt | Bold | 1.5x |
| H3 | Sans | 12pt | Bold | 1.3x |
| Body | Serif | 11pt | Normal | 1.4x |
| Footer | Serif | 9pt | Normal | 1.0x |
| Code/Log | Mono | 9pt | Normal | 1.4x |

## Color Support

V2 adds RGB color configuration:

```python
config = DocumentConfig.clinical_standard()
config.text_color = (0, 0, 0)        # Black
config.header_color = (50, 50, 50)   # Dark gray
config.rule_color = (100, 100, 100)  # Medium gray
```

## Best Practices

### 1. Use Clinical Standard for Institutional Reports
```python
config = DocumentConfig.clinical_standard(
    header="YOUR INSTITUTION NAME",
)
```

### 2. Always Use CoverPage for Professional Documents
```python
engine.add(CoverPage(
    institution="INSTITUTE NAME",
    document_type="REPORT TYPE",
    document_number="Report No. XXX",
))
```

### 3. Use MetadataRail for Subject Info
Instead of KeyValueBlock, use MetadataRail for a more professional look:
```python
engine.add(MetadataRail(
    title="Subject Information",
    metadata={...}
))
```

### 4. Separate Sections with RuleBlock
```python
engine.add(RuleBlock(thickness=0.5, width_percent=80))
```

### 5. Use Proper Header Hierarchy
```python
engine.add(SectionHeader("Main Section", level=1))      # H1
engine.add(SectionHeader("Subsection", level=2))        # H2
engine.add(SectionHeader("Sub-subsection", level=3))    # H3
```

## Performance Notes

- V2 has the same performance as V1
- Page break checking is optimized
- Font caching is handled by fpdf2
- Typical generation time: < 1 second for 10-page documents

## Troubleshooting

### Issue: Fonts not rendering correctly
**Solution**: Ensure fpdf2 >= 2.7.0 is installed. Times, Helvetica, and Courier are standard PDF fonts.

### Issue: Text overflowing
**Solution**: V2 automatically handles word wrapping. If text still overflows, check:
- Font size (reduce if needed)
- Margins (increase if needed)
- Page width

### Issue: Page breaks in wrong places
**Solution**: V2 automatically manages page breaks. To force a break:
```python
# No built-in force break, but you can add large spacing:
engine.add(TextBlock(""))  # Empty block
```

## Future Enhancements (V3)

Planned features for V3:
- Multi-column layout support
- Image/figure embedding
- PDF/X compliance for professional printing
- CMYK color support
- Custom font embedding
- Chart/graph generation
- Table of contents generation
- Cross-references
- Footnotes/endnotes

## Example Output

The demo script generates `CLINICAL_STANDARD_DEMO.pdf` with:
- Professional cover page
- Styled metadata rail
- Clear section hierarchy
- Tables with data
- Warning blocks
- Signature blocks
- System logs appendix

Compare this to V1 output to see the dramatic improvement in professionalism and readability.

## Summary

Foundation V2 transforms PDF generation from "typewriter aesthetic" to "professional scientific publication." Key improvements:

✅ Professional typography (Times + Helvetica)
✅ Advanced layout blocks (CoverPage, MetadataRail, RuleBlock, TableBlock)
✅ The Clinical Standard preset
✅ Better spacing and page breaks
✅ Print-ready formatting
✅ Backward compatible with V1

**Use Foundation V2 for all new documentation that requires a professional, institutional appearance.**

---

*Foundation V2 - Engineered for the Institute for Advanced Ontological Studies*
*Version: 2.0.0 | Date: 2026-01-10*
