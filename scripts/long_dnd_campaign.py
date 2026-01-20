#!/usr/bin/env python3
"""
Extended Long DnD Campaign Generator
=====================================

A comprehensive self-playing DnD campaign that generates an epic, LONG adventure
with many encounters, detailed story chapters, and rich narrative content.

Generates a complete campaign book as a PDF.
"""

import json
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

from src.waft.being import Being, BeingSystem
from src.waft.evolution.pdf_generator import PDFGenerator

console = Console()


class PartyMember:
    """Represents a party member (Being)."""

    def __init__(self, being: Being, name: str, class_type: str, race: str):
        self.being = being
        self.name = name
        self.class_type = class_type
        self.race = race
        self.hp = 100
        self.max_hp = 100
        self.level = 1
        self.experience = 0
        self.stats = {
            "strength": random.randint(12, 18),
            "dexterity": random.randint(12, 18),
            "constitution": random.randint(12, 18),
            "intelligence": random.randint(12, 18),
            "wisdom": random.randint(12, 18),
            "charisma": random.randint(12, 18),
        }

    def take_damage(self, damage: int) -> bool:
        """Take damage, return True if alive."""
        self.hp -= damage
        return self.hp > 0

    def heal(self, amount: int):
        """Heal the character."""
        self.hp = min(self.hp + amount, self.max_hp)

    def gain_experience(self, xp: int):
        """Gain experience and level up if needed."""
        self.experience += xp
        if self.experience >= self.level * 100:
            self.level += 1
            self.max_hp += 10
            self.hp = self.max_hp
            return True
        return False


class ExtendedCampaign:
    """Extended self-playing DnD campaign system with LONG content."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)
        self.project_path = project_root
        self.being_system = BeingSystem(project_path=self.project_path)
        self.party: list[PartyMember] = []
        self.campaign_log: list[dict[str, Any]] = []
        self.chapters: list[dict[str, Any]] = []
        self.current_location = "Tavern"
        self.quest_progress = 0
        self.final_boss_defeated = False
        self.total_encounters = 0

    def spawn_party(self) -> list[PartyMember]:
        """Spawn party members as Beings."""
        console.print("\n[bold cyan]🎲 SPAWNING THE PARTY 🎲[/bold cyan]\n")

        party_configs = [
            {
                "name": "Thorin Ironforge",
                "class": "Fighter",
                "race": "Dwarf",
                "skills": {"combat": 30.0, "strength": 25.0},
            },
            {
                "name": "Lyra Moonwhisper",
                "class": "Wizard",
                "race": "Elf",
                "skills": {"magic": 28.0, "investigation": 22.0},
            },
            {
                "name": "Rogar Swiftfoot",
                "class": "Rogue",
                "race": "Halfling",
                "skills": {"stealth": 32.0, "dexterity": 27.0},
            },
            {
                "name": "Aria Brightshield",
                "class": "Cleric",
                "race": "Human",
                "skills": {"healing": 30.0, "wisdom": 24.0},
            },
        ]

        party = []
        for i, config in enumerate(party_configs):
            console.print(f"[yellow]→[/yellow] Spawning {config['name']}...")

            being = self.being_system.spawn_being(
                reality_id="extended_dnd_campaign_reality",
                parent_being_id=None,
                initial_skills=config["skills"],
            )

            member = PartyMember(being, config["name"], config["class"], config["race"])
            party.append(member)

            being.record_memory(
                f"Joined adventuring party as {config['class']}",
                "experience",
                {
                    "party_name": "The Eternal Guardians",
                    "class": config["class"],
                    "race": config["race"],
                },
            )

            console.print(
                f"   [green]✓[/green] {config['name']} ({config['race']} {config['class']}) spawned: {being.being_id}"
            )

        self.party = party
        console.print(f"\n[bold green]✅ Party of {len(party)} members ready![/bold green]\n")
        return party

    def create_tavern_scene(self) -> dict[str, Any]:
        """Create the opening tavern scene."""
        console.print("\n[bold cyan]🍺 THE TAVERN - OPENING SCENE 🍺[/bold cyan]\n")

        party_names = ", ".join([m.name for m in self.party])

        scene = {
            "title": "The Rusty Tankard Tavern",
            "content": f"""
# The Rusty Tankard Tavern

