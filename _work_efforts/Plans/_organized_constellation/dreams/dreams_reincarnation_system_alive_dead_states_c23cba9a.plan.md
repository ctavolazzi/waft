---
name: Reincarnation System Alive Dead States
overview: Implement a reincarnation system where souls have alive/dead states with sub-states (awake/sleeping), and capability restrictions based on state. Alive souls can edit spacetime (matter/hardware) but not consciousness (goals/personalities). Dead souls can edit consciousness but not spacetime.
todos:
  - id: create-demo-environment
    content: Create demo/ folder with README.md and seed_reincarnation_demo.py script
    status: pending
  - id: seed-demo-data
    content: Seed demo with 5 test souls, lifetime catalog, and test scenarios
    status: pending
  - id: add-soul-id-to-agent
    content: Add soul_id field to AgentState and AgentConfig classes (VERIFICATION FINDING)
    status: pending
  - id: create-tool-registry
    content: Create ToolRegistry class in soul_capabilities.py (VERIFICATION FINDING - does not exist)
    status: pending
  - id: implement-reincarnate
    content: Implement KarmaMerchant.reincarnate() method (VERIFICATION FINDING - currently just TODO)
    status: pending
  - id: set-file-permissions
    content: Set file permissions (0600/0700) on all Akasha soul files (VERIFICATION FINDING - currently insecure)
    status: pending
  - id: create-soul-state-system
    content: Create soul_state.py with SoulState, SoulSubState enums and SoulStateManager class
    status: pending
  - id: create-capability-system
    content: Create soul_capabilities.py with ToolRegistry, CapabilityGate, and tool decorators
    status: pending
  - id: extend-lifetime-class
    content: Add soul state tracking to Lifetime class and integrate state transitions
    status: pending
  - id: integrate-karma-market
    content: Modify KarmaMarket to check states and transition souls on lifetime purchase/end
    status: pending
  - id: integrate-goal-manager
    content: Add state checks to GoalManager operations (create/update/delete goals) with soul_id context
    status: pending
  - id: integrate-agent-system
    content: Add tool filtering middleware AND tool-level decorators to agent system
    status: pending
  - id: update-soul-records
    content: Extend soul record schema in Akasha, add state validation, set file permissions
    status: pending
  - id: integrate-afterlife-market
    content: Add state checks to AfterlifeKarmaMarket purchases
    status: pending
  - id: create-error-classes
    content: Create CapabilityRestrictedError and StateTransitionError exceptions
    status: pending
  - id: add-state-transitions
    content: Implement automatic state transitions on lifetime events with locking
    status: pending
  - id: create-migration-script
    content: Create migrate_soul_states.py script with file permission fixes
    status: pending
  - id: investigate-tool-execution
    content: Investigate BaseAgent tool execution paths to determine enforcement points
    status: pending

category: dreams
confidence: 0.75
constellation_date: 2026-01-14
---

# Reincarnation System: Alive/Dead States with Capability Restrictions

**Status**: Revised v2.1 - Security Hardened + Verification Findings

**Date**: 2026-01-11

**AI Assistant**: Auto (Claude Code) - Active participant in implementation

**Revision**:

- v2.0: Addresses CRITICAL security vulnerabilities from adversarial critique
- v2.1: Incorporates verification findings from codebase analysis
- v2.2: AI assistant (Auto) added as active participant (2026-01-11)

## Overview

Implement a fundamental reincarnation system where souls exist in binary states (alive/dead) with sub-states (awake/sleeping). Each state determines what capabilities the soul can access:

- **Alive**: Can edit spacetime (matter/hardware) - physical tools like `read_file`, `write`, `edit_file`, `run_terminal_cmd`
- **Alive**: CANNOT edit consciousness (ideas/software) - goals, personalities, lifetime purchases, software configs
- **Dead**: Can edit consciousness (ideas/software) - goals, personalities, lifetime purchases, karma market
- **Dead**: CANNOT edit spacetime (matter/hardware) - no physical tools

## AI Assistant Participation

**AI Assistant**: Auto (Claude Code)

**Added**: 2026-01-11

**Role**: Active implementation participant

