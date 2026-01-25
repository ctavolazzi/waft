"""
Teleport Massive Data Models

Content-addressable, serializable models for all story entities.
Designed for O(1) lookup, efficient compression, and self-querying.
"""

from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List, Any, Set
from uuid import uuid4


# =============================================================================
# ENUMS
# =============================================================================

class FactionType(Enum):
    """Types of factions in the TM universe."""
    SPECIES = "species"
    CORPORATION = "corporation"
    GOVERNMENT = "government"
    COSMIC_FORCE = "cosmic_force"
    CONDITION = "condition"  # e.g., Phaseburners
    COLLECTIVE = "collective"
    OTHER = "other"


class CharacterType(Enum):
    """Character classification."""
    HUMAN_TRADITIONAL = "human_traditional"
    HUMAN_ENHANCED = "human_enhanced"
    NEO_SAPIEN = "neo_sapien"
    HOMINID = "hominid"
    POLYMORPH = "polymorph"
    PHASEBURNER = "phaseburner"
    ANDROID = "android"
    PLASMOID = "plasmoid"
    OTHER = "other"


class RelationshipType(Enum):
    """Types of character relationships."""
    ALLY = "ally"
    ENEMY = "enemy"
    ROMANTIC = "romantic"
    FORMER_ROMANTIC = "former_romantic"
    PROFESSIONAL = "professional"
    FAMILY = "family"
    RIVAL = "rival"
    MENTOR = "mentor"
    STUDENT = "student"
    UNKNOWN = "unknown"


class ScintType(Enum):
    """Types of reality fractures."""
    TIMELINE_BRANCH = "timeline_branch"
    DIMENSIONAL_TEAR = "dimensional_tear"
    PARADOX = "paradox"
    QUANTUM_SUPERPOSITION = "quantum_superposition"
    PHASEBURN_FRACTURE = "phaseburn_fracture"


class NarrativeRole(Enum):
    """Character's role in the narrative."""
    PROTAGONIST = "protagonist"
    ANTAGONIST = "antagonist"
    DEUTERAGONIST = "deuteragonist"
    SUPPORTING = "supporting"
    MINOR = "minor"
    MENTIONED = "mentioned"


# =============================================================================
# BASE MODEL
# =============================================================================

