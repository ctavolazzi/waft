---
name: Agent Interface Implementation
overview: Implement the BaseAgent class and example agent based on the completed design document, integrating with Waft's existing systems (Decision Engine, Empirica, TavernKeeper, Session Analytics).
todos:
  - id: agent-1
    content: Create Pydantic models (MessageRole, Message, ToolDefinition, AgentState, AgentConfig, AgentEvent, AgentStep, Modification) in src/waft/core/agent.py
    status: pending
  - id: agent-2
    content: Implement BaseAgent abstract class with __init__, abstract methods (observe, decide, act, reflect), and helper methods
    status: pending
  - id: agent-3
    content: Implement OODA loop execution (run() async iterator, step() single cycle) with message processing and error handling
    status: pending
  - id: agent-4
    content: Implement self-modification capability (modify_self() method with safety validation and rollback support)
    status: pending
  - id: agent-5
    content: Implement communication protocol (send_message, receive_message, _process_inbox, _process_outbox)
    status: pending
  - id: agent-6
    content: Integrate Decision Engine in decide() method using DecisionMatrixCalculator
    status: pending
  - id: agent-7
    content: Integrate Empirica in reflect() method and initialization using EmpiricaManager
    status: pending
  - id: agent-8
    content: Integrate TavernKeeper in act() method and initialization using TavernKeeper
    status: pending
  - id: agent-9
    content: Integrate Session Analytics throughout lifecycle using SessionAnalytics
    status: pending
  - id: agent-10
    content: Create RefactorAgent example in src/waft/core/agent_example.py with full OODA loop implementation
    status: pending
  - id: agent-11
    content: Create API reference documentation in docs/AGENT_INTERFACE.md
    status: pending
  - id: agent-12
    content: Write unit tests for models (test_agent_models.py), BaseAgent (test_agent.py), integration (test_agent_integration.py), and example (test_agent_example.py)
    status: pending

category: hopes
confidence: 0.71
constellation_date: 2026-01-14
---

# Agent Interface Implementation Plan

## Overview

Implement the `BaseAgent` class and example `RefactorAgent` based on the completed design document (`docs/designs/002_agent_interface.md`). This will create the foundation for Waft's self-modifying AI SDK by enabling agents to observe, decide, act, and reflect within Python projects.

## Current State

- **Design Phase**: ✅ Complete
  - Design document: `docs/designs/002_agent_interface.md`
  - Research document: `docs/research/state_of_art_2026.md`
  - Design includes: AgentState, AgentConfig, BaseAgent, OODA loop, integration points

- **Implementation Phase**: ⏳ Pending
  - Need to implement: `src/waft/core/agent.py`
  - Need to create: Example agent (`src/waft/core/agent_example.py`)
  - Need to document: API reference (`docs/AGENT_INTERFACE.md`)
  - Need to test: Unit and integration tests

## Architecture

The implementation follows the design document's architecture:

```
BaseAgent (Abstract)
  ├── AgentState (Pydantic model)
  ├── AgentConfig (Pydantic model)
  ├── OODA Loop (observe → decide → act → reflect)
  ├── Integration Points
  │   ├── Decision Engine (decision_matrix.py)
  │   ├── Empirica (empirica.py)
  │   ├── TavernKeeper (tavern_keeper/)
  │   └── Session Analytics (session_analytics.py)
  └── Self-Modification (modify_self method)
```

## Implementation Tasks

### Phase 1: Core Models (Foundation)

**Task 1.1**: Create Pydantic models for state and configuration
- **File**: `src/waft/core/agent.py`
- **Models to create**:
  - `MessageRole` (Enum)
  - `Message` (BaseModel)
  - `ToolDefinition` (BaseModel)
  - `AgentState` (BaseModel) - with all fields from design
  - `AgentConfig` (BaseModel) - with all fields from design
  - `AgentEvent` (BaseModel)
  - `AgentStep` (BaseModel)
  - `Modification` (BaseModel)
- **Dependencies**: `pydantic`, `datetime`, `typing`
- **Reference**: Design doc sections 1-2

**Task 1.2**: Add validation and serialization
- Add Pydantic validators for state transitions
- Add JSON serialization methods
- Add state versioning support
- **Reference**: Design doc section 1 (State Management Rules)

