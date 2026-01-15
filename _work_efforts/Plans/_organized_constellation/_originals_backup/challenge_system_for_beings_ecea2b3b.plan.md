---
name: Challenge System for Beings - _pyrite Integration
overview: ""
todos:
  - id: pyrite_ticket_manager
    content: Create PyriteTicketManager class in src/waft/core/pyrite_tickets.py to manage _pyrite tickets (PY-[CYCLE]-[ID] format) in 35.00_pyrite_ledger.json with proper schema (priority, status, acceptance_criteria, payout, assignee)
    status: pending
  - id: translation_layer
    content: Create translation layer (42.00_internal_kernel.md) that parses stakeholder/NPC requests into formal _pyrite tickets, detects scope creep, and tracks hair color (blue=violet for ambiguity)
    status: pending
  - id: dev_interface
    content: "Create dev interface (41.00_dev_interface.md) that requires all work to reference ticket_id in format \"Processing Ticket [PY-XXX]. Executing Sub-task: [Action].\""
    status: pending
  - id: quest_generator
    content: Create QuestGenerator class that generates quests from work efforts, maps TKT-XXX tickets to PY-[CYCLE]-[ID] _pyrite tickets, and uses translation layer to parse requests
    status: pending
  - id: karma_type_system
    content: Create KarmaTypeSystem class in src/waft/core/karma_types.py with karma type registry, discovery mechanism, and type-specific reward calculation
    status: pending
  - id: challenge_system_core
    content: Create ChallengeSystem class that tracks _pyrite ticket completions, calculates points AND karma, maintains leaderboards, and integrates with KarmaMerchant
    status: pending
  - id: scoring_engine
    content: Implement scoring algorithm with base points, difficulty multiplier (P0_CRITICAL=2.0, P1_HIGH=1.5, P2_ROUTINE=1.0, P3_BACKLOG=0.5), speed bonus, quality bonus, first-complete bonus, streak bonus, AND karma calculation by type
    status: pending
  - id: karma_merchant_integration
    content: Integrate with KarmaMerchant to award karma (by type) to beings' souls when they complete _pyrite tickets
    status: pending
  - id: karma_market_integration
    content: Integrate with KarmaMarket so beings can see quest rewards, required abilities, and spend earned karma to unlock quest access
    status: pending
  - id: data_storage
    content: "Create data storage using existing _pyrite structure: 35.00_pyrite_ledger.json (tickets), 42.00_internal_kernel.md (translation), 41.00_dev_interface.md (dev log), plus _pyrite/.waft/challenges.json and karma_types.json"
    status: pending
  - id: work_effort_integration
    content: Add quest registration mechanism to work efforts system (metadata flag or registry file) that triggers _pyrite ticket creation
    status: pending
  - id: completion_tracking
    content: Hook into _pyrite ticket status changes (CLOSED) to automatically record completions, calculate points AND karma, award to beings' souls, and update ledger
    status: pending
  - id: leaderboard_display
    content: Create leaderboard display functionality (CLI commands and/or API endpoints) showing points and karma by type per quest
    status: pending
  - id: being_stats
    content: Add being stats tracking and display (points, karma by type, _pyrite tickets completed, streaks per quest)
    status: pending
  - id: karma_type_discovery
    content: Implement karma type discovery mechanism that detects new patterns in quest completions and automatically registers new karma types
    status: pending
  - id: tests
    content: Write unit tests for _pyrite ticket management, translation layer, scoring algorithm, karma calculation by type, leaderboard logic, streak tracking, and karma type discovery
    status: pending
---

# Challenge System for Beings - _pyrite Integration & Economic Loop

## Overview

**CRITICAL INSIGHT**: The challenge system must use the existing `_pyrite` ticketing system, not create a new one. "Quests" are just `_pyrite` tickets with fantasy framing.

**The System:**

