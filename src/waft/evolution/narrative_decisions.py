"""
Narrative Decision System - Decision types and validation for story evolution.

Defines the types of decisions agents can make to evolve stories.
"""

import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class DecisionType(str, Enum):
    """Types of narrative decisions agents can make."""

    CHARACTER_ACTION = "character_action"  # Character does something
    PLOT_TWIST = "plot_twist"  # Unexpected event or revelation
    WORLD_EVENT = "world_event"  # Environmental or world change
    CHARACTER_DEVELOPMENT = "character_development"  # Character growth or change
    RELATIONSHIP_CHANGE = "relationship_change"  # Character relationship evolves
    CONFLICT_ESCALATION = "conflict_escalation"  # Increase tension
    CONFLICT_RESOLUTION = "conflict_resolution"  # Resolve tension
    WORLD_BUILDING = "world_building"  # Expand world details


class NarrativeDecision(BaseModel):
    """A decision made by an agent to evolve the story."""

    decision_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    decision_type: DecisionType
    agent_id: str | None = None
    generation: int

    # Decision content
    description: str
    character: str | None = None
    location: str | None = None
    narrative_text: str | None = None

    # Decision metadata
    importance: float = Field(default=0.5, ge=0.0, le=1.0)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    reasoning: str | None = None

    # Validation
    validated: bool = False
    validation_errors: list[str] = Field(default_factory=list)

    timestamp: datetime = Field(default_factory=datetime.utcnow)

    def validate(self, story_state: "StoryState") -> tuple[bool, list[str]]:
        """
        Validate decision against current story state.

        Returns:
            (is_valid, list_of_errors)
        """
        errors = []

        # Check character exists if specified
        if self.character and self.character not in story_state.characters:
            errors.append(f"Character '{self.character}' does not exist in story")

        # Check decision type specific validations
        if self.decision_type == DecisionType.CHARACTER_ACTION:
            if not self.character:
                errors.append("CHARACTER_ACTION requires a character")
            if not self.narrative_text:
                errors.append("CHARACTER_ACTION requires narrative_text")

        elif self.decision_type == DecisionType.RELATIONSHIP_CHANGE:
            if not self.character:
                errors.append("RELATIONSHIP_CHANGE requires a character")
            # Should have relationship target in metadata
            if "target_character" not in (self.__dict__.get("metadata", {}) or {}):
                errors.append("RELATIONSHIP_CHANGE requires target_character")

        elif self.decision_type == DecisionType.PLOT_TWIST:
            if not self.narrative_text:
                errors.append("PLOT_TWIST requires narrative_text")

        # Check for contradictions (simple check)
        if self.character and self.character in story_state.characters:
            char = story_state.characters[self.character]
            # Check if character is dead but action is proposed
            if (
                char.attributes.get("status") == "dead"
                and self.decision_type == DecisionType.CHARACTER_ACTION
            ):
                errors.append(f"Character '{self.character}' is dead and cannot perform actions")

        self.validation_errors = errors
        self.validated = len(errors) == 0

        return self.validated, errors

    def to_event(self) -> "Event":
        """Convert decision to an Event for timeline."""
        from .story_state import Event

        return Event(
            event_id=f"event_{self.decision_id}",
            timestamp=self.timestamp,
            description=self.description,
            character=self.character,
            location=self.location,
            category=self.decision_type.value,
            importance=self.importance,
            narrative_text=self.narrative_text or self.description,
        )


class DecisionValidator:
    """Validates narrative decisions against story coherence."""

    @staticmethod
    def validate_decision(
        decision: NarrativeDecision, story_state: "StoryState"
    ) -> tuple[bool, list[str]]:
        """Validate a decision."""
        return decision.validate(story_state)

    @staticmethod
    def check_coherence(decision: NarrativeDecision, story_state: "StoryState") -> float:
        """
        Check how well decision fits with existing story.

        Returns:
            Coherence score (0.0 to 1.0)
        """
        score = 1.0

        # Penalize if character doesn't exist
        if decision.character and decision.character not in story_state.characters:
            score -= 0.3

        # Reward if character has been active recently
        if decision.character and decision.character in story_state.characters:
            char = story_state.characters[decision.character]
            if char.last_appearance:
                time_since = (datetime.utcnow() - char.last_appearance).total_seconds()
                # Recent appearance is good (within 24 hours = no penalty)
                if time_since > 86400:  # 24 hours
                    score -= 0.1

        # Check if decision type matches story phase
        if len(story_state.timeline) < 3:
            # Early story - prefer character actions and world building
            if decision.decision_type in [DecisionType.CONFLICT_RESOLUTION]:
                score -= 0.2
        else:
            # Later story - prefer plot twists and conflict
            if decision.decision_type in [DecisionType.WORLD_BUILDING]:
                score -= 0.1

        return max(0.0, min(1.0, score))
