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

console = Console()

# --- Display Constants ---

COLOR_GOLD = "#FFD700"
COLOR_CYAN = "#00FFFF"
COLOR_RED = "#D32F2F"
COLOR_GREEN = "#4CAF50"
COLOR_DIM = "#757575"

ANIMATION_DELAY_MOVE = 0.08
ANIMATION_DELAY_EVENT = 0.6
ANIMATION_DELAY_COMBAT = 0.3


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

    if animate:
        _run_animated(grid, rooms, state, event_log, project_path)
    else:
        _run_silent(grid, rooms, state, project_path)

    # Save
    out_path = save_dungeon_run(state, project_path)

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
        outcome = f"[bold {COLOR_GREEN}]ESCAPED[/bold {COLOR_GREEN}]"
    elif not state.alive:
        outcome = f"[bold {COLOR_RED}]DIED (turn {state.turn})[/bold {COLOR_RED}]"
    else:
        outcome = f"[{COLOR_DIM}]TIMEOUT[/{COLOR_DIM}]"

    content = Text()
    content.append("Outcome: ", style="white")
    content.append(f"{outcome}\n")
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