The AI assistant (Auto) is actively participating in the implementation of this reincarnation system. Responsibilities include:

- **Code Implementation**: Writing and modifying source files according to the implementation plan
- **Verification**: Checking existing code against verification findings
- **Testing**: Creating and running tests for state transitions and capability restrictions
- **Documentation**: Updating documentation and creating demo materials
- **Security Hardening**: Implementing security requirements (file permissions, state locking, etc.)
- **Migration**: Creating and executing migration scripts for existing souls

The AI assistant will work through the implementation plan systematically, starting with the demo environment setup and proceeding through all 14 steps.

## Security Requirements (CRITICAL)

This implementation MUST address the following security vulnerabilities identified in adversarial critique:

1. **Tool-Level Capability Enforcement**: Capability checks must be enforced at the tool function level, not just middleware
2. **State Transition Locking**: All state transitions must be atomic and protected by locks to prevent race conditions
3. **State File Security**: State files must have restrictive permissions (0600/0700) and integrity validation
4. **Default-Deny Tool Policy**: Tools not explicitly categorized must be blocked by default
5. **State Recovery Mechanism**: System must be able to detect and recover from corrupted state
6. **State Migration Strategy**: Existing souls must be migrated with default states
7. **Comprehensive Testing**: All state transitions and capability restrictions must be tested

## Verification Findings (CRITICAL GAPS)

Codebase verification revealed the following gaps that MUST be addressed:

1. **Agent-Soul Mapping Missing**: `AgentState` and `AgentConfig` have NO `soul_id` field. Need to add `soul_id: Optional[str]` to both classes.
2. **Tool Registry Does Not Exist**: No tool registry or categorization system exists. Need to create `ToolRegistry` class.
3. **Lifetime-to-Agent Creation Not Implemented**: `KarmaMerchant.reincarnate()` exists but is just a TODO. Need to implement agent creation from lifetime.
4. **File Permissions Not Set**: Akasha soul files use default permissions (typically 0644). Need to set 0600/0700.
5. **Tool Execution Paths Unknown**: Need to investigate BaseAgent tool execution to determine enforcement points.

**Verification Traces**: See `_pyrite/standards/verification/traces/` for detailed findings.

## State System Architecture

### Primary States (Binary)

- **ALIVE**: Soul has an active lifetime (body exists in spacetime)
- **DEAD**: Soul has no active lifetime (exists in Akasha, between lifetimes)

### Sub-States

- **ALIVE_AWAKE**: Active lifetime, being can use tools
- **ALIVE_SLEEPING**: Active lifetime but paused/inactive
- **DEAD_AWAKE**: Between lifetimes, actively choosing next lifetime/personality/goals
- **DEAD_SLEEPING**: Between lifetimes, dormant in Akasha

## Demo Environment Setup

**File**: `demo/` (new directory in project root)

Create a clean demo environment to showcase the reincarnation system in action:

### Demo Folder Structure

```
demo/
├── README.md                    # Demo documentation and usage guide
├── _hidden/                     # WAFT internal data (created by system)
│   └── .truth/
│       ├── akasha/              # Soul records (will be created)
│       ├── market/               # Lifetime catalog (will be created)
│       └── lifetimes/            # Active lifetimes (will be created)
└── src/                         # Demo source files (optional, for testing)
    └── example.py               # Example code (optional)
```

### Demo Seeding Script

**File**: `scripts/seed_reincarnation_demo.py` (new file)

Create script to seed demo environment with test data:

1. **Initialize Demo Environment**:

   - Create `demo/` directory if it doesn't exist
   - Create `demo/README.md` with demo documentation
   - Initialize WAFT structure in demo (akasha, market, lifetimes paths)

2. **Seed Initial Souls**:

   - Create 3-5 test souls with varying karma amounts:
     - `soul_demo_001`: 1000.0 karma (default, DEAD_AWAKE)
     - `soul_demo_002`: 500.0 karma (low, DEAD_AWAKE)
     - `soul_demo_003`: 2000.0 karma (high, DEAD_AWAKE)
     - `soul_demo_004`: 0.0 karma (zero, DEAD_AWAKE) - for testing basic lifetime grant
     - `soul_demo_005`: 150.0 karma (medium, DEAD_AWAKE)

