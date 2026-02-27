"""
Visualize — SVG generation for WAFT dungeon runs, awakening timelines,
and personnel comparisons.

Generates animated SVGs with CSS animations that can be embedded in
markdown, viewed in browsers, or committed to the repo as artifacts.

Output: _pyrite/visualizations/
"""

import json
from pathlib import Path

# --- Constants ---

VIZ_DIR = Path("_pyrite") / "visualizations"

# SVG dimensions
DUNGEON_SVG_WIDTH = 720
DUNGEON_SVG_HEIGHT = 400
DUNGEON_CELL_SIZE = 14

TIMELINE_SVG_WIDTH = 800
TIMELINE_SVG_HEIGHT = 300

CHART_SVG_WIDTH = 600
CHART_SVG_HEIGHT = 350

# Color palette
COLOR_WALL = "#333333"
COLOR_FLOOR = "#1a1a2e"
COLOR_CORRIDOR = "#16213e"
COLOR_PLAYER = "#00ff88"
COLOR_MONSTER = "#ff4444"
COLOR_TREASURE = "#ffd700"
COLOR_TRAP = "#ff6600"
COLOR_DEALER = "#ffd700"
COLOR_EXIT = "#00ffff"
COLOR_FOG = "#0a0a0a"
COLOR_BG = "#0d0d0d"
COLOR_TEXT = "#cccccc"
COLOR_ACCENT = "#ffd700"
COLOR_SUCCESS = "#4caf50"
COLOR_FAILURE = "#d32f2f"

PHASE_COLORS = {
    "orient": "#00ffff",
    "explore": "#ffd700",
    "challenge": "#d32f2f",
    "reflect": "#4caf50",
}


def _viz_dir(project_path: Path) -> Path:
    d = project_path / VIZ_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


# --- Animated Dungeon Map SVG ---


def generate_dungeon_svg(
    run_path: Path,
    project_path: Path,
) -> Path:
    """
    Generate an animated SVG showing the dungeon map with
    the agent's path animated step by step.
    """
    data = json.loads(run_path.read_text())
    events = data.get("events", [])
    seed = data.get("seed", 0)

    from .dungeon import generate_dungeon

    grid, rooms = generate_dungeon(seed)
    positions = _extract_positions(events)
    cell = DUNGEON_CELL_SIZE
    w = len(grid[0]) * cell
    h = len(grid) * cell

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {w + 40} {h + 80}" '
        f'width="{DUNGEON_SVG_WIDTH}" height="{DUNGEON_SVG_HEIGHT}">',
        "<style>",
        f"  svg {{ background: {COLOR_BG}; font-family: monospace; }}",
        "  .cell {{ opacity: 0; animation: fadeIn 0.3s forwards; }}",
        "  @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}",
        "  @keyframes pulse {{ 0%,100% {{ r: 4; }} 50% {{ r: 6; }} }}",
        "  .player {{ fill: {COLOR_PLAYER}; animation: pulse 1s infinite; }}",
        "  @keyframes walk {",
    ]

    if positions:
        steps = len(positions)
        for i, (px, py) in enumerate(positions):
            pct = (i / max(steps - 1, 1)) * 100
            svg_parts.append(
                f"    {pct:.1f}% {{ "
                f"cx: {px * cell + cell // 2 + 20}; "
                f"cy: {py * cell + cell // 2 + 60}; }}"
            )

    total_dur = max(len(positions) * 0.15, 2)
    svg_parts.extend([
        "  }",
        f"  .agent {{ animation: walk {total_dur:.1f}s ease-in-out forwards; }}",
        f"  .title {{ fill: {COLOR_ACCENT}; font-size: 14px; font-weight: bold; }}",
        f"  .subtitle {{ fill: {COLOR_TEXT}; font-size: 10px; }}",
        "</style>",
    ])

    # Title
    outcome = data.get("outcome", "?")
    agent = data.get("agent_id", "?")
    svg_parts.append(
        f'<text x="20" y="24" class="title">'
        f"⬥ DUNGEON: seed {seed} — {outcome.upper()}</text>"
    )
    svg_parts.append(
        f'<text x="20" y="42" class="subtitle">'
        f"{agent} | T{data.get('turns', 0)} | "
        f"HP {data.get('hp_remaining', 0)} | "
        f"Slain {data.get('monsters_slain', 0)}</text>"
    )

    # Grid tiles
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            sx = x * cell + 20
            sy = y * cell + 60
            color = _tile_svg_color(tile, x, y, rooms)
            if color:
                delay = (x + y) * 0.01
                svg_parts.append(
                    f'<rect x="{sx}" y="{sy}" '
                    f'width="{cell}" height="{cell}" '
                    f'fill="{color}" class="cell" '
                    f'style="animation-delay: {delay:.2f}s;" />'
                )

    # Encounter markers
    for room in rooms:
        if room.encounter in ("monster", "treasure", "trap", "dealer", "exit"):
            cx, cy = room.center
            sx = cx * cell + cell // 2 + 20
            sy = cy * cell + cell // 2 + 60
            marker_color, marker_char = _encounter_marker(room.encounter)
            svg_parts.append(
                f'<text x="{sx}" y="{sy + 4}" '
                f'fill="{marker_color}" text-anchor="middle" '
                f'font-size="{cell}" font-family="monospace">'
                f"{marker_char}</text>"
            )

    # Animated player dot
    if positions:
        start_x = positions[0][0] * cell + cell // 2 + 20
        start_y = positions[0][1] * cell + cell // 2 + 60
        svg_parts.append(
            f'<circle cx="{start_x}" cy="{start_y}" r="5" '
            f'class="player agent" />'
        )

    # Player path trail
    if len(positions) > 1:
        sx = positions[0][0] * cell + cell // 2 + 20
        sy = positions[0][1] * cell + cell // 2 + 60
        path_d = f"M {sx} {sy}"
        for px, py in positions[1:]:
            path_d += f" L {px * cell + cell // 2 + 20} {py * cell + cell // 2 + 60}"
        svg_parts.append(
            f'<path d="{path_d}" fill="none" '
            f'stroke="{COLOR_PLAYER}" stroke-width="1.5" '
            f'stroke-opacity="0.3" stroke-dasharray="4 2">'
            f'<animate attributeName="stroke-dashoffset" '
            f'from="1000" to="0" dur="{total_dur:.1f}s" />'
            f"</path>"
        )

    svg_parts.append("</svg>")
    svg_text = "\n".join(svg_parts)

    out = _viz_dir(project_path) / f"dungeon_{data.get('run_id', 'unknown')}.svg"
    out.write_text(svg_text)
    return out


