---
id: TKT-z88r-010
title: "Add D&D Scenario Template"
status: completed
created: 2026-01-12T22:18:00.000Z
created_by: ctavolazzi
last_updated: 2026-01-12T22:18:00.000Z
work_effort: WE-260112-z88r
---

# TKT-z88r-010: Add D&D Scenario Template

## Status: ✅ Completed

## Objective
Create a D&D scenario-themed template for evolution reports, featuring a fantasy/parchment aesthetic perfect for presenting evolution data in an adventure format.

## Implementation

### Template Created
- **File**: `src/waft/templates/dnd_scenario.py`
- **Style**: Fantasy/parchment aesthetic with medieval styling
- **Features**:
  - Parchment/cream background with aged paper aesthetic
  - Medieval serif typography (Times New Roman)
  - Decorative borders and dividers
  - Fantasy color palette (browns, golds, deep reds)
  - Stat block styling for Being statistics
  - Adventure box formatting
  - Treasure box styling for knowledge gained

### Integration
- ✅ Added `build_dnd_scenario_content()` function to `evolve_another_template.py`
- ✅ Added `dnd-scenario` template option to `generate_with_template()`
- ✅ Added to template list in `list_templates()`
- ✅ Added to `--all` template generation list

### Template Features
- **Color Scheme**: 
  - Background: #f4e8d0 (parchment)
  - Container: #faf5eb (cream)
  - Text: #3d2817 (dark brown)
  - Headings: #8b0000 (deep red), #654321 (brown), #8b4513 (saddle brown)
  - Accents: #daa520 (gold)
- **Typography**: Times New Roman serif font
- **Special Elements**:
  - Stat blocks for Being statistics
  - Adventure boxes for quest overview
  - Treasure boxes for knowledge gained
  - Decorative dividers with symbols
  - Medieval borders and styling

## Usage

```bash
# Generate with D&D scenario template
/evolve-another-template --template dnd-scenario

# Or use interactively
/evolve-another-template
# Select "dnd-scenario" from the list
```

## Files Created
- `src/waft/templates/dnd_scenario.py` - D&D scenario template module

## Files Modified
- `scripts/evolve_another_template.py` - Added DnD template support

## Testing
- Template file created and validated
- Integration with evolve-another-template script complete
- Ready for use with evolution reports

## Notes
The D&D scenario template presents evolution data as an adventure quest, making the technical evolution process more engaging and narrative-driven. Perfect for users who want a fantasy-themed presentation of their Being's evolution journey.