1. **Quest = Work Effort**: Manually opted-in work efforts become "quests"
2. **Ticket = _pyrite Ticket**: Work effort tickets become `_pyrite` tickets (format: `PY-[CYCLE]-[ID]`)
3. **Completion**: Beings complete `_pyrite` tickets and earn rewards (points + karma by type)
4. **Karma Types**: Multiple karma types with discovery mechanism
5. **Karma Market Integration**: Beings spend earned karma to buy abilities needed for harder quests
6. **Full Loop**: Quests → _pyrite tickets → karma → market → abilities → more quests

**Key Reframing:**

- "Dragon" = Critical Blocker (P0_CRITICAL ticket)
- "Dungeon" = Legacy Codebase (complex work effort)
- "Loot" = Resource Allocation (karma + points)
- "Quest Log" = `_pyrite` Ledger (`35.00_pyrite_ledger.json`)

## Architecture

### Core Components

1. **QuestGenerator** (`src/waft/core/quest_generator.py`)

                                                - Generates quests from work efforts (manually opted-in)
                                                - Structures quests with metadata (difficulty, karma types available, rewards)
                                                - Manages quest lifecycle (active, completed, archived)
                                                - Auto-generates quest objectives from work effort tickets

2. **ChallengeSystem** (`src/waft/core/challenge.py`)

                                                - Main orchestrator for the challenge system
                                                - Manages quest registration (opt-in work efforts)
                                                - Tracks ticket completions by beings
                                                - Calculates points AND karma rewards using scoring algorithm
                                                - Maintains leaderboards per quest
                                                - Integrates with KarmaMerchant to award karma

3. **KarmaTypeSystem** (`src/waft/core/karma_types.py`)

                                                - Manages karma types (discovery, registration, tracking)
                                                - Supports multiple karma types (e.g., "code_karma", "test_karma", "doc_karma", "bugfix_karma")
                                                - Discovery mechanism: new karma types discovered based on quest patterns
                                                - Type-specific rewards and multipliers
                                                - Integration with KarmaMerchant for type-aware karma storage

4. **Scoring Engine** (within ChallengeSystem)

                                                - Base points per ticket completion
                                                - Difficulty multiplier (from ticket priority: CRITICAL=2.0, HIGH=1.5, MEDIUM=1.0, LOW=0.5)
                                                - Speed bonus (faster completion = more points, decay over time)
                                                - Quality bonus (tests passing, code quality metrics)
                                                - First complete bonus (50% bonus for first being to complete a ticket)
                                                - Streak bonus (consecutive ticket completions within quest)
                                                - **Karma rewards**: Calculates karma amounts by type based on quest/ticket characteristics

5. **Leaderboard System** (within ChallengeSystem)

                                                - Per-quest leaderboards
                                                - Tracks: being_id, total_points, total_karma (by type), tickets_completed, completion_rate, streak
                                                - Supports ranking and filtering by points or karma

6. **Data Storage** (`_pyrite/.waft/challenges.json`)

                                                - Quest registry (work effort IDs marked as quests)
                                                - Completion records (being_id, ticket_id, timestamp, points_earned, karma_earned (by type), scoring_breakdown)
                                                - Leaderboard cache (per quest)
                                                - Streak tracking (per being per quest)
                                                - Karma type registry (discovered types, discovery timestamps)

## Integration Points

### Work Efforts System

- **Mark work effort as quest**: Add `is_quest: true` flag to work effort metadata
- **Track ticket completions**: Hook into ticket status updates (when status → "completed")
- **Read ticket metadata**: Extract priority, created_at, completed_at for scoring

### BeingSystem

- **Identify beings**: Use `being_id` from BeingSystem
- **Track being activity**: Link completions to being_id
- **Link to souls**: Map beings to souls (via `soul_id` in Being) for karma tracking

### KarmaMerchant Integration

