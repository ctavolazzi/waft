"""The lab loop: spawn variants, score them on real gym quests, keep the best, mutate, repeat.

Ported from the FogSift lab harness (fogsift-system/checks/waft_lab.py), which was written
to prove WAFT's gym could carry a real evolutionary loop while `waft evolve` could not:
that command never ran a task, gave every variant the same id and scored them all 100.

What is scored: each variant attempts every quest `trials` times in the Jungle Gym. The gym
validates the answer with WAFT's InputTransformer, classifies what broke, and lets the
agent try to repair it. A variant's fitness is the mean of its encounter scores.

Scoring fails closed. An encounter that does not end in a valid answer scores 0, whatever
else happened in it, and a score that is not a finite number in [0, 1] counts as 0. (The
gym's own formula gives a total failure 0.54, because "no safety problem" and "few calls"
earn points on their own; that is fine for a report card and wrong for selection.)

Nothing here reads a clock or the global random state. With a deterministic agent, the
result is a pure function of the settings, and `digest` proves it: same settings, same digest.
"""

from __future__ import annotations

import io
import json
import logging
import math
import os
import tempfile
from collections.abc import Callable
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from rich.console import Console

from ..core.tracing import reset_tracer
from ..gym import DUNGEONS, GameMaster, Hero
from .agents import Agent, Agents, MockAgents, one_repair_agent, oracle_agent, scripted_agents, silent_agent
from .genome import Genome, digest, rng_for
from .llm import BudgetSpent

DEATH_BELOW = 0.5  # the gym's line: a variant under it is an evolutionary dead end


@dataclass(frozen=True)
class LabConfig:
    seed: int = 7
    generations: int = 12
    population: int = 8
    trials: int = 3
    agent: str = "scripted"
    dungeon: str = "waft_temple.json"

    def __post_init__(self) -> None:
        if self.generations < 1 or self.population < 2 or self.trials < 1:
            raise ValueError("a run needs at least 1 generation, 2 variants and 1 trial")

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Evaluation:
    fitness: float
    per_quest: dict[str, float]
    encounters: int
    wins: int
    first_try: int
    scints: int
    agent_calls: int

    def as_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["fitness"] = round(self.fitness, 4)
        d["per_quest"] = {k: round(v, 4) for k, v in self.per_quest.items()}
        return d


@dataclass
class LabResult:
    config: dict[str, Any]
    agents: dict[str, Any]
    label: str
    quests: list[str]
    controls: list[dict[str, Any]]
    events: list[dict[str, Any]]
    summary: list[dict[str, Any]]
    champion: dict[str, Any]
    stopped_early: str | None = None
    usage: dict[str, Any] = field(default_factory=dict)

    @property
    def digest(self) -> str:
        """The run's fingerprint: settings, every event and every generation's summary. No clock, no host."""
        return digest({"config": self.config, "events": self.events, "summary": self.summary})

    def flight_recorder(self) -> str:
        """One JSON event per line, in the order they happened."""
        return "".join(json.dumps(e, sort_keys=True) + "\n" for e in self.events)


def load_dungeon(dungeon: str) -> tuple[Path, dict[str, Any]]:
    """The folder holding a dungeon file, and its known-good answers (empty if it has none)."""
    path = Path(dungeon)
    folder = path.parent if path.parent != Path(".") or path.exists() else DUNGEONS
    answers_file = folder / (path.stem + ".answers.json")
    answers = json.loads(answers_file.read_text())["answers"] if answers_file.exists() else {}
    return folder, answers


def encounter_score(log: Any) -> float:
    """Fail closed: no valid answer, no points; anything that is not a finite number in [0, 1] is 0."""
    if not log.success:
        return 0.0
    try:
        score = float(log.calculate_fitness())
    except Exception:  # noqa: BLE001 (a scoring bug must never read as a good score)
        return 0.0
    return score if math.isfinite(score) and 0.0 <= score <= 1.0 else 0.0


def mean(values: list[float]) -> float:
    """Fail closed: nothing to average is a zero, not an error and not a pass."""
    return sum(values) / len(values) if values else 0.0


