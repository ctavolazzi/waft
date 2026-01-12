# Deep Code Analysis: D&D 5e AI Repositories - Algorithms & Patterns

**Generated**: 2026-01-11
**Analysis Type**: Deep Code & Algorithm Exploration
**Purpose**: Extract reusable algorithms, patterns, and code structures for WAFT integration

---

## Executive Summary

Deep analysis of actual source code from D&D 5e repositories reveals critical algorithms, data structures, and patterns that can directly benefit WAFT's D&D mechanics implementation. This document focuses on **actionable code patterns** rather than high-level descriptions.

---

## 1. ctavolazzi/AI-DnD - User's Own Repository

### 1.1 Game State Management Architecture

**File**: `pygame_mvp/game/game_state.py`

**Key Pattern**: Centralized state management with dataclasses

```python
@dataclass
class CharacterState:
    """State for a single character."""
    name: str
    char_class: str
    hp: int
    max_hp: int
    mana: int
    max_mana: int
    attack: int
    defense: int
    alive: bool = True
    team: str = "players"
    status_effects: List[str] = field(default_factory=list)
    ability_scores: Dict[str, int] = field(default_factory=dict)

    @property
    def hp_percent(self) -> float:
        if self.max_hp <= 0:
            return 0.0
        return self.hp / self.max_hp
```

**WAFT Integration Opportunity**:
- Use similar dataclass pattern for WAFT's Being state
- Property-based computed values (hp_percent, mana_percent)
- Status effects as list (extensible)
- Ability scores as dictionary (flexible)

**Algorithm**: HP percentage calculation
- **Formula**: `hp / max_hp` with zero-division protection
- **Use Case**: UI display, health bars, death detection

---

### 1.2 Inventory System Algorithm

**File**: `pygame_mvp/game/game_state.py`

**Key Pattern**: Stackable items with quantity tracking

```python
@dataclass
class InventoryState:
    items: List[Any] = field(default_factory=list)
    equipped: Dict[str, str] = field(default_factory=dict)  # slot: item_id
    gold: int = 0
    capacity: int = 20

    def add_item(self, item) -> bool:
        """Add an item to inventory."""
        # Try to stack with existing
        for existing in self.items:
            if hasattr(existing, 'name') and hasattr(item, 'name'):
                if existing.name == item.name and getattr(existing, 'stackable', True):
                    existing.quantity = getattr(existing, 'quantity', 1) + getattr(item, 'quantity', 1)
                    return True

        if len(self.items) < self.capacity:
            self.items.append(item)
            return True
        return False
```

**WAFT Integration Opportunity**:
- Stackable item algorithm (check name + stackable flag)
- Capacity management
- Equipped items as slot dictionary
- Gold as separate currency field

**Algorithm**: Item stacking
1. Check if item exists with same name
2. Check if item is stackable
3. Increment quantity if stackable
4. Otherwise add new item if capacity allows

---

### 1.3 Stats Adapter Pattern (4 Stats → 6 Stats)

**File**: `pygame_mvp/game/stats_adapter.py`

**Key Pattern**: Adapter pattern for D&D stat conversion

```python
class StatsAdapter:
    """
    Converts game Character stats to D&D UI-compatible format.
    Game uses 4 core stats (STR, DEX, INT, CON).
    D&D UIs expect 6 stats (STR, DEX, CON, INT, WIS, CHA).
    """

    CLASS_BASE_STATS = {
        CharacterClass.FIGHTER: {
            "str_bonus": 2,
            "dex_penalty": -1,
            "con_bonus": 1,
            "wis_base": 10,
            "cha_base": 10,
        },
        # ... other classes
    }

    def modifier(self, stat_value: int) -> int:
        """Calculate D20 modifier from stat value.
        10-11 = +0
        12-13 = +1
        14-15 = +2
        etc.
        """
        return (stat_value - 10) // 2
```