def _tile_svg_color(
    tile: str, x: int, y: int, rooms: list
) -> str | None:
    """Map tile to SVG color."""
    if tile == "█":
        return COLOR_WALL
    if tile == "·":
        return COLOR_FLOOR
    if tile == "░":
        return COLOR_CORRIDOR
    if tile == " ":
        return None
    return COLOR_FLOOR


def _encounter_marker(encounter: str) -> tuple[str, str]:
    """Get SVG color and character for an encounter."""
    return {
        "monster": (COLOR_MONSTER, "M"),
        "treasure": (COLOR_TREASURE, "$"),
        "trap": (COLOR_TRAP, "^"),
        "dealer": (COLOR_DEALER, "♦"),
        "exit": (COLOR_EXIT, ">"),
    }.get(encounter, (COLOR_TEXT, "?"))


def _extract_positions(events: list[dict]) -> list[tuple[int, int]]:
    """Extract player positions from event data."""
    positions = []
    for e in events:
        pos = e.get("position")
        if pos and (isinstance(pos, (list, tuple)) and len(pos) == 2):
            px, py = int(pos[0]), int(pos[1])
            if not positions or positions[-1] != (px, py):
                positions.append((px, py))
    return positions


# --- Animated Awakening Timeline SVG ---


def generate_timeline_svg(
    run_path: Path,
    project_path: Path,
) -> Path:
    """
    Generate an animated SVG timeline showing awakening run phases
    with events appearing sequentially.
    """
    data = json.loads(run_path.read_text())
    steps = data.get("steps", [])
    run_id = data.get("run_id", "unknown")
    agent = data.get("agent_id", "unknown")

    w = TIMELINE_SVG_WIDTH
    h = TIMELINE_SVG_HEIGHT
    margin = 60
    usable_w = w - margin * 2

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        "<style>",
        f"  svg {{ background: {COLOR_BG}; font-family: monospace; }}",
        "  .event {{ opacity: 0; animation: appear 0.4s forwards; }}",
        "  @keyframes appear {{ from {{ opacity:0; transform:translateY(5px); }} "
        "to {{ opacity:1; transform:translateY(0); }} }}",
        "  .line {{ stroke-dasharray: 1000; stroke-dashoffset: 1000; "
        f"animation: draw {len(steps) * 0.3}s linear forwards; }}",
        "  @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}",
        "</style>",
    ]

    # Title
    svg_parts.append(
        f'<text x="{margin}" y="28" fill="{COLOR_ACCENT}" '
        f'font-size="14" font-weight="bold">'
        f"⬥ AWAKENING: {run_id}</text>"
    )
    svg_parts.append(
        f'<text x="{margin}" y="44" fill="{COLOR_TEXT}" font-size="10">'
        f"{agent} | {len(steps)} steps</text>"
    )

    # Timeline axis
    axis_y = h - 40
    svg_parts.append(
        f'<line x1="{margin}" y1="{axis_y}" '
        f'x2="{w - margin}" y2="{axis_y}" '
        f'stroke="{COLOR_TEXT}" stroke-width="1" class="line" />'
    )

    if not steps:
        svg_parts.append("</svg>")
        out = _viz_dir(project_path) / f"timeline_{run_id}.svg"
        out.write_text("\n".join(svg_parts))
        return out

    # Plot events
    step_w = usable_w / max(len(steps), 1)
    for i, step in enumerate(steps):
        x = margin + i * step_w + step_w / 2
        phase = step.get("phase", "unknown")
        color = PHASE_COLORS.get(phase, COLOR_TEXT)
        action = step.get("action", "")
        delay = i * 0.3

        # Event dot
        dot_y = axis_y - 20
        dice = step.get("dice_roll")
        if dice:
            dot_y = axis_y - 30 - (20 if dice.get("success") else 0)
            dot_color = COLOR_SUCCESS if dice.get("success") else COLOR_FAILURE
        else:
            dot_color = color

        svg_parts.append(
            f'<circle cx="{x:.1f}" cy="{dot_y}" r="6" '
            f'fill="{dot_color}" class="event" '
            f'style="animation-delay: {delay:.1f}s;" />'
        )

        # Connector to axis
        svg_parts.append(
            f'<line x1="{x:.1f}" y1="{dot_y + 6}" '
            f'x2="{x:.1f}" y2="{axis_y}" '
            f'stroke="{dot_color}" stroke-width="1" '
            f'stroke-opacity="0.4" class="event" '
            f'style="animation-delay: {delay:.1f}s;" />'
        )

        # Label
        label = action.replace("roll_", "").replace("face_the_", "")[:8]
        svg_parts.append(
            f'<text x="{x:.1f}" y="{axis_y + 16}" '
            f'fill="{color}" font-size="8" text-anchor="middle" '
            f'class="event" style="animation-delay: {delay:.1f}s;">'
            f"{label}</text>"
        )

        # Phase label (only on first of each phase)
        if i == 0 or steps[i - 1].get("phase") != phase:
            svg_parts.append(
                f'<text x="{x:.1f}" y="{dot_y - 14}" '
                f'fill="{color}" font-size="9" text-anchor="middle" '
                f'font-weight="bold" class="event" '
                f'style="animation-delay: {delay:.1f}s;">'
                f"{phase.upper()}</text>"
            )

    svg_parts.append("</svg>")
    out = _viz_dir(project_path) / f"timeline_{run_id}.svg"
    out.write_text("\n".join(svg_parts))
    return out


