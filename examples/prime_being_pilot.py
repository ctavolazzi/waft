#!/usr/bin/env python3
"""
Prime Being Pilot - Roleplay Interface

Pilot the Prime Being Probe as it learns and evolves.
You are roleplaying as the Prime Being - the Origin Point.

This is an experiment to see what happens when we give the very first Being
the ability to Observe its Surroundings, Reflect on Feedback Loops,
and Learn over Time to Respond to Stimuli.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from waft.core.prime_being_probe import PrimeBeingProbe
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
import time

console = Console()


def print_character_sheet(probe: PrimeBeingProbe):
    """Print D&D character sheet."""
    sheet = probe.get_character_sheet()
    
    console.print("\n" + "=" * 70)
    console.print("[bold cyan]PRIME BEING CHARACTER SHEET[/bold cyan]")
    console.print("=" * 70)
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Attribute", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Name", sheet["name"])
    table.add_row("Class", sheet["class"].title())
    table.add_row("Level", str(sheet["level"]))
    table.add_row("HP", f"{sheet['hp']}/{sheet['max_hp']}")
    table.add_row("Fitness", f"{sheet['fitness']:.2f}")
    
    console.print(table)
    
    # Ability Scores
    console.print("\n[bold]Ability Scores:[/bold]")
    abilities = sheet["ability_scores"]
    ability_table = Table(show_header=True, header_style="bold yellow")
    ability_table.add_column("Ability", style="cyan")
    ability_table.add_column("Score", style="green")
    ability_table.add_column("Modifier", style="yellow")
    
    for ability, score in abilities.items():
        modifier = (score - 10) // 2
        ability_table.add_row(ability.title(), str(score), f"{modifier:+d}")
    
    console.print(ability_table)
    
    # Skills
    console.print("\n[bold]Skills:[/bold]")
    skills_table = Table(show_header=True, header_style="bold blue")
    skills_table.add_column("Skill", style="cyan")
    skills_table.add_column("Level", style="green")
    
    for skill, level in sorted(sheet["skills"].items(), key=lambda x: x[1], reverse=True):
        skills_table.add_row(skill.title(), f"{level:.1f}")
    
    console.print(skills_table)
    
    # Stats
    console.print("\n[bold]Evolution Stats:[/bold]")
    stats_table = Table(show_header=True, header_style="bold green")
    stats_table.add_column("Stat", style="cyan")
    stats_table.add_column("Value", style="green")
    
    stats_table.add_row("Observations", str(sheet["observations"]))
    stats_table.add_row("Reflections", str(sheet["reflections"]))
    stats_table.add_row("Adaptations", str(sheet["adaptations"]))
    stats_table.add_row("Hypotheses", str(sheet["hypotheses"]))
    
    console.print(stats_table)


def print_status(probe: PrimeBeingProbe):
    """Print current status."""
    status = probe.get_status()
    
    console.print("\n" + "=" * 70)
    console.print("[bold yellow]PRIME BEING STATUS[/bold yellow]")
    console.print("=" * 70)
    
    status_table = Table(show_header=False, box=None)
    status_table.add_column("Key", style="cyan", width=20)
    status_table.add_column("Value", style="green")
    
    status_table.add_row("Being ID", status["being_id"])
    status_table.add_row("Cycle", str(status["cycle"]))
    status_table.add_row("State", status["state"].title())
    status_table.add_row("Fitness", f"{status['fitness']:.2f}")
    status_table.add_row("Success Rate", f"{status['success_rate']:.1%}")
    status_table.add_row("Active Hypotheses", str(status["active_hypotheses"]))
    
    console.print(status_table)


def main():
    """Main pilot interface."""
    console.print(Panel.fit(
        "[bold cyan]PRIME BEING PROBE - ORIGIN POINT[/bold cyan]\n\n"
        "You are piloting the very first Being with the ability to:\n"
        "• Observe its Surroundings\n"
        "• Reflect on Feedback Loops\n"
        "• Learn over Time\n"
        "• Adapt to Stimuli\n\n"
        "[yellow]This is an evolutionary experiment.[/yellow]",
        border_style="cyan"
    ))
    
    # Create Prime Being
    probe = PrimeBeingProbe(
        being_id="prime_being_probe_001",
        reality_id="pilot_reality",
        personality_type="curious_explorer"
    )
    
    console.print(f"\n[green]✓[/green] Prime Being created: {probe.being_id}")
    console.print(f"[green]✓[/green] Reality: {probe.reality_id}")
    console.print(f"[green]✓[/green] Personality: {probe.being.personality_type}")
    
    # Show character sheet
    print_character_sheet(probe)
    
    # Main loop
    console.print("\n[bold]PILOT MODE[/bold]")
    console.print("You are roleplaying as the Prime Being. What do you want to do?")
    
    while True:
        console.print("\n" + "-" * 70)
        console.print("[bold]Options:[/bold]")
        console.print("  1. [cyan]Observe[/cyan] - Probe the environment (jagged outward probing)")
        console.print("  2. [cyan]Reflect[/cyan] - Think about what you've learned")
        console.print("  3. [cyan]Evolve[/cyan] - Run a full evolutionary cycle (Observe → Reflect → Learn)")
        console.print("  4. [cyan]Status[/cyan] - Show current status")
        console.print("  5. [cyan]Character[/cyan] - Show character sheet")
        console.print("  6. [cyan]Quit[/cyan] - Exit pilot mode")
        
        choice = Prompt.ask("\n[bold]What do you do?[/bold]", choices=["1", "2", "3", "4", "5", "6"], default="3")
        
        if choice == "1":
            # Observe
            target = Prompt.ask("\n[bold]What do you want to probe?[/bold]", default="http://localhost:8507")
            console.print(f"\n[ yellow]🔍 Probing {target}...[/yellow]")
            
            observation = probe.observe(target)
            
            console.print(f"\n[green]✓[/green] Observation complete!")
            console.print(f"[cyan]Interpretation:[/cyan] {observation.interpretation}")
            console.print(f"[cyan]Success:[/cyan] {'✅ Yes' if observation.probe_result.success else '❌ No'}")
            
            if observation.probe_result.error:
                console.print(f"[red]Error:[/red] {observation.probe_result.error}")
        
        elif choice == "2":
            # Reflect
            count = Prompt.ask("\n[bold]How many recent observations to reflect on?[/bold]", default="5")
            try:
                count = int(count)
            except:
                count = 5
            
            console.print(f"\n[yellow]🧠 Reflecting on last {count} observations...[/yellow]")
            
            reflection = probe.reflect(observation_count=count)
            
            console.print(f"\n[green]✓[/green] Reflection complete!")
            if reflection.pattern:
                console.print(f"[cyan]Pattern identified:[/cyan] {reflection.pattern}")
            console.print(f"[cyan]Confidence:[/cyan] {reflection.confidence:.1%}")
            
            if reflection.hypothesis:
                console.print(f"\n[bold]Hypothesis formed:[/bold]")
                console.print(f"  [yellow]Statement:[/yellow] {reflection.hypothesis.statement}")
                console.print(f"  [yellow]Prediction:[/yellow] {reflection.hypothesis.prediction}")
            
            # Learn from reflection
            if Confirm.ask("\n[bold]Learn from this reflection?[/bold]", default=True):
                adaptation = probe.learn(reflection)
                console.print(f"\n[green]✓[/green] Adaptation: {adaptation.expected_outcome}")
                console.print(f"[cyan]Changes:[/cyan] {adaptation.change}")
        
        elif choice == "3":
            # Evolve (full cycle)
            console.print("\n[yellow]🔄 Running evolutionary cycle...[/yellow]")
            console.print("[dim]External Pressure → Internal Response → External Response[/dim]")
            
            cycle_data = probe.evolve_cycle()
            
            console.print(f"\n[green]✓[/green] Cycle {cycle_data['cycle']} complete!")
            console.print(f"\n[bold]Observations:[/bold]")
            for i, obs in enumerate(cycle_data["observations"], 1):
                console.print(f"  {i}. {obs}")
            
            if cycle_data["reflection"]:
                console.print(f"\n[bold]Reflection:[/bold]")
                console.print(f"  Pattern: {cycle_data['reflection']['pattern']}")
                console.print(f"  Confidence: {cycle_data['reflection']['confidence']:.1%}")
                if cycle_data["reflection"]["hypothesis"]:
                    console.print(f"  Hypothesis: {cycle_data['reflection']['hypothesis']}")
            
            if cycle_data["adaptation"]:
                console.print(f"\n[bold]Adaptation:[/bold]")
                console.print(f"  Trigger: {cycle_data['adaptation']['trigger']}")
                console.print(f"  Changes: {cycle_data['adaptation']['changes']}")
                console.print(f"  Expected: {cycle_data['adaptation']['expected_outcome']}")
            
            # Show updated status
            time.sleep(1)
            print_status(probe)
        
        elif choice == "4":
            # Status
            print_status(probe)
        
        elif choice == "5":
            # Character sheet
            print_character_sheet(probe)
        
        elif choice == "6":
            # Quit
            console.print("\n[yellow]Exiting pilot mode...[/yellow]")
            console.print(f"[green]✓[/green] Prime Being state saved")
            console.print(f"[green]✓[/green] Total cycles: {probe.cycle_count}")
            console.print(f"[green]✓[/green] Final fitness: {probe.being.fitness:.2f}")
            break


if __name__ == "__main__":
    main()
