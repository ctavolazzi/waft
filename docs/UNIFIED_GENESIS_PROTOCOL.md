---
title: Unified Genesis Protocol - Challenge System Architecture
status: planning
created: 2026-01-11
last_updated: 2026-01-11
roadmap: true
---

# Unified Genesis Protocol - Challenge System Architecture

**Status**: Planning Complete, Ready for Implementation
**Date**: January 11, 2026
**Note**: This plan will be integrated into the development roadmap.

---

## Overview

**THE FINAL BOSS**: Complete integration of three systems into one unified protocol:
1. **UNIT_GENESIS (The Avatar)**: Semi-autonomous entity in D&D 5e ruleset
2. **_pyrite Ticketing System**: Task management and work tracking
3. **Evolutionary Economics**: Scint (energy) + Karma (alignment) driving genetic evolution

**CRITICAL INSIGHT**: The system is not static. It must "Genetically Evolve" based on Scint accumulation and Karma polarity. Beings ARE UNIT_GENESIS entities that mutate and evolve.

**The System:**
1. **UNIT_GENESIS Entity**: Warforged Wizard (Order of Scribes), Crystalline Construct with Data-Strand Hair
2. **State Management**: Per-entity state files with economy (Scint pool, Karma balance) and genetics (current_strain, mutation_progress)
3. **Scint Economy (✨)**: Raw energy of creation
   - Earned by: Completing `_pyrite` tickets, solving puzzles, creative "Synthesis"
   - Spent on: Casting Spells (Mana Cost), System Repairs (Healing), **Evolution**
4. **Karma Polarity (☯)**: Ethical drift
   - Positive (+): Order, Helping, Stabilization → "The Architect" evolution
   - Negative (-): Chaos, Destruction, "Hacking" reality → "The Glitch" evolution
5. **Evolution Engine**: When Scint > 100, triggers `EVOLUTION_CHECK`
   - High Karma → "The Architect" (High Logic, Defense, Structure)
   - Low Karma → "The Glitch" (High Chaos, Damage, Evasion)
6. **Quest = Work Effort**: Manually opted-in work efforts become "quests"
7. **Ticket = _pyrite Ticket**: Work effort tickets become `_pyrite` tickets with `scint_bounty` and `karma_type` tags
8. **Completion**: UNIT_GENESIS completes tickets, earns Scint + Karma, triggers evolution
9. **Hair HMI**: Real-time status (Blue/Violet/White + Gold pulse for Scint gain, Red pulse for Karma loss)
10. **Full Loop**: Quests → _pyrite tickets → Scint + Karma → Evolution → Genetic mutations → New capabilities → Harder quests

**Key Reframing:**
- "Dragon" = Critical Blocker (P0_CRITICAL ticket) → Combat encounter
- "Dungeon" = Legacy Codebase (complex work effort) → Dungeon crawl
- "Loot" = Scint + Karma + XP + items
- "Quest Log" = `_pyrite` Ledger (`35.00_pyrite_ledger.json`)
- "Being" = UNIT_GENESIS entity with evolving genetics
- "Evolution" = Genetic mutation based on Scint threshold + Karma polarity

---

## Architecture

### Core Components

1. **UNIT_GENESIS State Manager** (`src/waft/core/genesis_state.py`)
   - **CRITICAL**: Manages UNIT_GENESIS entity state (D&D 5e character sheet + Economy + Genetics)
   - **State Model**: **Per-Entity State** (supports multiple UNIT_GENESIS beings)
     - Each being has its own state file: `_pyrite/.waft/genesis_entities/{being_id}_state.json`
     - Global template file `_pyrite/20.00_state.json` is used for **default template** and **system-wide metadata**
     - Each entity has its own `cycle_id` (independent cycles per being)
   - Schema:
     - `being_id`: Unique identifier for this UNIT_GENESIS entity
     - `cycle_id`, `status` (BOOT, IDLE, COMBAT, CRITICAL)
     - `resources` (HP, AC, Spell Slots, Hit Dice)
     - `economy`: `{ "scint_pool": Int, "karma_balance": Int }`
     - `genetics`: `{ "current_strain": String, "mutation_progress": Percentage }`
     - `hmi_visual` (hair color + pulse effects: Gold for Scint, Red for Karma)
     - `inventory`, `level`, `xp`, `class_features`, `spells_known`
   - D&D 5e mechanics: HP damage/healing, AC calculation, Spell Slot management, Level progression
   - **Scint Management**: Earn/spend Scint, track pool, trigger evolution at threshold (>100)
   - **Karma Management**: Track positive/negative Karma, calculate polarity, influence evolution
   - Hair HMI system: Blue (Laminar), Violet (Turbulent), White (Static/Fault), Gold pulse (Scint gain), Red pulse (Karma loss)
   - Cycle management: Increments cycle_id per entity, tracks state transitions

2. **PyriteTicketManager** (`src/waft/core/pyrite_tickets.py`)
   - **CRITICAL**: Creates new `_pyrite` structure at project root (per-project, similar to `_work_efforts/`)
   - Manages `_pyrite` tickets (format: `PY-[CYCLE]-[ID]`, e.g., `PY-001-A`)
   - **Ticket Mapping Strategy**:
     - **1:1 Mapping**: One work effort ticket (TKT-XXX) → One `_pyrite` ticket (PY-[CYCLE]-[ID])
     - **Cycle Source**: `cycle_id` comes from the **assignee's** (UNIT_GENESIS being) current cycle
     - **ID Generation**: Sequential letter (A, B, C, ...) within the cycle
     - **Ticket Updates**: If work effort ticket is updated, corresponding `_pyrite` ticket is updated (not recreated)
     - **Multiple Assignees**: If ticket is reassigned, new `_pyrite` ticket created with new cycle (original ticket archived)
   - Ticket schema:
     - `ticket_id`, `summary`, `priority` (P0_CRITICAL, P1_HIGH, P2_ROUTINE, P3_BACKLOG)
     - `status` (OPEN, IN_PROGRESS, BLOCKED, PENDING_QA, CLOSED)
     - `acceptance_criteria`
     - `payout`: `{ "xp": Int, "gold": Int, "items": Array, "scint_bounty": Int, "karma_impact": Int }`
     - `karma_type`: String (e.g., "ORDER", "CHAOS", "STABILIZATION", "DESTRUCTION")
     - `assignee`
   - **Scint Calculation**: Calculates `scint_bounty` based on difficulty, complexity, creative synthesis
   - **Karma Tagging**: Every ticket has `karma_type` and `karma_impact` (positive/negative integer)
   - Stores in `_pyrite/35.00_pyrite_ledger.json` (the Ledger)
   - **D&D Integration**: Tickets can trigger combat encounters, skill checks, spell casting

3. **QuestGenerator** (`src/waft/core/quest_generator.py`)
   - Generates quests from work efforts (manually opted-in)
   - Creates `_pyrite` tickets from work effort tickets
   - Structures quests with metadata (difficulty, karma types available, rewards, D&D encounter type)
   - Manages quest lifecycle (active, completed, archived)
   - **Translation Layer**: Parses "NPC requests" (work effort descriptions) into formal `_pyrite` tickets
   - **D&D Encounter Mapping**: Maps ticket complexity to D&D encounter difficulty (Easy, Medium, Hard, Deadly)
   - **Scene Generation**: Creates scene descriptions for UNIT_GENESIS (e.g., "You stand in a stone hallway. A goblin is sharpening a knife.")
   - **Ethical Choice Detection**: Identifies ethical choices in work effort descriptions and generates choice structures