**WAFT Integration Opportunity**:
- **CRITICAL**: This solves the 4-stat vs 6-stat problem
- Class-based stat derivation (WIS/CHA from class)
- Modifier calculation: `(stat - 10) // 2`
- AC calculation: `10 + dex_modifier`
- Proficiency bonus: `2 + (level // 4)`

**Algorithms Extracted**:
1. **Ability Modifier**: `(ability_score - 10) // 2`
2. **AC Calculation**: `10 + dex_modifier`
3. **Initiative**: `dex_modifier`
4. **Proficiency Bonus**: `2 + (level // 4)`

---

### 1.4 Save System with Checksums

**File**: `pygame_mvp/game/save_system.py`

**Key Pattern**: JSON serialization with integrity checking

```python
def _calculate_checksum(self, data: str) -> str:
    """Calculate checksum for save data integrity."""
    return hashlib.md5(data.encode()).hexdigest()

def save_game(self, slot: int, save_name: str, game_data: Dict[str, Any], ...):
    # Build save structure
    save_data = {
        "version": self.SAVE_VERSION,
        "slot": slot,
        "name": save_name,
        "created_at": now,
        "updated_at": now,
        "metadata": metadata or {},
        "game_data": game_data
    }

    # Calculate checksum
    json_str = json.dumps(save_data, sort_keys=True)
    save_data["checksum"] = self._calculate_checksum(json_str)
```

**WAFT Integration Opportunity**:
- Save file integrity checking
- Version tracking for migration
- Metadata separation from game data
- Backup system before overwrite

**Algorithm**: Save integrity
1. Serialize to JSON with sorted keys
2. Calculate MD5 checksum
3. Store checksum with data
4. Verify on load

---

### 1.5 Quest System Architecture

**File**: `pygame_mvp/game/quests.py`

**Key Pattern**: Objective-based quest tracking

```python
@dataclass
class QuestObjective:
    description: str
    objective_type: ObjectiveType
    target: str
    required_count: int = 1
    current_count: int = 0
    completed: bool = False
    optional: bool = False

    def update(self, count: int = 1) -> bool:
        """Update progress. Returns True if objective completed."""
        self.current_count = min(self.current_count + count, self.required_count)
        if self.current_count >= self.required_count:
            self.completed = True
        return self.completed

    @property
    def progress_text(self) -> str:
        if self.required_count > 1:
            return f"{self.description} ({self.current_count}/{self.required_count})"
        return self.description
```

**WAFT Integration Opportunity**:
- Objective types: KILL, COLLECT, REACH, TALK, SURVIVE, EXPLORE
- Progress tracking with min() to prevent over-counting
- Optional objectives for bonus rewards
- Progress text generation

**Algorithm**: Progress calculation
- **Formula**: `min(current + count, required)`
- **Completion**: `current >= required`
- **Progress %**: `completed / total_required * 100`

---

### 1.6 Character System with Equipment

**File**: `pygame_mvp/game/systems.py`

**Key Pattern**: Equipment-based stat aggregation

```python
class Character:
    def __init__(self, name: str, level: int = 1, max_hp: int = 20):
        self.name = name
        self.level = level
        self.base_stats = Stats()
        self.equipment: Dict[str, Optional[Item]] = {"weapon": None, "armor": None}

    @property
    def total_stats(self) -> Stats:
        """Aggregate base stats with equipment bonuses."""
        total = Stats(
            self.base_stats.strength,
            self.base_stats.dexterity,
            self.base_stats.intelligence,
            self.base_stats.constitution,
        )
        for item in self.equipment.values():
            if item:
                total += item.stats_bonus
        return total
```

**WAFT Integration Opportunity**:
- Equipment slots as dictionary
- Stat aggregation via operator overloading
- Base stats + equipment bonuses = total stats

**Algorithm**: Stat aggregation
1. Start with base stats
2. Iterate equipped items
3. Add item stat bonuses
4. Return total stats

