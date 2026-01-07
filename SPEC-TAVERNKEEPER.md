# SPEC-TAVERNKEEPER: TavernKeeper RPG Gamification System

**Created**: 2026-01-06
**Status**: ✅ Complete - Ready for Merge
**Branch**: `feat/tavern-keeper`
**Last Updated**: 2026-01-06

---

## Executive Summary

TavernKeeper transforms the `waft` CLI into a "Living Repository" by implementing RPG gamification mechanics with a Constructivist Sci-Fi theme. The system uses TinyDB for state, d20 for dice rolling, Tracery for procedural narratives, and Rich for terminal UI.

---

## Class Diagram

```
┌─────────────────────────────────────┐
│      TavernKeeper                   │
├─────────────────────────────────────┤
│ - project_path: Path                │
│ - data_dir: Path                    │
│ - chronicles_path: Path             │
│ - db: TinyDB (optional)             │
│ - _data: Dict (fallback)            │
├─────────────────────────────────────┤
│ + get_character() -> Dict           │
│ + get_ability_score(ability) -> int │
│ + get_ability_modifier(ability) -> int│
│ + get_proficiency_bonus() -> int    │
│ + get_max_hp() -> int               │
│ + get_current_hp() -> int           │
│ + roll_check(ability, dc, ...) -> Dict│
│ + narrate(event, outcome, ...) -> str│
│ + apply_status_effect(effect)       │
│ + award_rewards(rewards) -> Dict    │
│ + log_adventure(event)              │
│ + get_character_sheet() -> Dict     │
│ + process_command_hook(...) -> Dict│
└─────────────────────────────────────┘
```

---

## Grammar Draft (Tracery)

### Success Narratives

**Grammar Structure**:
```json
{
  "origin": [
    "The #structure# #action# as #challenge# #outcome#.",
    "Wisdom flows through the #component# as #achievement# manifests."
  ],
  "structure": ["foundation", "framework", "architecture"],
  "action": ["holds firm", "resonates", "stabilizes"],
  "challenge": ["entropy", "complexity", "uncertainty"],
  "outcome": ["dissipates", "recedes", "transforms"],
  "component": ["codebase", "system", "repository"],
  "achievement": ["stability", "clarity", "efficiency"]
}
```

**Example Outputs**:
- "The foundation holds firm as entropy dissipates."
- "Wisdom flows through the codebase as stability manifests."

### Failure Narratives

**Grammar Structure**:
```json
{
  "origin": [
    "The #structure# trembles as #problem# reveals itself.",
    "Wisdom falters - the #component# resists #action#."
  ],
  "structure": ["foundation", "framework", "architecture"],
  "problem": ["instability", "complexity", "uncertainty"],
  "component": ["codebase", "system", "repository"],
  "action": ["verification", "construction", "integration"]
}
```

**Example Outputs**:
- "The foundation trembles as instability reveals itself."
- "Wisdom falters - the codebase resists verification."

### Level Up Narratives

**Grammar Structure**:
```json
{
  "origin": [
    "The #entity# evolves - new #capability# emerges from accumulated wisdom.",
    "The TavernKeeper raises a glass: 'You have grown, #title#.'"
  ],
  "entity": ["structure", "system", "repository"],
  "capability": ["resilience", "clarity", "efficiency"],
  "title": ["Architect", "Constructor", "Builder"]
}
```

**Example Outputs**:
- "The structure evolves - new resilience emerges from accumulated wisdom."
- "The TavernKeeper raises a glass: 'You have grown, Architect.'"

**Note**: During development, AI will review generated narratives and refine grammars for better context fit and theme consistency.

---

## Hook Map: Command → RPG Check → Reward/Penalty

| Waft Command | RPG Check Type | Ability Used | DC | Success Reward | Failure Penalty |
|-------------|----------------|--------------|-----|----------------|-----------------|
| `waft new` | Character Creation | CHA | 10 | +50 Insight, +10 Credits | N/A |
| `waft verify` | Constitution Save | CON | 12 | +5 Insight, +2 Integrity | -10 Integrity, "Unstable" debuff |
| `waft init` | Ritual Casting | WIS | 10 | +25 Insight, +5 Credits | -5 Integrity |
| `waft info` | Perception Check | WIS | 8 | +2 Insight | None |
| `waft sync` | Resource Management | INT | 10 | +3 Insight, +5 Credits | -5 Credits |
| `waft add` | Acquisition | CHA | 12 | +5 Insight, +2 Credits | -3 Credits |
| `waft finding log` | Discovery | INT | 10 | +10 Insight, +5 Credits | None |
| `waft assess` | Wisdom Save | WIS | 15 | +25 Insight, +10 Credits | -5 Integrity |
| `waft check` | Safety Gate | WIS | 12 | +5 Insight | -10 Integrity, "Risky" debuff |
| `waft goal create` | Quest Creation | CHA | 10 | +5 Insight | None |

### Dice Roll Modifiers

- **Critical Success (20)**: 200% XP, loot drop chance (100%)
- **Superior (19)**: 150% XP, loot drop chance (25%)
- **Optimal (11-18)**: 110% XP
- **Nominal (2-10)**: 100% XP
- **Critical Failure (1)**: 50% XP, integrity damage, "Entropy Spike" debuff

---

## Step-by-Step Build Order

### Phase 1: Foundation ✅ Complete

