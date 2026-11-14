"""Genomes: what a variant inherits, and what mutation is allowed to change.

A genome is a kind plus a flat set of named genes (numbers and booleans). Its id is the
hash of its canonical form, so two variants with the same genes are the same variant, and
no two different variants can share an id. (WAFT's older `evolve` gave every variant in a
generation one id; see tests/test_being_ids.py.)

Nothing here reads a clock or the global random state. Every random draw comes from a
generator seeded by `rng_for(...)`, so a run is a pure function of its seed and settings.
"""

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass
from typing import Any

Gene = bool | int | float


def canon(value: Any) -> str:
    """Canonical JSON: sorted keys, no spaces, floats rounded to 6 places. What every hash here is taken over."""

    def tidy(v: Any) -> Any:
        if isinstance(v, bool) or v is None or isinstance(v, (int, str)):
            return v
        if isinstance(v, float):
            return round(v, 6)
        if isinstance(v, dict):
            return {str(k): tidy(x) for k, x in v.items()}
        if isinstance(v, (list, tuple)):
            return [tidy(x) for x in v]
        raise TypeError(f"{type(v).__name__} has no canonical form")

    return json.dumps(tidy(value), sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canon(value).encode("utf-8")).hexdigest()


def rng_for(*parts: Any) -> random.Random:
    """A generator that depends on nothing but its arguments."""
    h = hashlib.sha256("|".join(map(str, parts)).encode("utf-8")).digest()
    return random.Random(int.from_bytes(h[:8], "big"))


@dataclass(frozen=True)
class Genome:
    kind: str
    genes: tuple[tuple[str, Gene], ...]

    @classmethod
    def of(cls, kind: str, **genes: Gene) -> Genome:
        return cls(kind, tuple(sorted(genes.items())))

    def __getitem__(self, name: str) -> Gene:
        return dict(self.genes)[name]

    def as_dict(self) -> dict[str, Gene]:
        return json.loads(canon(dict(self.genes)))

    @property
    def id(self) -> str:
        return "g_" + digest({"kind": self.kind, "genes": dict(self.genes)})[:10]


def _clamp(x: float, low: float, high: float) -> float:
    return min(high, max(low, x))


class MockFamily:
    """Three probabilities that drive a stand-in agent: how often it breaks syntax, breaks
    logic, and manages a repair. Ported from the FogSift lab harness (checks/waft_lab.py)."""

    kind = "mock"

    def random(self, rnd: random.Random) -> Genome:
        return Genome.of(
            self.kind,
            p_syntax=rnd.uniform(0.5, 0.95),
            p_logic=rnd.uniform(0.5, 0.95),
            p_repair=rnd.uniform(0.1, 0.5),
        )

    def mutate(self, genome: Genome, rnd: random.Random, sigma: float = 0.12) -> Genome:
        return Genome.of(
            self.kind,
            **{k: _clamp(float(v) + rnd.gauss(0, sigma), 0.02, 0.98) for k, v in genome.genes},
        )

    def traits(self, genome: Genome) -> list[str]:
        g = genome.as_dict()
        return [
            f"breaks syntax {g['p_syntax']:.0%}",
            f"breaks logic {g['p_logic']:.0%}",
            f"repairs {g['p_repair']:.0%}",
        ]


# The rules a prompt genome can switch on. Each is one sentence of a system prompt.
FORMAT_RULES = (
    "",
    "Answer with JSON.",
    "Answer with only a JSON object. No prose, no code fences, nothing before or after it.",
)
SCHEMA_RULE = (
    "The object has exactly these keys: 'alternatives' (a list of names), 'criteria' "
    "(a map from criterion name to weight), 'scores' (a map from each alternative to a map "
    "from each criterion to a number) and 'methodology' (the string 'WSM')."
)
WEIGHTS_RULE = "Criterion weights are positive numbers and must sum to 1.0. Fix them if the text gets this wrong."
TIDY_RULE = "Trim whitespace from every name, and write numbers as numbers, not strings."
EXAMPLE_RULE = (
    'Example of the shape: {"alternatives": ["A", "B"], "criteria": {"Cost": 0.5, "Speed": 0.5}, '
    '"scores": {"A": {"Cost": 7, "Speed": 4}, "B": {"Cost": 5, "Speed": 9}}, "methodology": "WSM"}'
)
BASE_RULE = "You turn a description of a decision into a decision matrix."

MAX_TEMPERATURE = 1.2


class PromptFamily:
    """A system prompt assembled from switchable rules, plus a sampling temperature.

    This is the genome for a real model: evolution changes what the model is told and how
    it samples, never the task or the scoring.
    """

    kind = "prompt"
    _switches = ("schema_rule", "weights_rule", "tidy_rule", "example")

    def random(self, rnd: random.Random) -> Genome:
        return Genome.of(
            self.kind,
            format_rule=rnd.choice((0, 0, 1)),
            schema_rule=rnd.random() < 0.25,
            weights_rule=rnd.random() < 0.25,
            tidy_rule=rnd.random() < 0.25,
            example=rnd.random() < 0.15,
            temperature=round(rnd.uniform(0.6, MAX_TEMPERATURE), 2),
        )

    def mutate(self, genome: Genome, rnd: random.Random) -> Genome:
        genes = dict(genome.genes)
        names = sorted(genes)
        # One or two genes change. Small steps: evolution here is a walk, not a lottery.
        for name in rnd.sample(names, k=1 if rnd.random() < 0.6 else 2):
            if name in self._switches:
                genes[name] = not genes[name]
            elif name == "format_rule":
                genes[name] = int(_clamp(int(genes[name]) + rnd.choice((-1, 1)), 0, len(FORMAT_RULES) - 1))
            elif name == "temperature":
                genes[name] = round(_clamp(float(genes[name]) + rnd.gauss(0, 0.25), 0.0, MAX_TEMPERATURE), 2)
        return Genome.of(self.kind, **genes)

    def system_prompt(self, genome: Genome) -> str:
        g = genome.as_dict()
        parts = [BASE_RULE, FORMAT_RULES[int(g["format_rule"])]]
        if g["schema_rule"]:
            parts.append(SCHEMA_RULE)
        if g["weights_rule"]:
            parts.append(WEIGHTS_RULE)
        if g["tidy_rule"]:
            parts.append(TIDY_RULE)
        if g["example"]:
            parts.append(EXAMPLE_RULE)
        return " ".join(p for p in parts if p)

    def traits(self, genome: Genome) -> list[str]:
        g = genome.as_dict()
        out = [("no format rule", "asks for JSON", "JSON only, strict")[int(g["format_rule"])]]
        if g["schema_rule"]:
            out.append("names the keys")
        if g["weights_rule"]:
            out.append("weights sum to 1")
        if g["tidy_rule"]:
            out.append("tidies names")
        if g["example"]:
            out.append("shows an example")
        out.append(f"temperature {float(g['temperature']):.2f}")
        return out


FAMILIES = {MockFamily.kind: MockFamily, PromptFamily.kind: PromptFamily}
