# DnD Game Visualization Wrapper

## Overview

Create a Typst template wrapper that uses D&D 5e Typst packages (`@preview/wenyuan-campaign:0.1.2` and `@preview/dragonling:0.2.0`) to generate D&D game visualizations as PDFs. This will enable generating beautiful D&D game documentation, character sheets, stat blocks, encounter diagrams, campaign state visualizations, and rule guides.

## Files to Create/Modify

### 1. Create Typst Wrapper Module

**File:** `src/waft/templates/typst/wrappers/dnd_game.py`

**Purpose:** Python wrapper for generating D&D game visualizations using Typst D&D packages

**Key Features:**

- Generate character sheets (PCs and NPCs)
- Render stat blocks (monsters, creatures)
- Display encounter visualizations (combat state, initiative order)
- Create campaign state diagrams (party composition, locations, NPCs)
- Generate dice roll visualizations
- Create spell/item reference cards
- Generate session documentation
- Display map/region information

**Function Signature:**

```python
from typing import Literal, Optional, List, Dict, Any
from dataclasses import dataclass
from pathlib import Path

DocumentType = Literal["character_sheet", "stat_block", "encounter", "campaign_state", "session_log", "spell_reference", "item_reference"]
TemplatePackage = Literal["wenyuan-campaign", "dragonling"]

@dataclass
class Character:
    """Character data structure with validation."""
    name: str
    class_level: str  # e.g., "Fighter 5"
    race: str
    background: Optional[str] = None
    alignment: Optional[str] = None
    ability_scores: Optional[Dict[str, int]] = None  # {"STR": 16, "DEX": 14, ...}
    hit_points: Optional[Dict[str, int]] = None  # {"current": 45, "max": 50}
    armor_class: Optional[int] = None
    skills: Optional[List[Dict[str, Any]]] = None
    equipment: Optional[List[str]] = None
    spells: Optional[List[str]] = None
    
    def __post_init__(self):
        """Validate character data after initialization."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Character name must be a non-empty string")
        if not self.class_level or not isinstance(self.class_level, str):
            raise ValueError("Character class_level must be a non-empty string")
        if not self.race or not isinstance(self.race, str):
            raise ValueError("Character race must be a non-empty string")
        # Validate ability scores if provided
        if self.ability_scores:
            valid_abilities = {"STR", "DEX", "CON", "INT", "WIS", "CHA"}
            for ability in self.ability_scores:
                if ability not in valid_abilities:
                    raise ValueError(f"Invalid ability score: {ability}. Must be one of {valid_abilities}")
                if not isinstance(self.ability_scores[ability], int) or self.ability_scores[ability] < 1 or self.ability_scores[ability] > 30:
                    raise ValueError(f"Ability score {ability} must be an integer between 1 and 30")

@dataclass
class StatBlock:
    """Monster/NPC stat block data structure."""
    name: str
    size_type: str  # e.g., "Medium humanoid (human)"
    armor_class: int
    hit_points: int
    speed: str  # e.g., "30 ft."
    ability_scores: Dict[str, int]
    skills: Optional[List[str]] = None
    damage_resistances: Optional[List[str]] = None
    damage_immunities: Optional[List[str]] = None
    condition_immunities: Optional[List[str]] = None
    senses: Optional[str] = None
    languages: Optional[str] = None
    challenge_rating: Optional[str] = None
    traits: Optional[List[Dict[str, str]]] = None  # [{"name": "Trait Name", "text": "Description"}]
    actions: Optional[List[Dict[str, str]]] = None
    legendary_actions: Optional[List[Dict[str, str]]] = None
    
    def __post_init__(self):
        """Validate stat block data."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Stat block name must be a non-empty string")
        if not isinstance(self.armor_class, int) or self.armor_class < 0:
            raise ValueError("Armor class must be a non-negative integer")
        if not isinstance(self.hit_points, int) or self.hit_points < 1:
            raise ValueError("Hit points must be a positive integer")
        # Validate ability scores
        valid_abilities = {"STR", "DEX", "CON", "INT", "WIS", "CHA"}
        for ability in self.ability_scores:
            if ability not in valid_abilities:
                raise ValueError(f"Invalid ability score: {ability}")

@dataclass
class EncounterParticipant:
    """Participant in an encounter (PC or NPC)."""
    name: str
    initiative: int
    is_player: bool
    current_hp: Optional[int] = None
    max_hp: Optional[int] = None
    armor_class: Optional[int] = None
    conditions: Optional[List[str]] = None
    
    def __post_init__(self):
        """Validate encounter participant."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Participant name must be a non-empty string")
        if not isinstance(self.initiative, int):
            raise ValueError("Initiative must be an integer")

def generate_dnd_game(
    title: str,
    content: str,
    output_path: Path,
    document_type: DocumentType = "character_sheet",
    template_package: TemplatePackage = "wenyuan-campaign",
    characters: Optional[List[Character]] = None,
    stat_blocks: Optional[List[StatBlock]] = None,
    encounter_participants: Optional[List[EncounterParticipant]] = None,
    show_rules: bool = False,
    **kwargs
) -> Path:
```

