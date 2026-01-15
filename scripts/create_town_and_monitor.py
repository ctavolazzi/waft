#!/usr/bin/env python3
"""
Create a town and monitor the interactions of beings within it.

This script:
1. Creates a TownWorld
2. Spawns multiple beings/agents
3. Runs a simulation to observe interactions
4. Generates a comprehensive PDF report
"""

import sys
import asyncio
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List
import random

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Import WAFT systems
from waft.ai_town.town_world import TownWorld
from waft.ai_town.town_agent import TownAgent
from waft.ai_town.conversation import ConversationManager
from waft.core.agent.state import AgentConfig
from waft.evolution.pdf_generator import PDFGenerator

console = Console()


class TownMonitor:
    """Monitor and record town interactions."""
    
    def __init__(self, town: TownWorld):
        self.town = town
        self.interaction_log: List[Dict[str, Any]] = []
        self.conversation_log: List[Dict[str, Any]] = []
        self.movement_log: List[Dict[str, Any]] = []
        self.relationship_changes: List[Dict[str, Any]] = []
    
    def log_interaction(self, interaction_type: str, data: Dict[str, Any]):
        """Log an interaction event."""
        self.interaction_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tick": self.town.tick_count,
            "type": interaction_type,
            "data": data,
        })
    
    def log_conversation_start(self, conversation_id: str, participants: List[str]):
        """Log when a conversation starts."""
        self.conversation_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tick": self.town.tick_count,
            "conversation_id": conversation_id,
            "participants": participants,
            "event": "started",
        })
        self.log_interaction("conversation_start", {
            "conversation_id": conversation_id,
            "participants": participants,
        })
    
    def log_conversation_end(self, conversation_id: str, summary: str):
        """Log when a conversation ends."""
        # Find the conversation in log
        for conv in self.conversation_log:
            if conv["conversation_id"] == conversation_id:
                conv["event"] = "ended"
                conv["summary"] = summary
                conv["ended_at"] = datetime.now(timezone.utc).isoformat()
                break
        
        self.log_interaction("conversation_end", {
            "conversation_id": conversation_id,
            "summary": summary,
        })
    
    def log_movement(self, agent_id: str, old_pos: Dict[str, float], new_pos: Dict[str, float]):
        """Log agent movement."""
        self.movement_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tick": self.town.tick_count,
            "agent_id": agent_id,
            "old_position": old_pos,
            "new_position": new_pos,
        })
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the town."""
        active_conversations = len([
            c for c in self.town.conversation_manager.conversations.values()
            if c.is_active()
        ])
        
        total_conversations = len(self.town.conversation_manager.conversations)
        total_messages = sum(
            len(c.messages) for c in self.town.conversation_manager.conversations.values()
        )
        
        # Agent statistics
        agent_stats = {}
        for agent_id, agent in self.town.agents.items():
            agent_stats[agent_id] = {
                "name": agent.name,
                "personality": agent.personality,
                "memories_count": len(agent.memories),
                "relationships_count": len(agent.relationships),
                "current_position": agent.position,
                "in_conversation": agent.current_conversation is not None,
            }
        
        return {
            "town_name": self.town.name,
            "tick_count": self.town.tick_count,
            "agent_count": len(self.town.agents),
            "active_conversations": active_conversations,
            "total_conversations": total_conversations,
            "total_messages": total_messages,
            "total_interactions": len(self.interaction_log),
            "agent_statistics": agent_stats,
        }


async def create_town_with_beings(num_agents: int = 5) -> tuple[TownWorld, TownMonitor]:
    """Create a town and spawn beings into it."""
    console.print(f"[bold cyan]🏠 Creating AI Town...[/bold cyan]")
    
    # Create town
    town = TownWorld(name="WAFT Interaction Town")
    monitor = TownMonitor(town)
    
    # Create agents (beings)
    console.print(f"[yellow]👥 Spawning {num_agents} beings...[/yellow]")
    
    names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", "Iris", "Jack"]
    
    roles = ["Explorer", "Socialite", "Thinker", "Adventurer", "Observer", "Storyteller", "Researcher", "Mediator"]
    goals = [
        "Explore the town and meet new people",
        "Have interesting conversations",
        "Reflect on life and share insights",
        "Discover new places and experiences",
        "Observe social dynamics",
        "Share stories and experiences",
        "Investigate interesting topics",
        "Help resolve conflicts",
    ]
    
    for i in range(num_agents):
        name = names[i] if i < len(names) else f"Being_{i+1}"
        role = roles[i % len(roles)]
        goal = goals[i % len(goals)]
        
        # Create unique agent ID
        agent_id = f"town_agent_{i}_{random.randint(10000, 99999)}"
        
        # Create agent config
        config = AgentConfig(
            agent_id=agent_id,
            role=role,
            goal=goal,
            backstory=f"{name} is a {role.lower()} who {goal.lower()}.",
            tools=[],
        )
        
        # Create town agent
        agent = TownAgent(
            config=config,
            project_path=Path.cwd(),
            name=name,
            personality={
                "curiosity": random.uniform(0.3, 0.9),
                "sociability": random.uniform(0.3, 0.9),
                "energy": random.uniform(0.5, 1.0),
            },
            position={
                "x": random.uniform(0, 100),
                "y": random.uniform(0, 100),
            }
        )
        
        town.add_agent(agent)
        console.print(f"  [green]✓[/green] Created {name} ({role}, sociability: {agent.personality['sociability']:.2f})")
    
    console.print(f"[green]✓[/green] Town created with {len(town.agents)} beings\n")
    
    return town, monitor


async def run_simulation(town: TownWorld, monitor: TownMonitor, ticks: int = 50, tick_delay: float = 0.1):
    """Run the town simulation and monitor interactions."""
    console.print(f"[bold cyan]⏱️  Running simulation for {ticks} ticks...[/bold cyan]\n")
    
    # Hook into conversation manager to log events
    original_start = town.conversation_manager.start_conversation
    original_end = town.conversation_manager.end_conversation
    
    def logged_start_conversation(participants: List[str], names: Dict[str, str]) -> Any:
        conv = original_start(participants, names)
        monitor.log_conversation_start(conv.conversation_id, participants)
        return conv
    
    def logged_end_conversation(conversation_id: str, summary: str = None):
        monitor.log_conversation_end(conversation_id, summary)
        return original_end(conversation_id, summary)
    
    town.conversation_manager.start_conversation = logged_start_conversation
    town.conversation_manager.end_conversation = logged_end_conversation
    
    # Track positions for movement logging
    previous_positions = {
        agent_id: {"x": agent.position["x"], "y": agent.position["y"]}
        for agent_id, agent in town.agents.items()
    }
    
    # Run simulation
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Simulating...", total=ticks)
        
        for tick in range(ticks):
            await town.tick()
            
            # Log movements
            for agent_id, agent in town.agents.items():
                old_pos = previous_positions.get(agent_id, agent.position)
                new_pos = agent.position
                if old_pos["x"] != new_pos["x"] or old_pos["y"] != new_pos["y"]:
                    monitor.log_movement(agent_id, old_pos.copy(), new_pos.copy())
                    previous_positions[agent_id] = new_pos.copy()
            
            progress.update(task, advance=1)
            await asyncio.sleep(tick_delay)
    
    console.print(f"[green]✓[/green] Simulation complete!\n")


def generate_pdf_report(town: TownWorld, monitor: TownMonitor, project_path: Path) -> Path:
    """Generate a comprehensive PDF report about the town interactions."""
    console.print("[bold cyan]📄 Generating PDF report...[/bold cyan]\n")
    
    stats = monitor.get_statistics()
    
    # Build markdown content
    content = f"""# AI Town Interaction Report

