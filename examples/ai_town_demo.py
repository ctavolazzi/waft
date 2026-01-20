#!/usr/bin/env python3
"""
AI Town Demo: Basic demonstration of AI Town using WAFT tools.

Creates a virtual town with AI agents that can move, chat, and socialize.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Import directly from modules to avoid __init__ issues
import importlib.util

# Load AgentConfig directly
spec = importlib.util.spec_from_file_location(
    "agent_state", src_path / "waft" / "core" / "agent" / "state.py"
)
agent_state = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agent_state)
AgentConfig = agent_state.AgentConfig

# Load TownAgent directly
spec = importlib.util.spec_from_file_location(
    "town_agent", src_path / "waft" / "ai_town" / "town_agent.py"
)
town_agent_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(town_agent_mod)
TownAgent = town_agent_mod.TownAgent

# Load TownWorld directly
spec = importlib.util.spec_from_file_location(
    "town_world", src_path / "waft" / "ai_town" / "town_world.py"
)
town_world_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(town_world_mod)
TownWorld = town_world_mod.TownWorld


async def main():
    """Run the AI Town demo."""
    print("🏠 Creating AI Town...")

    # Create the town
    town = TownWorld(name="WAFT AI Town")

    # Create some agents
    project_path = Path(__file__).parent.parent

    agents_data = [
        {"name": "Alice", "role": "Explorer", "goal": "Explore the town and meet new people"},
        {"name": "Bob", "role": "Socialite", "goal": "Have interesting conversations"},
        {"name": "Charlie", "role": "Thinker", "goal": "Reflect on life and share insights"},
        {"name": "Diana", "role": "Adventurer", "goal": "Discover new places and experiences"},
    ]

    print(f"👥 Creating {len(agents_data)} agents...")
    for agent_data in agents_data:
        config = AgentConfig(
            role=agent_data["role"],
            goal=agent_data["goal"],
            tools=[],
        )
        agent = TownAgent(
            config=config,
            project_path=project_path,
            name=agent_data["name"],
        )
        town.add_agent(agent)
        print(f"  ✅ Created {agent.name} ({agent.scientific_name})")

    print("\n🌍 Town State:")
    state = town.get_state_summary()
    print(f"  Agents: {state['agent_count']}")
    print(f"  Active Conversations: {state['active_conversations']}")

    # Run simulation
    print("\n⏱️  Running simulation for 50 ticks...")
    await town.run_simulation(ticks=50, tick_delay=0.05)

    # Final state
    print("\n📊 Final Town State:")
    final_state = town.get_state_summary()
    print(f"  Ticks: {final_state['tick_count']}")
    print(f"  Agents: {final_state['agent_count']}")
    print(f"  Active Conversations: {final_state['active_conversations']}")
    print(f"  Total Conversations: {final_state['total_conversations']}")

    # Show conversations
    print("\n💬 Conversations:")
    for conv_id, conversation in town.conversation_manager.conversations.items():
        print(f"\n  Conversation {conv_id[:8]}...")
        print(f"    Participants: {', '.join(conversation.participants)}")
        print(f"    Messages: {len(conversation.messages)}")
        print(f"    Duration: {conversation.get_duration():.1f}s")
        if conversation.summary:
            print(f"    Summary: {conversation.summary}")
        # Show first few messages
        for msg in conversation.messages[:3]:
            print(f"      {msg.agent_name}: {msg.content[:50]}...")

    # Show agent memories
    print("\n🧠 Agent Memories:")
    for agent_id, agent in town.agents.items():
        memories = town.memory.get_agent_memories(agent_id)
        print(f"  {agent.name}: {len(memories)} memories")
        if memories:
            print(f"    Latest: {memories[-1]['summary'][:60]}...")

    print("\n✅ Demo complete!")


if __name__ == "__main__":
    asyncio.run(main())
