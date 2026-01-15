---
name: TavernKeeper RPG Gamification System
overview: Design and implement the TavernKeeper module - a gamification engine that transforms software development into a semi-autonomous RPG using tinydb, d20, tracery, and rich. This replaces/enhances the current gamification system with RPG mechanics, procedural narrative, and persistent game state.
todos:
  - id: tavern-1
    content: Create feature branch feat/tavern-keeper and add dependencies (tinydb, d20, pytracery) to pyproject.toml
    status: pending
  - id: tavern-2
    content: Create SPEC-TAVERNKEEPER.md document with class diagram, grammar draft, hook map, and build order
    status: pending
  - id: tavern-3
    content: Implement TavernKeeper core class with TinyDB initialization and basic structure
    status: pending
    dependencies:
      - tavern-1
  - id: tavern-4
    content: Implement dice rolling system using d20 library (roll_check method)
    status: pending
    dependencies:
      - tavern-3
  - id: tavern-5
    content: Create Tracery grammar files for success, failure, and level up narratives (Constructivist Sci-Fi theme)
    status: pending
    dependencies:
      - tavern-3
  - id: tavern-6
    content: Implement narrative generation system (narrate method using Tracery)
    status: pending
    dependencies:
      - tavern-5
  - id: tavern-7
    content: Implement character system (ability scores, HP calculation, proficiency bonus)
    status: pending
    dependencies:
      - tavern-3
  - id: tavern-8
    content: Implement status effects system (buffs/debuffs) with application and duration tracking
    status: pending
    dependencies:
      - tavern-7
  - id: tavern-9
    content: Implement reward/penalty system (award_rewards, apply_status_effect methods)
    status: pending
    dependencies:
      - tavern-7
      - tavern-8
  - id: tavern-10
    content: Implement adventure journal logging system (log_adventure method)
    status: pending
    dependencies:
      - tavern-3
  - id: tavern-11
    content: Hook waft new command → Character creation event with narrative
    status: pending
    dependencies:
      - tavern-4
      - tavern-6
      - tavern-9
  - id: tavern-12
    content: Hook waft verify command → Constitution save with dice roll and narrative
    status: pending
    dependencies:
      - tavern-4
      - tavern-6
      - tavern-9
  - id: tavern-13
    content: Hook remaining commands (init, info, sync, add, finding log, assess, check, goal create)
    status: pending
    dependencies:
      - tavern-11
      - tavern-12
  - id: tavern-14
    content: Create waft character command to display full character sheet with D&D stats
    status: pending
    dependencies:
      - tavern-7
  - id: tavern-15
    content: Implement data migration from gamification.json to chronicles.json (backward compatible)
    status: pending
    dependencies:
      - tavern-3
  - id: tavern-16
    content: Write comprehensive tests for TavernKeeper system (dice, narrative, status effects, hooks)
    status: pending
    dependencies:
      - tavern-13
      - tavern-14

category: dreams
confidence: 0.60
constellation_date: 2026-01-14
---

# TavernKeeper RPG Gamification System - Research & Architecture Plan

## Objective
Transform `waft` from a static tool into a "Living Repository" by implementing the TavernKeeper system - a gamification engine that makes maintaining code feel like playing a game with Constructivist Sci-Fi theme.

## Vision
- **Theme**: Constructivist Sci-Fi (not generic fantasy)
- **HP** → **Integrity** (Structural stability)
- **XP** → **Insight** (Accumulated knowledge)
- **Gold** → **Credits** (Resource allocation)
- **DM** → **The TavernKeeper** (System narrator)

## Tech Stack (The "Holy Trinity")

**DO NOT DEVIATE** from this stack unless critical incompatibility:

1. **Memory**: `tinydb` - Document storage for game state in `_pyrite/.waft/chronicles.json`
2. **Fate**: `d20` - Dice rolling parser for skill checks
3. **Voice**: `tracery` (Python port) - Grammar-based procedural text generation for flavor
4. **Display**: `rich` - Already in use; for UI panels and progress bars

## Phase 1: Research & Analysis

### Step 1.1: Codebase Hook Point Analysis

**Task**: Scan `src/waft/main.py` and `src/waft/core/` to identify where game events should trigger.

**Hook Points Identified**:

