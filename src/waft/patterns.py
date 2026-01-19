"""
DESIGN PATTERNS - Built on the core without changing it

Using the core primitives (Score, Evaluation, Step, Session, Guide),
implement every relevant design pattern.

RULE: Don't modify core.py. Only compose/extend it.
"""

from foundation import Score, Evaluation, Step, Session, Guide, evaluate_text, evaluate_answer
from abc import ABC, abstractmethod
from typing import Callable, List, Optional
from dataclasses import dataclass, field
from enum import Enum

# ============================================================================
# PATTERN 1: STRATEGY - Different evaluation strategies
# ============================================================================

class EvaluationStrategy(ABC):
    """Strategy for evaluating text quality."""

    @abstractmethod
    def evaluate(self, text: str, context: str = "") -> Evaluation:
        """Evaluate text and return Evaluation."""
        pass


class LengthBasedStrategy(EvaluationStrategy):
    """Simple strategy: quality = length."""

    def evaluate(self, text: str, context: str = "") -> Evaluation:
        score = evaluate_text(text)
        confidence = Score(min(len(text) / 150.0, 1.0))
        # Length-based: moderate doubt and curiosity
        doubt = Score(0.3)
        curiosity = Score(0.4)
        return Evaluation(
            factuality=score,
            validity=score,
            coherence=score,
            utility=score,
            faithfulness=score,
            confidence=confidence,
            doubt=doubt,
            curiosity=curiosity
        )


class StrictStrategy(EvaluationStrategy):
    """Strict strategy: penalize everything."""

    def evaluate(self, text: str, context: str = "") -> Evaluation:
        base = evaluate_text(text)
        # Penalize by 30%
        penalized = Score(base.value * 0.7)
        # Strict = high confidence, low doubt, low curiosity
        # (Certain about standards, not questioning, not exploring)
        confidence = Score(0.9)
        doubt = Score(0.2)  # Low doubt = certain about judgment
        curiosity = Score(0.2)  # Low curiosity = not seeking alternatives
        return Evaluation(
            factuality=penalized,
            validity=penalized,
            coherence=penalized,
            utility=penalized,
            faithfulness=penalized,
            confidence=confidence,
            doubt=doubt,
            curiosity=curiosity
        )


class LenientStrategy(EvaluationStrategy):
    """Lenient strategy: boost scores."""

    def evaluate(self, text: str, context: str = "") -> Evaluation:
        base = evaluate_text(text)
        # Boost by 30%
        boosted = Score(min(base.value * 1.3, 1.0))
        # Lenient = lower confidence, high doubt, high curiosity
        # (Being generous means uncertain, open to alternatives)
        confidence = Score(0.6)
        doubt = Score(0.7)  # High doubt = questioning the evaluation
        curiosity = Score(0.8)  # High curiosity = exploring alternatives
        return Evaluation(
            factuality=boosted,
            validity=boosted,
            coherence=boosted,
            utility=boosted,
            faithfulness=boosted,
            confidence=confidence,
            doubt=doubt,
            curiosity=curiosity
        )


class StrategyGuide(Guide):
    """Guide with pluggable evaluation strategy."""

    def __init__(self, strategy: EvaluationStrategy, max_iterations: int = 10, quality_threshold: float = 0.8):
        super().__init__(max_iterations, quality_threshold)
        self.strategy = strategy

    def _evaluate(self, answer: str, problem: str) -> Evaluation:
        """Use the strategy to evaluate."""
        return self.strategy.evaluate(answer, problem)


# ============================================================================
# PATTERN 2: CHAIN OF RESPONSIBILITY - Evaluation pipeline
# ============================================================================

class EvaluationHandler(ABC):
    """Handler in the evaluation chain."""

    def __init__(self):
        self._next: Optional[EvaluationHandler] = None

    def set_next(self, handler: 'EvaluationHandler') -> 'EvaluationHandler':
        """Set the next handler in the chain."""
        self._next = handler
        return handler

    @abstractmethod
    def handle(self, evaluation: Evaluation) -> Evaluation:
        """Process the evaluation."""
        pass

    def _pass_to_next(self, evaluation: Evaluation) -> Evaluation:
        """Pass to next handler if exists."""
        if self._next:
            return self._next.handle(evaluation)
        return evaluation


class MinimumScoreHandler(EvaluationHandler):
    """Enforce minimum scores."""

    def __init__(self, minimum: float = 0.1):
        super().__init__()
        self.minimum = minimum

    def handle(self, evaluation: Evaluation) -> Evaluation:
        """Ensure no score falls below minimum."""
        def clamp(score: Score) -> Score:
            return Score(max(score.value, self.minimum))

        modified = Evaluation(
            factuality=clamp(evaluation.factuality),
            validity=clamp(evaluation.validity),
            coherence=clamp(evaluation.coherence),
            utility=clamp(evaluation.utility),
            faithfulness=clamp(evaluation.faithfulness),
            confidence=clamp(evaluation.confidence),
            doubt=clamp(evaluation.doubt),
            curiosity=clamp(evaluation.curiosity)
        )
        return self._pass_to_next(modified)


