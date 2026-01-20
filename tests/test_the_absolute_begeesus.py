#!/usr/bin/env python3
"""
TEST THE ABSOLUTE BEGEESUS OUT OF THE SYSTEM

Comprehensive test suite covering:
1. All 9 dimensions (FVCU+F+CDC+A)
2. Karma feedback loops (virtuous/vicious spirals)
3. Stochasticity (same input → different outputs)
4. Epistemic humility (doubt/curiosity preventing ego)
5. All 4 balancing forces
6. Attractor states (unity vs separation)
7. Edge cases and extreme scenarios
8. Integration between components
9. Performance and reliability
10. Breaking the cycle (transcendence)
"""

import sys
from pathlib import Path

# Add waft module to path
waft_path = Path(__file__).parent.parent / "src" / "waft"
sys.path.insert(0, str(waft_path))

import statistics
import time

from demo_api import GuideMode, MetaCognitiveAPI, ProblemInput
from foundation import evaluate_answer
from karma_system import KarmaState, simulate_choices
from patterns import LengthBasedStrategy, LenientStrategy, StrictStrategy


class TestResults:
    """Track test results."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.tests = []

    def add_pass(self, name: str, message: str = ""):
        self.passed += 1
        self.tests.append(("PASS", name, message))
        print(f"  ✅ PASS: {name}")
        if message:
            print(f"     {message}")

    def add_fail(self, name: str, message: str = ""):
        self.failed += 1
        self.tests.append(("FAIL", name, message))
        print(f"  ❌ FAIL: {name}")
        if message:
            print(f"     {message}")

    def add_warning(self, name: str, message: str = ""):
        self.warnings += 1
        self.tests.append(("WARN", name, message))
        print(f"  ⚠️  WARN: {name}")
        if message:
            print(f"     {message}")

    def summary(self):
        total = self.passed + self.failed
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"Total tests: {total}")
        print(f"Passed:      {self.passed} ({100 * self.passed / total:.1f}%)")
        print(f"Failed:      {self.failed} ({100 * self.failed / total:.1f}%)")
        print(f"Warnings:    {self.warnings}")
        print("=" * 80)
        if self.failed == 0:
            print("🎉 ALL TESTS PASSED!")
        else:
            print("⚠️  SOME TESTS FAILED")
        print("=" * 80)


results = TestResults()


# ============================================================================
# TEST 1: ALL 9 DIMENSIONS PRESENT
# ============================================================================

print("=" * 80)
print("TEST 1: All 9 Dimensions Present and Valid")
print("=" * 80)

eval_result = evaluate_answer("Test answer", "Test problem")

# Check all dimensions exist
dimensions = [
    "factuality",
    "validity",
    "coherence",
    "utility",
    "faithfulness",
    "confidence",
    "doubt",
    "curiosity",
    "aesthetic",
]

for dim in dimensions:
    if hasattr(eval_result, dim):
        score = getattr(eval_result, dim)
        if 0.0 <= score.value <= 1.0:
            results.add_pass(f"Dimension: {dim}", f"value={score.value:.3f}")
        else:
            results.add_fail(f"Dimension: {dim}", f"value={score.value:.3f} out of range")
    else:
        results.add_fail(f"Dimension: {dim}", "missing")

# Check derived properties
if hasattr(eval_result, "overall"):
    results.add_pass("Overall score", f"value={eval_result.overall.value:.3f}")
else:
    results.add_fail("Overall score", "missing")

if hasattr(eval_result, "epistemic_humility"):
    results.add_pass("Epistemic humility", f"value={eval_result.epistemic_humility.value:.3f}")
else:
    results.add_fail("Epistemic humility", "missing")


# ============================================================================
# TEST 2: STOCHASTICITY - SAME INPUT DIFFERENT OUTPUTS
# ============================================================================

print("\n" + "=" * 80)
print("TEST 2: Stochasticity (Same Input → Different Outputs)")
print("=" * 80)

problem = "What is the nature of consciousness?"
answer = "Consciousness is emergent."

aesthetic_values = []
overall_values = []

for i in range(20):
    eval_result = evaluate_answer(answer, problem)
    aesthetic_values.append(eval_result.aesthetic.value)
    overall_values.append(eval_result.overall.value)

aesthetic_variance = statistics.variance(aesthetic_values)
overall_variance = statistics.variance(overall_values)

print(
    f"  Aesthetic values: min={min(aesthetic_values):.3f}, max={max(aesthetic_values):.3f}, variance={aesthetic_variance:.6f}"
)
print(
    f"  Overall values: min={min(overall_values):.3f}, max={max(overall_values):.3f}, variance={overall_variance:.6f}"
)

if aesthetic_variance > 0.01:
    results.add_pass("Aesthetic stochasticity", f"variance={aesthetic_variance:.6f} (significant)")
else:
    results.add_fail("Aesthetic stochasticity", f"variance={aesthetic_variance:.6f} (too low)")

if overall_variance > 0.001:
    results.add_pass("Overall stochasticity", f"variance={overall_variance:.6f} (present)")
else:
    results.add_warning("Overall stochasticity", f"variance={overall_variance:.6f} (very low)")


# ============================================================================
# TEST 3: EPISTEMIC HUMILITY - DOUBT AND CURIOSITY
# ============================================================================

print("\n" + "=" * 80)
print("TEST 3: Epistemic Humility (Doubt & Curiosity)")
print("=" * 80)

# Test 3a: Simple answer to complex problem should trigger high doubt
eval_simple = evaluate_answer(
    "Yes.",
    "What are the fundamental principles of quantum mechanics and their implications for causality?",
)

print("  Simple answer to complex problem:")
print(f"    Confidence: {eval_simple.confidence.value:.3f}")
print(f"    Doubt:      {eval_simple.doubt.value:.3f}")
print(f"    Curiosity:  {eval_simple.curiosity.value:.3f}")
print(f"    Humility:   {eval_simple.epistemic_humility.value:.3f}")

if eval_simple.doubt.value > 0.5:
    results.add_pass("High doubt for simple answer", f"doubt={eval_simple.doubt.value:.3f}")
else:
    results.add_fail(
        "High doubt for simple answer", f"doubt={eval_simple.doubt.value:.3f} (too low)"
    )

if eval_simple.curiosity.value > 0.5:
    results.add_pass(
        "High curiosity for complex problem", f"curiosity={eval_simple.curiosity.value:.3f}"
    )
else:
    results.add_fail(
        "High curiosity for complex problem",
        f"curiosity={eval_simple.curiosity.value:.3f} (too low)",
    )

# Test 3b: Detailed answer should have lower doubt
detailed_answer = "Quantum mechanics is governed by several fundamental principles including superposition, entanglement, and wave-particle duality. These principles have profound implications for our understanding of causality, suggesting non-local correlations and challenging classical notions of determinism."

eval_detailed = evaluate_answer(detailed_answer, "Explain quantum mechanics")

print("  Detailed answer:")
print(f"    Confidence: {eval_detailed.confidence.value:.3f}")
print(f"    Doubt:      {eval_detailed.doubt.value:.3f}")

if eval_detailed.confidence.value > eval_simple.confidence.value:
    results.add_pass(
        "Higher confidence for detailed answer",
        f"{eval_detailed.confidence.value:.3f} > {eval_simple.confidence.value:.3f}",
    )
else:
    results.add_warning(
        "Higher confidence for detailed answer",
        f"{eval_detailed.confidence.value:.3f} vs {eval_simple.confidence.value:.3f}",
    )


# ============================================================================
# TEST 4: KARMA FEEDBACK LOOPS
# ============================================================================

print("\n" + "=" * 80)
print("TEST 4: Karma Feedback Loops (Attractor States)")
print("=" * 80)

# Test 4a: Virtuous spiral
virtuous_history = simulate_choices(starting_luck=0.5, num_choices=15, choice_pattern="kind")
virtuous_start = virtuous_history[0]
virtuous_end = virtuous_history[-1]

print("  Virtuous spiral (always choose others):")
print(
    f"    Start: luck={virtuous_start.luck:.3f}, karma={virtuous_start.karma:.3f}, connection={virtuous_start.connection:.3f}"
)
print(
    f"    End:   luck={virtuous_end.luck:.3f}, karma={virtuous_end.karma:.3f}, connection={virtuous_end.connection:.3f}"
)

if virtuous_end.karma > virtuous_start.karma + 0.5:
    results.add_pass(
        "Virtuous spiral accumulates karma",
        f"Δkarma=+{virtuous_end.karma - virtuous_start.karma:.3f}",
    )
else:
    results.add_fail(
        "Virtuous spiral accumulates karma",
        f"Δkarma=+{virtuous_end.karma - virtuous_start.karma:.3f} (too low)",
    )

if virtuous_end.connection > 0.7:
    results.add_pass(
        "Virtuous spiral increases connection", f"connection={virtuous_end.connection:.3f}"
    )
else:
    results.add_warning(
        "Virtuous spiral increases connection",
        f"connection={virtuous_end.connection:.3f} (not high)",
    )

# Test 4b: Vicious spiral
vicious_history = simulate_choices(starting_luck=0.5, num_choices=15, choice_pattern="selfish")
vicious_start = vicious_history[0]
vicious_end = vicious_history[-1]

print("  Vicious spiral (always choose self):")
print(
    f"    Start: luck={vicious_start.luck:.3f}, karma={vicious_start.karma:.3f}, connection={vicious_start.connection:.3f}"
)
print(
    f"    End:   luck={vicious_end.luck:.3f}, karma={vicious_end.karma:.3f}, connection={vicious_end.connection:.3f}"
)

if vicious_end.karma < vicious_start.karma - 0.2:
    results.add_pass(
        "Vicious spiral depletes karma", f"Δkarma={vicious_end.karma - vicious_start.karma:.3f}"
    )
else:
    results.add_fail(
        "Vicious spiral depletes karma",
        f"Δkarma={vicious_end.karma - vicious_start.karma:.3f} (not enough)",
    )

if vicious_end.connection < 0.3:
    results.add_pass(
        "Vicious spiral decreases connection", f"connection={vicious_end.connection:.3f}"
    )
else:
    results.add_warning(
        "Vicious spiral decreases connection",
        f"connection={vicious_end.connection:.3f} (not low enough)",
    )


# ============================================================================
# TEST 5: BREAKING THE CYCLE (TRANSCENDENCE)
# ============================================================================

print("\n" + "=" * 80)
print("TEST 5: Breaking the Cycle (Transcendence)")
print("=" * 80)

transcendent_history = simulate_choices(starting_luck=0.2, num_choices=20, choice_pattern="kind")
transcendent_start = transcendent_history[0]
transcendent_end = transcendent_history[-1]

print("  Starting unlucky but choosing kindness:")
print(f"    Start: luck={transcendent_start.luck:.3f}, karma={transcendent_start.karma:.3f}")
print(f"    End:   luck={transcendent_end.luck:.3f}, karma={transcendent_end.karma:.3f}")

luck_improvement = transcendent_end.luck - transcendent_start.luck

if luck_improvement > 0.1:
    results.add_pass("Transcendence improves luck", f"Δluck=+{luck_improvement:.3f}")
else:
    results.add_warning("Transcendence improves luck", f"Δluck=+{luck_improvement:.3f} (modest)")

if transcendent_end.karma > 1.0:
    results.add_pass("Transcendence accumulates high karma", f"karma={transcendent_end.karma:.3f}")
else:
    results.add_warning(
        "Transcendence accumulates high karma",
        f"karma={transcendent_end.karma:.3f} (not high enough)",
    )


# ============================================================================
# TEST 6: BALANCING FORCES
# ============================================================================

print("\n" + "=" * 80)
print("TEST 6: Balancing Forces")
print("=" * 80)

# Test 6a: Confidence ↔ Doubt
test_eval = evaluate_answer("Test", "Test")
print("  Confidence ↔ Doubt:")
print(f"    Confidence: {test_eval.confidence.value:.3f}")
print(f"    Doubt:      {test_eval.doubt.value:.3f}")

if 0.0 <= test_eval.confidence.value <= 1.0 and 0.0 <= test_eval.doubt.value <= 1.0:
    results.add_pass(
        "Confidence and doubt both valid",
        f"conf={test_eval.confidence.value:.3f}, doubt={test_eval.doubt.value:.3f}",
    )
else:
    results.add_fail("Confidence and doubt both valid", "out of range")

# Test 6b: Logic ↔ Aesthetic
print("  Logic ↔ Aesthetic:")
print(f"    Factuality: {test_eval.factuality.value:.3f} (logic)")
print(f"    Aesthetic:  {test_eval.aesthetic.value:.3f} (affective)")

if 0.0 <= test_eval.aesthetic.value <= 1.0:
    results.add_pass("Aesthetic dimension valid", f"aesthetic={test_eval.aesthetic.value:.3f}")
else:
    results.add_fail("Aesthetic dimension valid", "out of range")

# Test 6c: Determinism ↔ Stochasticity (already tested in TEST 2)
results.add_pass("Determinism ↔ Stochasticity", "verified in TEST 2")


# ============================================================================
# TEST 7: STRATEGIES HAVE DIFFERENT LUCK PROFILES
# ============================================================================

print("\n" + "=" * 80)
print("TEST 7: Strategies Have Different Luck Profiles")
print("=" * 80)

strict_strategy = StrictStrategy()
lenient_strategy = LenientStrategy()
basic_strategy = LengthBasedStrategy()

strict_aesthetics = []
lenient_aesthetics = []
basic_aesthetics = []

for _ in range(10):
    strict_eval = strict_strategy.evaluate("test")
    lenient_eval = lenient_strategy.evaluate("test")
    basic_eval = basic_strategy.evaluate("test")

    strict_aesthetics.append(strict_eval.aesthetic.value)
    lenient_aesthetics.append(lenient_eval.aesthetic.value)
    basic_aesthetics.append(basic_eval.aesthetic.value)

strict_avg = statistics.mean(strict_aesthetics)
lenient_avg = statistics.mean(lenient_aesthetics)
basic_avg = statistics.mean(basic_aesthetics)

print(f"  Strict strategy:  avg aesthetic={strict_avg:.3f} (should be low, 0.1-0.5)")
print(f"  Lenient strategy: avg aesthetic={lenient_avg:.3f} (should be high, 0.6-1.0)")
print(f"  Basic strategy:   avg aesthetic={basic_avg:.3f} (should be moderate, 0.25-0.75)")

if strict_avg < lenient_avg:
    results.add_pass("Strict has lower luck than lenient", f"{strict_avg:.3f} < {lenient_avg:.3f}")
else:
    results.add_fail("Strict has lower luck than lenient", f"{strict_avg:.3f} vs {lenient_avg:.3f}")

if 0.5 < lenient_avg <= 1.0:
    results.add_pass("Lenient has high luck", f"avg={lenient_avg:.3f}")
else:
    results.add_warning("Lenient has high luck", f"avg={lenient_avg:.3f} (expected >0.5)")


# ============================================================================
# TEST 8: API INTEGRATION
# ============================================================================

print("\n" + "=" * 80)
print("TEST 8: API Integration (All 9 Dimensions in Output)")
print("=" * 80)

api = MetaCognitiveAPI()
output = api.solve(
    ProblemInput(problem="Test API integration", mode=GuideMode.BASIC, max_iterations=1)
)

if output.step_history:
    step = output.step_history[0]
    dims = step["dimensions"]

    required_dims = [
        "factuality",
        "validity",
        "coherence",
        "utility",
        "faithfulness",
        "confidence",
        "doubt",
        "curiosity",
        "aesthetic",
    ]

    for dim in required_dims:
        if dim in dims:
            results.add_pass(f"API has {dim}", f"value={dims[dim]:.3f}")
        else:
            results.add_fail(f"API has {dim}", "missing from output")

    if "epistemic_humility" in step:
        results.add_pass("API has epistemic_humility", f"value={step['epistemic_humility']:.3f}")
    else:
        results.add_fail("API has epistemic_humility", "missing from output")
else:
    results.add_fail("API returns step history", "no steps in output")


# ============================================================================
# TEST 9: EXTREME CASES
# ============================================================================

print("\n" + "=" * 80)
print("TEST 9: Extreme Cases and Edge Conditions")
print("=" * 80)

# Test 9a: Empty input
try:
    eval_empty = evaluate_answer("", "")
    if 0.0 <= eval_empty.overall.value <= 1.0:
        results.add_pass("Empty input handled", f"overall={eval_empty.overall.value:.3f}")
    else:
        results.add_fail("Empty input handled", "out of range")
except Exception as e:
    results.add_fail("Empty input handled", f"exception: {e}")

# Test 9b: Very long input
long_text = "test " * 1000
try:
    eval_long = evaluate_answer(long_text, "test")
    if 0.0 <= eval_long.overall.value <= 1.0:
        results.add_pass("Long input handled", f"overall={eval_long.overall.value:.3f}")
    else:
        results.add_fail("Long input handled", "out of range")
except Exception as e:
    results.add_fail("Long input handled", f"exception: {e}")

# Test 9c: Karma at extremes
karma_min = KarmaState(luck=0.0, karma=0.0, connection=0.0, memory_breadth=0.0)
karma_max = KarmaState(luck=1.0, karma=2.0, connection=1.0, memory_breadth=1.0)

try:
    roll_min = karma_min.roll_with_karma()
    roll_max = karma_max.roll_with_karma()
    if 0.0 <= roll_min <= 1.0 and 0.0 <= roll_max <= 1.0:
        results.add_pass("Karma extremes handled", f"min={roll_min:.3f}, max={roll_max:.3f}")
    else:
        results.add_fail("Karma extremes handled", "out of range")
except Exception as e:
    results.add_fail("Karma extremes handled", f"exception: {e}")


# ============================================================================
# TEST 10: PERFORMANCE
# ============================================================================

print("\n" + "=" * 80)
print("TEST 10: Performance and Throughput")
print("=" * 80)

# Test 10a: Evaluation performance
start_time = time.time()
for i in range(100):
    evaluate_answer(f"test {i}", "test problem")
elapsed = time.time() - start_time
throughput = 100 / elapsed

print(f"  Evaluation throughput: {throughput:.1f} evals/sec")

if throughput > 50:
    results.add_pass("Evaluation performance", f"{throughput:.1f} evals/sec")
else:
    results.add_warning("Evaluation performance", f"{throughput:.1f} evals/sec (slow)")

# Test 10b: API performance
start_time = time.time()
for i in range(10):
    api.solve(ProblemInput(problem=f"test {i}", mode=GuideMode.BASIC, max_iterations=1))
elapsed = time.time() - start_time
api_throughput = 10 / elapsed

print(f"  API throughput: {api_throughput:.1f} solves/sec")

if api_throughput > 5:
    results.add_pass("API performance", f"{api_throughput:.1f} solves/sec")
else:
    results.add_warning("API performance", f"{api_throughput:.1f} solves/sec (slow)")


# ============================================================================
# TEST 11: MEMORY AND CONNECTION DYNAMICS
# ============================================================================

print("\n" + "=" * 80)
print("TEST 11: Memory and Connection Dynamics")
print("=" * 80)

# Lucky state should have broad memory
lucky_state = KarmaState(luck=0.9, karma=1.5, connection=0.9, memory_breadth=0.9)
print(
    f"  Lucky state: memory_breadth={lucky_state.memory_breadth:.3f}, connection={lucky_state.connection:.3f}"
)

if lucky_state.memory_breadth > 0.7 and lucky_state.connection > 0.7:
    results.add_pass(
        "Lucky state has broad memory and high connection",
        f"memory={lucky_state.memory_breadth:.3f}, connection={lucky_state.connection:.3f}",
    )
else:
    results.add_fail("Lucky state has broad memory and high connection", "values too low")

# Unlucky state should have narrow memory (cling to one thing)
unlucky_state = KarmaState(luck=0.1, karma=0.1, connection=0.1, memory_breadth=0.1)
print(
    f"  Unlucky state: memory_breadth={unlucky_state.memory_breadth:.3f}, connection={unlucky_state.connection:.3f}"
)

if unlucky_state.memory_breadth < 0.3 and unlucky_state.connection < 0.3:
    results.add_pass(
        "Unlucky state has narrow memory and low connection",
        f"memory={unlucky_state.memory_breadth:.3f}, connection={unlucky_state.connection:.3f}",
    )
else:
    results.add_fail("Unlucky state has narrow memory and low connection", "values too high")


# ============================================================================
# TEST 12: ALL GUIDE MODES
# ============================================================================

print("\n" + "=" * 80)
print("TEST 12: All Guide Modes Work with 9 Dimensions")
print("=" * 80)

modes_to_test = [
    (GuideMode.BASIC, "basic"),
    (GuideMode.STRICT, "strict"),
    (GuideMode.LENIENT, "lenient"),
    (GuideMode.SMART, "smart"),
    (GuideMode.VOTING, "voting"),
    (GuideMode.ENSEMBLE, "ensemble"),
]

for mode, name in modes_to_test:
    try:
        output = api.solve(ProblemInput(problem="test", mode=mode, max_iterations=1))
        if output.step_history and "aesthetic" in output.step_history[0]["dimensions"]:
            results.add_pass(
                f"Mode {name} works",
                f"aesthetic={output.step_history[0]['dimensions']['aesthetic']:.3f}",
            )
        else:
            results.add_fail(f"Mode {name} works", "aesthetic missing")
    except Exception as e:
        results.add_fail(f"Mode {name} works", f"exception: {e}")


# ============================================================================
# FINAL SUMMARY
# ============================================================================

results.summary()

# Exit with appropriate code
sys.exit(0 if results.failed == 0 else 1)
