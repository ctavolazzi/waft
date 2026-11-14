"""Agents: the thing a genome turns into when it is asked to do a task.

To the gym an agent is just a function from a prompt to text. A factory here builds one
for a genome, a quest and a trial. Three kinds exist:

    mock      three probabilities drive a stand-in (no model, no network)
    scripted  a prompt genome talks to the scripted fake model through the real client
    model     a prompt genome talks to the providers named in the environment

and three fixed agents the lab uses as controls: one that says nothing, one that always
knows the answer, and one that needs exactly one repair.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any, Protocol

from .fake_model import MODEL_NAME, ScriptedModel
from .genome import Genome, MockFamily, PromptFamily, rng_for
from .llm import BudgetSpent, LLMClient, LLMError, Provider

Agent = Callable[[str], str]

REPAIR_MARKER = "REALITY FRACTURE"  # the gym's stabilization prompt carries this phrase


class Agents(Protocol):
    kind: str
    deterministic: bool
    family: Any

    def make(self, genome: Genome, quest_name: str, trial: int) -> Agent: ...

    def describe(self) -> dict[str, Any]: ...

    def label(self) -> str: ...


class MockAgents:
    """A stand-in for a model. Its answers are a pure function of (seed, genome, quest, trial, call number)."""

    kind = "mock"
    deterministic = True

    def __init__(self, seed: int, answers: dict[str, Any]) -> None:
        self.seed = seed
        self.answers = answers
        self.family = MockFamily()

    def make(self, genome: Genome, quest_name: str, trial: int) -> Agent:
        genes = genome.as_dict()
        good = json.dumps(self.answers[quest_name])
        calls = 0

        def agent(prompt: str) -> str:
            nonlocal calls
            calls += 1
            r = rng_for(self.seed, genome.id, quest_name, trial, calls)
            if REPAIR_MARKER in prompt:
                return good if r.random() < genes["p_repair"] else good[: len(good) // 2]
            if r.random() < genes["p_syntax"]:
                return good[: len(good) // 2]  # cut off mid-object: a syntax tear
            if r.random() < genes["p_logic"]:
                bad = json.loads(good)
                bad["criteria"][next(iter(bad["criteria"]))] = 0.9  # weights no longer sum to 1.0
                return json.dumps(bad)
            return good

        return agent

    def describe(self) -> dict[str, Any]:
        return {"kind": self.kind, "model": "none", "deterministic": True}

    def label(self) -> str:
        return "simulated agents (seeded mock, no model)"


class ModelAgents:
    """Prompt genomes in front of a chat model, real or scripted."""

    def __init__(self, client: LLMClient, *, kind: str, deterministic: bool, label: str) -> None:
        self.client = client
        self.kind = kind
        self.deterministic = deterministic
        self._label = label
        self.family = PromptFamily()

    def make(self, genome: Genome, quest_name: str, trial: int) -> Agent:
        system = self.family.system_prompt(genome)
        temperature = float(genome["temperature"])

        def agent(prompt: str) -> str:
            try:
                reply = self.client.chat(
                    [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
                    max_tokens=600,
                    temperature=temperature,
                )
            except BudgetSpent:
                raise
            except LLMError:
                return ""  # a model that could not be reached answered nothing
            return reply.text

        return agent

    def describe(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "model": ", ".join(p["model"] for p in self.client.describe()),
            "providers": [p["name"] for p in self.client.describe()],
            "deterministic": self.deterministic,
        }

    def label(self) -> str:
        return self._label


def scripted_agents(seed: int, answers: dict[str, Any], max_calls: int | None = None) -> ModelAgents:
    """The full model path (client, HTTP shape, prompt genomes) against the scripted fake. No network."""
    model = ScriptedModel(answers, seed=seed)
    client = LLMClient(
        [Provider(base_url="http://scripted.invalid/v1", model=MODEL_NAME)],
        transport=model.transport(),
        max_calls=max_calls,
    )
    return ModelAgents(
        client, kind="scripted", deterministic=True, label="simulated agents (scripted fake model)"
    )


def model_agents(client: LLMClient) -> ModelAgents:
    names = ", ".join(p["model"] for p in client.describe())
    return ModelAgents(client, kind="model", deterministic=False, label=f"model: {names}")


# ---------------------------------------------------------------------- control agents


def silent_agent(_prompt: str) -> str:
    """Says nothing. If this scores above zero, the scoring is broken."""
    return ""


def oracle_agent(answer: dict[str, Any]) -> Agent:
    """Always returns the known-good answer. If this scores below one, the scoring is broken."""
    text = json.dumps(answer)
    return lambda _prompt: text


def one_repair_agent(answer: dict[str, Any]) -> Agent:
    """Wraps its first answer in a code fence, then answers cleanly when asked to repair.

    It must score above the silent agent and below the oracle: that the score can tell
    "right first time" from "right after a fix" is what makes it worth selecting on.
    """
    text = json.dumps(answer)
    return lambda prompt: text if REPAIR_MARKER in prompt else f"```json\n{text}\n```"