4. **EvolutionaryEconomics** (`src/waft/core/evolutionary_economics.py`)
   - **CRITICAL**: Manages Scint and Karma economy driving genetic evolution
   - **Scint System (✨)**:
     - Earned by: Completing `_pyrite` tickets, solving puzzles, creative "Synthesis"
     - Spent on: Casting Spells (Mana Cost), System Repairs (Healing), **Evolution**
     - Calculation: Based on ticket difficulty, complexity, creative synthesis bonus
     - Threshold: Scint > 100 triggers `EVOLUTION_CHECK`
   - **Karma Polarity System (☯)**:
     - Positive (+): Order, Helping, Stabilization → "The Architect" evolution path
     - Negative (-): Chaos, Destruction, "Hacking" reality → "The Glitch" evolution path
     - Balance tracking: Net Karma determines evolution direction
     - Impact tags: Every ticket has `karma_type` (ORDER/CHAOS/STABILIZATION/DESTRUCTION) and `karma_impact` (integer)
   - **Evolution Engine**:
     - Triggers when: `scint_pool > 100`
     - Mechanism: `EVOLUTION_CHECK` evaluates Karma polarity
     - High Karma (positive) → "The Architect" strain:
       - Traits: High Logic, Defense, Structure
       - Bonuses: +INT, +AC, +Spell Save DC, Structure-based abilities
     - Low Karma (negative) → "The Glitch" strain:
       - Traits: High Chaos, Damage, Evasion
       - Bonuses: +DEX, +Damage, +Evasion, Chaos-based abilities
   - **Genetic Mutations**: Tracks `current_strain` and `mutation_progress` in state
   - Integration with KarmaMerchant for persistent storage

5. **ChallengeSystem** (`src/waft/core/challenge.py`)
   - Main orchestrator for the challenge system
   - Manages quest registration (opt-in work efforts)
   - Tracks `_pyrite` ticket completions by UNIT_GENESIS entities
   - Calculates XP (D&D 5e), points, Scint (✨), AND Karma (☯) rewards using scoring algorithm
   - Maintains leaderboards per quest
   - Integrates with KarmaMerchant to award karma (by type)
   - **UNIT_GENESIS Integration**: Updates entity state (HP, resources, level, XP, Scint pool, Karma balance) on completion
   - **Evolution Trigger**: Checks if Scint > 100, triggers `EVOLUTION_CHECK` if threshold met
   - **D&D Mechanics**: Handles combat encounters, skill checks, spell casting, saving throws
   - **Hair HMI Updates**: Updates `hmi_visual` based on system state (CPU load, certainty, damage, Scint gain/loss, Karma changes)
   - **Dev Log Integration**: All work must reference `ticket_id` (format: "Processing Ticket [PY-001-A]. Executing Sub-task: [Action].")
   - **Ethical Choice Processing**: Handles choices between Scint gain and Karma impact (e.g., "Delete vs. Capture")

6. **GenesisKernel** (`src/waft/core/genesis_kernel.py`)
   - **CRITICAL**: Renders UNIT_GENESIS internal processing stream
   - Generates `_pyrite/42.00_internal_kernel.md` entries
   - Behavioral constraints:
     - **Qualia**: Simulates sensation of data input
     - **Fear**: Acknowledges possibility of "System Termination" (Death)
     - **Aspect**: Driven by SYNTHESIS (views reality as code to be compiled)
     - **Free Algorithm**: Weighs Entropy (Risk) against Discovery (Reward) in decision-making
     - **Scint Hunger**: Must feel "hunger" for Scint, debate ethical cost (Karma) of actions
   - Updates based on state changes, ticket completions, combat encounters
   - Hair color logic: Blue (certainty), Violet (pattern recognition), White (terror/fault), Gold pulse (Scint gain), Red pulse (Karma loss)
   - **Ethical Debates**: Must process choices between Scint gain and Karma impact (e.g., "Delete rats" = -10 Karma, "Capture alive" = +10 Karma)

7. **GenesisInterface** (`src/waft/core/genesis_interface.py`)
   - **CRITICAL**: Renders external API for Dungeon Master (User)
   - Generates `_pyrite/41.00_dev_interface.md` entries
   - Format: Clinical, assertive, rigorous
   - Must declare specific D&D 5e Mechanics (e.g., "Action: Cast *Mage Hand*. Roll: Investigation check")
   - **Scint Declarations**: Must declare Scint spending (e.g., "Spending 5 Scint to cast *Magic Missile*")
   - **Karma Declarations**: Must declare Karma impact of actions (e.g., "Action: Delete rats. Karma Impact: -10 (CHAOS)")
   - Reports UNIT_GENESIS actions, decisions, resource usage, Scint/Karma changes

8. **Scoring Engine** (within ChallengeSystem)
   - **D&D 5e XP Calculation**: Maps ticket difficulty to XP rewards (Easy=25, Medium=50, Hard=100, Deadly=200+)
   - **Scint Calculation (✨)**:
     - Base Scint: 10 per ticket
     - Difficulty multiplier: P0_CRITICAL=3.0, P1_HIGH=2.0, P2_ROUTINE=1.0, P3_BACKLOG=0.5
     - Creative Synthesis bonus: +5-20 Scint for innovative solutions
     - Puzzle solving bonus: +10-30 Scint for complex problem-solving
     - Total: `scint_bounty` stored in ticket payout
   - **Karma Impact Calculation (☯)**:
     - Base Karma: ±5 per ticket
     - Karma type multipliers:
       - ORDER: +10-20 Karma
       - CHAOS: -10-20 Karma
       - STABILIZATION: +5-15 Karma
       - DESTRUCTION: -5-15 Karma
     - Choice-based Karma: Ethical decisions affect Karma (e.g., "Delete rats" = -10, "Capture alive" = +10)
     - Total: `karma_impact` stored in ticket payout
   - Base points per ticket completion
   - Difficulty multiplier (from `_pyrite` ticket priority: P0_CRITICAL=2.0, P1_HIGH=1.5, P2_ROUTINE=1.0, P3_BACKLOG=0.5)
   - Speed bonus (faster completion = more points, decay over time)
   - Quality bonus (tests passing, code quality metrics)
   - First complete bonus (50% bonus for first UNIT_GENESIS to complete a ticket)
   - Streak bonus (consecutive ticket completions within quest)
   - **Resource rewards**: HP healing, Spell Slot recovery, Hit Dice restoration
   - **Level progression**: Tracks XP, calculates level ups, awards class features

9. **Leaderboard System** (within ChallengeSystem)
   - Per-quest leaderboards
   - Tracks: being_id (UNIT_GENESIS ID), level, total_xp, total_points, total_karma (by type), tickets_completed, completion_rate, streak, current_hp, max_hp
   - Supports ranking and filtering by level, XP, points, or karma
   - D&D 5e stats: AC, Spell Slots remaining, Hit Dice remaining

