"""
Solution Engineering System

Proposes and implements solutions to problems:
- Code modifications
- Configuration changes
- Architecture changes
- New capabilities
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from enum import Enum

from .diagnostician import Diagnosis


class SolutionType(Enum):
    """Types of solutions."""
    CODE_MODIFICATION = "code_modification"
    CONFIGURATION_CHANGE = "configuration_change"
    ARCHITECTURE_CHANGE = "architecture_change"
    NEW_CAPABILITY = "new_capability"
    WORKAROUND = "workaround"
    UNKNOWN = "unknown"


class RiskLevel(Enum):
    """Risk levels for solutions."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Solution:
    """A proposed solution to a problem."""
    type: SolutionType
    description: str
    implementation: str  # Description of how to implement
    risk: RiskLevel
    estimated_effort: int  # Estimated hours/difficulty
    files_to_modify: List[str] = None
    code_changes: Optional[Dict[str, str]] = None  # file_path -> new_code
    
    def __post_init__(self):
        """Initialize files_to_modify if not provided."""
        if self.files_to_modify is None:
            self.files_to_modify = []


@dataclass
class ImplementationResult:
    """Result of implementing a solution."""
    success: bool
    error: Optional[str] = None
    modified_files: List[str] = None
    backup_path: Optional[str] = None
    test_results: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize modified_files if not provided."""
        if self.modified_files is None:
            self.modified_files = []


class SolutionEngineer:
    """Engineers solutions to problems."""
    
    # Solution templates for common problems
    SOLUTION_TEMPLATES = {
        "INTERACTIVE_INPUT_REQUIRED": {
            "type": SolutionType.CODE_MODIFICATION,
            "description": "Add non-interactive mode to scenario",
            "implementation": "Modify scenario to accept optional input stream or use default choices",
            "risk": RiskLevel.LOW,
            "estimated_effort": 2,
            "files": ["examples/tavern_scenario.py", "examples/tavern_scenario_evolved.py"]
        },
        "POOR_DECISION_LOGIC": {
            "type": SolutionType.CODE_MODIFICATION,
            "description": "Improve decision weights in being_make_choice",
            "implementation": "Adjust skill weights, add memory-based learning, improve personality influence",
            "risk": RiskLevel.MEDIUM,
            "estimated_effort": 5,
            "files": ["examples/tavern_scenario_evolved.py"]
        },
        "MISSING_DEPENDENCY": {
            "type": SolutionType.CONFIGURATION_CHANGE,
            "description": "Install missing dependency",
            "implementation": "Add dependency to pyproject.toml and install",
            "risk": RiskLevel.LOW,
            "estimated_effort": 1,
            "files": ["pyproject.toml"]
        },
        "FILE_NOT_FOUND": {
            "type": SolutionType.CODE_MODIFICATION,
            "description": "Create missing file or fix path",
            "implementation": "Create file with default content or fix file path reference",
            "risk": RiskLevel.LOW,
            "estimated_effort": 1,
            "files": []
        },
        "PERMISSION_DENIED": {
            "type": SolutionType.CONFIGURATION_CHANGE,
            "description": "Fix file permissions",
            "implementation": "Change file permissions or run with appropriate privileges",
            "risk": RiskLevel.MEDIUM,
            "estimated_effort": 1,
            "files": []
        },
        "PERFORMANCE_DEGRADATION": {
            "type": SolutionType.CODE_MODIFICATION,
            "description": "Optimize performance",
            "implementation": "Add caching, reduce complexity, optimize algorithms",
            "risk": RiskLevel.MEDIUM,
            "estimated_effort": 8,
            "files": []
        }
    }
    
    def __init__(self):
        """Initialize solution engineer."""
        self.solution_history: List[Solution] = []
        self.implementation_history: List[ImplementationResult] = []
    
    def propose_solution(self, diagnosis: Diagnosis) -> Solution:
        """
        Propose solution based on diagnosis.
        
        Args:
            diagnosis: The diagnosis of the problem
        
        Returns:
            Proposed solution
        """
        # Look up solution template
        if diagnosis.cause in self.SOLUTION_TEMPLATES:
            template = self.SOLUTION_TEMPLATES[diagnosis.cause]
            solution = Solution(
                type=template["type"],
                description=template["description"],
                implementation=template["implementation"],
                risk=template["risk"],
                estimated_effort=template["estimated_effort"],
                files_to_modify=template.get("files", [])
            )
        else:
            # Generic solution
            solution = Solution(
                type=SolutionType.UNKNOWN,
                description=f"Address {diagnosis.cause}",
                implementation=diagnosis.solution_hint,
                risk=RiskLevel.MEDIUM,
                estimated_effort=5
            )
        
        self.solution_history.append(solution)
        return solution
    
    def implement_solution(
        self,
        solution: Solution,
        modification_engine: Optional[Any] = None  # SelfModificationEngine
    ) -> ImplementationResult:
        """
        Implement solution with safety checks.
        
        Args:
            solution: The solution to implement
            modification_engine: SelfModificationEngine instance (optional)
        
        Returns:
            Implementation result
        """
        # If modification engine provided, use it
        if modification_engine:
            try:
                result = modification_engine.modify_code(
                    solution.files_to_modify[0] if solution.files_to_modify else None,
                    solution
                )
                self.implementation_history.append(result)
                return result
            except Exception as e:
                return ImplementationResult(
                    success=False,
                    error=f"Modification engine error: {str(e)}"
                )
        
        # Otherwise, return placeholder (actual implementation would go here)
        return ImplementationResult(
            success=False,
            error="No modification engine provided - solution not implemented"
        )
    
    def get_solution_history(self, count: int = 10) -> List[Solution]:
        """Get recent solution history."""
        return self.solution_history[-count:] if self.solution_history else []
    
    def get_implementation_history(self, count: int = 10) -> List[ImplementationResult]:
        """Get recent implementation history."""
        return self.implementation_history[-count:] if self.implementation_history else []
