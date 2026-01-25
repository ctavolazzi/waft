"""
WAFT CLI Banner: Epic ASCII Art and Enhanced Output.

Because every great CLI deserves a legendary banner.
"""

import random
import sys
from typing import Literal

# Rich library for beautiful terminal output
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.style import Style
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich import box

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


# ASCII Art Banners
BANNER_WAVE = r"""
 ██╗    ██╗ █████╗ ███████╗████████╗
 ██║    ██║██╔══██╗██╔════╝╚══██╔══╝
 ██║ █╗ ██║███████║█████╗     ██║
 ██║███╗██║██╔══██║██╔══╝     ██║
 ╚███╔███╔╝██║  ██║██║        ██║
  ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝        ╚═╝
"""

BANNER_CYBER = r"""
╦ ╦╔═╗╔═╗╔╦╗
║║║╠═╣╠╣  ║
╚╩╝╩ ╩╚   ╩
"""

BANNER_BLOCKS = r"""
█   █ █▀█ █▀▀ ▀█▀
█▄█▄█ █▀█ █▀▀  █
 ▀ ▀  ▀ ▀ ▀    ▀
"""

BANNER_NEON = r"""
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█ ░██   ██░░█░▄▀█░▄▄░█▄▄░▄▄██ ▄▄▄█▄▄░▄▄██
█ ███   ██▄▄█░█▀█░▄███▀█░██▀█ ▄▄▄██▀█░█▀██
█ ▀█▀   ▀▄▄▄█▄▄▄█▄▄▄███▄███▄█▄▄▄▄█▄▄█▄▄▄▄█
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
"""

BANNER_MATRIX = r"""
┌─┐ ┬ ┬┌─┐┌─┐┌┬┐
│ │ │ │├─┤│ │ │
└─┘ └─┘┴ ┴└─┘ ┴
╦ ╦┌─┐┬  ┬┌─┐  ╔═╗┌─┐┌─┐┌┐┌┌┬┐
║║║├─┤└┐┌┘├┤   ╠═╣│ ┬├┤ │││ │
╚╩╝┴ ┴ └┘ └─┘  ╩ ╩└─┘└─┘┘└┘ ┴
╔═╗┬─┐┌─┐┌┬┐┌─┐┬ ┬┌─┐┬─┐┬┌─
╠╣ ├┬┘├─┤│││├┤ ││││ │├┬┘├┴┐
╚  ┴└─┴ ┴┴ ┴└─┘└┴┘└─┘┴└─┴ ┴
"""

BANNER_MINIMAL = r"""
 _    _  ___  ______ _____
| |  | |/ _ \ |  ___|_   _|
| |  | / /_\ \| |_    | |
| |/\| |  _  ||  _|   | |
\  /\  / | | || |     | |
 \/  \/\_| |_/\_|     \_/
"""

BANNER_EPIC = r"""
                                  ████████████
                              ██████░░░░░░░░████
                           █████░░░░░░░░░░░░░░░███
                         ████░░░░░░░░░░░░░░░░░░░░███
                        ███░░░░░░░░░░░░░░░░░░░░░░░░██
 ██╗    ██╗ █████╗     ███░░░░░░░░░░░░░░░░░░░░░░░░░██
 ██║    ██║██╔══██╗    ██░░░░░░░░░░░░░░░░░░░░░░░░░░░██
 ██║ █╗ ██║███████║    ██░░░░░░░███████████░░░░░░░░░██
 ██║███╗██║██╔══██║    ██░░░░████▒▒▒▒▒▒▒▒████░░░░░░░██
 ╚███╔███╔╝██║  ██║    ██░░░██▒▒▒▒▒▒▒▒▒▒▒▒▒▒██░░░░░░██
  ╚══╝╚══╝ ╚═╝  ╚═╝    ██░░░██▒▒▒▒▒▒▒▒▒▒▒▒▒▒██░░░░░░██
                        ██░░░██▒▒▒▒▒▒▒▒▒▒▒▒██░░░░░░██
 ███████╗████████╗       ██░░░░████▒▒▒▒▒▒████░░░░░██
 ██╔════╝╚══██╔══╝        ██░░░░░░░███████░░░░░░░██
 █████╗     ██║            ███░░░░░░░░░░░░░░░░░███
 ██╔══╝     ██║              ████░░░░░░░░░░░████
 ██║        ██║                █████████████
 ╚═╝        ╚═╝                     ██
                                    ██
         WAVE AGENT                 ██
      FRAMEWORK & TOOLS             ██
                               ████████████
"""

