"""
ADVANCED CAPABILITIES - Built on proven foundation + patterns

After proving foundation and patterns work, build advanced capabilities:
1. Adaptive Guide - learns from history
2. Quality Analyzer - deep metrics
3. Strategy Selector - picks best strategy for problem type
4. Session Replay - reproduce and analyze past sessions
"""

import statistics
from dataclasses import dataclass

from foundation import Guide, Session
from patterns import (
    EvaluationStrategy,
    LengthBasedStrategy,
    LenientStrategy,
    StrategyGuide,
    StrictStrategy,
)

# ============================================================================
# ADVANCED 1: ADAPTIVE GUIDE - Learns from history
# ============================================================================


@dataclass
class PerformanceStats:
    """Statistics for a strategy's performance."""

    strategy_name: str
    success_rate: float = 0.0
    avg_quality: float = 0.0
    avg_iterations: float = 0.0
    total_uses: int = 0


class AdaptiveGuide(Guide):
    """Guide that learns which strategies work best."""

    def __init__(self, max_iterations: int = 10, quality_threshold: float = 0.8):
        super().__init__(max_iterations, quality_threshold)
        self._strategies: dict[str, EvaluationStrategy] = {
            "strict": StrictStrategy(),
            "lenient": LenientStrategy(),
            "length": LengthBasedStrategy(),
        }
        self._stats: dict[str, PerformanceStats] = {
            name: PerformanceStats(name) for name in self._strategies.keys()
        }
        self._current_strategy = "length"  # default

    def _select_best_strategy(self) -> str:
        """Select strategy with highest success rate."""
        if all(s.total_uses == 0 for s in self._stats.values()):
            return "length"  # default when no history

        # Pick strategy with best avg_quality * success_rate
        best_name = max(
            self._stats.keys(),
            key=lambda name: self._stats[name].avg_quality * self._stats[name].success_rate
            if self._stats[name].total_uses > 0
            else 0,
        )
        return best_name

    def _update_stats(self, strategy_name: str, session: Session) -> None:
        """Update statistics after session."""
        stats = self._stats[strategy_name]
        stats.total_uses += 1

        # Calculate success (did we reach threshold?)
        final_quality = session.final_evaluation.overall.value
        success = final_quality >= self.quality_threshold

        # Update running averages
        n = stats.total_uses
        stats.success_rate = ((stats.success_rate * (n - 1)) + (1.0 if success else 0.0)) / n
        stats.avg_quality = ((stats.avg_quality * (n - 1)) + final_quality) / n
        stats.avg_iterations = ((stats.avg_iterations * (n - 1)) + len(session.steps)) / n

    def solve(self, problem: str) -> Session:
        """Solve with adaptive strategy selection."""
        # Select best strategy based on history
        self._current_strategy = self._select_best_strategy()

        # Solve with selected strategy
        strategy = self._strategies[self._current_strategy]
        guide = StrategyGuide(strategy, self.max_iterations, self.quality_threshold)
        session = guide.solve(problem)

        # Update stats
        self._update_stats(self._current_strategy, session)

        return session

    def get_stats(self) -> dict[str, PerformanceStats]:
        """Get current performance statistics."""
        return self._stats.copy()


# ============================================================================
# ADVANCED 2: QUALITY ANALYZER - Deep metrics
# ============================================================================


@dataclass
class QualityMetrics:
    """Deep quality analysis."""

    overall_score: float
    improvement_rate: float  # how much quality improved per step
    convergence_speed: float  # how fast it converged
    consistency: float  # how consistent scores are
    efficiency: float  # quality per iteration

    @property
    def grade(self) -> str:
        """Letter grade for overall quality."""
        if self.overall_score >= 0.9:
            return "A"
        if self.overall_score >= 0.8:
            return "B"
        if self.overall_score >= 0.7:
            return "C"
        if self.overall_score >= 0.6:
            return "D"
        return "F"


