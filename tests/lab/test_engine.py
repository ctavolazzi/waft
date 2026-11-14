"""The loop: it scores real gym encounters, fails closed, and is a pure function of its settings."""

import ast
import json
import math
import random
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

import waft.lab.engine as engine
import waft.lab.genome as genome
from waft.lab import LabConfig, run
from waft.lab.agents import MockAgents, model_agents, scripted_agents
from waft.lab.engine import encounter_score, mean
from waft.lab.fake_model import MODEL_NAME, ScriptedModel, ScriptedServer
from waft.lab.llm import BudgetSpent, LLMClient, Provider

SMALL = dict(generations=4, population=6, trials=2)


@pytest.fixture(scope="module")
def scripted():
    return run(LabConfig(seed=7, agent="scripted", **SMALL))


def evals(result, generation=None):
    return [e for e in result.events if e["event"] == "EVAL" and (generation is None or e["generation"] == generation)]


# ---------------------------------------------------------------- controls: can the scoring fail?


def test_controls_score_what_they_must(scripted):
    by_name = {c["name"]: c for c in scripted.controls}

    assert by_name["an agent that says nothing scores zero"]["score"] == 0.0
    assert by_name["an agent that always knows the answer scores one"]["score"] == 1.0
    assert 0.0 < by_name["an agent that needs one repair scores between the two"]["score"] < 1.0
    assert all(c["expected"] == c["observed"] for c in scripted.controls)


def log(success=True, fitness=0.9):
    return SimpleNamespace(success=success, calculate_fitness=lambda: fitness)


@pytest.mark.parametrize("fitness", [float("nan"), float("inf"), -0.1, 1.5])
def test_a_score_that_is_not_a_number_in_range_counts_as_zero(fitness):
    assert encounter_score(log(fitness=fitness)) == 0.0


def test_a_failed_encounter_scores_zero_whatever_the_gym_formula_says():
    """The gym gives a total failure 0.54. Selecting on that would let an agent that never answers survive."""
    assert encounter_score(log(success=False, fitness=0.54)) == 0.0
    assert encounter_score(log(success=True, fitness=0.88)) == 0.88


def test_a_scoring_bug_never_reads_as_a_good_score():
    def broken():
        raise RuntimeError("scoring blew up")

    assert encounter_score(SimpleNamespace(success=True, calculate_fitness=broken)) == 0.0


def test_nothing_to_average_is_zero():
    assert mean([]) == 0.0


# ---------------------------------------------------------------- what a run must look like


def test_every_variant_in_a_generation_has_its_own_id(scripted):
    for g in range(SMALL["generations"] + 1):
        ids = [e["id"] for e in evals(scripted, g)]
        assert len(ids) == SMALL["population"]
        assert len(set(ids)) == len(ids)


def test_the_best_never_falls_and_scores_stay_in_range(scripted):
    bests = [row["best"] for row in scripted.summary]

    assert all(later >= earlier for earlier, later in zip(bests, bests[1:]))
    assert all(math.isfinite(e["fitness"]) and 0.0 <= e["fitness"] <= 1.0 for e in evals(scripted))


def test_the_kept_half_carries_over_and_children_name_a_kept_parent(scripted):
    for g in range(1, SMALL["generations"] + 1):
        kept_before = {e["id"] for e in evals(scripted, g - 1) if e["kept"]}
        now = evals(scripted, g)
        assert kept_before <= {e["id"] for e in now}  # elitism
        assert all(e["parent"] in kept_before for e in now)


def test_evolution_improves_on_the_scripted_model():
    result = run(LabConfig(seed=7, generations=10, population=8, trials=3, agent="scripted"))

    assert result.summary[-1]["best"] > result.summary[0]["best"]
    assert result.summary[-1]["mean"] > result.summary[0]["mean"]
    # What it learned is the thing the script rewards: strict JSON and the weights rule.
    assert result.champion["genes"]["format_rule"] == 2
    assert "No prose" in result.champion["system_prompt"]


def test_the_mock_family_runs_too():
    result = run(LabConfig(seed=7, agent="mock", **SMALL))
    assert result.label == "simulated agents (seeded mock, no model)"
    assert result.summary[-1]["best"] >= result.summary[0]["best"]


# ---------------------------------------------------------------- determinism


def test_the_same_settings_give_the_same_digest_and_another_seed_does_not(scripted):
    again = run(LabConfig(seed=7, agent="scripted", **SMALL))
    other = run(LabConfig(seed=8, agent="scripted", **SMALL))

    assert again.digest == scripted.digest
    assert again.flight_recorder() == scripted.flight_recorder()
    assert other.digest != scripted.digest


def test_the_global_random_state_does_not_matter(scripted):
    random.seed(12345)
    random.random()
    assert run(LabConfig(seed=7, agent="scripted", **SMALL)).digest == scripted.digest


