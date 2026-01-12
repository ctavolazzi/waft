"""
Lifecycle Test: Reincarnation Cycle Validation

Tests the complete Being lifecycle:
1. SPAWN - Create a new Being
2. LIVE - Give it experiences and skills
3. DIE - Archive the Being
4. REINCARNATE - Bring it back with soul continuity
5. VERIFY - Validate soul_id, lifetimes, and inheritance

This is a "Reality Fracture" test to earn Scint in the WAFT game.
"""

from pathlib import Path
import sys
import random
from typing import Dict, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.being import Being, BeingSystem, BeingState
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def print_stage(stage: str, description: str):
    """Print a lifecycle stage."""
    console.print(f"\n[bold cyan]{'='*60}[/bold cyan]")
    console.print(f"[bold yellow]STAGE: {stage}[/bold yellow]")
    console.print(f"[dim]{description}[/dim]")
    console.print(f"[bold cyan]{'='*60}[/bold cyan]\n")


def print_being_stats(being: Being, title: str):
    """Print Being statistics in a table."""
    table = Table(title=title, show_header=True)
    table.add_column("Attribute", style="cyan")
    table.add_column("Value", style="yellow")

    table.add_row("Being ID", being.being_id[:16] + "...")
    table.add_row("Soul ID", str(being.soul_id)[:16] + "..." if being.soul_id else "None")
    table.add_row("Lifetimes", str(being.lifetimes))
    table.add_row("State", being.state.value)
    table.add_row("Will to Live", f"{being.will_to_live:.2f}")
    table.add_row("Stamina", f"{being.stamina:.2f}/{being.stamina_max:.2f}")
    table.add_row("Skills", ", ".join([f"{k}:{v:.1f}" for k, v in being.skills.items()]) or "None")
    table.add_row("Memories", str(len(being.memories)))
    table.add_row("Lessons", str(len(being.lessons_learned)))

    console.print(table)


def simulate_life(being: Being, being_system: BeingSystem) -> Being:
    """
    Simulate a Being's life experiences.

    The Being will:
    - Learn some skills
    - Record memories
    - Learn lessons
    - Make decisions

    Returns the Being after living.
    """
    console.print("[bold]Simulating life experiences...[/bold]\n")

    # Learn some skills
    skills_to_learn = [
        ("wisdom", "cognitive", 10.0),
        ("charisma", "social", 8.0),
        ("survival", "practical", 12.0),
        ("magic", "mystical", 5.0)
    ]

    for skill_name, skill_type, level_increase in skills_to_learn:
        result = being.learn_skill(skill_name, skill_type, level_increase)
        console.print(f"  [green]✓[/green] Learned {skill_name}: {result['old_level']:.1f} → {result['new_level']:.1f}")

    # Record some memories
    memories = [
        ("Entered a tavern and met a mysterious stranger", "experience"),
        ("Helped defend the village from bandits", "achievement"),
        ("Lost a dear friend in battle", "trauma"),
        ("Discovered a hidden truth about my past", "revelation")
    ]

    console.print()
    for memory_content, memory_type in memories:
        being.record_memory(memory_content, memory_type)
        console.print(f"  [blue]◉[/blue] Memory: {memory_content[:50]}...")

    # Learn some lessons
    lessons = [
        ("Trust your instincts in combat", "success"),
        ("Always check for traps before entering", "failure"),
        ("Friendship is worth more than gold", "success")
    ]

    console.print()
    for lesson, outcome in lessons:
        being.learn_lesson(lesson, outcome)
        console.print(f"  [magenta]◆[/magenta] Lesson: {lesson}")

    # Make some decisions (depletes stamina and fatigue)
    console.print()
    console.print("[dim]Making life decisions...[/dim]")
    for i in range(5):
        try:
            decision = being.make_decision(
                decision_type=random.choice(["explore", "rest", "learn_skill", "pursue_goal"]),
                stamina_cost=random.uniform(3.0, 8.0)
            )
            quality = decision['experience']['quality']
            console.print(f"  [yellow]→[/yellow] Decision {i+1}: {decision['decision_type']} (quality: {quality})")
        except ValueError as e:
            console.print(f"  [red]✗[/red] {e}")
            break

    # Update state
    being.state = BeingState.LEARNING
    being_system._save_being(being)

    return being


