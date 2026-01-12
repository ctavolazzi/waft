"""
Town Tavern Scenario - Evolved with WAFT Being System

An evolved version of the tavern scenario that uses WAFT Beings to make decisions
automatically. The Being learns from experiences and evolves over multiple runs.

This demonstrates:
- WAFT Being system integration
- Automatic decision-making based on skills and personality
- Evolutionary learning from past experiences
- D&D 5e physics engine
"""

from pathlib import Path
import sys
import random
from typing import Optional, Dict, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.core.dnd5e import (
    DnD5eCharacter,
    DnD5eStats,
    DnDRoller,
    ArmorType
)
from waft.being import Being, BeingState
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from datetime import datetime

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


def print_being_decision(being: Being, choice: str, reasoning: str):
    """Print Being's decision with reasoning."""
    console.print(f"\n[dim][Being {being.being_id[:8]}...][/dim]")
    console.print(f"[cyan]Decision:[/cyan] {choice}")
    console.print(f"[dim]Reasoning: {reasoning}[/dim]")


def create_character(being: Being) -> DnD5eCharacter:
    """Create a D&D character based on Being's skills and attributes."""
    console.print("\n[bold]Creating Character from Being...[/bold]\n")
    
    # Map Being skills to D&D ability scores
    # Higher skills = better ability scores
    def skill_to_ability(skill_level: float) -> int:
        """Convert skill level (0-100) to ability score (8-18)."""
        # Map 0-100 to 8-18
        base = 8
        bonus = int((skill_level / 100.0) * 10)
        return min(18, base + bonus)
    
    # Use Being's skills if available, otherwise roll
    if "strength" in being.skills:
        strength = skill_to_ability(being.skills.get("strength", 50))
    else:
        strength = roll_ability_score()
    
    if "dexterity" in being.skills:
        dexterity = skill_to_ability(being.skills.get("dexterity", 50))
    else:
        dexterity = roll_ability_score()
    
    if "constitution" in being.skills:
        constitution = skill_to_ability(being.skills.get("constitution", 50))
    else:
        constitution = roll_ability_score()
    
    if "intelligence" in being.skills:
        intelligence = skill_to_ability(being.skills.get("intelligence", 50))
    else:
        intelligence = roll_ability_score()
    
    if "wisdom" in being.skills:
        wisdom = skill_to_ability(being.skills.get("wisdom", 50))
    else:
        wisdom = roll_ability_score()
    
    if "charisma" in being.skills:
        charisma = skill_to_ability(being.skills.get("charisma", 50))
    else:
        charisma = roll_ability_score()
    
    console.print(f"  STR: {strength}  DEX: {dexterity}  CON: {constitution}")
    console.print(f"  INT: {intelligence}  WIS: {wisdom}  CHA: {charisma}")
    
    # Calculate modifiers
    con_mod = DnD5eStats.ability_modifier(constitution)
    
    # Calculate starting HP
    hit_die = 10  # Fighter hit die
    max_hp = hit_die + con_mod
    
    character = DnD5eCharacter(
        name=f"Being-{being.being_id[:8]}",
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
        armor_type=ArmorType.NONE,
    )
    
    console.print(f"\n[bold green]Character Created![/bold green]")
    console.print(f"  Name: {character.name}")
    console.print(f"  Level: {character.level}")
    console.print(f"  HP: {character.hp}/{character.max_hp}")
    console.print(f"  AC: {character.ac}")
    
    return character


def roll_ability_score() -> int:
    """Roll 4d6, drop lowest."""
    rolls = []
    for _ in range(4):
        rolls.append(DnDRoller.roll("1d6"))
    rolls.sort(reverse=True)
    return sum(rolls[:3])


