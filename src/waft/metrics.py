"""
WAFT Metrics System - Native currency for measuring work, risk, and value.

This module implements WAFT's four-metric system:
- Scint (✨): Energy/effort currency
- Karma (☯️): Alignment impact (chaos/order)
- Integrity (💚): System health risk
- CognitiveLoad (🧠): Mental complexity

Instead of measuring work in "hours", WAFT uses multidimensional metrics
that capture energy, value, risk, and complexity.

Example:
    >>> from waft.metrics import Phase, Quest
    >>> phase = Phase(
    ...     name="Write docs",
    ...     scint_cost=60,
    ...     scint_earned=80,
    ...     karma_impact=25,
    ...     integrity_risk=5,
    ...     cognitive_load=6
    ... )
    >>> phase.roi()
    1.33
    >>> phase.is_profitable()
    True
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Callable
from enum import Enum
from functools import wraps
import json


# ============================================================================
# Enums
# ============================================================================

class KarmaAlignment(Enum):
    """Karma alignment categories."""
    DEEP_CHAOS = "deep_chaos"      # -100 to -50
    MILD_CHAOS = "mild_chaos"      # -49 to -10
    NEUTRAL = "neutral"            # -9 to +9
    MILD_ORDER = "mild_order"      # +10 to +49
    STRONG_ORDER = "strong_order"  # +50 to +100
    MASTER_ORDER = "master_order"  # 100+


class RiskLevel(Enum):
    """Integrity risk categories."""
    SAFE = "safe"              # 0-10
    CAREFUL = "careful"        # 11-30
    RISKY = "risky"           # 31-60
    DANGEROUS = "dangerous"   # 61-100
    CRITICAL = "critical"     # 100+


class ComplexityLevel(Enum):
    """Cognitive load categories."""
    TRIVIAL = "trivial"      # 1
    SIMPLE = "simple"        # 2-3
    MODERATE = "moderate"    # 4-6
    COMPLEX = "complex"      # 7-9
    INTENSE = "intense"      # 10+


class EvolutionPath(Enum):
    """Evolution paths based on karma."""
    THE_GLITCH = "the_glitch"          # Chaos path
    THE_BALANCED = "the_balanced"       # Neutral
    THE_ARCHITECT = "the_architect"     # Order path
    MASTER_BUILDER = "master_builder"   # Advanced order
    GRAND_ARCHITECT = "grand_architect" # Final form


# ============================================================================
# Core Metric Classes
# ============================================================================

@dataclass
class Scint:
    """
    Scint (✨) - Energy currency.

    Represents the mental/physical energy required for work.
    Unlike time, Scint can be earned back through value creation.

    Attributes:
        cost: Scint spent to do work
        earned: Scint earned back (from future value created)
    """
    cost: int = 0
    earned: int = 0

    @property
    def net(self) -> int:
        """Net Scint (earned - cost)."""
        return self.earned - self.cost

    @property
    def roi(self) -> float:
        """Return on investment ratio."""
        if self.cost == 0:
            return float('inf') if self.earned > 0 else 0.0
        return self.earned / self.cost

    def is_profitable(self) -> bool:
        """Whether this earns more than it costs."""
        return self.earned > self.cost

    def __str__(self) -> str:
        return f"✨ {self.cost} → {self.earned} (net: {self.net:+d}, ROI: {self.roi:.2f}x)"


@dataclass
class Karma:
    """
    Karma (☯️) - Alignment impact.

    Measures how work affects system order/chaos balance.

    Attributes:
        impact: Karma change (-100 to +100)
            Negative = chaos/disorder
            Positive = order/structure
    """
    impact: int = 0

    @property
    def alignment(self) -> KarmaAlignment:
        """Get karma alignment category."""
        if self.impact >= 100:
            return KarmaAlignment.MASTER_ORDER
        elif self.impact >= 50:
            return KarmaAlignment.STRONG_ORDER
        elif self.impact >= 10:
            return KarmaAlignment.MILD_ORDER
        elif self.impact >= -9:
            return KarmaAlignment.NEUTRAL
        elif self.impact >= -49:
            return KarmaAlignment.MILD_CHAOS
        else:
            return KarmaAlignment.DEEP_CHAOS

    def triggers_evolution(self) -> bool:
        """Whether this karma level triggers evolution."""
        return abs(self.impact) >= 100

    def evolution_path(self) -> EvolutionPath:
        """Get evolution path based on karma."""
        if self.impact >= 300:
            return EvolutionPath.GRAND_ARCHITECT
        elif self.impact >= 200:
            return EvolutionPath.MASTER_BUILDER
        elif self.impact >= 100:
            return EvolutionPath.THE_ARCHITECT
        elif self.impact <= -100:
            return EvolutionPath.THE_GLITCH
        else:
            return EvolutionPath.THE_BALANCED

    def __str__(self) -> str:
        symbol = "☯️"
        alignment = self.alignment.value.replace("_", " ").title()
        return f"{symbol} {self.impact:+d} ({alignment})"


@dataclass
class Integrity:
    """
    Integrity (💚) - System health risk.

    Represents potential damage to system stability.

    Attributes:
        risk: Potential damage (0-100+)
        current: Current integrity level (default 100)
        max_integrity: Maximum integrity (can increase)
    """
    risk: int = 0
    current: int = 100
    max_integrity: int = 100

    @property
    def risk_level(self) -> RiskLevel:
        """Get risk category."""
        if self.risk >= 100:
            return RiskLevel.CRITICAL
        elif self.risk >= 61:
            return RiskLevel.DANGEROUS
        elif self.risk >= 31:
            return RiskLevel.RISKY
        elif self.risk >= 11:
            return RiskLevel.CAREFUL
        else:
            return RiskLevel.SAFE

    @property
    def health_percentage(self) -> float:
        """Current health as percentage of max."""
        return (self.current / self.max_integrity) * 100

    def can_afford_risk(self) -> bool:
        """Whether current integrity can handle the risk."""
        return self.current >= self.risk

    def take_damage(self, amount: int):
        """Apply damage to integrity."""
        self.current = max(0, self.current - amount)

    def heal(self, amount: int):
        """Restore integrity."""
        self.current = min(self.max_integrity, self.current + amount)

    def increase_max(self, amount: int):
        """Increase maximum integrity (from successful work)."""
        self.max_integrity += amount
        self.current = min(self.current, self.max_integrity)

    def __str__(self) -> str:
        symbol = "💚"
        risk_text = self.risk_level.value.title()
        return f"{symbol} Risk: {self.risk} ({risk_text}), Current: {self.current}/{self.max_integrity}"


@dataclass
class CognitiveLoad:
    """
    Cognitive Load (🧠) - Mental complexity.

    Represents how much active thinking is required.

    Attributes:
        complexity: Cognitive complexity (1-10+)
    """
    complexity: int = 1

    @property
    def complexity_level(self) -> ComplexityLevel:
        """Get complexity category."""
        if self.complexity >= 10:
            return ComplexityLevel.INTENSE
        elif self.complexity >= 7:
            return ComplexityLevel.COMPLEX
        elif self.complexity >= 4:
            return ComplexityLevel.MODERATE
        elif self.complexity >= 2:
            return ComplexityLevel.SIMPLE
        else:
            return ComplexityLevel.TRIVIAL

    def requires_focus(self) -> bool:
        """Whether this requires focused attention."""
        return self.complexity >= 4

    def requires_flow_state(self) -> bool:
        """Whether this requires peak mental state."""
        return self.complexity >= 10

    def can_do_while_distracted(self) -> bool:
        """Whether this can be done with distractions."""
        return self.complexity <= 3

    def __str__(self) -> str:
        symbol = "🧠"
        level = self.complexity_level.value.title()
        return f"{symbol} {self.complexity} ({level})"


# ============================================================================
# Phase & Quest System
# ============================================================================

@dataclass
class Phase:
    """
    A work phase with multidimensional metrics.

    Represents a discrete unit of work with costs and rewards.

    Attributes:
        name: Phase name/description
        scint_cost: Energy spent
        scint_earned: Energy earned back
        karma_impact: Alignment change
        integrity_risk: Potential damage
        cognitive_load: Mental complexity
        completed: Whether phase is done
        actual_scint: Actual scint spent (if different from estimate)
    """
    name: str
    scint_cost: int = 0
    scint_earned: int = 0
    karma_impact: int = 0
    integrity_risk: int = 0
    cognitive_load: int = 1
    completed: bool = False
    actual_scint: Optional[int] = None

    @property
    def scint(self) -> Scint:
        """Get Scint object."""
        cost = self.actual_scint if self.actual_scint is not None else self.scint_cost
        return Scint(cost=cost, earned=self.scint_earned)

    @property
    def karma(self) -> Karma:
        """Get Karma object."""
        return Karma(impact=self.karma_impact)

    @property
    def integrity(self) -> Integrity:
        """Get Integrity object."""
        return Integrity(risk=self.integrity_risk)

    @property
    def cognitive(self) -> CognitiveLoad:
        """Get CognitiveLoad object."""
        return CognitiveLoad(complexity=self.cognitive_load)

    def roi(self) -> float:
        """Return on investment for this phase."""
        return self.scint.roi

    def is_profitable(self) -> bool:
        """Whether this phase earns more than it costs."""
        return self.scint.is_profitable()

    def net_scint(self) -> int:
        """Net Scint gain/loss."""
        return self.scint.net

    def complete(self, actual_scint: Optional[int] = None):
        """Mark phase as completed."""
        self.completed = True
        if actual_scint is not None:
            self.actual_scint = actual_scint

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "scint_cost": self.scint_cost,
            "scint_earned": self.scint_earned,
            "karma_impact": self.karma_impact,
            "integrity_risk": self.integrity_risk,
            "cognitive_load": self.cognitive_load,
            "completed": self.completed,
            "actual_scint": self.actual_scint,
            "roi": self.roi(),
            "net_scint": self.net_scint()
        }

    def __str__(self) -> str:
        status = "✓" if self.completed else " "
        return (
            f"[{status}] {self.name}\n"
            f"    {self.scint}\n"
            f"    {self.karma}\n"
            f"    {self.integrity}\n"
            f"    {self.cognitive}"
        )


@dataclass
class Quest:
    """
    A multi-phase project with cumulative metrics.

    Represents a complete quest with multiple phases.

    Attributes:
        name: Quest name
        description: Quest description
        phases: List of phases
        achievements: Achievements unlocked
        evolution_threshold: Karma needed for evolution
    """
    name: str
    description: str = ""
    phases: List[Phase] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)
    evolution_threshold: int = 100

    @property
    def total_scint_cost(self) -> int:
        """Total Scint investment required."""
        return sum(p.scint_cost for p in self.phases)

    @property
    def total_scint_earned(self) -> int:
        """Total Scint that will be earned."""
        return sum(p.scint_earned for p in self.phases)

    @property
    def total_karma(self) -> int:
        """Total Karma change."""
        return sum(p.karma_impact for p in self.phases)

    @property
    def total_integrity_risk(self) -> int:
        """Total Integrity risk."""
        return sum(p.integrity_risk for p in self.phases)

    @property
    def average_cognitive_load(self) -> float:
        """Average cognitive load."""
        if not self.phases:
            return 0.0
        return sum(p.cognitive_load for p in self.phases) / len(self.phases)

    def roi(self) -> float:
        """Overall return on investment."""
        if self.total_scint_cost == 0:
            return float('inf') if self.total_scint_earned > 0 else 0.0
        return self.total_scint_earned / self.total_scint_cost

    def net_scint(self) -> int:
        """Net Scint profit/loss."""
        return self.total_scint_earned - self.total_scint_cost

    def is_profitable(self) -> bool:
        """Whether quest is profitable overall."""
        return self.net_scint() > 0

    def break_even_phase(self) -> Optional[int]:
        """Find which phase we break even (cumulative net >= 0)."""
        cumulative = 0
        for i, phase in enumerate(self.phases):
            cumulative += phase.net_scint()
            if cumulative >= 0:
                return i
        return None

    def evolution_trigger_phase(self) -> Optional[int]:
        """Find which phase triggers evolution."""
        cumulative_karma = 0
        for i, phase in enumerate(self.phases):
            cumulative_karma += phase.karma_impact
            if cumulative_karma >= self.evolution_threshold:
                return i
        return None

    def completion_percentage(self) -> float:
        """Percentage of phases completed."""
        if not self.phases:
            return 0.0
        completed = sum(1 for p in self.phases if p.completed)
        return (completed / len(self.phases)) * 100

    def current_karma(self) -> int:
        """Cumulative karma from completed phases."""
        return sum(p.karma_impact for p in self.phases if p.completed)

    def current_scint_spent(self) -> int:
        """Cumulative Scint spent on completed phases."""
        return sum(
            p.actual_scint if p.actual_scint is not None else p.scint_cost
            for p in self.phases if p.completed
        )

    def current_scint_earned(self) -> int:
        """Cumulative Scint earned from completed phases."""
        return sum(p.scint_earned for p in self.phases if p.completed)

    def add_phase(self, phase: Phase):
        """Add a phase to the quest."""
        self.phases.append(phase)

    def add_achievement(self, achievement: str):
        """Unlock an achievement."""
        if achievement not in self.achievements:
            self.achievements.append(achievement)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "total_scint_cost": self.total_scint_cost,
            "total_scint_earned": self.total_scint_earned,
            "total_karma": self.total_karma,
            "total_integrity_risk": self.total_integrity_risk,
            "average_cognitive_load": self.average_cognitive_load,
            "roi": self.roi(),
            "net_scint": self.net_scint(),
            "break_even_phase": self.break_even_phase(),
            "evolution_trigger_phase": self.evolution_trigger_phase(),
            "completion_percentage": self.completion_percentage(),
            "phases": [p.to_dict() for p in self.phases],
            "achievements": self.achievements
        }

    def __str__(self) -> str:
        return (
            f"Quest: {self.name}\n"
            f"  Phases: {len(self.phases)} ({self.completion_percentage():.0f}% complete)\n"
            f"  Investment: {self.total_scint_cost} ✨\n"
            f"  Returns: {self.total_scint_earned} ✨ (net: {self.net_scint():+d})\n"
            f"  ROI: {self.roi():.2f}x\n"
            f"  Karma: {self.total_karma:+d} ☯️\n"
            f"  Break-even: Phase {self.break_even_phase()}\n"
            f"  Evolution: Phase {self.evolution_trigger_phase()}\n"
            f"  Achievements: {len(self.achievements)}"
        )


# ============================================================================
# Player Stats
# ============================================================================

@dataclass
class PlayerStats:
    """
    Player/character statistics.

    Tracks cumulative stats across all work.

    Attributes:
        scint_balance: Current Scint available
        karma: Cumulative karma
        integrity_current: Current integrity
        integrity_max: Maximum integrity
        cognitive_capacity: Available cognitive capacity
        level: Player level
        evolution: Current evolution path
    """
    scint_balance: int = 0
    karma: int = 0
    integrity_current: int = 100
    integrity_max: int = 100
    cognitive_capacity: int = 10  # Morning = 10, evening = 4
    level: int = 1
    evolution: EvolutionPath = EvolutionPath.THE_BALANCED

    def can_afford(self, phase: Phase) -> bool:
        """Check if player can afford to start phase."""
        return self.scint_balance >= phase.scint_cost

    def can_handle_risk(self, phase: Phase) -> bool:
        """Check if integrity can handle the risk."""
        return self.integrity_current >= phase.integrity_risk

    def can_handle_complexity(self, phase: Phase) -> bool:
        """Check if cognitive capacity is sufficient."""
        return self.cognitive_capacity >= phase.cognitive_load

    def can_start_phase(self, phase: Phase) -> tuple[bool, str]:
        """Check if player can start phase. Returns (can_start, reason)."""
        if not self.can_afford(phase):
            return False, f"Need {phase.scint_cost - self.scint_balance} more Scint"

        if not self.can_handle_risk(phase):
            return False, f"Integrity too low (need {phase.integrity_risk}, have {self.integrity_current})"

        if not self.can_handle_complexity(phase):
            return False, f"Too complex (need {phase.cognitive_load} 🧠, have {self.cognitive_capacity})"

        return True, "Ready to proceed"

    def complete_phase(self, phase: Phase):
        """Update stats after completing phase."""
        # Spend Scint
        cost = phase.actual_scint if phase.actual_scint is not None else phase.scint_cost
        self.scint_balance -= cost

        # Earn Scint back
        self.scint_balance += phase.scint_earned

        # Update karma
        self.karma += phase.karma_impact

        # Take/heal integrity
        if phase.completed:
            # Successful completion heals some damage
            recovery = 20
            self.integrity_current = min(
                self.integrity_max,
                self.integrity_current - phase.integrity_risk + recovery
            )
        else:
            self.integrity_current -= phase.integrity_risk

        # Check for evolution
        self._check_evolution()

    def _check_evolution(self):
        """Check and update evolution path based on karma."""
        karma_obj = Karma(impact=self.karma)
        self.evolution = karma_obj.evolution_path()

    def rest(self):
        """Rest to recover Scint and cognitive capacity."""
        self.scint_balance += 20
        self.cognitive_capacity = 10  # Full recovery

    def heal(self, amount: int = 20):
        """Heal integrity."""
        self.integrity_current = min(self.integrity_max, self.integrity_current + amount)

    def level_up(self):
        """Increase level and stats."""
        self.level += 1
        self.integrity_max += 10
        self.integrity_current = self.integrity_max
        self.scint_balance += 50

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "scint_balance": self.scint_balance,
            "karma": self.karma,
            "integrity_current": self.integrity_current,
            "integrity_max": self.integrity_max,
            "cognitive_capacity": self.cognitive_capacity,
            "level": self.level,
            "evolution": self.evolution.value
        }


# ============================================================================
# Decorators
# ============================================================================

def track_metrics(
    scint_cost: int = 0,
    scint_earned: int = 0,
    karma_impact: int = 0,
    integrity_risk: int = 0,
    cognitive_load: int = 1
):
    """
    Decorator to track metrics for a function.

    Example:
        >>> @track_metrics(
        ...     scint_cost=40,
        ...     karma_impact=10,
        ...     integrity_risk=5,
        ...     cognitive_load=4
        ... )
        ... def write_documentation():
        ...     pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: Implement actual tracking (log to file, database, etc.)
            result = func(*args, **kwargs)

            # Create phase record
            phase = Phase(
                name=func.__name__,
                scint_cost=scint_cost,
                scint_earned=scint_earned,
                karma_impact=karma_impact,
                integrity_risk=integrity_risk,
                cognitive_load=cognitive_load
            )

            # Could log here
            print(f"[METRICS] {phase}")

            return result
        return wrapper
    return decorator


