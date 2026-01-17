#!/usr/bin/env python3
"""
WAFT Metrics System - Demo & Examples

This script demonstrates how to use WAFT's native metric system
to track work in Scint, Karma, Integrity, and Cognitive Load.
"""

from waft.metrics import (
    Phase,
    Quest,
    PlayerStats,
    Scint,
    Karma,
    Integrity,
    CognitiveLoad,
    track_metrics,
    prioritize_phases
)


def demo_basic_metrics():
    """Demonstrate basic metric objects."""
    print("=" * 60)
    print("DEMO 1: Basic Metrics")
    print("=" * 60)

    # Scint - Energy currency
    scint = Scint(cost=60, earned=80)
    print(f"\n{scint}")
    print(f"  Profitable? {scint.is_profitable()}")
    print(f"  ROI: {scint.roi:.2f}x")

    # Karma - Alignment
    karma = Karma(impact=25)
    print(f"\n{karma}")
    print(f"  Evolution trigger? {karma.triggers_evolution()}")

    # Integrity - Risk
    integrity = Integrity(risk=15, current=100)
    print(f"\n{integrity}")
    print(f"  Can afford risk? {integrity.can_afford_risk()}")

    # Cognitive Load
    cognitive = CognitiveLoad(complexity=6)
    print(f"\n{cognitive}")
    print(f"  Requires focus? {cognitive.requires_focus()}")


def demo_phase():
    """Demonstrate Phase tracking."""
    print("\n" + "=" * 60)
    print("DEMO 2: Phase Tracking")
    print("=" * 60)

    phase = Phase(
        name="Write comprehensive documentation",
        scint_cost=60,
        scint_earned=80,
        karma_impact=25,
        integrity_risk=5,
        cognitive_load=6
    )

    print(f"\n{phase}")
    print(f"\nROI: {phase.roi():.2f}x")
    print(f"Net Scint: {phase.net_scint():+d}")
    print(f"Is profitable? {phase.is_profitable()}")

    # Complete the phase
    phase.complete(actual_scint=55)  # Actually took less!
    print(f"\n✓ Phase completed! (actual: 55 Scint, estimated: 60)")


def demo_quest():
    """Demonstrate Quest with multiple phases."""
    print("\n" + "=" * 60)
    print("DEMO 3: Multi-Phase Quest")
    print("=" * 60)

    # Create quest
    quest = Quest(
        name="Organize Project Repository",
        description="Clean up and structure the codebase for better navigation"
    )

    # Add phases
    phases_data = [
        ("Setup automation", 80, 100, 30, 5, 7),
        ("Move large PDFs", 30, 50, 15, 10, 2),
        ("Archive experiments", 50, 75, 25, 20, 5),
        ("Consolidate docs", 70, 90, 35, 25, 6),
        ("README rewrite", 90, 120, 50, 30, 8),
    ]

    for name, cost, earned, karma, risk, cognitive in phases_data:
        quest.add_phase(Phase(
            name=name,
            scint_cost=cost,
            scint_earned=earned,
            karma_impact=karma,
            integrity_risk=risk,
            cognitive_load=cognitive
        ))

    # Print quest summary
    print(f"\n{quest}")

    # Analysis
    print(f"\nAnalysis:")
    print(f"  Is profitable? {quest.is_profitable()}")
    print(f"  Break-even at: Phase {quest.break_even_phase()}")
    print(f"  Evolution triggers at: Phase {quest.evolution_trigger_phase()}")

    # Print individual phases
    print(f"\nPhases:")
    for i, phase in enumerate(quest.phases):
        print(f"  {i}. {phase.name}")
        print(f"     Scint: {phase.scint_cost} → {phase.scint_earned} (net: {phase.net_scint():+d})")
        print(f"     Karma: {phase.karma_impact:+d}, Risk: {phase.integrity_risk}, Complexity: {phase.cognitive_load} 🧠")