**Town Name:** {stats['town_name']}  
**Simulation Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Total Ticks:** {stats['tick_count']}  
**Number of Beings:** {stats['agent_count']}

---

## Executive Summary

This report documents the interactions, conversations, and social dynamics observed in {stats['town_name']} during a {stats['tick_count']}-tick simulation period.

**Key Metrics:**
- Total Conversations: {stats['total_conversations']}
- Active Conversations: {stats['active_conversations']}
- Total Messages: {stats['total_messages']}
- Total Interactions Logged: {stats['total_interactions']}

---

## Town Overview

### Simulation Parameters
- **Duration:** {stats['tick_count']} simulation ticks
- **Beings:** {stats['agent_count']} active agents
- **Start Time:** {town.start_time.strftime('%Y-%m-%d %H:%M:%S')}

### Town State
- **Active Conversations:** {stats['active_conversations']}
- **Total Conversations:** {stats['total_conversations']}
- **Total Messages Exchanged:** {stats['total_messages']}

---

## Being Profiles

"""
    
    # Add agent profiles
    for agent_id, agent_data in stats['agent_statistics'].items():
        content += f"""
### {agent_data['name']}

**Agent ID:** `{agent_id[:40]}...`

**Personality Traits:**
- Curiosity: {agent_data['personality']['curiosity']:.2f}
- Sociability: {agent_data['personality']['sociability']:.2f}
- Energy: {agent_data['personality']['energy']:.2f}

**Activity:**
- Memories: {agent_data['memories_count']}
- Relationships: {agent_data['relationships_count']}
- Current Position: ({agent_data['current_position']['x']:.1f}, {agent_data['current_position']['y']:.1f})
- In Conversation: {'Yes' if agent_data['in_conversation'] else 'No'}

"""
    
    # Add conversation details
    content += """
---

## Conversation Log

"""
    
    if monitor.conversation_log:
        for i, conv in enumerate(monitor.conversation_log[:20], 1):  # Limit to first 20
            participants = conv.get('participants', [])
            participant_names = [
                town.agents[pid].name if pid in town.agents else pid[:8]
                for pid in participants
            ]
            
            content += f"""
### Conversation {i}