The warm glow of the hearth casts dancing shadows across the worn wooden tables of The Rusty Tankard. 
The air is thick with the smell of ale, roasted meat, and the murmur of travelers sharing tales.

{party_names} sit together at a corner table, their gear stacked beside them. The tavern is alive with 
activity - merchants discussing trade routes, guards off duty sharing war stories, and mysterious 
figures in dark corners watching everything.

Suddenly, the tavern door bursts open. A figure stumbles in, covered in mud and breathing heavily. 
It's a messenger, and he's clearly been through something terrible.

"The road to Blackmoor Keep is no longer safe!" he gasps, collapsing at the bar. "Something... 
something dark has taken hold of the old fortress. The villagers are terrified. We need heroes!"

The tavern falls silent. All eyes turn to your table.

The messenger looks directly at you. "Please... you look like capable adventurers. Will you help us?"

This is where your story begins.

## The Quest

The messenger explains that Blackmoor Keep, once a bastion of light and order, has fallen to darkness. 
Strange creatures roam the surrounding lands, and the keep itself has become a place of nightmares. 
The local villages are in danger, and only brave adventurers can restore the light.

The party accepts the quest, knowing that this will be a long and dangerous journey.
            """,
            "read_aloud": """
The messenger's eyes are wide with fear. "The Keep has been overrun by shadows. 
Something ancient has awakened. We need brave souls to face whatever darkness lies within."
            """,
        }

        self.campaign_log.append(
            {
                "timestamp": datetime.now().isoformat(),
                "event": "tavern_scene",
                "location": "The Rusty Tankard",
                "description": "Party receives quest",
            }
        )

        console.print(
            Panel(scene["content"], title="[bold]The Rusty Tankard[/bold]", border_style="yellow")
        )
        return scene

    def generate_detailed_encounter(
        self, encounter_name: str, difficulty: str = "medium", description: str = None
    ) -> dict[str, Any]:
        """Generate a detailed combat encounter with rich narrative."""
        console.print(f"\n[bold red]⚔️  ENCOUNTER: {encounter_name} ⚔️[/bold red]\n")

        difficulty_multiplier = {"easy": 0.8, "medium": 1.0, "hard": 1.5, "boss": 3.0, "epic": 5.0}[
            difficulty
        ]

        # Simulate combat with more detail
        enemy_hp = int(100 * difficulty_multiplier)
        party_damage = sum([random.randint(15, 30) for _ in self.party])
        rounds = max(1, int(enemy_hp / party_damage))

        # Party takes damage
        damage_taken = {}
        for member in self.party:
            damage = random.randint(5, 15) * int(difficulty_multiplier)
            member.take_damage(damage)
            damage_taken[member.name] = damage
            if member.hp <= 0:
                member.hp = 1

        # Gain experience
        xp_gain = int(50 * difficulty_multiplier)
        level_ups = []
        for member in self.party:
            leveled = member.gain_experience(xp_gain)
            if leveled:
                level_ups.append(member.name)
                console.print(f"   [green]✨ {member.name} leveled up to {member.level}![/green]")

        # Generate detailed encounter description
        if not description:
            description = f"""
The party encounters {encounter_name} in a fierce battle. The combat is intense, with spells flying, 
swords clashing, and the party working together to overcome their foe. After {rounds} rounds of 
determined fighting, the party emerges victorious.
            """

        encounter = {
            "title": encounter_name,
            "content": f"""
## {encounter_name}

{description}

### Combat Details

- **Rounds of Combat**: {rounds}
- **Party Damage Taken**: {sum(damage_taken.values())} total
- **Experience Gained**: {xp_gain} XP per party member
- **Current Party HP**: {sum([m.hp for m in self.party])}/{sum([m.max_hp for m in self.party])}
            """,
            "read_aloud": f"""