TAGLINES = [
    "Evolving Intelligence, One Generation at a Time",
    "Where Agents Learn to Transcend",
    "The Physics of Artificial Cognition",
    "Breeding Digital Gods Since 2024",
    "Directed Evolution for the Digital Age",
    "Watch Them Grow, Watch Them Learn",
    "Nature's Algorithm, Perfected",
    "From Chaos, Order Emerges",
    "Silicon Dreams, Carbon Ambitions",
    "The Future is Evolving",
]

TIPS = [
    "Use 'waft gym run' to test your agents' fitness",
    "The Battle Royale mode pits agents against each other",
    "Genetic crossover combines the best of two parents",
    "Flight Recorder tracks every evolutionary event",
    "Use 'waft evolve start' to begin evolution",
    "The Pantheon contains timeless guiding entities",
    "Check the visualizer at http://localhost:8000",
    "Use 'waft dashboard' for a quick status overview",
    "Beings can have skills, memories, and personality",
    "The Scint Detector finds styling divergences",
]


def get_random_banner() -> str:
    """Get a random banner."""
    banners = [BANNER_WAVE, BANNER_CYBER, BANNER_MINIMAL, BANNER_EPIC]
    return random.choice(banners)


def get_random_tagline() -> str:
    """Get a random tagline."""
    return random.choice(TAGLINES)


def get_random_tip() -> str:
    """Get a random tip."""
    return random.choice(TIPS)


def print_banner(
    style: Literal["wave", "cyber", "blocks", "neon", "matrix", "minimal", "epic", "random"] = "wave",
    show_tagline: bool = True,
    show_tip: bool = True,
    show_version: bool = True,
) -> None:
    """
    Print the WAFT banner with optional extras.

    Args:
        style: Banner style to use
        show_tagline: Show random tagline
        show_tip: Show random tip
        show_version: Show version info
    """
    banners = {
        "wave": BANNER_WAVE,
        "cyber": BANNER_CYBER,
        "blocks": BANNER_BLOCKS,
        "neon": BANNER_NEON,
        "matrix": BANNER_MATRIX,
        "minimal": BANNER_MINIMAL,
        "epic": BANNER_EPIC,
        "random": get_random_banner(),
    }

    banner = banners.get(style, BANNER_WAVE)

    if RICH_AVAILABLE:
        _print_rich_banner(banner, show_tagline, show_tip, show_version)
    else:
        _print_simple_banner(banner, show_tagline, show_tip, show_version)


def _print_rich_banner(
    banner: str,
    show_tagline: bool,
    show_tip: bool,
    show_version: bool,
) -> None:
    """Print banner using Rich library."""
    console = Console()

    # Gradient colors for the banner
    colors = ["bright_blue", "blue", "cyan", "bright_cyan", "white"]

    # Print banner with color
    banner_text = Text()
    lines = banner.strip().split("\n")
    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        banner_text.append(line + "\n", style=color)

    console.print(banner_text)

    # Version info
    if show_version:
        console.print(
            "  [dim]Wave Agent Framework & Tools[/dim]  [bold cyan]v0.9.4[/bold cyan]",
            highlight=False,
        )
        console.print()

    # Tagline
    if show_tagline:
        tagline = get_random_tagline()
        console.print(
            f"  [italic bright_magenta]{tagline}[/italic bright_magenta]",
            highlight=False,
        )
        console.print()

    # Tip
    if show_tip:
        tip = get_random_tip()
        console.print(
            Panel(
                f"[yellow]Tip:[/yellow] {tip}",
                box=box.ROUNDED,
                border_style="dim",
                padding=(0, 2),
            )
        )
        console.print()


