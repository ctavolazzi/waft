# State of the Art: Agent Architecture Patterns (2026)

**Date**: 2026-01-09  
**Purpose**: Research summary of leading agent frameworks to inform Waft's BaseAgent design  
**Status**: Foundation Document

---

## Executive Summary

This document synthesizes architectural patterns from four leading agent frameworks (LangGraph, AG2, CrewAI, E2B/OpenDevin) to inform the design of Waft's `BaseAgent` class. The goal is to create a "Hybrid Core" that combines the best patterns while maintaining Waft's unique self-modification capabilities.

---

## 1. LangGraph: Graph State Machines

### Core Pattern
**Agents are loops with strict state schemas.**

### Key Architectural Elements

#### State Schema (Pydantic Model)
```python
class AgentState(TypedDict):
    messages: List[BaseMessage]  # Conversation history
    next: str  # Next node in graph
    # ... custom fields
```

#### Graph-Based Execution
- Agents are defined as **directed graphs** (nodes = steps, edges = transitions)
- State flows through graph nodes
- Each node is a function that receives state and returns updated state
- Conditional edges allow branching logic

#### Key Strengths
1. **Explicit Control Flow**: Graph visualization makes agent logic transparent
2. **State Management**: Typed state schema prevents errors
3. **Composability**: Graphs can be nested and reused
4. **Debugging**: Easy to trace execution path through graph

#### Key Limitations
1. **Static Structure**: Graph must be defined upfront (harder to modify dynamically)
2. **Complexity**: Large graphs become hard to manage
3. **Learning**: No built-in mechanism for graph evolution

### Waft Application
- **Adopt**: State schema pattern (Pydantic model for `AgentState`)
- **Adopt**: Explicit state transitions (OODA loop as graph nodes)
- **Enhance**: Allow graph modification (self-modification capability)

---

## 2. AG2: Conversation as Programming

### Core Pattern
**Agents must support peer-to-peer message passing.**

### Key Architectural Elements

#### Message Protocol
```python
class Message(BaseModel):
    role: str  # "user", "assistant", "system", "agent"
    content: str
    metadata: Dict[str, Any]  # Tool calls, citations, etc.
```

#### Conversation-First Design
- Agents communicate via **messages**, not function calls
- Messages are the primary abstraction (not state objects)
- Supports multi-turn conversations naturally
- Tool calls are embedded in messages (not separate API)

#### Key Strengths
1. **Interoperability**: Messages work across different agent implementations
2. **Natural Communication**: Mirrors human conversation patterns
3. **Tool Integration**: Tools are invoked via message metadata
4. **Multi-Agent**: Easy to route messages between agents

#### Key Limitations
1. **State Management**: Less explicit than LangGraph's state schema
2. **Control Flow**: Conversation flow is implicit (harder to visualize)
3. **Performance**: Message passing overhead for internal operations

### Waft Application
- **Adopt**: Message-based communication protocol
- **Adopt**: Message history as primary state component
- **Enhance**: Add explicit state schema alongside messages (hybrid approach)

---

## 3. CrewAI: Role-Based Delegation

### Core Pattern
**Agents need distinct "Personas" and "Duties" defined in their config.**

### Key Architectural Elements

#### Agent Configuration
```python
class AgentConfig(BaseModel):
    role: str  # "Senior Developer", "Code Reviewer", etc.
    goal: str  # Primary objective
    backstory: str  # Personality and context
    tools: List[Tool]  # Available capabilities
    verbose: bool  # Logging level
```

#### Role-Based Architecture
- Each agent has a **role** (what they are)
- Each agent has a **goal** (what they want to achieve)
- Each agent has a **backstory** (personality and context)
- Agents are **delegated** tasks based on their role

#### Crew Orchestration
- Multiple agents work together in a **crew**
- Tasks are assigned to agents based on role matching
- Agents collaborate through shared context

#### Key Strengths
1. **Clarity**: Role/goal/backstory makes agent purpose explicit
2. **Specialization**: Agents can be experts in specific domains
3. **Collaboration**: Natural multi-agent workflows
4. **Personality**: Backstory enables narrative and gamification

#### Key Limitations
1. **Rigidity**: Roles are static (hard to adapt)
2. **Coordination**: Crew orchestration adds complexity
3. **State**: Less explicit state management than LangGraph

### Waft Application
- **Adopt**: Role/goal/backstory configuration pattern
- **Adopt**: Persona system (aligns with TavernKeeper)
- **Enhance**: Allow role/goal evolution (self-modification)

---

## 4. E2B/OpenDevin: Sandboxing

