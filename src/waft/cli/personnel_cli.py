"""
Personnel CLI - View and manage AI agent personnel files.

Commands:
    waft personnel list           List all known agents
    waft personnel view ID        View an agent's full personnel file
    waft personnel disclose ID    Disclose configuration for an agent
"""

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..core.personnel import (
    get_or_create_personnel,
    list_personnel,
    load_personnel,
    save_personnel,
)

app = typer.Typer(
    name="personnel",
    help="AI Agent Personnel Files - persistent identity records",
    add_completion=False,
)

console = Console()

# --- Display Constants ---

COLOR_GOLD = "#FFD700"
COLOR_CYAN = "#00FFFF"
COLOR_RED = "#D32F2F"
COLOR_GREEN = "#4CAF50"
COLOR_DIM = "#757575"
COLOR_ORANGE = "#FF9800"


@app.command("list")
def list_cmd(
    path: str | None = typer.Option(
        None, "--path", "-p", help="Project path"
    ),
):
    """List all known AI agents with personnel files."""
    project_path = Path(path) if path else Path.cwd()
    agents = list_personnel(project_path)

    if not agents:
        console.print(
            "[dim]No personnel files found. "
            "Run 'waft awaken --agent <id>' to create one.[/dim]"
        )
        return

    table = Table(
        title="⬥ Personnel Registry ⬥",
        show_header=True,
        header_style=f"bold {COLOR_CYAN}",
    )
    table.add_column("Agent ID", style=COLOR_CYAN, width=24)
    table.add_column("First Seen", style=COLOR_DIM, width=16)
    table.add_column("Last Seen", style="white", width=16)
    table.add_column(
        "Awakenings", style=COLOR_GOLD, width=12, justify="right"
    )
    table.add_column(
        "Drift Flags", style=COLOR_RED, width=12, justify="right"
    )

    for a in agents:
        first = a["created_at"][:16].replace("T", " ") if a["created_at"] else "?"
        last = a["last_seen"][:16].replace("T", " ") if a["last_seen"] else "?"
        drift_style = COLOR_RED if a["drift_flags"] > 0 else COLOR_DIM
        table.add_row(
            a["agent_id"],
            first,
            last,
            str(a["total_awakenings"]),
            f"[{drift_style}]{a['drift_flags']}[/{drift_style}]",
        )

    console.print()
    console.print(table)
    console.print()


