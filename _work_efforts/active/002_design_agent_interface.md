# Work Effort: Design Agent Interface (002)

## Status: In Progress
**Started**: 2026-01-09 01:20:00 PST  
**Last Updated**: 2026-01-09 01:20:00 PST

## Objective
Design the `BaseAgent` class interface for Waft's self-modifying AI SDK, combining best practices from LangGraph, AG2, CrewAI, and E2B with Waft's unique self-modification capabilities.

## Related Tickets
- **TKT-ai-sdk-002**: Design Agent base class and interface
- **Parent Work Effort**: WE-260109-ai-sdk (AI SDK Architecture)

## Tasks
1. [x] Research state-of-the-art agent architectures
2. [x] Create research document (`docs/research/state_of_art_2026.md`)
3. [x] Design AgentState schema (Pydantic model)
4. [x] Design AgentConfig schema (role/goal/backstory)
5. [x] Design BaseAgent abstract class
6. [x] Design communication protocol (inbox/outbox)
7. [x] Design OODA loop implementation
8. [x] Design self-modification method
9. [x] Create design document (`docs/designs/002_agent_interface.md`)
10. [x] Create work effort document (this file)

## Progress

### Completed
- ✅ **Research Phase**: Analyzed LangGraph, AG2, CrewAI, and E2B/OpenDevin patterns
- ✅ **Research Document**: Created `docs/research/state_of_art_2026.md` with architectural patterns
- ✅ **Design Document**: Created `docs/designs/002_agent_interface.md` with complete BaseAgent specification
- ✅ **State Schema**: Defined `AgentState` with message history, knowledge, tools, working memory
- ✅ **Configuration Schema**: Defined `AgentConfig` with role/goal/backstory pattern
- ✅ **Base Class**: Designed `BaseAgent` with OODA loop methods and self-modification capability
- ✅ **Communication Protocol**: Designed inbox/outbox pattern for multi-agent support
- ✅ **Integration Points**: Defined integration with Decision Engine, Empirica, TavernKeeper

### Key Design Decisions

1. **Hybrid State Management**
   - Combined LangGraph's explicit state schema with AG2's message protocol
   - State is a Pydantic model for type safety
   - Message history is primary state component

2. **Message-First Communication**
   - All agent communication via `Message` objects (AG2 protocol)
   - Supports both single-agent and multi-agent scenarios
   - Inbox/outbox pattern for swarm behavior

3. **Role-Based Identity**
   - Agents have explicit role/goal/backstory (CrewAI pattern)
   - Enables specialization and collaboration
   - Integrates with TavernKeeper personality system

4. **Safety-First Execution**
   - Sandboxing for code execution (E2B pattern)
   - 4-tier safety model integration
   - Validation pipeline before modifications

5. **Self-Modification Capability**
   - `modify_self()` method for agent evolution
   - Supports all 5 types of self-modification
   - Validation and rollback built-in

## Deliverables

1. **Research Document**: `docs/research/state_of_art_2026.md`
   - LangGraph: Graph state machines
   - AG2: Conversation as programming
   - CrewAI: Role-based delegation
   - E2B/OpenDevin: Sandboxing

2. **Design Document**: `docs/designs/002_agent_interface.md`
   - Complete BaseAgent specification
   - AgentState schema
   - AgentConfig schema
   - Communication protocol
   - OODA loop implementation
   - Self-modification method
   - Example implementation

3. **Work Effort Document**: `_work_efforts/active/002_design_agent_interface.md` (this file)

## Architecture Highlights

### State Schema (AgentState)
```python
class AgentState(BaseModel):
    memory: List[Message]  # Conversation history (AG2)
    knowledge: Dict[str, Any]  # Long-term storage
    tools: List[ToolDefinition]  # Available capabilities
    working_memory: Dict[str, Any]  # Scratchpad
    inbox: List[Message]  # Incoming messages
    outbox: List[Message]  # Outgoing messages
    # ... Waft-specific fields
```

### Base Class Methods
- `observe()` - Observe project state (OODA: Observe)
- `decide()` - Make decision (OODA: Orient/Decide)
- `act()` - Execute action (OODA: Act)
- `reflect()` - Reflect and learn (OODA: Reflect)
- `run()` - Main execution loop (AG2 protocol)
- `step()` - Single OODA cycle
- `modify_self()` - Self-modification (Waft unique)

### Communication Protocol
- **Inbox/Outbox**: Message queues for multi-agent communication
- **Message Routing**: Via message broker (Redis, RabbitMQ)
- **AG2 Compatible**: Messages follow AG2 protocol

## Integration Points

1. **Decision Engine**: Agents use Decision Matrix for reasoning
2. **Empirica**: Epistemic tracking for knowledge measurement
3. **TavernKeeper**: Personality and gamification
4. **Sandbox**: Isolated code execution
5. **Self-Modification Engine**: Safe code modification

## Next Steps

1. **Implementation Phase** (TKT-ai-sdk-002)
   - Implement `BaseAgent` class (`src/waft/core/agent.py`)
   - Implement `AgentState` and `AgentConfig` models
   - Implement sandbox integration
   - Create example agent (RefactorAgent)
   - Write tests

2. **Documentation Phase**
   - API reference documentation
   - Usage examples
   - Multi-agent guide

3. **Testing Phase**
   - Unit tests for BaseAgent
   - Integration tests with existing systems
   - Multi-agent swarm tests

## Notes

- Design is complete and ready for implementation
- All patterns from research document incorporated
- Supports both single-agent and multi-agent scenarios
- Self-modification capability is unique to Waft
- Safety model integrated throughout

## Links

- Research Document: `docs/research/state_of_art_2026.md`
- Design Document: `docs/designs/002_agent_interface.md`
- Ticket: `_work_efforts/WE-260109-ai-sdk_ai_sdk_architecture/tickets/TKT-ai-sdk-002_design_agent_interface.md`
- Parent Work Effort: `_work_efforts/WE-260109-ai-sdk_ai_sdk_architecture/WE-260109-ai-sdk_index.md`
