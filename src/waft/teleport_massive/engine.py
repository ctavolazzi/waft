"""
Teleport Massive Story Engine

Autonomous story generation with visual novel output.
Takes a configuration, generates narrative, tracks state.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, List, Any, Callable
from datetime import datetime
import json
import random

from .models import (
    Character, Faction, Location, Artifact, TimelineEvent,
    ScintPoint, StoryState, KnowledgeState, Scene,
    CharacterType, NarrativeRole, FactionType
)
from .storage import StoryStore
from .config import StoryConfig, Tone, NarrativeStyle
from .lore import TMLore


# =============================================================================
# STORY ENGINE
# =============================================================================

class StoryEngine:
    """
    The core story generation engine.

    Maintains world state, generates scenes, tracks consistency.
    """

    def __init__(self, config: StoryConfig, store: StoryStore, lore: TMLore):
        self.config = config
        self.store = store
        self.lore = lore

        # Current state
        self.current_state: Optional[StoryState] = None

        # Random generator (seeded for reproducibility)
        self.rng = random.Random(config.seed)

    def initialize(self) -> StoryState:
        """
        Initialize the story with starting conditions.

        Creates the initial world state based on configuration.
        """
        # Build initial state
        state = StoryState(
            timeline_id=self.config.timeline,
            current_chapter=0,
            current_scene=0,
            characters=self._init_characters(),
            factions=self._init_factions(),
            locations=self._init_locations(),
            artifacts=self._init_artifacts(),
            knowledge_states=self._init_knowledge(),
            open_threads=self._init_threads(),
            active_timelines=[self.config.timeline],
        )

        # Save and set as current
        self.store.save_state(state, self.config.timeline)
        self.current_state = state

        # Tag as story start
        self.store.tag("story_start", state.state_hash)

        return state

    def _init_characters(self) -> Dict[str, Dict]:
        """Initialize characters from lore based on config."""
        chars = {}
        for char_id, char_data in self.lore.characters.items():
            # Check if character should be included
            if self._should_include_character(char_id):
                chars[char_id] = char_data
        return chars

    def _init_factions(self) -> Dict[str, Dict]:
        """Initialize factions from lore based on config."""
        factions = {}
        for faction_id, faction_data in self.lore.factions.items():
            if faction_id in self.config.active_factions or faction_id in ["source", "nexus"]:
                factions[faction_id] = faction_data
        return factions

    def _init_locations(self) -> Dict[str, Dict]:
        """Initialize locations from lore."""
        return dict(self.lore.locations)

    def _init_artifacts(self) -> Dict[str, Dict]:
        """Initialize artifacts from lore."""
        return dict(self.lore.artifacts)

    def _init_knowledge(self) -> Dict[str, Dict]:
        """Initialize what each character knows at start."""
        knowledge = {}
        for char_id in self._init_characters().keys():
            knowledge[char_id] = {
                "knows": self.lore.get_starting_knowledge(char_id),
                "believes": [],
                "suspects": [],
                "doesnt_know": self.lore.get_hidden_from(char_id),
            }
        return knowledge

    def _init_threads(self) -> List[str]:
        """Initialize starting plot threads."""
        threads = []
        if self.config.starting_event == "mayor_disappearance":
            threads.append("thread:mayor_rodriguez_disappearance")
        if self.config.aziah_resurrection_quest:
            threads.append("thread:aziah_wife_resurrection")
        if self.config.sam_android_transformation:
            threads.append("thread:sam_identity_crisis")
        threads.append("thread:teleport_massive_conspiracy")
        return threads

    def _should_include_character(self, char_id: str) -> bool:
        """Determine if a character should be in the story."""
        # Always include protagonist
        if char_id == self.config.protagonist:
            return True
        # Include main cast
        if char_id in ["sam_iker", "diana_meilou", "sarah_letliner", "aziah", "mayor_rodriguez"]:
            return True
        # Include based on faction affiliations
        char_data = self.lore.characters.get(char_id, {})
        affiliations = char_data.get("faction_affiliations", [])
        return any(f in self.config.active_factions for f in affiliations)

    # -------------------------------------------------------------------------
    # Scene Generation
    # -------------------------------------------------------------------------

    def generate_scene(self, chapter: int, scene_num: int) -> Scene:
        """
        Generate a single scene.

        This is the core generation function that would integrate
        with an LLM for actual prose generation.
        """
        if not self.current_state:
            self.initialize()

        # Determine scene parameters
        pov_char = self._select_pov_character(chapter, scene_num)
        location = self._select_location(chapter, scene_num)
        characters_present = self._select_characters_for_scene(pov_char, location)

        # Generate beat sheet
        beats = self._generate_beats(chapter, scene_num, pov_char)

        # Create scene object
        scene = Scene(
            title=self._generate_scene_title(chapter, scene_num),
            chapter=chapter,
            scene_number=scene_num,
            timeline_id=self.config.timeline,
            location=location,
            pov_character=pov_char,
            characters_present=characters_present,
            beat_sheet=beats,
            state_before=self.current_state.state_hash if self.current_state else "",
            status="generated"
        )

        # Generate prose (placeholder for LLM integration)
        scene.content = self._generate_prose(scene)
        scene.word_count = len(scene.content.split())

        # Update world state
        new_state = self._apply_scene_effects(scene)
        scene.state_after = new_state.state_hash

        # Save scene
        self.store.save_entity(scene, "scene")

        return scene

    def _select_pov_character(self, chapter: int, scene_num: int) -> str:
        """Select POV character for a scene."""
        # Default to protagonist for most scenes
        if scene_num == 1 or self.rng.random() < 0.7:
            return self.config.protagonist

        # Occasionally switch POV
        candidates = list(self.current_state.characters.keys())
        candidates = [c for c in candidates if c != self.config.protagonist]
        if candidates:
            return self.rng.choice(candidates)
        return self.config.protagonist

    def _select_location(self, chapter: int, scene_num: int) -> str:
        """Select location for a scene."""
        locations = list(self.current_state.locations.keys())
        if not locations:
            return "unknown_location"

        # Weight towards relevant locations based on plot
        if chapter <= 3:
            preferred = ["teleport_massive_hq", "city_streets", "police_station"]
        else:
            preferred = ["teleport_massive_labs", "underground", "aziah_lab"]

        for pref in preferred:
            if pref in locations:
                if self.rng.random() < 0.6:
                    return pref

        return self.rng.choice(locations)

    def _select_characters_for_scene(self, pov_char: str, location: str) -> List[str]:
        """Select which characters appear in a scene."""
        present = [pov_char]

        # Add regular partners
        if pov_char == "sam_iker":
            if self.rng.random() < 0.7:
                present.append("diana_meilou")
            if self.rng.random() < 0.5:
                present.append("sarah_letliner")

        # Add 0-2 additional characters
        others = [c for c in self.current_state.characters.keys() if c not in present]
        num_others = self.rng.randint(0, min(2, len(others)))
        present.extend(self.rng.sample(others, num_others) if others else [])

        return present

    def _generate_beats(self, chapter: int, scene_num: int, pov_char: str) -> List[str]:
        """Generate beat sheet for a scene."""
        beats = []

        # Opening beat
        beats.append(f"OPEN: Establish {pov_char} in location")

        # Middle beats based on plot threads
        for thread in self.current_state.open_threads[:2]:
            beats.append(f"DEVELOP: Progress on {thread}")

        # Complication
        beats.append("COMPLICATION: Something goes wrong or is revealed")

        # Closing beat
        beats.append("CLOSE: Decision or cliffhanger")

        return beats

    def _generate_prose(self, scene: Scene) -> str:
        """
        Generate actual prose for a scene.

        This is a placeholder that returns template prose.
        In production, this would call an LLM.
        """
        # Get character and location data
        pov_data = self.current_state.characters.get(scene.pov_character, {})
        location_data = self.current_state.locations.get(scene.location, {})

        pov_name = pov_data.get("name", scene.pov_character)
        location_name = location_data.get("name", scene.location)

        # Build prose template
        prose = f"""## Chapter {scene.chapter}, Scene {scene.scene_number}: {scene.title}

