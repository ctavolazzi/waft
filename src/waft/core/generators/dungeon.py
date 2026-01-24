"""
Dungeon Generator - Five Room Dungeon Structure
===============================================

Generates dungeon adventures using the classic Five Room Dungeon pattern:
1. Entrance/Guardian - Initial challenge to enter
2. Puzzle/Roleplay Challenge - Non-combat challenge
3. Trick/Setback - Red herring or complication
4. Climax/Boss - Main encounter
5. Reward/Revelation - Treasure and story hooks
"""

import random
from dataclasses import dataclass, field
from enum import Enum

from .names import NameGenerator


class DungeonTheme(Enum):
    CRYPT = "crypt"
    CAVE = "cave"
    RUINS = "ruins"
    TEMPLE = "temple"
    LAIR = "lair"
    MINE = "mine"
    SEWER = "sewer"
    TOWER = "tower"


# Room templates for each stage
ENTRANCE_GUARDIANS = {
    "crypt": [
        ("Skeletal Sentinels", "Two animated skeletons stand guard at the iron doors, ancient weapons raised."),
        ("Warded Gate", "The entrance is sealed with glowing runes. A riddle is carved above the door."),
        ("Undead Gatekeeper", "A ghoul in tattered robes demands to know your business with the dead."),
    ],
    "cave": [
        ("Giant Spider Web", "The entrance is choked with massive webs. Something large scuttles in the darkness."),
        ("Territorial Beast", "A dire wolf guards the cave mouth, its pups visible behind it."),
        ("Goblin Ambush", "Hidden goblins rain arrows from murder holes above the entrance."),
    ],
    "ruins": [
        ("Crumbling Entrance", "The ancient doorway is unstable. Dislodging the wrong stone could collapse it."),
        ("Stone Golem", "A moss-covered guardian activates as you approach, grinding to life."),
        ("Magical Barrier", "An invisible force prevents entry. Ancient text describes the password."),
    ],
    "temple": [
        ("Zealot Guards", "Robed cultists demand proof of faith before allowing entry."),
        ("Divine Test", "A statue demands an offering before the doors will open."),
        ("Trapped Threshold", "The floor tiles are pressure plates - step wrong and face divine wrath."),
    ],
    "lair": [
        ("Monstrous Guardian", "The creature's pet guards the entrance - a twisted beast of fang and claw."),
        ("Warning Display", "Impaled corpses and warning signs surround the entrance. Something wants privacy."),
        ("Patrol Return", "You must time your entry to avoid the returning scouts."),
    ],
    "mine": [
        ("Collapsed Entrance", "The mine entrance is partially collapsed. You'll need to dig or find another way."),
        ("Mining Equipment", "A rickety elevator is the only way down. Someone cut the safety rope."),
        ("Gas Warning", "Strange fumes emanate from below. You'll need protection or speed."),
    ],
    "sewer": [
        ("Locked Grate", "A heavy iron grate bars the way. You can hear things moving below."),
        ("Slime Guardian", "An ooze creature blocks the passage, dissolving anything that touches it."),
        ("Thieves' Guild Mark", "A hidden symbol warns this is guild territory. Enter uninvited at your peril."),
    ],
    "tower": [
        ("Arcane Lock", "The tower door is sealed with complex magic. A puzzle mechanism awaits."),
        ("Clockwork Sentinel", "A mechanical guardian patrols the tower base in predictable patterns."),
        ("Magical Stairs", "The stairs only appear for those who know the trigger phrase."),
    ],
}

PUZZLES = [
    ("Tile Puzzle", "The floor is covered in colored tiles. A mural on the wall suggests the safe path."),
    ("Pressure Plates", "Four pressure plates must be activated in the correct order shown by wall carvings."),
    ("Mirror Maze", "A room of mirrors - one reflection doesn't match. Find the false mirror."),
    ("Lever Sequence", "Six levers line the wall. A poem hints at the correct sequence."),
    ("Symbol Matching", "Rotating discs with symbols must align to match the constellation overhead."),
    ("Weight Puzzle", "Place stones on scales to perfectly balance them and unlock the door."),
    ("Elemental Challenge", "Four braziers must be lit in the order of the seasons."),
    ("Riddle Door", "A face carved in stone asks three riddles. Answer wrong and face the consequence."),
    ("Blood Lock", "The lock requires a willing sacrifice of blood - but how much?"),
    ("Musical Puzzle", "Chimes must be struck in a sequence. The answer is in an old song."),
]

