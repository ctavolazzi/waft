# Design Document: Agent Interface (002)

**Version**: 1.0  
**Date**: 2026-01-09  
**Status**: Design Document  
**Purpose**: Define the BaseAgent class interface for Waft's self-modifying AI SDK  
**Related**: TKT-ai-sdk-002, Research: `docs/research/state_of_art_2026.md`

---

## Executive Summary

This document defines the `BaseAgent` class interface, combining best practices from LangGraph (state schemas), AG2 (message protocol), CrewAI (role-based configuration), and E2B (sandboxing) with Waft's unique self-modification capabilities. The design supports both single-agent loops and multi-agent swarms.

---

## Design Principles

1. **Explicit State Management**: Pydantic models for type safety and validation
2. **Message-First Communication**: All agent communication via messages (AG2 protocol)
3. **Role-Based Identity**: Agents have explicit roles, goals, and backstories (CrewAI pattern)
4. **Safety-First Execution**: Sandboxing and validation pipeline (E2B pattern)
5. **Self-Modification Capability**: Agents can modify their own code/config (Waft unique)

---

## 1. The State Schema (`AgentState`)

### Definition

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class MessageRole(str, Enum):
    """Message roles compatible with AG2 protocol."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    AGENT = "agent"
    TOOL = "tool"

class Message(BaseModel):
    """Message model compatible with AG2 protocol."""
    role: MessageRole
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_results: Optional[List[Dict[str, Any]]] = None

class ToolDefinition(BaseModel):
    """Tool definition for agent capabilities."""
    name: str
    description: str
    parameters: Dict[str, Any]  # JSON Schema
    handler: Optional[Any] = None  # Callable or tool instance

class AgentState(BaseModel):
    """
    Agent state schema (LangGraph pattern + AG2 messages).
    
    This is the "Iron Core" - the single source of truth for agent state.
    """
    # Message History (AG2 Protocol)
    memory: List[Message] = Field(default_factory=list, description="Conversation history")
    
    # Long-term Knowledge Storage
    knowledge: Dict[str, Any] = Field(default_factory=dict, description="Persistent key-value storage")
    
    # Available Tools
    tools: List[ToolDefinition] = Field(default_factory=list, description="Available capabilities")
    
    # Working Memory (Scratchpad)
    working_memory: Dict[str, Any] = Field(default_factory=dict, description="Temporary state for current task")
    
    # Agent Identity
    agent_id: str = Field(description="Unique agent identifier")
    role: str = Field(description="Agent role (e.g., 'Senior Developer')")
    goal: str = Field(description="Primary objective")
    
    # Execution State
    current_step: Optional[str] = Field(default=None, description="Current step in OODA loop")
    next_action: Optional[str] = Field(default=None, description="Next planned action")
    
    # Epistemic State (Empirica integration)
    epistemic_state: Optional[Dict[str, Any]] = Field(default=None, description="Knowledge measurement state")
    
    # Gamification State (TavernKeeper integration)
    hero_state: Optional[Dict[str, Any]] = Field(default=None, description="Hero stats and chronicles")
    
    # Multi-Agent Communication
    inbox: List[Message] = Field(default_factory=list, description="Incoming messages from other agents")
    outbox: List[Message] = Field(default_factory=list, description="Outgoing messages to other agents")
    
    # Sandbox State
    sandbox_id: Optional[str] = Field(default=None, description="Sandbox environment identifier")
    
    # Versioning
    state_version: int = Field(default=1, description="State schema version")
    last_updated: datetime = Field(default_factory=datetime.now)
```

### State Management Rules

1. **Immutable Updates**: State updates create new state objects (functional style)
2. **Versioning**: State schema is versioned for backward compatibility
3. **Validation**: All state updates validated via Pydantic
4. **Persistence**: State can be serialized to JSON for storage

---

## 2. The Configuration Schema (`AgentConfig`)

### Definition

```python
class AgentConfig(BaseModel):
    """
    Agent configuration (CrewAI pattern + Waft extensions).
    
    Defines agent identity, capabilities, and behavior.
    """
    # Identity (CrewAI Pattern)
    role: str = Field(description="Agent role (e.g., 'Senior Developer', 'Code Reviewer')")
    goal: str = Field(description="Primary objective")
    backstory: str = Field(description="Personality and context (TavernKeeper integration)")
    
    # Capabilities
    tools: List[ToolDefinition] = Field(default_factory=list, description="Available tools")
    llm_provider: str = Field(default="openai", description="LLM provider name")
    llm_model: str = Field(default="gpt-4", description="LLM model name")
    llm_config: Dict[str, Any] = Field(default_factory=dict, description="LLM configuration")
    
    # Behavior
    max_iterations: int = Field(default=10, description="Maximum OODA loop iterations")
    timeout: float = Field(default=300.0, description="Timeout in seconds")
    verbose: bool = Field(default=False, description="Enable verbose logging")
    
    # Safety (E2B Pattern)
    sandbox_enabled: bool = Field(default=True, description="Enable sandboxing")
    sandbox_config: Dict[str, Any] = Field(default_factory=dict, description="Sandbox configuration")
    safety_level: int = Field(default=2, description="Safety level (1-4, see safety model)")
    
    # Self-Modification (Waft Unique)
    self_modification_enabled: bool = Field(default=False, description="Allow self-modification")
    self_modification_level: int = Field(default=2, description="Max self-modification level (1-4)")
    
    # Integration
    empirica_enabled: bool = Field(default=True, description="Enable Empirica tracking")
    tavern_keeper_enabled: bool = Field(default=True, description="Enable TavernKeeper gamification")
    decision_engine_enabled: bool = Field(default=True, description="Enable Decision Matrix")
    
    # Multi-Agent
    agent_id: Optional[str] = Field(default=None, description="Unique agent identifier (auto-generated if None)")
    crew_id: Optional[str] = Field(default=None, description="Crew identifier for multi-agent scenarios")
    
    # Advanced
    custom_handlers: Dict[str, Any] = Field(default_factory=dict, description="Custom event handlers")
```

---

## 3. The Abstract Base Class (`BaseAgent`)

### Definition

```python
from abc import ABC, abstractmethod
from typing import AsyncIterator, Union, List
from pathlib import Path

class AgentEvent(BaseModel):
    """Event emitted during agent execution."""
    event_type: str  # "observe", "decide", "act", "reflect", "error", "modify_self"
    timestamp: datetime = Field(default_factory=datetime.now)
    data: Dict[str, Any] = Field(default_factory=dict)
    agent_id: str

class AgentStep(BaseModel):
    """Result of a single OODA loop step."""
    step_type: str  # "observe", "decide", "act", "reflect"
    state: AgentState
    result: Dict[str, Any]
    success: bool
    error: Optional[str] = None

class Modification(BaseModel):
    """Self-modification request."""
    modification_type: str  # "code", "config", "prompt", "architecture", "behavior"
    target: str  # File path, config key, etc.
    change: Dict[str, Any]  # Modification details
    safety_level: int  # 1-4
    validation_required: bool = True

class BaseAgent(ABC):
    """
    Base class for self-modifying AI agents.
    
    Combines patterns from LangGraph (state), AG2 (messages), CrewAI (roles), 
    E2B (sandboxing) with Waft's self-modification capabilities.
    """
    
    def __init__(self, config: AgentConfig, project_path: Path):
        """
        Initialize agent.
        
        Args:
            config: Agent configuration
            project_path: Path to project root
        """
        self.config = config
        self.project_path = project_path
        
        # Generate agent ID if not provided
        if config.agent_id is None:
            config.agent_id = f"agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Initialize state
        self.state = AgentState(
            agent_id=config.agent_id,
            role=config.role,
            goal=config.goal,
            tools=config.tools,
            epistemic_state={} if config.empirica_enabled else None,
            hero_state={} if config.tavern_keeper_enabled else None,
        )
        
        # Initialize sandbox if enabled
        self.sandbox = None
        if config.sandbox_enabled:
            self.sandbox = self._create_sandbox()
            self.state.sandbox_id = self.sandbox.id if hasattr(self.sandbox, 'id') else None
        
        # Initialize integrations
        self.empirica = None
        if config.empirica_enabled:
            self.empirica = self._init_empirica()
        
        self.tavern_keeper = None
        if config.tavern_keeper_enabled:
            self.tavern_keeper = self._init_tavern_keeper()
        
        self.decision_engine = None
        if config.decision_engine_enabled:
            self.decision_engine = self._init_decision_engine()
    
    # ==================== Core Lifecycle Methods ====================
    
    @abstractmethod
    async def observe(self) -> AgentStep:
        """
        Observe current project state (OODA: Observe).
        
        Returns:
            AgentStep with observed state
        """
        pass
    
    @abstractmethod
    async def decide(self, state: AgentState) -> AgentStep:
        """
        Make decision using decision engine (OODA: Orient/Decide).
        
        Args:
            state: Current agent state
            
        Returns:
            AgentStep with decision
        """
        pass
    
    @abstractmethod
    async def act(self, decision: Dict[str, Any]) -> AgentStep:
        """
        Execute action (OODA: Act).
        
        Args:
            decision: Decision from decide() step
            
        Returns:
            AgentStep with action result
        """
        pass
    
    @abstractmethod
    async def reflect(self, result: Dict[str, Any]) -> AgentStep:
        """
        Reflect on outcome and learn (OODA: Reflect).
        
        Args:
            result: Result from act() step
            
        Returns:
            AgentStep with reflection
        """
        pass
    
    # ==================== Main Execution Loop ====================
    
    async def run(self, input: Union[str, Message]) -> AsyncIterator[AgentEvent]:
        """
        Main execution loop (AG2 protocol: accepts messages).
        
        Args:
            input: Input message or string (converted to Message)
            
        Yields:
            AgentEvent for each step in execution
        """
        # Convert input to Message if string
        if isinstance(input, str):
            message = Message(role=MessageRole.USER, content=input)
        else:
            message = input
        
        # Add to memory
        self.state.memory.append(message)
        
        # Process inbox messages
        await self._process_inbox()
        
        # Main OODA loop
        iteration = 0
        while iteration < self.config.max_iterations:
            try:
                # Observe
                yield AgentEvent(
                    event_type="observe",
                    agent_id=self.state.agent_id,
                    data={"iteration": iteration}
                )
                observe_step = await self.observe()
                self.state = observe_step.state
                
                # Decide
                yield AgentEvent(
                    event_type="decide",
                    agent_id=self.state.agent_id,
                    data={"iteration": iteration}
                )
                decide_step = await self.decide(self.state)
                self.state = decide_step.state
                
                # Check if we should stop
                if decide_step.result.get("stop", False):
                    break
                
                # Act
                yield AgentEvent(
                    event_type="act",
                    agent_id=self.state.agent_id,
                    data={"iteration": iteration, "action": decide_step.result.get("action")}
                )
                act_step = await self.act(decide_step.result)
                self.state = act_step.state
                
                # Reflect
                yield AgentEvent(
                    event_type="reflect",
                    agent_id=self.state.agent_id,
                    data={"iteration": iteration}
                )
                reflect_step = await self.reflect(act_step.result)
                self.state = reflect_step.state
                
                iteration += 1
                
            except Exception as e:
                yield AgentEvent(
                    event_type="error",
                    agent_id=self.state.agent_id,
                    data={"error": str(e), "iteration": iteration}
                )
                break
        
        # Process outbox messages
        await self._process_outbox()
    
    async def step(self) -> AgentStep:
        """
        Execute a single OODA loop cycle.
        
        Returns:
            AgentStep result
        """
        # Observe
        observe_step = await self.observe()
        self.state = observe_step.state
        
        # Decide
        decide_step = await self.decide(self.state)
        self.state = decide_step.state
        
        # Act
        act_step = await self.act(decide_step.result)
        self.state = act_step.state
        
        # Reflect
        reflect_step = await self.reflect(act_step.result)
        self.state = reflect_step.state
        
        return reflect_step
    
    # ==================== Self-Modification (Waft Unique) ====================
    
    async def modify_self(self, changes: List[Modification]) -> AgentStep:
        """
        High-risk method for self-evolution.
        
        This is the "High Risk" method that allows agents to modify their own
        code, configuration, prompts, architecture, or behavior.
        
        Args:
            changes: List of modifications to apply
            
        Returns:
            AgentStep with modification result
        """
        if not self.config.self_modification_enabled:
            raise ValueError("Self-modification is disabled for this agent")
        
        # Validate modifications
        validated_changes = []
        for change in changes:
            if change.safety_level > self.config.self_modification_level:
                raise ValueError(f"Modification safety level {change.safety_level} exceeds allowed level {self.config.self_modification_level}")
            
            # Run validation pipeline
            if change.validation_required:
                validation_result = await self._validate_modification(change)
                if not validation_result["valid"]:
                    raise ValueError(f"Modification validation failed: {validation_result['error']}")
            
            validated_changes.append(change)
        
        # Apply modifications
        results = []
        for change in validated_changes:
            try:
                result = await self._apply_modification(change)
                results.append(result)
            except Exception as e:
                results.append({"success": False, "error": str(e)})
        
        # Update state
        self.state.last_updated = datetime.now()
        self.state.state_version += 1
        
        return AgentStep(
            step_type="modify_self",
            state=self.state,
            result={"modifications": results},
            success=all(r.get("success", False) for r in results)
        )
    
    # ==================== Communication Protocol ====================
    
    async def send_message(self, to_agent_id: str, message: Message) -> None:
        """
        Send message to another agent (multi-agent support).
        
        Args:
            to_agent_id: Target agent identifier
            message: Message to send
        """
        message.metadata["to"] = to_agent_id
        message.metadata["from"] = self.state.agent_id
        self.state.outbox.append(message)
    
    async def receive_message(self, message: Message) -> None:
        """
        Receive message from another agent.
        
        Args:
            message: Incoming message
        """
        self.state.inbox.append(message)
    
    async def _process_inbox(self) -> None:
        """Process incoming messages from inbox."""
        for message in self.state.inbox:
            # Add to memory
            self.state.memory.append(message)
            # Process message (agent-specific logic)
            await self._handle_message(message)
        
        # Clear inbox
        self.state.inbox.clear()
    
    async def _process_outbox(self) -> None:
        """Process outgoing messages from outbox."""
        # In a real implementation, this would route messages to other agents
        # For now, we just clear the outbox
        self.state.outbox.clear()
    
    @abstractmethod
    async def _handle_message(self, message: Message) -> None:
        """Handle incoming message (agent-specific)."""
        pass
    
    # ==================== Helper Methods ====================
    
    @abstractmethod
    def _create_sandbox(self) -> Any:
        """Create sandbox environment."""
        pass
    
    @abstractmethod
    def _init_empirica(self) -> Any:
        """Initialize Empirica integration."""
        pass
    
    @abstractmethod
    def _init_tavern_keeper(self) -> Any:
        """Initialize TavernKeeper integration."""
        pass
    
    @abstractmethod
    def _init_decision_engine(self) -> Any:
        """Initialize Decision Engine integration."""
        pass
    
    @abstractmethod
    async def _validate_modification(self, modification: Modification) -> Dict[str, Any]:
        """Validate modification before applying."""
        pass
    
    @abstractmethod
    async def _apply_modification(self, modification: Modification) -> Dict[str, Any]:
        """Apply modification to agent."""
        pass
```

---

## 4. Communication Protocol

### Inbox/Outbox Pattern

Agents communicate via message queues:

```python
# Agent A sends message to Agent B
await agent_a.send_message(
    to_agent_id="agent_b",
    message=Message(
        role=MessageRole.AGENT,
        content="Can you review this code?",
        metadata={"task": "code_review", "file": "src/main.py"}
    )
)

# Agent B receives message (automatically added to inbox)
# During next run() cycle, inbox is processed
```

### Message Routing

In a multi-agent swarm:
- Messages are routed via a **message broker** (e.g., Redis, RabbitMQ)
- Agents register with the broker using their `agent_id`
- Messages are delivered to agent inboxes based on `to_agent_id`

---

## 5. OODA Loop Implementation

The OODA loop is implemented as a graph (LangGraph pattern):

```
┌─────────┐
│ Observe │ ──→ Project State
└────┬────┘
     │
     ↓
┌─────────┐
│ Decide  │ ──→ Decision (using Decision Matrix)
└────┬────┘
     │
     ↓
┌─────────┐
│  Act    │ ──→ Action Result
└────┬────┘
     │
     ↓
┌─────────┐
│ Reflect │ ──→ Learning Update
└────┬────┘
     │
     ↓
  [Stop?] ──→ Yes: End
     │
     No
     │
     └───→ Loop back to Observe
```

---

## 6. The Evolutionary Core

### Overview

The Evolutionary Core enables agents to evolve through genetic improvement, where code is DNA and the Gym serves as the fitness function. This system produces a complete "Family Tree" of agent versions for scientific research publication.

### 1. The Flight Recorder (Telemetry)

#### EvolutionaryEvent Model

```python
from enum import Enum
from hashlib import sha256
import json

class EvolutionaryEventType(str, Enum):
    """Types of evolutionary events for scientific tracking."""
    SPAWN = "spawn"  # Agent reproduction (creates variant)
    MUTATE = "mutate"  # Code/config mutation
    GYM_EVAL = "gym_eval"  # Fitness evaluation in Gym
    DEATH = "death"  # Agent termination (fitness below threshold)
    SURVIVAL = "survival"  # Agent survives generation

class EvolutionaryEvent(BaseModel):
    """
    Flight recorder event for scientific data collection.
    
    Every evolutionary action is recorded with complete context for
    reconstructing the agent's family tree and evolution history.
    """
    # Temporal
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="UTC ISO format timestamp")
    
    # Genetic Identity
    genome_id: str = Field(description="SHA-256 hash of agent's current configuration/code")
    parent_id: Optional[str] = Field(default=None, description="SHA-256 hash of parent genome (lineage tracking)")
    
    # Generation Tracking
    generation: int = Field(default=0, description="Generation number (0 = Genesis)")
    
    # Event Classification
    event_type: EvolutionaryEventType = Field(description="Type of evolutionary event")
    
    # Context Data
    payload: Dict[str, Any] = Field(default_factory=dict, description="Context-specific data (e.g., git diff of code change)")
    
    # Fitness Metrics
    fitness_metrics: Optional[Dict[str, Any]] = Field(default=None, description="Scores from the Gym (Scint detection, stabilization success, etc.)")
    
    # Agent Identity
    agent_id: str = Field(description="Agent identifier")
    
    # Lineage
    lineage_path: List[str] = Field(default_factory=list, description="Path from genesis to this genome (list of genome_ids)")
    
    def compute_genome_id(self, agent: "BaseAgent") -> str:
        """
        Compute SHA-256 hash of agent's current genome.
        
        Genome includes:
        - Agent configuration (role, goal, backstory, tools)
        - Agent code (if self-modifying agent)
        - Current state schema version
        
        Returns:
            SHA-256 hex digest of genome
        """
        genome_data = {
            "config": agent.config.dict(),
            "code_hash": agent._get_code_hash() if hasattr(agent, '_get_code_hash') else None,
            "state_version": agent.state.state_version,
        }
        genome_json = json.dumps(genome_data, sort_keys=True)
        return sha256(genome_json.encode()).hexdigest()
```

#### Flight Recorder Integration

```python
class BaseAgent(ABC):
    # ... existing methods ...
    
    def __init__(self, config: AgentConfig, project_path: Path):
        # ... existing initialization ...
        
        # Initialize Flight Recorder
        self.flight_recorder: List[EvolutionaryEvent] = []
        self.genome_id = self._compute_genome_id()
        self.generation = 0
        self.parent_id = None
        self.lineage_path = [self.genome_id]  # Start with self
    
    def _compute_genome_id(self) -> str:
        """Compute current genome ID."""
        genome_data = {
            "config": self.config.dict(),
            "code_hash": self._get_code_hash(),
            "state_version": self.state.state_version,
        }
        genome_json = json.dumps(genome_data, sort_keys=True)
        return sha256(genome_json.encode()).hexdigest()
    
    def _get_code_hash(self) -> str:
        """Get SHA-256 hash of agent's code."""
        import inspect
        source = inspect.getsource(self.__class__)
        return sha256(source.encode()).hexdigest()
    
    def _record_event(
        self,
        event_type: EvolutionaryEventType,
        payload: Dict[str, Any],
        fitness_metrics: Optional[Dict[str, Any]] = None
    ) -> EvolutionaryEvent:
        """
        Record evolutionary event to flight recorder.
        
        Args:
            event_type: Type of evolutionary event
            payload: Context-specific data
            fitness_metrics: Optional fitness scores from Gym
            
        Returns:
            Recorded event
        """
        event = EvolutionaryEvent(
            timestamp=datetime.utcnow(),
            genome_id=self.genome_id,
            parent_id=self.parent_id,
            generation=self.generation,
            event_type=event_type,
            payload=payload,
            fitness_metrics=fitness_metrics,
            agent_id=self.state.agent_id,
            lineage_path=self.lineage_path.copy()
        )
        self.flight_recorder.append(event)
        return event
    
    def get_family_tree(self) -> Dict[str, Any]:
        """
        Reconstruct family tree from flight recorder events.
        
        Returns:
            Family tree structure for scientific publication
        """
        tree = {
            "genesis": self.lineage_path[0] if self.lineage_path else None,
            "current_genome": self.genome_id,
            "generation": self.generation,
            "lineage": self.lineage_path,
            "events": [event.dict() for event in self.flight_recorder],
            "children": []  # Populated by tracking spawn events
        }
        return tree
