"""
waft.gym: the Jungle Gym. An agent (any function from a prompt to text) is given a quest,
its answer is validated by WAFT's InputTransformer, fractures ("scints") are classified,
a repair loop gives it up to three more tries, and the encounter is scored.

This package lived at src/gym/rpg until 2026-11-14. It moved inside waft so that it ships
in the wheel and no longer shares a top-level name with the unrelated `gym` package on PyPI.
`gym.rpg` remains as a thin alias for code that imports the old path from a source checkout.
"""

from pathlib import Path

from .game_master import GameMaster
from .models import BattleLog, Hero, Quest
from .scint import RealityAnchor, RegexScintDetector, Scint, ScintType
from .stabilizer import StabilizationLoop

# The quest files that ship with WAFT.
DUNGEONS = Path(__file__).parent / "dungeons"

__all__ = [
    "DUNGEONS",
    "Hero",
    "Quest",
    "BattleLog",
    "GameMaster",
    "ScintType",
    "Scint",
    "RealityAnchor",
    "RegexScintDetector",
    "StabilizationLoop",
]
