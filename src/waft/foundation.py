"""
THE CORE - Building TheGuide from first principles

Start with the atomic data type and build up brick by brick.
"""

from dataclasses import dataclass
from typing import Protocol as TypingProtocol
from enum import Enum

# ============================================================================
# LEVEL 0: THE ATOMIC DATA TYPE
# ============================================================================
# What is the CORE? A quality score - one number representing goodness.

@dataclass(frozen=True)
class Score:
    """
    The atomic unit: a single quality measurement.
    Immutable. Between 0.0 and 1.0.
    """
    value: float  # 0.0 (terrible) to 1.0 (perfect)

    def __post_init__(self):
        if not 0.0 <= self.value <= 1.0:
            raise ValueError(f"Score must be 0-1, got {self.value}")

    def is_good(self, threshold: float = 0.8) -> bool:
        """Core decision: is this good enough?"""
        return self.value >= threshold

    def __float__(self) -> float:
        return self.value


# ============================================================================
# LEVEL 1: ONE FUNCTION - THE CORE TRANSFORMATION
# ============================================================================
# Transform text → score. This is the fundamental operation.

def evaluate_text(text: str) -> Score:
    """
    THE CORE FUNCTION

    Input:  text (string)
    Output: score (0.0 to 1.0)

    This is the atomic transformation.
    Everything else builds on this.
    """
    # In real impl, this calls an LLM
    # For now, simple heuristic: longer = better (toy example)
    quality = min(len(text) / 100.0, 1.0)
    return Score(quality)


# ============================================================================
# LEVEL 2: MULTI-DIMENSIONAL SCORE
# ============================================================================
# One score isn't enough. We need FVCU+Faithfulness taxonomy.

@dataclass(frozen=True)
class Evaluation:
    """
    Multi-dimensional quality assessment.
    Built from 6 atomic Scores (FVCU+F+C taxonomy).
    """
    factuality: Score      # Is it factually correct?
    validity: Score        # Is the reasoning valid?
    coherence: Score       # Does it make sense?
    utility: Score         # Is it useful?
    faithfulness: Score    # Is it faithful to the problem?
    confidence: Score      # How certain are we about this evaluation? (META-COGNITIVE)

    @property
    def overall(self) -> Score:
        """Aggregate all dimensions into one score."""
        avg = (
            self.factuality.value +
            self.validity.value +
            self.coherence.value +
            self.utility.value +
            self.faithfulness.value +
            self.confidence.value
        ) / 6.0
        return Score(avg)

    def is_good(self, threshold: float = 0.8) -> bool:
        """Is the overall quality good enough?"""
        return self.overall.is_good(threshold)


def evaluate_answer(answer: str, problem: str) -> Evaluation:
    """
    THE CORE EVALUATION FUNCTION

    Input:  answer text + problem context
    Output: multi-dimensional Evaluation

    This is one level up from evaluate_text.
    """
    # In real impl, LLM evaluates each dimension
    # For now, toy heuristic
    base_score = evaluate_text(answer)

    # Confidence: measure certainty about evaluation
    # Higher for longer, more detailed answers
    # Lower for short, vague answers
    confidence_value = min(len(answer) / 150.0, 1.0)  # Longer = more confident
    confidence_score = Score(confidence_value)

    return Evaluation(
        factuality=base_score,
        validity=base_score,
        coherence=base_score,
        utility=base_score,
        faithfulness=base_score,
        confidence=confidence_score  # NEW: Meta-cognitive dimension
    )


# ============================================================================
# LEVEL 3: ONE REASONING STEP
# ============================================================================
# One problem → one answer → one evaluation. This is one step.

@dataclass
class Step:
    """
    One iteration of reasoning.

    problem → answer → evaluation

    This is the core cycle, executed once.
    """
    problem: str
    answer: str
    evaluation: Evaluation
    iteration_number: int

    def should_continue(self, threshold: float = 0.8) -> bool:
        """Should we iterate again?"""
        return not self.evaluation.is_good(threshold)


def execute_step(problem: str, iteration: int) -> Step:
    """
    THE CORE REASONING FUNCTION

    Input:  problem, iteration number
    Output: completed Step

    This executes one full cycle: generate answer → evaluate.
    """
    # In real impl, LLM generates answer
    answer = f"Answer to: {problem}"

    # Evaluate the answer
    evaluation = evaluate_answer(answer, problem)

    return Step(
        problem=problem,
        answer=answer,
        evaluation=evaluation,
        iteration_number=iteration
    )


# ============================================================================
# LEVEL 4: MULTIPLE STEPS (THE LOOP)
# ============================================================================
# Keep executing steps until good enough or max iterations.

