"""
Status State Models - Typed State Management (inspired by AI-DnD patterns)

Provides typed dataclasses for WAFT status state with computed properties,
following the pattern from AI-DnD's CharacterState with hp_percent property.

Benefits:
- Type safety and IDE autocomplete
- Computed properties for derived metrics
- Clear data structure
- Easier testing
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class EpistemicState:
    """
    Epistemic state with computed properties (inspired by AI-DnD CharacterState).

    Stores base values and computes derived metrics via @property decorators.
    """

    initialized: bool = False
    knowledge_pct: float = 0.0
    uncertainty_pct: float = 0.0
    moon_phase: str = "🌑"
    moon_phase_desc: str = "Unknown"
    vectors: dict[str, Any] = field(default_factory=dict)
    message: str | None = None

    @property
    def coverage_pct(self) -> float:
        """
        Total epistemic coverage (computed property).

        Formula: Average of knowledge and (100 - uncertainty)
        This gives a balanced view of both what we know and what we're not uncertain about.
        """
        if not self.initialized:
            return 0.0
        # Average of knowledge and certainty (100 - uncertainty)
        certainty = 100.0 - self.uncertainty_pct
        return (self.knowledge_pct + certainty) / 2.0

    @property
    def health_status(self) -> str:
        """
        Health indicator based on coverage (computed property).

        Returns:
            "Excellent", "Good", "Moderate", or "Low"
        """
        if not self.initialized:
            return "Unknown"

        coverage = self.coverage_pct
        if coverage >= 90:
            return "Excellent"
        elif coverage >= 75:
            return "Good"
        elif coverage >= 50:
            return "Moderate"
        else:
            return "Low"

    @property
    def knowledge_ratio(self) -> float:
        """Knowledge as ratio (0.0-1.0)."""
        return self.knowledge_pct / 100.0 if self.initialized else 0.0

    @property
    def uncertainty_ratio(self) -> float:
        """Uncertainty as ratio (0.0-1.0)."""
        return self.uncertainty_pct / 100.0 if self.initialized else 1.0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary (for backward compatibility)."""
        return {
            "initialized": self.initialized,
            "knowledge_pct": self.knowledge_pct,
            "uncertainty_pct": self.uncertainty_pct,
            "moon_phase": self.moon_phase,
            "moon_phase_desc": self.moon_phase_desc,
            "vectors": self.vectors,
            "message": self.message,
            "coverage_pct": self.coverage_pct,
            "health_status": self.health_status,
        }


@dataclass
class GamificationState:
    """
    Gamification state with computed properties (inspired by AI-DnD CharacterState).

    Stores base values and computes derived metrics via @property decorators.
    """

    available: bool = False
    level: int = 1
    integrity: float = 100.0
    insight: float = 0.0
    achievements_count: int = 0
    achievements: list[str] = field(default_factory=list)

    @property
    def integrity_status(self) -> str:
        """
        Integrity status indicator (computed property).

        Returns:
            "Excellent", "Good", "Fair", or "Poor"
        """
        if not self.available:
            return "Unknown"

        if self.integrity >= 90:
            return "Excellent"
        elif self.integrity >= 75:
            return "Good"
        elif self.integrity >= 50:
            return "Fair"
        else:
            return "Poor"

    @property
    def integrity_ratio(self) -> float:
        """Integrity as ratio (0.0-1.0)."""
        return self.integrity / 100.0 if self.available else 0.0

    @property
    def next_level_xp(self) -> float:
        """
        XP needed for next level (example formula, inspired by AI-DnD).

        Formula: 1000 * (level ** 1.5)
        """
        if not self.available:
            return 0.0
        return 1000.0 * (self.level**1.5)

    @property
    def level_progress_pct(self) -> float:
        """
        Progress toward next level as percentage.

        Assumes current insight is progress toward next_level_xp.
        """
        if not self.available or self.next_level_xp <= 0:
            return 0.0
        return min((self.insight / self.next_level_xp) * 100, 100.0)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary (for backward compatibility)."""
        return {
            "available": self.available,
            "level": self.level,
            "integrity": self.integrity,
            "insight": self.insight,
            "achievements_count": self.achievements_count,
            "achievements": self.achievements,
            "integrity_status": self.integrity_status,
            "level_progress_pct": self.level_progress_pct,
        }


@dataclass
class ProjectHealthState:
    """
    Project health state with computed properties.
    """

    pyrite_valid: bool = False
    structure_valid: bool = False
    lock_exists: bool = False
    genesis_files_count: int = 0
    genesis_files_total: int = 3

    @property
    def health_score(self) -> float:
        """
        Overall health score (0.0-100.0).

        Formula: Average of all health indicators
        """
        indicators = [
            100.0 if self.pyrite_valid else 0.0,
            100.0 if self.structure_valid else 0.0,
            100.0 if self.lock_exists else 0.0,
            (self.genesis_files_count / self.genesis_files_total * 100.0)
            if self.genesis_files_total > 0
            else 0.0,
        ]
        return sum(indicators) / len(indicators) if indicators else 0.0

    @property
    def health_status(self) -> str:
        """Health status indicator."""
        score = self.health_score
        if score >= 90:
            return "Excellent"
        elif score >= 75:
            return "Good"
        elif score >= 50:
            return "Fair"
        else:
            return "Poor"

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary (for backward compatibility)."""
        return {
            "pyrite_valid": self.pyrite_valid,
            "structure_valid": self.structure_valid,
            "lock_exists": self.lock_exists,
            "genesis_files_count": self.genesis_files_count,
            "genesis_files_total": self.genesis_files_total,
            "health_score": self.health_score,
            "health_status": self.health_status,
        }