### Phase 2: BaseAgent Class (Core Implementation)

**Task 2.1**: Implement BaseAgent abstract class
- **File**: `src/waft/core/agent.py`
- **Methods to implement**:
  - `__init__()` - Initialize agent with config and project path
  - Abstract methods: `observe()`, `decide()`, `act()`, `reflect()`
  - Abstract helpers: `_create_sandbox()`, `_init_empirica()`, `_init_tavern_keeper()`, `_init_decision_engine()`, `_handle_message()`, `_validate_modification()`, `_apply_modification()`
- **Reference**: Design doc section 3

**Task 2.2**: Implement OODA loop execution
- **Methods**:
  - `run()` - Main execution loop (async iterator)
  - `step()` - Single OODA cycle
- **Features**:
  - Message processing (inbox/outbox)
  - Iteration limits
  - Error handling
  - Event emission
- **Reference**: Design doc sections 3, 5

**Task 2.3**: Implement self-modification capability
- **Method**: `modify_self()`
- **Features**:
  - Safety level validation
  - Modification validation pipeline
  - Rollback support
  - State versioning
- **Reference**: Design doc section 3 (Self-Modification), section 8 (Safety Model)

**Task 2.4**: Implement communication protocol
- **Methods**:
  - `send_message()` - Send to other agents
  - `receive_message()` - Receive from other agents
  - `_process_inbox()` - Process incoming messages
  - `_process_outbox()` - Process outgoing messages
- **Reference**: Design doc section 4

### Phase 3: Integration Points

**Task 3.1**: Integrate Decision Engine
- **File**: `src/waft/core/agent.py`
- **Integration**: Use `DecisionMatrixCalculator` from `decision_matrix.py`
- **Location**: In `decide()` method
- **Reference**: Design doc section 6 (Decision Engine)
- **Existing code**: `src/waft/core/decision_matrix.py`

**Task 3.2**: Integrate Empirica
- **File**: `src/waft/core/agent.py`
- **Integration**: Use `EmpiricaManager` from `empirica.py`
- **Location**: In `reflect()` method, initialization
- **Reference**: Design doc section 6 (Empirica)
- **Existing code**: `src/waft/core/empirica.py`

**Task 3.3**: Integrate TavernKeeper
- **File**: `src/waft/core/agent.py`
- **Integration**: Use `TavernKeeper` from `tavern_keeper/keeper.py`
- **Location**: In `act()` method, initialization
- **Reference**: Design doc section 6 (TavernKeeper)
- **Existing code**: `src/waft/core/tavern_keeper/keeper.py`

**Task 3.4**: Integrate Session Analytics
- **File**: `src/waft/core/agent.py`
- **Integration**: Use `SessionAnalytics` from `session_analytics.py`
- **Location**: Throughout lifecycle (observe, act, reflect)
- **Reference**: Design doc (implicit - for learning system)
- **Existing code**: `src/waft/core/session_analytics.py`

### Phase 4: Example Implementation

**Task 4.1**: Create RefactorAgent example
- **File**: `src/waft/core/agent_example.py`
- **Class**: `RefactorAgent(BaseAgent)`
- **Implementation**:
  - `observe()` - Scan for complex functions
  - `decide()` - Use decision engine to choose refactoring strategy
  - `act()` - Execute refactoring
  - `reflect()` - Learn from outcome
- **Reference**: Design doc section 7

**Task 4.2**: Add helper methods for RefactorAgent
- Code complexity analysis
- Function extraction logic
- Test execution
- **Reference**: Design doc section 7

### Phase 5: Documentation

**Task 5.1**: Create API reference documentation
- **File**: `docs/AGENT_INTERFACE.md`
- **Sections**:
  - Overview
  - BaseAgent API reference
  - AgentState schema
  - AgentConfig schema
  - OODA loop usage
  - Integration examples
  - Self-modification guide
  - Multi-agent communication
- **Reference**: Design doc + implementation

**Task 5.2**: Add docstrings to all classes and methods
- Follow Python docstring conventions
- Include type hints
- Add usage examples in docstrings
- **Files**: `src/waft/core/agent.py`, `src/waft/core/agent_example.py`

