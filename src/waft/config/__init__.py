"""Configuration constants for Waft.

This package contains centralized configuration for:
- Visual themes (emojis, colors)
- Command abilities mapping
- Gamification thresholds
- Default values
"""

from .theme import Emoji, Color
from .abilities import get_command_ability, COMMAND_ABILITIES

__all__ = [
    "Emoji",
    "Color",
    "get_command_ability",
    "COMMAND_ABILITIES",
]