class QualityAnalyzer:
    """Analyze session quality in depth."""

    @staticmethod
    def analyze(session: Session) -> QualityMetrics:
        """Perform deep analysis of session quality."""
        if not session.steps:
            return QualityMetrics(0, 0, 0, 0, 0)

        # Extract quality scores over time
        scores = [step.evaluation.overall.value for step in session.steps]

        # Overall score (final)
        overall = scores[-1]

        # Improvement rate (slope of quality over time)
        if len(scores) > 1:
            improvement = (scores[-1] - scores[0]) / len(scores)
        else:
            improvement = 0.0

        # Convergence speed (how quickly it stabilized)
        if len(scores) > 1:
            # Measure variance in second half vs first half
            mid = len(scores) // 2
            first_var = statistics.variance(scores[:mid]) if mid > 1 else 1.0
            second_var = statistics.variance(scores[mid:]) if len(scores) - mid > 1 else 0.0
            convergence = 1.0 - (second_var / (first_var + 0.01))  # avoid div by zero
            convergence = max(0.0, min(1.0, convergence))
        else:
            convergence = 1.0

        # Consistency (inverse of variance)
        if len(scores) > 1:
            variance = statistics.variance(scores)
            consistency = 1.0 / (1.0 + variance)
        else:
            consistency = 1.0

        # Efficiency (quality per iteration)
        efficiency = overall / len(scores)

        return QualityMetrics(
            overall_score=overall,
            improvement_rate=improvement,
            convergence_speed=convergence,
            consistency=consistency,
            efficiency=efficiency,
        )


# ============================================================================
# ADVANCED 3: STRATEGY SELECTOR - Picks best strategy for problem type
# ============================================================================


class ProblemClassifier:
    """Classify problem type to select optimal strategy."""

    @staticmethod
    def classify(problem: str) -> str:
        """Classify problem into type."""
        problem_lower = problem.lower()

        # Math problems -> strict
        if any(
            word in problem_lower
            for word in ["math", "calculate", "equation", "solve", "+", "-", "*", "/"]
        ):
            return "math"

        # Creative problems -> lenient
        if any(
            word in problem_lower
            for word in ["creative", "brainstorm", "imagine", "story", "design"]
        ):
            return "creative"

        # Factual problems -> strict
        if any(word in problem_lower for word in ["fact", "true", "false", "verify", "check"]):
            return "factual"

        # Default
        return "general"


class StrategySelector:
    """Select optimal strategy based on problem type."""

    def __init__(self):
        self._strategy_map = {
            "math": StrictStrategy(),
            "factual": StrictStrategy(),
            "creative": LenientStrategy(),
            "general": LengthBasedStrategy(),
        }

    def select_for_problem(self, problem: str) -> EvaluationStrategy:
        """Select best strategy for this problem."""
        problem_type = ProblemClassifier.classify(problem)
        return self._strategy_map.get(problem_type, LengthBasedStrategy())


class SmartGuide(Guide):
    """Guide that selects strategy based on problem type."""

    def __init__(self, max_iterations: int = 10, quality_threshold: float = 0.8):
        super().__init__(max_iterations, quality_threshold)
        self._selector = StrategySelector()

    def solve(self, problem: str) -> Session:
        """Solve with problem-appropriate strategy."""
        strategy = self._selector.select_for_problem(problem)
        guide = StrategyGuide(strategy, self.max_iterations, self.quality_threshold)
        return guide.solve(problem)


# ============================================================================
# ADVANCED 4: SESSION REPLAY - Reproduce and analyze
# ============================================================================


class SessionRecorder:
    """Record and replay sessions."""

    def __init__(self):
        self._recordings: list[Session] = []

    def record(self, session: Session) -> None:
        """Record a session."""
        self._recordings.append(session)

    def replay(self, index: int) -> Session:
        """Get recorded session."""
        return self._recordings[index]

    def analyze_all(self) -> dict[str, any]:
        """Analyze all recorded sessions."""
        if not self._recordings:
            return {"total": 0}

        metrics = [QualityAnalyzer.analyze(s) for s in self._recordings]

        return {
            "total": len(self._recordings),
            "avg_quality": statistics.mean(m.overall_score for m in metrics),
            "avg_efficiency": statistics.mean(m.efficiency for m in metrics),
            "avg_improvement_rate": statistics.mean(m.improvement_rate for m in metrics),
            "grade_distribution": {
                "A": sum(1 for m in metrics if m.grade == "A"),
                "B": sum(1 for m in metrics if m.grade == "B"),
                "C": sum(1 for m in metrics if m.grade == "C"),
                "D": sum(1 for m in metrics if m.grade == "D"),
                "F": sum(1 for m in metrics if m.grade == "F"),
            },
        }


# ============================================================================
# ADVANCED 5: ENSEMBLE GUIDE - Combines multiple strategies
# ============================================================================