### Phase 6: Testing

**Task 6.1**: Unit tests for models
- **File**: `tests/test_agent_models.py`
- **Tests**:
  - AgentState validation
  - AgentConfig validation
  - Message protocol
  - State transitions
- **Reference**: Design doc section 9

**Task 6.2**: Unit tests for BaseAgent
- **File**: `tests/test_agent.py`
- **Tests**:
  - Initialization
  - OODA loop execution
  - Self-modification validation
  - Message handling
- **Reference**: Design doc section 9

**Task 6.3**: Integration tests
- **File**: `tests/test_agent_integration.py`
- **Tests**:
  - Decision Engine integration
  - Empirica integration
  - TavernKeeper integration
  - Session Analytics integration
- **Reference**: Design doc section 9

**Task 6.4**: Example agent tests
- **File**: `tests/test_agent_example.py`
- **Tests**:
  - RefactorAgent observe/decide/act/reflect
  - Refactoring logic
  - Error handling
- **Reference**: Design doc section 9

## File Structure

```
src/waft/core/
  ├── agent.py              # BaseAgent implementation (NEW)
  └── agent_example.py      # RefactorAgent example (NEW)

docs/
  └── AGENT_INTERFACE.md    # API reference (NEW)

tests/
  ├── test_agent_models.py      # Model tests (NEW)
  ├── test_agent.py             # BaseAgent tests (NEW)
  ├── test_agent_integration.py # Integration tests (NEW)
  └── test_agent_example.py     # Example agent tests (NEW)
```

## Dependencies

### Existing Dependencies (Already in project)
- `pydantic` - For models (already used)
- `typing` - Type hints
- `datetime` - Timestamps
- `pathlib` - Path handling

### New Dependencies (May need to add)
- None - All dependencies already available

### Integration Dependencies
- `src/waft/core/decision_matrix.py` - Decision Engine
- `src/waft/core/empirica.py` - Empirica Manager
- `src/waft/core/tavern_keeper/keeper.py` - TavernKeeper
- `src/waft/core/session_analytics.py` - Session Analytics

## Implementation Order

1. **Phase 1** (Foundation): Create Pydantic models - enables type safety
2. **Phase 2** (Core): Implement BaseAgent class - core functionality
3. **Phase 3** (Integration): Connect to existing systems - makes it functional
4. **Phase 4** (Example): Create RefactorAgent - demonstrates usage
5. **Phase 5** (Documentation): Write API docs - enables adoption
6. **Phase 6** (Testing): Write tests - ensures quality

## Success Criteria

- [ ] All Pydantic models implemented and validated
- [ ] BaseAgent class fully implemented with all abstract methods
- [ ] OODA loop executes correctly (observe → decide → act → reflect)
- [ ] All integration points working (Decision Engine, Empirica, TavernKeeper, Session Analytics)
- [ ] RefactorAgent example works end-to-end
- [ ] API documentation complete
- [ ] Unit tests passing (>80% coverage)
- [ ] Integration tests passing
- [ ] Example agent tests passing

## Risks & Mitigations

**Risk 1**: Integration complexity with existing systems
- **Mitigation**: Use existing manager classes, don't duplicate logic

**Risk 2**: Async/await complexity
- **Mitigation**: Follow design doc patterns, use async/await consistently

**Risk 3**: Self-modification safety
- **Mitigation**: Implement validation pipeline strictly, defer to safety model

**Risk 4**: State management complexity
- **Mitigation**: Use Pydantic for validation, immutable state updates

## Next Steps After Completion

1. Design Self-Modification Engine (TKT-ai-sdk-003) - depends on BaseAgent
2. Design Learning System (TKT-ai-sdk-004) - depends on BaseAgent + Session Analytics
3. Create more example agents (testing agent, documentation agent, etc.)

## References

- Design Document: `docs/designs/002_agent_interface.md`
- Vision Document: `docs/AI_SDK_VISION.md`
- Decision Matrix: `src/waft/core/decision_matrix.py`
- Empirica: `src/waft/core/empirica.py`
- TavernKeeper: `src/waft/core/tavern_keeper/keeper.py`
- Session Analytics: `src/waft/core/session_analytics.py`