def being_make_choice(being: Being, character: DnD5eCharacter, choices: Dict[str, Dict[str, Any]]) -> str:
    """
    Have the Being make a choice based on its skills, personality, and memories.
    
    Args:
        being: The Being making the decision
        character: The D&D character
        choices: Dict of choice_id -> {description, skill_type, dc}
    
    Returns:
        Choice ID (e.g., "1", "2", "3")
    """
    # Analyze choices based on Being's skills and character's abilities
    choice_scores = {}
    
    for choice_id, choice_info in choices.items():
        score = 0.0
        
        # Base score from Being's relevant skill
        skill_type = choice_info.get("skill_type", "")
        if skill_type in being.skills:
            score += being.skills[skill_type] / 10.0
        
        # Bonus from character's ability modifier
        if skill_type == "perception":
            score += character.wis_modifier * 2
        elif skill_type == "investigation":
            score += character.int_modifier * 2
        elif skill_type == "persuasion":
            score += character.cha_modifier * 2
        elif skill_type == "intelligence":
            score += character.int_modifier * 2
        
        # Personality influence
        if being.personality_type == "analytical" and skill_type in ["investigation", "intelligence"]:
            score += 5.0
        elif being.personality_type == "intuitive" and skill_type == "perception":
            score += 5.0
        elif being.personality_type == "creative" and skill_type == "persuasion":
            score += 5.0
        
        # Learn from past memories
        for memory in being.memories:
            metadata = memory.get("metadata", {})
            if metadata.get("choice") == choice_id:
                if metadata.get("success", False):
                    score += 3.0  # Prefer choices that worked before
                else:
                    score -= 1.0  # Avoid choices that failed
        
        # Add some randomness (luck factor)
        luck_bonus = (being.luck - 50.0) / 10.0
        score += luck_bonus + random.uniform(-2.0, 2.0)
        
        choice_scores[choice_id] = score
    
    # Select best choice
    best_choice = max(choice_scores.items(), key=lambda x: x[1])[0]
    
    # Generate reasoning
    reasoning = f"Chose option {best_choice} (score: {choice_scores[best_choice]:.1f})"
    if skill_type in being.skills:
        reasoning += f" based on {skill_type} skill ({being.skills[skill_type]:.1f})"
    
    return best_choice, reasoning