@dataclass
class Session:
    """
    Complete reasoning session.

    Multiple Steps executed until:
    - Quality threshold met
    - Max iterations reached

    This is the complete loop.
    """
    problem: str
    steps: list[Step]
    max_iterations: int
    quality_threshold: float

    @property
    def final_answer(self) -> str:
        """The last answer produced."""
        return self.steps[-1].answer if self.steps else ""

    @property
    def final_evaluation(self) -> Evaluation:
        """The last evaluation."""
        return self.steps[-1].evaluation if self.steps else None

    @property
    def converged(self) -> bool:
        """Did we reach good quality?"""
        return self.final_evaluation.is_good(self.quality_threshold) if self.final_evaluation else False


def solve(problem: str, max_iterations: int = 10, quality_threshold: float = 0.8) -> Session:
    """
    THE CORE SOLVING FUNCTION

    Input:  problem statement
    Output: Session with all steps

    This is the complete guidance loop:
    1. Execute step
    2. Check quality
    3. Continue or stop
    """
    steps = []

    for i in range(max_iterations):
        step = execute_step(problem, iteration=i+1)
        steps.append(step)

        # Stop if good enough
        if not step.should_continue(quality_threshold):
            break

    return Session(
        problem=problem,
        steps=steps,
        max_iterations=max_iterations,
        quality_threshold=quality_threshold
    )


# ============================================================================
# LEVEL 5: MAKE IT A CLASS (OOP WRAPPER)
# ============================================================================
# Everything above is functional. Now wrap in a class.

class Guide:
    """
    The Guide: Meta-cognitive reasoning system.

    Built on core primitives:
    - Score (atomic quality)
    - Evaluation (multi-dimensional quality)
    - Step (one reasoning cycle)
    - Session (complete loop)
    """

    def __init__(self, max_iterations: int = 10, quality_threshold: float = 0.8):
        self.max_iterations = max_iterations
        self.quality_threshold = quality_threshold

    def solve(self, problem: str) -> Session:
        """Solve a problem using iterative reasoning."""
        return solve(
            problem=problem,
            max_iterations=self.max_iterations,
            quality_threshold=self.quality_threshold
        )


# ============================================================================
# TEST THE CORE
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("TESTING THE CORE")
    print("="*80)

    # Test Level 0: Atomic Score
    print("\nLevel 0: Atomic Score")
    score = Score(0.85)
    print(f"  Score: {score.value}")
    print(f"  Is good? {score.is_good()}")

    # Test Level 1: Core transformation
    print("\nLevel 1: Core Transformation")
    text = "This is a test answer with some content"
    result = evaluate_text(text)
    print(f"  Text: {text[:40]}...")
    print(f"  Score: {result.value:.3f}")

    # Test Level 2: Multi-dimensional
    print("\nLevel 2: Multi-dimensional Evaluation")
    eval_result = evaluate_answer("test answer", "test problem")
    print(f"  Factuality: {eval_result.factuality.value:.3f}")
    print(f"  Overall: {eval_result.overall.value:.3f}")
    print(f"  Is good? {eval_result.is_good()}")

    # Test Level 3: One Step
    print("\nLevel 3: One Reasoning Step")
    step = execute_step("What is 2+2?", iteration=1)
    print(f"  Problem: {step.problem}")
    print(f"  Answer: {step.answer}")
    print(f"  Quality: {step.evaluation.overall.value:.3f}")
    print(f"  Should continue? {step.should_continue()}")

    # Test Level 4: Full Loop
    print("\nLevel 4: Complete Session")
    session = solve("Explain quantum computing", max_iterations=3)
    print(f"  Problem: {session.problem}")
    print(f"  Steps executed: {len(session.steps)}")
    print(f"  Final answer: {session.final_answer}")
    print(f"  Converged? {session.converged}")

    # Test Level 5: Class interface
    print("\nLevel 5: Class Interface")
    guide = Guide(max_iterations=5, quality_threshold=0.7)
    session = guide.solve("What is machine learning?")
    print(f"  Steps: {len(session.steps)}")
    print(f"  Final quality: {session.final_evaluation.overall.value:.3f}")

    print("\n" + "="*80)
    print("CORE VERIFIED")
    print("="*80)
    print("\nBuilt from ground up:")
    print("  Level 0: Score (atomic data type)")
    print("  Level 1: evaluate_text() (core function)")
    print("  Level 2: Evaluation (multi-dimensional)")
    print("  Level 3: Step (one cycle)")
    print("  Level 4: Session (complete loop)")
    print("  Level 5: Guide (class wrapper)")
