"""
AI Helper - Easy integration for AI assistants to contribute narratives.

This module provides simple functions that AI assistants (Cursor, Claude, etc.)
can call to contribute observations, reflections, and notes to the chronicle.
"""

from pathlib import Path
from typing import Optional, Dict, Any

from .keeper import TavernKeeper
from .narrator import Narrator


def get_narrator(project_path: Optional[Path] = None) -> Narrator:
    """
    Get a Narrator instance for the current project.
    
    Usage in AI code:
        from waft.core.tavern_keeper.ai_helper import get_narrator
        narrator = get_narrator()
        narrator.observe("That refactor looks beautiful!", mood="delighted")
    
    Args:
        project_path: Path to project (defaults to current directory)
        
    Returns:
        Narrator instance
    """
    if project_path is None:
        project_path = Path.cwd()
    
    tavern = TavernKeeper(project_path)
    return Narrator(tavern)


def quick_observe(
    observation: str,
    mood: str = "neutral",
    project_path: Optional[Path] = None,
) -> None:
    """
    Quick function to log an observation.
    
    Usage:
        quick_observe("woah that's kinda sick", mood="surprised")
        quick_observe("that's so beautiful wow holy cannoli I love this", mood="delighted")
        quick_observe("weird that's not right", mood="concerned")
    
    Args:
        observation: The observation text
        mood: Emotional tone (neutral, surprised, delighted, concerned, amazed)
        project_path: Path to project (defaults to current directory)
    """
    narrator = get_narrator(project_path)
    narrator.observe(observation, mood=mood, source="ai")


def quick_note(
    note: str,
    category: str = "general",
    project_path: Optional[Path] = None,
) -> None:
    """
    Quick function to log a note.
    
    Usage:
        quick_note("Fixed the bug in the authentication module", category="bug")
        quick_note("Added new feature for user profiles", category="feature")
    
    Args:
        note: The note text
        category: Category (bug, feature, refactor, insight, etc.)
        project_path: Path to project (defaults to current directory)
    """
    narrator = get_narrator(project_path)
    narrator.note(note, category=category, tags=["ai"])


def celebrate_moment(
    celebration: str,
    achievement: Optional[str] = None,
    project_path: Optional[Path] = None,
) -> None:
    """
    Celebrate a moment of beauty or achievement.
    
    Usage:
        celebrate_moment("that's so beautiful wow holy cannoli I love this")
        celebrate_moment("The code structure is perfect", achievement="clean_architecture")
    
    Args:
        celebration: What's being celebrated
        achievement: Optional achievement name
        project_path: Path to project (defaults to current directory)
    """
    narrator = get_narrator(project_path)
    narrator.celebrate(celebration, achievement=achievement)


def raise_concern(
    question: str,
    concern_type: str = "general",
    project_path: Optional[Path] = None,
) -> None:
    """
    Log a concern or question.
    
    Usage:
        raise_concern("weird that's not right", concern_type="bug")
        raise_concern("This might cause performance issues", concern_type="performance")
    
    Args:
        question: The question or concern
        concern_type: Type of concern (bug, design, performance, etc.)
        project_path: Path to project (defaults to current directory)
    """
    narrator = get_narrator(project_path)
    narrator.question(question, concern=concern_type)

