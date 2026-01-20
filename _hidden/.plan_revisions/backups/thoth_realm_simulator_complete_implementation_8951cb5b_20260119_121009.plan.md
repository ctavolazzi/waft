---
name: Thoth Realm Simulator Complete Implementation
overview: "Complete implementation plan for Thoth Realm Simulator covering 6 phases: Core Functionality (Prime Directive tracking, Being lifecycle, Tool ledgers), Armory System (tool management with Keeper + Assistants), Being Intelligence (learning/memory), Visualization enhancements, PDF Generation, and Realm Documentation Evolution."
todos:
  - id: phase1-realm-being-dataclass
    content: Update RealmBeing dataclass with Beyond connection fields, progress tracking, and state management
    status: pending
  - id: phase1-realm-creation
    content: "Implement proper Realm creation process: Rules → Access Point → Prime Being → Tether"
    status: pending
  - id: phase1-being-selection
    content: "Implement Being selection system: bubbling, selection, frozen/queued storage"
    status: pending
  - id: phase1-prime-directive-progress
    content: Implement Prime Directive progress tracking and success condition checking
    status: pending
  - id: phase1-being-lifecycle
    content: "Implement Being lifecycle management: aging, death, tool return"
    status: pending
  - id: phase1-tool-ledger
    content: Implement actual tool ledger file storage with hash chain
    status: pending
  - id: phase2-armory-class
    content: Create Armory class for tool storage, lending, and retrieval
    status: pending
  - id: phase2-armory-beings
    content: Create ArmoryKeeper and ArmoryAssistant classes
    status: pending
  - id: phase2-armory-integration
    content: "Integrate Armory system into simulator: lending, retrieval, monitoring"
    status: pending
  - id: phase3-being-memory
    content: Implement Being learning and memory system
    status: pending
  - id: phase4-visualization
    content: Add progress bars and tool evolution visualization to web interface
    status: pending
  - id: phase5-pdf-generator
    content: Create SimulationPDFGenerator class using WAFT ScientificPDFGenerator
    status: pending
  - id: phase5-pdf-hooks
    content: "Integrate PDF generation hooks: milestones, periodic, completion"
    status: pending
  - id: phase6-documentation-system
    content: Create RealmDocumentationSystem with tier evolution
    status: pending
  - id: phase6-documentation-integration
    content: Integrate documentation system into simulator with evolution checks
    status: pending
---

# Thoth Realm Simulator - Step-by-Step Implementation Plan

## Current State Analysis

**Working:**

- Realm creation with Prime Beings
- Being spawning and prayer system
- Tool granting and use
- Tool evolution (common → legendary)
- Tool awareness checks
- Wake-up events
- Density threshold system
- Real-time web interface
- Console Goblin debugging
- Realm Browser for past simulations

**Missing (Critical):**

- Prime Directive progress tracking
- Being lifecycle (death/completion)
- Actual tool ledger file storage
- Tool return/retrieval system
- Armory beings (Keeper + Assistants)
- Being learning/memory
- PDF generation system
- Realm documentation evolution

## Phase 1: Core Functionality (Critical Gaps)

### Step 1.1: Update RealmBeing Dataclass

**File:** `simulation/thoth_realm_simulator.py`

Add new fields to `RealmBeing` dataclass:

- `beyond_tether: Optional[str]` - Tether ID connecting to Beyond
- `access_point_established: bool` - Communication boundary set
- `access_point_rules: Dict[str, Any]` - Rules for crossing boundary
- `selected_beings_frozen: List[str]` - Frozen/stored beings
- `selected_beings_queued: List[str]` - Queued for spawning
- `progress: float` - Prime Directive progress (0.0 to 1.0)
- `progress_history: List[Dict[str, Any]]` - Progress tracking over time
- `success_conditions: List[str]` - Success criteria for directive
- `state: str` - Realm state (active/completed)

### Step 1.2: Implement Realm Creation Process

**File:** `simulation/thoth_realm_simulator.py`

Update `create_realm()` method to follow proper order:

1. Set Rules of the Realm (before anyone lives there)
2. Create Prime Being (maintains connection to Beyond)
3. Establish Access Point (communication boundary)
4. Create Tether to Beyond
5. Initialize documentation system (Phase 6)

Add initialization in `__init__`:

- `self.bubbling_beings: Dict[str, List[Dict[str, Any]]]` - realm_id -> bubbled beings
- `self.selected_beings_frozen: Dict[str, List[str]]` - realm_id -> frozen being IDs
- `self.selected_beings_queued: Dict[str, List[str]]` - realm_id -> queued being IDs

