"""
The Chief CLI: Commands for iterative self-improvement loops.

Integrates Chief Wiggum's iterative development methodology into WAFT's CLI,
allowing for self-referential AI development loops.
"""

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..pantheon import TheChief
from ..utils import resolve_project_path

app = typer.Typer(
    name="chief",
    help="🚨 The Chief - Iterative self-improvement loops",
    add_completion=False,
)

console = Console()


@app.command("loop")
def start_loop(
    prompt: str = typer.Argument(
        ...,
        help="The prompt to iterate on. Include success criteria and <promise>COMPLETE</promise> tag.",
    ),
    max_iterations: int = typer.Option(
        10,
        "--max-iterations",
        "-n",
        help="Maximum number of iterations (recommended: 10-20)",
    ),
    completion_promise: str = typer.Option(
        None,
        "--completion-promise",
        "-c",
        help="Text phrase that signals completion (e.g., 'COMPLETE')",
    ),
) -> None:
    """
    Start a self-referential iteration loop.

    The Chief will repeatedly feed the same prompt to Claude, allowing it to
    see its previous work in files and git history, iteratively improving
    until completion criteria are met.

    Example:
        waft chief loop "Build a REST API for todos with tests" --max-iterations 15 --completion-promise "COMPLETE"
    """
    try:
        project_path = resolve_project_path()
        chief = TheChief(project_path=project_path)

        # Start loop
        result = chief.start_loop(
            prompt=prompt,
            max_iterations=max_iterations,
            completion_promise=completion_promise,
        )

        # Display result
        console.print()
        console.print(
            Panel(
                Text.from_markup(
                    f"[bold cyan]🚨 The Chief has initiated iteration loop[/bold cyan]\n\n"
                    f"[yellow]Loop ID:[/yellow] {result['loop_id']}\n"
                    f"[yellow]Max Iterations:[/yellow] {max_iterations}\n"
                    f"[yellow]Completion Promise:[/yellow] {completion_promise or 'None'}\n\n"
                    f"[dim]The loop will continue until:\n"
                    f"  • Completion promise is detected\n"
                    f"  • Max iterations reached\n"
                    f"  • Loop is cancelled with 'waft chief cancel'[/dim]"
                ),
                title="[bold]The Chief[/bold]",
                border_style="cyan",
            )
        )
        console.print()

        if not completion_promise:
            console.print(
                "[yellow]⚠️  Warning: No completion promise specified. "
                "Loop will run until max iterations.[/yellow]\n"
            )

        console.print(
            f"[green]✓[/green] Loop started. Use [cyan]waft chief status {result['loop_id']}[/cyan] to check progress.\n"
        )

    except Exception as e:
        console.print(f"[red]✗ Error starting loop:[/red] {e}\n")
        raise typer.Exit(code=1)


@app.command("cancel")
def cancel_loop(
    loop_id: str = typer.Argument(
        None,
        help="Loop ID to cancel (if not provided, cancels the most recent active loop)",
    ),
) -> None:
    """
    Cancel an active iteration loop.

    Example:
        waft chief cancel loop_20260123_120000
    """
    try:
        project_path = resolve_project_path()
        chief = TheChief(project_path=project_path)

        # If no loop_id provided, get the most recent active loop
        if not loop_id:
            active_loops = chief.get_active_loops()
            if not active_loops:
                console.print("[yellow]⚠️  No active loops to cancel.[/yellow]\n")
                raise typer.Exit(code=0)
            loop_id = active_loops[-1]["loop_id"]

        # Cancel loop
        result = chief.cancel_loop(loop_id)

        if "error" in result:
            console.print(f"[red]✗ Error:[/red] {result['error']}\n")
            raise typer.Exit(code=1)

        console.print()
        console.print(
            Panel(
                Text.from_markup(
                    f"[bold red]🚨 Loop Cancelled[/bold red]\n\n"
                    f"[yellow]Loop ID:[/yellow] {result['loop_id']}\n"
                    f"[yellow]Status:[/yellow] {result['status']}\n\n"
                    f"{result['message']}"
                ),
                title="[bold]The Chief[/bold]",
                border_style="red",
            )
        )
        console.print()

    except Exception as e:
        console.print(f"[red]✗ Error cancelling loop:[/red] {e}\n")
        raise typer.Exit(code=1)


@app.command("status")
def show_status(
    loop_id: str = typer.Argument(
        None,
        help="Loop ID to show status for (if not provided, shows all active loops)",
    ),
) -> None:
    """
    Show status of iteration loops.

    Example:
        waft chief status loop_20260123_120000
    """
    try:
        project_path = resolve_project_path()
        chief = TheChief(project_path=project_path)

        if loop_id:
            # Show specific loop
            loop_data = chief.get_loop_status(loop_id)
            if not loop_data:
                console.print(f"[red]✗ Loop not found:[/red] {loop_id}\n")
                raise typer.Exit(code=1)

            _display_loop_details(loop_data)
        else:
            # Show all active loops
            active_loops = chief.get_active_loops()
            if not active_loops:
                console.print("[yellow]⚠️  No active loops.[/yellow]\n")
                raise typer.Exit(code=0)

            _display_active_loops(active_loops)

    except Exception as e:
        console.print(f"[red]✗ Error showing status:[/red] {e}\n")
        raise typer.Exit(code=1)


@app.command("summary")
def show_summary() -> None:
    """
    Show The Chief's summary - all loops and analytics.

    Example:
        waft chief summary
    """
    try:
        project_path = resolve_project_path()
        chief = TheChief(project_path=project_path)

        summary = chief.get_chief_summary()

        console.print()
        console.print(
            Panel(
                _format_summary(summary),
                title="[bold cyan]🚨 The Chief - Summary[/bold cyan]",
                border_style="cyan",
            )
        )
        console.print()

    except Exception as e:
        console.print(f"[red]✗ Error showing summary:[/red] {e}\n")
        raise typer.Exit(code=1)