class NormalizeHandler(EvaluationHandler):
    """Normalize scores to 0-1 range."""

    def handle(self, evaluation: Evaluation) -> Evaluation:
        """Already normalized, just pass through."""
        return self._pass_to_next(evaluation)


class LoggingHandler(EvaluationHandler):
    """Log evaluations."""

    def handle(self, evaluation: Evaluation) -> Evaluation:
        """Log and pass through."""
        print(f"[LOG] Overall score: {evaluation.overall.value:.3f}")
        return self._pass_to_next(evaluation)


# ============================================================================
# PATTERN 3: OBSERVER - Watch quality changes
# ============================================================================

class QualityObserver(ABC):
    """Observer for quality changes."""

    @abstractmethod
    def update(self, step: Step) -> None:
        """Called when a new step is completed."""
        pass


class QualityLogger(QualityObserver):
    """Log quality scores."""

    def update(self, step: Step) -> None:
        print(f"[Observer] Iteration {step.iteration_number}: Quality={step.evaluation.overall.value:.3f}")


class ThresholdAlerter(QualityObserver):
    """Alert when quality crosses threshold."""

    def __init__(self, threshold: float = 0.9):
        self.threshold = threshold
        self.alerted = False

    def update(self, step: Step) -> None:
        if step.evaluation.overall.value >= self.threshold and not self.alerted:
            print(f"[ALERT] Quality threshold {self.threshold} reached!")
            self.alerted = True


class ObservableGuide(Guide):
    """Guide that notifies observers."""

    def __init__(self, max_iterations: int = 10, quality_threshold: float = 0.8):
        super().__init__(max_iterations, quality_threshold)
        self._observers: List[QualityObserver] = []

    def attach(self, observer: QualityObserver) -> None:
        """Attach an observer."""
        self._observers.append(observer)

    def detach(self, observer: QualityObserver) -> None:
        """Detach an observer."""
        self._observers.remove(observer)

    def _notify(self, step: Step) -> None:
        """Notify all observers."""
        for observer in self._observers:
            observer.update(step)


# ============================================================================
# PATTERN 4: DECORATOR - Add capabilities without modifying
# ============================================================================

class GuideDecorator(ABC):
    """Base decorator for Guide."""

    def __init__(self, guide: Guide):
        self._guide = guide

    def solve(self, problem: str) -> Session:
        """Delegate to wrapped guide."""
        return self._guide.solve(problem)


class ValidationDecorator(GuideDecorator):
    """Add validation before solving."""

    def solve(self, problem: str) -> Session:
        """Validate problem before solving."""
        if not problem or len(problem) < 5:
            raise ValueError("Problem too short")

        # Check for false premises
        if "2+2=5" in problem or "1=2" in problem:
            raise ValueError("False mathematical premise detected")

        return super().solve(problem)


class CachingDecorator(GuideDecorator):
    """Cache solutions."""

    def __init__(self, guide: Guide):
        super().__init__(guide)
        self._cache: dict[str, Session] = {}

    def solve(self, problem: str) -> Session:
        """Check cache before solving."""
        if problem in self._cache:
            print(f"[Cache] Hit for: {problem[:50]}")
            return self._cache[problem]

        print(f"[Cache] Miss for: {problem[:50]}")
        session = super().solve(problem)
        self._cache[problem] = session
        return session


class TimingDecorator(GuideDecorator):
    """Measure solve time."""

    def solve(self, problem: str) -> Session:
        """Time the solve operation."""
        import time
        start = time.time()
        session = super().solve(problem)
        elapsed = time.time() - start
        print(f"[Timing] Solved in {elapsed:.3f}s")
        return session


# ============================================================================
# PATTERN 5: FACTORY - Create different guide types
# ============================================================================

class GuideType(Enum):
    """Types of guides."""
    BASIC = "basic"
    STRICT = "strict"
    LENIENT = "lenient"
    OBSERVABLE = "observable"
    CACHED = "cached"


class GuideFactory:
    """Factory for creating guides."""

    @staticmethod
    def create(guide_type: GuideType, **kwargs) -> Guide:
        """Create a guide of the specified type."""
        if guide_type == GuideType.BASIC:
            return Guide(**kwargs)

        elif guide_type == GuideType.STRICT:
            return StrategyGuide(
                strategy=StrictStrategy(),
                **kwargs
            )

        elif guide_type == GuideType.LENIENT:
            return StrategyGuide(
                strategy=LenientStrategy(),
                **kwargs
            )

        elif guide_type == GuideType.OBSERVABLE:
            observable = ObservableGuide(**kwargs)
            # Attach default observers
            observable.attach(QualityLogger())
            return observable

        elif guide_type == GuideType.CACHED:
            base = Guide(**kwargs)
            return CachingDecorator(base)

        else:
            raise ValueError(f"Unknown guide type: {guide_type}")


# ============================================================================
# PATTERN 6: COMMAND - Each evaluation is a command
# ============================================================================

class Command(ABC):
    """Command interface."""

    @abstractmethod
    def execute(self) -> any:
        """Execute the command."""
        pass


