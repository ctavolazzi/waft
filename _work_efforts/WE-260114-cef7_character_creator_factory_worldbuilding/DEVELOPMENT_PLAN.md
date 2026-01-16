# Character Creator Factory - Development Plan

**Work Effort**: WE-260114-cef7  
**Date**: 2026-01-14  
**Status**: In Progress

---

## Overview

Create a comprehensive character creator feature that generates rich, worldbuilding-ready characters with:
- D&D 5e character stats
- Comprehensive backstory and lore
- Character CVs (using LaTeX templates)
- Narrative generation
- Worldbuilding integration

---

## Architecture

### Core Components

```
CharacterCreatorFactory
├── CharacterGenerator
│   ├── D&D 5e Character Creation
│   ├── Backstory Generation (Storyteller)
│   └── Lore Generation
├── DocumentGenerator
│   ├── Character Sheet (D&D 5e LaTeX)
│   ├── CV Generator (LaTeX CV template)
│   ├── Backstory PDF (Storyteller)
│   └── Worldbuilding Document
└── EvolutionSystem
    ├── Being Integration
    └── Character Evolution
```

---

## Implementation Phases

### Phase 1: D&D 5e LaTeX Template Integration ✅ (TKT-cef7-001)

**Objective**: Clone and integrate D&D 5e LaTeX template repository

**Tasks**:
1. Clone repository: `https://github.com/rpgtex/DND-5e-LaTeX-Template.git`
2. Analyze template structure and capabilities
3. Create integration module: `src/waft/templates/dnd5e_latex.py`
4. Integrate with existing PDF generation system
5. Test character sheet generation

**Deliverables**:
- D&D 5e LaTeX template integrated
- Character sheet LaTeX generator
- Test character sheet output

**Dependencies**: None

---

### Phase 2: Character Creator Factory ✅ (TKT-cef7-002)

**Objective**: Create CharacterCreatorFactory class with factory pattern

**Tasks**:
1. Create `src/waft/character_creator/` module
2. Implement `CharacterCreatorFactory` class
3. Implement character creation methods:
   - `create_character()` - Basic character
   - `create_character_with_backstory()` - With backstory
   - `create_character_with_cv()` - With CV
   - `create_character_full()` - Complete character
4. Integrate with D&D 5e character system
5. Integrate with Being system for persistence

**Deliverables**:
- `CharacterCreatorFactory` class
- Character creation methods
- Integration with D&D 5e and Being systems

**Dependencies**: Phase 1 (D&D 5e LaTeX template)

---

### Phase 3: Backstory & Lore Generation ✅ (TKT-cef7-003)

**Objective**: Implement comprehensive backstory/lore generation

**Tasks**:
1. Integrate with Storyteller for narrative generation
2. Create backstory generation templates
3. Implement lore generation system
4. Create character history generator
5. Integrate with worldbuilding templates

**Deliverables**:
- Backstory generation system
- Lore generation system
- Character history generator
- Integration with Storyteller

**Dependencies**: Phase 2 (Character Creator Factory)

---

### Phase 4: CV Generator ✅ (TKT-cef7-004)

**Objective**: Create CV generator for characters using LaTeX templates

**Tasks**:
1. Integrate with CV LaTeX template (from WE-260114-ar3y)
2. Create CV data structure for characters
3. Map character stats/backstory to CV format
4. Generate character CV PDF
5. Test CV generation

**Deliverables**:
- Character CV generator
- CV LaTeX template integration
- Test CV output

**Dependencies**: 
- Phase 2 (Character Creator Factory)
- WE-260114-ar3y (CV LaTeX templates)

---

### Phase 5: Worldbuilding Integration ✅ (TKT-cef7-005)

**Objective**: Integrate with worldbuilding templates and narratives

**Tasks**:
1. Integrate with worldbuilding templates (`src/waft/templates/worldbuild.py`)
2. Create worldbuilding document generator for characters
3. Integrate character narratives with worldbuilding
4. Create character relationship mapping
5. Generate worldbuilding documents

**Deliverables**:
- Worldbuilding integration
- Character worldbuilding document generator
- Character relationship mapping

**Dependencies**: Phase 3 (Backstory & Lore Generation)

---

### Phase 6: CLI Command/Tool ✅ (TKT-cef7-006)

**Objective**: Create CLI command/tool for character creation

**Tasks**:
1. Create CLI command: `/create-character` or similar
2. Add command options:
   - `--name` - Character name
   - `--backstory` - Generate backstory
   - `--cv` - Generate CV
   - `--worldbuilding` - Generate worldbuilding doc
   - `--full` - Generate everything
