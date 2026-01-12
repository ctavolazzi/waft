"""
Experiment Management Tool

Utilities for managing experiments in the _science directory.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class ExperimentManagerTool:
    """Tool for managing experiments."""
    
    def __init__(self, science_path: Path):
        """
        Initialize experiment manager tool.
        
        Args:
            science_path: Path to _science directory
        """
        self.science_path = science_path
        self.experiments_path = science_path / "experiments"
        self.data_path = science_path / "data"
        self.reports_path = science_path / "reports"
    
    def list_experiments(self) -> List[Dict[str, Any]]:
        """List all experiments."""
        experiments = []
        
        if not self.experiments_path.exists():
            return experiments
        
        for exp_file in self.experiments_path.glob("exp_*.json"):
            try:
                data = json.loads(exp_file.read_text())
                experiments.append({
                    "id": data.get("experiment_id", exp_file.stem),
                    "created": data.get("created_at", "unknown"),
                    "state": data.get("state", "unknown"),
                    "hypothesis": data.get("hypothesis", {}).get("statement", "N/A"),
                })
            except Exception:
                continue
        
        return sorted(experiments, key=lambda x: x.get("created", ""), reverse=True)
    
    def get_experiment_status(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific experiment."""
        exp_file = self.experiments_path / f"exp_{experiment_id}.json"
        
        if not exp_file.exists():
            return None
        
        try:
            data = json.loads(exp_file.read_text())
            return {
                "id": data.get("experiment_id"),
                "state": data.get("state"),
                "created": data.get("created_at"),
                "started": data.get("started_at"),
                "completed": data.get("completed_at"),
                "hypothesis": data.get("hypothesis", {}).get("statement"),
                "results": data.get("results", {}),
            }
        except Exception:
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get experiment statistics."""
        experiments = self.list_experiments()
        
        by_state = {}
        for exp in experiments:
            state = exp.get("state", "unknown")
            by_state[state] = by_state.get(state, 0) + 1
        
        return {
            "total": len(experiments),
            "by_state": by_state,
            "latest": experiments[0] if experiments else None,
        }
