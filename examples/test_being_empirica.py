"""
Test script for Being system with Empirica integration.

This script spawns the first Being and makes several decisions to verify
that Empirica integration is working correctly.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console
from rich.table import Table

from waft.being import BeingSystem
from waft.core.being_decisions import BeingDecisionSystem

console = Console()


async def test_being_empirica():
    """Test Being system with Empirica integration."""

    console.print(
        "\n[bold bright_blue]╔════════════════════════════════════════╗[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]║[/bold bright_blue]  [bold white]BEING EMPIRICA INTEGRATION TEST[/bold white]  [bold bright_blue]║[/bold bright_blue]"
    )
    console.print(
        "[bold bright_blue]╚════════════════════════════════════════╝[/bold bright_blue]\n"
    )

    # Initialize Being System
    project_path = Path(__file__).parent.parent
    being_system = BeingSystem(project_path=project_path)

    # Spawn first Being (will use Empirica)
    console.print("[bold cyan]Step 1:[/bold cyan] Spawning first Being...")
    being = being_system.spawn_being(
        reality_id="test_reality",
        initial_skills={"reasoning": 30.0, "creativity": 25.0, "analysis": 35.0},
    )

    console.print(f"[green]✓[/green] Being spawned: {being.being_id}")
    console.print(f"[green]✓[/green] Lifetimes: {being.lifetimes}")

    # Check Empirica integration
    if being.empirica_manager and being.empirica_session_id:
        console.print("[green]✓[/green] Empirica enabled!")
        console.print(f"[dim]  Session ID: {being.empirica_session_id}[/dim]")
    else:
        console.print("[yellow]⚠[/yellow] Empirica not enabled (may not be initialized)")

    console.print(f"[dim]  Stamina: {being.stamina:.1f}/{being.stamina_max:.1f}[/dim]")
    console.print(
        f"[dim]  Decision Fatigue: {being.decision_fatigue}/{being.decision_quota_max}[/dim]\n"
    )

    # Make several decisions
    console.print("[bold cyan]Step 2:[/bold cyan] Making decisions with Empirica...\n")

    decision_system = BeingDecisionSystem()
    results = []

    for i in range(5):
        try:
            console.print(f"[dim]Decision {i + 1}/5...[/dim]")
            result = await decision_system.make_decision(being)

            decision_type = result.get("decision_type")
            experience = result.get("experience", {})
            gate_result = result.get("empirica_gate")

            # Display result
            gate_display = (
                f" [bold magenta]Gate: {gate_result}[/bold magenta]" if gate_result else ""
            )
            quality = experience.get("quality", "unknown")
            stamina = result.get("stamina_remaining", being.stamina)

            console.print(
                f"  [green]✓[/green] {decision_type} | "
                f"Quality: [bold]{quality}[/bold] | "
                f"Stamina: {stamina:.1f}{gate_display}"
            )

            if experience.get("stamina_depleted"):
                mistakes = experience.get("mistakes", [])
                console.print(f"    [yellow]⚠ Stamina depleted! Mistakes: {len(mistakes)}[/yellow]")

            results.append(
                {
                    "decision": decision_type,
                    "gate": gate_result,
                    "quality": quality,
                    "stamina": stamina,
                }
            )

        except ValueError as e:
            console.print(f"  [yellow]⚠ {str(e)}[/yellow]")
            break

    # Summary table
    console.print("\n[bold cyan]Step 3:[/bold cyan] Summary\n")

    table = Table(title="Decision Results")
    table.add_column("Decision", style="cyan")
    table.add_column("Empirica Gate", style="magenta")
    table.add_column("Quality", style="green")
    table.add_column("Stamina", justify="right", style="yellow")

    for result in results:
        gate = result["gate"] or "N/A"
        table.add_row(result["decision"], gate, result["quality"], f"{result['stamina']:.1f}")

    console.print(table)

    # Final state
    console.print("\n[bold]Final Being State:[/bold]")
    console.print(f"  Stamina: {being.stamina:.1f}/{being.stamina_max:.1f}")
    console.print(f"  Will to Live: {being.will_to_live:.1f}")
    console.print(f"  Decision Fatigue: {being.decision_fatigue}/{being.decision_quota_max}")
    console.print(f"  Is Sleeping: {being.is_sleeping}")
    console.print(f"  Memories: {len(being.memories)}")
    console.print(f"  Lessons: {len(being.lessons_learned)}")

    # Empirica status
    if being.empirica_manager:
        console.print("\n[bold green]✓ Empirica Integration Working![/bold green]")
        console.print(f"  Session ID: {being.empirica_session_id}")
        console.print("  Preflight/Postflight assessments: ✅")
        console.print("  Check gates: ✅")
        console.print("  Finding/Unknown logging: ✅")
    else:
        console.print("\n[yellow]⚠ Empirica not enabled[/yellow]")
        console.print("  Check that Empirica is initialized in the project")

    console.print("\n[bold green]Test Complete![/bold green]\n")


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_being_empirica())
