"""
FogSift Creature Simulation - Terminal-based interactive simulation.

Run with: python -m waft.fogsift.simulation
"""

import json
import os
import sys
import time
from pathlib import Path

from .creature import FogSiftCreature, SPECIES, LifeStage


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def save_creature(creature: FogSiftCreature, path: Path):
    """Save creature to JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(creature.to_dict(), f, indent=2)


def load_creature(path: Path) -> FogSiftCreature | None:
    """Load creature from JSON file."""
    if not path.exists():
        return None
    with open(path, 'r') as f:
        return FogSiftCreature.from_dict(json.load(f))


def print_header():
    print("╔══════════════════════════════════════╗")
    print("║     🌲 FogSift Creature Sim 🌲       ║")
    print("║     Phase 0: Software Prototype      ║")
    print("╚══════════════════════════════════════╝")
    print()


def print_menu():
    print("\n┌─────────── Commands ───────────┐")
    print("│ [f] Feed      [p] Play         │")
    print("│ [s] Sleep     [w] Wake         │")
    print("│ [t] Tick 1hr  [T] Tick 6hrs    │")
    print("│ [l] Link      [u] Unlink       │")
    print("│ [n] New pet   [q] Quit & Save  │")
    print("└─────────────────────────────────┘")


def select_species() -> str:
    """Interactive species selection."""
    print("\n╭─────── Choose Your Species ───────╮")
    for i, (key, species) in enumerate(SPECIES.items(), 1):
        sprites = species['sprites']
        print(f"│ [{i}] {sprites['idle']} {species['name']:<12} ({species['element'].value}) │")
    print("╰────────────────────────────────────╯")

    while True:
        choice = input("\nSelect [1-4]: ").strip()
        if choice in ['1', '2', '3', '4']:
            return list(SPECIES.keys())[int(choice) - 1]
        print("Invalid choice, try again.")


def run_simulation(save_path: Path | None = None):
    """Run interactive terminal simulation."""
    if save_path is None:
        save_path = Path.home() / ".fogsift" / "creature.json"

    # Try to load existing creature
    creature = load_creature(save_path)
    creature2: FogSiftCreature | None = None  # Second creature for linking demo

    if creature is None:
        clear_screen()
        print_header()
        print("No existing creature found. Let's create one!\n")

        name = input("Name your creature: ").strip() or "Pixel"
        species_id = select_species()

        creature = FogSiftCreature.hatch(name=name, species_id=species_id)
        print(f"\n🥚 {creature.sprite} {name} has been created!")
        time.sleep(1)

    # Main loop
    running = True
    message = "Welcome back!" if creature.age_hours > 0 else "Your journey begins!"

    while running:
        clear_screen()
        print_header()

        # Show creature status
        print(creature.status())

        # Show second creature if exists
        if creature2:
            print("\n── Linked Creature ──")
            print(creature2.status())

        # Show message
        if message:
            print(f"\n💬 {message}")

        print_menu()

        # Get input
        try:
            cmd = input("\n> ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            cmd = 'q'

        message = ""

        if cmd == 'f':
            message = creature.feed()
        elif cmd == 'p':
            message = creature.play()
        elif cmd == 's':
            message = creature.sleep()
        elif cmd == 'w':
            message = creature.wake()
        elif cmd == 't':
            events = creature.tick(hours_passed=1)
            if creature2:
                events.extend(creature2.tick(hours_passed=1))
            message = " | ".join(events) if events else "⏰ 1 hour passed."
        elif cmd == 'T':
            all_events = []
            for _ in range(6):
                all_events.extend(creature.tick(hours_passed=1))
                if creature2:
                    all_events.extend(creature2.tick(hours_passed=1))
            message = " | ".join(all_events) if all_events else "⏰ 6 hours passed."
        elif cmd == 'l':
            if creature2 is None:
                # Create a second creature for linking demo
                print("\n🔗 Creating a second creature to link with...")
                name2 = input("Name the second creature: ").strip() or "Friend"
                species2 = select_species()
                creature2 = FogSiftCreature.hatch(name=name2, species_id=species2)
                creature2.stage = creature.stage  # Match stages
                message = creature.link(creature2)
            else:
                message = creature.link(creature2)
        elif cmd == 'u':
            message = creature.unlink()
            if creature2:
                creature2.unlink()
        elif cmd == 'n':
            print("\n⚠️  This will replace your current creature!")
            confirm = input("Are you sure? [y/N]: ").strip().lower()
            if confirm == 'y':
                name = input("Name your new creature: ").strip() or "Pixel"
                species_id = select_species()
                creature = FogSiftCreature.hatch(name=name, species_id=species_id)
                creature2 = None
                message = f"🥚 {creature.name} has hatched!"
        elif cmd == 'q':
            save_creature(creature, save_path)
            if creature2:
                save_creature(creature2, save_path.with_name("creature2.json"))
            print(f"\n💾 Saved to {save_path}")
            print("👋 Goodbye!")
            running = False
        elif cmd == '':
            # Empty input = minor tick
            events = creature.tick(hours_passed=1/60)
            if creature2:
                events.extend(creature2.tick(hours_passed=1/60))
            if events:
                message = " | ".join(events)
        else:
            message = f"Unknown command: {cmd}"


def run_batch_simulation(generations: int = 100):
    """
    Run a batch simulation to test evolution mechanics.
    Good for finding balance issues before filming.
    """
    print("╔══════════════════════════════════════╗")
    print("║   FogSift Batch Evolution Test       ║")
    print("╚══════════════════════════════════════╝\n")

    results = {
        "healthy": 0,
        "normal": 0,
        "neglected": 0,
        "dead": 0,
    }

    for i in range(generations):
        creature = FogSiftCreature.hatch(name=f"Test_{i}", species_id="pixel_fox")

        # Simulate different care patterns
        care_style = i % 3  # 0=good, 1=medium, 2=neglect

        # Simulate 7 days (168 hours)
        for hour in range(168):
            events = creature.tick(hours_passed=1)

            if creature.is_dead:
                break

            # Care based on style
            if care_style == 0:  # Good care
                if creature.hunger < 50:
                    creature.feed()
                if hour % 4 == 0:
                    creature.play()
            elif care_style == 1:  # Medium care
                if creature.hunger < 30:
                    creature.feed()
                if hour % 8 == 0:
                    creature.play()
            # care_style == 2: neglect (no care)

        # Record results
        if creature.is_dead:
            results["dead"] += 1
        else:
            results[creature.evolution_path] += 1

        # Progress
        if (i + 1) % 10 == 0:
            print(f"  Simulated {i + 1}/{generations} creatures...")

    print("\n┌─────────── Results ───────────┐")
    print(f"│ Healthy:   {results['healthy']:>4} ({100*results['healthy']/generations:.1f}%) │")
    print(f"│ Normal:    {results['normal']:>4} ({100*results['normal']/generations:.1f}%) │")
    print(f"│ Neglected: {results['neglected']:>4} ({100*results['neglected']/generations:.1f}%) │")
    print(f"│ Dead:      {results['dead']:>4} ({100*results['dead']/generations:.1f}%) │")
    print("└───────────────────────────────┘")

    return results


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--batch":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        run_batch_simulation(count)
    else:
        run_simulation()
