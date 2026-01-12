"""
Problem Detection System

Monitors system execution and detects problems:
- Execution failures (exceptions, errors)
- Performance issues (slow, stuck, timeout)
- Decision quality (bad choices, low fitness)
- Missing capabilities (can't handle input, can't make decisions)
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from enum import Enum
import traceback
import time


class ProblemType(Enum):
    """Types of problems that can be detected."""
    EXECUTION_FAILURE = "execution_failure"
    PERFORMANCE_ISSUE = "performance_issue"
    DECISION_QUALITY = "decision_quality"
    MISSING_CAPABILITY = "missing_capability"
    STATE_ANOMALY = "state_anomaly"
    # Refinement opportunities (polish without redesign)
    ROUGH_EDGE = "rough_edge"  # Needs polish (formatting, naming, docs)
    CRACK = "crack"  # Small bug/inconsistency that can be fixed
    BROKEN_PART = "broken_part"  # Dead code, unused imports, etc.
    UNKNOWN = "unknown"


class Severity(Enum):
    """Problem severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Problem:
    """A detected problem in system execution."""
    type: ProblemType
    severity: Severity
    description: str
    context: Dict[str, Any]
    timestamp: float = None
    exception: Optional[Exception] = None
    traceback: Optional[str] = None
    
    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = time.time()


class ProblemDetector:
    """Detects problems in system execution."""
    
    # Thresholds
    TIMEOUT_THRESHOLD = 30.0  # seconds
    MIN_FITNESS_GAIN = 5.0
    MAX_DECISION_TIME = 5.0  # seconds
    
    def __init__(self, notebook_manager=None):
        """
        Initialize problem detector.
        
        Args:
            notebook_manager: Optional NotebookManager for automatic journaling
        """
        self.detected_problems: List[Problem] = []
        self.notebook_manager = notebook_manager
    
    def monitor_execution(
        self,
        execution_result: Dict[str, Any],
        execution_time: Optional[float] = None
    ) -> List[Problem]:
        """
        Monitor execution and detect problems.
        
        Args:
            execution_result: Result from execution (may contain exception, fitness, etc.)
            execution_time: Time taken for execution (if not in result)
        
        Returns:
            List of detected problems
        """
        problems = []
        
        # Check for exceptions
        if "exception" in execution_result or "error" in execution_result:
            exception = execution_result.get("exception") or execution_result.get("error")
            exc_type = type(exception).__name__ if exception else "UnknownError"
            exc_msg = str(exception) if exception else execution_result.get("error_message", "Unknown error")
            
            # Determine severity based on exception type
            severity = self._determine_severity_from_exception(exc_type, exc_msg)
            
            problems.append(Problem(
                type=ProblemType.EXECUTION_FAILURE,
                severity=severity,
                description=f"{exc_type}: {exc_msg}",
                context=execution_result.get("context", {}),
                exception=exception,
                traceback=execution_result.get("traceback")
            ))
        
        # Check for performance issues
        exec_time = execution_time or execution_result.get("duration", 0.0)
        if exec_time > self.TIMEOUT_THRESHOLD:
            problems.append(Problem(
                type=ProblemType.PERFORMANCE_ISSUE,
                severity=Severity.HIGH,
                description=f"Execution exceeded timeout threshold ({exec_time:.2f}s > {self.TIMEOUT_THRESHOLD}s)",
                context={
                    "execution_time": exec_time,
                    "threshold": self.TIMEOUT_THRESHOLD,
                    **execution_result.get("context", {})
                }
            ))
        elif exec_time > self.MAX_DECISION_TIME:
            problems.append(Problem(
                type=ProblemType.PERFORMANCE_ISSUE,
                severity=Severity.MEDIUM,
                description=f"Decision took longer than expected ({exec_time:.2f}s > {self.MAX_DECISION_TIME}s)",
                context={
                    "execution_time": exec_time,
                    "threshold": self.MAX_DECISION_TIME,
                    **execution_result.get("context", {})
                }
            ))
        
        # Check for decision quality
        fitness_gained = execution_result.get("fitness_gained", 0.0)
        if fitness_gained < self.MIN_FITNESS_GAIN:
            problems.append(Problem(
                type=ProblemType.DECISION_QUALITY,
                severity=Severity.LOW,
                description=f"Low fitness gain from decisions ({fitness_gained:.1f} < {self.MIN_FITNESS_GAIN})",
                context={
                    "fitness_gained": fitness_gained,
                    "min_fitness": self.MIN_FITNESS_GAIN,
                    **execution_result.get("context", {})
                }
            ))
        
        # Check for missing capabilities
        if execution_result.get("missing_capability"):
            problems.append(Problem(
                type=ProblemType.MISSING_CAPABILITY,
                severity=Severity.MEDIUM,
                description=f"Missing capability: {execution_result['missing_capability']}",
                context=execution_result.get("context", {})
            ))
        
        # Store problems
        self.detected_problems.extend(problems)
        
        # Auto-journal problems if notebook manager available
        if self.notebook_manager:
            for problem in problems:
                # Sanitize context for JSON serialization
                sanitized_context = {
                    "execution_time": exec_time,
                    "execution_result_keys": list(execution_result.keys()),
                    "has_exception": "exception" in execution_result or "error" in execution_result
                }
                # Add sanitized execution result (without exception objects)
                if "context" in execution_result:
                    sanitized_context["execution_context"] = execution_result["context"]
                if "duration" in execution_result:
                    sanitized_context["duration"] = execution_result["duration"]
                if "fitness_gained" in execution_result:
                    sanitized_context["fitness_gained"] = execution_result["fitness_gained"]
                
                self.notebook_manager.journal_problem(
                    problem,
                    context=sanitized_context
                )
        
        return problems
    
    def _determine_severity_from_exception(self, exc_type: str, exc_msg: str) -> Severity:
        """Determine severity from exception type and message."""
        # Critical: System crashes, data corruption
        if exc_type in ("SystemExit", "KeyboardInterrupt", "MemoryError"):
            return Severity.CRITICAL
        
        # High: Execution failures that prevent operation
        if exc_type in ("EOFError", "FileNotFoundError", "PermissionError", "ImportError"):
            return Severity.HIGH
        
        # Medium: Logic errors, validation failures
        if exc_type in ("ValueError", "TypeError", "AttributeError", "KeyError"):
            return Severity.MEDIUM
        
        # Low: Warnings, recoverable errors
        return Severity.LOW
    
    def get_recent_problems(self, count: int = 10) -> List[Problem]:
        """Get most recent problems."""
        return sorted(
            self.detected_problems,
            key=lambda p: p.timestamp,
            reverse=True
        )[:count]
    
    def clear_problems(self):
        """Clear detected problems."""
        self.detected_problems = []