def test_a_fresh_process_gets_the_same_digest(scripted):
    code = (
        "from waft.lab import LabConfig, run;"
        f"print(run(LabConfig(seed=7, agent='scripted', generations={SMALL['generations']}, "
        f"population={SMALL['population']}, trials={SMALL['trials']})).digest)"
    )
    done = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=120)
    assert done.stdout.strip().splitlines()[-1] == scripted.digest, done.stderr[-400:]


def test_fitness_is_not_a_constant(scripted):
    """A fitness function that never ran a task returns one value for everyone. (`waft evolve` scored all variants 100.)"""
    assert len({e["fitness"] for e in evals(scripted)}) >= 4


def _clock_and_randomness_offences(source: str) -> list[str]:
    """Names in `source` that reach for a clock or for unseeded randomness. Works on the syntax tree."""
    banned_modules = {"time", "datetime", "uuid", "secrets"}
    offences = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            offences += [a.name for a in node.names if a.name.split(".")[0] in banned_modules]
        elif isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] in banned_modules:
            offences.append(node.module)
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "random":
            if node.attr != "Random":  # random.Random(seed) is the one allowed use
                offences.append(f"random.{node.attr}")
    return offences


@pytest.mark.parametrize("module", [engine, genome])
def test_the_loop_reads_no_clock_and_no_global_randomness(module):
    """Clocks and unseeded randomness must be injected, never reached for."""
    assert _clock_and_randomness_offences(Path(module.__file__).read_text()) == []


def test_the_clock_check_can_fail():
    """Control: the check above must notice each thing it exists to forbid."""
    planted = "import time\nfrom datetime import datetime\nimport random\nx = random.random()\ny = random.Random(3)\n"
    assert _clock_and_randomness_offences(planted) == ["time", "datetime", "random.random"]


# ---------------------------------------------------------------- the model path


def test_the_model_path_crosses_real_http_and_every_call_is_recorded(answers):
    model = ScriptedModel(answers, seed=3)
    with ScriptedServer(model) as base_url:
        client = LLMClient([Provider(base_url=base_url, model=MODEL_NAME, api_key="secret-key")])
        result = run(LabConfig(seed=3, generations=1, population=4, trials=1, agent="model"), agents=model_agents(client))
        client.close()

    assert result.usage["model_calls"] == len(model.calls) > 0
    assert result.agents["kind"] == "model" and result.agents["deterministic"] is False
    assert all(call["authorization"] == "Bearer secret-key" for call in model.calls)
    assert all(call["body"]["model"] == MODEL_NAME for call in model.calls)
    assert "secret-key" not in json.dumps([result.agents, result.events, result.champion, result.usage])
    assert any("REALITY FRACTURE" in call["user"] for call in model.calls)  # repairs go through the model too


def test_a_spent_budget_ends_the_run_cleanly_at_the_last_full_generation(answers):
    agents = scripted_agents(seed=5, answers=answers, max_calls=120)

    result = run(LabConfig(seed=5, generations=6, population=6, trials=2, agent="scripted"), agents=agents)

    assert result.stopped_early and "budget" in result.stopped_early
    assert 0 < len(result.summary) < 7
    assert all(e["generation"] <= result.summary[-1]["generation"] for e in evals(result))


def test_a_budget_too_small_for_generation_zero_is_an_error(answers):
    with pytest.raises(BudgetSpent):
        run(LabConfig(seed=5, agent="scripted", **SMALL), agents=scripted_agents(seed=5, answers=answers, max_calls=3))


def test_a_model_that_cannot_be_reached_scores_zero_not_a_crash(answers):
    import httpx

    def down(_request):
        raise httpx.ConnectError("nobody home")

    client = LLMClient([Provider(base_url="https://down.test/v1", model="m")], transport=httpx.MockTransport(down))
    result = run(LabConfig(seed=1, generations=1, population=2, trials=1, agent="model"), agents=model_agents(client))

    assert all(e["fitness"] == 0.0 for e in evals(result))


def test_the_mock_agent_is_a_pure_function_of_its_inputs(answers):
    agents = MockAgents(seed=9, answers=answers)
    g = agents.family.random(genome.rng_for("x"))
    first = [agents.make(g, "The Logic Trap", 0)("prompt") for _ in range(3)]
    again = [agents.make(g, "The Logic Trap", 0)("prompt") for _ in range(3)]
    assert first == again


def test_settings_that_make_no_sense_are_refused():
    for bad in (dict(generations=0), dict(population=1), dict(trials=0)):
        with pytest.raises(ValueError):
            LabConfig(**bad)


def test_a_run_leaves_the_working_directory_alone(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    run(LabConfig(seed=2, generations=1, population=2, trials=1, agent="scripted"))
    assert list(tmp_path.iterdir()) == []