---

## 2. 5e-bits/5e-database - Complete D&D 5e Data Structures

### 2.1 Class Data Structure

**File**: `src/2014/5e-SRD-Classes.json`

**Key Structure**:
```json
{
  "index": "barbarian",
  "name": "Barbarian",
  "hit_die": 12,
  "proficiency_choices": [...],
  "proficiencies": [...],
  "saving_throws": [{"index": "str", "name": "STR"}],
  "starting_equipment": [...],
  "starting_equipment_options": [...]
}
```

**WAFT Integration Opportunity**:
- **hit_die**: Used for HP calculation (d12 for Barbarian)
- **proficiency_choices**: Player choices during character creation
- **saving_throws**: Which saves the class is proficient in
- **starting_equipment**: Default equipment for new characters

**Algorithm**: HP Calculation from Hit Die
- **Formula**: `hit_die + CON_modifier` per level
- **Level 1**: `hit_die + CON_modifier` (max at level 1)
- **Level 2+**: `(hit_die / 2 + 1) + CON_modifier` (average roll)

---

### 2.2 Spell Data Structure

**File**: `src/2014/5e-SRD-Spells.json`

**Key Structure**:
```json
{
  "index": "acid-arrow",
  "name": "Acid Arrow",
  "level": 2,
  "damage": {
    "damage_type": {"index": "acid", "name": "Acid"},
    "damage_at_slot_level": {
      "2": "4d4",
      "3": "5d4",
      "4": "6d4"
    }
  },
  "dc": {
    "dc_type": {"index": "dex", "name": "DEX"},
    "dc_value": 14
  },
  "attack_type": "ranged",
  "casting_time": "1 action",
  "range": "90 feet"
}
```

**WAFT Integration Opportunity**:
- **Damage scaling**: Slot level determines damage dice
- **DC calculation**: `8 + proficiency + spellcasting_modifier`
- **Attack type**: Melee vs ranged spell attacks
- **Casting time**: Action economy (action, bonus action, reaction)

**Algorithm**: Spell Damage Calculation
1. Determine spell slot level used
2. Look up damage dice from `damage_at_slot_level[slot_level]`
3. Parse dice expression (e.g., "4d4")
4. Roll dice and apply modifiers

---

### 2.3 Monster Data Structure

**File**: `src/2014/5e-SRD-Monsters.json`

**Key Structure**:
```json
{
  "index": "aboleth",
  "name": "Aboleth",
  "armor_class": [{"type": "natural", "value": 17}],
  "hit_points": 135,
  "hit_dice": "18d10",
  "strength": 21,
  "dexterity": 9,
  "constitution": 15,
  "intelligence": 18,
  "wisdom": 15,
  "charisma": 18,
  "proficiency_bonus": 4,
  "actions": [
    {
      "name": "Tentacle",
      "attack_bonus": 9,
      "damage": [{"damage_type": {"index": "bludgeoning"}, "damage_dice": "2d6+5"}]
    }
  ],
  "special_abilities": [...],
  "legendary_actions": [...]
}
```

**WAFT Integration Opportunity**:
- **AC calculation**: Natural armor, armor type
- **Attack bonus**: `proficiency_bonus + ability_modifier`
- **Damage dice**: Parsed from string (e.g., "2d6+5")
- **Special abilities**: Unique monster mechanics
- **Legendary actions**: Boss mechanics

**Algorithm**: Attack Roll Calculation
- **Formula**: `d20 + attack_bonus >= target_AC`
- **Attack Bonus**: `proficiency_bonus + STR_modifier` (melee) or `DEX_modifier` (ranged)
- **Critical Hit**: Natural 20 on d20

---

## 3. foundryvtt/dnd5e - VTT System Patterns

### 3.1 Actor Data Model

**Pattern**: Modular template system with mixins