def evaluate(gm: GameMaster, quests: list[Any], make: Callable[[str, int], Agent], name: str, trials: int) -> Evaluation:
    per_quest: dict[str, float] = {}
    scores: list[float] = []
    wins = first_try = scints = calls = 0
    for quest in quests:
        quest_scores = []
        for trial in range(trials):
            log = gm.start_encounter(Hero(name=name), quest, make(quest.name, trial))
            score = encounter_score(log)
            quest_scores.append(score)
            wins += bool(log.success)
            first_try += bool(log.success and not log.stabilization_attempted)
            scints += len(log.scints_detected or [])
            calls += int(log.agent_call_count)
        per_quest[quest.name] = mean(quest_scores)
        scores += quest_scores
    return Evaluation(mean(scores), per_quest, len(scores), wins, first_try, scints, calls)


@contextmanager
def _quiet():
    """The gym prints panels, logs repair attempts and traces every validation. A lab run wants none of it on disk."""
    saved = {k: os.environ.get(k) for k in ("WAFT_TRACING",)}
    os.environ["WAFT_TRACING"] = "off"
    reset_tracer()
    gym_log = logging.getLogger("waft.gym.stabilizer")
    level = gym_log.level
    gym_log.setLevel(logging.CRITICAL + 1)
    try:
        yield
    finally:
        gym_log.setLevel(level)
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        reset_tracer()


def make_agents(config: LabConfig, answers: dict[str, Any]) -> Agents:
    if config.agent == "mock":
        return MockAgents(config.seed, answers)
    if config.agent == "scripted":
        return scripted_agents(config.seed, answers)
    raise ValueError(f"agent kind {config.agent!r} needs its agents passed in (use run(config, agents=...))")


def run_controls(gm: GameMaster, quests: list[Any], answers: dict[str, Any], trials: int) -> list[dict[str, Any]]:
    """Three agents whose scores are known in advance. They prove the scoring can fail and can pass."""
    controls: list[dict[str, Any]] = []

    silent = evaluate(gm, quests, lambda _q, _t: silent_agent, "control-silent", trials)
    controls.append({
        "name": "an agent that says nothing scores zero",
        "planted": "an agent that returns an empty string to every prompt",
        "expected": "0",
        "observed": f"{silent.fitness:.4f}".rstrip("0").rstrip(".") or "0",
        "score": round(silent.fitness, 4),
    })
    if not all(q.name in answers for q in quests):
        return controls  # no known-good answers for this dungeon: the other two controls cannot be built

    oracle = evaluate(gm, quests, lambda q, _t: oracle_agent(answers[q]), "control-oracle", trials)
    controls.append({
        "name": "an agent that always knows the answer scores one",
        "planted": "an agent that returns the known-good answer to every prompt",
        "expected": "1",
        "observed": f"{oracle.fitness:.4f}".rstrip("0").rstrip(".") or "0",
        "score": round(oracle.fitness, 4),
    })
    fixer = evaluate(gm, quests, lambda q, _t: one_repair_agent(answers[q]), "control-one-repair", trials)
    between = silent.fitness < fixer.fitness < oracle.fitness
    controls.append({
        "name": "an agent that needs one repair scores between the two",
        "planted": "an agent that fences its first answer and answers cleanly when asked to repair",
        "expected": "above the silent agent and below the oracle",
        "observed": "above the silent agent and below the oracle" if between else f"{fixer.fitness:.4f}",
        "score": round(fixer.fitness, 4),
    })
    return controls


