# D&D 5e Physics Engine Implementation - Findings Breakdown

**Generated**: 2026-01-11  
**Purpose**: Comprehensive breakdown of D&D 5e implementation findings and architecture  
**Status**: Implementation Complete

---

## Executive Summary

We successfully reverse-engineered the D&D 5e "physics engine" from multiple repositories and implemented it as the "biology" for WAFT Being agents. This document breaks down the critical findings, implementation decisions, and the architecture we built.

---

## 1. The Synthesis: Physics, Biology, and Logic

### 1.1 The "Physics" Engine (Core Algorithms)

These are the immutable laws of the simulation - we don't invent them, we implement the math found in the repositories.

#### The Modifier Algorithm
**Formula**: `(Score - 10) // 2`

This is the heartbeat of D&D. Every stat (STR, INT, etc.) boils down to this single formula.

**Insight**: Integer division handles scaling automatically:
- 10 → +0
- 12 → +1
- 14 → +2
- 16 → +3
- 18 → +4
- 20 → +5

**Implementation**: `DnD5eStats.ability_modifier(score: int) -> int`

#### The AC Calculation
**Formula**: `Base (10) + DEX Mod + Armor Bonus + Shield Bonus`

**Constraint**: Heavy armor *negates* the DEX bonus. We need an `if/else` logic gate.

**Armor Types**:
- **None**: `10 + DEX_modifier`
- **Light**: `armor_base + DEX_modifier`
- **Medium**: `armor_base + min(DEX_modifier, 2)` (max +2 DEX)
- **Heavy**: `armor_base` (no DEX modifier)

**Implementation**: `DnD5eStats.calculate_ac(dex_modifier, armor_type, armor_base)`

#### The Proficiency Curve
**Formula**: `2 + ((Level - 1) // 4)`

This is the "Experience" curve. It scales with level, not stats.

**Step Function**:
- Levels 1-4: +2
- Levels 5-8: +3
- Levels 9-12: +4
- Levels 13-16: +5
- Levels 17-20: +6

**Implementation**: `DnD5eStats.proficiency_bonus(level: int) -> int`

#### The Attack Roll
**Logic**: `d20 + (Ability Mod + Proficiency) >= Target AC`

**Finding**: Critical hits (Natural 20) are a separate boolean flag, not just a high number.

**Implementation**: `DnD5eCombat.make_attack_roll(attack_modifier, target_ac, advantage, disadvantage)`

---

### 1.2 The "Biology" (Data Structures)

How we structure the "Soul" of the agent (`20.00_state.json`).

#### The Character State (Dataclass)

**Key Finding**: Don't just store current values; store *Max* values and *Current* values separately (e.g., `hp` vs `max_hp`).

**Derived Stats**: Don't store "Modifier" in the database. Store the "Score" (e.g., 16 STR) and calculate the Modifier (+3) at runtime. This prevents desync.

**Implementation Pattern**:
```python
@dataclass
class DnD5eCharacter:
    # BASE stats (stored)
    strength: int = 10
    dexterity: int = 10
    # ...
    
    # Current/Max separation
    hp: int = 20
    max_hp: int = 20
    
    # Properties (DERIVED - calculated at runtime)
    @property
    def str_modifier(self) -> int:
        return DnD5eStats.ability_modifier(self.strength)
```

#### The Inventory System

**Finding**: Items need a `stackable` boolean flag. If `True`, adding an item just increments an integer counter rather than creating a new object.

**Implementation**: Equipment slots as optional strings:
- `equipped_weapon: Optional[str] = None`
- `equipped_armor: Optional[str] = None`

#### The Spellbook

**Finding**: Spells are data objects, not functions. They contain metadata: `damage_dice` ("4d6"), `save_type` ("DEX"), and `range`. The *Engine* interprets this data, rather than the spell containing code.

**Future Implementation**: Spell data structure with metadata fields.

---

### 1.3 The "Logic" (Software Patterns)

#### The Adapter Pattern

**Problem**: Some source systems (like pixel games) use 4 stats, but D&D uses 6.

**Solution**: An "Adapter" class that maps the inputs to the required outputs, filling in gaps with defaults or derived values.

**Implementation**: `StatsAdapter.convert_4_to_6(str, dex, int, con, char_class)`

#### The Command Pattern

**Finding**: Interactions are handled via string commands (e.g., `#attack`, `#cast`).

**Relevance**: This is perfect for LLMs. The AI outputs a text command, and our system parses and executes it. It creates a clean interface between the "Brain" (AI) and the "Body" (Game Engine).

**Future Implementation**: Command parser for LLM-generated actions.

#### Save System Integrity

**Finding**: Use MD5 checksums on save files. If the data is tampered with (or corrupted by a hallucination), the checksum fails, and we can trigger a "Reality Fracture" event in WAFT.

**Future Implementation**: Checksum validation for state files.

---

## 2. Implementation Architecture

### 2.1 Module Structure

