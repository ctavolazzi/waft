# 5e-database Data Structure Analysis

**Repository**: 5e-bits/5e-database  
**Analysis Date**: 2026-01-11  
**Purpose**: Understand D&D 5e data structures for WAFT integration

---

## Overview

5e-database provides complete D&D 5e game data in JSON format. This is the **definitive reference** for D&D 5e data structures.

---

## Key Data Files

### 1. Classes (`5e-SRD-Classes.json`)

**Structure**:
```json
{
  "index": "barbarian",
  "name": "Barbarian",
  "hit_die": 12,
  "proficiency_choices": [...],
  "proficiencies": [...],
  "saving_throws": [{"index": "str"}],
  "starting_equipment": [...],
  "starting_equipment_options": [...]
}
```

**Key Fields**:
- `hit_die`: Used for HP calculation (d12 for Barbarian)
- `proficiency_choices`: Player choices during creation
- `saving_throws`: Which saves the class is proficient in
- `starting_equipment`: Default equipment

**WAFT Integration**:
- Use for character creation
- HP calculation: `hit_die + CON_modifier`
- Proficiency assignment

---

### 2. Spells (`5e-SRD-Spells.json`)

**Structure**:
```json
{
  "index": "acid-arrow",
  "name": "Acid Arrow",
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

**Key Fields**:
- `level`: Spell level (0-9)
- `damage_at_slot_level`: Damage scaling with slot level
- `dc`: Saving throw DC calculation
- `casting_time`: Action economy

**WAFT Integration**:
- Spell damage calculation
- DC calculation: `8 + proficiency + spellcasting_modifier`
- Action economy tracking

---

### 3. Monsters (`5e-SRD-Monsters.json`)

**Structure**:
```json
{
  "index": "aboleth",
  "name": "Aboleth",
  "armor_class": [{"type": "natural", "value": 17}],
  "hit_points": 135,
  "hit_dice": "18d10",
  "strength": 21,
  "proficiency_bonus": 4,
  "actions": [
    {
      "name": "Tentacle",
      "attack_bonus": 9,
      "damage": [{"damage_dice": "2d6+5"}]
    }
  ]
}
```

**Key Fields**:
- `armor_class`: AC calculation
- `hit_points`: Total HP
- `hit_dice`: HP calculation formula
- `actions`: Combat actions with attack bonuses
- `special_abilities`: Unique mechanics

**WAFT Integration**:
- NPC/enemy stat blocks
- Combat action definitions
- Attack bonus calculation

---

### 4. Equipment (`5e-SRD-Equipment.json`)

**Structure**: Items with properties, weights, values

**WAFT Integration**:
- Item database
- Equipment properties
- Weight and value tracking

---

## Data Access Patterns

### Installation Methods

**Option 1 - Docker** (Recommended):
```bash
docker run ghcr.io/5e-bits/5e-database:latest
```

**Option 2 - Local MongoDB**:
```bash
MONGODB_URI=mongodb://localhost/5e-database npm run db:refresh
```

**Option 3 - Direct JSON Access**:
- Clone repository
- Access JSON files directly from `src/2014/` or `src/2024/`

---

## WAFT Integration Strategy

### Phase 1: Data Loading

1. Clone 5e-database repository
2. Create data loaders for JSON files
3. Build Python classes from JSON structures
4. Cache loaded data

### Phase 2: Character Creation

1. Use Classes JSON for class selection
2. Use Races JSON for race selection
3. Use Backgrounds JSON for background
4. Calculate starting stats from class/race

### Phase 3: Game Mechanics

1. Use Spells JSON for spell system
2. Use Monsters JSON for NPCs/enemies
3. Use Equipment JSON for items
4. Use Rules JSON for game mechanics

---

## Key Algorithms from Data

### HP Calculation from Hit Die

**Formula**: `hit_die + CON_modifier` per level

**Level 1**: Always max (`hit_die + CON_modifier`)

**Level 2+**: Average roll `(hit_die / 2 + 1) + CON_modifier`

### Spell Damage Scaling

**Pattern**: Damage increases with slot level

**Example**: Acid Arrow
- Level 2 slot: 4d4 damage
- Level 3 slot: 5d4 damage
- Level 4 slot: 6d4 damage

### Attack Bonus Calculation

**Formula**: `proficiency_bonus + ability_modifier`

**Example**: Monster with STR 21, proficiency +4
- Attack bonus: `4 + 5 = 9` (STR 21 = +5 modifier)

---

**Status**: Data structure analysis complete. Ready for data integration.
