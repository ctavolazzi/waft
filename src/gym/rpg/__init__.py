"""Alias for waft.gym, which is where the Jungle Gym lives since 2026-11-14.

Kept so that code written against a source checkout (`from gym.rpg.game_master import GameMaster`)
keeps working. It is not part of the installed package; new code should import waft.gym.
"""

import sys

from waft import gym as _gym
from waft.gym import *  # noqa: F401,F403
from waft.gym import game_master, models, scint, stabilizer

# The same module objects under the old names, so classes are never duplicated.
for _name, _module in (
    ("game_master", game_master),
    ("models", models),
    ("scint", scint),
    ("stabilizer", stabilizer),
):
    sys.modules[f"{__name__}.{_name}"] = _module

# Callers find the quest files through this package's location; point them at the real one.
__file__ = _gym.__file__
__all__ = _gym.__all__
