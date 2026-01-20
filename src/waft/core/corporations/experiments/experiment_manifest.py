"""
Experiment Manifest: Track experiment metadata

Maintains metadata about experiments including parameters, results, and versions.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from ..security import read_secure_json, write_secure_file


class ExperimentManifest:
    """
    Manifest tracking experiment metadata.

    Records:
    - Experiment parameters
    - Results and outcomes
    - Configuration versions
    - Run history
    """

    def __init__(
        self,
        experiment_id: str,
        name: str,
        description: str = "",
        created_at: datetime | None = None,
    ):
        """
        Initialize experiment manifest.

        Args:
            experiment_id: Experiment identifier
            name: Experiment name
            description: Experiment description
            created_at: Creation timestamp
        """
        self.experiment_id = experiment_id
        self.name = name
        self.description = description
        self.created_at = created_at or datetime.utcnow()

        # Configuration
        self.config_version: str = "1.0.0"
        self.config_path: str | None = None

        # Parameters
        self.parameters: dict[str, Any] = {}

        # Results
        self.results: list[dict[str, Any]] = []

        # Run history
        self.runs: list[dict[str, Any]] = []

    def add_run(
        self,
        run_id: str,
        start_date: datetime,
        end_date: datetime | None = None,
        ticks: int = 0,
        results: dict[str, Any] | None = None,
    ) -> None:
        """
        Record an experiment run.

        Args:
            run_id: Run identifier
            start_date: Run start date
            end_date: Run end date (if completed)
            ticks: Number of ticks executed
            results: Run results
        """
        run = {
            "run_id": run_id,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat() if end_date else None,
            "ticks": ticks,
            "results": results or {},
            "status": "completed" if end_date else "running",
        }

        self.runs.append(run)

    def add_result(self, result: dict[str, Any]) -> None:
        """Add a result to the experiment."""
        result["timestamp"] = datetime.utcnow().isoformat()
        self.results.append(result)

    def to_dict(self) -> dict[str, Any]:
        """Convert manifest to dictionary."""
        return {
            "experiment_id": self.experiment_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "config_version": self.config_version,
            "config_path": self.config_path,
            "parameters": self.parameters,
            "results": self.results,
            "runs": self.runs,
            "run_count": len(self.runs),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExperimentManifest":
        """Create ExperimentManifest from dictionary."""
        manifest = cls(
            experiment_id=data["experiment_id"],
            name=data["name"],
            description=data.get("description", ""),
            created_at=datetime.fromisoformat(
                data.get("created_at", datetime.utcnow().isoformat())
            ),
        )

        manifest.config_version = data.get("config_version", "1.0.0")
        manifest.config_path = data.get("config_path")
        manifest.parameters = data.get("parameters", {})
        manifest.results = data.get("results", [])
        manifest.runs = data.get("runs", [])

        return manifest

    def save(self, output_path: Path) -> None:
        """Save manifest to file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # CRITICAL: Use secure file write
        try:
            write_secure_file(output_path, json.dumps(self.to_dict(), indent=2), encoding="utf-8")
        except OSError as e:
            raise OSError(f"Failed to save experiment manifest to {output_path}: {e}")

    @classmethod
    def load(cls, manifest_path: Path) -> "ExperimentManifest":
        """Load manifest from file."""
        try:
            # CRITICAL: Use secure JSON read with size limits
            data = read_secure_json(manifest_path)
            return cls.from_dict(data)
        except (OSError, ValueError, json.JSONDecodeError) as e:
            raise ValueError(f"Failed to load experiment manifest from {manifest_path}: {e}")


def create_experiment_manifest(
    experiment_id: str,
    name: str,
    description: str = "",
    config_path: Path | None = None,
    output_dir: Path | None = None,
) -> ExperimentManifest:
    """
    Create a new experiment manifest.

    Args:
        experiment_id: Experiment identifier
        name: Experiment name
        description: Experiment description
        config_path: Path to experiment configuration
        output_dir: Directory to save manifest

    Returns:
        Created ExperimentManifest
    """
    manifest = ExperimentManifest(experiment_id=experiment_id, name=name, description=description)

    if config_path:
        manifest.config_path = str(config_path)

    if output_dir:
        manifest_path = output_dir / f"{experiment_id}_manifest.json"
        manifest.save(manifest_path)

    return manifest