### Core Pattern
**Execution must be isolated.**

### Key Architectural Elements

#### Sandbox Environment
- Agents execute code in **isolated containers**
- File system is ephemeral (or controlled)
- Network access is restricted
- Resource limits (CPU, memory, time)

#### Safety Model
- **Read-only** operations: Safe, no validation needed
- **Write operations**: Validated before execution
- **System calls**: Restricted or monitored
- **Rollback**: Automatic on failure

#### Key Strengths
1. **Safety**: Prevents agents from damaging host system
2. **Reproducibility**: Isolated environments are consistent
3. **Security**: Limits attack surface
4. **Testing**: Can test agent code safely

#### Key Limitations
1. **Performance**: Container overhead
2. **Complexity**: Sandbox management adds infrastructure
3. **Limitations**: Some operations may be impossible in sandbox

### Waft Application
- **Adopt**: Sandboxing for code execution
- **Adopt**: Safety validation pipeline
- **Enhance**: Integrate with Waft's 4-tier safety model

---

## Synthesis: The Hybrid Core

### Combined Pattern for Waft's BaseAgent

#### 1. State Schema (from LangGraph)
```python
class AgentState(BaseModel):
    memory: List[Message]  # Conversation history (AG2 style)
    knowledge: Dict[str, Any]  # Long-term storage
    tools: List[ToolDefinition]  # Available capabilities
    working_memory: Dict[str, Any]  # Scratchpad
    # ... Waft-specific fields
```

#### 2. Message Protocol (from AG2)
- Agents communicate via `Message` objects
- Message history is primary state component
- Tool calls embedded in messages
- Supports peer-to-peer communication

#### 3. Role-Based Configuration (from CrewAI)
```python
class AgentConfig(BaseModel):
    role: str  # "Senior Developer", "Code Reviewer", etc.
    goal: str  # Primary objective
    backstory: str  # Personality (TavernKeeper integration)
    tools: List[Tool]  # Available capabilities
    # ... Waft-specific fields
```

#### 4. Sandboxing (from E2B/OpenDevin)
- Code execution in isolated environment
- Safety validation before modifications
- Automatic rollback on failure
- Resource limits and monitoring

### Waft's Unique Additions

1. **Self-Modification**: Agents can modify their own code/config
2. **Learning System**: Agents adapt from experience
3. **Epistemic Tracking**: Empirica integration for knowledge measurement
4. **Decision Engine**: Mathematical decision framework
5. **Gamification**: TavernKeeper integration for personality

---

## Design Principles

### 1. Explicit State Management
- Use Pydantic models for type safety
- State schema is versioned and validated
- State transitions are explicit and traceable

### 2. Message-First Communication
- All agent communication via messages
- Message history is primary state
- Supports both single-agent and multi-agent scenarios

### 3. Role-Based Identity
- Agents have explicit roles, goals, and backstories
- Enables specialization and collaboration
- Integrates with TavernKeeper personality system

### 4. Safety-First Execution
- All code execution in sandbox
- Validation pipeline before modifications
- Automatic rollback on failure
- Resource limits and monitoring

### 5. Self-Modification Capability
- Agents can modify their own code/config
- Modifications validated and reversible
- Learning system adapts from experience

---

## Implementation Priorities

### Phase 1: Core Agent Interface
1. Define `AgentState` schema (Pydantic model)
2. Define `AgentConfig` schema (role/goal/backstory)
3. Implement `BaseAgent` abstract class
4. Implement message protocol

### Phase 2: Execution Engine
1. Implement OODA loop as graph (LangGraph pattern)
2. Implement sandboxing (E2B pattern)
3. Integrate safety validation pipeline
4. Implement rollback system

### Phase 3: Multi-Agent Support
1. Implement inbox/outbox message queues
2. Implement agent discovery and routing
3. Implement crew orchestration (CrewAI pattern)
4. Test swarm scenarios

### Phase 4: Self-Modification
1. Implement `modify_self()` method
2. Integrate with Self-Modification Engine
3. Implement learning system
4. Test agent evolution

---

## References

- **LangGraph**: https://github.com/langchain-ai/langgraph
- **AG2**: Anthropic's Agent Protocol v2
- **CrewAI**: https://github.com/joaomdmoura/crewAI
- **E2B**: https://e2b.dev/
- **OpenDevin**: https://github.com/OpenDevin/OpenDevin

---

**Document Status**: ✅ Complete  
**Next Action**: Design BaseAgent interface (002_agent_interface.md)  
**Blocking**: None (research complete, ready for design)
