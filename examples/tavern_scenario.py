"""
Town Tavern Scenario - Waking Up

A classic D&D scenario: You wake up in a tavern, not remembering how you got there.
Your character has D&D 5e stats, and you'll need to use them to navigate the situation.

This demonstrates the D&D 5e physics engine integration with WAFT Beings.
"""

from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.core.dnd5e import (
    DnD5eCharacter,
    DnD5eStats,
    DnDRoller,
    DnD5eCombat,
    ArmorType
)
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm

console = Console()


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


def tavern_scenario(character: DnD5eCharacter):
    """Run the tavern scenario."""
    
    print_scenario(
        "You wake up with a pounding headache. The smell of ale and sawdust fills your nostrils.\n\n"
        "You're lying on a rough wooden floor, surrounded by empty tankards and sleeping patrons.\n"
        "The tavern is dimly lit by a few flickering candles. Your memory is hazy...\n\n"
        "How did you get here? What happened last night?"
    )
    
    # First choice: How do you react?
    console.print("\n[bold]What do you do?[/bold]")
    console.print("1. [cyan]Stand up slowly[/cyan] and look around (Perception check)")
    console.print("2. [cyan]Check your pockets[/cyan] for clues (Investigation check)")
    console.print("3. [cyan]Ask the bartender[/cyan] what happened (Persuasion check)")
    console.print("4. [cyan]Try to remember[/cyan] last night (Intelligence check)")
    
    choice = Prompt.ask("\nYour choice", choices=["1", "2", "3", "4"], default="1")
    
    if choice == "1":
        # Perception check (WIS)
        print_action("You stand up slowly, trying to get your bearings...")
        roll, _ = DnDRoller.attack_roll()
        wis_mod = character.wis_modifier
        prof = character.proficiency_bonus
        # Assume not proficient in Perception for level 1
        total = roll + wis_mod
        
        console.print(f"\n[dim]Roll: {roll} + WIS modifier ({wis_mod:+d}) = {total}[/dim]")
        
        if total >= 15:
            print_result(
                "You notice a strange symbol carved into the table near you - "
                "a crescent moon with a dagger through it. You also see a note "
                "sticking out of your boot."
            )
            found_note = True
        elif total >= 10:
            print_result(
                "You see the tavern is mostly empty except for a few sleeping drunks. "
                "The bartender is cleaning glasses behind the bar, watching you warily."
            )
            found_note = False
        else:
            print_result(
                "Your head is still spinning. You can't make out much in the dim light. "
                "The bartender glances at you but says nothing."
            )
            found_note = False
    
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
        print_action("You approach the bartender...")
        roll, _ = DnDRoller.attack_roll()
        cha_mod = character.cha_modifier
        total = roll + cha_mod
        
        console.print(f"\n[dim]Roll: {roll} + CHA modifier ({cha_mod:+d}) = {total}[/dim]")
        
        if total >= 15:
            print_result(
                "The bartender looks you over and says: 'You came in here last night with "
                "a group. They left you here, said you'd 'come to' eventually. Paid me "
                "extra to keep an eye on you. Strange folk, those ones.'"
            )
            found_note = False
        elif total >= 10:
            print_result(
                "The bartender grunts: 'You owe me 5 gold for the room. Pay up or get out.'"
            )
            found_note = False
        else:
            print_result(
                "The bartender glares at you: 'I don't know nothing. Now get out before "
                "I call the guards.'"
            )
            found_note = False
    
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
    print_scenario(
        "\nAs you're trying to make sense of things, a cloaked figure approaches your table.\n\n"
        "'You're awake,' they say in a low voice. 'Good. We need to talk. But not here.'\n\n"
        "They slide a note across the table and disappear into the shadows before you can respond."
    )
    
    # Read the note
    if Confirm.ask("\nDo you read the note?", default=True):
        print_scenario(
            "\n[bold]The Note:[/bold]\n\n"
            "'You were chosen for a reason. Meet me at the old mill outside town at midnight. "
            "Come alone, or don't come at all. Your life depends on it.\n\n"
            "- The Shadow'\n\n"
            "The note is signed with the same symbol you saw earlier: a crescent moon with a dagger."
        )
    
    # Final choice: What do you do?
    console.print("\n[bold]What do you do next?[/bold]")
    console.print("1. [cyan]Follow the note[/cyan] - Go to the old mill")
    console.print("2. [cyan]Ask around town[/cyan] - Try to learn more first")
    console.print("3. [cyan]Ignore it[/cyan] - Leave town and forget this ever happened")
    
    final_choice = Prompt.ask("\nYour choice", choices=["1", "2", "3"], default="1")
    
    if final_choice == "1":
        print_scenario(
            "\n[bold]To Be Continued...[/bold]\n\n"
            "You decide to follow the note. As you leave the tavern, you feel eyes watching you.\n"
            "The old mill awaits. What secrets does it hold?\n\n"
            "Your adventure has just begun."
        )
    elif final_choice == "2":
        print_scenario(
            "\n[bold]To Be Continued...[/bold]\n\n"
            "You decide to gather more information first. The townsfolk might know something "
            "about 'The Shadow' or the old mill. But time is running out...\n\n"
            "Your investigation begins."
        )
    else:
        print_scenario(
            "\n[bold]The End?[/bold]\n\n"
            "You decide to leave town and forget this ever happened. But as you walk away, "
            "you can't shake the feeling that this isn't over. The Shadow will find you again.\n\n"
            "Or maybe... you'll find them first."
        )
    
    # Show final character state
    console.print("\n[bold]Final Character State:[/bold]")
    console.print(f"  Name: {character.name}")
    console.print(f"  HP: {character.hp}/{character.max_hp}")
    console.print(f"  AC: {character.ac}")
    console.print(f"  Status Effects: {character.status_effects or 'None'}")


def main():
    """Main scenario runner."""
    console.print("\n[bold bright_blue]╔════════════════════════════════════════╗[/bold bright_blue]")
    console.print("[bold bright_blue]║[/bold bright_blue]  [bold white]TOWN TAVERN SCENARIO[/bold white]  [bold bright_blue]║[/bold bright_blue]")
    console.print("[bold bright_blue]║[/bold bright_blue]  [dim]A D&D 5e Adventure[/dim]  [bold bright_blue]║[/bold bright_blue]")
    console.print("[bold bright_blue]╚════════════════════════════════════════╝[/bold bright_blue]\n")
    
    # Create character
    character = create_character()
    
    # Run scenario
    tavern_scenario(character)
    
    console.print("\n[bold green]✓ Scenario Complete![/bold green]\n")


if __name__ == "__main__":
    main()
