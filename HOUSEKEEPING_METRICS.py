#!/usr/bin/env python3
"""
HOUSEKEEPING PLAN - Calculated with WAFT Metrics System

Using the actual metrics.py module to calculate real metrics
for the project housekeeping quest.
"""

import sys

sys.path.insert(0, "src")

from waft.metrics import Phase, PlayerStats, Quest, prioritize_phases

# ============================================================================
# THE HOUSEKEEPING QUEST
# ============================================================================


def create_housekeeping_quest() -> Quest:
    """Create the complete housekeeping quest with calculated metrics."""

    quest = Quest(
        name="The Great Reorganization",
        description="Transform root from 205 cluttered items to ~30 organized core items",
        evolution_threshold=100,
    )

    # Phase 0: Preparation & Validation
    quest.add_phase(
        Phase(
            name="Phase 0: Preparation & Validation",
            scint_cost=80,
            scint_earned=100,
            karma_impact=30,
            integrity_risk=5,
            cognitive_load=7,
        )
    )

    # Phase 1: Move PDFs to Git LFS
    quest.add_phase(
        Phase(
            name="Phase 1: Move PDFs to Git LFS",
            scint_cost=30,
            scint_earned=50,
            karma_impact=15,
            integrity_risk=10,
            cognitive_load=2,
        )
    )

    # Phase 2: Archive Obvious Experiments
    quest.add_phase(
        Phase(
            name="Phase 2: Archive Obvious Experiments",
            scint_cost=50,
            scint_earned=75,
            karma_impact=25,
            integrity_risk=20,
            cognitive_load=5,
        )
    )

    # Phase 3: Consolidate Research Docs
    quest.add_phase(
        Phase(
            name="Phase 3: Consolidate Research Docs",
            scint_cost=70,
            scint_earned=90,
            karma_impact=35,
            integrity_risk=25,
            cognitive_load=6,
        )
    )

    # Phase 4: Create Resources Directory
    quest.add_phase(
        Phase(
            name="Phase 4: Create Resources Directory",
            scint_cost=60,
            scint_earned=70,
            karma_impact=20,
            integrity_risk=15,
            cognitive_load=4,
        )
    )

    # Phase 5: Archive Historical Docs
    quest.add_phase(
        Phase(
            name="Phase 5: Archive Historical Docs",
            scint_cost=55,
            scint_earned=65,
            karma_impact=30,
            integrity_risk=10,
            cognitive_load=5,
        )
    )

    # Phase 6: README Rewrite
    quest.add_phase(
        Phase(
            name="Phase 6: README Rewrite",
            scint_cost=90,
            scint_earned=120,
            karma_impact=50,
            integrity_risk=30,
            cognitive_load=8,
        )
    )

    # Phase 7: Final Cleanup
    quest.add_phase(
        Phase(
            name="Phase 7: Final Cleanup",
            scint_cost=40,
            scint_earned=100,
            karma_impact=15,
            integrity_risk=5,
            cognitive_load=3,
        )
    )

    # Add achievements
    quest.add_achievement("The Automator")
    quest.add_achievement("Lightweight")
    quest.add_achievement("Archeologist")
    quest.add_achievement("Librarian")
    quest.add_achievement("Curator")
    quest.add_achievement("Historian")
    quest.add_achievement("Wordsmith")
    quest.add_achievement("Perfectionist")

    return quest