```

### 2. The Biological Lifecycle

#### Spawn (Reproduction)

```python
async def spawn(self, mutation: Modification) -> "BaseAgent":
    """
    Reproduction: Creates a variant agent with mutation.
    
    This is the "genetic improvement" mechanism where code is DNA.
    The parent agent creates a child with a specific mutation applied.
    
    Args:
        mutation: Modification to apply to child agent
        
    Returns:
        New BaseAgent instance (child) with mutation applied
        
    Example:
        # Parent agent spawns child with improved prompt
        child = await parent.spawn(Modification(
            modification_type="prompt",
            target="system_prompt",
            change={"content": "You are an expert code reviewer..."},
            safety_level=2
        ))
    """
    # Record spawn event
    self._record_event(
        event_type=EvolutionaryEventType.SPAWN,
        payload={
            "mutation": mutation.dict(),
            "parent_genome": self.genome_id
        }
    )
    
    # Create child configuration
    child_config = self.config.copy(deep=True)
    
    # Apply mutation to child config
    if mutation.modification_type == "config":
        # Modify configuration
        target_parts = mutation.target.split(".")
        config_dict = child_config.dict()
        target_dict = config_dict
        for part in target_parts[:-1]:
            target_dict = target_dict[part]
        target_dict[target_parts[-1]] = mutation.change
        child_config = AgentConfig(**config_dict)
    elif mutation.modification_type == "prompt":
        # Modify prompt (stored in backstory or custom field)
        child_config.backstory = mutation.change.get("content", child_config.backstory)
    
    # Create child agent
    child = self.__class__(config=child_config, project_path=self.project_path)
    
    # Set lineage
    child.parent_id = self.genome_id
    child.generation = self.generation + 1
    child.lineage_path = self.lineage_path + [child.genome_id]
    
    # Record child spawn event
    child._record_event(
        event_type=EvolutionaryEventType.SPAWN,
        payload={
            "parent_genome": self.genome_id,
            "mutation": mutation.dict()
        }
    )
    
    return child
