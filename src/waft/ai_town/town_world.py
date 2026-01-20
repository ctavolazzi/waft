"""
TownWorld: The game engine for AI Town.

Manages agents, conversations, and the simulation loop.
"""

import asyncio
import random
from datetime import datetime
from typing import Any

from .conversation import ConversationManager
from .memory import TownMemory
from .town_agent import TownAgent


class TownWorld:
    """
    The virtual town where agents live, chat, and socialize.

    Manages:
    - Agents in the town
    - Conversations between agents
    - Memory system
    - Simulation loop
    """

    def __init__(self, name: str = "AI Town"):
        self.name = name
        self.agents: dict[str, TownAgent] = {}
        self.conversation_manager = ConversationManager()
        self.memory = TownMemory()
        self.tick_count = 0
        self.start_time = datetime.utcnow()

    def add_agent(self, agent: TownAgent):
        """Add an agent to the town."""
        self.agents[agent.state.agent_id] = agent
        agent.state.working_memory["town_id"] = self.name

    def remove_agent(self, agent_id: str):
        """Remove an agent from the town."""
        if agent_id in self.agents:
            # End any active conversations
            conversation = self.conversation_manager.get_agent_conversation(agent_id)
            if conversation:
                self.conversation_manager.end_conversation(conversation.conversation_id)
            del self.agents[agent_id]

    def get_nearby_agents(self, agent_id: str, distance: float = 20.0) -> list[str]:
        """Get agents within distance of an agent."""
        agent = self.agents.get(agent_id)
        if not agent:
            return []

        nearby = []
        for other_id, other_agent in self.agents.items():
            if other_id == agent_id:
                continue

            # Calculate distance
            dx = agent.position["x"] - other_agent.position["x"]
            dy = agent.position["y"] - other_agent.position["y"]
            dist = (dx**2 + dy**2) ** 0.5

            if dist <= distance:
                nearby.append(other_id)

        return nearby

    async def tick(self):
        """Run one simulation tick."""
        self.tick_count += 1

        # Update each agent
        for agent_id, agent in self.agents.items():
            # Update observation context
            nearby = self.get_nearby_agents(agent_id)
            conversation = self.conversation_manager.get_agent_conversation(agent_id)

            # Set conversation state
            agent.current_conversation = conversation.conversation_id if conversation else None

            # Run agent step
            context = {
                "nearby_agents": nearby,
                "conversation": conversation.conversation_id if conversation else None,
                "tick": self.tick_count,
            }

            result = await agent.step(context)

            # Handle conversation actions
            action = result.get("action")
            if action == "seek_conversation" and not conversation:
                # Try to start a conversation
                await self._try_start_conversation(agent_id, nearby)
            elif action == "continue_conversation" and conversation:
                # Continue conversation (could generate message)
                pass
            elif action == "leave_conversation" and conversation:
                # End conversation
                await self._end_conversation(conversation.conversation_id)

    async def _try_start_conversation(self, agent_id: str, nearby_agents: list[str]):
        """Try to start a conversation with a nearby agent."""
        if not nearby_agents:
            return

        # Find an available agent
        available = [
            aid
            for aid in nearby_agents
            if not self.conversation_manager.get_agent_conversation(aid)
        ]

        if not available:
            return

        # Pick random available agent
        partner_id = random.choice(available)

        # Start conversation
        agent = self.agents[agent_id]
        partner = self.agents[partner_id]

        conversation = self.conversation_manager.start_conversation(
            [agent_id, partner_id], {agent_id: agent.name, partner_id: partner.name}
        )

        # Add initial greeting messages
        greeting1 = f"Hello {partner.name}! How are you?"
        greeting2 = f"Hi {agent.name}! I'm doing well, thanks for asking."

        self.conversation_manager.add_message(
            conversation.conversation_id, agent_id, agent.name, greeting1
        )
        self.conversation_manager.add_message(
            conversation.conversation_id, partner_id, partner.name, greeting2
        )

        # Update agent states
        agent.current_conversation = conversation.conversation_id
        partner.current_conversation = conversation.conversation_id

    async def _end_conversation(self, conversation_id: str):
        """End a conversation and create memories."""
        conversation = self.conversation_manager.get_conversation(conversation_id)
        if not conversation:
            return

        # Generate summary
        summary = self.conversation_manager.get_conversation_summary(conversation_id)

        # Create memories for participants
        for agent_id in conversation.participants:
            agent = self.agents.get(agent_id)
            if agent:
                self.memory.remember_conversation(
                    agent_id,
                    conversation_id,
                    summary,
                    conversation.participants,
                )
                agent.add_memory(
                    {
                        "conversation_id": conversation_id,
                        "summary": summary,
                        "participants": conversation.participants,
                    }
                )

        # End conversation
        self.conversation_manager.end_conversation(conversation_id, summary)

    async def run_simulation(self, ticks: int = 100, tick_delay: float = 0.1):
        """
        Run the simulation for a number of ticks.

        Args:
            ticks: Number of ticks to run
            tick_delay: Delay between ticks in seconds
        """
        for _ in range(ticks):
            await self.tick()
            await asyncio.sleep(tick_delay)

    def get_state_summary(self) -> dict[str, Any]:
        """Get a summary of the town state."""
        return {
            "name": self.name,
            "tick_count": self.tick_count,
            "agent_count": len(self.agents),
            "active_conversations": len(
                [c for c in self.conversation_manager.conversations.values() if c.is_active()]
            ),
            "total_conversations": len(self.conversation_manager.conversations),
            "agents": [
                {
                    "id": agent.state.agent_id,
                    "name": agent.name,
                    "position": agent.position,
                    "in_conversation": agent.current_conversation is not None,
                }
                for agent in self.agents.values()
            ],
        }