### Step 1.3: Implement Being Selection System

**File:** `simulation/thoth_realm_simulator.py`

Add three methods:

1. `beings_bubble_up(realm_id: str)` - Beings naturally bubble up in Realm

- Random chance based on density (max 30% per cycle)
- Creates bubbling being data with attributes (potential, alignment, readiness)
- Stores in `self.bubbling_beings`

2. `prime_being_selects_beings(realm_id: str)` - Prime Being evaluates and selects

- Evaluates each bubbling being
- High potential + high alignment → queue for spawning
- High potential + low readiness → freeze for later
- Low potential → ignore
- Updates realm tracking lists

3. `spawn_from_queued(realm_id: str)` - Spawn worker being from queued

- Pops next queued being ID
- Spawns as worker being
- Creates event

Add storage method:

- `_save_frozen_beings(realm_id: str)` - Save frozen beings to `_simulations/{simulation_id}/realms/{realm_id}/frozen_beings.json`

### Step 1.4: Update run_cycle for Being Selection

**File:** `simulation/thoth_realm_simulator.py`

In `run_cycle()`, add:

- Call `beings_bubble_up()` for each realm
- Every 5 cycles, call `prime_being_selects_beings()`
- Spawn from queued beings (30% chance) instead of random spawning

### Step 1.5: Implement Prime Directive Progress Tracking

**File:** `simulation/thoth_realm_simulator.py`

Add methods:

1. `_evaluate_prime_directive_progress(realm_id: str) -> float`

- Calculates progress based on:
 - Tool usage ratio (30% weight)
 - Legendary tool ratio (30% weight)
 - Awareness ratio (20% weight)
 - Density ratio (20% weight)
- Returns 0.0 to 1.0

2. `_check_prime_directive_success(realm_id: str) -> bool`

- Checks if progress >= 0.8
- Has at least one legendary tool
- Directive-specific checks (e.g., aware tools for awareness directives)
- Returns True if achieved

Update `run_cycle()`:

- After processing beings, evaluate progress
- Append to `realm.progress_history`
- Check for success, mark realm as "completed" if achieved

### Step 1.6: Implement Being Lifecycle Management

**File:** `simulation/thoth_realm_simulator.py`

Add in `__init__`:

- `self.being_lifespans: Dict[str, int]` - being_id -> lifespan_cycles
- `self.being_ages: Dict[str, int]` - being_id -> current_age

Update `spawn_worker_being()`:

- Assign random lifespan (50-200 cycles)
- Initialize age tracking

Add methods:

1. `_age_beings()` - Age all beings and check for death

- Increment age for all beings
- Check if age >= lifespan
- Call `_being_dies()` for dead beings

2. `_being_dies(being_id: str)` - Handle Being death

- Return all tools held by being (set `current_holder = None`)
- Remove from realm's `spawned_beings`
- Remove from tracking dictionaries
- Create "being_died" event
- Decrement metrics

Update `run_cycle()`:

- Call `_age_beings()` at start of cycle

### Step 1.7: Implement Tool Ledger Storage

**File:** `simulation/thoth_realm_simulator.py`

Add dataclass:

- `ToolLedgerEntry` - Immutable ledger entry with:
- `entry_id`, `timestamp`, `being_id`, `action`, `context`
- `spiritual_energy_before`, `spiritual_energy_after`
- `previous_hash`, `entry_hash` (for hash chain)

Add method:

- `_append_to_tool_ledger(tool: Tool, entry: ToolLedgerEntry)`
- Reads last entry to get previous hash
- Calculates entry hash
- Appends to `_simulations/{simulation_id}/tools/{tool_id}_ledger.jsonl`

Update `being_uses_tool()`:

- Create `ToolLedgerEntry` with energy before/after
- Call `_append_to_tool_ledger()`

## Phase 2: Armory System (Tool Management)

### Step 2.1: Create Armory Class

**File:** `simulation/armory.py` (new file)

Create `Armory` class with:

- `__init__(project_path: Path, simulation_id: str)`
- `tools_in_armory: Dict[str, Tool]` - tool_id -> Tool
- `tools_lent_out: Dict[str, ToolTether]` - tool_id -> Tether
- `tags: Dict[str, ToolTag]` - tag_id -> Tag
- `tethers: Dict[str, ToolTether]` - tether_id -> Tether

Add dataclasses:

- `ToolTag` - Unique identifier tag for tool
- `ToolTether` - Connection between tool and being/realm

