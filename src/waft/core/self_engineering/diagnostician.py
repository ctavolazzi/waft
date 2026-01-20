"""
Problem Diagnosis System

Diagnoses root causes of problems:
- Pattern matching for common failures
- Statistical analysis of failure patterns
- LLM reasoning for complex cases
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .problem_detector import Problem, ProblemType


class DiagnosisConfidence(Enum):
    """Confidence levels for diagnoses."""

    HIGH = "high"  # 0.8-1.0
    MEDIUM = "medium"  # 0.5-0.8
    LOW = "low"  # 0.0-0.5


@dataclass
class Diagnosis:
    """A diagnosis of a problem's root cause."""

    cause: str
    confidence: float  # 0.0-1.0
    explanation: str
    solution_hint: str
    related_problems: list[str] = None  # IDs or descriptions of related problems

    def __post_init__(self):
        """Initialize related_problems if not provided."""
        if self.related_problems is None:
            self.related_problems = []


class ProblemDiagnostician:
    """Diagnoses root causes of problems."""

    # Common failure patterns
    PATTERNS = {
        "INTERACTIVE_INPUT_REQUIRED": {
            "exception_types": ["EOFError"],
            "keywords": ["input", "readline", "stdin", "interactive"],
            "cause": "INTERACTIVE_INPUT_REQUIRED",
            "confidence": 0.9,
            "explanation": "System requires interactive input but running in non-interactive mode",
            "solution_hint": "Add non-interactive mode or input simulation",
        },
        "POOR_DECISION_LOGIC": {
            "indicators": ["low_fitness", "repeated_failures", "bad_choices"],
            "cause": "POOR_DECISION_LOGIC",
            "confidence": 0.7,
            "explanation": "Decision logic consistently produces poor outcomes",
            "solution_hint": "Improve decision weights or add new decision factors",
        },
        "MISSING_DEPENDENCY": {
            "exception_types": ["ImportError", "ModuleNotFoundError"],
            "keywords": ["No module named", "cannot import"],
            "cause": "MISSING_DEPENDENCY",
            "confidence": 0.8,
            "explanation": "Required module or dependency is missing",
            "solution_hint": "Install missing dependency or add to requirements",
        },
        "FILE_NOT_FOUND": {
            "exception_types": ["FileNotFoundError"],
            "keywords": ["No such file", "not found"],
            "cause": "FILE_NOT_FOUND",
            "confidence": 0.9,
            "explanation": "Required file or directory does not exist",
            "solution_hint": "Create missing file or fix path",
        },
        "PERMISSION_DENIED": {
            "exception_types": ["PermissionError"],
            "keywords": ["permission denied", "access denied"],
            "cause": "PERMISSION_DENIED",
            "confidence": 0.9,
            "explanation": "Insufficient permissions to access resource",
            "solution_hint": "Fix file permissions or run with appropriate privileges",
        },
        "PERFORMANCE_DEGRADATION": {
            "indicators": ["slow_execution", "timeout", "high_latency"],
            "cause": "PERFORMANCE_DEGRADATION",
            "confidence": 0.6,
            "explanation": "System performance has degraded",
            "solution_hint": "Optimize code, add caching, or reduce complexity",
        },
    }

    def __init__(self):
        """Initialize diagnostician."""
        self.diagnosis_history: list[Diagnosis] = []

    def diagnose(self, problem: Problem, system_state: dict[str, Any] | None = None) -> Diagnosis:
        """
        Diagnose root cause of problem.

        Args:
            problem: The problem to diagnose
            system_state: Current system state (optional)

        Returns:
            Diagnosis with root cause and solution hint
        """
        system_state = system_state or {}

        # Try pattern matching first
        diagnosis = self._pattern_match(problem)
        if diagnosis and diagnosis.confidence >= 0.7:
            self.diagnosis_history.append(diagnosis)
            return diagnosis

        # Try statistical analysis
        diagnosis = self._statistical_analysis(problem, system_state)
        if diagnosis and diagnosis.confidence >= 0.5:
            self.diagnosis_history.append(diagnosis)
            return diagnosis

        # Fallback to generic diagnosis
        diagnosis = Diagnosis(
            cause="UNKNOWN",
            confidence=0.3,
            explanation=f"Unable to determine root cause of {problem.type.value}",
            solution_hint="Investigate problem manually or collect more data",
        )
        self.diagnosis_history.append(diagnosis)
        return diagnosis

    def _pattern_match(self, problem: Problem) -> Diagnosis | None:
        """Match problem against known patterns."""
        problem_desc = problem.description.lower()
        exc_type = type(problem.exception).__name__ if problem.exception else ""

        for _pattern_name, pattern in self.PATTERNS.items():
            # Check exception types
            if "exception_types" in pattern:
                if exc_type in pattern["exception_types"]:
                    return Diagnosis(
                        cause=pattern["cause"],
                        confidence=pattern["confidence"],
                        explanation=pattern["explanation"],
                        solution_hint=pattern["solution_hint"],
                    )

            # Check keywords
            if "keywords" in pattern:
                if any(keyword.lower() in problem_desc for keyword in pattern["keywords"]):
                    return Diagnosis(
                        cause=pattern["cause"],
                        confidence=pattern["confidence"],
                        explanation=pattern["explanation"],
                        solution_hint=pattern["solution_hint"],
                    )

        return None

    def _statistical_analysis(
        self, problem: Problem, system_state: dict[str, Any]
    ) -> Diagnosis | None:
        """Analyze problem statistically."""
        # Check for repeated failures
        if problem.type == ProblemType.DECISION_QUALITY:
            decision_history = system_state.get("decision_history", [])
            if len(decision_history) >= 5:
                recent_failures = sum(1 for d in decision_history[-5:] if d.get("success") is False)
                if recent_failures >= 4:  # 4 out of 5 failed
                    return Diagnosis(
                        cause="POOR_DECISION_LOGIC",
                        confidence=0.7,
                        explanation="Decision logic consistently produces poor outcomes (4/5 recent failures)",
                        solution_hint="Improve decision weights or add new decision factors",
                    )

        # Check for performance degradation
        if problem.type == ProblemType.PERFORMANCE_ISSUE:
            execution_times = system_state.get("execution_times", [])
            if len(execution_times) >= 3:
                recent_avg = sum(execution_times[-3:]) / 3
                if recent_avg > system_state.get("baseline_time", 1.0) * 2:
                    return Diagnosis(
                        cause="PERFORMANCE_DEGRADATION",
                        confidence=0.6,
                        explanation=f"Execution time has degraded (avg {recent_avg:.2f}s vs baseline {system_state.get('baseline_time', 1.0):.2f}s)",
                        solution_hint="Optimize code, add caching, or reduce complexity",
                    )

        return None

    def get_diagnosis_history(self, count: int = 10) -> list[Diagnosis]:
        """Get recent diagnosis history."""
        return self.diagnosis_history[-count:] if self.diagnosis_history else []
