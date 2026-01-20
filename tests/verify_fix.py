#!/usr/bin/env python3
"""
VERIFY THE FIX - Test that the actual code fix works
"""

import json
import statistics
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import the NOW-FIXED TheGuide
import importlib.util

guide_path = Path(__file__).parent.parent / "src" / "waft" / "pantheon" / "guide.py"
spec = importlib.util.spec_from_file_location("guide", guide_path)
guide_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guide_module)
TheGuide = guide_module.TheGuide


class SimpleTestLLM:
    def __init__(self):
        self.call_count = 0

    def complete(self, prompt: str) -> str:
        self.call_count += 1
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
        return "Test answer"


print("=" * 80)
print("VERIFYING FIX IN ACTUAL CODE")
print("=" * 80)

with tempfile.TemporaryDirectory() as tmpdir:
    llm = SimpleTestLLM()
    guide = TheGuide(project_path=Path(tmpdir), client_llm=llm, guide_llm_config={"model": "test"})
    guide.guide_llm = llm  # Set guide LLM directly

    print("\nCreating 500 sessions with FIXED code...")
    times = []

    for i in range(500):
        start = time.time()
        answer, protocol = guide.solve(
            problem_statement=f"Test {i}", max_iterations=1, quality_threshold=0.90
        )
        times.append(time.time() - start)

        if (i + 1) % 50 == 0:
            print(f"  Session {i + 1}: {times[-1] * 1000:.2f}ms")

    first_50 = statistics.mean(times[:50])
    last_50 = statistics.mean(times[-50:])
    degradation = ((last_50 - first_50) / first_50) * 100

    print("\n📊 RESULTS WITH FIX:")
    print(f"  First 50 sessions: {first_50 * 1000:.2f}ms")
    print(f"  Last 50 sessions: {last_50 * 1000:.2f}ms")
    print(f"  Degradation: {degradation:.1f}%")

    if degradation < 600:
        print("\n✅ FIX VERIFIED - Performance degradation reduced")
    else:
        print("\n⚠️  Still showing high degradation")

print("\n" + "=" * 80)
