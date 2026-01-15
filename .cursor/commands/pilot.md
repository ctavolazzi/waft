# Pilot

**Spawn a Being with a Purpose and have it execute autonomously.**

Creates a new Being entity imbued with a Purpose derived from context, then has the Being "live" and execute to accomplish that purpose. The Being makes decisions, uses tools, learns skills, and works autonomously to fulfill its purpose.

**Use when:** Want to spawn a Being with a specific purpose/task and have it work autonomously, need a Being to accomplish a goal independently, or want to delegate work to a Being entity.

---

## Purpose

This command provides:
- **Purpose-Driven Being**: Spawns Being with specific purpose from context
- **Purpose Being Creation**: Creates Purpose Being that defines the goal
- **Autonomous Execution**: Being makes decisions and uses tools to accomplish purpose
- **Skill Learning**: Being learns skills as it works
- **Progress Tracking**: Being saves progress periodically

---

## Philosophy

### 1. Purpose as Direction

Beings with purpose:
- **Have Clear Goals**: Purpose defines what Being should accomplish
- **Make Decisions**: Being decides how to accomplish purpose
- **Use Tools**: Being uses codebase_search, file operations, etc.
- **Learn Skills**: Being develops abilities through work
- **Track Progress**: Being saves state periodically

### 2. Purpose Being Pattern

Purpose Beings:
- **Define Goals**: Purpose Being's purpose = parsed context/query
- **Link to Main Being**: Main Being is imbued with Purpose Being
- **Provide Direction**: Purpose Being guides main Being's actions
- **Enable Querying**: Main Being can query its purpose via `get_purpose()`

### 3. Autonomous Execution

Beings execute:
- **State Management**: Being state set to `LEARNING`
- **Decision Making**: Being makes decisions to accomplish purpose
- **Tool Usage**: Being uses available tools (codebase_search, file ops, etc.)
- **Skill Development**: Being learns skills as it works
- **Progress Saving**: Being saves progress periodically

---

## Execution Steps

### Step 1: Parse Context

**Purpose**: Extract purpose/query from user input

**Actions**:
1. Parse everything after `/pilot` as context
2. Extract purpose/query from context
3. If no context provided, ask user for purpose

**Output**: Purpose string/query for Being

---

### Step 2: Spawn Main Being

**Purpose**: Create main Being that will execute the purpose

**Actions**:
1. Use BeingSystem to spawn new Being
   - Being will automatically be descendant of TheOne
   - Reality: `"pilot_reality"` (or default)
   - No parent (spawns from TheOne)
2. Being is created with standard initialization
3. Being state: `LEARNING`

**Output**: Main Being instance

---

### Step 3: Create Purpose Being

**Purpose**: Create Purpose Being that defines the goal

**Actions**:
1. Spawn new Being for Purpose:
   - Being ID: `purpose_being_{timestamp}_{hash}`
   - Reality: Same as main Being
   - Parent: TheOne (or main Being's parent)
2. Set Purpose Being's purpose:
   - `purpose = {"query": parsed_context, "type": "pilot_mission"}`
   - Purpose Being's purpose = parsed context/query
3. Save Purpose Being

**Output**: Purpose Being instance

---

### Step 4: Imbue Main Being with Purpose

**Purpose**: Link main Being to Purpose Being

**Actions**:
1. Call `main_being.imbue_with_purpose(purpose_being)`
2. This sets `main_being.purpose_being_id = purpose_being.being_id`
3. Main Being can now query its purpose via `get_purpose()`

**Output**: Main Being with purpose linked

---

### Step 5: Have Being Execute

**Purpose**: Being "lives" and executes to accomplish purpose

**Actions**:
1. Set Being state to `LEARNING`
2. Being makes decisions to accomplish purpose:
   - Being queries purpose: `being.get_purpose(being_system)`
   - Being decides what actions to take
   - Being uses tools (codebase_search, file operations, etc.)
   - Being learns skills as it works
3. Being saves progress periodically:
   - Save Being state every N decisions
   - Update Being's skills, memories, lessons
4. Being continues until:
   - Purpose accomplished (Being determines completion)
   - Being decides to stop
   - User interrupts

**Output**: Being execution results and progress

---

## Usage Examples

### Basic Pilot

```
/pilot implement user authentication system
```

Spawns Being with purpose "implement user authentication system", Being works autonomously to accomplish it.

### Pilot with Context

```
/pilot analyze the codebase and create a refactoring plan
```

Spawns Being with purpose to analyze and plan refactoring.

### Pilot with Specific Goal

```
/pilot create a new API endpoint for user profiles
```

Spawns Being with purpose to create API endpoint.

---

## Integration

This command uses:
- **BeingSystem**: Being creation and management (`src/waft/being.py`)
- **TheOne**: Root ancestor (all Beings descend from TheOne)
- **Purpose System**: Purpose Being pattern for goal definition
- **RealitySystem**: Reality management (`src/waft/reality.py`)

**Being Storage**: `_hidden/.truth/beings/`

**Reality Storage**: `_hidden/.truth/realities/`

---

## When to Use

**Use `/pilot` when**:
- ✅ Want to spawn Being with specific purpose/task
- ✅ Need Being to work autonomously on a goal
- ✅ Want to delegate work to a Being entity
- ✅ Need Being to accomplish task independently
- ✅ Want Being to learn skills while working

**Don't use `/pilot` when**:
- ❌ Just need to spawn Being without purpose (use `/spawn`)
- ❌ Don't need autonomous execution
- ❌ Quick task that doesn't need Being tracking
- ❌ Already have Being for current work

---

## Being System Details

**Being ID Format**: `being_YYYYMMDD_HHMMSS_[hash]`

**Purpose Being ID Format**: `purpose_being_YYYYMMDD_HHMMSS_[hash]`

**Being States**:
- `SPAWNING`: Being created
- `LEARNING`: Being learning skills and executing purpose
- `EVOLVING`: Being evolving
- `COMPLETING`: Being finishing reality
- `ARCHIVED`: Being archived

**Purpose System**:
- Purpose Being: Defines the goal/mission
- Main Being: Executes the purpose
- Link: `main_being.purpose_being_id = purpose_being.being_id`
- Query: `main_being.get_purpose(being_system)` returns purpose dict

**Ancestral Chain**:
- All Beings descend from TheOne
- Chain: `[source_consciousness, the_one, ...parent_chain, being_id]`

---

## Related Commands

- **`/spawn`**: Spawn Being without purpose (manual control)
- **`/evolve`**: Spawn Being and run complete evolution workflow

---

## Implementation Notes

**Purpose Being Pattern**:
1. Purpose Being is a regular Being with `purpose` set
2. Main Being links to Purpose Being via `purpose_being_id`
3. Main Being queries purpose via `get_purpose()` method
4. Purpose Being's purpose dict contains the mission/goal

**Autonomous Execution**:
1. Being state set to `LEARNING`
2. Being queries purpose and makes decisions
3. Being uses tools (codebase_search, file operations, etc.)
4. Being learns skills and saves progress
5. Being continues until purpose accomplished or stopped

**Progress Saving**:
- Being saves state every N decisions (configurable)
- Being's skills, memories, lessons updated
- Being file written to disk periodically

---

**This command enables purpose-driven autonomous Being execution, allowing Beings to work independently toward specific goals while learning and evolving.**