{location_name}. {location_data.get("atmosphere", "The air felt charged with possibility.")}

{pov_name} stood at the threshold of discovery."""

        # Add footnote if enabled
        if self.config.enable_footnotes and self.rng.random() < 0.3:
            prose += """

*[^1]: In the year 2111, thresholds had become something of a specialty.
Teleport Massive had, quite literally, made a business of them.*

"""

        prose += f"""

The investigation had led here. Every clue, every whispered rumor about Teleport Massive,
every sleepless night parsing through classified documents—it all converged on this moment.

"""

        # Add character interactions
        others = [c for c in scene.characters_present if c != scene.pov_character]
        if others:
            other_data = self.current_state.characters.get(others[0], {})
            other_name = other_data.get("name", others[0])
            prose += f'"{pov_name}," {other_name} said, "we need to talk about what we found."\n\n'

        # Add meta-narrative if enabled
        if self.config.enable_meta_narrative and scene.chapter == 1 and scene.scene_number == 1:
            prose += """
---

*Reader, if you've found this manuscript, you already know more than you should.
The fact that you're reading these words means the Key has begun to turn.
What follows is not fiction. It never was.*

---

"""

        prose += f"""
The threads of conspiracy wound tighter. Mayor Rodriguez's disappearance was just the surface—
beneath it lay something far more troubling. Something that touched the very fabric of what
humanity had become in this post-singularity age.

{pov_name} made a decision.

There would be no turning back.

---

