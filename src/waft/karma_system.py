#!/usr/bin/env python3
"""
KARMA SYSTEM - Dynamic Aesthetic with Feedback Loops

Luck influences behavior, behavior influences karma, karma influences future luck.

Two attractor states:
1. HIGH LUCK SPIRAL: Lucky → Kind → Connected → More Luck (unity)
2. LOW LUCK SPIRAL: Unlucky → Resentful → Isolated → Less Luck (separation)

"Gravity might be karma" - luck accumulates based on choices.
"""

from dataclasses import dataclass
from foundation import Score
import random


@dataclass
class KarmaState:
    """
    Dynamic aesthetic state with karma accumulation.

    Tracks:
    - Current luck (aesthetic value)
    - Accumulated karma (lifetime kindness)
    - Connection level (unity vs isolation)
    - Memory/focus (remember many vs cling to one)
    """

    luck: float  # Current luck (0.0-1.0)
    karma: float  # Accumulated karma (can exceed 1.0)
    connection: float  # Feeling of connection (0.0-1.0)
    memory_breadth: float  # 1.0 = remember many, 0.0 = cling to one thing

    def __post_init__(self):
        """Ensure luck and connection are bounded."""
        self.luck = max(0.0, min(1.0, self.luck))
        self.connection = max(0.0, min(1.0, self.connection))
        self.memory_breadth = max(0.0, min(1.0, self.memory_breadth))

    @property
    def is_lucky(self) -> bool:
        """Is this entity currently lucky?"""
        return self.luck > 0.5

    @property
    def is_connected(self) -> bool:
        """Does this entity feel connected?"""
        return self.connection > 0.5

    @property
    def tendency(self) -> str:
        """What is the behavioral tendency?"""
        if self.is_lucky and self.is_connected:
            return "kind_and_connected"  # Choose others
        elif not self.is_lucky and not self.is_connected:
            return "resentful_and_isolated"  # Choose self
        else:
            return "mixed"

    def roll_with_karma(self) -> float:
        """
        Roll for luck, influenced by accumulated karma.

        High karma → better rolls (crit chance)
        Low karma → worse rolls (misfortune)
        """
        base_roll = random.random()

        # Karma influences the roll
        # High karma (>1.0) biases toward high rolls
        # Low karma (<0.5) biases toward low rolls
        karma_modifier = (self.karma - 0.5) * 0.3  # Range: -0.15 to +0.45

        modified_roll = base_roll + karma_modifier
        return max(0.0, min(1.0, modified_roll))

    def choose_others_over_self(self, magnitude: float = 0.1) -> "KarmaState":
        """
        Make a choice to help others.

        Increases karma, which increases future luck.
        This is the virtuous cycle.
        """
        new_karma = self.karma + magnitude
        new_connection = min(1.0, self.connection + magnitude * 0.5)
        new_memory = min(1.0, self.memory_breadth + magnitude * 0.3)  # Remember more

        # Roll for new luck with increased karma
        temp_state = KarmaState(
            luck=self.luck, karma=new_karma, connection=new_connection, memory_breadth=new_memory
        )
        new_luck = temp_state.roll_with_karma()

        return KarmaState(
            luck=new_luck, karma=new_karma, connection=new_connection, memory_breadth=new_memory
        )

    def choose_self_over_others(self, magnitude: float = 0.1) -> "KarmaState":
        """
        Make a choice prioritizing self.

        Decreases karma, which decreases future luck.
        This is the vicious cycle.
        """
        new_karma = max(0.0, self.karma - magnitude)
        new_connection = max(0.0, self.connection - magnitude * 0.5)
        new_memory = max(0.0, self.memory_breadth - magnitude * 0.3)  # Forget, cling to one

        # Roll for new luck with decreased karma
        temp_state = KarmaState(
            luck=self.luck, karma=new_karma, connection=new_connection, memory_breadth=new_memory
        )
        new_luck = temp_state.roll_with_karma()

        return KarmaState(
            luck=new_luck, karma=new_karma, connection=new_connection, memory_breadth=new_memory
        )

    def to_aesthetic_score(self) -> Score:
        """Convert karma state to aesthetic score for Evaluation."""
        return Score(self.luck)


