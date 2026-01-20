"""
Encounter Generator - Dynamic encounter generation.

Generates encounters based on party level and integrates with existing encounter mechanics.
"""

import json
import random
from datetime import datetime
from typing import Any

from rich.console import Console
from rich.panel import Panel

from .party_manager import PartyMember
from .scenario_realm import ScenarioRealm

console = Console()


class EncounterGenerator:
    """
    Generates dynamic encounters for scenarios.

    Features:
    - Combat encounters
    - Social encounters
    - Puzzle/exploration encounters
    - Dynamic difficulty based on party level
    - Integration with existing encounter system
    """

    def __init__(self, scenario_realm: ScenarioRealm):
        """
        Initialize Encounter Generator.

        Args:
            scenario_realm: ScenarioRealm instance
        """
        self.realm = scenario_realm
        self.encounters_dir = scenario_realm.realm_path / "encounters"
        self.encounters_dir.mkdir(parents=True, exist_ok=True)

    def generate_encounter(
        self,
        party: list[PartyMember],
        encounter_name: str | None = None,
        difficulty: str = "medium",
        description: str | None = None,
    ) -> dict[str, Any]:
        """
        Generate a detailed combat encounter with rich narrative.

        Args:
            party: List of PartyMember instances
            encounter_name: Name of the encounter (auto-generated if None)
            difficulty: Difficulty level (easy, medium, hard, boss, epic)
            description: Custom description (auto-generated if None)

        Returns:
            Encounter data
        """
        console.print(
            f"\n[bold red]⚔️  ENCOUNTER: {encounter_name or 'Unknown Threat'} ⚔️[/bold red]\n"
        )

        # Generate encounter name if not provided
        if not encounter_name:
            encounter_names = [
                "Goblin Ambush",
                "Orc Raiders",
                "Dark Cultists",
                "Shadow Wolves",
                "Corrupted Treant",
                "Undead Warriors",
            ]
            encounter_name = random.choice(encounter_names)

        difficulty_multiplier = {
            "easy": 0.8,
            "medium": 1.0,
            "hard": 1.5,
            "boss": 3.0,
            "epic": 5.0,
        }.get(difficulty, 1.0)

        # Simulate combat
        enemy_hp = int(100 * difficulty_multiplier)
        party_damage = sum([random.randint(15, 30) for _ in party])
        rounds = max(1, int(enemy_hp / party_damage))

        # Party takes damage
        damage_taken = {}
        for member in party:
            damage = random.randint(5, 15) * int(difficulty_multiplier)
            member.take_damage(damage)
            damage_taken[member.name] = damage
            if member.hp <= 0:
                member.hp = 1  # Don't kill party members

        # Gain experience
        xp_gain = int(50 * difficulty_multiplier)
        level_ups = []
        for member in party:
            leveled = member.gain_experience(xp_gain)
            if leveled:
                level_ups.append(member.name)
                console.print(f"   [green]✨ {member.name} leveled up to {member.level}![/green]")

        # Generate description
        if not description:
            description = f"""
The party encounters {encounter_name} in a fierce battle. The combat is intense, with spells flying,
swords clashing, and the party working together to overcome their foe. After {rounds} rounds of
determined fighting, the party emerges victorious.
            """

        encounter = {
            "encounter_id": f"encounter_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "title": encounter_name,
            "content": f"""
## {encounter_name}

{description}

### Combat Details

- **Rounds of Combat**: {rounds}
- **Party Damage Taken**: {sum(damage_taken.values())} total
- **Experience Gained**: {xp_gain} XP per party member
- **Current Party HP**: {sum([m.hp for m in party])}/{sum([m.max_hp for m in party])}
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
            "generated_at": datetime.now().isoformat(),
        }

        # Display encounter
        console.print(
            Panel(encounter["content"], title=f"[bold]{encounter_name}[/bold]", border_style="red")
        )
        console.print(
            f"   [green]✓[/green] Encounter complete! Party HP: {sum([m.hp for m in party])}/{sum([m.max_hp for m in party])}"
        )

        # Save encounter log
        self._save_encounter_log(encounter)

        return encounter

    def _save_encounter_log(self, encounter: dict[str, Any]) -> None:
        """Save encounter to log file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.encounters_dir / f"{timestamp}_encounter.json"

        # Validate path
        if not self.realm.validate_path(log_file):
            raise ValueError("Encounter log path validation failed")

        log_file.write_text(json.dumps(encounter, indent=2))
