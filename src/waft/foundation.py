"""
DocumentEngine - Reusable Research Documentation Library

A content-agnostic PDF generation engine with modular content blocks,
automatic redaction, and configurable styling. Designed for scientific logs,
legal audits, journalism, and structured documentation.

The engine is completely portable - no WAFT-specific dependencies.
"""

import random
from dataclasses import dataclass

if TYPE_CHECKING:
    from ..core.science.observer import TheObserver
    from ..core.tavern_keeper import TavernKeeper

try:
    from fpdf import FPDF
except ImportError:
    raise ImportError("fpdf2 is required. Install with: pip install fpdf2>=2.7.0")


class RedactionStyle(Enum):
    """Redaction rendering styles."""

    BLACK_BAR = "black_bar"
    BLUR = "blur"  # Falls back to BLACK_BAR if not supported
    CROSS_OUT = "cross_out"


@dataclass
class DocumentConfig:
    """Configuration for document styling and behavior."""

    problem → answer → evaluation

    This is the core cycle, executed once.
    """

    @classmethod
    def scientific_log(cls) -> "DocumentConfig":
        """Preset config for scientific documentation."""
        return cls(
            fonts={
                "Header": ("Courier", "B"),
                "Body": ("Courier", ""),
                "Monospace": ("Courier", ""),
            },
            watermark="DRAFT",
            redaction_style=RedactionStyle.BLACK_BAR,
        )

    @classmethod
    def legal_audit(cls) -> "DocumentConfig":
        """Preset config for legal documentation."""
        return cls(
            fonts={
                "Header": "Courier-Bold",
                "Body": "Courier",
                "Monospace": "Courier",
            },
            watermark="CONFIDENTIAL",
            redaction_style=RedactionStyle.BLACK_BAR,
        )


class ContentBlock(ABC):
    """Abstract base class for all content blocks."""

    @abstractmethod
    def render(
        self,
        pdf: FPDF,
        config: DocumentConfig,
        redactor: "AutoRedactor",
        y_position: float,
    ) -> float:
        """
        Render the content block to PDF.

        Args:
            pdf: FPDF instance
            config: Document configuration
            redactor: AutoRedactor instance for automatic redaction
            y_position: Current Y position on page

        Returns:
            New Y position after rendering
        """
        pass

    return Step(problem=problem, answer=answer, evaluation=evaluation, iteration_number=iteration)


# ============================================================================
# SECTION B: THE IMPLEMENTATION (Story Script)
# ============================================================================


@dataclass
class Session:
    """
    Generate the Specimen-D Audit dossier using DocumentEngine.

    This demonstrates the API by building the document programmatically
    using content blocks instead of hardcoded FPDF calls.
    """
    if output_path is None:
        output_path = Path("_work_efforts/WAFT_SPECIMEN_D_AUDIT_v2.pdf")

    # Configure for Site-Delta-9 dossier style
    config = DocumentConfig.classified_dossier(
        header="SITE-DELTA-9 // BIO-LOG",
        watermark="INTERNAL USE ONLY",
    )

    # Initialize engine
    engine = DocumentEngine(config)

    # Set sensitive terms for automatic redaction
    engine.add_sensitive_terms(
        [
            "001-ALPHA-GENESIS",
            "Sunset District",
            "N-Judah",
            "Fai Wei Tam",
            "TAM",
            "FAI WEI",
        ]
    )

    @property
    def converged(self) -> bool:
        """Did we reach good quality?"""
        return (
            self.final_evaluation.is_good(self.quality_threshold)
            if self.final_evaluation
            else False
        )
    )


# ============================================================================
# SECTION C: THE FOUNDATION (WAFT Integration Layer)
# ============================================================================


class TheFoundation:
    """
    The Guide: Meta-cognitive reasoning system.

    Built on core primitives:
    - Score (atomic quality)
    - Evaluation (multi-dimensional quality)
    - Step (one reasoning cycle)
    - Session (complete loop)
    """

    def __init__(
        self,
        project_path: Path,
        observer: Optional["TheObserver"] = None,
        tavern_keeper: Optional["TavernKeeper"] = None,
        empirica_manager=None,
    ) -> None:
        """
        Initialize TheFoundation.

    def solve(self, problem: str) -> Session:
        """Solve a problem using iterative reasoning."""
        return solve(
            problem=problem,
            max_iterations=self.max_iterations,
            quality_threshold=self.quality_threshold,
        )



if __name__ == "__main__":
    print("=" * 80)
    print("TESTING THE CORE")
    print("=" * 80)

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

    print("\n" + "=" * 80)
    print("CORE VERIFIED")
    print("=" * 80)
    print("\nBuilt from ground up:")
    print("  Level 0: Score (atomic data type)")
    print("  Level 1: evaluate_text() (core function)")
    print("  Level 2: Evaluation (multi-dimensional)")
    print("  Level 3: Step (one cycle)")
    print("  Level 4: Session (complete loop)")
    print("  Level 5: Guide (class wrapper)")
