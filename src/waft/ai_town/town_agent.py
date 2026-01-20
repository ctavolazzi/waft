"""
TownAgent: AI agents that live in the virtual town.

Agents can:
- Move around the town
- Have conversations with other agents
- Remember past conversations
- Make decisions about what to do
- Form relationships
"""

import random
from datetime import datetime
from pathlib import Path
from typing import Any

from ..core.agent.base import BaseAgent
from ..core.agent.state import AgentConfig, AgentState


class TownAgent(BaseAgent):
    """
    An agent that lives in AI Town.

    Extends BaseAgent with town-specific capabilities:
    - Position in town
    - Conversation state
    - Memory of past conversations
    - Social relationships
    """

    def __init__(
        self,
        config: AgentConfig,
        project_path: Path,
        name: str,
        personality: dict[str, Any] | None = None,
        position: dict[str, float] | None = None,
    ):
        """
        Initialize a town agent.

        Args:
            config: Agent configuration
            project_path: Path to project root
            name: Agent's name
            personality: Personality traits (curiosity, sociability, etc.)
            position: Initial position in town (x, y)
        """
        super().__init__(config, project_path)

        self.name = name
        self.personality = personality or {
            "curiosity": random.uniform(0.3, 0.9),
            "sociability": random.uniform(0.3, 0.9),
            "energy": random.uniform(0.5, 1.0),
        }

        # Town-specific state
        self.position = position or {
            "x": random.uniform(0, 100),
            "y": random.uniform(0, 100),
        }

        self.current_conversation: str | None = None
        self.conversation_partners: list[str] = []  # Agent IDs
        self.memories: list[dict[str, Any]] = []  # Conversation memories
        self.relationships: dict[str, float] = {}  # Agent ID -> relationship score

        # Activity state
        self.current_activity: str | None = None
        self.activity_until: float | None = None

        # Initialize agent description
        self.description = self._generate_description()

    def _generate_description(self) -> str:
        """Generate agent description based on personality."""
        traits = []
        if self.personality["sociability"] > 0.7:
            traits.append("very social")
        elif self.personality["sociability"] < 0.4:
            traits.append("somewhat reserved")

        if self.personality["curiosity"] > 0.7:
            traits.append("curious")
        elif self.personality["curiosity"] < 0.4:
            traits.append("content")

        trait_str = ", ".join(traits) if traits else "balanced"
        return f"{self.name} is {trait_str} and lives in the town."

    async def observe(self) -> dict[str, Any]:
        """
        Observe the town state.

        Returns:
            Observation dictionary with nearby agents, conversations, etc.
        """
        # This will be populated by TownWorld
        return {
            "position": self.position,
            "nearby_agents": [],
            "available_conversations": [],
            "current_conversation": self.current_conversation,
        }

    async def decide(self, state: AgentState) -> dict[str, Any]:
        """
        Decide what to do next.

        Returns:
            Decision dictionary with action type and parameters
        """
        # Simple decision logic based on personality and state
        if self.current_conversation:
            # In conversation - decide to continue or leave
            if random.random() < 0.1:  # 10% chance to leave
                return {"action": "leave_conversation"}
            else:
                return {"action": "continue_conversation"}

        # Not in conversation - decide what to do
        if self.personality["sociability"] > 0.6 and random.random() < 0.3:
            # Social agent might want to start a conversation
            return {"action": "seek_conversation"}
        elif self.personality["curiosity"] > 0.6 and random.random() < 0.2:
            # Curious agent might want to explore
            return {"action": "explore"}
        else:
            # Default: wander
            return {"action": "wander"}

    async def act(self, decision: dict[str, Any]) -> dict[str, Any]:
        """
        Execute the decided action.

        Args:
            decision: Decision dictionary from decide()

        Returns:
            Action result dictionary
        """
        action = decision.get("action")

        if action == "wander":
            # Move to random nearby position
            self.position["x"] += random.uniform(-5, 5)
            self.position["y"] += random.uniform(-5, 5)
            # Keep in bounds
            self.position["x"] = max(0, min(100, self.position["x"]))
            self.position["y"] = max(0, min(100, self.position["y"]))
            return {"action": "wander", "new_position": self.position}

        elif action == "seek_conversation":
            return {"action": "seek_conversation", "ready": True}

        elif action == "explore":
            # Move towards a random point
            target = {
                "x": random.uniform(0, 100),
                "y": random.uniform(0, 100),
            }
            # Move partway towards target
            dx = (target["x"] - self.position["x"]) * 0.3
            dy = (target["y"] - self.position["y"]) * 0.3
            self.position["x"] += dx
            self.position["y"] += dy
            return {"action": "explore", "target": target, "new_position": self.position}

        elif action == "continue_conversation":
            return {"action": "continue_conversation", "ready": True}

        elif action == "leave_conversation":
            self.current_conversation = None
            return {"action": "leave_conversation"}

        else:
            return {"action": "idle"}

    async def reflect(self, result: dict[str, Any]) -> dict[str, Any]:
        """
        Reflect on the action result.

        Args:
            result: Result from act()

        Returns:
            Reflection dictionary
        """
        # Simple reflection - could be enhanced with LLM
        reflection = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": result.get("action"),
            "satisfaction": random.uniform(0.5, 1.0),  # Placeholder
        }

        # Add to journal
        self.state.journal.append(
            {
                "type": "Reflection",
                "timestamp": reflection["timestamp"],
                "content": reflection,
            }
        )

        return reflection

    def add_memory(self, memory: dict[str, Any]):
        """Add a conversation memory."""
        self.memories.append(
            {
                **memory,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
        # Keep last 20 memories
        if len(self.memories) > 20:
            self.memories.pop(0)

    def update_relationship(self, agent_id: str, delta: float):
        """Update relationship score with another agent."""
        if agent_id not in self.relationships:
            self.relationships[agent_id] = 0.5  # Neutral
        self.relationships[agent_id] = max(0, min(1, self.relationships[agent_id] + delta))

    def get_memory_summary(self) -> str:
        """Get a summary of recent memories for conversation context."""
        if not self.memories:
            return f"{self.name} has no memories yet."

        recent = self.memories[-5:]  # Last 5 memories
        summaries = [m.get("summary", m.get("content", "")) for m in recent]
        return f"{self.name} remembers: " + "; ".join(summaries[:3])