| Waft Command | RPG Event Type | Hook Location | Current Behavior |
|-------------|----------------|---------------|------------------|
| `waft new` | Character Creation | `main.py:48` | Creates project, awards 50 Insight |
| `waft verify` | Constitution Save | `main.py:196` | Checks structure, updates Integrity |
| `waft init` | Initialization Ritual | `main.py:356` | Sets up structure, initializes Empirica |
| `waft info` | Perception Check | `main.py:445` | Displays project information |
| `waft sync` | Resource Management | `main.py:285` | Syncs dependencies |
| `waft add` | Acquisition | `main.py:313` | Adds dependency |
| `waft finding log` | Discovery Event | `main.py:692` | Awards 10 Insight |
| `waft assess` | Wisdom Save | `main.py:789` | Epistemic assessment, awards 25 Insight |
| `waft check` | Safety Gate | `main.py:746` | Sentinel check |
| `waft goal create` | Quest Creation | `main.py:845` | Creates goal |

**Integration Points**:
- `GamificationManager` in `src/waft/core/gamification.py` - Current gamification system
- Command decorators `@app.command()` - Entry points for hooks
- `console.print()` calls - Display points for narrative

### Step 1.2: Data Modeling

**File**: `_pyrite/.waft/chronicles.json` (TinyDB document store)

**JSON Schema Design**:

```json
{
  "character": {
    "name": "Project Name",
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
    "current_hp": 10
  },
  "status_effects": [
    {
      "id": "spaghetti_code",
      "name": "Spaghetti Code",
      "type": "debuff",
      "effect": {"wisdom": -2},
      "duration": null,
      "applied_at": "2026-01-06T00:00:00Z",
      "description": "Code complexity reduces Wisdom"
    }
  ],
  "adventure_journal": [
    {
      "timestamp": "2026-01-06T00:00:00Z",
      "event": "project_created",
      "narrative": "The TavernKeeper watches as a new structure emerges...",
      "dice_roll": "1d20+2",
      "result": 15,
      "outcome": "success",
      "rewards": {"insight": 50, "credits": 10}
    }
  ],
  "quests": [
    {
      "id": "quest_001",
      "name": "First Build",
      "description": "Create your first project",
      "status": "completed",
      "completed_at": "2026-01-06T00:00:00Z",
      "rewards": {"insight": 50, "achievement": "first_build"}
    }
  ],
  "achievements": ["first_build"],
  "tavern_keeper_state": {
    "last_narrative": "The structure stands firm...",
    "mood": "optimistic",
    "wisdom_shared": 0
  }
}
```

**TinyDB Structure**:
- Single document per project
- Queryable fields: `character.level`, `status_effects.type`, `adventure_journal.event`
- Indexed on: `timestamp`, `event`, `outcome`

### Step 1.3: Grammar Design (Tracery)

**File**: `src/waft/core/tavern_keeper/grammars.py`

**Success Narratives** (Constructivist Sci-Fi):
```json
{
  "success": [
    "The structure #material# holds firm against the #challenge#.",
    "Wisdom flows through the #component# as #action# completes.",
    "The TavernKeeper nods approvingly as #achievement# manifests."
  ],
  "material": ["foundation", "framework", "architecture", "substrate"],
  "challenge": ["entropy", "complexity", "uncertainty", "technical debt"],
  "component": ["codebase", "system", "repository", "project"],
  "action": ["verification", "construction", "integration", "optimization"],
  "achievement": ["stability", "clarity", "efficiency", "resilience"]
}
```

**Failure Narratives**:
```json
{
  "failure": [
    "The #structure# trembles as #problem# reveals itself.",
    "Wisdom falters - the #component# resists #action#.",
    "The TavernKeeper notes the #issue# with concern."
  ],
  "structure": ["foundation", "framework", "architecture"],
  "problem": ["instability", "complexity", "uncertainty"],
  "component": ["codebase", "system", "repository"],
  "action": ["verification", "construction", "integration"],
  "issue": ["structural weakness", "logical inconsistency", "technical debt"]
}
```

**Level Up Narratives**:
```json
{
  "level_up": [
    "The #entity# evolves - new #capability# emerges from accumulated wisdom.",
    "The TavernKeeper raises a glass: 'You have grown, #title#.'",
    "Level #level# achieved. The #aspect# deepens."
  ],
  "entity": ["structure", "system", "repository", "codebase"],
  "capability": ["resilience", "clarity", "efficiency", "wisdom"],
  "title": ["Architect", "Constructor", "Builder", "Craftsman"],
  "aspect": ["foundation", "framework", "understanding", "mastery"]
}
```

## Phase 2: Architecture Design

### Class Diagram

