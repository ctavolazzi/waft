"""
TavernKeeper - RPG Gamification Engine for Living Repositories

The TavernKeeper transforms software development into a semi-autonomous RPG
with Constructivist Sci-Fi theme. It uses:
- TinyDB for state storage
- d20 for dice rolling
- Tracery for procedural narrative generation
- Rich for terminal UI rendering
"""

from .keeper import TavernKeeper
from .narrator import Narrator

__all__ = ["TavernKeeper", "Narrator"]
