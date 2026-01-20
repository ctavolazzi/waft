#!/usr/bin/env python3
"""
External Drive Realm Status: View and manage the External Drive Realm Entity.

The External Drive Realm is a Pantheon Entity (Timeless Force) that maintains
storage principles and manages content routing to realms on the external drive.
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

from src.waft.pantheon import ExternalDriveRealm

app = typer.Typer()
console = Console()


@app.command()
def status():
    """
    View External Drive Realm status.

    Shows realm availability, registered realms, storage stats, and current status.
    """
    project_path = Path.cwd()
    realm = ExternalDriveRealm(project_path)

    summary = realm.get_realm_summary()

    console.print("\n[bold cyan]💾 External Drive Realm Status[/bold cyan]\n")

    # Status panel
    status_color = "green" if summary["realm_active"] else "red"
    status_icon = "✅" if summary["realm_active"] else "❌"

    status_content = f"""
[bold]Realm Status:[/bold] {status_icon} {"Active" if summary["realm_active"] else "Inactive"}
[bold]Drive Available:[/bold] {summary["drive_available"]}
[bold]Drive Path:[/bold] {summary.get("drive_path", "N/A")}
[bold]Registered Realms:[/bold] {summary["registered_realms"]}
[bold]Content in Realms:[/bold] {summary["content_in_realms"]}
[bold]Last Update:[/bold] {summary.get("last_update", "N/A")}
"""

    console.print(Panel(status_content.strip(), title="Realm Status", border_style=status_color))

    # Storage principles
    principles = summary.get("storage_principles", {})
    console.print("\n[bold]Storage Principles:[/bold]")
    principles_table = Table(show_header=True, header_style="bold magenta")
    principles_table.add_column("Principle", style="cyan")
    principles_table.add_column("Value", style="green")

    principles_table.add_row(
        "Core Content → Local", "✅" if principles.get("core_content_local") else "❌"
    )
    principles_table.add_row(
        "Augmented Content → External",
        "✅" if principles.get("augmented_content_external") else "❌",
    )
    principles_table.add_row(
        "Fallback to Local", "✅" if principles.get("fallback_to_local") else "❌"
    )

    console.print(principles_table)

    # Storage stats
    stats = summary.get("storage_stats", {})
    if stats:
        console.print("\n[bold]Storage Statistics:[/bold]")
        stats_table = Table(show_header=True, header_style="bold magenta")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")

        stats_table.add_row("Total Content", str(stats.get("total_content", 0)))
        stats_table.add_row("Content on External", str(stats.get("content_on_external", 0)))
        stats_table.add_row("Content Local", str(stats.get("content_local", 0)))
        stats_table.add_row("Total PDFs", str(stats.get("total_pdfs", 0)))
        stats_table.add_row("PDFs on External", str(stats.get("pdfs_on_external", 0)))
        stats_table.add_row("PDFs Local", str(stats.get("pdfs_local", 0)))

        console.print(stats_table)

    # List realms
    realms = realm.list_realms()
    if realms:
        console.print("\n[bold]Registered Realms:[/bold]")
        realms_table = Table(show_header=True, header_style="bold magenta")
        realms_table.add_column("Realm ID", style="cyan")
        realms_table.add_column("Realm Name", style="green")
        realms_table.add_column("Drive", style="yellow")
        realms_table.add_column("Status", style="magenta")
        realms_table.add_column("Created", style="dim")

        for r in realms:
            realms_table.add_row(
                r["realm_id"], r["realm_name"], r["drive_name"], r["status"], r["created_at"][:19]
            )

        console.print(realms_table)
    else:
        console.print("\n[yellow]⚠️  No realms registered yet[/yellow]")
        console.print("[dim]Use 'register' command to create a realm[/dim]")

    console.print()


@app.command()
def register(
    realm_name: str = typer.Argument(..., help="Name of the realm (e.g., 'Universe', 'Earth')"),
    drive_name: str = typer.Option("Easystore", "--drive", "-d", help="External drive name"),
    project_name: str = typer.Option(
        None, "--project", "-p", help="Project name (auto-detected if not provided)"
    ),
):
    """
    Register a new realm on the external drive.

    Creates a realm structure: Realms/[realm_name]/ on the external drive.
    """
    project_path = Path.cwd()
    realm = ExternalDriveRealm(project_path)

    result = realm.register_realm(
        realm_name=realm_name, drive_name=drive_name, project_name=project_name
    )

    if result["success"]:
        console.print("\n[bold green]✅ Realm Registered[/bold green]\n")
        console.print(f"[bold]Realm ID:[/bold] {result['realm']['realm_id']}")
        console.print(f"[bold]Realm Name:[/bold] {result['realm']['realm_name']}")
        console.print(f"[bold]Storage Path:[/bold] {result['realm']['realm_storage_path']}")
        console.print(f"[bold]Status:[/bold] {result['realm']['status']}\n")
    else:
        console.print("\n[bold red]❌ Failed to Register Realm[/bold red]\n")
        console.print(f"[bold]Error:[/bold] {result.get('error', 'Unknown error')}\n")


@app.command()
def list():
    """
    List all registered realms.
    """
    project_path = Path.cwd()
    realm = ExternalDriveRealm(project_path)

    realms = realm.list_realms()

    if not realms:
        console.print("\n[yellow]⚠️  No realms registered[/yellow]\n")
        return

    console.print("\n[bold cyan]📋 Registered Realms[/bold cyan]\n")

    for r in realms:
        panel_content = f"""
[bold]Realm Name:[/bold] {r["realm_name"]}
[bold]Realm ID:[/bold] {r["realm_id"]}
[bold]Drive:[/bold] {r["drive_name"]}
[bold]Storage Path:[/bold] {r["realm_storage_path"]}
[bold]Status:[/bold] {r["status"]}
[bold]Created:[/bold] {r["created_at"]}
"""
        console.print(
            Panel(panel_content.strip(), title=f"Realm: {r['realm_name']}", border_style="cyan")
        )

    console.print()


@app.command()
def content(realm_name: str = typer.Argument(..., help="Realm name")):
    """
    List all content stored in a specific realm.
    """
    project_path = Path.cwd()
    realm = ExternalDriveRealm(project_path)

    content_list = realm.get_realm_content(realm_name)

    if not content_list:
        console.print(f"\n[yellow]⚠️  No content in realm '{realm_name}'[/yellow]\n")
        return

    console.print(f"\n[bold cyan]📦 Content in Realm: {realm_name}[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Content Path", style="cyan")
    table.add_column("Storage Path", style="green")
    table.add_column("Type", style="yellow")
    table.add_column("Registered", style="dim")

    for entry in content_list:
        table.add_row(
            entry["content_path"],
            entry["storage_path"],
            entry["content_type"],
            entry["registered_at"][:19],
        )

    console.print(table)
    console.print()


if __name__ == "__main__":
    app()
