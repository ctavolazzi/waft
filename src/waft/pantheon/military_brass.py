"""
Military Brass: Pantheon God of Structure, Accountability, and Documentation

The Military Brass oversees serious, structured work - Missions that require
precision, accountability, and comprehensive documentation.

Following "as above, so below" principles:
- As above: Pantheon god organizing military command structure
- So below: File-based system managing mission documentation and tracking
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


class Mission:
    """A Mission - serious, structured work with full documentation."""
    
    def __init__(
        self,
        mission_id: str,
        name: str,
        objective: str,
        classification: str = "INTERNAL",
        briefing: Optional[str] = None,
        success_criteria: Optional[List[str]] = None,
        difficulty: int = 5,
        created_at: Optional[str] = None
    ):
        """
        Initialize a mission.
        
        Args:
            mission_id: Unique identifier for the mission
            name: Mission name
            objective: Clear mission objective
            classification: Security classification (INTERNAL, CONFIDENTIAL, etc.)
            briefing: Mission briefing content
            success_criteria: List of measurable success criteria
            difficulty: Mission difficulty (1-10)
            created_at: ISO timestamp when mission was created
        """
        self.mission_id = mission_id
        self.name = name
        self.objective = objective
        self.classification = classification
        self.briefing = briefing or ""
        self.success_criteria = success_criteria or []
        self.difficulty = difficulty
        self.created_at = created_at or datetime.now().isoformat()
        self.status = "active"
        self.progress = "0%"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert mission to dictionary."""
        return {
            "id": self.mission_id,
            "name": self.name,
            "type": "mission",
            "status": self.status,
            "classification": self.classification,
            "objective": self.objective,
            "briefing": self.briefing,
            "success_criteria": self.success_criteria,
            "difficulty": self.difficulty,
            "progress": self.progress,
            "created_at": self.created_at
        }