```
┌─────────────────────────────────────┐
│      TavernKeeper                   │
├─────────────────────────────────────┤
│ - db: TinyDB                        │
│ - grammar: TraceryGrammar           │
│ - project_path: Path                │
├─────────────────────────────────────┤
│ + roll_check(ability, dc)           │
│ + narrate(event, outcome)           │
│ + apply_status_effect(effect)       │
│ + award_rewards(rewards)            │
│ + log_adventure(event)              │
│ + get_character_sheet()             │
│ + process_command_hook(command)     │
└─────────────────────────────────────┘
           │
           │ uses
           ▼
┌─────────────────────────────────────┐
│      Character                      │
├─────────────────────────────────────┤
│ - name: str                         │
│ - level: int                        │
│ - integrity: float                  │
│ - insight: float                    │
│ - credits: int                      │
│ - ability_scores: Dict[str, int]    │
│ - current_hp: int                   │
│ - max_hp: int                       │
├─────────────────────────────────────┤
│ + get_modifier(ability)             │
│ + get_proficiency_bonus()           │
│ + calculate_hp()                    │
│ + level_up()                        │
└─────────────────────────────────────┘
```

### Hook Map: Command → RPG Check → Reward/Penalty

| Waft Command | RPG Check Type | Ability Used | DC/Challenge | Success Reward | Failure Penalty |
|-------------|----------------|--------------|--------------|----------------|-----------------|
| `waft new` | Character Creation | N/A | N/A | +50 Insight, +10 Credits, Achievement | N/A |
| `waft verify` | Constitution Save | CON | 12 | +2 Integrity, +5 Insight | -10 Integrity, Status: "Unstable" |
| `waft init` | Ritual Casting | WIS | 10 | +25 Insight, Status: "Initialized" | -5 Integrity |
| `waft info` | Perception Check | WIS | 8 | +2 Insight | None |
| `waft sync` | Resource Management | INT | 10 | +5 Credits, +3 Insight | -5 Credits |
| `waft add` | Acquisition | CHA | 12 | +5 Insight, +2 Credits | -3 Credits |
| `waft finding log` | Discovery | INT | 10 | +10 Insight, +5 Credits | None |
| `waft assess` | Wisdom Save | WIS | 15 | +25 Insight, +10 Credits | -5 Integrity |
| `waft check` | Safety Gate | WIS | 12 | +5 Insight | -10 Integrity, Status: "Risky" |
| `waft goal create` | Quest Creation | CHA | 10 | +5 Insight, Quest added | None |

### Status Effects System

**Buffs**:
- "Well Structured" (+2 CON, +1 WIS) - From successful verification
- "Documented" (+1 CHA, +1 INT) - From good documentation
- "Optimized" (+2 DEX, +1 INT) - From performance improvements

**Debuffs**:
- "Spaghetti Code" (-2 WIS, -1 INT) - From high complexity
- "Technical Debt" (-1 CON, -1 STR) - From accumulated issues
- "Unstable" (-2 CON) - From failed verification
- "Risky" (-1 WIS) - From failed safety checks

## Phase 3: Implementation Plan

### Step 3.1: Dependencies & Setup

1. **Add dependencies to `pyproject.toml`**:
   ```toml
   dependencies = [
       # ... existing ...
       "tinydb>=4.8.0",
       "d20>=2.0.0",
   ]
   
   [project.optional-dependencies]
   tavern-keeper = [
       "pytracery>=0.1.1",  # Python tracery port
   ]
   ```

2. **Create feature branch**:
   ```bash
   git checkout -b feat/tavern-keeper
   ```

### Step 3.2: Core TavernKeeper Class

**File**: `src/waft/core/tavern_keeper/__init__.py`

**Implementation Checklist**:
- [ ] Create `TavernKeeper` class with TinyDB initialization
- [ ] Implement `roll_check(ability: str, dc: int) -> Dict[str, Any]`
- [ ] Implement `narrate(event: str, outcome: str) -> str`
- [ ] Implement `apply_status_effect(effect: Dict) -> None`
- [ ] Implement `award_rewards(rewards: Dict) -> Dict`
- [ ] Implement `log_adventure(event: Dict) -> None`
- [ ] Implement `get_character_sheet() -> Dict`
- [ ] Implement `process_command_hook(command: str, success: bool) -> Dict`

### Step 3.3: Grammar System

**File**: `src/waft/core/tavern_keeper/grammars.py`

**Implementation Checklist**:
- [ ] Define success grammar (Tracery JSON)
- [ ] Define failure grammar
- [ ] Define level up grammar
- [ ] Define status effect grammar
- [ ] Create `GrammarManager` class to load/manage grammars

### Step 3.4: Command Hook Integration

**File**: `src/waft/main.py`

