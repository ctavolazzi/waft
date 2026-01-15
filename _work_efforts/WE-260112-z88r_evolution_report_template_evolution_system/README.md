# Evolution Report Template Evolution System

**Work Effort**: WE-260112-z88r  
**Status**: Active  
**Created**: 2026-01-12

## Overview

This work effort tracks the development and evolution of alternative template formats for the complete evolution report. The `/evolve-another-template` command allows users to generate the same evolution data in different presentation styles.

## Purpose

The default evolution report format may not suit all use cases. This system provides:
- **Multiple Template Options**: Academic paper, field guide, lab notes, etc.
- **Same Data, Different Formats**: All templates use the same evolution data
- **Template Evolution**: New templates can be added over time
- **User Choice**: Users can select the format that best fits their needs

## Current Status

### ✅ Completed
- **TKT-z88r-001**: Create evolve-another-template command
- **TKT-z88r-002**: Implement academic paper template
- **TKT-z88r-003**: Implement field guide template

### 🚧 In Progress
- Template system architecture

### 📋 Planned
- **TKT-z88r-004**: Add lab notes template
- **TKT-z88r-005**: Add personal memo template
- **TKT-z88r-006**: Add technical memo template
- **TKT-z88r-007**: Create template comparison system
- **TKT-z88r-008**: Add template selection UI

## Available Templates

1. **academic** - Two-column academic paper format (arXiv style)
   - Abstract section
   - Author information
   - Section numbering
   - References
   - Professional typography

2. **field-guide** - Field guide format
   - Single-column layout
   - Clear section headers
   - Examples and use cases
   - Step-by-step format
   - Visual hierarchy

## Usage

```bash
# Generate with academic paper template
/evolve-another-template --template academic

# Generate with field guide template
/evolve-another-template --template field-guide

# List available templates
/evolve-another-template --list

# Generate all templates
/evolve-another-template --all
```

## Implementation

- **Command**: `.cursor/commands/evolve-another-template.md`
- **Script**: `scripts/evolve_another_template.py`
- **CLI**: `waft evolve-another-template` (registered in `src/waft/main.py`)
- **Templates**: `src/waft/templates/`

## Adding New Templates

To add a new template:

1. Create ticket in this work effort: `TKT-z88r-XXX`
2. Implement template builder function in `scripts/evolve_another_template.py`
3. Add template to `generate_with_template()` function
4. Update template list in command documentation
5. Test template generation
6. Mark ticket as completed

## Future Enhancements

- Template comparison system (side-by-side view)
- Template selection UI (interactive chooser)
- Template customization options
- Template preview before generation
- Template evolution tracking (version history)

## Related Work

- Evolution System: `/evolve` command
- PDF Generation: `src/waft/evolution/pdf_generator.py`
- Template System: `src/waft/templates/`
- Being System: `src/waft/being.py`

---

**All template evolution work and tickets are tracked in this work effort folder.**
