"""
Interactive D&D Game - A Complete Playable Adventure

A full-featured interactive D&D 5e game featuring:
- Character creation with rolled stats
- Combat encounters with real dice rolling
- Interactive choices affecting the story
- Shop system for equipment
- NPC interactions
- Story generation
- Save/load functionality

Uses all available WAFT D&D tools:
- DnD5eCharacter for character state
- DnDRoller for dice mechanics
- DnD5eCombat for combat resolution
- Rich console for beautiful output
"""

import json
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from waft.core.dnd5e import ArmorType, DnD5eCharacter, DnD5eCombat, DnD5eStats, DnDRoller

console = Console()


class GameState:
    """Tracks game state including character, inventory, gold, and story."""

    def __init__(self, character: DnD5eCharacter):
        self.character = character
        self.gold = 50  # Starting gold
        self.inventory: list[str] = []
        self.story_log: list[str] = []
        self.encounters_completed = 0
        self.game_start_time = datetime.now()

    def to_dict(self) -> dict[str, Any]:
        """Serialize game state to dictionary."""
        return {
            "character": self.character.to_dict(),
            "gold": self.gold,
            "inventory": self.inventory,
            "story_log": self.story_log,
            "encounters_completed": self.encounters_completed,
            "game_start_time": self.game_start_time.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GameState":
        """Load game state from dictionary."""
        character = DnD5eCharacter.from_dict(data["character"])
        state = cls(character)
        state.gold = data.get("gold", 50)
        state.inventory = data.get("inventory", [])
        state.story_log = data.get("story_log", [])
        state.encounters_completed = data.get("encounters_completed", 0)
        if "game_start_time" in data:
            state.game_start_time = datetime.fromisoformat(data["game_start_time"])
        return state


class Shop:
    """Shop system for buying equipment."""

    ITEMS = {
        "sword": {"name": "Longsword", "cost": 15, "type": "weapon", "damage": "1d8"},
        "dagger": {"name": "Dagger", "cost": 2, "type": "weapon", "damage": "1d4"},
        "shield": {"name": "Shield", "cost": 10, "type": "armor", "ac_bonus": 2},
        "leather": {"name": "Leather Armor", "cost": 10, "type": "armor", "ac": 11},
        "chain": {"name": "Chain Mail", "cost": 75, "type": "armor", "ac": 16},
        "potion": {"name": "Healing Potion", "cost": 50, "type": "consumable", "healing": "2d4+2"},
        "rations": {"name": "Rations (1 day)", "cost": 5, "type": "consumable"},
    }

    @classmethod
    def display_shop(cls, game_state: GameState):
        """Display shop and allow purchases."""
        console.print("\n[bold cyan]🏪 THE ADVENTURER'S SHOP 🏪[/bold cyan]\n")
        console.print(f"Your gold: [yellow]{game_state.gold} gp[/yellow]\n")

        table = Table(title="Available Items")
        table.add_column("Item", style="cyan")
        table.add_column("Cost", style="yellow", justify="right")
        table.add_column("Description", style="white")

        for key, item in cls.ITEMS.items():
            desc = f"{item['type'].title()}"
            if "damage" in item:
                desc += f" - {item['damage']} damage"
            if "ac" in item:
                desc += f" - AC {item['ac']}"
            if "ac_bonus" in item:
                desc += f" - +{item['ac_bonus']} AC"
            if "healing" in item:
                desc += f" - {item['healing']} healing"

            table.add_row(item["name"], f"{item['cost']} gp", desc)

        console.print(table)
        console.print("\n")

        while True:
            choice = Prompt.ask(
                "What would you like to buy? (item name or 'leave')", default="leave"
            ).lower()

            if choice == "leave":
                break

            # Find item
            item_key = None
            for key, item in cls.ITEMS.items():
                if key in choice or item["name"].lower() in choice:
                    item_key = key
                    break

            if not item_key:
                console.print("[red]Item not found![/red]")
                continue

            item = cls.ITEMS[item_key]

            if game_state.gold < item["cost"]:
                console.print(
                    f"[red]Not enough gold! You need {item['cost']} gp but only have {game_state.gold} gp.[/red]"
                )
                continue

            # Purchase
            game_state.gold -= item["cost"]
            game_state.inventory.append(item["name"])

            # Apply equipment
            if item["type"] == "weapon":
                game_state.character.equipped_weapon = item["name"]
                console.print(f"[green]✓[/green] Equipped {item['name']}!")
            elif item["type"] == "armor":
                if "ac" in item:
                    game_state.character.armor_type = (
                        ArmorType.MEDIUM if item["ac"] >= 14 else ArmorType.LIGHT
                    )
                    game_state.character.armor_base = item["ac"]
                elif "ac_bonus" in item:
                    game_state.character.armor_base += item["ac_bonus"]
                game_state.character.equipped_armor = item["name"]
                console.print(
                    f"[green]✓[/green] Equipped {item['name']}! AC is now {game_state.character.ac}"
                )

            console.print(f"[green]Purchased {item['name']} for {item['cost']} gp![/green]")
            console.print(f"Remaining gold: [yellow]{game_state.gold} gp[/yellow]\n")


class CombatEncounter:
    """Combat encounter system."""

    ENEMIES = {
        "goblin": {"name": "Goblin", "ac": 15, "hp": 7, "damage": "1d6", "xp": 50},
        "orc": {"name": "Orc", "ac": 13, "hp": 15, "damage": "1d12+3", "xp": 100},
        "skeleton": {"name": "Skeleton", "ac": 13, "hp": 13, "damage": "1d6+2", "xp": 50},
        "bandit": {"name": "Bandit", "ac": 12, "hp": 11, "damage": "1d6", "xp": 25},
        "wolf": {"name": "Wolf", "ac": 13, "hp": 11, "damage": "2d4+2", "xp": 50},
    }

    @classmethod
    def run_combat(cls, game_state: GameState, enemy_type: str = None) -> bool:
        """Run a combat encounter. Returns True if player wins."""
        if not enemy_type:
            enemy_type = random.choice(list(cls.ENEMIES.keys()))

        enemy = cls.ENEMIES[enemy_type].copy()
        enemy["current_hp"] = enemy["hp"]

        console.print(f"\n[bold red]⚔️  COMBAT: {enemy['name']} ⚔️[/bold red]\n")
        console.print(f"Enemy: {enemy['name']} (AC {enemy['ac']}, HP {enemy['hp']})")
        console.print(
            f"You: {game_state.character.name} (AC {game_state.character.ac}, HP {game_state.character.hp}/{game_state.character.max_hp})\n"
        )

        round_num = 1

        while enemy["current_hp"] > 0 and game_state.character.hp > 0:
            console.print(f"[dim]--- Round {round_num} ---[/dim]\n")

            # Player turn
            console.print("[cyan]Your turn![/cyan]")
            action = Prompt.ask(
                "Action: [bold]attack[/bold], [bold]flee[/bold]",
                choices=["attack", "flee"],
                default="attack",
            )

            if action == "flee":
                flee_roll = DnDRoller.roll("1d20") + game_state.character.dex_modifier
                if flee_roll >= 15:
                    console.print("[green]✓[/green] You successfully flee!")
                    return False
                else:
                    console.print("[red]✗[/red] You couldn't escape!")

            # Player attack
            attack_mod = game_state.character.str_modifier + game_state.character.proficiency_bonus
            hit, critical = DnD5eCombat.make_attack_roll(attack_mod, enemy["ac"])

            if hit:
                # Determine damage
                if game_state.character.equipped_weapon:
                    # Use weapon damage if equipped
                    if "sword" in game_state.character.equipped_weapon.lower():
                        damage_dice = "1d8"
                    elif "dagger" in game_state.character.equipped_weapon.lower():
                        damage_dice = "1d4"
                    else:
                        damage_dice = "1d6"  # Default
                else:
                    damage_dice = "1d4"  # Unarmed

                damage = DnDRoller.roll_damage(damage_dice) + game_state.character.str_modifier

                if critical:
                    damage *= 2
                    console.print("[bold yellow]CRITICAL HIT![/bold yellow]")

                enemy["current_hp"] -= damage
                console.print(
                    f"[green]✓[/green] You hit for {damage} damage! ({enemy['name']} HP: {enemy['current_hp']}/{enemy['hp']})"
                )
            else:
                console.print("[red]✗[/red] You miss!")

            # Enemy turn (if still alive)
            if enemy["current_hp"] > 0:
                console.print(f"\n[red]{enemy['name']}'s turn![/red]")
                enemy_attack = DnDRoller.roll("1d20") + 2  # Simple enemy attack bonus

                if enemy_attack >= game_state.character.ac:
                    enemy_damage = DnDRoller.roll_damage(enemy["damage"])
                    DnD5eCombat.apply_damage(game_state.character, enemy_damage)
                    console.print(
                        f"[red]✗[/red] {enemy['name']} hits you for {enemy_damage} damage! (Your HP: {game_state.character.hp}/{game_state.character.max_hp})"
                    )

                    if game_state.character.hp <= 0:
                        console.print("\n[bold red]💀 YOU HAVE BEEN DEFEATED! 💀[/bold red]\n")
                        return False
                else:
                    console.print(f"[green]✓[/green] {enemy['name']} misses!")

            round_num += 1
            console.print()

        # Victory!
        if enemy["current_hp"] <= 0:
            console.print(
                f"[bold green]🎉 VICTORY! You defeated the {enemy['name']}! 🎉[/bold green]\n"
            )

            # Gain XP and gold
            xp_gain = enemy["xp"]
            gold_gain = random.randint(5, 15)
            game_state.gold += gold_gain

            console.print(f"[green]+[/green] Gained {xp_gain} XP")
            console.print(f"[yellow]+[/yellow] Found {gold_gain} gp")

            # Check for level up (simple: every 100 XP = level up)
            # For simplicity, we'll just increment level after encounters
            if game_state.encounters_completed > 0 and game_state.encounters_completed % 3 == 0:
                game_state.character.level += 1
                hp_gain = (
                    DnDRoller.roll(f"1d{game_state.character.hit_die}")
                    + game_state.character.con_modifier
                )
                game_state.character.max_hp += hp_gain
                game_state.character.hp += hp_gain
                console.print(
                    f"[bold cyan]✨ LEVEL UP! You are now level {game_state.character.level}! ✨[/bold cyan]"
                )
                console.print(
                    f"[green]+[/green] Gained {hp_gain} HP (now {game_state.character.hp}/{game_state.character.max_hp})"
                )

            game_state.encounters_completed += 1
            return True

        return False


def create_character() -> DnD5eCharacter:
    """Create a character with rolled stats."""
    console.print("\n[bold cyan]🎲 CHARACTER CREATION 🎲[/bold cyan]\n")

    name = Prompt.ask("What is your character's name?", default="Adventurer")

    # Roll ability scores (4d6, drop lowest)
    console.print("\n[dim]Rolling ability scores (4d6, drop lowest)...[/dim]")

    def roll_ability_score() -> int:
        rolls = [DnDRoller.roll("1d6") for _ in range(4)]
        rolls.sort(reverse=True)
        return sum(rolls[:3])

    strength = roll_ability_score()
    dexterity = roll_ability_score()
    constitution = roll_ability_score()
    intelligence = roll_ability_score()
    wisdom = roll_ability_score()
    charisma = roll_ability_score()

    console.print(
        f"  [cyan]STR:[/cyan] {strength:2d}  [cyan]DEX:[/cyan] {dexterity:2d}  [cyan]CON:[/cyan] {constitution:2d}"
    )
    console.print(
        f"  [cyan]INT:[/cyan] {intelligence:2d}  [cyan]WIS:[/cyan] {wisdom:2d}  [cyan]CHA:[/cyan] {charisma:2d}"
    )

    # Calculate HP
    con_mod = DnD5eStats.ability_modifier(constitution)
    hit_die = 10
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
        armor_type=ArmorType.NONE,
        proficient_saves=["STR", "CON"],
        proficient_skills=["Athletics", "Perception"],
    )

    console.print("\n[bold green]✓ Character Created![/bold green]")
    console.print(f"  Name: {character.name}")
    console.print(f"  Level: {character.level}")
    console.print(f"  HP: {character.hp}/{character.max_hp}")
    console.print(f"  AC: {character.ac}")
    console.print(f"  Proficiency Bonus: +{character.proficiency_bonus}")

    return character