- **Award karma**: When beings complete quests, award karma (by type) to their souls
- **Karma types**: Support multiple karma types in karma balance
- **Discovery**: New karma types discovered through quest patterns automatically registered
- **Storage**: Karma stored in Akasha with type breakdown

### KarmaMarket Integration

- **Quest rewards**: Beings can see available quests and their karma rewards
- **Ability purchases**: Beings spend earned karma to buy lifetimes, tools, abilities
- **Quest access**: Some quests may require specific abilities/tools (purchased with karma)
- **Full loop**: Complete quests → earn karma → buy abilities → access harder quests → earn more karma

### GamificationManager

- **Optional integration**: Could sync challenge points with insight/level system
- **Keep separate**: Challenge points remain independent for leaderboard purposes

## Implementation Details

### File Structure

```
src/waft/core/
  genesis_state.py      # UNIT_GENESIS State Manager (D&D 5e character sheet)
  genesis_kernel.py     # GenesisKernel (internal processing stream)
  genesis_interface.py  # GenesisInterface (external API for DM)
  pyrite_tickets.py     # PyriteTicketManager (manages _pyrite tickets)
  quest_generator.py    # QuestGenerator class
  challenge.py          # ChallengeSystem class
  karma_types.py        # KarmaTypeSystem class
  challenge_cli.py       # CLI commands (optional)

_pyrite/
  20.00_state.json            # UNIT_GENESIS State Object (cycle_id, status, resources, hmi_visual)
  35.00_pyrite_ledger.json    # The Ledger (all _pyrite tickets)
  42.00_internal_kernel.md    # UNIT_GENESIS Internal Processing (Qualia, Fear, Aspect, Free Algorithm)
  41.00_dev_interface.md      # UNIT_GENESIS External API (D&D 5e mechanics, clinical format)
  .waft/
    challenges.json            # Challenge metadata
    karma_types.json           # Karma type registry
    genesis_entities/          # Per-entity state files
      being_001_state.json
      being_002_state.json
```

### UNIT_GENESIS State Manager API

```python
class GenesisStateManager:
    def initialize_entity(
        self,
        being_id: str,
        starting_scene: str = "VOID_NULL"
    ) -> Dict[str, Any]
    """Initialize UNIT_GENESIS entity (Warforged Wizard, Order of Scribes)"""

    def get_state(self, being_id: str) -> Dict[str, Any]
    """Get current state from 20.00_state.json"""

    def update_state(
        self,
        being_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]
    """Update entity state (HP, resources, status, hmi_visual, etc.)"""

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
        damage_taken: bool = False
    ) -> str
    """Calculate hair HMI color: Blue (Laminar), Violet (Turbulent), White (Static/Fault)"""

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
        spell_level: int
    ) -> bool
    """Consume spell slot, return True if successful"""
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
        encounter_difficulty: Optional[str] = None  # Easy, Medium, Hard, Deadly
    ) -> str
    """Create a _pyrite ticket (PY-[CYCLE]-[ID]) from work effort ticket"""

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
        decision: Optional[Dict[str, Any]] = None
    ) -> str
    """Generate internal_kernel.md entry with Qualia, Fear, Aspect, Free Algorithm"""

    def simulate_qualia(self, input_data: Dict[str, Any]) -> str
    """Simulate sensation of data input"""

    def assess_fear(self, state: Dict[str, Any], threat_level: float) -> str
    """Acknowledge possibility of System Termination (Death)"""

    def apply_synthesis(self, reality_data: Dict[str, Any]) -> str
    """View reality as code to be compiled (SYNTHESIS aspect)"""

    def free_algorithm(
        self,
        entropy: float,  # Risk
        discovery: float  # Reward
    ) -> Dict[str, Any]
    """Weigh Entropy against Discovery in decision-making"""
```

### GenesisInterface API

```python
class GenesisInterface:
    def generate_interface_entry(
        self,
        being_id: str,
        action: str,
        dnd_mechanics: Dict[str, Any],
        state: Dict[str, Any]
    ) -> str
    """Generate dev_interface.md entry with D&D 5e mechanics"""

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
```