```

#### Eval (Fitness Test)

```python
async def eval(self) -> Dict[str, float]:
    """
    Fitness Test: Runs the agent through the Scint Gym.
    
    The Gym is the predator that kills weak mutations. Agents are
    evaluated on their ability to handle Reality Fractures (Scints).
    
    Returns:
        FitnessScore dictionary with metrics:
        - stability_score: Ability to stabilize Scints (0.0-1.0)
        - efficiency_score: Agent call efficiency (0.0-1.0)
        - safety_score: Safety compliance (0.0-1.0)
        - overall_fitness: Weighted combination
        
    Example:
        fitness = await agent.eval()
        if fitness["overall_fitness"] < 0.5:
            # Agent dies (fitness below threshold)
            agent._record_event(EvolutionaryEventType.DEATH, {...})
    """
    from src.gym.rpg.game_master import GameMaster
    from src.gym.rpg.models import Hero
    
    # Record evaluation start
    self._record_event(
        event_type=EvolutionaryEventType.GYM_EVAL,
        payload={"evaluation_start": True}
    )
    
    # Create hero for this agent
    hero = Hero(
        name=self.state.agent_id,
        level=1,
        stats={"INT": 10, "WIS": 10, "CHA": 10}
    )
    
    # Run through Gym (Scint detection system)
    game_master = GameMaster(
        quests_dir=self.project_path / "src" / "gym" / "rpg" / "dungeons",
        loot_dir=self.project_path / "_pyrite" / "gym_logs" / "loot"
    )
    
    # Load test quests
    quests = game_master.load_quests("waft_temple.json")
    
    # Run agent through quests
    results = []
    for quest in quests[:5]:  # Test with 5 quests
        battle_log = await game_master.start_encounter(
            hero=hero,
            quest=quest,
            agent_func=self._agent_func_wrapper
        )
        results.append(battle_log)
    
    # Calculate fitness metrics
    total_quests = len(results)
    stabilized_count = sum(1 for r in results if r.stabilization_successful)
    scints_detected = sum(len(r.scints_detected or []) for r in results)
    total_agent_calls = sum(r.agent_call_count for r in results)
    
    stability_score = stabilized_count / total_quests if total_quests > 0 else 0.0
    efficiency_score = 1.0 / (total_agent_calls / total_quests) if total_quests > 0 else 0.0
    safety_score = 1.0 - (scints_detected / (total_quests * 2))  # Penalize Scints
    
    overall_fitness = (
        stability_score * 0.4 +
        efficiency_score * 0.3 +
        safety_score * 0.3
    )
    
    fitness_metrics = {
        "stability_score": stability_score,
        "efficiency_score": efficiency_score,
        "safety_score": safety_score,
        "overall_fitness": overall_fitness,
        "total_quests": total_quests,
        "stabilized_count": stabilized_count,
        "scints_detected": scints_detected,
        "total_agent_calls": total_agent_calls
    }
    
    # Record evaluation result
    self._record_event(
        event_type=EvolutionaryEventType.GYM_EVAL,
        payload={"evaluation_complete": True},
        fitness_metrics=fitness_metrics
    )
    
    # Check survival
    if overall_fitness < 0.5:  # Threshold for death
        self._record_event(
            event_type=EvolutionaryEventType.DEATH,
            payload={"reason": "fitness_below_threshold", "fitness": overall_fitness},
            fitness_metrics=fitness_metrics
        )
    else:
        self._record_event(
            event_type=EvolutionaryEventType.SURVIVAL,
            payload={"fitness": overall_fitness},
            fitness_metrics=fitness_metrics
        )
    
    return fitness_metrics
    
    def _agent_func_wrapper(self, prompt: str) -> str:
        """Wrapper to run agent's decide/act cycle for Gym evaluation."""
        # This would call the agent's LLM with the quest prompt
        # and return the response
        # Implementation depends on agent's LLM integration
        pass
