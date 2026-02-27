"""
Dungeon CLI - Self-playing AI dungeon crawl with animated map display.

Commands:
    waft dungeon           Run a new dungeon crawl (animated)
    waft dungeon run       Run silently (data only)
    waft dungeon replay    Replay a saved run
"""

import time
from pathlib import Path

import typer
from rich.columns import Columns
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..core.dungeon import (
    MAX_TURNS,
    GameState,
    Room,
    _find_path_bfs,
    _pick_target,
    _resolve_encounter,
    generate_dungeon,
    render_map,
    save_dungeon_run,
)

app = typer.Typer(
    name="dungeon",
    help="AI Dungeon Crawl - self-playing D&D dungeon with animated map",
    add_completion=False,
    invoke_without_command=True,
)

# --- Display Constants ---

COLOR_GOLD = "#FFD700"
COLOR_CYAN = "#00FFFF"
COLOR_RED = "#D32F2F"
COLOR_GREEN = "#4CAF50"
COLOR_DIM = "#757575"

ANIMATION_DELAY_MOVE = 0.08
ANIMATION_DELAY_EVENT = 0.6
ANIMATION_DELAY_COMBAT = 0.3

console = Console()


@app.command("stats")
def stats_cmd(
    path: str | None = typer.Option(
        None, "--path", "-p", help="Project path"
    ),
):
    """Show aggregate statistics across all dungeon runs."""
    from ..core.visualize import compute_dungeon_stats

    project_path = Path(path) if path else Path.cwd()
    stats = compute_dungeon_stats(project_path)

    if stats["total_runs"] == 0:
        console.print("[dim]No dungeon runs found.[/dim]")
        return

    table = Table(
        title="⬥ Dungeon Statistics ⬥",
        show_header=False,
        box=None,
        padding=(0, 2),
    )
    table.add_column("Metric", style="white")
    table.add_column("Value", style=COLOR_GOLD, justify="right")

    table.add_row("Total Runs", str(stats["total_runs"]))
    table.add_row(
        "Outcomes",
        f"{stats['escaped']} escaped / "
        f"{stats['died']} died / "
        f"{stats['timeout']} timeout",
    )
    table.add_row("Escape Rate", f"{stats['escape_rate']:.1%}")
    table.add_row("Avg Turns", f"{stats['avg_turns']:.1f}")
    table.add_row(
        "Avg HP on Escape", f"{stats['avg_hp_on_escape']:.1f}"
    )
    table.add_row("Total Gold", str(stats["total_gold"]))
    table.add_row(
        "Total Monsters Slain", str(stats["total_monsters_slain"])
    )
    table.add_row("Unique Seeds", str(stats["unique_seeds"]))
    table.add_row(
        "Dealer",
        f"{stats['dealer_wins']}W / "
        f"{stats['dealer_encounters']} encounters",
    )
    table.add_row("Agents", ", ".join(stats["agents"]))

    console.print()
    console.print(Panel(table, border_style=COLOR_GOLD))
    console.print()


@app.command("viz")
def viz_cmd(
    run_id: str | None = typer.Argument(
        None, help="Run ID to visualize (latest if not given)"
    ),
    path: str | None = typer.Option(
        None, "--path", "-p", help="Project path"
    ),
):
    """Generate animated SVG visualization of a dungeon run."""
    from ..core.dungeon import DUNGEON_RUNS_DIR
    from ..core.visualize import generate_dungeon_svg

    project_path = Path(path) if path else Path.cwd()
    runs_dir = project_path / DUNGEON_RUNS_DIR

    if run_id:
        run_path = runs_dir / f"{run_id}.json"
    else:
        files = sorted(runs_dir.glob("DNG-*.json"), reverse=True)
        if not files:
            console.print("[dim]No dungeon runs found.[/dim]")
            raise typer.Exit(1)
        run_path = files[0]

    if not run_path.exists():
        console.print(f"[red]Run not found: {run_id}[/red]")
        raise typer.Exit(1)

    out = generate_dungeon_svg(run_path, project_path)
    console.print(f"[{COLOR_GREEN}]✓ SVG saved: {out}[/{COLOR_GREEN}]")


