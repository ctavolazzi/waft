"""
Experiment System

Manages individual experiments with state capture and data collection.
"""

import json
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .data_collection import DataCollector
from .hypothesis import Hypothesis
from .state_capture import StateCapture, SystemState


class ExperimentState:
    """States of an experiment."""

    DESIGNED = "designed"
    INITIALIZED = "initialized"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ANALYZED = "analyzed"


@dataclass
class Experiment:
    """A single experiment."""

    experiment_id: str
    hypothesis: Hypothesis
    state: str = ExperimentState.DESIGNED
    initial_state: SystemState | None = None
    final_state: SystemState | None = None
    data_collector: DataCollector | None = None
    results: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: str | None = None
    completed_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "experiment_id": self.experiment_id,
            "hypothesis": self.hypothesis.to_dict(),
            "state": self.state,
            "initial_state": self.initial_state.to_dict() if self.initial_state else None,
            "final_state": self.final_state.to_dict() if self.final_state else None,
            "results": self.results,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Experiment":
        """Create from dictionary."""
        from .state_capture import SystemState

        experiment = cls(
            experiment_id=data["experiment_id"],
            hypothesis=Hypothesis.from_dict(data["hypothesis"]),
            state=data.get("state", ExperimentState.DESIGNED),
            results=data.get("results", {}),
            metadata=data.get("metadata", {}),
            created_at=data.get("created_at", datetime.now().isoformat()),
            started_at=data.get("started_at"),
            completed_at=data.get("completed_at"),
        )

        if data.get("initial_state"):
            experiment.initial_state = SystemState.from_dict(data["initial_state"])
        if data.get("final_state"):
            experiment.final_state = SystemState.from_dict(data["final_state"])

        return experiment


class ExperimentManager:
    """Manages experiments."""

    def __init__(self, storage_path: Path):
        """
        Initialize experiment manager.

        Args:
            storage_path: Path to store experiments (relative or absolute)
        """
        # Use storage path resolver to route to external drive if available
        try:
            import sys
            from pathlib import Path as PathType

            # Try to import from src/waft/utils
            project_root = PathType(__file__).parent.parent
            sys.path.insert(0, str(project_root))
            from src.waft.utils import get_storage_path

            # Resolve storage path (routes to external drive if augmented content)
            resolved_storage = get_storage_path(PathType(storage_path))
            self.storage_path = resolved_storage
        except (ImportError, Exception):
            # Fallback to original behavior if storage resolver not available
            self.storage_path = Path(storage_path)

        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.experiments_path = self.storage_path / "experiments"
        self.states_path = self.storage_path / "states"
        self.data_path = self.storage_path / "data"

        self.experiments_path.mkdir(exist_ok=True)
        self.states_path.mkdir(exist_ok=True)
        self.data_path.mkdir(exist_ok=True)

        self.state_capture = StateCapture(self.states_path)

    def create_experiment(
        self, hypothesis: Hypothesis, metadata: dict[str, Any] | None = None
    ) -> Experiment:
        """
        Create a new experiment.

        Args:
            hypothesis: Hypothesis to test
            metadata: Optional metadata

        Returns:
            Experiment instance
        """
        experiment_id = f"exp_{uuid.uuid4().hex[:8]}"

        experiment = Experiment(
            experiment_id=experiment_id, hypothesis=hypothesis, metadata=metadata or {}
        )

        # Create data collector
        experiment.data_collector = DataCollector(self.data_path)

        # Save experiment
        self._save_experiment(experiment)

        return experiment

    def capture_initial_state(
        self,
        experiment: Experiment,
        components: dict[str, Any],
        metadata: dict[str, Any] | None = None,
    ) -> SystemState:
        """
        Capture initial state (A) of the system.

        Args:
            experiment: Experiment instance
            components: System components to capture
            metadata: Optional metadata

        Returns:
            Initial system state
        """
        initial_state = self.state_capture.capture_state(
            state_type="initial",
            components=components,
            metadata={"experiment_id": experiment.experiment_id, **(metadata or {})},
        )

        experiment.initial_state = initial_state
        experiment.state = ExperimentState.INITIALIZED
        self._save_experiment(experiment)

        return initial_state

    def capture_final_state(
        self,
        experiment: Experiment,
        components: dict[str, Any],
        metadata: dict[str, Any] | None = None,
    ) -> SystemState:
        """
        Capture final state (B) of the system.

        Args:
            experiment: Experiment instance
            components: System components to capture
            metadata: Optional metadata

        Returns:
            Final system state
        """
        final_state = self.state_capture.capture_state(
            state_type="final",
            components=components,
            metadata={"experiment_id": experiment.experiment_id, **(metadata or {})},
        )

        experiment.final_state = final_state
        experiment.completed_at = datetime.now().isoformat()
        experiment.state = ExperimentState.COMPLETED

        # Save data
        if experiment.data_collector:
            experiment.data_collector.save(experiment.experiment_id)

        self._save_experiment(experiment)

        return final_state

    def run_experiment(
        self,
        experiment: Experiment,
        experiment_function: Callable[[Experiment], dict[str, Any]],
        initial_components: dict[str, Any],
        final_components: Callable[[], dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Run an experiment.

        Args:
            experiment: Experiment instance
            experiment_function: Function that runs the experiment
            initial_components: Initial system components
            final_components: Function that returns final components (or None to use initial)

        Returns:
            Experiment results
        """
        # Capture initial state (A)
        self.capture_initial_state(experiment, initial_components)

        # Start experiment
        experiment.state = ExperimentState.RUNNING
        experiment.started_at = datetime.now().isoformat()
        self._save_experiment(experiment)

        try:
            # Run experiment (data collection happens inside experiment_function)
            results = experiment_function(experiment)
            experiment.results = results

            # Capture final state (B)
            if final_components:
                final_comp = final_components()
            else:
                final_comp = initial_components  # Use initial if no final function

            self.capture_final_state(experiment, final_comp)

            return results

        except Exception as e:
            experiment.state = ExperimentState.FAILED
            experiment.results = {"error": str(e)}
            self._save_experiment(experiment)
            raise

    def _save_experiment(self, experiment: Experiment):
        """Save experiment to file."""
        filename = f"{experiment.experiment_id}.json"
        filepath = self.experiments_path / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(experiment.to_dict(), f, indent=2, default=str)

    def load_experiment(self, experiment_id: str) -> Experiment | None:
        """Load experiment by ID."""
        filename = f"{experiment_id}.json"
        filepath = self.experiments_path / filename

        if not filepath.exists():
            return None

        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

        experiment = Experiment.from_dict(data)

        # Load data collector
        if experiment.data_collector is None:
            experiment.data_collector = DataCollector(self.data_path)
        experiment.data_collector.load(experiment_id)

        return experiment

    def list_experiments(self) -> list[str]:
        """List all experiment IDs."""
        return [f.stem for f in self.experiments_path.glob("exp_*.json")]