@dataclass
class StatusState:
    """
    Complete typed status state (inspired by AI-DnD game state management).

    Provides type safety and computed properties for all status data.
    """

    epistemic: EpistemicState = field(default_factory=EpistemicState)
    gamification: GamificationState = field(default_factory=GamificationState)
    project_health: ProjectHealthState = field(default_factory=ProjectHealthState)
    flight_events: list[dict[str, Any]] = field(default_factory=list)
    git_status: dict[str, Any] = field(default_factory=dict)
    epistemic_phase: str = "Unknown"
    work_efforts: dict[str, Any] = field(default_factory=dict)
    recent_activity: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    @property
    def overall_health_score(self) -> float:
        """
        Overall system health score (0.0-100.0).

        Combines epistemic coverage, gamification integrity, and project health.
        """
        epistemic_score = self.epistemic.coverage_pct if self.epistemic.initialized else 50.0
        gamification_score = self.gamification.integrity if self.gamification.available else 50.0
        project_score = self.project_health.health_score

        # Weighted average
        return epistemic_score * 0.3 + gamification_score * 0.3 + project_score * 0.4

    @property
    def overall_health_status(self) -> str:
        """Overall health status indicator."""
        score = self.overall_health_score
        if score >= 90:
            return "Excellent"
        elif score >= 75:
            return "Good"
        elif score >= 50:
            return "Fair"
        else:
            return "Poor"

    @classmethod
    def from_dict(cls, status_dict: dict[str, Any]) -> "StatusState":
        """
        Create StatusState from status dictionary (backward compatibility).

        Args:
            status_dict: Status dictionary from check_status()

        Returns:
            StatusState instance
        """
        # Extract nested states
        epistemic_data = status_dict.get("epistemic_state", {})
        gamification_data = status_dict.get("gamification_state", {})
        health_data = status_dict.get("project_health", {})

        # Create typed states
        epistemic = EpistemicState(
            initialized=epistemic_data.get("initialized", False),
            knowledge_pct=epistemic_data.get("knowledge_pct", 0.0),
            uncertainty_pct=epistemic_data.get("uncertainty_pct", 0.0),
            moon_phase=epistemic_data.get("moon_phase", "🌑"),
            moon_phase_desc=epistemic_data.get("moon_phase_desc", "Unknown"),
            vectors=epistemic_data.get("vectors", {}),
            message=epistemic_data.get("message"),
        )

        gamification = GamificationState(
            available=gamification_data.get("available", False),
            level=gamification_data.get("level", 1),
            integrity=gamification_data.get("integrity", 100.0),
            insight=gamification_data.get("insight", 0.0),
            achievements_count=gamification_data.get("achievements_count", 0),
            achievements=gamification_data.get("achievements", []),
        )

        project_health = ProjectHealthState(
            pyrite_valid=health_data.get("pyrite_valid", False),
            structure_valid=health_data.get("structure_valid", False),
            lock_exists=health_data.get("lock_exists", False),
            genesis_files_count=health_data.get("genesis_files_count", 0),
            genesis_files_total=health_data.get("genesis_files_total", 3),
        )

        return cls(
            epistemic=epistemic,
            gamification=gamification,
            project_health=project_health,
            flight_events=status_dict.get("flight_recorder_events", []),
            git_status=status_dict.get("git_status", {}),
            epistemic_phase=status_dict.get("epistemic_phase", "Unknown"),
            work_efforts=status_dict.get("work_efforts", {}),
            recent_activity=status_dict.get("recent_activity", {}),
            timestamp=datetime.utcnow(),
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert to dictionary (for backward compatibility with existing code).

        Returns:
            Dictionary compatible with existing status dict format
        """
        return {
            "epistemic_state": self.epistemic.to_dict(),
            "gamification_state": self.gamification.to_dict(),
            "project_health": self.project_health.to_dict(),
            "flight_recorder_events": self.flight_events,
            "git_status": self.git_status,
            "epistemic_phase": self.epistemic_phase,
            "work_efforts": self.work_efforts,
            "recent_activity": self.recent_activity,
            "overall_health_score": self.overall_health_score,
            "overall_health_status": self.overall_health_status,
            "timestamp": self.timestamp.isoformat(),
        }
