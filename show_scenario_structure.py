#!/usr/bin/env python3.12
"""Show the complete structure of a scenario."""

import sys
import subprocess

# Install dependencies if needed
try:
    import yaml
    from rich.console import Console
    from rich.tree import Tree
except ImportError:
    print("Installing dependencies...")
    subprocess.run([
        sys.executable, "-m", "pip", "install",
        "--break-system-packages", "--quiet",
        "pyyaml", "rich"
    ], check=True)
    import yaml
    from rich.console import Console
    from rich.tree import Tree

# Import directly
sys.path.insert(0, '/home/user/waft/src/waft/core/scenario_formats')
from eleventy_cyoa import ElevntyCYOAParser

console = Console()

def build_tree(scenario, node_id, tree, visited=None):
    """Recursively build a tree structure."""
    if visited is None:
        visited = set()

    if node_id in visited:
        return

    visited.add(node_id)
    node = scenario.get_node(node_id)

    if node.is_ending:
        return

    for choice in node.choices:
        child_node = scenario.get_node(choice.path)
        if child_node:
            style = "green" if child_node.is_ending else "cyan"
            ending_marker = " ⚡" if child_node.is_ending else ""
            branch = tree.add(f"[{style}]{child_node.title}{ending_marker}[/{style}]")
            branch.label = f"{branch.label} [dim]({choice.text})[/dim]"
            build_tree(scenario, choice.path, branch, visited)

if __name__ == "__main__":
    scenario = ElevntyCYOAParser.load_scenario('/home/user/waft/examples/eleventy_cyoa_demo')

    console.print("\n[bold cyan]📖 Eleventy CYOA Scenario Structure[/bold cyan]\n")

    # Basic info
    console.print(f"[yellow]Total nodes:[/yellow] {len(scenario.nodes)}")
    console.print(f"[yellow]Start node:[/yellow] {scenario.start_node_id}")

    # Count endings
    endings = [n for n in scenario.nodes.values() if n.is_ending]
    console.print(f"[yellow]Endings:[/yellow] {len(endings)}")

    # List all nodes
    console.print("\n[bold]All Nodes:[/bold]")
    for node_id, node in sorted(scenario.nodes.items()):
        marker = "⚡" if node.is_ending else "📄"
        console.print(f"  {marker} {node_id}: {node.title}")

    # Show tree structure
    console.print("\n[bold]Decision Tree:[/bold]")
    tree = Tree(f"[bold cyan]{scenario.get_start_node().title}[/bold cyan]")
    build_tree(scenario, scenario.start_node_id, tree)
    console.print(tree)

    # List all possible endings
    console.print("\n[bold]Possible Endings:[/bold]")
    for i, ending in enumerate(endings, 1):
        console.print(f"  {i}. [green]{ending.title}[/green] [dim]({ending.id})[/dim]")

    console.print()
