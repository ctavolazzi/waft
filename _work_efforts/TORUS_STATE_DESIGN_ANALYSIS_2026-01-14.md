# Torus State Design Analysis
## Single Source of Truth for All Existence

**Date**: 2026-01-14 19:44:33 PST  
**Purpose**: Determine the optimal design pattern for the unified State object - the "Torus" that represents the entire application state in one form.

---

## Executive Summary

**Goal**: Create a unified State object that serves as the "Single Source of Truth for all Existence" - the complete application state in one form.

**Current State**: Multiple fragmented state systems exist:
- `AgentState` (Pydantic) - "Iron Core" for agent state
- `StatusState` (dataclass) - typed status state
- `PyriteState` - stored in `pyrite_state.json`
- `PrimeBeingProbe` state - per-being JSON files
- `UNIT_GENESIS` state - per-entity JSON files
- Status snapshots - with checksums
- Scientific method tool state - timestamped JSON files

**Decision Needed**: What form should the unified Torus State take?

---

## Current State Landscape

### Existing State Systems

1. **AgentState** (`src/waft/core/agent/state.py`)
   - **Type**: Pydantic BaseModel
   - **Purpose**: Agent state schema (LangGraph pattern + AG2 messages)
   - **Storage**: In-memory, serialized to JSON when needed
   - **Scope**: Individual agent state
   - **Description**: "Iron Core" - single source of truth for agent state

2. **StatusState** (`src/waft/core/status_state.py`)
   - **Type**: Dataclass with computed properties
   - **Purpose**: Typed status state with health metrics
   - **Storage**: Converted to dict, then JSON
   - **Scope**: System status snapshot
   - **Components**: EpistemicState, GamificationState, ProjectHealthState

3. **PyriteState** (`src/waft/pyrite.py`)
   - **Type**: Dictionary serialized to JSON
   - **Storage**: `_pyrite/.waft/pyrite_state.json`
   - **Scope**: Pyrite system state (attributes, work effort graph, secrets)
   - **Pattern**: Single JSON file per project

4. **PrimeBeingProbe State** (`src/waft/core/prime_being_probe.py`)
   - **Type**: Dictionary serialized to JSON
   - **Storage**: `{being_id}_state.json` per being
   - **Scope**: Individual being state
   - **Pattern**: Per-entity files

5. **UNIT_GENESIS State** (`docs/UNIFIED_GENESIS_PROTOCOL.md`)
   - **Type**: JSON schema
   - **Storage**: `_pyrite/.waft/genesis_entities/{being_id}_state.json`
   - **Scope**: Per-entity state + global template (`20.00_state.json`)
   - **Pattern**: Per-entity files + global template

6. **Status Snapshots** (`src/waft/core/status_persistence.py`)
   - **Type**: Dictionary with checksum
   - **Storage**: `_pyrite/.waft/status_snapshots/{snapshot_id}.json`
   - **Scope**: Historical status snapshots
   - **Pattern**: Timestamped files with integrity checking

7. **Scientific Method Tool State** (`scientific_method_tool/state_capture.py`)
   - **Type**: SystemState (dataclass) serialized to JSON
   - **Storage**: `state_{state_type}_{timestamp}.json`
   - **Scope**: Experiment state snapshots
   - **Pattern**: Timestamped files

### Storage Patterns Observed

1. **JSON as Universal Format**: All state systems use JSON for persistence
2. **Pydantic Models**: Some use Pydantic (AgentState) - serialize to JSON
3. **Dataclasses**: Some use dataclasses (StatusState) - convert to dict then JSON
4. **Dictionaries**: Some use plain dicts (PyriteState) - direct JSON serialization
5. **Checksums**: StatusPersistence uses MD5 checksums for integrity
6. **Per-Entity vs. Single File**: Mix of both patterns

---

## Design Options Analysis

### Option 1: Single JSON File (`torus_state.json`)

**Description**: One unified JSON file containing all application state.