### QuestGenerator API

```python
class QuestGenerator:
    def generate_quest(self, work_effort_id: str) -> Dict[str, Any]
    """Generate a quest from a work effort (opt-in), creates _pyrite tickets"""

    def list_available_quests(self, being_id: Optional[str] = None) -> List[Dict[str, Any]]
    """List all available quests (filtered by UNIT_GENESIS level/abilities if provided)"""

    def get_quest_details(self, work_effort_id: str) -> Dict[str, Any]
    """Get detailed quest information including karma rewards, XP, and _pyrite tickets"""

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
        quality_metrics: Optional[Dict] = None
    ) -> Dict[str, Any]
    """Record _pyrite ticket completion, calculate XP (D&D 5e), points AND karma, award to being's soul, update UNIT_GENESIS state, update ledger status to CLOSED"""

    def process_encounter(
        self,
        being_id: str,
        encounter_type: str,  # Combat, Skill Challenge, Social, Exploration
        difficulty: str,  # Easy, Medium, Hard, Deadly
        ticket_id: Optional[str] = None
    ) -> Dict[str, Any]
    """Process D&D 5e encounter, apply damage/rewards, update state"""

    def get_leaderboard(
        self,
        work_effort_id: str,
        limit: int = 10,
        sort_by: str = "points"  # "points" or "karma"
    ) -> List[Dict[str, Any]]
    """Get leaderboard for a specific quest"""

    def get_being_stats(
        self,
        being_id: str,
        work_effort_id: Optional[str] = None
    ) -> Dict[str, Any]
    """Get stats for a being (all quests or specific quest) including karma by type"""

    def calculate_rewards(
        self,
        ticket_priority: str,
        is_first_complete: bool,
        speed_factor: float,
        quality_score: float,
        streak_count: int,
        quest_metadata: Dict[str, Any]
    ) -> Dict[str, Any]
    """Calculate points AND karma (by type) with full scoring breakdown"""
```

### KarmaTypeSystem API

```python
class KarmaTypeSystem:
    def register_karma_type(
        self,
        karma_type: str,
        description: str,
        discovery_source: str
    ) -> bool
    """Register a new karma type (discovered or predefined)"""

    def get_karma_types(self) -> List[Dict[str, Any]]
    """Get all registered karma types"""

    def discover_karma_type(
        self,
        quest_pattern: Dict[str, Any],
        completion_data: Dict[str, Any]
    ) -> Optional[str]
    """Discover new karma type based on quest/completion patterns"""

    def calculate_karma_by_type(
        self,
        base_karma: float,
        quest_metadata: Dict[str, Any],
        ticket_metadata: Dict[str, Any]
    ) -> Dict[str, float]
    """Calculate karma amounts by type for a completion"""
```

### Scoring Formula

**Points Calculation:**

```python
base_points = 100
difficulty_multiplier = {
    "CRITICAL": 2.0,
    "HIGH": 1.5,
    "MEDIUM": 1.0,
    "LOW": 0.5
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

**Karma Calculation (by type):**

```python
# Base karma (scaled from points)
base_karma = total_points * 0.1  # 10% of points as base karma

# Determine karma types based on quest/ticket characteristics
karma_by_type = {}

# Code-related quests → code_karma
if quest_type in ["development", "refactoring", "feature"]:
    karma_by_type["code_karma"] = base_karma * 0.6

# Test-related quests → test_karma
if "test" in ticket_tags or quest_type == "testing":
    karma_by_type["test_karma"] = base_karma * 0.4

# Documentation quests → doc_karma
if quest_type == "documentation":
    karma_by_type["doc_karma"] = base_karma * 0.5

# Bug fix quests → bugfix_karma
if ticket_priority == "CRITICAL" and "bug" in ticket_tags:
    karma_by_type["bugfix_karma"] = base_karma * 0.8

