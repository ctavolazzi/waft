---
name: D&D 5e Character Rules Integration
overview: Transform the gamification system to use D&D 5e character mechanics, mapping existing stats (Integrity, Insight, Level) to D&D concepts (HP, XP, Level) and adding ability scores, modifiers, proficiency bonus, and D&D-style stat displays.
todos:
  - id: dnd-1
    content: Add ability scores (STR, DEX, CON, INT, WIS, CHA) to GamificationManager data structure and methods
    status: pending
  - id: dnd-2
    content: "Implement ability modifier calculation: (Score - 10) / 2 rounded down"
    status: pending
    dependencies:
      - dnd-1
  - id: dnd-3
    content: "Implement proficiency bonus calculation based on level (D&D 5e standard: +2 at 1-4, +3 at 5-8, etc.)"
    status: pending
    dependencies:
      - dnd-1
  - id: dnd-4
    content: "Map Integrity to HP: Max HP = 8 + CON mod + (Level-1) * (4 + CON mod), Current HP = Max HP * (Integrity/100)"
    status: pending
    dependencies:
      - dnd-1
      - dnd-2
  - id: dnd-5
    content: Update waft stats command to display D&D ability scores, modifiers, HP, proficiency bonus
    status: pending
    dependencies:
      - dnd-1
      - dnd-2
      - dnd-3
      - dnd-4
  - id: dnd-6
    content: Update waft level command to show D&D level progression and XP thresholds
    status: pending
    dependencies:
      - dnd-4
  - id: dnd-7
    content: Add data migration logic to initialize ability scores for existing projects (default to 8 or derive from stats)
    status: pending
    dependencies:
      - dnd-1
  - id: dnd-8
    content: Update tests to cover D&D mechanics (ability scores, modifiers, HP, proficiency)
    status: pending
    dependencies:
      - dnd-1
      - dnd-2
      - dnd-3
      - dnd-4
---

# D&D 5e Character Rules Integration Plan

## Objective

Transform the gamification system to use D&D 5e character mechanics, enabling the CLI to display and track development progress using D&D 5e rules as the character progresses.

## Current System Analysis

**Existing Stats:**

- **Integrity** (0-100%): Structural stability → Maps to **Hit Points (HP)**
- **Insight** (accumulated): Verified knowledge → Maps to **Experience Points (XP)**
- **Level** (calculated from Insight): Current level → Maps to **D&D Level**
- **Achievements**: Unlocked badges

**Current Display:**

- `waft stats` - Shows Integrity, Insight, Level, Achievements
- `waft level` - Shows level details and progress
- `waft dashboard` - HUD with integrity bar

## D&D 5e Mechanics to Add

### 1. Ability Scores (Core Stats)

Add 6 ability scores that represent different aspects of development:

- **Strength (STR)**: Code quality, robustness, structural integrity
- **Dexterity (DEX)**: Speed, efficiency, quick fixes
- **Constitution (CON)**: Project health, resilience, stability
- **Intelligence (INT)**: Problem-solving, architecture, design
- **Wisdom (WIS)**: Best practices, patterns, experience
- **Charisma (CHA)**: Documentation quality, communication, clarity

**Initial Values**: Start at 8 (D&D standard) or derive from current stats

**Range**: 1-20 (D&D standard)

**Improvement**: Increase on level up or through achievements

### 2. Ability Modifiers

Calculate modifiers from ability scores: `(Score - 10) / 2` (rounded down)**Example**: STR 15 → +2 modifier, STR 8 → -1 modifier

### 3. Proficiency Bonus

Based on level (D&D 5e standard):

- Level 1-4: +2
- Level 5-8: +3
- Level 9-12: +4
- Level 13-16: +5
- Level 17-20: +6

### 4. Hit Points (HP)

Map Integrity to HP:

- **Max HP**: `8 + CON modifier + (Level - 1) * (4 + CON modifier)`
- **Current HP**: `Max HP * (Integrity / 100)`
- **Hit Dice**: d8 (standard for many classes)

### 5. Experience Points (XP)

Map Insight to XP:

- Use Insight value directly as XP
- D&D level thresholds can be used for level calculation
- Or keep current `Level = sqrt(Insight / 100) + 1` formula

### 6. Skills (Optional)

Derive skills from ability scores + proficiency:

- **Code Quality** (STR + proficiency)
- **Performance** (DEX + proficiency)
- **Maintainability** (CON + proficiency)
- **Architecture** (INT + proficiency)
- **Best Practices** (WIS + proficiency)
- **Documentation** (CHA + proficiency)

### 7. Saving Throws

Based on ability scores + proficiency (if proficient):

- **Code Quality Save** (STR)
- **Performance Save** (DEX)
- **Stability Save** (CON)
- **Architecture Save** (INT)
- **Pattern Save** (WIS)
- **Clarity Save** (CHA)

## Implementation Plan

### Phase 1: Core D&D Stats (Ability Scores)

**File**: `src/waft/core/gamification.py`

1. **Add ability scores to data structure**:
   ```python
      "ability_scores": {
          "strength": 8,
          "dexterity": 8,
          "constitution": 8,
          "intelligence": 8,
          "wisdom": 8,
          "charisma": 8
      }
   ```




2. **Add methods**:

- `get_ability_score(ability: str) -> int`

- `set_ability_score(ability: str, value: int) -> None`

- `get_ability_modifier(ability: str) -> int`

- `get_proficiency_bonus() -> int`

3. **Initialize ability scores**:

- Option 1: All start at 8 (standard D&D)

- Option 2: Derive from current stats (e.g., CON from Integrity, INT from Insight)

