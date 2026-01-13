# Spawn

**Spawn a new Being into a Reality.**

Creates a new Being entity that can learn skills, make decisions, and evolve. The Being is spawned into a specified Reality (or a default one if not specified). First Being will automatically initialize with Empirica for epistemic tracking.

**Use when:** Need to create a new Being for work tracking, want to spawn a Being into a Reality, need Being context for evolutionary work, or want to start a new Being lifecycle.

---

## Purpose

This command provides:
- **Being Creation**: Spawns new Being entity
- **Reality Integration**: Places Being into a Reality environment
- **Empirica Integration**: First Being automatically gets Empirica session
- **Genetic Lineage**: Tracks Being's origin (Source or parent)
- **Skill Inheritance**: Optionally inherit skills from parent Being
- **Lifecycle Management**: Being can learn, evolve, and make decisions

---

## Philosophy

### 1. Being as Entity

Beings are entities that:
- **Exist in Realities**: Spawned into simulation environments
- **Learn Skills**: Develop abilities through experience
- **Make Decisions**: Use stamina and decision fatigue
- **Evolve**: Improve through natural selection
- **Track Lineage**: Maintain genetic ancestry chain

### 2. Source Connection

All Beings connect to Source:
- **First Being**: Spawns from Source consciousness
- **Reincarnated Being**: Spawns from parent Being (inherits skills with mutation)
- **Ancestral Chain**: Complete lineage from Source → Being
- **Return to Source**: Learnings flow back to Source

### 3. Reality as Environment

Realities provide:
- **Learning Environment**: Where Beings develop skills
- **Evolutionary Pressure**: Natural selection occurs
- **Memory Generation**: Experiences become memories
- **Skill Development**: Abilities improve through work

---

## Execution Steps

### Step 1: Determine Reality

**Purpose**: Identify or create Reality for Being

**Actions**:
1. Check if `reality_id` is provided in user input
2. If not provided, use default: `"default_reality"`
3. Check if Reality exists (using RealitySystem)
4. If Reality doesn't exist, create it:
   - Type: `RealityType.LEARNING` (default)
   - Configuration: `{}` (empty, can be customized)
   - Source: `"source_consciousness"`

**Output**: Valid `reality_id` for Being spawn

---

### Step 2: Check for Parent Being

**Purpose**: Determine if Being should inherit from parent

**Actions**:
1. Check if `parent_being_id` is provided in user input
2. If provided:
   - Validate parent Being exists
   - Load parent Being to inherit skills
   - Skills will be inherited with ±5% mutation
3. If not provided:
   - Being spawns from Source (first birth)
   - No skill inheritance
   - `lifetimes = 1`

**Output**: `parent_being_id` (or `None`) and inherited skills dict

---

### Step 3: Check for Initial Skills

**Purpose**: Allow custom initial skills

**Actions**:
1. Check if `initial_skills` provided in user input
2. If provided, use those skills
3. If parent provided, merge parent skills (with mutation) with initial skills
4. If neither, start with empty skills `{}`

**Output**: Initial skills dictionary for Being

---

### Step 4: Spawn Being

**Purpose**: Create new Being entity

**Actions**:
1. Initialize `BeingSystem`:
   ```python
   from waft.being import BeingSystem
   being_system = BeingSystem(project_path=Path.cwd())
   ```
2. Call `spawn_being()`:
   ```python
   being = being_system.spawn_being(
       reality_id=reality_id,
       parent_being_id=parent_being_id,
       initial_skills=initial_skills
   )
   ```
3. Being is automatically saved to `_hidden/.truth/beings/`
4. First Being automatically gets Empirica session (if available)

**Output**: Created `Being` instance

---

### Step 5: Display Being Information

**Purpose**: Show user the spawned Being details

**Actions**:
1. Display Being ID: `being.being_id`
2. Display Reality ID: `being.reality_id`
3. Display Parent Being ID: `being.parent_being_id` (or "Source" if None)
4. Display Lifetimes: `being.lifetimes`
5. Display Skills: `being.skills`
6. Display State: `being.state.value`
7. Display Empirica Status:
   - `empirica_enabled`: Whether Empirica is active
   - `empirica_session_id`: Session ID if enabled
