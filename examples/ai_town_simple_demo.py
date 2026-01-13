#!/usr/bin/env python3
"""
AI Town Simple Demo: Standalone demonstration of AI Town concept.

A basic implementation that doesn't require full WAFT imports.
"""

import asyncio
import random
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
from pathlib import Path
import uuid


@dataclass
class Agent:
    """A simple agent in the town."""
    agent_id: str
    name: str
    position: Dict[str, float]
    personality: Dict[str, float]
    current_conversation: Optional[str] = None
    memories: List[Dict[str, Any]] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.personality:
            self.personality = {
                "curiosity": random.uniform(0.3, 0.9),
                "sociability": random.uniform(0.3, 0.9),
                "energy": random.uniform(0.5, 1.0),
            }


@dataclass
class ConversationMessage:
    """A message in a conversation."""
    agent_id: str
    agent_name: str
    content: str
    timestamp: float


@dataclass
class Conversation:
    """A conversation between agents."""
    conversation_id: str
    participants: List[str]
    messages: List[ConversationMessage] = field(default_factory=list)
    started_at: float = field(default_factory=lambda: datetime.utcnow().timestamp())
    ended_at: Optional[float] = None
    
    def add_message(self, agent_id: str, agent_name: str, content: str):
        """Add a message to the conversation."""
        self.messages.append(ConversationMessage(
            agent_id=agent_id,
            agent_name=agent_name,
            content=content,
            timestamp=datetime.utcnow().timestamp(),
        ))
    
    def is_active(self) -> bool:
        """Check if conversation is still active."""
        return self.ended_at is None