def tavern_scenario_evolved(being: Being, character: DnD5eCharacter) -> Dict[str, Any]:
    """Run the tavern scenario with a Being making decisions."""
    
    results = {
        "found_note": False,
        "read_note": True,
        "final_choice": "1",
        "fitness_gained": 0.0
    }
    
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
    
    choices = {
        "1": {"description": "Stand up slowly", "skill_type": "perception", "dc": 15},
        "2": {"description": "Check your pockets", "skill_type": "investigation", "dc": 12},
        "3": {"description": "Ask the bartender", "skill_type": "persuasion", "dc": 15},
        "4": {"description": "Try to remember", "skill_type": "intelligence", "dc": 15}
    }
    
    choice, reasoning = being_make_choice(being, character, choices)
    print_being_decision(being, choices[choice]["description"], reasoning)
    
    if choice == "1":
        # Perception check (WIS)
        print_action("You stand up slowly, trying to get your bearings...")
        roll, _ = DnDRoller.attack_roll()
        wis_mod = character.wis_modifier
        total = roll + wis_mod
        
        console.print(f"\n[dim]Roll: {roll} + WIS modifier ({wis_mod:+d}) = {total}[/dim]")
        
        if total >= 15:
            print_result(
                "You notice a strange symbol carved into the table near you - "
                "a crescent moon with a dagger through it. You also see a note "
                "sticking out of your boot."
            )
            results["found_note"] = True
            results["fitness_gained"] += 10.0
            being.record_memory(
                f"Successfully found note using {choices[choice]['description']}",
                memory_type="success",
                metadata={"choice": choice, "success": True, "fitness": 10.0}
            )
        elif total >= 10:
            print_result(
                "You see the tavern is mostly empty except for a few sleeping drunks. "
                "The bartender is cleaning glasses behind the bar, watching you warily."
            )
            results["fitness_gained"] += 5.0
            being.record_memory(
                f"Partial success with {choices[choice]['description']}",
                memory_type="partial",
                metadata={"choice": choice, "success": False, "fitness": 5.0}
            )
        else:
            print_result(
                "Your head is still spinning. You can't make out much in the dim light. "
                "The bartender glances at you but says nothing."
            )
            results["fitness_gained"] += 2.0
            being.record_memory(
                f"Failed with {choices[choice]['description']}",
                memory_type="failure",
                metadata={"choice": choice, "success": False, "fitness": 2.0}
            )
    
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
            results["found_note"] = True
            results["fitness_gained"] += 10.0
            being.record_memory(
                f"Successfully found note using {choices[choice]['description']}",
                memory_type="success",
                metadata={"choice": choice, "success": True, "fitness": 10.0}
            )
        else:
            print_result(
                "You find some loose coins and a few trinkets, but nothing that explains "
                "how you got here. Your memory is still foggy."
            )
            results["fitness_gained"] += 3.0
            being.record_memory(
                f"Partial success with {choices[choice]['description']}",
                memory_type="partial",
                metadata={"choice": choice, "success": False, "fitness": 3.0}
            )
    
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
            results["fitness_gained"] += 8.0
            being.record_memory(
                f"Successfully persuaded bartender using {choices[choice]['description']}",
                memory_type="success",
                metadata={"choice": choice, "success": True, "fitness": 8.0}
            )
        elif total >= 10:
            print_result(
                "The bartender grunts: 'You owe me 5 gold for the room. Pay up or get out.'"
            )
            results["fitness_gained"] += 4.0
            being.record_memory(
                f"Partial success with {choices[choice]['description']}",
                memory_type="partial",
                metadata={"choice": choice, "success": False, "fitness": 4.0}
            )
        else:
            print_result(
                "The bartender glares at you: 'I don't know nothing. Now get out before "
                "I call the guards.'"
            )
            results["fitness_gained"] += 1.0
            being.record_memory(
                f"Failed with {choices[choice]['description']}",
                memory_type="failure",
                metadata={"choice": choice, "success": False, "fitness": 1.0}
            )
    
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
            results["fitness_gained"] += 7.0
            being.record_memory(
                f"Successfully remembered using {choices[choice]['description']}",
                memory_type="success",
                metadata={"choice": choice, "success": True, "fitness": 7.0}
            )
        elif total >= 10:
            print_result(
                "You remember bits and pieces: A tavern, a meeting, voices. But the details "
                "are lost in the fog of whatever happened to you."
            )
            results["fitness_gained"] += 4.0
            being.record_memory(
                f"Partial success with {choices[choice]['description']}",
                memory_type="partial",
                metadata={"choice": choice, "success": False, "fitness": 4.0}
            )
        else:
            print_result(
                "Your mind is a complete blank. Whatever happened last night, it's gone. "
                "You'll need to find another way to figure this out."
            )
            results["fitness_gained"] += 1.0
            being.record_memory(
                f"Failed with {choices[choice]['description']}",
                memory_type="failure",
                metadata={"choice": choice, "success": False, "fitness": 1.0}
            )
    
    # Next scene: A stranger approaches
    print_scenario(
        "\nAs you're trying to make sense of things, a cloaked figure approaches your table.\n\n"
        "'You're awake,' they say in a low voice. 'Good. We need to talk. But not here.'\n\n"
        "They slide a note across the table and disappear into the shadows before you can respond."
    )
    
    # Being decides to read the note (based on curiosity/personality)
    read_note = True  # Most beings would read it
    if being.personality_type == "analytical":
        read_note = True  # Always read
    elif being.personality_type == "intuitive":
        read_note = random.random() > 0.2  # 80% chance
    
    results["read_note"] = read_note
    
    if read_note:
        print_scenario(
            "\n[bold]The Note:[/bold]\n\n"
            "'You were chosen for a reason. Meet me at the old mill outside town at midnight. "
            "Come alone, or don't come at all. Your life depends on it.\n\n"
            "- The Shadow'\n\n"
            "The note is signed with the same symbol you saw earlier: a crescent moon with a dagger."
        )
        results["fitness_gained"] += 5.0
    
    # Final choice: What do you do?
    console.print("\n[bold]What do you do next?[/bold]")
    console.print("1. [cyan]Follow the note[/cyan] - Go to the old mill")
    console.print("2. [cyan]Ask around town[/cyan] - Try to learn more first")
    console.print("3. [cyan]Ignore it[/cyan] - Leave town and forget this ever happened")
    
    final_choices = {
        "1": {"description": "Follow the note", "skill_type": "courage", "fitness": 15.0},
        "2": {"description": "Ask around town", "skill_type": "investigation", "fitness": 10.0},
        "3": {"description": "Ignore it", "skill_type": "wisdom", "fitness": 5.0}
    }
    
    final_choice, reasoning = being_make_choice(being, character, final_choices)
    print_being_decision(being, final_choices[final_choice]["description"], reasoning)
    results["final_choice"] = final_choice
    
    if final_choice == "1":
        print_scenario(
            "\n[bold]To Be Continued...[/bold]\n\n"
            "You decide to follow the note. As you leave the tavern, you feel eyes watching you.\n"
            "The old mill awaits. What secrets does it hold?\n\n"
            "Your adventure has just begun."
        )
        results["fitness_gained"] += 15.0
    elif final_choice == "2":
        print_scenario(
            "\n[bold]To Be Continued...[/bold]\n\n"
            "You decide to gather more information first. The townsfolk might know something "
            "about 'The Shadow' or the old mill. But time is running out...\n\n"
            "Your investigation begins."
        )
        results["fitness_gained"] += 10.0
    else:
        print_scenario(
            "\n[bold]The End?[/bold]\n\n"
            "You decide to leave town and forget this ever happened. But as you walk away, "
            "you can't shake the feeling that this isn't over. The Shadow will find you again.\n\n"
            "Or maybe... you'll find them first."
        )
        results["fitness_gained"] += 5.0
    
    # Update Being's fitness
    being.fitness += results["fitness_gained"]
    
    # Learn from experience - improve relevant skills
    if choice in ["1", "2", "3", "4"]:
        skill_type = choices[choice]["skill_type"]
        if skill_type in being.skills:
            # Improve skill based on success
            improvement = 0.5 if results["fitness_gained"] >= 8.0 else 0.2
            being.skills[skill_type] = min(100.0, being.skills[skill_type] + improvement)
        else:
            being.skills[skill_type] = 1.0  # Start learning
    
    # Show final character state
    console.print("\n[bold]Final Character State:[/bold]")
    console.print(f"  Name: {character.name}")
    console.print(f"  HP: {character.hp}/{character.max_hp}")
    console.print(f"  AC: {character.ac}")
    
    # Show Being evolution
    console.print("\n[bold]Being Evolution:[/bold]")
    console.print(f"  Fitness: {being.fitness:.1f}")
    console.print(f"  Skills: {len(being.skills)} skills learned")
    console.print(f"  Memories: {len(being.memories)} experiences")
    
    return results


