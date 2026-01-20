"""
D&D 5e Campaign State Management

Manages campaign state, sessions, characters, and events.
Provides persistence and state tracking for the AI DM system.
"""

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class CampaignStatus(Enum):
    """Campaign status."""

    PLANNING = "planning"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class SessionStatus(Enum):
    """Session status."""

    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class CampaignEvent:
    """A single event in the campaign."""

    event_id: str
    timestamp: str
    event_type: str  # "encounter", "choice", "decision", "narrative", etc.
    description: str
    participants: list[str] = field(default_factory=list)  # Being IDs
    data: dict[str, Any] = field(default_factory=dict)
    sequence_id: str | None = None  # If from scenario engine
    choice_made: str | None = None  # If player choice
    decision_matrix_id: str | None = None  # If used decision matrix


@dataclass
class CampaignSession:
    """A single campaign session."""

    session_id: str
    campaign_id: str
    session_number: int
    status: SessionStatus
    start_time: str
    end_time: str | None = None
    events: list[CampaignEvent] = field(default_factory=list)
    current_sequence_id: str | None = None
    containers: dict[str, list[str]] = field(default_factory=dict)  # Scenario engine containers
    notes: str = ""
    summary: str | None = None


@dataclass
class CampaignState:
    """Complete campaign state."""

    campaign_id: str
    campaign_name: str
    status: CampaignStatus
    created_at: str
    updated_at: str
    scenario_file: str | None = None
    start_sequence_id: str | None = None
    current_sequence_id: str | None = None

    # Characters
    player_characters: dict[str, str] = field(default_factory=dict)  # player_name -> being_id
    npcs: dict[str, str] = field(default_factory=dict)  # npc_name -> being_id

    # Sessions
    sessions: list[CampaignSession] = field(default_factory=list)
    current_session_id: str | None = None

    # Campaign state
    containers: dict[str, list[str]] = field(default_factory=dict)  # Scenario engine containers
    campaign_data: dict[str, Any] = field(default_factory=dict)  # Custom campaign data

    # Decisions
    decisions_made: list[dict[str, Any]] = field(default_factory=list)  # Decision matrix results

    # Analysis
    scientific_experiments: list[str] = field(default_factory=list)  # Experiment IDs

    # Metadata
    description: str = ""
    difficulty: str = "medium"
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        # Convert enums to strings
        data["status"] = self.status.value
        if self.sessions:
            data["sessions"] = [
                {**asdict(session), "status": session.status.value} for session in self.sessions
            ]
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CampaignState":
        """Create from dictionary."""
        # Convert status strings to enums
        data["status"] = CampaignStatus(data["status"])

        # Convert sessions
        if "sessions" in data and data["sessions"]:
            sessions = []
            for session_data in data["sessions"]:
                session_data["status"] = SessionStatus(session_data["status"])
                session = CampaignSession(**session_data)
                sessions.append(session)
            data["sessions"] = sessions

        return cls(**data)


