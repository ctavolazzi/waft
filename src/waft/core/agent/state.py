"""
Agent State Models: The DNA of Waft agents.

Defines the Pydantic models for agent state, configuration, and evolutionary events.
"""

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
    timestamp: datetime = Field(default_factory=datetime.utcnow)
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

    # Private Journal (The Cogito)
    journal: List[Dict[str, Any]] = Field(default_factory=list, description="Private journal entries (Thoughts and Reflections)")
    short_term_memory: List[Dict[str, Any]] = Field(default_factory=list, description="Short-term memory buffer (recent thoughts/reflections)")

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

    # Metabolism (Energy System)
    energy: float = Field(default=100.0, description="Organism energy level (0.0-100.0)")

    # Anatomical Archetype (Linnaean Constraints)
    anatomical_symbol: str = Field(default="☿", description="Anatomical symbol (☿, ⚥, ⚲, ⴲ)")
    anatomical_archetype: str = Field(default="Social/Fluid", description="Archetype name")

    # Inventory (Marsupial Pouch & Appendage) - Capacity determined by archetype
    appendage: List[Dict[str, Any]] = Field(default_factory=list, description="Appendage items")
    pocket: List[Dict[str, Any]] = Field(default_factory=list, description="Pocket/Marsupial Pouch items")

    # Gestation (Reproduction)
    developing_seeds: List[Dict[str, Any]] = Field(default_factory=list, description="Developing seeds in pocket")
    gestation_pulses: Dict[str, int] = Field(default_factory=dict, description="Pulse count for each seed (seed_id -> pulses)")

    # Reproduction state
    last_conjugation_pulse: Optional[int] = Field(default=None, description="Last pulse when conjugation occurred")

    # Versioning
    state_version: int = Field(default=1, description="State schema version")
    last_updated: datetime = Field(default_factory=datetime.utcnow)


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

    # Metabolism (Energy System)
    energy_consumption_rate: float = Field(default=1.0, description="Energy consumed per OODA slice")

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


class Modification(BaseModel):
    """Self-modification request."""
    modification_type: str  # "code", "config", "prompt", "architecture", "behavior"
    target: str  # File path, config key, etc.
    change: Dict[str, Any]  # Modification details
    safety_level: int  # 1-4
    validation_required: bool = True


class EvolutionaryEventType(str, Enum):
    """Types of evolutionary events for scientific tracking."""
    SPAWN = "spawn"  # Agent reproduction (creates variant)
    MUTATE = "mutate"  # Code/config mutation
    GYM_EVAL = "gym_eval"  # Fitness evaluation in Gym
    DEATH = "death"  # Agent termination (fitness below threshold)
    SURVIVAL = "survival"  # Agent survives generation
    SESSION_END = "session_end"  # Session completion marker


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