# --- Personnel Comparison Chart SVG ---


def generate_personnel_chart_svg(project_path: Path) -> Path:
    """
    Generate an animated SVG bar chart comparing all agents'
    cumulative stats.
    """
    from .personnel import list_personnel, load_personnel

    agents = list_personnel(project_path)
    if not agents:
        return _empty_svg(project_path, "No agents found")

    w = CHART_SVG_WIDTH
    h = CHART_SVG_HEIGHT
    margin_l = 120
    margin_r = 40
    margin_t = 60
    bar_h = 24
    gap = 8
    usable_w = w - margin_l - margin_r

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        "<style>",
        f"  svg {{ background: {COLOR_BG}; font-family: monospace; }}",
        "  .bar {{ animation: grow 0.8s ease-out forwards; transform-origin: left; }}",
        "  @keyframes grow {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}",
        "  .label {{ opacity: 0; animation: fadeLabel 0.3s forwards; }}",
        "  @keyframes fadeLabel {{ to {{ opacity: 1; }} }}",
        "</style>",
        f'<text x="{margin_l}" y="28" fill="{COLOR_ACCENT}" '
        f'font-size="14" font-weight="bold">'
        f"⬥ PERSONNEL COMPARISON</text>",
        f'<text x="{margin_l}" y="44" fill="{COLOR_TEXT}" font-size="10">'
        f"{len(agents)} agents registered</text>",
    ]

    # Load full personnel data
    agent_data = []
    for a in agents:
        pf = load_personnel(a["agent_id"], project_path)
        if pf:
            agent_data.append(pf)

    if not agent_data:
        svg_parts.append("</svg>")
        out = _viz_dir(project_path) / "personnel_chart.svg"
        out.write_text("\n".join(svg_parts))
        return out

    max_awakenings = max(
        (pf.stats.total_awakenings for pf in agent_data), default=1
    )
    max_awakenings = max(max_awakenings, 1)

    for i, pf in enumerate(agent_data):
        y = margin_t + i * (bar_h + gap)
        delay = i * 0.15
        awk = pf.stats.total_awakenings
        bar_w = (awk / max_awakenings) * usable_w

        drift_count = len(pf.drift_flags)
        bar_color = COLOR_FAILURE if drift_count > 0 else COLOR_SUCCESS

        # Agent name
        svg_parts.append(
            f'<text x="{margin_l - 8}" y="{y + bar_h // 2 + 4}" '
            f'fill="{COLOR_TEXT}" font-size="10" text-anchor="end" '
            f'class="label" style="animation-delay: {delay}s;">'
            f"{pf.agent_id}</text>"
        )

        # Bar
        svg_parts.append(
            f'<rect x="{margin_l}" y="{y}" '
            f'width="{max(bar_w, 2)}" height="{bar_h}" '
            f'fill="{bar_color}" rx="3" class="bar" '
            f'style="animation-delay: {delay}s;" />'
        )

        # Value label
        dice_rate = pf.stats.dice_success_rate
        dealer_rate = pf.stats.dealer_win_rate
        svg_parts.append(
            f'<text x="{margin_l + bar_w + 8}" y="{y + bar_h // 2 + 4}" '
            f'fill="{COLOR_TEXT}" font-size="9" '
            f'class="label" style="animation-delay: {delay + 0.4}s;">'
            f"{awk} runs | "
            f"dice {dice_rate:.0%} | "
            f"dealer {dealer_rate:.0%}"
            f"{'  ⚠ DRIFT' if drift_count else ''}"
            f"</text>"
        )

    svg_parts.append("</svg>")
    out = _viz_dir(project_path) / "personnel_chart.svg"
    out.write_text("\n".join(svg_parts))
    return out


