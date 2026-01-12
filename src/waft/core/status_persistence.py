"""
Status Persistence - Save and Track Status Snapshots (inspired by AI-DnD save system)

Provides:
- Status snapshot saving with checksums (data integrity)
- Status history tracking
- Status comparison utilities
- Integrity verification

Pattern: Inspired by AI-DnD's save_system.py with checksum verification.
"""

import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import asdict


class StatusPersistence:
    """
    Persist and verify status snapshots with checksum integrity checking.
    
    Stores snapshots in: _pyrite/.waft/status_snapshots/
    """
    
    def __init__(self, project_path: Path):
        """
        Initialize status persistence.
        
        Args:
            project_path: Project root path
        """
        self.project_path = project_path
        self.snapshots_dir = project_path / "_pyrite" / ".waft" / "status_snapshots"
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)
    
    def save_status_snapshot(
        self,
        status: Dict[str, Any],
        snapshot_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Save status snapshot with checksum.
        
        Args:
            status: Status dictionary (from check_status() or StatusState.to_dict())
            snapshot_id: Optional snapshot ID (default: timestamp-based)
            metadata: Optional additional metadata
        
        Returns:
            Snapshot dictionary with checksum
        """
        if snapshot_id is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            snapshot_id = f"status_{timestamp}"
        
        snapshot = {
            "version": "1.0",
            "snapshot_id": snapshot_id,
            "timestamp": datetime.utcnow().isoformat(),
            "status": status,
            "metadata": metadata or {
                "source": "waft-status",
                "project_path": str(self.project_path),
            }
        }
        
        # Calculate checksum (before adding checksum field)
        json_str = json.dumps(snapshot, sort_keys=True, default=str)
        checksum = hashlib.md5(json_str.encode()).hexdigest()
        snapshot["checksum"] = checksum
        
        # Save to file
        snapshot_file = self.snapshots_dir / f"{snapshot_id}.json"
        snapshot_file.write_text(json.dumps(snapshot, indent=2, default=str))
        
        return snapshot
    
    def load_status_snapshot(
        self,
        snapshot_id: str,
        verify_integrity: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Load and verify status snapshot.
        
        Args:
            snapshot_id: Snapshot ID (filename without .json)
            verify_integrity: Whether to verify checksum
        
        Returns:
            Status dictionary if valid, None if invalid or not found
        """
        snapshot_file = self.snapshots_dir / f"{snapshot_id}.json"
        
        if not snapshot_file.exists():
            return None
        
        try:
            data = json.loads(snapshot_file.read_text())
            
            if verify_integrity:
                stored_checksum = data.pop("checksum", None)
                
                # Recalculate checksum
                json_str = json.dumps(data, sort_keys=True, default=str)
                calculated_checksum = hashlib.md5(json_str.encode()).hexdigest()
                
                if stored_checksum != calculated_checksum:
                    return None  # Integrity check failed
            
            return data.get("status")
        except (json.JSONDecodeError, KeyError, IOError):
            return None
    
    def list_snapshots(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        List all available snapshots.
        
        Args:
            limit: Optional limit on number of snapshots to return
        
        Returns:
            List of snapshot metadata dictionaries
        """
        snapshots = []
        
        for snapshot_file in sorted(self.snapshots_dir.glob("*.json"), reverse=True):
            try:
                data = json.loads(snapshot_file.read_text())
                snapshots.append({
                    "snapshot_id": data.get("snapshot_id", snapshot_file.stem),
                    "timestamp": data.get("timestamp"),
                    "version": data.get("version"),
                    "metadata": data.get("metadata", {}),
                    "checksum": data.get("checksum"),
                    "file_path": str(snapshot_file),
                })
            except (json.JSONDecodeError, KeyError):
                continue
        
        if limit:
            snapshots = snapshots[:limit]
        
        return snapshots
    
    def get_latest_snapshot(self) -> Optional[Dict[str, Any]]:
        """
        Get the most recent status snapshot.
        
        Returns:
            Status dictionary if available, None otherwise
        """
        snapshots = self.list_snapshots(limit=1)
        if not snapshots:
            return None
        
        return self.load_status_snapshot(snapshots[0]["snapshot_id"])
    
    def compare_snapshots(
        self,
        snapshot_id_1: str,
        snapshot_id_2: str
    ) -> Optional[Dict[str, Any]]:
        """
        Compare two status snapshots.
        
        Args:
            snapshot_id_1: First snapshot ID
            snapshot_id_2: Second snapshot ID
        
        Returns:
            Comparison dictionary with differences, or None if either snapshot invalid
        """
        status1 = self.load_status_snapshot(snapshot_id_1)
        status2 = self.load_status_snapshot(snapshot_id_2)
        
        if status1 is None or status2 is None:
            return None
        
        comparison = {
            "snapshot_1": snapshot_id_1,
            "snapshot_2": snapshot_id_2,
            "differences": {},
            "unchanged": [],
        }
        
        # Compare key metrics
        def compare_dicts(dict1: Dict, dict2: Dict, path: str = "") -> None:
            """Recursively compare dictionaries."""
            all_keys = set(dict1.keys()) | set(dict2.keys())
            
            for key in all_keys:
                current_path = f"{path}.{key}" if path else key
                
                val1 = dict1.get(key)
                val2 = dict2.get(key)
                
                if val1 != val2:
                    if isinstance(val1, dict) and isinstance(val2, dict):
                        compare_dicts(val1, val2, current_path)
                    else:
                        comparison["differences"][current_path] = {
                            "old": val1,
                            "new": val2,
                        }
                else:
                    comparison["unchanged"].append(current_path)
        
        compare_dicts(status1, status2)
        
        return comparison
    
    def get_status_history(
        self,
        metric_path: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get history of a specific metric across snapshots.
        
        Args:
            metric_path: Dot-separated path to metric (e.g., "epistemic_state.knowledge_pct")
            limit: Optional limit on number of snapshots
        
        Returns:
            List of {timestamp, value} dictionaries
        """
        snapshots = self.list_snapshots(limit=limit)
        history = []
        
        for snapshot_meta in snapshots:
            status = self.load_status_snapshot(snapshot_meta["snapshot_id"])
            if status is None:
                continue
            
            # Navigate to metric
            value = status
            for key in metric_path.split("."):
                if isinstance(value, dict):
                    value = value.get(key)
                else:
                    value = None
                    break
            
            if value is not None:
                history.append({
                    "timestamp": snapshot_meta["timestamp"],
                    "value": value,
                    "snapshot_id": snapshot_meta["snapshot_id"],
                })
        
        return history
    
    def delete_snapshot(self, snapshot_id: str) -> bool:
        """
        Delete a status snapshot.
        
        Args:
            snapshot_id: Snapshot ID to delete
        
        Returns:
            True if deleted, False if not found
        """
        snapshot_file = self.snapshots_dir / f"{snapshot_id}.json"
        if snapshot_file.exists():
            snapshot_file.unlink()
            return True
        return False
    
    def cleanup_old_snapshots(self, keep_count: int = 100) -> int:
        """
        Clean up old snapshots, keeping only the most recent N.
        
        Args:
            keep_count: Number of snapshots to keep
        
        Returns:
            Number of snapshots deleted
        """
        snapshots = self.list_snapshots()
        
        if len(snapshots) <= keep_count:
            return 0
        
        # Delete oldest snapshots
        to_delete = snapshots[keep_count:]
        deleted_count = 0
        
        for snapshot in to_delete:
            if self.delete_snapshot(snapshot["snapshot_id"]):
                deleted_count += 1
        
        return deleted_count


def save_status_snapshot(
    status: Dict[str, Any],
    project_path: Optional[Path] = None,
    snapshot_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convenience function to save a status snapshot.
    
    Args:
        status: Status dictionary
        project_path: Project root path (default: current directory)
        snapshot_id: Optional snapshot ID
    
    Returns:
        Snapshot dictionary with checksum
    """
    if project_path is None:
        project_path = Path.cwd()
    
    persistence = StatusPersistence(project_path)
    return persistence.save_status_snapshot(status, snapshot_id=snapshot_id)


def load_status_snapshot(
    snapshot_id: str,
    project_path: Optional[Path] = None,
    verify_integrity: bool = True
) -> Optional[Dict[str, Any]]:
    """
    Convenience function to load a status snapshot.
    
    Args:
        snapshot_id: Snapshot ID
        project_path: Project root path (default: current directory)
        verify_integrity: Whether to verify checksum
    
    Returns:
        Status dictionary if valid, None otherwise
    """
    if project_path is None:
        project_path = Path.cwd()
    
    persistence = StatusPersistence(project_path)
    return persistence.load_status_snapshot(snapshot_id, verify_integrity=verify_integrity)