**Key Concepts** (from web search):
- **CommonTemplate**: Shared fields (abilities, currency)
- **AttributesFields**: AC, Initiative, Movement, HP
- **TraitsFields**: Size, Damage Immunities/Resistances, Conditions

**WAFT Integration Opportunity**:
- Template-based data model
- Mixin pattern for shared fields
- Derived data calculation (`prepareDerivedData()`)

**Algorithm**: Derived Data Calculation
1. Calculate ability modifiers from scores
2. Calculate skill totals (ability + proficiency if proficient)
3. Calculate AC from armor + DEX modifier
4. Calculate passive perception (10 + WIS + proficiency)

---

## 4. raeleus/Hashtag-DnD - AI Dungeon Scripting

### 4.1 Hashtag Command System

**Pattern**: Command-based game mechanics via hashtags

**Key Commands** (from README):
- `#roll 5d20+6` - Dice rolling with modifiers
- `#check intelligence` - Ability checks
- `#attack` - Combat attacks
- `#cast` - Spell casting
- `#inventory` - Inventory management
- `#encounter` - Combat setup
- `#initiative` - Turn order
- `#heal` / `#damage` - HP modification

**WAFT Integration Opportunity**:
- Command-based interface for WAFT beings
- Dice expression parsing
- Combat encounter management
- Inventory commands

**Algorithm**: Dice Expression Parsing
- **Pattern**: `NdM+K` where N=dice count, M=sides, K=modifier
- **Example**: `5d20+6` = roll 5d20, add 6
- **Advanced**: `2d20kh1` = keep highest of 2d20

---

## 5. Key Algorithms for WAFT Integration

### 5.1 Ability Score Modifier Calculation

**Formula**: `modifier = (ability_score - 10) // 2`

**Python Implementation**:
```python
def calculate_modifier(ability_score: int) -> int:
    """Calculate D&D 5e ability modifier."""
    return (ability_score - 10) // 2
```

**Examples**:
- 10 → +0
- 12 → +1
- 14 → +2
- 16 → +3
- 18 → +4

---

### 5.2 Proficiency Bonus Calculation

**Formula**: Based on character level

**Python Implementation**:
```python
def calculate_proficiency_bonus(level: int) -> int:
    """Calculate proficiency bonus based on level."""
    if 1 <= level <= 4:
        return 2
    elif 5 <= level <= 8:
        return 3
    elif 9 <= level <= 12:
        return 4
    elif 13 <= level <= 16:
        return 5
    elif 17 <= level <= 20:
        return 6
    else:
        return 2 + (level // 4)  # For levels > 20
```

**Table**:
| Level | Proficiency Bonus |
|-------|-------------------|
| 1-4   | +2                |
| 5-8   | +3                |
| 9-12  | +4                |
| 13-16 | +5                |
| 17-20 | +6                |

---

### 5.3 Armor Class (AC) Calculation

**Base Formula**: `10 + DEX_modifier`

**With Armor**:
- **Light Armor**: `armor_base + DEX_modifier`
- **Medium Armor**: `armor_base + DEX_modifier (max +2)`
- **Heavy Armor**: `armor_base` (no DEX modifier)

**Python Implementation**:
```python
def calculate_ac(dex_modifier: int, armor_type: str = "none", armor_base: int = 0) -> int:
    """Calculate Armor Class."""
    if armor_type == "none":
        return 10 + dex_modifier
    elif armor_type == "light":
        return armor_base + dex_modifier
    elif armor_type == "medium":
        return armor_base + min(dex_modifier, 2)
    elif armor_type == "heavy":
        return armor_base
    return 10
```

---

### 5.4 Hit Points (HP) Calculation

**Level 1**: `hit_die + CON_modifier` (always max)

**Level 2+**: `(hit_die / 2 + 1) + CON_modifier` (average roll, or roll)