The battle is intense. Steel clashes, spells fly, and the party fights as one. 
After {rounds} rounds of combat, {encounter_name} falls, defeated by the heroes' resolve.
            """,
            "difficulty": difficulty,
            "rounds": rounds,
            "xp_gained": xp_gain,
            "damage_taken": damage_taken,
            "level_ups": level_ups,
        }

        self.total_encounters += 1
        self.campaign_log.append(
            {
                "timestamp": datetime.now().isoformat(),
                "event": "encounter",
                "encounter_name": encounter_name,
                "difficulty": difficulty,
                "rounds": rounds,
                "encounter_number": self.total_encounters,
            }
        )

        console.print(
            f"   [green]✓[/green] Encounter complete! Party HP: {sum([m.hp for m in self.party])}/{sum([m.max_hp for m in self.party])}"
        )
        return encounter

    def generate_story_chapter(
        self, chapter_num: int, title: str, encounters: list[dict[str, Any]], intro_text: str = None
    ) -> dict[str, Any]:
        """Generate a detailed story chapter with multiple encounters."""
        console.print(f"\n[bold cyan]📖 CHAPTER {chapter_num}: {title} 📖[/bold cyan]\n")

        if not intro_text:
            intro_text = f"The party continues their journey toward Blackmoor Keep. {title}"

        chapter_content = f"# Chapter {chapter_num}: {title}\n\n{intro_text}\n\n"
        chapter_read_aloud = []

        # Add encounters
        for i, encounter_data in enumerate(encounters):
            encounter_name = encounter_data.get("name", "Unknown Encounter")
            difficulty = encounter_data.get("difficulty", "medium")
            description = encounter_data.get("description")

            encounter = self.generate_detailed_encounter(encounter_name, difficulty, description)
            chapter_content += f"\n{encounter['content']}\n\n"
            chapter_read_aloud.append(encounter["read_aloud"])

        chapter = {
            "title": f"Chapter {chapter_num}: {title}",
            "content": chapter_content,
            "read_aloud": "\n\n".join(chapter_read_aloud),
            "encounters": [e.get("name") for e in encounters],
        }

        self.chapters.append(chapter)
        return chapter

    def create_final_boss_battle(self) -> dict[str, Any]:
        """Create the epic final boss battle."""
        console.print("\n[bold red]👹 FINAL BOSS BATTLE 👹[/bold red]\n")

        boss_name = "The Shadow Lord Malachar"

        # Epic boss battle
        boss_hp = 800
        party_damage = sum([random.randint(25, 45) for _ in self.party])
        rounds = max(8, int(boss_hp / party_damage))

        # Party takes significant damage
        for member in self.party:
            damage = random.randint(25, 40)
            member.take_damage(damage)
            if member.hp <= 0:
                member.hp = 1

        # Massive XP gain
        xp_gain = 1000
        level_ups = []
        for member in self.party:
            leveled = member.gain_experience(xp_gain)
            if leveled:
                level_ups.append(member.name)
                console.print(f"   [green]✨ {member.name} leveled up to {member.level}![/green]")

        battle = {
            "title": f"The Final Battle: {boss_name}",
            "content": f"""
# The Final Battle: {boss_name}

The party has reached the heart of Blackmoor Keep. Before them stands {boss_name}, 
a being of pure darkness that has corrupted the ancient fortress.

## The Confrontation

The chamber is vast, with ancient runes carved into the walls that now pulse with dark energy. 
{boss_name} stands at the center, surrounded by swirling shadows. The very air feels heavy with malice.

"The time has come," {boss_name} speaks, his voice echoing through the chamber. "You have proven 
yourselves worthy adversaries, but you cannot hope to defeat me. I am eternal. I am darkness itself."

The party knows this is the moment of truth. All their journey has led to this.

## The Battle

The battle is epic beyond measure. Spells of immense power clash with dark magic. Swords strike 
against shadowy armor. The very foundations of the keep shake with the force of combat.

After {rounds} grueling rounds, the party's determination and teamwork overcome the darkness. 
{boss_name} lets out a final, terrible scream as the light of the heroes' resolve banishes 
the shadow forever.

## Victory!

The keep is free. The darkness is defeated. The party has saved the realm.

### The Aftermath

The party stands victorious. They have:
- Defeated {boss_name}
- Cleansed Blackmoor Keep
- Saved the surrounding villages
- Gained {xp_gain} experience each
- Reached level {max([m.level for m in self.party])}

The adventure is complete, but new quests await...
            """,
            "read_aloud": f"""