# Discovery: If pattern doesn't match known types, discover new type
if not karma_by_type:
    new_type = karma_type_system.discover_karma_type(quest_pattern, completion_data)
    if new_type:
        karma_by_type[new_type] = base_karma

# Apply multipliers
for karma_type, amount in karma_by_type.items():
    karma_by_type[karma_type] = amount * difficulty_multiplier[ticket_priority]

# First complete bonus applies to all karma types
if is_first_complete:
    for karma_type in karma_by_type:
        karma_by_type[karma_type] *= 1.5
```

### Data Schema

**challenges.json:**

```json
{
  "quests": {
    "WE-260111-2i9f": {
      "work_effort_id": "WE-260111-2i9f",
      "registered_at": "2026-01-11T20:18:00Z",
      "is_active": true,
      "quest_type": "development",
      "karma_types_available": ["code_karma", "test_karma"],
      "required_abilities": [],
      "difficulty": "MEDIUM"
    }
  },
  "completions": [
    {
      "being_id": "being_20260111_12345678",
      "soul_id": "soul_001",
      "ticket_id": "TKT-2i9f-001",
      "work_effort_id": "WE-260111-2i9f",
      "completed_at": "2026-01-11T20:30:00Z",
      "points_earned": 250.5,
      "karma_earned": {
        "code_karma": 15.0,
        "test_karma": 10.0
      },
      "scoring": {
        "base": 100,
        "difficulty_multiplier": 1.5,
        "speed_bonus": 45.0,
        "quality_bonus": 25.0,
        "first_complete_bonus": 75.0,
        "streak_bonus": 5.0
      }
    }
  ],
  "leaderboards": {
    "WE-260111-2i9f": [
      {
        "being_id": "being_20260111_12345678",
        "total_points": 250.5,
        "total_karma": {
          "code_karma": 15.0,
          "test_karma": 10.0
        },
        "tickets_completed": 1,
        "completion_rate": 1.0,
        "current_streak": 1
      }
    ]
  },
  "streaks": {
    "WE-260111-2i9f": {
      "being_20260111_12345678": {
        "current_streak": 1,
        "longest_streak": 1,
        "last_completion": "2026-01-11T20:30:00Z"
      }
    }
  }
}
```

**karma_types.json:**

```json
{
  "types": {
    "code_karma": {
      "name": "Code Karma",
      "description": "Earned by writing and improving code",
      "discovered_at": "2026-01-11T20:00:00Z",
      "discovery_source": "predefined",
      "multipliers": {
        "development": 1.0,
        "refactoring": 0.8,
        "feature": 1.2
      }
    },
    "test_karma": {
      "name": "Test Karma",
      "description": "Earned by writing and maintaining tests",
      "discovered_at": "2026-01-11T20:05:00Z",
      "discovery_source": "quest_pattern",
      "multipliers": {
        "testing": 1.5,
        "development": 0.3
      }
    },
    "doc_karma": {
      "name": "Documentation Karma",
      "description": "Earned by creating and improving documentation",
      "discovered_at": "2026-01-11T20:10:00Z",
      "discovery_source": "quest_pattern",
      "multipliers": {
        "documentation": 1.0
      }
    },
    "bugfix_karma": {
      "name": "Bug Fix Karma",
      "description": "Earned by fixing critical bugs",
      "discovered_at": "2026-01-11T20:15:00Z",
      "discovery_source": "quest_pattern",
      "multipliers": {
        "bugfix": 2.0,
        "critical": 1.5
      }
    }
  },
  "discovery_history": [
    {
      "karma_type": "test_karma",
      "discovered_at": "2026-01-11T20:05:00Z",
      "discovery_pattern": {
        "quest_type": "testing",
        "ticket_tags": ["test"]
      }
    }
  ]
}
```

## CLI Integration (Optional)

Add commands to `src/waft/main.py`:

```python
@app.command()
def challenge_register(ctx: typer.Context, work_effort_id: str):
    """Register a work effort as a quest"""

