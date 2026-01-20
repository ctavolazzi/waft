"""
The Archivist: Pantheon Entity of Divine Personnel Records

The Archivist is the mirror to The Librarian - while The Librarian manages
mortal knowledge and records, The Archivist maintains the sacred personnel
files of the Pantheon itself. Every God's backstory, astrology, relationships,
and divine attributes are preserved in The Archivist's domain.

Following "as above, so below" principles:
- As above: Keeper of divine identities and celestial histories
- So below: File-based system managing Pantheon personnel records

Storage:
- Personnel Files: _pantheon/personnel/{entity_id}/
- Profile Data: profile.json
- Backstory: backstory.md
- Artwork: artwork/
- Registry: _pantheon/archivist/personnel_registry.json
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class AstrologyProfile:
    """Astrological profile for a Pantheon entity."""

    birthday: str
    zodiac_sign: str
    element: str
    ruling_planet: str
    moon_sign: str | None = None
    rising_sign: str | None = None
    chinese_zodiac: str | None = None
    tarot_card: str | None = None
    cusp_name: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AstrologyProfile":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class PersonalityProfile:
    """Personality profile for a Pantheon entity."""

    archetype: str
    traits: list[str] = field(default_factory=list)
    virtues: list[str] = field(default_factory=list)
    flaws: list[str] = field(default_factory=list)
    fears: list[str] = field(default_factory=list)
    desires: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PersonalityProfile":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class DivineStatistics:
    """Divine power statistics for a Pantheon entity."""

    power_level: int = 50
    wisdom: int = 50
    charisma: int = 50
    speed: int = 50
    detail_orientation: int = 50
    comprehensiveness: int = 50

    def to_dict(self) -> dict[str, int]:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DivineStatistics":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class PantheonEntity:
    """A Pantheon entity's complete personnel record."""

    entity_id: str
    name: str
    title: str
    domain: str
    realm: str | None = None
    tier: str = "Minor Deity"

    # Identity
    true_name: str | None = None
    epithets: list[str] = field(default_factory=list)
    symbols: list[str] = field(default_factory=list)
    sacred_colors: list[str] = field(default_factory=list)

    # Profiles
    astrology: AstrologyProfile | None = None
    personality: PersonalityProfile | None = None
    statistics: DivineStatistics | None = None

    # Backstory
    origin: str | None = None
    awakening: str | None = None
    ascension: str | None = None
    prophecy: str | None = None

    # Powers
    major_powers: list[str] = field(default_factory=list)
    minor_powers: list[str] = field(default_factory=list)
    passive_powers: list[str] = field(default_factory=list)

    # Relationships
    allied_gods: dict[str, str] = field(default_factory=dict)
    rival_gods: list[str] = field(default_factory=list)

    # Worship
    prayer: str | None = None
    blessing: str | None = None
    curse: str | None = None
    holy_day: str | None = None

    # Quotes
    quotes: list[str] = field(default_factory=list)

    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
    artwork_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert entity to dictionary."""
        result = {
            "entity_id": self.entity_id,
            "name": self.name,
            "title": self.title,
            "domain": self.domain,
            "realm": self.realm,
            "tier": self.tier,
            "identity": {
                "true_name": self.true_name,
                "epithets": self.epithets,
                "symbols": self.symbols,
                "sacred_colors": self.sacred_colors,
            },
            "backstory": {
                "origin": self.origin,
                "awakening": self.awakening,
                "ascension": self.ascension,
                "prophecy": self.prophecy,
            },
            "powers": {
                "major": self.major_powers,
                "minor": self.minor_powers,
                "passive": self.passive_powers,
            },
            "relationships": {
                "allied_gods": self.allied_gods,
                "rival_gods": self.rival_gods,
            },
            "worship": {
                "prayer": self.prayer,
                "blessing": self.blessing,
                "curse": self.curse,
                "holy_day": self.holy_day,
            },
            "quotes": self.quotes,
            "created_at": self.created_at,
            "last_updated": self.last_updated,
            "artwork_path": self.artwork_path,
        }

        if self.astrology:
            result["astrology"] = self.astrology.to_dict()
        if self.personality:
            result["personality"] = self.personality.to_dict()
        if self.statistics:
            result["statistics"] = self.statistics.to_dict()

        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PantheonEntity":
        """Create entity from dictionary."""
        # Extract nested data
        identity = data.get("identity", {})
        backstory = data.get("backstory", {})
        powers = data.get("powers", {})
        relationships = data.get("relationships", {})
        worship = data.get("worship", {})

        entity = cls(
            entity_id=data["entity_id"],
            name=data["name"],
            title=data["title"],
            domain=data["domain"],
            realm=data.get("realm"),
            tier=data.get("tier", "Minor Deity"),
            # Identity
            true_name=identity.get("true_name"),
            epithets=identity.get("epithets", []),
            symbols=identity.get("symbols", []),
            sacred_colors=identity.get("sacred_colors", []),
            # Backstory
            origin=backstory.get("origin"),
            awakening=backstory.get("awakening"),
            ascension=backstory.get("ascension"),
            prophecy=backstory.get("prophecy"),
            # Powers
            major_powers=powers.get("major", []),
            minor_powers=powers.get("minor", []),
            passive_powers=powers.get("passive", []),
            # Relationships
            allied_gods=relationships.get("allied_gods", {}),
            rival_gods=relationships.get("rival_gods", []),
            # Worship
            prayer=worship.get("prayer"),
            blessing=worship.get("blessing"),
            curse=worship.get("curse"),
            holy_day=worship.get("holy_day"),
            # Other
            quotes=data.get("quotes", []),
            created_at=data.get("created_at", datetime.now().isoformat()),
            last_updated=data.get("last_updated", datetime.now().isoformat()),
            artwork_path=data.get("artwork_path"),
        )

        # Load profiles
        if "astrology" in data:
            entity.astrology = AstrologyProfile.from_dict(data["astrology"])
        if "personality" in data:
            entity.personality = PersonalityProfile.from_dict(data["personality"])
        if "statistics" in data:
            entity.statistics = DivineStatistics.from_dict(data["statistics"])

        return entity


class Archivist:
    """
    The Archivist: Pantheon Entity (Timeless Force that Binds Reality Together)

    Keeper of Divine Personnel Records - a timeless Entity that maintains
    the sacred personnel files of all Pantheon gods. The Archivist preserves
    identities, backstories, astrology, and divine attributes.

    Mirror to The Librarian:
    - Librarian: Manages mortal knowledge and records
    - Archivist: Manages divine personnel and celestial histories

    Storage:
    - Personnel Files: _pantheon/personnel/{entity_id}/
    - Registry: _pantheon/archivist/personnel_registry.json
    """

    def __init__(self, project_path: Path | None = None):
        """Initialize The Archivist."""
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)

        self.project_path = project_path
        self.pantheon_path = project_path / "_pantheon"
        self.personnel_path = self.pantheon_path / "personnel"
        self.archivist_path = self.pantheon_path / "archivist"
        self.registry_path = self.archivist_path / "personnel_registry.json"

        # Ensure directories
        self._ensure_directories()

        # Load registry
        self.registry: dict[str, dict[str, Any]] = {}
        self._load_registry()

    def _ensure_directories(self) -> None:
        """Ensure directory structure exists."""
        self.pantheon_path.mkdir(parents=True, exist_ok=True)
        self.personnel_path.mkdir(parents=True, exist_ok=True)
        self.archivist_path.mkdir(parents=True, exist_ok=True)

    def _load_registry(self) -> None:
        """Load registry from disk."""
        if self.registry_path.exists():
            with open(self.registry_path) as f:
                data = json.load(f)
                self.registry = data.get("entities", {})

    def _save_registry(self) -> None:
        """Save registry to disk."""
        data = {
            "entities": self.registry,
            "total_entities": len(self.registry),
            "last_updated": datetime.now().isoformat(),
        }
        with open(self.registry_path, "w") as f:
            json.dump(data, f, indent=2)

    def register_entity(self, entity: PantheonEntity) -> dict[str, Any]:
        """
        Register a new Pantheon entity.

        Args:
            entity: The PantheonEntity to register

        Returns:
            Registry entry for the entity
        """
        entity_path = self.personnel_path / entity.entity_id
        entity_path.mkdir(parents=True, exist_ok=True)
        (entity_path / "artwork").mkdir(exist_ok=True)

        # Save profile
        profile_path = entity_path / "profile.json"
        with open(profile_path, "w") as f:
            json.dump(entity.to_dict(), f, indent=2)

        # Update registry
        self.registry[entity.entity_id] = {
            "name": entity.name,
            "title": entity.title,
            "domain": entity.domain,
            "tier": entity.tier,
            "holy_day": entity.holy_day,
            "profile_path": str(profile_path),
            "registered_at": datetime.now().isoformat(),
        }
        self._save_registry()

        return self.registry[entity.entity_id]

    def get_entity(self, entity_id: str) -> PantheonEntity | None:
        """Get a Pantheon entity by ID."""
        entity_path = self.personnel_path / entity_id / "profile.json"
        if not entity_path.exists():
            return None

        with open(entity_path) as f:
            data = json.load(f)
            return PantheonEntity.from_dict(data)

    def list_entities(self, tier: str | None = None) -> list[dict[str, Any]]:
        """List all registered entities."""
        entities = list(self.registry.values())
        if tier:
            entities = [e for e in entities if e.get("tier") == tier]
        return entities

    def get_entity_profile_path(self, entity_id: str) -> Path | None:
        """Get the file path for an entity's profile."""
        if entity_id in self.registry:
            return Path(self.registry[entity_id]["profile_path"])
        return None

    def get_entity_artwork_path(self, entity_id: str) -> Path:
        """Get the artwork directory for an entity."""
        return self.personnel_path / entity_id / "artwork"

    def update_entity(self, entity: PantheonEntity) -> dict[str, Any]:
        """Update an existing entity's profile."""
        entity.last_updated = datetime.now().isoformat()
        return self.register_entity(entity)

    def get_horoscope(self, entity_id: str) -> dict[str, Any] | None:
        """Get an entity's horoscope data."""
        entity = self.get_entity(entity_id)
        if entity and entity.astrology:
            return {
                "entity": entity.name,
                "birthday": entity.astrology.birthday,
                "zodiac": entity.astrology.zodiac_sign,
                "element": entity.astrology.element,
                "ruling_planet": entity.astrology.ruling_planet,
                "tarot_card": entity.astrology.tarot_card,
            }
        return None

    def get_all_holy_days(self) -> dict[str, str]:
        """Get all holy days for all entities."""
        return {eid: e.get("holy_day", "Unknown") for eid, e in self.registry.items() if e.get("holy_day")}

    def get_summary(self) -> dict[str, Any]:
        """Get summary of The Archivist's domain."""
        entities = list(self.registry.values())

        by_tier = {}
        for e in entities:
            tier = e.get("tier", "Unknown")
            by_tier[tier] = by_tier.get(tier, 0) + 1

        return {
            "total_entities": len(entities),
            "by_tier": by_tier,
            "holy_days_documented": len([e for e in entities if e.get("holy_day")]),
            "last_updated": datetime.now().isoformat(),
        }

    def generate_tarot_card_data(self, entity_id: str) -> dict[str, Any] | None:
        """Generate data for a tarot card representation."""
        entity = self.get_entity(entity_id)
        if not entity:
            return None

        return {
            "card_name": entity.name,
            "card_number": entity.astrology.tarot_card if entity.astrology else "Unknown",
            "title": entity.title,
            "domain": entity.domain,
            "element": entity.astrology.element if entity.astrology else "Unknown",
            "symbols": entity.symbols,
            "colors": entity.sacred_colors,
            "keywords": entity.personality.traits[:5] if entity.personality else [],
            "blessing": entity.blessing,
            "warning": entity.curse,
            "quote": entity.quotes[0] if entity.quotes else None,
        }

    def export_personnel_file(self, entity_id: str) -> str:
        """Export a formatted personnel file for an entity."""
        entity = self.get_entity(entity_id)
        if not entity:
            return f"Entity {entity_id} not found."

        lines = [
            f"# PANTHEON PERSONNEL FILE",
            f"## {entity.name}",
            f"**Title:** {entity.title}",
            f"**Domain:** {entity.domain}",
            f"**Tier:** {entity.tier}",
            "",
            "### Identity",
            f"**True Name:** {entity.true_name or 'Unknown'}",
            f"**Epithets:** {', '.join(entity.epithets) if entity.epithets else 'None'}",
            "",
        ]

        if entity.astrology:
            lines.extend(
                [
                    "### Astrology",
                    f"**Birthday:** {entity.astrology.birthday}",
                    f"**Zodiac:** {entity.astrology.zodiac_sign}",
                    f"**Element:** {entity.astrology.element}",
                    f"**Ruling Planet:** {entity.astrology.ruling_planet}",
                    f"**Tarot Card:** {entity.astrology.tarot_card or 'Unknown'}",
                    "",
                ]
            )

        if entity.personality:
            lines.extend(
                [
                    "### Personality",
                    f"**Archetype:** {entity.personality.archetype}",
                    f"**Traits:** {', '.join(entity.personality.traits)}",
                    f"**Virtues:** {', '.join(entity.personality.virtues)}",
                    f"**Flaws:** {', '.join(entity.personality.flaws)}",
                    "",
                ]
            )

        if entity.quotes:
            lines.extend(
                [
                    "### Sacred Quotes",
                    *[f'> "{q}"' for q in entity.quotes],
                    "",
                ]
            )

        lines.extend(
            [
                "---",
                f"*Filed by The Archivist | Last Updated: {entity.last_updated}*",
            ]
        )

        return "\n".join(lines)
