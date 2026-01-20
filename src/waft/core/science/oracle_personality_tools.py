"""
Oracle Personality Tools

Utilities for managing and evolving Oracle personality.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .oracle_personality import OraclePersonality, OraclePersonalityType


class PersonalityManager:
    """Manages Oracle personality evolution and customization."""

    def __init__(self, project_path: Path):
        """Initialize personality manager."""
        self.project_path = Path(project_path)
        self.personality_file = project_path / ".empirica" / "oracle_personality.json"
        self.interaction_history_file = project_path / ".empirica" / "oracle_interactions.jsonl"

    def load_personality(self) -> OraclePersonality:
        """Load personality from file or create default."""
        if self.personality_file.exists():
            try:
                return OraclePersonality.from_file(self.personality_file)
            except Exception:
                pass

        return OraclePersonality()

    def save_personality(self, personality: OraclePersonality) -> None:
        """Save personality to file."""
        personality.save_to_file(self.personality_file)

    def evolve_personality(
        self, personality: OraclePersonality, feedback: dict[str, Any], learning_rate: float = 0.1
    ) -> OraclePersonality:
        """
        Evolve personality based on feedback.

        Args:
            personality: Current personality
            feedback: Feedback dict with trait adjustments
            learning_rate: How quickly to adapt (0.0-1.0)

        Returns:
            Evolved personality
        """
        # Create new personality data
        new_data = personality.data.copy()

        # Adjust traits based on feedback
        if "trait_adjustments" in feedback:
            traits = new_data.get("traits", {})
            for trait, adjustment in feedback["trait_adjustments"].items():
                if trait in traits:
                    current = traits[trait]
                    adjustment_value = adjustment * learning_rate
                    traits[trait] = max(0.0, min(1.0, current + adjustment_value))

        # Adjust communication style
        if "style_adjustments" in feedback:
            style = new_data.get("communication_style", {})
            for key, value in feedback["style_adjustments"].items():
                if key in style:
                    if isinstance(style[key], (int, float)):
                        style[key] = max(0.0, min(1.0, style[key] + (value * learning_rate)))
                    else:
                        style[key] = value

        return OraclePersonality(new_data)

    def log_interaction(self, interaction: dict[str, Any]) -> None:
        """Log an interaction for personality analysis."""
        self.interaction_history_file.parent.mkdir(parents=True, exist_ok=True)

        interaction["timestamp"] = datetime.now().isoformat()

        with open(self.interaction_history_file, "a") as f:
            f.write(json.dumps(interaction) + "\n")

    def analyze_interactions(self, limit: int = 100) -> dict[str, Any]:
        """
        Analyze interaction history to suggest personality adjustments.

        Args:
            limit: Maximum number of interactions to analyze

        Returns:
            Analysis dict with suggested adjustments
        """
        if not self.interaction_history_file.exists():
            return {"suggestions": []}

        interactions = []
        with open(self.interaction_history_file) as f:
            for line in f:
                try:
                    interactions.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        # Analyze last N interactions
        recent = interactions[-limit:] if len(interactions) > limit else interactions

        # Simple analysis: count positive/negative feedback
        positive_count = sum(1 for i in recent if i.get("feedback", {}).get("positive", False))
        negative_count = sum(1 for i in recent if i.get("feedback", {}).get("negative", False))

        suggestions = []

        # Suggest adjustments based on feedback patterns
        if positive_count > negative_count * 2:
            # Mostly positive - could increase confidence traits
            suggestions.append(
                {
                    "trait": "wisdom",
                    "adjustment": 0.1,
                    "reason": "High positive feedback suggests wisdom is valued",
                }
            )

        if negative_count > positive_count:
            # Mostly negative - might need more practicality
            suggestions.append(
                {
                    "trait": "practicality",
                    "adjustment": 0.1,
                    "reason": "Negative feedback suggests need for more practical guidance",
                }
            )

        return {
            "total_interactions": len(recent),
            "positive_feedback": positive_count,
            "negative_feedback": negative_count,
            "suggestions": suggestions,
        }

    def create_personality_from_template(
        self, template_name: str, customizations: dict[str, Any] | None = None
    ) -> OraclePersonality:
        """
        Create personality from template with customizations.

        Args:
            template_name: Template name (wise_mentor, analytical_scientist, etc.)
            customizations: Optional dict of customizations

        Returns:
            Customized personality
        """
        try:
            personality_type = OraclePersonalityType(template_name)
            personality = OraclePersonality.from_preset(personality_type)
        except ValueError:
            # Unknown template, use default
            personality = OraclePersonality()

        if customizations:
            # Apply customizations
            if "traits" in customizations:
                for trait, value in customizations["traits"].items():
                    if "traits" not in personality.data:
                        personality.data["traits"] = {}
                    personality.data["traits"][trait] = max(0.0, min(1.0, value))

            if "communication_style" in customizations:
                personality.data["communication_style"].update(
                    customizations["communication_style"]
                )

        return personality