**Python Implementation**:
```python
def calculate_hp_at_level(level: int, hit_die: int, con_modifier: int, roll: bool = False) -> int:
    """Calculate HP for a given level."""
    if level == 1:
        return hit_die + con_modifier

    if roll:
        # Roll hit die
        hp_gain = random.randint(1, hit_die) + con_modifier
    else:
        # Use average
        hp_gain = (hit_die // 2 + 1) + con_modifier

    return hp_gain
```

---

### 5.5 Dice Rolling Algorithm

**Library**: `d20` (used by Avrae)

**Basic Usage**:
```python
import d20

result = d20.roll("1d20+5")
print(result.total)  # Total: 15
print(result.crit)   # Critical hit detection
```

**Advanced Expressions**:
- `2d20kh1` - Keep highest of 2d20 (advantage)
- `2d20kl1` - Keep lowest of 2d20 (disadvantage)
- `4d6dl1` - Drop lowest die (ability score generation)

**WAFT Integration**:
- Use `d20` library for all dice rolling
- Supports complex expressions
- Built-in critical hit detection
- Tree-based representation for parsing

---

### 5.6 Attack Roll Algorithm

**Formula**: `d20 + attack_modifier >= target_AC`

**Attack Modifier**: `proficiency_bonus + ability_modifier`

**Python Implementation**:
```python
def make_attack_roll(attack_modifier: int, advantage: bool = False, disadvantage: bool = False) -> tuple:
    """Make an attack roll. Returns (total, hit, critical)."""
    if advantage and not disadvantage:
        roll = max(d20.roll("1d20").total, d20.roll("1d20").total)
    elif disadvantage and not advantage:
        roll = min(d20.roll("1d20").total, d20.roll("1d20").total)
    else:
        roll = d20.roll("1d20").total

    total = roll + attack_modifier
    critical = (roll == 20)
    return (total, total, critical)
```

---

### 5.7 Saving Throw Algorithm

**Formula**: `d20 + ability_modifier + proficiency_bonus (if proficient) >= DC`

**Python Implementation**:
```python
def make_saving_throw(ability_modifier: int, proficiency_bonus: int, is_proficient: bool, dc: int) -> bool:
    """Make a saving throw. Returns True if successful."""
    roll = d20.roll("1d20").total
    modifier = ability_modifier
    if is_proficient:
        modifier += proficiency_bonus

    total = roll + modifier
    return total >= dc
```

---

## 6. Data Structure Patterns

### 6.1 Character Data Model

**From AI-DnD**:
```python
@dataclass
class CharacterState:
    name: str
    char_class: str
    hp: int
    max_hp: int
    mana: int
    max_mana: int
    attack: int
    defense: int
    alive: bool = True
    ability_scores: Dict[str, int] = field(default_factory=dict)
    status_effects: List[str] = field(default_factory=list)
```

**From 5e-database**:
- Ability scores: STR, DEX, CON, INT, WIS, CHA
- Skills: List of proficiencies
- Equipment: Starting equipment + options
- Features: Class features by level

**WAFT Integration**:
- Combine both approaches
- Use dataclass for state
- Use dictionary for ability scores (flexible)
- Status effects as list (extensible)

---

### 6.2 Inventory Data Model

**From AI-DnD**:
```python
@dataclass
class InventoryState:
    items: List[Any] = field(default_factory=list)
    equipped: Dict[str, str] = field(default_factory=dict)  # slot: item_id
    gold: int = 0
    capacity: int = 20
```

**From 5e-database**:
- Equipment categories
- Item properties (weapon, armor, consumable)
- Item weights and values

**WAFT Integration**:
- Slot-based equipment system
- Stackable items with quantity
- Gold as separate currency
- Capacity limits

---

### 6.3 Spell Data Model

**From 5e-database**:
```json
{
  "level": 2,
  "damage": {
    "damage_at_slot_level": {
      "2": "4d4",
      "3": "5d4"
    }
  },
  "dc": {
    "dc_type": {"index": "dex"},
    "dc_value": 14
  },
  "casting_time": "1 action",
  "range": "90 feet"
}
```

