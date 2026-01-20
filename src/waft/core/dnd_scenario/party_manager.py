"""
Party Manager - Party creation and management for scenarios.

Integrates with BeingSystem to create party members as Beings.
"""

import random
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from rich.console import Console

from ...being import BeingSystem, Being
from .scenario_realm import ScenarioRealm
from .party_state_manager import PartyStateManager

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
        self.stats = {
            "strength": random.randint(12, 18),
            "dexterity": random.randint(12, 18),
            "constitution": random.randint(12, 18),
            "intelligence": random.randint(12, 18),
            "wisdom": random.randint(12, 18),
            "charisma": random.randint(12, 18)
        }
    
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
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "being_id": self.being.being_id,
            "name": self.name,
            "class_type": self.class_type,
            "race": self.race,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "level": self.level,
            "experience": self.experience,
            "stats": self.stats
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], being_system: BeingSystem) -> 'PartyMember':
        """Create from dictionary."""
        try:
            being = being_system._load_being(data["being_id"])
        except (FileNotFoundError, ValueError) as e:
            raise ValueError(f"Being not found: {data['being_id']}: {e}")
        
        member = cls(being, data["name"], data["class_type"], data["race"])
        member.hp = data.get("hp", 100)
        member.max_hp = data.get("max_hp", 100)
        member.level = data.get("level", 1)
        member.experience = data.get("experience", 0)
        member.stats = data.get("stats", member.stats)
        return member


class PartyManager:
    """
    Manages party creation and state.
    
    Features:
    - Spawn party members as Beings
    - Load/save party state
    - Party state persistence
    """
    
    def __init__(self, scenario_realm: ScenarioRealm):
        """
        Initialize Party Manager.
        
        Args:
            scenario_realm: ScenarioRealm instance
        """
        self.realm = scenario_realm
        self.party_state_manager = PartyStateManager(scenario_realm)
        self.being_system = BeingSystem(project_path=scenario_realm.project_path)
        self.party: List[PartyMember] = []
    
    def spawn_party(self, force_new: bool = False) -> List[PartyMember]:
        """
        Spawn party members as Beings.
        
        Args:
            force_new: Force new party creation even if state exists
            
        Returns:
            List of PartyMember instances
        """
        # Try to load existing party state
        if not force_new:
            party_state = self.party_state_manager.load_party_state()
            if party_state and "party_members" in party_state:
                console.print("[yellow]Loading existing party...[/yellow]")
                self.party = [
                    PartyMember.from_dict(member_data, self.being_system)
                    for member_data in party_state["party_members"]
                ]
                console.print(f"[green]✅ Loaded party of {len(self.party)} members[/green]")
                return self.party
        
        # Create new party
        console.print("\n[bold cyan]🎲 SPAWNING THE PARTY 🎲[/bold cyan]\n")
        
        party_configs = [
            {"name": "Thorin Ironforge", "class": "Fighter", "race": "Dwarf", "skills": {"combat": 30.0, "strength": 25.0}},
            {"name": "Lyra Moonwhisper", "class": "Wizard", "race": "Elf", "skills": {"magic": 28.0, "investigation": 22.0}},
            {"name": "Rogar Swiftfoot", "class": "Rogue", "race": "Halfling", "skills": {"stealth": 32.0, "dexterity": 27.0}},
            {"name": "Aria Brightshield", "class": "Cleric", "race": "Human", "skills": {"healing": 30.0, "wisdom": 24.0}},
        ]
        
        party = []
        reality_id = "dnd_scenario_realm_reality"
        
        for config in party_configs:
            console.print(f"[yellow]→[/yellow] Spawning {config['name']}...")
            
            being = self.being_system.spawn_being(
                reality_id=reality_id,
                parent_being_id=None,
                initial_skills=config["skills"]
            )
            
            member = PartyMember(being, config["name"], config["class"], config["race"])
            party.append(member)
            
            being.record_memory(
                f"Joined adventuring party as {config['class']}",
                "experience",
                {
                    "party_name": "The Eternal Guardians",
                    "class": config["class"],
                    "race": config["race"]
                }
            )
            
            console.print(f"   [green]✓[/green] {config['name']} ({config['race']} {config['class']}) spawned: {being.being_id}")
        
        self.party = party
        console.print(f"\n[bold green]✅ Party of {len(party)} members ready![/bold green]\n")
        
        # Save party state
        self.save_party_state()
        
        return party
    
    def save_party_state(self) -> None:
        """Save current party state."""
        party_state = {
            "party_members": [member.to_dict() for member in self.party],
            "total_hp": sum([m.hp for m in self.party]),
            "total_max_hp": sum([m.max_hp for m in self.party]),
            "average_level": sum([m.level for m in self.party]) / len(self.party) if self.party else 0,
            "saved_at": datetime.now().isoformat()
        }
        
        self.party_state_manager.save_party_state(party_state)
    
    def get_party(self) -> List[PartyMember]:
        """Get current party."""
        if not self.party:
            return self.spawn_party()
        return self.party