Methods:

- `store_tool(tool: Tool) -> ToolTag` - Store tool, create tag
- `lend_tool(tool_id: str, being_id: str, realm_id: str) -> Optional[ToolTether]` - Lend tool, create tether
- `retrieve_tool(tool_id: str, reason: str) -> bool` - Retrieve tool back
- `_save_armory_state()` - Save to `_simulations/{simulation_id}/armory/armory_state.json`

### Step 2.2: Create Armory Beings System

**File:** `simulation/armory_beings.py` (new file)

Create two dataclasses:

1. `ArmoryKeeper` - Global keeper managing all tools

- `being_id`, `skills`, `knowledge`
- Methods:
 - `evaluate_prayer_request()` - Evaluate if Being should receive tool
 - `catalog_tool()` - Catalog tool in knowledge base
 - `monitor_usage()` - Monitor and record tool usage patterns

2. `ArmoryAssistant` - Per-Realm assistant

- `being_id`, `realm_id`, `skills`, `local_knowledge`
- Methods:
 - `request_tool_retrieval()` - Request tool retrieval
 - `maintain_local_ledger()` - Maintain local ledger copy

### Step 2.3: Integrate Armory into Simulator

**File:** `simulation/thoth_realm_simulator.py`

In `__init__`:

- Import and create `Armory` instance
- Create global `ArmoryKeeper`
- Track `self.armory_assistants: Dict[str, ArmoryAssistant]`

In `create_realm()`:

- Spawn `ArmoryAssistant` for new realm
- Store assistant as Being in system

In `being_prays_for_tool()`:

- Get realm's Armory Assistant
- Armory Keeper evaluates request
- If approved, create tool and catalog it
- Lend from Armory using `armory.lend_tool()`

In `being_uses_tool()`:

- Armory Keeper monitors usage
- Update Being's history in Keeper's knowledge

In `_being_dies()`:

- Assistant requests tool retrieval
- Use `armory.retrieve_tool()`

In `_create_tool()`:

- Store tool in Armory using `armory.store_tool()`

## Phase 3: Being Intelligence (Learning & Memory)

### Step 3.1: Implement Being Memory System

**File:** `simulation/thoth_realm_simulator.py`

Add in `__init__`:

- `self.being_memories: Dict[str, List[Dict[str, Any]]]` - being_id -> memories

Update `being_uses_tool()`:

- Create memory entry with cycle, tool_id, success, energy_gained, wake_event
- Append to being's memories (keep last 50)
- Call `_being_learns_from_experience()`

Add method:

- `_being_learns_from_experience(being_id: str, memory: Dict[str, Any])`
- Improve prayer skill if tool use was successful
- Learn which tools work best
- Increase learning skill after 5+ successful uses

## Phase 4: Visualization & Analytics

### Step 4.1: Add Prime Directive Progress Visualization

**File:** `simulation/simulation_viewer.html`

Add to realm display:

- Progress bar showing `realm.progress * 100`
- Progress percentage text
- CSS styling for progress bars

### Step 4.2: Add Tool Evolution Visualization

**File:** `simulation/simulation_viewer.html`

Add tool evolution timeline:

- Display tools with their legendary status
- Color-code by tier
- Show evolution progression

## Phase 5: PDF Generation System

### Step 5.1: Create Simulation PDF Generator

**File:** `simulation/simulation_pdf_generator.py` (new file)

Create `SimulationPDFGenerator` class:

- `__init__(simulator: ThothRealmSimulator)`
- Uses `ScientificPDFGenerator.from_content()` from WAFT

Methods:

- `generate_completion_pdf() -> Path` - After simulation completes
- `generate_milestone_pdf(milestone_type: str, milestone_data: Dict) -> Path` - At key milestones
- `generate_periodic_pdf(cycle: int) -> Path` - Every N cycles

Content building methods:

- `_build_completion_content()` - Full simulation report
- `_build_milestone_content()` - Milestone-specific report
- `_build_periodic_content()` - Periodic status report
- `_format_metrics_table()` - Metrics as markdown table
- `_format_realm_outcomes()` - Realm outcomes summary
- `_format_tool_evolution()` - Tool evolution data
- `_format_being_lifecycle()` - Being lifecycle stats
- `_format_events_timeline()` - Key events timeline
- `_format_tool_ledger_summary()` - Tool ledger summary
- `_format_frozen_beings()` - Frozen beings data
- `_format_reproducibility_data()` - System info, config, file locations