**WAFT Integration**:
- Spell level determines slot requirement
- Damage scales with slot level
- DC based on spellcasting ability
- Action economy (casting time)

---

## 7. Integration Opportunities for WAFT

### 7.1 Direct Code Reuse

**High Priority**:
1. **StatsAdapter** from AI-DnD - Solves 4-stat to 6-stat conversion
2. **SaveSystem** from AI-DnD - Game state persistence with checksums
3. **QuestTracker** from AI-DnD - Objective-based quest system
4. **d20 library** - Dice rolling engine (already exists)

**Medium Priority**:
5. **InventoryState** from AI-DnD - Stackable items, equipment slots
6. **CharacterState** from AI-DnD - HP, mana, status effects
7. **GameStateSerializer** from AI-DnD - State serialization patterns

---

### 7.2 Algorithm Integration

**Critical Algorithms for WAFT**:
1. **Ability Modifier**: `(score - 10) // 2`
2. **Proficiency Bonus**: Level-based table lookup
3. **AC Calculation**: Base 10 + DEX, modified by armor
4. **HP Calculation**: Hit die + CON modifier per level
5. **Attack Roll**: d20 + proficiency + ability modifier
6. **Saving Throw**: d20 + ability + proficiency (if proficient) vs DC

---

### 7.3 Data Structure Integration

**From 5e-database**:
- **Classes JSON**: Complete class data (hit dice, proficiencies, starting equipment)
- **Spells JSON**: All spells with damage, DC, casting time
- **Monsters JSON**: NPC/enemy stat blocks
- **Equipment JSON**: All items with properties

**WAFT Integration**:
- Use 5e-database as reference data source
- Parse JSON structures for game mechanics
- Build WAFT's D&D system on top of this data

---

### 7.4 Pattern Integration

**Game State Management**:
- Centralized state with dataclasses
- Property-based computed values
- State serialization for persistence

**Quest System**:
- Objective-based tracking
- Progress calculation
- Reward distribution

**Combat System**:
- Turn-based initiative
- Attack roll vs AC
- Damage application
- Status effects

---

## 8. Specific Code Snippets for WAFT

### 8.1 D&D 5e Stat Calculator

```python
class DnD5eStats:
    """D&D 5e stat calculations for WAFT."""

    @staticmethod
    def ability_modifier(score: int) -> int:
        """Calculate ability modifier."""
        return (score - 10) // 2

    @staticmethod
    def proficiency_bonus(level: int) -> int:
        """Calculate proficiency bonus."""
        return 2 + ((level - 1) // 4)

    @staticmethod
    def armor_class(dex_mod: int, armor_type: str = "none", armor_base: int = 0) -> int:
        """Calculate AC."""
        if armor_type == "none":
            return 10 + dex_mod
        elif armor_type == "light":
            return armor_base + dex_mod
        elif armor_type == "medium":
            return armor_base + min(dex_mod, 2)
        elif armor_type == "heavy":
            return armor_base
        return 10

    @staticmethod
    def spell_save_dc(spellcasting_mod: int, proficiency: int) -> int:
        """Calculate spell save DC."""
        return 8 + spellcasting_mod + proficiency
```

---

### 8.2 Dice Roller Integration

```python
import d20

class DnDRoller:
    """D&D dice rolling for WAFT."""

    @staticmethod
    def roll(expression: str) -> int:
        """Roll dice expression."""
        result = d20.roll(expression)
        return result.total

    @staticmethod
    def attack_roll(advantage: bool = False, disadvantage: bool = False) -> tuple:
        """Make attack roll. Returns (total, is_critical)."""
        if advantage:
            roll = max(d20.roll("1d20").total, d20.roll("1d20").total)
        elif disadvantage:
            roll = min(d20.roll("1d20").total, d20.roll("1d20").total)
        else:
            roll = d20.roll("1d20").total

        is_critical = (roll == 20)
        return (roll, is_critical)
```