**Integration Points**:
- [ ] Hook `waft new` → Character creation event
- [ ] Hook `waft verify` → Constitution save
- [ ] Hook `waft init` → Ritual casting
- [ ] Hook `waft info` → Perception check
- [ ] Hook `waft sync` → Resource management
- [ ] Hook `waft add` → Acquisition
- [ ] Hook `waft finding log` → Discovery
- [ ] Hook `waft assess` → Wisdom save
- [ ] Hook `waft check` → Safety gate
- [ ] Hook `waft goal create` → Quest creation

**Pattern**:
```python
@app.command()
def verify(...):
    # ... existing code ...
    
    # TavernKeeper hook
    tavern = TavernKeeper(project_path)
    result = tavern.roll_check("constitution", dc=12)
    
    if verification_passed:
        narrative = tavern.narrate("verification_success", "success")
        rewards = tavern.award_rewards({"integrity": 2, "insight": 5})
        console.print(f"[dim]{narrative}[/dim]")
    else:
        narrative = tavern.narrate("verification_failure", "failure")
        penalties = tavern.apply_status_effect({"type": "debuff", "id": "unstable"})
        console.print(f"[dim]{narrative}[/dim]")
```

### Step 3.5: CLI Commands

**New Commands**:
- [ ] `waft character` - Display full character sheet
- [ ] `waft journal` - Show adventure journal (last N entries)
- [ ] `waft quests` - List active/completed quests
- [ ] `waft status` - Show active buffs/debuffs

**Enhanced Commands**:
- [ ] `waft stats` - Add TavernKeeper narrative
- [ ] `waft level` - Add level up narrative

### Step 3.6: Data Migration

**File**: `src/waft/core/tavern_keeper/migration.py`

**Migration Logic**:
- [ ] Check for existing `gamification.json`
- [ ] Migrate Integrity → HP
- [ ] Migrate Insight → XP
- [ ] Initialize ability scores (default 8 or derive from stats)
- [ ] Create `chronicles.json` with migrated data
- [ ] Preserve backward compatibility

## Phase 4: Testing

### Test Files
- [ ] `tests/test_tavern_keeper.py` - Core functionality
- [ ] `tests/test_grammars.py` - Grammar generation
- [ ] `tests/test_hooks.py` - Command hook integration
- [ ] `tests/test_migration.py` - Data migration

### Test Coverage
- [ ] Dice rolling (d20 integration)
- [ ] Narrative generation (Tracery)
- [ ] Status effect application
- [ ] Reward/penalty system
- [ ] Adventure journal logging
- [ ] Character sheet generation
- [ ] Command hook processing

## Phase 5: Documentation

### Files to Create
- [ ] `SPEC-TAVERNKEEPER.md` - Full specification (this document)
- [ ] `docs/TAVERN_KEEPER_GUIDE.md` - User guide
- [ ] Update `README.md` - Add TavernKeeper section
- [ ] Update `CHANGELOG.md` - Document new feature

## Step-by-Step Build Order

### Week 1: Foundation
1. ✅ Create feature branch `feat/tavern-keeper`
2. ✅ Add dependencies (tinydb, d20, pytracery)
3. ✅ Create `TavernKeeper` class skeleton
4. ✅ Implement TinyDB storage
5. ✅ Implement basic dice rolling (d20)
6. ✅ Create grammar files (Tracery JSON)

### Week 2: Core Mechanics
7. ✅ Implement character creation
8. ✅ Implement ability score system
9. ✅ Implement HP/Integrity mapping
10. ✅ Implement status effects
11. ✅ Implement reward/penalty system
12. ✅ Implement adventure journal

### Week 3: Integration
13. ✅ Hook `waft new` command
14. ✅ Hook `waft verify` command
15. ✅ Hook `waft init` command
16. ✅ Hook remaining commands
17. ✅ Add narrative display to commands
18. ✅ Create `waft character` command

### Week 4: Polish
19. ✅ Data migration from gamification.json
20. ✅ Add tests
21. ✅ Create documentation
22. ✅ Update README/CHANGELOG
23. ✅ Final testing and bug fixes

## Success Criteria

- [ ] TavernKeeper class implemented with all core methods
- [ ] TinyDB storage working (`chronicles.json`)
- [ ] Dice rolling integrated (d20)
- [ ] Narrative generation working (Tracery)
- [ ] All command hooks integrated
- [ ] Character sheet display functional
- [ ] Adventure journal logging
- [ ] Status effects system working
- [ ] Data migration from old system
- [ ] Tests passing
- [ ] Documentation complete

## Estimated Time
- Research & Architecture: 4-6 hours
- Core Implementation: 8-12 hours
- Integration: 6-8 hours
- Testing: 4-6 hours
- Documentation: 2-3 hours
- **Total: ~24-35 hours** (3-4 weeks part-time)