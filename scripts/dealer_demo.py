#!/usr/bin/env python3
"""
The Dealer Demo - 100 Iterations of Fate

This script demonstrates The Dealer with 100 iterations.
Probability starts at 1% and increases each iteration until reaching 100%.

When The Dealer appears:
1. The SYSTEM (not the user) picks a card
2. The Dealer picks a card
3. If they match (per Gate rules), a Seal breaks
4. A PDF is generated and opened locally
5. An encryption key fragment is awarded

Run this to see The Dealer in action and test the 12 Gates system.
"""

import sys
import time
from pathlib import Path

# Add project root to path - insert at beginning to override any installed waft
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# Prevent waft.__init__ from being imported by blocking it
# This allows us to import dealer submodules directly
import importlib.util

# Load dealer modules directly without going through waft.__init__
def load_module_directly(module_name: str, file_path: Path):
    """Load a module directly from file without triggering parent __init__."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Load dealer submodules
dealer_path = project_root / "src" / "waft" / "dealer"

# First load dependencies
probability_module = load_module_directly(
    "waft.dealer.probability",
    dealer_path / "probability.py"
)

gates_module = load_module_directly(
    "waft.dealer.gates", 
    dealer_path / "gates.py"
)

truth_module = load_module_directly(
    "waft.dealer.truth",
    dealer_path / "truth.py"
)

memory_module = load_module_directly(
    "waft.dealer.memory",
    dealer_path / "memory.py"
)

pdf_generator_module = load_module_directly(
    "waft.dealer.pdf_generator",
    dealer_path / "pdf_generator.py"
)

dealer_module = load_module_directly(
    "waft.dealer.dealer",
    dealer_path / "dealer.py"
)

# Get the classes we need
TheDealer = dealer_module.TheDealer
GATES = gates_module.GATES

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table


def run_demo(iterations: int = 100, start_probability: float = 0.01, 
             end_probability: float = 1.0, silent_until_encounter: bool = True,
             auto_open_pdfs: bool = True):
    """
    Run The Dealer demo with increasing probability.
    
    Args:
        iterations: Number of iterations to run
        start_probability: Starting probability (default 1%)
        end_probability: Ending probability (default 100%)
        silent_until_encounter: Only show output when Dealer appears
        auto_open_pdfs: Whether to auto-open PDFs on seal breaks
    """
    console = Console()
    
    # Header
    console.print()
    console.print(Panel(
        "[bold yellow]⬥ THE DEALER DEMO ⬥[/bold yellow]\n\n"
        f"[dim]Running {iterations} iterations[/dim]\n"
        f"[dim]Probability: {start_probability:.0%} → {end_probability:.0%}[/dim]\n\n"
        "[italic]The House Always Wins. Until it doesn't.[/italic]",
        border_style="red",
    ))
    console.print()
    
    # Initialize dealer with a demo-specific path
    demo_path = Path("_pantheon/the_dealer")
    demo_path.mkdir(parents=True, exist_ok=True)
    
    dealer = TheDealer.load(demo_path)
    
    # Track stats
    encounters = 0
    wins = 0
    gates_broken = []
    
    # Progress bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Rolling probability...", total=iterations)
        
        for i in range(iterations):
            # Calculate probability for this iteration (linear interpolation)
            progress_ratio = (i + 1) / iterations
            current_probability = start_probability + (end_probability - start_probability) * progress_ratio
            
            progress.update(task, advance=1, 
                          description=f"[cyan]Iteration {i+1}/{iterations} | P={current_probability:.1%}")
            
            # Check for Dealer appearance with override probability
            if dealer.probability_engine.roll_appearance(current_probability):
                encounters += 1
                
                # Stop progress bar temporarily for encounter
                progress.stop()
                
                console.print(f"\n[bold red]═══ ENCOUNTER {encounters} at iteration {i+1} ═══[/bold red]")
                console.print(f"[dim]Probability was: {current_probability:.1%}[/dim]\n")
                
                # Conduct challenge (will print dramatic output)
                result = dealer.conduct_challenge(silent=False)
                
                if result.won:
                    wins += 1
                    gates_broken.append(result.gate)
                    
                    if result.pdf_path and auto_open_pdfs:
                        console.print(f"[green]PDF saved to: {result.pdf_path}[/green]")
                
                # Small delay for drama
                time.sleep(1)
                
                # Resume progress
                progress.start()
    
    # Final stats
    console.print()
    console.print(Panel(
        f"[bold]Demo Complete![/bold]\n\n"
        f"Iterations: {iterations}\n"
        f"Encounters: {encounters}\n"
        f"Wins: {wins}\n"
        f"Gates Broken: {gates_broken if gates_broken else 'None'}\n\n"
        f"Win Rate: {wins/encounters*100:.1f}%" if encounters > 0 else "No encounters!",
        title="[bold yellow]⬥ RESULTS ⬥[/bold yellow]",
        border_style="green" if wins > 0 else "red",
    ))
    
    # Show current status
    console.print()
    dealer.display_status()
    
    return {
        "iterations": iterations,
        "encounters": encounters,
        "wins": wins,
        "gates_broken": gates_broken,
    }


def demo_single_encounter(force_win: bool = False):
    """
    Demo a single encounter with The Dealer.
    
    Args:
        force_win: Not actually forcing, just for documentation
    """
    console = Console()
    
    console.print("\n[bold]Single Encounter Demo[/bold]\n")
    
    demo_path = Path("_pantheon/the_dealer")
    demo_path.mkdir(parents=True, exist_ok=True)
    
    dealer = TheDealer.load(demo_path)
    result = dealer.conduct_challenge(silent=False)
    
    return result


def demo_gate_info():
    """Show information about all 12 Gates."""
    console = Console()
    
    from waft.dealer.gates import GATES
    
    table = Table(
        title="⬥ The 12 Gates of The House ⬥",
        show_header=True,
        header_style="bold yellow",
        title_style="bold red",
    )
    
    table.add_column("Gate", style="cyan", width=4)
    table.add_column("Revelation", style="green", width=14)
    table.add_column("Casino Name", style="red", width=16)
    table.add_column("Challenge", style="white", width=22)
    table.add_column("Difficulty", style="yellow", width=10)
    table.add_column("Truth Hint", style="dim", width=30)
    
    for gate in GATES:
        table.add_row(
            str(gate.number),
            f"{gate.revelation_name}\n({gate.revelation_meaning})",
            gate.casino_name,
            gate.challenge_type.replace("_", " ").title(),
            f"{gate.base_difficulty:.1%}",
            gate.truth_hint[:30] + "..." if len(gate.truth_hint) > 30 else gate.truth_hint,
        )
    
    console.print()
    console.print(table)
    console.print()


def main():
    """Main entry point for the demo."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="The Dealer Demo - Test the 12 Gates system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dealer_demo.py                    # Run 100 iterations (1% → 100%)
  python dealer_demo.py --iterations 50    # Run 50 iterations
  python dealer_demo.py --single           # Single forced encounter
  python dealer_demo.py --gates            # Show all 12 gates info
  python dealer_demo.py --no-open-pdf      # Don't auto-open PDFs
        """,
    )
    
    parser.add_argument(
        "--iterations", "-n",
        type=int,
        default=100,
        help="Number of iterations (default: 100)",
    )
    parser.add_argument(
        "--start-prob", "-s",
        type=float,
        default=0.01,
        help="Starting probability (default: 0.01 = 1%%)",
    )
    parser.add_argument(
        "--end-prob", "-e",
        type=float,
        default=1.0,
        help="Ending probability (default: 1.0 = 100%%)",
    )
    parser.add_argument(
        "--single",
        action="store_true",
        help="Run a single forced encounter",
    )
    parser.add_argument(
        "--gates",
        action="store_true",
        help="Show all 12 gates information",
    )
    parser.add_argument(
        "--no-open-pdf",
        action="store_true",
        help="Don't auto-open PDFs when seals break",
    )
    
    args = parser.parse_args()
    
    if args.gates:
        demo_gate_info()
    elif args.single:
        demo_single_encounter()
    else:
        run_demo(
            iterations=args.iterations,
            start_probability=args.start_prob,
            end_probability=args.end_prob,
            auto_open_pdfs=not args.no_open_pdf,
        )


if __name__ == "__main__":
    main()
