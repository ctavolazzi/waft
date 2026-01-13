"""
Town Tavern Scenario - Waking Up

A classic D&D scenario: You wake up in a tavern, not remembering how you got there.
Your character has D&D 5e stats, and you'll need to use them to navigate the situation.

This demonstrates the D&D 5e physics engine integration with WAFT Beings.
"""

from pathlib import Path
import sys
from datetime import datetime
from typing import List, Dict, Any
import subprocess
import platform
import re

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.core.dnd5e import (
    DnD5eCharacter,
    DnD5eStats,
    DnDRoller,
    DnD5eCombat,
    ArmorType
)
from waft.evolution.pdf_generator import PDFGenerator
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm

console = Console()


class GameSession:
    """Tracks game events for PDF story generation."""
    
    def __init__(self, character: DnD5eCharacter):
        self.character = character
        self.events: List[Dict[str, Any]] = []
        self.start_time = datetime.now()
        
    def add_event(self, event_type: str, description: str, details: Dict[str, Any] = None):
        """Add an event to the session log."""
        self.events.append({
            "type": event_type,
            "description": description,
            "details": details or {},
            "timestamp": datetime.now()
        })
    
    def to_story_markdown(self) -> str:
        """Convert session events into a narrative story."""
        story = f"""# The Tavern Adventure: {self.character.name}'s Story

*Generated on {self.start_time.strftime('%B %d, %Y at %I:%M %p')}*

---

## Chapter 1: Awakening

The story begins when **{self.character.name}** awakens in a dimly lit tavern, with no memory of how they arrived there. The air is thick with the smell of ale and sawdust, and the flickering candlelight casts long shadows across the room.

### Character Profile

**Name:** {self.character.name}  
**Level:** {self.character.level}  
**Class:** Fighter  
**Hit Points:** {self.character.hp}/{self.character.max_hp}  
**Armor Class:** {self.character.ac}

**Ability Scores:**
- **Strength:** {self.character.strength} (Modifier: {self.character.str_modifier:+d})
- **Dexterity:** {self.character.dexterity} (Modifier: {self.character.dex_modifier:+d})
- **Constitution:** {self.character.constitution} (Modifier: {self.character.con_modifier:+d})
- **Intelligence:** {self.character.intelligence} (Modifier: {self.character.int_modifier:+d})
- **Wisdom:** {self.character.wisdom} (Modifier: {self.character.wis_modifier:+d})
- **Charisma:** {self.character.charisma} (Modifier: {self.character.cha_modifier:+d})

**Proficiency Bonus:** {self.character.proficiency_bonus:+d}

---

## Chapter 2: The Investigation

"""
        
        # Add events as narrative
        for event in self.events:
            if event["type"] == "choice":
                story += f"\n### {event['description']}\n\n"
                if "roll" in event["details"]:
                    roll = event["details"]["roll"]
                    modifier = event["details"].get("modifier", 0)
                    total = event["details"].get("total", roll + modifier)
                    story += f"*{self.character.name} rolled a {roll} on the d20.* "
                    if modifier != 0:
                        story += f"With a modifier of {modifier:+d}, the total was **{total}**. "
                    story += "\n\n"
                
                if "outcome" in event["details"]:
                    story += f"{event['details']['outcome']}\n\n"
            
            elif event["type"] == "scene":
                story += f"\n### {event['description']}\n\n"
                if "content" in event["details"]:
                    story += f"{event['details']['content']}\n\n"
            
            elif event["type"] == "decision":
                story += f"\n**{self.character.name} decided to:** {event['description']}\n\n"
                if "ending" in event["details"]:
                    # Clean up rich formatting tags for markdown
                    ending_text = event['details']['ending']
                    # Remove rich markup like [bold] and [/bold]
                    ending_text = re.sub(r'\[/?bold\]', '**', ending_text)
                    ending_text = re.sub(r'\[/?[^\]]+\]', '', ending_text)  # Remove other rich tags
                    story += f"{ending_text}\n\n"
        
        story += "\n---\n\n"
        story += "## Epilogue\n\n"
        story += f"*The adventure of {self.character.name} continues...*\n\n"
        story += f"*Final Status: {self.character.hp}/{self.character.max_hp} HP, AC {self.character.ac}*\n"
        
        return story


def print_scenario(text: str, style: str = "bold cyan"):
    """Print scenario text in a styled panel."""
    console.print(Panel(text, style=style, border_style="bright_blue"))


def print_action(text: str):
    """Print action text."""
    console.print(f"[yellow]→[/yellow] {text}")


def print_result(text: str):
    """Print result text."""
    console.print(f"[green]✓[/green] {text}")


