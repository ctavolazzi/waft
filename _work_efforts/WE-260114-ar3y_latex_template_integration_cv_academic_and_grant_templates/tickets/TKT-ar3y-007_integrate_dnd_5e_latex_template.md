---
id: TKT-ar3y-007
parent: WE-260114-ar3y
title: "Integrate D&D 5e LaTeX Template"
status: pending
created: 2026-01-15T05:29:00.000Z
created_by: ctavolazzi
assigned_to: null
completed: null
---

# TKT-ar3y-007: Integrate D&D 5e LaTeX Template

## Metadata
- **Created**: Wednesday, January 14, 2026 at 9:29:00 PM PST
- **Parent Work Effort**: WE-260114-ar3y
- **Author**: ctavolazzi

## Description
Integrate the D&D 5e LaTeX template (rpgtex/DND-5e-LaTeX-Template) into WAFT's PDF template library system. This template provides authentic D&D 5e book styling with monster stat blocks, read-aloud text, sidebars, and special section headers perfect for campaign materials.

## Repository
- **URL:** https://github.com/rpgtex/DND-5e-LaTeX-Template
- **License:** MIT
- **Location:** `templates_exploration/dnd-5e-latex-template/`

## Key Features
- `dndbook` document class and `dnd` package
- Monster stat block environments (`DndMonster`)
- Read-aloud text boxes (`DndReadAloud`)
- Sidebars and comment boxes (`DndSidebar`, `DndComment`)
- Special section headers (feats, items, spells)
- D&D 5e color schemes (PHB, DMG, Basic Rules)
- Multi-language support
- Background images and footer decorations

## Acceptance Criteria
- [ ] Template repository cloned and explored
- [ ] Template structure documented in TEMPLATE_EXPLORATION.md
- [ ] Integration strategy defined
- [ ] Create LaTeX-based template module (`src/waft/templates/dnd5e_latex.py`)
- [ ] Create WeasyPrint alternative (`src/waft/templates/dnd5e_campaign.py`)
- [ ] Extract monster stat block structure
- [ ] Extract read-aloud and sidebar environments
- [ ] Support D&D 5e color schemes
- [ ] Integrate with existing `dnd_scenario.py` template
- [ ] Register in template library system (WE-260112-q6gl)
- [ ] Create command tools:
  - `/dnd-campaign-book` - Generate full campaign book
  - `/dnd-adventure` - Generate adventure module
  - `/dnd-monster-manual` - Generate monster collection
  - `/dnd-stat-block` - Generate single monster stat block

## Files Changed
- `templates_exploration/dnd-5e-latex-template/` - Cloned repository
- `TEMPLATE_EXPLORATION.md` - Updated with D&D 5e template analysis
- `src/waft/templates/dnd5e_latex.py` - (to be created) LaTeX-based template
- `src/waft/templates/dnd5e_campaign.py` - (to be created) WeasyPrint alternative

## Implementation Notes

### Integration Strategy

#### Option 1: LaTeX Compilation (Direct)
- Use template as-is with LaTeX compilation
- Create Python wrapper to generate `.tex` files
- Compile with `pdflatex`/`lualatex`/`xelatex`
- **Pros:** Authentic styling, full feature support
- **Cons:** Requires LaTeX installation, slower generation

#### Option 2: WeasyPrint Conversion (Recommended)
- Convert LaTeX styling to HTML/CSS
- Extract color schemes, fonts, layouts
- Recreate environments as HTML/CSS
- **Pros:** No LaTeX dependency, faster, integrates with existing templates
- **Cons:** May lose some LaTeX-specific features

#### Option 3: Hybrid Approach
- Use LaTeX for complex documents (campaign books)
- Use WeasyPrint for simpler documents (stat blocks, handouts)
- **Pros:** Best of both worlds
- **Cons:** More complex implementation

### Key Components to Extract

1. **Monster Stat Blocks**
   - Structure: type, basics, ability scores, actions, attacks
   - Styling: colored boxes, proper formatting
   - Integration: Can work with existing `src/waft/core/dnd5e/` modules

2. **Read-Aloud Text**
   - Styling: italic, colored background
   - Use case: Adventure modules, DM notes

3. **Sidebars and Comments**
   - Styling: floating boxes, colored backgrounds
   - Use case: Additional information, tips, references

4. **Color Schemes**
   - PHB colors (LightGreen, LightCyan, Mauve, Tan)
   - DMG colors (Lavender, Coral, SlateGray, Lilac)
   - Basic Rules (Green)
   - Integration: Can enhance existing `dnd_scenario.py` template

5. **Special Sections**
   - Feats, items, spells headers
   - Map regions (areas, sub-areas)
   - Tables with D&D styling

### Integration with Existing D&D Code

WAFT already has D&D-related code:
- `src/waft/core/dnd5e/` - D&D 5e game mechanics
- `src/waft/templates/dnd_scenario.py` - D&D scenario template (WeasyPrint)
- `src/waft/evolution/dnd5e_character_sheet_template.html` - Character sheet

The LaTeX template complements these by providing:
- Official book styling
- Monster stat block formatting
- Campaign book structure
- Professional publishing quality

### Commands to Create

1. **`/dnd-campaign-book`**
   - Generate full campaign book with LaTeX
   - Input: Campaign data (JSON/YAML)
   - Output: PDF campaign book

2. **`/dnd-adventure`**
   - Generate adventure module
   - Input: Adventure data
   - Output: PDF adventure module

3. **`/dnd-monster-manual`**
   - Generate monster collection
   - Input: Monster data (can use existing `src/waft/core/dnd5e/`)
   - Output: PDF monster manual

4. **`/dnd-stat-block`**
   - Generate single monster stat block
   - Input: Monster data
   - Output: PDF stat block

## Dependencies
- LaTeX installation (for Option 1)
- D&D 5e template files (already cloned)
- Existing D&D 5e modules in WAFT

## Related
- WE-260112-z88r (Evolution report templates - includes D&D scenario template)
- WE-260112-q6gl (PDF template library system)
- `src/waft/core/dnd5e/` (D&D 5e game mechanics)
- `src/waft/templates/dnd_scenario.py` (Existing D&D template)

## Next Steps
1. ✅ Clone repository (completed)
2. ✅ Document template structure (completed)
3. ⏳ Decide on integration approach (LaTeX vs WeasyPrint vs Hybrid)
4. ⏳ Create template modules
5. ⏳ Integrate with template library
6. ⏳ Create command tools
7. ⏳ Test with sample data

## Commits
- (populated as work progresses)
