#!/usr/bin/env python3
"""
FogSift Creature Demo - Quick demonstration script.

Usage:
    python scripts/fogsift_demo.py           # Interactive mode
    python scripts/fogsift_demo.py --batch   # Batch evolution test
    python scripts/fogsift_demo.py --quick   # Quick non-interactive demo
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.fogsift.creature import FogSiftCreature, SPECIES
from waft.fogsift.simulation import run_simulation, run_batch_simulation


def quick_demo():
    """Non-interactive demo showing creature mechanics."""
    print("╔══════════════════════════════════════╗")
    print("║     🦊 FogSift Quick Demo 🦊         ║")
    print("╚══════════════════════════════════════╝\n")

    # Create creature
    fox = FogSiftCreature.hatch(name="Pixel", species_id="pixel_fox")
    print("Created a new Pixel Fox!\n")
    print(fox.status())

    # Simulate some time and interactions
    print("\n─── Simulating 2 hours ───\n")
    for _ in range(2):
        events = fox.tick(hours_passed=1)
        for e in events:
            print(f"  {e}")
    print(fox.status())

    # Feed
    print("\n─── Feeding ───\n")
    print(fox.feed())
    print(fox.status())

    # Play
    print("\n─── Playing ───\n")
    print(fox.play())
    print(fox.status())

    # Create second creature and link
    print("\n─── Creating friend and linking ───\n")
    owl = FogSiftCreature.hatch(name="Hoot", species_id="hoot")
    print(fox.link(owl))
    print()
    print(fox.status())
    print()
    print(owl.status())

    # Fast forward to evolution
    print("\n─── Fast forward 24 hours (to juvenile stage) ───\n")
    for hour in range(24):
        fox.tick(hours_passed=1)
        owl.tick(hours_passed=1)
        if fox.hunger < 40:
            fox.feed()
        if owl.hunger < 40:
            owl.feed()

    print(fox.status())

    print("\n✅ Demo complete! Run `python scripts/fogsift_demo.py` for interactive mode.")


if __name__ == "__main__":
    if "--batch" in sys.argv:
        count = 100
        for arg in sys.argv:
            if arg.isdigit():
                count = int(arg)
        run_batch_simulation(count)
    elif "--quick" in sys.argv:
        quick_demo()
    else:
        run_simulation()