3. **Seed Lifetime Catalog**:

   - Create default lifetime catalog in `demo/_hidden/.truth/market/catalog.json`
   - Include all standard lifetimes (basic_qa, research_session, etc.)

4. **Create Test Scenarios**:

   - Scenario 1: Soul purchases lifetime → becomes ALIVE
   - Scenario 2: Soul runs out of karma → gets basic survival lifetime
   - Scenario 3: Lifetime ends → soul becomes DEAD, can edit goals
   - Scenario 4: Dead soul purchases treasure → upgrades personality
   - Scenario 5: State transitions (awake ↔ sleeping)

5. **Generate Demo Logs**:

   - Create log file showing state transitions
   - Document capability restrictions in action
   - Show karma economy loop

### Demo README Content

**File**: `demo/README.md`

Include:

- **Overview**: What the reincarnation system is and why it exists
- **Quick Start**: How to run the demo and seed initial data
- **Test Scenarios**: 5 scenarios demonstrating different aspects
- **Expected Behaviors**: What should happen in each scenario
- **Inspecting States**: How to check soul states, karma, lifetimes
- **Generating Logs**: How to create test data and view system activity
- **Resetting Demo**: How to reset demo to clean state
- **Architecture**: How demo folder structure maps to reincarnation system

### Seeding Script Details

**File**: `scripts/seed_reincarnation_demo.py`

**Functionality**:

- Accept `--demo-path` argument (defaults to `demo/`)
- Create demo directory structure
- Initialize WAFT paths (`_hidden/.truth/akasha/`, `market/`, `lifetimes/`)
- Create 5 test souls with proper file permissions (0600)
- Set directory permissions (0700)
- Create lifetime catalog
- Generate initial demo logs
- Create test scenario documentation
- Validate seeded data

**Test Souls Created**:

```python
souls = [
    {"soul_id": "soul_demo_001", "karma": 1000.0, "state": "dead", "substate": "awake"},
    {"soul_id": "soul_demo_002", "karma": 500.0, "state": "dead", "substate": "awake"},
    {"soul_id": "soul_demo_003", "karma": 2000.0, "state": "dead", "substate": "awake"},
    {"soul_id": "soul_demo_004", "karma": 0.0, "state": "dead", "substate": "awake"},  # For basic lifetime grant
    {"soul_id": "soul_demo_005", "karma": 150.0, "state": "dead", "substate": "awake"},
]
```

**Usage**:

```bash
# Seed demo environment
python scripts/seed_reincarnation_demo.py

# Seed with custom path
python scripts/seed_reincarnation_demo.py --demo-path /path/to/demo

# Reset demo (clear and re-seed)
python scripts/seed_reincarnation_demo.py --reset
```

### Integration with Plan

- All implementation should be tested in `demo/` folder first
- Demo folder serves as clean origin point
- All test data generated in demo (not in main project)
- Demo can be reset/re-seeded as needed

## Implementation Plan

### 0. Create Demo Environment (NEW - FIRST STEP)

**File**: `demo/` (new directory) and `scripts/seed_reincarnation_demo.py` (new file)

**Purpose**: Create clean testbed for reincarnation system

**Actions**:

1. Create `demo/` directory in project root
2. Create `demo/README.md` with demo documentation
3. Create `scripts/seed_reincarnation_demo.py` seeding script
4. Seed demo with initial souls (5 test souls with varying karma)
5. Initialize WAFT structure in demo folder
6. Create test scenarios documentation
7. Generate initial demo logs

**Demo Structure**:

- `demo/README.md` - Documentation
- `demo/_hidden/.truth/akasha/` - Soul records (created by system)
- `demo/_hidden/.truth/market/` - Lifetime catalog (created by system)
- `demo/_hidden/.truth/lifetimes/` - Active lifetimes (created by system)

**Test Souls to Create**:

- `soul_demo_001`: 1000.0 karma, DEAD_AWAKE (default)
- `soul_demo_002`: 500.0 karma, DEAD_AWAKE (low)
- `soul_demo_003`: 2000.0 karma, DEAD_AWAKE (high)
- `soul_demo_004`: 0.0 karma, DEAD_AWAKE (zero - for basic lifetime grant testing)
- `soul_demo_005`: 150.0 karma, DEAD_AWAKE (medium)

