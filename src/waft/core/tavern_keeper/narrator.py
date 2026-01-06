"""
The Narrator - AI-contributed narrative system for TavernKeeper.

Allows AI assistants and developers to contribute contextual narratives,
observations, and reflections to the adventure journal.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

from .keeper import TavernKeeper


class Narrator:
    """
    The Narrator - Allows AI and humans to contribute to the story.

    This enables collaborative storytelling where AI assistants can
    observe, reflect, and contribute narratives to the chronicle.
    """

    def __init__(self, tavern_keeper: TavernKeeper):
        """
        Initialize the Narrator.

        Args:
            tavern_keeper: TavernKeeper instance to log to
        """
        self.tavern = tavern_keeper

    def observe(
        self,
        observation: str,
        context: Optional[Dict[str, Any]] = None,
        mood: str = "neutral",
        source: str = "ai",
    ) -> None:
        """
        Log an observation to the chronicle.

        Args:
            observation: The narrative observation
            context: Optional context (file changed, command run, etc.)
            mood: Emotional tone (neutral, surprised, delighted, concerned, amazed)
            source: Source of observation (ai, human, system)
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "observation",
            "narrative": observation,
            "mood": mood,
            "source": source,
            "context": context or {},
            "type": "narrative",
        }

        self.tavern.log_adventure(entry)

    def reflect(
        self,
        reflection: str,
        trigger: Optional[str] = None,
        insight: Optional[str] = None,
    ) -> None:
        """
        Log a reflection - deeper thoughts about the codebase or process.

        Args:
            reflection: The reflective narrative
            trigger: What triggered this reflection
            insight: Key insight or realization
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "reflection",
            "narrative": reflection,
            "trigger": trigger,
            "insight": insight,
            "type": "narrative",
        }

        self.tavern.log_adventure(entry)

    def celebrate(
        self,
        celebration: str,
        achievement: Optional[str] = None,
    ) -> None:
        """
        Log a celebration - moments of delight and beauty.

        Args:
            celebration: What's being celebrated
            achievement: Optional achievement unlocked
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "celebration",
            "narrative": celebration,
            "achievement": achievement,
            "mood": "delighted",
            "type": "narrative",
        }

        self.tavern.log_adventure(entry)

    def question(
        self,
        question: str,
        concern: Optional[str] = None,
    ) -> None:
        """
        Log a question or concern - moments of uncertainty.

        Args:
            question: The question or concern
            concern: Type of concern (bug, design, performance, etc.)
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "question",
            "narrative": question,
            "concern": concern,
            "mood": "curious",
            "type": "narrative",
        }

        self.tavern.log_adventure(entry)

    def note(
        self,
        note: str,
        category: str = "general",
        tags: Optional[list] = None,
    ) -> None:
        """
        Log a general note - any observation or thought.

        Args:
            note: The note content
            category: Category (bug, feature, refactor, insight, etc.)
            tags: Optional tags for organization
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "note",
            "narrative": note,
            "category": category,
            "tags": tags or [],
            "type": "narrative",
        }

        self.tavern.log_adventure(entry)

