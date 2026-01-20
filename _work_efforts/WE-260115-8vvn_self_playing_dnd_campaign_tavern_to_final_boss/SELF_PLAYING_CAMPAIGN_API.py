#!/usr/bin/env python3
"""
Self-Playing DnD Campaign - API Mode
=====================================

Runs the campaign and sends state updates to FastAPI backend
for real-time display in Electron.
"""

import os
import random
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from rich.console import Console

from src.waft.being import Being, BeingSystem
from src.waft.evolution.pdf_generator import PDFGenerator

console = Console()

# API URL for state updates
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
ELECTRON_MODE = os.getenv("ELECTRON_MODE", "0") == "1"


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

    def to_dict(self):
        """Convert to dictionary for API."""
        return {
            "name": self.name,
            "class": self.class_type,
            "race": self.race,
            "level": self.level,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "experience": self.experience,
        }


def send_state_update(state: dict[str, Any]):
    """Send state update to FastAPI backend."""
    if not ELECTRON_MODE:
        return

    try:
        response = requests.post(f"{API_URL}/api/dnd-campaign/update", json=state, timeout=2)
        if response.status_code == 200:
            return True
    except Exception:
        # Silently fail - don't break campaign if API is down
        pass
    return False


class SelfPlayingCampaignAPI:
    """Self-playing DnD campaign with API integration."""

    def __init__(self, work_effort_path: Path):
        self.work_effort_path = work_effort_path
        self.project_path = project_root
        self.being_system = BeingSystem(project_path=self.project_path)
        self.party: list[PartyMember] = []
        self.campaign_log: list[str] = []
        self.encounters: list[dict[str, Any]] = []
        self.current_scene = "Starting..."
        self.final_boss_defeated = False

    def update_state(self):
        """Update state and send to API."""
        party_data = [m.to_dict() for m in self.party]

        state = {
            "status": "running" if not self.final_boss_defeated else "complete",
            "message": "🎲 Adventure in Progress..."
            if not self.final_boss_defeated
            else "🎉 VICTORY!",
            "party": party_data,
            "current_scene": self.current_scene,
            "encounters": self.encounters,
            "log": self.campaign_log,
            "victory": self.final_boss_defeated,
        }

        send_state_update(state)

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
        for config in party_configs:
            being = self.being_system.spawn_being(
                reality_id="dnd_campaign_reality",
                parent_being_id=None,
                initial_skills=config["skills"],
            )

            member = PartyMember(being, config["name"], config["class"], config["race"])
            party.append(member)

            being.record_memory(
                f"Joined adventuring party as {config['class']}",
                "experience",
                {
                    "party_name": "The Tavern Heroes",
                    "class": config["class"],
                    "race": config["race"],
                },
            )

            self.campaign_log.append(
                f"✨ {config['name']} ({config['race']} {config['class']}) joined the party!"
            )

        self.party = party
        self.update_state()
        time.sleep(1)
        return party

    def create_tavern_scene(self) -> dict[str, Any]:
        """Create the opening tavern scene."""
        console.print("\n[bold cyan]🍺 THE TAVERN - OPENING SCENE 🍺[/bold cyan]\n")

        self.current_scene = "The Rusty Tankard Tavern - A messenger arrives with an urgent quest!"
        self.campaign_log.append("🍺 The party sits in The Rusty Tankard tavern...")
        self.campaign_log.append("🚪 A messenger bursts through the door!")
        self.campaign_log.append("📜 Quest received: Investigate Blackmoor Keep!")
        self.update_state()
        time.sleep(2)

        return {
            "title": "The Rusty Tankard Tavern",
            "content": "The warm glow of the hearth casts dancing shadows. A messenger arrives with news of darkness at Blackmoor Keep. The party accepts the quest!",
        }

    def generate_encounter(self, encounter_name: str, difficulty: str = "medium") -> dict[str, Any]:
        """Generate a combat encounter."""
        console.print(f"\n[bold red]⚔️  ENCOUNTER: {encounter_name} ⚔️[/bold red]\n")

        self.current_scene = f"⚔️ Battle: {encounter_name}"
        self.campaign_log.append(f"⚔️ Encounter: {encounter_name}")
        self.update_state()
        time.sleep(1)

        difficulty_multiplier = {"easy": 0.8, "medium": 1.0, "hard": 1.5, "boss": 3.0}[difficulty]

        enemy_hp = int(100 * difficulty_multiplier)
        party_damage = sum([random.randint(15, 30) for _ in self.party])
        rounds = max(1, int(enemy_hp / party_damage))

        for member in self.party:
            damage = random.randint(5, 15) * int(difficulty_multiplier)
            member.take_damage(damage)
            if member.hp <= 0:
                member.hp = 1

        xp_gain = int(50 * difficulty_multiplier)
        leveled_members = []
        for member in self.party:
            leveled = member.gain_experience(xp_gain)
            if leveled:
                leveled_members.append(member.name)
                self.campaign_log.append(f"✨ {member.name} leveled up to {member.level}!")

        encounter = {
            "name": encounter_name,
            "description": f"Epic battle lasting {rounds} rounds. The party emerges victorious!",
            "rounds": rounds,
            "xp": xp_gain,
            "difficulty": difficulty,
        }

        self.encounters.append(encounter)
        self.campaign_log.append(f"✅ {encounter_name} defeated! +{xp_gain} XP")
        self.update_state()
        time.sleep(2)

        return encounter

    def create_final_boss_battle(self) -> dict[str, Any]:
        """Create the epic final boss battle."""
        console.print("\n[bold red]👹 FINAL BOSS BATTLE 👹[/bold red]\n")

        boss_name = "The Shadow Lord Malachar"
        self.current_scene = f"👹 FINAL BOSS: {boss_name}"
        self.campaign_log.append(f"👹 FINAL BOSS APPEARS: {boss_name}!")
        self.update_state()
        time.sleep(2)

        boss_hp = 500
        party_damage = sum([random.randint(20, 40) for _ in self.party])
        rounds = max(5, int(boss_hp / party_damage))

        for i in range(rounds):
            self.campaign_log.append(f"⚔️ Round {i + 1}: The battle rages on...")
            self.update_state()
            time.sleep(1)

        for member in self.party:
            damage = random.randint(20, 35)
            member.take_damage(damage)
            if member.hp <= 0:
                member.hp = 1

        xp_gain = 500
        for member in self.party:
            leveled = member.gain_experience(xp_gain)
            if leveled:
                self.campaign_log.append(f"✨ {member.name} leveled up to {member.level}!")

        self.campaign_log.append(f"🎉 {boss_name} DEFEATED!")
        self.campaign_log.append("🏆 VICTORY! The realm is saved!")
        self.final_boss_defeated = True
        self.current_scene = "🎉 VICTORY! The Shadow Lord Malachar has been defeated!"
        self.update_state()
        time.sleep(3)

        return {
            "name": boss_name,
            "description": f"Epic {rounds}-round battle. The party's determination overcomes the darkness!",
            "rounds": rounds,
            "xp": xp_gain,
            "victory": True,
        }

    def run_complete_campaign(self):
        """Run the complete self-playing campaign with API updates."""
        console.print("\n" + "=" * 80)
        console.print("[bold cyan]🎲 SELF-PLAYING DND CAMPAIGN (API MODE) 🎲[/bold cyan]")
        console.print("=" * 80 + "\n")

        # Phase 1: Spawn Party
        self.spawn_party()
        time.sleep(1)

        # Phase 2: Tavern Scene
        self.create_tavern_scene()
        time.sleep(1)

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
            self.current_scene = f"Chapter {i}: {chapter_config['title']}"
            self.campaign_log.append(f"📖 Chapter {i}: {chapter_config['title']}")
            self.update_state()
            time.sleep(1)

            for encounter_name in chapter_config["encounters"]:
                difficulty = (
                    "boss"
                    if i >= 4 and encounter_name == chapter_config["encounters"][-1]
                    else "medium"
                )
                self.generate_encounter(encounter_name, difficulty)

        # Phase 4: Final Boss
        self.create_final_boss_battle()

        # Phase 5: Generate PDF
        console.print("\n[bold cyan]📚 GENERATING CAMPAIGN PDF 📚[/bold cyan]\n")
        self.generate_campaign_pdf()

        # Final state update
        self.update_state()

        console.print(
            "\n[bold green]✅ CAMPAIGN COMPLETE! Check the Electron window![/bold green]\n"
        )

    def generate_campaign_pdf(self):
        """Generate the complete campaign PDF."""
        output_dir = self.work_effort_path / "output"
        output_dir.mkdir(exist_ok=True)

        party_summary = "\n".join(
            [f"- **{m.name}**: {m.race} {m.class_type} (Level {m.level})" for m in self.party]
        )

        markdown_content = f"""# The Tavern Heroes: A Self-Playing Adventure

**Generated by**: WAFT Self-Playing Campaign System  
**Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Party**: {", ".join([m.name for m in self.party])}

---

## The Party

{party_summary}

---

## Campaign Log

"""

        for entry in self.campaign_log:
            markdown_content += f"- {entry}\n"

        markdown_content += f"""

---

## Campaign Summary

- **Total Encounters**: {len(self.encounters)}
- **Final Boss**: The Shadow Lord Malachar - DEFEATED
- **Party Levels**: {", ".join([f"{m.name} (Level {m.level})" for m in self.party])}
- **Status**: ✅ VICTORY

The realm is saved. The darkness is banished. The heroes return to the tavern as legends.

---

*This campaign was generated automatically by the WAFT Self-Playing Campaign System.*
"""

        output_path = output_dir / "Self_Playing_DnD_Campaign_Complete.pdf"
        generator = PDFGenerator.from_content(
            content=markdown_content,
            title="The Tavern Heroes: A Self-Playing Adventure",
            style="premium",
        )

        pdf_path = generator.save(output_path=output_path, convert_to_png=False)

        console.print(f"[green]✅ Campaign PDF generated: {pdf_path}[/green]")


def main():
    """Main entry point."""
    work_effort_path = Path(__file__).parent

    campaign = SelfPlayingCampaignAPI(work_effort_path)
    campaign.run_complete_campaign()


if __name__ == "__main__":
    main()
