#!/usr/bin/env python3
"""
Mission Control Status: View real-time mission monitoring and command center status.

Inspired by Avatar's human base operations and Fern Gully's fairy coordination.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.pantheon import MissionControl
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import typer

app = typer.Typer()
console = Console()


@app.command()
def status(
    mission_id: str = typer.Option(None, "--mission", "-m", help="Specific mission ID"),
    summary: bool = typer.Option(False, "--summary", "-s", help="Show control summary only")
):
    """
    View Mission Control status.
    
    Shows real-time mission monitoring, status tracking, and command center overview.
    """
    project_path = Path.cwd()
    mission_control = MissionControl(project_path)
    
    if summary:
        # Show control summary
        summary_data = mission_control.get_control_summary()
        
        console.print("\n[bold cyan]🎯 Mission Control Summary[/bold cyan]\n")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Missions Monitored", str(summary_data["missions_monitored"]))
        table.add_row("Active Commands", str(summary_data["active_commands"]))
        table.add_row("Active Alerts", str(summary_data["active_alerts"]))
        
        console.print(table)
        
        if summary_data["mission_statuses"]:
            console.print("\n[bold]Mission Status Breakdown:[/bold]")
            status_table = Table(show_header=True, header_style="bold magenta")
            status_table.add_column("Status", style="cyan")
            status_table.add_column("Count", style="green")
            
            for status, count in summary_data["mission_statuses"].items():
                status_table.add_row(status, str(count))
            
            console.print(status_table)
        
        console.print(f"\n[dim]Last Update: {summary_data['last_update']}[/dim]\n")
        
    elif mission_id:
        # Show specific mission status
        status_data = mission_control.get_status(mission_id)
        
        if not status_data:
            console.print(f"[red]❌ Mission {mission_id} not found in Mission Control[/red]\n")
            return
        
        console.print(f"\n[bold cyan]📡 Mission Status: {mission_id}[/bold cyan]\n")
        
        panel_content = f"""
[bold]Status:[/bold] {status_data['status']}
[bold]Progress:[/bold] {status_data['progress']:.1%}
[bold]Last Update:[/bold] {status_data['last_update']}
"""
        
        if status_data.get('alerts'):
            panel_content += f"\n[bold yellow]⚠️  Alerts:[/bold yellow]\n"
            for alert in status_data['alerts']:
                panel_content += f"  • {alert}\n"
        
        if status_data.get('telemetry'):
            panel_content += f"\n[bold]Telemetry:[/bold]\n"
            for key, value in status_data['telemetry'].items():
                panel_content += f"  • {key}: {value}\n"
        
        console.print(Panel(panel_content.strip(), border_style="cyan"))
        console.print()
        
    else:
        # Show all mission statuses
        all_status = mission_control.get_all_status()
        
        if not all_status:
            console.print("[yellow]⚠️  No missions currently being monitored[/yellow]\n")
            return
        
        console.print("\n[bold cyan]🎯 Mission Control: All Missions[/bold cyan]\n")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Mission ID", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Progress", style="yellow")
        table.add_column("Alerts", style="red")
        table.add_column("Last Update", style="dim")
        
        for status_data in all_status:
            alerts_count = len(status_data.get('alerts', []))
            alerts_display = str(alerts_count) if alerts_count > 0 else "—"
            
            table.add_row(
                status_data['mission_id'],
                status_data['status'],
                f"{status_data['progress']:.1%}",
                alerts_display,
                status_data['last_update'][:19]  # Truncate to readable format
            )
        
        console.print(table)
        console.print()


@app.command()
def command(
    mission_id: str = typer.Argument(..., help="Mission ID"),
    command: str = typer.Argument(..., help="Command (halt, resume, prioritize, etc.)"),
    parameters: str = typer.Option(None, "--params", "-p", help="JSON parameters")
):
    """
    Issue a command to a mission.
    
    Commands: halt, resume, prioritize, update_status, etc.
    """
    import json
    
    project_path = Path.cwd()
    mission_control = MissionControl(project_path)
    
    params_dict = {}
    if parameters:
        try:
            params_dict = json.loads(parameters)
        except json.JSONDecodeError:
            console.print("[red]❌ Invalid JSON parameters[/red]\n")
            return
    
    command_data = mission_control.issue_command(
        mission_id=mission_id,
        command=command,
        parameters=params_dict
    )
    
    console.print(f"\n[bold green]✅ Command Issued[/bold green]\n")
    console.print(f"[bold]Command ID:[/bold] {command_data['command_id']}")
    console.print(f"[bold]Mission:[/bold] {mission_id}")
    console.print(f"[bold]Command:[/bold] {command}")
    console.print(f"[bold]Status:[/bold] {command_data['status']}")
    console.print(f"[bold]Issued At:[/bold] {command_data['issued_at']}\n")


if __name__ == "__main__":
    app()