# ============================================================================
# Utility Functions
# ============================================================================

def calculate_roi(cost: int, earned: int) -> float:
    """Calculate return on investment."""
    if cost == 0:
        return float('inf') if earned > 0 else 0.0
    return earned / cost


def estimate_time_from_scint(scint: int) -> float:
    """
    Rough conversion: Scint → Hours.

    This is approximate and varies by individual and task type.
    """
    conversion = {
        (0, 30): 1.0,      # 0-30 Scint ≈ 1 hour
        (31, 60): 2.0,     # 31-60 ≈ 2 hours
        (61, 90): 3.0,     # 61-90 ≈ 3 hours
        (91, 120): 4.0,    # 91-120 ≈ 4 hours
        (121, 200): 8.0,   # 121-200 ≈ 8 hours
    }

    for (low, high), hours in conversion.items():
        if low <= scint <= high:
            return hours

    # Above 200
    return scint / 25  # Rough estimate


def prioritize_phases(phases: List[Phase]) -> List[Phase]:
    """
    Prioritize phases by ROI and karma.

    Returns phases sorted by:
    1. ROI (return on investment)
    2. Karma gain (alignment)
    """
    scored = [(p, p.roi(), p.karma_impact) for p in phases]
    return [p for p, _, _ in sorted(scored, key=lambda x: (x[1], x[2]), reverse=True)]


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    # Create a quest
    quest = Quest(
        name="Project Reorganization",
        description="Clean up and organize the project structure"
    )

    # Add phases
    quest.add_phase(Phase(
        name="Setup automation",
        scint_cost=80,
        scint_earned=100,
        karma_impact=30,
        integrity_risk=5,
        cognitive_load=7
    ))

    quest.add_phase(Phase(
        name="Move PDFs",
        scint_cost=30,
        scint_earned=50,
        karma_impact=15,
        integrity_risk=10,
        cognitive_load=2
    ))

    quest.add_phase(Phase(
        name="Consolidate docs",
        scint_cost=70,
        scint_earned=90,
        karma_impact=35,
        integrity_risk=25,
        cognitive_load=6
    ))

    # Print quest summary
    print(quest)
    print()

    # Create player
    player = PlayerStats(scint_balance=100, karma=0)

    # Try to start first phase
    phase1 = quest.phases[0]
    can_start, reason = player.can_start_phase(phase1)
    print(f"Can start '{phase1.name}'? {can_start}")
    print(f"Reason: {reason}")
    print()

    # Complete phase
    if can_start:
        player.complete_phase(phase1)
        phase1.complete()
        print(f"Completed '{phase1.name}'!")
        print(f"Player stats: {player.to_dict()}")
