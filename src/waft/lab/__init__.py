"""waft.lab: directed evolution you can check.

    waft lab run       breed variants on the Jungle Gym's quests and record the run in a Logbook
    waft lab verify    re-derive every hash of a recorded run, against a published head
    waft lab show      print what a recorded run says happened
    waft lab share     turn a run into a card, a replay page and a short video
    waft lab doctor    prove the lab works here: controls, a small run, a tamper test

The pieces: `engine` (the loop), `genome` (what is inherited), `agents` (mock, scripted
fake model, real model), `llm` (the provider client), `recorder` (the Logbook), `share`.
"""

from .engine import LabConfig, LabResult, run

__all__ = ["LabConfig", "LabResult", "run"]
