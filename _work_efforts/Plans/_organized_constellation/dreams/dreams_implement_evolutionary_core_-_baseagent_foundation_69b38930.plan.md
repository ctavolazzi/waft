---
name: Implement Evolutionary Core - BaseAgent Foundation
overview: "Implement the foundational Python structures for the Evolutionary Code Laboratory: create agent module structure, implement Pydantic state models (AgentConfig, AgentState, EvolutionaryEvent), and implement BaseAgent abstract class with biological lifecycle methods (spawn, eval, evolve) and OODA loop."
todos:
  - id: scaffold-structure
    content: Create directory structure src/waft/core/agent/ and __init__.py with exports
    status: pending
  - id: implement-state-models
    content: "Implement state.py with all Pydantic models: MessageRole, Message, ToolDefinition, AgentConfig, AgentState, EvolutionaryEventType, EvolutionaryEvent, AgentEvent, AgentStep, Modification"
    status: pending
  - id: implement-baseagent
    content: "Implement base.py with BaseAgent class: __init__, genome_id computation, flight recorder methods, spawn/eval/evolve skeletons, OODA loop (run/step), communication protocol"
    status: pending
  - id: create-work-effort
    content: Create _work_efforts/active/003_implement_agent_core.md and link to TKT-ai-sdk-002
    status: pending

category: dreams
confidence: 0.55
constellation_date: 2026-01-14
---

# Implementation Plan: Evolutionary Core - BaseAgent Foundation

## Overview

Implement the foundational Python structures for the Evolutionary Code Laboratory, moving from design phase to implementation. This creates the "DNA" (state models) and "Organism" (BaseAgent class) that enable agent evolution.

## Files to Create

### 1. Directory Structure

- Create `src/waft/core/agent/` directory
- Create `src/waft/core/agent/__init__.py` with module exports

### 2. State Models (`src/waft/core/agent/state.py`)

Implement Pydantic models from design document:

**MessageRole Enum** (AG2 protocol):

- USER, ASSISTANT, SYSTEM, AGENT, TOOL

**Message Model**:

- role: MessageRole
- content: str
- metadata: Dict[str, Any] (default: {})
- timestamp: datetime (default: now)
- tool_calls: Optional[List[Dict]]
- tool_results: Optional[List[Dict]]

**ToolDefinition Model**:

- name: str
- description: str
- parameters: Dict[str, Any] (JSON Schema)
- handler: Optional[Any]

**AgentConfig Model** (CrewAI pattern + Waft extensions):

- Identity: role, goal, backstory, agent_id (Optional, auto-generated)
- Capabilities: tools (List[ToolDefinition]), llm_provider, llm_model, llm_config
- Behavior: max_iterations, timeout, verbose
- Safety: sandbox_enabled, sandbox_config, safety_level (1-4)
- Self-Modification: self_modification_enabled, self_modification_level (1-4)
- Integration: empirica_enabled, tavern_keeper_enabled, decision_engine_enabled
- Multi-Agent: crew_id (Optional)
- Advanced: custom_handlers

**AgentState Model** (LangGraph pattern + AG2 messages):

- memory: List[Message] (conversation history)
- knowledge: Dict[str, Any] (long-term storage)
- tools: List[ToolDefinition]
- working_memory: Dict[str, Any] (scratchpad)
- agent_id: str
- role: str
- goal: str
- current_step: Optional[str]
- next_action: Optional[str]
- epistemic_state: Optional[Dict] (Empirica)
- hero_state: Optional[Dict] (TavernKeeper)
- inbox: List[Message] (multi-agent)
- outbox: List[Message] (multi-agent)
- sandbox_id: Optional[str]
- state_version: int (default: 1)
- last_updated: datetime

**EvolutionaryEventType Enum**:

- SPAWN, MUTATE, GYM_EVAL, DEATH, SURVIVAL

**EvolutionaryEvent Model** (Flight Recorder):

- timestamp: datetime (UTC)
- genome_id: str (SHA-256 hash)
- parent_id: Optional[str] (lineage tracking)
- generation: int (0 = Genesis)
- event_type: EvolutionaryEventType
- payload: Dict[str, Any]
- fitness_metrics: Optional[Dict[str, Any]]
- agent_id: str
- lineage_path: List[str]

**AgentEvent Model**:

- event_type: str
- timestamp: datetime
- data: Dict[str, Any]
- agent_id: str

**AgentStep Model**:

- step_type: str
- state: AgentState
- result: Dict[str, Any]
- success: bool
- error: Optional[str]

**Modification Model**:

- modification_type: str (code/config/prompt/architecture/behavior)
- target: str
- change: Dict[str, Any]
- safety_level: int (1-4)
- validation_required: bool (default: True)

### 3. BaseAgent Class (`src/waft/core/agent/base.py`)

Implement abstract base class with:

**Initialization (`__init__`)**:

- Accept AgentConfig and project_path: Path
- Auto-generate agent_id if None: `agent_{timestamp}`
- Initialize AgentState from config
- Initialize Flight Recorder (List[EvolutionaryEvent])
- Compute genome_id via `_compute_genome_id()` (SHA-256 of config + code_hash + state_version)
- Set generation=0, parent_id=None, lineage_path=[genome_id]
- Initialize integrations (Empirica, TavernKeeper, Decision Engine) if enabled
- Initialize sandbox if enabled

**Genome ID Computation**:

- `_compute_genome_id() -> str`: SHA-256 hash of config.dict() + code_hash + state_version
- `_get_code_hash() -> str`: SHA-256 hash of agent class source code (inspect.getsource)

**Flight Recorder Methods**:

- `_record_event(event_type, payload, fitness_metrics=None) -> EvolutionaryEvent`: Record event with current genome_id, parent_id, generation, lineage_path
- `get_family_tree() -> Dict[str, Any]`: Reconstruct family tree from flight recorder