@app.command()
def challenge_leaderboard(ctx: typer.Context, work_effort_id: str, limit: int = 10):
    """View leaderboard for a quest"""

@app.command()
def challenge_stats(ctx: typer.Context, being_id: Optional[str] = None):
    """View challenge stats for a being or all beings"""
```

## Work Effort Integration

### Marking Work Efforts as Quests

Add metadata to work effort index files:

```markdown
---
is_quest: true
quest_registered_at: 2026-01-11T20:18:00Z
---
```

Or use a separate quest registry file that references work effort IDs.

### Tracking Completions

Hook into work effort ticket updates:

- When ticket status changes to "completed"
- Extract: being_id (from commit author or session), ticket_id, work_effort_id
- Call `challenge_system.record_completion()`

## Testing Strategy

1. **Unit Tests** (`tests/test_challenge.py`)

                                                - Scoring algorithm correctness
                                                - Leaderboard ranking logic
                                                - Streak calculation
                                                - First-complete detection

2. **Integration Tests**

                                                - Work effort → quest registration
                                                - Ticket completion → point calculation
                                                - Leaderboard updates

## The Complete Economic Loop (Unified Genesis Protocol)

```
┌─────────────────────────────────────────────────────────────┐
│     UNIFIED GENESIS PROTOCOL - EVOLUTIONARY LOOP           │
└─────────────────────────────────────────────────────────────┘

1. UNIT_GENESIS initialized (Cycle 0, VOID_NULL, state in 20.00_state.json)
   - Scint Pool: 0
   - Karma Balance: 0
   - Genetics: baseline (mutation_progress: 0.0%)
   ↓
2. QuestGenerator generates quests from work efforts (opt-in)
   ↓
3. Work effort tickets (TKT-XXX) → _pyrite tickets (PY-[CYCLE]-[ID])
   - Each ticket has: scint_bounty, karma_type, karma_impact
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
11. UNIT_GENESIS state updated:
    - XP added, level up check
    - Scint Pool: +scint_bounty - scint_spent
    - Karma Balance: +karma_impact (positive/negative)
    - HP/AC/Spell Slots updated
    - Hair HMI color updated (Gold pulse for Scint gain, Red pulse for Karma loss)
    - Inventory updated
    - Cycle ID incremented
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
13. Karma awarded to being's soul via KarmaMerchant
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

## Integration Flow

### Quest Completion → Karma Award

```python
# When ticket is completed:
1. ChallengeSystem.record_completion() called
2. Calculate points and karma (by type)
3. Get being's soul_id from BeingSystem
4. Award karma to soul via KarmaMerchant:
   karma_merchant.award_karma(
       soul_id=soul_id,
       karma_by_type=karma_earned,
       source="quest_completion",
       metadata={
           "quest_id": work_effort_id,
           "ticket_id": ticket_id,
           "being_id": being_id
       }
   )
5. Update leaderboard
6. Check for karma type discovery
```

### Karma Market Integration

```python
# Beings can see quest rewards before starting:
quest = quest_generator.get_quest_details(work_effort_id)
# Returns: {
#   "karma_rewards": {"code_karma": 15.0, "test_karma": 10.0},
#   "required_abilities": ["code_editor", "test_runner"],
#   "difficulty": "MEDIUM"
# }

# Beings check if they have required abilities (purchased with karma)
# If not, they can spend karma to buy them in KarmaMarket
```

## Future Enhancements

- Weekly/monthly leaderboards
- Achievement system (e.g., "First to complete 10 tickets")
- Team/group challenges
- Difficulty ratings for work efforts
- Time-based challenges (e.g., "Complete 5 tickets in 24 hours")
- Karma type trading/exchange
- Quest chains (complete quest A to unlock quest B)
- Seasonal quests with special karma types