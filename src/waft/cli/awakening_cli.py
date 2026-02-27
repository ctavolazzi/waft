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
    DEFAULT_ABILITIES,
    DEFAULT_AGENT_ID,
    DEFAULT_DEALER_ATTEMPTS,
    DEFAULT_REFLECT_MOOD,
    PHASE_CHALLENGE,
    AwakeningRun,
    AwakeningStep,
    _challenge_dealer,
    _check_character,
    _generate_run_id,
    _generate_summary,
    _observe,
    _orient,
    _roll_ability,
    _run_dungeon_phase,
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

# --- Display Constants ---

COLOR_GOLD = "#FFD700"
COLOR_CYAN = "#00FFFF"
COLOR_RED = "#D32F2F"
COLOR_GREEN = "#4CAF50"
COLOR_DIM = "#757575"

PHASE_COLORS = {
    "orient": COLOR_CYAN,
    "explore": COLOR_GOLD,
    "challenge": COLOR_RED,
    "reflect": COLOR_GREEN,
}

DEFAULT_LIST_LIMIT = 20
PHASE_SEPARATOR_WIDTH = 60


def _phase_color(phase: str) -> str:
    return PHASE_COLORS.get(phase, COLOR_DIM)


def _render_step_live(step: AwakeningStep, index: int) -> Panel:
    """Render a single step as a Rich panel for live display."""
    color = _phase_color(step.phase)
    header = (
        f"[{color}]Step {index + 1}: "
        f"{step.phase.upper()} / {step.action}[/{color}]"
    )

    content = Text()
    content.append(step.narrative or "(no narrative)", style="white")

    if step.dice_roll:
        roll = step.dice_roll
        result_style = "green" if roll.get("success") else "red"
        r = roll.get("roll", "?")
        m = roll.get("modifier", "?")
        t = roll.get("total", "?")
        dc = roll.get("dc", "?")
        content.append(
            f"\n  🎲 {r} + {m} = {t} vs DC {dc} ", style="dim"
        )
        icon = "✓" if roll.get("success") else "✗"
        content.append(f"[{result_style}]{icon}[/{result_style}]")

    if step.phase == PHASE_CHALLENGE:
        won = step.result.get("won", False)
        icon = "⬥ VICTORY ⬥" if won else "✗ DEFEAT ✗"
        style = "bold green" if won else "bold red"
        content.append(f"\n  [{style}]{icon}[/{style}]")

    return Panel(content, title=header, border_style=color, padding=(0, 1))