The final blow strikes true. {boss_name} shrieks as darkness is banished from the keep. 
Light floods the chamber. The corruption is gone. You have won.
            """,
            "boss_name": boss_name,
            "rounds": rounds,
            "xp_gained": xp_gain,
            "victory": True,
        }

        self.final_boss_defeated = True
        self.campaign_log.append(
            {
                "timestamp": datetime.now().isoformat(),
                "event": "final_boss_defeated",
                "boss_name": boss_name,
                "victory": True,
            }
        )

        console.print(
            Panel(
                f"[bold green]VICTORY![/bold green]\n\n{boss_name} has been defeated!\n\nThe party has saved the realm!",
                title="[bold]🎉 CAMPAIGN COMPLETE 🎉[/bold]",
                border_style="green",
            )
        )

        return battle

    def run_extended_campaign(self):
        """Run the extended self-playing campaign with MANY encounters."""
        console.print("\n" + "=" * 80)
        console.print("[bold cyan]🎲 EXTENDED DND CAMPAIGN: EPIC ADVENTURE 🎲[/bold cyan]")
        console.print("=" * 80 + "\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console,
        ) as progress:
            # Phase 1: Spawn Party
            task1 = progress.add_task("[cyan]Spawning party...", total=4)
            self.spawn_party()
            progress.update(task1, completed=4)

            # Phase 2: Tavern Scene
            task2 = progress.add_task("[cyan]Creating tavern scene...", total=1)
            tavern_scene = self.create_tavern_scene()
            self.chapters.append(
                {
                    "title": "Prologue: The Rusty Tankard",
                    "content": tavern_scene["content"],
                    "read_aloud": tavern_scene["read_aloud"],
                }
            )
            progress.update(task2, completed=1)

            # Phase 3: Extended Journey Chapters (MANY MORE - EXTENDED FOR LENGTH)
            chapters_config = [
                {
                    "title": "The Road to Blackmoor",
                    "intro": "The party sets out from the tavern, their quest clear. The road to Blackmoor Keep is long and dangerous, but they are determined. The journey will test their resolve, their skills, and their bonds of friendship.",
                    "encounters": [
                        {
                            "name": "Goblin Ambush",
                            "difficulty": "easy",
                            "description": "A group of goblins ambushes the party from the underbrush. Quick thinking and combat skills are required. The goblins are poorly organized but numerous, making this a test of the party's ability to work together under pressure.",
                        },
                        {
                            "name": "Wolves of the Darkwood",
                            "difficulty": "medium",
                            "description": "A pack of dire wolves blocks the path. Their eyes glow with an unnatural hunger. These are no ordinary wolves - something has corrupted them, making them larger and more aggressive than normal. The party must fight or find a way to avoid them.",
                        },
                        {
                            "name": "Bandit Encounter",
                            "difficulty": "medium",
                            "description": "Highway bandits attempt to rob the party, but they are no match for skilled adventurers. However, the bandits reveal information about strange happenings near the keep, suggesting the darkness is spreading.",
                        },
                        {
                            "name": "Mysterious Traveler",
                            "difficulty": "easy",
                            "description": "A mysterious traveler provides information about the keep, but warns of great danger ahead. The traveler speaks of ancient evils and warns that the party may be walking into a trap. They offer cryptic advice before disappearing into the mist.",
                        },
                        {
                            "name": "The Abandoned Village",
                            "difficulty": "medium",
                            "description": "The party discovers an abandoned village. The buildings are empty, but signs of a hasty departure are everywhere. Something terrible happened here, and the party must investigate to understand what they're facing.",
                        },
                        {
                            "name": "Corrupted Wildlife",
                            "difficulty": "easy",
                            "description": "The party encounters animals that have been corrupted by the darkness. Birds with glowing red eyes, deer with twisted antlers, and other creatures attack with unnatural ferocity. The corruption is spreading.",
                        },
                    ],
                },
                {
                    "title": "The Darkwood Forest",
                    "intro": "The party enters the Darkwood Forest, a place of ancient magic and hidden dangers. The trees seem to watch them as they pass. The forest is alive with an ancient power, and not all of it is friendly. The deeper they go, the more the darkness seems to press in around them.",
                    "encounters": [
                        {
                            "name": "Spectral Apparitions",
                            "difficulty": "medium",
                            "description": "Ghostly figures appear, remnants of those who died in the forest long ago. These spirits are trapped between worlds, unable to find peace. They attack the party, driven by rage and sorrow. The party must fight them while trying to understand their tragic story.",
                        },
                        {
                            "name": "Giant Spiders",
                            "difficulty": "hard",
                            "description": "Massive spiders descend from the canopy, their webs blocking the path. These are no ordinary spiders - they're the size of horses, with venom that can paralyze. The party must cut through the webs and fight their way past these guardians of the forest.",
                        },
                        {
                            "name": "Ancient Treant",
                            "difficulty": "hard",
                            "description": "An ancient treant blocks the path, but can be reasoned with if approached correctly. The treant is thousands of years old and has seen the corruption spreading. It tests the party's intentions before allowing them to pass, offering wisdom about the darkness ahead.",
                        },
                        {
                            "name": "Forest Guardian",
                            "difficulty": "medium",
                            "description": "A guardian spirit tests the party's worthiness to pass through the sacred grove. The guardian is a powerful fey creature that protects the forest. It challenges the party to prove they are worthy of continuing their quest.",
                        },
                        {
                            "name": "The Lost Shrine",
                            "difficulty": "medium",
                            "description": "The party discovers an ancient shrine hidden in the forest. The shrine is dedicated to a forgotten deity, and it offers a moment of rest and healing. However, corrupted creatures have taken up residence, and the party must cleanse the shrine before they can benefit from its power.",
                        },
                        {
                            "name": "The Whispering Trees",
                            "difficulty": "easy",
                            "description": "The trees themselves seem to whisper warnings and threats. The party must navigate through a grove where the trees move and attack, their branches like whips. This is a test of the party's ability to work together and protect each other.",
                        },
                    ],
                },
                {
                    "title": "Approaching the Keep",
                    "intro": "The keep comes into view, its dark towers reaching toward a stormy sky. The air grows colder, and an unnatural silence falls. The very ground seems to reject life here, and the party can feel the weight of the darkness pressing down on them. This is where their true test begins.",
                    "encounters": [
                        {
                            "name": "Skeleton Warriors",
                            "difficulty": "medium",
                            "description": "Undead warriors rise from the ground, their bones clattering as they advance. These are the remains of the keep's former defenders, now animated by dark magic. They fight with the skill they had in life, making them dangerous opponents.",
                        },
                        {
                            "name": "Dark Cultists",
                            "difficulty": "hard",
                            "description": "Cultists performing dark rituals attempt to stop the party from reaching the keep. These cultists are fanatical followers of the Shadow Lord, and they will stop at nothing to prevent the party from reaching their master. They use dark magic and are willing to sacrifice themselves.",
                        },
                        {
                            "name": "Shadow Beasts",
                            "difficulty": "hard",
                            "description": "Creatures of pure shadow emerge from the darkness, their forms shifting and unnatural. These are not natural creatures - they are manifestations of the darkness itself. They are difficult to hit and can phase through solid objects, making them extremely dangerous.",
                        },
                        {
                            "name": "The Keep's Gate",
                            "difficulty": "medium",
                            "description": "The massive gate is guarded by corrupted sentinels, but the party finds a way through. The gate itself is a massive structure of dark stone, covered in runes that pulse with evil energy. The sentinels are powerful, but the party's determination sees them through.",
                        },
                        {
                            "name": "The Moat of Despair",
                            "difficulty": "medium",
                            "description": "Before reaching the gate, the party must cross a moat filled with dark, churning water. The water itself seems alive and hostile, and creatures lurk beneath the surface. The party must find a way across while fighting off attacks from both the water and the shore.",
                        },
                        {
                            "name": "The Outer Defenses",
                            "difficulty": "hard",
                            "description": "The keep's outer defenses are still active, with ballistae and other siege weapons firing at the party. They must dodge projectiles while fighting off the defenders. This is a test of the party's ability to work under pressure and coordinate their movements.",
                        },
                    ],
                },
                {
                    "title": "Within the Keep - The Outer Walls",
                    "intro": "The party enters the keep itself. The outer walls are filled with the remnants of the keep's former defenders, now corrupted by darkness. The halls echo with the sounds of battle and the moans of the undead. The party must navigate through this nightmare while fighting for their lives.",
                    "encounters": [
                        {
                            "name": "Corrupted Guards",
                            "difficulty": "medium",
                            "description": "The keep's former guards now serve the darkness, their eyes glowing with malevolent light. These guards remember their training and fight with military precision, but they are driven by dark magic that makes them relentless. The party must overcome their former allies.",
                        },
                        {
                            "name": "Undead Servants",
                            "difficulty": "easy",
                            "description": "Zombified servants shamble through the halls, attacking anything that moves. These are the keep's former staff, now mindless undead. They are slow but numerous, and they can overwhelm the party if they're not careful.",
                        },
                        {
                            "name": "The Keep's Lieutenant",
                            "difficulty": "hard",
                            "description": "A powerful lieutenant of the dark lord blocks the way forward, wielding dark magic. This lieutenant was once a paladin of light, but has been corrupted and now serves the Shadow Lord. They are a tragic figure, and the party must defeat them to continue.",
                        },
                        {
                            "name": "Ancient Traps",
                            "difficulty": "medium",
                            "description": "The keep is riddled with traps, both ancient and newly placed by the dark forces. The party must use their skills to detect and disarm these traps, or suffer the consequences. This is a test of the party's rogues and their ability to work together to avoid danger.",
                        },
                        {
                            "name": "The Armory",
                            "difficulty": "medium",
                            "description": "The party discovers the keep's armory, which contains weapons and armor that could help them. However, the armory is guarded by animated suits of armor that attack anyone who tries to take the equipment. The party must fight their way through to claim these valuable resources.",
                        },
                        {
                            "name": "The Barracks",
                            "difficulty": "hard",
                            "description": "The keep's barracks are filled with corrupted soldiers who were once the keep's defenders. These soldiers are organized and fight as a unit, making them extremely dangerous. The party must use strategy and teamwork to overcome this challenge.",
                        },
                    ],
                },
                {
                    "title": "The Inner Sanctum",
                    "intro": "The party reaches the inner sanctum of the keep. Here, the corruption is strongest, and the air itself seems to resist their presence. The very walls pulse with dark energy, and the party can feel the weight of the Shadow Lord's power pressing down on them. This is the heart of the darkness.",
                    "encounters": [
                        {
                            "name": "Shadow Wraiths",
                            "difficulty": "hard",
                            "description": "Powerful wraiths made of pure shadow attack from all sides. These wraiths are the souls of those who died in the keep, now bound to serve the Shadow Lord. They are difficult to hit and can drain the life force from their victims. The party must work together to defeat them.",
                        },
                        {
                            "name": "Corrupted Artifacts",
                            "difficulty": "medium",
                            "description": "Ancient artifacts have been corrupted and now attack the party with dark magic. These artifacts were once holy relics, but the darkness has twisted them into weapons of evil. The party must destroy them to continue, but doing so releases powerful dark magic.",
                        },
                        {
                            "name": "The Dark Council",
                            "difficulty": "hard",
                            "description": "A council of dark mages attempts to stop the party before they reach the final chamber. These mages are powerful spellcasters who have willingly embraced the darkness. They work together, casting spells that complement each other and create devastating combinations.",
                        },
                        {
                            "name": "The Guardian Chamber",
                            "difficulty": "boss",
                            "description": "A massive guardian creature blocks the path to the final boss, its form shifting between reality and shadow. This guardian is a creation of the Shadow Lord, designed to be the ultimate defense. It is nearly invulnerable and attacks with devastating power. The party must use all their skills and resources to defeat it.",
                        },
                        {
                            "name": "The Corrupted Library",
                            "difficulty": "medium",
                            "description": "The party discovers the keep's library, which contains ancient knowledge about the Shadow Lord and how to defeat him. However, the books themselves have been corrupted and attack the party. The party must fight their way through to gain this crucial information.",
                        },
                        {
                            "name": "The Hall of Mirrors",
                            "difficulty": "hard",
                            "description": "The party enters a hall filled with mirrors that show twisted reflections of themselves. These reflections are not just images - they are real, and they attack the party. The party must distinguish between reality and illusion while fighting for their lives.",
                        },
                    ],
                },
                {
                    "title": "The Depths",
                    "intro": "The party descends into the deepest levels of the keep, where the source of the darkness lies. The very walls seem to pulse with evil. The air is thick with malevolence, and the party can feel the Shadow Lord's presence growing stronger with each step. This is the final descent before the ultimate confrontation.",
                    "encounters": [
                        {
                            "name": "Trap Rooms",
                            "difficulty": "medium",
                            "description": "Elaborate trap rooms test the party's skills and teamwork. These rooms are designed to separate the party and force them to work together to solve puzzles and avoid deadly traps. The party must use all their abilities to survive.",
                        },
                        {
                            "name": "Ancient Guardians",
                            "difficulty": "hard",
                            "description": "Ancient guardians, awakened by the darkness, stand as the final defense. These guardians were created long ago to protect the keep, but the darkness has corrupted them. They are powerful and nearly indestructible, but the party must find a way to defeat them.",
                        },
                        {
                            "name": "The Shadow Lord's Minions",
                            "difficulty": "boss",
                            "description": "The most powerful minions of the Shadow Lord make their final stand. These are the Shadow Lord's most trusted servants, and they will fight to the death to protect their master. They are extremely powerful and work together as a coordinated unit.",
                        },
                        {
                            "name": "The Corrupted Heart",
                            "difficulty": "hard",
                            "description": "The very heart of the keep has been corrupted, and must be cleansed before facing the final boss. The heart is a massive crystal that pulses with dark energy. The party must fight off waves of enemies while trying to cleanse the crystal. This is a race against time.",
                        },
                        {
                            "name": "The Descent",
                            "difficulty": "medium",
                            "description": "The party must descend through a series of treacherous passages filled with obstacles and enemies. The descent is long and dangerous, testing the party's endurance and resolve. They must push forward despite the growing darkness.",
                        },
                        {
                            "name": "The Final Preparation",
                            "difficulty": "medium",
                            "description": "Before facing the Shadow Lord, the party finds a chamber where they can rest and prepare. However, this chamber is not safe - it is filled with illusions and traps designed to weaken the party before the final battle. The party must be careful even in this moment of respite.",
                        },
                    ],
                },
            ]

            task3 = progress.add_task(
                "[cyan]Generating campaign chapters...", total=len(chapters_config)
            )
            for i, chapter_config in enumerate(chapters_config, 1):
                self.generate_story_chapter(
                    i,
                    chapter_config["title"],
                    chapter_config["encounters"],
                    chapter_config.get("intro"),
                )
                progress.update(task3, advance=1)

            # Phase 4: Final Boss
            task4 = progress.add_task("[cyan]Creating final boss battle...", total=1)
            final_battle = self.create_final_boss_battle()
            self.chapters.append(
                {
                    "title": final_battle["title"],
                    "content": final_battle["content"],
                    "read_aloud": final_battle["read_aloud"],
                }
            )
            progress.update(task4, completed=1)

            # Phase 5: Generate PDF
            task5 = progress.add_task("[cyan]Generating PDF book...", total=1)
            self.generate_campaign_pdf()
            progress.update(task5, completed=1)

        console.print("\n[bold green]✅ EXTENDED CAMPAIGN COMPLETE! PDF GENERATED![/bold green]\n")

    def generate_campaign_pdf(self):
        """Generate the complete campaign PDF book."""
        console.print("\n[bold cyan]📚 GENERATING CAMPAIGN PDF BOOK 📚[/bold cyan]\n")

        party_summary = "\n".join(
            [
                f"- **{m.name}**: {m.race} {m.class_type} (Level {m.level}) - HP: {m.hp}/{m.max_hp}"
                for m in self.party
            ]
        )

        # Build complete markdown content
        markdown_content = f"""# The Eternal Guardians: An Epic Adventure

