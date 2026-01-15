---
name: Genesis Implementation
overview: Implement the Evolutionary Core (AgentState, AgentConfig, BaseAgent) and run Experiment 001 to verify the biological lifecycle of agents with genome ID computation and spawn functionality.
todos:
  - id: create-agent-module
    content: Create src/waft/core/agent/ directory structure and __init__.py
    status: completed
  - id: implement-state-models
    content: Implement state.py with AgentState, AgentConfig, EvolutionaryEvent Pydantic models
    status: completed
  - id: implement-base-agent
    content: Implement base.py with BaseAgent class, genome ID computation, spawn(), and _record_event()
    status: completed
  - id: create-experiment-001
    content: Create tests/experiments/001_genesis_verification.py test file
    status: completed
  - id: run-experiment
    content: Run Experiment 001 and capture console output
    status: completed
  - id: report-results
    content: Report experiment results with genome IDs and lineage verification
    status: completed
---

# Genesis Implementation Plan

## Phase 1: Evolutionary Core Implementation

### 1.1 Create `src/waft/core/agent/state.py`

- Implement Pydantic models:
  - `MessageRole` enum (USER, ASSISTANT, SYSTEM, AGENT, TOOL)
  - `Message` model (AG2 protocol compatible)
  - `ToolDefinition` model
  - `AgentState` model (Iron Core - single source of truth)
  - `AgentConfig` model (CrewAI pattern + Waft extensions)
  - `EvolutionaryEventType` enum (SPAWN, MUTATE, GYM_EVAL, DEATH, SURVIVAL)
  - `EvolutionaryEvent` model (Flight Recorder event)

### 1.2 Create `src/waft/core/agent/base.py`

- Implement `BaseAgent` abstract class:
  - `__init__()`: Initialize agent with config, compute genome_id, initialize flight_recorder
  - `_compute_genome_id()`: SHA-256 hash of config + code_hash + state_version
  - `_get_code_hash()`: SHA-256 hash of agent's source code using inspect
  - `_record_event()`: Append EvolutionaryEvent to flight_recorder list
  - `spawn()`: Create child agent with mutation, set parent_id, increment generation
  - Abstract methods: `observe()`, `decide()`, `act()`, `reflect()` (stubs for now)

### 1.3 Create `src/waft/core/agent/__init__.py`

- Export public API: BaseAgent, AgentState, AgentConfig, EvolutionaryEvent

## Phase 2: Experiment 001 - Genesis Verification

### 2.1 Create `tests/experiments/001_genesis_verification.py`

- Test Genesis Agent (Generation 0):
  - Instantiate BaseAgent
  - Verify genome_id is computed
  - Print genome_id
- Test Spawn (Generation 1):
  - Spawn child with mutation
  - Verify child.parent_id == parent.genome_id
  - Verify child.generation == parent.generation + 1
  - Print child genome_id and parent_id
- Verify Flight Recorder:
  - Check that SPAWN events are recorded

## Phase 3: Execution & Reporting

### 3.1 Run Experiment 001

- Execute test and capture console output
- Verify all assertions pass

### 3.2 Report Results

- Provide console output showing:
  - Genesis agent genome_id
  - Child agent genome_id and parent_id
  - Verification that parent_id matches parent's genome_id
  - Flight Recorder event data

## Implementation Details

### Genome ID Calculation (from design doc):

```python
genome_data = {
    "config": self.config.dict(),
    "code_hash": self._get_code_hash(),
    "state_version": self.state.state_version
}
genome_json = json.dumps(genome_data, sort_keys=True)
return sha256(genome_json.encode()).hexdigest()
```

### Spawn Logic:

- Create child_config from parent (deep copy)
- Apply mutation to child_config
- Instantiate child agent
- Set child.parent_id = parent.genome_id
- Set child.generation = parent.generation + 1
- Set child.lineage_path = parent.lineage_path + [child.genome_id]
- Record SPAWN event in both parent and child

## Files to Create/Modify

1. `src/waft/core/agent/__init__.py` (new)
2. `src/waft/core/agent/state.py` (new)
3. `src/waft/core/agent/base.py` (new)
4. `tests/experiments/__init__.py` (new, if needed)
5. `tests/experiments/001_genesis_verification.py` (new)