class MilitaryBrass:
    """
    Military Brass: God of Structure, Accountability, and Documentation
    
    Oversees serious, structured work - Missions that require precision,
    accountability, and comprehensive documentation.
    
    Storage:
    - Missions: _pantheon/military_brass/missions/
    - Briefings: _pantheon/military_brass/briefings/
    - Debriefings: _pantheon/military_brass/debriefings/
    - Mission PDFs: _pantheon/military_brass/missions/*.pdf
    """
    
    def __init__(self, project_path: Optional[Path] = None):
        """
        Initialize the Military Brass.
        
        Args:
            project_path: Path to project root (default: current directory)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.pantheon_path = project_path / "_pantheon"
        self.brass_path = self.pantheon_path / "military_brass"
        
        # Ensure directory structure exists
        self.brass_path.mkdir(parents=True, exist_ok=True)
        (self.brass_path / "missions").mkdir(parents=True, exist_ok=True)
        (self.brass_path / "briefings").mkdir(parents=True, exist_ok=True)
        (self.brass_path / "debriefings").mkdir(parents=True, exist_ok=True)
        
        # Mission registry
        self.missions_file = self.brass_path / "missions_registry.json"
        self.missions = self._load_missions()
    
    def _load_missions(self) -> List[Dict[str, Any]]:
        """Load missions from registry."""
        if not self.missions_file.exists():
            return []
        
        try:
            with open(self.missions_file, 'r') as f:
                data = json.load(f)
                return data.get("missions", [])
        except (json.JSONDecodeError, IOError):
            return []
    
    def _save_missions(self) -> None:
        """Save missions to registry."""
        data = {
            "missions": self.missions,
            "updated_at": datetime.now().isoformat()
        }
        with open(self.missions_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_mission(
        self,
        name: str,
        objective: str,
        classification: str = "INTERNAL",
        briefing: Optional[str] = None,
        success_criteria: Optional[List[str]] = None,
        difficulty: Optional[int] = None
    ) -> Mission:
        """
        Create a new mission.
        
        Args:
            name: Mission name
            objective: Clear mission objective
            classification: Security classification
            briefing: Mission briefing content
            success_criteria: List of measurable success criteria
            difficulty: Mission difficulty (1-10), auto-calculated if None
            
        Returns:
            Created Mission object
        """
        mission_id = f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name.lower().replace(' ', '_')[:20]}"
        
        # Auto-calculate difficulty if not provided
        if difficulty is None:
            # Base difficulty on objective complexity
            word_count = len(objective.split())
            criteria_count = len(success_criteria or [])
            difficulty = min(10, max(1, (word_count // 10) + (criteria_count // 2) + 3))
        
        mission = Mission(
            mission_id=mission_id,
            name=name,
            objective=objective,
            classification=classification,
            briefing=briefing,
            success_criteria=success_criteria,
            difficulty=difficulty
        )
        
        # Register mission
        self.missions.append(mission.to_dict())
        self._save_missions()
        
        # Auto-register with Mission Control
        try:
            from .mission_control import MissionControl
            mission_control = MissionControl(self.project_path)
            mission_control.register_mission(mission.mission_id)
        except Exception:
            # Mission Control integration is optional
            pass
        
        return mission
    
    def get_mission(self, mission_id: str) -> Optional[Mission]:
        """Get mission by ID."""
        for mission_data in self.missions:
            if mission_data.get("id") == mission_id:
                return Mission(
                    mission_id=mission_data["id"],
                    name=mission_data["name"],
                    objective=mission_data["objective"],
                    classification=mission_data.get("classification", "INTERNAL"),
                    briefing=mission_data.get("briefing"),
                    success_criteria=mission_data.get("success_criteria", []),
                    difficulty=mission_data.get("difficulty", 5),
                    created_at=mission_data.get("created_at")
                )
        return None
    
    def list_missions(
        self,
        status: Optional[str] = None,
        classification: Optional[str] = None
    ) -> List[Mission]:
        """
        List missions with optional filters.
        
        Args:
            status: Filter by status (active, complete, etc.)
            classification: Filter by classification
            
        Returns:
            List of Mission objects
        """
        missions = []
        for mission_data in self.missions:
            if status and mission_data.get("status") != status:
                continue
            if classification and mission_data.get("classification") != classification:
                continue
            
            mission = Mission(
                mission_id=mission_data["id"],
                name=mission_data["name"],
                objective=mission_data["objective"],
                classification=mission_data.get("classification", "INTERNAL"),
                briefing=mission_data.get("briefing"),
                success_criteria=mission_data.get("success_criteria", []),
                difficulty=mission_data.get("difficulty", 5),
                created_at=mission_data.get("created_at")
            )
            mission.status = mission_data.get("status", "active")
            mission.progress = mission_data.get("progress", "0%")
            missions.append(mission)
        
        return missions
    
    def update_mission_status(
        self,
        mission_id: str,
        status: str,
        progress: Optional[str] = None
    ) -> bool:
        """
        Update mission status.
        
        Args:
            mission_id: Mission ID
            status: New status
            progress: Optional progress update
            
        Returns:
            True if updated, False if mission not found
        """
        for mission_data in self.missions:
            if mission_data.get("id") == mission_id:
                mission_data["status"] = status
                if progress:
                    mission_data["progress"] = progress
                self._save_missions()
                return True
        return False
    
    def generate_mission_briefing(self, mission: Mission) -> str:
        """
        Generate mission briefing document.
        
        Args:
            mission: Mission object
            
        Returns:
            Briefing document content
        """
        briefing = f"""# Mission Briefing: {mission.name}

**Mission ID**: {mission.mission_id}  
**Classification**: {mission.classification}  
**Date**: {mission.created_at}  
**Status**: {mission.status}

## Objective

{mission.objective}

## Success Criteria

"""
        for i, criterion in enumerate(mission.success_criteria, 1):
            briefing += f"{i}. {criterion}\n"
        
        briefing += f"""
## Mission Details

**Difficulty**: {mission.difficulty}/10  
**Progress**: {mission.progress}

## Briefing

{mission.briefing or "Mission briefing prepared. Objective defined and approved."}

## Status

Mission status: {mission.status}

---
*Mission briefing prepared by Military Brass*
"""
        return briefing
    
    def save_briefing(self, mission: Mission) -> Path:
        """
        Save mission briefing to file.
        
        Args:
            mission: Mission object
            
        Returns:
            Path to briefing file
        """
        briefing_content = self.generate_mission_briefing(mission)
        briefing_path = self.brass_path / "briefings" / f"{mission.mission_id}_briefing.md"
        briefing_path.write_text(briefing_content, encoding="utf-8")
        return briefing_path