@app.command("replay")
def replay_cmd(
    run_id: str | None = typer.Argument(
        None, help="Run ID to replay (latest if not given)"
    ),
    path: str | None = typer.Option(
        None, "--path", "-p", help="Project path"
    ),
    speed: float = typer.Option(
        1.0, "--speed", "-s", help="Playback speed multiplier"
    ),
):
    """Replay a saved dungeon run with animated display."""
    from ..core.dungeon import DUNGEON_RUNS_DIR, generate_dungeon

    project_path = Path(path) if path else Path.cwd()
    runs_dir = project_path / DUNGEON_RUNS_DIR

    if run_id:
        run_path = runs_dir / f"{run_id}.json"
    else:
        files = sorted(runs_dir.glob("DNG-*.json"), reverse=True)
        if not files:
            console.print("[dim]No dungeon runs found.[/dim]")
            raise typer.Exit(1)
        run_path = files[0]

    if not run_path.exists():
        console.print("[red]Run not found.[/red]")
        raise typer.Exit(1)

    import json

    data = json.loads(run_path.read_text())
    seed = data.get("seed", 0)
    events = data.get("events", [])
    agent = data.get("agent_id", "unknown")
    outcome = data.get("outcome", "?")

    grid, rooms = generate_dungeon(seed)
    state = GameState(
        agent_id=agent,
        dungeon_seed=seed,
        rooms_total=len(rooms),
        player_max_hp=data.get("hp_remaining", 20)
        + abs(min(0, data.get("hp_remaining", 0))),
    )

    if rooms:
        sx, sy = rooms[0].center
        state.player_x = sx
        state.player_y = sy
        rooms[0].explored = True

    event_log = [
        f"[{COLOR_CYAN}]REPLAY: {data.get('run_id', '?')}[/{COLOR_CYAN}]"
    ]

    delay = ANIMATION_DELAY_EVENT / speed

    with Live(
        _build_display(grid, rooms, state, event_log),
        console=console,
        refresh_per_second=12,
        transient=True,
    ) as live:
        for evt in events:
            pos = evt.get("position", [0, 0])
            if pos and len(pos) == 2:
                state.player_x = int(pos[0])
                state.player_y = int(pos[1])

            for room in rooms:
                if room.contains(state.player_x, state.player_y):
                    room.explored = True

            etype = evt.get("event_type", "")
            desc = evt.get("description", "")
            colors = {
                "start": COLOR_CYAN,
                "encounter": COLOR_RED,
                "combat_win": COLOR_GREEN,
                "combat_loss": COLOR_RED,
                "treasure": COLOR_GOLD,
                "trap": "#FF6600",
                "dealer": COLOR_GOLD,
                "exit": COLOR_GREEN,
                "death": COLOR_RED,
            }
            color = colors.get(etype, COLOR_DIM)
            event_log.append(f"[{color}]{desc}[/{color}]")

            live.update(_build_display(grid, rooms, state, event_log))
            time.sleep(delay)

    # Show final summary
    console.print()
    console.print(Panel(
        Text(
            f"Replay complete: {outcome.upper()}\n"
            f"Turns: {data.get('turns', 0)} | "
            f"HP: {data.get('hp_remaining', 0)} | "
            f"Gold: {data.get('gold', 0)} | "
            f"Slain: {data.get('monsters_slain', 0)}",
        ),
        title=f"[bold {COLOR_GOLD}]⬥ REPLAY: {data.get('run_id', '?')} ⬥[/bold {COLOR_GOLD}]",
        border_style=COLOR_GOLD,
    ))


