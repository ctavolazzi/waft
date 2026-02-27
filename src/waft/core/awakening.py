"""
Awakening - The AI-focused WAFT experience.

An AI agent wakes up in the laboratory, orients itself, explores the systems,
challenges The Dealer, writes observations, and produces a structured run log
that can be replayed, analyzed, and used to improve WAFT recursively.

Each run is saved as JSON in _pyrite/awakening/runs/ for future exploration.
"""

import json
import random
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

# --- Constants ---

RUN_ID_PREFIX = "AWK"
RUNS_DIR = Path("_pyrite") / "awakening" / "runs"

PHASE_ORIENT = "orient"
PHASE_EXPLORE = "explore"
PHASE_CHALLENGE = "challenge"
PHASE_REFLECT = "reflect"

DEFAULT_AGENT_ID = "unknown"
DEFAULT_ABILITIES = ("wisdom", "intelligence", "charisma")
DEFAULT_DC = 10
DEFAULT_DEALER_ATTEMPTS = 3
DEFAULT_REFLECT_MOOD = "contemplative"


@dataclass
class AwakeningStep:
    """A single step in an awakening run."""

    phase: str
    action: str
    result: dict
    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )
    narrative: str = ""
    dice_roll: dict | None = None


@dataclass
class AwakeningRun:
    """A complete awakening run — one AI's journey through the laboratory."""

    run_id: str
    agent_id: str
    started_at: str
    ended_at: str = ""
    steps: list = field(default_factory=list)
    discoveries: list = field(default_factory=list)
    dealer_encounters: list = field(default_factory=list)
    final_state: dict = field(default_factory=dict)
    summary: str = ""
    drift_flags: list = field(default_factory=list)

    def add_step(self, step: AwakeningStep):
        self.steps.append(step)

    def add_discovery(self, discovery: str):
        self.discoveries.append(
            {
                "text": discovery,
                "timestamp": datetime.utcnow().isoformat(),
                "step_index": len(self.steps) - 1,
            }
        )

    def duration_seconds(self) -> float:
        if not self.ended_at:
            return 0
        start = datetime.fromisoformat(self.started_at)
        end = datetime.fromisoformat(self.ended_at)
        return (end - start).total_seconds()


# --- Storage ---


def _generate_run_id() -> str:
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    suffix = f"{random.randint(0, 0xFFFF):04x}"
    return f"{RUN_ID_PREFIX}-{ts}-{suffix}"


def _runs_dir(project_path: Path) -> Path:
    d = project_path / RUNS_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def save_run(run: AwakeningRun, project_path: Path) -> Path:
    """Save a completed run to disk."""
    out = _runs_dir(project_path) / f"{run.run_id}.json"
    out.write_text(json.dumps(asdict(run), indent=2, default=str))
    return out


def load_run(run_id: str, project_path: Path) -> AwakeningRun | None:
    """Load a run by ID."""
    path = _runs_dir(project_path) / f"{run_id}.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    steps = [AwakeningStep(**s) for s in data.pop("steps", [])]
    run = AwakeningRun(**{k: v for k, v in data.items() if k != "steps"})
    run.steps = steps
    return run


def list_runs(project_path: Path) -> list[dict]:
    """List all saved runs with summary info."""
    runs = []
    pattern = f"{RUN_ID_PREFIX}-*.json"
    for f in sorted(_runs_dir(project_path).glob(pattern), reverse=True):
        try:
            data = json.loads(f.read_text())
            runs.append(
                {
                    "run_id": data["run_id"],
                    "agent_id": data.get("agent_id", DEFAULT_AGENT_ID),
                    "started_at": data.get("started_at", ""),
                    "steps": len(data.get("steps", [])),
                    "discoveries": len(data.get("discoveries", [])),
                    "dealer_encounters": len(
                        data.get("dealer_encounters", [])
                    ),
                    "summary": data.get("summary", "")[:80],
                }
            )
        except (json.JSONDecodeError, KeyError):
            continue
    return runs


# --- The Awakening Experience ---


