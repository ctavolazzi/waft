#!/usr/bin/env python3
"""
Self-Playing DnD Campaign with Electron Window
==============================================

A complete self-playing DnD campaign that displays in an Electron window,
showing the game playing itself in real-time!
"""

import random
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from rich.console import Console

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


class ElectronCampaignDisplay:
    """Manages Electron window for real-time campaign display."""

    def __init__(self, work_effort_path: Path):
        self.work_effort_path = work_effort_path
        self.electron_app_path = project_root / "recap_review_app" / "frontend"
        self.html_file = work_effort_path / "output" / "campaign_display.html"
        self.html_file.parent.mkdir(exist_ok=True)
        self.electron_process = None

    def start_electron_window(self):
        """Start Electron window showing the campaign."""
        # Create initial HTML
        self.update_html(
            {
                "status": "starting",
                "message": "🎲 Self-Playing DnD Campaign Starting...",
                "party": [],
                "current_scene": "Initializing...",
                "encounters": [],
                "log": [],
            }
        )

        # Open the HTML file - will try Electron, fallback to browser
        try:
            # First, just open the file - system will use default handler
            # On macOS, this might open in browser, but that's fine
            console.print("[yellow]→[/yellow] Opening campaign display window...")

            # Try npx electron first (if available)
            try:
                subprocess.Popen(
                    ["npx", "electron", str(self.html_file)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                console.print("[green]✅ Opening in Electron window![/green]")
            except:
                # Fallback: use system default (browser on macOS)
                subprocess.Popen(["open", str(self.html_file)])
                console.print("[green]✅ Opening in browser window![/green]")
                console.print(
                    "[yellow]💡 Tip: Install Electron globally for better experience: npm install -g electron[/yellow]"
                )
        except Exception as e:
            # Last resort: just tell user where the file is
            console.print(f"[yellow]⚠️  Could not auto-open: {e}[/yellow]")
            console.print(f"[green]📄 HTML file created at: {self.html_file}[/green]")
            console.print(
                "[yellow]   Open it manually or run: open output/campaign_display.html[/yellow]"
            )

    def update_html(self, campaign_state: dict[str, Any]):
        """Update the HTML file with current campaign state."""
        party_html = ""
        for member in campaign_state.get("party", []):
            hp_percent = (member["hp"] / member["max_hp"]) * 100
            party_html += f"""
            <div class="party-member">
                <h3>{member["name"]}</h3>
                <p class="class-race">{member["race"]} {member["class"]} - Level {member["level"]}</p>
                <div class="hp-bar">
                    <div class="hp-fill" style="width: {hp_percent}%"></div>
                    <span class="hp-text">{member["hp"]}/{member["max_hp"]} HP</span>
                </div>
                <p class="xp">XP: {member["experience"]}</p>
            </div>
            """

        encounters_html = ""
        for encounter in campaign_state.get("encounters", []):
            encounters_html += f"""
            <div class="encounter">
                <h4>⚔️ {encounter["name"]}</h4>
                <p>{encounter["description"]}</p>
                <p class="encounter-meta">Rounds: {encounter.get("rounds", 1)} | XP: +{encounter.get("xp", 0)}</p>
            </div>
            """

        log_html = ""
        for entry in campaign_state.get("log", [])[-10:]:  # Last 10 entries
            log_html += f"<div class='log-entry'>{entry}</div>"

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Self-Playing DnD Campaign</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Georgia', serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #f5f5f5;
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        h1 {{
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}

        .status {{
            text-align: center;
            font-size: 1.5em;
            margin-bottom: 30px;
            padding: 15px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
        }}

        .party {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .party-member {{
            background: rgba(255,255,255,0.15);
            padding: 20px;
            border-radius: 10px;
            border: 2px solid rgba(255,255,255,0.3);
        }}

        .party-member h3 {{
            color: #ffd700;
            margin-bottom: 10px;
        }}

        .class-race {{
            font-style: italic;
            margin-bottom: 15px;
        }}

        .hp-bar {{
            background: rgba(0,0,0,0.3);
            height: 30px;
            border-radius: 15px;
            position: relative;
            margin-bottom: 10px;
            overflow: hidden;
        }}

        .hp-fill {{
            background: linear-gradient(90deg, #4caf50, #8bc34a);
            height: 100%;
            transition: width 0.5s ease;
            border-radius: 15px;
        }}

        .hp-text {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-weight: bold;
            color: white;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.7);
        }}

        .current-scene {{
            background: rgba(255,255,255,0.1);
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 5px solid #ffd700;
        }}

        .current-scene h2 {{
            color: #ffd700;
            margin-bottom: 15px;
        }}

        .encounters {{
            margin-bottom: 30px;
        }}

        .encounter {{
            background: rgba(255,255,255,0.1);
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 8px;
            border-left: 4px solid #ff6b6b;
        }}

        .encounter h4 {{
            color: #ffd700;
            margin-bottom: 10px;
        }}

        .encounter-meta {{
            font-size: 0.9em;
            color: #ccc;
            margin-top: 10px;
        }}

        .log {{
            background: rgba(0,0,0,0.3);
            padding: 15px;
            border-radius: 10px;
            max-height: 300px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}

        .log-entry {{
            padding: 5px;
            margin-bottom: 5px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}

        .victory {{
            text-align: center;
            padding: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            margin-top: 30px;
        }}

        .victory h2 {{
            font-size: 3em;
            color: #ffd700;
            margin-bottom: 20px;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .party-member, .encounter, .log-entry {{
            animation: fadeIn 0.5s ease;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎲 Self-Playing DnD Campaign 🎲</h1>
        <div class="status" id="status">{campaign_state.get("message", "Running...")}</div>

        <div class="party" id="party">
            {party_html}
        </div>

        <div class="current-scene" id="current-scene">
            <h2>Current Scene</h2>
            <p>{campaign_state.get("current_scene", "Starting adventure...")}</p>
        </div>

        <div class="encounters" id="encounters">
            <h2 style="margin-bottom: 15px; color: #ffd700;">⚔️ Encounters</h2>
            {encounters_html}
        </div>

        <div class="log" id="log">
            <h3 style="margin-bottom: 10px; color: #ffd700;">📜 Campaign Log</h3>
            {log_html}
        </div>

        {'<div class="victory"><h2>🎉 VICTORY! 🎉</h2><p>The Shadow Lord Malachar has been defeated!<br>The realm is saved!</p></div>' if campaign_state.get("victory") else ""}
    </div>

    <script>
        // Auto-refresh every 2 seconds to show updates
        let refreshCount = 0;
        const maxRefreshes = 300; // 10 minutes max

        function autoRefresh() {{
            refreshCount++;
            if (refreshCount < maxRefreshes) {{
                setTimeout(() => {{
                    location.reload();
                }}, 2000);
            }} else {{
                document.getElementById('status').textContent = '🎉 Campaign Complete! Window will stay open.';
            }}
        }}

        autoRefresh();
    </script>
</body>
</html>"""

        self.html_file.write_text(html_content, encoding="utf-8")

    def stop_electron(self):
        """Stop Electron process."""
        if self.electron_process:
            self.electron_process.terminate()


class SelfPlayingCampaignElectron:
    """Self-playing DnD campaign with Electron window display."""

    def __init__(self, work_effort_path: Path):
        self.work_effort_path = work_effort_path
        self.project_path = project_root
        self.being_system = BeingSystem(project_path=self.project_path)
        self.party: list[PartyMember] = []
        self.campaign_log: list[str] = []
        self.encounters: list[dict[str, Any]] = []
        self.current_scene = "Starting..."
        self.display = ElectronCampaignDisplay(work_effort_path)
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
        self.update_display()
        return party

    def update_display(self):
        """Update Electron window with current state."""
        party_data = [
            {
                "name": m.name,
                "class": m.class_type,
                "race": m.race,
                "level": m.level,
                "hp": m.hp,
                "max_hp": m.max_hp,
                "experience": m.experience,
            }
            for m in self.party
        ]

        self.display.update_html(
            {
                "status": "running" if not self.final_boss_defeated else "victory",
                "message": "🎲 Adventure in Progress..."
                if not self.final_boss_defeated
                else "🎉 VICTORY!",
                "party": party_data,
                "current_scene": self.current_scene,
                "encounters": self.encounters,
                "log": self.campaign_log,
                "victory": self.final_boss_defeated,
            }
        )

    def create_tavern_scene(self) -> dict[str, Any]:
        """Create the opening tavern scene."""
        console.print("\n[bold cyan]🍺 THE TAVERN - OPENING SCENE 🍺[/bold cyan]\n")

        self.current_scene = "The Rusty Tankard Tavern - A messenger arrives with an urgent quest!"
        self.campaign_log.append("🍺 The party sits in The Rusty Tankard tavern...")
        self.campaign_log.append("🚪 A messenger bursts through the door!")
        self.campaign_log.append("📜 Quest received: Investigate Blackmoor Keep!")
        self.update_display()
        time.sleep(2)

        scene = {
            "title": "The Rusty Tankard Tavern",
            "content": "The warm glow of the hearth casts dancing shadows. A messenger arrives with news of darkness at Blackmoor Keep. The party accepts the quest!",
        }

        return scene

    def generate_encounter(self, encounter_name: str, difficulty: str = "medium") -> dict[str, Any]:
        """Generate a combat encounter."""
        console.print(f"\n[bold red]⚔️  ENCOUNTER: {encounter_name} ⚔️[/bold red]\n")

        self.current_scene = f"⚔️ Battle: {encounter_name}"
        self.campaign_log.append(f"⚔️ Encounter: {encounter_name}")
        self.update_display()
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
        self.update_display()
        time.sleep(2)

        return encounter

    def create_final_boss_battle(self) -> dict[str, Any]:
        """Create the epic final boss battle."""
        console.print("\n[bold red]👹 FINAL BOSS BATTLE 👹[/bold red]\n")

        boss_name = "The Shadow Lord Malachar"
        self.current_scene = f"👹 FINAL BOSS: {boss_name}"
        self.campaign_log.append(f"👹 FINAL BOSS APPEARS: {boss_name}!")
        self.update_display()
        time.sleep(2)

        boss_hp = 500
        party_damage = sum([random.randint(20, 40) for _ in self.party])
        rounds = max(5, int(boss_hp / party_damage))

        for i in range(rounds):
            self.campaign_log.append(f"⚔️ Round {i + 1}: The battle rages on...")
            self.update_display()
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
        self.update_display()
        time.sleep(3)

        return {
            "name": boss_name,
            "description": f"Epic {rounds}-round battle. The party's determination overcomes the darkness!",
            "rounds": rounds,
            "xp": xp_gain,
            "victory": True,
        }

    def run_complete_campaign(self):
        """Run the complete self-playing campaign with Electron display."""
        console.print("\n" + "=" * 80)
        console.print("[bold cyan]🎲 SELF-PLAYING DND CAMPAIGN WITH ELECTRON WINDOW 🎲[/bold cyan]")
        console.print("=" * 80 + "\n")

        # Start Electron window
        console.print("[yellow]→[/yellow] Opening Electron window...")
        self.display.start_electron_window()
        time.sleep(2)  # Give Electron time to start

        # Phase 1: Spawn Party
        self.spawn_party()
        time.sleep(2)

        # Phase 2: Tavern Scene
        self.create_tavern_scene()
        time.sleep(2)

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
            self.update_display()
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

        # Update display one final time
        self.current_scene = "🎉 Campaign Complete! Check the PDF for the full story!"
        self.update_display()

        console.print(
            "\n[bold green]✅ CAMPAIGN COMPLETE! Check the Electron window![/bold green]\n"
        )
        console.print(f"[yellow]💡 HTML file: {self.display.html_file}[/yellow]\n")
        console.print(
            "[yellow]💡 The window will stay open. Close it when done viewing.[/yellow]\n"
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

    campaign = SelfPlayingCampaignElectron(work_effort_path)
    campaign.run_complete_campaign()

    # Keep Electron open
    console.print(
        "\n[yellow]💡 Window is still open. Close it when you're done viewing![/yellow]\n"
    )
    console.print(f"[green]📄 HTML file location: {campaign.display.html_file}[/green]\n")
    console.print(
        "[blue]💡 You can also open it manually: open output/campaign_display.html[/blue]\n"
    )


if __name__ == "__main__":
    main()
