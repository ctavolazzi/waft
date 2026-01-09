"""
Workflow Decision Analysis - Quantitative decision matrix for workflow implementation.

Uses DecisionCLI to analyze workflow implementation options.
"""

from pathlib import Path
from typing import Dict, Any
from rich.console import Console

from .decision_cli import DecisionCLI


class WorkflowDecisionAnalyzer:
    """Analyzes workflow implementation options using decision matrix."""
    
    def __init__(self, project_path: Path):
        """
        Initialize workflow decision analyzer.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.console = Console()
        self.decision_cli = DecisionCLI(project_path)
    
    def analyze_workflow_options(self) -> Dict[str, Any]:
        """
        Run decision matrix analysis for workflow implementation options.
        
        Returns:
            Dictionary with decision results
        """
        problem = "How should we implement command chaining and workflow orchestration?"
        
        alternatives = [
            "Simple /setup only",
            "Full /workflow with NLP parsing",
            "Hybrid: /setup + /workflow with AI interpretation",
            "AI-native: Let AI interpret directly",
        ]
        
        criteria = {
            "Implementation Speed": 0.25,  # How fast to implement
            "Flexibility": 0.25,  # How flexible for future use
            "User Experience": 0.20,  # How natural/easy to use
            "Maintenance Complexity": 0.15,  # How complex to maintain
            "Immediate Value": 0.15,  # How quickly it solves the problem
        }
        
        criterion_descriptions = {
            "Implementation Speed": "Time to implement (lower is better, but inverted in scores)",
            "Flexibility": "Ability to handle various command sequences",
            "User Experience": "How natural and intuitive the interface is",
            "Maintenance Complexity": "Ongoing maintenance burden (lower is better, inverted)",
            "Immediate Value": "How quickly it solves the user's immediate need",
        }
        
        # Scores on 1-10 scale
        scores = {
            "Simple /setup only": {
                "Implementation Speed": 9.0,  # Very fast (1 hour)
                "Flexibility": 3.0,  # Limited to one sequence
                "User Experience": 7.0,  # Simple, but limited
                "Maintenance Complexity": 9.0,  # Very simple (low complexity = high score)
                "Immediate Value": 8.0,  # Solves immediate need well
            },
            "Full /workflow with NLP parsing": {
                "Implementation Speed": 4.0,  # Slow (4-6 hours)
                "Flexibility": 10.0,  # Maximum flexibility
                "User Experience": 8.0,  # Very natural
                "Maintenance Complexity": 5.0,  # Complex parsing logic
                "Immediate Value": 6.0,  # Takes time to implement
            },
            "Hybrid: /setup + /workflow with AI interpretation": {
                "Implementation Speed": 6.0,  # Medium (2-3 hours)
                "Flexibility": 8.0,  # Good flexibility
                "User Experience": 9.0,  # Natural, AI handles complexity
                "Maintenance Complexity": 7.0,  # Moderate (AI interpretation simpler than parsing)
                "Immediate Value": 9.0,  # Immediate /setup + future flexibility
            },
            "AI-native: Let AI interpret directly": {
                "Implementation Speed": 7.0,  # Fast (1-2 hours)
                "Flexibility": 9.0,  # Very flexible
                "User Experience": 10.0,  # Most natural
                "Maintenance Complexity": 6.0,  # Moderate (depends on AI)
                "Immediate Value": 7.0,  # Good, but less structured
            },
        }
        
        return self.decision_cli.run_decision_matrix(
            problem=problem,
            alternatives=alternatives,
            criteria=criteria,
            scores=scores,
            methodology="WSM",
            criterion_descriptions=criterion_descriptions,
            show_details=True,
            show_sensitivity=True
        )