def display_character_sheet(game_state: GameState):
    """Display character sheet."""
    char = game_state.character

    table = Table(title=f"{char.name} - Level {char.level} {char.char_class.title()}")
    table.add_column("Stat", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("HP", f"{char.hp}/{char.max_hp}")
    table.add_row("AC", str(char.ac))
    table.add_row("Level", str(char.level))
    table.add_row("Proficiency", f"+{char.proficiency_bonus}")

    table.add_row("", "")
    table.add_row("[bold]Ability Scores[/bold]", "")
    table.add_row("Strength", f"{char.strength} ({char.str_modifier:+d})")
    table.add_row("Dexterity", f"{char.dexterity} ({char.dex_modifier:+d})")
    table.add_row("Constitution", f"{char.constitution} ({char.con_modifier:+d})")
    table.add_row("Intelligence", f"{char.intelligence} ({char.int_modifier:+d})")
    table.add_row("Wisdom", f"{char.wisdom} ({char.wis_modifier:+d})")
    table.add_row("Charisma", f"{char.charisma} ({char.cha_modifier:+d})")

    table.add_row("", "")
    table.add_row("[bold]Equipment[/bold]", "")
    table.add_row("Weapon", char.equipped_weapon or "None")
    table.add_row("Armor", char.equipped_armor or "None")

    table.add_row("", "")
    table.add_row("[bold]Resources[/bold]", "")
    table.add_row("Gold", f"{game_state.gold} gp")
    table.add_row("Inventory", ", ".join(game_state.inventory) if game_state.inventory else "Empty")

    console.print("\n")
    console.print(table)
    console.print("\n")


def save_game(game_state: GameState, filename: str = "dnd_game_save.json"):
    """Save game state to file."""
    save_path = Path(__file__).parent / filename
    save_path.write_text(json.dumps(game_state.to_dict(), indent=2))
    console.print(f"[green]✓[/green] Game saved to {save_path}")


def load_game(filename: str = "dnd_game_save.json") -> GameState | None:
    """Load game state from file."""
    save_path = Path(__file__).parent / filename
    if not save_path.exists():
        return None

    try:
        data = json.loads(save_path.read_text())
        return GameState.from_dict(data)
    except Exception as e:
        console.print(f"[red]Error loading game: {e}[/red]")
        return None


def main_game_loop(game_state: GameState):
    """Main game loop."""
    console.print("\n[bold cyan]🎮 WELCOME TO THE ADVENTURE! 🎮[/bold cyan]\n")
    console.print("You find yourself in a small town. What would you like to do?\n")

    while True:
        if game_state.character.hp <= 0:
            console.print("\n[bold red]💀 GAME OVER 💀[/bold red]\n")
            break

        choice = Prompt.ask(
            "What do you do?",
            choices=["explore", "shop", "rest", "character", "combat", "save", "quit"],
            default="explore",
        )

        if choice == "quit":
            if Confirm.ask("Save before quitting?"):
                save_game(game_state)
            break

        elif choice == "explore":
            console.print("\n[cyan]You explore the area...[/cyan]\n")
            story_options = [
                "You discover an ancient ruin with mysterious markings.",
                "You find a hidden path leading into the forest.",
                "A traveling merchant approaches you with a quest.",
                "You stumble upon a bandit camp in the distance.",
                "An old hermit offers you wisdom and a small trinket.",
            ]
            story = random.choice(story_options)
            console.print(Panel(story, border_style="cyan"))
            game_state.story_log.append(story)

            if Confirm.ask("\nWould you like to investigate further?"):
                if "bandit" in story.lower() or "ruin" in story.lower():
                    CombatEncounter.run_combat(game_state)
                else:
                    gold_found = random.randint(1, 10)
                    game_state.gold += gold_found
                    console.print(f"[yellow]+[/yellow] Found {gold_found} gp!")

        elif choice == "shop":
            Shop.display_shop(game_state)

        elif choice == "rest":
            console.print("\n[cyan]You rest and recover...[/cyan]\n")
            healing = DnDRoller.roll("1d8") + game_state.character.con_modifier
            old_hp = game_state.character.hp
            DnD5eCombat.apply_healing(game_state.character, healing)
            hp_gained = game_state.character.hp - old_hp
            console.print(
                f"[green]✓[/green] Restored {hp_gained} HP (now {game_state.character.hp}/{game_state.character.max_hp})"
            )

        elif choice == "character":
            display_character_sheet(game_state)

        elif choice == "combat":
            enemy_choice = Prompt.ask(
                "Choose an enemy (or 'random')",
                choices=["goblin", "orc", "skeleton", "bandit", "wolf", "random"],
                default="random",
            )
            if enemy_choice == "random":
                enemy_choice = None
            CombatEncounter.run_combat(game_state, enemy_choice)

        elif choice == "save":
            save_game(game_state)

        console.print()


def main():
    """Main entry point."""
    console.print(
        Panel.fit(
            "[bold cyan]🎲 INTERACTIVE D&D GAME 🎲[/bold cyan]\n"
            "A complete playable D&D 5e adventure!",
            border_style="bright_blue",
        )
    )

    # Check for saved game
    if Path(__file__).parent.joinpath("dnd_game_save.json").exists():
        if Confirm.ask("\nLoad saved game?"):
            game_state = load_game()
            if game_state:
                console.print("[green]✓[/green] Game loaded!")
                main_game_loop(game_state)
                return

    # Create new character
    character = create_character()
    game_state = GameState(character)

    # Start game
    main_game_loop(game_state)

    console.print("\n[bold]Thanks for playing![/bold]\n")


if __name__ == "__main__":
    main()
