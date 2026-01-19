"""
Simulation State Manager: Save/load simulation checkpoints

Manages saving and loading simulation state at any point for resuming experiments.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import json

from ..simulation.corporation_simulator import CorporationSimulator
from ..corporation import Corporation


class SimulationStateManager:
    """
    Manages simulation state checkpoints.
    
    Allows saving simulation state at any point and resuming from that point.
    """
    
    def __init__(self, corporation: Corporation, project_path: Optional[Path] = None):
        """
        Initialize state manager.
        
        Args:
            corporation: Corporation to manage state for
            project_path: Project root path
        """
        self.corporation = corporation
        self.project_path = Path(project_path) if project_path else Path.cwd()
        
        self.checkpoints_dir = (
            self.project_path / "_realms" / "bureaucracy_realm" / "corporations"
            / corporation.corp_id / "simulation" / "checkpoints"
        )
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)
    
    def save_checkpoint(
        self,
        simulator: CorporationSimulator,
        checkpoint_name: Optional[str] = None
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
        
        # Collect state
        state = {
            "checkpoint_name": checkpoint_name,
            "created_at": datetime.utcnow().isoformat(),
            "corporation": self.corporation.to_dict(),
            "time_manager": simulator.time_manager.to_dict(),
            "accounting": simulator.accounting.to_dict(),
            "event_queue": [e.to_dict() for e in simulator.event_queue],
            "monthly_expenses": simulator.monthly_expenses
        }
        
        # Save to file
        checkpoint_path.write_text(
            json.dumps(state, indent=2),
            encoding="utf-8"
        )
        
        return checkpoint_path
    
    def load_checkpoint(
        self,
        checkpoint_path: Path,
        simulator: CorporationSimulator
    ) -> None:
        """
        Load simulation checkpoint.
        
        Args:
            checkpoint_path: Path to checkpoint file
            simulator: Simulator to restore state to
        """
        state = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        
        # Restore time manager
        if "time_manager" in state:
            from ..simulation.time_manager import TimeManager
            simulator.time_manager = TimeManager.from_dict(state["time_manager"])
        
        # Restore event queue
        if "event_queue" in state:
            from ..simulation.event_system import EconomicEvent
            simulator.event_queue = [
                EconomicEvent.from_dict(e) for e in state["event_queue"]
            ]
        
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
        return sorted(self.checkpoints_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