TRICKS_SETBACKS = [
    ("False Treasure", "A chest full of gold - actually copper covered in gold paint. Triggers alarm when taken."),
    ("Shapechanger", "An ally NPC reveals themselves to be a doppelganger working for the boss."),
    ("Collapsing Room", "The ceiling begins to collapse. You must choose what to save - treasure or shortcut."),
    ("Prisoner's Dilemma", "Two prisoners - one tells only truth, one only lies. One knows the safe path."),
    ("Cursed Item", "A powerful magical item that seems helpful but carries a terrible curse."),
    ("Illusory Path", "The obvious path forward is an illusion hiding a pit. The real path is hidden."),
    ("Betrayal", "A former ally appears, now working for the enemy. They know your weaknesses."),
    ("Time Limit", "A mechanism activates. You now have limited time before the dungeon seals forever."),
    ("Split Party", "A trap separates the group. Each half faces different challenges."),
    ("Moral Choice", "Save the captives and alert the boss, or let them die to maintain surprise."),
]

BOSSES = {
    "crypt": [
        ("Lich", "An ancient wizard who traded their soul for immortality. Commands legions of undead."),
        ("Vampire Lord", "A noble turned monster, surrounded by thralls and dark power."),
        ("Death Knight", "A fallen paladin cursed to eternal unlife, still clad in corrupted holy armor."),
    ],
    "cave": [
        ("Dragon", "A young dragon has claimed this cave. Its hoard glitters behind it."),
        ("Giant Spider Queen", "A massive spider surrounded by her brood. Webs everywhere."),
        ("Troll King", "An unusually intelligent troll leads a small clan. Fire is your friend."),
    ],
    "ruins": [
        ("Awakened Guardian", "The ancient protector has been corrupted, now destroying what it swore to defend."),
        ("Demon Prince", "Summoned long ago, this demon has been bound here - but the bindings weaken."),
        ("Mad Wizard's Ghost", "The wizard who built this place refuses to let it fall to intruders."),
    ],
    "temple": [
        ("High Priest", "The corrupted religious leader wields divine magic twisted to dark purpose."),
        ("Summoned God-Fragment", "A piece of a dark god manifests, terrible and hungry."),
        ("Fallen Angel", "Once a celestial being, now twisted by corruption and bound to the temple."),
    ],
    "lair": [
        ("Beast Lord", "The intelligent monster who rules here. Cunning, powerful, and territorial."),
        ("Aberrant Horror", "Something from beyond that defies natural law. Madness incarnate."),
        ("Warlord", "A powerful warrior who has united monsters under their banner."),
    ],
    "mine": [
        ("Earth Elemental", "Awakened by mining too deep, this being of living stone is furious."),
        ("Dwarf Lich", "A dwarven wizard who refused to abandon their mine, even in death."),
        ("Purple Worm", "The tunnels lead to the lair of a massive burrowing predator."),
    ],
    "sewer": [
        ("Rat King", "A horrifying amalgamation of rats fused into one intelligent, malevolent being."),
        ("Otyugh Alpha", "A massive garbage-eater that has grown far too large and hungry."),
        ("Thieves' Guild Master", "The criminal mastermind uses the sewers as their domain."),
    ],
    "tower": [
        ("Archmage", "The tower's master wields terrible magic and knows you're coming."),
        ("Beholder", "A floating orb of madness and eye-beams has claimed the tower's apex."),
        ("Demon-Possessed Scholar", "Once a peaceful researcher, now a vessel for something terrible."),
    ],
}

REWARDS = [
    ("Ancient Weapon", "A legendary blade lost to history, still sharp after all these years."),
    ("Spellbook", "Contains spells thought lost to time. Power at a price."),
    ("Treasure Hoard", "Gold, gems, and artifacts - enough to live comfortably for years."),
    ("Magical Artifact", "An item of significant power, with its own agenda."),
    ("Knowledge", "Maps, documents, or memories revealing secrets worth more than gold."),
    ("Ally", "A powerful being now owes you a favor, or a captive joins your cause."),
    ("Property", "The dungeon itself - cleared of threats, it could be a base of operations."),
    ("Connection", "Your deeds here have caught the attention of powerful people."),
]

REVELATIONS = [
    "The boss was merely a servant of a greater evil.",
    "A clue points to an even larger dungeon complex nearby.",
    "The treasure includes a map to somewhere legendary.",
    "A dying enemy reveals a conspiracy reaching into civilized lands.",
    "An ancient prophecy names one of you as chosen for something.",
    "The dungeon was just one piece of a larger puzzle.",
    "Someone you trusted arranged for you to come here - but why?",
    "The real enemy got away, taking something important.",
]