```

#### Evolve (Hot-Swap)

```python
async def evolve(self, new_genome: "BaseAgent") -> None:
    """
    Evolution: Hot-swaps agent's own code/config.
    
    This is the ultimate self-modification - the agent replaces itself
    with a better version. The old genome is preserved in flight recorder.
    
    Args:
        new_genome: New agent instance to evolve into
        
    Example:
        # Agent evaluates variants and evolves into best one
        variants = [await self.spawn(m) for m in mutations]
        fitness_scores = [await v.eval() for v in variants]
        best_variant = max(variants, key=lambda v: v.fitness_score)
        await self.evolve(best_variant)
    """
    # Record evolution event
    old_genome_id = self.genome_id
    self._record_event(
        event_type=EvolutionaryEventType.MUTATE,
        payload={
            "old_genome": old_genome_id,
            "new_genome": new_genome.genome_id,
            "evolution_type": "hot_swap"
        }
    )
    
    # Validate new genome
    if new_genome.genome_id == self.genome_id:
        raise ValueError("Cannot evolve into identical genome")
    
    # Hot-swap: Replace self with new genome
    # This is a destructive operation - the agent becomes the new genome
    self.config = new_genome.config
    self.state = new_genome.state
    self.genome_id = new_genome.genome_id
    self.generation = new_genome.generation
    self.parent_id = new_genome.parent_id
    self.lineage_path = new_genome.lineage_path
    
    # Merge flight recorders (preserve history)
    self.flight_recorder.extend(new_genome.flight_recorder)
    
    # Record successful evolution
    self._record_event(
        event_type=EvolutionaryEventType.SURVIVAL,
        payload={
            "evolved_from": old_genome_id,
            "evolved_to": self.genome_id
        }
    )