**Implementation Details:**

- Import D&D packages: `#import "@preview/wenyuan-campaign:0.1.2": *` or `#import "@preview/dragonling:0.2.0": *`
- Support multiple document types (character sheets, stat blocks, encounters, etc.)
- Use `wenyuan-campaign` for campaign documents and character sheets
- Use `dragonling` for stat blocks and general D&D 5e content
- Support character sheet generation with full stats
- Support stat block generation for monsters/NPCs
- Support encounter visualization with initiative order
- Include dice roll visualization helpers
- Generate spell/item reference cards
- Support campaign state documentation

**Security & Validation:**

- **Character Data Validation**: All character data validated via `Character` dataclass
  - Name, class, race must be non-empty strings
  - Ability scores must be integers 1-30
  - Hit points must be positive integers
  - Validation function: `_validate_character(character: Character) -> bool`

- **Stat Block Validation**: All stat block data validated via `StatBlock` dataclass
  - Name, size_type must be non-empty strings
  - AC, HP must be positive integers
  - Ability scores validated
  - Validation function: `_validate_stat_block(stat_block: StatBlock) -> bool`

- **Content Sanitization**: User-provided `content` must be sanitized before embedding in Typst template
  - Escape special Typst characters (`#`, `{`, `}`, `[`, `]`, `(`)
  - Use Typst's raw text blocks for user content when possible
  - Validate content doesn't contain dangerous Typst commands
  - Sanitization function: `_sanitize_typst_content(content: str) -> str`

- **Name/Text Validation**: All names and text fields sanitized to prevent Typst injection
  - Sanitize character names, monster names, spell names
  - Validate no command injection in text fields
  - Sanitization function: `_sanitize_name(name: str) -> str`

- **Document Type & Template Validation**: Use `Literal` types for type safety
  - `DocumentType = Literal["character_sheet", "stat_block", "encounter", "campaign_state", "session_log", "spell_reference", "item_reference"]`
  - `TemplatePackage = Literal["wenyuan-campaign", "dragonling"]`
  - Validate at runtime if needed (for dynamic inputs)

- **Error Handling**: Comprehensive error handling for:
  - Invalid character data (raise `ValueError` with clear message)
  - Invalid stat block structure (raise `ValueError` with details)
  - Typst compilation failures (propagate `RuntimeError` from `TypstCompiler`)
  - Missing D&D packages (handle gracefully with clear error message)

### 2. Update Typst Wrappers Init

**File:** `src/waft/templates/typst/wrappers/__init__.py`

**Action:** Add export for the new wrapper (optional, since registry auto-discovers)

### 3. Example Usage Script (Optional)

**File:** `examples/generate_dnd_visualization.py`

**Purpose:** Demonstrate how to use the wrapper to generate D&D game PDFs

**Examples to include:**

- Character sheet generation
- Stat block generation
- Encounter visualization
- Campaign state documentation
- Session log generation

## Implementation Details

### Document Types Supported

**Phase 1 (Initial Implementation):**

1. **Character Sheet**: Full D&D 5e character sheet with stats, skills, equipment
2. **Stat Block**: Monster/NPC stat block with combat stats, traits, actions

**Phase 2 (Future Enhancements):**

3. **Encounter**: Combat encounter visualization with initiative order
4. **Campaign State**: Party composition, locations, NPCs, world state
5. **Session Log**: Game session documentation with events, dice rolls
6. **Spell Reference**: Spell cards with full spell descriptions
7. **Item Reference**: Magic item cards with descriptions

**Note**: Start with Character Sheet and Stat Block only to reduce complexity and ensure quality. Add other document types in future iterations after initial implementation is stable.

### Template Packages

1. **Wenyuan Campaign** (`@preview/wenyuan-campaign:0.1.2`):
   - Best for: Campaign documents, character sheets, adventure modules
   - Features: Professional D&D campaign layout, statblocks, multi-column layouts
   - Requires: Custom fonts (TeX Gyre Bonum, Scaly Sans, etc.)

2. **Dragonling** (`@preview/dragonling:0.2.0`):
   - Best for: Stat blocks, general D&D 5e content formatting
   - Features: Stat blocks, spell formatting, breakout boxes, tables
   - Simpler: No custom font requirements

### Layout Features