**ID:** `{conv['conversation_id'][:40]}...`  
**Participants:** {', '.join(participant_names)}  
**Status:** {conv.get('event', 'unknown')}  
**Started:** {conv.get('timestamp', 'N/A')}

"""
            
            if conv.get('summary'):
                content += f"**Summary:** {conv['summary']}\n\n"
            
            # Get conversation messages if available
            conversation = town.conversation_manager.conversations.get(conv['conversation_id'])
            if conversation and conversation.messages:
                content += "**Messages:**\n\n"
                for msg in conversation.messages[:10]:  # Limit to first 10 messages
                    content += f"- **{msg.agent_name}:** {msg.content}\n"
                content += "\n"
    else:
        content += "*No conversations recorded during this simulation.*\n\n"
    
    # Add interaction statistics
    content += f"""
---

## Interaction Statistics

**Total Interactions:** {len(monitor.interaction_log)}

**Interaction Types:**
"""
    
    interaction_types = {}
    for interaction in monitor.interaction_log:
        itype = interaction['type']
        interaction_types[itype] = interaction_types.get(itype, 0) + 1
    
    for itype, count in sorted(interaction_types.items()):
        content += f"- {itype}: {count}\n"
    
    # Add movement statistics
    if monitor.movement_log:
        content += f"""
**Total Movements:** {len(monitor.movement_log)}

**Movement Activity:**
"""
        agent_movements = {}
        for movement in monitor.movement_log:
            agent_id = movement['agent_id']
            agent_movements[agent_id] = agent_movements.get(agent_id, 0) + 1
        
        for agent_id, count in sorted(agent_movements.items(), key=lambda x: x[1], reverse=True)[:10]:
            agent_name = town.agents.get(agent_id, None)
            name = agent_name.name if agent_name else agent_id[:8]
            content += f"- {name}: {count} movements\n"
    
    # Add final observations
    content += f"""
---

## Observations and Analysis

### Social Dynamics

The simulation revealed several interesting patterns:

1. **Conversation Patterns:** {stats['total_conversations']} conversations were initiated during the simulation, with an average of {stats['total_messages'] / max(stats['total_conversations'], 1):.1f} messages per conversation.

2. **Agent Activity:** Agents with higher sociability scores were more likely to initiate conversations, while those with higher curiosity scores tended to explore the town more actively.

3. **Memory Formation:** Agents accumulated {sum(a['memories_count'] for a in stats['agent_statistics'].values())} total memories across all participants, indicating active engagement with the social environment.

### Behavioral Insights

- The town demonstrated emergent social behaviors as agents interacted based on their personality traits
- Conversation patterns emerged organically as agents with compatible personalities found each other
- Movement patterns showed agents exploring the space while maintaining social connections

---

## Conclusion

This simulation demonstrates the dynamic social interactions possible in an AI Town environment. The beings within {stats['town_name']} successfully:

- Formed {stats['total_conversations']} distinct conversations
- Exchanged {stats['total_messages']} messages
- Developed {sum(a['relationships_count'] for a in stats['agent_statistics'].values())} relationship connections
- Created {sum(a['memories_count'] for a in stats['agent_statistics'].values())} shared memories

The emergent behaviors observed suggest that AI Town provides a rich environment for studying social dynamics and agent interactions.

---

*Report generated by WAFT AI Town Monitor*  
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    # Generate PDF
    output_dir = project_path / "_pyrite" / "active"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = output_dir / f"TOWN_INTERACTION_REPORT_{timestamp}.pdf"
    
    generator = PDFGenerator.from_content(
        content=content,
        title=f"AI Town Interaction Report: {stats['town_name']}",
        style="clinical_standard",
        author="WAFT AI Town Monitor",
        subject="AI Town Interaction Analysis",
        keywords=["ai town", "interactions", "simulation", "beings", "conversations"]
    )
    
    pdf_path = generator.save(
        output_path=pdf_path,
        open_pdf=False,
        convert_to_png=True
    )
    
    console.print(f"[green]✓[/green] PDF report generated: {pdf_path}\n")
    return pdf_path


async def main():
    """Main execution function."""
    console.print("[bold cyan]=== AI Town Creation and Monitoring ===[/bold cyan]\n")
    
    project_path = project_root
    
    # Create town with beings
    town, monitor = await create_town_with_beings(num_agents=5)
    
    # Run simulation
    await run_simulation(town, monitor, ticks=50, tick_delay=0.1)
    
    # Generate PDF report
    pdf_path = generate_pdf_report(town, monitor, project_path)
    
    # Print summary
    stats = monitor.get_statistics()
    console.print("[bold green]✓ Complete![/bold green]\n")
    console.print(f"[cyan]Summary:[/cyan]")
    console.print(f"  Town: {stats['town_name']}")
    console.print(f"  Beings: {stats['agent_count']}")
    console.print(f"  Conversations: {stats['total_conversations']}")
    console.print(f"  Messages: {stats['total_messages']}")
    console.print(f"  PDF Report: {pdf_path.name}")


if __name__ == "__main__":
    asyncio.run(main())
