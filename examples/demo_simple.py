"""
Simple Demo: Helper Beings in Action

Quick demo showing beings making decisions and evolving.
"""

from pathlib import Path
import sys
import asyncio

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.being import BeingSystem
from waft.core.being_decisions import BeingDecisionSystem
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


async def main():
    console.print("\n[bold bright_blue]╔════════════════════════════════════════╗[/bold bright_blue]")
    console.print("[bold bright_blue]║[/bold bright_blue]  [bold white]HELPER BEINGS DEMO[/bold white]  [bold bright_blue]║[/bold bright_blue]")
    console.print("[bold bright_blue]╚════════════════════════════════════════╝[/bold bright_blue]\n")
    
    project_path = Path(__file__).parent.parent
    being_system = BeingSystem(project_path=project_path)
    decision_system = BeingDecisionSystem()
    
    # Find existing beings
    beings_path = project_path / "_hidden" / ".truth" / "beings"
    beings = []
    
    if beings_path.exists():
        for being_file in list(beings_path.glob("*.json"))[:3]:  # Limit to 3 for demo
            try:
                being = being_system._load_being(being_file.stem)
                beings.append(being)
            except Exception:
                pass
    
    if not beings:
        console.print("[yellow]No beings found. Spawning one...[/yellow]")
        being = being_system.spawn_being(
            reality_id="demo_reality",
            initial_skills={"coding": 40.0, "analysis": 35.0}
        )
        beings.append(being)
    
    console.print(f"[green]✓[/green] Loaded {len(beings)} beings\n")
    
    # Show initial state
    table = Table(title="Initial State")
    table.add_column("Being ID", style="dim", max_width=30)
    table.add_column("Stamina", justify="right")
    table.add_column("Top Skill", style="green")
    
    initial_skills = {}
    for being in beings:
        if being.skills:
            top = max(being.skills.items(), key=lambda x: x[1])
            table.add_row(
                being.being_id[:28] + "...",
                f"{being.stamina:.1f}",
                f"{top[0]}: {top[1]:.1f}"
            )
            initial_skills[being.being_id] = being.skills.copy()
    
    console.print(table)
    console.print("\n[bold]Running 10 cycles...[/bold]\n")
    
    # Run cycles
    for cycle in range(1, 11):
        for being in beings:
            if being.is_sleeping:
                being.process_sleep()
                continue
            
            being.regenerate_stamina()
            
            try:
                result = await decision_system.make_decision(being)
                decision = result.get("decision_type")
                quality = result.get("experience", {}).get("quality", "unknown")
                
                if decision == "learn_skill" and not result.get("experience", {}).get("stamina_depleted"):
                    if being.skills:
                        skill = list(being.skills.keys())[0]
                        being.learn_skill(skill, "cognitive", 1.0)
                
                being_system._save_being(being)
                
                if cycle % 3 == 0:  # Show every 3rd cycle
                    console.print(f"  [dim]Cycle {cycle}: {decision} ({quality})[/dim]")
            except ValueError:
                if being.decision_fatigue <= 0:
                    being.enter_sleep()
    
    # Show final state
    console.print("\n[bold]Final State:[/bold]\n")
    
    final_table = Table(title="Evolution Results")
    final_table.add_column("Being ID", style="dim", max_width=30)
    final_table.add_column("Skill", style="green")
    final_table.add_column("Initial", justify="right", style="dim")
    final_table.add_column("Final", justify="right", style="green")
    final_table.add_column("Change", justify="right", style="yellow")
    
    for being in beings:
        being = being_system._load_being(being.being_id)  # Reload
        if being.skills:
            top_name, top_final = max(being.skills.items(), key=lambda x: x[1])
            top_initial = initial_skills.get(being.being_id, {}).get(top_name, top_final)
            change = top_final - top_initial
            
            final_table.add_row(
                being.being_id[:28] + "...",
                top_name,
                f"{top_initial:.1f}",
                f"{top_final:.1f}",
                f"+{change:.1f}" if change > 0 else f"{change:.1f}"
            )
    
    console.print(final_table)
    
    console.print(Panel(
        "[bold green]Demo Complete![/bold green]\n\n"
        "Beings made autonomous decisions, learned skills,\n"
        "and evolved through the cycles.",
        title="Summary",
        border_style="bright_blue"
    ))
    console.print()


if __name__ == "__main__":
    asyncio.run(main())