- Character sheet with ability scores, skills, equipment
- Stat block with combat stats, traits, actions
- Initiative order visualization
- Party composition display
- Location/NPC tracking
- Dice roll history
- Spell/item cards

### Content Structure

The generated Typst content will include:

1. Title page with document type
2. Character sheet/stat block visualization (if provided)
3. Encounter state (if participants provided)
4. Rules section (if `show_rules=True`)
5. Custom content section

## Typst Template Structure

```typst
#import "@preview/wenyuan-campaign:0.1.2": *

#set page(margin: 1in)

= {title}

// Character sheet visualization
#if characters:
  #for character in characters:
    #character-sheet(character)

// Stat block visualization
#if stat_blocks:
  #for stat_block in stat_blocks:
    #stat-block(stat_block)

// Encounter visualization
#if encounter_participants:
  #encounter-state(..encounter_participants)

// Rules section
#if show_rules:
  #rules-section()

// Custom content
{content}
```

## Testing Plan

1. **Unit Tests:**
   - Test wrapper function with various parameters
   - Test different document types
   - Test different template packages
   - Test edge cases (empty characters, invalid stats)

2. **Visual Tests:**
   - Generate sample PDFs for each document type
   - Verify character sheet rendering
   - Check stat block formatting
   - Validate Typst compilation

3. **Example Scenarios:**
   - Level 5 Fighter character sheet
   - Orc stat block
   - Combat encounter with 4 PCs vs 3 goblins
   - Campaign state with party and locations

## Security Considerations

### Input Validation

1. **Character Data**: Must be validated via `Character` dataclass
   - Reject empty strings, None values, and invalid ability scores
   - Sanitize before embedding in Typst template
   - Validation happens before Typst compilation

2. **Stat Block Data**: Must be validated via `StatBlock` dataclass
   - Reject invalid AC, HP values
   - Validate ability scores
   - Sanitize trait/action descriptions

3. **User Content**: Sanitize all user-provided content
   - Escape special Typst characters
   - Use raw text blocks when appropriate
   - Validate no dangerous Typst commands present

4. **Name/Text Fields**: Sanitize all names and text
   - Character names, monster names, spell names
   - Prevent Typst injection in all text fields

5. **Path Validation**: Inherited from `TypstCompiler`
   - All paths validated for path traversal protection
   - Content size limits enforced
   - Compilation timeouts in place

### Error Handling

- **Invalid Inputs**: Raise `ValueError` with clear, actionable error messages
- **Compilation Failures**: Propagate `RuntimeError` from `TypstCompiler` with Typst error details
- **Missing Dependencies**: Handle D&D package unavailability gracefully with helpful error message
- **Type Errors**: Use `Literal` types for compile-time safety, runtime validation for dynamic inputs

## Assumptions

1. **D&D Package Availability**: Assumes D&D packages are available in Typst Universe
   - **Mitigation**: Handle gracefully if packages unavailable, provide clear error message
   - **Fallback**: Document minimum Typst version required (0.10.0+)

2. **Typst Version**: Assumes Typst CLI version 0.10.0 or higher
   - **Mitigation**: `TypstCompiler` already checks version on initialization
   - **Fallback**: Clear error message if version insufficient

3. **D&D 5e Knowledge**: Assumes users understand D&D 5e rules
   - **Mitigation**: Provide clear validation error messages with format examples
   - **Documentation**: Include format guide in module docstring

4. **Template Package Understanding**: Assumes users understand template package differences
   - **Mitigation**: Default to `wenyuan-campaign` (most feature-rich)
   - **Documentation**: Include template package descriptions in docstring

## Integration Points

- **TypstTemplateRegistry**: Auto-discovered via `generate_*` function pattern
- **TypstCompiler**: Uses existing compiler infrastructure with security hardening
- **D&D Packages**: External Typst package dependencies (handled by Typst)
- **QuestPDFGenerator**: Can be enhanced to use this wrapper for consistency

## Success Criteria

- ✅ Wrapper module created and follows existing patterns
- ✅ Supports Character Sheet and Stat Block document types (Phase 1)
- ✅ Generates visually appealing D&D game PDFs
- ✅ Auto-discovered by TypstTemplateRegistry
- ✅ Example usage script demonstrates capabilities
- ✅ Comprehensive module docstring with:
  - Purpose and usage examples
  - Character/stat block format documentation
  - Document type descriptions
  - Security considerations
  - Error handling documentation
- ✅ All inputs validated and sanitized
- ✅ Comprehensive error handling implemented
- ✅ Security measures in place (validation, sanitization)

## Future Enhancements (Out of Scope)

- Interactive D&D game logic
- Dice rolling and probability calculations
- Campaign management system
- Character creation wizard
- Map generation
- Initiative tracker integration