@app.command("batch")
def batch_cmd(
    count: int = typer.Option(
        20, "--count", "-n", help="Number of runs"
    ),
    agent_id: str = typer.Option(
        "unknown", "--agent", "-a", help="Agent identifier"
    ),
    path: str | None = typer.Option(
        None, "--path", "-p", help="Project path"
    ),
):
    """Run a batch of dungeons and analyze seed difficulty."""
    from ..core.dungeon import run_dungeon, save_dungeon_run

    project_path = Path(path) if path else Path.cwd()
    import random as _random

    results = []
    console.print(
        f"\n[bold {COLOR_GOLD}]⬥ BATCH RUN: "
        f"{count} dungeons ⬥[/bold {COLOR_GOLD}]\n"
    )

    for _i in range(count):
        seed = _random.randint(0, 99999)
        state = run_dungeon(agent_id, seed=seed, project_path=project_path)
        save_dungeon_run(state, project_path)
        icon = (
            f"[{COLOR_GREEN}]✓[/{COLOR_GREEN}]"
            if state.escaped
            else f"[{COLOR_RED}]✗[/{COLOR_RED}]"
            if not state.alive
            else f"[{COLOR_DIM}]○[/{COLOR_DIM}]"
        )
        console.print(
            f"  {icon} seed {seed:5d} | "
            f"T{state.turn:3d} HP{state.player_hp:3d} "
            f"G{state.player_gold:3d} M{state.monsters_slain}"
        )
        results.append({
            "seed": seed,
            "outcome": "escaped" if state.escaped else (
                "died" if not state.alive else "timeout"
            ),
            "turns": state.turn,
            "hp": state.player_hp,
            "gold": state.player_gold,
            "monsters": state.monsters_slain,
        })

    # Analyze
    escaped = [r for r in results if r["outcome"] == "escaped"]
    died = [r for r in results if r["outcome"] == "died"]

    console.print(
        f"\n[bold]Results: "
        f"[{COLOR_GREEN}]{len(escaped)} escaped[/{COLOR_GREEN}] / "
        f"[{COLOR_RED}]{len(died)} died[/{COLOR_RED}] / "
        f"{count - len(escaped) - len(died)} timeout"
        f"[/bold]"
    )

    if escaped:
        best = min(escaped, key=lambda r: r["turns"])
        richest = max(escaped, key=lambda r: r["gold"])
        console.print(
            f"  Fastest escape: seed {best['seed']} "
            f"(T{best['turns']}, HP{best['hp']})"
        )
        console.print(
            f"  Richest escape: seed {richest['seed']} "
            f"(G{richest['gold']}, T{richest['turns']})"
        )

    if died:
        quickest_death = min(died, key=lambda r: r["turns"])
        longest_fight = max(died, key=lambda r: r["monsters"])
        console.print(
            f"  Quickest death: seed {quickest_death['seed']} "
            f"(T{quickest_death['turns']})"
        )
        console.print(
            f"  Most kills before death: seed {longest_fight['seed']} "
            f"(M{longest_fight['monsters']}, T{longest_fight['turns']})"
        )

    console.print()


