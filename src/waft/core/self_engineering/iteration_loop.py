"""
Self-Engineering Iteration Loop

Main loop that:
1. Tries to play the game
2. Detects problems
3. Diagnoses causes
4. Engineers solutions
5. Implements fixes
6. Tests improvements
7. Iterates
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Callable
import time
import traceback

from .problem_detector import ProblemDetector, Problem
from .diagnostician import ProblemDiagnostician, Diagnosis
from .solution_engineer import SolutionEngineer, Solution, ImplementationResult
from .self_modification import SelfModificationEngine


@dataclass
class Improvement:
    """An improvement made during iteration."""
    iteration: int
    problem: Problem
    diagnosis: Diagnosis
    solution: Solution
    implementation: ImplementationResult
    timestamp: float


@dataclass
class IterationResult:
    """Result of self-engineering iteration."""
    success: bool
    iterations: int
    improvements: List[Improvement]
    message: str
    final_state: Optional[Dict[str, Any]] = None


class SelfEngineeringLoop:
    """Main iteration loop for self-engineering."""
    
    def __init__(
        self,
        scenario_runner: Callable[[], Dict[str, Any]],
        project_path: Optional[str] = None
    ):
        """
        Initialize self-engineering loop.
        
        Args:
            scenario_runner: Function that runs the scenario and returns execution result
            project_path: Path to project root
        """
        self.scenario_runner = scenario_runner
        self.problem_detector = ProblemDetector()
        self.diagnostician = ProblemDiagnostician()
        self.solution_engineer = SolutionEngineer()
        self.modification_engine = SelfModificationEngine(project_path=project_path)
        
        self.improvements: List[Improvement] = []
        self.iteration_count = 0
    
    def run_iteration(self, max_iterations: int = 10) -> IterationResult:
        """
        Run self-engineering iteration loop.
        
        Args:
            max_iterations: Maximum number of iterations
        
        Returns:
            Iteration result with improvements made
        """
        iteration = 0
        
        while iteration < max_iterations:
            self.iteration_count = iteration + 1
            
            # 1. Try to play
            execution_result = self._run_scenario()
            
            # 2. Detect problems
            problems = self.problem_detector.monitor_execution(execution_result)
            
            if not problems:
                # No problems - system is working!
                return IterationResult(
                    success=True,
                    iterations=iteration + 1,
                    improvements=self.improvements,
                    message="System is functioning correctly - no problems detected",
                    final_state=execution_result
                )
            
            # 3. Diagnose causes
            diagnoses = []
            for problem in problems:
                diagnosis = self.diagnostician.diagnose(problem, execution_result)
                diagnoses.append((problem, diagnosis))
            
            # 4. Engineer solutions
            solutions = []
            for problem, diagnosis in diagnoses:
                solution = self.solution_engineer.propose_solution(diagnosis)
                solutions.append((problem, diagnosis, solution))
            
            # 5. Implement solutions (one at a time, with testing)
            for problem, diagnosis, solution in solutions:
                # Skip if solution is too risky
                if solution.risk.value in ["high", "critical"]:
                    continue  # Would need approval in real system
                
                # Implement solution
                result = self.solution_engineer.implement_solution(
                    solution,
                    modification_engine=self.modification_engine
                )
                
                if result.success:
                    improvement = Improvement(
                        iteration=iteration + 1,
                        problem=problem,
                        diagnosis=diagnosis,
                        solution=solution,
                        implementation=result,
                        timestamp=time.time()
                    )
                    self.improvements.append(improvement)
            
            iteration += 1
        
        return IterationResult(
            success=False,
            iterations=iteration,
            improvements=self.improvements,
            message=f"Reached max iterations ({max_iterations})"
        )
    
    def _run_scenario(self) -> Dict[str, Any]:
        """
        Run the scenario and capture execution data.
        
        Returns:
            Execution result with context, exceptions, fitness, etc.
        """
        start_time = time.time()
        execution_result = {
            "context": {},
            "fitness_gained": 0.0,
            "success": False
        }
        
        try:
            # Run scenario
            result = self.scenario_runner()
            
            # Capture results
            execution_result.update({
                "success": True,
                "fitness_gained": result.get("fitness_gained", 0.0),
                "context": {
                    "being_id": result.get("being_id"),
                    "character_name": result.get("character_name"),
                    "choices_made": result.get("choices_made", []),
                    **result.get("context", {})
                }
            })
            
        except Exception as e:
            # Capture exception
            execution_result.update({
                "success": False,
                "exception": e,
                "error": str(e),
                "error_message": str(e),
                "traceback": traceback.format_exc(),
                "context": {
                    "exception_type": type(e).__name__
                }
            })
        
        execution_result["duration"] = time.time() - start_time
        
        return execution_result
    
    def get_improvements(self) -> List[Improvement]:
        """Get all improvements made."""
        return self.improvements
    
    def get_recent_improvements(self, count: int = 5) -> List[Improvement]:
        """Get most recent improvements."""
        return sorted(
            self.improvements,
            key=lambda i: i.timestamp,
            reverse=True
        )[:count]