### Step 5.2: Integrate PDF Generation Hooks

**File:** `simulation/thoth_realm_simulator.py`

In `__init__`:

- Import and create `SimulationPDFGenerator` instance

In `_check_prime_directive_success()`:

- Generate milestone PDF when directive achieved

In `_check_tool_awareness()`:

- Generate milestone PDF when tool becomes aware

In `run_cycle()`:

- Generate periodic PDF every 100 cycles

Add method:

- `stop_simulation()` - Generate completion PDF

**File:** `simulation/simulation_server.py`

Add endpoint:

- `POST /api/simulation/{simulation_id}/generate-pdf` - On-demand PDF generation

## Phase 6: Realm Documentation Evolution System

### Step 6.1: Create Realm Documentation System

**File:** `simulation/realm_documentation.py` (new file)

Create `DocumentationTier` enum:

- BASIC_ENGLISH (0)
- STRUCTURED_MARKDOWN (1)
- SCIENTIFIC_FORMAT (2)
- ADVANCED_TEMPLATES (3)
- CUSTOM_DOCUMENTATION (4)

Create `RealmDocumentationSystem` class:

- `__init__(realm_id: str, simulation_path: Path)`
- `current_tier: DocumentationTier`
- `documentation_history: List[Dict[str, Any]]`
- `docs_generated: int`, `docs_quality_score: float`

Methods:

- `check_evolution(realm, simulator) -> bool` - Check if ready to evolve tier
- `evolve_tier(realm, simulator)` - Evolve to next tier
- `generate_documentation(doc_type, content, realm, simulator) -> Path`
- `_generate_basic_english()` - Tier 0: Simple text
- `_generate_markdown()` - Tier 1: Structured markdown
- `_generate_scientific()` - Tier 2: Scientific format
- `_generate_advanced_template()` - Tier 3: LaTeX/Typst
- `_generate_custom()` - Tier 4: Custom style
- `_load_state()`, `_save_state()` - Persistence

### Step 6.2: Integrate Documentation System

**File:** `simulation/thoth_realm_simulator.py`

In `__init__`:

- Track `self.realm_documentation: Dict[str, RealmDocumentationSystem]`

In `create_realm()`:

- Initialize documentation system (starts at Tier 0)
- Generate initial "realm_creation" documentation

In `run_cycle()`:

- Check documentation evolution every cycle
- Generate periodic documentation every 50 cycles

In `_check_prime_directive_success()`:

- Generate milestone documentation when directive achieved

## Implementation Order

**Phase 1 (Critical - Do First):**

1. Update RealmBeing dataclass (Step 1.1)
2. Implement Realm Creation Process (Step 1.2)
3. Implement Being Selection System (Step 1.3-1.4)
4. Implement Prime Directive Progress Tracking (Step 1.5)
5. Implement Being Lifecycle Management (Step 1.6)
6. Implement Tool Ledger Storage (Step 1.7)

**Phase 2 (Important - Do Second):**

7. Create Armory Class (Step 2.1)
8. Create Armory Beings System (Step 2.2)
9. Integrate Armory into Simulator (Step 2.3)

**Phase 3 (Enhancement - Do Third):**

10. Implement Being Memory System (Step 3.1)

**Phase 4 (Polish - Do Fourth):**

11. Add Visualization Enhancements (Step 4.1-4.2)

**Phase 5 (Documentation - Do Fifth):**

12. Create Simulation PDF Generator (Step 5.1)
13. Integrate PDF Generation Hooks (Step 5.2)

**Phase 6 (Advanced - Do Last):**

14. Create Realm Documentation System (Step 6.1)
15. Integrate Documentation System (Step 6.2)

## Testing Strategy

After each phase:

1. Run simulation for 100+ cycles
2. Verify features work as expected
3. Check Console Goblin for errors
4. Verify data persistence (ledgers, snapshots, armory state)
5. Test Realm Browser can load past simulations
6. Verify Armory beings are spawned and functioning
7. Check PDFs are generated correctly
8. Verify documentation evolution works

## Success Criteria

- Prime Directives can be achieved and tracked
- Beings have meaningful lifecycles (spawn, work, die)
- Tool ledgers are stored and retrievable
- Armory Keeper and Assistants manage tools effectively
- Tools can be returned to Armory on death
- Beings learn from experience
- Visualization shows progress clearly
- PDFs are automatically generated at milestones and completion
- PDFs contain all necessary information for proof and peer review
- PDFs enable full reproducibility of simulation runs
- Realm documentation evolves based on progress