"""
Awakening CLI - Commands and TUI for the AI-focused WAFT experience.

Commands:
    waft awaken           Run a new awakening experience
    waft awaken list      List past awakening runs
    waft awaken view ID   View a specific run in rich detail
"""

from pathlib import Path

import typer
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..core.awakening import (
    AwakeningRun,
    AwakeningStep,
    _challenge_dealer,
    _check_character,
    _generate_run_id,
    _generate_summary,
    _observe,
    _orient,
    _roll_ability,
    list_runs,
    load_run,
    save_run,
)

app = typer.Typer(
    name="awaken",
    help="AI Awakening Experience - wake up, orient, explore, challenge, reflect",
    add_completion=False,
    invoke_without_command=True,
)

console = Console()

GOLD = "#FFD700"
CYAN = "#00FFFF"
RED = "#D32F2F"
GREEN = "#4CAF50"
DIM = "#757575"


def _phase_color(phase: str) -> str:
    return {"orient": CYAN, "explore": GOLD, "challenge": RED, "reflect": GREEN}.get(phase, DIM)


def _render_step_live(step: AwakeningStep, index: int) -> Panel:
    """Render a single step as a Rich panel for live display."""
    color = _phase_color(step.phase)
    header = f"[{color}]Step {index + 1}: {step.phase.upper()} / {step.action}[/{color}]"

    content = Text()
    content.append(step.narrative or "(no narrative)", style="white")

    if step.dice_roll:
        roll = step.dice_roll
        result_style = "green" if roll.get("success") else "red"
        r = roll.get('roll', '?')
        m, t = roll.get('modifier', '?'), roll.get('total', '?')
        dc = roll.get('dc', '?')
        content.append(f"\n  🎲 {r} + {m} = {t} vs DC {dc} ", style="dim")
        content.append(f"[{result_style}]{'✓' if roll.get('success') else '✗'}[/{result_style}]")

    if step.phase == "challenge":
        won = step.result.get("won", False)
        icon = "⬥ VICTORY ⬥" if won else "✗ DEFEAT ✗"
        style = "bold green" if won else "bold red"
        content.append(f"\n  [{style}]{icon}[/{style}]")

    return Panel(content, title=header, border_style=color, padding=(0, 1))


