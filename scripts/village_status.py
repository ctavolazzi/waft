#!/usr/bin/env python3
"""
The Village Status: View community coordination and collective wisdom.

Inspired by Avatar's Na'vi village and Fern Gully's fairy community.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.waft.pantheon import TheVillage

app = typer.Typer()
console = Console()


@app.command()
def status(
    gathering_id: str = typer.Option(None, "--gathering", "-g", help="Specific gathering ID"),
    summary: bool = typer.Option(False, "--summary", "-s", help="Show village summary only"),
):
    """
    View The Village status.

    Shows community gatherings, connections, shared quests, and collective wisdom.
    """
    project_path = Path.cwd()
    village = TheVillage(project_path)

    if summary:
        # Show village summary
        summary_data = village.get_village_summary()

        console.print("\n[bold green]🌳 The Village Summary[/bold green]\n")

        table = Table(show_header=True, header_style="bold green")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Active Gatherings", str(summary_data["active_gatherings"]))
        table.add_row("Total Connections", str(summary_data["total_connections"]))
        table.add_row("Shared Quests", str(summary_data["shared_quests"]))
        table.add_row("Collective Wisdom", str(summary_data["collective_wisdom_count"]))

        console.print(table)
        console.print(f"\n[dim]Last Update: {summary_data['last_update']}[/dim]\n")

    elif gathering_id:
        # Show specific gathering
        gathering_file = village.gatherings_path / f"{gathering_id}.json"

        if not gathering_file.exists():
            console.print(f"[red]❌ Gathering {gathering_id} not found[/red]\n")
            return

        import json

        gathering_data = json.loads(gathering_file.read_text(encoding="utf-8"))

        console.print(f"\n[bold green]🌳 Gathering: {gathering_data['topic']}[/bold green]\n")

        panel_content = f"""
[bold]Topic:[/bold] {gathering_data["topic"]}
[bold]Description:[/bold] {gathering_data["description"]}
[bold]Status:[/bold] {gathering_data["status"]}
[bold]Participants:[/bold] {len(gathering_data.get("participants", []))}
[bold]Created:[/bold] {gathering_data["created_at"]}
"""

        if gathering_data.get("insights"):
            panel_content += "\n[bold]Insights:[/bold]\n"
            for insight_entry in gathering_data["insights"]:
                insight_text = insight_entry.get("insight", "")
                contributor = insight_entry.get("contributor", "Unknown")
                panel_content += f"  • {insight_text} [dim]({contributor})[/dim]\n"

        console.print(Panel(panel_content.strip(), border_style="green"))
        console.print()

    else:
        # Show all active gatherings
        import json

        registry = json.loads(village.registry_file.read_text(encoding="utf-8"))

        active_gatherings = []
        for gathering_id in registry["active_gatherings"]:
            gathering_file = village.gatherings_path / f"{gathering_id}.json"
            if gathering_file.exists():
                gathering_data = json.loads(gathering_file.read_text(encoding="utf-8"))
                if gathering_data.get("status") == "active":
                    active_gatherings.append(gathering_data)

        if not active_gatherings:
            console.print("[yellow]⚠️  No active gatherings in The Village[/yellow]\n")
            return

        console.print("\n[bold green]🌳 The Village: Active Gatherings[/bold green]\n")

        table = Table(show_header=True, header_style="bold green")
        table.add_column("Gathering ID", style="cyan")
        table.add_column("Topic", style="green")
        table.add_column("Participants", style="yellow")
        table.add_column("Insights", style="magenta")
        table.add_column("Created", style="dim")

        for gathering in active_gatherings:
            participants_count = len(gathering.get("participants", []))
            insights_count = len(gathering.get("insights", []))

            table.add_row(
                gathering["gathering_id"],
                gathering["topic"],
                str(participants_count),
                str(insights_count),
                gathering["created_at"][:19],
            )

        console.print(table)
        console.print()


@app.command()
def gathering(
    topic: str = typer.Argument(..., help="Gathering topic"),
    description: str = typer.Argument(..., help="Gathering description"),
    participants: str = typer.Option(
        None, "--participants", "-p", help="Comma-separated participant IDs"
    ),
):
    """
    Create a new village gathering.
    """
    project_path = Path.cwd()
    village = TheVillage(project_path)

    participants_list = []
    if participants:
        participants_list = [p.strip() for p in participants.split(",")]

    gathering_data = village.create_gathering(
        topic=topic, description=description, participants=participants_list
    )

    console.print("\n[bold green]✅ Gathering Created[/bold green]\n")
    console.print(f"[bold]Gathering ID:[/bold] {gathering_data['gathering_id']}")
    console.print(f"[bold]Topic:[/bold] {gathering_data['topic']}")
    console.print(f"[bold]Status:[/bold] {gathering_data['status']}")
    console.print(f"[bold]Created:[/bold] {gathering_data['created_at']}\n")


@app.command()
def insight(
    gathering_id: str = typer.Argument(..., help="Gathering ID"),
    insight: str = typer.Argument(..., help="Insight text"),
    contributor: str = typer.Option(None, "--contributor", "-c", help="Contributor identifier"),
):
    """
    Add an insight to a gathering.
    """
    project_path = Path.cwd()
    village = TheVillage(project_path)

    gathering_data = village.add_insight(
        gathering_id=gathering_id, insight=insight, contributor=contributor
    )

    console.print("\n[bold green]✅ Insight Added[/bold green]\n")
    console.print(f"[bold]Gathering:[/bold] {gathering_id}")
    console.print(f"[bold]Insight:[/bold] {insight}")
    console.print(f"[bold]Total Insights:[/bold] {len(gathering_data.get('insights', []))}\n")


@app.command()
def wisdom(
    wisdom: str = typer.Argument(..., help="Wisdom text"),
    source: str = typer.Option(None, "--source", "-s", help="Source of wisdom"),
):
    """
    Add to collective wisdom.
    """
    project_path = Path.cwd()
    village = TheVillage(project_path)

    wisdom_entry = village.add_wisdom(wisdom=wisdom, source=source)

    console.print("\n[bold green]✅ Wisdom Added[/bold green]\n")
    console.print(f"[bold]Wisdom ID:[/bold] {wisdom_entry['wisdom_id']}")
    console.print(f"[bold]Wisdom:[/bold] {wisdom_entry['wisdom']}")
    if source:
        console.print(f"[bold]Source:[/bold] {source}")
    console.print()


if __name__ == "__main__":
    app()