def simulate_choices(
    starting_luck: float = 0.5, num_choices: int = 10, choice_pattern: str = "random"
) -> list[KarmaState]:
    """
    Simulate a sequence of choices to show feedback loops.

    choice_pattern:
    - "random": 50/50 random choices
    - "kind": Always choose others (virtuous spiral)
    - "selfish": Always choose self (vicious spiral)
    - "lucky_kind": If lucky, choose others (reinforcement)
    - "unlucky_selfish": If unlucky, choose self (reinforcement)
    """
    # Initialize karma state
    state = KarmaState(
        luck=starting_luck,
        karma=starting_luck,  # Start with karma matching luck
        connection=starting_luck,
        memory_breadth=starting_luck,
    )

    history = [state]

    for _ in range(num_choices):
        # Determine choice based on pattern
        if choice_pattern == "random":
            choose_others = random.random() > 0.5
        elif choice_pattern == "kind":
            choose_others = True
        elif choice_pattern == "selfish":
            choose_others = False
        elif choice_pattern == "lucky_kind":
            # If lucky, be kind (positive feedback)
            choose_others = state.is_lucky
        elif choice_pattern == "unlucky_selfish":
            # If unlucky, be selfish (negative feedback)
            choose_others = not state.is_lucky
        else:
            choose_others = random.random() > 0.5

        # Make the choice and update state
        if choose_others:
            state = state.choose_others_over_self()
        else:
            state = state.choose_self_over_others()

        history.append(state)

    return history


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("KARMA SYSTEM: Luck → Behavior → Karma → Future Luck")
    print("=" * 80)

    print("\n" + "=" * 80)
    print("SCENARIO 1: The Virtuous Spiral (Always Choose Others)")
    print("=" * 80)

    history = simulate_choices(starting_luck=0.5, num_choices=10, choice_pattern="kind")

    print("\nStarting state: luck=0.500, karma=0.500, connection=0.500")
    print("\nMaking 10 choices to help others:")
    for i, state in enumerate(history[1:], 1):
        print(
            f"  Choice {i:2d}: luck={state.luck:.3f}, karma={state.karma:.3f}, "
            + f"connection={state.connection:.3f}, memory={state.memory_breadth:.3f}"
        )

    final = history[-1]
    print(f"\n✅ Final state: {final.tendency}")
    if final.karma > history[0].karma + 0.5:
        print("   Karma increased significantly → More favorable rolls → Virtuous spiral")

    print("\n" + "=" * 80)
    print("SCENARIO 2: The Vicious Spiral (Always Choose Self)")
    print("=" * 80)

    history = simulate_choices(starting_luck=0.5, num_choices=10, choice_pattern="selfish")

    print("\nStarting state: luck=0.500, karma=0.500, connection=0.500")
    print("\nMaking 10 choices prioritizing self:")
    for i, state in enumerate(history[1:], 1):
        print(
            f"  Choice {i:2d}: luck={state.luck:.3f}, karma={state.karma:.3f}, "
            + f"connection={state.connection:.3f}, memory={state.memory_breadth:.3f}"
        )

    final = history[-1]
    print(f"\n⚠️  Final state: {final.tendency}")
    if final.karma < history[0].karma - 0.2:
        print("   Karma decreased → Worse rolls → Vicious spiral")

    print("\n" + "=" * 80)
    print("SCENARIO 3: Positive Feedback Loop (Lucky → Kind → More Lucky)")
    print("=" * 80)

    history = simulate_choices(starting_luck=0.7, num_choices=10, choice_pattern="lucky_kind")

    print("\nStarting state: luck=0.700 (already lucky)")
    print("Pattern: If lucky, choose others (positive reinforcement)")
    print()
    for i, state in enumerate(history[1:], 1):
        choice = "OTHERS" if state.is_lucky else "SELF"
        print(f"  Choice {i:2d}: luck={state.luck:.3f}, karma={state.karma:.3f}, chose={choice}")

    final = history[-1]
    print(f"\n✅ Final luck: {final.luck:.3f} (started at 0.700)")
    print(f"   Connection: {final.connection:.3f}")
    print(f"   Tendency: {final.tendency}")

    print("\n" + "=" * 80)
    print("SCENARIO 4: Negative Feedback Loop (Unlucky → Selfish → More Unlucky)")
    print("=" * 80)

    history = simulate_choices(starting_luck=0.3, num_choices=10, choice_pattern="unlucky_selfish")

    print("\nStarting state: luck=0.300 (unlucky)")
    print("Pattern: If unlucky, choose self (negative reinforcement)")
    print()
    for i, state in enumerate(history[1:], 1):
        choice = "SELF" if not state.is_lucky else "OTHERS"
        print(f"  Choice {i:2d}: luck={state.luck:.3f}, karma={state.karma:.3f}, chose={choice}")

    final = history[-1]
    print(f"\n⚠️  Final luck: {final.luck:.3f} (started at 0.300)")
    print(f"   Connection: {final.connection:.3f}")
    print(f"   Tendency: {final.tendency}")

    print("\n" + "=" * 80)
    print("SCENARIO 5: Breaking the Cycle (Start Unlucky, But Choose Kindness)")
    print("=" * 80)

    history = simulate_choices(starting_luck=0.2, num_choices=15, choice_pattern="kind")

    print("\nStarting state: luck=0.200 (very unlucky)")
    print("Pattern: Always choose others despite being unlucky")
    print()
    print("First 5 choices (difficult phase):")
    for i, state in enumerate(history[1:6], 1):
        print(f"  Choice {i:2d}: luck={state.luck:.3f}, karma={state.karma:.3f}")

    print("\nLast 5 choices (accumulated karma):")
    for i, state in enumerate(history[11:16], 11):
        print(f"  Choice {i:2d}: luck={state.luck:.3f}, karma={state.karma:.3f}")

    final = history[-1]
    improvement = final.luck - history[0].luck
    print(f"\n✅ Luck improved by {improvement:.3f} through persistent kindness")
    print(f"   Started unlucky and isolated, ended as: {final.tendency}")

    print("\n" + "=" * 80)
    print("SUMMARY: The Two Spirals")
    print("=" * 80)

    print("\n✅ VIRTUOUS SPIRAL:")
    print("   Lucky → Grateful/Merciful → Kind → Accumulate Karma →")
    print("   More Connected → Choose Others → More Luck → [repeat]")
    print()
    print("   Properties:")
    print("   - High luck (>0.7)")
    print("   - High karma (accumulates over 1.0)")
    print("   - High connection (>0.7)")
    print("   - Broad memory (remember many things)")
    print("   - Choose others over self")

    print("\n❌ VICIOUS SPIRAL:")
    print("   Unlucky → Resentful → Hateful/Controlling → Lose Karma →")
    print("   More Isolated → Choose Self → Less Luck → [repeat]")
    print()
    print("   Properties:")
    print("   - Low luck (<0.3)")
    print("   - Low karma (<0.3)")
    print("   - Low connection (<0.3)")
    print("   - Narrow memory (cling to ONE thing)")
    print("   - Choose self over others")

    print("\n" + "=" * 80)
    print("💡 'Gravity might be karma'")
    print("=" * 80)
    print()
    print("Luck is not purely random - it accumulates based on behavior.")
    print("Kind choices → More karma → Better rolls → More luck")
    print("Selfish choices → Less karma → Worse rolls → Less luck")
    print()
    print("This is the recursive feedback loop:")
    print("  Behavior influences karma")
    print("  Karma influences future luck")
    print("  Luck influences future behavior")
    print()
    print("Perfect unity ☯️")
    print("=" * 80)