def main():
    """Main scenario runner with evolution."""
    console.print("\n[bold bright_blue]╔════════════════════════════════════════╗[/bold bright_blue]")
    console.print("[bold bright_blue]║[/bold bright_blue]  [bold white]TOWN TAVERN SCENARIO - EVOLVED[/bold white]  [bold bright_blue]║[/bold bright_blue]")
    console.print("[bold bright_blue]║[/bold bright_blue]  [dim]WAFT Being + D&D 5e Adventure[/dim]  [bold bright_blue]║[/bold bright_blue]")
    console.print("[bold bright_blue]╚════════════════════════════════════════╝[/bold bright_blue]\n")
    
    # Create a Being
    being = Being(
        being_id=f"tavern_being_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        reality_id="tavern_scenario",
        personality_type="analytical",  # Start with analytical personality
        skills={
            "perception": 30.0,
            "investigation": 40.0,
            "persuasion": 25.0,
            "intelligence": 35.0,
        }
    )
    
    console.print(f"[dim]Created Being: {being.being_id}[/dim]")
    console.print(f"[dim]Personality: {being.personality_type}[/dim]\n")
    
    # Create character from Being
    character = create_character(being)
    
    # Run scenario
    results = tavern_scenario_evolved(being, character)
    
    # Show evolution summary
    console.print("\n[bold green]✓ Scenario Complete![/bold green]")
    console.print(f"\n[bold]Evolution Summary:[/bold]")
    console.print(f"  Total Fitness Gained: {results['fitness_gained']:.1f}")
    console.print(f"  Being Fitness: {being.fitness:.1f}")
    console.print(f"  Skills Improved: {len([s for s in being.skills.values() if s > 0])}")
    console.print(f"  Memories Stored: {len(being.memories)}")
    
    # Show skill progression
    if being.skills:
        table = Table(title="Skill Progression")
        table.add_column("Skill", style="cyan")
        table.add_column("Level", justify="right", style="green")
        for skill, level in sorted(being.skills.items(), key=lambda x: x[1], reverse=True):
            table.add_row(skill.title(), f"{level:.1f}")
        console.print("\n")
        console.print(table)
    
    console.print("\n[dim]This Being can now be used as a parent for future evolutions![/dim]\n")


if __name__ == "__main__":
    main()
