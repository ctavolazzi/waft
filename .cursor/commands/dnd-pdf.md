# /dnd-pdf - Generate D&D PDFs with Typst

**Purpose:** Generate beautiful D&D 5e PDFs (character sheets, stat blocks, encounters) using Typst templates

**Usage:** `/dnd-pdf [type] [options]`

**Types:**
- `character` - Generate character sheet PDF
- `stat-block` - Generate monster/NPC stat block PDF
- `encounter` - Generate encounter visualization PDF
- `party` - Generate party character sheets PDF

**Options:**
- `--name [name]` - Character/monster name
- `--output [path]` - Output PDF path (default: auto-generated)
- `--template [wenyuan|dragonling]` - Template package (default: wenyuan)

---

## Overview

The `/dnd-pdf` command generates professional D&D 5e PDFs using Typst templates:

- **Character Sheets**: Full D&D 5e character sheets with stats, skills, equipment
- **Stat Blocks**: Monster and NPC stat blocks with combat stats, traits, actions
- **Encounter Visualizations**: Combat encounter with initiative order
- **Party Sheets**: Multiple character sheets in one PDF

**Perfect for:**
- Creating character sheets for your campaign
- Generating monster stat blocks for encounters
- Documenting encounters and combat
- Creating party reference sheets

---

## Quick Start

### Generate Character Sheet
```
/dnd-pdf character --name "Thorin Ironforge"
```

### Generate Stat Block
```
/dnd-pdf stat-block --name "Orc"
```

### Generate Encounter
```
/dnd-pdf encounter
```

### Generate Party Sheets
```
/dnd-pdf party
```

---

## Examples

### Character Sheet
```
/dnd-pdf character --name "Lyra Moonwhisper" --template wenyuan
```

Generates a character sheet PDF with:
- Ability scores and modifiers
- Skills and proficiencies
- Equipment and inventory
- Hit points and armor class
- Spells (if applicable)

### Stat Block
```
/dnd-pdf stat-block --name "Ancient Dragon" --template dragonling
```

Generates a stat block PDF with:
- Combat statistics (AC, HP, speed)
- Ability scores
- Traits and special abilities
- Actions and legendary actions
- Challenge rating

### Encounter Visualization
```
/dnd-pdf encounter
```

Generates an encounter PDF showing:
- Initiative order
- Participant stats (HP, AC)
- Current conditions
- Combat state

---

## Template Packages

### Wenyuan Campaign (`wenyuan`)
- **Best for**: Character sheets, campaign documents
- **Style**: Professional D&D campaign layout
- **Features**: Multi-column layouts, statblocks

### Dragonling (`dragonling`)
- **Best for**: Stat blocks, general D&D content
- **Style**: Clean, official-style formatting
- **Features**: Stat blocks, spell formatting, tables

---

## Integration

The command uses:
- **Typst Wrapper**: `src/waft/templates/typst/wrappers/dnd_game.py`
- **Typst Packages**: `@preview/wenyuan-campaign:0.1.2`, `@preview/dragonling:0.2.0`
- **Typst Compiler**: WAFT's TypstCompiler with security hardening

---

## Output

PDFs are generated in:
- Default: `examples_output/` directory
- Custom: Path specified with `--output` option

Files are named automatically:
- `{name}_character_sheet.pdf`
- `{name}_stat_block.pdf`
- `encounter_{timestamp}.pdf`

---

**Created to provide easy PDF generation for D&D game materials using Typst templates.**

---

End Command ---
