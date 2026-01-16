"""
HourglassTorus: Eternal Evolution Tracking Structure

A toroidal (doughnut-shaped) data structure that cycles through generations
and cycles, recording evolution forevermore. The structure has:
- Top Half (Past): Completed generations/cycles
- Narrow Center (Present): Current generation/cycle being recorded
- Bottom Half (Future): Space for next generation/cycle

The structure rotates continuously, recording evolution from this point
forward in Spacetime, generation after generation, cycle after cycle.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


class HourglassTorus:
    """
    Hourglass/Torus evolution tracking structure.
    
    Manages generation/cycle rotation, records evolution events,
    archives old cycles, and provides query interface for evolution history.
    """
    
    def __init__(
        self,
        project_path: Optional[Path] = None,
        torus_path: Optional[Path] = None,
        max_past_cycles: int = 1000,
        max_future_cycles: int = 100
    ):
        """
        Initialize HourglassTorus.
        
        Args:
            project_path: Path to project root
            torus_path: Path to torus storage
            max_past_cycles: Maximum cycles to keep in past (top half)
            max_future_cycles: Maximum cycles to reserve in future (bottom half)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        
        if torus_path is None:
            torus_path = project_path / "_hidden" / ".truth" / "celestial_body" / "hourglass_torus"
        else:
            torus_path = Path(torus_path)
        
        self.torus_path = torus_path
        self.torus_path.mkdir(parents=True, exist_ok=True)
        
        self.generations_path = self.torus_path / "generations"
        self.cycles_path = self.torus_path / "cycles"
        self.current_cycle_file = self.torus_path / "current_cycle.json"
        self.torus_index_file = self.torus_path / "torus_index.json"
        
        self.generations_path.mkdir(exist_ok=True)
        self.cycles_path.mkdir(exist_ok=True)
        
        self.max_past_cycles = max_past_cycles
        self.max_future_cycles = max_future_cycles
        
        # Torus state
        self.current_generation: int = 0
        self.current_cycle: int = 0
        self.current_cycle_data: Dict[str, Any] = {}
        
        # Load existing state
        self._load()
    
    def _load(self):
        """Load torus state from disk."""
        if self.torus_index_file.exists():
            with open(self.torus_index_file, 'r') as f:
                index = json.load(f)
                self.current_generation = index.get("current_generation", 0)
                self.current_cycle = index.get("current_cycle", 0)
        
        if self.current_cycle_file.exists():
            with open(self.current_cycle_file, 'r') as f:
                self.current_cycle_data = json.load(f)
        else:
            # Initialize first cycle
            self._initialize_first_cycle()
    
    def _save(self):
        """Save torus state to disk."""
        # Save index
        index = {
            "current_generation": self.current_generation,
            "current_cycle": self.current_cycle,
            "max_past_cycles": self.max_past_cycles,
            "max_future_cycles": self.max_future_cycles,
            "updated_at": datetime.now().isoformat(),
        }
        
        with open(self.torus_index_file, 'w') as f:
            json.dump(index, f, indent=2)
        
        # Save current cycle
        if self.current_cycle_data:
            with open(self.current_cycle_file, 'w') as f:
                json.dump(self.current_cycle_data, f, indent=2)
    
    def _initialize_first_cycle(self):
        """Initialize the first cycle."""
        self.current_generation = 0
        self.current_cycle = 0
        self.current_cycle_data = {
            "generation": self.current_generation,
            "cycle": self.current_cycle,
            "started_at": datetime.now().isoformat(),
            "events": [],
            "state": "active",
        }
        self._save()
    
    def record_event(self, event: Dict[str, Any]):
        """
        Record an evolution event in the current cycle.
        
        Args:
            event: Event data
        """
        event["timestamp"] = datetime.now().isoformat()
        event["generation"] = self.current_generation
        event["cycle"] = self.current_cycle
        
        if "events" not in self.current_cycle_data:
            self.current_cycle_data["events"] = []
        
        self.current_cycle_data["events"].append(event)
        self._save()
    
    def complete_cycle(self) -> Dict[str, Any]:
        """
        Complete the current cycle and move it to the top (past).
        
        Returns:
            Completed cycle data
        """
        # Mark cycle as completed
        self.current_cycle_data["completed_at"] = datetime.now().isoformat()
        self.current_cycle_data["state"] = "completed"
        
        # Save completed cycle to cycles directory
        cycle_file = self.cycles_path / f"generation_{self.current_generation}_cycle_{self.current_cycle}.json"
        with open(cycle_file, 'w') as f:
            json.dump(self.current_cycle_data, f, indent=2)
        
        # Move to next cycle
        self.current_cycle += 1
        
        # Check if we need to start a new generation
        # (For now, cycles continue indefinitely, but we can add generation logic)
        
        # Initialize next cycle
        self.current_cycle_data = {
            "generation": self.current_generation,
            "cycle": self.current_cycle,
            "started_at": datetime.now().isoformat(),
            "events": [],
            "state": "active",
        }
        
        self._save()
        
        # Archive old cycles if needed
        self._archive_old_cycles()
        
        return self.current_cycle_data
    
    def start_new_generation(self) -> int:
        """
        Start a new generation.
        
        Returns:
            New generation number
        """
        # Complete current cycle first
        if self.current_cycle_data.get("state") == "active":
            self.complete_cycle()
        
        # Move to next generation
        self.current_generation += 1
        self.current_cycle = 0
        
        # Save generation metadata
        generation_file = self.generations_path / f"generation_{self.current_generation}.json"
        generation_data = {
            "generation": self.current_generation,
            "started_at": datetime.now().isoformat(),
            "cycles": [],
        }
        
        with open(generation_file, 'w') as f:
            json.dump(generation_data, f, indent=2)
        
        # Initialize first cycle of new generation
        self.current_cycle_data = {
            "generation": self.current_generation,
            "cycle": self.current_cycle,
            "started_at": datetime.now().isoformat(),
            "events": [],
            "state": "active",
        }
        
        self._save()
        
        return self.current_generation
    
    def _archive_old_cycles(self):
        """Archive old cycles when past limit is reached."""
        # Get all cycle files
        cycle_files = sorted(self.cycles_path.glob("*.json"))
        
        if len(cycle_files) > self.max_past_cycles:
            # Create archive directory
            archive_path = self.torus_path / "archive"
            archive_path.mkdir(exist_ok=True)
            
            # Move oldest cycles to archive
            cycles_to_archive = cycle_files[:len(cycle_files) - self.max_past_cycles]
            for cycle_file in cycles_to_archive:
                archive_file = archive_path / cycle_file.name
                cycle_file.rename(archive_file)
    
    def get_current_cycle(self) -> Dict[str, Any]:
        """Get current cycle data."""
        return self.current_cycle_data.copy()
    
    def get_cycle(self, generation: int, cycle: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific cycle.
        
        Args:
            generation: Generation number
            cycle: Cycle number
            
        Returns:
            Cycle data or None if not found
        """
        cycle_file = self.cycles_path / f"generation_{generation}_cycle_{cycle}.json"
        
        if cycle_file.exists():
            with open(cycle_file, 'r') as f:
                return json.load(f)
        
        # Check archive
        archive_file = self.torus_path / "archive" / f"generation_{generation}_cycle_{cycle}.json"
        if archive_file.exists():
            with open(archive_file, 'r') as f:
                return json.load(f)
        
        return None
    
    def get_generation(self, generation: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific generation.
        
        Args:
            generation: Generation number
            
        Returns:
            Generation data or None if not found
        """
        generation_file = self.generations_path / f"generation_{generation}.json"
        
        if generation_file.exists():
            with open(generation_file, 'r') as f:
                return json.load(f)
        
        return None
    
    def query_history(
        self,
        generation: Optional[int] = None,
        cycle: Optional[int] = None,
        event_type: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Query evolution history.
        
        Args:
            generation: Optional filter by generation
            cycle: Optional filter by cycle
            event_type: Optional filter by event type
            limit: Optional limit on results
            
        Returns:
            List of events matching query
        """
        events = []
        
        if generation is not None and cycle is not None:
            # Get specific cycle
            cycle_data = self.get_cycle(generation, cycle)
            if cycle_data:
                events = cycle_data.get("events", [])
        else:
            # Get all cycles
            cycle_files = sorted(self.cycles_path.glob("*.json"))
            
            for cycle_file in cycle_files:
                with open(cycle_file, 'r') as f:
                    cycle_data = json.load(f)
                    events.extend(cycle_data.get("events", []))
            
            # Also check archive
            archive_path = self.torus_path / "archive"
            if archive_path.exists():
                archive_files = sorted(archive_path.glob("*.json"))
                for archive_file in archive_files:
                    with open(archive_file, 'r') as f:
                        cycle_data = json.load(f)
                        events.extend(cycle_data.get("events", []))
        
        # Apply filters
        if generation is not None:
            events = [e for e in events if e.get("generation") == generation]
        
        if cycle is not None:
            events = [e for e in events if e.get("cycle") == cycle]
        
        if event_type:
            events = [e for e in events if e.get("type") == event_type]
        
        # Sort by timestamp
        events.sort(key=lambda e: e.get("timestamp", ""))
        
        # Apply limit
        if limit:
            events = events[-limit:]
        
        return events
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get torus statistics."""
        cycle_files = list(self.cycles_path.glob("*.json"))
        generation_files = list(self.generations_path.glob("*.json"))
        
        archive_path = self.torus_path / "archive"
        archived_cycles = 0
        if archive_path.exists():
            archived_cycles = len(list(archive_path.glob("*.json")))
        
        return {
            "current_generation": self.current_generation,
            "current_cycle": self.current_cycle,
            "total_cycles": len(cycle_files),
            "total_generations": len(generation_files),
            "archived_cycles": archived_cycles,
            "max_past_cycles": self.max_past_cycles,
            "max_future_cycles": self.max_future_cycles,
        }
    
    def rotate(self):
        """
        Rotate the torus structure.
        
        This is the continuous evolution mechanism - the torus rotates,
        moving cycles through the hourglass structure.
        """
        # Complete current cycle (moves to top/past)
        self.complete_cycle()
        
        # The rotation is implicit - cycles flow from bottom (future)
        # through center (present) to top (past)
        
        # This method can be called periodically to ensure cycles
        # are properly rotated through the structure