def create_character() -> DnD5eCharacter:
    """Create a starting character for the scenario."""
    console.print("\n[bold]Creating Your Character...[/bold]\n")
    
    name = Prompt.ask("What is your name?", default="Adventurer")
    
    # Roll ability scores (4d6, drop lowest - standard D&D method)
    console.print("\n[dim]Rolling ability scores (4d6, drop lowest)...[/dim]")
    
    def roll_ability_score() -> int:
        """Roll 4d6, drop lowest."""
        rolls = []
        for _ in range(4):
            rolls.append(DnDRoller.roll("1d6"))
        rolls.sort(reverse=True)
        # Drop lowest, sum top 3
        return sum(rolls[:3])
    
    strength = roll_ability_score()
    dexterity = roll_ability_score()
    constitution = roll_ability_score()
    intelligence = roll_ability_score()
    wisdom = roll_ability_score()
    charisma = roll_ability_score()
    
    console.print(f"  STR: {strength}  DEX: {dexterity}  CON: {constitution}")
    console.print(f"  INT: {intelligence}  WIS: {wisdom}  CHA: {charisma}")
    
    # Calculate modifiers
    str_mod = DnD5eStats.ability_modifier(strength)
    con_mod = DnD5eStats.ability_modifier(constitution)
    
    # Calculate starting HP (level 1: hit_die + CON modifier, max at level 1)
    hit_die = 10  # Fighter hit die
    max_hp = hit_die + con_mod
    
    character = DnD5eCharacter(
        name=name,
        level=1,
        char_class="fighter",
        hit_die=hit_die,
        strength=strength,
        dexterity=dexterity,
        constitution=constitution,
        intelligence=intelligence,
        wisdom=wisdom,
        charisma=charisma,
        hp=max_hp,
        max_hp=max_hp,
        armor_type=ArmorType.NONE,  # Woke up without armor
    )
    
    console.print(f"\n[bold green]Character Created![/bold green]")
    console.print(f"  Name: {character.name}")
    console.print(f"  Level: {character.level}")
    console.print(f"  HP: {character.hp}/{character.max_hp}")
    console.print(f"  AC: {character.ac}")
    console.print(f"  STR Modifier: {str_mod:+d}")
    console.print(f"  Proficiency Bonus: {character.proficiency_bonus:+d}")
    
    return character


