"""
Teleport Massive Writer Module

A sophisticated storytelling engine for the Teleport Massive universe.
Supports parameterized story generation, visual novel output, and
content-addressed storage for efficient history lookup.

Usage:
    from waft.teleport_massive import TMWriter, StoryConfig

    config = StoryConfig(
        protagonist="sam_iker",
        starting_era="2111",
        focus_faction="teleport_massive",
        tone="noir_cosmic"
    )

    writer = TMWriter(config)
    chapter = writer.generate_chapter(1)
"""

from .models import (
    Character,
    Faction,
    Location,
    Artifact,
    TimelineEvent,
    ScintPoint,
    StoryState,
    KnowledgeState,
)
from .storage import StoryStore, ContentHash
from .config import StoryConfig, ConfigParameter
from .engine import TMWriter, StoryEngine
from .lore import TMLore

__all__ = [
    # Models
    "Character",
    "Faction",
    "Location",
    "Artifact",
    "TimelineEvent",
    "ScintPoint",
    "StoryState",
    "KnowledgeState",
    # Storage
    "StoryStore",
    "ContentHash",
    # Config
    "StoryConfig",
    "ConfigParameter",
    # Engine
    "TMWriter",
    "StoryEngine",
    # Lore
    "TMLore",
]

__version__ = "0.1.0"