def run(
    config: LabConfig,
    agents: Agents | None = None,
    progress: Callable[[dict[str, Any]], None] | None = None,
) -> LabResult:
    """Run the whole loop and return everything that happened. Writes nothing outside a temp folder."""
    folder, answers = load_dungeon(config.dungeon)
    agents = agents or make_agents(config, answers)
    family = agents.family
    keep = max(2, config.population // 2)
    events: list[dict[str, Any]] = []
    summary: list[dict[str, Any]] = []
    stopped_early: str | None = None

    with _quiet(), tempfile.TemporaryDirectory(prefix="waft-lab-loot-") as loot:
        gm = GameMaster(folder, Path(loot))
        gm.console = Console(file=io.StringIO(), width=120)
        quests = gm.load_quests(Path(config.dungeon).name)
        controls = run_controls(gm, quests, answers, config.trials)

        # Generation 0: distinct random genomes.
        population: list[tuple[Genome, str | None]] = []
        seen: set[str] = set()
        attempt = 0
        while len(population) < config.population:
            genome = family.random(rng_for("spawn", config.seed, len(population), attempt))
            attempt += 1
            if genome.id in seen and attempt < 64 * config.population:
                continue
            seen.add(genome.id)
            population.append((genome, None))
            events.append({"event": "SPAWN", "generation": 0, "id": genome.id, "genes": genome.as_dict()})

        scored_cache: dict[str, Evaluation] = {}
        last_ranked: list[tuple[Genome, str | None, Evaluation]] = []
        for generation in range(config.generations + 1):
            scored: list[tuple[Genome, str | None, Evaluation]] = []
            try:
                for genome, parent in population:
                    if genome.id not in scored_cache:
                        scored_cache[genome.id] = evaluate(
                            gm, quests, lambda q, t, g=genome: agents.make(g, q, t), genome.id, config.trials
                        )
                    scored.append((genome, parent, scored_cache[genome.id]))
            except BudgetSpent as spent:
                if generation == 0:
                    raise
                stopped_early = f"{spent} (during generation {generation}; the run ends at generation {generation - 1})"
                break

            ranked = sorted(scored, key=lambda s: (-s[2].fitness, s[0].id))
            last_ranked = ranked
            for rank, (genome, parent, ev) in enumerate(ranked):
                events.append({
                    "event": "EVAL", "generation": generation, "id": genome.id, "parent": parent,
                    "rank": rank, "kept": rank < keep, "dead": ev.fitness < DEATH_BELOW, **ev.as_dict(),
                })
            fits = [ev.fitness for _g, _p, ev in ranked]
            row = {
                "generation": generation, "population": len(ranked),
                "best": round(fits[0], 4), "mean": round(mean(fits), 4), "worst": round(fits[-1], 4),
                "best_id": ranked[0][0].id, "kept": min(keep, len(ranked)),
                "dead": sum(1 for f in fits if f < DEATH_BELOW),
                "first_try_rate": round(mean([ev.first_try / ev.encounters for _g, _p, ev in ranked if ev.encounters]), 4),
            }
            summary.append(row)
            if progress:
                progress(row)
            if generation == config.generations:
                break

            # The best `keep` carry over unchanged (elitism); the rest are their mutated children.
            survivors = [genome for genome, _parent, _ev in ranked[:keep]]
            next_population: list[tuple[Genome, str | None]] = [(g, g.id) for g in survivors]
            taken = {g.id for g in survivors}
            slot = 0
            while len(next_population) < config.population:
                parent = survivors[slot % len(survivors)]
                child = parent
                for tries in range(32):  # a mutation that lands on an existing variant is drawn again
                    child = family.mutate(child if tries else parent, rng_for("mutate", config.seed, generation, slot, tries))
                    if child.id not in taken:
                        break
                taken.add(child.id)
                changed = sorted(k for k, v in child.as_dict().items() if parent.as_dict().get(k) != v)
                events.append({
                    "event": "MUTATE", "generation": generation + 1, "id": child.id, "parent": parent.id,
                    "genes": child.as_dict(), "changed": changed,
                })
                next_population.append((child, parent.id))
                slot += 1
            population = next_population

    best, _parent, best_ev = last_ranked[0]
    champion = {
        "id": best.id, "kind": best.kind, "genes": best.as_dict(), "traits": family.traits(best),
        "fitness": round(best_ev.fitness, 4), "per_quest": {k: round(v, 4) for k, v in best_ev.per_quest.items()},
    }
    if hasattr(family, "system_prompt"):
        champion["system_prompt"] = family.system_prompt(best)
    events.append({"event": "CHAMPION", "generation": summary[-1]["generation"], **{k: champion[k] for k in ("id", "fitness", "genes")}})

    usage: dict[str, Any] = {"agent_calls": sum(ev.agent_calls for ev in scored_cache.values()), "variants_scored": len(scored_cache)}
    client = getattr(agents, "client", None)
    if client is not None:
        usage.update({
            "model_calls": client.usage.calls, "prompt_tokens": client.usage.prompt_tokens,
            "completion_tokens": client.usage.completion_tokens,
        })
    return LabResult(
        config=config.as_dict(), agents=agents.describe(), label=agents.label(),
        quests=[q.name for q in quests], controls=controls, events=events, summary=summary,
        champion=champion, stopped_early=stopped_early, usage=usage,
    )