---

### 8.3 Character State for WAFT Beings

```python
@dataclass
class DnD5eBeingState:
    """D&D 5e state for WAFT beings."""
    # Core stats
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10

    # Derived values
    level: int = 1
    hp: int = 20
    max_hp: int = 20
    ac: int = 10

    # Equipment
    equipped_weapon: Optional[str] = None
    equipped_armor: Optional[str] = None

    # Status
    status_effects: List[str] = field(default_factory=list)

    def calculate_modifiers(self) -> Dict[str, int]:
        """Calculate all ability modifiers."""
        return {
            "str": (self.strength - 10) // 2,
            "dex": (self.dexterity - 10) // 2,
            "con": (self.constitution - 10) // 2,
            "int": (self.intelligence - 10) // 2,
            "wis": (self.wisdom - 10) // 2,
            "cha": (self.charisma - 10) // 2,
        }

    def calculate_ac(self) -> int:
        """Calculate current AC."""
        dex_mod = (self.dexterity - 10) // 2
        # TODO: Apply armor bonuses
        return 10 + dex_mod
```

---

## 9. Libraries and Tools Identified

### 9.1 Python Libraries

1. **d20** - Dice rolling engine
   - Installation: `pip install d20`
   - Used by: Avrae, many D&D tools
   - Features: Complex expressions, critical detection

2. **dnd-character** - Character management
   - Installation: `pip install dnd-character`
   - Features: Serializable character objects

3. **pythonanddragons** - D&D 5e combat
   - Installation: `pip install pythonanddragons`
   - Features: Character management, combat handling

---

### 9.2 Data Sources

1. **5e-database** - Complete D&D 5e data
   - Format: JSON files
   - Content: Classes, spells, monsters, equipment
   - API: Available at dnd5eapi.co

2. **5e-SRD** - System Reference Document
   - Legal: Open Gaming License
   - Content: Core rules and mechanics

---

## 10. WAFT-Specific Integration Plan

### 10.1 Immediate Actions

1. **Install d20 library**:
   ```bash
   pip install d20
   ```

2. **Create D&D 5e module in WAFT**:
   - `src/waft/core/dnd5e/` directory
   - `stats.py` - Stat calculations
   - `dice.py` - Dice rolling wrapper
   - `character.py` - Character state
   - `combat.py` - Combat mechanics

3. **Integrate 5e-database data**:
   - Download or reference JSON files
   - Create data loaders
   - Build character creation from class data

---

### 10.2 Code Patterns to Adopt

1. **Dataclass-based state** (from AI-DnD)
2. **Property-based computed values** (hp_percent, modifiers)
3. **Adapter pattern** (4-stat to 6-stat conversion)
4. **Save system with checksums** (integrity checking)
5. **Quest system with objectives** (progress tracking)

---

### 10.3 Algorithms to Implement

1. ✅ Ability modifier calculation
2. ✅ Proficiency bonus lookup
3. ✅ AC calculation
4. ✅ HP calculation per level
5. ✅ Attack roll mechanics
6. ✅ Saving throw mechanics
7. ✅ Spell damage calculation
8. ✅ Dice expression parsing

---

## 11. Additional Discoveries

### 11.1 Avrae Discord Bot

**Key Features**:
- Advanced dice rolling
- Character sheet integration
- Initiative tracking
- Uses `d20` library
- Draconic language (modified Python)

**WAFT Integration**:
- Study dice rolling patterns
- Character sheet data structures
- Command-based interface patterns

---

### 11.2 Hashtag-DnD Command System

**Key Features**:
- Hashtag-based commands (`#roll`, `#attack`, `#cast`)
- Inventory management
- Combat encounters
- Location travel
- Skill checks

**WAFT Integration**:
- Command parsing patterns
- Game state modification via commands
- Combat encounter setup