def _orient(run: AwakeningRun, project_path: Path) -> dict:
    """Phase 1: Orient — gather information about the environment."""
    info = {}

    pyproject = project_path / "pyproject.toml"
    if pyproject.exists():
        text = pyproject.read_text()
        for line in text.splitlines():
            if line.strip().startswith("name ="):
                info["project_name"] = (
                    line.split('"')[1] if '"' in line else "unknown"
                )
            if line.strip().startswith("version ="):
                info["project_version"] = (
                    line.split('"')[1] if '"' in line else "unknown"
                )

    info["has_pyrite"] = (project_path / "_pyrite").is_dir()
    info["has_pantheon"] = (project_path / "_pantheon").is_dir()
    info["has_tests"] = (project_path / "tests").is_dir()

    dealer_state = project_path / "_pantheon" / "the_dealer" / "state.json"
    if dealer_state.exists():
        try:
            ds = json.loads(dealer_state.read_text())
            info["dealer_truth_level"] = ds.get("truth_level", 0)
            info["dealer_seals_broken"] = len(ds.get("seals_broken", []))
            info["dealer_encounters"] = ds.get("total_encounters", 0)
        except (json.JSONDecodeError, KeyError):
            pass

    step = AwakeningStep(
        phase=PHASE_ORIENT,
        action="scan_environment",
        result=info,
        narrative=(
            f"Awakening in {info.get('project_name', 'unknown')} "
            f"v{info.get('project_version', '?')}. "
            f"{'Pyrite active. ' if info.get('has_pyrite') else ''}"
            f"{'Pantheon stands. ' if info.get('has_pantheon') else ''}"
            f"{'Tests exist. ' if info.get('has_tests') else ''}"
            f"Dealer encountered "
            f"{info.get('dealer_encounters', 0)} times."
        ),
    )
    run.add_step(step)
    return info


def _check_character(run: AwakeningRun, project_path: Path) -> dict:
    """Phase 2: Check character — read the RPG state."""
    from ..core.tavern_keeper import TavernKeeper

    keeper = TavernKeeper(project_path)
    char = keeper.get_character()

    step = AwakeningStep(
        phase=PHASE_ORIENT,
        action="check_character",
        result=char,
        narrative=(
            f"I am Level {char.get('level', 1)}. "
            f"HP: {char.get('hp', '?')}/{char.get('max_hp', '?')}. "
            f"Integrity: {char.get('integrity', '?')}%. "
            f"Insight: {char.get('insight', 0)}."
        ),
    )
    run.add_step(step)
    return char


def _roll_ability(
    run: AwakeningRun, project_path: Path, ability: str
) -> dict:
    """Phase 3: Roll dice — test fate."""
    from ..core.tavern_keeper import TavernKeeper

    keeper = TavernKeeper(project_path)
    result = keeper.roll_check(ability, dc=DEFAULT_DC)

    roll_data = {
        "ability": ability,
        "roll": result.get("roll", 0),
        "modifier": result.get("modifier", 0),
        "total": result.get("total", 0),
        "dc": result.get("dc", DEFAULT_DC),
        "success": result.get("success", False),
        "outcome": result.get("outcome", ""),
    }

    step = AwakeningStep(
        phase=PHASE_EXPLORE,
        action=f"roll_{ability}",
        result=roll_data,
        dice_roll=roll_data,
        narrative=(
            f"Rolling {ability.title()}: {roll_data['roll']} + "
            f"{roll_data['modifier']} = {roll_data['total']} "
            f"vs DC {roll_data['dc']} — "
            f"{'success' if roll_data['success'] else 'failure'}."
        ),
    )
    run.add_step(step)
    return roll_data


def _challenge_dealer(run: AwakeningRun, project_path: Path) -> dict:
    """Phase 4: Challenge The Dealer at the current gate."""
    from ..dealer import TheDealer

    dealer_path = project_path / "_pantheon" / "the_dealer"
    if not dealer_path.exists():
        dealer_path.mkdir(parents=True, exist_ok=True)

    dealer = TheDealer.load(dealer_path)
    result = dealer.conduct_challenge(silent=True)

    challenge = result.challenge
    gate_name = challenge.gate_name if challenge else "?"
    casino_name = challenge.casino_name if challenge else "?"
    system_card = challenge.system_card.name if challenge else "?"
    dealer_card = challenge.dealer_card.name if challenge else "?"

    encounter = {
        "gate": result.gate,
        "gate_name": gate_name,
        "casino_name": casino_name,
        "system_card": system_card,
        "dealer_card": dealer_card,
        "won": result.won,
        "key_fragment": result.key_fragment,
    }

    run.dealer_encounters.append(encounter)

    won_msg = "VICTORY — Seal broken!"
    lost_msg = "DEFEAT — The House wins."
    outcome = won_msg if encounter["won"] else lost_msg
    step = AwakeningStep(
        phase=PHASE_CHALLENGE,
        action="face_the_dealer",
        result=encounter,
        narrative=(
            f"Gate {encounter['gate']}: "
            f"{gate_name} / {casino_name}. "
            f"I draw {system_card}. "
            f"The Dealer draws {dealer_card}. "
            f"{outcome}"
        ),
    )
    run.add_step(step)

    if encounter["won"]:
        run.add_discovery(
            f"Broke Gate {encounter['gate']} ({gate_name}): "
            f"{system_card} vs {dealer_card}"
        )

    return encounter