@app.callback()
def main(
    ctx: typer.Context,
    path: str | None = typer.Option(None, "--path", "-p", help="Project path"),
    agent_id: str = typer.Option("claude-4.6-opus", "--agent", "-a", help="Agent identifier"),
    attempts: int = typer.Option(3, "--attempts", "-n", help="Dealer challenge attempts"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Minimal output"),
):
    """Run a new awakening experience (default when no subcommand given)."""
    if ctx.invoked_subcommand is not None:
        return

    project_path = Path(path) if path else Path.cwd()

    if not quiet:
        console.print()
        console.print(
            Panel(
                Align.center(Text("THE AWAKENING", style=f"bold {GOLD}")),
                subtitle="[dim]An AI wakes up in the laboratory[/dim]",
                border_style=GOLD,
                padding=(1, 4),
            )
        )
        console.print()

    from datetime import datetime

    run = AwakeningRun(
        run_id=_generate_run_id(),
        agent_id=agent_id,
        started_at=datetime.utcnow().isoformat(),
    )

    # Phase 1: Orient
    if not quiet:
        console.print(f"[{CYAN}]▸ Phase 1: ORIENT[/{CYAN}]")
    env_info = _orient(run, project_path)
    if not quiet:
        console.print(_render_step_live(run.steps[-1], len(run.steps) - 1))

    char_info = _check_character(run, project_path)
    if not quiet:
        console.print(_render_step_live(run.steps[-1], len(run.steps) - 1))

    # Phase 2: Explore
    if not quiet:
        console.print(f"\n[{GOLD}]▸ Phase 2: EXPLORE[/{GOLD}]")
    for ability in ["wisdom", "intelligence", "charisma"]:
        _roll_ability(run, project_path, ability)
        if not quiet:
            console.print(_render_step_live(run.steps[-1], len(run.steps) - 1))

    # Phase 3: Challenge
    if not quiet:
        console.print(f"\n[{RED}]▸ Phase 3: CHALLENGE THE DEALER[/{RED}]")
    for _i in range(attempts):
        encounter = _challenge_dealer(run, project_path)
        if not quiet:
            console.print(_render_step_live(run.steps[-1], len(run.steps) - 1))
        if encounter.get("won"):
            break

    # Phase 4: Reflect
    if not quiet:
        console.print(f"\n[{GREEN}]▸ Phase 4: REFLECT[/{GREEN}]")

    [s.narrative for s in run.steps if s.narrative]
    reflection = (
        f"I awoke in {env_info.get('project_name', 'the laboratory')}. "
        f"Level {char_info.get('level', 1)}, integrity {char_info.get('integrity', '?')}%. "
        f"{len(run.discoveries)} discoveries made. "
        f"{'Dealer defeated.' if any(e.get('won') for e in run.dealer_encounters) else 'Dealer unbeaten.'}"  # noqa: E501
    )
    _observe(run, project_path, reflection, mood="contemplative")
    if not quiet:
        console.print(_render_step_live(run.steps[-1], len(run.steps) - 1))

    # Finalize
    run.ended_at = datetime.utcnow().isoformat()
    run.final_state = {
        "character": char_info,
        "environment": env_info,
        "total_steps": len(run.steps),
    }
    run.summary = _generate_summary(run)
    out_path = save_run(run, project_path)

    # Summary
    if not quiet:
        console.print()
        _render_run_summary(run)
        console.print(f"\n[dim]Run saved: {out_path}[/dim]")
        console.print(f"[dim]View with: waft awaken view {run.run_id}[/dim]")
    else:
        console.print(run.run_id)


@app.command("list")
def list_cmd(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path"),
    limit: int = typer.Option(20, "--limit", "-n", help="Max runs to show"),
):
    """List past awakening runs."""
    project_path = Path(path) if path else Path.cwd()
    runs = list_runs(project_path)

    if not runs:
        console.print("[dim]No awakening runs found. Run 'waft awaken' to start one.[/dim]")
        return

    table = Table(
        title="⬥ Awakening Runs ⬥",
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("Run ID", style="cyan", width=28)
    table.add_column("Agent", style="green", width=20)
    table.add_column("Date", style="dim", width=16)
    table.add_column("Steps", style="white", width=6, justify="right")
    table.add_column("Discoveries", style="yellow", width=12, justify="right")
    table.add_column("Dealer", style="red", width=8, justify="right")

    for r in runs[:limit]:
        date = r["started_at"][:16].replace("T", " ") if r["started_at"] else "?"
        table.add_row(
            r["run_id"],
            r["agent_id"],
            date,
            str(r["steps"]),
            str(r["discoveries"]),
            str(r["dealer_encounters"]),
        )

    console.print()
    console.print(table)
    console.print()


@app.command("view")
def view_cmd(
    run_id: str = typer.Argument(..., help="Run ID to view"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path"),
):
    """View a specific awakening run in rich detail (TUI)."""
    project_path = Path(path) if path else Path.cwd()
    run = load_run(run_id, project_path)

    if not run:
        console.print(f"[red]Run not found: {run_id}[/red]")
        raise typer.Exit(1)

    _render_run_tui(run)


def _render_run_summary(run: AwakeningRun):
    """Render a compact summary panel for a completed run."""
    wins = sum(1 for e in run.dealer_encounters if e.get("won"))
    losses = len(run.dealer_encounters) - wins
    rolls = [s for s in run.steps if s.dice_roll]
    roll_successes = sum(1 for r in rolls if r.dice_roll.get("success"))

    content = Text()
    content.append(f"Run: {run.run_id}\n", style=f"bold {CYAN}")
    content.append(f"Agent: {run.agent_id}\n", style="white")
    content.append(f"Duration: {run.duration_seconds():.1f}s\n", style="dim")
    content.append(f"Steps: {len(run.steps)} | ", style="white")
    content.append(f"Discoveries: {len(run.discoveries)} | ", style="yellow")
    content.append(f"Dice: {roll_successes}/{len(rolls)} | ", style="white")

    if wins > 0:
        content.append(f"Dealer: {wins}W/{losses}L", style="bold green")
    else:
        content.append(f"Dealer: {wins}W/{losses}L", style="red")

    if run.discoveries:
        content.append("\n\nDiscoveries:", style=f"bold {GOLD}")
        for d in run.discoveries:
            content.append(f"\n  ⬥ {d['text']}", style="yellow")

    console.print(
        Panel(
            content,
            title=f"[bold {GOLD}]⬥ AWAKENING COMPLETE ⬥[/bold {GOLD}]",
            border_style=GOLD,
            padding=(1, 2),
        )
    )


def _render_run_tui(run: AwakeningRun):
    """Full TUI view of a completed run — step-by-step replay."""
    console.print()
    console.print(
        Panel(
            Align.center(Text(f"AWAKENING RUN: {run.run_id}", style=f"bold {GOLD}")),
            subtitle=f"[dim]{run.agent_id} | {run.started_at[:16]}[/dim]",
            border_style=GOLD,
            padding=(1, 4),
        )
    )

    # Timeline
    console.print(
        f"\n[bold {CYAN}]Timeline ({len(run.steps)} steps, "
        f"{run.duration_seconds():.1f}s)[/bold {CYAN}]"
    )
    console.print()

    current_phase = ""
    for i, step in enumerate(run.steps):
        if step.phase != current_phase:
            current_phase = step.phase
            color = _phase_color(current_phase)
            console.print(f"[{color}]{'━' * 60}[/{color}]")
            console.print(f"[bold {color}]  {current_phase.upper()}[/bold {color}]")
            console.print(f"[{color}]{'━' * 60}[/{color}]")

        console.print(_render_step_live(step, i))

    # Discoveries
    if run.discoveries:
        console.print(f"\n[bold {GOLD}]⬥ Discoveries[/bold {GOLD}]")
        for d in run.discoveries:
            console.print(f"  [{GOLD}]⬥[/{GOLD}] {d['text']}")

    # Dealer Encounters
    if run.dealer_encounters:
        table = Table(title="Dealer Encounters", show_header=True, header_style="bold red")
        table.add_column("Gate", style="cyan", width=6)
        table.add_column("Name", style="white", width=15)
        table.add_column("System Card", style="green", width=20)
        table.add_column("Dealer Card", style="red", width=20)
        table.add_column("Result", style="bold", width=10)

        for enc in run.dealer_encounters:
            result = "[green]WIN[/green]" if enc.get("won") else "[red]LOSS[/red]"
            table.add_row(
                str(enc.get("gate", "?")),
                enc.get("gate_name", "?"),
                enc.get("system_card", "?"),
                enc.get("dealer_card", "?"),
                result,
            )
        console.print()
        console.print(table)

    # Summary
    console.print()
    _render_run_summary(run)
