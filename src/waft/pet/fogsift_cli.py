#!/usr/bin/env python3
"""
FogSift Interactive CLI

A terminal-based tamagotchi you can interact with in real-time.
Perfect for Phase 0 testing and YouTube content.

Usage:
    python -m src.waft.pet.fogsift_cli

Controls:
    f - Feed
    p - Play
    s - Sleep toggle
    l - Link (spawn second creature)
    q - Quit

    1-4 - Select creature (when multiple)
"""

import json
import os
import sys
import time
import select
from pathlib import Path
from typing import Optional

try:
    from .fogsift_creature import (
        FogSiftCreature,
        create_starter,
        breed,
        STARTER_SPECIES,
    )
except ImportError:
    # Allow running as standalone script
    from fogsift_creature import (
        FogSiftCreature,
        create_starter,
        breed,
        STARTER_SPECIES,
    )


# Save directory
SAVE_DIR = Path.home() / ".fogsift"


def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_key_nonblocking() -> Optional[str]:
    """Get a keypress without blocking (Unix only)."""
    if os.name == 'nt':
        # Windows - use msvcrt
        import msvcrt
        if msvcrt.kbhit():
            return msvcrt.getch().decode('utf-8', errors='ignore')
        return None
    else:
        # Unix - use select
        try:
            import termios
            import tty

            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setcbreak(fd)
                rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
                if rlist:
                    return sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return None
        except (termios.error, AttributeError):
            # Fallback for non-interactive terminals
            time.sleep(0.1)
            return None


def save_creature(creature: FogSiftCreature) -> Path:
    """Save creature to disk."""
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    path = SAVE_DIR / f"{creature.creature_id}.json"
    path.write_text(json.dumps(creature.to_dict(), indent=2))
    return path


def load_creature(creature_id: str) -> Optional[FogSiftCreature]:
    """Load creature from disk."""
    path = SAVE_DIR / f"{creature_id}.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    return FogSiftCreature.from_dict(data)


def list_saved_creatures() -> list[str]:
    """List all saved creature IDs."""
    if not SAVE_DIR.exists():
        return []
    return [p.stem for p in SAVE_DIR.glob("*.json")]


def render_multi_creature(creatures: list[FogSiftCreature], selected: int) -> str:
    """Render multiple creatures side by side."""
    if not creatures:
        return "No creatures!"

    if len(creatures) == 1:
        return creatures[0].get_status()

    # Build side-by-side view
    lines = []
    lines.append("=" * 70)

    # Headers
    header = ""
    for i, c in enumerate(creatures):
        marker = ">>>" if i == selected else "   "
        header += f"{marker} [{i+1}] {c.name[:12]:<12} "
    lines.append(header)
    lines.append("-" * 70)

    # ASCII art side by side
    arts = [c.get_ascii_art().split('\n') for c in creatures]
    max_lines = max(len(a) for a in arts)
    for line_idx in range(max_lines):
        row = ""
        for art in arts:
            if line_idx < len(art):
                row += f"    {art[line_idx]:<14}"
            else:
                row += " " * 18
        lines.append(row)

    lines.append("-" * 70)

    # Stats
    def bar(v): return "█" * int(v / 20) + "░" * (5 - int(v / 20))

    for label, attr in [("HGR", "hunger"), ("NRG", "energy"), ("MOD", "mood"), ("SOC", "social")]:
        row = ""
        for c in creatures:
            val = getattr(c, attr)
            row += f"    {label}[{bar(val)}]{val:5.0f} "
        lines.append(row)

    lines.append("-" * 70)

    # Status line
    status = ""
    for c in creatures:
        emo = c.get_emotion()[:8]
        link = "LINKED" if c.is_linked else ""
        status += f"    {emo:<8} {link:<6} "
    lines.append(status)

    lines.append("=" * 70)

    return "\n".join(lines)


def render_help() -> str:
    """Render help text."""
    return """
╔══════════════════════════════════════════════════════════════════════╗
║  CONTROLS                                                            ║
╠══════════════════════════════════════════════════════════════════════╣
║  [F] Feed      [P] Play      [S] Sleep      [L] Link/Add creature    ║
║  [1-4] Select creature       [B] Breed      [Q] Quit & Save          ║
╚══════════════════════════════════════════════════════════════════════╝
"""


