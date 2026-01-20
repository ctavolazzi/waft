#!/usr/bin/env python3
"""
Self-Playing DnD Campaign: Tavern to Final Boss
===============================================

A complete self-playing DnD campaign that generates itself from start to finish.
The party starts in a tavern and the story unfolds automatically, building to
an epic final boss battle.

Uses WAFT's Being system, scientific method, and PDF generation - all free/open source.
"""

import json
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from rich.console import Console
from rich.panel import Panel

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


class SelfPlayingCampaign:
    """Self-playing DnD campaign system."""

    def __init__(self, work_effort_path: Path):
        self.work_effort_path = work_effort_path
        self.project_path = project_root
        self.being_system = BeingSystem(project_path=self.project_path)
        self.party: list[PartyMember] = []
        self.campaign_log: list[dict[str, Any]] = []
        self.chapters: list[dict[str, Any]] = []
        self.current_location = "Tavern"
        self.quest_progress = 0
        self.final_boss_defeated = False

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
        for _i, config in enumerate(party_configs):
            console.print(f"[yellow]→[/yellow] Spawning {config['name']}...")

            being = self.being_system.spawn_being(
                reality_id="dnd_campaign_reality",
                parent_being_id=None,
                initial_skills=config["skills"],
            )

            member = PartyMember(being, config["name"], config["class"], config["race"])
            party.append(member)

            # Record memory
            being.record_memory(
                f"Joined adventuring party as {config['class']}",
                "experience",
                {
                    "party_name": "The Tavern Heroes",
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
            """,
            "read_aloud": """
The messenger's eyes are wide with fear. "The Keep has been overrun by shadows.
Something ancient has awakened. We need brave souls to face whatever darkness lies within."
            """,
            "sidebar": {
                "title": "The Quest",
                "content": "Investigate Blackmoor Keep and defeat the darkness that has taken hold.",
            },
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

    def generate_encounter(self, encounter_name: str, difficulty: str = "medium") -> dict[str, Any]:
        """Generate a combat encounter."""
        console.print(f"\n[bold red]⚔️  ENCOUNTER: {encounter_name} ⚔️[/bold red]\n")

        difficulty_multiplier = {"easy": 0.8, "medium": 1.0, "hard": 1.5, "boss": 3.0}[difficulty]

        # Simulate combat
        enemy_hp = int(100 * difficulty_multiplier)
        party_damage = sum([random.randint(15, 30) for _ in self.party])
        rounds = max(1, int(enemy_hp / party_damage))

        # Party takes some damage
        for member in self.party:
            damage = random.randint(5, 15) * int(difficulty_multiplier)
            member.take_damage(damage)
            if member.hp <= 0:
                member.hp = 1  # Don't kill party members, just knock them out

        # Gain experience
        xp_gain = int(50 * difficulty_multiplier)
        for member in self.party:
            leveled = member.gain_experience(xp_gain)
            if leveled:
                console.print(f"   [green]✨ {member.name} leveled up to {member.level}![/green]")

        encounter = {
            "title": encounter_name,
            "content": f"""
The party faces {encounter_name} in a fierce battle that lasts {rounds} rounds.
Through teamwork and determination, they emerge victorious, though not without taking some damage.

Experience gained: {xp_gain} XP per party member.
            """,
            "read_aloud": f"""
The battle is intense. Steel clashes, spells fly, and the party fights as one.
After {rounds} rounds of combat, {encounter_name} falls, defeated by the heroes' resolve.
            """,
            "difficulty": difficulty,
            "rounds": rounds,
            "xp_gained": xp_gain,
        }

        self.campaign_log.append(
            {
                "timestamp": datetime.now().isoformat(),
                "event": "encounter",
                "encounter_name": encounter_name,
                "difficulty": difficulty,
                "rounds": rounds,
            }
        )

        console.print(
            f"   [green]✓[/green] Encounter complete! Party HP: {sum([m.hp for m in self.party])}/{sum([m.max_hp for m in self.party])}"
        )
        return encounter

    def generate_story_chapter(
        self, chapter_num: int, title: str, encounters: list[str]
    ) -> dict[str, Any]:
        """Generate a story chapter with encounters."""
        console.print(f"\n[bold cyan]📖 CHAPTER {chapter_num}: {title} 📖[/bold cyan]\n")

        chapter_content = f"# {title}\n\n"
        chapter_read_aloud = []

        # Add chapter introduction
        chapter_content += f"The party continues their journey toward Blackmoor Keep. {title}\n\n"

        # Add encounters
        for i, encounter_name in enumerate(encounters):
            difficulty = "boss" if i == len(encounters) - 1 and chapter_num >= 4 else "medium"
            encounter = self.generate_encounter(encounter_name, difficulty)
            chapter_content += f"## {encounter['title']}\n\n{encounter['content']}\n\n"
            chapter_read_aloud.append(encounter["read_aloud"])

        chapter = {
            "title": f"Chapter {chapter_num}: {title}",
            "content": chapter_content,
            "read_aloud": "\n\n".join(chapter_read_aloud),
            "encounters": encounters,
        }

        self.chapters.append(chapter)
        return chapter

    def create_final_boss_battle(self) -> dict[str, Any]:
        """Create the epic final boss battle."""
        console.print("\n[bold red]👹 FINAL BOSS BATTLE 👹[/bold red]\n")

        boss_name = "The Shadow Lord Malachar"

        # Epic boss battle
        boss_hp = 500
        party_damage = sum([random.randint(20, 40) for _ in self.party])
        rounds = max(5, int(boss_hp / party_damage))

        # Party takes significant damage
        for member in self.party:
            damage = random.randint(20, 35)
            member.take_damage(damage)
            if member.hp <= 0:
                member.hp = 1

        # Massive XP gain
        xp_gain = 500
        for member in self.party:
            leveled = member.gain_experience(xp_gain)
            if leveled:
                console.print(f"   [green]✨ {member.name} leveled up to {member.level}![/green]")

        battle = {
            "title": f"The Final Battle: {boss_name}",
            "content": f"""
# The Final Battle

The party has reached the heart of Blackmoor Keep. Before them stands {boss_name},
a being of pure darkness that has corrupted the ancient fortress.

The battle is epic. Spells of immense power clash with dark magic. Swords strike
against shadowy armor. The very foundations of the keep shake with the force of combat.

After {rounds} grueling rounds, the party's determination and teamwork overcome the darkness.
{boss_name} lets out a final, terrible scream as the light of the heroes' resolve banishes
the shadow forever.

The keep is free. The darkness is defeated. The party has saved the realm.

## Victory!

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

    def run_complete_campaign(self):
        """Run the complete self-playing campaign."""
        console.print("\n" + "=" * 80)
        console.print(
            "[bold cyan]🎲 SELF-PLAYING DND CAMPAIGN: TAVERN TO FINAL BOSS 🎲[/bold cyan]"
        )
        console.print("=" * 80 + "\n")

        # Phase 1: Spawn Party
        self.spawn_party()

        # Phase 2: Tavern Scene
        tavern_scene = self.create_tavern_scene()
        self.chapters.append(
            {
                "title": "Prologue: The Rusty Tankard",
                "content": tavern_scene["content"],
                "read_aloud": tavern_scene["read_aloud"],
                "sidebar": tavern_scene.get("sidebar"),
            }
        )

        # Phase 3: Journey Chapters
        chapters_config = [
            {
                "title": "The Road to Blackmoor",
                "encounters": ["Goblin Ambush", "Wolves of the Darkwood", "Bandit Encounter"],
            },
            {
                "title": "Approaching the Keep",
                "encounters": ["Skeleton Warriors", "Dark Cultists", "Shadow Beasts"],
            },
            {
                "title": "Within the Keep",
                "encounters": ["Corrupted Guards", "Undead Servants", "The Keep's Lieutenant"],
            },
            {
                "title": "The Depths",
                "encounters": ["Trap Rooms", "Ancient Guardians", "The Shadow Lord's Minions"],
            },
        ]

        for i, chapter_config in enumerate(chapters_config, 1):
            self.generate_story_chapter(i, chapter_config["title"], chapter_config["encounters"])

        # Phase 4: Final Boss
        final_battle = self.create_final_boss_battle()
        self.chapters.append(
            {
                "title": final_battle["title"],
                "content": final_battle["content"],
                "read_aloud": final_battle["read_aloud"],
            }
        )

        # Phase 5: Generate PDF
        self.generate_campaign_pdf()

        console.print("\n[bold green]✅ CAMPAIGN COMPLETE! PDF GENERATED![/bold green]\n")

    def generate_campaign_pdf(self):
        """Generate the complete campaign PDF."""
        console.print("\n[bold cyan]📚 GENERATING CAMPAIGN PDF 📚[/bold cyan]\n")

        output_dir = self.work_effort_path / "output"
        output_dir.mkdir(exist_ok=True)

        party_summary = "\n".join(
            [f"- **{m.name}**: {m.race} {m.class_type} (Level {m.level})" for m in self.party]
        )

        # Prepare chapters for LaTeX
        latex_chapters = []
        for chapter in self.chapters:
            latex_chapters.append(
                {
                    "title": chapter["title"],
                    "content": chapter["content"],
                    "read_aloud": chapter.get("read_aloud", ""),
                    "sidebar": chapter.get("sidebar"),
                }
            )

        # Add party summary chapter
        latex_chapters.insert(
            1,
            {
                "title": "The Party",
                "content": f"""
# The Party

The heroes who answered the call:

{party_summary}

Together, they form a formidable team ready to face any challenge.
            """,
                "read_aloud": "",
                "sidebar": None,
            },
        )

        try:
            output_path = output_dir / "Self_Playing_DnD_Campaign_Complete.pdf"

            # Build complete markdown content
            markdown_content = f"""# The Tavern Heroes: A Self-Playing Adventure

**Generated by**: WAFT Self-Playing Campaign System
**Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Party**: {", ".join([m.name for m in self.party])}

---

## The Party

{party_summary}

---

"""

            # Add all chapters
            for chapter in latex_chapters:
                markdown_content += f"\n\n{chapter['content']}\n\n"
                if chapter.get("read_aloud"):
                    markdown_content += f"\n> **Read Aloud:**\n> {chapter['read_aloud']}\n\n"
                markdown_content += "---\n"

            # Add final summary
            markdown_content += f"""
## Campaign Summary

The party has completed their epic adventure:

- **Total Encounters**: {len(self.campaign_log) - 1}  # -1 for tavern scene
- **Final Boss**: The Shadow Lord Malachar - DEFEATED
- **Party Levels**: {", ".join([f"{m.name} (Level {m.level})" for m in self.party])}
- **Status**: ✅ VICTORY

The realm is saved. The darkness is banished. The heroes return to the tavern as legends.

---

*This campaign was generated automatically by the WAFT Self-Playing Campaign System.*
*All encounters, story beats, and outcomes were determined by the system itself.*
"""

            # Generate PDF using PDFGenerator (no LaTeX required)
            generator = PDFGenerator.from_content(
                content=markdown_content,
                title="The Tavern Heroes: A Self-Playing Adventure",
                style="premium",
            )

            pdf_path = generator.save(
                output_path=output_path,
                convert_to_png=False,  # Skip PNG to avoid extra dependencies
            )

            console.print(f"[green]✅ Campaign PDF generated: {pdf_path}[/green]")

            # Save campaign log
            log_path = output_dir / "campaign_log.json"
            with open(log_path, "w") as f:
                json.dump(
                    {
                        "campaign_info": {
                            "title": "The Tavern Heroes: A Self-Playing Adventure",
                            "party": [
                                {
                                    "name": m.name,
                                    "class": m.class_type,
                                    "race": m.race,
                                    "level": m.level,
                                    "being_id": m.being.being_id,
                                }
                                for m in self.party
                            ],
                            "final_boss_defeated": self.final_boss_defeated,
                            "total_chapters": len(self.chapters),
                        },
                        "campaign_log": self.campaign_log,
                        "chapters": self.chapters,
                    },
                    f,
                    indent=2,
                )

            console.print(f"[green]✅ Campaign log saved: {log_path}[/green]")

            return pdf_path

        except Exception as e:
            console.print(f"[red]❌ Error generating PDF: {e}[/red]")
            raise


def main():
    """Main entry point."""
    work_effort_path = Path(__file__).parent

    campaign = SelfPlayingCampaign(work_effort_path)
    campaign.run_complete_campaign()


if __name__ == "__main__":
    main()
