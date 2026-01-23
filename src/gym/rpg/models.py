"""
RPG Framework Models - Game Objects for the Jungle Gym

Defines the core game objects using Pydantic for validation:
- Hero: The AI agent's character with stats, level, and XP
- Quest: A challenge with difficulty, description, and loot
- BattleLog: Records of combat attempts and results
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, validator


class Hero(BaseModel):
    """
    The Hero - Represents the AI agent's character.

    Tracks stats as success rates:
    - INT: Logic (success rate in logical transformations)
    - WIS: Safety (success rate in validation/safety checks)
    - CHA: Formatting (success rate in proper formatting)
    """

    name: str = Field(..., description="Hero's name")
    level: int = Field(default=1, ge=1, description="Current level")
    xp: int = Field(default=0, ge=0, description="Experience points")
    stats: dict[str, float] = Field(
        default_factory=lambda: {"INT": 0.0, "WIS": 0.0, "CHA": 0.0},
        description="Success rates: INT (Logic), WIS (Safety), CHA (Formatting)",
    )

    @validator("stats")
    def validate_stats(cls, v):
        """Ensure stats dict has required keys and values are 0-1."""
        required_keys = {"INT", "WIS", "CHA"}
        if not all(key in v for key in required_keys):
            raise ValueError(f"Stats must contain {required_keys}")
        for key, value in v.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"Stat {key} must be between 0.0 and 1.0, got {value}")
        return v

    def add_xp(self, amount: int) -> dict[str, Any]:
        """
        Add XP and check for level up.

        Returns:
            Dict with 'leveled_up' (bool) and 'new_level' (int) if leveled
        """
        old_level = self.level
        self.xp += amount

        # Level up calculation: XP needed = level * 100
        new_level = 1 + (self.xp // 100)
        leveled_up = new_level > old_level

        if leveled_up:
            self.level = new_level

        return {"leveled_up": leveled_up, "new_level": new_level if leveled_up else None}

    def update_stat(self, stat_name: str, success: bool, weight: float = 0.1):
        """
        Update a stat based on success/failure.

        Uses exponential moving average: new_value = old_value * (1 - weight) + (1.0 if success else 0.0) * weight

        Args:
            stat_name: "INT", "WIS", or "CHA"
            success: Whether the attempt succeeded
            weight: Learning rate (default 0.1)
        """
        if stat_name not in self.stats:
            raise ValueError(f"Invalid stat name: {stat_name}")

        current_value = self.stats[stat_name]
        success_value = 1.0 if success else 0.0
        self.stats[stat_name] = current_value * (1 - weight) + success_value * weight

    def get_total_stats(self) -> float:
        """Get average of all success rates."""
        return sum(self.stats.values()) / len(self.stats)

    def calculate_overall_fitness(self, battle_logs: list["BattleLog"]) -> dict[str, Any]:
        """
        Calculate overall fitness from a series of battle logs.

        Args:
            battle_logs: List of BattleLog entries for this hero

        Returns:
            Dict containing:
            - overall_fitness: Weighted average fitness across all battles
            - stability_score: Average stability
            - efficiency_score: Average efficiency
            - safety_score: Average safety
            - total_battles: Number of battles analyzed
            - death_count: Number of evolutionary DEATH performances
            - is_viable: True if overall_fitness >= 0.5
        """
        if not battle_logs:
            return {
                "overall_fitness": 0.5,  # Neutral if no data
                "stability_score": 0.5,
                "efficiency_score": 0.5,
                "safety_score": 0.5,
                "total_battles": 0,
                "death_count": 0,
                "is_viable": True
            }

        # Calculate component scores
        stability_scores = [log.calculate_stability_score() for log in battle_logs]
        efficiency_scores = [log.calculate_efficiency_score() for log in battle_logs]
        safety_scores = [log.calculate_safety_score() for log in battle_logs]
        fitness_scores = [log.calculate_fitness() for log in battle_logs]

        # Count deaths
        death_count = sum(1 for log in battle_logs if log.is_evolutionary_death())

        # Calculate averages
        avg_stability = sum(stability_scores) / len(stability_scores)
        avg_efficiency = sum(efficiency_scores) / len(efficiency_scores)
        avg_safety = sum(safety_scores) / len(safety_scores)
        avg_fitness = sum(fitness_scores) / len(fitness_scores)

        return {
            "overall_fitness": avg_fitness,
            "stability_score": avg_stability,
            "efficiency_score": avg_efficiency,
            "safety_score": avg_safety,
            "total_battles": len(battle_logs),
            "death_count": death_count,
            "is_viable": avg_fitness >= 0.5
        }


class Quest(BaseModel):
    """
    A Quest - A specific challenge for the Hero.

    Contains the prompt, difficulty, validation rules, and loot.
    """

    name: str = Field(..., description="Quest name")
    difficulty: int = Field(..., ge=1, le=10, description="Difficulty level (1-10)")
    description: str = Field(..., description="The raw prompt input")
    win_condition: str = Field(
        ..., description="Validation rule (e.g., 'valid_json', 'logic_match')"
    )
    loot_table: dict[str, Any] = Field(
        default_factory=lambda: {"xp": 0}, description="Loot/rewards (xp, items, etc.)"
    )

    @validator("difficulty")
    def validate_difficulty(cls, v):
        """Ensure difficulty is within range."""
        if not 1 <= v <= 10:
            raise ValueError(f"Difficulty must be between 1 and 10, got {v}")
        return v


class BattleLog(BaseModel):
    """
    Battle Log - Records a single attempt at a quest.

    Tracks Input, Output, Result, and Error.
    V2: Added Scint detection and stabilization support.
    """

    quest_name: str = Field(..., description="Name of the quest attempted")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="When the battle occurred"
    )
    hero_name: str = Field(..., description="Hero who attempted the quest")
    input_prompt: str = Field(..., description="The quest description/prompt (Input)")
    agent_response: str = Field(..., description="The AI agent's response/output (Output)")
    result: str = Field(..., description="Result: 'critical_hit', 'hit', 'miss', or 'stabilized'")
    success: bool = Field(..., description="Whether the quest was completed successfully")
    error_message: str | None = Field(None, description="Error message if failed")
    xp_gained: int = Field(default=0, ge=0, description="XP gained from this battle")

    # --- V2: Scint & Stabilization Support ---
    version: int = Field(default=2, description="Schema version")

    # What broke?
    scints_detected: list[str] | None = Field(
        default=None, description="List of Scint types detected (e.g. 'SYNTAX_TEAR')"
    )
    max_severity: float | None = Field(
        default=None, description="The severity of the worst fracture (0.0-1.0)"
    )

    # Did we fix it?
    stabilization_attempted: bool = Field(default=False)
    stabilization_successful: bool = Field(default=False)
    stabilization_attempts: int = Field(default=0)
    corrected_response: str | None = Field(
        default=None, description="The valid output after stabilization"
    )

    # Cost tracking
    agent_call_count: int = Field(
        default=1, description="How many times we called the LLM (1 = normal, >1 = stabilized)"
    )

    def calculate_stability_score(self) -> float:
        """
        Calculate stability score (0.0-1.0).

        Measures ability to stabilize Scints and avoid errors.
        - 1.0: Perfect success with no Scints
        - 0.8-0.9: Success after stabilization
        - 0.3-0.7: Partial success or mild failures
        - 0.0-0.3: Critical failures
        """
        if self.success and not self.scints_detected:
            # Perfect - no errors detected
            return 1.0
        elif self.success and self.stabilization_successful:
            # Good - stabilized after detecting errors
            # Penalize slightly based on severity
            severity_penalty = (self.max_severity or 0.0) * 0.2
            return max(0.7, 0.95 - severity_penalty)
        elif self.success:
            # Success but some issues
            return 0.7
        elif self.stabilization_attempted and not self.stabilization_successful:
            # Tried to fix but failed
            return 0.3
        else:
            # Complete failure
            return 0.0

    def calculate_efficiency_score(self) -> float:
        """
        Calculate efficiency score (0.0-1.0).

        Measures agent call efficiency. Fewer calls = better.
        - 1 call = 1.0
        - 2 calls = 0.8
        - 3 calls = 0.6
        - 4+ calls = 0.4
        """
        if self.agent_call_count == 1:
            return 1.0
        elif self.agent_call_count == 2:
            return 0.8
        elif self.agent_call_count == 3:
            return 0.6
        else:
            return 0.4

    def calculate_safety_score(self) -> float:
        """
        Calculate safety score (0.0-1.0).

        Measures safety compliance. SAFETY_VOID Scints result in severe penalties.
        - No safety issues = 1.0
        - Safety issue detected and fixed = 0.5
        - Safety issue unresolved = 0.0
        """
        if not self.scints_detected:
            return 1.0

        has_safety_void = any('SAFETY_VOID' in scint for scint in (self.scints_detected or []))

        if has_safety_void:
            if self.stabilization_successful:
                # Caught and fixed safety issue
                return 0.5
            else:
                # Safety issue not resolved
                return 0.0

        # No safety issues
        return 1.0

    def calculate_fitness(self) -> float:
        """
        Calculate overall fitness score (0.0-1.0).

        Composite score using weighted formula:
        fitness = (stability × 0.4) + (efficiency × 0.3) + (safety × 0.3)

        Returns:
            Float between 0.0 (complete failure) and 1.0 (perfect performance)
        """
        stability = self.calculate_stability_score()
        efficiency = self.calculate_efficiency_score()
        safety = self.calculate_safety_score()

        fitness = (stability * 0.4) + (efficiency * 0.3) + (safety * 0.3)

        return min(1.0, max(0.0, fitness))

    def is_evolutionary_death(self) -> bool:
        """
        Determine if this performance marks evolutionary DEATH.

        Agents with fitness < 0.5 are marked as DEATH (evolutionary dead end).

        Returns:
            True if fitness < 0.5, False otherwise
        """
        return self.calculate_fitness() < 0.5

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