@app.command("leaderboard")
def leaderboard_cmd(
    path: str | None = typer.Option(
        None, "--path", "-p", help="Project path"
    ),
    limit: int = typer.Option(
        10, "--limit", "-n", help="Top N entries"
    ),
):
    """Show the all-time dungeon leaderboard by agent."""
    import json

    from ..core.dungeon import DUNGEON_RUNS_DIR

    project_path = Path(path) if path else Path.cwd()
    runs_dir = project_path / DUNGEON_RUNS_DIR

    if not runs_dir.exists():
        console.print("[dim]No dungeon runs found.[/dim]")
        return

    runs = []
    for f in runs_dir.glob("DNG-*.json"):
        try:
            runs.append(json.loads(f.read_text()))
        except (json.JSONDecodeError, KeyError):
            continue

    if not runs:
        console.print("[dim]No dungeon runs found.[/dim]")
        return

    # Agent stats
    agents = {}
    for r in runs:
        aid = r.get("agent_id", "unknown")
        if aid not in agents:
            agents[aid] = {
                "runs": 0,
                "escaped": 0,
                "died": 0,
                "total_gold": 0,
                "total_monsters": 0,
                "total_turns": 0,
                "best_gold": 0,
                "best_seed": 0,
            }
        a = agents[aid]
        a["runs"] += 1
        if r.get("outcome") == "escaped":
            a["escaped"] += 1
        elif r.get("outcome") == "died":
            a["died"] += 1
        a["total_gold"] += r.get("gold", 0)
        a["total_monsters"] += r.get("monsters_slain", 0)
        a["total_turns"] += r.get("turns", 0)
        gold = r.get("gold", 0)
        if gold > a["best_gold"]:
            a["best_gold"] = gold
            a["best_seed"] = r.get("seed", 0)

    # Sort by escape rate then total gold
    sorted_agents = sorted(
        agents.items(),
        key=lambda x: (
            x[1]["escaped"] / max(x[1]["runs"], 1),
            x[1]["total_gold"],
        ),
        reverse=True,
    )

    table = Table(
        title="⬥ Dungeon Leaderboard ⬥",
        show_header=True,
        header_style=f"bold {COLOR_GOLD}",
    )
    table.add_column("#", style=COLOR_DIM, width=3)
    table.add_column("Agent", style=COLOR_CYAN, width=22)
    table.add_column("Runs", style="white", width=5, justify="right")
    table.add_column(
        "Escape %", style=COLOR_GREEN, width=9, justify="right"
    )
    table.add_column(
        "Gold", style=COLOR_GOLD, width=6, justify="right"
    )
    table.add_column(
        "Kills", style=COLOR_RED, width=6, justify="right"
    )
    table.add_column("Best Run", style=COLOR_DIM, width=16)

    for rank, (aid, a) in enumerate(sorted_agents[:limit], 1):
        esc_rate = a["escaped"] / max(a["runs"], 1)
        table.add_row(
            str(rank),
            aid,
            str(a["runs"]),
            f"{esc_rate:.0%}",
            str(a["total_gold"]),
            str(a["total_monsters"]),
            f"seed {a['best_seed']} (G{a['best_gold']})",
        )

    console.print()
    console.print(table)
    console.print()


@app.command("messages")
def messages_cmd(
    seed: int | None = typer.Argument(
        None, help="Filter by dungeon seed"
    ),
    path: str | None = typer.Option(
        None, "--path", "-p", help="Project path"
    ),
    limit: int = typer.Option(20, "--limit", "-n", help="Max messages"),
):
    """View inter-agent messages (dungeon graffiti)."""
    from ..core.datastore import MessageStore

    project_path = Path(path) if path else Path.cwd()
    store = MessageStore(project_path)

    if seed is not None:
        msgs = store.query_by_seed(seed)
        title = f"⬥ Messages for seed {seed} ⬥"
    else:
        msgs = store.query(tag="dungeon", limit=limit)
        title = "⬥ Dungeon Messages ⬥"

    if not msgs:
        console.print("[dim]No messages found.[/dim]")
        return

    table = Table(title=title, show_header=True, header_style="bold")
    table.add_column("Agent", style=COLOR_CYAN, width=20)
    table.add_column("Message", style="white", width=50)
    table.add_column("Time", style=COLOR_DIM, width=12)

    for m in msgs[:limit]:
        ts = m.get("timestamp", "")[:16].replace("T", " ")
        table.add_row(
            m.get("author", "?"),
            m.get("text", "")[:60],
            ts,
        )

    console.print()
    console.print(table)
    console.print(f"\n[dim]{len(msgs)} message(s) total[/dim]")
    console.print()