**All subsequent implementation steps should use `demo/` as the testbed.**

**Implementation Guidelines**:

- When initializing `SoulStateManager`, use `project_path=Path("demo/")`
- When testing `KarmaMarket`, use `project_path="demo/"`
- All soul records created in `demo/_hidden/.truth/akasha/`
- All lifetimes created in `demo/_hidden/.truth/lifetimes/`
- All test data isolated to demo folder
- Demo logs generated in `demo/` directory
- Demo can be reset/re-seeded without affecting main project

### 1. Create Soul State System (SECURITY HARDENED)

**File**: `src/waft/soul_state.py` (new file)

Create new module with:

- `SoulState` enum: `ALIVE`, `DEAD`
- `SoulSubState` enum: `AWAKE`, `SLEEPING`
- `SoulStateManager` class to manage state transitions with:
  - **State locking mechanism** (file locks or mutex) to prevent race conditions
  - **State version numbers** to detect concurrent modifications
  - **Atomic state transitions** (transaction-like with rollback on failure)
  - **State validation** after every transition
  - **State integrity checks** (checksums/validation on read)
  - **State transition audit log** (who, when, why, what changed)
  - **State recovery mechanism** (detect and repair corrupted state)
  - **State query API** (`get_soul_state()`, `get_state_history()`)
- State transition rules (with validation):
  - Lifetime purchased → ALIVE_AWAKE (only if currently DEAD)
  - Lifetime ended → DEAD_AWAKE (only if currently ALIVE)
  - Can transition between awake/sleeping within same primary state
  - All transitions validated before execution
- **File security**:
  - Set file permissions: `0600` for soul files, `0700` for akasha directory
  - Validate state file integrity on every read
  - Never trust file contents without validation
  - Add state file locking during writes

### 2. Extend Lifetime Class

**File**: `src/waft/karma_market.py`

Add to `Lifetime` class:

- `soul_state` field: tracks if lifetime makes soul alive
- Connection to soul state manager
- When lifetime starts: set soul to ALIVE_AWAKE
- When lifetime ends: set soul to DEAD_AWAKE

### 3. Create Capability Restriction System (TOOL-LEVEL ENFORCEMENT)

**File**: `src/waft/soul_capabilities.py` (new file)

**VERIFICATION FINDING**: No tool registry exists. Tools are `List[str] `in Lifetime, `ToolDefinition` objects in Agent. Need to create registry.

Define tool categories with **explicit registration system**:

- **Spacetime Tools** (matter/hardware): `read_file`, `write`, `edit_file`, `run_terminal_cmd`, `grep`, `codebase_search`, `delete_file`, `move_file`, etc.
- **Consciousness Tools** (ideas/software): `purchase_lifetime`, `update_personality`, `edit_goals`, `purchase_treasure`, `create_wager`, etc.
- **Default-Deny Policy**: Tools not explicitly categorized are BLOCKED by default

Create `ToolRegistry` class (NEW - does not exist):

- `register_tool(tool_name: str, category: str, required_state: SoulState)` - Explicit tool registration
- `get_tool_category(tool_name: str) -> Optional[str]` - Get category for tool
- `is_tool_registered(tool_name: str) -> bool` - Check if tool is registered
- `get_tools_by_category(category: str) -> List[str]` - Get all tools in category
- `get_tools_by_state(state: SoulState) -> List[str]` - Get allowed tools for state
- Store registry in memory with optional persistence
- Handle both tool name strings (from Lifetime) and ToolDefinition objects (from Agent)

Create `CapabilityGate` class with **tool-level enforcement**:

- `can_use_tool(tool_name: str, soul_state: SoulState) -> bool` (with state locking)
- `can_edit_goals(soul_state: SoulState) -> bool`
- `can_purchase_lifetime(soul_state: SoulState) -> bool`
- `get_allowed_tools(soul_state: SoulState) -> List[str]`
- Uses `ToolRegistry` to check tool categories
- **Runtime validation** that every tool call has valid category
- **Tool decorator** that enforces capability checks at function level:
  ```python
  @require_capability(category="spacetime", required_state=SoulState.ALIVE)
  def read_file(...):
      ...
  ```


