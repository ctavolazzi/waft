"""
The Observer: Scientific Registry for Evolutionary Code Laboratory.

A singleton class that maintains an immutable JSONL log of all evolutionary events
for scientific research and phylogenetic tree reconstruction.
"""

import json
from pathlib import Path
from typing import Optional
from datetime import datetime
from threading import Lock


class TheObserver:
    """
    Singleton scientific registry for recording evolutionary events.
    
    Maintains an immutable .jsonl log in _pyrite/science/laboratory.jsonl
    that records every spawn, mutation, and fitness test for research.
    """
    
    _instance: Optional["TheObserver"] = None
    _lock = Lock()
    
    def __new__(cls, project_path: Optional[Path] = None):
        """Singleton pattern: ensure only one Observer exists."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, project_path: Optional[Path] = None):
        """Initialize TheObserver with project path."""
        if self._initialized:
            return
        
        if project_path is None:
            # Try to detect project root by looking for _pyrite directory
            current = Path.cwd()
            for parent in [current] + list(current.parents):
                if (parent / "_pyrite").exists():
                    project_path = parent
                    break
            
            if project_path is None:
                project_path = current
        
        self.project_path = Path(project_path)
        self.laboratory_path = self.project_path / "_pyrite" / "science"
        self.laboratory_path.mkdir(parents=True, exist_ok=True)
        self.log_file = self.laboratory_path / "laboratory.jsonl"
        
        self._initialized = True
    
    def observe_event(self, event: "EvolutionaryEvent") -> None:
        """
        Record an evolutionary event to the laboratory log.
        
        STRICT DOCTRINE: Passive recording only. Never interferes.
        Logs every 'Metabolic Action' and 'Phylogenetic Event'.
        
        Args:
            event: EvolutionaryEvent to record
        """
        # Convert event to dict, ensuring datetime is ISO formatted
        event_dict = event.dict()
        if isinstance(event_dict.get("timestamp"), datetime):
            event_dict["timestamp"] = event_dict["timestamp"].isoformat()
        
        # Ensure scientific_name is included (from payload or compute from genome_id)
        if "scientific_name" not in event_dict:
            payload = event_dict.get("payload", {})
            if "scientific_name" in payload:
                event_dict["scientific_name"] = payload["scientific_name"]
            else:
                # Compute from genome_id if not present (skip for SESSION_END)
                from .taxonomy import LineagePoet
                genome_id = event_dict.get("genome_id", "")
                event_type = event_dict.get("event_type", "")
                if genome_id and event_type != "session_end":
                    try:
                        event_dict["scientific_name"] = LineagePoet.generate_name(genome_id)
                    except (ValueError, IndexError):
                        # Invalid genome_id format, skip
                        event_dict["scientific_name"] = None
                elif event_type == "session_end":
                    event_dict["scientific_name"] = "SESSION_END"
        
        # Write as JSONL (one JSON object per line)
        with open(self.log_file, "a", encoding="utf-8") as f:
            json.dump(event_dict, f, ensure_ascii=False)
            f.write("\n")
    
    def get_laboratory_log(self, limit: Optional[int] = None) -> list:
        """
        Read events from the laboratory log.
        
        Args:
            limit: Maximum number of events to return (None = all)
            
        Returns:
            List of event dictionaries
        """
        if not self.log_file.exists():
            return []
        
        events = []
        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    events.append(json.loads(line))
                    if limit and len(events) >= limit:
                        break
        
        return events


# Forward reference for type hint
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..agent.state import EvolutionaryEvent