*[Scene continues...]*
"""

        return prose

    def _apply_scene_effects(self, scene: Scene) -> StoryState:
        """Apply scene effects to world state and return new state."""
        # Clone current state
        new_state = StoryState(
            timeline_id=self.current_state.timeline_id,
            current_chapter=scene.chapter,
            current_scene=scene.scene_number,
            characters=dict(self.current_state.characters),
            factions=dict(self.current_state.factions),
            locations=dict(self.current_state.locations),
            artifacts=dict(self.current_state.artifacts),
            knowledge_states=dict(self.current_state.knowledge_states),
            open_threads=list(self.current_state.open_threads),
            resolved_threads=list(self.current_state.resolved_threads),
            active_timelines=list(self.current_state.active_timelines),
            scint_points=list(self.current_state.scint_points),
            last_event=f"scene_{scene.chapter}_{scene.scene_number}",
            pov_character=scene.pov_character,
        )

        # Update and save
        self.store.save_state(new_state, self.config.timeline)
        self.current_state = new_state

        return new_state

    def _generate_scene_title(self, chapter: int, scene_num: int) -> str:
        """Generate a title for the scene."""
        titles = {
            (1, 1): "The Disappearance",
            (1, 2): "First Lead",
            (1, 3): "The Corporation",
            (1, 4): "Questions Without Answers",
            (2, 1): "Deeper",
            (2, 2): "The Phaseburner",
            (2, 3): "Corporate Lies",
            (2, 4): "A Name in the Dark",
        }
        return titles.get((chapter, scene_num), f"Scene {chapter}.{scene_num}")

    # -------------------------------------------------------------------------
    # Chapter Generation
    # -------------------------------------------------------------------------

    def generate_chapter(self, chapter_num: int) -> List[Scene]:
        """Generate all scenes in a chapter."""
        scenes = []
        for scene_num in range(1, self.config.scenes_per_chapter + 1):
            scene = self.generate_scene(chapter_num, scene_num)
            scenes.append(scene)
        return scenes

    # -------------------------------------------------------------------------
    # Visual Novel Export
    # -------------------------------------------------------------------------

    def export_visual_novel(self, output_path: Path) -> Dict[str, Any]:
        """
        Export the story in visual novel format.

        Returns a structure suitable for VN engines.
        """
        vn_data = {
            "metadata": {
                "title": "Teleport Massive",
                "config": self.config.to_dict(),
                "generated_at": datetime.utcnow().isoformat(),
            },
            "characters": {},
            "scenes": [],
            "choices": [],
        }

        # Export characters
        for char_id, char_data in self.current_state.characters.items():
            vn_data["characters"][char_id] = {
                "name": char_data.get("name", char_id),
                "display_name": char_data.get("full_name", char_data.get("name", char_id)),
                "description": char_data.get("description", ""),
            }

        # Export would continue with scenes...

        # Write to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(vn_data, indent=2))

        return vn_data


# =============================================================================
# TM WRITER (High-level API)
# =============================================================================

class TMWriter:
    """
    High-level API for the Teleport Massive Writer.

    Usage:
        writer = TMWriter.create("classic_tm")
        chapter = writer.generate_chapter(1)
        writer.export_pdf(Path("chapter1.pdf"))
    """

    def __init__(self, config: StoryConfig, base_path: Optional[Path] = None):
        self.config = config
        self.base_path = base_path or Path.home() / ".waft" / "teleport_massive"

        # Initialize components
        self.store = StoryStore(self.base_path / "store")
        self.lore = TMLore()
        self.engine = StoryEngine(config, self.store, self.lore)

    @classmethod
    def create(cls, preset: str = "classic_tm", **overrides) -> "TMWriter":
        """Create a writer with a preset configuration."""
        from .config import ConfigPresets

        preset_map = {
            "classic_tm": ConfigPresets.classic_tm,
            "pratchett": ConfigPresets.pratchett_mode,
            "cosmic_horror": ConfigPresets.cosmic_horror,
            "aziah": ConfigPresets.aziah_perspective,
            "short": ConfigPresets.short_story,
        }

        config_func = preset_map.get(preset, ConfigPresets.classic_tm)
        config = config_func()

        # Apply overrides
        for key, value in overrides.items():
            if hasattr(config, key):
                setattr(config, key, value)

        return cls(config)

    def initialize(self) -> StoryState:
        """Initialize the story world."""
        return self.engine.initialize()

    def generate_chapter(self, chapter_num: int) -> List[Scene]:
        """Generate a chapter."""
        if not self.engine.current_state:
            self.initialize()
        return self.engine.generate_chapter(chapter_num)

    def get_current_state(self) -> Optional[StoryState]:
        """Get current story state."""
        return self.engine.current_state

    def get_history(self) -> List[StoryState]:
        """Get full story history."""
        return list(self.store.history())

    def export_visual_novel(self, output_path: Path) -> Dict[str, Any]:
        """Export as visual novel data."""
        return self.engine.export_visual_novel(output_path)

    def stats(self) -> Dict[str, Any]:
        """Get writer statistics."""
        return {
            "config": self.config.to_dict(),
            "store": self.store.stats(),
            "current_chapter": self.engine.current_state.current_chapter if self.engine.current_state else 0,
            "current_scene": self.engine.current_state.current_scene if self.engine.current_state else 0,
        }
