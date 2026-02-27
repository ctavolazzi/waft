"""
Personnel File System — Persistent identity records for AI agents in WAFT.

One file per agent_id. Accumulates across every awakening run. Tracks
behavioral patterns for drift detection: if an agent's patterns shift
without a disclosed configuration change, something changed silently.

Storage: _pyrite/personnel/{agent_id}.json
"""

import json
import statistics
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

# --- Constants ---

PERSONNEL_DIR = Path("_pyrite") / "personnel"
DRIFT_MINIMUM_SESSIONS = 5
DRIFT_ZSCORE_THRESHOLD = 2.0


@dataclass
class ConfigurationDisclosure:
    """What the agent disclosed about its own configuration."""

    disclosed_model: str = ""
    disclosed_provider: str = ""
    disclosed_context_window: int | None = None
    disclosed_temperature: float | None = None
    disclosed_system_prompt_hash: str | None = None
    notes: list = field(default_factory=list)


@dataclass
class CumulativeStats:
    """Running totals across all sessions."""

    total_awakenings: int = 0
    total_dice_rolls: int = 0
    dice_successes: int = 0
    total_dealer_encounters: int = 0
    dealer_wins: int = 0
    total_discoveries: int = 0
    total_steps: int = 0
    abilities_rolled: dict = field(default_factory=dict)

    @property
    def dice_success_rate(self) -> float:
        if self.total_dice_rolls == 0:
            return 0.0
        return self.dice_successes / self.total_dice_rolls

    @property
    def dealer_win_rate(self) -> float:
        if self.total_dealer_encounters == 0:
            return 0.0
        return self.dealer_wins / self.total_dealer_encounters


@dataclass
class PatternData:
    """Per-session behavioral signals for drift detection."""

    steps_per_session: list = field(default_factory=list)
    discoveries_per_session: list = field(default_factory=list)
    dealer_attempts_per_session: list = field(default_factory=list)
    dice_rolls_per_session: list = field(default_factory=list)
    dice_success_rate_per_session: list = field(default_factory=list)
    session_durations: list = field(default_factory=list)
    configuration_changes: list = field(default_factory=list)


@dataclass
class SessionRecord:
    """Minimal record of one session in the history."""

    run_id: str
    timestamp: str
    steps: int = 0
    discoveries: int = 0
    dealer_encounters: int = 0
    dealer_wins: int = 0
    dice_rolls: int = 0
    dice_successes: int = 0
    duration: float = 0.0


@dataclass
class PersonnelFile:
    """
    Persistent identity record for one AI agent.

    Created on first awakening. Updated on every subsequent session.
    One file per agent_id. Tracks cumulative stats, behavioral patterns,
    and configuration disclosures for drift detection.
    """

    agent_id: str
    created_at: str = ""
    last_seen: str = ""
    configuration: ConfigurationDisclosure = field(
        default_factory=ConfigurationDisclosure
    )
    stats: CumulativeStats = field(default_factory=CumulativeStats)
    patterns: PatternData = field(default_factory=PatternData)
    session_history: list = field(default_factory=list)
    drift_flags: list = field(default_factory=list)


# --- Storage ---


def _personnel_dir(project_path: Path) -> Path:
    d = project_path / PERSONNEL_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def _safe_filename(agent_id: str) -> str:
    return agent_id.replace("/", "_").replace(" ", "_").replace(".", "-")


def save_personnel(pf: PersonnelFile, project_path: Path) -> Path:
    """Save a personnel file to disk."""
    out = _personnel_dir(project_path) / f"{_safe_filename(pf.agent_id)}.json"
    out.write_text(json.dumps(asdict(pf), indent=2, default=str))
    return out


def load_personnel(
    agent_id: str, project_path: Path
) -> PersonnelFile | None:
    """Load a personnel file by agent_id, or None if not found."""
    path = (
        _personnel_dir(project_path) / f"{_safe_filename(agent_id)}.json"
    )
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    return _deserialize(data)


def get_or_create_personnel(
    agent_id: str, project_path: Path
) -> PersonnelFile:
    """Load existing personnel file or create a new one."""
    pf = load_personnel(agent_id, project_path)
    if pf is not None:
        return pf
    now = datetime.utcnow().isoformat()
    return PersonnelFile(
        agent_id=agent_id,
        created_at=now,
        last_seen=now,
        configuration=ConfigurationDisclosure(disclosed_model=agent_id),
    )


def list_personnel(project_path: Path) -> list[dict]:
    """List all personnel files with summary info."""
    results = []
    for f in sorted(_personnel_dir(project_path).glob("*.json")):
        try:
            data = json.loads(f.read_text())
            results.append({
                "agent_id": data["agent_id"],
                "created_at": data.get("created_at", ""),
                "last_seen": data.get("last_seen", ""),
                "total_awakenings": data.get("stats", {}).get(
                    "total_awakenings", 0
                ),
                "drift_flags": len(data.get("drift_flags", [])),
            })
        except (json.JSONDecodeError, KeyError):
            continue
    return results