**Structure**:
```json
{
  "version": "1.0",
  "timestamp": "2026-01-14T19:44:33Z",
  "checksum": "md5_hash",
  "agents": { /* AgentState objects */ },
  "status": { /* StatusState data */ },
  "pyrite": { /* PyriteState data */ },
  "beings": { /* PrimeBeingProbe + UNIT_GENESIS states */ },
  "snapshots": { /* Status snapshot references */ },
  "experiments": { /* Scientific method tool states */ },
  "metadata": { /* System metadata */ }
}
```

**Pros**:
- ✅ Single source of truth in one file
- ✅ Easy to backup/restore
- ✅ Simple to understand
- ✅ Atomic updates (write entire state at once)
- ✅ Easy to version control
- ✅ Fast to load (one file read)

**Cons**:
- ❌ Large file size (all state in one file)
- ❌ Write conflicts (multiple processes)
- ❌ Memory intensive (load entire state)
- ❌ No partial updates (must rewrite entire file)
- ❌ Risk of corruption (single point of failure)
- ❌ Difficult to scale (file grows unbounded)

**Best For**: Small to medium projects, single-user scenarios, simple state

---

### Option 2: Hierarchical JSON Structure (Multiple Files, One Root)

**Description**: Multiple JSON files organized hierarchically, with one root index file.

**Structure**:
```
_pyrite/.waft/torus/
├── 00.00_torus_index.json          # Root index
├── 10.00_agents/                   # Agent states
│   ├── {agent_id}_state.json
├── 20.00_status/                   # Status states
│   ├── current_status.json
│   └── snapshots/
├── 30.00_pyrite/                   # Pyrite state
│   └── pyrite_state.json
├── 40.00_beings/                   # Being states
│   ├── {being_id}_state.json
├── 50.00_experiments/              # Experiment states
│   └── {experiment_id}_state.json
└── 90.00_metadata/                 # System metadata
    └── system_metadata.json
```

**Root Index**:
```json
{
  "version": "1.0",
  "timestamp": "2026-01-14T19:44:33Z",
  "checksum": "md5_hash",
  "agents": ["agent_001", "agent_002"],
  "beings": ["being_001", "being_002"],
  "experiments": ["exp_001"],
  "status_snapshot": "status_20260114_194433",
  "pyrite_state": "pyrite_state.json",
  "metadata": "system_metadata.json"
}
```

**Pros**:
- ✅ Organized structure (Johnny Decimal)
- ✅ Partial updates (update only changed files)
- ✅ Scalable (add new entity types easily)
- ✅ Parallel access (different files)
- ✅ Modular (each subsystem independent)
- ✅ Easy to backup (backup entire directory)

**Cons**:
- ⚠️ More complex (multiple files to manage)
- ⚠️ Consistency challenges (multiple files must be in sync)
- ⚠️ More file I/O (multiple reads/writes)
- ⚠️ Index must be maintained

**Best For**: Large projects, multi-user scenarios, complex state, modular architecture

---

### Option 3: Pydantic Model with JSON Serialization

**Description**: Single Pydantic BaseModel class that unifies all state, serialized to JSON.

**Structure**:
```python
class TorusState(BaseModel):
    """The Torus - Single Source of Truth for all Existence."""
    version: str = "1.0"
    timestamp: datetime
    checksum: Optional[str] = None
    
    # Sub-states
    agents: Dict[str, AgentState] = Field(default_factory=dict)
    status: StatusState = Field(default_factory=StatusState)
    pyrite: PyriteState = Field(default_factory=PyriteState)
    beings: Dict[str, BeingState] = Field(default_factory=dict)
    experiments: Dict[str, ExperimentState] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def save(self, path: Path) -> None:
        """Save to JSON with checksum."""
        ...
    
    @classmethod
    def load(cls, path: Path) -> 'TorusState':
        """Load from JSON with integrity check."""
        ...
```

**Storage**: Single JSON file (`torus_state.json`) or hierarchical structure