@app.command("analyze")
def analyze_loop(
    loop_id: str = typer.Argument(..., help="Loop ID to analyze"),
) -> None:
    """
    Analyze the effectiveness of a completed loop.

    Example:
        waft chief analyze loop_20260123_120000
    """
    try:
        project_path = resolve_project_path()
        chief = TheChief(project_path=project_path)

        analysis = chief.analyze_loop_effectiveness(loop_id)

        if "error" in analysis:
            console.print(f"[red]✗ Error:[/red] {analysis['error']}\n")
            raise typer.Exit(code=1)

        console.print()
        console.print(
            Panel(
                _format_analysis(analysis),
                title=f"[bold cyan]📊 Loop Analysis - {loop_id}[/bold cyan]",
                border_style="cyan",
            )
        )
        console.print()

    except Exception as e:
        console.print(f"[red]✗ Error analyzing loop:[/red] {e}\n")
        raise typer.Exit(code=1)


def _display_loop_details(loop_data: dict) -> None:
    """Display detailed information about a loop."""
    console.print()
    console.print(
        Panel(
            Text.from_markup(
                f"[bold cyan]Loop Details[/bold cyan]\n\n"
                f"[yellow]Loop ID:[/yellow] {loop_data['loop_id']}\n"
                f"[yellow]Status:[/yellow] {loop_data['status']}\n"
                f"[yellow]Current Iteration:[/yellow] {loop_data['current_iteration']}/{loop_data['max_iterations']}\n"
                f"[yellow]Completion Promise:[/yellow] {loop_data['completion_promise'] or 'None'}\n\n"
                f"[yellow]Prompt:[/yellow]\n{loop_data['prompt']}\n\n"
                f"[yellow]Created:[/yellow] {loop_data['created_at']}\n"
                f"[yellow]Completed:[/yellow] {loop_data['completed_at'] or 'In progress'}"
            ),
            title="[bold]The Chief[/bold]",
            border_style="cyan",
        )
    )
    console.print()

    # Show iteration history if available
    if loop_data.get("iterations_history"):
        table = Table(title="Iteration History", show_header=True)
        table.add_column("Iteration", style="cyan")
        table.add_column("Timestamp", style="yellow")
        table.add_column("Summary", style="white")

        for iteration in loop_data["iterations_history"][-5:]:  # Show last 5
            table.add_row(
                str(iteration["iteration"]),
                iteration["timestamp"],
                str(iteration["data"])[:50] + "...",
            )

        console.print(table)
        console.print()


def _display_active_loops(active_loops: list) -> None:
    """Display table of active loops."""
    console.print()

    table = Table(title="🚨 Active Iteration Loops", show_header=True)
    table.add_column("Loop ID", style="cyan")
    table.add_column("Status", style="yellow")
    table.add_column("Progress", style="green")
    table.add_column("Promise", style="white")
    table.add_column("Created", style="dim")

    for loop in active_loops:
        progress = f"{loop['current_iteration']}/{loop['max_iterations']}"
        table.add_row(
            loop["loop_id"],
            loop["status"],
            progress,
            loop["completion_promise"] or "None",
            loop["created_at"][:19],
        )

    console.print(table)
    console.print()


def _format_summary(summary: dict) -> Text:
    """Format summary text."""
    text = Text()
    text.append("Active Loops: ", style="yellow bold")
    text.append(f"{summary['active_loops']}\n", style="cyan")
    text.append("Completed Loops: ", style="yellow bold")
    text.append(f"{summary['completed_loops']}\n", style="cyan")
    text.append("Total Loops: ", style="yellow bold")
    text.append(f"{summary['total_loops']}\n", style="cyan")
    text.append("Total Iterations: ", style="yellow bold")
    text.append(f"{summary['total_iterations']}\n", style="cyan")
    text.append("Avg Iterations/Loop: ", style="yellow bold")
    text.append(f"{summary['average_iterations_per_loop']}\n\n", style="cyan")

    # Wiggum integration info
    wiggum = summary.get("wiggum_integration", {})
    text.append("🎩 Chief Wiggum Integration\n", style="bold magenta")
    text.append(f"  Status: ", style="yellow")
    text.append(
        f"{'✓ Enabled' if wiggum.get('enabled') else '✗ Disabled'}\n",
        style="green" if wiggum.get("enabled") else "red",
    )
    text.append(f"  Version: ", style="yellow")
    text.append(f"{wiggum.get('version', 'unknown')}\n", style="cyan")

    text.append(f"\nLast Update: ", style="yellow bold")
    text.append(f"{summary['last_update']}", style="dim")

    return text


def _format_analysis(analysis: dict) -> Text:
    """Format analysis text."""
    text = Text()
    text.append("Total Iterations: ", style="yellow bold")
    text.append(f"{analysis['total_iterations']}\n", style="cyan")
    text.append("Status: ", style="yellow bold")
    text.append(f"{analysis['status']}\n", style="cyan")
    text.append("Efficiency Ratio: ", style="yellow bold")
    text.append(f"{analysis['efficiency_ratio']:.2%}\n", style="cyan")
    text.append("Completed Successfully: ", style="yellow bold")
    text.append(
        f"{'✓ Yes' if analysis['completed_successfully'] else '✗ No'}\n",
        style="green" if analysis["completed_successfully"] else "red",
    )

    if analysis["duration_seconds"]:
        minutes = analysis["duration_seconds"] / 60
        text.append("Duration: ", style="yellow bold")
        text.append(f"{minutes:.2f} minutes\n", style="cyan")

    return text


if __name__ == "__main__":
    app()