- [x] Create feature branch `feat/tavern-keeper`
- [x] Add dependencies (tinydb, d20, pytracery) to pyproject.toml
- [x] Create TavernKeeper core class structure
- [x] Implement basic character system (ability scores, HP, XP)
- [x] Implement dice rolling (d20)
- [x] Create Tracery grammar files
- [x] Implement narrative generation with Tracery (with fallback)
- [x] Create SPEC document (this file)

### Phase 2: Core Mechanics ✅ Complete

- [x] Implement status effects system (buffs/debuffs)
- [x] Implement reward/penalty system
- [x] Implement adventure journal logging
- [x] Add data migration from gamification.json
- [x] Test character creation and stat updates

### Phase 3: Command Integration ✅ Complete

- [x] Hook `waft new` → Character creation event
- [x] Hook `waft verify` → Constitution save
- [x] Hook `waft init` → Ritual casting
- [x] Hook `waft info` → Perception check
- [x] Hook `waft sync` → Resource management
- [x] Hook `waft add` → Acquisition
- [x] Hook `waft finding log` → Discovery
- [x] Hook `waft assess` → Wisdom save
- [x] Hook `waft check` → Safety gate
- [x] Hook `waft goal create` → Quest creation

### Phase 4: CLI Commands ✅ Complete

- [x] Create `waft character` command (full character sheet)
- [x] Create `waft chronicle` command (adventure log)
- [x] Create `waft quests` command (active/completed quests)
- [x] Create `waft roll` command (manual dice roll)
- [x] Create `waft note` command (add note to chronicle)
- [x] Create `waft observe` command (log observation)
- [x] Create `waft dashboard` command (Red October Dashboard)

### Phase 5: Git Merge Driver ✅ Complete

- [x] Create `scripts/json_merge_driver.py`
- [x] Implement 3-way semantic merge logic
- [x] Configure `.gitattributes` for `chronicles.json`
- [x] Test merge scenarios

### Phase 6: Dashboard (Rich UI) ✅ Complete

- [x] Create "Red October" color theme
- [x] Implement dashboard layout (Header, Body, Footer)
- [x] Add character stats panel
- [x] Add adventure journal feed
- [x] Add repo health panel
- [x] Integrate with `waft dashboard` command

### Phase 7: Testing & Polish ✅ Complete

- [x] Write tests for TavernKeeper core
- [x] Write tests for dice rolling
- [x] Write tests for narrative generation
- [x] Write tests for command hooks
- [x] Test data migration
- [x] Test git merge driver
- [x] Balance XP curves
- [x] Refine narratives (AI review)

---

## Data Schema

### chronicles.json Structure

```json
{
  "character": {
    "name": "project-name",
    "level": 1,
    "integrity": 100.0,
    "insight": 0.0,
    "credits": 0,
    "ability_scores": {
      "strength": 8,
      "dexterity": 8,
      "constitution": 8,
      "intelligence": 8,
      "wisdom": 8,
      "charisma": 8
    },
    "proficiency_bonus": 2,
    "hit_dice": "d8",
    "max_hp": 10,
    "current_hp": 10,
    "created_at": "2026-01-06T00:00:00Z",
    "updated_at": "2026-01-06T00:00:00Z"
  },
  "status_effects": [
    {
      "id": "unstable",
      "name": "Unstable",
      "type": "debuff",
      "effect": {"constitution": -2},
      "duration": null,
      "applied_at": "2026-01-06T00:00:00Z",
      "description": "Failed verification reduces Constitution"
    }
  ],
  "adventure_journal": [
    {
      "timestamp": "2026-01-06T00:00:00Z",
      "event": "verify",
      "narrative": "The structure holds firm...",
      "dice_roll": "1d20+2",
      "result": 15,
      "outcome": "success",
      "rewards": {"insight": 5, "integrity": 2},
      "classification": "optimal"
    }
  ],
  "quests": [],
  "achievements": [],
  "tavern_keeper_state": {
    "last_narrative": "The structure holds firm...",
    "mood": "optimistic",
    "wisdom_shared": 0
  }
}
```

---

## Implementation Status

### ✅ Completed

1. ✅ Feature branch created
2. ✅ Dependencies added to pyproject.toml
3. ✅ TavernKeeper core class structure
4. ✅ Character system (ability scores, HP calculation, proficiency bonus)
5. ✅ Dice rolling system (d20 integration with fallback)
6. ✅ Narrative generation with placeholder replacement
7. ✅ Grammar files created
8. ✅ SPEC document created
9. ✅ Status effects system (buffs/debuffs with application/removal)
10. ✅ CLI command: `waft character` (full character sheet)
11. ✅ Command hooks integrated (all 10 major commands)
12. ✅ Git merge driver (semantic JSON merging)
13. ✅ Data migration from gamification.json
14. ✅ Comprehensive test suite (15 tests, all passing)
15. ✅ Adventure journal logging

### ✅ All Phases Complete

All implementation phases are complete. The system is fully functional and ready for merge.

---

## Next Steps

1. ✅ **Complete Tracery Integration**: Implemented with fallback (Tracery optional)
2. ✅ **Hook Commands**: All 10 commands integrated
3. ✅ **Create CLI Commands**: All commands created (`character`, `chronicle`, `quests`, `roll`, `note`, `observe`, `dashboard`)
4. ✅ **Test System**: Comprehensive test suite (15 tests, all passing)
5. ✅ **AI Review**: Narratives reviewed and grammars refined

---

**Status**: ✅ **Complete** - All phases implemented, tested, and ready for merge to main.