8. Display Lifecycle Attributes:
   - `stamina`: Current stamina
   - `stamina_max`: Maximum stamina
   - `will_to_live`: Will to live value
   - `decision_fatigue`: Current decision fatigue
   - `decision_quota_max`: Max decisions before sleep
   - `personality_type`: Personality type
9. Display Ancestral Chain: `being.ancestral_chain`

**Output Format**:
```markdown
## Being Spawned Successfully

**Being ID**: `being_20260113_002328_a1b2c3d4`
**Reality**: `default_reality`
**Parent**: Source (first birth)
**Lifetimes**: 1

**Skills**: `{}`
**State**: `SPAWNING`

**Empirica**:
- Enabled: ✅ Yes
- Session ID: `abc-123-def-456`

**Lifecycle**:
- Stamina: 100.0 / 100.0
- Will to Live: 100.0
- Decision Fatigue: 0 / 50
- Personality: `balanced`

**Ancestral Chain**: `[source_consciousness, being_20260113_002328_a1b2c3d4]`
```

---

### Step 6: Document Being Spawn

**Purpose**: Create spawn record for tracking

**Actions**:
1. Create spawn document in `_pyrite/active/`:
   - Filename: `BEING_SPAWN_[being_id].md`
   - Include Being metadata
   - Include spawn timestamp
   - Include Reality information
   - Include parent/lineage information
2. Update devlog with spawn event (optional)

**Output**: Spawn record document

---

## Usage Examples

### Basic Spawn
```
/spawn
```

Spawns new Being into `default_reality` from Source.

### Spawn into Specific Reality
```
/spawn --reality "my_reality"
```

Spawns Being into specified Reality (creates Reality if it doesn't exist).

### Spawn from Parent Being
```
/spawn --parent "being_20260112_123456_abc12345"
```

Spawns Being from parent (inherits skills with mutation, reincarnation).

### Spawn with Initial Skills
```
/spawn --skills "{\"investigation\": 30.0, \"analysis\": 25.0}"
```

Spawns Being with custom initial skills.

### Spawn with All Options
```
/spawn --reality "evolution_reality" --parent "being_20260112_123456_abc12345" --skills "{\"coding\": 40.0}"
```

Spawns Being with Reality, parent, and custom skills (parent skills merged with custom).

---

## Integration

This command uses:
- **BeingSystem**: Being creation and management (`src/waft/being.py`)
- **RealitySystem**: Reality management (`src/waft/reality.py`)
- **Source Consciousness**: Source connection and lineage
- **Empirica**: Epistemic tracking (if available, first Being only)

**Being Storage**: `_hidden/.truth/beings/`

**Reality Storage**: `_hidden/.truth/realities/`

---

## When to Use

**Use `/spawn` when**:
- ✅ Need to create a new Being for work tracking
- ✅ Want to spawn Being into a Reality
- ✅ Starting new evolutionary work cycle
- ✅ Need Being context for decision-making
- ✅ Want to track work through Being lifecycle
- ✅ Need Being for genetic lineage tracking

**Don't use `/spawn` when**:
- ❌ Already have Being for current work
- ❌ Just need to load existing Being (use BeingSystem directly)
- ❌ Don't need Being tracking overhead
- ❌ Quick task that doesn't need Being context

---

## Being System Details

**Being ID Format**: `being_YYYYMMDD_HHMMSS_[hash]`

**Being States**:
- `SPAWNING`: Being created
- `LEARNING`: Being learning skills
- `EVOLVING`: Being evolving
- `COMPLETING`: Being finishing reality
- `ARCHIVED`: Being archived

**First Being**:
- Automatically gets Empirica session (if Empirica available)
- Spawns from Source consciousness
- `lifetimes = 1`
- No parent Being

**Reincarnated Being**:
- Inherits skills from parent (±5% mutation)
- `lifetimes = parent.lifetimes + 1`
- Ancestral chain includes parent

---

## Related Commands

- **`/evolve`**: Spawn Being and run complete evolution workflow
- **`/version-bake`**: Quality workflow (can use existing Being)

---

**This command spawns a new Being entity into a Reality for tracking work, learning, and evolution.**

--- End Command ---