def demo_player_stats():
    """Demonstrate player stats and decision-making."""
    print("\n" + "=" * 60)
    print("DEMO 4: Player Stats & Decision Making")
    print("=" * 60)

    # Create player
    player = PlayerStats(
        scint_balance=100,
        karma=0,
        integrity_current=100,
        cognitive_capacity=10  # Morning, fully rested
    )

    print(f"\nPlayer Stats:")
    print(f"  Scint: {player.scint_balance} ✨")
    print(f"  Karma: {player.karma:+d} ☯️")
    print(f"  Integrity: {player.integrity_current}/{player.integrity_max} 💚")
    print(f"  Cognitive: {player.cognitive_capacity} 🧠")
    print(f"  Level: {player.level}")
    print(f"  Evolution: {player.evolution.value}")

    # Try to start a phase
    phase = Phase(
        name="Complex refactoring",
        scint_cost=120,
        scint_earned=150,
        karma_impact=40,
        integrity_risk=50,
        cognitive_load=8
    )

    can_start, reason = player.can_start_phase(phase)
    print(f"\nCan start '{phase.name}'?")
    print(f"  {can_start}: {reason}")

    if not can_start:
        print(f"\n  💡 Recommendation: Rest to recover Scint")
        player.rest()
        print(f"  After rest: {player.scint_balance} ✨")

        can_start, reason = player.can_start_phase(phase)
        print(f"  Can start now? {can_start}: {reason}")

    # Complete phase
    if can_start:
        print(f"\n  ⚙️  Starting phase...")
        player.complete_phase(phase)
        phase.complete()

        print(f"\n  ✓ Phase completed!")
        print(f"  New stats:")
        print(f"    Scint: {player.scint_balance} ✨")
        print(f"    Karma: {player.karma:+d} ☯️")
        print(f"    Integrity: {player.integrity_current}/{player.integrity_max} 💚")
        print(f"    Evolution: {player.evolution.value}")


def demo_prioritization():
    """Demonstrate phase prioritization."""
    print("\n" + "=" * 60)
    print("DEMO 5: Phase Prioritization")
    print("=" * 60)

    # Create various phases with different ROI
    phases = [
        Phase("Quick win", scint_cost=10, scint_earned=30, karma_impact=5, integrity_risk=5, cognitive_load=2),
        Phase("Big effort", scint_cost=100, scint_earned=150, karma_impact=50, integrity_risk=30, cognitive_load=8),
        Phase("Break even", scint_cost=50, scint_earned=50, karma_impact=10, integrity_risk=10, cognitive_load=4),
        Phase("Loss leader", scint_cost=40, scint_earned=20, karma_impact=30, integrity_risk=5, cognitive_load=3),
        Phase("High karma", scint_cost=30, scint_earned=40, karma_impact=60, integrity_risk=15, cognitive_load=5),
    ]

    print("\nOriginal order:")
    for i, p in enumerate(phases):
        print(f"  {i+1}. {p.name}: ROI={p.roi():.2f}x, Karma={p.karma_impact:+d}")

    # Prioritize
    prioritized = prioritize_phases(phases)

    print("\nPrioritized by ROI + Karma:")
    for i, p in enumerate(prioritized):
        print(f"  {i+1}. {p.name}: ROI={p.roi():.2f}x, Karma={p.karma_impact:+d}")


def demo_decorator():
    """Demonstrate the metrics tracking decorator."""
    print("\n" + "=" * 60)
    print("DEMO 6: Automatic Metric Tracking")
    print("=" * 60)

    @track_metrics(
        scint_cost=40,
        scint_earned=60,
        karma_impact=20,
        integrity_risk=10,
        cognitive_load=5
    )
    def write_api_documentation():
        """Write comprehensive API docs."""
        print("\n  📝 Writing API documentation...")
        print("  ✓ Documentation complete!")
        return "docs/api.md"

    result = write_api_documentation()
    print(f"\n  Result: {result}")


def demo_evolution():
    """Demonstrate evolution system."""
    print("\n" + "=" * 60)
    print("DEMO 7: Evolution System")
    print("=" * 60)

    player = PlayerStats(scint_balance=500, karma=0)

    print(f"\nStarting Evolution: {player.evolution.value}")

    # Simulate doing high-karma work
    karma_gains = [30, 40, 50, 60, 80, 100]

    for i, karma_gain in enumerate(karma_gains):
        player.karma += karma_gain
        player._check_evolution()

        print(f"\nPhase {i+1}: +{karma_gain} Karma")
        print(f"  Total Karma: {player.karma:+d}")
        print(f"  Evolution: {player.evolution.value}")

        if player.karma >= 100 and i == 4:
            print(f"  🎉 EVOLUTION TRIGGERED! Unlocked: {player.evolution.value}")


def main():
    """Run all demos."""
    print("\n" + "🎮" * 30)
    print("WAFT METRICS SYSTEM - DEMONSTRATION")
    print("🎮" * 30)

    demo_basic_metrics()
    demo_phase()
    demo_quest()
    demo_player_stats()
    demo_prioritization()
    demo_decorator()
    demo_evolution()

    print("\n" + "=" * 60)
    print("✨ DEMO COMPLETE! ✨")
    print("=" * 60)
    print("\nFor more information:")
    print("  - Documentation: docs/WAFT_METRICS_SYSTEM.md")
    print("  - Code: src/waft/metrics.py")
    print("  - Try it yourself!")
    print()


if __name__ == "__main__":
    main()
