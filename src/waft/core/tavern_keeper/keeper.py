"""
TavernKeeper - Core class for RPG gamification system.

Manages character stats, dice rolling, narrative generation, and game state.
"""

import json
import math
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

try:
    from tinydb import TinyDB, Query
    TINYDB_AVAILABLE = True
except ImportError:
    TINYDB_AVAILABLE = False

try:
    import d20
    D20_AVAILABLE = True
except ImportError:
    D20_AVAILABLE = False

try:
    import tracery
    TRACERY_AVAILABLE = True
except ImportError:
    TRACERY_AVAILABLE = False


class TavernKeeper:
    """
    The TavernKeeper - Narrator and game master for the Living Repository.

    Manages:
    - Character stats (ability scores, HP, XP, Level)
    - Dice rolling (d20 system)
    - Narrative generation (Tracery)
    - Status effects (buffs/debuffs)
    - Adventure journal
    """

    def __init__(self, project_path: Path):
        """
        Initialize the TavernKeeper.

        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.data_dir = project_path / "_pyrite" / ".waft"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.chronicles_path = self.data_dir / "chronicles.json"

        # Initialize database
        if TINYDB_AVAILABLE:
            self.db = TinyDB(str(self.chronicles_path))
        else:
            self.db = None
            # Fallback to JSON file
            self._data = self._load_json_data()

        # Initialize character if needed
        if not self._character_exists():
            self._initialize_character()
        
        # Migrate from gamification.json if it exists
        self._migrate_from_gamification()

    def _load_json_data(self) -> Dict[str, Any]:
        """Load data from JSON file (fallback if TinyDB not available)."""
        if self.chronicles_path.exists():
            try:
                with open(self.chronicles_path, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        return {
            "character": self._default_character(),
            "status_effects": [],
            "adventure_journal": [],
            "quests": [],
            "achievements": [],
            "tavern_keeper_state": {
                "last_narrative": "",
                "mood": "optimistic",
                "wisdom_shared": 0,
            },
        }

    def _default_character(self) -> Dict[str, Any]:
        """Create default character stats."""
        return {
            "name": self.project_path.name,
            "level": 1,
            "integrity": 100.0,
            "insight": 0.0,
            "credits": 0,
            "ability_scores": {
                "strength": 8,
                "dexterity": 8,
                "constitution": 8,
                "intelligence": 8,
                "wisdom": 8,
                "charisma": 8,
            },
            "proficiency_bonus": 2,
            "hit_dice": "d8",
            "max_hp": 10,
            "current_hp": 10,
            "created_at": datetime.now().isoformat(),
        }

    def _character_exists(self) -> bool:
        """Check if character data exists."""
        if self.db:
            return len(self.db.table("character").all()) > 0
        else:
            return "character" in self._data and self._data["character"]

    def _initialize_character(self) -> None:
        """Initialize character with default stats."""
        character = self._default_character()
        
        if self.db:
            self.db.table("character").insert(character)
        else:
            self._data["character"] = character
            self._save_json_data()

    def _migrate_from_gamification(self) -> None:
        """Migrate data from gamification.json to chronicles.json if needed."""
        gamification_path = self.data_dir / "gamification.json"
        if not gamification_path.exists():
            return
        
        try:
            with open(gamification_path, "r") as f:
                gam_data = json.load(f)
            
            character = self.get_character()
            
            # Migrate stats if character is at defaults
            if character.get("insight", 0.0) == 0.0 and character.get("integrity", 100.0) == 100.0:
                # Map existing stats
                character["integrity"] = gam_data.get("integrity", 100.0)
                character["insight"] = gam_data.get("insight", 0.0)
                character["level"] = self._calculate_level_from_insight(character["insight"])
                
                # Migrate achievements
                achievements = gam_data.get("achievements", [])
                if achievements:
                    if self.db:
                        # Store achievements in a separate table or in character
                        pass
                    else:
                        self._data["achievements"] = achievements
                
                # Migrate history as adventure journal entries
                history = gam_data.get("history", [])
                if history:
                    journal_entries = []
                    for entry in history[-50:]:  # Keep last 50 entries
                        journal_entries.append({
                            "timestamp": entry.get("timestamp", datetime.now().isoformat()),
                            "event": entry.get("type", "unknown"),
                            "narrative": entry.get("reason", ""),
                            "outcome": "success" if entry.get("type") == "insight_award" else "info",
                        })
                    
                    if self.db:
                        for entry in journal_entries:
                            self.db.table("adventure_journal").insert(entry)
                    else:
                        self._data["adventure_journal"] = journal_entries + self._data.get("adventure_journal", [])
                
                # Save updated character
                if self.db:
                    self.db.table("character").update(character, Query().name == character["name"])
                else:
                    self._data["character"] = character
                    self._save_json_data()
        except (json.JSONDecodeError, IOError, KeyError):
            # Migration failed, continue with defaults
            pass

    def _calculate_level_from_insight(self, insight: float) -> int:
        """Calculate level from insight using polynomial curve."""
        if insight <= 0:
            return 1
        # Level = sqrt(Insight / 100) + 1 (existing formula)
        level = int(math.sqrt(insight / 100)) + 1
        return max(1, level)

    def _save_json_data(self) -> None:
        """Save data to JSON file (fallback)."""
        self._data["updated_at"] = datetime.now().isoformat()
        with open(self.chronicles_path, "w") as f:
            json.dump(self._data, f, indent=2)

    def get_character(self) -> Dict[str, Any]:
        """Get current character stats."""
        if self.db:
            chars = self.db.table("character").all()
            return chars[0] if chars else self._default_character()
        else:
            return self._data.get("character", self._default_character())

    def get_ability_score(self, ability: str) -> int:
        """
        Get ability score.

        Args:
            ability: One of strength, dexterity, constitution, intelligence, wisdom, charisma

        Returns:
            Ability score (1-20)
        """
        character = self.get_character()
        return character.get("ability_scores", {}).get(ability.lower(), 8)

    def get_ability_modifier(self, ability: str) -> int:
        """
        Calculate ability modifier: (Score - 10) / 2, rounded down.

        Args:
            ability: Ability name

        Returns:
            Modifier (can be negative)
        """
        score = self.get_ability_score(ability)
        return (score - 10) // 2

    def get_proficiency_bonus(self) -> int:
        """
        Get proficiency bonus based on level (D&D 5e standard).

        Returns:
            Proficiency bonus (+2 to +6)
        """
        character = self.get_character()
        level = character.get("level", 1)

        if level <= 4:
            return 2
        elif level <= 8:
            return 3
        elif level <= 12:
            return 4
        elif level <= 16:
            return 5
        else:
            return 6

    def get_max_hp(self) -> int:
        """
        Calculate max HP from CON and level.
        Formula: 8 + CON mod + (Level - 1) * (4 + CON mod)

        Returns:
            Maximum hit points
        """
        character = self.get_character()
        level = character.get("level", 1)
        con_mod = self.get_ability_modifier("constitution")

        base_hp = 8 + con_mod
        level_hp = (level - 1) * (4 + con_mod)
        return max(1, base_hp + level_hp)

    def get_current_hp(self) -> int:
        """
        Calculate current HP from Integrity.
        Current HP = Max HP * (Integrity / 100)

        Returns:
            Current hit points
        """
        character = self.get_character()
        integrity = character.get("integrity", 100.0)
        max_hp = self.get_max_hp()
        return int(max_hp * (integrity / 100.0))

    def roll_check(self, ability: str, dc: int, advantage: bool = False, disadvantage: bool = False) -> Dict[str, Any]:
        """
        Roll a d20 check against a difficulty class (DC).

        Args:
            ability: Ability to use (for modifier)
            dc: Difficulty class (target number)
            advantage: Roll with advantage (2d20kh1)
            disadvantage: Roll with disadvantage (2d20kl1)

        Returns:
            Dictionary with roll result, total, success, and narrative
        """
        if not D20_AVAILABLE:
            # Fallback: simple random roll
            import random
            roll = random.randint(1, 20)
            if advantage:
                roll2 = random.randint(1, 20)
                roll = max(roll, roll2)
            elif disadvantage:
                roll2 = random.randint(1, 20)
                roll = min(roll, roll2)
        else:
            # Use d20 library
            if advantage:
                dice_str = "2d20kh1"
            elif disadvantage:
                dice_str = "2d20kl1"
            else:
                dice_str = "1d20"

            result = d20.roll(dice_str)
            roll = result.total

        modifier = self.get_ability_modifier(ability)
        total = roll + modifier
        success = total >= dc

        # Determine roll classification
        if roll == 1:
            classification = "critical_failure"
        elif roll == 20:
            classification = "critical_success"
        elif success:
            if roll >= 19:
                classification = "superior"
            elif roll >= 11:
                classification = "optimal"
            else:
                classification = "nominal"
        else:
            classification = "failure"

        return {
            "roll": roll,
            "modifier": modifier,
            "total": total,
            "dc": dc,
            "success": success,
            "classification": classification,
        }

    def narrate(self, event: str, outcome: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate narrative text using Tracery (or fallback).

        Args:
            event: Event type (e.g., "verification_success", "level_up")
            outcome: Outcome type ("success", "failure", "level_up")
            context: Optional context for narrative (character name, etc.)

        Returns:
            Generated narrative text
        """
        from .grammars import get_grammar

        character = self.get_character()
        char_name = character.get("name", "the Construct")

        # Determine grammar type
        if outcome == "level_up":
            grammar_type = "level_up"
        elif "critical_success" in event or outcome == "critical_success":
            grammar_type = "critical_success"
        elif "critical_failure" in event or outcome == "critical_failure":
            grammar_type = "critical_failure"
        elif outcome == "success":
            grammar_type = "success"
        elif outcome == "failure":
            grammar_type = "failure"
        elif event == "commit":
            grammar_type = "commit"
        else:
            grammar_type = "success"  # Default

        # Get grammar
        grammar = get_grammar(grammar_type)

        # Try to use Tracery if available
        if TRACERY_AVAILABLE:
            try:
                tracery_grammar = tracery.Grammar(grammar)
                narrative = tracery_grammar.flatten("#origin#")

                # Replace placeholders with context if provided
                if context:
                    for key, value in context.items():
                        narrative = narrative.replace(f"#{key}#", str(value))

                # Replace common placeholders
                narrative = narrative.replace("#entity#", char_name)
                narrative = narrative.replace("#component#", char_name)
                narrative = narrative.replace("#structure#", char_name)

                return narrative
            except Exception:
                # Fallback to simple selection if Tracery fails
                pass

        # Fallback: Simple random selection from grammar
        import random
        import re
        if "origin" in grammar:
            narrative = random.choice(grammar["origin"])
            # Simple placeholder replacement - replace all #key# patterns
            # First replace common placeholders
            narrative = narrative.replace("#entity#", char_name)
            narrative = narrative.replace("#component#", char_name)
            narrative = narrative.replace("#structure#", char_name)
            
            # Replace other grammar placeholders by expanding them
            placeholder_pattern = re.compile(r"#(\w+)#")
            
            def replace_placeholder(match):
                key = match.group(1)
                # Check if it's in context first
                if context and key in context:
                    return str(context[key])
                # Check if it's in grammar
                if key in grammar:
                    choices = grammar[key]
                    if isinstance(choices, list):
                        return random.choice(choices)
                    return str(choices)
                # Unknown placeholder, return as-is
                return match.group(0)
            
            # Replace all placeholders recursively
            max_iterations = 10
            iteration = 0
            while "#" in narrative and iteration < max_iterations:
                new_narrative = placeholder_pattern.sub(replace_placeholder, narrative)
                if new_narrative == narrative:
                    break
                narrative = new_narrative
                iteration += 1
            
            # Final cleanup - remove any remaining #placeholders#
            narrative = re.sub(r"#\w+#", "", narrative).strip()
            if not narrative:
                narrative = f"The TavernKeeper observes {char_name}."
            
            return narrative

        # Ultimate fallback
        return f"The TavernKeeper observes {char_name}."

    def apply_status_effect(self, effect: Dict[str, Any]) -> None:
        """
        Apply a status effect (buff or debuff).

        Args:
            effect: Dictionary with id, name, type, effect, duration, description
        """
        # Ensure required fields
        if "id" not in effect:
            effect["id"] = effect.get("name", "unknown").lower().replace(" ", "_")
        if "applied_at" not in effect:
            effect["applied_at"] = datetime.now().isoformat()

        if self.db:
            # Remove existing effect with same id if present
            self.db.table("status_effects").remove(Query().id == effect["id"])
            self.db.table("status_effects").insert(effect)
        else:
            # Remove existing effect with same id if present
            effects = self._data.setdefault("status_effects", [])
            effects[:] = [e for e in effects if e.get("id") != effect["id"]]
            effects.append(effect)
            self._save_json_data()

    def remove_status_effect(self, effect_id: str) -> None:
        """
        Remove a status effect by ID.

        Args:
            effect_id: ID of the effect to remove
        """
        if self.db:
            self.db.table("status_effects").remove(Query().id == effect_id)
        else:
            effects = self._data.setdefault("status_effects", [])
            self._data["status_effects"] = [e for e in effects if e.get("id") != effect_id]
            self._save_json_data()

    def get_active_status_effects(self) -> List[Dict[str, Any]]:
        """
        Get all active status effects.

        Returns:
            List of active status effects
        """
        if self.db:
            return self.db.table("status_effects").all()
        else:
            return self._data.get("status_effects", [])

    def apply_status_effect_from_classification(self, classification: str) -> None:
        """
        Apply status effect based on dice roll classification.

        Args:
            classification: One of critical_failure, failure, success, etc.
        """
        if classification == "critical_failure":
            self.apply_status_effect({
                "id": "entropy_spike",
                "name": "Entropy Spike",
                "type": "debuff",
                "effect": {"constitution": -2},
                "duration": None,  # Permanent until removed
                "description": "Critical failure causes structural instability",
            })
        elif classification == "critical_success":
            self.apply_status_effect({
                "id": "harmonic_resonance",
                "name": "Harmonic Resonance",
                "type": "buff",
                "effect": {"intelligence": +2, "wisdom": +2},
                "duration": 3600,  # 1 hour in seconds
                "description": "Critical success creates perfect alignment",
            })

    def award_rewards(self, rewards: Dict[str, Any]) -> Dict[str, Any]:
        """
        Award rewards (XP, Credits, etc.).

        Args:
            rewards: Dictionary with insight, credits, integrity changes

        Returns:
            Dictionary with updated stats and level_up flag
        """
        character = self.get_character()
        old_level = character.get("level", 1)
        old_insight = character.get("insight", 0.0)

        # Apply rewards
        new_insight = old_insight + rewards.get("insight", 0.0)
        new_credits = character.get("credits", 0) + rewards.get("credits", 0)

        # Update integrity if provided
        integrity_delta = rewards.get("integrity", 0.0)
        current_integrity = character.get("integrity", 100.0)
        new_integrity = max(0.0, min(100.0, current_integrity + integrity_delta))

        # Calculate new level
        new_level = self._calculate_level_from_insight(new_insight)
        level_up = new_level > old_level

        # Update character
        character["insight"] = new_insight
        character["credits"] = new_credits
        character["integrity"] = new_integrity
        character["level"] = new_level
        character["proficiency_bonus"] = self.get_proficiency_bonus()
        character["max_hp"] = self.get_max_hp()
        character["current_hp"] = self.get_current_hp()
        character["updated_at"] = datetime.now().isoformat()

        # Save
        if self.db:
            self.db.table("character").update(character, Query().name == character["name"])
        else:
            self._data["character"] = character
            self._save_json_data()

        return {
            "level_up": level_up,
            "old_level": old_level,
            "new_level": new_level,
            "old_insight": old_insight,
            "new_insight": new_insight,
            "new_credits": new_credits,
            "new_integrity": new_integrity,
        }

    def log_adventure(self, event: Dict[str, Any]) -> None:
        """
        Log an event to the adventure journal.

        Args:
            event: Dictionary with timestamp, event, narrative, dice_roll, result, outcome, rewards
        """
        if "timestamp" not in event:
            event["timestamp"] = datetime.now().isoformat()

        if self.db:
            self.db.table("adventure_journal").insert(event)
        else:
            self._data.setdefault("adventure_journal", []).append(event)
            # Keep only last 100 entries
            if len(self._data["adventure_journal"]) > 100:
                self._data["adventure_journal"] = self._data["adventure_journal"][-100:]
            self._save_json_data()

    def get_character_sheet(self) -> Dict[str, Any]:
        """
        Get full character sheet with all stats.

        Returns:
            Complete character data
        """
        character = self.get_character()

        return {
            "character": character,
            "ability_scores": character.get("ability_scores", {}),
            "ability_modifiers": {
                ability: self.get_ability_modifier(ability)
                for ability in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
            },
            "proficiency_bonus": self.get_proficiency_bonus(),
            "hp": {
                "current": self.get_current_hp(),
                "max": self.get_max_hp(),
            },
            "status_effects": self._data.get("status_effects", []) if not self.db else self.db.table("status_effects").all(),
        }

    def process_command_hook(self, command: str, success: bool, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a command hook - roll dice, generate narrative, award rewards.

        Args:
            command: Command name (e.g., "verify", "new")
            success: Whether command succeeded
            context: Optional context (file count, etc.)

        Returns:
            Dictionary with narrative, rewards, and dice results
        """
        # Define command mappings to RPG checks
        command_map = {
            "new": {"ability": "charisma", "dc": 10, "base_xp": 50, "base_credits": 10},
            "verify": {"ability": "constitution", "dc": 12, "base_xp": 5, "base_credits": 0},
            "init": {"ability": "wisdom", "dc": 10, "base_xp": 25, "base_credits": 5},
            "info": {"ability": "wisdom", "dc": 8, "base_xp": 2, "base_credits": 0},
            "sync": {"ability": "intelligence", "dc": 10, "base_xp": 3, "base_credits": 5},
            "add": {"ability": "charisma", "dc": 12, "base_xp": 5, "base_credits": 2},
            "finding_log": {"ability": "intelligence", "dc": 10, "base_xp": 10, "base_credits": 5},
            "assess": {"ability": "wisdom", "dc": 15, "base_xp": 25, "base_credits": 10},
            "check": {"ability": "wisdom", "dc": 12, "base_xp": 5, "base_credits": 0},
            "goal_create": {"ability": "charisma", "dc": 10, "base_xp": 5, "base_credits": 0},
        }

        cmd_config = command_map.get(command, {"ability": "wisdom", "dc": 10, "base_xp": 5, "base_credits": 0})

        # Roll dice
        dice_result = self.roll_check(cmd_config["ability"], cmd_config["dc"])

        # Calculate XP multiplier based on roll
        xp_multiplier = 1.0
        if dice_result["classification"] == "critical_failure":
            xp_multiplier = 0.5
        elif dice_result["classification"] == "critical_success":
            xp_multiplier = 2.0
        elif dice_result["classification"] == "superior":
            xp_multiplier = 1.5
        elif dice_result["classification"] == "optimal":
            xp_multiplier = 1.1

        # Only award if successful
        if not success:
            xp_multiplier = 0.0

        # Calculate rewards
        base_xp = cmd_config["base_xp"] if success else 0
        xp_gained = int(base_xp * xp_multiplier)

        rewards = {
            "insight": xp_gained,
            "credits": cmd_config["base_credits"] if success else 0,
            "integrity": 2.0 if success else -10.0,
        }

        # Apply status effects based on classification
        if dice_result["classification"] in ["critical_failure", "critical_success"]:
            self.apply_status_effect_from_classification(dice_result["classification"])

        # Award rewards
        reward_result = self.award_rewards(rewards)

        # Generate narrative
        outcome = "success" if success else "failure"
        narrative = self.narrate(f"{command}_{outcome}", outcome, context)

        # Log adventure
        self.log_adventure({
            "event": command,
            "narrative": narrative,
            "dice_roll": f"1d20+{dice_result['modifier']}",
            "result": dice_result["total"],
            "outcome": outcome,
            "rewards": rewards,
            "classification": dice_result["classification"],
        })

        return {
            "narrative": narrative,
            "dice_result": dice_result,
            "rewards": reward_result,
            "xp_gained": xp_gained,
        }

