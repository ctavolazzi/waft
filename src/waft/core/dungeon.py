"""
Dungeon — Procedural dungeon generation and self-playing AI game engine.

Generates a dungeon with rooms, corridors, monsters, treasures, traps,
and a Dealer encounter. An AI agent autonomously explores the dungeon,
making decisions based on simple heuristics. Every move is logged as
structured data for the awakening/personnel systems.

The game plays itself. You watch.
"""

import json
import random
from collections import deque
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

# --- Constants ---

# Map dimensions
MAP_WIDTH = 48
MAP_HEIGHT = 24
MIN_ROOM_SIZE = 4
MAX_ROOM_SIZE = 9
MAX_ROOMS = 9
CORRIDOR_CHANCE = 0.15

# Tile types
TILE_VOID = " "
TILE_WALL = "█"
TILE_FLOOR = "·"
TILE_CORRIDOR = "░"
TILE_DOOR = "▫"
TILE_PLAYER = "@"
TILE_MONSTER = "M"
TILE_TREASURE = "$"
TILE_TRAP = "^"
TILE_DEALER = "♦"
TILE_EXIT = ">"
TILE_EXPLORED = "."
TILE_FOG = " "

# Game balance
PLAYER_START_HP = 20
PLAYER_START_GOLD = 0
MAX_TURNS = 200
HEAL_ON_TREASURE = 3
TRAP_DAMAGE_MIN = 2
TRAP_DAMAGE_MAX = 6

# Monsters
MONSTER_TABLE = [
    {"name": "Goblin", "hp": 4, "attack": 2, "xp": 10, "glyph": "g"},
    {"name": "Skeleton", "hp": 6, "attack": 3, "xp": 15, "glyph": "s"},
    {"name": "Orc", "hp": 10, "attack": 4, "xp": 25, "glyph": "O"},
    {"name": "Wraith", "hp": 8, "attack": 5, "xp": 30, "glyph": "W"},
    {"name": "Troll", "hp": 14, "attack": 6, "xp": 40, "glyph": "T"},
    {"name": "Dragon", "hp": 20, "attack": 8, "xp": 100, "glyph": "D"},
]

# Encounter distribution per room
ENCOUNTER_WEIGHTS = {
    "empty": 30,
    "monster": 35,
    "treasure": 20,
    "trap": 10,
    "dealer": 5,
}

# AI decision weights
AI_EXPLORE_WEIGHT = 10
AI_FLEE_HP_THRESHOLD = 0.3


# --- Data Structures ---


