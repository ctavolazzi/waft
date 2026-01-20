#!/usr/bin/env python3
"""
Realm Colonization CLI: Trigger colonization of new Realms

This script allows you to:
- Detect and colonize new external drives as Realms
- View colonization status
- View tethers to Realms
- View assimilated data
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

from src.waft.core.realm_colonization import RealmColonizationSystem
from src.waft.core.the_one_core_being import TheOneCoreBeing

app = typer.Typer()
console = Console()


@app.command()
def colonize(
    drive_name: str = typer.Option("Easystore", "--drive", "-d", help="External drive name"),
    realm_name: str = typer.Option(
        None, "--realm", "-r", help="Realm name (auto-generated if not provided)"
    ),
):
    """
    Detect and colonize a new external drive as a Realm.

    This will:
    1. Detect the external drive
    2. Create PrimeBeing for the Realm
    3. Form Tether through observation
    4. Launch scouting mission
    5. Report to Mission Control
    """
    project_path = Path.cwd()
    colonization = RealmColonizationSystem(project_path=project_path)

    console.print(f"\n[bold cyan]🌍 Colonizing Realm on {drive_name}...[/bold cyan]\n")

    result = colonization.detect_and_colonize_realm(drive_name=drive_name, realm_name=realm_name)

    if result.get("success"):
        console.print("[bold green]✅ Realm Colonized Successfully[/bold green]\n")

        panel_content = f"""
[bold]Realm Name:[/bold] {result["realm_name"]}
[bold]Realm Path:[/bold] {result["realm_path"]}
[bold]Prime Being ID:[/bold] {result["prime_being_id"]}
[bold]Tether ID:[/bold] {result["tether_id"]}
[bold]Mission ID:[/bold] {result["mission_id"]}
[bold]Findings:[/bold] {len(result["scouting_result"].get("findings", []))} items
[bold]Gaps Discovered:[/bold] {len(result["scouting_result"].get("gaps_discovered", []))}
[bold]Holes Identified:[/bold] {len(result["scouting_result"].get("holes_identified", []))}
"""
        console.print(
            Panel(panel_content.strip(), title="Colonization Result", border_style="green")
        )

        if result["scouting_result"].get("findings_path"):
            console.print(
                f"\n[dim]Findings written to: {result['scouting_result']['findings_path']}[/dim]\n"
            )
    else:
        console.print("\n[bold red]❌ Colonization Failed[/bold red]\n")
        console.print(f"[bold]Error:[/bold] {result.get('error', 'Unknown error')}\n")


@app.command()
def status():
    """
    View colonization status.
    """
    project_path = Path.cwd()
    colonization = RealmColonizationSystem(project_path=project_path)
    the_one_core = TheOneCoreBeing(project_path=project_path)

    console.print("\n[bold cyan]🌍 Realm Colonization Status[/bold cyan]\n")

    # Load colonization state
    import json

    state_file = colonization.colonized_realms_file
    if state_file.exists():
        state = json.loads(state_file.read_text(encoding="utf-8"))
        realms = state.get("colonized_realms", [])
    else:
        realms = []

    # Get tethers
    the_one_core.get_tethers()

    # Get summary
    summary = the_one_core.get_summary()

    # Colonization summary
    console.print(
        Panel(
            f"""
[bold]Colonized Realms:[/bold] {len(realms)}
[bold]Active Tethers:[/bold] {summary["active_tethers"]}
[bold]Total Tethers:[/bold] {summary["total_tethers"]}
[bold]Assimilated Records:[/bold] {summary["assimilated_records"]}
[bold]Gaps Discovered:[/bold] {summary["gaps_discovered"]}
[bold]Holes Identified:[/bold] {summary["holes_identified"]}
""".strip(),
            title="Colonization Summary",
            border_style="cyan",
        )
    )

    # List colonized realms
    if realms:
        console.print("\n[bold]Colonized Realms:[/bold]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Realm Name", style="cyan")
        table.add_column("Prime Being", style="green")
        table.add_column("Tether ID", style="yellow")
        table.add_column("Mission ID", style="magenta")
        table.add_column("Colonized", style="dim")

        for realm in realms:
            table.add_row(
                realm["realm_name"],
                realm["prime_being_id"],
                realm.get("tether_id", "N/A")[:20] + "...",
                realm.get("mission_id", "N/A")[:20] + "...",
                realm.get("colonized_at", "N/A")[:19],
            )

        console.print(table)
    else:
        console.print("\n[yellow]⚠️  No realms colonized yet[/yellow]")
        console.print("[dim]Use 'colonize' command to colonize a new Realm[/dim]")

    console.print()


@app.command()
def tethers():
    """
    View all tethers to Realms.
    """
    project_path = Path.cwd()
    the_one_core = TheOneCoreBeing(project_path=project_path)

    tethers = the_one_core.get_tethers()

    console.print("\n[bold cyan]🔗 Tethers to Realms[/bold cyan]\n")

    if tethers:
        for tether in tethers:
            panel_content = f"""
[bold]Tether ID:[/bold] {tether["tether_id"]}
[bold]Realm Name:[/bold] {tether["realm_name"]}
[bold]Realm Path:[/bold] {tether["realm_path"]}
[bold]Prime Being ID:[/bold] {tether["prime_being_id"]}
[bold]Status:[/bold] {tether["status"]}
[bold]Formed At:[/bold] {tether["formed_at"]}
[bold]Last Communication:[/bold] {tether["last_communication"]}
"""
            console.print(
                Panel(
                    panel_content.strip(),
                    title=f"Tether: {tether['realm_name']}",
                    border_style="cyan",
                )
            )
    else:
        console.print("[yellow]⚠️  No tethers formed yet[/yellow]\n")


@app.command()
def assimilated():
    """
    View assimilated data from Realm scouts.
    """
    project_path = Path.cwd()
    the_one_core = TheOneCoreBeing(project_path=project_path)

    data = the_one_core.get_assimilated_data()

    console.print("\n[bold cyan]📊 Assimilated Data[/bold cyan]\n")

    records = data.get("assimilated_data", [])
    gaps = data.get("gaps_discovered", [])
    holes = data.get("holes_identified", [])

    console.print(f"[bold]Total Records:[/bold] {len(records)}")
    console.print(f"[bold]Total Gaps:[/bold] {len(gaps)}")
    console.print(f"[bold]Total Holes:[/bold] {len(holes)}\n")

    if records:
        console.print("[bold]Recent Assimilations:[/bold]")
        for record in records[-5:]:  # Show last 5
            console.print(f"\n[bold]Realm:[/bold] {record['realm_name']}")
            console.print(f"[bold]Assimilated:[/bold] {record['assimilated_at']}")
            if record.get("gaps_discovered"):
                console.print(f"[bold]Gaps:[/bold] {', '.join(record['gaps_discovered'])}")
            if record.get("holes_identified"):
                console.print(f"[bold]Holes:[/bold] {', '.join(record['holes_identified'])}")

    if gaps:
        console.print("\n[bold]All Gaps Discovered:[/bold]")
        for gap in gaps:
            console.print(f"  - {gap}")

    if holes:
        console.print("\n[bold]All Holes Identified:[/bold]")
        for hole in holes:
            console.print(f"  - {hole}")

    console.print()


if __name__ == "__main__":
    app()