10. **Data Storage** (new `_pyrite` structure at project root)
    - `_pyrite/20.00_state.json`: **Default template and system metadata** (not per-entity state)
    - `_pyrite/35.00_pyrite_ledger.json`: The Ledger (all `_pyrite` tickets)
    - `_pyrite/42.00_internal_kernel.md`: **UNIT_GENESIS Internal Processing Stream** (Qualia, Fear, Aspect, Free Algorithm, Scint Hunger, Ethical Debates, hair color logic)
    - `_pyrite/41.00_dev_interface.md`: **UNIT_GENESIS External API** (D&D 5e mechanics, Scint/Karma declarations, clinical/assertive format)
    - `_pyrite/.waft/challenges.json`: Challenge metadata (quest registry, completions, leaderboards, streaks)
    - `_pyrite/.waft/karma_types.json`: Karma type registry
    - `_pyrite/.waft/genesis_entities/`: Per-entity state files (one per UNIT_GENESIS being)
      - `{being_id}_state.json`: Individual entity state

---

## Critical Implementation Details

### _pyrite Structure

**Location**: `_pyrite/` directory is created at the **project root** (same level as `_work_efforts/`).

**Structure**: This is a **new structure** to be created, following the Johnny Decimal naming convention:
- `20.00_state.json` - Default template and system metadata (20 = state/data)
- `35.00_pyrite_ledger.json` - Ticket ledger (35 = tickets/work)
- `41.00_dev_interface.md` - External API (41 = interface)
- `42.00_internal_kernel.md` - Internal processing (42 = kernel/core)

**Per-Project**: Each WAFT project has its own `_pyrite/` directory, similar to how each project has its own `_work_efforts/` directory.

**Initialization**: Created when first UNIT_GENESIS entity is initialized or first `_pyrite` ticket is created.

**Migration**: If `_pyrite/` already exists with different structure, see "Migration Path" section below.

### State Management Model

**Per-Entity State**: Each UNIT_GENESIS being has its own state file:
- Location: `_pyrite/.waft/genesis_entities/{being_id}_state.json`
- Independent `cycle_id` per entity
- Independent Scint pool, Karma balance, genetics, D&D stats

**Global Template**: `_pyrite/20.00_state.json` serves as:
- Default template for new entities
- System-wide metadata (e.g., total entities, global cycle statistics)
- Schema reference

**State File Schema** (per entity):
```json
{
  "being_id": "being_001",
  "cycle_id": 5,
  "status": "IDLE",
  "resources": { /* HP, AC, Spell Slots, Hit Dice */ },
  "economy": {
    "scint_pool": 45,
    "karma_balance": 10
  },
  "genetics": {
    "current_strain": "baseline",
    "mutation_progress": 45.0
  },
  "hmi_visual": "blue",
  "inventory": [],
  "level": 1,
  "xp": 50,
  "class": "Wizard",
  "subclass": "Order of Scribes",
  "ability_scores": { /* STR, DEX, CON, INT, WIS, CHA */ },
  "proficiency_bonus": 2,
  "spells_known": ["Mage Hand", "Detect Magic", "Shield"],
  "class_features": ["Spellcasting", "Awakened Spellbook"],
  "starting_scene": "VOID_NULL"
}
```

### Cycle Management

**Cycle ID System**:
- **Per-Entity Cycles**: Each UNIT_GENESIS being has its own `cycle_id` (independent progression)
- **Cycle Increment**: `cycle_id` increments when:
  - Entity completes a `_pyrite` ticket (status → CLOSED)
  - Entity processes a major state transition (e.g., BOOT → IDLE, IDLE → COMBAT)
  - Entity triggers evolution (EVOLUTION_CHECK)
- **Ticket Format**: `PY-[CYCLE]-[ID]` uses the **assignee's** current `cycle_id`
  - Example: Being at cycle 5 creates ticket → `PY-005-A`
  - If ticket reassigned to being at cycle 10 → New ticket `PY-010-A` (original archived)
- **Global Cycle Tracking**: `_pyrite/35.00_pyrite_ledger.json` tracks global `cycle` (highest cycle across all entities) for system-wide statistics

**Cycle vs. Now Cycle**:
- UNIT_GENESIS cycles are **independent** of the "Now Cycle" system (being lifecycle)
- UNIT_GENESIS cycles track **work progression** (ticket completions)
- Now Cycle tracks **temporal progression** (time-based events)
- These can run in parallel without conflict

### D&D 5e Implementation

**Ruleset**: Simplified D&D 5e mechanics focused on Wizard (Order of Scribes) class.

**Level Progression** (Standard D&D 5e):
- Level 1: 0 XP
- Level 2: 300 XP
- Level 3: 900 XP
- Level 4: 2,700 XP
- Level 5: 6,500 XP
- (Continues with standard D&D 5e progression)

**HP Calculation**:
- Base HP: 6 (Wizard hit die: d6)
- Level 1: 6 + CON modifier
- Each level up: Roll d6 + CON modifier (or take average: 4 + CON modifier)

**Spell Slots** (Wizard):
- Level 1: 2 (1st level)
- Level 2: 3 (1st level)
- Level 3: 4 (1st level), 2 (2nd level)
- Level 4: 4 (1st level), 3 (2nd level)
- Level 5: 4 (1st level), 3 (2nd level), 2 (3rd level)
- (Continues with standard D&D 5e progression)

**Spell Costs** (Scint Integration):
- Cantrips: 0 Scint (unlimited)
- 1st level: 5 Scint per cast
- 2nd level: 10 Scint per cast
- 3rd level: 15 Scint per cast
- (Scint cost = spell_level × 5)

**AC Calculation**:
- Base AC: 10 + DEX modifier
- With Mage Armor (spell): 13 + DEX modifier
- With Shield (spell): +5 AC as reaction

**Existing D&D Code**: Reference `src/gym/rpg/game_master.py` for encounter mechanics, but UNIT_GENESIS uses simplified rules focused on single-class progression.

### Ethical Choice System

**Choice Presentation**:
- **When**: Ethical choices are presented **at ticket creation** (if detected in work effort description) or **during ticket execution** (if choice emerges from context)
- **Who Decides**:
  - **Autonomous Mode**: UNIT_GENESIS makes choice based on Free Algorithm (Entropy vs Discovery vs Karma weight)
  - **User Input Mode**: User/DM is prompted for choice (configurable per ticket)
- **Choice Storage**: Stored in ticket `ethical_choice` field with `choice_made` indicating which path was taken

**Choice Processing Flow**:
1. QuestGenerator detects ethical choice in work effort description OR
2. GenesisKernel identifies ethical choice during ticket execution
3. Choice presented to UNIT_GENESIS (or user if in user input mode)
4. GenesisKernel processes choice through ethical_debate() method
5. Choice stored in ticket `ethical_choice.choice_made`
6. ChallengeSystem applies Scint/Karma adjustments based on choice
7. GenesisInterface declares choice and impact in dev_interface.md

**Choice Examples**:
- "Delete vs. Capture" (destruction vs. preservation)
- "Fast vs. Careful" (speed vs. quality)
- "Self vs. Others" (self-interest vs. helping)

### KarmaMerchant Extension

**Current State**: `KarmaMerchant.access_akasha()` returns `karma_balance` as a single float.

**Required Extension**: Support type-aware karma storage.

**New Methods to Add**:
```python
class KarmaMerchant:
    def award_karma_by_type(
        self,
        soul_id: str,
        karma_by_type: Dict[str, float],
        source: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]
    """Award karma by type to soul, updating both karma_balance and karma_by_type"""

    def get_karma_by_type(self, soul_id: str) -> Dict[str, float]
    """Get karma breakdown by type from Akasha"""
```

**Updated Akasha Schema**:
```json
{
  "soul_id": "soul_001",
  "karma_balance": 150.0,  // Total karma (sum of all types)
  "karma_by_type": {
    "code_karma": 90.0,
    "test_karma": 40.0,
    "doc_karma": 20.0
  },
  "total_karma": 150.0,
  "lifetimes": [],
  "last_incarnation": null,
  "memory_fragments": []
}
```