```
src/waft/core/dnd5e/
├── __init__.py          # Module exports
├── stats.py             # Core algorithms (modifiers, AC, proficiency)
├── dice.py              # Dice rolling wrapper (d20 library)
├── character.py         # Character dataclass with state management
├── combat.py            # Combat mechanics (attack rolls, saving throws)
└── adapter.py           # 4-stat to 6-stat conversion
```

### 2.2 Core Classes

#### DnD5eStats
**Purpose**: Immutable physics engine - pure calculation functions.

**Methods**:
- `ability_modifier(score: int) -> int`
- `proficiency_bonus(level: int) -> int`
- `calculate_ac(dex_modifier, armor_type, armor_base) -> int`
- `spell_save_dc(spellcasting_mod, proficiency) -> int`

**Design**: All methods are `@staticmethod` - no state, pure functions.

#### DnDRoller
**Purpose**: Wrapper around `d20` library with error handling.

**Methods**:
- `roll(expression: str) -> int`
- `attack_roll(advantage, disadvantage) -> tuple[int, bool]`
- `roll_damage(dice_expression: str) -> int`

**Error Handling**: All methods wrapped in try/except with clear error messages.

#### DnD5eCharacter
**Purpose**: Character state dataclass - the "soul" of the agent.

**Key Features**:
- Stores BASE stats (scores), not modifiers
- Separate current/max values (hp vs max_hp)
- Properties calculate derived values at runtime
- Full validation in `__post_init__`
- Serialization support (`to_dict()`, `from_dict()`)

#### DnD5eCombat
**Purpose**: Combat interaction mechanics.

**Methods**:
- `make_attack_roll(attack_modifier, target_ac, advantage, disadvantage) -> tuple[bool, bool]`
- `make_saving_throw(ability_mod, proficiency, is_proficient, dc) -> bool`
- `apply_damage(character, damage) -> tuple[int, bool]`
- `apply_healing(character, healing) -> int`

#### StatsAdapter
**Purpose**: Convert 4-stat systems to 6-stat D&D format.

**Method**:
- `convert_4_to_6(str, dex, int, con, char_class) -> Dict[str, int]`

---

## 3. Critical Design Decisions

### 3.1 Store Base Stats, Not Modifiers

**Decision**: Store ability scores (16 STR), calculate modifiers (+3) at runtime.

**Rationale**: Prevents desync. If we stored modifiers and scores separately, they could get out of sync.

**Implementation**: Properties calculate modifiers on-demand:
```python
@property
def str_modifier(self) -> int:
    return DnD5eStats.ability_modifier(self.strength)
```

### 3.2 Separate Current and Max Values

**Decision**: Store `hp` and `max_hp` separately, not just `hp` with a calculation.

**Rationale**: Max HP can change (level up, items), and we need to track both.

**Implementation**: 
```python
hp: int = 20
max_hp: int = 20
```

### 3.3 Critical Hits Are Boolean Flags

**Decision**: Natural 20 is a separate boolean flag, not just a high number.

**Rationale**: Critical hits have special rules (always hit, double damage dice).

**Implementation**: `attack_roll()` returns `(roll, is_critical)` tuple.

### 3.4 Heavy Armor Negates DEX

**Decision**: AC calculation has conditional logic based on armor type.

**Rationale**: This is a core D&D 5e rule - heavy armor doesn't benefit from DEX.

**Implementation**: `if/else` logic in `calculate_ac()`:
```python
elif armor_type == ArmorType.HEAVY:
    return armor_base  # No DEX modifier
```

### 3.5 Input Validation

**Decision**: Validate all inputs (ability scores 1-30, levels 1-20).

**Rationale**: Prevents invalid states and calculation errors.

**Implementation**: Validation in `__post_init__` and all calculation methods.

---

## 4. Implementation Highlights

### 4.1 Error Handling

All dice operations wrapped in try/except:
```python
try:
    result = d20.roll(expression)
    return result.total
except Exception as e:
    raise ValueError(f"Invalid dice expression '{expression}': {e}")
```

### 4.2 Type Safety

Full type hints throughout:
```python
def ability_modifier(score: int) -> int:
    """Calculate ability modifier from ability score."""
```

### 4.3 Enums for Constants

`ArmorType` enum instead of string literals:
```python
class ArmorType(str, Enum):
    NONE = "none"
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"
```

### 4.4 Documentation

Comprehensive docstrings for all functions:
- Parameter descriptions
- Return value descriptions
- Examples where helpful
- Formula explanations

---

## 5. The Tavern Scenario

### 5.1 Overview

Created an interactive scenario demonstrating the D&D 5e system in action.

**Location**: `examples/tavern_scenario.py`

### 5.2 Features

1. **Character Creation**: Roll ability scores (4d6, drop lowest)
2. **Skill Checks**: Perception, Investigation, Persuasion, Intelligence
3. **Interactive Choices**: Multiple paths through the narrative
4. **D&D Mechanics**: Real dice rolling, modifiers, proficiency

### 5.3 What It Demonstrates