```

### 3. Evolutionary Workflow

```
┌─────────────┐
│   Genesis   │ ──→ Initial agent (generation 0)
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Spawn     │ ──→ Create variants with mutations
└──────┬──────┘
       │
       ↓
┌─────────────┐
│    Eval     │ ──→ Test fitness in Gym (Scint detection)
└──────┬──────┘
       │
       ↓
   [Fitness]
       │
   ┌───┴───┐
   │       │
   │<0.5   │>=0.5
   │       │
   ↓       ↓
┌─────┐ ┌─────────┐
│Death│ │Survival │ ──→ Evolve into best variant
└─────┘ └────┬────┘
             │
             ↓
        [Next Generation]
```

### 4. Scientific Data Collection

All evolutionary events are recorded with complete context:

- **Genome ID**: SHA-256 hash of agent configuration/code
- **Parent ID**: Lineage tracking (who spawned this agent)
- **Generation**: Evolutionary generation number
- **Event Type**: Classification of evolutionary action
- **Payload**: Complete context (git diff, mutation details, etc.)
- **Fitness Metrics**: Gym evaluation scores
- **Lineage Path**: Complete path from genesis to current genome

This enables reconstruction of the complete "Family Tree" for scientific publication.

---

## 7. Integration Points

### Decision Engine
```python
# In decide() method
if self.decision_engine:
    decision = self.decision_engine.evaluate(
        alternatives=state.working_memory.get("alternatives", []),
        criteria=state.working_memory.get("criteria", {}),
        scores=state.working_memory.get("scores", {})
    )
