"""
Mission Control: Pantheon Entity of Coordination, Monitoring, and Command

Mission Control serves as the central command center for coordinating missions,
monitoring operations, and providing real-time oversight. Inspired by Avatar's
human base operations and Fern Gully's fairy coordination systems.

Following "as above, so below" principles:
- As above: Central command hub coordinating all mission operations
- So below: File-based system managing mission monitoring, status tracking, and coordination
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


class MissionStatus:
    """Real-time mission status tracking."""
    
    def __init__(
        self,
        mission_id: str,
        status: str = "monitoring",
        progress: float = 0.0,
        last_update: Optional[str] = None,
        alerts: Optional[List[str]] = None,
        telemetry: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize mission status.
        
        Args:
            mission_id: Mission identifier
            status: Current status (monitoring, active, critical, completed, aborted)
            progress: Progress percentage (0.0-1.0)
            last_update: ISO timestamp of last update
            alerts: List of active alerts
            telemetry: Real-time telemetry data
        """
        self.mission_id = mission_id
        self.status = status
        self.progress = progress
        self.last_update = last_update or datetime.now().isoformat()
        self.alerts = alerts or []
        self.telemetry = telemetry or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "mission_id": self.mission_id,
            "status": self.status,
            "progress": self.progress,
            "last_update": self.last_update,
            "alerts": self.alerts,
            "telemetry": self.telemetry
        }


class MissionControl:
    """
    Mission Control: Central command center for mission coordination.
    
    Provides:
    - Real-time mission monitoring
    - Status tracking and alerts
    - Command interface for mission operations
    - Coordination with Military Brass
    - Telemetry and operational data
    """
    
    def __init__(self, project_path: Path):
        """
        Initialize Mission Control.
        
        Args:
            project_path: Project root path
        """
        self.project_path = project_path
        self.control_path = project_path / "_pantheon" / "mission_control"
        self.control_path.mkdir(parents=True, exist_ok=True)
        
        # Mission Control directories
        self.status_path = self.control_path / "status"
        self.status_path.mkdir(exist_ok=True)
        self.commands_path = self.control_path / "commands"
        self.commands_path.mkdir(exist_ok=True)
        self.telemetry_path = self.control_path / "telemetry"
        self.telemetry_path.mkdir(exist_ok=True)
        
        # Registry
        self.registry_file = self.control_path / "control_registry.json"
        self._ensure_registry()
    
    def _ensure_registry(self) -> None:
        """Ensure registry file exists."""
        if not self.registry_file.exists():
            registry = {
                "missions_monitored": [],
                "active_commands": [],
                "alerts": [],
                "last_update": datetime.now().isoformat()
            }
            self.registry_file.write_text(
                json.dumps(registry, indent=2),
                encoding="utf-8"
            )
    
    def register_mission(self, mission_id: str) -> Dict[str, Any]:
        """
        Register a mission for monitoring.
        
        Args:
            mission_id: Mission identifier
            
        Returns:
            Registration confirmation
        """
        registry = json.loads(self.registry_file.read_text(encoding="utf-8"))
        
        if mission_id not in registry["missions_monitored"]:
            registry["missions_monitored"].append(mission_id)
            registry["last_update"] = datetime.now().isoformat()
            self.registry_file.write_text(
                json.dumps(registry, indent=2),
                encoding="utf-8"
            )
        
        # Create initial status
        status = MissionStatus(mission_id=mission_id)
        status_file = self.status_path / f"{mission_id}_status.json"
        status_file.write_text(
            json.dumps(status.to_dict(), indent=2),
            encoding="utf-8"
        )
        
        return {
            "mission_id": mission_id,
            "status": "registered",
            "message": "Mission Control is now monitoring this mission"
        }
    
    def update_status(
        self,
        mission_id: str,
        status: Optional[str] = None,
        progress: Optional[float] = None,
        alerts: Optional[List[str]] = None,
        telemetry: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Update mission status.
        
        Args:
            mission_id: Mission identifier
            status: New status
            progress: Progress percentage
            alerts: New alerts
            telemetry: Telemetry data
            
        Returns:
            Updated status
        """
        status_file = self.status_path / f"{mission_id}_status.json"
        
        if status_file.exists():
            current = json.loads(status_file.read_text(encoding="utf-8"))
        else:
            current = MissionStatus(mission_id=mission_id).to_dict()
        
        # Update fields
        if status:
            current["status"] = status
        if progress is not None:
            current["progress"] = progress
        if alerts:
            current["alerts"].extend(alerts)
        if telemetry:
            current["telemetry"].update(telemetry)
        
        current["last_update"] = datetime.now().isoformat()
        
        status_file.write_text(
            json.dumps(current, indent=2),
            encoding="utf-8"
        )
        
        return current
    
    def get_status(self, mission_id: str) -> Optional[Dict[str, Any]]:
        """
        Get current mission status.
        
        Args:
            mission_id: Mission identifier
            
        Returns:
            Status dictionary or None
        """
        status_file = self.status_path / f"{mission_id}_status.json"
        
        if status_file.exists():
            return json.loads(status_file.read_text(encoding="utf-8"))
        return None
    
    def get_all_status(self) -> List[Dict[str, Any]]:
        """
        Get status of all monitored missions.
        
        Returns:
            List of status dictionaries
        """
        statuses = []
        for status_file in self.status_path.glob("*_status.json"):
            statuses.append(
                json.loads(status_file.read_text(encoding="utf-8"))
            )
        return statuses
    
    def issue_command(
        self,
        mission_id: str,
        command: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Issue a command to a mission.
        
        Args:
            mission_id: Mission identifier
            command: Command name (e.g., "halt", "resume", "prioritize")
            parameters: Command parameters
            
        Returns:
            Command confirmation
        """
        command_id = f"cmd_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        command_data = {
            "command_id": command_id,
            "mission_id": mission_id,
            "command": command,
            "parameters": parameters or {},
            "issued_at": datetime.now().isoformat(),
            "status": "pending"
        }
        
        command_file = self.commands_path / f"{command_id}.json"
        command_file.write_text(
            json.dumps(command_data, indent=2),
            encoding="utf-8"
        )
        
        # Update registry
        registry = json.loads(self.registry_file.read_text(encoding="utf-8"))
        registry["active_commands"].append(command_id)
        registry["last_update"] = datetime.now().isoformat()
        self.registry_file.write_text(
            json.dumps(registry, indent=2),
            encoding="utf-8"
        )
        
        return command_data
    
    def get_control_summary(self) -> Dict[str, Any]:
        """
        Get Mission Control summary.
        
        Returns:
            Summary of all operations
        """
        registry = json.loads(self.registry_file.read_text(encoding="utf-8"))
        all_status = self.get_all_status()
        
        return {
            "missions_monitored": len(registry["missions_monitored"]),
            "active_commands": len(registry["active_commands"]),
            "active_alerts": len(registry["alerts"]),
            "mission_statuses": {
                status["status"]: sum(1 for s in all_status if s["status"] == status["status"])
                for status in all_status
            },
            "last_update": registry["last_update"]
        }