**Biological Lifecycle Methods**:

1. **`spawn(mutation: Modification) -> "BaseAgent"`** (Skeleton):

   - Record SPAWN event
   - Create child_config = self.config.copy(deep=True)
   - Apply mutation to child_config (handle config/prompt mutation types)
   - Create child agent instance: `self.__class__(child_config, project_path)`
   - Set child.parent_id = self.genome_id
   - Set child.generation = self.generation + 1
   - Set child.lineage_path = self.lineage_path + [child.genome_id]
   - Record child spawn event
   - Return child

2. **`eval() -> Dict[str, float]`** (Skeleton/Placeholder):

   - Record GYM_EVAL event (start)
   - Return placeholder fitness metrics:
     ```python
     {
         "stability_score": 0.0,
         "efficiency_score": 0.0,
         "safety_score": 0.0,
         "overall_fitness": 0.0
     }
     ```

   - Note: Full Gym integration will be implemented later
   - Record GYM_EVAL event (complete) with fitness_metrics
   - Check fitness threshold (< 0.5 = DEATH, else SURVIVAL)

3. **`evolve(new_genome: "BaseAgent") -> None`** (Skeleton):

   - Record MUTATE event
   - Validate: new_genome.genome_id != self.genome_id
   - Hot-swap: self.config = new_genome.config, self.state = new_genome.state
   - Update: self.genome_id, self.generation, self.parent_id, self.lineage_path
   - Merge flight recorders: self.flight_recorder.extend(new_genome.flight_recorder)
   - Record SURVIVAL event

**OODA Loop Methods** (Abstract - to be implemented by subclasses):

- `async observe() -> AgentStep`: Observe project state
- `async decide(state: AgentState) -> AgentStep`: Make decision
- `async act(decision: Dict[str, Any]) -> AgentStep`: Execute action
- `async reflect(result: Dict[str, Any]) -> AgentStep`: Reflect and learn

**Main Execution Loop**:

- `async run(input: Union[str, Message]) -> AsyncIterator[AgentEvent]`:
  - Convert string input to Message if needed
  - Add message to state.memory
  - Process inbox messages
  - Main loop (up to max_iterations):
    - Yield observe event → call observe()
    - Yield decide event → call decide()
    - Check if stop → break
    - Yield act event → call act()
    - Yield reflect event → call reflect()
  - Process outbox messages
  - Handle exceptions → yield error event

- `async step() -> AgentStep`:
  - Execute single OODA cycle: observe → decide → act → reflect
  - Return final reflect step

**Communication Protocol**:

- `async send_message(to_agent_id: str, message: Message) -> None`
- `async receive_message(message: Message) -> None`
- `async _process_inbox() -> None`
- `async _process_outbox() -> None`
- `async _handle_message(message: Message) -> None` (abstract)

**Helper Methods** (Abstract - to be implemented by subclasses):

- `_create_sandbox() -> Any`
- `_init_empirica() -> Any`
- `_init_tavern_keeper() -> Any`
- `_init_decision_engine() -> Any`
- `async _validate_modification(modification: Modification) -> Dict[str, Any]`
- `async _apply_modification(modification: Modification) -> Dict[str, Any]`

### 4. Module Exports (`src/waft/core/agent/__init__.py`)

Export:

- BaseAgent
- AgentConfig, AgentState, AgentEvent, AgentStep
- Message, MessageRole, ToolDefinition
- EvolutionaryEvent, EvolutionaryEventType
- Modification

### 5. Work Effort Document

Create `_work_efforts/active/003_implement_agent_core.md`:

- Link to TKT-ai-sdk-002
- Track implementation progress
- Document design decisions

## Implementation Details

### Code Style

Follow existing codebase patterns:

- Use Pydantic BaseModel with Field() for validation
- Use type hints (typing module)
- Follow existing import patterns
- Use async/await for async methods
- Use pathlib.Path for paths
- Follow existing docstring format

### Dependencies

- pydantic (already in dependencies)
- typing (standard library)
- datetime (standard library)
- hashlib (standard library)
- json (standard library)
- inspect (standard library)
- abc (standard library)

### Integration Points (Placeholders)

- Empirica: `_init_empirica()` returns None for now
- TavernKeeper: `_init_tavern_keeper()` returns None for now
- Decision Engine: `_init_decision_engine()` returns None for now
- Sandbox: `_create_sandbox()` returns None for now

These will be implemented in future tickets.

### Genome ID Calculation

```python
def _compute_genome_id(self) -> str:
    genome_data = {
        "config": self.config.dict(),
        "code_hash": self._get_code_hash(),
        "state_version": self.state.state_version,
    }
    genome_json = json.dumps(genome_data, sort_keys=True)
    return sha256(genome_json.encode()).hexdigest()
```

### Flight Recorder Storage

Flight recorder is in-memory (List[EvolutionaryEvent]). Persistence will be added in future ticket.

## Testing Considerations

- Unit tests for Pydantic model validation
- Unit tests for genome_id computation (deterministic)
- Unit tests for spawn() lineage tracking
- Unit tests for flight recorder event recording
- Integration tests with existing systems (future)

## Files Created

1. `src/waft/core/agent/__init__.py` - Module exports
2. `src/waft/core/agent/state.py` - All Pydantic models (~400 lines)
3. `src/waft/core/agent/base.py` - BaseAgent class (~600 lines)
4. `_work_efforts/active/003_implement_agent_core.md` - Work effort tracking

## Next Steps (Future Tickets)

- Implement Gym integration for eval()
- Implement sandbox integration
- Implement Empirica/TavernKeeper/Decision Engine integrations
- Add flight recorder persistence
- Create example agent (RefactorAgent)
- Write comprehensive tests