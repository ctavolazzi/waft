"""
Personality Alignment System: Calculate pleasure/pain from personality-goal-experience alignment.

Calculates how aligned a being's experiences are with their personality traits and goals,
generating pleasure (alignment) or pain (misalignment).
"""

from typing import Any


class PersonalityAlignment:
    """
    Calculates pleasure/pain based on personality-goal-experience alignment.

    Uses a simplified scoring system (can be enhanced with cosine similarity if needed).
    """

    def calculate_alignment(
        self, personality: dict[str, Any], goals: list[dict[str, Any]], experience: dict[str, Any]
    ) -> tuple[float, float]:
        """
        Calculate pleasure and pain scores.

        Simplified alignment calculation:
        - Personality alignment: Match experience type to personality preferences
        - Goal progress: Check if experience advances any goals
        - Experience intensity: Use experience intensity as multiplier

        Formula:
        - Alignment score: personality_match × goal_progress
        - Pleasure = alignment_score × positive_experience_intensity
        - Pain = (1 - alignment_score) × negative_experience_intensity

        Args:
            personality: Personality traits dict (from Being.personality)
            goals: Lifetime goals list (from Being.goals)
            experience: Experience dict from current cycle

        Returns:
            (pleasure, pain) tuple (0.0-1.0 each)
        """
        experience_type = experience.get("type", "neutral")
        experience_intensity = experience.get("intensity", 0.5)
        experience_description = experience.get("description", "")

        # Calculate personality match
        personality_match = self._calculate_personality_match(
            personality, experience_type, experience_description
        )

        # Calculate goal progress
        goal_progress = self._calculate_goal_progress(goals, experience)

        # Calculate alignment score
        alignment_score = (personality_match + goal_progress) / 2.0

        # Calculate pleasure and pain
        if experience_type == "positive":
            pleasure = alignment_score * experience_intensity
            pain = (
                (1.0 - alignment_score) * experience_intensity * 0.1
            )  # Minimal pain from positive experiences
        elif experience_type == "negative":
            pleasure = (
                alignment_score * experience_intensity * 0.1
            )  # Minimal pleasure from negative experiences
            pain = (1.0 - alignment_score) * experience_intensity
        else:  # neutral
            pleasure = alignment_score * experience_intensity * 0.3
            pain = (1.0 - alignment_score) * experience_intensity * 0.3

        # Clamp to 0.0-1.0
        pleasure = max(0.0, min(1.0, pleasure))
        pain = max(0.0, min(1.0, pain))

        return (pleasure, pain)

    def _calculate_personality_match(
        self, personality: dict[str, Any], experience_type: str, experience_description: str
    ) -> float:
        """
        Calculate how well experience matches personality.

        Args:
            personality: Personality traits dict
            experience_type: Type of experience (positive, negative, neutral)
            experience_description: Description of experience

        Returns:
            Match score (0.0-1.0)
        """
        # Simple matching based on personality type and experience type
        # Can be enhanced with more sophisticated personality trait matching

        personality_type = personality.get("type", "balanced")

        # Base match score
        match = 0.5  # Neutral base

        # Adjust based on experience type
        if experience_type == "positive":
            # Positive experiences generally align with most personalities
            match = 0.7
        elif experience_type == "negative":
            # Negative experiences generally misalign
            match = 0.3
        else:  # neutral
            match = 0.5

        # Adjust based on personality type preferences
        if personality_type == "analytical":
            # Analytical beings prefer learning/structured experiences
            if (
                "learn" in experience_description.lower()
                or "skill" in experience_description.lower()
            ):
                match = min(1.0, match + 0.2)
        elif personality_type == "creative":
            # Creative beings prefer exploration/novel experiences
            if (
                "explore" in experience_description.lower()
                or "discover" in experience_description.lower()
            ):
                match = min(1.0, match + 0.2)

        return match

    def _calculate_goal_progress(
        self, goals: list[dict[str, Any]], experience: dict[str, Any]
    ) -> float:
        """
        Calculate goal progress from experience.

        Args:
            goals: List of goal dicts
            experience: Experience dict

        Returns:
            Goal progress score (0.0-1.0)
        """
        if not goals:
            # No goals = neutral progress
            return 0.5

        # Check if experience advances any goals
        experience_description = experience.get("description", "").lower()

        progress_scores = []
        for goal in goals:
            goal_description = goal.get("description", "").lower()
            goal_type = goal.get("type", "general")

            # Simple keyword matching (can be enhanced)
            if goal_type in experience_description or goal_description in experience_description:
                progress_scores.append(0.8)  # Good progress
            else:
                progress_scores.append(0.3)  # Little progress

        # Average progress across all goals
        if progress_scores:
            return sum(progress_scores) / len(progress_scores)

        return 0.5  # Default neutral progress