def main():
    """Main interactive loop."""
    print("\n🥚 FogSift Creature Simulator 🥚\n")

    # Check for saved creatures
    saved = list_saved_creatures()
    creatures: list[FogSiftCreature] = []

    if saved:
        print(f"Found {len(saved)} saved creature(s).")
        choice = input("Load saved? (y/n): ").strip().lower()
        if choice == 'y':
            for cid in saved[:4]:  # Max 4 creatures
                c = load_creature(cid)
                if c:
                    creatures.append(c)
                    print(f"  Loaded: {c.name} ({c.species})")

    if not creatures:
        # Create new starter
        print("\nChoose your starter:")
        for i, (name, info) in enumerate(STARTER_SPECIES.items(), 1):
            print(f"  [{i}] {name} ({info['element'].value}, {info['personality']})")

        choice = input("\nSelect (1-4): ").strip()
        species_list = list(STARTER_SPECIES.keys())
        idx = int(choice) - 1 if choice.isdigit() else 0
        idx = max(0, min(idx, len(species_list) - 1))
        species = species_list[idx]

        name = input(f"Name your {species}: ").strip() or species
        creatures.append(create_starter(species, name))
        print(f"\n✨ {name} the {species} has appeared!")

    selected = 0
    last_save = time.time()
    running = True

    # Speed multiplier for demo (1.0 = real time, 60.0 = 1 min = 1 hour)
    time_multiplier = 60.0  # Fast mode for demo

    print("\nStarting simulation... (60x speed for demo)")
    print("Press any key to begin...")
    input()

    try:
        while running:
            # Calculate elapsed time
            now = time.time()

            # Tick all creatures (accelerated time)
            for c in creatures:
                real_hours = (now - c.last_update) / 3600
                sim_hours = real_hours * time_multiplier
                events = c.tick(sim_hours)

                # Log events
                for e in events.get("events", []):
                    if e["type"] == "evolution":
                        print(f"\n🎉 {c.name} evolved to {e['to']}!")
                    elif e["type"] == "hungry":
                        pass  # Don't spam
                    elif e["type"] == "sleep":
                        print(f"\n😴 {c.name} fell asleep...")
                    elif e["type"] == "wake":
                        print(f"\n☀️ {c.name} woke up!")

            # Render
            clear_screen()
            print(render_multi_creature(creatures, selected))
            print(render_help())
            print(f"Time: {time_multiplier}x | Auto-save every 30s")

            # Auto-save periodically
            if now - last_save > 30:
                for c in creatures:
                    save_creature(c)
                last_save = now

            # Get input
            key = get_key_nonblocking()

            if key:
                key = key.lower()
                current = creatures[selected] if creatures else None

                if key == 'q':
                    running = False

                elif key == 'f' and current:
                    result = current.feed()
                    if not result["success"]:
                        print(f"\n❌ {result['message']}")
                        time.sleep(1)

                elif key == 'p' and current:
                    result = current.play()
                    if not result["success"]:
                        print(f"\n❌ {result['message']}")
                        time.sleep(1)

                elif key == 's' and current:
                    if current.is_sleeping:
                        current.is_sleeping = False
                        current.energy = max(20, current.energy)
                    else:
                        current.is_sleeping = True

                elif key == 'l':
                    if len(creatures) < 4:
                        # Add another creature
                        species_list = list(STARTER_SPECIES.keys())
                        import random
                        species = random.choice(species_list)
                        new_creature = create_starter(species, f"{species}_{len(creatures)+1}")
                        new_creature.age_hours = 2  # Skip egg for demo
                        new_creature.tick(0)
                        creatures.append(new_creature)

                        # Link with current
                        if current and len(creatures) > 1:
                            current.link(new_creature)

                elif key == 'b':
                    # Breed selected with next creature
                    if len(creatures) >= 2:
                        other_idx = (selected + 1) % len(creatures)
                        baby = breed(current, creatures[other_idx])
                        if baby and len(creatures) < 4:
                            baby.name = f"Baby_{len(creatures)+1}"
                            creatures.append(baby)
                            print(f"\n🥚 An egg appeared!")
                            time.sleep(1)

                elif key in '1234':
                    idx = int(key) - 1
                    if idx < len(creatures):
                        selected = idx

            time.sleep(0.1)  # Small delay to prevent CPU spin

    except KeyboardInterrupt:
        pass

    finally:
        # Save on exit
        print("\n\nSaving creatures...")
        for c in creatures:
            path = save_creature(c)
            print(f"  Saved {c.name} to {path}")
        print("\nGoodbye! 👋")


if __name__ == "__main__":
    main()
