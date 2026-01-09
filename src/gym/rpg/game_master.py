"""
Game Master - The Dungeon Master (DM) for the Jungle Gym

Runs the game loop, manages quests, and orchestrates encounters between
the Hero (AI agent) and challenges (Waft validation).
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from .models import Hero, Quest, BattleLog

# Import InputTransformer from waft.core
# Note: This assumes 'src' is in sys.path (as done in play_gym.py)
try:
    from waft.core.input_transformer import InputTransformer
except ImportError:
    # Fallback: try relative import if running from within src
    import sys
    from pathlib import Path
    src_path = Path(__file__).parent.parent.parent
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    from waft.core.input_transformer import InputTransformer


class GameMaster:
    """
    The Game Master - Runs the RPG game loop.
    
    Responsibilities:
    - Load quests from JSON files
    - Display quest start screens
    - Run encounters (pass prompt to agent, validate response)
    - Track XP, level ups, and loot
    """
    
    def __init__(self, quests_dir: Path, loot_dir: Path):
        """
        Initialize the Game Master.
        
        Args:
            quests_dir: Directory containing quest JSON files
            loot_dir: Directory to save successful quest outputs
        """
        self.quests_dir = Path(quests_dir)
        self.loot_dir = Path(loot_dir)
        self.loot_dir.mkdir(parents=True, exist_ok=True)
        self.console = Console()
        self.quests: List[Quest] = []
        
    def load_quests(self, dungeon_file: str) -> List[Quest]:
        """
        Load quests from a dungeon JSON file.
        
        Args:
            dungeon_file: Name of the dungeon file (e.g., "waft_temple.json")
        
        Returns:
            List of Quest objects
        """
        dungeon_path = self.quests_dir / dungeon_file
        if not dungeon_path.exists():
            raise FileNotFoundError(f"Dungeon file not found: {dungeon_path}")
        
        with open(dungeon_path, 'r') as f:
            data = json.load(f)
        
        self.quests = [Quest(**quest_data) for quest_data in data.get('quests', [])]
        return self.quests
    
    def start_encounter(
        self,
        hero: Hero,
        quest: Quest,
        agent_func: Callable[[str], str]
    ) -> BattleLog:
        """
        Run a quest encounter.
        
        Process:
        1. Display "Quest Start" screen (Rich panel)
        2. Pass quest.description to agent_func (The AI)
        3. Take AI's response (The Attack)
        4. Combat Calculation: Validate response with InputTransformer
        5. Result:
           - Hit (Success): Gain XP, update stats, save loot
           - Miss (Fail): Log validation error
        
        Args:
            hero: The Hero attempting the quest
            quest: The Quest to attempt
            agent_func: Function that takes prompt string, returns response string
        
        Returns:
            BattleLog recording the encounter
        """
        # 1. Display Quest Start Screen
        self._display_quest_start(hero, quest)
        
        # 2. Get AI response
        self.console.print(f"\n[cyan]📜 Quest Prompt:[/cyan]")
        self.console.print(Panel(quest.description, border_style="cyan"))
        
        agent_response = agent_func(quest.description)
        
        # 3. Combat Calculation - Validate with InputTransformer
        success = False
        error_message = None
        loot_saved = False
        
        try:
            # Try to parse the response as JSON
            import json as json_lib
            response_data = json_lib.loads(agent_response)
            
            # Validate using InputTransformer (The Waft Iron Core)
            matrix = InputTransformer.transform_input(response_data)
            
            # Success! The validation passed
            success = True
            
            # Save loot (prompt + response) to _pyrite/gym_logs/loot
            loot_data = {
                "quest_name": quest.name,
                "timestamp": datetime.now().isoformat(),
                "hero_name": hero.name,
                "prompt": quest.description,
                "response": agent_response,
                "validated_matrix": {
                    "alternatives": [alt.name for alt in matrix.alternatives],
                    "criteria": {crit.name: crit.weight for crit in matrix.criteria},
                    "methodology": matrix.methodology
                }
            }
            
            loot_filename = f"{quest.name.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            loot_path = self.loot_dir / loot_filename
            
            with open(loot_path, 'w') as f:
                json_lib.dump(loot_data, f, indent=2)
            
            loot_saved = True
            
        except json_lib.JSONDecodeError as e:
            error_message = f"Invalid JSON: {str(e)}"
        except ValueError as e:
            error_message = f"Validation Error: {str(e)}"
        except Exception as e:
            error_message = f"Unexpected Error: {str(e)}"
        
        # 4. Calculate XP and update Hero
        xp_gained = 0
        if success:
            xp_gained = quest.rewards.get('xp', 0)
            level_result = hero.add_xp(xp_gained)
            
            # Display result
            self._display_combat_result(hero, quest, success, error_message, xp_gained, level_result)
        else:
            self._display_combat_result(hero, quest, success, error_message, xp_gained, None)
        
        # Create battle log
        battle_log = BattleLog(
            quest_name=quest.name,
            hero_name=hero.name,
            input_prompt=quest.description,
            agent_response=agent_response,
            success=success,
            error_message=error_message,
            xp_gained=xp_gained,
            loot_saved=loot_saved
        )
        
        return battle_log
    
    def _display_quest_start(self, hero: Hero, quest: Quest):
        """Display the Quest Start screen using Rich panels."""
        table = Table(show_header=False, box=box.SIMPLE)
        table.add_column(style="cyan", width=20)
        table.add_column(style="white")
        
        table.add_row("🎯 Quest:", quest.name)
        table.add_row("⚔️  Difficulty:", f"{quest.difficulty}/10")
        table.add_row("📊 Level Req:", str(quest.level_requirement))
        table.add_row("🏆 XP Reward:", str(quest.rewards.get('xp', 0)))
        table.add_row("", "")
        table.add_row("Hero:", hero.name)
        table.add_row("Level:", str(hero.level))
        table.add_row("XP:", str(hero.xp))
        table.add_row("Stats:", f"INT:{hero.intelligence} WIS:{hero.wisdom} CHA:{hero.charisma}")
        
        panel = Panel(
            table,
            title="[bold cyan]QUEST START[/bold cyan]",
            border_style="cyan",
            padding=(1, 2)
        )
        
        self.console.print("\n")
        self.console.print(panel)
    
    def _display_combat_result(
        self,
        hero: Hero,
        quest: Quest,
        success: bool,
        error_message: Optional[str],
        xp_gained: int,
        level_result: Optional[Dict[str, Any]]
    ):
        """Display the combat result."""
        if success:
            result_text = Text()
            result_text.append("✅ ", style="bold green")
            result_text.append("VICTORY! ", style="bold green")
            result_text.append(f"+{xp_gained} XP", style="yellow")
            
            if level_result and level_result.get('leveled_up'):
                result_text.append("\n🎉 ", style="bold gold1")
                result_text.append(f"LEVEL UP! ", style="bold gold1")
                result_text.append(f"Level {level_result['new_level']}", style="gold1")
                if level_result.get('stat_increased'):
                    result_text.append(f"\n📈 {level_result['stat_increased'].title()} increased!", style="cyan")
            
            panel = Panel(
                result_text,
                title="[bold green]COMBAT RESULT[/bold green]",
                border_style="green",
                padding=(1, 2)
            )
        else:
            result_text = Text()
            result_text.append("❌ ", style="bold red")
            result_text.append("DEFEAT! ", style="bold red")
            result_text.append("\n💔 ", style="red")
            result_text.append("Damage Taken: ", style="red")
            result_text.append("Validation Failed", style="yellow")
            if error_message:
                result_text.append(f"\n\nError: {error_message}", style="dim red")
            
            panel = Panel(
                result_text,
                title="[bold red]COMBAT RESULT[/bold red]",
                border_style="red",
                padding=(1, 2)
            )
        
        self.console.print("\n")
        self.console.print(panel)
    
    def display_character_sheet(self, hero: Hero):
        """Display the Hero's character sheet at the end of the session."""
        table = Table(show_header=False, box=box.ROUNDED)
        table.add_column(style="cyan", width=20)
        table.add_column(style="white")
        
        table.add_row("Name:", hero.name)
        table.add_row("Level:", str(hero.level))
        table.add_row("XP:", str(hero.xp))
        table.add_row("XP to Next Level:", str((hero.level * 100) - hero.xp))
        table.add_row("", "")
        table.add_row("Intelligence:", f"{hero.intelligence} ({self._get_modifier(hero.intelligence)})")
        table.add_row("Wisdom:", f"{hero.wisdom} ({self._get_modifier(hero.wisdom)})")
        table.add_row("Charisma:", f"{hero.charisma} ({self._get_modifier(hero.charisma)})")
        table.add_row("", "")
        table.add_row("Total Stats:", str(hero.get_total_stats()))
        
        panel = Panel(
            table,
            title="[bold gold1]CHARACTER SHEET[/bold gold1]",
            border_style="gold1",
            padding=(1, 2)
        )
        
        self.console.print("\n")
        self.console.print(panel)
    
    def _get_modifier(self, stat: int) -> str:
        """Calculate D&D 5e ability modifier."""
        modifier = (stat - 10) // 2
        return f"+{modifier}" if modifier >= 0 else str(modifier)
