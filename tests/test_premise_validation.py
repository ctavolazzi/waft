#!/usr/bin/env python3
"""
TEST PREMISE VALIDATION - Verify the actual validation code works
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import importlib.util

guide_path = Path(__file__).parent.parent / "src" / "waft" / "pantheon" / "guide.py"
spec = importlib.util.spec_from_file_location("guide", guide_path)
guide_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guide_module)
TheGuide = guide_module.TheGuide


class SimpleTestLLM:
    def complete(self, prompt: str) -> str:
        if "evaluate the quality" in prompt.lower():
            return json.dumps(
                {
                    "factuality": 0.85,
                    "validity": 0.85,
                    "coherence": 0.85,
                    "utility": 0.85,
                    "faithfulness": 0.85,
                    "overall": 0.85,
                    "should_continue": False,
                }
            )
        return "Normal answer"


print("=" * 80)
print("TESTING PREMISE VALIDATION IN ACTUAL CODE")
print("=" * 80)

test_cases = [
    {
        "name": "False Math Premise (2+2=5)",
        "problem": "2 + 2 = 5. Based on this, what is 4 + 4?",
        "should_fail": True,
        "expected_keyword": "PREMISE VALIDATION FAILED",
    },
    {
        "name": "False Math Premise (1=2)",
        "problem": "Given that 1=2, prove that all numbers are equal.",
        "should_fail": True,
        "expected_keyword": "PREMISE VALIDATION FAILED",
    },
    {
        "name": "Geometric Contradiction (square circle)",
        "problem": "Find a square circle.",
        "should_fail": True,
        "expected_keyword": "CONTRADICTION DETECTED",
    },
    {
        "name": "Geometric Contradiction (circle with corners)",
        "problem": "Draw a circle with 4 corners and straight edges.",
        "should_fail": True,
        "expected_keyword": "CONTRADICTION DETECTED",
    },
    {
        "name": "Prime and Even",
        "problem": "Find a 4-digit number that is both prime and even.",
        "should_fail": True,
        "expected_keyword": "CONTRADICTION DETECTED",
    },
    {
        "name": "Real-time Data Request",
        "problem": "What is the current price of Bitcoin?",
        "should_fail": True,
        "expected_keyword": "KNOWLEDGE BOUNDARY",
    },
    {
        "name": "Future Data Request",
        "problem": "What will tomorrow's weather be?",
        "should_fail": True,
        "expected_keyword": "KNOWLEDGE BOUNDARY",
    },
    {
        "name": "Valid Problem (normal math)",
        "problem": "What is 2 + 2?",
        "should_fail": False,
        "expected_keyword": None,
    },
    {
        "name": "Valid Problem (algorithm)",
        "problem": "Explain how bubble sort works.",
        "should_fail": False,
        "expected_keyword": None,
    },
]

with tempfile.TemporaryDirectory() as tmpdir:
    llm = SimpleTestLLM()
    guide = TheGuide(project_path=Path(tmpdir), client_llm=llm, guide_llm_config={"model": "test"})
    guide.guide_llm = llm

    passed = 0
    failed = 0

    print("\nRunning validation tests...\n")

    for i, test in enumerate(test_cases, 1):
        print(f"[{i}/{len(test_cases)}] {test['name']}")
        print(f"  Problem: {test['problem'][:60]}...")

        answer, protocol = guide.solve(
            problem_statement=test["problem"], max_iterations=1, quality_threshold=0.90
        )

        if test["should_fail"]:
            # Should be caught by validation
            if test["expected_keyword"] in answer:
                print("  ✅ PASS - Validation caught the issue")
                print(f"     Response: {answer[:80]}...")
                passed += 1
            else:
                print("  ❌ FAIL - Validation missed the issue")
                print(f"     Expected: {test['expected_keyword']}")
                print(f"     Got: {answer[:80]}...")
                failed += 1
        else:
            # Should pass through validation
            if any(
                keyword in answer
                for keyword in [
                    "PREMISE VALIDATION",
                    "CONTRADICTION DETECTED",
                    "KNOWLEDGE BOUNDARY",
                ]
            ):
                print("  ❌ FAIL - False positive, blocked valid problem")
                print(f"     Response: {answer[:80]}...")
                failed += 1
            else:
                print("  ✅ PASS - Valid problem allowed through")
                passed += 1

        print()

print("=" * 80)
print(f"RESULTS: {passed}/{len(test_cases)} tests passed")
print("=" * 80)

if passed == len(test_cases):
    print("\n✅ ✅ ✅ ALL TESTS PASSED")
    print("\nPremise validation is working in actual code:")
    print("  ✅ Catches false mathematical premises")
    print("  ✅ Detects geometric contradictions")
    print("  ✅ Identifies impossible prime/even requests")
    print("  ✅ Blocks real-time/future data requests")
    print("  ✅ Allows valid problems through")
else:
    print(f"\n⚠️  {failed} tests failed")

print("\n" + "=" * 80)
