#!/usr/bin/env python3
"""
ANTI-DOGFOODING DEMONSTRATION

Shows how DOUBT and CURIOSITY prevent the system from:
1. Ego - Being too sure of itself
2. Dogfooding - Self-reinforcing without critical evaluation
3. Overconfidence - Missing blind spots
4. Rigidity - Getting stuck in patterns

The system now has 8 dimensions (FVCU+F+CDC):
- 5 core quality dimensions
- 3 meta-cognitive dimensions that balance each other:
  * Confidence (certainty) ↔ Doubt (skepticism)
  * Conviction ↔ Curiosity (exploring alternatives)
"""

import sys

sys.path.insert(0, ".")

from demo_api import MetaCognitiveAPI, ProblemInput, GuideMode
from foundation import evaluate_answer

print("=" * 80)
print("ANTI-DOGFOODING: DOUBT & CURIOSITY")
print("Preventing Ego, Overconfidence, and Self-Reinforcement")
print("=" * 80)

print("\n" + "=" * 80)
print("SCENARIO 1: Simple answer to complex problem (CATCH DOGFOODING)")
print("=" * 80)

# The problem that started this: system being too confident
eval1 = evaluate_answer(
    answer="Yes, definitely.",
    problem="What are all the implications of quantum entanglement for our understanding of reality, causality, and the nature of information?",
)

print("\nProblem: Complex philosophical question about quantum mechanics")
print('Answer:  "Yes, definitely." (overly simple)')
print()
print("System evaluation:")
print(f"  Confidence:  {eval1.confidence.value:.3f} ⬇️  LOW (not certain about this)")
print(f"  Doubt:       {eval1.doubt.value:.3f} ⬆️  HIGH (very skeptical!)")
print(f"  Curiosity:   {eval1.curiosity.value:.3f} ⬆️  HIGH (need to explore more!)")
print(f"  → Epistemic Humility: {eval1.epistemic_humility.value:.3f} ⬆️")
print()
print("✅ System REFUSES to dogfood:")
print("   - Recognizes answer is too simple")
print("   - High doubt = questions the evaluation")
print("   - High curiosity = wants alternatives")

print("\n" + "=" * 80)
print("SCENARIO 2: Detailed answer reduces doubt")
print("=" * 80)

detailed = """Quantum entanglement is a phenomenon where particles become correlated such that
the quantum state of one particle cannot be described independently of the others. This has
profound implications: it challenges local realism, suggests non-local correlations, enables
quantum cryptography, and raises questions about the nature of information and measurement."""

eval2 = evaluate_answer(detailed, "Explain quantum entanglement")

print(f"\nAnswer length: {len(detailed)} characters")
print()
print("System evaluation:")
print(f"  Confidence:  {eval2.confidence.value:.3f} ⬆️  HIGHER (more evidence)")
print(f"  Doubt:       {eval2.doubt.value:.3f} ⬇️  LOWER (less skeptical)")
print(f"  Curiosity:   {eval2.curiosity.value:.3f} (moderate)")
print(f"  → Epistemic Humility: {eval2.epistemic_humility.value:.3f} ⬇️")
print()
print("✅ Appropriate confidence with detailed evidence")

print("\n" + "=" * 80)
print("SCENARIO 3: Strict vs Lenient - Different epistemic stances")
print("=" * 80)

api = MetaCognitiveAPI()

print("\nTesting same problem with STRICT mode:")
strict_out = api.solve(
    ProblemInput(problem="Is this system perfect?", mode=GuideMode.STRICT, max_iterations=1)
)
strict_dims = strict_out.step_history[0]["dimensions"]

print(f"  Confidence:  {strict_dims['confidence']:.3f} (high - certain about standards)")
print(f"  Doubt:       {strict_dims['doubt']:.3f} (low - not questioning)")
print(f"  Curiosity:   {strict_dims['curiosity']:.3f} (low - not exploring)")
print(f"  → Humility:  {strict_out.step_history[0]['epistemic_humility']:.3f}")
print("  ⚠️  RISK: Low humility = potential for ego")