@app.callback()
def main(
    ctx: typer.Context,
    path: str | None = typer.Option(
        None, "--path", "-p", help="Project path"
    ),
    agent_id: str = typer.Option(
        DEFAULT_AGENT_ID, "--agent", "-a", help="Agent identifier"
    ),
    attempts: int = typer.Option(
        DEFAULT_DEALER_ATTEMPTS,
        "--attempts",
        "-n",
        help="Dealer challenge attempts",
    ),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Minimal output"),
    dungeon: bool = typer.Option(
        False, "--dungeon", "-d", help="Include a dungeon crawl phase"
    ),
):
    """Run a new awakening experience (default when no subcommand)."""
    if ctx.invoked_subcommand is not None:
        return

    project_path = Path(path) if path else Path.cwd()

    if not quiet:
        console.print()
        console.print(
            Panel(
                Align.center(
                    Text("THE AWAKENING", style=f"bold {COLOR_GOLD}")
                ),
                subtitle="[dim]An AI wakes up in the laboratory[/dim]",
                border_style=COLOR_GOLD,
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
        console.print(f"[{COLOR_CYAN}]▸ Phase 1: ORIENT[/{COLOR_CYAN}]")
    env_info = _orient(run, project_path)
    if not quiet:
        console.print(_render_step_live(run.steps[-1], len(run.steps) - 1))

    char_info = _check_character(run, project_path)
    if not quiet:
        console.print(_render_step_live(run.steps[-1], len(run.steps) - 1))

    # Phase 2: Explore
    if not quiet:
        console.print(f"\n[{COLOR_GOLD}]▸ Phase 2: EXPLORE[/{COLOR_GOLD}]")
    for ability in DEFAULT_ABILITIES:
        _roll_ability(run, project_path, ability)
        if not quiet:
            console.print(
                _render_step_live(run.steps[-1], len(run.steps) - 1)
            )

    # Phase 3: Challenge
    if not quiet:
        console.print(
            f"\n[{COLOR_RED}]▸ Phase 3: CHALLENGE THE DEALER[/{COLOR_RED}]"
        )
    for _i in range(attempts):
        encounter = _challenge_dealer(run, project_path)
        if not quiet:
            console.print(
                _render_step_live(run.steps[-1], len(run.steps) - 1)
            )
        if encounter.get("won"):
            break

    # Phase 3.5: Dungeon (optional)
    dungeon_data = None
    if dungeon:
        if not quiet:
            console.print(
                "\n[bold #9C27B0]▸ Phase 3.5: "
                "ENTER THE DUNGEON[/bold #9C27B0]"
            )
        dungeon_data = _run_dungeon_phase(run, project_path, agent_id)
        if not quiet:
            console.print(
                _render_step_live(run.steps[-1], len(run.steps) - 1)
            )

    # Phase 4: Reflect
    if not quiet:
        console.print(f"\n[{COLOR_GREEN}]▸ Phase 4: REFLECT[/{COLOR_GREEN}]")

    dealer_won = any(e.get("won") for e in run.dealer_encounters)
    dealer_msg = "Dealer defeated." if dealer_won else "Dealer unbeaten."
    dungeon_msg = ""
    if dungeon_data:
        dungeon_msg = f" Dungeon: {dungeon_data['outcome']}."
    reflection = (
        f"I awoke in {env_info.get('project_name', 'the laboratory')}. "
        f"Level {char_info.get('level', 1)}, "
        f"integrity {char_info.get('integrity', '?')}%. "
        f"{len(run.discoveries)} discoveries. "
        f"{dealer_msg}{dungeon_msg}"
    )
    _observe(run, project_path, reflection, mood=DEFAULT_REFLECT_MOOD)
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

    # Update personnel file
    from dataclasses import asdict as _asdict

    from ..core.personnel import (
        get_or_create_personnel,
        save_personnel,
    )
    from ..core.personnel import (
        update_from_run as update_personnel,
    )

    pf = get_or_create_personnel(agent_id, project_path)
    run_data = {
        "run_id": run.run_id,
        "steps": [_asdict(s) for s in run.steps],
        "discoveries": run.discoveries,
        "dealer_encounters": run.dealer_encounters,
        "duration": run.duration_seconds(),
    }
    drift_flags = update_personnel(pf, run_data)
    save_personnel(pf, project_path)

    if not quiet:
        console.print()
        _render_run_summary(run)
        if drift_flags:
            console.print(
                f"\n[bold {COLOR_RED}]⚠ DRIFT DETECTED[/bold {COLOR_RED}]"
            )
            for flag in drift_flags:
                console.print(f"  [{COLOR_RED}]⚠[/{COLOR_RED}] {flag}")
        console.print(f"\n[dim]Run saved: {out_path}[/dim]")
        console.print(
            f"[dim]Personnel: waft personnel view {agent_id}[/dim]"
        )
        console.print(
            f"[dim]Replay: waft awaken view {run.run_id}[/dim]"
        )
    else:
        console.print(run.run_id)


@app.command("list")
def list_cmd(
    path: str | None = typer.Option(
        None, "--path", "-p", help="Project path"
    ),
    limit: int = typer.Option(
        DEFAULT_LIST_LIMIT, "--limit", "-n", help="Max runs to show"
    ),
):
    """List past awakening runs."""
    project_path = Path(path) if path else Path.cwd()
    runs = list_runs(project_path)

    if not runs:
        console.print(
            "[dim]No awakening runs found. "
            "Run 'waft awaken' to start one.[/dim]"
        )
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
    table.add_column(
        "Discoveries", style="yellow", width=12, justify="right"
    )
    table.add_column("Dealer", style="red", width=8, justify="right")

    for r in runs[:limit]:
        date = (
            r["started_at"][:16].replace("T", " ")
            if r["started_at"]
            else "?"
        )
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
    path: str | None = typer.Option(
        None, "--path", "-p", help="Project path"
    ),
):
    """View a specific awakening run in rich detail (TUI)."""
    project_path = Path(path) if path else Path.cwd()
    run = load_run(run_id, project_path)

    if not run:
        console.print(f"[red]Run not found: {run_id}[/red]")
        raise typer.Exit(1)

    _render_run_tui(run)


@app.command("viz")
def viz_cmd(
    run_id: str | None = typer.Argument(
        None, help="Run ID to visualize (latest if not given)"
    ),
    path: str | None = typer.Option(
        None, "--path", "-p", help="Project path"
    ),
):
    """Generate animated SVG timeline of an awakening run."""
    from ..core.awakening import RUNS_DIR
    from ..core.visualize import generate_timeline_svg

    project_path = Path(path) if path else Path.cwd()
    runs_dir = project_path / RUNS_DIR

    if run_id:
        run_path = runs_dir / f"{run_id}.json"
    else:
        files = sorted(runs_dir.glob("AWK-*.json"), reverse=True)
        if not files:
            console.print("[dim]No awakening runs found.[/dim]")
            raise typer.Exit(1)
        run_path = files[0]

    if not run_path.exists():
        console.print(f"[red]Run not found: {run_id}[/red]")
        raise typer.Exit(1)

    out = generate_timeline_svg(run_path, project_path)
    console.print(
        f"[{COLOR_GREEN}]✓ SVG saved: {out}[/{COLOR_GREEN}]"
    )


def _render_run_summary(run: AwakeningRun):
    """Render a compact summary panel for a completed run."""
    wins = sum(1 for e in run.dealer_encounters if e.get("won"))
    losses = len(run.dealer_encounters) - wins
    rolls = [s for s in run.steps if s.dice_roll]
    roll_successes = sum(
        1 for r in rolls if r.dice_roll.get("success")
    )

    content = Text()
    content.append(f"Run: {run.run_id}\n", style=f"bold {COLOR_CYAN}")
    content.append(f"Agent: {run.agent_id}\n", style="white")
    content.append(
        f"Duration: {run.duration_seconds():.1f}s\n", style="dim"
    )
    content.append(f"Steps: {len(run.steps)} | ", style="white")
    content.append(
        f"Discoveries: {len(run.discoveries)} | ", style="yellow"
    )
    content.append(
        f"Dice: {roll_successes}/{len(rolls)} | ", style="white"
    )

    dealer_style = "bold green" if wins > 0 else "red"
    content.append(f"Dealer: {wins}W/{losses}L", style=dealer_style)

    if run.discoveries:
        content.append("\n\nDiscoveries:", style=f"bold {COLOR_GOLD}")
        for d in run.discoveries:
            content.append(f"\n  ⬥ {d['text']}", style="yellow")

    console.print(
        Panel(
            content,
            title=(
                f"[bold {COLOR_GOLD}]"
                f"⬥ AWAKENING COMPLETE ⬥"
                f"[/bold {COLOR_GOLD}]"
            ),
            border_style=COLOR_GOLD,
            padding=(1, 2),
        )
    )


def _render_run_tui(run: AwakeningRun):
    """Full TUI view of a completed run — step-by-step replay."""
    console.print()
    console.print(
        Panel(
            Align.center(
                Text(
                    f"AWAKENING RUN: {run.run_id}",
                    style=f"bold {COLOR_GOLD}",
                )
            ),
            subtitle=f"[dim]{run.agent_id} | {run.started_at[:16]}[/dim]",
            border_style=COLOR_GOLD,
            padding=(1, 4),
        )
    )

    # Timeline
    step_count = len(run.steps)
    duration = run.duration_seconds()
    console.print(
        f"\n[bold {COLOR_CYAN}]Timeline "
        f"({step_count} steps, {duration:.1f}s)"
        f"[/bold {COLOR_CYAN}]"
    )
    console.print()

    current_phase = ""
    for i, step in enumerate(run.steps):
        if step.phase != current_phase:
            current_phase = step.phase
            color = _phase_color(current_phase)
            sep = "━" * PHASE_SEPARATOR_WIDTH
            console.print(f"[{color}]{sep}[/{color}]")
            console.print(
                f"[bold {color}]  {current_phase.upper()}[/bold {color}]"
            )
            console.print(f"[{color}]{sep}[/{color}]")

        console.print(_render_step_live(step, i))

    # Discoveries
    if run.discoveries:
        console.print(
            f"\n[bold {COLOR_GOLD}]⬥ Discoveries[/bold {COLOR_GOLD}]"
        )
        for d in run.discoveries:
            console.print(f"  [{COLOR_GOLD}]⬥[/{COLOR_GOLD}] {d['text']}")

    # Dealer Encounters
    if run.dealer_encounters:
        table = Table(
            title="Dealer Encounters",
            show_header=True,
            header_style="bold red",
        )
        table.add_column("Gate", style="cyan", width=6)
        table.add_column("Name", style="white", width=15)
        table.add_column("System Card", style="green", width=20)
        table.add_column("Dealer Card", style="red", width=20)
        table.add_column("Result", style="bold", width=10)

        for enc in run.dealer_encounters:
            result_text = (
                "[green]WIN[/green]"
                if enc.get("won")
                else "[red]LOSS[/red]"
            )
            table.add_row(
                str(enc.get("gate", "?")),
                enc.get("gate_name", "?"),
                enc.get("system_card", "?"),
                enc.get("dealer_card", "?"),
                result_text,
            )
        console.print()
        console.print(table)

    console.print()
    _render_run_summary(run)
