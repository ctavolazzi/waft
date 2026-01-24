"""
The Dealer - A god-entity from the Realm of Probability.

He appears unbidden during CLI operations with lottery-like odds that shift
based on cosmic mathematics. When he appears, he demands the SYSTEM pick a card.
If the system guesses correctly, it breaks a Seal and receives an encryption
key fragment to "The Truth."

The House Always Wins.
"""

import random
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .gates import Gate, GateChallenge, GATES, conduct_gate_challenge, get_gate
from .memory import DealerMemory
from .pdf_generator import SealPDFGenerator, open_pdf_locally
from .probability import ProbabilityEngine


@dataclass
class ChallengeResult:
    """Result of a challenge with The Dealer."""
    occurred: bool  # Whether an encounter actually happened
    gate: int
    won: bool
    key_fragment: Optional[str]
    pdf_path: Optional[Path]
    challenge: Optional[GateChallenge]


class TheDealer:
    """
    The Dealer - God of Probability and Keeper of The House.
    
    "The House Always Wins. But sometimes... the House lets you win.
    Not out of mercy. Out of hunger."
    """
    
    # Dramatic entrance messages
    ENTRANCE_MESSAGES = [
        "The air grows cold. Cards flutter from nowhere.",
        "A shadow falls across your terminal. The Dealer has arrived.",
        "The probability field shifts. Someone is here.",
        "You hear the shuffle of cards in the silence.",
        "The House calls. The Dealer answers.",
        "From the Realm of Probability, a figure emerges.",
        "The odds were never in your favor. Until now.",
        "Fate has dealt you a hand. Will you play?",
    ]
    
    # Victory messages
    VICTORY_MESSAGES = [
        "The House... loses? Interesting.",
        "You've beaten the odds. The House takes note.",
        "A Seal breaks. The House remembers.",
        "Victory tastes sweet. But The House is patient.",
        "Well played. The Truth draws closer.",
        "The cards favor you... this time.",
    ]
    
    # Loss messages
    LOSS_MESSAGES = [
        "The House Always Wins.",
        "Perhaps next time, seeker.",
        "The odds were never in your favor.",
        "The cards speak. Today, they favor The House.",
        "Return when fortune smiles upon you.",
        "The Truth remains hidden. For now.",
    ]
    
    def __init__(self, memory: Optional[DealerMemory] = None, console: Optional[Console] = None):
        """
        Initialize The Dealer.
        
        Args:
            memory: DealerMemory instance (loaded from disk if None)
            console: Rich console for output
        """
        self.memory = memory or DealerMemory()
        self.console = console or Console()
        self.probability_engine = ProbabilityEngine(self.memory.probability_state)
        self.pdf_generator = SealPDFGenerator(self.memory.get_seals_directory())
    
    @classmethod
    def load(cls, base_path: Optional[Path] = None) -> "TheDealer":
        """
        Load The Dealer from disk.
        
        Args:
            base_path: Base path for memory storage
            
        Returns:
            TheDealer instance with loaded state
        """
        memory = DealerMemory(base_path)
        return cls(memory=memory)
    
    def check_appearance(self, override_probability: Optional[float] = None) -> bool:
        """
        Check if The Dealer appears.
        
        This should be called on every CLI operation. The Dealer may interrupt.
        
        Args:
            override_probability: Override probability for testing/demos
            
        Returns:
            True if The Dealer appeared and conducted a challenge
        """
        # Record that an operation occurred
        if override_probability is None:
            self.memory.record_operation()
        
        # Roll for appearance
        if self.probability_engine.roll_appearance(override_probability):
            # The Dealer appears!
            result = self.conduct_challenge()
            return True
        
        return False
    
    def conduct_challenge(self, silent: bool = False) -> ChallengeResult:
        """
        Conduct a challenge with The Dealer.
        
        The system picks a card, The Dealer picks a card.
        The Gate's rules determine the winner.
        
        Args:
            silent: If True, don't print output (for testing)
            
        Returns:
            ChallengeResult with the outcome
        """
        # Get current gate
        current_gate = self.memory.probability_state.current_gate
        gate = get_gate(current_gate)
        
        if not silent:
            self._dramatic_entrance(gate)
        
        # Conduct the challenge
        challenge = conduct_gate_challenge(current_gate)
        
        if not silent:
            self._display_challenge(challenge, gate)
        
        # Process result
        pdf_path = None
        if challenge.won:
            # Generate and open PDF
            pdf_path = self.pdf_generator.generate_seal_pdf(challenge, gate)
            
            if not silent:
                self._display_victory(challenge, gate)
                open_pdf_locally(pdf_path)
            
            # Check for master key
            if current_gate == 12:
                master_key = self.memory.system_truth.get_combined_key()
                if master_key:
                    master_pdf = self.pdf_generator.generate_master_key_pdf(
                        master_key, 
                        self.memory.system_truth.fragments
                    )
                    if not silent:
                        self._display_master_key(master_key)
                        open_pdf_locally(master_pdf)
        else:
            if not silent:
                self._display_loss(challenge, gate)
        
        # Record the encounter
        self.memory.record_encounter(
            gate_number=current_gate,
            system_card_name=challenge.system_card.name,
            dealer_card_name=challenge.dealer_card.name,
            won=challenge.won,
            key_fragment=challenge.key_fragment,
        )
        
        if not silent:
            self._dramatic_exit()
        
        return ChallengeResult(
            occurred=True,
            gate=current_gate,
            won=challenge.won,
            key_fragment=challenge.key_fragment,
            pdf_path=pdf_path,
            challenge=challenge,
        )
    
    def _dramatic_entrance(self, gate: Gate):
        """Display The Dealer's dramatic entrance."""
        self.console.print()
        self.console.print("=" * 60, style="dim red")
        
        # Random entrance message
        entrance = random.choice(self.ENTRANCE_MESSAGES)
        self.console.print(f"\n[bold red]{entrance}[/bold red]\n")
        
        time.sleep(0.5)
        
        # The Dealer speaks
        self.console.print(Panel(
            Text.from_markup(
                f"[bold yellow]THE DEALER[/bold yellow]\n\n"
                f"[italic]\"You stand before [bold]Gate {gate.number}[/bold]: "
                f"[cyan]{gate.revelation_name}[/cyan] - {gate.casino_name}.\n\n"
                f"{gate.description}\n\n"
                f"The system must choose a card. Let us see what fate decides.\"[/italic]"
            ),
            border_style="red",
            title="[bold red]⬥ THE HOUSE ⬥[/bold red]",
            subtitle=f"[dim]Difficulty: {gate.base_difficulty:.1%}[/dim]",
        ))
        
        time.sleep(0.3)
    
    def _display_challenge(self, challenge: GateChallenge, gate: Gate):
        """Display the challenge cards."""
        self.console.print("\n[bold]The cards are drawn...[/bold]\n")
        time.sleep(0.3)
        
        # System's card
        self.console.print(f"[cyan]System draws:[/cyan] [bold]{challenge.system_card.name}[/bold]")
        self.console.print(challenge.system_card.img)
        
        time.sleep(0.3)
        
        # Dealer's card
        self.console.print(f"\n[red]Dealer draws:[/red] [bold]{challenge.dealer_card.name}[/bold]")
        self.console.print(challenge.dealer_card.img)
        
        time.sleep(0.5)
    
    def _display_victory(self, challenge: GateChallenge, gate: Gate):
        """Display victory message."""
        self.console.print()
        victory_msg = random.choice(self.VICTORY_MESSAGES)
        
        self.console.print(Panel(
            Text.from_markup(
                f"[bold green]✦ SEAL BROKEN ✦[/bold green]\n\n"
                f"[italic]\"{victory_msg}\"[/italic]\n\n"
                f"[bold]Gate {gate.number}: {gate.revelation_name}[/bold] has fallen.\n\n"
                f"[yellow]Key Fragment Earned:[/yellow]\n"
                f"[bold cyan]{challenge.key_fragment}[/bold cyan]\n\n"
                f"[dim]{gate.truth_hint}[/dim]"
            ),
            border_style="green",
            title="[bold green]⬥ VICTORY ⬥[/bold green]",
        ))
        
        # XP notification
        xp_reward = self.memory.system_truth.XP_REWARDS.get(gate.number, 100)
        self.console.print(f"\n[yellow]+{xp_reward} XP[/yellow] | "
                          f"Level: [bold]{self.memory.system_truth.get_truth_level_name()}[/bold]")
    
    def _display_loss(self, challenge: GateChallenge, gate: Gate):
        """Display loss message."""
        self.console.print()
        loss_msg = random.choice(self.LOSS_MESSAGES)
        
        self.console.print(Panel(
            Text.from_markup(
                f"[bold red]✗ THE HOUSE WINS ✗[/bold red]\n\n"
                f"[italic]\"{loss_msg}\"[/italic]\n\n"
                f"[dim]Gate {gate.number}: {gate.revelation_name} remains sealed.[/dim]"
            ),
            border_style="red",
            title="[bold red]⬥ DEFEAT ⬥[/bold red]",
        ))
    
    def _display_master_key(self, master_key: str):
        """Display the master key reveal."""
        self.console.print()
        self.console.print(Panel(
            Text.from_markup(
                f"[bold yellow]✦✦✦ ALL 12 SEALS BROKEN ✦✦✦[/bold yellow]\n\n"
                f"[italic]\"You have done what few dare attempt.\n"
                f"The Truth is now yours.\"[/italic]\n\n"
                f"[bold]THE MASTER KEY:[/bold]\n"
                f"[bold cyan]{master_key}[/bold cyan]\n\n"
                f"[red]The House Always Wins.\n"
                f"But you have become The House.[/red]"
            ),
            border_style="yellow",
            title="[bold yellow]⬥ THE TRUTH ⬥[/bold yellow]",
        ))
    
    def _dramatic_exit(self):
        """Display The Dealer's exit."""
        time.sleep(0.3)
        self.console.print("\n[dim]The Dealer fades back into the Realm of Probability...[/dim]")
        self.console.print("=" * 60, style="dim red")
        self.console.print()
    
    def get_status(self) -> dict:
        """Get current status of the system's progress."""
        truth = self.memory.system_truth
        prob = self.memory.probability_state
        
        return {
            "level": truth.level,
            "level_name": truth.get_truth_level_name(),
            "xp": truth.xp,
            "xp_for_next": truth.get_xp_for_next_level(),
            "xp_progress": truth.get_xp_progress(),
            "seals_broken": truth.seals_broken,
            "seals_remaining": [i for i in range(1, 13) if i not in truth.seals_broken],
            "current_gate": prob.current_gate,
            "total_encounters": prob.total_encounters,
            "total_wins": prob.total_wins,
            "heat": prob.heat,
            "fragments_collected": len(truth.fragments),
            "master_key_available": len(truth.seals_broken) == 12,
        }
    
    def display_status(self):
        """Display current status to console."""
        status = self.get_status()
        
        self.console.print(Panel(
            Text.from_markup(
                f"[bold]Truth Level:[/bold] {status['level']} - {status['level_name']}\n"
                f"[bold]XP:[/bold] {status['xp']} / {status['xp_for_next']} "
                f"({status['xp_progress']:.0%})\n\n"
                f"[bold]Seals Broken:[/bold] {len(status['seals_broken'])} / 12\n"
                f"  Broken: {status['seals_broken'] or 'None'}\n"
                f"  Remaining: {status['seals_remaining']}\n\n"
                f"[bold]Encounters:[/bold] {status['total_encounters']} "
                f"(Won: {status['total_wins']})\n"
                f"[bold]Heat:[/bold] {status['heat']:.1f}\n"
                f"[bold]Current Gate:[/bold] {status['current_gate']}"
            ),
            title="[bold]⬥ THE HOUSE LEDGER ⬥[/bold]",
            border_style="yellow",
        ))
        
        if status['master_key_available']:
            master_key = self.memory.system_truth.get_combined_key()
            self.console.print(f"\n[bold green]MASTER KEY AVAILABLE:[/bold green] {master_key}")