def print_quest_analysis(quest: Quest):
    """Print comprehensive quest analysis."""

    print("=" * 80)
    print("THE GREAT REORGANIZATION - QUEST ANALYSIS")
    print("=" * 80)

    # Overall stats
    print(f"\n{quest}")

    # Investment breakdown
    print(f"\n{'=' * 80}")
    print("INVESTMENT BREAKDOWN")
    print("=" * 80)

    print("\nTotal Investment:")
    print(f"  Scint Cost: {quest.total_scint_cost} ✨")
    print(f"  Scint Earned: {quest.total_scint_earned} ✨")
    print(f"  Net Profit: {quest.net_scint():+d} ✨")
    print(f"  ROI: {quest.roi():.2f}x")

    print("\nKarma Impact:")
    print(f"  Total Karma Gain: {quest.total_karma:+d} ☯️")
    karma_obj = quest.phases[0].karma  # Just for accessing Karma methods
    karma_obj.impact = quest.total_karma
    print(f"  Final Evolution: {karma_obj.evolution_path().value}")

    print("\nRisk Profile:")
    print(f"  Total Integrity Risk: {quest.total_integrity_risk} 💚")
    print(f"  Average Risk per Phase: {quest.total_integrity_risk / len(quest.phases):.1f}")

    print("\nComplexity:")
    print(f"  Average Cognitive Load: {quest.average_cognitive_load:.1f} 🧠")

    # Milestones
    print(f"\n{'=' * 80}")
    print("KEY MILESTONES")
    print("=" * 80)

    break_even = quest.break_even_phase()
    evolution = quest.evolution_trigger_phase()

    print(f"\nBreak-Even Point: Phase {break_even}")
    if break_even is not None:
        cumulative = sum(p.net_scint() for p in quest.phases[: break_even + 1])
        print(f"  After '{quest.phases[break_even].name}'")
        print(f"  Cumulative net: {cumulative:+d} ✨")

    print(f"\nEvolution Trigger: Phase {evolution}")
    if evolution is not None:
        cumulative_karma = sum(p.karma_impact for p in quest.phases[: evolution + 1])
        print(f"  After '{quest.phases[evolution].name}'")
        print(f"  Cumulative karma: {cumulative_karma:+d} ☯️")
        print("  🎉 UNLOCKS: The Architect evolution!")

    # Phase-by-phase
    print(f"\n{'=' * 80}")
    print("PHASE-BY-PHASE BREAKDOWN")
    print("=" * 80)

    cumulative_scint = 0
    cumulative_karma = 0

    for i, phase in enumerate(quest.phases):
        cumulative_scint += phase.net_scint()
        cumulative_karma += phase.karma_impact

        print(f"\n{phase.name}")
        print(
            f"  Scint: {phase.scint_cost} → {phase.scint_earned} (net: {phase.net_scint():+d}, ROI: {phase.roi():.2f}x)"
        )
        print(f"  Karma: {phase.karma_impact:+d} ☯️")
        print(f"  Integrity Risk: {phase.integrity_risk} 💚 ({phase.integrity.risk_level.value})")
        print(
            f"  Cognitive Load: {phase.cognitive_load} 🧠 ({phase.cognitive.complexity_level.value})"
        )

        print("  Cumulative:")
        print(f"    Net Scint: {cumulative_scint:+d} ✨")
        print(f"    Total Karma: {cumulative_karma:+d} ☯️")

        if i == break_even:
            print("  ⚡ BREAK-EVEN POINT!")

        if i == evolution:
            print("  🎉 EVOLUTION TRIGGERED! (The Architect)")

    # Achievements
    print(f"\n{'=' * 80}")
    print("ACHIEVEMENTS")
    print("=" * 80)

    for achievement in quest.achievements:
        print(f"  🏆 {achievement}")

    # Recommendation
    print(f"\n{'=' * 80}")
    print("RECOMMENDATION")
    print("=" * 80)

    if quest.is_profitable():
        print("\n✅ HIGHLY RECOMMENDED")
        print("\nReasons:")
        print(f"  • Profitable: {quest.roi():.2f}x ROI ({quest.net_scint():+d} ✨ profit)")
        print(f"  • High Karma: +{quest.total_karma} (triggers evolution)")
        print(f"  • Manageable Risk: {quest.total_integrity_risk} total damage")
        print(f"  • {len(quest.achievements)} achievements unlocked")
    else:
        print("\n⚠️ RECONSIDER")
        print("\nConcerns:")
        print(f"  • Not profitable: {quest.roi():.2f}x ROI ({quest.net_scint():+d} ✨)")


