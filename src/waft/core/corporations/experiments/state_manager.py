"""
Simulation State Manager: Save/load simulation checkpoints

Manages saving and loading simulation state at any point for resuming experiments.
"""

import json
from datetime import datetime
from pathlib import Path

from ..corporation import Corporation
from ..security import (
    read_secure_json,
    set_directory_permissions,
    validate_path_in_project,
    write_secure_file,
)
from ..simulation.corporation_simulator import CorporationSimulator


class SimulationStateManager:
    """
    Manages simulation state checkpoints.

    Allows saving simulation state at any point and resuming from that point.
    """

    def __init__(self, corporation: Corporation, project_path: Path | None = None):
        """
        Initialize state manager.

        Args:
            corporation: Corporation to manage state for
            project_path: Project root path
        """
        self.corporation = corporation
        self.project_path = Path(project_path) if project_path else Path.cwd()

        self.checkpoints_dir = (
            self.project_path
            / "_realms"
            / "bureaucracy_realm"
            / "corporations"
            / corporation.corp_id
            / "simulation"
            / "checkpoints"
        )

        # CRITICAL: Validate path is within project
        if not validate_path_in_project(self.checkpoints_dir, self.project_path):
            raise ValueError(
                f"Invalid checkpoints path: {self.checkpoints_dir} is outside project directory"
            )

        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)
        # CRITICAL: Set secure directory permissions
        set_directory_permissions(self.checkpoints_dir)

    def save_checkpoint(
        self, simulator: CorporationSimulator, checkpoint_name: str | None = None
    ) -> Path:
        """
        Save simulation checkpoint.

        Args:
            simulator: Simulator to save state from
            checkpoint_name: Optional checkpoint name (auto-generated if not provided)

        Returns:
            Path to saved checkpoint file
        """
        if checkpoint_name is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            checkpoint_name = f"checkpoint_{timestamp}"

        checkpoint_path = self.checkpoints_dir / f"{checkpoint_name}.json"

        # CRITICAL: Validate checkpoint name (prevent path traversal in filename)
        if ".." in checkpoint_name or "/" in checkpoint_name or "\\" in checkpoint_name:
            raise ValueError(
                f"Invalid checkpoint name: {checkpoint_name} (contains path traversal)"
            )

        # Collect state
        state = {
            "checkpoint_name": checkpoint_name,
            "created_at": datetime.utcnow().isoformat(),
            "corporation": self.corporation.to_dict(),
            "time_manager": simulator.time_manager.to_dict(),
            "accounting": simulator.accounting.to_dict(),
            "event_queue": [e.to_dict() for e in simulator.event_queue],
            "monthly_expenses": simulator.monthly_expenses,
        }

        # CRITICAL: Use secure file write
        try:
            write_secure_file(checkpoint_path, json.dumps(state, indent=2), encoding="utf-8")
        except OSError as e:
            raise OSError(f"Failed to save checkpoint to {checkpoint_path}: {e}")

        return checkpoint_path

    def load_checkpoint(self, checkpoint_path: Path, simulator: CorporationSimulator) -> None:
        """
        Load simulation checkpoint.

        Args:
            checkpoint_path: Path to checkpoint file
            simulator: Simulator to restore state to

        Raises:
            ValueError: If checkpoint is invalid
            IOError: If checkpoint cannot be read
        """
        # CRITICAL: Validate path is within project
        if not validate_path_in_project(checkpoint_path, self.project_path):
            raise ValueError(
                f"Invalid checkpoint path: {checkpoint_path} is outside project directory"
            )

        try:
            # CRITICAL: Use secure JSON read with size limits
            state = read_secure_json(checkpoint_path)
        except (OSError, ValueError, json.JSONDecodeError) as e:
            raise ValueError(f"Failed to load checkpoint from {checkpoint_path}: {e}")

        # Restore time manager
        if "time_manager" in state:
            from ..simulation.time_manager import TimeManager

            simulator.time_manager = TimeManager.from_dict(state["time_manager"])

        # Restore event queue
        if "event_queue" in state:
            from ..simulation.event_system import EconomicEvent

            simulator.event_queue = [EconomicEvent.from_dict(e) for e in state["event_queue"]]

        # Restore monthly expenses
        if "monthly_expenses" in state:
            simulator.monthly_expenses = state["monthly_expenses"]

        # Restore corporation state
        if "corporation" in state:
            # Update financial state
            if "financial_state" in state["corporation"]:
                from ..financial_state import FinancialState

                self.corporation.financial_state = FinancialState.from_dict(
                    state["corporation"]["financial_state"]
                )

            # Save corporation manifest
            self.corporation._save_manifest()

    def list_checkpoints(self) -> list[Path]:
        """List all available checkpoints."""
        return sorted(
            self.checkpoints_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True
        )