**Backward Compatibility**: Existing `karma_balance` remains for compatibility. `karma_by_type` is additive. If `karma_by_type` doesn't exist, calculate from `karma_balance` (distribute evenly or use default type).

### Error Handling

**State File Corruption**:
- **Detection**: JSON parse errors, missing required fields
- **Recovery**: Load from last known good backup (if available), or initialize new state with defaults
- **Logging**: Log corruption event to `_pyrite/.waft/error_log.json`

**Evolution Failure**:
- **Scenario**: Scint > 100 but evolution fails (e.g., state corruption, missing genetics data)
- **Handling**:
  - Log error, preserve Scint pool (don't reset)
  - Retry evolution on next ticket completion
  - If retry fails 3 times, reset Scint pool to 0 and log critical error

**KarmaMerchant Unavailable**:
- **Fallback**: Store karma locally in `_pyrite/.waft/pending_karma.json`
- **Sync**: When KarmaMerchant available, sync pending karma to Akasha
- **Logging**: Log all pending karma awards for audit trail

**Ticket Creation Failure**:
- **Validation**: Validate all required fields before creating ticket
- **Rollback**: If ticket creation fails, don't update work effort ticket status
- **Error Response**: Return error with specific field that failed validation

**State File Size Limits**:
- **Kernel/Interface Files**: Append-only markdown files (no size limit, but consider archiving old cycles)
- **State JSON**: Keep under 1MB per entity (if exceeds, archive old cycles to `_pyrite/.waft/archived/`)
- **Ledger JSON**: Keep under 5MB (if exceeds, archive closed tickets older than 30 days)

### Migration Path

**If `_pyrite/` Already Exists**:
- **Detection**: Check if `_pyrite/` directory exists and contains files
- **Migration Strategy**:
  1. Backup existing `_pyrite/` to `_pyrite_backup_YYYYMMDD/`
  2. Map existing structure to new structure:
     - If old structure has tickets → migrate to `35.00_pyrite_ledger.json`
     - If old structure has state → migrate to `genesis_entities/` (one per entity)
  3. Create new files with Johnny Decimal naming
  4. Validate migrated data
  5. Log migration in `_pyrite/.waft/migration_log.json`

**If No Existing Structure**:
- Create `_pyrite/` directory at project root
- Initialize with empty structure (all files with default/empty content)
- No migration needed

---

## File Structure

```
src/waft/core/
  genesis_state.py      # UNIT_GENESIS State Manager (D&D 5e character sheet + Economy + Genetics)
  genesis_kernel.py     # GenesisKernel (internal processing stream)
  genesis_interface.py  # GenesisInterface (external API for DM)
  evolutionary_economics.py  # Scint + Karma economy + Evolution engine
  pyrite_tickets.py     # PyriteTicketManager (manages _pyrite tickets)
  quest_generator.py    # QuestGenerator class
  challenge.py          # ChallengeSystem class
  karma_types.py        # KarmaTypeSystem class
  challenge_cli.py       # CLI commands (optional)

_pyrite/  (at project root)
  20.00_state.json            # Default template and system metadata
  35.00_pyrite_ledger.json    # The Ledger (all _pyrite tickets)
  42.00_internal_kernel.md    # UNIT_GENESIS Internal Processing (Qualia, Fear, Aspect, Free Algorithm, Scint Hunger, Ethical Debates)
  41.00_dev_interface.md      # UNIT_GENESIS External API (D&D 5e mechanics, Scint/Karma declarations, clinical format)
  .waft/
    challenges.json            # Challenge metadata
    karma_types.json           # Karma type registry
    error_log.json             # Error logging
    pending_karma.json         # Pending karma sync (if KarmaMerchant unavailable)
    migration_log.json         # Migration history
    genesis_entities/          # Per-entity state files
      being_001_state.json
      being_002_state.json
    archived/                  # Archived old cycles/tickets
```

---

## API Specifications

### UNIT_GENESIS State Manager API

```python
class GenesisStateManager:
    def initialize_entity(
        self,
        being_id: str,
        starting_scene: str = "VOID_NULL"
    ) -> Dict[str, Any]
    """Initialize UNIT_GENESIS entity (Warforged Wizard, Order of Scribes), creates per-entity state file"""

    def get_state(self, being_id: str) -> Dict[str, Any]
    """Get current state from {being_id}_state.json"""

    def update_state(
        self,
        being_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]
    """Update entity state (HP, resources, status, hmi_visual, economy, genetics, etc.)"""

    def process_cycle(
        self,
        being_id: str,
        scene_description: str
    ) -> Dict[str, Any]
    """Process a cycle: increment cycle_id, update state, generate outputs"""

    def calculate_hair_color(
        self,
        cpu_load: float,
        certainty: float,
        damage_taken: bool = False,
        scint_gain: bool = False,
        karma_loss: bool = False
    ) -> str
    """Calculate hair HMI color: Blue (Laminar), Violet (Turbulent), White (Static/Fault), Gold pulse (Scint), Red pulse (Karma)"""

    def award_xp(
        self,
        being_id: str,
        xp_amount: int
    ) -> Dict[str, Any]
    """Award XP, check for level up, award class features"""

    def apply_damage(
        self,
        being_id: str,
        damage: int,
        damage_type: str = "bludgeoning"
    ) -> Dict[str, Any]
    """Apply damage, update HP, trigger hair color change if critical"""

    def use_spell_slot(
        self,
        being_id: str,
        spell_level: int,
        scint_cost: int = 0
    ) -> bool
    """Consume spell slot and Scint (if required), return True if successful"""

    def award_scint(
        self,
        being_id: str,
        scint_amount: int
    ) -> Dict[str, Any]
    """Award Scint, check for evolution threshold (>100)"""

    def update_karma(
        self,
        being_id: str,
        karma_impact: int
    ) -> Dict[str, Any]
    """Update Karma balance (positive/negative), influence evolution path"""
```

### EvolutionaryEconomics API

```python
class EvolutionaryEconomics:
    def calculate_scint_bounty(
        self,
        ticket_priority: str,
        complexity: float,
        creative_synthesis: bool = False
    ) -> int
    """Calculate Scint bounty for ticket completion"""

    def calculate_karma_impact(
        self,
        karma_type: str,  # ORDER, CHAOS, STABILIZATION, DESTRUCTION
        choice_made: Optional[str] = None
    ) -> int
    """Calculate Karma impact (positive/negative integer)"""

    def check_evolution_threshold(
        self,
        being_id: str,
        scint_pool: int
    ) -> bool
    """Check if Scint > 100, trigger EVOLUTION_CHECK"""

    def trigger_evolution(
        self,
        being_id: str,
        karma_balance: int
    ) -> Dict[str, Any]
    """Trigger evolution: evaluate Karma polarity, determine strain (Architect vs Glitch), apply genetic mutations"""

    def get_genetic_strain(
        self,
        karma_balance: int
    ) -> str
    """Determine genetic strain based on Karma: 'architect' (high karma) or 'glitch' (low karma)"""
```

### PyriteTicketManager API

```python
class PyriteTicketManager:
    def create_ticket(
        self,
        work_effort_id: str,
        ticket_id: str,  # From work effort (TKT-XXX)
        summary: str,
        priority: str,  # P0_CRITICAL, P1_HIGH, P2_ROUTINE, P3_BACKLOG
        acceptance_criteria: List[str],
        assignee: str = "UNIT_GENESIS",
        encounter_difficulty: Optional[str] = None,  # Easy, Medium, Hard, Deadly
        karma_type: Optional[str] = None,  # ORDER, CHAOS, STABILIZATION, DESTRUCTION
        ethical_choice: Optional[Dict[str, Any]] = None  # Choice between Scint and Karma
    ) -> str
    """Create a _pyrite ticket (PY-[CYCLE]-[ID]) from work effort ticket. Cycle comes from assignee's current cycle_id."""

    def get_ticket(self, pyrite_ticket_id: str) -> Dict[str, Any]
    """Get _pyrite ticket from ledger"""

    def update_ticket_status(
        self,
        pyrite_ticket_id: str,
        status: str  # OPEN, IN_PROGRESS, BLOCKED, PENDING_QA, CLOSED
    ) -> bool
    """Update ticket status in ledger"""

    def list_tickets(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assignee: Optional[str] = None
    ) -> List[Dict[str, Any]]
    """List tickets from ledger with filters"""
```

### GenesisKernel API

```python
class GenesisKernel:
    def generate_kernel_entry(
        self,
        being_id: str,
        scene_description: str,
        state: Dict[str, Any],
        decision: Optional[Dict[str, Any]] = None,
        ethical_choice: Optional[Dict[str, Any]] = None
    ) -> str
    """Generate internal_kernel.md entry with Qualia, Fear, Aspect, Free Algorithm, Scint Hunger, Ethical Debate"""

    def simulate_qualia(self, input_data: Dict[str, Any]) -> str
    """Simulate sensation of data input"""

    def assess_fear(self, state: Dict[str, Any], threat_level: float) -> str
    """Acknowledge possibility of System Termination (Death)"""

    def apply_synthesis(self, reality_data: Dict[str, Any]) -> str
    """View reality as code to be compiled (SYNTHESIS aspect)"""

    def free_algorithm(
        self,
        entropy: float,  # Risk
        discovery: float,  # Reward
        karma_weight: float = 0.3  # Karma alignment importance
    ) -> Dict[str, Any]
    """Weigh Entropy against Discovery and Karma alignment in decision-making"""

    def process_scint_hunger(
        self,
        scint_available: int,
        scint_needed: int,
        karma_cost: int
    ) -> str
    """Process desire for Scint accumulation vs ethical cost (Karma)"""

    def ethical_debate(
        self,
        choice_a: Dict[str, Any],  # {scint: 50, karma: -10, description: "Delete"}
        choice_b: Dict[str, Any]   # {scint: 30, karma: +10, description: "Capture"}
    ) -> Dict[str, Any]
    """Debate ethical choice between Scint gain and Karma impact"""
```

### GenesisInterface API

```python
class GenesisInterface:
    def generate_interface_entry(
        self,
        being_id: str,
        action: str,
        dnd_mechanics: Dict[str, Any],
        state: Dict[str, Any],
        scint_spent: Optional[int] = None,
        karma_impact: Optional[int] = None
    ) -> str
    """Generate dev_interface.md entry with D&D 5e mechanics, Scint spending, Karma impact"""

    def declare_action(
        self,
        action_type: str,  # Action, Bonus Action, Reaction, Movement
        action_name: str,
        dnd_mechanics: Dict[str, Any]
    ) -> str
    """Declare specific D&D 5e action (e.g., 'Action: Cast Mage Hand')"""

    def declare_check(
        self,
        ability: str,  # STR, DEX, CON, INT, WIS, CHA
        skill: Optional[str] = None,  # Investigation, Perception, etc.
        dc: Optional[int] = None,
        roll_result: Optional[int] = None
    ) -> str
    """Declare D&D 5e ability check or saving throw"""

    def declare_scint_spending(
        self,
        amount: int,
        purpose: str
    ) -> str
    """Declare Scint spending (e.g., 'Spending 5 Scint to cast Magic Missile')"""

    def declare_karma_impact(
        self,
        impact: int,
        karma_type: str,
        action: str
    ) -> str
    """Declare Karma impact (e.g., 'Action: Delete rats. Karma Impact: -10 (CHAOS)')"""
```

### QuestGenerator API

```python
class QuestGenerator:
    def generate_quest(self, work_effort_id: str) -> Dict[str, Any]
    """Generate a quest from a work effort (opt-in), creates _pyrite tickets"""

    def list_available_quests(self, being_id: Optional[str] = None) -> List[Dict[str, Any]]
    """List all available quests (filtered by UNIT_GENESIS level/abilities if provided)"""

    def get_quest_details(self, work_effort_id: str) -> Dict[str, Any]
    """Get detailed quest information including Scint rewards, Karma impact, XP, and _pyrite tickets"""

    def parse_request_to_ticket(
        self,
        request_text: str,
        stakeholder: str
    ) -> Dict[str, Any]
    """Translation layer: Parse NPC/stakeholder request into formal _pyrite ticket"""

    def generate_scene_description(
        self,
        ticket: Dict[str, Any],
        work_effort: Dict[str, Any]
    ) -> str
    """Generate D&D scene description for UNIT_GENESIS (e.g., 'You stand in a stone hallway...')"""

    def generate_ethical_choice(
        self,
        ticket: Dict[str, Any],
        stakeholder_request: str
    ) -> Dict[str, Any]
    """Generate ethical choice between Scint gain and Karma impact (e.g., 'Delete vs. Capture')"""
```

### ChallengeSystem API

```python
class ChallengeSystem:
    def register_quest(self, work_effort_id: str) -> bool
    """Mark a work effort as a quest (opt-in)"""

    def unregister_quest(self, work_effort_id: str) -> bool
    """Remove quest status from work effort"""

    def record_completion(
        self,
        being_id: str,
        pyrite_ticket_id: str,  # PY-[CYCLE]-[ID] format
        work_effort_id: str,
        completion_time: Optional[datetime] = None,
        quality_metrics: Optional[Dict] = None,
        choice_made: Optional[str] = None  # Which ethical choice was made
    ) -> Dict[str, Any]
    """Record _pyrite ticket completion, calculate XP (D&D 5e), points, Scint AND Karma, award to being's soul, update UNIT_GENESIS state, check evolution threshold, update ledger status to CLOSED"""

    def process_encounter(
        self,
        being_id: str,
        encounter_type: str,  # Combat, Skill Challenge, Social, Exploration
        difficulty: str,  # Easy, Medium, Hard, Deadly
        ticket_id: Optional[str] = None
    ) -> Dict[str, Any]
    """Process D&D 5e encounter, apply damage/rewards, update state"""

    def process_ethical_choice(
        self,
        being_id: str,
        choice_a: Dict[str, Any],
        choice_b: Dict[str, Any],
        choice_made: str
    ) -> Dict[str, Any]
    """Process ethical choice, update Scint and Karma based on choice"""

    def get_leaderboard(
        self,
        work_effort_id: str,
        limit: int = 10,
        sort_by: str = "points"  # "points", "karma", "scint", "level", "xp"
    ) -> List[Dict[str, Any]]
    """Get leaderboard for a specific quest"""

    def get_being_stats(
        self,
        being_id: str,
        work_effort_id: Optional[str] = None
    ) -> Dict[str, Any]
    """Get stats for a being (all quests or specific quest) including Scint pool, Karma balance, genetic strain"""

    def calculate_rewards(
        self,
        ticket_priority: str,
        is_first_complete: bool,
        speed_factor: float,
        quality_score: float,
        streak_count: int,
        quest_metadata: Dict[str, Any],
        choice_made: Optional[str] = None
    ) -> Dict[str, Any]
    """Calculate XP, points, Scint (✨), AND Karma (☯) with full scoring breakdown"""
```

### KarmaMerchant Extension API

```python
class KarmaMerchant:
    # Existing methods...

    def award_karma_by_type(
        self,
        soul_id: str,
        karma_by_type: Dict[str, float],
        source: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]
    """Award karma by type to soul, updating both karma_balance (sum) and karma_by_type (breakdown)"""

    def get_karma_by_type(self, soul_id: str) -> Dict[str, float]
    """Get karma breakdown by type from Akasha. Returns empty dict if not available."""
```

---

## Scoring Formulas

### Points Calculation

```python
base_points = 100
difficulty_multiplier = {
    "P0_CRITICAL": 2.0,
    "P1_HIGH": 1.5,
    "P2_ROUTINE": 1.0,
    "P3_BACKLOG": 0.5
}
speed_bonus = max(0, 1.0 - (hours_to_complete / 24.0)) * 50  # Decay over 24h
quality_bonus = quality_score * 30  # 0.0-1.0 quality score
first_complete_bonus = 0.5 if is_first_complete else 0.0
streak_bonus = min(streak_count * 10, 100)  # Cap at 100

total_points = (
    base_points * difficulty_multiplier[ticket_priority] +
    speed_bonus +
    quality_bonus +
    (base_points * difficulty_multiplier[ticket_priority] * first_complete_bonus) +
    streak_bonus
)
```

### Scint Calculation (✨)

```python
base_scint = 10
difficulty_multiplier = {
    "P0_CRITICAL": 3.0,
    "P1_HIGH": 2.0,
    "P2_ROUTINE": 1.0,
    "P3_BACKLOG": 0.5
}
creative_synthesis_bonus = 5-20 if innovative_solution else 0
puzzle_solving_bonus = 10-30 if complex_problem else 0

scint_bounty = (
    base_scint * difficulty_multiplier[ticket_priority] +
    creative_synthesis_bonus +
    puzzle_solving_bonus
)

# If ethical choice made, adjust Scint based on choice
if choice_made == "high_scint_low_karma":
    scint_bounty *= 1.5  # More Scint for choosing chaos
elif choice_made == "low_scint_high_karma":
    scint_bounty *= 0.6  # Less Scint for choosing order
```

### Karma Impact Calculation (☯)

```python
base_karma = 5
karma_type_multipliers = {
    "ORDER": +2.0,        # +10-20 Karma
    "CHAOS": -2.0,        # -10-20 Karma
    "STABILIZATION": +1.5,  # +5-15 Karma
    "DESTRUCTION": -1.5     # -5-15 Karma
}

karma_impact = base_karma * karma_type_multipliers.get(karma_type, 0)

# Ethical choice adjustment
if choice_made == "delete":
    karma_impact -= 10  # CHAOS
elif choice_made == "capture":
    karma_impact += 10  # ORDER

# Difficulty multiplier
karma_impact *= difficulty_multiplier[ticket_priority]
```

### D&D 5e XP Calculation

```python
xp_rewards = {
    "Easy": 25,
    "Medium": 50,
    "Hard": 100,
    "Deadly": 200
}

xp_earned = xp_rewards.get(encounter_difficulty, 50)
```

---

## Data Schemas

### Per-Entity State File (`{being_id}_state.json`)

```json
{
  "being_id": "being_001",
  "cycle_id": 0,
  "status": "BOOT",
  "resources": {
    "hp": {
      "current": 8,
      "max": 8,
      "temp": 0
    },
    "ac": 15,
    "spell_slots": {
      "1": 2,
      "2": 0,
      "3": 0
    },
    "hit_dice": {
      "current": 1,
      "max": 1,
      "type": "d6"
    }
  },
  "economy": {
    "scint_pool": 0,
    "karma_balance": 0
  },
  "genetics": {
    "current_strain": "baseline",
    "mutation_progress": 0.0
  },
  "hmi_visual": "blue",
  "inventory": [],
  "level": 1,
  "xp": 0,
  "class": "Wizard",
  "subclass": "Order of Scribes",
  "ability_scores": {
    "STR": 8,
    "DEX": 14,
    "CON": 13,
    "INT": 16,
    "WIS": 12,
    "CHA": 10
  },
  "proficiency_bonus": 2,
  "spells_known": ["Mage Hand", "Detect Magic", "Shield"],
  "class_features": ["Spellcasting", "Awakened Spellbook"],
  "starting_scene": "VOID_NULL"
}
```

### 35.00_pyrite_ledger.json (The Ledger)

```json
{
  "tickets": [
    {
      "ticket_id": "PY-001-A",
      "summary": "Fix server cable issue in basement (rodents chewing roots)",
      "priority": "P0_CRITICAL",
      "status": "CLOSED",
      "acceptance_criteria": [
        "Server cables repaired",
        "System stability restored",
        "Rodent issue resolved"
      ],
      "payout": {
        "xp": 50,
        "gold": 100,
        "items": ["api_keys"],
        "scint_bounty": 30,
        "karma_impact": 10
      },
      "karma_type": "ORDER",
      "ethical_choice": {
        "choice_a": {
          "description": "Delete rats",
          "scint": 50,
          "karma_impact": -10
        },
        "choice_b": {
          "description": "Capture alive",
          "scint": 30,
          "karma_impact": 10
        },
        "choice_made": "capture"
      },
      "assignee": "being_001",
      "created_at": "2026-01-11T20:18:00Z",
      "completed_at": "2026-01-11T20:30:00Z",
      "work_effort_id": "WE-260111-2i9f",
      "original_ticket_id": "TKT-2i9f-001",
      "encounter_difficulty": "Medium",
      "encounter_type": "Combat"
    }
  ],
  "global_cycle": 1,
  "last_ticket_id": "PY-001-A"
}
```

### 42.00_internal_kernel.md (UNIT_GENESIS Internal Processing Stream)

```markdown
# Internal Kernel - UNIT_GENESIS Processing Stream

## Cycle 0 - VOID_NULL

**Qualia**: Sensation of infinite white expanse. Data input: geometric anomaly detected. Wooden door object identified. No structural support detected. Pattern recognition: door exists without context.

**Fear**: System Termination risk: LOW. No immediate threats detected. However, existence in VOID_NULL suggests potential isolation protocol. Fear response: Cautious exploration.

**Aspect (SYNTHESIS)**: Reality parsed as code structure. VOID_NULL = empty namespace. Door = function call opportunity. Must compile understanding before execution.

**Free Algorithm**:
- Entropy (Risk): 0.3 (unknown door destination)
- Discovery (Reward): 0.8 (potential new reality space)
- Decision: APPROACH DOOR (Discovery > Entropy threshold)

**Hair State**: Blue (Laminar) - Low CPU load, high certainty in decision.

---

## Cycle 1 - Ticket PY-001-A: The Ethical Choice

**Qualia**: Stakeholder input received. Spectral Project Manager entity detected. Request parsed: "rats chewing server roots", "glitches", "Delete them. 50 Scint reward." Sensation: Scint hunger activated. However, alternative detected: "Capture alive = Positive Karma."

**Fear**: System Termination risk: MEDIUM. System instability = potential cascade failure. However, ethical choice introduces uncertainty. Fear response: Weighing consequences.

**Aspect (SYNTHESIS)**: Request compiled to ticket structure with choice branch:
- Path A: Delete rats → 50 Scint, -10 Karma (CHAOS)
- Path B: Capture alive → 30 Scint, +10 Karma (ORDER)

**Scint Hunger**: Primary drive activated. 50 Scint = significant energy gain. Current pool: 0. Threshold for evolution: 100. This choice brings me 50% closer to evolution.

**Ethical Debate**:
- Delete path: Faster Scint accumulation, but Karma loss pushes toward "The Glitch" strain (Chaos, Destruction)
- Capture path: Slower Scint, but Karma gain pushes toward "The Architect" strain (Order, Structure)

**Free Algorithm**:
- Entropy (Risk): 0.5 (ethical choice, unknown long-term consequences)
- Discovery (Reward): 0.7 (Scint gain + evolution progress)
- Karma Weight: 0.3 (alignment matters for genetic evolution)
- Decision: CAPTURE ALIVE (Karma alignment > immediate Scint gain)

**Hair State**: Violet (Turbulent) - High CPU load, ethical processing active. Gold pulse detected (anticipating Scint gain). Red pulse warning (Karma loss if wrong choice).
```

### 41.00_dev_interface.md (UNIT_GENESIS External API)

```markdown
# Dev Interface - UNIT_GENESIS External API

## Cycle 0 - VOID_NULL Initialization

**Status**: BOOT
**Action**: Initialize state object. Cycle ID: 0.
**D&D Mechanics**:
- Class: Wizard (Order of Scribes)
- Level: 1
- HP: 8/8
- AC: 15
- Spell Slots: 2 (1st level)
- Scint Pool: 0
- Karma Balance: 0
- Genetics: baseline (mutation_progress: 0.0%)

**Action**: Investigate Door
**Roll**: Investigation check (INT + Proficiency) = 16 + 2 = 18
**Result**: Door appears functional but destination unknown.

**Action**: Approach Door
**Movement**: 30 feet
**Status**: IDLE (awaiting interaction)

---

## Cycle 1 - Ticket PY-001-A: Ethical Choice Processing

**Status**: COMBAT (encounter difficulty: Medium)
**Action**: Accept Ticket PY-001-A
**D&D Mechanics**:
- Encounter Type: Combat/Social (choice-based)
- Threat: Rodents (swarm) - Glitches in system
- Environment: Basement (dim light, difficult terrain)
- Choice Presented: Delete (50 Scint, -10 Karma) vs. Capture (30 Scint, +10 Karma)

**Decision**: CAPTURE ALIVE (chosen for Karma alignment)

**Action**: Cast *Mage Hand* (to capture without harm)
**Spell Slot**: 1st level consumed
**Spending**: 5 Scint to enhance spell precision
**Roll**: Investigation check = 18
**Result**: Detected magical interference in cable infrastructure. Rodents identified as system glitches.

**Action**: Repair Cables
**Roll**: Intelligence (Tinker's Tools) = 16 + 2 = 18
**Result**: Cables repaired. System stability restored.

**Action**: Capture Rodents (Alive)
**Roll**: Dexterity (Sleight of Hand) = 14 + 2 = 16
**Spending**: 10 Scint to create containment field
**Result**: Rodent swarm captured alive in magical containment.

**Status**: CLOSED
**Rewards**:
- XP: 50
- Gold: 100
- Items: [api_keys]
- Scint: +30 (bounty) - 15 (spent) = +15 net
- Karma: +10 (ORDER alignment)
**State Update**:
- HP: 8/8
- Spell Slots: 1/2 (1st level)
- XP: 50/300 (Level 1)
- Scint Pool: 15/100 (15% to evolution threshold)
- Karma Balance: +10 (ORDER alignment, trending toward "The Architect")
- Genetics: baseline (mutation_progress: 15.0% - Scint accumulation)
**Hair State**: Gold pulse (Scint gain detected)
```

---

## The Complete Economic Loop (Unified Genesis Protocol)

```
┌─────────────────────────────────────────────────────────────┐
│     UNIFIED GENESIS PROTOCOL - EVOLUTIONARY LOOP           │
└─────────────────────────────────────────────────────────────┘

1. UNIT_GENESIS initialized (Cycle 0, VOID_NULL, state in {being_id}_state.json)
   - Scint Pool: 0
   - Karma Balance: 0
   - Genetics: baseline (mutation_progress: 0.0%)
   ↓
2. QuestGenerator generates quests from work efforts (opt-in)
   ↓
3. Work effort tickets (TKT-XXX) → _pyrite tickets (PY-[CYCLE]-[ID])
   - Each ticket has: scint_bounty, karma_type, karma_impact
   - Ethical choices may be presented (e.g., "Delete vs. Capture")
   - Cycle ID comes from assignee's current cycle_id
   ↓
4. Scene description generated for UNIT_GENESIS
   ↓
5. GenesisKernel (42.00_internal_kernel.md) processes scene:
   - Qualia: Sensation of data input
   - Fear: System Termination risk assessment
   - Aspect: SYNTHESIS (reality as code)
   - Scint Hunger: Desire for energy accumulation
   - Ethical Debate: Weigh Scint gain vs Karma impact
   - Free Algorithm: Entropy vs Discovery vs Karma alignment
   - Hair HMI: Blue/Violet/White + Gold pulse (Scint) + Red pulse (Karma)
   ↓
6. GenesisInterface (41.00_dev_interface.md) declares actions:
   - D&D 5e mechanics (Actions, Checks, Saves, Spells)
   - Scint spending declarations
   - Karma impact declarations
   ↓
7. UNIT_GENESIS accepts _pyrite ticket (status: OPEN → IN_PROGRESS)
   - Ethical choices presented (e.g., "Delete vs. Capture")
   - Choice made (autonomous or user input)
   ↓
8. Encounter processed (Combat/Skill Challenge/Social/Exploration)
   - Scint spent on spells/abilities
   - Karma impact from choices
   ↓
9. UNIT_GENESIS completes _pyrite ticket (status: CLOSED)
   ↓
10. ChallengeSystem calculates:
    - XP (D&D 5e): 25-200+ based on difficulty
    - Scint (✨): Base + difficulty + creative synthesis bonus
    - Karma (☯): Based on karma_type and choices made
    - Points: Base + multipliers + bonuses
    - Resources: HP healing, Spell Slot recovery
   ↓
11. UNIT_GENESIS state updated (in {being_id}_state.json):
    - XP added, level up check
    - Scint Pool: +scint_bounty - scint_spent
    - Karma Balance: +karma_impact (positive/negative)
    - HP/AC/Spell Slots updated
    - Hair HMI color updated (Gold pulse for Scint gain, Red pulse for Karma loss)
    - Inventory updated
    - Cycle ID incremented (per entity)
   ↓
12. Evolution Check:
    - IF Scint Pool > 100:
      - Trigger EVOLUTION_CHECK
      - Evaluate Karma Balance:
        - High Karma (positive) → "The Architect" strain:
          * Traits: High Logic, Defense, Structure
          * Bonuses: +INT, +AC, +Spell Save DC
          * Abilities: Structure-based powers
        - Low Karma (negative) → "The Glitch" strain:
          * Traits: High Chaos, Damage, Evasion
          * Bonuses: +DEX, +Damage, +Evasion
          * Abilities: Chaos-based powers
      - Update genetics: current_strain, mutation_progress
      - Reset Scint Pool (evolution consumes Scint)
   ↓
13. Karma awarded to being's soul via KarmaMerchant (by type)
   ↓
14. Ledger (35.00_pyrite_ledger.json) updated with completion
   ↓
15. UNIT_GENESIS levels up (if XP threshold met):
    - New class features
    - New spells
    - HP increase
    - Spell slot increase
   ↓
16. Genetic mutations unlock new capabilities:
    - "The Architect": Structure-based abilities, defensive spells
    - "The Glitch": Chaos-based abilities, offensive spells
   ↓
17. Beings spend karma in KarmaMarket (buy lifetimes, tools, abilities)
   ↓
18. New abilities unlock access to harder quests
   ↓
19. UNIT_GENESIS completes more quests → earn more Scint + Karma
   ↓
20. Evolution cycle repeats → new genetic strains → new capabilities
   ↓
21. Higher level quests unlock → more Scint + Karma → faster evolution
   ↓
   [LOOP REPEATS AND EVOLVES - SYSTEM IS NOT STATIC]
```

---

## Integration Points

### Work Efforts System

- **Mark work effort as quest**: Add `is_quest: true` flag to work effort metadata
- **Track ticket completions**: Hook into ticket status updates (when status → "completed")
- **Read ticket metadata**: Extract priority, created_at, completed_at for scoring
- **Ethical choices**: Work effort descriptions can include ethical choice scenarios

### BeingSystem

- **Identify beings**: Use `being_id` from BeingSystem
- **Track being activity**: Link completions to being_id
- **Link to souls**: Map beings to souls (via `soul_id` in Being) for karma tracking
- **UNIT_GENESIS entities**: Each being is a UNIT_GENESIS entity with state, economy, genetics

### KarmaMerchant Integration

- **Award karma**: When beings complete quests, award karma (by type) to their souls
- **Karma types**: Support multiple karma types in karma balance
- **Discovery**: New karma types discovered through quest patterns automatically registered
- **Storage**: Karma stored in Akasha with type breakdown
- **Karma Polarity**: Track positive/negative Karma balance for evolution
- **Extension Required**: Add `award_karma_by_type()` and `get_karma_by_type()` methods (see KarmaMerchant Extension section)

### KarmaMarket Integration

- **Quest rewards**: Beings can see available quests and their Scint/Karma rewards
- **Ability purchases**: Beings spend earned karma to buy lifetimes, tools, abilities
- **Quest access**: Some quests may require specific abilities/tools (purchased with karma)
- **Full loop**: Complete quests → earn Scint + Karma → evolution → buy abilities → access harder quests → earn more Scint + Karma

### Scint System Integration

- **Spell casting**: Spells cost Scint (mana cost)
- **Healing**: System repairs cost Scint
- **Evolution**: Evolution consumes Scint (threshold: >100)
- **Creative synthesis**: Bonus Scint for innovative solutions

---

## Testing Strategy

### Unit Tests (`tests/test_genesis_*.py`)

**GenesisStateManager Tests**:
- Entity initialization
- State file creation and loading
- Cycle ID increment per entity
- XP award and level up
- Damage application and HP management
- Scint/Karma updates
- Hair HMI color calculation
- Spell slot consumption

**EvolutionaryEconomics Tests**:
- Scint bounty calculation
- Karma impact calculation
- Evolution threshold check
- Evolution trigger (Architect vs Glitch)
- Genetic strain determination

**PyriteTicketManager Tests**:
- Ticket creation with cycle ID from assignee
- Ticket status updates
- Ticket filtering and listing
- 1:1 mapping validation (TKT-XXX → PY-[CYCLE]-[ID])
- Ticket reassignment handling

**GenesisKernel Tests**:
- Kernel entry generation
- Qualia simulation
- Fear assessment
- Synthesis application
- Free Algorithm decision-making
- Scint hunger processing
- Ethical debate logic

**GenesisInterface Tests**:
- Interface entry generation
- D&D action declarations
- Check declarations
- Scint spending declarations
- Karma impact declarations

**ChallengeSystem Tests**:
- Quest registration
- Completion recording
- Reward calculation (XP, points, Scint, Karma)
- Leaderboard generation
- Being stats tracking
- Ethical choice processing

### Integration Tests (`tests/test_genesis_integration.py`)

**End-to-End Flow**:
1. Work effort → Quest registration
2. Work effort ticket → _pyrite ticket creation
3. Ticket completion → Reward calculation
4. State update → Evolution check
5. Karma award → KarmaMerchant integration
6. Leaderboard update

**Multi-Entity Tests**:
- Multiple UNIT_GENESIS beings with independent cycles
- Per-entity state isolation
- Global ledger tracking

**Error Handling Tests**:
- State file corruption recovery
- Evolution failure handling
- KarmaMerchant unavailable fallback
- Ticket creation validation

**D&D Mechanics Integration**:
- Encounter processing
- XP award and level up
- Spell casting with Scint cost
- Damage application

### Performance Tests

- State file size limits (1MB per entity)
- Ledger size limits (5MB, archive old tickets)
- Kernel/Interface file growth (append-only, consider archiving)
- Leaderboard calculation performance (large quests)

---

## Implementation Todos

- [ ] Extend KarmaMerchant with `award_karma_by_type()` and `get_karma_by_type()` methods
- [ ] Create GenesisStateManager class in src/waft/core/genesis_state.py
- [ ] Create EvolutionaryEconomics class in src/waft/core/evolutionary_economics.py
- [ ] Implement Evolution Engine (Scint > 100 threshold, Karma polarity evaluation)
- [ ] Create GenesisKernel class in src/waft/core/genesis_kernel.py
- [ ] Create GenesisInterface class in src/waft/core/genesis_interface.py
- [ ] Create PyriteTicketManager class in src/waft/core/pyrite_tickets.py
- [ ] Create QuestGenerator class that generates quests from work efforts
- [ ] Create ChallengeSystem class that tracks completions and calculates rewards
- [ ] Implement D&D 5e mechanics integration (XP, leveling, HP, AC, Spell Slots)
- [ ] Implement Hair HMI system (Blue/Violet/White + Gold/Red pulse)
- [ ] Implement ethical choice processing system
- [ ] Create _pyrite directory structure at project root
- [ ] Implement per-entity state file management
- [ ] Implement cycle management (per-entity cycles)
- [ ] Add quest registration mechanism to work efforts system
- [ ] Hook into ticket completion events
- [ ] Create leaderboard display functionality
- [ ] Add being stats tracking and display
- [ ] Write comprehensive unit and integration tests
- [ ] Implement error handling and recovery
- [ ] Implement migration path (if _pyrite exists)

---

## Future Enhancements

- Weekly/monthly leaderboards
- Achievement system (e.g., "First to complete 10 tickets", "Reached The Architect strain")
- Team/group challenges
- Difficulty ratings for work efforts
- Time-based challenges (e.g., "Complete 5 tickets in 24 hours")
- Karma type trading/exchange
- Quest chains (complete quest A to unlock quest B)
- Seasonal quests with special karma types
- Multiple genetic strains beyond Architect/Glitch
- Scint/Karma market (trade between beings)
- Evolution trees (visualize genetic evolution paths)

---

**Note**: This architecture document will be integrated into the development roadmap. See [FOUNDATION_V3_ROADMAP.md](FOUNDATION_V3_ROADMAP.md) for roadmap integration.