@dataclass
class TMEntity:
    """Base class for all TM entities with content-addressing."""

    id: str = field(default_factory=lambda: str(uuid4())[:8])
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    tags: List[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        d = asdict(self)
        # Convert enums to their values
        for key, value in d.items():
            if isinstance(value, Enum):
                d[key] = value.value
            elif isinstance(value, list):
                d[key] = [v.value if isinstance(v, Enum) else v for v in value]
        return d

    def to_json(self) -> str:
        """Serialize to JSON."""
        return json.dumps(self.to_dict(), sort_keys=True, indent=2)

    @property
    def content_hash(self) -> str:
        """Generate content-addressed hash for this entity."""
        # Exclude timestamps for content comparison
        d = self.to_dict()
        d.pop('created_at', None)
        d.pop('updated_at', None)
        content = json.dumps(d, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16]


# =============================================================================
# CHARACTER MODEL
# =============================================================================

@dataclass
class Character(TMEntity):
    """A character in the TM universe."""

    name: str = ""
    full_name: str = ""
    aliases: List[str] = field(default_factory=list)

    # Classification
    character_type: CharacterType = CharacterType.HUMAN_TRADITIONAL
    narrative_role: NarrativeRole = NarrativeRole.SUPPORTING
    faction_affiliations: List[str] = field(default_factory=list)  # Faction IDs

    # Core traits
    occupation: str = ""
    age: Optional[int] = None
    description: str = ""

    # Psychology (Internal)
    motivations: List[str] = field(default_factory=list)
    fears: List[str] = field(default_factory=list)
    secrets: List[str] = field(default_factory=list)
    internal_conflicts: List[str] = field(default_factory=list)

    # Presentation (External)
    public_persona: str = ""
    speech_patterns: str = ""
    physical_description: str = ""
    mannerisms: List[str] = field(default_factory=list)

    # Relationships (character_id -> relationship)
    relationships: Dict[str, str] = field(default_factory=dict)

    # Arc tracking
    arc_summary: str = ""
    key_moments: List[str] = field(default_factory=list)
    transformation: str = ""  # e.g., "human -> android"

    # State (mutable across story)
    is_alive: bool = True
    current_location: str = ""

    def __repr__(self) -> str:
        return f"Character({self.name}, {self.character_type.value}, {self.narrative_role.value})"


# =============================================================================
# FACTION MODEL
# =============================================================================

@dataclass
class Faction(TMEntity):
    """A faction, organization, or group in the TM universe."""

    name: str = ""
    faction_type: FactionType = FactionType.OTHER

    description: str = ""
    philosophy: str = ""
    goals: List[str] = field(default_factory=list)
    methods: List[str] = field(default_factory=list)

    # Power structure
    leader: str = ""  # Character ID
    key_members: List[str] = field(default_factory=list)  # Character IDs

    # Relationships
    allies: List[str] = field(default_factory=list)  # Faction IDs
    enemies: List[str] = field(default_factory=list)  # Faction IDs

    # Resources
    resources: List[str] = field(default_factory=list)
    territories: List[str] = field(default_factory=list)  # Location IDs

    # Narrative role
    narrative_function: str = ""  # e.g., "primary antagonist organization"

    def __repr__(self) -> str:
        return f"Faction({self.name}, {self.faction_type.value})"


# =============================================================================
# LOCATION MODEL
# =============================================================================

@dataclass
class Location(TMEntity):
    """A location in the TM universe."""

    name: str = ""
    location_type: str = ""  # e.g., "corporate_hq", "city", "planet"

    description: str = ""
    atmosphere: str = ""  # Mood/feeling
    sensory_details: Dict[str, str] = field(default_factory=dict)  # sight, sound, smell, etc.

    # Geography
    parent_location: str = ""  # Location ID (e.g., city contains building)
    sub_locations: List[str] = field(default_factory=list)  # Location IDs

    # Associations
    controlling_faction: str = ""  # Faction ID
    inhabitants: List[str] = field(default_factory=list)  # Character IDs

    # Narrative
    scenes_set_here: List[str] = field(default_factory=list)  # Scene IDs
    significance: str = ""

    def __repr__(self) -> str:
        return f"Location({self.name}, {self.location_type})"


# =============================================================================
# ARTIFACT MODEL
# =============================================================================

@dataclass
class Artifact(TMEntity):
    """An important object, technology, or concept in the TM universe."""

    name: str = ""
    artifact_type: str = ""  # e.g., "technology", "weapon", "document", "concept"

    description: str = ""
    origin: str = ""

    # Properties
    capabilities: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    cost_of_use: str = ""  # e.g., "causes phaseburn"

    # Ownership
    current_owner: str = ""  # Character or Faction ID
    previous_owners: List[str] = field(default_factory=list)

    # Narrative
    significance: str = ""
    connected_to: List[str] = field(default_factory=list)  # Other entity IDs

    def __repr__(self) -> str:
        return f"Artifact({self.name}, {self.artifact_type})"


# =============================================================================
# TIMELINE EVENT MODEL
# =============================================================================

@dataclass
class TimelineEvent(TMEntity):
    """An event in the timeline."""

    name: str = ""
    date: str = ""  # Can be specific "2111-03-15" or vague "Before First Ascension"
    timeline_id: str = "prime"  # Which timeline/reality this belongs to

    description: str = ""

    # Participants
    characters_involved: List[str] = field(default_factory=list)
    factions_involved: List[str] = field(default_factory=list)
    location: str = ""

    # Causality
    causes: List[str] = field(default_factory=list)  # Event IDs that led to this
    effects: List[str] = field(default_factory=list)  # Event IDs this caused

    # Scinting
    is_scint_point: bool = False
    branches_created: List[str] = field(default_factory=list)  # Timeline IDs

    # Narrative
    significance: str = ""
    pov_character: str = ""  # Character ID

    def __repr__(self) -> str:
        return f"TimelineEvent({self.name}, {self.date}, timeline={self.timeline_id})"


# =============================================================================
# SCINT POINT MODEL
# =============================================================================

@dataclass
class ScintPoint(TMEntity):
    """A point where reality fractures into multiple branches."""

    name: str = ""
    scint_type: ScintType = ScintType.TIMELINE_BRANCH

    # When/where
    triggering_event: str = ""  # Event ID
    date: str = ""
    location: str = ""

    # What happened
    description: str = ""
    cause: str = ""

    # Branches
    parent_timeline: str = "prime"
    child_timelines: List[str] = field(default_factory=list)

    # Divergence details
    divergence_description: str = ""  # What's different between branches
    characters_affected: List[str] = field(default_factory=list)

    # Can branches interact?
    cross_branch_effects: bool = False

    def __repr__(self) -> str:
        return f"ScintPoint({self.name}, {self.scint_type.value})"


# =============================================================================
# KNOWLEDGE STATE MODEL
# =============================================================================

@dataclass
class KnowledgeState(TMEntity):
    """What a character knows/believes at a point in time."""

    character_id: str = ""
    as_of_event: str = ""  # Event ID or scene ID

    # Epistemic states
    knows: List[str] = field(default_factory=list)  # Facts they know
    believes: List[str] = field(default_factory=list)  # Things they believe (may be wrong)
    suspects: List[str] = field(default_factory=list)  # Things they suspect
    doesnt_know: List[str] = field(default_factory=list)  # Key things they're unaware of
    believes_wrongly: List[str] = field(default_factory=list)  # Specific false beliefs

    # About other characters
    opinions: Dict[str, str] = field(default_factory=dict)  # char_id -> opinion
    trust_levels: Dict[str, int] = field(default_factory=dict)  # char_id -> 0-100

    def __repr__(self) -> str:
        return f"KnowledgeState({self.character_id}, as_of={self.as_of_event})"


# =============================================================================
# STORY STATE MODEL (IMMUTABLE SNAPSHOT)
# =============================================================================

@dataclass
class StoryState(TMEntity):
    """An immutable snapshot of the entire story state at a point in time."""

    # Identity
    state_hash: str = ""  # Content-addressed ID
    parent_hash: str = ""  # Previous state (git-like)

    # Position
    timeline_id: str = "prime"
    current_chapter: int = 0
    current_scene: int = 0

    # All entity states at this moment
    characters: Dict[str, Dict] = field(default_factory=dict)  # id -> Character.to_dict()
    factions: Dict[str, Dict] = field(default_factory=dict)
    locations: Dict[str, Dict] = field(default_factory=dict)
    artifacts: Dict[str, Dict] = field(default_factory=dict)

    # Knowledge states for all characters
    knowledge_states: Dict[str, Dict] = field(default_factory=dict)  # char_id -> KnowledgeState

    # Active plot threads
    open_threads: List[str] = field(default_factory=list)
    resolved_threads: List[str] = field(default_factory=list)

    # Scint tracking
    active_timelines: List[str] = field(default_factory=list)
    scint_points: List[str] = field(default_factory=list)  # ScintPoint IDs

    # Narrative position
    last_event: str = ""
    pov_character: str = ""

    def compute_hash(self) -> str:
        """Compute content-addressed hash for this state."""
        # Create deterministic representation
        content = {
            'timeline_id': self.timeline_id,
            'chapter': self.current_chapter,
            'scene': self.current_scene,
            'characters': self.characters,
            'factions': self.factions,
            'locations': self.locations,
            'artifacts': self.artifacts,
            'knowledge_states': self.knowledge_states,
            'open_threads': sorted(self.open_threads),
            'active_timelines': sorted(self.active_timelines),
        }
        serialized = json.dumps(content, sort_keys=True)
        return hashlib.sha256(serialized.encode()).hexdigest()[:16]

    def finalize(self) -> "StoryState":
        """Compute and set the state hash."""
        self.state_hash = self.compute_hash()
        return self

    def __repr__(self) -> str:
        return f"StoryState(ch{self.current_chapter}:sc{self.current_scene}, hash={self.state_hash[:8] if self.state_hash else 'unfinalized'})"


# =============================================================================
# SCENE MODEL
# =============================================================================

@dataclass
class Scene(TMEntity):
    """A single scene in the narrative."""

    title: str = ""
    chapter: int = 0
    scene_number: int = 0

    # Context
    timeline_id: str = "prime"
    location: str = ""  # Location ID
    pov_character: str = ""  # Character ID

    # Content
    summary: str = ""
    beat_sheet: List[str] = field(default_factory=list)  # Key beats
    content: str = ""  # Actual prose

    # Characters present
    characters_present: List[str] = field(default_factory=list)

    # State changes
    state_before: str = ""  # StoryState hash
    state_after: str = ""  # StoryState hash
    events_occurred: List[str] = field(default_factory=list)  # Event IDs

    # Revelations
    information_revealed: List[str] = field(default_factory=list)
    to_whom: Dict[str, List[str]] = field(default_factory=dict)  # char_id -> [info revealed]

    # Metadata
    word_count: int = 0
    status: str = "planned"  # planned, drafted, revised, final

    def __repr__(self) -> str:
        return f"Scene(ch{self.chapter}:sc{self.scene_number} '{self.title}')"
