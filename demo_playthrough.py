#!/usr/bin/env python3.12
"""Automated demo playthrough of the Eleventy CYOA scenario."""

import sys
import subprocess

# Install dependencies if needed
try:
    import yaml
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
except ImportError:
    print("Installing dependencies...")
    subprocess.run([
        sys.executable, "-m", "pip", "install",
        "--break-system-packages", "--quiet",
        "pyyaml", "rich"
    ], check=True)
    import yaml
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown

# Import directly
sys.path.insert(0, '/home/user/waft/src/waft/core/scenario_formats')
from eleventy_cyoa import ElevntyCYOAParser

console = Console()

def demo_playthrough(scenario, path_choices):
    """
    Automated playthrough following a specific path.

    Args:
        scenario: Loaded scenario
        path_choices: List of choice indices (0-based) to follow
    """
    current_node = scenario.get_start_node()
    visited = []

    console.print(Panel.fit(
        "[bold cyan]📖 Eleventy CYOA Demo Playthrough[/bold cyan]",
        subtitle="The Cavern Entrance"
    ))

    for step, choice_idx in enumerate(path_choices, 1):
        visited.append(current_node.id)

        # Display current node
        console.print(f"\n[bold yellow]═══ Step {step} ═══[/bold yellow]")
        console.print(Panel(f"[bold]{current_node.title}[/bold]", style="cyan"))
        console.print(Markdown(current_node.content))

        # Check if ending
        if current_node.is_ending:
            console.print("\n[bold green]═══ THE END ═══[/bold green]")
            break

        # Display choices
        console.print("\n[yellow]Choices:[/yellow]")
        for i, choice in enumerate(current_node.choices):
            marker = "→" if i == choice_idx else " "
            style = "bold green" if i == choice_idx else "dim"
            console.print(f"  [{style}]{marker} {i+1}. {choice.text}[/{style}]")

        # Follow the chosen path
        if choice_idx >= len(current_node.choices):
            console.print(f"[red]Invalid choice {choice_idx}[/red]")
            break

        selected = current_node.choices[choice_idx]
        console.print(f"\n[green]→ Choosing: {selected.text}[/green]")

        # Navigate
        next_node = scenario.get_node(selected.path)
        if next_node is None:
            console.print(f"[red]Error: Node '{selected.path}' not found![/red]")
            break

        current_node = next_node

    # Final node if it's an ending
    if current_node.is_ending:
        visited.append(current_node.id)
        console.print(f"\n[bold yellow]═══ Final Node ═══[/bold yellow]")
        console.print(Panel(f"[bold]{current_node.title}[/bold]", style="cyan"))
        console.print(Markdown(current_node.content))
        console.print("\n[bold green]═══ THE END ═══[/bold green]")

    # Stats
    console.print(f"\n[dim]Path taken: {' → '.join(visited)}[/dim]")
    console.print(f"[dim]Nodes visited: {len(visited)}/7[/dim]")

if __name__ == "__main__":
    scenario = ElevntyCYOAParser.load_scenario('/home/user/waft/examples/eleventy_cyoa_demo')

    console.print("\n[bold]Running 3 different playthroughs...[/bold]\n")

    # Playthrough 1: Cautious explorer
    console.print("[bold magenta]━━━ PLAYTHROUGH 1: The Cautious Explorer ━━━[/bold magenta]")
    demo_playthrough(scenario, [2])  # Turn back immediately

    console.print("\n\n")

    # Playthrough 2: Mushroom mystic
    console.print("[bold magenta]━━━ PLAYTHROUGH 2: The Mushroom Mystic ━━━[/bold magenta]")
    demo_playthrough(scenario, [0, 0])  # Dark passage → Mushroom grove

    console.print("\n\n")

    # Playthrough 3: Crystal keeper via river
    console.print("[bold magenta]━━━ PLAYTHROUGH 3: The Crystal Keeper ━━━[/bold magenta]")
    demo_playthrough(scenario, [1, 0])  # Underground river → Crystal chamber
