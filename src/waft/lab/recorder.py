"""Put a lab run on the record, and read it back.

One run becomes one Logbook (waft.record): a hash-chained list of records plus the stored
artefacts they cite. What goes in:

    controls    three agents whose scores are known in advance (silent, oracle, one repair)
    handoffs    the flight recorder, the per-generation summary, the champion and the result,
                each re-read from the store and hashed again by the reader
    balances    numbers measured two ways (the engine's summary against the stored events,
                and one run against a second run with the same settings)
    checks      the claims a run has to earn: unique ids, a best score that never falls,
                finite scores, a completed run, an improvement
    verdicts    decided by rule R1 from the checks, never by this module

The last record's hash is the head. Publish it (a commit, a post, a message to someone):
a run that verifies against a head published elsewhere has not been edited since.

Two fingerprints, on purpose. The head identifies this recorded run, with its time and
host, so it differs every time. The result digest identifies what the loop computed, so
with deterministic agents it is the same for the same settings on any machine.
"""

from __future__ import annotations

import json
import math
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..record import Logbook, VerifyReport, dec, plainify, sha256, verify
from .engine import LabResult

SCENARIO = "waft.lab/1"
NODE_VERIFIER = Path(__file__).resolve().parent.parent / "record" / "node" / "verify.mjs"


@dataclass
class RecordedRun:
    path: Path
    head: str
    verdicts: dict[str, str]
    report: VerifyReport

    @property
    def status(self) -> str:
        """The worst verdict: fail beats warn beats pass."""
        for level in ("fail", "warn", "skip", "pass"):
            if level in self.verdicts.values():
                return level
        return "skip"


@dataclass
class RunView:
    """A recorded run, read back from its Logbook. Everything `show` and `share` need."""

    path: Path
    run_id: str
    head: str
    started: str
    closed: bool
    result: dict[str, Any]
    summary: list[dict[str, Any]]
    champion: dict[str, Any]
    events: list[dict[str, Any]]
    checks: list[dict[str, Any]] = field(default_factory=list)
    controls: list[dict[str, Any]] = field(default_factory=list)
    balances: list[dict[str, Any]] = field(default_factory=list)
    verdicts: dict[str, str] = field(default_factory=dict)
    git_head: str = ""

    @property
    def status(self) -> str:
        for level in ("fail", "warn", "skip", "pass"):
            if level in self.verdicts.values():
                return level
        return "skip"


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=1) + "\n").encode("utf-8")


def record(
    result: LabResult,
    out_root: Path | str,
    *,
    replay: LabResult | None = None,
    argv: list[str] | None = None,
    repo: Path | str | None = None,
) -> RecordedRun:
    """Write the run as a Logbook under `out_root` and seal it. Returns where it is and its head."""
    cfg = result.config
    deterministic = bool(result.agents.get("deterministic"))
    exact = "exact" if deterministic else "volatile"
    lb = Logbook.create(
        out_root,
        label=f"lab {cfg['agent']} seed {cfg['seed']}",
        scenario=SCENARIO,
        argv=argv if argv is not None else ["waft", "lab", "run"],
        repo=repo,
        meta=plainify({"config": cfg, "agents": result.agents, "label": result.label, "quests": result.quests}),
    )
    verdicts: dict[str, str] = {}

    # ---- scoring: can it fail, can it pass?
    since = lb.next_seq
    for c in result.controls:
        lb.control(c["name"], planted=c["planted"], expected=c["expected"], observed=c["observed"], evidence=[])
    lb.check(
        "scoring", "the three control agents were scored", len(result.controls) == 3, cls="should",
        expected=3, observed=len(result.controls), evidence=[],
        detail="the oracle and one-repair controls need the dungeon's known-good answers",
    )
    lb.settle("scoring", since)
    verdicts["scoring"] = lb.conclude("scoring")

    # ---- evolution: store what happened, then make claims about it
    since = lb.next_seq
    flight = result.flight_recorder().encode("utf-8")
    payloads = {
        "flight_recorder.jsonl": (flight, "application/x-ndjson", "every event of the run, one per line"),
        "summary.json": (_json_bytes(result.summary), "application/json", "one row per generation"),
        "champion.json": (_json_bytes(result.champion), "application/json", "the best variant of the last generation"),
        "result.json": (
            _json_bytes({
                "config": cfg, "agents": result.agents, "label": result.label, "quests": result.quests,
                "controls": result.controls, "digest": result.digest, "usage": result.usage,
                "stopped_early": result.stopped_early,
            }),
            "application/json", "settings, agents, controls and the result digest",
        ),
    }
    stored: dict[str, bytes] = {}
    for name, (data, media, note) in payloads.items():
        ref = lb.put(data, name, media=media, determinism=exact)
        stored[name] = lb.artifact(ref)  # read back from the store, as any later reader would
        lb.handoff(
            "waft.lab.engine", "waft.lab.recorder", ref, schema=f"{SCENARIO}:{name}", via="object store",
            consumer_saw=sha256(stored[name]), note=note,
        )

    events = [json.loads(line) for line in stored["flight_recorder.jsonl"].decode("utf-8").splitlines() if line.strip()]
    evals = [e for e in events if e["event"] == "EVAL"]
    generations = sorted({e["generation"] for e in evals})
    last = generations[-1]
    best_by_generation = [max(e["fitness"] for e in evals if e["generation"] == g) for g in generations]

    lb.reconcile(
        "best fitness of the last generation", dec(result.summary[-1]["best"]), dec(best_by_generation[-1]),
        a_source="the engine's summary row", b_source="the highest EVAL fitness in the stored flight recorder",
        basis="consistency", why="the summary must say what the events say",
    )
    lb.reconcile(
        "evaluations in the flight recorder", len(evals), cfg["population"] * len(generations),
        a_source="EVAL events counted in the stored flight recorder", b_source="population x generations run",
        basis="expectation", why="every variant of every generation is scored exactly once",
    )
    if replay is not None:
        lb.reconcile(
            "the same settings give the same result", result.digest, replay.digest,
            a_source="result digest of this run", b_source="result digest of a second run with the same settings",
            basis="consistency", why="with deterministic agents the loop is a pure function of its settings",
        )

    duplicates = sum(
        len(ids) - len(set(ids)) for ids in ([e["id"] for e in evals if e["generation"] == g] for g in generations)
    )
    lb.check(
        "evolution", "every variant in a generation has its own id", duplicates == 0,
        expected={"duplicate_ids": 0}, observed={"duplicate_ids": duplicates, "generations": len(generations)}, evidence=[],
    )
    falls = [g for g, (a, b) in zip(generations[1:], zip(best_by_generation, best_by_generation[1:])) if b < a]
    lb.check(
        "evolution", "the best score never falls from one generation to the next", not falls,
        expected="non-decreasing", observed=" ".join(dec(b) for b in best_by_generation), evidence=[],
        detail="the best variants carry over unchanged, so the best can only stay or rise",
    )
    scores = [e["fitness"] for e in evals]
    in_range = all(isinstance(s, (int, float)) and math.isfinite(s) and 0 <= s <= 1 for s in scores)
    lb.check(
        "evolution", "every score is a finite number between 0 and 1", in_range,
        expected="0 <= score <= 1", observed={"scores": len(scores), "lowest": dec(min(scores)), "highest": dec(max(scores))},
        evidence=[],
    )
    lb.check(
        "evolution", "the run completed every generation it was asked for", result.stopped_early is None, cls="should",
        expected=cfg["generations"], observed=last, detail=result.stopped_early or "", evidence=[],
    )
    lb.check(
        "evolution", "the best variant of the last generation beats the best of generation 0",
        best_by_generation[-1] > best_by_generation[0], cls="should",
        expected=f"above {dec(best_by_generation[0])}", observed=dec(best_by_generation[-1]), evidence=[],
    )
    lb.check(
        "evolution", "who the agents were", True, cls="info", observed=result.label, evidence=[],
        detail="a result against simulated agents says nothing about any real model",
    )
    if replay is None and deterministic:
        lb.note("this run was not replayed, so its reproducibility was not checked", tag="warning")
    lb.settle("evolution", since)
    verdicts["evolution"] = lb.conclude("evolution")

    lb.note(f"result digest {result.digest}", tag="digest")
    head = lb.close()
    return RecordedRun(lb.path, head, verdicts, verify(lb.path, expect_head=head))


