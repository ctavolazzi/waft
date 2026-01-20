"""
Scenario Orchestrator - Main scenario execution engine.

Routes to different scenario modes and manages scenario flow.
"""

import random
from datetime import datetime
from typing import Any

from rich.console import Console
from rich.panel import Panel

from .encounter_generator import EncounterGenerator
from .lore_builder import LoreBuilder
from .party_manager import PartyManager
from .party_state_manager import PartyStateManager
from .scenario_realm import ScenarioRealm
from .security import validate_experiment_id, validate_iteration

console = Console()


class ScenarioOrchestrator:
    """
    Main scenario execution orchestrator.

    Features:
    - Scenario mode routing (encounter/explore/lore)
    - Scenario execution loop
    - Input validation
    - Rate limiting
    """

    def __init__(self, scenario_realm: ScenarioRealm):
        """
        Initialize Scenario Orchestrator.

        Args:
            scenario_realm: ScenarioRealm instance
        """
        self.realm = scenario_realm
        self.party_state_manager = PartyStateManager(scenario_realm)
        self.party_manager = PartyManager(scenario_realm)
        self.encounter_generator = EncounterGenerator(scenario_realm)
        self.lore_builder = LoreBuilder(scenario_realm)

        # Rate limiting (simple in-memory for now)
        self._crystallization_count = 0
        self._restoration_count = 0
        self._last_crystallization_time = None
        self._last_restoration_time = None

    def run_scenario(
        self, mode: str, experiment_id: str | None = None, iteration: int | None = None
    ) -> dict[str, Any]:
        """
        Run a scenario in the specified mode.

        Args:
            mode: Scenario mode (encounter, explore, lore, resume)
            experiment_id: Optional experiment ID (validated)
            iteration: Optional iteration number (validated)

        Returns:
            Scenario execution results
        """
        # Validate experiment ID if provided
        if experiment_id:
            is_valid, error = validate_experiment_id(experiment_id)
            if not is_valid:
                raise ValueError(f"Invalid experiment ID: {error}")

        # Validate iteration if provided
        if iteration is not None:
            is_valid, error = validate_iteration(iteration)
            if not is_valid:
                raise ValueError(f"Invalid iteration: {error}")

        # Route to appropriate mode
        if mode == "encounter":
            return self._run_encounter_scenario(experiment_id, iteration)
        elif mode == "explore":
            return self._run_exploration_scenario(experiment_id, iteration)
        elif mode == "lore":
            return self._run_lore_scenario(experiment_id, iteration)
        elif mode == "resume":
            return self._run_resume_scenario()
        else:
            raise ValueError(f"Unknown scenario mode: {mode}")

    def _run_encounter_scenario(
        self, experiment_id: str | None, iteration: int | None
    ) -> dict[str, Any]:
        """Run an encounter scenario."""
        console.print(Panel.fit("[bold cyan]⚔️  ENCOUNTER SCENARIO[/bold cyan]", style="cyan"))

        # Get or spawn party
        party = self.party_manager.get_party()

        # Generate encounter
        encounter = self.encounter_generator.generate_encounter(party=party, difficulty="medium")

        # Save party state after encounter
        self.party_manager.save_party_state()

        return {
            "mode": "encounter",
            "status": "complete",
            "encounter": encounter,
            "party_hp": sum([m.hp for m in party]),
            "party_max_hp": sum([m.max_hp for m in party]),
            "experiment_id": experiment_id,
            "iteration": iteration,
            "timestamp": datetime.now().isoformat(),
        }

    def _run_exploration_scenario(
        self, experiment_id: str | None, iteration: int | None
    ) -> dict[str, Any]:
        """Run an exploration scenario."""
        console.print(Panel.fit("[bold cyan]🗺️  EXPLORATION SCENARIO[/bold cyan]", style="cyan"))

        # Get party
        party = self.party_manager.get_party()

        # Generate exploration location
        locations = [
            "Ancient Ruins",
            "Mysterious Forest",
            "Hidden Cave",
            "Abandoned Village",
            "Mountain Pass",
            "River Crossing",
        ]

        location = random.choice(locations)

        console.print(f"[yellow]The party explores {location}...[/yellow]")

        # Add lore entry for location
        lore_file = self.lore_builder.add_lore_entry(
            category="locations",
            entry_name=location,
            entry_data={
                "description": f"The party discovered {location} during their exploration.",
                "details": {
                    "discovered_by": ", ".join([m.name for m in party]),
                    "discovered_at": datetime.now().isoformat(),
                },
            },
        )

        console.print(f"[green]✅ Discovered {location}![/green]")
        console.print(f"   Lore entry created: {lore_file.name}")

        # Save party state
        self.party_manager.save_party_state()

        return {
            "mode": "explore",
            "status": "complete",
            "location": location,
            "lore_file": str(lore_file),
            "experiment_id": experiment_id,
            "iteration": iteration,
            "timestamp": datetime.now().isoformat(),
        }

    def _run_lore_scenario(
        self, experiment_id: str | None, iteration: int | None
    ) -> dict[str, Any]:
        """Run a lore building scenario."""
        console.print(Panel.fit("[bold cyan]📖 LORE BUILDING SCENARIO[/bold cyan]", style="cyan"))

        # Get party
        party = self.party_manager.get_party()

        # Generate NPC or event

        npc_names = [
            "Elder Thorne",
            "Merchant Kael",
            "Scholar Elara",
            "Guard Captain Rik",
            "Mystic Zara",
            "Bard Finn",
        ]
        event_types = [
            "Festival Celebration",
            "Ancient Prophecy",
            "Trade Agreement",
            "Mysterious Sign",
            "Heroic Deed",
            "Legendary Tale",
        ]

        if random.random() < 0.5:
            # Create NPC lore
            npc_name = random.choice(npc_names)
            console.print(f"[yellow]The party meets {npc_name}...[/yellow]")

            lore_file = self.lore_builder.add_lore_entry(
                category="npcs",
                entry_name=npc_name,
                entry_data={
                    "description": f"The party encountered {npc_name}, who shared valuable information about the realm.",
                    "details": {
                        "encountered_by": ", ".join([m.name for m in party]),
                        "encountered_at": datetime.now().isoformat(),
                        "role": random.choice(["Merchant", "Scholar", "Guard", "Mystic", "Bard"]),
                    },
                },
            )

            console.print(f"[green]✅ Met {npc_name}![/green]")
            console.print(f"   Lore entry created: {lore_file.name}")

            lore_type = "npc"
            lore_name = npc_name
        else:
            # Create event lore
            event_name = random.choice(event_types)
            console.print(f"[yellow]The party witnesses {event_name}...[/yellow]")

            lore_file = self.lore_builder.add_lore_entry(
                category="events",
                entry_name=event_name,
                entry_data={
                    "description": f"The party witnessed {event_name}, an important event in the realm's history.",
                    "details": {
                        "witnessed_by": ", ".join([m.name for m in party]),
                        "witnessed_at": datetime.now().isoformat(),
                        "significance": "Historical",
                    },
                },
            )

            console.print(f"[green]✅ Witnessed {event_name}![/green]")
            console.print(f"   Lore entry created: {lore_file.name}")

            lore_type = "event"
            lore_name = event_name

        # Save party state
        self.party_manager.save_party_state()

        return {
            "mode": "lore",
            "status": "complete",
            "lore_type": lore_type,
            "lore_name": lore_name,
            "lore_file": str(lore_file),
            "experiment_id": experiment_id,
            "iteration": iteration,
            "timestamp": datetime.now().isoformat(),
        }

    def _run_resume_scenario(self) -> dict[str, Any]:
        """Resume from last scenario state."""
        console.print(Panel.fit("[bold cyan]▶️  RESUMING SCENARIO[/bold cyan]", style="cyan"))

        # Load party state
        party_state = self.party_state_manager.load_party_state()

        if party_state is None:
            return {
                "mode": "resume",
                "status": "no_state_found",
                "message": "No saved party state found. Starting new scenario.",
            }

        return {
            "mode": "resume",
            "status": "resumed",
            "party_state": party_state,
            "timestamp": datetime.now().isoformat(),
        }

    def get_party_state(self) -> dict[str, Any] | None:
        """Get current party state."""
        return self.party_state_manager.load_party_state()