class CampaignStateManager:
    """Manages campaign state persistence and retrieval."""

    def __init__(self, project_path: Path):
        """Initialize campaign state manager."""
        self.project_path = Path(project_path)
        self.campaigns_dir = self.project_path / "_pyrite" / ".waft" / "campaigns"
        self.campaigns_dir.mkdir(parents=True, exist_ok=True)

    def create_campaign(
        self,
        campaign_name: str,
        scenario_file: str | None = None,
        description: str = "",
        difficulty: str = "medium",
    ) -> CampaignState:
        """Create a new campaign."""
        campaign_id = f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        campaign = CampaignState(
            campaign_id=campaign_id,
            campaign_name=campaign_name,
            status=CampaignStatus.PLANNING,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            scenario_file=scenario_file,
            description=description,
            difficulty=difficulty,
        )

        self.save_campaign(campaign)
        return campaign

    def save_campaign(self, campaign: CampaignState) -> Path:
        """Save campaign state to file."""
        campaign.updated_at = datetime.now().isoformat()

        file_path = self.campaigns_dir / f"{campaign.campaign_id}.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(campaign.to_dict(), f, indent=2, default=str)

        return file_path

    def load_campaign(self, campaign_id: str) -> CampaignState | None:
        """Load campaign by ID."""
        file_path = self.campaigns_dir / f"{campaign_id}.json"

        if not file_path.exists():
            return None

        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        return CampaignState.from_dict(data)

    def list_campaigns(self) -> list[dict[str, Any]]:
        """List all campaigns."""
        campaigns = []

        for file_path in self.campaigns_dir.glob("campaign_*.json"):
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
                campaigns.append(
                    {
                        "campaign_id": data.get("campaign_id"),
                        "campaign_name": data.get("campaign_name"),
                        "status": data.get("status"),
                        "created_at": data.get("created_at"),
                        "session_count": len(data.get("sessions", [])),
                    }
                )

        return sorted(campaigns, key=lambda x: x["created_at"], reverse=True)

    def add_session(
        self, campaign_id: str, session_number: int | None = None
    ) -> CampaignSession:
        """Add a new session to campaign."""
        campaign = self.load_campaign(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")

        if session_number is None:
            session_number = len(campaign.sessions) + 1

        session_id = f"session_{campaign_id}_{session_number:03d}"

        session = CampaignSession(
            session_id=session_id,
            campaign_id=campaign_id,
            session_number=session_number,
            status=SessionStatus.SCHEDULED,
            start_time=datetime.now().isoformat(),
        )

        campaign.sessions.append(session)
        campaign.current_session_id = session_id

        self.save_campaign(campaign)
        return session

    def add_event(
        self,
        campaign_id: str,
        session_id: str,
        event_type: str,
        description: str,
        participants: list[str] | None = None,
        data: dict[str, Any] | None = None,
        sequence_id: str | None = None,
        choice_made: str | None = None,
        decision_matrix_id: str | None = None,
    ) -> CampaignEvent:
        """Add an event to a session."""
        campaign = self.load_campaign(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")

        # Find session
        session = None
        session_index = None
        for i, s in enumerate(campaign.sessions):
            if s.session_id == session_id:
                session = s
                session_index = i
                break

        if not session:
            raise ValueError(
                f"Session {session_id} not found in campaign {campaign_id}. Available sessions: {[s.session_id for s in campaign.sessions]}"
            )

        event_id = f"event_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        event = CampaignEvent(
            event_id=event_id,
            timestamp=datetime.now().isoformat(),
            event_type=event_type,
            description=description,
            participants=participants or [],
            data=data or {},
            sequence_id=sequence_id,
            choice_made=choice_made,
            decision_matrix_id=decision_matrix_id,
        )

        session.events.append(event)
        campaign.updated_at = datetime.now().isoformat()

        self.save_campaign(campaign)
        return event

    def update_session_status(
        self, campaign_id: str, session_id: str, status: SessionStatus
    ) -> None:
        """Update session status."""
        campaign = self.load_campaign(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")

        for session in campaign.sessions:
            if session.session_id == session_id:
                session.status = status
                if status == SessionStatus.COMPLETED:
                    session.end_time = datetime.now().isoformat()
                campaign.updated_at = datetime.now().isoformat()
                self.save_campaign(campaign)
                return

        raise ValueError(f"Session {session_id} not found")

    def get_campaign_summary(self, campaign_id: str) -> dict[str, Any]:
        """Get campaign summary statistics."""
        campaign = self.load_campaign(campaign_id)
        if not campaign:
            return {}

        return {
            "campaign_id": campaign.campaign_id,
            "campaign_name": campaign.campaign_name,
            "status": campaign.status.value,
            "session_count": len(campaign.sessions),
            "total_events": sum(len(s.events) for s in campaign.sessions),
            "player_count": len(campaign.player_characters),
            "npc_count": len(campaign.npcs),
            "decisions_made": len(campaign.decisions_made),
            "experiments_run": len(campaign.scientific_experiments),
            "created_at": campaign.created_at,
            "updated_at": campaign.updated_at,
        }