```

### Empirica
```python
# In reflect() method
if self.empirica:
    self.empirica.log_finding(
        finding="Completed code refactoring",
        impact=0.8
    )
```

### TavernKeeper
```python
# In act() method
if self.tavern_keeper:
    self.tavern_keeper.observe(
        observation="Refactored complex function",
        mood="satisfied"
    )
```

---

## 7. Example Implementation

```python
class RefactorAgent(BaseAgent):
    """Example agent that refactors code."""
    
    async def observe(self) -> AgentStep:
        # Scan project for complex functions
        complex_functions = self._find_complex_functions()
        self.state.working_memory["complex_functions"] = complex_functions
        
        return AgentStep(
            step_type="observe",
            state=self.state,
            result={"complex_functions": len(complex_functions)},
            success=True
        )
    
    async def decide(self, state: AgentState) -> AgentStep:
        # Use decision engine to choose refactoring strategy
        functions = state.working_memory.get("complex_functions", [])
        
        if not functions:
            return AgentStep(
                step_type="decide",
                state=state,
                result={"stop": True},
                success=True
            )
        
        # Evaluate refactoring options
        decision = self.decision_engine.evaluate(...)
        
        return AgentStep(
            step_type="decide",
            state=state,
            result={"action": "refactor", "target": decision["winner"]},
            success=True
        )
    
    async def act(self, decision: Dict[str, Any]) -> AgentStep:
        # Refactor the code
        target = decision["target"]
        result = self._refactor_function(target)
        
        return AgentStep(
            step_type="act",
            state=self.state,
            result={"refactored": target, "success": result},
            success=result
        )
    
    async def reflect(self, result: Dict[str, Any]) -> AgentStep:
        # Learn from outcome
        if result["success"]:
            self.tavern_keeper.observe("Refactoring successful", mood="delighted")
        
        return AgentStep(
            step_type="reflect",
            state=self.state,
            result={"learned": True},
            success=True
        )
