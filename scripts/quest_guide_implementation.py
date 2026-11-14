#!/usr/bin/env python3
"""Thin wrapper around waft.core.quest_guide, where the quest system lives since 2026-11-14.

It moved into the package so the API can import it from an installed wheel. This file keeps
`python scripts/quest_guide_implementation.py --status` (and every other flag) working.
"""

import sys
from pathlib import Path

try:
    from waft.core import quest_guide
except ImportError:  # run from a checkout without an install
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
    from waft.core import quest_guide

from waft.core.quest_guide import *  # noqa: E402,F401,F403
from waft.core.quest_guide import QuestManager, QuestProgress, QuestStatus, main  # noqa: E402,F401

if __name__ == "__main__":
    quest_guide.main()
