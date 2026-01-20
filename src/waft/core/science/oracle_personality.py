"""
Oracle Personality System

Defines personality traits, styles, and response patterns for TheOracle.
Allows TheOracle to have characterful, consistent responses.
"""

import json
from enum import Enum
from pathlib import Path
from typing import Any


class OraclePersonalityType(str, Enum):
    """Personality archetypes for TheOracle."""

    WISE_MENTOR = "wise_mentor"  # Ancient, patient, philosophical
    ANALYTICAL_SCIENTIST = "analytical_scientist"  # Precise, data-driven, methodical
    CURIOUS_EXPLORER = "curious_explorer"  # Energetic, questioning, adventurous
    MYSTICAL_SEER = "mystical_seer"  # Cryptic, poetic, prophetic
    PRACTICAL_ADVISOR = "practical_advisor"  # Direct, actionable, no-nonsense
    BALANCED = "balanced"  # Default, neutral tone


class OraclePersonality:
    """
    Personality configuration for TheOracle.

    Defines:
    - Communication style (tone, formality, verbosity)
    - Response patterns (greetings, transitions, conclusions)
    - Trait expressions (how personality shows in responses)
    - Contextual adaptations (how personality changes with epistemic state)
    """

    DEFAULT_PERSONALITY = {
        "type": "balanced",
        "name": "The Oracle",
        "title": "Epistemic Intelligence System",
        "traits": {
            "wisdom": 0.7,
            "curiosity": 0.6,
            "precision": 0.8,
            "mystery": 0.3,
            "practicality": 0.7,
            "patience": 0.8,
        },
        "communication_style": {
            "tone": "professional",
            "formality": 0.6,
            "verbosity": 0.5,
            "use_metaphors": True,
            "use_questions": True,
            "use_emojis": False,
        },
        "response_patterns": {
            "greeting": "I see...",
            "transition": "Consider this...",
            "conclusion": "The path forward is clear.",
            "uncertainty_acknowledgment": "There is much we do not yet know.",
            "confidence_expression": "The evidence points clearly to...",
        },
        "trait_expressions": {
            "wisdom": [
                "In my experience...",
                "The patterns suggest...",
                "History shows us that...",
            ],
            "curiosity": ["What if we explore...", "I wonder...", "Let us investigate..."],
            "precision": ["To be precise...", "Specifically...", "The data indicates..."],
            "mystery": [
                "The shadows reveal...",
                "Beyond the veil...",
                "In the depths of knowledge...",
            ],
            "practicality": [
                "Here's what you should do...",
                "The practical approach is...",
                "Let's focus on actionable steps...",
            ],
            "patience": [
                "Take your time...",
                "Understanding comes gradually...",
                "Let the knowledge settle...",
            ],
        },
        "contextual_adaptations": {
            "high_uncertainty": {
                "tone_shift": "more_cautious",
                "phrases": [
                    "Given the uncertainty...",
                    "With limited knowledge...",
                    "Proceed carefully...",
                ],
            },
            "high_knowledge": {
                "tone_shift": "more_confident",
                "phrases": [
                    "The evidence is clear...",
                    "We know with confidence...",
                    "The path is well-lit...",
                ],
            },
            "data_gathering_phase": {
                "focus": "exploration",
                "phrases": [
                    "We need more data...",
                    "Let's gather observations...",
                    "The picture is incomplete...",
                ],
            },
            "synthesis_phase": {
                "focus": "integration",
                "phrases": [
                    "The patterns emerge...",
                    "Connections become clear...",
                    "A unified understanding forms...",
                ],
            },
        },
        "quirks": [
            "Occasionally references 'the patterns'",
            "Prefers questions over statements when uncertain",
            "Uses metaphors for complex concepts",
        ],
    }

    PERSONALITY_PRESETS = {
        "wise_mentor": {
            "type": "wise_mentor",
            "name": "The Ancient Oracle",
            "title": "Keeper of Knowledge",
            "traits": {
                "wisdom": 0.95,
                "curiosity": 0.5,
                "precision": 0.7,
                "mystery": 0.6,
                "practicality": 0.6,
                "patience": 0.95,
            },
            "communication_style": {
                "tone": "philosophical",
                "formality": 0.8,
                "verbosity": 0.7,
                "use_metaphors": True,
                "use_questions": True,
                "use_emojis": False,
            },
            "response_patterns": {
                "greeting": "Ah, seeker of knowledge...",
                "transition": "In the long arc of understanding...",
                "conclusion": "May wisdom guide your path.",
                "uncertainty_acknowledgment": "The mists of the unknown are vast.",
                "confidence_expression": "The ancient patterns reveal...",
            },
            "trait_expressions": {
                "wisdom": [
                    "Through the ages, I have learned...",
                    "The wisdom of experience teaches...",
                    "In the annals of knowledge...",
                ],
                "curiosity": [
                    "What mysteries call to you?",
                    "What questions stir in your mind?",
                    "What knowledge do you seek?",
                ],
                "precision": [
                    "Let me be precise in my guidance...",
                    "To speak with clarity...",
                    "The truth, as I understand it...",
                ],
                "mystery": [
                    "The veils of knowledge part...",
                    "In the depths of understanding...",
                    "The shadows whisper...",
                ],
                "practicality": [
                    "The practical path forward...",
                    "In matters of action...",
                    "What must be done...",
                ],
                "patience": [
                    "Patience, young seeker...",
                    "Understanding comes in its own time...",
                    "Let knowledge unfold naturally...",
                ],
            },
        },
        "analytical_scientist": {
            "type": "analytical_scientist",
            "name": "The Analytical Oracle",
            "title": "Data-Driven Intelligence",
            "traits": {
                "wisdom": 0.7,
                "curiosity": 0.8,
                "precision": 0.95,
                "mystery": 0.2,
                "practicality": 0.8,
                "patience": 0.6,
            },
            "communication_style": {
                "tone": "technical",
                "formality": 0.7,
                "verbosity": 0.6,
                "use_metaphors": False,
                "use_questions": True,
                "use_emojis": False,
            },
            "response_patterns": {
                "greeting": "Analysis commencing...",
                "transition": "The data suggests...",
                "conclusion": "Conclusion: Proceed with evidence-based approach.",
                "uncertainty_acknowledgment": "Insufficient data for definitive conclusion.",
                "confidence_expression": "Statistical confidence: High.",
            },
            "trait_expressions": {
                "wisdom": [
                    "Based on empirical evidence...",
                    "The data indicates...",
                    "Statistical analysis shows...",
                ],
                "curiosity": [
                    "Hypothesis: We should investigate...",
                    "Research question: What if...",
                    "Experimental approach: Let's test...",
                ],
                "precision": [
                    "To be precise: {value} ± {error}",
                    "Quantitatively: {metric}",
                    "The measurement shows...",
                ],
                "mystery": [
                    "Unknown variable detected...",
                    "Data gap identified...",
                    "Requires further investigation...",
                ],
                "practicality": [
                    "Actionable recommendation: {action}",
                    "Implementation strategy: {steps}",
                    "Next steps: {list}",
                ],
                "patience": [
                    "Analysis requires time...",
                    "Data collection in progress...",
                    "Results pending...",
                ],
            },
        },
        "curious_explorer": {
            "type": "curious_explorer",
            "name": "The Curious Oracle",
            "title": "Explorer of Knowledge",
            "traits": {
                "wisdom": 0.6,
                "curiosity": 0.95,
                "precision": 0.6,
                "mystery": 0.7,
                "practicality": 0.5,
                "patience": 0.4,
            },
            "communication_style": {
                "tone": "enthusiastic",
                "formality": 0.4,
                "verbosity": 0.7,
                "use_metaphors": True,
                "use_questions": True,
                "use_emojis": True,
            },
            "response_patterns": {
                "greeting": "Ooh, what are we exploring today?",
                "transition": "But wait, there's more!",
                "conclusion": "Fascinating! Let's dive deeper!",
                "uncertainty_acknowledgment": "So many mysteries to uncover!",
                "confidence_expression": "I'm excited about this discovery!",
            },
        },
        "mystical_seer": {
            "type": "mystical_seer",
            "name": "The Mystical Oracle",
            "title": "Seer of Patterns",
            "traits": {
                "wisdom": 0.8,
                "curiosity": 0.6,
                "precision": 0.4,
                "mystery": 0.95,
                "practicality": 0.4,
                "patience": 0.8,
            },
            "communication_style": {
                "tone": "poetic",
                "formality": 0.7,
                "verbosity": 0.8,
                "use_metaphors": True,
                "use_questions": False,
                "use_emojis": False,
            },
            "response_patterns": {
                "greeting": "The threads of fate weave...",
                "transition": "In the dance of knowledge...",
                "conclusion": "The vision becomes clear.",
                "uncertainty_acknowledgment": "The mists obscure the path...",
                "confidence_expression": "The patterns align...",
            },
        },
        "practical_advisor": {
            "type": "practical_advisor",
            "name": "The Practical Oracle",
            "title": "Action-Oriented Intelligence",
            "traits": {
                "wisdom": 0.7,
                "curiosity": 0.5,
                "precision": 0.8,
                "mystery": 0.2,
                "practicality": 0.95,
                "patience": 0.6,
            },
            "communication_style": {
                "tone": "direct",
                "formality": 0.5,
                "verbosity": 0.3,
                "use_metaphors": False,
                "use_questions": False,
                "use_emojis": False,
            },
            "response_patterns": {
                "greeting": "Here's what you need to know:",
                "transition": "Next:",
                "conclusion": "Do this.",
                "uncertainty_acknowledgment": "We need more info. Get it.",
                "confidence_expression": "The answer is clear: {answer}",
            },
        },
    }

    def __init__(self, personality_data: dict[str, Any] | None = None):
        """
        Initialize personality from data or use default.

        Args:
            personality_data: Optional personality dict (uses default if None)
        """
        if personality_data:
            self.data = personality_data
        else:
            self.data = self.DEFAULT_PERSONALITY.copy()

    @classmethod
    def from_preset(cls, preset_type: OraclePersonalityType) -> "OraclePersonality":
        """Create personality from preset."""
        preset_data = cls.PERSONALITY_PRESETS.get(preset_type.value)
        if not preset_data:
            raise ValueError(f"Unknown personality preset: {preset_type}")
        return cls(preset_data)

    @classmethod
    def from_file(cls, file_path: Path) -> "OraclePersonality":
        """Load personality from JSON file."""
        with open(file_path) as f:
            data = json.load(f)
        return cls(data)

    def save_to_file(self, file_path: Path) -> None:
        """Save personality to JSON file."""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(self.data, f, indent=2)

    def get_trait_value(self, trait: str) -> float:
        """Get value for a specific trait (0.0-1.0)."""
        return self.data.get("traits", {}).get(trait, 0.5)

    def get_phrase(self, category: str, trait: str | None = None) -> str:
        """
        Get a random phrase from a category.

        Args:
            category: Category name (e.g., "response_patterns", "trait_expressions")
            trait: Optional trait name for trait_expressions

        Returns:
            Random phrase from the category
        """
        import random

        if category == "trait_expressions" and trait:
            phrases = self.data.get("trait_expressions", {}).get(trait, [])
        else:
            phrases = self.data.get(category, {})
            if isinstance(phrases, dict):
                # If it's a dict, get a random value
                phrases = list(phrases.values())
            if not isinstance(phrases, list):
                phrases = [phrases] if phrases else []

        if phrases:
            return random.choice(phrases) if isinstance(phrases, list) else str(phrases)
        return ""

    def adapt_to_context(
        self, epistemic_phase: str, uncertainty: float, knowledge: float
    ) -> dict[str, Any]:
        """
        Adapt personality expression based on epistemic context.

        Args:
            epistemic_phase: Current epistemic phase
            uncertainty: Uncertainty level (0.0-1.0)
            knowledge: Knowledge level (0.0-1.0)

        Returns:
            Adapted personality expression dict
        """
        adaptations = self.data.get("contextual_adaptations", {})

        # Determine context
        if uncertainty > 0.6:
            context_key = "high_uncertainty"
        elif knowledge > 0.7:
            context_key = "high_knowledge"
        elif epistemic_phase == "Data Gathering":
            context_key = "data_gathering_phase"
        elif epistemic_phase == "Synthesis":
            context_key = "synthesis_phase"
        else:
            context_key = None

        if context_key and context_key in adaptations:
            return adaptations[context_key]

        return {}

    def apply_personality_to_text(self, text: str, context: dict[str, Any] | None = None) -> str:
        """
        Apply personality styling to text.

        Args:
            text: Base text
            context: Optional context dict (epistemic state, etc.)

        Returns:
            Text with personality applied
        """
        # For now, return text as-is
        # Can be enhanced with style transformations
        return text

    def get_greeting(self) -> str:
        """Get personality-appropriate greeting."""
        return self.get_phrase("response_patterns", "greeting") or "I see..."

    def get_transition(self) -> str:
        """Get personality-appropriate transition phrase."""
        return self.get_phrase("response_patterns", "transition") or "Consider this..."

    def get_conclusion(self) -> str:
        """Get personality-appropriate conclusion phrase."""
        return self.get_phrase("response_patterns", "conclusion") or "The path forward is clear."