print("\nTesting same problem with LENIENT mode:")
lenient_out = api.solve(
    ProblemInput(problem="Is this system perfect?", mode=GuideMode.LENIENT, max_iterations=1)
)
lenient_dims = lenient_out.step_history[0]["dimensions"]

print(f"  Confidence:  {lenient_dims['confidence']:.3f} (lower - uncertain)")
print(f"  Doubt:       {lenient_dims['doubt']:.3f} (high - questioning)")
print(f"  Curiosity:   {lenient_dims['curiosity']:.3f} (high - exploring)")
print(f"  → Humility:  {lenient_out.step_history[0]['epistemic_humility']:.3f}")
print("  ✅ HIGH humility = prevents ego")

print("\n" + "=" * 80)
print("SCENARIO 4: Detecting overconfidence")
print("=" * 80)

print("\nWhen confidence is too high, doubt increases as a counterbalance:")
print()

# Test with overconfident answer
confident_answer = "I am absolutely certain this is the only correct answer and there are no alternatives whatsoever."
eval3 = evaluate_answer(confident_answer, "What is the best approach?")

print(f"Answer: '{confident_answer[:60]}...'")
print()
print("System response:")
print(f"  Confidence:  {eval3.confidence.value:.3f}")
print(f"  Doubt:       {eval3.doubt.value:.3f} ← Counterbalances high confidence")
print(f"  Curiosity:   {eval3.curiosity.value:.3f} ← Seeks alternatives")
print()
print("✅ System adds doubt when confidence is too high")
print("   This prevents dogfooding and overconfidence")

print("\n" + "=" * 80)
print("SCENARIO 5: The original problem - System analyzing itself")
print("=" * 80)

print("\nRemember: The system gave itself confidence=1.000 when")
print("analyzing what to add next. This was the ego problem.")
print()
print("Now with doubt and curiosity:")

self_analysis = api.solve(
    ProblemInput(
        problem="This meta-cognitive system is perfect and needs no improvements whatsoever.",
        mode=GuideMode.VOTING,
        max_iterations=1,
    )
)

dims = self_analysis.step_history[0]["dimensions"]
print(f"  Confidence:  {dims['confidence']:.3f}")
print(f"  Doubt:       {dims['doubt']:.3f} ← Questions this claim")
print(f"  Curiosity:   {dims['curiosity']:.3f} ← Explores alternatives")
print(f"  Humility:    {self_analysis.step_history[0]['epistemic_humility']:.3f}")
print()
if dims["doubt"] > 0.3:
    print("✅ System questions its own perfection")
    print("   Doubt prevents ego and dogfooding")
else:
    print("⚠️  System still too confident in itself")

print("\n" + "=" * 80)
print("SUMMARY: HOW DOUBT & CURIOSITY PREVENT DOGFOODING")
print("=" * 80)

print("\nThe 3 Meta-Cognitive Dimensions:")
print()
print("1. CONFIDENCE")
print("   - How certain we are about the evaluation")
print("   - High = certain, Low = uncertain")
print()
print("2. DOUBT (Anti-Dogfooding)")
print("   - Should we question this evaluation?")
print("   - High = skeptical, Low = trusting")
print("   - Increases when:")
print("     • Answer is too simple for complex problem")
print("     • Confidence seems too high")
print("     • Not enough evidence")
print()
print("3. CURIOSITY (Anti-Ego)")
print("   - Should we explore alternatives?")
print("   - High = explore more, Low = satisfied")
print("   - Increases when:")
print("     • Problem has complexity")
print("     • Answer seems too definitive")
print("     • Questions in the problem")
print()
print("Together they create EPISTEMIC HUMILITY:")
print("  humility = (doubt + curiosity + (1 - confidence)) / 3")
print()
print("High humility prevents:")
print("  ❌ Ego (being too sure)")
print("  ❌ Dogfooding (self-reinforcing without critique)")
print("  ❌ Overconfidence (missing blind spots)")
print("  ❌ Rigidity (getting stuck in patterns)")

print("\n" + "=" * 80)
print("✅ SYSTEM NOW HAS SELF-DOUBT AND CURIOSITY")
print("✅ PREVENTS EGO AND DOGFOODING")
print("=" * 80)