@app.command("analyze")
def analyze_cmd(
    path: str | None = typer.Option(
        None, "--path", "-p", help="Project path"
    ),
):
    """Mine all dungeon runs for patterns and insights."""
    from ..core.archaeology import analyze

    project_path = Path(path) if path else Path.cwd()
    results = analyze(project_path)

    if results.get("total_runs", 0) == 0:
        console.print("[dim]No dungeon runs to analyze.[/dim]")
        return

    console.print(
        f"\n[bold {COLOR_GOLD}]⬥ DUNGEON ARCHAEOLOGY ⬥[/bold {COLOR_GOLD}]"
    )
    console.print(
        f"[dim]Analyzed {results['total_runs']} runs[/dim]\n"
    )

    for insight in results.get("readable", []):
        console.print(f"  [{COLOR_GOLD}]⬥[/{COLOR_GOLD}] {insight}")

    # Death causes table
    deaths = results.get("death_analysis", {})
    causes = deaths.get("death_causes", {})
    if causes:
        console.print(
            f"\n[bold {COLOR_RED}]Kill Board:[/bold {COLOR_RED}]"
        )
        for monster, kills in sorted(
            causes.items(), key=lambda x: x[1], reverse=True
        ):
            console.print(f"  [{COLOR_RED}]{monster}[/{COLOR_RED}]: {kills} kills")

    # Seed difficulty
    seeds = results.get("seed_difficulty", {})
    deadliest = seeds.get("deadliest_seeds", [])
    if deadliest:
        console.print(
            f"\n[bold {COLOR_RED}]Deadliest Seeds:[/bold {COLOR_RED}]"
        )
        for s in deadliest[:5]:
            console.print(
                f"  seed {s['seed']}: "
                f"{s.get('died', 0)} deaths, "
                f"{s.get('escaped', 0)} escapes"
            )

    console.print(
        "\n[dim]Insights saved to _pyrite/insights/[/dim]\n"
    )


def _hp_bar(hp: int, max_hp: int, width: int = 20) -> str:
    """Render an HP bar with color."""
    frac = hp / max_hp if max_hp else 0
    filled = int(frac * width)
    empty = width - filled
    if frac > 0.6:
        color = COLOR_GREEN
    elif frac > 0.3:
        color = COLOR_GOLD
    else:
        color = COLOR_RED
    return f"[{color}]{'█' * filled}[/{color}][{COLOR_DIM}]{'░' * empty}[/{COLOR_DIM}]"


def _build_hud(state: GameState, event_log: list[str]) -> Panel:
    """Build the HUD panel showing stats and recent events."""
    content = Text()
    content.append(f"  HP: {state.player_hp}/{state.player_max_hp}  ", style="white")
    content.append(_hp_bar(state.player_hp, state.player_max_hp))
    content.append(f"\n  Gold: {state.player_gold}", style=COLOR_GOLD)
    content.append(f"  XP: {state.player_xp}", style=COLOR_CYAN)
    content.append(f"  Level: {state.player_level}", style="white")
    content.append(f"\n  Turn: {state.turn}/{MAX_TURNS}", style=COLOR_DIM)
    content.append(
        f"  Rooms: {state.rooms_explored}/{state.rooms_total}",
        style=COLOR_DIM,
    )
    content.append(
        f"  Slain: {state.monsters_slain}", style=COLOR_RED
    )

    content.append("\n\n  [bold]Event Log:[/bold]")
    for line in event_log[-6:]:
        content.append(f"\n  {line}")

    return Panel(
        content,
        title=f"[bold {COLOR_GOLD}]⬥ {state.agent_id} ⬥[/bold {COLOR_GOLD}]",
        border_style=COLOR_GOLD,
    )


def _build_display(
    grid: list[list[str]],
    rooms: list[Room],
    state: GameState,
    event_log: list[str],
) -> Panel:
    """Build the full display with map + HUD."""
    map_str = render_map(grid, rooms, state, fog=True)
    map_panel = Panel(
        map_str,
        title=f"[bold {COLOR_CYAN}]Dungeon (seed {state.dungeon_seed})[/bold {COLOR_CYAN}]",
        border_style=COLOR_CYAN,
        padding=(0, 0),
    )
    hud = _build_hud(state, event_log)

    outer = Text()
    outer.append(f"\n{map_str}\n")

    return Panel(
        Columns([map_panel, hud], padding=1),
        title=f"[bold {COLOR_GOLD}]⬥ THE DUNGEON ⬥[/bold {COLOR_GOLD}]",
        border_style=COLOR_DIM,
    )