def load_run(path: Path | str) -> RunView:
    """Read a recorded run back. Raises ValueError if the folder is not a lab run."""
    path = Path(path)
    if not (path / "chain.jsonl").exists():
        raise ValueError(f"{path} is not a recorded run (no chain.jsonl)")
    lb = Logbook.open(path)
    records = lb.records()
    if not records or records[0]["data"].get("scenario") != SCENARIO:
        raise ValueError(f"{path} is a Logbook, but not a waft lab run")

    artefacts: dict[str, Any] = {}
    for r in lb.records("handoff"):
        ref = r["data"]["artifact"]
        raw = lb.artifact(ref).decode("utf-8")
        if ref["name"].endswith(".jsonl"):
            artefacts[ref["name"]] = [json.loads(line) for line in raw.splitlines() if line.strip()]
        else:
            artefacts[ref["name"]] = json.loads(raw)
    for needed in ("result.json", "summary.json", "champion.json", "flight_recorder.jsonl"):
        if needed not in artefacts:
            raise ValueError(f"{path} is missing {needed}")

    return RunView(
        path=path,
        run_id=records[0]["run"],
        head=records[-1]["hash"],
        started=records[0]["ts"],
        closed=records[-1]["kind"] == "run.end",
        result=artefacts["result.json"],
        summary=artefacts["summary.json"],
        champion=artefacts["champion.json"],
        events=artefacts["flight_recorder.jsonl"],
        checks=[r["data"] for r in lb.records("check")],
        controls=[r["data"] for r in lb.records("control")],
        balances=[r["data"] for r in lb.records("reconcile")],
        verdicts={r["data"]["subject"]: r["data"]["status"] for r in lb.records("verdict")},
        git_head=records[0]["data"].get("git", {}).get("head", ""),
    )


def verify_run(path: Path | str, expect_head: str | None = None) -> VerifyReport:
    return verify(Path(path), expect_head=expect_head or None)


def verify_with_node(path: Path | str, expect_head: str | None = None) -> dict[str, Any] | None:
    """Ask the second verifier (Node, written from the specification alone). None if node is not installed."""
    node = shutil.which("node")
    if not node or not NODE_VERIFIER.exists():
        return None
    argv = [node, str(NODE_VERIFIER), str(path)]
    if expect_head:
        argv += ["--expect-head", expect_head]
    done = subprocess.run(argv, capture_output=True, text=True, timeout=120)
    try:
        return json.loads(done.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return {"ok": False, "clean": False, "codes": ["E_NODE"], "error": (done.stderr or done.stdout)[-300:]}