def _print_simple_banner(
    banner: str,
    show_tagline: bool,
    show_tip: bool,
    show_version: bool,
) -> None:
    """Print banner without Rich (fallback)."""
    print(banner)

    if show_version:
        print("  Wave Agent Framework & Tools  v0.9.4")
        print()

    if show_tagline:
        print(f"  {get_random_tagline()}")
        print()

    if show_tip:
        print(f"  Tip: {get_random_tip()}")
        print()


def print_success(message: str) -> None:
    """Print a success message."""
    if RICH_AVAILABLE:
        Console().print(f"[bold green]✓[/bold green] {message}")
    else:
        print(f"✓ {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    if RICH_AVAILABLE:
        Console().print(f"[bold red]✗[/bold red] {message}")
    else:
        print(f"✗ {message}", file=sys.stderr)


def print_warning(message: str) -> None:
    """Print a warning message."""
    if RICH_AVAILABLE:
        Console().print(f"[bold yellow]⚠[/bold yellow] {message}")
    else:
        print(f"⚠ {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    if RICH_AVAILABLE:
        Console().print(f"[bold blue]ℹ[/bold blue] {message}")
    else:
        print(f"ℹ {message}")


def print_agent_spawn(agent_name: str, generation: int, fitness: float | None = None) -> None:
    """Print agent spawn notification."""
    if RICH_AVAILABLE:
        console = Console()
        fitness_str = f" (fitness: {fitness:.2%})" if fitness else ""
        console.print(
            Panel(
                f"[bold cyan]🧬 Agent Spawned[/bold cyan]\n"
                f"Name: [bold]{agent_name}[/bold]\n"
                f"Generation: [yellow]{generation}[/yellow]{fitness_str}",
                box=box.DOUBLE,
                border_style="cyan",
                padding=(0, 2),
            )
        )
    else:
        print(f"🧬 Agent Spawned: {agent_name} (Gen {generation})")


def print_battle_result(
    winner: str,
    loser: str,
    winner_health: float,
    rounds: int,
) -> None:
    """Print battle result notification."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(
            Panel(
                f"[bold yellow]⚔️ BATTLE COMPLETE[/bold yellow]\n\n"
                f"[bold green]Winner:[/bold green] {winner}\n"
                f"[bold red]Defeated:[/bold red] {loser}\n"
                f"Health Remaining: [cyan]{winner_health:.1f}%[/cyan]\n"
                f"Rounds: [magenta]{rounds}[/magenta]",
                box=box.HEAVY,
                border_style="yellow",
                padding=(0, 2),
            )
        )
    else:
        print(f"⚔️ Battle Complete: {winner} defeats {loser}")


def print_evolution_progress(
    generation: int,
    population: int,
    best_fitness: float,
    avg_fitness: float,
) -> None:
    """Print evolution progress."""
    if RICH_AVAILABLE:
        console = Console()
        table = Table(
            title=f"Generation {generation}",
            box=box.SIMPLE_HEAD,
            show_header=True,
            header_style="bold cyan",
        )
        table.add_column("Metric", style="dim")
        table.add_column("Value", justify="right")

        table.add_row("Population", str(population))
        table.add_row("Best Fitness", f"{best_fitness:.2%}")
        table.add_row("Avg Fitness", f"{avg_fitness:.2%}")

        console.print(table)
    else:
        print(f"Gen {generation}: Pop={population}, Best={best_fitness:.2%}, Avg={avg_fitness:.2%}")


def create_progress_bar(description: str = "Processing"):
    """Create a progress bar context manager."""
    if RICH_AVAILABLE:
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
    else:
        # Fallback: return a dummy context manager
        class DummyProgress:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def add_task(self, description, total=100):
                print(f"{description}...")
                return 0

            def update(self, task_id, advance=1):
                pass

        return DummyProgress()


# Quick test
if __name__ == "__main__":
    print_banner("epic")
    print()
    print_success("Evolution initialized successfully!")
    print_info("Starting generation 1...")
    print_warning("Low population detected")
    print_error("Agent failed fitness test")
    print()
    print_agent_spawn("Quantum Prime", 5, 0.847)
    print()
    print_battle_result("Nova Striker", "Dark Matter", 34.5, 12)
    print()
    print_evolution_progress(42, 100, 0.923, 0.671)
