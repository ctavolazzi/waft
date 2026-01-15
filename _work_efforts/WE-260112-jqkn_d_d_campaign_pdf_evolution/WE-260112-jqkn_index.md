---
id: WE-260112-jqkn
title: "D&D Campaign PDF Evolution"
status: active
created: 2026-01-12T16:47:08.000Z
created_by: ctavolazzi
last_updated: 2026-01-12T16:47:08.000Z
branch: feature/WE-260112-jqkn-d_d_campaign_pdf_evolution
repository: waft
---

# WE-260112-jqkn: D&D Campaign PDF Evolution

## Metadata
- **Created**: Monday, January 12, 2026 at 4:47:08 PM PST
- **Author**: ctavolazzi
- **Repository**: waft
- **Branch**: feature/WE-260112-jqkn-d_d_campaign_pdf_evolution

## Objective
Create a comprehensive D&D 5e campaign plan that serves as a testbed for evolving the PDF maker. Generate multiple campaign documents using different PDF generator features, styles, and layouts to identify improvements, test capabilities, and document evolution.

## Campaign: "The Shattered Crown"
A 3-act campaign (levels 1-5) focused on political intrigue and ancient magic.

## Documents to Generate
1. **Player's Guide** - Campaign introduction with premium styling
2. **Dungeon Master's Guide** - Complete campaign reference with clinical standard styling
3. **Encounter Sheets** - Quick reference with compact layout
4. **World Map Document** - Location guide with image integration
5. **NPC Reference Cards** - Quick NPC lookup with card-based layout

## Progress
- 1/12/2026: Work effort created. Starting campaign content creation.
- 1/12/2026: All 5 campaign documents created and PDFs generated.
- 1/12/2026: Quality analysis completed and findings documented.
- 1/12/2026: Evolution report generated.
- 1/12/2026: Work effort PDF generator tool created - converts entire work effort to comprehensive PDF.

## Commits
- (populated as work progresses)

## Related
- PDF Generator: `src/waft/evolution/pdf_generator.py`
- Scientific PDF Generator: `src/waft/evolution/scientific_pdf_generator.py`
- PDF Generation Script: `examples/generate_dnd_campaign_pdfs.py`

## Tools

### Work Effort PDF Generator
**File:** `generate_work_effort_pdf.py`

Converts the entire work effort into a comprehensive PDF document including:
- All markdown files (campaign content, findings, analysis)
- Generated PDFs (as references with file sizes)
- Screenshots/PNG files (as references)
- Analysis results (formatted from JSON)
- Code examples (all scripts used)
- Complete documentation

**Usage:**
```bash
python3 _work_efforts/WE-260112-jqkn_d_d_campaign_pdf_evolution/generate_work_effort_pdf.py
```

**Output:**
- `WE-260112-jqkn_COMPLETE.pdf` - Complete work effort PDF
- `WE-260112-jqkn_COMPLETE.md` - Intermediate markdown (for debugging)

**Features:**
- Automatically collects all content from work effort
- Formats analysis results from JSON
- Includes code examples
- References all generated PDFs and screenshots
- Uses ScientificPDFGenerator for quality analysis
- Premium styling for professional presentation

---

### Character Sheet Generator
**File:** `generate_character_sheet.py`

Generates D&D 5e character sheet PDFs in both blank (template) and filled formats.

**Usage:**
```bash
# Generate both blank and example filled sheets
python3 _work_efforts/WE-260112-jqkn_d_d_campaign_pdf_evolution/generate_character_sheet.py
```

**Output:**
- `character_sheet_blank.pdf` - Blank template for manual filling
- `character_sheet_[name].pdf` - Filled character sheet (example: Aldric the Brave)

**Features:**
- **Blank Template**: Complete D&D 5e character sheet with all standard fields
- **Filled Sheets**: Automatically calculates modifiers, skill bonuses, saving throws
- **Standard Format**: All D&D 5e fields included (abilities, skills, combat, equipment, etc.)
- **Customizable**: Pass character data dictionary to generate custom sheets
- **Clinical Standard Styling**: Clean, professional appearance

**Character Data Format:**
```python
character_data = {
    "name": "Character Name",
    "class": "Fighter",
    "level": 3,
    "abilities": {"STR": 16, "DEX": 13, "CON": 15, "INT": 10, "WIS": 12, "CHA": 11},
    "skill_proficiencies": ["Athletics", "Perception"],
    "attacks": [{"name": "Longsword", "bonus": 5, "damage": "1d8+3", ...}],
    # ... more fields
}
```

**Functions:**
- `generate_blank_sheet()` - Creates blank template
- `generate_filled_sheet(character_data)` - Creates filled sheet from data

---

### Being Character Sheet Generator
**File:** `src/waft/evolution/being_character_sheet_generator.py`

Generates D&D 5e character sheets for Beings in multiple formats:
- **.txt** (default, generated automatically when Being is created)
- **.md** (on demand)
- **.pdf** (on demand)

**Integration:**
- Automatically generates `.txt` character sheet when a Being is spawned via `BeingSystem.spawn_being()`
- Uses template with placeholders for key details
- Converts Being skills and attributes to D&D character stats
- Integrates with D&D 5e character system

**Usage:**

**Automatic (.txt generation):**
```python
from src.waft.being import BeingSystem

being_system = BeingSystem(project_path=project_path)
being = being_system.spawn_being(reality_id="my_reality")
# .txt character sheet automatically generated in:
# _hidden/.truth/beings/{being_id}/character_sheet.txt
```

**On Demand (.md and .pdf):**
```python
from src.waft.evolution.being_character_sheet_generator import (
    generate_character_sheet_md,
    generate_character_sheet_pdf
)

# Generate .md
md_path = generate_character_sheet_md(being, project_path=project_path)

# Generate .pdf
pdf_path = generate_character_sheet_pdf(being, project_path=project_path)
```

**Features:**
- **Template System**: Uses placeholders for key details
- **Being Integration**: Converts Being skills to D&D ability scores
- **Automatic Generation**: .txt created automatically on Being spawn
- **On-Demand Formats**: .md and .pdf generated only when requested
- **D&D 5e Compatible**: Full D&D 5e character sheet format
- **Being Data Mapping**: Maps Being personality, memories, skills to character sheet

**Template Placeholders:**
- `{NAME}`, `{CLASS_LEVEL}`, `{BACKGROUND}`, etc.
- `{STR}`, `{STR_MOD}`, `{STR_SAVE}`, etc. (all abilities)
- `{ACROBATICS}`, `{ATHLETICS}`, etc. (all skills)
- `{AC}`, `{HP}`, `{INITIATIVE}`, etc. (combat stats)
- `{BEING_ID}`, `{REALITY_ID}`, `{GENERATED_DATE}` (metadata)

**Functions:**
- `generate_character_sheet_txt(being, ...)` - Auto-called on spawn, generates .txt
- `generate_character_sheet_md(being, ...)` - On-demand, generates .md
- `generate_character_sheet_pdf(being, ...)` - On-demand, generates .pdf
- `being_to_character_data(being, character)` - Converts Being to character data
- `create_character_from_being(being)` - Creates D&D character from Being