def kill_being(being: Being, being_system: BeingSystem) -> Being:
    """
    Kill a Being by depleting will_to_live and archiving.

    Returns the dead Being.
    """
    console.print("[bold red]Ending life...[/bold red]\n")

    # Deplete will to live
    being.will_to_live = 0.0
    console.print(f"  [red]✗[/red] Will to live depleted: {being.will_to_live}")

    # Check death
    is_dead = being.check_death()
    console.print(f"  [red]✗[/red] Death check: {is_dead}")

    # Archive the Being (complete its existence)
    console.print("\n[dim]Archiving Being and extracting memories...[/dim]")
    completion = being_system.complete_being(
        being_id=being.being_id,
        final_fitness=random.uniform(50.0, 80.0)
    )

    console.print(f"  [green]✓[/green] Archived with fitness: {completion['total_capacity']:.2f}")
    console.print(f"  [green]✓[/green] Memory package extracted: {len(completion['memory_package']['memories'])} memories")

    # Reload to get ARCHIVED state
    dead_being = being_system._load_being(being.being_id)
    return dead_being


def main():
    """Run the full reincarnation cycle test."""
    console.print(Panel.fit(
        "[bold cyan]REINCARNATION CYCLE TEST[/bold cyan]\n"
        "[dim]Testing digital Samsara: Birth → Life → Death → Rebirth[/dim]",
        border_style="bright_blue"
    ))

    # Initialize Being System
    project_path = Path.cwd()
    being_system = BeingSystem(project_path=project_path)

    # ========== STAGE 1: SPAWN ==========
    print_stage("1. SPAWN", "Creating a new Being from Source Consciousness")

    reality_id = "tavern_reality_001"
    first_being = being_system.spawn_being(
        reality_id=reality_id,
        parent_being_id=None,
        initial_skills={"courage": 20.0, "curiosity": 30.0}
    )

    # Assign soul_id for karma tracking
    first_being.soul_id = f"soul_{first_being.being_id}"
    being_system._save_being(first_being)

    print_being_stats(first_being, "🌱 FIRST BIRTH")

    console.print(f"\n[green]✓[/green] Being spawned with lifetimes={first_being.lifetimes}")
    console.print(f"[green]✓[/green] Soul ID assigned: {first_being.soul_id[:24]}...")

    # ========== STAGE 2: LIVE ==========
    print_stage("2. LIVE", "Simulating life experiences in the Tavern")

    lived_being = simulate_life(first_being, being_system)

    print_being_stats(lived_being, "🧙 AFTER LIVING")

    # ========== STAGE 3: DIE ==========
    print_stage("3. DIE", "Ending life and archiving the Being")

    dead_being = kill_being(lived_being, being_system)

    print_being_stats(dead_being, "💀 DEATH")

    assert dead_being.state == BeingState.ARCHIVED, "Being should be ARCHIVED"
    console.print(f"\n[green]✓[/green] Being is ARCHIVED (dead)")

    # ========== STAGE 4: REINCARNATE ==========
    print_stage("4. REINCARNATE", "Bringing the Being back with soul continuity")

    # Attempt reincarnation
    console.print("[bold]Attempting reincarnation...[/bold]\n")

    reincarnated_being = being_system.reincarnate_being(
        dead_being_id=dead_being.being_id,
        reality_id=reality_id,
        use_karma=False,  # Simple reincarnation for this test
        purchase_order={"memory_continuity": 0.5}  # Carry over 50% of memories
    )

    print_being_stats(reincarnated_being, "🔄 REINCARNATED")

    # ========== STAGE 5: VERIFY ==========
    print_stage("5. VERIFY", "Validating soul continuity and lifecycle mechanics")

    verification_results = []

    # Check 1: Soul ID persistence
    soul_matches = (reincarnated_being.soul_id == dead_being.soul_id)
    verification_results.append(("Soul ID persistence", soul_matches,
                                f"Expected: {dead_being.soul_id[:24]}...\n         Got: {reincarnated_being.soul_id[:24] if reincarnated_being.soul_id else 'None'}..."))

    # Check 2: Lifetimes incremented
    lifetimes_incremented = (reincarnated_being.lifetimes == dead_being.lifetimes + 1)
    verification_results.append(("Lifetimes incremented", lifetimes_incremented,
                                f"Expected: {dead_being.lifetimes + 1}, Got: {reincarnated_being.lifetimes}"))

    # Check 3: Parent linkage
    parent_linked = (reincarnated_being.parent_being_id == dead_being.being_id)
    verification_results.append(("Parent being linkage", parent_linked,
                                f"Parent: {reincarnated_being.parent_being_id[:16] if reincarnated_being.parent_being_id else 'None'}..."))

    # Check 4: Skills inherited (with mutation)
    skills_inherited = len(reincarnated_being.skills) > 0
    verification_results.append(("Skills inherited", skills_inherited,
                                f"Inherited {len(reincarnated_being.skills)} skills with mutations"))

    # Check 5: Memory continuity (50%)
    expected_memories = int(len(dead_being.memories) * 0.5)
    memories_carried = len(reincarnated_being.memories) >= expected_memories * 0.8  # Allow 20% variance
    verification_results.append(("Memory continuity", memories_carried,
                                f"Carried over {len(reincarnated_being.memories)}/{len(dead_being.memories)} memories"))

    # Check 6: New being ID (different instance)
    new_instance = (reincarnated_being.being_id != dead_being.being_id)
    verification_results.append(("New instance created", new_instance,
                                f"New ID: {reincarnated_being.being_id[:16]}..."))

    # Check 7: State is SPAWNING (fresh start)
    fresh_state = (reincarnated_being.state == BeingState.SPAWNING)
    verification_results.append(("Fresh state", fresh_state,
                                f"State: {reincarnated_being.state.value}"))

    # Print verification results
    console.print("\n[bold]Verification Results:[/bold]\n")

    all_passed = True
    for check_name, passed, details in verification_results:
        if passed:
            console.print(f"  [green]✓[/green] {check_name}")
            console.print(f"    [dim]{details}[/dim]")
        else:
            console.print(f"  [red]✗[/red] {check_name}")
            console.print(f"    [dim]{details}[/dim]")
            all_passed = False

    # Final summary
    console.print(f"\n[bold cyan]{'='*60}[/bold cyan]")
    if all_passed:
        console.print("[bold green]🎉 ALL CHECKS PASSED! REINCARNATION CYCLE VALIDATED 🎉[/bold green]")
        console.print("\n[yellow]✨ SCINT EARNED: +50 (Reality Fracture stabilized)[/yellow]")
        console.print("[yellow]☯ KARMA EARNED: +10 (Test completed successfully)[/yellow]")
    else:
        console.print("[bold red]❌ SOME CHECKS FAILED[/bold red]")
    console.print(f"[bold cyan]{'='*60}[/bold cyan]\n")

    # Print reincarnation lineage
    console.print("\n[bold]Reincarnation Lineage:[/bold]")
    console.print(f"  Lifetime 1: {dead_being.being_id[:24]}... [red](ARCHIVED)[/red]")
    console.print(f"  Lifetime 2: {reincarnated_being.being_id[:24]}... [green](REINCARNATED)[/green]")
    console.print(f"\n  [cyan]Soul Thread: {reincarnated_being.soul_id[:32]}...[/cyan]")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