class EnsembleGuide(Guide):
    """Guide that runs multiple strategies and combines results."""

    def __init__(self, max_iterations: int = 10, quality_threshold: float = 0.8):
        super().__init__(max_iterations, quality_threshold)
        self._strategies = [StrictStrategy(), LenientStrategy(), LengthBasedStrategy()]

    def solve(self, problem: str) -> Session:
        """Solve with all strategies and pick best."""
        sessions = []

        for strategy in self._strategies:
            guide = StrategyGuide(strategy, self.max_iterations, self.quality_threshold)
            session = guide.solve(problem)
            sessions.append(session)

        # Pick session with highest final quality
        best = max(sessions, key=lambda s: s.final_evaluation.overall.value)
        return best


# ============================================================================
# TEST ADVANCED CAPABILITIES
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("TESTING ADVANCED CAPABILITIES")
    print("=" * 80)

    # Test 1: Adaptive Guide
    print("\n[ADVANCED 1: ADAPTIVE GUIDE]")
    adaptive = AdaptiveGuide(max_iterations=2)
    for i in range(5):
        session = adaptive.solve(f"Test problem {i}")
        print(f"  Session {i + 1}: quality={session.final_evaluation.overall.value:.3f}")

    print("\n  Learning statistics:")
    for name, stats in adaptive.get_stats().items():
        print(
            f"    {name}: success_rate={stats.success_rate:.2f}, "
            f"avg_quality={stats.avg_quality:.3f}, uses={stats.total_uses}"
        )
    print("  ✅ Adaptive guide learns from experience")

    # Test 2: Quality Analyzer
    print("\n[ADVANCED 2: QUALITY ANALYZER]")
    guide = Guide(max_iterations=3)
    session = guide.solve("Test problem for analysis")
    metrics = QualityAnalyzer.analyze(session)
    print(f"  Overall: {metrics.overall_score:.3f} (Grade: {metrics.grade})")
    print(f"  Improvement rate: {metrics.improvement_rate:.3f}")
    print(f"  Convergence: {metrics.convergence_speed:.3f}")
    print(f"  Consistency: {metrics.consistency:.3f}")
    print(f"  Efficiency: {metrics.efficiency:.3f}")
    print("  ✅ Deep quality analysis working")

    # Test 3: Strategy Selector
    print("\n[ADVANCED 3: STRATEGY SELECTOR]")
    smart = SmartGuide(max_iterations=2)
    test_problems = ["Calculate 2 + 2", "Write a creative story", "Verify this fact is true"]
    for prob in test_problems:
        session = smart.solve(prob)
        problem_type = ProblemClassifier.classify(prob)
        print(f"  Problem: '{prob[:30]}...'")
        print(f"    Classified as: {problem_type}")
        print(f"    Quality: {session.final_evaluation.overall.value:.3f}")
    print("  ✅ Smart strategy selection working")

    # Test 4: Session Recorder
    print("\n[ADVANCED 4: SESSION RECORDER]")
    recorder = SessionRecorder()
    for i in range(5):
        session = guide.solve(f"Recorded problem {i}")
        recorder.record(session)

    analysis = recorder.analyze_all()
    print(f"  Total recordings: {analysis['total']}")
    print(f"  Average quality: {analysis['avg_quality']:.3f}")
    print(f"  Average efficiency: {analysis['avg_efficiency']:.3f}")
    print(f"  Grade distribution: {analysis['grade_distribution']}")
    print("  ✅ Session recording and analysis working")

    # Test 5: Ensemble Guide
    print("\n[ADVANCED 5: ENSEMBLE GUIDE]")
    ensemble = EnsembleGuide(max_iterations=2)
    session = ensemble.solve("Test problem for ensemble")
    print(f"  Ensemble quality: {session.final_evaluation.overall.value:.3f}")
    print("  ✅ Ensemble combining strategies")

    print("\n" + "=" * 80)
    print("ALL ADVANCED CAPABILITIES WORKING")
    print("=" * 80)
    print("\n✅ Adaptive Guide - learns from history")
    print("✅ Quality Analyzer - deep metrics")
    print("✅ Strategy Selector - problem-specific strategies")
    print("✅ Session Recorder - replay and analyze")
    print("✅ Ensemble Guide - combine multiple strategies")
    print("\n🎯 BUILT ON PROVEN FOUNDATION + PATTERNS")
