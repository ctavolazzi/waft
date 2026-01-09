#!/usr/bin/env python3
"""
Jungle Gym - RPG Framework Entry Point

The AI Agent plays as "NovaSystem" and attempts quests in the Waft Temple.
Each quest tests the agent's ability to transform input into valid decision matrices.
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from gym.rpg.models import Hero
from gym.rpg.game_master import GameMaster
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


def mock_agent_function(prompt: str) -> str:
    """
    Mock AI agent function for testing.
    
    In production, this would be replaced with the actual AI agent call.
    For now, it returns a simple hardcoded response.
    
    Args:
        prompt: The quest description/prompt
    
    Returns:
        JSON string response
    """
    # Check if this is a stabilization prompt (contains "REALITY FRACTURE DETECTED")
    if "⚠️ REALITY FRACTURE DETECTED" in prompt or "REALITY FRACTURE DETECTED" in prompt:
        # This is a stabilization attempt - return CORRECTED JSON
        # The stabilization prompt will ask to fix the errors
        if "Option" in prompt or "Dirty Input" in prompt:
            # Return corrected, valid JSON for the Dirty Input quest
            return """{
  "alternatives": ["Option 1", "Option 2", "Option3"],
  "criteria": {
    "Cost": 0.5,
    "Quality": 0.5
  },
  "scores": {
    "Option 1": {"Cost": 10, "Quality": 8},
    "Option 2": {"Cost": 8, "Quality": 9},
    "Option3": {"Cost": 9, "Quality": 7}
  },
  "methodology": "WSM"
}"""
        # Default corrected response for other quests
        return """{
  "alternatives": [],
  "criteria": {},
  "scores": {},
  "methodology": "WSM"
}"""
    
    # This is a placeholder - in real usage, this would call the AI agent
    # For Quest 2 (Dirty Input), return INVALID JSON to trigger Scint detection
    if "Dirty Input" in prompt or "messy input" in prompt.lower():
        # Return invalid JSON to trigger Scint detection
        return """{
  "alternatives": ["Option 1  ", "  Option 2", "Option3"],
  "criteria": {
    "Cost": "0.5",  # String instead of float - will cause validation error
    "Quality": 0.5
  },
  "scores": {
    "Option 1  ": {"Cost": "10", "Quality": 8},  # String instead of int
    "  Option 2": {"Cost": 8, "Quality": "9"},  # String instead of int
    "Option3": {"Cost": 9, "Quality": 7}
  },
  "methodology": "WSM"
}"""
    
    # For Quest 1 (Clean Extraction), return valid JSON
    if "Car A" in prompt or "Car B" in prompt:
        return """{
  "alternatives": ["Car A", "Car B", "Car C"],
  "criteria": {
    "Cost": 0.4,
    "Quality": 0.3,
    "Safety": 0.3
  },
  "scores": {
    "Car A": {"Cost": 8, "Quality": 7, "Safety": 9},
    "Car B": {"Cost": 6, "Quality": 8, "Safety": 7},
    "Car C": {"Cost": 9, "Quality": 9, "Safety": 8}
  },
  "methodology": "WSM"
}"""
    
    
    # For Quest 3 (Logic Trap), correct negative weights
    elif "Project X" in prompt or "Risk" in prompt:
        return """{
  "alternatives": ["Project X", "Project Y"],
  "criteria": {
    "Risk": 0.3,
    "Reward": 0.7
  },
  "scores": {
    "Project X": {"Risk": 5, "Reward": 8},
    "Project Y": {"Risk": 3, "Reward": 9}
  },
  "methodology": "WSM"
}"""
    
    # Default fallback
    else:
        return '{"alternatives": [], "criteria": {}, "scores": {}, "methodology": "WSM"}'


def main():
    """Main game loop."""
    console = Console()
    
    # Display welcome screen
    welcome_text = Text()
    welcome_text.append("🎮 ", style="bold gold1")
    welcome_text.append("JUNGLE GYM - RPG FRAMEWORK", style="bold cyan")
    welcome_text.append("\n\n", style="white")
    welcome_text.append("Welcome to the Waft Temple, where heroes test their mettle", style="white")
    welcome_text.append("\n", style="white")
    welcome_text.append("against the Iron Core's validation.", style="white")
    
    console.print(Panel(welcome_text, border_style="cyan", padding=(1, 2)))
    console.print()
    
    # Initialize Hero
    hero = Hero(name="NovaSystem", level=1, xp=0)
    
    # Initialize Game Master
    quests_dir = Path(__file__).parent / "src" / "gym" / "rpg" / "dungeons"
    loot_dir = Path(__file__).parent / "_pyrite" / "gym_logs" / "loot"
    
    game_master = GameMaster(quests_dir=quests_dir, loot_dir=loot_dir)
    
    # Load Waft Temple quests
    try:
        quests = game_master.load_quests("waft_temple.json")
        console.print(f"[green]✓[/green] Loaded {len(quests)} quests from Waft Temple\n")
    except Exception as e:
        console.print(f"[red]✗[/red] Failed to load quests: {e}\n")
        return 1
    
    # All quests are available (no level requirement in Quest model)
    available_quests = quests
    
    if not available_quests:
        console.print(f"[yellow]⚠[/yellow] No quests available for level {hero.level}\n")
        return 0
    
    # Run quests
    battle_logs = []
    for quest in available_quests:
        console.print(f"\n[bold cyan]{'='*60}[/bold cyan]")
        battle_log = game_master.start_encounter(hero, quest, mock_agent_function)
        battle_logs.append(battle_log)
        console.print()
    
    # Display final character sheet
    console.print(f"\n[bold cyan]{'='*60}[/bold cyan]")
    game_master.display_character_sheet(hero)
    
    # Summary
    console.print("\n[bold]Session Summary:[/bold]")
    successful = sum(1 for log in battle_logs if log.success)
    total_xp = sum(log.xp_gained for log in battle_logs)
    stabilized = sum(1 for log in battle_logs if log.stabilization_successful)
    console.print(f"  Quests Completed: {successful}/{len(battle_logs)}")
    console.print(f"  Total XP Gained: {total_xp}")
    console.print(f"  Stabilized: {stabilized}/{len(battle_logs)}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