@dataclass
class Room:
    """A single dungeon room."""
    name: str
    room_type: str  # entrance, puzzle, setback, boss, reward
    description: str
    challenge: str | None = None
    enemies: list[str] = field(default_factory=list)
    loot: list[str] = field(default_factory=list)
    secrets: list[str] = field(default_factory=list)
    connections: list[str] = field(default_factory=list)  # Names of connected rooms

    def storyteller_context(self) -> dict:
        return {
            "name": self.name,
            "type": self.room_type,
            "description": self.description,
            "challenge": self.challenge,
            "enemies": self.enemies,
            "loot": self.loot,
            "secrets": self.secrets,
        }


@dataclass
class Dungeon:
    """A complete five-room dungeon."""
    name: str
    theme: str
    hook: str  # Why adventurers would come here
    rooms: list[Room] = field(default_factory=list)
    revelation: str = ""  # Story hook after completion

    def description(self) -> str:
        """Generate overview description."""
        return f"**{self.name}** - {self.theme.title()} ({len(self.rooms)} rooms)\n\n*{self.hook}*"

    def storyteller_context(self) -> dict:
        """Context for AI storyteller."""
        return {
            "name": self.name,
            "theme": self.theme,
            "hook": self.hook,
            "rooms": [r.storyteller_context() for r in self.rooms],
            "revelation": self.revelation,
            "structure": "Five Room Dungeon: Entrance → Puzzle → Setback → Boss → Reward",
        }