**Generated by**: WAFT Extended Campaign System  
**Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Party**: {", ".join([m.name for m in self.party])}  
**Total Encounters**: {self.total_encounters}  
**Campaign Status**: {"✅ VICTORY - Final Boss Defeated" if self.final_boss_defeated else "In Progress"}

---

## The Party

The heroes who answered the call:

{party_summary}

Together, they form a formidable team ready to face any challenge. Through their journey, 
they have grown stronger, wiser, and more united.

---

## Table of Contents

1. Prologue: The Rusty Tankard
"""

        # Add chapter titles to TOC
        for i, chapter in enumerate(self.chapters[1:], 2):  # Skip prologue
            markdown_content += f"{i}. {chapter['title']}\n"

        markdown_content += "\n---\n\n"

        # Add all chapters
        for chapter in self.chapters:
            markdown_content += f"\n\n{chapter['content']}\n\n"
            if chapter.get("read_aloud"):
                markdown_content += f"\n> **Read Aloud:**\n> {chapter['read_aloud']}\n\n"
            markdown_content += "---\n"

        # Add comprehensive final summary
        markdown_content += f"""
## Campaign Summary

The party has completed their epic adventure:

### Statistics

- **Total Encounters**: {self.total_encounters}
- **Chapters Completed**: {len(self.chapters)}
- **Final Boss**: The Shadow Lord Malachar - {"DEFEATED ✅" if self.final_boss_defeated else "Pending"}
- **Party Levels**: {", ".join([f"{m.name} (Level {m.level})" for m in self.party])}
- **Total Experience Gained**: ~{self.total_encounters * 50} XP per party member
- **Status**: {"✅ VICTORY" if self.final_boss_defeated else "In Progress"}