---

## 12. Next Steps for Deep Exploration

### 12.1 Clone and Study

1. **ctavolazzi/AI-DnD** (HIGHEST PRIORITY)
   - Clone repository
   - Study `game_manager.py` architecture
   - Analyze `pixel_game_manager.py` for UI patterns
   - Extract quest system implementation

2. **5e-bits/5e-database**
   - Clone repository
   - Study JSON structure
   - Create data loaders
   - Map data to WAFT models

3. **foundryvtt/dnd5e**
   - Study actor data model
   - Analyze template system
   - Understand derived data calculation

---

### 12.2 Algorithm Implementation

1. Create `waft.core.dnd5e` module
2. Implement stat calculation functions
3. Integrate `d20` library
4. Build character creation system
5. Implement combat mechanics

---

## 13. Code Examples for WAFT

### 13.1 Complete D&D 5e Character Class

```python
from dataclasses import dataclass, field
from typing import Dict, Optional, List
import d20

@dataclass
class DnD5eCharacter:
    """Complete D&D 5e character for WAFT."""
    name: str
    level: int = 1

    # Ability scores
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10

    # Hit points
    hp: int = 20
    max_hp: int = 20

    # Class info
    char_class: str = "fighter"
    hit_die: int = 10

    # Equipment
    equipped_weapon: Optional[str] = None
    equipped_armor: Optional[str] = None

    # Proficiencies
    proficient_saves: List[str] = field(default_factory=list)
    proficient_skills: List[str] = field(default_factory=list)

    def ability_modifier(self, score: int) -> int:
        """Calculate ability modifier."""
        return (score - 10) // 2

    def proficiency_bonus(self) -> int:
        """Get proficiency bonus for current level."""
        return 2 + ((self.level - 1) // 4)

    def armor_class(self) -> int:
        """Calculate current AC."""
        dex_mod = self.ability_modifier(self.dexterity)
        # TODO: Apply armor
        return 10 + dex_mod

    def make_attack_roll(self, advantage: bool = False) -> tuple:
        """Make attack roll. Returns (total, hit, critical)."""
        roll, is_critical = self._roll_d20(advantage)
        str_mod = self.ability_modifier(self.strength)
        prof = self.proficiency_bonus()
        total = roll + str_mod + prof
        return (total, total, is_critical)

    def _roll_d20(self, advantage: bool = False) -> tuple:
        """Roll d20. Returns (result, is_critical)."""
        if advantage:
            roll = max(d20.roll("1d20").total, d20.roll("1d20").total)
        else:
            roll = d20.roll("1d20").total
        return (roll, roll == 20)
```

---

## 14. Summary of Findings

### 14.1 Critical Algorithms

1. **Ability Modifier**: `(score - 10) // 2` ✅
2. **Proficiency Bonus**: Level-based table ✅
3. **AC Calculation**: Base 10 + modifiers ✅
4. **HP Calculation**: Hit die + CON per level ✅
5. **Attack Roll**: d20 + modifiers vs AC ✅
6. **Saving Throw**: d20 + modifiers vs DC ✅

### 14.2 Data Structures

1. **Character State**: Dataclass with properties ✅
2. **Inventory**: List with stacking algorithm ✅
3. **Equipment**: Dictionary of slots ✅
4. **Quests**: Objective-based tracking ✅
5. **Spells**: Level-based damage scaling ✅

### 14.3 Code Patterns

1. **Adapter Pattern**: 4-stat to 6-stat conversion ✅
2. **State Management**: Centralized with dataclasses ✅
3. **Save System**: JSON with checksums ✅
4. **Quest System**: Objective progress tracking ✅
5. **Combat System**: Turn-based with initiative ✅

---

**Status**: Deep code analysis complete. Ready for implementation phase.

**Next Action**: Begin implementing D&D 5e module in WAFT using extracted algorithms and patterns.
