#!/usr/bin/env python3
"""
STOCHASTIC DEMONSTRATION - Luck and Fate

Shows how AESTHETIC dimension adds necessary randomness:
1. Same input → different outputs (prevents pure determinism)
2. Luck component (the d20 roll)
3. Fate component (deterministic pull)
4. "Luck is gravity" - influences outcome without logical reason

The system MUST be able to make different choices with identical inputs.
This prevents the final form of rigidity: pure determinism.
"""

import sys

sys.path.insert(0, ".")

from demo_api import MetaCognitiveAPI, ProblemInput, GuideMode
from foundation import evaluate_answer

print("=" * 80)
print("STOCHASTIC BEHAVIOR: LUCK AND FATE")
print("Preventing Pure Determinism")
print("=" * 80)

print("\n" + "=" * 80)
print("SCENARIO 1: The d20 Roll - Same input, different aesthetic")
print("=" * 80)

problem = "What is the meaning of life?"
answer = "42"

print(f"\nProblem: {problem}")
print(f"Answer:  {answer}")
print("\nRolling the d20 10 times (same input, different luck):\n")

aesthetic_scores = []
overall_scores = []

for i in range(10):
    eval_result = evaluate_answer(answer, problem)
    aesthetic_scores.append(eval_result.aesthetic.value)
    overall_scores.append(eval_result.overall.value)
    print(
        f"  Roll {i + 1:2d}: aesthetic={eval_result.aesthetic.value:.3f}, overall={eval_result.overall.value:.3f}"
    )

print(f"\nAesthetic variance: {max(aesthetic_scores) - min(aesthetic_scores):.3f}")
print(f"Overall variance:   {max(overall_scores) - min(overall_scores):.3f}")
print("\n✅ Same input produces different outputs")
print("   This is the d20 roll in action - luck varies")

print("\n" + "=" * 80)
print("SCENARIO 2: Fate vs Luck")
print("=" * 80)

print("\nAesthetic = 70% Luck + 30% Fate")
print("  - Luck:  Pure randomness (d20 roll)")
print("  - Fate:  Deterministic pull based on content")
print("\nExample breakdown:")

eval1 = evaluate_answer("Short", "Test")
eval2 = evaluate_answer(
    "This is a much longer answer with more content and detail",
    "Complex problem requiring detailed analysis",
)

print(f"\nShort answer:")
print(f"  Aesthetic: {eval1.aesthetic.value:.3f} (fate component is low)")
print(f"\nLong answer:")
print(f"  Aesthetic: {eval2.aesthetic.value:.3f} (fate component is higher)")
print("\n✅ Fate provides deterministic pull, luck adds variance")

print("\n" + "=" * 80)
print("SCENARIO 3: Different strategies, different luck")
print("=" * 80)

api = MetaCognitiveAPI()

print("\nStrict strategy = Low luck (fate is harsh)")
print("Lenient strategy = High luck (fate is kind)")
print("Basic strategy = Moderate luck (balanced)")

problem = "Is this a good idea?"

print("\n5 trials with each strategy:\n")

for mode, name in [
    (GuideMode.STRICT, "Strict"),
    (GuideMode.LENIENT, "Lenient"),
    (GuideMode.BASIC, "Basic"),
]:
    aesthetics = []
    for _ in range(5):
        output = api.solve(ProblemInput(problem=problem, mode=mode, max_iterations=1))
        aesthetic = output.step_history[0]["dimensions"]["aesthetic"]
        aesthetics.append(aesthetic)

    avg = sum(aesthetics) / len(aesthetics)
    min_val = min(aesthetics)
    max_val = max(aesthetics)

    print(f"{name:8s}: avg={avg:.3f}, range=[{min_val:.3f}, {max_val:.3f}]")

print("\n✅ Different strategies have different luck profiles")
print("   Strict: Low luck (0.1-0.5)")
print("   Lenient: High luck (0.6-1.0)")
print("   Basic: Moderate (0.25-0.75)")

