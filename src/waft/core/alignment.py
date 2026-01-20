"""
Alignment System: Calculate alignment between Arrow of Intent and outcomes/interpretations.

Alignment is the measure of how well beings' intentions align with each other
and with their environment. Perfect alignment generates pleasure, while misalignment
causes friction and pain.
"""

from typing import Any

from .harm import ArrowOfIntent, Harm, Help


class AlignmentSystem:
    """
    Calculates alignment between beings' Arrows of Intent and outcomes.

    Alignment score (0.0-1.0):
    - 1.0 = perfect alignment (parallel arrows, matching outcomes)
    - 0.0 = no alignment (perpendicular arrows, mismatched outcomes)
    - Negative values = misalignment (opposite arrows, conflicting outcomes)
    """

    def calculate_alignment_between_beings(
        self, arrow1: ArrowOfIntent, arrow2: ArrowOfIntent
    ) -> float:
        """
        Calculate alignment between two beings' Arrows of Intent.

        Uses cosine similarity:
        - Parallel arrows (same direction) = 1.0
        - Perpendicular arrows = 0.0
        - Opposite arrows = -1.0

        Args:
            arrow1: First being's Arrow of Intent
            arrow2: Second being's Arrow of Intent

        Returns:
            Alignment score (-1.0 to 1.0)
        """
        return arrow1.cosine_similarity(arrow2)

    def calculate_alignment_with_environment(
        self,
        arrow: ArrowOfIntent,
        stimulus: dict[str, Any],
        being_goals: list[dict[str, Any]],
        being_personality: dict[str, Any],
    ) -> float:
        """
        Calculate alignment between a being's Arrow of Intent and environment/stimulus.

        Measures how well the stimulus matches the being's goals and personality.

        Args:
            arrow: Being's Arrow of Intent
            stimulus: Environmental stimulus or event
            being_goals: Being's lifetime goals
            being_personality: Being's personality traits

        Returns:
            Alignment score (0.0-1.0)
        """
        # Calculate goal alignment
        goal_alignment = self._calculate_goal_alignment(stimulus, being_goals)

        # Calculate personality alignment
        personality_alignment = self._calculate_personality_alignment(stimulus, being_personality)

        # Combined alignment (weighted average)
        alignment = goal_alignment * 0.6 + personality_alignment * 0.4

        return max(0.0, min(1.0, alignment))

    def calculate_alignment_with_outcome(
        self, intended_arrow: ArrowOfIntent, actual_arrow: ArrowOfIntent
    ) -> float:
        """
        Calculate alignment between intended outcome and actual outcome.

        Measures how well the actual outcome matches the intended outcome.

        Args:
            intended_arrow: Arrow representing intended outcome
            actual_arrow: Arrow representing actual outcome

        Returns:
            Alignment score (-1.0 to 1.0)
        """
        return intended_arrow.cosine_similarity(actual_arrow)

    def calculate_harm_help_alignment(
        self,
        source_arrow: ArrowOfIntent,
        target_arrow: ArrowOfIntent,
        harm_or_help: Harm | None = None,
        help_event: Help | None = None,
    ) -> float:
        """
        Calculate alignment between source and target for Harm/Help events.

        This determines how the target being interprets the source's intent.
        High alignment = target feels pleasure from help or less pain from harm.
        Low alignment = target feels pain from harm or less pleasure from help.

        Args:
            source_arrow: Source being's Arrow of Intent
            target_arrow: Target being's Arrow of Intent
            harm_or_help: Optional Harm event
            help_event: Optional Help event

        Returns:
            Alignment score (-1.0 to 1.0)
        """
        # Base alignment from arrow similarity
        base_alignment = source_arrow.cosine_similarity(target_arrow)

        # Adjust based on intentionality
        if harm_or_help:
            if harm_or_help.intentional:
                # Intentional harm with misalignment = more pain
                # Intentional harm with alignment = less pain (target understands)
                return base_alignment * 0.5  # Reduce alignment impact for intentional harm
            else:
                # Unintentional harm - alignment helps reduce pain
                return base_alignment * 0.8  # Alignment helps more for unintentional

        if help_event:
            if help_event.intentional:
                # Intentional help with alignment = more pleasure
                return base_alignment * 1.2  # Boost alignment for intentional help
            else:
                # Unintentional help - still positive but less impactful
                return base_alignment * 0.9

        return base_alignment

    def alignment_to_pleasure(self, alignment_score: float) -> float:
        """
        Convert alignment score to pleasure value.

        Args:
            alignment_score: Alignment score (-1.0 to 1.0)

        Returns:
            Pleasure value (0.0-1.0)
        """
        # Map [-1.0, 1.0] to [0.0, 1.0]
        # Negative alignment = 0.0 pleasure
        # Positive alignment = scaled to pleasure
        if alignment_score <= 0.0:
            return 0.0

        return min(1.0, alignment_score)

    def alignment_to_pain(self, alignment_score: float) -> float:
        """
        Convert alignment score to pain value.

        Args:
            alignment_score: Alignment score (-1.0 to 1.0)

        Returns:
            Pain value (0.0-1.0)
        """
        # Map [-1.0, 1.0] to [0.0, 1.0]
        # Negative alignment = pain
        # Positive alignment = 0.0 pain
        if alignment_score >= 0.0:
            return 0.0

        # Convert negative alignment to pain
        return min(1.0, abs(alignment_score))

    def _calculate_goal_alignment(
        self, stimulus: dict[str, Any], goals: list[dict[str, Any]]
    ) -> float:
        """Calculate how well stimulus aligns with goals."""
        if not goals:
            return 0.5  # Neutral if no goals

        stimulus_description = str(stimulus.get("description", "")).lower()
        stimulus_type = str(stimulus.get("type", "neutral")).lower()

        alignment_scores = []
        for goal in goals:
            goal_description = str(goal.get("description", "")).lower()
            goal_type = str(goal.get("type", "general")).lower()

            # Check if stimulus advances goal
            if goal_type in stimulus_description or goal_description in stimulus_description:
                alignment_scores.append(0.8)
            elif stimulus_type == "positive":
                alignment_scores.append(0.6)  # Positive experiences generally help
            elif stimulus_type == "negative":
                alignment_scores.append(0.2)  # Negative experiences generally hinder
            else:
                alignment_scores.append(0.5)  # Neutral

        if alignment_scores:
            return sum(alignment_scores) / len(alignment_scores)

        return 0.5

    def _calculate_personality_alignment(
        self, stimulus: dict[str, Any], personality: dict[str, Any]
    ) -> float:
        """Calculate how well stimulus aligns with personality."""
        personality_type = personality.get("type", "balanced")
        stimulus_type = str(stimulus.get("type", "neutral")).lower()
        stimulus_description = str(stimulus.get("description", "")).lower()

        # Base alignment
        alignment = 0.5

        # Adjust based on personality type
        if personality_type == "analytical":
            if "learn" in stimulus_description or "skill" in stimulus_description:
                alignment = 0.8
            elif stimulus_type == "positive":
                alignment = 0.6
        elif personality_type == "creative":
            if "explore" in stimulus_description or "discover" in stimulus_description:
                alignment = 0.8
            elif stimulus_type == "positive":
                alignment = 0.6
        elif personality_type == "systematic":
            if "goal" in stimulus_description or "progress" in stimulus_description:
                alignment = 0.8
            elif stimulus_type == "positive":
                alignment = 0.6
        else:  # balanced, intuitive
            if stimulus_type == "positive":
                alignment = 0.6
            elif stimulus_type == "negative":
                alignment = 0.4

        return alignment
