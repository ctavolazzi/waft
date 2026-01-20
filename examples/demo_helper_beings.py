"""
Demo: Helper Beings Autonomous System

This demo showcases the WAFT Being system:
1. Spawns a team of specialized helper beings
2. Creates an environment for them
3. Lets them run autonomously and make decisions
4. Shows their evolution and learning
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from waft.being import BeingSystem
from waft.core.being_decisions import BeingDecisionSystem

console = Console()


def demo_spawn_beings(being_system: BeingSystem):
    """Step 1: Spawn helper beings."""
    console.print(
        "\n[bold bright_blue]╔════════════════════════════════════════╗[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]║[/bold bright_blue]  [bold white]STEP 1: SPAWNING HELPER BEINGS[/bold white]  [bold bright_blue]║[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]╚════════════════════════════════════════╝[/bold bright_blue]\n"
    )

    helpers = [
        {
            "name": "Code Analyst",
            "personality_type": "analytical",
            "skills": {
                "code_analysis": 45.0,
                "reasoning": 40.0,
                "pattern_recognition": 35.0,
                "debugging": 30.0,
            },
        },
        {
            "name": "Documentation Specialist",
            "personality_type": "systematic",
            "skills": {
                "documentation": 50.0,
                "writing": 45.0,
                "organization": 40.0,
                "communication": 35.0,
            },
        },
        {
            "name": "Test Engineer",
            "personality_type": "systematic",
            "skills": {
                "testing": 45.0,
                "quality_assurance": 40.0,
                "automation": 35.0,
                "debugging": 30.0,
            },
        },
        {
            "name": "Research Assistant",
            "personality_type": "analytical",
            "skills": {
                "research": 50.0,
                "investigation": 45.0,
                "information_gathering": 40.0,
                "analysis": 35.0,
            },
        },
        {
            "name": "Creative Problem Solver",
            "personality_type": "creative",
            "skills": {
                "creativity": 45.0,
                "problem_solving": 40.0,
                "innovation": 35.0,
                "design": 30.0,
            },
        },
    ]

    spawned_beings = []

    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console
    ) as progress:
        for helper in helpers:
            task = progress.add_task(f"Spawning {helper['name']}...", total=None)

            being = being_system.spawn_being(
                reality_id="demo_reality", initial_skills=helper["skills"]
            )
            being.personality_type = helper["personality_type"]
            being_system._save_being(being)

            spawned_beings.append({"being": being, "helper_info": helper})

            progress.update(task, completed=True)
            console.print(f"  [green]✓[/green] {being.being_id[:30]}...")

    console.print(
        f"\n[bold green]✓ Successfully spawned {len(spawned_beings)} helper beings![/bold green]\n"
    )
    return spawned_beings


def demo_show_initial_state(beings_data):
    """Step 2: Show initial state."""
    console.print(
        "\n[bold bright_blue]╔════════════════════════════════════════╗[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]║[/bold bright_blue]  [bold white]STEP 2: INITIAL STATE[/bold white]  [bold bright_blue]║[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]╚════════════════════════════════════════╝[/bold bright_blue]\n"
    )

    table = Table(title="Helper Beings - Initial State")
    table.add_column("Name", style="cyan", width=25)
    table.add_column("Personality", style="magenta")
    table.add_column("Top Skill", style="green")
    table.add_column("Stamina", justify="right", style="yellow")
    table.add_column("Will to Live", justify="right", style="green")

    for item in beings_data:
        being = item["being"]
        helper = item["helper_info"]

        if being.skills:
            top_skill = max(being.skills.items(), key=lambda x: x[1])
            top_skill_display = f"{top_skill[0]}: {top_skill[1]:.1f}"
        else:
            top_skill_display = "None"

        table.add_row(
            helper["name"],
            being.personality_type,
            top_skill_display,
            f"{being.stamina:.1f}",
            f"{being.will_to_live:.1f}",
        )

    console.print(table)
    console.print()


async def demo_run_autonomous(being_system: BeingSystem, beings_data, num_cycles: int = 25):
    """Step 3: Run beings autonomously."""
    console.print(
        "\n[bold bright_blue]╔════════════════════════════════════════╗[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]║[/bold bright_blue]  [bold white]STEP 3: AUTONOMOUS OPERATION[/bold white]  [bold bright_blue]║[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]╚════════════════════════════════════════╝[/bold bright_blue]\n"
    )

    decision_system = BeingDecisionSystem()
    beings = [item["being"] for item in beings_data]

    console.print(f"[dim]Running {num_cycles} cycles...[/dim]\n")

    cycle_summaries = []

    for cycle in range(1, num_cycles + 1):
        cycle_data = {"cycle": cycle, "decisions": [], "sleeping": 0, "awake": 0}

        for being in beings:
            # Process sleep
            if being.is_sleeping:
                awake = being.process_sleep()
                if not awake:
                    cycle_data["sleeping"] += 1
                    continue
                else:
                    cycle_data["awake"] += 1

            # Regenerate stamina
            being.regenerate_stamina()

            # Update will_to_live
            will_change = being.calculate_will_to_live_change(
                {"decisions_made": 0, "pain": being.pain, "pleasure": being.pleasure}
            )
            being.will_to_live = max(0.0, min(100.0, being.will_to_live + will_change))

            # Make decision
            try:
                result = await decision_system.make_decision(being)

                decision_type = result.get("decision_type")
                experience = result.get("experience", {})

                # Calculate pleasure/pain
                pleasure, pain = being.calculate_pleasure_pain(
                    personality=being.personality, goals=being.goals, experience=experience
                )
                being.pleasure = pleasure
                being.pain = pain

                # Update will_to_live
                if experience.get("type") == "positive":
                    being.will_to_live = min(
                        100.0, being.will_to_live + experience.get("intensity", 0.0) * 2.0
                    )

                # Learn from experience
                if decision_type == "learn_skill" and not experience.get("stamina_depleted"):
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
                        "being_id": being.being_id[:15] + "...",
                        "decision": decision_type,
                        "quality": experience.get("quality", "unknown"),
                    }
                )

                being_system._save_being(being)

            except ValueError:
                if being.is_sleeping or being.decision_fatigue <= 0:
                    being.enter_sleep()
                    cycle_data["sleeping"] += 1
                else:
                    cycle_data["awake"] += 1

        cycle_summaries.append(cycle_data)

        # Show progress every 5 cycles
        if cycle % 5 == 0 or cycle == num_cycles:
            decisions_made = len(cycle_data["decisions"])
            console.print(
                f"[bold]Cycle {cycle:2d}/{num_cycles}[/bold] | "
                f"Decisions: {decisions_made:2d} | "
                f"Awake: {cycle_data['awake']} | "
                f"Sleeping: {cycle_data['sleeping']}"
            )

    console.print(f"\n[bold green]✓ Completed {num_cycles} cycles![/bold green]\n")
    return cycle_summaries


def demo_show_evolution(beings_data, initial_skills):
    """Step 4: Show evolution results."""
    console.print(
        "\n[bold bright_blue]╔════════════════════════════════════════╗[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]║[/bold bright_blue]  [bold white]STEP 4: EVOLUTION RESULTS[/bold white]  [bold bright_blue]║[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]╚════════════════════════════════════════╝[/bold bright_blue]\n"
    )

    table = Table(title="Evolution Summary")
    table.add_column("Name", style="cyan", width=25)
    table.add_column("Skill", style="green")
    table.add_column("Initial", justify="right", style="dim")
    table.add_column("Final", justify="right", style="green")
    table.add_column("Change", justify="right", style="yellow")
    table.add_column("Memories", justify="right", style="cyan")
    table.add_column("Stamina", justify="right", style="yellow")

    for item in beings_data:
        being = item["being"]
        helper = item["helper_info"]

        # Reload to get latest state
        being = being_system._load_being(being.being_id)

        # Find top skill and its change
        if being.skills:
            top_skill_name, top_skill_final = max(being.skills.items(), key=lambda x: x[1])
            top_skill_initial = initial_skills.get(being.being_id, {}).get(
                top_skill_name, top_skill_final
            )
            skill_change = top_skill_final - top_skill_initial
            change_display = f"+{skill_change:.1f}" if skill_change > 0 else f"{skill_change:.1f}"
        else:
            top_skill_name = "None"
            top_skill_initial = 0.0
            top_skill_final = 0.0
            change_display = "0.0"

        table.add_row(
            helper["name"],
            top_skill_name,
            f"{top_skill_initial:.1f}",
            f"{top_skill_final:.1f}",
            change_display,
            str(len(being.memories)),
            f"{being.stamina:.1f}",
        )

    console.print(table)
    console.print()


def demo_show_decisions(cycle_summaries):
    """Step 5: Show decision patterns."""
    console.print(
        "\n[bold bright_blue]╔════════════════════════════════════════╗[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]║[/bold bright_blue]  [bold white]STEP 5: DECISION PATTERNS[/bold white]  [bold bright_blue]║[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]╚════════════════════════════════════════╝[/bold bright_blue]\n"
    )

    # Count decision types
    decision_counts = {}
    quality_counts = {"excellent": 0, "good": 0, "fair": 0, "poor": 0}

    for cycle_data in cycle_summaries:
        for decision in cycle_data["decisions"]:
            decision_type = decision["decision"]
            quality = decision["quality"]

            decision_counts[decision_type] = decision_counts.get(decision_type, 0) + 1
            if quality in quality_counts:
                quality_counts[quality] += 1

    table = Table(title="Decision Statistics")
    table.add_column("Decision Type", style="cyan")
    table.add_column("Count", justify="right", style="green")

    for decision_type, count in sorted(decision_counts.items(), key=lambda x: x[1], reverse=True):
        table.add_row(decision_type, str(count))

    console.print(table)

    console.print("\n[bold]Quality Distribution:[/bold]")
    quality_table = Table(show_header=False)
    quality_table.add_column("Quality", style="cyan")
    quality_table.add_column("Count", justify="right", style="green")

    for quality, count in sorted(quality_counts.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            quality_table.add_row(quality, str(count))

    console.print(quality_table)
    console.print()


async def main():
    """Run the complete demo."""
    console.print(
        "\n[bold bright_blue]╔═══════════════════════════════════════════════════════════╗[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]║[/bold bright_blue]  [bold white]WAFT HELPER BEINGS DEMO - AUTONOMOUS EVOLUTION[/bold white]  [bold bright_blue]║[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]╚═══════════════════════════════════════════════════════════╝[/bold bright_blue]"
    )

    # Initialize systems
    project_path = Path(__file__).parent.parent
    being_system = BeingSystem(project_path=project_path)

    # Step 1: Spawn beings
    beings_data = demo_spawn_beings(being_system)

    # Store initial skills for comparison
    initial_skills = {}
    for item in beings_data:
        being = item["being"]
        initial_skills[being.being_id] = being.skills.copy()

    # Step 2: Show initial state
    demo_show_initial_state(beings_data)

    # Step 3: Run autonomously
    cycle_summaries = await demo_run_autonomous(being_system, beings_data, num_cycles=15)

    # Step 4: Show evolution
    demo_show_evolution(beings_data, initial_skills)

    # Step 5: Show decision patterns
    demo_show_decisions(cycle_summaries)

    # Final summary
    total_decisions = sum(len(cycle["decisions"]) for cycle in cycle_summaries)
    total_sleeping = sum(cycle["sleeping"] for cycle in cycle_summaries)

    console.print(
        Panel(
            f"[bold green]Demo Complete![/bold green]\n\n"
            f"• Beings spawned: {len(beings_data)}\n"
            f"• Cycles completed: {len(cycle_summaries)}\n"
            f"• Total decisions: {total_decisions}\n"
            f"• Sleep events: {total_sleeping}\n"
            f"• Average decisions/cycle: {total_decisions / len(cycle_summaries):.1f}",
            title="Summary",
            border_style="bright_blue",
        )
    )
    console.print()


if __name__ == "__main__":
    asyncio.run(main())