# --- Dungeon Stats Aggregate ---


def compute_dungeon_stats(project_path: Path) -> dict:
    """Compute aggregate statistics across all dungeon runs."""
    from .dungeon import DUNGEON_RUNS_DIR

    runs_dir = project_path / DUNGEON_RUNS_DIR
    if not runs_dir.exists():
        return {"total_runs": 0}

    runs = []
    for f in runs_dir.glob("DNG-*.json"):
        try:
            runs.append(json.loads(f.read_text()))
        except (json.JSONDecodeError, KeyError):
            continue

    if not runs:
        return {"total_runs": 0}

    escaped = [r for r in runs if r.get("outcome") == "escaped"]
    died = [r for r in runs if r.get("outcome") == "died"]
    timeout = [r for r in runs if r.get("outcome") == "timeout"]

    all_turns = [r.get("turns", 0) for r in runs]
    all_hp = [r.get("hp_remaining", 0) for r in escaped]
    all_gold = [r.get("gold", 0) for r in runs]
    all_monsters = [r.get("monsters_slain", 0) for r in runs]
    agents = list({r.get("agent_id", "?") for r in runs})

    return {
        "total_runs": len(runs),
        "escaped": len(escaped),
        "died": len(died),
        "timeout": len(timeout),
        "escape_rate": len(escaped) / len(runs) if runs else 0,
        "avg_turns": sum(all_turns) / len(all_turns) if all_turns else 0,
        "avg_hp_on_escape": (
            sum(all_hp) / len(all_hp) if all_hp else 0
        ),
        "total_gold": sum(all_gold),
        "total_monsters_slain": sum(all_monsters),
        "agents": agents,
        "unique_seeds": len({r.get("seed") for r in runs}),
        "dealer_encounters": sum(
            1 for r in runs if r.get("dealer_encountered")
        ),
        "dealer_wins": sum(1 for r in runs if r.get("dealer_won")),
    }


def _empty_svg(project_path: Path, message: str) -> Path:
    """Generate an empty SVG with a message."""
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 400 100" width="400" height="100">'
        f'<rect width="400" height="100" fill="{COLOR_BG}" />'
        f'<text x="200" y="55" fill="{COLOR_TEXT}" '
        f'font-size="14" text-anchor="middle" '
        f'font-family="monospace">{message}</text>'
        f"</svg>"
    )
    out = _viz_dir(project_path) / "empty.svg"
    out.write_text(svg)
    return out