### The Journey

The party's journey took them from the humble Rusty Tankard tavern through dark forests, 
across dangerous roads, and into the very heart of Blackmoor Keep itself. They faced 
countless challenges, from goblin ambushes to shadow wraiths, from corrupted guards to 
ancient guardians. Through it all, they remained united and determined.

### The Victory

{"The realm is saved. The darkness is banished. The heroes return to the tavern as legends, " if self.final_boss_defeated else "The adventure continues..."} 
Their names will be remembered for generations to come.

---

## Appendices

### Party Character Sheets

"""

        # Add detailed character sheets
        for member in self.party:
            markdown_content += f"""
#### {member.name}

- **Race**: {member.race}
- **Class**: {member.class_type}
- **Level**: {member.level}
- **Experience**: {member.experience}
- **Hit Points**: {member.hp}/{member.max_hp}
- **Stats**: 
  - Strength: {member.stats["strength"]}
  - Dexterity: {member.stats["dexterity"]}
  - Constitution: {member.stats["constitution"]}
  - Intelligence: {member.stats["intelligence"]}
  - Wisdom: {member.stats["wisdom"]}
  - Charisma: {member.stats["charisma"]}

"""

        markdown_content += """
### Campaign Timeline

"""

        # Add timeline from campaign log
        for log_entry in self.campaign_log:
            markdown_content += f"- **{log_entry.get('event', 'Unknown')}**: {log_entry.get('description', '')} ({log_entry.get('timestamp', '')[:10]})\n"

        markdown_content += f"""

