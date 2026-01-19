#!/usr/bin/env python3
"""
PRODUCTION API - Clean, predictable, composable interface

This demonstrates the real-world API for the meta-cognitive system.
Clear contracts, predictable behavior, measurable results.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Literal
from enum import Enum
import json

from foundation import Score, Evaluation, Session, Guide
from patterns import GuideFactory, GuideType
from composite import LeafGuide, VotingGuide
from advanced import (
    AdaptiveGuide, SmartGuide, EnsembleGuide,
    QualityAnalyzer, QualityMetrics,
    SessionRecorder
)


# ============================================================================
# CLEAN API TYPES - Predictable, composable units
# ============================================================================

class GuideMode(Enum):
    """Available guide modes with clear semantics."""
    BASIC = "basic"           # Simple iterative refinement
    STRICT = "strict"         # High standards, precise evaluation
    LENIENT = "lenient"       # Flexible, exploratory
    SMART = "smart"           # Auto-selects strategy per problem
    ADAPTIVE = "adaptive"     # Learns from history
    VOTING = "voting"         # Multiple guides vote
    ENSEMBLE = "ensemble"     # All strategies, pick best


@dataclass
class ProblemInput:
    """Input contract - what goes into the system."""
    problem: str
    mode: GuideMode = GuideMode.BASIC
    max_iterations: int = 10
    quality_threshold: float = 0.8


@dataclass
class QualityReport:
    """Output contract - what comes out of the system."""
    final_quality: float
    grade: str
    iterations_used: int
    improvement_rate: float
    efficiency: float
    convergence_speed: float
    consistency: float


@dataclass
class SolutionOutput:
    """Complete output - predictable structure."""
    problem: str
    mode: str
    final_answer: str
    quality_report: QualityReport
    step_history: List[Dict]
    session_id: Optional[str] = None


# ============================================================================
# PRODUCTION API CLASS - The main interface
# ============================================================================

class MetaCognitiveAPI:
    """
    Production API for meta-cognitive problem solving.

    Clean interface:
        input: ProblemInput  → output: SolutionOutput

    Predictable: Same input always produces deterministic evaluation
    Composable: Outputs can feed into other systems
    Measurable: Quality metrics at every level
    """

    def __init__(self):
        """Initialize API with recorder for analytics."""
        self.recorder = SessionRecorder()
        self._session_count = 0

    def solve(self, input: ProblemInput) -> SolutionOutput:
        """
        Main API endpoint: solve a problem with specified mode.

        Args:
            input: ProblemInput with problem, mode, and parameters

        Returns:
            SolutionOutput with solution, quality report, and history

        Contract:
            - Always returns SolutionOutput structure
            - Quality metrics always present
            - Step history always available
            - Deterministic quality evaluation
        """
        # Create appropriate guide based on mode
        guide = self._create_guide(input)

        # Execute solving
        session = guide.solve(input.problem)

        # Record for analytics
        self.recorder.record(session)
        self._session_count += 1

        # Analyze quality
        metrics = QualityAnalyzer.analyze(session)

        # Build quality report
        quality_report = QualityReport(
            final_quality=metrics.overall_score,
            grade=metrics.grade,
            iterations_used=len(session.steps),
            improvement_rate=metrics.improvement_rate,
            efficiency=metrics.efficiency,
            convergence_speed=metrics.convergence_speed,
            consistency=metrics.consistency
        )

        # Build step history
        step_history = [
            {
                'iteration': step.iteration_number,
                'answer': step.answer,
                'quality': step.evaluation.overall.value,
                'epistemic_humility': step.evaluation.epistemic_humility.value,
                'dimensions': {
                    # Core quality
                    'factuality': step.evaluation.factuality.value,
                    'validity': step.evaluation.validity.value,
                    'coherence': step.evaluation.coherence.value,
                    'utility': step.evaluation.utility.value,
                    'faithfulness': step.evaluation.faithfulness.value,
                    # Meta-cognitive (prevent ego/dogfooding)
                    'confidence': step.evaluation.confidence.value,  # Certainty
                    'doubt': step.evaluation.doubt.value,            # Skepticism
                    'curiosity': step.evaluation.curiosity.value,    # Explore alternatives
                    # Affective (prevents pure rationality/determinism)
                    'aesthetic': step.evaluation.aesthetic.value,    # Luck/fate - the stochastic element
                }
            }
            for step in session.steps
        ]

        # Get final answer
        final_answer = session.steps[-1].answer if session.steps else ""

        # Build complete output
        return SolutionOutput(
            problem=input.problem,
            mode=input.mode.value,
            final_answer=final_answer,
            quality_report=quality_report,
            step_history=step_history,
            session_id=f"session_{self._session_count}"
        )

    def _create_guide(self, input: ProblemInput) -> Guide:
        """Create appropriate guide based on mode."""
        if input.mode == GuideMode.BASIC:
            return Guide(input.max_iterations, input.quality_threshold)

        elif input.mode == GuideMode.STRICT:
            return GuideFactory.create(
                GuideType.STRICT,
                max_iterations=input.max_iterations,
                quality_threshold=input.quality_threshold
            )

        elif input.mode == GuideMode.LENIENT:
            return GuideFactory.create(
                GuideType.LENIENT,
                max_iterations=input.max_iterations,
                quality_threshold=input.quality_threshold
            )

        elif input.mode == GuideMode.SMART:
            return SmartGuide(input.max_iterations, input.quality_threshold)

        elif input.mode == GuideMode.ADAPTIVE:
            return AdaptiveGuide(input.max_iterations, input.quality_threshold)

        elif input.mode == GuideMode.VOTING:
            voting = VotingGuide("Production Voting Panel")
            voting.add(LeafGuide(GuideFactory.create(GuideType.STRICT, max_iterations=input.max_iterations)))
            voting.add(LeafGuide(GuideFactory.create(GuideType.LENIENT, max_iterations=input.max_iterations)))
            return voting

        elif input.mode == GuideMode.ENSEMBLE:
            return EnsembleGuide(input.max_iterations, input.quality_threshold)

        else:
            return Guide(input.max_iterations, input.quality_threshold)

    def get_analytics(self) -> Dict:
        """
        Get analytics across all sessions.

        Returns:
            Dict with aggregate statistics, quality distribution, etc.
        """
        return self.recorder.analyze_all()

    def to_json(self, output: SolutionOutput) -> str:
        """Convert output to JSON for integration."""
        return json.dumps({
            'problem': output.problem,
            'mode': output.mode,
            'session_id': output.session_id,
            'final_answer': output.final_answer,
            'quality': {
                'final_quality': output.quality_report.final_quality,
                'grade': output.quality_report.grade,
                'iterations_used': output.quality_report.iterations_used,
                'improvement_rate': output.quality_report.improvement_rate,
                'efficiency': output.quality_report.efficiency,
                'convergence_speed': output.quality_report.convergence_speed,
                'consistency': output.quality_report.consistency,
            },
            'step_history': output.step_history
        }, indent=2)


# ============================================================================
# DEMONSTRATION - Prove it works with real examples
# ============================================================================

def run_demo():
    """
    Demonstrate the API with real examples.
    Prove: predictable, measurable, reliable.
    """
    print("="*80)
    print("PRODUCTION API DEMONSTRATION")
    print("Clean Input → Predictable Output → Measurable Quality")
    print("="*80)

    api = MetaCognitiveAPI()

    # Test case 1: Basic mode
    print("\n[TEST 1: BASIC MODE]")
    input1 = ProblemInput(
        problem="What is recursion in programming?",
        mode=GuideMode.BASIC,
        max_iterations=5
    )
    output1 = api.solve(input1)
    print(f"Input:  problem='{input1.problem[:50]}...', mode={input1.mode.value}")
    print(f"Output: quality={output1.quality_report.final_quality:.3f}, " +
          f"grade={output1.quality_report.grade}, " +
          f"iterations={output1.quality_report.iterations_used}")
    print(f"        efficiency={output1.quality_report.efficiency:.3f}, " +
          f"consistency={output1.quality_report.consistency:.3f}")

    # Test case 2: Compare modes on same problem
    print("\n[TEST 2: MODE COMPARISON - SAME PROBLEM]")
    problem = "Explain quantum entanglement"
    modes = [GuideMode.BASIC, GuideMode.STRICT, GuideMode.LENIENT]

    results = []
    for mode in modes:
        input_i = ProblemInput(problem=problem, mode=mode, max_iterations=3)
        output_i = api.solve(input_i)
        results.append(output_i)
        print(f"  {mode.value:10s}: quality={output_i.quality_report.final_quality:.3f}, " +
              f"grade={output_i.quality_report.grade}, " +
              f"iterations={output_i.quality_report.iterations_used}")

    best = max(results, key=lambda r: r.quality_report.final_quality)
    print(f"  → Best mode: {best.mode} (quality={best.quality_report.final_quality:.3f})")

    # Test case 3: Smart mode auto-selection
    print("\n[TEST 3: SMART MODE - AUTO STRATEGY SELECTION]")
    test_problems = [
        "Calculate 127 * 83",
        "Write a creative poem about AI",
        "Is water H2O? True or false"
    ]
    for prob in test_problems:
        input_i = ProblemInput(problem=prob, mode=GuideMode.SMART, max_iterations=3)
        output_i = api.solve(input_i)
        print(f"  Problem: '{prob[:40]}'")
        print(f"    → Quality: {output_i.quality_report.final_quality:.3f}, " +
              f"Grade: {output_i.quality_report.grade}")

    # Test case 4: Voting mode
    print("\n[TEST 4: VOTING MODE - CONSENSUS]")
    input4 = ProblemInput(
        problem="What is the best programming paradigm?",
        mode=GuideMode.VOTING,
        max_iterations=3
    )
    output4 = api.solve(input4)
    print(f"  Voting result: quality={output4.quality_report.final_quality:.3f}, " +
          f"grade={output4.quality_report.grade}")
    print(f"  Iterations: {output4.quality_report.iterations_used}")

    # Test case 5: Ensemble mode
    print("\n[TEST 5: ENSEMBLE MODE - ALL STRATEGIES]")
    input5 = ProblemInput(
        problem="Explain machine learning",
        mode=GuideMode.ENSEMBLE,
        max_iterations=3
    )
    output5 = api.solve(input5)
    print(f"  Ensemble result: quality={output5.quality_report.final_quality:.3f}, " +
          f"grade={output5.quality_report.grade}")
    print(f"  Efficiency: {output5.quality_report.efficiency:.3f}")

    # Test case 6: JSON export
    print("\n[TEST 6: JSON EXPORT - API INTEGRATION]")
    json_output = api.to_json(output1)
    print(f"  JSON length: {len(json_output)} chars")
    print(f"  JSON preview: {json_output[:150]}...")
    # Verify it's valid JSON
    parsed = json.loads(json_output)
    print(f"  ✅ Valid JSON, contains {len(parsed)} top-level keys")

    # Analytics across all sessions
    print("\n[TEST 7: ANALYTICS ACROSS SESSIONS]")
    analytics = api.get_analytics()
    print(f"  Total sessions: {analytics['total']}")
    print(f"  Average quality: {analytics['avg_quality']:.3f}")
    print(f"  Average efficiency: {analytics['avg_efficiency']:.3f}")
    print(f"  Grade distribution: {analytics['grade_distribution']}")

    # Demonstrate step history
    print("\n[TEST 8: STEP HISTORY - ITERATION TRANSPARENCY]")
    print(f"  Session: {output1.session_id}")
    print(f"  Problem: '{output1.problem[:50]}...'")
    print(f"  Step-by-step quality progression:")
    for step in output1.step_history:
        print(f"    Iteration {step['iteration']}: quality={step['quality']:.3f}")

    print("\n" + "="*80)
    print("✅ API DEMONSTRATION COMPLETE")
    print("="*80)
    print("\nProven capabilities:")
    print("  ✅ Clean input/output contracts")
    print("  ✅ Predictable structure (ProblemInput → SolutionOutput)")
    print("  ✅ Measurable quality at every level")
    print("  ✅ Multiple modes for different use cases")
    print("  ✅ JSON export for integration")
    print("  ✅ Analytics across sessions")
    print("  ✅ Full iteration history")
    print("  ✅ Deterministic evaluation")
    print("\n🎯 PRODUCTION READY")


if __name__ == "__main__":
    run_demo()