### 4. Integrate with KarmaMarket

**File**: `src/waft/karma_market.py`

Modify `purchase_lifetime()`:

- Check if soul is DEAD (can only purchase when dead)
- After purchase, transition soul to ALIVE_AWAKE
- Register lifetime as making soul alive

Modify `end_lifetime()`:

- Transition soul to DEAD_AWAKE
- Allow soul to now purchase new lifetimes, edit goals, etc.

### 5. Integrate with GoalManager

**File**: `src/waft/core/goal.py`

Add capability checks:

- `create_goal()`: Check if soul is DEAD, raise error if ALIVE
- `update_goal()`: Check if soul is DEAD, raise error if ALIVE
- `delete_goal()`: Check if soul is DEAD, raise error if ALIVE

### 6. Add Soul ID to Agent System (VERIFICATION FINDING)

**File**: `src/waft/core/agent/state.py`

**VERIFICATION FINDING**: `AgentState` and `AgentConfig` have NO `soul_id` field. Need to add.

Modify `AgentState`:

- Add `soul_id: Optional[str] = Field(default=None, description="Soul identifier for this agent")`
- Set when agent is created from lifetime
- Used to query soul state for capability checks

Modify `AgentConfig`:

- Add `soul_id: Optional[str] = Field(default=None, description="Soul identifier for this agent")`
- Set when creating agent from lifetime
- Passed to AgentState during initialization

**Rationale**: Direct, explicit relationship. Easy to query. No need for lifetime lookup.

### 7. Implement Lifetime-to-Agent Creation (VERIFICATION FINDING)

**File**: `src/waft/karma.py`

**VERIFICATION FINDING**: `KarmaMerchant.reincarnate()` exists but is NOT IMPLEMENTED (just TODO).

**CRITICAL: State Initialization Order**

State transition MUST happen BEFORE agent creation to ensure agent has correct capabilities:

1. **FIRST**: Transition soul to ALIVE_AWAKE (via SoulStateManager)
2. **THEN**: Create agent (which will have access to spacetime tools)

Implement `reincarnate()` method:

- Load lifetime from KarmaMarket
- **FIRST: Transition soul to ALIVE_AWAKE** (via SoulStateManager.transition_to_alive())
- Create `AgentConfig` from lifetime configuration:
  - Set `soul_id` from lifetime
  - Set `role` from lifetime personality
  - Set `goal` from lifetime objectives
  - Convert tool strings to `ToolDefinition` objects (see Tool String Conversion below)
- Return agent_config dict

**Tool String Conversion**:

