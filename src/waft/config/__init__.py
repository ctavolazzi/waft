"""Configuration constants for Waft.

This package contains centralized configuration for:
- Visual themes (emojis, colors)
- Command abilities mapping
- Gamification thresholds
- Default values
"""

from .abilities import COMMAND_ABILITIES, get_command_ability
from .theme import Color, Emoji

__all__ = [
    "Emoji",
    "Color",
    "get_command_ability",
    "COMMAND_ABILITIES",
]
