# AI-DnD Code Analysis - Key Findings for WAFT

**Repository**: ctavolazzi/AI-DnD  
**Analysis Date**: 2026-01-11  
**Purpose**: Extract algorithms and patterns for WAFT integration

---

## Architecture Overview

**Core Structure**:
- `pygame_mvp/game/` - Core game systems
- `pygame_mvp/ui/` - Pixel-based UI components
- `sentinel/` - Validation and world state management

**Key Files Analyzed**:
1. `game_state.py` - Centralized state management
2. `game_manager.py` - Game loop coordination
3. `stats_adapter.py` - D&D stat conversion (4→6 stats)
4. `save_system.py` - State persistence with checksums
5. `quests.py` - Objective-based quest tracking
6. `systems.py` - Character, combat, item systems

---

## Critical Algorithms Extracted

### 1. Stats Adapter (4 Stats → 6 Stats)

**File**: `pygame_mvp/game/stats_adapter.py`

**Problem Solved**: Game uses 4 stats (STR, DEX, INT, CON), D&D UI needs 6 (STR, DEX, CON, INT, WIS, CHA)

**Solution**:
```python
class StatsAdapter:
    CLASS_BASE_STATS = {
        CharacterClass.FIGHTER: {
            "str_bonus": 2,
            "wis_base": 10,
            "cha_base": 10,
        },
        # Derives WIS/CHA from class
    }
    
    def modifier(self, stat_value: int) -> int:
        return (stat_value - 10) // 2
```

**WAFT Integration**: ✅ **CRITICAL** - Use this pattern for WAFT's stat system

---

### 2. Game State Management

**File**: `pygame_mvp/game/game_state.py`

**Pattern**: Dataclass-based state with computed properties

```python
@dataclass
class CharacterState:
    hp: int
    max_hp: int
    
    @property
    def hp_percent(self) -> float:
        if self.max_hp <= 0:
            return 0.0
        return self.hp / self.max_hp
```

**WAFT Integration**: Use for WAFT Being state management

---

### 3. Inventory Stacking Algorithm

**File**: `pygame_mvp/game/game_state.py`

**Algorithm**:
1. Check if item with same name exists
2. Check if item is stackable
3. Increment quantity if stackable
4. Otherwise add new item if capacity allows

**WAFT Integration**: Use for inventory management

---

### 4. Save System with Integrity

**File**: `pygame_mvp/game/save_system.py`

**Features**:
- MD5 checksum for integrity
- Version tracking
- Backup system
- Metadata separation

**WAFT Integration**: Use for game state persistence

---

### 5. Quest Objective Tracking

**File**: `pygame_mvp/game/quests.py`

**Pattern**: Objective-based with progress calculation

```python
def update(self, count: int = 1) -> bool:
    self.current_count = min(self.current_count + count, self.required_count)
    if self.current_count >= self.required_count:
        self.completed = True
    return self.completed
```

**WAFT Integration**: Use for quest/work effort tracking

---

## Key Code Patterns

### Pattern 1: Equipment-Based Stat Aggregation

```python
@property
def total_stats(self) -> Stats:
    total = self.base_stats
    for item in self.equipment.values():
        if item:
            total += item.stats_bonus
    return total
```

**WAFT Integration**: Aggregate base stats + equipment bonuses

---

### Pattern 2: Class-Based Stat Derivation

```python
CLASS_BASE_STATS = {
    CharacterClass.FIGHTER: {"stats": Stats(14, 10, 8, 12), "hp": 30},
    CharacterClass.WIZARD: {"stats": Stats(6, 10, 16, 8), "hp": 18},
}
```

**WAFT Integration**: Define class templates for character creation

---

### Pattern 3: State Serialization

```python
@staticmethod
def serialize_character(character) -> dict:
    return {
        "name": character.name,
        "hp": character.hp,
        "max_hp": character.max_hp,
        # ... serialize all fields
    }
```

**WAFT Integration**: Use for Being state persistence

---

## Integration Priority

### HIGH Priority (Implement First)

1. **StatsAdapter** - Solves 4-stat to 6-stat problem
2. **Ability Modifier Calculation** - `(score - 10) // 2`
3. **Proficiency Bonus** - Level-based lookup
4. **AC Calculation** - Base 10 + modifiers

### MEDIUM Priority

5. **Save System** - State persistence
6. **Quest System** - Objective tracking
7. **Inventory System** - Stackable items

### LOW Priority (Reference)

8. **Pixel UI** - UI patterns (if needed)
9. **Image Generation** - API integration (if needed)

---

## Files to Study Further

1. `pygame_mvp/game/game_manager.py` - Main game loop
2. `pygame_mvp/game/pixel_game_manager.py` - UI integration
3. `pygame_mvp/game/tile_map.py` - Map system
4. `sentinel/validators/` - World state validation

---

**Status**: Code analysis complete. Ready for WAFT integration.
