"""
Experiment Loop System

Runs iterative experiments with variable changes for hypothesis testing.
"""

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .experiment import Experiment, ExperimentManager
from .hypothesis import Hypothesis


@dataclass
class ExperimentResult:
    """Result of a single experiment run."""

    experiment_id: str
    hypothesis_verified: bool | None
    confidence: float
    data_summary: dict[str, Any]
    state_changes: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class IterationConfig:
    """Configuration for experiment iterations."""

    variable_name: str
    values: list[Any]  # List of values to test
    description: str = ""


class ExperimentLoop:
    """Runs iterative experiments with variable changes."""

    def __init__(self, storage_path: Path):
        """
        Initialize experiment loop.

        Args:
            storage_path: Path to store experiments and data
        """
        self.storage_path = Path(storage_path)
        self.manager = ExperimentManager(self.storage_path)
        self.results: list[ExperimentResult] = []

    def run_iterative_experiment(
        self,
        hypothesis: Hypothesis,
        experiment_function: Callable[[Experiment], dict[str, Any]],
        initial_components_function: Callable[[dict[str, Any]], dict[str, Any]],
        final_components_function: Callable[[], dict[str, Any]] | None = None,
        iteration_configs: list[IterationConfig] | None = None,
        max_iterations: int = 10,
    ) -> list[ExperimentResult]:
        """
        Run iterative experiments with variable changes.

        Args:
            hypothesis: Hypothesis to test
            experiment_function: Function that runs the experiment
            initial_components_function: Function that creates initial components based on variables
            final_components_function: Optional function that returns final components
            iteration_configs: List of variable configurations to iterate over
            max_iterations: Maximum number of iterations

        Returns:
            List of experiment results
        """
        self.results = []
        iteration_configs = iteration_configs or []

        # Get independent variables from hypothesis
        independent_vars = hypothesis.get_independent_variables()

        # If no iteration configs provided, use independent variables
        if not iteration_configs:
            for var in independent_vars:
                if var.range:
                    # Generate values from range
                    min_val, max_val = var.range
                    step = (max_val - min_val) / max_iterations
                    values = [min_val + step * i for i in range(max_iterations)]
                else:
                    # Use single value
                    values = [var.value]

                iteration_configs.append(
                    IterationConfig(
                        variable_name=var.name,
                        values=values,
                        description=f"Iterating over {var.name}",
                    )
                )

        # Run experiments for each variable configuration
        for config in iteration_configs:
            for value in config.values:
                # Create experiment with modified variable
                modified_hypothesis = self._modify_hypothesis(
                    hypothesis, config.variable_name, value
                )

                # Create experiment
                experiment = self.manager.create_experiment(
                    modified_hypothesis,
                    metadata={
                        "iteration_config": config.variable_name,
                        "iteration_value": value,
                        "iteration_description": config.description,
                    },
                )

                # Create initial components with current variable values
                var_values = {
                    var.name: var.value for var in modified_hypothesis.get_independent_variables()
                }
                initial_components = initial_components_function(var_values)

                # Run experiment
                try:
                    results = self.manager.run_experiment(
                        experiment,
                        experiment_function,
                        initial_components,
                        final_components_function,
                    )

                    # Analyze results
                    result = self._analyze_experiment(experiment, results)
                    self.results.append(result)

                except Exception as e:
                    # Record failed experiment
                    result = ExperimentResult(
                        experiment_id=experiment.experiment_id,
                        hypothesis_verified=False,
                        confidence=0.0,
                        data_summary={"error": str(e)},
                        state_changes={},
                        metadata={"failed": True, "error": str(e)},
                    )
                    self.results.append(result)

        # Save results summary
        self._save_results_summary()

        return self.results

    def _modify_hypothesis(
        self, hypothesis: Hypothesis, variable_name: str, new_value: Any
    ) -> Hypothesis:
        """Create a modified hypothesis with changed variable value."""
        import copy

        # Deep copy hypothesis
        modified = Hypothesis(
            statement=hypothesis.statement,
            prediction=hypothesis.prediction,
            variables=[copy.deepcopy(v) for v in hypothesis.variables],
            created_at=hypothesis.created_at,
        )

        # Modify variable
        var = modified.get_variable(variable_name)
        if var:
            var.value = new_value

        return modified

    def _analyze_experiment(
        self, experiment: Experiment, results: dict[str, Any]
    ) -> ExperimentResult:
        """Analyze experiment results."""
        # Compare states
        state_changes = {}
        if experiment.initial_state and experiment.final_state:
            state_changes = self.manager.state_capture.compare_states(
                experiment.initial_state, experiment.final_state
            )

        # Summarize data
        data_summary = {}
        if experiment.data_collector:
            all_series = experiment.data_collector.get_all_series()
            for name, series in all_series.items():
                values = series.get_values()
                if values:
                    data_summary[name] = {
                        "count": len(values),
                        "min": min(values) if isinstance(values[0], (int, float)) else None,
                        "max": max(values) if isinstance(values[0], (int, float)) else None,
                        "mean": sum(values) / len(values)
                        if isinstance(values[0], (int, float))
                        else None,
                        "last": values[-1],
                    }

        # Determine if hypothesis verified (placeholder - would need actual analysis)
        hypothesis_verified = None
        confidence = 0.0

        # Simple verification: check if prediction matches results
        if "prediction_match" in results:
            hypothesis_verified = results["prediction_match"]
            confidence = results.get("confidence", 0.5)

        return ExperimentResult(
            experiment_id=experiment.experiment_id,
            hypothesis_verified=hypothesis_verified,
            confidence=confidence,
            data_summary=data_summary,
            state_changes=state_changes,
            metadata=experiment.metadata,
        )

    def _save_results_summary(self):
        """Save results summary to file."""
        summary = {
            "total_experiments": len(self.results),
            "verified": sum(1 for r in self.results if r.hypothesis_verified is True),
            "refuted": sum(1 for r in self.results if r.hypothesis_verified is False),
            "inconclusive": sum(1 for r in self.results if r.hypothesis_verified is None),
            "results": [self._result_to_dict(r) for r in self.results],
        }

        filename = f"results_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.storage_path / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, default=str)

    def _result_to_dict(self, result: ExperimentResult) -> dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "experiment_id": result.experiment_id,
            "hypothesis_verified": result.hypothesis_verified,
            "confidence": result.confidence,
            "data_summary": result.data_summary,
            "state_changes": result.state_changes,
            "metadata": result.metadata,
        }

    def get_results(self) -> list[ExperimentResult]:
        """Get all experiment results."""
        return self.results

    def get_verified_experiments(self) -> list[ExperimentResult]:
        """Get experiments that verified the hypothesis."""
        return [r for r in self.results if r.hypothesis_verified is True]

    def get_refuted_experiments(self) -> list[ExperimentResult]:
        """Get experiments that refuted the hypothesis."""
        return [r for r in self.results if r.hypothesis_verified is False]