@dataclass
class Room:
    """A rectangular room in the dungeon."""

    x: int
    y: int
    w: int
    h: int
    encounter: str = "empty"
    encounter_data: dict = field(default_factory=dict)
    explored: bool = False
    cleared: bool = False

    @property
    def center(self) -> tuple[int, int]:
        return (self.x + self.w // 2, self.y + self.h // 2)

    def contains(self, px: int, py: int) -> bool:
        return self.x <= px < self.x + self.w and self.y <= py < self.y + self.h

    def intersects(self, other: "Room") -> bool:
        return (
            self.x < other.x + other.w + 1
            and self.x + self.w + 1 > other.x
            and self.y < other.y + other.h + 1
            and self.y + self.h + 1 > other.y
        )


@dataclass
class GameEvent:
    """A single event in the game log."""

    turn: int
    event_type: str
    description: str
    data: dict = field(default_factory=dict)
    position: tuple[int, int] = (0, 0)


@dataclass
class GameState:
    """Complete state of a dungeon run."""

    agent_id: str
    dungeon_seed: int = 0
    player_x: int = 0
    player_y: int = 0
    player_hp: int = PLAYER_START_HP
    player_max_hp: int = PLAYER_START_HP
    player_gold: int = PLAYER_START_GOLD
    player_xp: int = 0
    player_level: int = 1
    inventory: list = field(default_factory=list)
    turn: int = 0
    alive: bool = True
    escaped: bool = False
    rooms_explored: int = 0
    rooms_total: int = 0
    monsters_slain: int = 0
    traps_triggered: int = 0
    treasures_found: int = 0
    dealer_encountered: bool = False
    dealer_won: bool = False
    events: list = field(default_factory=list)

    def add_event(self, event_type: str, desc: str, **data):
        self.events.append(
            GameEvent(
                turn=self.turn,
                event_type=event_type,
                description=desc,
                data=data,
                position=(self.player_x, self.player_y),
            )
        )

    @property
    def hp_fraction(self) -> float:
        return self.player_hp / self.player_max_hp if self.player_max_hp else 0


# --- Dungeon Generation ---


def generate_dungeon(seed: int | None = None) -> tuple[list[list[str]], list[Room]]:
    """
    Generate a dungeon map with rooms and corridors.

    Returns (grid, rooms) where grid is MAP_HEIGHT x MAP_WIDTH
    and rooms is a list of Room objects.
    """
    if seed is not None:
        random.seed(seed)

    grid = [[TILE_VOID for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
    rooms = []

    for _ in range(MAX_ROOMS * 3):
        if len(rooms) >= MAX_ROOMS:
            break

        w = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
        h = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
        x = random.randint(1, MAP_WIDTH - w - 1)
        y = random.randint(1, MAP_HEIGHT - h - 1)

        room = Room(x=x, y=y, w=w, h=h)
        if any(room.intersects(r) for r in rooms):
            continue

        _carve_room(grid, room)
        if rooms:
            _carve_corridor(grid, rooms[-1].center, room.center)

        rooms.append(room)

    # Place encounters
    if len(rooms) > 2:
        for room in rooms[1:-1]:
            room.encounter, room.encounter_data = _roll_encounter()
        rooms[-1].encounter = "exit"
        rooms[-1].encounter_data = {}

    # Ensure at least one Dealer encounter
    dealer_placed = any(r.encounter == "dealer" for r in rooms)
    if not dealer_placed and len(rooms) > 3:
        mid_room = rooms[len(rooms) // 2]
        if mid_room.encounter not in ("exit",):
            mid_room.encounter = "dealer"
            mid_room.encounter_data = {}

    for room in rooms:
        room.explored = False
        room.cleared = False

    return grid, rooms


def _carve_room(grid: list[list[str]], room: Room):
    """Carve a room into the grid. Preserves existing corridors."""
    for dy in range(room.h):
        for dx in range(room.w):
            gy, gx = room.y + dy, room.x + dx
            if 0 <= gy < MAP_HEIGHT and 0 <= gx < MAP_WIDTH:
                is_edge = (
                    dy == 0 or dy == room.h - 1
                    or dx == 0 or dx == room.w - 1
                )
                if is_edge:
                    if grid[gy][gx] != TILE_CORRIDOR:
                        grid[gy][gx] = TILE_WALL
                else:
                    grid[gy][gx] = TILE_FLOOR


def _carve_corridor(
    grid: list[list[str]],
    start: tuple[int, int],
    end: tuple[int, int],
):
    """Carve an L-shaped corridor between two points."""
    x1, y1 = start
    x2, y2 = end

    if random.random() < 0.5:
        _carve_h(grid, x1, x2, y1)
        _carve_v(grid, y1, y2, x2)
    else:
        _carve_v(grid, y1, y2, x1)
        _carve_h(grid, x1, x2, y2)


def _carve_h(grid: list[list[str]], x1: int, x2: int, y: int):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        if 0 <= y < MAP_HEIGHT and 0 <= x < MAP_WIDTH:
            if grid[y][x] in (TILE_VOID, TILE_WALL):
                grid[y][x] = TILE_CORRIDOR


def _carve_v(grid: list[list[str]], y1: int, y2: int, x: int):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        if 0 <= y < MAP_HEIGHT and 0 <= x < MAP_WIDTH:
            if grid[y][x] in (TILE_VOID, TILE_WALL):
                grid[y][x] = TILE_CORRIDOR


def _roll_encounter() -> tuple[str, dict]:
    """Roll a random encounter for a room."""
    roll = random.randint(1, sum(ENCOUNTER_WEIGHTS.values()))
    cumulative = 0
    for encounter_type, weight in ENCOUNTER_WEIGHTS.items():
        cumulative += weight
        if roll <= cumulative:
            if encounter_type == "monster":
                monster = random.choice(MONSTER_TABLE)
                return "monster", dict(monster)
            if encounter_type == "treasure":
                gold = random.randint(5, 25)
                return "treasure", {"gold": gold}
            if encounter_type == "trap":
                dmg = random.randint(TRAP_DAMAGE_MIN, TRAP_DAMAGE_MAX)
                return "trap", {"damage": dmg}
            return encounter_type, {}
    return "empty", {}


# --- Map Rendering ---


def render_map(
    grid: list[list[str]],
    rooms: list[Room],
    state: GameState,
    fog: bool = True,
) -> str:
    """
    Render the dungeon map as a string with color codes for Rich.

    If fog=True, only show explored rooms and adjacent tiles.
    """
    visible = set()
    if fog:
        _compute_visibility(grid, state.player_x, state.player_y, visible)
        for room in rooms:
            if room.explored:
                for dy in range(room.h):
                    for dx in range(room.w):
                        visible.add((room.x + dx, room.y + dy))

    lines = []
    lines.append("[dim]┌" + "─" * MAP_WIDTH + "┐[/dim]")

    for y in range(MAP_HEIGHT):
        row = "[dim]│[/dim]"
        for x in range(MAP_WIDTH):
            if x == state.player_x and y == state.player_y:
                row += f"[bold green]{TILE_PLAYER}[/bold green]"
            elif fog and (x, y) not in visible:
                row += TILE_FOG
            else:
                tile = grid[y][x]
                row += _colorize_tile(tile, x, y, rooms)
        row += "[dim]│[/dim]"
        lines.append(row)

    lines.append("[dim]└" + "─" * MAP_WIDTH + "┘[/dim]")
    return "\n".join(lines)


def _compute_visibility(
    grid: list[list[str]],
    px: int,
    py: int,
    visible: set,
    radius: int = 5,
):
    """Simple radius-based visibility."""
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            nx, ny = px + dx, py + dy
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                if dx * dx + dy * dy <= radius * radius:
                    visible.add((nx, ny))


def _colorize_tile(
    tile: str, x: int, y: int, rooms: list[Room]
) -> str:
    """Apply Rich color markup to a tile."""
    if tile == TILE_WALL:
        return f"[#555555]{TILE_WALL}[/#555555]"
    if tile == TILE_FLOOR:
        for room in rooms:
            if room.contains(x, y) and not room.cleared:
                if room.encounter == "monster":
                    glyph = room.encounter_data.get("glyph", "M")
                    cx, cy = room.center
                    if x == cx and y == cy:
                        return f"[bold red]{glyph}[/bold red]"
                elif room.encounter == "treasure":
                    cx, cy = room.center
                    if x == cx and y == cy:
                        return f"[bold yellow]{TILE_TREASURE}[/bold yellow]"
                elif room.encounter == "trap":
                    cx, cy = room.center
                    if x == cx and y == cy:
                        return f"[bold magenta]{TILE_TRAP}[/bold magenta]"
                elif room.encounter == "dealer":
                    cx, cy = room.center
                    if x == cx and y == cy:
                        return f"[bold #FFD700]{TILE_DEALER}[/bold #FFD700]"
                elif room.encounter == "exit":
                    cx, cy = room.center
                    if x == cx and y == cy:
                        return f"[bold cyan]{TILE_EXIT}[/bold cyan]"
        return f"[#444444]{TILE_FLOOR}[/#444444]"
    if tile == TILE_CORRIDOR:
        return f"[#333333]{TILE_CORRIDOR}[/#333333]"
    return tile


# --- AI Agent ---


def _find_path_bfs(
    grid: list[list[str]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> list[tuple[int, int]]:
    """BFS pathfinding from start to goal on walkable tiles."""
    queue = deque([(start, [start])])
    visited = {start}
    walkable = {TILE_FLOOR, TILE_CORRIDOR, TILE_DOOR}

    while queue:
        (cx, cy), path = queue.popleft()
        if (cx, cy) == goal:
            return path[1:]

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = cx + dx, cy + dy
            if (
                0 <= nx < MAP_WIDTH
                and 0 <= ny < MAP_HEIGHT
                and (nx, ny) not in visited
                and grid[ny][nx] in walkable
            ):
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))

    return []


def _pick_target(
    rooms: list[Room], state: GameState
) -> Room | None:
    """AI picks the next room to explore. Saves exit for last."""
    unexplored = [r for r in rooms if not r.explored]
    non_exit = [r for r in unexplored if r.encounter != "exit"]

    # If critically low HP, head for exit
    if state.hp_fraction < AI_FLEE_HP_THRESHOLD:
        exit_rooms = [r for r in rooms if r.encounter == "exit"]
        if exit_rooms:
            return exit_rooms[0]

    # Explore non-exit rooms first
    if non_exit:
        return min(
            non_exit,
            key=lambda r: abs(r.center[0] - state.player_x)
            + abs(r.center[1] - state.player_y),
        )

    # All non-exit rooms explored — head for exit
    exit_unexplored = [
        r for r in unexplored if r.encounter == "exit"
    ]
    if exit_unexplored:
        return exit_unexplored[0]

    # Everything explored — try exit even if already visited
    exit_rooms = [r for r in rooms if r.encounter == "exit"]
    if exit_rooms and not state.escaped:
        return exit_rooms[0]

    return None


# --- Combat ---


def _resolve_combat(state: GameState, monster: dict) -> dict:
    """Simple combat: trade blows until one side dies."""
    m_hp = monster["hp"]
    m_atk = monster["attack"]
    m_name = monster["name"]
    rounds = 0
    log = []

    while m_hp > 0 and state.player_hp > 0:
        rounds += 1
        p_roll = random.randint(1, 20)
        p_dmg = max(1, p_roll // 4 + state.player_level)
        m_hp -= p_dmg
        log.append(f"You hit {m_name} for {p_dmg}")

        if m_hp <= 0:
            break

        m_roll = random.randint(1, 20)
        m_dmg = max(1, m_roll // 5 + m_atk // 2)
        state.player_hp -= m_dmg
        log.append(f"{m_name} hits you for {m_dmg}")

    won = m_hp <= 0
    if won:
        state.player_xp += monster.get("xp", 0)
        state.monsters_slain += 1

    return {
        "won": won,
        "rounds": rounds,
        "monster": m_name,
        "log": log,
        "xp_gained": monster.get("xp", 0) if won else 0,
    }


# --- Game Loop ---


def run_dungeon(
    agent_id: str,
    seed: int | None = None,
    project_path: Path | None = None,
) -> GameState:
    """
    Run a complete self-playing dungeon game.

    The AI agent autonomously explores, fights, loots, and either
    escapes or dies. Every action is logged.
    """
    if seed is None:
        seed = random.randint(0, 999999)

    grid, rooms = generate_dungeon(seed)

    state = GameState(
        agent_id=agent_id,
        dungeon_seed=seed,
        rooms_total=len(rooms),
    )

    if not rooms:
        state.add_event("error", "No rooms generated")
        return state

    # Place player in first room
    sx, sy = rooms[0].center
    state.player_x = sx
    state.player_y = sy
    rooms[0].explored = True
    rooms[0].cleared = True
    state.rooms_explored = 1

    state.add_event(
        "start",
        f"Entered the dungeon (seed {seed}). "
        f"{len(rooms)} rooms await.",
        rooms=len(rooms),
        seed=seed,
    )

    # Game loop
    while state.turn < MAX_TURNS and state.alive and not state.escaped:
        state.turn += 1

        target = _pick_target(rooms, state)
        if target is None:
            state.add_event("stuck", "No target room found — wandering.")
            break

        path = _find_path_bfs(
            grid, (state.player_x, state.player_y), target.center
        )
        if not path:
            target.explored = True
            state.add_event(
                "unreachable",
                f"Cannot reach room at {target.center}.",
            )
            continue

        # Move along path
        for step_x, step_y in path:
            state.player_x = step_x
            state.player_y = step_y

        # Arrive at room
        if not target.explored:
            target.explored = True
            state.rooms_explored += 1

        if target.cleared:
            continue

        # Resolve encounter
        _resolve_encounter(state, target, grid, rooms, project_path)

        if state.player_hp <= 0:
            state.alive = False
            state.add_event("death", "You have fallen in the dungeon.")

    if state.alive and not state.escaped:
        state.add_event("timeout", f"Ran out of turns ({MAX_TURNS}).")

    # Final event
    if state.escaped:
        state.add_event(
            "complete",
            f"Escaped the dungeon! "
            f"Slain {state.monsters_slain} monsters, "
            f"found {state.treasures_found} treasures, "
            f"earned {state.player_gold} gold.",
        )
    elif not state.alive:
        state.add_event(
            "complete",
            f"Died on turn {state.turn}. "
            f"Slain {state.monsters_slain} monsters before falling.",
        )

    return state


def _resolve_encounter(
    state: GameState,
    room: Room,
    grid: list[list[str]],
    rooms: list[Room],
    project_path: Path | None,
):
    """Resolve whatever is in the room."""
    enc = room.encounter

    if enc == "empty":
        state.add_event("explore", "An empty room. Dust and silence.")
        room.cleared = True

    elif enc == "monster":
        monster = room.encounter_data
        state.add_event(
            "encounter",
            f"A {monster['name']} lurches from the shadows!",
            monster=monster["name"],
        )
        result = _resolve_combat(state, monster)
        if result["won"]:
            state.add_event(
                "combat_win",
                f"Defeated the {monster['name']}! "
                f"+{result['xp_gained']} XP.",
                **result,
            )
        else:
            state.add_event(
                "combat_loss",
                f"The {monster['name']} was too strong.",
                **result,
            )
        room.cleared = True

    elif enc == "treasure":
        gold = room.encounter_data.get("gold", 10)
        state.player_gold += gold
        state.treasures_found += 1
        heal = min(HEAL_ON_TREASURE, state.player_max_hp - state.player_hp)
        state.player_hp += heal
        state.add_event(
            "treasure",
            f"Found a treasure chest! +{gold} gold, +{heal} HP.",
            gold=gold,
            heal=heal,
        )
        room.cleared = True

    elif enc == "trap":
        dmg = room.encounter_data.get("damage", 3)
        state.player_hp -= dmg
        state.traps_triggered += 1
        state.add_event(
            "trap",
            f"Triggered a trap! -{dmg} HP.",
            damage=dmg,
        )
        room.cleared = True

    elif enc == "dealer":
        state.dealer_encountered = True
        state.add_event(
            "dealer",
            "The air grows cold. Cards flutter from nowhere. "
            "The Dealer has appeared.",
        )
        if project_path:
            from ..dealer import TheDealer

            dealer_path = project_path / "_pantheon" / "the_dealer"
            if dealer_path.exists():
                dealer = TheDealer.load(dealer_path)
                result = dealer.conduct_challenge(silent=True)
                state.dealer_won = result.won
                card_info = {}
                if result.challenge:
                    card_info = {
                        "system_card": result.challenge.system_card.name,
                        "dealer_card": result.challenge.dealer_card.name,
                        "gate": result.gate,
                    }
                won_str = "SEAL BROKEN" if result.won else "THE HOUSE WINS"
                state.add_event(
                    "dealer_result",
                    f"Gate {result.gate}: {won_str}.",
                    won=result.won,
                    **card_info,
                )
        room.cleared = True

    elif enc == "exit":
        state.escaped = True
        state.add_event("exit", "Found the exit! Escaping the dungeon.")
        room.cleared = True

    else:
        room.cleared = True


# --- Persistence ---

DUNGEON_RUNS_DIR = Path("_pyrite") / "dungeon" / "runs"


def save_dungeon_run(state: GameState, project_path: Path) -> Path:
    """Save a dungeon run to disk."""
    d = project_path / DUNGEON_RUNS_DIR
    d.mkdir(parents=True, exist_ok=True)

    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    suffix = f"{random.randint(0, 0xFFFF):04x}"
    run_id = f"DNG-{ts}-{suffix}"

    data = {
        "run_id": run_id,
        "agent_id": state.agent_id,
        "seed": state.dungeon_seed,
        "timestamp": datetime.utcnow().isoformat(),
        "outcome": "escaped" if state.escaped else (
            "died" if not state.alive else "timeout"
        ),
        "turns": state.turn,
        "hp_remaining": state.player_hp,
        "gold": state.player_gold,
        "xp": state.player_xp,
        "rooms_explored": state.rooms_explored,
        "rooms_total": state.rooms_total,
        "monsters_slain": state.monsters_slain,
        "treasures_found": state.treasures_found,
        "traps_triggered": state.traps_triggered,
        "dealer_encountered": state.dealer_encountered,
        "dealer_won": state.dealer_won,
        "events": [asdict(e) for e in state.events],
    }

    out = d / f"{run_id}.json"
    out.write_text(json.dumps(data, indent=2, default=str))
    return out
