"""
Teleport Massive Story Configuration

Parameterized story setup - select starting conditions, characters,
timeline, tone, and other parameters before generation.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional
import json


class Tone(Enum):
    """Story tone presets."""
    NOIR = "noir"
    COSMIC_HORROR = "cosmic_horror"
    NOIR_COSMIC = "noir_cosmic"  # The classic TM blend
    HOPEFUL = "hopeful"
    DARK = "dark"
    SATIRICAL = "satirical"  # Pratchett mode
    LITERARY = "literary"


class NarrativeStyle(Enum):
    """Narrative voice style."""
    THIRD_LIMITED = "third_limited"  # Close POV
    THIRD_OMNISCIENT = "third_omniscient"  # God's eye
    FIRST_PERSON = "first_person"  # Character narrates
    UNRELIABLE = "unreliable"  # Narrator may lie
    META = "meta"  # Fourth wall aware


class PacingStyle(Enum):
    """Story pacing."""
    THRILLER = "thriller"  # Fast, tense
    LITERARY = "literary"  # Slower, contemplative
    EPISODIC = "episodic"  # Self-contained segments
    BUILDING = "building"  # Gradual escalation


# =============================================================================
# CONFIG PARAMETER
# =============================================================================

@dataclass
class ConfigParameter:
    """A single configurable parameter."""

    name: str
    display_name: str
    description: str
    param_type: str  # "select", "multi_select", "boolean", "number", "text"

    # For select/multi_select
    options: List[Dict[str, str]] = field(default_factory=list)  # [{"value": "x", "label": "X"}, ...]

    # Constraints
    default: Any = None
    required: bool = False
    min_value: Optional[float] = None
    max_value: Optional[float] = None

    def validate(self, value: Any) -> bool:
        """Validate a value against this parameter."""
        if self.required and value is None:
            return False

        if self.param_type == "select":
            valid_values = [opt["value"] for opt in self.options]
            return value in valid_values

        if self.param_type == "multi_select":
            valid_values = [opt["value"] for opt in self.options]
            return all(v in valid_values for v in value)

        if self.param_type == "number":
            if self.min_value is not None and value < self.min_value:
                return False
            if self.max_value is not None and value > self.max_value:
                return False

        return True


# =============================================================================
# STORY CONFIG
# =============================================================================

@dataclass
class StoryConfig:
    """
    Complete story configuration.

    This is what you fill out before generating a story.
    Like a character creation screen, but for the whole narrative.
    """

    # -------------------------------------------------------------------------
    # Core Settings
    # -------------------------------------------------------------------------

    # Protagonist selection
    protagonist: str = "sam_iker"  # Character ID

    # Starting point
    starting_year: int = 2111
    starting_event: str = "mayor_disappearance"  # Event ID or name

    # Which timeline
    timeline: str = "prime"

    # -------------------------------------------------------------------------
    # Faction Focus
    # -------------------------------------------------------------------------

    # Primary faction in focus
    primary_faction: str = "teleport_massive"

    # Active factions (which factions appear)
    active_factions: List[str] = field(default_factory=lambda: [
        "teleport_massive",
        "the_commonwealth",
        "android_rights_movement",
        "corpos"
    ])

    # -------------------------------------------------------------------------
    # Tone & Style
    # -------------------------------------------------------------------------

    tone: Tone = Tone.NOIR_COSMIC
    narrative_style: NarrativeStyle = NarrativeStyle.THIRD_LIMITED
    pacing: PacingStyle = PacingStyle.THRILLER

    # Pratchett elements
    enable_footnotes: bool = True
    enable_meta_narrative: bool = True  # Fourth wall awareness
    humor_level: int = 3  # 0-5, where 5 is full Pratchett

    # -------------------------------------------------------------------------
    # Content Toggles
    # -------------------------------------------------------------------------

    # What to include
    include_ascension_lore: bool = True
    include_source_nexus: bool = False  # Deep cosmic stuff
    include_phaseburn_horror: bool = True

    # Character arcs to enable
    sam_android_transformation: bool = True
    aziah_resurrection_quest: bool = True

    # -------------------------------------------------------------------------
    # Technical Settings
    # -------------------------------------------------------------------------

    # Generation
    chapter_count: int = 12
    scenes_per_chapter: int = 4
    target_word_count: int = 80000

    # Scinting
    allow_scinting: bool = True
    max_parallel_timelines: int = 3

    # -------------------------------------------------------------------------
    # Seed & Randomization
    # -------------------------------------------------------------------------

    seed: Optional[int] = None  # For reproducible generation
    randomization_level: float = 0.3  # 0.0 = deterministic, 1.0 = chaotic

    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "protagonist": self.protagonist,
            "starting_year": self.starting_year,
            "starting_event": self.starting_event,
            "timeline": self.timeline,
            "primary_faction": self.primary_faction,
            "active_factions": self.active_factions,
            "tone": self.tone.value,
            "narrative_style": self.narrative_style.value,
            "pacing": self.pacing.value,
            "enable_footnotes": self.enable_footnotes,
            "enable_meta_narrative": self.enable_meta_narrative,
            "humor_level": self.humor_level,
            "include_ascension_lore": self.include_ascension_lore,
            "include_source_nexus": self.include_source_nexus,
            "include_phaseburn_horror": self.include_phaseburn_horror,
            "sam_android_transformation": self.sam_android_transformation,
            "aziah_resurrection_quest": self.aziah_resurrection_quest,
            "chapter_count": self.chapter_count,
            "scenes_per_chapter": self.scenes_per_chapter,
            "target_word_count": self.target_word_count,
            "allow_scinting": self.allow_scinting,
            "max_parallel_timelines": self.max_parallel_timelines,
            "seed": self.seed,
            "randomization_level": self.randomization_level,
        }

    def to_json(self) -> str:
        """Serialize to JSON."""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StoryConfig":
        """Deserialize from dictionary."""
        # Handle enums
        if "tone" in data and isinstance(data["tone"], str):
            data["tone"] = Tone(data["tone"])
        if "narrative_style" in data and isinstance(data["narrative_style"], str):
            data["narrative_style"] = NarrativeStyle(data["narrative_style"])
        if "pacing" in data and isinstance(data["pacing"], str):
            data["pacing"] = PacingStyle(data["pacing"])

        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    @classmethod
    def from_json(cls, json_str: str) -> "StoryConfig":
        """Deserialize from JSON."""
        return cls.from_dict(json.loads(json_str))


# =============================================================================
# CONFIG SCHEMA (For UI generation)
# =============================================================================

def get_config_schema() -> List[ConfigParameter]:
    """
    Return the full configuration schema.

    This can be used to generate a UI (web form, CLI wizard, etc.)
    """
    return [
        ConfigParameter(
            name="protagonist",
            display_name="Protagonist",
            description="The main character whose perspective we follow",
            param_type="select",
            options=[
                {"value": "sam_iker", "label": "Sam Iker - Haunted Detective"},
                {"value": "aziah", "label": "Aziah - Grieving Scientist"},
                {"value": "diana", "label": "Diana Meilou - Sam's Partner"},
                {"value": "sarah", "label": "Sarah Letliner - Tech Prodigy"},
            ],
            default="sam_iker",
            required=True
        ),
        ConfigParameter(
            name="starting_year",
            display_name="Starting Year",
            description="When does the story begin?",
            param_type="number",
            default=2111,
            min_value=2000,
            max_value=3000
        ),
        ConfigParameter(
            name="starting_event",
            display_name="Inciting Incident",
            description="What triggers the story?",
            param_type="select",
            options=[
                {"value": "mayor_disappearance", "label": "Mayor Rodriguez Disappears"},
                {"value": "phaseburn_incident", "label": "Phaseburn Incident"},
                {"value": "aziah_experiment", "label": "Aziah's Experiment Goes Wrong"},
                {"value": "android_uprising", "label": "Android Rights Protest"},
            ],
            default="mayor_disappearance"
        ),
        ConfigParameter(
            name="tone",
            display_name="Tone",
            description="The overall mood and atmosphere",
            param_type="select",
            options=[
                {"value": "noir_cosmic", "label": "Noir + Cosmic Horror (Classic TM)"},
                {"value": "noir", "label": "Pure Noir Detective"},
                {"value": "cosmic_horror", "label": "Cosmic Horror Focus"},
                {"value": "satirical", "label": "Satirical (Full Pratchett)"},
                {"value": "hopeful", "label": "Hopeful Sci-Fi"},
            ],
            default="noir_cosmic"
        ),
        ConfigParameter(
            name="narrative_style",
            display_name="Narrative Style",
            description="How the story is told",
            param_type="select",
            options=[
                {"value": "third_limited", "label": "Third Person Limited (Close POV)"},
                {"value": "third_omniscient", "label": "Third Person Omniscient"},
                {"value": "first_person", "label": "First Person"},
                {"value": "unreliable", "label": "Unreliable Narrator"},
                {"value": "meta", "label": "Meta/Fourth Wall Aware"},
            ],
            default="third_limited"
        ),
        ConfigParameter(
            name="active_factions",
            display_name="Active Factions",
            description="Which factions appear in this story?",
            param_type="multi_select",
            options=[
                {"value": "teleport_massive", "label": "Teleport Massive"},
                {"value": "the_commonwealth", "label": "The Commonwealth (AI Government)"},
                {"value": "android_rights_movement", "label": "Android Rights Movement"},
                {"value": "corpos", "label": "Corporate Powers"},
                {"value": "polymorphs", "label": "Polymorphs"},
                {"value": "phaseburners", "label": "Phaseburner Survivors"},
                {"value": "neo_sapiens", "label": "Neo-Sapiens"},
                {"value": "galactic_federation", "label": "Galactic Federation"},
            ],
            default=["teleport_massive", "the_commonwealth", "android_rights_movement"]
        ),
        ConfigParameter(
            name="enable_footnotes",
            display_name="Enable Footnotes",
            description="Include Pratchett-style footnotes?",
            param_type="boolean",
            default=True
        ),
        ConfigParameter(
            name="enable_meta_narrative",
            display_name="Meta-Narrative",
            description="Allow fourth-wall breaking? (The manuscript is real)",
            param_type="boolean",
            default=True
        ),
        ConfigParameter(
            name="humor_level",
            display_name="Humor Level",
            description="How much Pratchett-style humor? (0=Serious, 5=Maximum wit)",
            param_type="number",
            default=3,
            min_value=0,
            max_value=5
        ),
        ConfigParameter(
            name="allow_scinting",
            display_name="Allow Reality Fractures",
            description="Can the timeline split into parallel realities?",
            param_type="boolean",
            default=True
        ),
        ConfigParameter(
            name="include_ascension_lore",
            display_name="Ascension Cycle Lore",
            description="Include the deep lore about humanity's previous Ascensions?",
            param_type="boolean",
            default=True
        ),
        ConfigParameter(
            name="include_source_nexus",
            display_name="Source/Nexus Cosmology",
            description="Include the cosmic forces (Source and Nexus)?",
            param_type="boolean",
            default=False
        ),
        ConfigParameter(
            name="sam_android_transformation",
            display_name="Sam's Transformation Arc",
            description="Does Sam transform into an android during the story?",
            param_type="boolean",
            default=True
        ),
        ConfigParameter(
            name="chapter_count",
            display_name="Chapter Count",
            description="How many chapters?",
            param_type="number",
            default=12,
            min_value=1,
            max_value=50
        ),
    ]


# =============================================================================
# PRESET CONFIGS
# =============================================================================

class ConfigPresets:
    """Pre-built configuration presets."""

    @staticmethod
    def classic_tm() -> StoryConfig:
        """The classic Teleport Massive experience."""
        return StoryConfig(
            protagonist="sam_iker",
            tone=Tone.NOIR_COSMIC,
            narrative_style=NarrativeStyle.THIRD_LIMITED,
            enable_footnotes=True,
            enable_meta_narrative=True,
            humor_level=3,
            include_ascension_lore=True,
            sam_android_transformation=True,
            aziah_resurrection_quest=True,
        )

    @staticmethod
    def pratchett_mode() -> StoryConfig:
        """Full Terry Pratchett satire mode."""
        return StoryConfig(
            protagonist="sam_iker",
            tone=Tone.SATIRICAL,
            narrative_style=NarrativeStyle.THIRD_OMNISCIENT,
            enable_footnotes=True,
            enable_meta_narrative=True,
            humor_level=5,
            pacing=PacingStyle.EPISODIC,
        )

    @staticmethod
    def cosmic_horror() -> StoryConfig:
        """Dark cosmic horror focus."""
        return StoryConfig(
            protagonist="sam_iker",
            tone=Tone.COSMIC_HORROR,
            narrative_style=NarrativeStyle.UNRELIABLE,
            enable_footnotes=False,
            enable_meta_narrative=True,
            humor_level=0,
            include_source_nexus=True,
            include_phaseburn_horror=True,
        )

    @staticmethod
    def aziah_perspective() -> StoryConfig:
        """Story from Aziah's perspective - the tragic scientist."""
        return StoryConfig(
            protagonist="aziah",
            tone=Tone.LITERARY,
            narrative_style=NarrativeStyle.FIRST_PERSON,
            starting_event="aziah_experiment",
            enable_footnotes=False,
            humor_level=1,
            aziah_resurrection_quest=True,
        )

    @staticmethod
    def short_story() -> StoryConfig:
        """A shorter, focused story."""
        return StoryConfig(
            chapter_count=3,
            scenes_per_chapter=3,
            target_word_count=15000,
            allow_scinting=False,
            include_ascension_lore=False,
            include_source_nexus=False,
        )