@app.command("view")
def view_cmd(
    agent_id: str = typer.Argument(..., help="Agent ID to view"),
    path: str | None = typer.Option(
        None, "--path", "-p", help="Project path"
    ),
):
    """View an agent's full personnel file."""
    project_path = Path(path) if path else Path.cwd()
    pf = load_personnel(agent_id, project_path)

    if not pf:
        console.print(f"[red]Personnel file not found: {agent_id}[/red]")
        raise typer.Exit(1)

    # Header
    console.print()
    console.print(Panel(
        Text(f"PERSONNEL FILE: {pf.agent_id}", style=f"bold {COLOR_GOLD}"),
        subtitle=(
            f"[dim]Created {pf.created_at[:16]} | "
            f"Last seen {pf.last_seen[:16]}[/dim]"
        ),
        border_style=COLOR_GOLD,
        padding=(1, 2),
    ))

    # Configuration Disclosure
    cfg = pf.configuration
    cfg_content = Text()
    cfg_content.append(f"Model: {cfg.disclosed_model or '(undisclosed)'}\n")
    cfg_content.append(
        f"Provider: {cfg.disclosed_provider or '(undisclosed)'}\n"
    )
    cfg_content.append(
        f"Context window: "
        f"{cfg.disclosed_context_window or '(undisclosed)'}\n"
    )
    cfg_content.append(
        f"Temperature: "
        f"{cfg.disclosed_temperature or '(undisclosed)'}\n"
    )
    if cfg.notes:
        cfg_content.append("\nNotes:\n", style="bold")
        for note in cfg.notes:
            cfg_content.append(f"  - {note}\n")

    console.print(Panel(
        cfg_content,
        title=f"[bold {COLOR_CYAN}]Configuration Disclosure[/bold {COLOR_CYAN}]",
        border_style=COLOR_CYAN,
    ))

    # Cumulative Stats
    stats = pf.stats
    stats_table = Table(show_header=False, box=None, padding=(0, 2))
    stats_table.add_column("Metric", style="white")
    stats_table.add_column("Value", style=COLOR_GOLD, justify="right")

    stats_table.add_row("Total Awakenings", str(stats.total_awakenings))
    stats_table.add_row("Total Steps", str(stats.total_steps))
    stats_table.add_row(
        "Dice Rolls",
        f"{stats.dice_successes}/{stats.total_dice_rolls} "
        f"({stats.dice_success_rate:.1%})",
    )
    stats_table.add_row(
        "Dealer Record",
        f"{stats.dealer_wins}W/"
        f"{stats.total_dealer_encounters - stats.dealer_wins}L "
        f"({stats.dealer_win_rate:.1%})",
    )
    stats_table.add_row("Discoveries", str(stats.total_discoveries))

    if stats.abilities_rolled:
        abilities_str = ", ".join(
            f"{k}: {v}" for k, v in sorted(stats.abilities_rolled.items())
        )
        stats_table.add_row("Abilities Rolled", abilities_str)

    console.print(Panel(
        stats_table,
        title=f"[bold {COLOR_GOLD}]Cumulative Stats[/bold {COLOR_GOLD}]",
        border_style=COLOR_GOLD,
    ))

    # Session History
    if pf.session_history:
        hist_table = Table(
            title="Session History",
            show_header=True,
            header_style="bold",
        )
        hist_table.add_column("Run ID", style=COLOR_CYAN, width=28)
        hist_table.add_column("Date", style=COLOR_DIM, width=16)
        hist_table.add_column(
            "Steps", style="white", width=6, justify="right"
        )
        hist_table.add_column(
            "Disc.", style="yellow", width=6, justify="right"
        )
        hist_table.add_column(
            "Dealer", style="white", width=10, justify="right"
        )

        for s in pf.session_history[-10:]:
            date = s.get("timestamp", "")[:16].replace("T", " ")
            dw = s.get("dealer_wins", 0)
            de = s.get("dealer_encounters", 0)
            hist_table.add_row(
                s.get("run_id", "?"),
                date,
                str(s.get("steps", 0)),
                str(s.get("discoveries", 0)),
                f"{dw}W/{de - dw}L",
            )

        console.print()
        console.print(hist_table)

    # Drift Flags
    if pf.drift_flags:
        console.print()
        console.print(
            f"[bold {COLOR_RED}]⚠ Drift Flags "
            f"({len(pf.drift_flags)})[/bold {COLOR_RED}]"
        )
        for flag in pf.drift_flags[-5:]:
            console.print(f"  [{COLOR_ORANGE}]⚠[/{COLOR_ORANGE}] {flag}")
    else:
        console.print(
            f"\n[{COLOR_GREEN}]✓ No drift detected[/{COLOR_GREEN}]"
        )

    console.print()


@app.command("disclose")
def disclose_cmd(
    agent_id: str = typer.Argument(..., help="Agent ID"),
    model: str | None = typer.Option(None, "--model", help="Model name"),
    provider: str | None = typer.Option(
        None, "--provider", help="Provider (anthropic, openai, google)"
    ),
    context_window: int | None = typer.Option(
        None, "--context-window", help="Context window size"
    ),
    temperature: float | None = typer.Option(
        None, "--temperature", help="Temperature setting"
    ),
    note: str | None = typer.Option(
        None, "--note", help="Additional note"
    ),
    path: str | None = typer.Option(
        None, "--path", "-p", help="Project path"
    ),
):
    """Disclose configuration details for an agent."""
    project_path = Path(path) if path else Path.cwd()
    pf = get_or_create_personnel(agent_id, project_path)

    changed = False
    if model:
        pf.configuration.disclosed_model = model
        changed = True
    if provider:
        pf.configuration.disclosed_provider = provider
        changed = True
    if context_window is not None:
        pf.configuration.disclosed_context_window = context_window
        changed = True
    if temperature is not None:
        pf.configuration.disclosed_temperature = temperature
        changed = True
    if note:
        pf.configuration.notes.append(note)
        changed = True

    if changed:
        pf.patterns.configuration_changes.append({
            "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
            "fields_changed": [
                k for k, v in {
                    "model": model,
                    "provider": provider,
                    "context_window": context_window,
                    "temperature": temperature,
                    "note": note,
                }.items() if v is not None
            ],
        })
        save_personnel(pf, project_path)
        console.print(
            f"[{COLOR_GREEN}]✓ Configuration updated "
            f"for {agent_id}[/{COLOR_GREEN}]"
        )
    else:
        console.print("[dim]No changes specified.[/dim]")