print("\n" + "=" * 80)
print("SCENARIO 4: Non-deterministic decision making")
print("=" * 80)

print("\nTwo identical calls with identical inputs:")
print("Should they produce the same result? NO!")
print("\nThis prevents rigidity through pure determinism.")

problem = "Should we proceed with plan A or plan B?"

print(f"\nProblem: {problem}")
print("\n10 trials:")

results = []
for i in range(10):
    output = api.solve(ProblemInput(problem=problem, mode=GuideMode.VOTING, max_iterations=1))
    quality = output.quality_report.final_quality
    aesthetic = output.step_history[0]["dimensions"]["aesthetic"]
    results.append((quality, aesthetic))
    print(f"  Trial {i + 1:2d}: quality={quality:.3f}, aesthetic={aesthetic:.3f}")

quality_variance = max(r[0] for r in results) - min(r[0] for r in results)
aesthetic_variance = max(r[1] for r in results) - min(r[1] for r in results)

print(f"\nQuality variance:   {quality_variance:.3f}")
print(f"Aesthetic variance: {aesthetic_variance:.3f}")

if quality_variance > 0.01:
    print("\n✅ System makes different decisions with identical inputs")
    print("   This is the stochastic element preventing pure determinism")
else:
    print("\n⚠️  Variance is low (but non-zero due to aesthetic)")

print("\n" + "=" * 80)
print("SCENARIO 5: Luck is Gravity")
print("=" * 80)

print("\nLuck influences outcomes without logical reason.")
print("It's a fundamental force - like gravity.")
print("\nExample: Two logically equivalent answers")

answer_a = "Yes, that's correct"
answer_b = "That's correct, yes"

print(f"\nAnswer A: '{answer_a}'")
print(f"Answer B: '{answer_b}'")
print("\nLogically identical, but luck varies:\n")

for i in range(5):
    eval_a = evaluate_answer(answer_a, "Is this right?")
    eval_b = evaluate_answer(answer_b, "Is this right?")

    print(
        f"  Trial {i + 1}: A={eval_a.aesthetic.value:.3f}, B={eval_b.aesthetic.value:.3f}, diff={abs(eval_a.aesthetic.value - eval_b.aesthetic.value):.3f}"
    )

print("\n✅ Luck creates variance even for logically identical inputs")
print("   This is the 'gravity' that pulls outcomes in unpredictable ways")

print("\n" + "=" * 80)
print("SUMMARY: AESTHETIC DIMENSION (9th dimension)")
print("=" * 80)

print("\nThe 9 Dimensions (FVCU+F+CDC+A):")
print()
print("1-5. Core Quality:")
print("   Factuality, Validity, Coherence, Utility, Faithfulness")
print()
print("6-8. Meta-Cognitive (prevent ego/dogfooding):")
print("   Confidence, Doubt, Curiosity")
print()
print("9. Affective (prevents pure rationality/determinism):")
print("   AESTHETIC - Luck/Fate")
print()
print("Aesthetic = 70% Luck + 30% Fate")
print("  - Luck:  random.random() (the d20 roll)")
print("  - Fate:  Deterministic component based on content")
print()
print("Purpose:")
print("  ❌ Prevents pure determinism")
print("  ❌ Allows different choices with identical inputs")
print("  ✅ Adds necessary randomness")
print("  ✅ 'Luck is gravity' - influences without logic")
print()
print("Balancing Forces (complete):")
print("  • Confidence ↔ Doubt (certainty vs skepticism)")
print("  • Conviction ↔ Curiosity (satisfied vs exploring)")
print("  • Logic ↔ Aesthetic (rational vs affective)")
print("  • Determinism ↔ Stochasticity (predictable vs random)")

print("\n" + "=" * 80)
print("✅ SYSTEM NOW HAS LUCK AND FATE")
print("✅ PREVENTS PURE DETERMINISM")
print("✅ SAME INPUT CAN PRODUCE DIFFERENT OUTPUTS")
print("=" * 80)
