"""
Self-Engineering System: The Meta-Game

Enables the system to:
1. Detect when it can't play itself
2. Diagnose why it can't
3. Engineer solutions
4. Iterate on itself
5. Journal findings and reflect
6. Create actionable work (scenarios, quests, work efforts)
"""

from .actionable_creator import ActionableCreator
from .notebook import ActionableType, NotebookEntry, NotebookEntryType, NotebookManager, Reflection
from .problem_detector import Problem, ProblemDetector, ProblemType, Severity
from .refinement_detector import RefinementDetector, RefinementOpportunity

# Future imports (when implemented)
# from .diagnostician import Diagnosis, ProblemDiagnostician
# from .solution_engineer import Solution, SolutionEngineer
# from .self_modification import SelfModificationEngine, ModificationResult
# from .iteration_loop import SelfEngineeringLoop, IterationResult

__all__ = [
    "Problem",
    "ProblemDetector",
    "ProblemType",
    "Severity",
    "NotebookManager",
    "NotebookEntry",
    "NotebookEntryType",
    "Reflection",
    "ActionableType",
    "ActionableCreator",
    "RefinementDetector",
    "RefinementOpportunity",
    # Future exports
    # "Diagnosis",
    # "ProblemDiagnostician",
    # "Solution",
    # "SolutionEngineer",
    # "SelfModificationEngine",
    # "ModificationResult",
    # "SelfEngineeringLoop",
    # "IterationResult",
]