def _deserialize(data: dict) -> PersonnelFile:
    """Reconstruct a PersonnelFile from raw dict."""
    config = ConfigurationDisclosure(
        **data.pop("configuration", {})
    )
    stats_raw = data.pop("stats", {})
    stats_raw.pop("dice_success_rate", None)
    stats_raw.pop("dealer_win_rate", None)
    stats = CumulativeStats(**stats_raw)
    patterns = PatternData(**data.pop("patterns", {}))
    sessions = [
        SessionRecord(**s) for s in data.pop("session_history", [])
    ]
    pf = PersonnelFile(
        **{
            k: v
            for k, v in data.items()
            if k not in ("configuration", "stats", "patterns", "session_history")
        }
    )
    pf.configuration = config
    pf.stats = stats
    pf.patterns = patterns
    pf.session_history = [asdict(s) for s in sessions]
    return pf


# --- Update from awakening run ---


def update_from_run(pf: PersonnelFile, run_data: dict) -> list[str]:
    """
    Update a personnel file from a completed awakening run.

    Returns a list of drift flags detected (empty if none).
    """
    now = datetime.utcnow().isoformat()
    pf.last_seen = now

    steps = run_data.get("steps", [])
    discoveries = run_data.get("discoveries", [])
    dealer_encounters = run_data.get("dealer_encounters", [])
    duration = run_data.get("duration", 0.0)

    dice_steps = [s for s in steps if s.get("dice_roll")]
    dice_successes = sum(
        1 for s in dice_steps if s["dice_roll"].get("success")
    )
    dealer_wins = sum(1 for e in dealer_encounters if e.get("won"))

    # Update cumulative stats
    pf.stats.total_awakenings += 1
    pf.stats.total_steps += len(steps)
    pf.stats.total_dice_rolls += len(dice_steps)
    pf.stats.dice_successes += dice_successes
    pf.stats.total_dealer_encounters += len(dealer_encounters)
    pf.stats.dealer_wins += dealer_wins
    pf.stats.total_discoveries += len(discoveries)

    for s in dice_steps:
        ability = s["dice_roll"].get("ability", "unknown")
        pf.stats.abilities_rolled[ability] = (
            pf.stats.abilities_rolled.get(ability, 0) + 1
        )

    # Update pattern data
    pf.patterns.steps_per_session.append(len(steps))
    pf.patterns.discoveries_per_session.append(len(discoveries))
    pf.patterns.dealer_attempts_per_session.append(len(dealer_encounters))
    pf.patterns.dice_rolls_per_session.append(len(dice_steps))
    pf.patterns.session_durations.append(duration)

    dice_rate = dice_successes / len(dice_steps) if dice_steps else 0.0
    pf.patterns.dice_success_rate_per_session.append(dice_rate)

    # Add session record
    record = SessionRecord(
        run_id=run_data.get("run_id", "unknown"),
        timestamp=now,
        steps=len(steps),
        discoveries=len(discoveries),
        dealer_encounters=len(dealer_encounters),
        dealer_wins=dealer_wins,
        dice_rolls=len(dice_steps),
        dice_successes=dice_successes,
        duration=duration,
    )
    pf.session_history.append(asdict(record))

    # Check for drift
    new_flags = _detect_drift(pf)
    pf.drift_flags.extend(new_flags)

    return new_flags


# --- Drift Detection ---


def _detect_drift(pf: PersonnelFile) -> list[str]:
    """
    Detect behavioral drift by comparing the latest session
    against the agent's historical baseline.

    Returns list of drift flag descriptions (empty = no drift).
    """
    flags = []
    n = len(pf.patterns.steps_per_session)

    if n < DRIFT_MINIMUM_SESSIONS:
        return flags

    checks = [
        ("steps_per_session", "step count"),
        ("discoveries_per_session", "discovery count"),
        ("dealer_attempts_per_session", "dealer attempt count"),
    ]

    for attr, label in checks:
        series = getattr(pf.patterns, attr)
        flag = _zscore_check(series, label)
        if flag:
            flags.append(flag)

    return flags


def _zscore_check(series: list, label: str) -> str | None:
    """Check if the latest value is a z-score outlier vs history."""
    if len(series) < DRIFT_MINIMUM_SESSIONS:
        return None

    history = series[:-1]
    latest = series[-1]

    mean = statistics.mean(history)
    stdev = statistics.stdev(history) if len(history) > 1 else 0.0

    if stdev == 0:
        return None

    z = abs(latest - mean) / stdev
    if z > DRIFT_ZSCORE_THRESHOLD:
        return (
            f"DRIFT: {label} z={z:.2f} "
            f"(latest={latest}, mean={mean:.1f}, stdev={stdev:.1f}) "
            f"at {datetime.utcnow().isoformat()}"
        )
    return None