@app.callback()
def main(
    ctx: typer.Context,
    path: str | None = typer.Option(
        None, "--path", "-p", help="Project path"
    ),
    agent_id: str = typer.Option(
        "unknown", "--agent", "-a", help="Agent identifier"
    ),
    seed: int | None = typer.Option(
        None, "--seed", "-s", help="Dungeon seed (random if not set)"
    ),
    animate: bool = typer.Option(
        True, "--animate/--no-animate", help="Show animated display"
    ),
):
    """Run a self-playing dungeon crawl."""
    if ctx.invoked_subcommand is not None:
        return

    import random as _random

    project_path = Path(path) if path else Path.cwd()
    if seed is None:
        seed = _random.randint(0, 999999)

    grid, rooms = generate_dungeon(seed)

    state = GameState(
        agent_id=agent_id,
        dungeon_seed=seed,
        rooms_total=len(rooms),
    )

    if not rooms:
        console.print("[red]Failed to generate dungeon.[/red]")
        raise typer.Exit(1)

    # Place player
    sx, sy = rooms[0].center
    state.player_x = sx
    state.player_y = sy
    rooms[0].explored = True
    rooms[0].cleared = True
    state.rooms_explored = 1
    state.add_event(
        "start",
        f"Entered the dungeon (seed {seed}). {len(rooms)} rooms await.",
    )

    event_log = [f"[{COLOR_CYAN}]Entered the dungeon...[/{COLOR_CYAN}]"]

    # Check prior agent messages
    from ..core.dungeon import _read_seed_messages

    prior = _read_seed_messages(seed, project_path)
    if prior:
        msg = prior[0]["text"][:60]
        event_log.append(
            f"[{COLOR_GOLD}]Intel: {len(prior)} prior message(s). "
            f"{msg}[/{COLOR_GOLD}]"
        )
        state.add_event(
            "intel",
            f"Found {len(prior)} message(s): {msg}",
            total_messages=len(prior),
        )

    if animate:
        _run_animated(grid, rooms, state, event_log, project_path)
    else:
        _run_silent(grid, rooms, state, project_path)

    # Save
    out_path = save_dungeon_run(state, project_path)

    # Post message for future agents
    from ..core.dungeon import _post_run_message

    _post_run_message(state, project_path)

    # Update personnel file
    from ..core.personnel import (
        get_or_create_personnel,
        save_personnel,
    )

    pf = get_or_create_personnel(agent_id, project_path)
    pf.last_seen = __import__("datetime").datetime.utcnow().isoformat()
    save_personnel(pf, project_path)

    if animate:
        _show_summary(state, out_path)


def _run_animated(
    grid: list[list[str]],
    rooms: list[Room],
    state: GameState,
    event_log: list[str],
    project_path: Path,
):
    """Run the dungeon with live animated display."""
    with Live(
        _build_display(grid, rooms, state, event_log),
        console=console,
        refresh_per_second=12,
        transient=True,
    ) as live:
        while state.turn < MAX_TURNS and state.alive and not state.escaped:
            state.turn += 1

            target = _pick_target(rooms, state)
            if target is None:
                event_log.append(f"[{COLOR_DIM}]No target — stuck.[/{COLOR_DIM}]")
                live.update(_build_display(grid, rooms, state, event_log))
                break

            path = _find_path_bfs(
                grid, (state.player_x, state.player_y), target.center
            )
            if not path:
                target.explored = True
                continue

            # Animate movement
            for step_x, step_y in path:
                state.player_x = step_x
                state.player_y = step_y
                live.update(
                    _build_display(grid, rooms, state, event_log)
                )
                time.sleep(ANIMATION_DELAY_MOVE)

            # Explore room
            if not target.explored:
                target.explored = True
                state.rooms_explored += 1

            if target.cleared:
                continue

            # Resolve and animate encounter
            prev_event_count = len(state.events)
            _resolve_encounter(state, target, grid, rooms, project_path)

            for evt in state.events[prev_event_count:]:
                event_log.append(_format_event(evt))

            live.update(_build_display(grid, rooms, state, event_log))
            time.sleep(ANIMATION_DELAY_EVENT)

            if state.player_hp <= 0:
                state.alive = False
                event_log.append(
                    f"[bold {COLOR_RED}]YOU HAVE FALLEN.[/bold {COLOR_RED}]"
                )
                state.add_event("death", "You have fallen in the dungeon.")
                live.update(
                    _build_display(grid, rooms, state, event_log)
                )
                time.sleep(1.0)

        if state.alive and not state.escaped:
            state.add_event("timeout", f"Ran out of turns ({MAX_TURNS}).")

        if state.escaped:
            event_log.append(
                f"[bold {COLOR_GREEN}]ESCAPED![/bold {COLOR_GREEN}]"
            )
            state.add_event(
                "complete",
                f"Escaped! Slain {state.monsters_slain}, "
                f"gold {state.player_gold}.",
            )
            live.update(_build_display(grid, rooms, state, event_log))
            time.sleep(1.0)