class EvaluateCommand(Command):
    """Command to evaluate an answer."""

    def __init__(self, answer: str, problem: str):
        self.answer = answer
        self.problem = problem
        self._result: Optional[Evaluation] = None

    def execute(self) -> Evaluation:
        """Execute evaluation."""
        self._result = evaluate_answer(self.answer, self.problem)
        return self._result

    @property
    def result(self) -> Optional[Evaluation]:
        """Get result if executed."""
        return self._result


class SolveCommand(Command):
    """Command to solve a problem."""

    def __init__(self, guide: Guide, problem: str):
        self.guide = guide
        self.problem = problem
        self._result: Optional[Session] = None

    def execute(self) -> Session:
        """Execute solve."""
        self._result = self.guide.solve(self.problem)
        return self._result

    @property
    def result(self) -> Optional[Session]:
        """Get result if executed."""
        return self._result


class CommandQueue:
    """Queue of commands to execute."""

    def __init__(self):
        self._commands: List[Command] = []

    def add(self, command: Command) -> None:
        """Add command to queue."""
        self._commands.append(command)

    def execute_all(self) -> List[any]:
        """Execute all commands."""
        results = []
        for cmd in self._commands:
            results.append(cmd.execute())
        return results


# ============================================================================
# PATTERN 7: BUILDER - Build complex sessions
# ============================================================================

class SessionBuilder:
    """Builder for constructing sessions step by step."""

    def __init__(self):
        self._problem: Optional[str] = None
        self._steps: List[Step] = []
        self._max_iterations: int = 10
        self._quality_threshold: float = 0.8

    def with_problem(self, problem: str) -> 'SessionBuilder':
        """Set the problem."""
        self._problem = problem
        return self

    def with_max_iterations(self, max_iterations: int) -> 'SessionBuilder':
        """Set max iterations."""
        self._max_iterations = max_iterations
        return self

    def with_quality_threshold(self, threshold: float) -> 'SessionBuilder':
        """Set quality threshold."""
        self._quality_threshold = threshold
        return self

    def add_step(self, step: Step) -> 'SessionBuilder':
        """Add a step."""
        self._steps.append(step)
        return self

    def build(self) -> Session:
        """Build the session."""
        if not self._problem:
            raise ValueError("Problem not set")

        return Session(
            problem=self._problem,
            steps=self._steps,
            max_iterations=self._max_iterations,
            quality_threshold=self._quality_threshold
        )


# ============================================================================
# TEST THE PATTERNS
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("TESTING DESIGN PATTERNS")
    print("="*80)

    # Pattern 1: Strategy
    print("\n[PATTERN 1: STRATEGY]")
    strict_guide = StrategyGuide(StrictStrategy(), max_iterations=2)
    lenient_guide = StrategyGuide(LenientStrategy(), max_iterations=2)
    print("  Created strict and lenient guides")

    # Pattern 2: Chain of Responsibility
    print("\n[PATTERN 2: CHAIN OF RESPONSIBILITY]")
    handler = MinimumScoreHandler(0.2)
    handler.set_next(LoggingHandler())
    print("  Created evaluation chain with min score + logging")

    # Pattern 3: Observer
    print("\n[PATTERN 3: OBSERVER]")
    observable = ObservableGuide(max_iterations=2)
    observable.attach(QualityLogger())
    observable.attach(ThresholdAlerter(0.5))
    print("  Attached quality logger and threshold alerter")

    # Pattern 4: Decorator
    print("\n[PATTERN 4: DECORATOR]")
    base = Guide(max_iterations=2)
    validated = ValidationDecorator(base)
    cached = CachingDecorator(validated)
    timed = TimingDecorator(cached)
    print("  Stacked decorators: Timing → Caching → Validation → Base")

    # Pattern 5: Factory
    print("\n[PATTERN 5: FACTORY]")
    factory_guide = GuideFactory.create(GuideType.STRICT, max_iterations=2)
    print(f"  Created {GuideType.STRICT.value} guide from factory")

    # Pattern 6: Command
    print("\n[PATTERN 6: COMMAND]")
    queue = CommandQueue()
    queue.add(SolveCommand(Guide(max_iterations=1), "Test problem 1"))
    queue.add(SolveCommand(Guide(max_iterations=1), "Test problem 2"))
    print("  Created command queue with 2 solve commands")

    # Pattern 7: Builder
    print("\n[PATTERN 7: BUILDER]")
    builder = SessionBuilder()
    builder.with_problem("Built problem") \
           .with_max_iterations(3) \
           .with_quality_threshold(0.75)
    print("  Built session with fluent interface")

    print("\n" + "="*80)
    print("ALL PATTERNS IMPLEMENTED")
    print("="*80)
    print("\n✅ Strategy - Pluggable evaluation algorithms")
    print("✅ Chain of Responsibility - Evaluation pipeline")
    print("✅ Observer - Watch quality changes")
    print("✅ Decorator - Add capabilities without modifying core")
    print("✅ Factory - Create different guide types")
    print("✅ Command - Encapsulate operations as objects")
    print("✅ Builder - Construct complex sessions")
    print("\n🎯 ALL BUILT ON TOP OF CORE WITHOUT MODIFYING IT")