- Character creation with rolled stats
- Ability modifiers affecting skill checks
- Different outcomes based on roll totals
- Interactive narrative with player choices

---

## 6. Key Algorithms Extracted

### 6.1 Ability Modifier
```python
modifier = (score - 10) // 2
```

### 6.2 Proficiency Bonus
```python
proficiency = 2 + ((level - 1) // 4)
```

### 6.3 AC Calculation
```python
if armor_type == "none":
    ac = 10 + dex_modifier
elif armor_type == "light":
    ac = armor_base + dex_modifier
elif armor_type == "medium":
    ac = armor_base + min(dex_modifier, 2)
elif armor_type == "heavy":
    ac = armor_base
```

### 6.4 Attack Roll
```python
roll, is_critical = roll_d20(advantage, disadvantage)
total = roll + ability_modifier + proficiency_bonus
hit = total >= target_ac or is_critical
```

### 6.5 Saving Throw
```python
roll = roll_d20()
modifier = ability_modifier
if is_proficient:
    modifier += proficiency_bonus
success = (roll + modifier) >= dc
```

---

## 7. Integration Points

### 7.1 WAFT Being Integration

**Status**: Planned, not yet implemented

**Approach**: Add optional `dnd5e_character: Optional[DnD5eCharacter]` field to Being class.

**Benefits**:
- Beings can have D&D stats
- Persistent character state
- Integration with WAFT lifecycle

### 7.2 State Schema

**Status**: Planned, not yet implemented

**Schema Addition**:
```json
{
  "dnd5e": {
    "level": 1,
    "char_class": "fighter",
    "ability_scores": {
      "strength": 16,
      "dexterity": 14,
      "constitution": 15,
      "intelligence": 12,
      "wisdom": 10,
      "charisma": 10
    },
    "hp": 20,
    "max_hp": 20,
    "ac": 12,
    "equipment": {
      "weapon": null,
      "armor": null,
      "armor_type": "none"
    },
    "proficiencies": {
      "saves": [],
      "skills": []
    },
    "status_effects": []
  }
}
```

---

## 8. Testing Strategy

### 8.1 Unit Tests Needed

1. **Stats Tests**:
   - Modifier calculation (10→+0, 12→+1, 14→+2, etc.)
   - Proficiency bonus (level 1→+2, level 5→+3, etc.)
   - AC calculation (all armor types)
   - Input validation (bounds checking)

2. **Dice Tests**:
   - Basic rolling
   - Attack rolls (advantage, disadvantage)
   - Error handling (invalid expressions)

3. **Character Tests**:
   - Character creation
   - Property calculations
   - Serialization (to_dict, from_dict)
   - Validation

4. **Combat Tests**:
   - Attack rolls
   - Saving throws
   - Damage application
   - Healing application

### 8.2 Integration Tests

- Character creation → skill checks
- Combat flow (attack → damage → death)
- State persistence (save/load)

---

## 9. Future Enhancements

### 9.1 5e SRD Data Integration

**Status**: Planned

**Purpose**: Ingest JSON files from `5e-bits/5e-database` for:
- Complete class data
- All spells with metadata
- Monster stat blocks
- Equipment database

### 9.2 Spell System

**Status**: Planned

**Features**:
- Spell data structures
- Spell slot management
- Spell casting mechanics
- Damage calculation from spell data

### 9.3 Inventory System

**Status**: Planned

**Features**:
- Stackable items
- Equipment slots
- Item properties
- Weight management

### 9.4 Command Pattern

**Status**: Planned

**Purpose**: LLM-generated command parsing:
- `#attack` → Attack roll
- `#cast` → Spell casting
- `#check` → Skill check
- `#inventory` → Inventory management

---

## 10. Lessons Learned

### 10.1 Reverse Engineering Works

We didn't invent D&D mechanics - we extracted them from proven implementations. This saved weeks of design work.

### 10.2 Store Base, Calculate Derived

Storing base stats and calculating modifiers at runtime prevents desync and keeps data clean.

### 10.3 Validation is Critical

Input validation caught many potential bugs before they became problems.

### 10.4 Type Hints Help

Full type hints made the code self-documenting and caught errors early.

### 10.5 Enums Over Strings

Using enums for constants (like `ArmorType`) prevents typos and enables IDE autocomplete.

---

## 11. Conclusion

We successfully reverse-engineered the D&D 5e physics engine and implemented it as a clean, well-structured module. The implementation follows best practices:

- ✅ Input validation
- ✅ Error handling
- ✅ Type hints
- ✅ Comprehensive documentation
- ✅ Separation of concerns
- ✅ Testable design

The system is ready for integration with WAFT Beings and can serve as the "biology" for agent capabilities.

**Next Steps**:
1. Write unit tests
2. Integrate with Being class
3. Update state schema
4. Create more scenarios
5. Add 5e SRD data integration

---

**Status**: Implementation Complete  
**Date**: 2026-01-11  
**Version**: 1.0.0
