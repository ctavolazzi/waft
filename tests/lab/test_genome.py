"""Genomes: ids come from content, randomness comes from arguments only."""

import random

from waft.lab.genome import FORMAT_RULES, Genome, MockFamily, PromptFamily, canon, rng_for


def test_the_id_is_the_content():
    a = Genome.of("mock", p_syntax=0.5, p_logic=0.25, p_repair=0.125)
    b = Genome.of("mock", p_repair=0.125, p_logic=0.25, p_syntax=0.5)  # same genes, another order
    c = Genome.of("mock", p_syntax=0.5, p_logic=0.25, p_repair=0.126)
    d = Genome.of("prompt", p_syntax=0.5, p_logic=0.25, p_repair=0.125)  # same genes, another kind

    assert a.id == b.id
    assert len({a.id, c.id, d.id}) == 3
    assert a.id.startswith("g_") and len(a.id) == 12


def test_canonical_form_is_stable():
    assert canon({"b": 1.0000004, "a": [True, None, "x"]}) == '{"a":[true,null,"x"],"b":1.0}'


def test_rng_depends_only_on_its_arguments():
    random.seed(1)
    first = rng_for("spawn", 7, 0).random()
    random.seed(2)  # the global generator must not matter
    assert rng_for("spawn", 7, 0).random() == first
    assert rng_for("spawn", 7, 1).random() != first
    assert rng_for("spawn", 8, 0).random() != first


def test_mock_mutation_stays_in_range_and_changes_something():
    family = MockFamily()
    genome = family.random(rng_for("t", 1))
    child = family.mutate(genome, rng_for("t", 2))

    assert child.id != genome.id
    assert all(0.02 <= float(v) <= 0.98 for _k, v in child.genes)


def test_prompt_mutation_changes_one_or_two_genes():
    family = PromptFamily()
    genome = family.random(rng_for("t", 1))
    for n in range(40):
        child = family.mutate(genome, rng_for("t", "m", n))
        changed = [k for k in child.as_dict() if child.as_dict()[k] != genome.as_dict()[k]]
        assert len(changed) <= 2
        assert 0 <= child["format_rule"] < len(FORMAT_RULES)
        assert 0.0 <= child["temperature"] <= 1.2


def test_the_system_prompt_is_built_from_the_switched_on_rules():
    family = PromptFamily()
    bare = Genome.of("prompt", format_rule=0, schema_rule=False, weights_rule=False, tidy_rule=False, example=False, temperature=0.5)
    full = Genome.of("prompt", format_rule=2, schema_rule=True, weights_rule=True, tidy_rule=True, example=True, temperature=0.5)

    assert "JSON" not in family.system_prompt(bare)
    prompt = family.system_prompt(full)
    for phrase in ("No prose", "exactly these keys", "sum to 1.0", "Trim whitespace", "Example of the shape"):
        assert phrase in prompt
    assert "JSON only, strict" in family.traits(full)