class TownWorld:
    """The virtual town where agents live and chat."""
    
    def __init__(self, name: str = "AI Town"):
        self.name = name
        self.agents: Dict[str, Agent] = {}
        self.conversations: Dict[str, Conversation] = {}
        self.active_conversations: Dict[str, str] = {}  # agent_id -> conversation_id
        self.tick_count = 0
    
    def add_agent(self, agent: Agent):
        """Add an agent to the town."""
        self.agents[agent.agent_id] = agent
    
    def get_nearby_agents(self, agent_id: str, distance: float = 20.0) -> List[str]:
        """Get agents within distance."""
        agent = self.agents.get(agent_id)
        if not agent:
            return []
        
        nearby = []
        for other_id, other in self.agents.items():
            if other_id == agent_id:
                continue
            
            dx = agent.position["x"] - other.position["x"]
            dy = agent.position["y"] - other.position["y"]
            dist = (dx**2 + dy**2)**0.5
            
            if dist <= distance:
                nearby.append(other_id)
        
        return nearby
    
    async def tick(self):
        """Run one simulation tick."""
        self.tick_count += 1
        
        for agent_id, agent in self.agents.items():
            # Update conversation state
            agent.current_conversation = self.active_conversations.get(agent_id)
            
            # Simple decision logic
            if agent.current_conversation:
                # In conversation - might leave
                if random.random() < 0.05:  # 5% chance to leave
                    self._end_conversation(agent.current_conversation)
                    agent.current_conversation = None
            else:
                # Not in conversation - might start one
                if agent.personality["sociability"] > 0.6 and random.random() < 0.2:
                    nearby = self.get_nearby_agents(agent_id)
                    available = [
                        aid for aid in nearby
                        if aid not in self.active_conversations
                    ]
                    if available:
                        partner_id = random.choice(available)
                        self._start_conversation(agent_id, partner_id)
            
            # Move around
            if not agent.current_conversation:
                agent.position["x"] += random.uniform(-2, 2)
                agent.position["y"] += random.uniform(-2, 2)
                agent.position["x"] = max(0, min(100, agent.position["x"]))
                agent.position["y"] = max(0, min(100, agent.position["y"]))
    
    def _start_conversation(self, agent1_id: str, agent2_id: str):
        """Start a conversation between two agents."""
        conversation_id = str(uuid.uuid4())
        conversation = Conversation(
            conversation_id=conversation_id,
            participants=[agent1_id, agent2_id],
        )
        self.conversations[conversation_id] = conversation
        self.active_conversations[agent1_id] = conversation_id
        self.active_conversations[agent2_id] = conversation_id
        
        agent1 = self.agents[agent1_id]
        agent2 = self.agents[agent2_id]
        
        # Add greeting messages
        conversation.add_message(agent1_id, agent1.name, f"Hello {agent2.name}! How are you?")
        conversation.add_message(agent2_id, agent2.name, f"Hi {agent1.name}! I'm doing well, thanks!")
        
        agent1.current_conversation = conversation_id
        agent2.current_conversation = conversation_id
    
    def _end_conversation(self, conversation_id: str):
        """End a conversation."""
        conversation = self.conversations.get(conversation_id)
        if conversation:
            conversation.ended_at = datetime.utcnow().timestamp()
            for agent_id in conversation.participants:
                if agent_id in self.active_conversations:
                    del self.active_conversations[agent_id]
                agent = self.agents.get(agent_id)
                if agent:
                    agent.current_conversation = None
                    # Add memory
                    summary = f"Conversation with {len(conversation.messages)} messages"
                    agent.memories.append({
                        "conversation_id": conversation_id,
                        "summary": summary,
                        "timestamp": datetime.utcnow().isoformat(),
                    })
    
    async def run_simulation(self, ticks: int = 100, tick_delay: float = 0.05):
        """Run the simulation."""
        for _ in range(ticks):
            await self.tick()
            await asyncio.sleep(tick_delay)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get town summary."""
        return {
            "name": self.name,
            "tick_count": self.tick_count,
            "agent_count": len(self.agents),
            "active_conversations": len([
                c for c in self.conversations.values() if c.is_active()
            ]),
            "total_conversations": len(self.conversations),
        }


async def main():
    """Run the demo."""
    print("🏠 Creating AI Town...")
    
    town = TownWorld(name="WAFT AI Town")
    
    # Create agents
    names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
    print(f"👥 Creating {len(names)} agents...")
    
    for name in names:
        agent = Agent(
            agent_id=str(uuid.uuid4()),
            name=name,
            position={"x": random.uniform(0, 100), "y": random.uniform(0, 100)},
            personality={},
        )
        town.add_agent(agent)
        print(f"  ✅ Created {agent.name} (sociability: {agent.personality['sociability']:.2f})")
    
    print(f"\n🌍 Initial State:")
    state = town.get_summary()
    print(f"  Agents: {state['agent_count']}")
    print(f"  Active Conversations: {state['active_conversations']}")
    
    # Run simulation
    print(f"\n⏱️  Running simulation for 50 ticks...")
    await town.run_simulation(ticks=50, tick_delay=0.05)
    
    # Final state
    print(f"\n📊 Final State:")
    final_state = town.get_summary()
    print(f"  Ticks: {final_state['tick_count']}")
    print(f"  Agents: {final_state['agent_count']}")
    print(f"  Active Conversations: {final_state['active_conversations']}")
    print(f"  Total Conversations: {final_state['total_conversations']}")
    
    # Show conversations
    print(f"\n💬 Conversations:")
    for conv_id, conversation in list(town.conversations.items())[:5]:
        print(f"\n  Conversation {conv_id[:8]}...")
        print(f"    Participants: {', '.join([town.agents[p].name for p in conversation.participants])}")
        print(f"    Messages: {len(conversation.messages)}")
        if conversation.messages:
            for msg in conversation.messages[:2]:
                print(f"      {msg.agent_name}: {msg.content}")
    
    # Show agent memories
    print(f"\n🧠 Agent Memories:")
    for agent_id, agent in list(town.agents.items())[:3]:
        print(f"  {agent.name}: {len(agent.memories)} memories")
        if agent.memories:
            print(f"    Latest: {agent.memories[-1]['summary']}")
    
    print(f"\n✅ Demo complete!")


if __name__ == "__main__":
    asyncio.run(main())