3. Integrate with CLI system
4. Add help documentation
5. Test CLI command

**Deliverables**:
- CLI command for character creation
- Command options and help
- Integration with CLI system

**Dependencies**: Phases 2-5 (All core features)

---

### Phase 7: Documentation ✅ (TKT-cef7-007)

**Objective**: Document character creator usage and patterns

**Tasks**:
1. Create usage documentation
2. Document API reference
3. Create examples and tutorials
4. Document integration patterns
5. Update main documentation

**Deliverables**:
- Usage documentation
- API reference
- Examples and tutorials
- Integration guide

**Dependencies**: All previous phases

---

## File Structure

```
src/waft/
├── character_creator/
│   ├── __init__.py
│   ├── factory.py              # CharacterCreatorFactory
│   ├── generator.py            # Character generation logic
│   ├── backstory.py            # Backstory generation
│   ├── lore.py                 # Lore generation
│   └── cv_generator.py         # CV generation
├── templates/
│   ├── dnd5e_latex.py          # D&D 5e LaTeX template (NEW)
│   └── [existing templates...]
└── [existing modules...]
```

---

## Integration Points

### Existing Systems

1. **D&D 5e System** (`src/waft/core/dnd5e/`)
   - `DnD5eCharacter` class
   - `DnD5eStats` for calculations
   - `DnDRoller` for dice rolling

2. **Being System** (`src/waft/being.py`)
   - `Being` class for persistence
   - `BeingSystem` for management

3. **Storyteller** (`src/waft/evolution/storyteller.py`)
   - Narrative generation
   - Story PDF generation

4. **PDF Templates** (`src/waft/templates/`)
   - PDF generation system
   - Template registry

5. **Worldbuilding Templates** (`src/waft/templates/worldbuild.py`)
   - Worldbuilding document generation

### New Integrations

1. **D&D 5e LaTeX Template** (NEW)
   - Repository: https://github.com/rpgtex/DND-5e-LaTeX-Template.git
   - Character sheet LaTeX generation

2. **CV LaTeX Templates** (from WE-260114-ar3y)
   - TwentySecondsCurriculumVitae-LaTex
   - Character CV generation

---

## Usage Examples

### Basic Character Creation

```python
from src.waft.character_creator import CharacterCreatorFactory

factory = CharacterCreatorFactory()

# Create basic character
character = factory.create_character(
    name="Aelric the Bold",
    char_class="fighter",
    level=5
)
```

### Character with Backstory

```python
# Create character with backstory
character = factory.create_character_with_backstory(
    name="Lyra Moonwhisper",
    char_class="wizard",
    level=3,
    backstory_style="detailed"
)
```

### Character with CV

```python
# Create character with CV
character = factory.create_character_with_cv(
    name="Thorin Ironforge",
    char_class="cleric",
    level=7
)
# CV automatically generated
```

### Full Character (Everything)

```python
# Create complete character with all features
character = factory.create_character_full(
    name="Zephyr Stormcaller",
    char_class="ranger",
    level=4,
    generate_backstory=True,
    generate_cv=True,
    generate_worldbuilding=True
)
```

### CLI Usage

```bash
# Create basic character
waft create-character --name "Aelric the Bold" --class fighter --level 5

# Create character with backstory
waft create-character --name "Lyra Moonwhisper" --backstory

# Create character with CV
waft create-character --name "Thorin Ironforge" --cv

# Create full character
waft create-character --name "Zephyr Stormcaller" --full
```

---

## Testing Strategy

### Unit Tests
- Character creation methods
- Backstory generation
- CV generation
- Worldbuilding integration

### Integration Tests
- D&D 5e system integration
- Being system integration
- Storyteller integration
- Template system integration

### End-to-End Tests
- Complete character creation workflow
- Document generation
- CLI command execution

---

## Success Criteria

1. ✅ D&D 5e LaTeX template integrated and working
2. ✅ CharacterCreatorFactory creates characters successfully
3. ✅ Backstory generation produces rich narratives
4. ✅ CV generation creates professional character CVs
5. ✅ Worldbuilding integration works seamlessly
6. ✅ CLI command functional and documented
7. ✅ All documentation complete

---

## Next Steps

1. **Immediate**: Clone D&D 5e LaTeX template repository
2. **Phase 1**: Integrate D&D 5e LaTeX template
3. **Phase 2**: Create CharacterCreatorFactory class
4. **Phase 3**: Implement backstory/lore generation
5. **Phase 4**: Create CV generator
6. **Phase 5**: Integrate worldbuilding
7. **Phase 6**: Create CLI command
8. **Phase 7**: Document everything

---

**Last Updated**: 2026-01-14 21:27 PST