**Pros**:
- ✅ Type safety (Pydantic validation)
- ✅ IDE autocomplete
- ✅ Schema validation
- ✅ Computed properties support
- ✅ Easy serialization/deserialization
- ✅ Can use with Option 1 or Option 2

**Cons**:
- ⚠️ Requires Pydantic dependency
- ⚠️ More complex than plain dict
- ⚠️ Validation overhead

**Best For**: Type-safe state management, validation requirements, IDE support

---

### Option 4: Dataclass with JSON Serialization

**Description**: Single dataclass that unifies all state, converted to dict then JSON.

**Structure**:
```python
@dataclass
class TorusState:
    """The Torus - Single Source of Truth for all Existence."""
    version: str = "1.0"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    checksum: Optional[str] = None
    
    # Sub-states
    agents: Dict[str, AgentState] = field(default_factory=dict)
    status: StatusState = field(default_factory=StatusState)
    pyrite: PyriteState = field(default_factory=PyriteState)
    beings: Dict[str, BeingState] = field(default_factory=dict)
    experiments: Dict[str, ExperimentState] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def overall_health(self) -> float:
        """Computed property for overall health."""
        ...
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        ...
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TorusState':
        """Create from dictionary."""
        ...
```

**Storage**: Single JSON file or hierarchical structure

**Pros**:
- ✅ Computed properties (like StatusState)
- ✅ Type hints
- ✅ Standard library (no dependencies)
- ✅ Lightweight
- ✅ Can use with Option 1 or Option 2

**Cons**:
- ⚠️ Manual serialization (to_dict/from_dict)
- ⚠️ No automatic validation
- ⚠️ Less IDE support than Pydantic

**Best For**: Lightweight state management, computed properties, standard library preference

---

### Option 5: Hybrid Approach (Index + Entity Files)

**Description**: Root index file with references to entity-specific files (like UNIT_GENESIS pattern).

**Structure**:
```
_pyrite/.waft/torus/
├── torus_index.json                # Root index
├── agents/
│   └── {agent_id}.json
├── beings/
│   └── {being_id}.json
├── experiments/
│   └── {experiment_id}.json
└── system/
    ├── status.json
    ├── pyrite.json
    └── metadata.json
```

**Index**:
```json
{
  "version": "1.0",
  "timestamp": "2026-01-14T19:44:33Z",
  "checksum": "md5_hash",
  "entities": {
    "agents": ["agent_001", "agent_002"],
    "beings": ["being_001", "being_002"],
    "experiments": ["exp_001"]
  },
  "system": {
    "status": "system/status.json",
    "pyrite": "system/pyrite.json",
    "metadata": "system/metadata.json"
  }
}
```

**Pros**:
- ✅ Best of both worlds (index + entity files)
- ✅ Scalable (add entities without touching index)
- ✅ Partial updates (update only changed entities)
- ✅ Follows existing UNIT_GENESIS pattern
- ✅ Easy to query (read index, then specific entities)

**Cons**:
- ⚠️ More complex than single file
- ⚠️ Consistency challenges
- ⚠️ More file I/O

**Best For**: Large-scale systems, entity-heavy state, existing UNIT_GENESIS pattern alignment

---

## Decision Criteria

### Must-Have Requirements

1. **Single Source of Truth**: One authoritative representation of state
2. **Persistence**: Must be saved to disk (survive restarts)
3. **Integrity**: Must have checksum/validation
4. **Accessibility**: Must be easy to read/write
5. **Scalability**: Must handle growth (agents, beings, experiments)

### Nice-to-Have Requirements

1. **Type Safety**: Type hints and validation
2. **Computed Properties**: Derived metrics
3. **Partial Updates**: Update only changed parts
4. **Version Control Friendly**: Git-friendly format
5. **Backup/Restore**: Easy to backup and restore
6. **Query Performance**: Fast to read specific parts
7. **Atomic Updates**: All-or-nothing updates

### Constraints

1. **Existing Patterns**: Must work with existing state systems
2. **File Format**: JSON is universal (already used everywhere)
3. **Dependencies**: Prefer standard library, but Pydantic is acceptable
4. **Complexity**: Balance simplicity vs. features

