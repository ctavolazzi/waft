#!/usr/bin/env python3
"""
Integration test and example for SystemOrchestrator.

This script demonstrates how to:
1. Initialize the SystemOrchestrator
2. Access multiple WAFT systems through a unified interface
3. Perform cross-system operations (Being quests with karma rewards)
4. Check system status

Run this script from the project root:
    python examples/test_orchestrator_integration.py
"""

from pathlib import Path
import asyncio
import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.json import JSON

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.core.orchestrator import SystemOrchestrator


console = Console()


def print_section(title: str):
    """Print a section header."""
    console.print(f"\n[bold cyan]{'=' * 60}[/bold cyan]")
    console.print(f"[bold cyan]{title}[/bold cyan]")
    console.print(f"[bold cyan]{'=' * 60}[/bold cyan]\n")


def main():
    """Run the integration test."""
    console.print(Panel.fit(
        "[bold green]SystemOrchestrator Integration Test[/bold green]\n"
        "Demonstrating unified access to WAFT systems",
        border_style="green"
    ))

    # =========================================================================
    # Step 1: Initialize Orchestrator
    # =========================================================================
    print_section("Step 1: Initialize SystemOrchestrator")

    project_path = Path.cwd()
    console.print(f"Project path: [yellow]{project_path}[/yellow]")

    orchestrator = SystemOrchestrator(project_path=project_path)
    console.print("[green]✓[/green] SystemOrchestrator initialized")

    # =========================================================================
    # Step 2: List Available Systems
    # =========================================================================
    print_section("Step 2: List Available Systems")

    available_systems = orchestrator.list_available_systems()
    console.print("Available systems:")
    for system in available_systems:
        console.print(f"  • {system}")

    # =========================================================================
    # Step 3: Access Individual Systems
    # =========================================================================
    print_section("Step 3: Access Individual Systems")

    console.print("Accessing systems (lazy initialization)...")

    # Access SourceConsciousness
    source = orchestrator.get_source_consciousness()
    console.print("[green]✓[/green] SourceConsciousness initialized")

    # Access BeingSystem (shares SourceConsciousness)
    being_system = orchestrator.get_being_system()
    console.print("[green]✓[/green] BeingSystem initialized")

    # Access KarmaMerchant
    karma_merchant = orchestrator.get_karma_merchant()
    console.print("[green]✓[/green] KarmaMerchant initialized")

    # Access TavernKeeper
    tavern_keeper = orchestrator.get_tavern_keeper()
    console.print("[green]✓[/green] TavernKeeper initialized")

    # Access RealitySystem
    reality_system = orchestrator.get_reality_system()
    console.print("[green]✓[/green] RealitySystem initialized")

    # Access ScintDetector
    scint_detector = orchestrator.get_scint_detector()
    console.print("[green]✓[/green] RegexScintDetector initialized")

    # =========================================================================
    # Step 4: Create a Test Being
    # =========================================================================
    print_section("Step 4: Create Test Being")

    console.print("Creating test reality and being...")

    # Create a test reality
    reality_config = {
        "name": "Test Quest Reality",
        "description": "A reality for testing quest coordination",
        "type": "TESTING"
    }

    reality = reality_system.create_reality(
        reality_type="TESTING",
        configuration=reality_config,
        source_id="source_consciousness"
    )
    reality_id = reality.get("reality_id")
    console.print(f"[green]✓[/green] Reality created: [yellow]{reality_id}[/yellow]")

    # Spawn a being in the reality
    being_id = "test_hero_001"
    initial_skills = {
        "debugging": 0.7,
        "problem_solving": 0.8,
        "pattern_recognition": 0.6
    }

    being = being_system.spawn_being(
        reality_id=reality_id,
        parent_being_id=None,
        initial_skills=initial_skills
    )
    console.print(f"[green]✓[/green] Being spawned: [yellow]{being_id}[/yellow]")

    # Display being info
    console.print("\nBeing details:")
    console.print(f"  Reality: {being.reality_id}")
    console.print(f"  Soul ID: {being.soul_id}")
    console.print(f"  Skills: {list(initial_skills.keys())}")

    # =========================================================================
    # Step 5: Coordinate Being Quest (Cross-System Operation)
    # =========================================================================
    print_section("Step 5: Coordinate Being Quest")

    console.print("Sending being on a quest (demonstrates cross-system coordination)...")

    quest_data = {
        "quest_type": "debug",
        "difficulty": 3,
        "ability": "INT",
        "context": {
            "location": "Digital Forest",
            "objective": "Find and fix the memory leak"
        }
    }

    console.print(f"\nQuest parameters:")
    console.print(f"  Type: {quest_data['quest_type']}")
    console.print(f"  Difficulty: {quest_data['difficulty']}")
    console.print(f"  Ability: {quest_data['ability']}")

    # Execute quest coordination
    quest_result = orchestrator.coordinate_being_quest(
        being_id=being.being_id,
        quest_data=quest_data
    )

    # Display quest results
    console.print("\n[bold]Quest Results:[/bold]")

    result_table = Table(show_header=True, header_style="bold magenta")
    result_table.add_column("Aspect", style="cyan")
    result_table.add_column("Value", style="yellow")

    result_table.add_row("Success", "✓ Yes" if quest_result["success"] else "✗ No")
    result_table.add_row(
        "Roll",
        f"{quest_result['roll_result']['total']} "
        f"(d20: {quest_result['roll_result']['d20']}, "
        f"modifier: {quest_result['roll_result']['modifier']})"
    )
    result_table.add_row("DC", str(quest_result['roll_result']['dc']))
    result_table.add_row("Scints Detected", str(len(quest_result['scints_detected'])))
    result_table.add_row("Karma Impact", f"+{quest_result['karma_impact']}")

    console.print(result_table)

    # Display narrative
    console.print("\n[bold]Quest Narrative:[/bold]")
    console.print(Panel(
        quest_result['narrative'],
        border_style="blue",
        title="[bold]Story[/bold]"
    ))

    # Display rewards
    console.print("\n[bold]Rewards:[/bold]")
    rewards = quest_result['rewards']
    console.print(f"  • Insight: +{rewards['insight']}")
    console.print(f"  • Credits: +{rewards['credits']}")
    console.print(f"  • Integrity: {rewards['integrity_change']:+d}")

    # Display scints if any
    if quest_result['scints_detected']:
        console.print("\n[bold yellow]⚠ Reality Fractures Detected:[/bold yellow]")
        for scint in quest_result['scints_detected']:
            console.print(f"  • [{scint['type']}] {scint['description']} (severity: {scint['severity']:.2f})")

    # =========================================================================
    # Step 6: Test Scint Stabilization
    # =========================================================================
    print_section("Step 6: Test Scint Stabilization")

    if quest_result['scints_detected']:
        console.print("Attempting to stabilize detected reality fractures...")

        for scint in quest_result['scints_detected']:
            stabilization_result = orchestrator.coordinate_scint_stabilization(
                being_id=being.being_id,
                scint_data=scint
            )

            console.print(f"\n[bold]{scint['type']}[/bold]")
            console.print(f"  Ability used: {stabilization_result['ability_used']}")
            console.print(f"  Roll: {stabilization_result['roll_result']['total']}")
            console.print(
                f"  Result: {'✓ Stabilized' if stabilization_result['stabilized'] else '✗ Failed'}"
            )
            if stabilization_result['stabilized']:
                console.print(f"  Karma reward: +{stabilization_result['karma_reward']}")
    else:
        console.print("[green]No scints detected - reality remains stable![/green]")

    # =========================================================================
    # Step 7: Check System Status
    # =========================================================================
    print_section("Step 7: Check System Status")

    status = orchestrator.get_system_status()

    console.print("[bold]System Status:[/bold]")
    console.print(f"\nProject path: [yellow]{status['project_path']}[/yellow]")
    console.print(f"\nInitialized systems: [cyan]{len(status['initialized_systems'])}[/cyan]")

    for system_name in status['initialized_systems']:
        console.print(f"  • {system_name}")

    if status['system_details']:
        console.print("\n[bold]System Details:[/bold]")
        console.print(JSON(json.dumps(status['system_details'], indent=2)))

    # =========================================================================
    # Step 8: Access TavernKeeper Character
    # =========================================================================
    print_section("Step 8: Access TavernKeeper Character")

    character = tavern_keeper.get_character()

    console.print("[bold]D&D Character Stats:[/bold]")

    char_table = Table(show_header=True, header_style="bold magenta")
    char_table.add_column("Attribute", style="cyan")
    char_table.add_column("Value", style="yellow")

    char_table.add_row("Level", str(character.get("level", 1)))
    char_table.add_row("Insight (XP)", str(character.get("insight", 0)))
    char_table.add_row("Integrity (HP%)", f"{character.get('integrity', 100)}%")
    char_table.add_row("Credits", str(character.get("credits", 0)))

    console.print(char_table)

    console.print("\n[bold]Ability Scores:[/bold]")
    abilities = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    for ability in abilities:
        score = character.get(ability, 10)
        modifier = (score - 10) // 2
        console.print(f"  {ability}: {score} ({modifier:+d})")

    # =========================================================================
    # Step 9: Source Consciousness Stats
    # =========================================================================
    print_section("Step 9: Source Consciousness Stats")

    source_stats = source.get_source_stats()

    console.print("[bold]Source Consciousness:[/bold]")
    console.print(f"  Total capacity: {source_stats.get('total_capacity', 0)}")
    console.print(f"  Accumulated karma: {source_stats.get('accumulated_karma', 0)}")
    console.print(f"  Permutations: {len(source_stats.get('permutations', []))}")
    console.print(f"  Status: {source_stats.get('status', 'unknown')}")

    # =========================================================================
    # Conclusion
    # =========================================================================
    print_section("Conclusion")

    console.print("[bold green]✓ Integration test completed successfully![/bold green]\n")
    console.print("The SystemOrchestrator successfully:")
    console.print("  1. ✓ Initialized with lazy loading")
    console.print("  2. ✓ Provided access to all major WAFT systems")
    console.print("  3. ✓ Coordinated cross-system operations (Being + TavernKeeper + Karma)")
    console.print("  4. ✓ Demonstrated scint detection and stabilization")
    console.print("  5. ✓ Reported comprehensive system status")
    console.print("\n[bold cyan]The orchestrator is ready for use![/bold cyan]")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        import traceback
        console.print(traceback.format_exc())
        sys.exit(1)