def tavern_scenario(character: DnD5eCharacter, session: GameSession):
    """Run the tavern scenario."""
    
    opening_text = (
        "You wake up with a pounding headache. The smell of ale and sawdust fills your nostrils.\n\n"
        "You're lying on a rough wooden floor, surrounded by empty tankards and sleeping patrons.\n"
        "The tavern is dimly lit by a few flickering candles. Your memory is hazy...\n\n"
        "How did you get here? What happened last night?"
    )
    
    print_scenario(opening_text)
    session.add_event("scene", "The Awakening", {"content": opening_text})
    
    # First choice: How do you react?
    console.print("\n[bold]What do you do?[/bold]")
    console.print("1. [cyan]Stand up slowly[/cyan] and look around (Perception check)")
    console.print("2. [cyan]Check your pockets[/cyan] for clues (Investigation check)")
    console.print("3. [cyan]Ask the bartender[/cyan] what happened (Persuasion check)")
    console.print("4. [cyan]Try to remember[/cyan] last night (Intelligence check)")
    
    choice = Prompt.ask("\nYour choice", choices=["1", "2", "3", "4"], default="1")
    
    if choice == "1":
        # Perception check (WIS)
        action_text = "You stand up slowly, trying to get your bearings..."
        print_action(action_text)
        roll, _ = DnDRoller.attack_roll()
        wis_mod = character.wis_modifier
        prof = character.proficiency_bonus
        # Assume not proficient in Perception for level 1
        total = roll + wis_mod
        
        console.print(f"\n[dim]Roll: {roll} + WIS modifier ({wis_mod:+d}) = {total}[/dim]")
        
        if total >= 15:
            outcome = (
                "You notice a strange symbol carved into the table near you - "
                "a crescent moon with a dagger through it. You also see a note "
                "sticking out of your boot."
            )
            print_result(outcome)
            found_note = True
        elif total >= 10:
            outcome = (
                "You see the tavern is mostly empty except for a few sleeping drunks. "
                "The bartender is cleaning glasses behind the bar, watching you warily."
            )
            print_result(outcome)
            found_note = False
        else:
            outcome = (
                "Your head is still spinning. You can't make out much in the dim light. "
                "The bartender glances at you but says nothing."
            )
            print_result(outcome)
            found_note = False
        
        session.add_event("choice", "Perception Check: Stand up and look around", {
            "roll": roll,
            "modifier": wis_mod,
            "total": total,
            "outcome": outcome,
            "success": total >= 15
        })
    
    elif choice == "2":
        # Investigation check (INT)
        print_action("You pat down your pockets and check your belongings...")
        roll, _ = DnDRoller.attack_roll()
        int_mod = character.int_modifier
        total = roll + int_mod
        
        console.print(f"\n[dim]Roll: {roll} + INT modifier ({int_mod:+d}) = {total}[/dim]")
        
        if total >= 12:
            print_result(
                "You find a crumpled note in your pocket. It reads: 'Meet at the old mill. "
                "Midnight. Come alone. - The Shadow'"
            )
            found_note = True
        else:
            print_result(
                "You find some loose coins and a few trinkets, but nothing that explains "
                "how you got here. Your memory is still foggy."
            )
            found_note = False
    
    elif choice == "3":
        # Persuasion check (CHA)
        action_text = "You approach the bartender..."
        print_action(action_text)
        roll, _ = DnDRoller.attack_roll()
        cha_mod = character.cha_modifier
        total = roll + cha_mod
        
        console.print(f"\n[dim]Roll: {roll} + CHA modifier ({cha_mod:+d}) = {total}[/dim]")
        
        if total >= 15:
            outcome = (
                "The bartender looks you over and says: 'You came in here last night with "
                "a group. They left you here, said you'd 'come to' eventually. Paid me "
                "extra to keep an eye on you. Strange folk, those ones.'"
            )
            print_result(outcome)
            found_note = False
        elif total >= 10:
            outcome = (
                "The bartender grunts: 'You owe me 5 gold for the room. Pay up or get out.'"
            )
            print_result(outcome)
            found_note = False
        else:
            outcome = (
                "The bartender glares at you: 'I don't know nothing. Now get out before "
                "I call the guards.'"
            )
            print_result(outcome)
            found_note = False
        
        session.add_event("choice", "Persuasion Check: Ask the bartender", {
            "roll": roll,
            "modifier": cha_mod,
            "total": total,
            "outcome": outcome,
            "success": total >= 15
        })
    
    else:  # choice == "4"
        # Intelligence check (INT)
        print_action("You close your eyes and try to piece together last night...")
        roll, _ = DnDRoller.attack_roll()
        int_mod = character.int_modifier
        total = roll + int_mod
        
        console.print(f"\n[dim]Roll: {roll} + INT modifier ({int_mod:+d}) = {total}[/dim]")
        
        if total >= 15:
            print_result(
                "Fragments come back to you: You were meeting someone. There was a job offer. "
                "Something about retrieving an artifact. The meeting was supposed to be secret. "
                "Then... nothing. You must have been drugged."
            )
            found_note = False
        elif total >= 10:
            print_result(
                "You remember bits and pieces: A tavern, a meeting, voices. But the details "
                "are lost in the fog of whatever happened to you."
            )
            found_note = False
        else:
            print_result(
                "Your mind is a complete blank. Whatever happened last night, it's gone. "
                "You'll need to find another way to figure this out."
            )
            found_note = False
    
    # Next scene: A stranger approaches
    stranger_scene = (
        "\nAs you're trying to make sense of things, a cloaked figure approaches your table.\n\n"
        "'You're awake,' they say in a low voice. 'Good. We need to talk. But not here.'\n\n"
        "They slide a note across the table and disappear into the shadows before you can respond."
    )
    print_scenario(stranger_scene)
    session.add_event("scene", "The Mysterious Stranger", {"content": stranger_scene})
    
    # Read the note
    read_note = Confirm.ask("\nDo you read the note?", default=True)
    if read_note:
        note_content = (
            "\n[bold]The Note:[/bold]\n\n"
            "'You were chosen for a reason. Meet me at the old mill outside town at midnight. "
            "Come alone, or don't come at all. Your life depends on it.\n\n"
            "- The Shadow'\n\n"
            "The note is signed with the same symbol you saw earlier: a crescent moon with a dagger."
        )
        print_scenario(note_content)
        session.add_event("scene", "Reading the Note", {"content": note_content})
    else:
        session.add_event("decision", "Decided not to read the note", {})
    
    # Final choice: What do you do?
    console.print("\n[bold]What do you do next?[/bold]")
    console.print("1. [cyan]Follow the note[/cyan] - Go to the old mill")
    console.print("2. [cyan]Ask around town[/cyan] - Try to learn more first")
    console.print("3. [cyan]Ignore it[/cyan] - Leave town and forget this ever happened")
    
    final_choice = Prompt.ask("\nYour choice", choices=["1", "2", "3"], default="1")
    
    if final_choice == "1":
        ending = (
            "\n[bold]To Be Continued...[/bold]\n\n"
            "You decide to follow the note. As you leave the tavern, you feel eyes watching you.\n"
            "The old mill awaits. What secrets does it hold?\n\n"
            "Your adventure has just begun."
        )
        print_scenario(ending)
        session.add_event("decision", "Follow the note - Go to the old mill", {"ending": ending})
    elif final_choice == "2":
        ending = (
            "\n[bold]To Be Continued...[/bold]\n\n"
            "You decide to gather more information first. The townsfolk might know something "
            "about 'The Shadow' or the old mill. But time is running out...\n\n"
            "Your investigation begins."
        )
        print_scenario(ending)
        session.add_event("decision", "Ask around town - Gather more information", {"ending": ending})
    else:
        ending = (
            "\n[bold]The End?[/bold]\n\n"
            "You decide to leave town and forget this ever happened. But as you walk away, "
            "you can't shake the feeling that this isn't over. The Shadow will find you again.\n\n"
            "Or maybe... you'll find them first."
        )
        print_scenario(ending)
        session.add_event("decision", "Ignore it - Leave town", {"ending": ending})
    
    # Show final character state
    console.print("\n[bold]Final Character State:[/bold]")
    console.print(f"  Name: {character.name}")
    console.print(f"  HP: {character.hp}/{character.max_hp}")
    console.print(f"  AC: {character.ac}")
    console.print(f"  Status Effects: {character.status_effects or 'None'}")