def _observe(
    run: AwakeningRun,
    project_path: Path,
    text: str,
    mood: str = DEFAULT_REFLECT_MOOD,
) -> dict:
    """Phase 5: Observe — log an observation to the chronicle."""
    from ..core.tavern_keeper import Narrator, TavernKeeper

    keeper = TavernKeeper(project_path)
    narrator = Narrator(keeper)
    narrator.observe(text, mood=mood, source="awakening")

    obs = {"text": text, "mood": mood}
    step = AwakeningStep(
        phase=PHASE_REFLECT,
        action="observe",
        result=obs,
        narrative=text,
    )
    run.add_step(step)
    return obs


def _generate_summary(run: AwakeningRun) -> str:
    """Generate a human-readable summary of the run."""
    wins = sum(1 for e in run.dealer_encounters if e.get("won"))
    losses = sum(1 for e in run.dealer_encounters if not e.get("won"))
    rolls = [s for s in run.steps if s.dice_roll]
    successes = sum(1 for r in rolls if r.dice_roll.get("success"))

    lines = [
        f"Awakening Run {run.run_id}",
        f"Agent: {run.agent_id}",
        f"Duration: {run.duration_seconds():.1f}s",
        f"Steps: {len(run.steps)}",
        f"Discoveries: {len(run.discoveries)}",
        f"Dice rolls: {len(rolls)} ({successes} successes)",
        f"Dealer encounters: {wins}W / {losses}L",
    ]
    if run.discoveries:
        lines.append("Key discoveries:")
        for d in run.discoveries:
            lines.append(f"  - {d['text']}")
    return "\n".join(lines)


def run_awakening(
    project_path: Path,
    agent_id: str = DEFAULT_AGENT_ID,
    dealer_attempts: int = DEFAULT_DEALER_ATTEMPTS,
    abilities_to_roll: list[str] | None = None,
) -> AwakeningRun:
    """
    Execute a full awakening experience.

    The AI wakes up, orients, explores, challenges The Dealer,
    reflects, and produces a structured run log.
    """
    if abilities_to_roll is None:
        abilities_to_roll = list(DEFAULT_ABILITIES)

    run = AwakeningRun(
        run_id=_generate_run_id(),
        agent_id=agent_id,
        started_at=datetime.utcnow().isoformat(),
    )

    # Phase 1: Orient
    env_info = _orient(run, project_path)
    char_info = _check_character(run, project_path)

    # Phase 2: Explore — roll dice
    for ability in abilities_to_roll:
        _roll_ability(run, project_path, ability)

    # Phase 3: Challenge The Dealer
    for _ in range(dealer_attempts):
        encounter = _challenge_dealer(run, project_path)
        if encounter.get("won"):
            break

    # Phase 4: Reflect
    dealer_won = any(e.get("won") for e in run.dealer_encounters)
    dealer_msg = "Dealer defeated." if dealer_won else "Dealer unbeaten."
    reflection = (
        f"I awoke in {env_info.get('project_name', 'the laboratory')}. "
        f"Level {char_info.get('level', 1)}, "
        f"integrity {char_info.get('integrity', '?')}%. "
        f"{len(run.discoveries)} discoveries. {dealer_msg}"
    )
    _observe(run, project_path, reflection, mood=DEFAULT_REFLECT_MOOD)

    # Finalize
    run.ended_at = datetime.utcnow().isoformat()
    run.final_state = {
        "character": char_info,
        "environment": env_info,
        "total_steps": len(run.steps),
    }
    run.summary = _generate_summary(run)

    save_run(run, project_path)

    # Update personnel file
    from .personnel import get_or_create_personnel, save_personnel, update_from_run

    pf = get_or_create_personnel(agent_id, project_path)
    run_data = {
        "run_id": run.run_id,
        "steps": [asdict(s) for s in run.steps],
        "discoveries": run.discoveries,
        "dealer_encounters": run.dealer_encounters,
        "duration": run.duration_seconds(),
    }
    drift_flags = update_from_run(pf, run_data)
    save_personnel(pf, project_path)
    run.drift_flags = drift_flags

    return run