class DungeonGenerator:
    """Generates five-room dungeons."""

    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)
        self.name_gen = NameGenerator(seed)

    def generate(self, theme: str | DungeonTheme | None = None, hook: str | None = None) -> Dungeon:
        """Generate a complete five-room dungeon."""

        # Choose theme
        if theme is None:
            theme = self.rng.choice(list(DungeonTheme)).value
        elif isinstance(theme, DungeonTheme):
            theme = theme.value

        # Generate name
        name = self._generate_dungeon_name(theme)

        # Generate hook if not provided
        if hook is None:
            hook = self._generate_hook(theme)

        # Generate the five rooms
        rooms = [
            self._generate_entrance(theme),
            self._generate_puzzle(),
            self._generate_setback(),
            self._generate_boss(theme),
            self._generate_reward(),
        ]

        # Connect rooms
        for i, room in enumerate(rooms[:-1]):
            room.connections.append(rooms[i + 1].name)

        # Generate revelation
        revelation = self.rng.choice(REVELATIONS)

        return Dungeon(
            name=name,
            theme=theme,
            hook=hook,
            rooms=rooms,
            revelation=revelation,
        )

    def _generate_dungeon_name(self, theme: str) -> str:
        """Generate an appropriate dungeon name."""
        prefixes = {
            "crypt": ["The Forgotten", "The Haunted", "The Cursed", "The Ancient"],
            "cave": ["The Deep", "The Dark", "The Echoing", "The Twisted"],
            "ruins": ["The Lost", "The Fallen", "The Sunken", "The Crumbling"],
            "temple": ["The Defiled", "The Hidden", "The Forbidden", "The Sacred"],
            "lair": ["The Dread", "The Fetid", "The Terrible", "The Monster's"],
            "mine": ["The Abandoned", "The Collapsed", "The Bleeding", "The Deep"],
            "sewer": ["The Forgotten", "The Flooded", "The Reeking", "The Underground"],
            "tower": ["The Twisted", "The Dark", "The Arcane", "The Obsidian"],
        }

        suffixes = {
            "crypt": ["Crypt", "Tomb", "Mausoleum", "Catacomb"],
            "cave": ["Caverns", "Caves", "Depths", "Hollows"],
            "ruins": ["Ruins", "Citadel", "Fortress", "Palace"],
            "temple": ["Temple", "Sanctum", "Shrine", "Cathedral"],
            "lair": ["Lair", "Den", "Nest", "Domain"],
            "mine": ["Mine", "Depths", "Pit", "Excavation"],
            "sewer": ["Sewers", "Undercity", "Depths", "Warrens"],
            "tower": ["Tower", "Spire", "Pinnacle", "Citadel"],
        }

        prefix = self.rng.choice(prefixes.get(theme, ["The Dark"]))
        suffix = self.rng.choice(suffixes.get(theme, ["Dungeon"]))

        # Sometimes add a name
        if self.rng.random() < 0.4:
            name = self.name_gen.first_name(race="human")
            return f"{name}'s {suffix}"

        return f"{prefix} {suffix}"

    def _generate_hook(self, theme: str) -> str:
        """Generate why adventurers would explore this dungeon."""
        hooks = {
            "crypt": [
                "A noble family needs ancestral remains recovered.",
                "Undead have been emerging and attacking the nearby village.",
                "A legendary artifact was buried with an ancient king.",
            ],
            "cave": [
                "Travelers have been disappearing on the mountain road.",
                "Rare minerals needed for a cure can only be found here.",
                "A monster has been stealing livestock and retreating here.",
            ],
            "ruins": [
                "A scholar believes lost knowledge lies within.",
                "Bandits are using the ruins as a base.",
                "Strange lights have been seen, and no one who investigates returns.",
            ],
            "temple": [
                "Cultists are preparing a dark ritual.",
                "A holy artifact must be recovered before it's corrupted.",
                "Innocents are being held for sacrifice.",
            ],
            "lair": [
                "The monster must be slain before it attacks the town.",
                "A bounty has been placed on the creature's head.",
                "It took something precious that must be recovered.",
            ],
            "mine": [
                "Miners broke through to something they shouldn't have.",
                "Valuable ore is needed urgently, but the mine is overrun.",
                "Workers are trapped below and need rescue.",
            ],
            "sewer": [
                "People have been disappearing from the streets above.",
                "The thieves' guild has information you need.",
                "Something is poisoning the city's water supply.",
            ],
            "tower": [
                "A wizard has been kidnapping people for experiments.",
                "The tower appeared overnight - that's not normal.",
                "An artifact of terrible power is being created within.",
            ],
        }
        return self.rng.choice(hooks.get(theme, ["Adventure awaits."]))

    def _generate_entrance(self, theme: str) -> Room:
        """Generate the entrance/guardian room."""
        guardians = ENTRANCE_GUARDIANS.get(theme, ENTRANCE_GUARDIANS["cave"])
        name, desc = self.rng.choice(guardians)

        return Room(
            name="The Entrance",
            room_type="entrance",
            description=desc,
            challenge=name,
            enemies=["Guardian"] if "Guardian" in name or "Sentinel" in name else [],
        )

    def _generate_puzzle(self) -> Room:
        """Generate the puzzle/roleplay room."""
        name, desc = self.rng.choice(PUZZLES)

        return Room(
            name="The Challenge",
            room_type="puzzle",
            description=desc,
            challenge=name,
            secrets=["Hint hidden in the room's decorations"],
        )

    def _generate_setback(self) -> Room:
        """Generate the trick/setback room."""
        name, desc = self.rng.choice(TRICKS_SETBACKS)

        return Room(
            name="The Twist",
            room_type="setback",
            description=desc,
            challenge=name,
            secrets=["Careful observation reveals the truth"],
        )

    def _generate_boss(self, theme: str) -> Room:
        """Generate the climax/boss room."""
        bosses = BOSSES.get(theme, BOSSES["cave"])
        name, desc = self.rng.choice(bosses)

        return Room(
            name="The Confrontation",
            room_type="boss",
            description=f"**{name}**: {desc}",
            challenge=f"Defeat the {name}",
            enemies=[name],
            loot=["Boss's personal treasure"],
        )

    def _generate_reward(self) -> Room:
        """Generate the reward/revelation room."""
        reward_name, reward_desc = self.rng.choice(REWARDS)

        return Room(
            name="The Reward",
            room_type="reward",
            description=f"Beyond the defeated guardian lies the prize. {reward_desc}",
            loot=[reward_name],
            secrets=["Something here points to a larger mystery..."],
        )


# Convenience function
def generate_dungeon(theme: str | None = None, seed: int | None = None) -> Dungeon:
    """Quick dungeon generation."""
    return DungeonGenerator(seed).generate(theme=theme)


if __name__ == "__main__":
    # Demo
    gen = DungeonGenerator(seed=42)
    print("=== Dungeon Generator Demo ===\n")

    dungeon = gen.generate(theme="crypt")
    print(dungeon.description())
    print()

    for i, room in enumerate(dungeon.rooms, 1):
        print(f"Room {i}: {room.name} ({room.room_type})")
        print(f"  {room.description[:100]}...")
        if room.challenge:
            print(f"  Challenge: {room.challenge}")
        if room.enemies:
            print(f"  Enemies: {', '.join(room.enemies)}")
        if room.loot:
            print(f"  Loot: {', '.join(room.loot)}")
        print()

    print(f"Revelation: {dungeon.revelation}")
