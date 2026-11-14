"""The quest system: passing a checkpoint must record it (it raised NameError instead)."""

from waft.core.quest_guide import QuestManager


def test_a_passed_checkpoint_is_recorded_for_every_quest_that_lists_it(tmp_path):
    manager = QuestManager(tmp_path)
    quest_id, quest = next((qid, q) for qid, q in manager.quests.items() if q.checkpoints)
    checkpoint_id = quest.checkpoints[0]
    manager.checkpoints[checkpoint_id].validator = lambda _project_path: (True, "planted pass")

    passed, message = manager.check_checkpoint(checkpoint_id)

    assert (passed, message) == (True, "planted pass")
    assert checkpoint_id in manager.progress[quest_id].checkpoints_passed


def test_a_failed_checkpoint_records_nothing(tmp_path):
    manager = QuestManager(tmp_path)
    quest_id, quest = next((qid, q) for qid, q in manager.quests.items() if q.checkpoints)
    checkpoint_id = quest.checkpoints[0]
    manager.checkpoints[checkpoint_id].validator = lambda _project_path: (False, "planted fail")

    passed, _message = manager.check_checkpoint(checkpoint_id)

    assert passed is False
    assert quest_id not in manager.progress or checkpoint_id not in manager.progress[quest_id].checkpoints_passed
