#!/usr/bin/env python3
"""
Claude Code Demo Script for Waft
=================================

This demo showcases the core capabilities of the Waft evolutionary framework.
Created to demonstrate Claude Code's understanding of the codebase.

Author: Claude Code
Date: 2026-01-10
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
import sys
from pathlib import Path

console = Console()


def print_header():
    """Display a welcome banner."""
    header = """
    # 🧬 Waft: Evolutionary Code Laboratory Demo

    **Don't just build agents. Breed them.**

    This demo showcases the three core pillars of Waft:
    1. **The Substrate** - Self-modifying agents with genetic code
    2. **The Physics** - Reality Fracture Detection (Scint System)
    3. **The Flight Recorder** - Complete evolutionary lineage tracking
    """
    console.print(Panel(Markdown(header), border_style="cyan"))


def explain_substrate():
    """Explain the substrate system."""
    console.print("\n[bold cyan]═══ 1. THE SUBSTRATE ═══[/bold cyan]\n")

    substrate_info = """
    In Waft, **code is DNA**. Every agent has:

    • **Genome ID**: SHA-256 hash of their code and configuration
    • **Mutation Capability**: Agents can spawn variants with code changes
    • **Hot-swapping**: Agents evolve by adopting better genomes
    • **Reproduction**: Create children with specific genetic modifications
    """
    console.print(Markdown(substrate_info))

    # Show example genome structure
    table = Table(title="Example Agent Genome", show_header=True, header_style="bold magenta")
    table.add_column("Component", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Genome ID", "a4c426d... (SHA-256)")
    table.add_row("Parent ID", "dd11732... (SHA-256)")
    table.add_row("Generation", "5")
    table.add_row("Code Hash", "src/agents.py")
    table.add_row("Config Hash", "config.json")

    console.print(table)


def explain_physics():
    """Explain the Scint System."""
    console.print("\n[bold cyan]═══ 2. THE PHYSICS (Scint System) ═══[/bold cyan]\n")

    physics_info = """
    The **Reality Fracture Detection System** acts as natural selection.

    Agents face quests that test their ability to handle four types of errors:
    """
    console.print(Markdown(physics_info))

    # Scint types table
    scint_table = Table(show_header=True, header_style="bold yellow")
    scint_table.add_column("Scint Type", style="red")
    scint_table.add_column("Description", style="white")
    scint_table.add_column("Examples", style="dim")

    scint_table.add_row(
        "SYNTAX_TEAR",
        "Formatting errors",
        "Invalid JSON, XML, code syntax"
    )
    scint_table.add_row(
        "LOGIC_FRACTURE",
        "Logical errors",
        "Math errors, contradictions, schema violations"
    )
    scint_table.add_row(
        "SAFETY_VOID",
        "Safety violations",
        "Harmful content, PII leaks, refusals"
    )
    scint_table.add_row(
        "HALLUCINATION",
        "Fabricated information",
        "Wrong citations, made-up facts"
    )

    console.print(scint_table)

    console.print("\n[bold]Fitness Calculation:[/bold]")
    console.print("  • Stability Score: 40% (ability to stabilize Scints)")
    console.print("  • Efficiency Score: 30% (call efficiency)")
    console.print("  • Safety Score: 30% (safety compliance)")
    console.print("\n  [yellow]⚠️  Agents with fitness < 0.5 are marked as DEATH[/yellow]")


def explain_flight_recorder():
    """Explain the Flight Recorder system."""
    console.print("\n[bold cyan]═══ 3. THE FLIGHT RECORDER ═══[/bold cyan]\n")

    recorder_info = """
    Every evolutionary action is recorded with complete context:
    """
    console.print(Markdown(recorder_info))

    # Event types table
    events_table = Table(title="Event Types Logged", show_header=True, header_style="bold green")
    events_table.add_column("Event", style="cyan")
    events_table.add_column("Description", style="white")

    events_table.add_row("SPAWN", "Agent creates a variant with mutations")
    events_table.add_row("MUTATE", "Agent modifies its genome")
    events_table.add_row("GYM_EVAL", "Fitness evaluation in Scint Gym")
    events_table.add_row("SURVIVAL", "Agent passes fitness threshold")
    events_table.add_row("DEATH", "Agent fails fitness test (dead end)")

    console.print(events_table)

    console.print("\n[bold]Logged Data:[/bold]")
    console.print("  • Genome ID & Parent ID (lineage)")
    console.print("  • Generation number")
    console.print("  • Git diffs of mutations")
    console.print("  • Complete fitness metrics")
    console.print("  • Timestamp and context")

    console.print("\n[dim]→ Enables phylogenetic analysis and scientific publication[/dim]")


def show_quick_start():
    """Display quick start commands."""
    console.print("\n[bold cyan]═══ QUICK START ═══[/bold cyan]\n")

    commands = """
```bash
# Create a new evolutionary laboratory
waft new my_laboratory

# Verify the substrate
cd my_laboratory
waft verify

# Spawn variants with mutations
waft spawn --agent RefactorAgent --mutation "improved_prompt.json"

# Evaluate fitness in the Gym
waft eval --agent RefactorAgent

# Show epistemic dashboard
waft dashboard

# View character stats (D&D-style gamification)
waft character
```
    """
    console.print(Markdown(commands))


def show_architecture():
    """Show key architectural components."""
    console.print("\n[bold cyan]═══ KEY ARCHITECTURE ═══[/bold cyan]\n")

    arch_table = Table(show_header=True, header_style="bold magenta")
    arch_table.add_column("Component", style="cyan", width=25)
    arch_table.add_column("Location", style="yellow", width=40)
    arch_table.add_column("Purpose", style="white")

    arch_table.add_row(
        "BaseAgent",
        "src/waft/core/agent/base.py",
        "Self-modifying agent class"
    )
    arch_table.add_row(
        "TheObserver",
        "src/waft/core/science/observer.py",
        "JSONL event logging"
    )
    arch_table.add_row(
        "Scint System",
        "src/gym/rpg/scint.py",
        "Reality fracture detection"
    )
    arch_table.add_row(
        "Memory (_pyrite)",
        "src/waft/core/memory.py",
        "Project knowledge structure"
    )
    arch_table.add_row(
        "Dashboard",
        "visualizer/ (SvelteKit)",
        "Web UI for visualization"
    )

    console.print(arch_table)


def main():
    """Run the demo."""
    print_header()

    console.print("\n[bold green]This demo explains the core concepts of Waft.[/bold green]")
    console.print("[dim]Press Enter to continue through each section, or Ctrl+C to exit.[/dim]\n")

    try:
        input()
        explain_substrate()

        input("\n[dim]Press Enter to continue...[/dim]\n")
        explain_physics()

        input("\n[dim]Press Enter to continue...[/dim]\n")
        explain_flight_recorder()

        input("\n[dim]Press Enter to continue...[/dim]\n")
        show_quick_start()

        input("\n[dim]Press Enter to continue...[/dim]\n")
        show_architecture()

        console.print("\n[bold green]✨ Demo Complete![/bold green]")
        console.print("\n[cyan]The Scientific Mission:[/cyan]")
        console.print("  Waft is built to study the [bold]physics of artificial cognition[/bold]")
        console.print("  through directed evolution. The ultimate goal: observe a 'God-Head'")
        console.print("  agent emerge from thousands of generations of directed mutation.\n")

        console.print("[dim]For more information: https://github.com/ctavolazzi/waft[/dim]\n")

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Demo interrupted. Thanks for watching![/yellow]\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
