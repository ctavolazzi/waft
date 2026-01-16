"""
Story State Models - Data structures for evolving stories.

Defines the state models for stories that evolve over time with agent direction.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class Character(BaseModel):
    """Character in the story."""
    name: str
    role: Optional[str] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)
    relationships: Dict[str, str] = Field(default_factory=dict)  # character_name -> relationship_type
    arc: Optional[str] = None  # Character development arc
    mentions: int = 0
    last_appearance: Optional[datetime] = None


class Event(BaseModel):
    """Event in the story timeline."""
    event_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    description: str
    character: Optional[str] = None
    location: Optional[str] = None
    category: str = "event"  # event, action, revelation, conflict, resolution
    importance: float = 0.5  # 0.0 to 1.0
    narrative_text: Optional[str] = None


class PlotPoint(BaseModel):
    """Plot point in the story structure."""
    plot_point_id: str
    title: str
    description: str
    act: Optional[str] = None  # beginning, middle, end
    resolved: bool = False
    importance: float = 0.5


class StoryState(BaseModel):
    """
    Complete state of an evolving story.
    
    Tracks characters, timeline, plot points, and world state across generations.
    """
    story_id: str = Field(description="Unique story identifier")
    title: str = Field(description="Story title")
    generation: int = Field(default=0, description="Current generation number")
    
    # Story elements
    characters: Dict[str, Character] = Field(default_factory=dict, description="Story characters")
    timeline: List[Event] = Field(default_factory=list, description="Chronological event timeline")
    plot_points: List[PlotPoint] = Field(default_factory=list, description="Story plot points")
    world_state: Dict[str, Any] = Field(default_factory=dict, description="World state and settings")
    
    # Narrative
    narrative_text: str = Field(default="", description="Current narrative prose")
    summary: str = Field(default="", description="Story summary")
    
    # Quality metrics
    coherence_score: float = Field(default=1.0, description="Story coherence (0.0 to 1.0)")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    evolution_history: List[Dict[str, Any]] = Field(default_factory=list, description="History of changes")
    
    def add_character(self, character: Character) -> None:
        """Add or update a character."""
        self.characters[character.name] = character
        self.last_updated = datetime.utcnow()
    
    def add_event(self, event: Event) -> None:
        """Add an event to the timeline."""
        self.timeline.append(event)
        # Update character last appearance if applicable
        if event.character and event.character in self.characters:
            self.characters[event.character].last_appearance = event.timestamp
            self.characters[event.character].mentions += 1
        self.last_updated = datetime.utcnow()
    
    def add_plot_point(self, plot_point: PlotPoint) -> None:
        """Add a plot point."""
        self.plot_points.append(plot_point)
        self.last_updated = datetime.utcnow()
    
    def get_recent_events(self, limit: int = 10) -> List[Event]:
        """Get most recent events."""
        return sorted(self.timeline, key=lambda e: e.timestamp, reverse=True)[:limit]
    
    def get_characters_by_role(self, role: str) -> List[Character]:
        """Get all characters with a specific role."""
        return [char for char in self.characters.values() if char.role == role]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return self.dict()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StoryState":
        """Create from dictionary."""
        # Convert nested dicts to models
        if "characters" in data:
            data["characters"] = {
                name: Character(**char_data) if isinstance(char_data, dict) else char_data
                for name, char_data in data["characters"].items()
            }
        if "timeline" in data:
            data["timeline"] = [
                Event(**event_data) if isinstance(event_data, dict) else event_data
                for event_data in data["timeline"]
            ]
        if "plot_points" in data:
            data["plot_points"] = [
                PlotPoint(**plot_data) if isinstance(plot_data, dict) else plot_data
                for plot_data in data["plot_points"]
            ]
        return cls(**data)
