"""
Teleport Massive Canonical Lore

The authoritative data source for the TM universe.
All characters, factions, locations, and history.
"""

from __future__ import annotations
from typing import Dict, List, Any, Optional


class TMLore:
    """
    Canonical lore for the Teleport Massive universe.

    This is the single source of truth for all world data.
    """

    def __init__(self):
        self._init_world_state()
        self._init_characters()
        self._init_factions()
        self._init_locations()
        self._init_artifacts()
        self._init_timeline()
        self._init_knowledge_map()

    # =========================================================================
    # WORLD STATE
    # =========================================================================

    def _init_world_state(self):
        """Core world parameters."""
        self.world = {
            "year": 2111,
            "era": "Post-Singularity, Post-Scarcity",
            "political_status": "Galactic Federation Member",
            "ascension_cycle": {
                "current": 3,
                "phase": "Harvest",
                "context": "The Struggle of Earth",
                "previous_ascensions": 2,
            },
            "technology_level": {
                "agi": "Advanced, ubiquitous",
                "teleportation": "Mastered (with side effects)",
                "genetic_engineering": "Neo-Sapien creation possible",
                "nanotech": "Polymorph collectives exist",
                "dimensional_travel": "Possible (causes Phaseburn)",
            },
            "cosmic_forces": {
                "source": {
                    "name": "Source",
                    "description": "The energy from which everything in the Universe derives",
                    "nature": "Creative, generative",
                },
                "nexus": {
                    "name": "Nexus",
                    "description": "The sinister and foreboding antagonist to the Universe itself",
                    "nature": "Destructive, entropic",
                },
            },
        }

    # =========================================================================
    # CHARACTERS
    # =========================================================================

    def _init_characters(self):
        """All characters in the TM universe."""
        self.characters: Dict[str, Dict[str, Any]] = {
            # -----------------------------------------------------------------
            # PROTAGONISTS
            # -----------------------------------------------------------------
            "sam_iker": {
                "id": "sam_iker",
                "name": "Sam Iker",
                "full_name": "Detective Sam Iker",
                "character_type": "human_traditional",
                "narrative_role": "protagonist",
                "occupation": "Detective",
                "description": "A seasoned investigator haunted by personal tragedy he feels he caused",
                "faction_affiliations": ["police_force"],

                # Psychology
                "motivations": [
                    "Find the truth about Mayor Rodriguez",
                    "Atone for past failures",
                    "Protect those he cares about",
                ],
                "fears": [
                    "Repeating past mistakes",
                    "Losing more people he loves",
                    "The truth about himself",
                ],
                "secrets": [
                    "Blames himself for a past death",
                    "Growing suspicion about the nature of identity",
                ],
                "internal_conflicts": [
                    "Duty vs. personal feelings for Diana",
                    "Human identity vs. what he's becoming",
                ],

                # Arc
                "arc_summary": "Detective investigating TM → discovers conspiracy → transforms into android → confronts nature of identity",
                "transformation": "human → android",
                "key_moments": [
                    "Takes Mayor Rodriguez case",
                    "First encounter with Phaseburner",
                    "Discovers TM cloning experiments",
                    "Transformation into android",
                    "Confrontation with Aziah",
                ],

                # Relationships
                "relationships": {
                    "diana_meilou": "former_romantic, professional_partner",
                    "sarah_letliner": "professional, protective",
                    "aziah": "antagonist, mirror",
                    "mayor_rodriguez": "case_subject",
                },

                # Initial state
                "is_alive": True,
                "current_location": "city_streets",
            },

            "diana_meilou": {
                "id": "diana_meilou",
                "name": "Diana Meilou",
                "full_name": "Detective Diana Meilou",
                "aliases": ["Diona"],
                "character_type": "human_enhanced",
                "narrative_role": "deuteragonist",
                "occupation": "Detective",
                "description": "Sam's ex-girlfriend and current partner, navigating professional and personal complexities",
                "faction_affiliations": ["police_force"],

                "motivations": [
                    "Solve the case",
                    "Protect Sam from himself",
                    "Prove herself independent of their history",
                ],
                "fears": [
                    "Losing Sam again",
                    "The case consuming them both",
                ],
                "internal_conflicts": [
                    "Professional distance vs. lingering feelings",
                    "Trust in Sam vs. his increasingly erratic behavior",
                ],

                "relationships": {
                    "sam_iker": "former_romantic, professional_partner",
                    "sarah_letliner": "professional, mentor",
                },

                "is_alive": True,
                "current_location": "police_station",
            },

            "sarah_letliner": {
                "id": "sarah_letliner",
                "name": "Sarah Letliner",
                "full_name": "Sarah Letliner",
                "aliases": ["Sara"],
                "character_type": "human_enhanced",
                "narrative_role": "supporting",
                "occupation": "Tech Prodigy / Analyst",
                "age": 24,
                "description": "A young technical genius who provides crucial insights into TM's technology",
                "faction_affiliations": ["police_force", "tech_underground"],

                "motivations": [
                    "Understand the technology",
                    "Prove her worth",
                    "Uncover the truth",
                ],
                "fears": [
                    "Being underestimated",
                    "The implications of what she discovers",
                ],

                "relationships": {
                    "sam_iker": "professional, admiration",
                    "diana_meilou": "professional, student",
                },

                "is_alive": True,
                "current_location": "tech_lab",
            },

            # -----------------------------------------------------------------
            # ANTAGONISTS
            # -----------------------------------------------------------------
            "aziah": {
                "id": "aziah",
                "name": "Aziah",
                "full_name": "Dr. Aziah Calderon",
                "character_type": "human_enhanced",
                "narrative_role": "antagonist",
                "occupation": "Quantum Scientist / TM Lead Researcher",
                "description": "A brilliant scientist driven by the tragic quest to resurrect his wife",
                "faction_affiliations": ["teleport_massive"],

                "motivations": [
                    "Resurrect his wife",
                    "Push the boundaries of science",
                    "Prove death is not final",
                ],
                "fears": [
                    "That his wife is truly gone",
                    "That he's become a monster",
                    "Success (and its implications)",
                ],
                "secrets": [
                    "The true nature of TM's cloning experiments",
                    "His wife's death was connected to TM technology",
                    "He's not entirely sure the clones are 'not' his wife",
                ],
                "internal_conflicts": [
                    "Love vs. ethics",
                    "Scientist vs. grieving husband",
                    "What he's doing vs. what she would have wanted",
                ],

                "arc_summary": "Grieving scientist → unethical experiments → confrontation → choice",
                "key_quote": "They said death was final. They must be wrong.",

                "relationships": {
                    "sam_iker": "antagonist, mirror",
                    "wife_deceased": "motivation, obsession",
                    "teleport_massive": "employer, enabler",
                },

                "is_alive": True,
                "current_location": "teleport_massive_labs",
            },

            # -----------------------------------------------------------------
            # KEY FIGURES
            # -----------------------------------------------------------------
            "mayor_rodriguez": {
                "id": "mayor_rodriguez",
                "name": "Mayor Rodriguez",
                "full_name": "Mayor Elena Rodriguez",
                "character_type": "human_enhanced",
                "narrative_role": "supporting",
                "occupation": "Mayor / Political Figure",
                "description": "A key figure in humanity's interstellar colonization who mysteriously vanishes",
                "faction_affiliations": ["the_commonwealth", "galactic_federation"],

                "motivations": [
                    "Humanity's expansion into the galaxy",
                    "Balance between progress and ethics",
                ],
                "secrets": [
                    "Knew about TM's experiments",
                    "Was about to expose them",
                ],

                "is_alive": "unknown",  # The central mystery
                "current_location": "unknown",
            },

            "fai_wei": {
                "id": "fai_wei",
                "name": "Fai Wei",
                "full_name": "Fai Wei",
                "character_type": "human_enhanced",
                "narrative_role": "antagonist",
                "occupation": "Founder and CEO of Teleport Massive",
                "description": "The visionary founder who built the teleportation empire",
                "faction_affiliations": ["teleport_massive"],

                "motivations": [
                    "Corporate dominance",
                    "Technological supremacy",
                    "Control",
                ],

                "is_alive": True,
                "current_location": "teleport_massive_hq",
            },
        }

    # =========================================================================
    # FACTIONS
    # =========================================================================

    def _init_factions(self):
        """All factions in the TM universe."""
        self.factions: Dict[str, Dict[str, Any]] = {
            # -----------------------------------------------------------------
            # CORPORATIONS
            # -----------------------------------------------------------------
            "teleport_massive": {
                "id": "teleport_massive",
                "name": "Teleport Massive",
                "faction_type": "corporation",
                "description": "The corporation that invented real-life teleportation, one of the most powerful entities in all Reality",
                "philosophy": "Progress at any cost",
                "goals": [
                    "Monopolize teleportation technology",
                    "Expand influence across spacetime",
                    "Unlock the secrets of dimensional travel",
                ],
                "methods": [
                    "Cutting-edge research",
                    "Corporate espionage",
                    "Unethical experiments",
                    "Political manipulation",
                ],
                "secrets": [
                    "Human cloning experiments",
                    "Phaseburn victims hidden from public",
                    "Connection to Mayor Rodriguez disappearance",
                ],
                "leader": "fai_wei",
                "key_members": ["aziah"],
                "narrative_function": "Primary antagonist organization",
            },

            "corpos": {
                "id": "corpos",
                "name": "Corporate Powers (Corpos)",
                "faction_type": "corporation",
                "description": "Powerful corporations with deep-rooted agendas driving innovation and conspiracy",
                "philosophy": "Profit and power",
                "goals": [
                    "Economic dominance",
                    "Political influence",
                    "Technological control",
                ],
                "narrative_function": "Background power players, systemic antagonist",
            },

            # -----------------------------------------------------------------
            # GOVERNMENT
            # -----------------------------------------------------------------
            "the_commonwealth": {
                "id": "the_commonwealth",
                "name": "The Commonwealth",
                "faction_type": "government",
                "description": "An AI-driven central government balancing the complexities of future society",
                "philosophy": "Order through optimization",
                "goals": [
                    "Maintain societal stability",
                    "Balance faction interests",
                    "Guide humanity's integration into galactic community",
                ],
                "narrative_function": "Ambiguous authority - neither fully ally nor enemy",
            },

            "galactic_federation": {
                "id": "galactic_federation",
                "name": "Galactic Federation",
                "faction_type": "government",
                "description": "The interstellar political body humanity has joined",
                "philosophy": "Cooperation between species",
                "goals": [
                    "Maintain galactic peace",
                    "Facilitate interspecies relations",
                ],
                "narrative_function": "Larger context, background power",
            },

            # -----------------------------------------------------------------
            # SPECIES/GROUPS
            # -----------------------------------------------------------------
            "humans_traditional": {
                "id": "humans_traditional",
                "name": "Traditional Humans",
                "faction_type": "species",
                "description": "Unenhanced baseline humans navigating the new world order",
                "narrative_function": "Perspective anchor, audience surrogate",
            },

            "humans_enhanced": {
                "id": "humans_enhanced",
                "name": "Enhanced Humans",
                "faction_type": "species",
                "description": "Technologically augmented humans with various enhancements",
                "narrative_function": "Transitional identity, bridge between old and new",
            },

            "neo_sapiens": {
                "id": "neo_sapiens",
                "name": "Neo-Sapiens",
                "faction_type": "species",
                "description": "Genetically superior beings created by humans, demigod-like in abilities",
                "philosophy": "Evolution directed",
                "narrative_function": "Push human potential, question of creation",
            },

            "hominids": {
                "id": "hominids",
                "name": "Hominids",
                "faction_type": "species",
                "description": "Diverse human-like species from across the galaxy within the Galactic Federation",
                "narrative_function": "Introduce galactic diversity and perspective",
            },

            "polymorphs": {
                "id": "polymorphs",
                "name": "Polymorphs",
                "faction_type": "collective",
                "description": "Intelligent nanobot collectives with shapeshifting abilities, a non-biological hive-mind",
                "philosophy": "Fluidity of form, unity of purpose",
                "narrative_function": "Challenge definition of life and identity",
            },

            "phaseburners": {
                "id": "phaseburners",
                "name": "Phaseburners",
                "faction_type": "condition",
                "description": "Individuals afflicted by the physical and psychological scars of dimensional travel",
                "philosophy": "Survival and solidarity",
                "narrative_function": "Living cost of technological progress, victims",
            },

            "android_rights_movement": {
                "id": "android_rights_movement",
                "name": "Sentient Androids",
                "faction_type": "species",
                "description": "Sentient synthetic beings in a struggle for civil rights and recognition",
                "philosophy": "Synthetic autonomy, equal rights",
                "goals": [
                    "Legal recognition as persons",
                    "End to discrimination",
                    "Self-determination",
                ],
                "narrative_function": "Mirror for Sam's transformation, rights allegory",
            },

            "plasmoids": {
                "id": "plasmoids",
                "name": "Plasmoids",
                "faction_type": "species",
                "description": "Living plasma beings with incomprehensible timescales and agendas",
                "philosophy": "Unknown - operates on different temporal scale",
                "narrative_function": "Truly alien perspective, cosmic scale",
            },

            # -----------------------------------------------------------------
            # COSMIC FORCES
            # -----------------------------------------------------------------
            "source": {
                "id": "source",
                "name": "Source",
                "faction_type": "cosmic_force",
                "description": "The energy from which everything in the Universe derives",
                "philosophy": "Creation, generation, growth",
                "narrative_function": "Ultimate cosmic positive force",
            },

            "nexus": {
                "id": "nexus",
                "name": "Nexus",
                "faction_type": "cosmic_force",
                "description": "The sinister and foreboding antagonist to the Universe itself",
                "philosophy": "Entropy, destruction, ending",
                "narrative_function": "Ultimate cosmic threat, deep lore antagonist",
            },

            "the_others": {
                "id": "the_others",
                "name": "The Others",
                "faction_type": "other",
                "description": "An umbrella for the myriad of unclassified beings and factions",
                "narrative_function": "Narrative flexibility, mystery preservation",
            },
        }

    # =========================================================================
    # LOCATIONS
    # =========================================================================

    def _init_locations(self):
        """Key locations in the TM universe."""
        self.locations: Dict[str, Dict[str, Any]] = {
            "teleport_massive_hq": {
                "id": "teleport_massive_hq",
                "name": "Teleport Massive Headquarters",
                "location_type": "corporate_hq",
                "description": "The gleaming tower that houses the most powerful corporation in reality",
                "atmosphere": "Corporate perfection masking dark secrets",
                "controlling_faction": "teleport_massive",
            },

            "teleport_massive_labs": {
                "id": "teleport_massive_labs",
                "name": "TM Research Labs",
                "location_type": "research_facility",
                "description": "Where the unethical experiments are conducted",
                "atmosphere": "Clinical sterility with an undercurrent of wrongness",
                "parent_location": "teleport_massive_hq",
                "controlling_faction": "teleport_massive",
            },

            "city_streets": {
                "id": "city_streets",
                "name": "The City",
                "location_type": "urban",
                "description": "The sprawling metropolis of 2111, where traditional and enhanced humans coexist",
                "atmosphere": "Neon and rain, hope and despair intermingled",
            },

            "police_station": {
                "id": "police_station",
                "name": "Central Precinct",
                "location_type": "government_building",
                "description": "Where Sam and Diana work their cases",
                "atmosphere": "Bureaucratic but purposeful",
            },

            "underground": {
                "id": "underground",
                "name": "The Underground",
                "location_type": "hidden_district",
                "description": "Where Phaseburners and other outcasts survive",
                "atmosphere": "Desperate but defiant",
            },

            "aziah_lab": {
                "id": "aziah_lab",
                "name": "Aziah's Private Laboratory",
                "location_type": "research_facility",
                "description": "Where Aziah conducts his most personal experiments",
                "atmosphere": "Obsession made manifest",
            },
        }

    # =========================================================================
    # ARTIFACTS
    # =========================================================================

    def _init_artifacts(self):
        """Important objects, technologies, and concepts."""
        self.artifacts: Dict[str, Dict[str, Any]] = {
            "teleportation_technology": {
                "id": "teleportation_technology",
                "name": "Teleportation Technology",
                "artifact_type": "technology",
                "description": "The groundbreaking technology that allows instant travel",
                "capabilities": [
                    "Instant transportation",
                    "Dimensional travel (experimental)",
                ],
                "limitations": [
                    "Causes Phaseburn in some cases",
                    "Energy intensive",
                ],
                "cost_of_use": "Risk of Phaseburn, especially for dimensional travel",
                "current_owner": "teleport_massive",
            },

            "phaseburn": {
                "id": "phaseburn",
                "name": "Phaseburn",
                "artifact_type": "condition",
                "description": "A perilous side effect of dimensional travel that fractures one's existence",
                "effects": [
                    "Physical scarring",
                    "Psychological trauma",
                    "Fractured existence across dimensions",
                    "Sometimes: glimpses of other realities",
                ],
                "significance": "Living testament to the cost of progress",
            },

            "swab_swae": {
                "id": "swab_swae",
                "name": "SWAB/SWAE",
                "artifact_type": "artifact",
                "description": "Mysterious artifacts from outside time",
                "origin": "Unknown - outside normal spacetime",
                "capabilities": ["Unknown"],
                "significance": "Deep mystery, possibly connected to Source/Nexus",
            },

            "the_manuscript": {
                "id": "the_manuscript",
                "name": "The Manuscript",
                "artifact_type": "document",
                "description": "The document you are reading. It is both key and lock.",
                "capabilities": [
                    "Opens the door",
                    "Unlocks the Key",
                ],
                "significance": "Meta-narrative anchor, breaks fourth wall",
            },

            "cloning_technology": {
                "id": "cloning_technology",
                "name": "Human Cloning Technology",
                "artifact_type": "technology",
                "description": "TM's secret human replication experiments",
                "capabilities": [
                    "Create physical duplicates of humans",
                    "Potentially transfer consciousness?",
                ],
                "current_owner": "teleport_massive",
                "significance": "Central to Aziah's quest and TM's crimes",
            },
        }

    # =========================================================================
    # TIMELINE
    # =========================================================================

    def _init_timeline(self):
        """Key events in the TM timeline."""
        self.timeline: List[Dict[str, Any]] = [
            {
                "id": "first_ascension",
                "name": "First Ascension",
                "date": "Ancient history",
                "description": "Humanity's first Ascension - details lost",
            },
            {
                "id": "second_ascension",
                "name": "Second Ascension",
                "date": "Deep past",
                "description": "Humanity's second Ascension - details fragmentary",
            },
            {
                "id": "singularity",
                "name": "The Technological Singularity",
                "date": "~2050",
                "description": "Humanity achieves technological singularity",
            },
            {
                "id": "tm_founded",
                "name": "Teleport Massive Founded",
                "date": "~2070",
                "description": "Fai Wei founds Teleport Massive",
            },
            {
                "id": "teleportation_achieved",
                "name": "Teleportation Achieved",
                "date": "~2080",
                "description": "TM perfects teleportation technology",
            },
            {
                "id": "galactic_contact",
                "name": "Galactic Federation Contact",
                "date": "~2095",
                "description": "Humanity joins the Galactic Federation",
            },
            {
                "id": "aziah_wife_death",
                "name": "Aziah's Wife Dies",
                "date": "~2108",
                "description": "The tragedy that drives Aziah's quest begins",
            },
            {
                "id": "mayor_disappearance",
                "name": "Mayor Rodriguez Disappears",
                "date": "2111",
                "description": "The inciting incident - Mayor Rodriguez vanishes",
                "is_starting_event": True,
            },
            {
                "id": "story_present",
                "name": "Story Present",
                "date": "2111",
                "description": "Current narrative time - Third Ascension, Harvest phase",
            },
        ]

    # =========================================================================
    # KNOWLEDGE MAP
    # =========================================================================

    def _init_knowledge_map(self):
        """What each character knows at story start."""
        self.starting_knowledge: Dict[str, List[str]] = {
            "sam_iker": [
                "Mayor Rodriguez is missing",
                "Teleport Massive is involved somehow",
                "Diana is his ex and current partner",
            ],
            "diana_meilou": [
                "Mayor Rodriguez is missing",
                "Sam has personal demons",
                "Something is wrong at TM",
            ],
            "sarah_letliner": [
                "TM's technology has hidden flaws",
                "Phaseburn is more common than reported",
            ],
            "aziah": [
                "How to clone humans",
                "His wife can be brought back",
                "What really happened to Mayor Rodriguez",
            ],
        }

        self.hidden_knowledge: Dict[str, List[str]] = {
            "sam_iker": [
                "TM is cloning humans",
                "Aziah's true motivations",
                "The Ascension Cycle",
                "Source and Nexus",
            ],
            "diana_meilou": [
                "Sam will transform",
                "The depth of TM's crimes",
            ],
            "sarah_letliner": [
                "The full scope of what she'll uncover",
            ],
        }

    # =========================================================================
    # QUERY METHODS
    # =========================================================================

    def get_character(self, char_id: str) -> Optional[Dict[str, Any]]:
        """Get a character by ID."""
        return self.characters.get(char_id)

    def get_faction(self, faction_id: str) -> Optional[Dict[str, Any]]:
        """Get a faction by ID."""
        return self.factions.get(faction_id)

    def get_location(self, loc_id: str) -> Optional[Dict[str, Any]]:
        """Get a location by ID."""
        return self.locations.get(loc_id)

    def get_starting_knowledge(self, char_id: str) -> List[str]:
        """Get what a character knows at story start."""
        return self.starting_knowledge.get(char_id, [])

    def get_hidden_from(self, char_id: str) -> List[str]:
        """Get what is hidden from a character at story start."""
        return self.hidden_knowledge.get(char_id, [])

    def get_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get a timeline event by ID."""
        for event in self.timeline:
            if event["id"] == event_id:
                return event
        return None

    def list_characters_by_faction(self, faction_id: str) -> List[str]:
        """Get all characters affiliated with a faction."""
        result = []
        for char_id, char_data in self.characters.items():
            if faction_id in char_data.get("faction_affiliations", []):
                result.append(char_id)
        return result

    def get_all_character_ids(self) -> List[str]:
        """Get all character IDs."""
        return list(self.characters.keys())

    def get_all_faction_ids(self) -> List[str]:
        """Get all faction IDs."""
        return list(self.factions.keys())

    def summary(self) -> Dict[str, int]:
        """Get a summary of lore contents."""
        return {
            "characters": len(self.characters),
            "factions": len(self.factions),
            "locations": len(self.locations),
            "artifacts": len(self.artifacts),
            "timeline_events": len(self.timeline),
        }
