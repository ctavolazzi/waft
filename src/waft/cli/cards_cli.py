"""
Cards CLI - Playing cards utility and Dealer status commands.

Basic card operations plus status checks for The Dealer and the 12 Gates.
"""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ..dealer.card_generator import create_card, new_deck
from ..dealer.card_generator import draw_card as draw_playing_card
from ..dealer.card_generator import draw_hand as draw_playing_hand

app = typer.Typer(
    name="cards",
    help="Playing cards utility and The Dealer status",
    add_completion=False,
)

console = Console()


# Suit mapping for card creation
SUIT_MAP = {"S": 0, "C": 1, "H": 2, "D": 3}
SUIT_NAMES = {0: "Spades", 1: "Clubs", 2: "Hearts", 3: "Diamonds"}
RANK_MAP = {"A": 1, "J": 11, "Q": 12, "K": 13}


def parse_card_string(card_str: str) -> tuple[int, int]:
    """
    Parse a card string like 'AS' or '10H' into value and suit.
    
    Args:
        card_str: Card string (e.g., 'AS', '10H', 'KD')
        
    Returns:
        Tuple of (value, suit) for Card creation
    """
    card_str = card_str.upper().strip()

    # Handle 10 specially
    if card_str.startswith("10"):
        rank = "10"
        suit = card_str[2:]
    else:
        rank = card_str[:-1]
        suit = card_str[-1]

    # Parse rank
    if rank in RANK_MAP:
        value = RANK_MAP[rank]
    else:
        value = int(rank)

    # Parse suit
    suit_num = SUIT_MAP.get(suit)
    if suit_num is None:
        raise ValueError(f"Invalid suit: {suit}. Use S, C, H, or D.")

    return value, suit_num


@app.command("draw")
def draw_card():
    """Draw a single random card from a fresh deck."""
    deck = new_deck()
    card = draw_playing_card(deck)

    console.print(f"\n[bold cyan]{card.name}[/bold cyan]\n")
    console.print(card.img)
    console.print()


@app.command("hand")
def draw_hand(
    count: int = typer.Option(5, "--count", "-n", help="Number of cards to draw"),
):
    """Draw a hand of cards from a fresh deck."""
    if count < 1 or count > 52:
        console.print("[red]Count must be between 1 and 52[/red]")
        raise typer.Exit(1)

    deck = new_deck()
    hand = draw_playing_hand(deck, count)

    console.print(f"\n[bold]Drew {count} cards:[/bold]\n")

    for card in hand.cards:
        console.print(f"[cyan]{card.name}[/cyan]")
        console.print(card.img)
        console.print()


@app.command("shuffle")
def shuffle_deck():
    """Create and shuffle a new deck, showing deck stats."""
    deck = new_deck()
    deck.shuffle()

    console.print("\n[green]✓[/green] Deck shuffled")
    console.print(f"  Cards remaining: {deck.remaining}")
    console.print(f"  Cards drawn: {deck.drawn}")
    console.print()


@app.command("info")
def card_info(
    card_str: str = typer.Argument(..., help="Card to show (e.g., AS, 10H, KD)"),
):
    """Show information about a specific card."""
    try:
        value, suit = parse_card_string(card_str)
        card = create_card(value=value, suit=suit)

        console.print(f"\n[bold cyan]{card.name}[/bold cyan]\n")
        console.print(f"  Value: {card.value}")
        console.print(f"  Suit: {card.suit_name} (#{card.suit})")
        console.print(f"  Rank: {card.rank}")
        console.print()
        console.print(card.img)
        console.print()

    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("[dim]Format: RANK + SUIT (e.g., AS, 10H, KD, 2C)[/dim]")
        raise typer.Exit(1)


@app.command("dealer-status")
def dealer_status(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path"),
):
    """Show The Dealer's current status and your progress through the 12 Gates."""
    from ..dealer import TheDealer

    base_path = Path(path) / "_pantheon/the_dealer" if path else None
    dealer = TheDealer.load(base_path)

    dealer.display_status()