---

## Recommendation Matrix

| Criterion | Option 1<br/>Single JSON | Option 2<br/>Hierarchical | Option 3<br/>Pydantic | Option 4<br/>Dataclass | Option 5<br/>Hybrid |
|-----------|-------------------------|---------------------------|----------------------|------------------------|---------------------|
| **Single Source of Truth** | ✅ Excellent | ✅ Excellent | ✅ Excellent | ✅ Excellent | ✅ Excellent |
| **Simplicity** | ✅ Excellent | ⚠️ Good | ⚠️ Good | ⚠️ Good | ⚠️ Fair |
| **Scalability** | ❌ Poor | ✅ Excellent | ⚠️ Good | ⚠️ Good | ✅ Excellent |
| **Partial Updates** | ❌ Poor | ✅ Excellent | ⚠️ Good | ⚠️ Good | ✅ Excellent |
| **Type Safety** | ❌ Poor | ❌ Poor | ✅ Excellent | ⚠️ Good | ⚠️ Good |
| **Computed Properties** | ❌ Poor | ❌ Poor | ✅ Excellent | ✅ Excellent | ⚠️ Good |
| **Performance** | ⚠️ Good | ⚠️ Good | ⚠️ Good | ⚠️ Good | ✅ Excellent |
| **Integrity** | ⚠️ Good | ⚠️ Good | ✅ Excellent | ⚠️ Good | ⚠️ Good |
| **Existing Pattern Alignment** | ⚠️ Fair | ✅ Excellent | ⚠️ Good | ⚠️ Good | ✅ Excellent |
| **Backup/Restore** | ✅ Excellent | ⚠️ Good | ✅ Excellent | ✅ Excellent | ⚠️ Good |

---

## Final Recommendation

### **Option 3 + Option 2: Pydantic Model with Hierarchical Storage**

**Rationale**:
1. **Type Safety**: Pydantic provides validation and IDE support
2. **Computed Properties**: Can use Pydantic validators and properties
3. **Hierarchical Storage**: Scalable, supports partial updates
4. **Existing Patterns**: Aligns with UNIT_GENESIS pattern (index + entity files)
5. **Best of Both Worlds**: Type safety + scalability

**Implementation**:
- **Root Model**: `TorusState` (Pydantic BaseModel)
- **Storage Pattern**: Hierarchical JSON files (Option 2 structure)
- **Index File**: `_pyrite/.waft/torus/00.00_torus_index.json`
- **Entity Files**: Per-entity JSON files in subdirectories
- **System Files**: System-wide state in `system/` directory

**Benefits**:
- ✅ Single source of truth (index file)
- ✅ Type-safe (Pydantic validation)
- ✅ Scalable (hierarchical structure)
- ✅ Partial updates (update only changed entities)
- ✅ Computed properties (Pydantic validators)
- ✅ Integrity checking (checksums)
- ✅ Aligns with existing patterns

**Trade-offs**:
- ⚠️ More complex than single file
- ⚠️ Requires Pydantic dependency (already used)
- ⚠️ More file I/O than single file

---

## Next Steps

1. **Create TorusState Model**: Define Pydantic model with all sub-states
2. **Implement Storage Layer**: Hierarchical JSON storage with index
3. **Migration Path**: Migrate existing state systems to Torus
4. **Integrity System**: Add checksums and validation
5. **API Layer**: Create read/write API for Torus state
6. **Documentation**: Document Torus state schema and usage

---

## Questions to Answer

1. **Storage Location**: `_pyrite/.waft/torus/` or project root?
2. **Index Format**: JSON or TOML?
3. **Checksum Algorithm**: MD5 (current) or SHA-256 (more secure)?
4. **Migration Strategy**: How to migrate existing state?
5. **Backward Compatibility**: Support old state formats?

---

**This analysis provides the foundation for implementing the Torus State - the Single Source of Truth for all Existence.**