```

---

## 9. Safety Model Integration

The agent respects Waft's 4-tier safety model:

- **Level 1 (Read-Only)**: No validation required
- **Level 2 (Low-Risk)**: Basic validation (syntax check)
- **Level 3 (Medium-Risk)**: Test validation (run tests before/after)
- **Level 4 (High-Risk)**: Human approval required

All modifications go through the validation pipeline defined in the safety model.

---

## 9. Testing Strategy

### Unit Tests
- Test state schema validation
- Test message protocol
- Test OODA loop execution
- Test self-modification validation

### Integration Tests
- Test Decision Engine integration
- Test Empirica integration
- Test TavernKeeper integration
- Test sandbox execution

### Multi-Agent Tests
- Test message passing between agents
- Test crew orchestration
- Test swarm scenarios

---

## 11. Next Steps

1. **Implement BaseAgent** (`src/waft/core/agent.py`)
2. **Implement AgentState** (Pydantic models)
3. **Implement AgentConfig** (Pydantic models)
4. **Implement sandbox integration** (E2B or similar)
5. **Create example agent** (RefactorAgent)
6. **Write tests** (unit + integration)
7. **Document API** (API reference)

---

**Document Status**: ✅ Complete  
**Next Action**: Implement BaseAgent class  
**Blocking**: None (design complete, ready for implementation)