def generate_pdf_story(session: GameSession) -> Path:
    """Generate PDF story and save to desktop."""
    console.print("\n[yellow]→[/yellow] Generating your adventure story PDF...")
    
    # Get desktop path
    desktop_path = Path.home() / "Desktop"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"Tavern_Adventure_{session.character.name}_{timestamp}.pdf"
    pdf_path = desktop_path / pdf_filename
    
    # Generate markdown story
    story_markdown = session.to_story_markdown()
    
    # Generate PDF
    try:
        generator = PDFGenerator.from_content(
            content=story_markdown,
            title=f"The Tavern Adventure: {session.character.name}'s Story",
            style="premium"
        )
        
        pdf_path = generator.save(
            output_path=pdf_path,
            open_pdf=False,  # We'll open manually
            convert_to_png=False  # No need for PNG
        )
        
        console.print(f"[green]✓[/green] PDF generated: {pdf_path}")
        
        # Open PDF automatically
        console.print("[yellow]→[/yellow] Opening PDF on desktop...")
        system = platform.system()
        if system == "Darwin":  # macOS
            subprocess.run(["open", str(pdf_path)], check=False)
        elif system == "Windows":
            subprocess.run(["start", str(pdf_path)], shell=True, check=False)
        else:  # Linux
            subprocess.run(["xdg-open", str(pdf_path)], check=False)
        
        console.print(f"[green]✓[/green] PDF opened on desktop!")
        return pdf_path
        
    except Exception as e:
        console.print(f"[red]✗[/red] PDF generation failed: {e}")
        # Fallback: save markdown
        md_path = desktop_path / pdf_filename.replace(".pdf", ".md")
        md_path.write_text(story_markdown)
        console.print(f"[yellow]⚠[/yellow]  Markdown saved instead: {md_path}")
        return md_path


def main():
    """Main scenario runner."""
    console.print("\n[bold bright_blue]╔════════════════════════════════════════╗[/bold bright_blue]")
    console.print("[bold bright_blue]║[/bold bright_blue]  [bold white]TOWN TAVERN SCENARIO[/bold white]  [bold bright_blue]║[/bold bright_blue]")
    console.print("[bold bright_blue]║[/bold bright_blue]  [dim]A D&D 5e Adventure[/dim]  [bold bright_blue]║[/bold bright_blue]")
    console.print("[bold bright_blue]╚════════════════════════════════════════╝[/bold bright_blue]\n")
    
    # Create character
    character = create_character()
    
    # Create game session tracker
    session = GameSession(character)
    session.add_event("scene", "Character Creation", {
        "character_name": character.name,
        "stats": {
            "strength": character.strength,
            "dexterity": character.dexterity,
            "constitution": character.constitution,
            "intelligence": character.intelligence,
            "wisdom": character.wisdom,
            "charisma": character.charisma
        }
    })
    
    # Run scenario
    tavern_scenario(character, session)
    
    console.print("\n[bold green]✓ Scenario Complete![/bold green]\n")
    
    # Generate PDF story
    pdf_path = generate_pdf_story(session)
    
    console.print(f"\n[bold green]🎉 Your adventure story is ready![/bold green]")
    console.print(f"[dim]Saved to: {pdf_path}[/dim]\n")


if __name__ == "__main__":
    main()