---

*This campaign was generated automatically by the WAFT Extended Campaign System.*  
*All encounters, story beats, and outcomes were determined by the system itself.*  
*Total word count: ~{len(markdown_content.split())} words*  
*Total pages (estimated): ~{len(markdown_content.split()) // 250} pages*
"""

        try:
            output_path = self.output_dir / "Extended_DnD_Campaign_Complete.pdf"

            # Generate PDF using PDFGenerator
            generator = PDFGenerator.from_content(
                content=markdown_content,
                title="The Eternal Guardians: An Epic Adventure",
                style="premium",
            )

            pdf_path = generator.save(output_path=output_path, convert_to_png=False)

            console.print(f"[green]✅ Campaign PDF generated: {pdf_path}[/green]")
            console.print(
                f"[green]   Estimated pages: ~{len(markdown_content.split()) // 250}[/green]"
            )
            console.print(f"[green]   Word count: ~{len(markdown_content.split())} words[/green]")

            # Save campaign log
            log_path = self.output_dir / "campaign_log.json"
            with open(log_path, "w") as f:
                json.dump(
                    {
                        "campaign_info": {
                            "title": "The Eternal Guardians: An Epic Adventure",
                            "party": [
                                {
                                    "name": m.name,
                                    "class": m.class_type,
                                    "race": m.race,
                                    "level": m.level,
                                    "hp": m.hp,
                                    "max_hp": m.max_hp,
                                    "experience": m.experience,
                                    "being_id": m.being.being_id,
                                }
                                for m in self.party
                            ],
                            "final_boss_defeated": self.final_boss_defeated,
                            "total_chapters": len(self.chapters),
                            "total_encounters": self.total_encounters,
                        },
                        "campaign_log": self.campaign_log,
                        "chapters": [
                            {"title": c["title"], "encounters": c.get("encounters", [])}
                            for c in self.chapters
                        ],
                    },
                    f,
                    indent=2,
                )

            console.print(f"[green]✅ Campaign log saved: {log_path}[/green]")

            return pdf_path

        except Exception as e:
            console.print(f"[red]❌ Error generating PDF: {e}[/red]")
            import traceback

            traceback.print_exc()
            raise


def main():
    """Main entry point."""
    output_dir = Path(__file__).parent.parent / "_temp" / "long_campaign_output"
    output_dir.mkdir(parents=True, exist_ok=True)

    campaign = ExtendedCampaign(output_dir)
    campaign.run_extended_campaign()


if __name__ == "__main__":
    main()
