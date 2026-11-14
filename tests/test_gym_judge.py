"""The gym's judge must enforce what its quests say they require.

Until 2026-11-14 the gym validated answers with the InputTransformer alone, which checks
shape but not the maths. An answer whose weights summed to 1.5, or were negative, won
quests whose win condition reads "weights sum to 1.0".
"""

import io
import json

import pytest
from rich.console import Console

from waft.gym import DUNGEONS, GameMaster, Hero
from waft.gym.game_master import validate_answer

ANSWERS = json.loads((DUNGEONS / "waft_temple.answers.json").read_text())["answers"]


def _copy(name):
    return json.loads(json.dumps(ANSWERS[name]))


@pytest.mark.parametrize("name", sorted(ANSWERS))
def test_reference_answers_are_valid(name):
    matrix = validate_answer(_copy(name))
    assert [a.name for a in matrix.alternatives] == ANSWERS[name]["alternatives"]


def test_every_quest_has_a_reference_answer():
    quests = json.loads((DUNGEONS / "waft_temple.json").read_text())["quests"]
    assert {q["name"] for q in quests} == set(ANSWERS)


def test_weights_that_do_not_sum_to_one_are_rejected():
    answer = _copy("The Clean Extraction")
    answer["criteria"]["Cost"] = 0.9  # 0.9 + 0.3 + 0.3
    with pytest.raises(ValueError, match="sum to 1.0"):
        validate_answer(answer)


def test_negative_weights_are_rejected():
    """The Logic Trap exists to catch this; it could be won without fixing it."""
    answer = _copy("The Logic Trap")
    answer["criteria"] = {"Risk": -0.3, "Reward": 1.3}
    with pytest.raises(ValueError, match="negative weight"):
        validate_answer(answer)


def test_a_missing_score_is_rejected():
    answer = _copy("The Dirty Input")
    del answer["scores"]["Option3"]["Quality"]
    with pytest.raises(ValueError):
        validate_answer(answer)


def test_an_encounter_with_bad_weights_is_not_a_win(tmp_path):
    gm = GameMaster(DUNGEONS, tmp_path / "loot")
    gm.console = Console(file=io.StringIO())
    quest = next(q for q in gm.load_quests("waft_temple.json") if q.name == "The Logic Trap")
    bad = _copy("The Logic Trap")
    bad["criteria"]["Risk"] = 0.9

    log = gm.start_encounter(Hero(name="stubborn"), quest, lambda _prompt: json.dumps(bad))

    assert log.success is False
    assert "LOGIC_FRACTURE" in (log.scints_detected or [])
    assert log.agent_call_count == 4  # one attempt and three refused repairs