@app.command("summon")
def summon_dealer(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path"),
    force: bool = typer.Option(False, "--force", "-f", help="Force dealer to appear (100% chance)"),
):
    """
    Attempt to summon The Dealer for a challenge.
    
    Normally, The Dealer appears with very low probability.
    Use --force to guarantee an appearance (for testing).
    """
    from ..dealer import TheDealer

    base_path = Path(path) / "_pantheon/the_dealer" if path else None
    dealer = TheDealer.load(base_path)

    if force:
        console.print("[yellow]Forcing The Dealer to appear...[/yellow]")
        dealer.conduct_challenge()
    else:
        probability = dealer.probability_engine.calculate_appearance_chance()
        console.print(f"[dim]Current appearance probability: {probability:.6%}[/dim]")

        if dealer.check_appearance():
            pass  # Challenge was conducted
        else:
            console.print("\n[dim]The Dealer does not appear... yet.[/dim]")
            console.print("[dim]Try again, or use --force to guarantee an appearance.[/dim]")


@app.command("gates")
def show_gates():
    """Show information about all 12 Gates of The House."""
    from ..dealer.gates import GATES

    table = Table(
        title="⬥ The 12 Gates of The House ⬥",
        show_header=True,
        header_style="bold yellow",
    )

    table.add_column("Gate", style="cyan", width=4)
    table.add_column("Revelation", style="green", width=12)
    table.add_column("Casino Name", style="red", width=15)
    table.add_column("Challenge", style="white", width=20)
    table.add_column("Difficulty", style="yellow", width=10)

    for gate in GATES:
        table.add_row(
            str(gate.number),
            gate.revelation_name,
            gate.casino_name,
            gate.challenge_type.replace("_", " ").title(),
            f"{gate.base_difficulty:.1%}",
        )

    console.print()
    console.print(table)
    console.print()


@app.command("history")
def show_history(
    limit: int = typer.Option(10, "--limit", "-n", help="Number of encounters to show"),
    path: str | None = typer.Option(None, "--path", "-p", help="Project path"),
):
    """Show recent encounter history with The Dealer."""
    from ..dealer import DealerMemory

    base_path = Path(path) / "_pantheon/the_dealer" if path else Path("_pantheon/the_dealer")
    memory = DealerMemory(base_path)

    encounters = memory.get_encounter_history(limit=limit)

    if not encounters:
        console.print("[dim]No encounters recorded yet.[/dim]")
        return

    table = Table(
        title="⬥ Encounter History ⬥",
        show_header=True,
        header_style="bold",
    )

    table.add_column("Time", style="dim")
    table.add_column("Gate", style="cyan")
    table.add_column("System Card", style="green")
    table.add_column("Dealer Card", style="red")
    table.add_column("Result", style="bold")

    for enc in encounters:
        result = "[green]WIN[/green]" if enc.won else "[red]LOSS[/red]"
        table.add_row(
            enc.timestamp.strftime("%Y-%m-%d %H:%M"),
            str(enc.gate_number),
            enc.system_card,
            enc.dealer_card,
            result,
        )

    console.print()
    console.print(table)
    console.print()


@app.command("journal")
def dealer_journal(
    path: str | None = typer.Option(None, "--path", "-p", help="Project path"),
):
    """Generate The Dealer's journal from encounter memory."""
    from ..core.dealer_journal import generate_journal

    project_path = Path(path) if path else Path.cwd()
    journal = generate_journal(project_path)

    console.print()
    for line in journal.split("\n"):
        if line.startswith("# "):
            console.print(f"[bold #FFD700]{line}[/bold #FFD700]")
        elif line.startswith("## "):
            console.print(f"[bold cyan]{line}[/bold cyan]")
        elif line.startswith("*"):
            console.print(f"[dim]{line}[/dim]")
        else:
            console.print(line)
    console.print()