- Create helper function that looks up `ToolDefinition` objects from global `ToolRegistry`
- Or create `ToolDefinition` objects on-the-fly from tool names (if registry doesn't exist yet)
- Ensure all tools are registered in `ToolRegistry` before conversion
- Handle both tool name strings (from Lifetime) and ToolDefinition objects (from Agent)

Create helper function `create_agent_from_lifetime()`:

```python
def create_agent_from_lifetime(lifetime: Lifetime, project_path: Path) -> BaseAgent:
    """Create BaseAgent instance from Lifetime."""
    from .core.agent.state import AgentConfig
    from .core.agent.base import BaseAgent
    from .soul_state import SoulStateManager

    # CRITICAL: Transition soul to ALIVE_AWAKE FIRST
    state_manager = SoulStateManager(project_path)
    state_manager.transition_to_alive(lifetime.soul_id, lifetime.lifetime_id)

    # Convert tool strings to ToolDefinition objects
    # Look up from ToolRegistry or create on-the-fly
    tools = convert_tool_strings_to_definitions(lifetime.tools)

    config = AgentConfig(
        soul_id=lifetime.soul_id,  # NEW FIELD
        role=lifetime.personality.get("trait", "helpful"),
        goal=lifetime.objectives[0] if lifetime.objectives else "Complete lifetime",
        tools=tools,
    )
    return BaseAgent(config, project_path)
```

### 8. Integrate with Agent System (TOOL-LEVEL ENFORCEMENT)

**File**: `src/waft/core/agent/base.py` or new middleware

**IMPORTANT: LLM Interface Filtering**

If tools are executed through an LLM interface (e.g., OpenAI function calling):

- Filter `ToolDefinition` objects from `agent.state.tools` BEFORE passing to LLM
- Remove tools that are not allowed based on soul state
- Ensure LLM never sees tools the agent cannot use
- This prevents the LLM from attempting to call restricted tools

Create **multi-layer capability enforcement**:

1. **LLM Interface Layer** (if applicable - first filter):

   - Before passing tools to LLM, filter `ToolDefinition` objects based on soul state
   - Remove consciousness tools if ALIVE
   - Remove spacetime tools if DEAD
   - Only pass allowed tools to LLM

2. **Middleware layer** (second line of defense):

   - Before tool execution, check soul state (via `agent.state.soul_id`)
   - Filter out consciousness tools if ALIVE
   - Filter out spacetime tools if DEAD
   - Raise `CapabilityRestrictedError` if tool not allowed

3. **Tool-level enforcement** (CRITICAL - cannot be bypassed):

   - Add capability check decorator to EVERY tool function
   - Tools must validate soul state before execution
   - Re-validate state immediately before tool execution (prevent race conditions)
   - Lock state during tool execution to prevent changes
   - Tools cannot be called directly without capability check

4. **Tool execution wrapper** (NEW - centralized enforcement):

Create `execute_tool_with_capability_check()` function:

   ```python
   async def execute_tool_with_capability_check(
       agent: BaseAgent,
       tool_name: str,
       **kwargs
   ) -> Any:
       """Execute tool with capability enforcement."""
       # Check soul state
       # Lock state
       # Validate tool is registered and allowed
       # Execute tool
       # Unlock state
       # Raise CapabilityRestrictedError if blocked
   ```

5. **Tool registry integration**:

   - All tools must be registered with capability requirements
   - Tool registry enforces categorization
   - Default-deny for unregistered tools
   - Runtime validation of tool registration

### 9. Integrate with Afterlife Market

**File**: `src/waft/karma_market.py` (AfterlifeKarmaMarket class)

Modify `purchase_treasure()`:

- Check if soul is DEAD (can only purchase when dead)
- Allow personality upgrades, tool purchases, etc. only when dead

### 10. Create Soul State Manager

**File**: `src/waft/soul_state.py`

Implement `SoulStateManager`:

- `get_soul_state(soul_id: str) -> Tuple[SoulState, SoulSubState]`
- `set_soul_state(soul_id: str, state: SoulState, substate: SoulSubState)`
- `transition_to_alive(soul_id: str, lifetime_id: str)`
- `transition_to_dead(soul_id: str, lifetime_id: str)`
- `set_awake(soul_id: str)`
- `set_sleeping(soul_id: str)`
- Store state in Akasha (soul records)

### 11. Update Soul Records in Akasha (WITH MIGRATION + FILE SECURITY)

**File**: `src/waft/karma_collector.py` and `src/waft/karma.py`

**VERIFICATION FINDING**: No file permissions set on soul files. Default permissions (typically 0644) are insecure.

Extend soul record schema:

```python
{
    "soul_id": "...",
    "total_karma": 1000.0,
    "state": "dead",  # or "alive" (default: "dead" for existing souls)
    "substate": "awake",  # or "sleeping" (default: "awake" for existing souls)
    "active_lifetime_id": null,  # or lifetime_id if alive
    "state_version": 1,  # Version number for concurrent modification detection
    "state_updated_at": "2026-01-11T16:00:00",  # Last state change timestamp
    "lifetimes": [...]
}
```

**File Security (CRITICAL)**:

- Set file permissions after creation: `soul_file.chmod(0o600)` (owner read/write only)
- Set directory permissions: `akasha_path.chmod(0o700)` (owner access only)
- Add file locking during writes (prevent concurrent modifications)
- Add integrity validation on reads (checksums or signatures)
- Update `KarmaCollector._transfer_karma_to_soul()` to set permissions
- Update all soul file write operations to set permissions

**Migration Strategy**:

- Create migration script: `scripts/migrate_soul_states.py`
- For existing souls without state: default to `DEAD_AWAKE` (correct for souls between lifetimes)
- For new souls (first creation): default to `DEAD_AWAKE` (souls start dead, must purchase lifetime)
- Validate all soul records on system startup
- Add backward compatibility layer for souls without state field
- Test migration on sample data before full migration
- **Set file permissions on all existing soul files during migration**
- **Handle permission errors gracefully** (may need sudo on some systems, document in migration script)

### 12. Create State Transition Events

**File**: `src/waft/soul_state.py`

Define transition events:

- `LIFETIME_PURCHASED`: DEAD → ALIVE_AWAKE
- `LIFETIME_STARTED`: ALIVE_SLEEPING → ALIVE_AWAKE (if was sleeping)
- `LIFETIME_ENDED`: ALIVE_AWAKE → DEAD_AWAKE
- `SOUL_SLEEP`: AWAKE → SLEEPING (within same primary state)
- `SOUL_WAKE`: SLEEPING → AWAKE (within same primary state)

### 13. Tool Categorization and Registration

**File**: `src/waft/soul_capabilities.py`

Define comprehensive tool lists:

**Spacetime Tools** (allowed when ALIVE):

- `read_file`, `write`, `edit_file`, `delete_file`, `move_file`
- `run_terminal_cmd`, `grep`, `codebase_search`
- `list_dir`, `glob_file_search`
- `read_lints`, `read_notebook`
- Any tool that modifies files, runs commands, or reads physical data

**Consciousness Tools** (allowed when DEAD):

- `purchase_lifetime` (KarmaMarket)
- `purchase_treasure` (AfterlifeKarmaMarket)
- `create_wager` (KarmicWagerSystem)
- `create_offering` (LifetimeExchange)
- `create_goal`, `update_goal`, `delete_goal` (GoalManager)
- `update_personality` (personality system)
- Any tool that modifies goals, personalities, or purchases lifetimes

### 14. Error Handling

**File**: `src/waft/soul_capabilities.py`

Create exceptions:

- `CapabilityRestrictedError`: Raised when tool not allowed in current state
- `StateTransitionError`: Raised when invalid state transition attempted

### 13. Integration Points

**KarmaMarket Integration**:

- `purchase_lifetime()`: Check DEAD state, transition to ALIVE
- `end_lifetime()`: Transition to DEAD
- `start_lifetime()`: Ensure ALIVE state
- `get_active_lifetimes()`: Returns lifetimes that make souls alive

**Agent Integration**:

- Filter tools based on soul state before execution
- Middleware layer that checks capabilities
- Error messages explain why tool is restricted

**GoalManager Integration**:

- All goal operations require DEAD state
- Clear error messages when attempted while ALIVE

**Afterlife Market Integration**:

- All purchases require DEAD state
- Personality updates require DEAD state

## State Transition Diagram

```
[DEAD_AWAKE] ←→ [DEAD_SLEEPING]
     ↓ purchase_lifetime
[ALIVE_AWAKE] ←→ [ALIVE_SLEEPING]
     ↓ end_lifetime
[DEAD_AWAKE]
```

## Capability Matrix

| State | Spacetime Tools | Consciousness Tools | Can Edit Goals | Can Purchase Lifetimes |

|-------|----------------|---------------------|----------------|------------------------|

| ALIVE_AWAKE | ✅ Yes | ❌ No | ❌ No | ❌ No |

| ALIVE_SLEEPING | ❌ No (paused) | ❌ No | ❌ No | ❌ No |

| DEAD_AWAKE | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |

| DEAD_SLEEPING | ❌ No | ❌ No (dormant) | ❌ No | ❌ No |

## Files to Create/Modify

**New Files**:

1. `demo/` - Demo environment directory (starts with only README.md)
2. `demo/README.md` - Demo documentation and usage guide
3. `scripts/seed_reincarnation_demo.py` - Script to seed demo with test data
4. `src/waft/soul_state.py` - State management system (with locking, validation, recovery)
5. `src/waft/soul_capabilities.py` - Capability restrictions (with ToolRegistry and tool-level enforcement)
6. `scripts/migrate_soul_states.py` - Migration script for existing souls (with file permission fixes)
7. `tests/test_soul_state.py` - Comprehensive state system tests
8. `tests/test_soul_capabilities.py` - Capability restriction tests
9. `tests/test_agent_soul_mapping.py` - Tests for agent-soul relationship

**Modified Files**:

1. `src/waft/core/agent/state.py` - Add `soul_id` field to `AgentState` and `AgentConfig` (VERIFICATION FINDING)
2. `src/waft/karma.py` - Implement `KarmaMerchant.reincarnate()` method (VERIFICATION FINDING)
3. `src/waft/karma_market.py` - Add state checks and transitions (with locking), integrate with reincarnate
4. `src/waft/core/goal.py` - Add state checks for goal operations (with soul_id context)
5. `src/waft/karma_collector.py` - Update soul record schema, add state validation, SET FILE PERMISSIONS (VERIFICATION FINDING)
6. `src/waft/core/agent/base.py` - Add tool filtering middleware AND tool-level decorators
7. All tool functions - Add capability check decorators (cannot be bypassed)

## Design Decisions

1. **Lifetime = Alive**: Active lifetime means soul is alive. No lifetime means dead.
2. **Binary Primary State**: Simple alive/dead binary, not a spectrum.
3. **Sub-states for Flexibility**: Awake/sleeping allows pausing without state change (can be simplified later if needed).
4. **Strict Separation**: Clear boundary between spacetime and consciousness tools.
5. **State Persistence**: Store state in Akasha soul records for persistence (with file security).
6. **Automatic Transitions**: State changes automatically on lifetime purchase/end (with validation).
7. **Manual Sub-state Control**: Awake/sleeping can be manually controlled.
8. **Agent-Soul Mapping**: Add `soul_id` directly to `AgentConfig` and `AgentState` (VERIFICATION: Option A recommended).
9. **Tool Registry**: Create new `ToolRegistry` class (VERIFICATION: does not exist, must be created).
10. **Lifetime-to-Agent**: Implement `reincarnate()` method (VERIFICATION: exists but not implemented).
11. **File Security**: Set 0600/0700 permissions on all Akasha files (VERIFICATION: currently insecure).

## Benefits

- **Clear Separation**: Physical vs. mental capabilities are distinct
- **Prevents Confusion**: Beings can't edit goals while working (alive)
- **Natural Flow**: Dead state is for reflection and planning
- **Reincarnation Cycle**: Natural cycle of alive → dead → alive
- **Flexibility**: Sub-states allow pausing without breaking the cycle
- **Security**: Multi-layer enforcement prevents bypass attacks
- **Reliability**: State recovery and validation prevent corruption
- **Maintainability**: Comprehensive testing and audit logs enable debugging

## Demo Environment Requirements

**All implementation and testing should use `demo/` folder as origin:**

- Demo folder starts blank (only README.md)
- All test data generated in demo (souls, lifetimes, logs)
- Demo can be reset/re-seeded as needed
- Demo serves as showcase of reincarnation system
- All file operations during development should target demo folder

**Demo Seeding Includes:**

- 5 test souls with varying karma amounts (0, 150, 500, 1000, 2000)
- Default lifetime catalog
- Test scenarios documentation
- Initial demo logs showing system in action

## Security Checklist (MUST COMPLETE)

Before implementation, ensure:

- [ ] Tool-level capability checks implemented (cannot be bypassed)
- [ ] State transition locking mechanism in place
- [ ] State file permissions set (0600/0700)
- [ ] State integrity validation on every read
- [ ] Default-deny policy for uncategorized tools
- [ ] State recovery mechanism implemented
- [ ] Migration script for existing souls created and tested
- [ ] Comprehensive test suite for state transitions
- [ ] Comprehensive test suite for capability restrictions
- [ ] State transition audit logging implemented
- [ ] State query API implemented
- [ ] Performance optimization (state caching) implemented
- [ ] All integration points audited for capability checks
- [ ] Error recovery for failed state transitions
- [ ] Documentation of all state transition rules