"""
World Manager - Orchestrates Generators and Maintains World State
================================================================

The World Manager:
- Generates world seeds on game start
- Tracks NPCs, locations, and relationships
- Manages location connections
- Provides rich context to the AI storyteller
- Handles on-demand generation of new areas
"""

import random
from dataclasses import dataclass, field
from typing import Literal
from uuid import uuid4

from .names import NameGenerator
from .npcs import NPCGenerator, NPC
from .tavern import TavernGenerator, Tavern
from .dungeon import DungeonGenerator, Dungeon


LocationType = Literal["tavern", "dungeon", "town", "wilderness", "shop", "road"]


@dataclass
class Location:
    """A generated location in the world."""
    id: str
    name: str
    location_type: LocationType
    description: str
    data: dict = field(default_factory=dict)  # Type-specific data (Tavern, Dungeon, etc.)
    connections: list[str] = field(default_factory=list)  # IDs of connected locations
    visited: bool = False
    known: bool = True  # Has player heard of this place?

    def storyteller_context(self) -> dict:
        """Get context for AI storyteller."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.location_type,
            "description": self.description,
            "visited": self.visited,
            **self.data,
        }


@dataclass
class WorldState:
    """Complete state of the generated world."""
    seed: int
    locations: dict[str, Location] = field(default_factory=dict)
    npcs: dict[str, NPC] = field(default_factory=dict)  # name -> NPC
    rumors: list[str] = field(default_factory=list)
    current_location_id: str | None = None
    discovered_secrets: list[str] = field(default_factory=list)
    active_quests: list[dict] = field(default_factory=list)

    def current_location(self) -> Location | None:
        """Get the current location."""
        if self.current_location_id:
            return self.locations.get(self.current_location_id)
        return None

    def add_location(self, location: Location):
        """Add a location to the world."""
        self.locations[location.id] = location

    def add_npc(self, npc: NPC, location_id: str | None = None):
        """Add an NPC to the world."""
        self.npcs[npc.name] = npc

    def get_known_npcs(self) -> list[NPC]:
        """Get NPCs the player has met."""
        return list(self.npcs.values())

    def to_dict(self) -> dict:
        """Serialize for API."""
        return {
            "seed": self.seed,
            "current_location": self.current_location_id,
            "locations": {k: v.storyteller_context() for k, v in self.locations.items()},
            "known_npcs": [n.short_description() for n in self.npcs.values()],
            "rumors": self.rumors,
            "active_quests": self.active_quests,
        }


class WorldManager:
    """
    Orchestrates procedural generation and maintains world state.

    Usage:
        world = WorldManager(seed=42)
        state, opening = world.generate_starting_world()
        # state now contains a tavern with NPCs, rumors, etc.

        # When player leaves tavern:
        dungeon_location = world.generate_location("dungeon", connected_to="tavern_id")
    """

    def __init__(self, seed: int | None = None):
        self.seed = seed or random.randint(0, 2**32)
        self.rng = random.Random(self.seed)

        # Initialize generators with same seed for reproducibility
        self.name_gen = NameGenerator(self.seed)
        self.npc_gen = NPCGenerator(self.seed)
        self.tavern_gen = TavernGenerator(self.seed)
        self.dungeon_gen = DungeonGenerator(self.seed)

        self.state = WorldState(seed=self.seed)

    def generate_starting_world(self, setting: str = "fantasy_tavern") -> tuple[WorldState, dict]:
        """
        Generate the starting world state.

        Returns:
            (WorldState, opening_context) - The world state and context for the AI.
        """
        if setting == "fantasy_tavern":
            return self._generate_tavern_start()
        elif setting == "dungeon_entrance":
            return self._generate_dungeon_start()
        else:
            return self._generate_tavern_start()

    def _generate_tavern_start(self) -> tuple[WorldState, dict]:
        """Generate starting tavern world."""
        # Generate the starting tavern
        tavern = self.tavern_gen.generate(tavern_type="adventurers_guild")

        # Create location entry
        tavern_location = Location(
            id=f"tavern_{uuid4().hex[:8]}",
            name=tavern.name,
            location_type="tavern",
            description=tavern.description(),
            data=tavern.storyteller_context(),
            visited=True,
            known=True,
        )

        self.state.add_location(tavern_location)
        self.state.current_location_id = tavern_location.id

        # Add tavern NPCs to world registry
        for npc in tavern.staff + tavern.patrons:
            self.state.add_npc(npc, tavern_location.id)

        # Add tavern rumors to world
        self.state.rumors.extend(tavern.rumors)

        # Generate connected locations (known but not visited)
        self._generate_nearby_locations(tavern_location, count=3)

        # Build opening context for AI
        opening_context = self._build_tavern_context(tavern, tavern_location)

        return self.state, opening_context

    def _generate_dungeon_start(self) -> tuple[WorldState, dict]:
        """Generate starting at a dungeon entrance."""
        # Generate dungeon
        dungeon = self.dungeon_gen.generate()

        # Create location entry
        dungeon_location = Location(
            id=f"dungeon_{uuid4().hex[:8]}",
            name=dungeon.name,
            location_type="dungeon",
            description=dungeon.description(),
            data=dungeon.storyteller_context(),
            visited=True,
            known=True,
        )

        self.state.add_location(dungeon_location)
        self.state.current_location_id = dungeon_location.id

        # Add quest hook
        self.state.active_quests.append({
            "name": f"Clear {dungeon.name}",
            "description": dungeon.hook,
            "location": dungeon_location.id,
            "status": "active",
        })

        opening_context = {
            "setting": "dungeon_entrance",
            "location": dungeon.name,
            "description": f"You stand before {dungeon.name}. {dungeon.hook}",
            "dungeon": dungeon.storyteller_context(),
            "current_room": dungeon.rooms[0].storyteller_context() if dungeon.rooms else None,
        }

        return self.state, opening_context

    def _generate_nearby_locations(self, from_location: Location, count: int = 3):
        """Generate nearby locations that the player has heard about."""
        location_types = ["dungeon", "town", "wilderness", "shop"]

        for _ in range(count):
            loc_type = self.rng.choice(location_types)
            new_location = self._generate_location_stub(loc_type)
            new_location.known = True
            new_location.visited = False
            new_location.connections.append(from_location.id)
            from_location.connections.append(new_location.id)
            self.state.add_location(new_location)

    def _generate_location_stub(self, location_type: str) -> Location:
        """Generate a location stub (minimal info until visited)."""
        if location_type == "dungeon":
            name = self.dungeon_gen._generate_dungeon_name(
                self.rng.choice(["crypt", "cave", "ruins", "temple", "lair"])
            )
            desc = "A dangerous location rumored to hold treasure."
        elif location_type == "town":
            name = self.name_gen.place_name().full_name
            desc = "A nearby settlement."
        elif location_type == "wilderness":
            name = self.name_gen.place_name().full_name
            desc = "Wild lands beyond the roads."
        elif location_type == "shop":
            name = f"{self.name_gen.first_name()}'s Shop"
            desc = "A merchant's establishment."
        else:
            name = self.name_gen.place_name().full_name
            desc = "A location of interest."

        return Location(
            id=f"{location_type}_{uuid4().hex[:8]}",
            name=name,
            location_type=location_type,
            description=desc,
        )

    def generate_location(
        self,
        location_type: LocationType,
        connected_to: str | None = None,
    ) -> Location:
        """
        Generate a full location on demand (when player travels there).

        Args:
            location_type: Type of location to generate
            connected_to: ID of location this connects to

        Returns:
            The newly generated Location
        """
        if location_type == "tavern":
            tavern = self.tavern_gen.generate()
            location = Location(
                id=f"tavern_{uuid4().hex[:8]}",
                name=tavern.name,
                location_type="tavern",
                description=tavern.description(),
                data=tavern.storyteller_context(),
            )
            # Register NPCs
            for npc in tavern.staff + tavern.patrons:
                self.state.add_npc(npc, location.id)
            self.state.rumors.extend(tavern.rumors)

        elif location_type == "dungeon":
            dungeon = self.dungeon_gen.generate()
            location = Location(
                id=f"dungeon_{uuid4().hex[:8]}",
                name=dungeon.name,
                location_type="dungeon",
                description=dungeon.description(),
                data=dungeon.storyteller_context(),
            )
            # Add quest
            self.state.active_quests.append({
                "name": f"Clear {dungeon.name}",
                "description": dungeon.hook,
                "location": location.id,
                "status": "active",
            })

        else:
            # Generic location
            location = self._generate_location_stub(location_type)
            location.visited = True

        # Connect to specified location
        if connected_to and connected_to in self.state.locations:
            location.connections.append(connected_to)
            self.state.locations[connected_to].connections.append(location.id)

        location.visited = True
        self.state.add_location(location)

        return location

    def move_to_location(self, location_id: str) -> dict:
        """
        Move player to a different location.

        Returns context for AI about the new location.
        """
        if location_id not in self.state.locations:
            return {"error": f"Unknown location: {location_id}"}

        location = self.state.locations[location_id]

        # Generate full content if not visited
        if not location.visited and not location.data:
            # Replace stub with full generation
            full_location = self.generate_location(
                location.location_type,
                connected_to=self.state.current_location_id
            )
            # Update the existing entry
            location.data = full_location.data
            location.description = full_location.description

        location.visited = True
        self.state.current_location_id = location_id

        return location.storyteller_context()

    def _build_tavern_context(self, tavern: Tavern, location: Location) -> dict:
        """Build rich context for AI from tavern data."""
        # Identify the most interesting patron (highest hook potential)
        interesting_patron = None
        for patron in tavern.patrons:
            if patron.hook and "nervous" in patron.personality_traits:
                interesting_patron = patron
                break
        if not interesting_patron and tavern.patrons:
            interesting_patron = tavern.patrons[0]

        # Get bartender
        bartender = next((s for s in tavern.staff if s.occupation == "bartender"), None)

        # Build structured context
        return {
            "setting": "fantasy_tavern",
            "location": tavern.name,
            "type": tavern.tavern_type,
            "mood": tavern.mood,

            # Prose description for narrative
            "description": tavern.description(),

            # Key characters
            "bartender": bartender.storyteller_context() if bartender else None,
            "featured_patron": interesting_patron.storyteller_context() if interesting_patron else None,

            # All characters (for reference)
            "staff": [s.storyteller_context() for s in tavern.staff],
            "patrons": [p.storyteller_context() for p in tavern.patrons],

            # Atmosphere
            "atmosphere": {
                "sounds": tavern.sounds,
                "smells": tavern.smells,
                "sights": tavern.sights,
            },

            # Plot hooks
            "rumors": tavern.rumors[:2],  # Give AI 2 rumors to work with

            # Connected locations (for AI to mention)
            "nearby_places": [
                self.state.locations[lid].name
                for lid in location.connections
                if lid in self.state.locations
            ],
        }

    def get_storyteller_context(self) -> dict:
        """
        Get complete world context for the AI storyteller.

        This is the main interface for providing world state to the AI.
        """
        current = self.state.current_location()
        if not current:
            return {"error": "No current location"}

        context = {
            "world_seed": self.state.seed,
            "current_location": current.storyteller_context(),
            "known_npcs": [npc.short_description() for npc in self.state.npcs.values()],
            "active_rumors": self.state.rumors[:3],
            "active_quests": self.state.active_quests,
            "nearby_locations": [
                {"name": self.state.locations[lid].name, "type": self.state.locations[lid].location_type}
                for lid in current.connections
                if lid in self.state.locations
            ],
        }

        # Add location-specific context
        if current.location_type == "tavern" and current.data:
            context["tavern_details"] = current.data

        return context

    def record_npc_interaction(self, npc_name: str, interaction_type: str):
        """Record that player interacted with an NPC."""
        if npc_name in self.state.npcs:
            npc = self.state.npcs[npc_name]
            # Could track interaction history, relationship changes, etc.
            pass

    def discover_secret(self, secret: str):
        """Record that player discovered a secret."""
        if secret not in self.state.discovered_secrets:
            self.state.discovered_secrets.append(secret)


# Convenience functions
def create_world(seed: int | None = None, setting: str = "fantasy_tavern") -> tuple[WorldManager, dict]:
    """Create a new world and return manager + opening context."""
    manager = WorldManager(seed)
    state, context = manager.generate_starting_world(setting)
    return manager, context


if __name__ == "__main__":
    # Demo
    print("=== World Manager Demo ===\n")

    manager, opening = create_world(seed=42)

    print(f"World Seed: {manager.state.seed}")
    print(f"Starting Location: {opening['location']}")
    print(f"\n{opening['description']}")

    print("\n--- Key NPCs ---")
    if opening.get("bartender"):
        print(f"Bartender: {opening['bartender']['name']}")
    if opening.get("featured_patron"):
        print(f"Interesting Patron: {opening['featured_patron']['name']}")
        print(f"  Hook: {opening['featured_patron'].get('hook', 'None')}")

    print("\n--- Rumors ---")
    for rumor in opening.get("rumors", []):
        print(f"  • {rumor}")

    print("\n--- Nearby Locations ---")
    for place in opening.get("nearby_places", []):
        print(f"  • {place}")

    print("\n--- Full World State ---")
    print(f"Total Locations: {len(manager.state.locations)}")
    print(f"Total NPCs: {len(manager.state.npcs)}")
    print(f"Active Quests: {len(manager.state.active_quests)}")
