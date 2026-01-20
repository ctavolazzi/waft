"""
Run helper beings autonomously in an environment.

Creates a reality, loads all helper beings, and lets them make decisions
autonomously through multiple cycles.
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console
from rich.table import Table

from waft.being import BeingSystem
from waft.core.being_decisions import BeingDecisionSystem
from waft.reality import RealitySystem, RealityType

console = Console()


async def run_autonomous_environment(num_cycles: int = 20):
    """Run beings autonomously through cycles."""

    console.print(
        "\n[bold bright_blue]╔════════════════════════════════════════╗[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]║[/bold bright_blue]  [bold white]AUTONOMOUS BEING ENVIRONMENT[/bold white]  [bold bright_blue]║[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]╚════════════════════════════════════════╝[/bold bright_blue]\n"
    )

    # Initialize systems
    project_path = Path(__file__).parent.parent
    being_system = BeingSystem(project_path=project_path)
    reality_system = RealitySystem(project_path=project_path)
    decision_system = BeingDecisionSystem()

    # Find all beings in helper_reality
    reality_id = "helper_reality"
    beings_path = project_path / "_hidden" / ".truth" / "beings"
    beings = []

    if beings_path.exists():
        for being_file in beings_path.glob("*.json"):
            try:
                being = being_system._load_being(being_file.stem)
                if being.reality_id == reality_id:
                    beings.append(being)
            except Exception as e:
                console.print(f"[yellow]⚠[/yellow] Could not load {being_file.stem}: {e}")

    # Create reality if it doesn't exist (for tracking purposes)
    try:
        reality = reality_system._load_reality(reality_id)
        if not reality.is_active:
            reality.is_active = True
            reality.started_at = datetime.now().isoformat()
            reality_system._save_reality(reality)
    except FileNotFoundError:
        # Create reality with specific ID
        from waft.reality import Reality

        reality = Reality(
            reality_id=reality_id,
            reality_type=RealityType.LEARNING,
            configuration={
                "description": "Environment for helper beings to learn and evolve",
                "learning_rate": 1.2,
                "skill_cap": 100.0,
            },
        )
        reality.is_active = True
        reality.started_at = datetime.now().isoformat()
        reality_system._save_reality(reality)
        console.print(f"[green]✓[/green] Created reality: {reality_id}")

    if not beings:
        console.print("[yellow]⚠[/yellow] No beings found in helper_reality")
        console.print("[dim]Run spawn_helper_beings.py first to create beings[/dim]\n")
        return

    console.print(f"[green]✓[/green] Loaded {len(beings)} beings\n")

    # Display initial state
    console.print("[bold cyan]Initial State[/bold cyan]\n")
    initial_table = Table(title="Beings Ready to Run")
    initial_table.add_column("Being ID", style="dim", max_width=30)
    initial_table.add_column("Personality", style="magenta")
    initial_table.add_column("Stamina", justify="right", style="yellow")
    initial_table.add_column("Fatigue", justify="right", style="cyan")
    initial_table.add_column("Will to Live", justify="right", style="green")

    for being in beings:
        initial_table.add_row(
            being.being_id[:28] + "..." if len(being.being_id) > 28 else being.being_id,
            being.personality_type,
            f"{being.stamina:.1f}/{being.stamina_max:.1f}",
            f"{being.decision_fatigue}/{being.decision_quota_max}",
            f"{being.will_to_live:.1f}",
        )

    console.print(initial_table)
    console.print("\n[bold cyan]Starting autonomous cycles...[/bold cyan]\n")

    # Run cycles
    cycle_results = []

    for cycle in range(1, num_cycles + 1):
        cycle_data = {"cycle": cycle, "decisions": [], "sleeping": [], "awake": []}

        for being in beings:
            # Process sleep if needed
            if being.is_sleeping:
                awake = being.process_sleep()
                if not awake:
                    cycle_data["sleeping"].append(being.being_id)
                    continue
                else:
                    cycle_data["awake"].append(being.being_id)

            # Regenerate stamina
            being.regenerate_stamina()

            # Update will_to_live based on cycle
            will_change = being.calculate_will_to_live_change(
                {
                    "decisions_made": 0,  # Will be updated after decision
                    "pain": being.pain,
                    "pleasure": being.pleasure,
                }
            )
            being.will_to_live = max(0.0, min(100.0, being.will_to_live + will_change))

            # Try to make a decision
            try:
                result = await decision_system.make_decision(being)

                decision_type = result.get("decision_type")
                experience = result.get("experience", {})

                # Calculate pleasure/pain from experience
                pleasure, pain = being.calculate_pleasure_pain(
                    personality=being.personality, goals=being.goals, experience=experience
                )
                being.pleasure = pleasure
                being.pain = pain

                # Update will_to_live based on experience
                if experience.get("type") == "positive":
                    being.will_to_live = min(
                        100.0, being.will_to_live + experience.get("intensity", 0.0) * 2.0
                    )

                # Learn from experience
                if decision_type == "learn_skill" and not experience.get("stamina_depleted"):
                    # Improve a random skill
                    if being.skills:
                        skill_name = list(being.skills.keys())[0]
                        being.learn_skill(skill_name, "cognitive", level_increase=1.0)

                # Record memory
                if decision_type == "record_memory":
                    being.record_memory(
                        f"Cycle {cycle}: {experience.get('description', decision_type)}",
                        "experience",
                    )

                cycle_data["decisions"].append(
                    {
                        "being_id": being.being_id[:20] + "..."
                        if len(being.being_id) > 20
                        else being.being_id,
                        "decision": decision_type,
                        "quality": experience.get("quality", "unknown"),
                        "stamina": f"{being.stamina:.1f}",
                    }
                )

                # Save being state
                being_system._save_being(being)

            except ValueError as e:
                # Being can't make decisions (sleeping, exhausted, etc.)
                if "sleeping" in str(e).lower():
                    cycle_data["sleeping"].append(being.being_id)
                elif "fatigue" in str(e).lower():
                    being.enter_sleep()
                    cycle_data["sleeping"].append(being.being_id)
                else:
                    cycle_data["awake"].append(being.being_id)

        cycle_results.append(cycle_data)

        # Display cycle summary
        if cycle % 5 == 0 or cycle == num_cycles:
            console.print(f"[bold]Cycle {cycle}/{num_cycles}[/bold]")
            console.print(f"  Decisions made: {len(cycle_data['decisions'])}")
            console.print(
                f"  Awake: {len(cycle_data['awake'])}, Sleeping: {len(cycle_data['sleeping'])}"
            )

            # Show sample decisions
            if cycle_data["decisions"]:
                sample = cycle_data["decisions"][:3]
                for decision in sample:
                    console.print(
                        f"    [dim]{decision['being_id']}: {decision['decision']} ({decision['quality']})[/dim]"
                    )
            console.print()

    # Final summary
    console.print("\n[bold cyan]Final Summary[/bold cyan]\n")

    final_table = Table(title="Final Being States")
    final_table.add_column("Being ID", style="dim", max_width=30)
    final_table.add_column("Personality", style="magenta")
    final_table.add_column("Stamina", justify="right", style="yellow")
    final_table.add_column("Will to Live", justify="right", style="green")
    final_table.add_column("Memories", justify="right", style="cyan")
    final_table.add_column("Top Skill", style="green")

    for being in beings:
        # Reload to get latest state
        being = being_system._load_being(being.being_id)

        top_skill = "None"
        if being.skills:
            top_skill_name, top_skill_level = max(being.skills.items(), key=lambda x: x[1])
            top_skill = f"{top_skill_name}: {top_skill_level:.1f}"

        final_table.add_row(
            being.being_id[:28] + "..." if len(being.being_id) > 28 else being.being_id,
            being.personality_type,
            f"{being.stamina:.1f}/{being.stamina_max:.1f}",
            f"{being.will_to_live:.1f}",
            str(len(being.memories)),
            top_skill,
        )

    console.print(final_table)

    # Statistics
    total_decisions = sum(len(cycle["decisions"]) for cycle in cycle_results)
    total_sleeping = sum(len(cycle["sleeping"]) for cycle in cycle_results)

    console.print("\n[bold]Statistics:[/bold]")
    console.print(f"  Total cycles: {num_cycles}")
    console.print(f"  Total decisions made: {total_decisions}")
    console.print(f"  Average decisions per cycle: {total_decisions / num_cycles:.1f}")
    console.print(f"  Total sleep events: {total_sleeping}")

    console.print("\n[bold green]✓ Autonomous run complete![/bold green]\n")

    return {
        "beings": beings,
        "cycles": cycle_results,
        "statistics": {
            "total_cycles": num_cycles,
            "total_decisions": total_decisions,
            "total_sleeping": total_sleeping,
        },
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run beings autonomously")
    parser.add_argument(
        "--cycles", type=int, default=20, help="Number of cycles to run (default: 20)"
    )

    args = parser.parse_args()

    asyncio.run(run_autonomous_environment(num_cycles=args.cycles))
