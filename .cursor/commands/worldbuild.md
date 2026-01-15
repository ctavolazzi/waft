# /worldbuild - Worldbuilding Document Creator

**Purpose:** Create compelling worldbuilding documents (fantasy or factual) with Foundation/TM formatting elements

**Usage:** `/worldbuild [content] [options]`

**Script:** `scripts/create_worldbuild.py`

---

## Overview

The Worldbuild tool creates rich, formatted PDF documents perfect for:
- **Fantasy Worldbuilding**: Lore, characters, locations, magic systems
- **Factual Documentation**: Reports, manuals, guides, research papers
- **SCP-style Documentation**: Anomaly reports, containment procedures
- **Corporate Reports**: Professional documentation with branding

**Formatting Elements:**
- KeyValueBlock (metadata, parameters)
- WarningBlock (severity levels: WARNING, CAUTION, CRITICAL)
- SignatureBlock (authorization, signatures)
- SectionHeader (hierarchical)
- Summary boxes
- Tables
- Log blocks (terminal-style)
- Classification banners

---

## Quick Start

### From Markdown
```
/worldbuild title:"Character Profile" markdown:"# Character Name\n\nDescription here"
```

### From File
```
/worldbuild file:character.md title:"Character Profile" doc-id:"CHAR-001"
```

### From Text
```
/worldbuild title:"Location Guide" text:"The ancient city of..."
```

---

## Features

- **Foundation/TM Elements**: KeyValueBlock, WarningBlock, SignatureBlock
- **Field Guide Styling**: Operational manual aesthetic
- **Flexible Content**: Markdown, text, structured JSON
- **Professional Formatting**: Classification banners, document headers
- **Worldbuilding Ready**: Perfect for fantasy or factual documentation

---

## Usage Examples

### Character Profile
```
/worldbuild title:"Character Profile" markdown:"# Elara Moonwhisper\n\nElven mage from the Northern Forests..."
```

### Location Guide
```
/worldbuild title:"The Ancient City" file:location.md doc-id:"LOC-001" classification:"PUBLIC"
```

### Research Report
```
/worldbuild title:"Research Report" markdown:"# Study Results\n\nFindings indicate..." doc-id:"TM-ARCH-009"
```

### With Custom Options
```
/worldbuild title:"Dossier" markdown:"# Subject\n\nDetails..." doc-id:"DOS-001" classification:"CLASSIFIED" issued-by:"Foundation"
```

---

## Output

All documents are saved to:
- `_work_efforts/worldbuild/[title]_[date].pdf`

Format:
- **Professional styling** (Foundation + Field Guide hybrid)
- **Printer-friendly** (black and white)
- **Ready for binder** (standard letter size)
- **Rich formatting** (tables, warnings, signatures, metadata)

---

## Integration

The Worldbuild tool is part of WAFT's document generation system:

```python
from waft import WorldbuildDocument

# Create document
doc = WorldbuildDocument(
    title="Character Profile",
    doc_id="CHAR-001",
    classification="INTERNAL"
)

# Add content blocks
doc.add_keyvalue_block({
    "Name": "Elara Moonwhisper",
    "Race": "Elf",
    "Class": "Mage",
    "Level": "15"
})

doc.add_section_header("Background", level=2)
doc.add_text("Elara was born in the Northern Forests...")

doc.add_warning_block("Character is marked as dangerous", severity="CAUTION")

doc.add_signature_block(
    role="AUTHORIZED BY",
    name="Game Master"
)

# Generate PDF
doc.generate()
```

---

## Use Cases

- **Fantasy Worldbuilding**: Create character sheets, location guides, lore documents
- **Game Documentation**: Player guides, rulebooks, campaign notes
- **Research Papers**: Academic-style reports with proper formatting
- **Corporate Reports**: Professional documentation with branding
- **SCP Documentation**: Anomaly reports, containment procedures
- **Technical Manuals**: Equipment guides, operational procedures

---

## Philosophy

Combines the best of:
- **Foundation V1/V2**: Rich block-based content (KeyValueBlock, WarningBlock, SignatureBlock)
- **TM Reports**: Professional corporate styling
- **Field Guides**: Operational manual aesthetic
- **Briefing Documents**: Compact, information-dense formatting

Result: A truly compelling worldbuilding tool that's also useful for factual documentation.

---

**Created for worldbuilders, game masters, researchers, and document creators.**

--- End Command ---