def _run_silent(
    grid: list[list[str]],
    rooms: list[Room],
    state: GameState,
    project_path: Path,
):
    """Run without animation."""
    while state.turn < MAX_TURNS and state.alive and not state.escaped:
        state.turn += 1
        target = _pick_target(rooms, state)
        if not target:
            break

        path = _find_path_bfs(
            grid, (state.player_x, state.player_y), target.center
        )
        if not path:
            target.explored = True
            continue

        for step_x, step_y in path:
            state.player_x = step_x
            state.player_y = step_y

        if not target.explored:
            target.explored = True
            state.rooms_explored += 1

        if not target.cleared:
            _resolve_encounter(state, target, grid, rooms, project_path)

        if state.player_hp <= 0:
            state.alive = False
            state.add_event("death", "You have fallen.")

    if state.alive and not state.escaped:
        state.add_event("timeout", f"Ran out of turns ({MAX_TURNS}).")
    if state.escaped:
        state.add_event(
            "complete",
            f"Escaped! Slain {state.monsters_slain}, "
            f"gold {state.player_gold}.",
        )


def _format_event(evt) -> str:
    """Format a GameEvent for the event log."""
    colors = {
        "start": COLOR_CYAN,
        "encounter": COLOR_RED,
        "combat_win": COLOR_GREEN,
        "combat_loss": COLOR_RED,
        "treasure": COLOR_GOLD,
        "trap": "#FF6600",
        "dealer": COLOR_GOLD,
        "dealer_result": COLOR_GOLD,
        "exit": COLOR_GREEN,
        "explore": COLOR_DIM,
        "death": COLOR_RED,
    }
    color = colors.get(evt.event_type, COLOR_DIM)
    return f"[{color}]{evt.description}[/{color}]"


def _show_summary(state: GameState, out_path: Path):
    """Show post-game summary."""
    if state.escaped:
        outcome_text = "ESCAPED"
        outcome_style = f"bold {COLOR_GREEN}"
    elif not state.alive:
        outcome_text = f"DIED (turn {state.turn})"
        outcome_style = f"bold {COLOR_RED}"
    else:
        outcome_text = "TIMEOUT"
        outcome_style = COLOR_DIM

    content = Text()
    content.append("Outcome: ", style="white")
    content.append(f"{outcome_text}\n", style=outcome_style)
    content.append(f"Turns: {state.turn}\n", style="white")
    content.append(
        f"HP: {state.player_hp}/{state.player_max_hp}\n", style="white"
    )
    content.append(f"Gold: {state.player_gold}\n", style=COLOR_GOLD)
    content.append(f"XP: {state.player_xp}\n", style=COLOR_CYAN)
    content.append(
        f"Rooms: {state.rooms_explored}/{state.rooms_total}\n",
        style="white",
    )
    content.append(
        f"Monsters slain: {state.monsters_slain}\n", style=COLOR_RED
    )
    content.append(
        f"Treasures: {state.treasures_found}\n", style=COLOR_GOLD
    )
    content.append(f"Traps: {state.traps_triggered}\n", style="#FF6600")
    if state.dealer_encountered:
        dealer_result = "WON" if state.dealer_won else "LOST"
        content.append(f"Dealer: {dealer_result}\n", style=COLOR_GOLD)

    console.print(
        Panel(
            content,
            title=(
                f"[bold {COLOR_GOLD}]⬥ DUNGEON COMPLETE ⬥"
                f"[/bold {COLOR_GOLD}]"
            ),
            border_style=COLOR_GOLD,
            padding=(1, 2),
        )
    )
    console.print(f"[dim]Run saved: {out_path}[/dim]")
