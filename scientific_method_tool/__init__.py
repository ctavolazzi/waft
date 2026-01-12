"""
Scientific Method Tool

Implements a rudimentary version of the scientific method for experimental verification:
1. Form hypothesis
2. Design experiment
3. Capture initial state (A)
4. Run experiment
5. Collect data during experiment (C)
6. Capture final state (B)
7. Analyze results
8. Verify or refute hypothesis
9. Iterate with variable changes
"""

from .experiment import Experiment, ExperimentState, ExperimentManager
from .hypothesis import Hypothesis, Variable, VariableType
from .state_capture import StateCapture, SystemState
from .data_collection import DataCollector, DataPoint, DataSeries
from .experiment_loop import ExperimentLoop, ExperimentResult, IterationConfig
from .analysis import ExperimentAnalyzer, AnalysisResult

__all__ = [
    "Experiment",
    "ExperimentState",
    "ExperimentManager",
    "Hypothesis",
    "Variable",
    "VariableType",
    "StateCapture",
    "SystemState",
    "DataCollector",
    "DataPoint",
    "DataSeries",
    "ExperimentLoop",
    "ExperimentResult",
    "IterationConfig",
    "ExperimentAnalyzer",
    "AnalysisResult",
]