- Option 3: User-configurable starting values

### Phase 2: HP and XP Mapping

1. **Add HP calculation**:

   ```python
      def get_max_hp(self) -> int:
          """Calculate max HP from CON and level."""
          con_mod = self.get_ability_modifier("constitution")
          base_hp = 8 + con_mod
          level_hp = (self.level - 1) * (4 + con_mod)
          return max(1, base_hp + level_hp)
      
      def get_current_hp(self) -> int:
          """Calculate current HP from Integrity."""
          max_hp = self.get_max_hp()
          return int(max_hp * (self.integrity / 100.0))
   ```



2. **Add XP tracking**:

- Use Insight as XP directly

- Or add separate XP field that tracks alongside Insight

### Phase 3: CLI Display Updates

**File**: `src/waft/main.py`

1. **Update `waft stats` command**:

- Show D&D ability scores with modifiers

- Show HP (current/max) instead of just Integrity %

- Show XP (Insight) and XP to next level

- Show Proficiency Bonus

- Show Level with D&D progression

2. **Update `waft level` command**:

- Show D&D level progression

- Show XP thresholds for next levels

- Show ability score improvements on level up

3. **Add `waft character` command** (optional):

- Full character sheet display

- Ability scores, modifiers, skills, saving throws

- HP, AC (if we add it), proficiency bonus

4. **Update `waft dashboard`**:

- Show HP bar instead of/in addition to Integrity bar

- Show ability score indicators

### Phase 4: Configuration

**File**: `src/waft/core/gamification.py`

1. **Add D&D mode toggle**:

   ```python
      "dnd_mode": True  # Enable D&D 5e rules
   ```



2. **Migration logic**:

- If existing data, initialize ability scores from current stats

- Preserve Integrity/Insight for backward compatibility

- Calculate HP from Integrity

### Phase 5: Level Up Improvements

1. **Ability Score Improvements**:

- On level up (every 4 levels in D&D), allow ability score increase

- Or automatically improve based on achievements/actions

2. **HP Increase on Level Up**:

- Roll hit dice or use average: `4 + CON modifier`

- Add to max HP

### Phase 6: Skills and Saving Throws

1. **Add skill proficiency tracking**:

   ```python
      "skill_proficiencies": ["code_quality", "architecture", ...]
   ```



2. **Calculate skill bonuses**:

- `ability_modifier + proficiency_bonus` (if proficient)

- `ability_modifier` (if not proficient)

3. **Add saving throw proficiencies**:

   ```python
      "saving_throw_proficiencies": ["constitution", "intelligence"]
   ```



## File Changes

### Core Files

- `src/waft/core/gamification.py` - Add D&D mechanics

- `src/waft/main.py` - Update CLI commands for D&D display

- `src/waft/cli/hud.py` - Update HUD for D&D stats

### Test Files

- `tests/test_gamification.py` - Add D&D mechanics tests

### Data Migration

- Existing `gamification.json` files need ability scores initialized

- Backward compatible (keep Integrity/Insight)

## Example Output

### `waft stats` (D&D Mode)

```javascript
🌊 Waft - Character Stats

Ability Scores:
  STR: 12 (+1)  |  DEX: 10 (+0)  |  CON: 14 (+2)
  INT: 15 (+2)  |  WIS: 13 (+1)  |  CHA: 11 (+0)

Combat Stats:
  HP: 18/20  |  Level: 3  |  Proficiency: +2

Experience:
  XP: 450  |  XP to Next Level: 150

Achievements: 3
```



### `waft character` (Full Sheet)

```javascript
🌊 Waft - Character Sheet

=== Ability Scores ===
Strength:      12 (+1)
Dexterity:     10 (+0)
Constitution:  14 (+2)
Intelligence:  15 (+2)
Wisdom:        13 (+1)
Charisma:      11 (+0)

=== Combat ===
Hit Points:    18/20
Level:         3
Proficiency:   +2

=== Skills ===
Code Quality:  +3 (STR + Prof)
Architecture:  +4 (INT + Prof)
Best Practices: +3 (WIS + Prof)
...

=== Saving Throws ===
Constitution:  +4 (CON + Prof)
Intelligence:  +4 (INT + Prof)
...
```



## Testing Strategy

1. **Unit Tests**:

- Ability score calculations

- Modifier calculations

- Proficiency bonus by level

- HP calculations

- XP/Insight mapping

2. **Integration Tests**:

- CLI command output with D&D stats

- Data migration from old format

- Level up with ability score improvements

3. **Backward Compatibility**:

- Existing projects without D&D stats should initialize defaults

- Integrity/Insight should still work

## Configuration Options

1. **Enable/Disable D&D Mode**:

- `waft config set dnd_mode true`

- Or auto-detect based on ability scores presence

2. **Starting Ability Scores**:

- Default: All 8

- Option: Point buy (27 points, D&D standard)

- Option: Roll (4d6 drop lowest, D&D standard)

- Option: Derive from current stats

## Success Criteria

- [ ] Ability scores (STR, DEX, CON, INT, WIS, CHA) implemented

- [ ] Ability modifiers calculated correctly

- [ ] Proficiency bonus based on level

- [ ] HP calculated from CON and Integrity

- [ ] XP mapped from Insight

- [ ] CLI commands show D&D stats

- [ ] Backward compatible with existing data

- [ ] Tests pass

- [ ] Documentation updated

## Estimated Time

- Core D&D mechanics: 2-3 hours

- CLI updates: 1-2 hours

- Testing: 1 hour
- Documentation: 30 minutes