def simulate_quest_execution(quest: Quest):
    """Simulate actually doing the quest."""

    print(f"\n{'=' * 80}")
    print("QUEST EXECUTION SIMULATION")
    print("=" * 80)

    # Create player
    player = PlayerStats(
        scint_balance=100,  # Starting resources
        karma=0,
        integrity_current=100,
        integrity_max=100,
        cognitive_capacity=10,  # Morning, fully rested
        level=1,
    )

    print("\nStarting Stats:")
    print(f"  Scint: {player.scint_balance} ✨")
    print(f"  Karma: {player.karma:+d} ☯️")
    print(f"  Integrity: {player.integrity_current}/{player.integrity_max} 💚")
    print(f"  Level: {player.level}")
    print(f"  Evolution: {player.evolution.value}")

    # Try each phase
    for i, phase in enumerate(quest.phases):
        print(f"\n{'-' * 80}")
        print(f"Phase {i}: {phase.name}")
        print(f"{'-' * 80}")

        # Check if can start
        can_start, reason = player.can_start_phase(phase)

        print(f"\nCan start? {can_start}")
        print(f"Reason: {reason}")

        if not can_start:
            # Need to rest/heal
            if not player.can_afford(phase):
                print("\n💤 Resting to recover Scint...")
                player.rest()
                can_start, reason = player.can_start_phase(phase)
                print(f"After rest: {can_start} - {reason}")

            if not player.can_handle_risk(phase):
                print("\n💚 Healing to restore Integrity...")
                player.heal(50)
                can_start, reason = player.can_start_phase(phase)
                print(f"After healing: {can_start} - {reason}")

        if can_start:
            # Execute phase
            print("\n⚙️  Executing phase...")
            player.complete_phase(phase)
            phase.complete()

            print("\n✅ Phase complete!")
            print("\nNew Stats:")
            print(f"  Scint: {player.scint_balance} ✨ ({phase.net_scint():+d})")
            print(f"  Karma: {player.karma:+d} ☯️")
            print(f"  Integrity: {player.integrity_current}/{player.integrity_max} 💚")
            print(f"  Evolution: {player.evolution.value}")

            if player.karma >= 100 and i > 0:
                if quest.phases[i - 1].karma.impact < 100:
                    print(f"\n🎉 EVOLUTION UNLOCKED: {player.evolution.value}!")

    # Final stats
    print(f"\n{'=' * 80}")
    print("FINAL STATS")
    print("=" * 80)

    print("\nPlayer Stats:")
    print(f"  Scint Balance: {player.scint_balance} ✨")
    print(f"  Karma: {player.karma:+d} ☯️")
    print(f"  Integrity: {player.integrity_current}/{player.integrity_max} 💚")
    print(f"  Level: {player.level}")
    print(f"  Evolution: {player.evolution.value}")

    print("\nQuest Completion:")
    print(f"  Phases Complete: {sum(1 for p in quest.phases if p.completed)}/{len(quest.phases)}")
    print(f"  Completion: {quest.completion_percentage():.0f}%")


def analyze_phase_priority():
    """Analyze which phases to prioritize."""

    print(f"\n{'=' * 80}")
    print("PHASE PRIORITIZATION ANALYSIS")
    print("=" * 80)

    quest = create_housekeeping_quest()

    print("\nOriginal Order:")
    for i, phase in enumerate(quest.phases):
        print(f"  {i}. {phase.name}: ROI={phase.roi():.2f}x, Karma={phase.karma_impact:+d}")

    # Prioritize
    prioritized = prioritize_phases(quest.phases)

    print("\nPrioritized by ROI + Karma:")
    for i, phase in enumerate(prioritized):
        print(f"  {i}. {phase.name}: ROI={phase.roi():.2f}x, Karma={phase.karma_impact:+d}")

    print("\n💡 Insight: While Phase 6 has highest karma, Phase 7 has highest ROI!")
    print("   Consider doing high-ROI phases when energy is low.")


def main():
    """Run complete analysis."""

    print("\n🎮" * 40)
    print("HOUSEKEEPING PLAN - WAFT METRICS ANALYSIS")
    print("🎮" * 40)

    # Create quest
    quest = create_housekeeping_quest()

    # Print analysis
    print_quest_analysis(quest)

    # Prioritization
    analyze_phase_priority()

    # Simulate
    simulate_quest_execution(quest)

    # Export to JSON
    print(f"\n{'=' * 80}")
    print("QUEST DATA (JSON)")
    print("=" * 80)

    import json

    print(json.dumps(quest.to_dict(), indent=2))

    print("\n✨ ANALYSIS COMPLETE! ✨\n")


if __name__ == "__main__":
    main()
