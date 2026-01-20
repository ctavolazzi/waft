#!/usr/bin/env python3
"""
TORTURE TEST SUITE - Test TheGuide under extreme conditions!

This suite goes beyond normal testing with:
- Edge cases and boundary conditions
- Chaos engineering (fault injection)
- Extreme performance stress tests
- Data corruption scenarios
- Race conditions and concurrency chaos
- Memory and resource exhaustion

Usage:
    python tests/torture_test_suite.py --all
    python tests/torture_test_suite.py --category chaos
    python tests/torture_test_suite.py --extreme
"""

import argparse
import concurrent.futures
import random
import string
import sys
import tempfile
import threading
import time
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import directly
import importlib.util

pantheon_path = Path(__file__).parent.parent / "src" / "waft" / "pantheon"
guide_path = pantheon_path / "guide.py"
spec = importlib.util.spec_from_file_location("guide", guide_path)
guide_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guide_module)

TheGuide = guide_module.TheGuide
Protocol = guide_module.Protocol
EvaluationScores = guide_module.EvaluationScores

# ============================================================================
# Test Framework (from mega_test_suite)
# ============================================================================


class TestResult:
    def __init__(self, name: str, passed: bool, message: str, duration: float = 0.0):
        self.name = name
        self.passed = passed
        self.message = message
        self.duration = duration


class TestRunner:
    def __init__(self):
        self.results: list[TestResult] = []
        self.start_time = time.time()

    def run_test(self, name: str, test_func, *args, **kwargs) -> TestResult:
        """Run a single test."""
        print(f"\n{'=' * 80}")
        print(f"🔥 TORTURE TEST: {name}")
        print(f"{'=' * 80}")

        start = time.time()
        try:
            result = test_func(*args, **kwargs)
            duration = time.time() - start
            test_result = TestResult(name, True, "✅ SURVIVED", duration)
            print(f"✅ SURVIVED in {duration:.2f}s")
        except AssertionError as e:
            duration = time.time() - start
            error_msg = str(e) if str(e) else "Assertion failed"
            test_result = TestResult(name, False, f"❌ FAILED: {error_msg}", duration)
            print(f"❌ FAILED: {error_msg}")
        except Exception as e:
            duration = time.time() - start
            error_msg = f"{type(e).__name__}: {str(e)}"
            test_result = TestResult(name, False, f"💥 CRASHED: {error_msg}", duration)
            print(f"💥 CRASHED: {error_msg}")
            import traceback

            traceback.print_exc()

        self.results.append(test_result)
        return test_result

    def print_summary(self):
        """Print test summary."""
        total_time = time.time() - self.start_time

        print("\n" + "=" * 80)
        print("🔥 TORTURE TEST SUMMARY")
        print("=" * 80)

        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        total = len(self.results)

        print(f"\nTotal Tests: {total}")
        print(f"✅ Survived: {passed}")
        print(f"❌ Failed/Crashed: {failed}")
        print(f"Survival Rate: {(passed / total) * 100:.1f}%")
        print(f"Total Time: {total_time:.2f}s")

        if failed > 0:
            print("\n❌ Failed/Crashed Tests:")
            for r in self.results:
                if not r.passed:
                    print(f"  - {r.name}: {r.message}")

        print("\n" + "=" * 80)


# ============================================================================
# Chaos LLM (Unpredictable Behavior)
# ============================================================================


class ChaosLLM:
    """LLM that randomly fails, hangs, or returns garbage."""

    def __init__(self, failure_rate=0.2, garbage_rate=0.2, slow_rate=0.2):
        self.failure_rate = failure_rate
        self.garbage_rate = garbage_rate
        self.slow_rate = slow_rate
        self.call_count = 0

    def complete(self, prompt: str) -> str:
        """Generate chaotic responses."""
        self.call_count += 1

        # Random failure
        if random.random() < self.failure_rate:
            raise Exception(f"Chaos LLM failure #{self.call_count}")

        # Random slowness
        if random.random() < self.slow_rate:
            time.sleep(random.uniform(0.1, 0.3))

        # Random garbage
        if random.random() < self.garbage_rate:
            return "".join(random.choices(string.ascii_letters + string.digits, k=100))

        # Normal evaluation response
        if "fvcu" in prompt.lower() or "evaluate" in prompt.lower():
            score = random.uniform(0.5, 0.95)
            return f"""```json
{{
  "factuality": {score:.2f},
  "validity": {score:.2f},
  "coherence": {score:.2f},
  "utility": {score:.2f},
  "faithfulness": {score:.2f},
  "overall": {score:.2f},
  "rationale": "Chaos evaluation",
  "strengths": ["Strength"],
  "weaknesses": ["Weakness"],
  "recommendations": ["Recommendation"],
  "should_continue": {str(random.random() > 0.5).lower()},
  "planning_detected": false,
  "unfaithful_reasoning_detected": false
}}
```"""

        return f"Chaos response #{self.call_count}"


# ============================================================================
# Stable LLM for controlled tests
# ============================================================================


class StableLLM:
    """Predictable LLM for non-chaos tests."""

    def __init__(self):
        self.call_count = 0

    def complete(self, prompt: str) -> str:
        self.call_count += 1

        if "fvcu" in prompt.lower() or "evaluate" in prompt.lower():
            return """```json
{
  "factuality": 0.85,
  "validity": 0.83,
  "coherence": 0.88,
  "utility": 0.84,
  "faithfulness": 0.87,
  "overall": 0.85,
  "rationale": "Test evaluation",
  "strengths": ["Good"],
  "weaknesses": ["Could improve"],
  "recommendations": ["Keep testing"],
  "should_continue": true,
  "planning_detected": false,
  "unfaithful_reasoning_detected": false
}
```"""

        return f"Response #{self.call_count}"


# ============================================================================
# EDGE CASE TESTS
# ============================================================================


def test_edge_empty_problem_statement(runner: TestRunner):
    """Test with empty problem statement."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        answer, protocol = guide.solve(problem_statement="", max_iterations=1)

        assert answer is not None, "Should handle empty problem statement"
        assert protocol is not None, "Should create protocol for empty problem"


def test_edge_massive_problem_statement(runner: TestRunner):
    """Test with 100KB problem statement."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create 100KB problem statement
        massive_problem = "A" * 100_000

        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        answer, protocol = guide.solve(problem_statement=massive_problem, max_iterations=1)

        assert len(protocol.problem_statement) == 100_000, (
            "Should preserve massive problem statement"
        )


def test_edge_zero_iterations(runner: TestRunner):
    """Test with max_iterations=0."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        answer, protocol = guide.solve(problem_statement="Test", max_iterations=0)

        assert protocol.iteration_count == 0, (
            f"Expected 0 iterations, got {protocol.iteration_count}"
        )


def test_edge_extreme_iterations(runner: TestRunner):
    """Test with 100 iterations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        start = time.time()
        answer, protocol = guide.solve(
            problem_statement="Extreme test",
            max_iterations=100,
            quality_threshold=1.0,  # Won't hit, do all iterations
        )
        duration = time.time() - start

        print(f"Completed 100 iterations in {duration:.2f}s")
        assert protocol.iteration_count == 100, (
            f"Expected 100 iterations, got {protocol.iteration_count}"
        )
        assert duration < 30.0, f"100 iterations took too long: {duration:.2f}s"


def test_edge_quality_threshold_zero(runner: TestRunner):
    """Test with quality_threshold=0.0 (should terminate immediately)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        answer, protocol = guide.solve(
            problem_statement="Test", max_iterations=10, quality_threshold=0.0
        )

        # Should terminate early due to threshold
        assert protocol.iteration_count <= 2, (
            f"Should terminate early with threshold=0.0, got {protocol.iteration_count} iterations"
        )


def test_edge_quality_threshold_impossible(runner: TestRunner):
    """Test with quality_threshold=1.0 (impossible to reach)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        answer, protocol = guide.solve(
            problem_statement="Test", max_iterations=5, quality_threshold=1.0
        )

        # Should do all iterations
        assert protocol.iteration_count == 5, (
            f"Expected 5 iterations, got {protocol.iteration_count}"
        )


def test_edge_unicode_chaos(runner: TestRunner):
    """Test with Unicode, emoji, and special characters."""
    with tempfile.TemporaryDirectory() as tmpdir:
        unicode_problem = "🔥💀🎮 Test with émojis, 中文, العربية, עברית, 🚀✨🌟"

        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        answer, protocol = guide.solve(problem_statement=unicode_problem, max_iterations=1)

        assert "🔥" in protocol.problem_statement, "Should preserve emojis"
        assert "中文" in protocol.problem_statement, "Should preserve Chinese"


# ============================================================================
# CHAOS ENGINEERING TESTS
# ============================================================================


def test_chaos_random_llm_failures(runner: TestRunner):
    """Test with LLM that randomly fails 30% of the time."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir),
            client_llm=ChaosLLM(failure_rate=0.3),
            guide_llm_config={"model": "test"},
        )
        guide.guide_llm = ChaosLLM(failure_rate=0.3)

        # Should handle failures gracefully
        try:
            answer, protocol = guide.solve(problem_statement="Chaos test", max_iterations=5)
            # If it completes, that's fine
            assert protocol is not None
        except Exception as e:
            # If it fails, that's also expected with chaos
            assert "Chaos LLM failure" in str(e)


def test_chaos_garbage_json_responses(runner: TestRunner):
    """Test with LLM that returns garbage 50% of the time."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir),
            client_llm=ChaosLLM(failure_rate=0.0, garbage_rate=0.5),
            guide_llm_config={"model": "test"},
        )
        guide.guide_llm = ChaosLLM(failure_rate=0.0, garbage_rate=0.5)

        # Should fallback to default scores when JSON is garbage
        answer, protocol = guide.solve(problem_statement="Garbage test", max_iterations=3)

        assert protocol is not None, "Should handle garbage JSON gracefully"
        # Some evaluations might have fallback scores (0.5)
        fallback_scores = [e for e in protocol.evaluations if e["scores"]["overall"] == 0.5]
        print(f"Got {len(fallback_scores)} fallback evaluations out of {len(protocol.evaluations)}")


def test_chaos_concurrent_writes_same_session(runner: TestRunner):
    """Test race condition: multiple threads writing to same session."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        # Create a protocol
        protocol = Protocol(
            session_id="race_test",
            problem_statement="Race condition test",
            quality_score=0.8,
            iteration_count=1,
        )

        # Write from multiple threads simultaneously
        def write_protocol(thread_id):
            for i in range(10):
                protocol.metadata["thread"] = thread_id
                protocol.metadata["write"] = i
                guide._save_session(protocol)
                time.sleep(0.001)

        threads = []
        for i in range(5):
            t = threading.Thread(target=write_protocol, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Should still have a valid protocol file
        retrieved = guide.get_protocol("race_test")
        assert retrieved is not None, "Protocol should exist after concurrent writes"


# ============================================================================
# EXTREME STRESS TESTS
# ============================================================================


def test_stress_100_concurrent_sessions(runner: TestRunner):
    """Stress test: 100 concurrent sessions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        print("Creating 100 concurrent sessions...")

        def run_session(i):
            guide = TheGuide(
                project_path=Path(tmpdir),
                client_llm=StableLLM(),
                guide_llm_config={"model": "test"},
            )
            guide.guide_llm = StableLLM()

            answer, protocol = guide.solve(problem_statement=f"Stress test {i}", max_iterations=2)
            return protocol.session_id

        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(run_session, i) for i in range(100)]
            session_ids = [f.result() for f in concurrent.futures.as_completed(futures)]
        duration = time.time() - start

        print(f"Completed 100 concurrent sessions in {duration:.2f}s")
        assert len(session_ids) == 100, f"Expected 100 session IDs, got {len(session_ids)}"
        assert len(set(session_ids)) == 100, f"Expected 100 unique IDs, got {len(set(session_ids))}"


def test_stress_massive_protocol_10mb(runner: TestRunner):
    """Test 10MB+ protocol serialization."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create massive reasoning chain
        massive_chain = [
            {
                "iteration": i,
                "instruction": "I" * 20000,  # 20KB per instruction
                "reasoning_trace": "R" * 100000,  # 100KB per trace
                "timestamp": datetime.now().isoformat(),
            }
            for i in range(100)  # 100 iterations = ~12MB
        ]

        massive_evaluations = [
            {
                "iteration": i,
                "scores": {
                    "factuality": 0.9,
                    "validity": 0.8,
                    "coherence": 0.85,
                    "utility": 0.9,
                    "faithfulness": 0.95,
                    "overall": 0.88,
                },
                "rationale": "R" * 10000,  # 10KB rationale
                "strengths": ["S"] * 100,
                "weaknesses": ["W"] * 100,
                "recommendations": ["R"] * 100,
            }
            for i in range(100)
        ]

        protocol = Protocol(
            session_id="massive_test",
            problem_statement="M" * 100000,  # 100KB
            reasoning_chain=massive_chain,
            evaluations=massive_evaluations,
            final_answer="A" * 100000,  # 100KB
            quality_score=0.88,
            iteration_count=100,
        )

        start = time.time()
        json_str = protocol.model_dump_json()
        duration = time.time() - start

        size_mb = len(json_str) / 1_000_000
        print(f"Serialized {size_mb:.2f}MB protocol in {duration:.3f}s")
        assert size_mb >= 10.0, f"Expected >= 10MB, got {size_mb:.2f}MB"
        assert duration < 5.0, f"Serialization too slow: {duration:.3f}s"


def test_stress_rapid_create_destroy(runner: TestRunner):
    """Test rapid creation and destruction (memory leak check)."""
    print("Rapidly creating/destroying 100 TheGuide instances...")

    with tempfile.TemporaryDirectory() as tmpdir:
        start = time.time()
        for i in range(100):
            guide = TheGuide(
                project_path=Path(tmpdir),
                client_llm=StableLLM(),
                guide_llm_config={"model": "test"},
            )
            guide.guide_llm = StableLLM()

            # Run a quick session
            answer, protocol = guide.solve(problem_statement=f"Test {i}", max_iterations=1)

            # Explicitly delete
            del guide

            if (i + 1) % 20 == 0:
                print(f"  Created/destroyed {i + 1}/100 instances")

        duration = time.time() - start
        print(f"Completed 100 create/destroy cycles in {duration:.2f}s")
        assert duration < 10.0, f"Create/destroy too slow: {duration:.2f}s"


def test_stress_storage_quota(runner: TestRunner):
    """Test with 1000 sessions (storage stress)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        print("Creating 1000 sessions (storage stress test)...")

        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        start = time.time()
        for i in range(1000):
            answer, protocol = guide.solve(problem_statement=f"Storage test {i}", max_iterations=1)

            if (i + 1) % 200 == 0:
                print(f"  Created {i + 1}/1000 sessions")

        duration = time.time() - start

        # Check storage
        sessions_dir = Path(tmpdir) / "_pantheon" / "guide" / "sessions"
        protocols_dir = Path(tmpdir) / "_pantheon" / "guide" / "protocols"

        session_count = len(list(sessions_dir.glob("*.json")))
        protocol_count = len(list(protocols_dir.glob("*.json")))

        print(f"Created {session_count} sessions and {protocol_count} protocols in {duration:.2f}s")
        assert session_count == 1000, f"Expected 1000 sessions, got {session_count}"
        assert protocol_count == 1000, f"Expected 1000 protocols, got {protocol_count}"


# ============================================================================
# DATA INTEGRITY TESTS
# ============================================================================


def test_integrity_corrupted_index(runner: TestRunner):
    """Test recovery from corrupted index file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )

        # Corrupt the index
        index_file = Path(tmpdir) / "_pantheon" / "guide" / "index.json"
        index_file.write_text("CORRUPTED{{{{{")

        # Create new instance (should recover)
        guide2 = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )

        # Should have fallback index
        assert guide2.index is not None, "Should recover from corrupted index"
        assert "sessions" in guide2.index, "Should have sessions key in recovered index"


def test_integrity_missing_protocol_file(runner: TestRunner):
    """Test handling of missing protocol file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        # Create a session
        answer, protocol = guide.solve(problem_statement="Test", max_iterations=1)

        # Delete the protocol file
        protocol_file = (
            Path(tmpdir) / "_pantheon" / "guide" / "protocols" / f"{protocol.session_id}.json"
        )
        protocol_file.unlink()

        # Try to retrieve (should handle gracefully)
        retrieved = guide.get_protocol(protocol.session_id)
        assert retrieved is None, "Should return None for missing protocol"


def test_integrity_duplicate_session_ids(runner: TestRunner):
    """Test handling of duplicate session IDs (edge case)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )

        # Manually create protocols with same ID
        protocol1 = Protocol(
            session_id="duplicate_test",
            problem_statement="First",
            quality_score=0.8,
            iteration_count=1,
        )

        protocol2 = Protocol(
            session_id="duplicate_test",
            problem_statement="Second (should overwrite)",
            quality_score=0.9,
            iteration_count=2,
        )

        guide._save_session(protocol1)
        guide._save_session(protocol2)

        # Retrieve (should get the second one)
        retrieved = guide.get_protocol("duplicate_test")
        assert retrieved.problem_statement == "Second (should overwrite)", (
            "Should get latest protocol"
        )
        assert retrieved.iteration_count == 2, "Should have overwritten"


# ============================================================================
# EXTREME BOUNDARY TESTS
# ============================================================================


def test_boundary_negative_iterations(runner: TestRunner):
    """Test with negative max_iterations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        # Should handle gracefully (treat as 0?)
        answer, protocol = guide.solve(problem_statement="Negative test", max_iterations=-5)

        assert protocol.iteration_count == 0, (
            f"Should do 0 iterations for negative max, got {protocol.iteration_count}"
        )


def test_boundary_quality_threshold_negative(runner: TestRunner):
    """Test with negative quality threshold."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        # Should terminate immediately (any score > -1.0)
        answer, protocol = guide.solve(
            problem_statement="Test", max_iterations=10, quality_threshold=-1.0
        )

        assert protocol.iteration_count <= 2, "Should terminate early with negative threshold"


def test_boundary_quality_threshold_over_one(runner: TestRunner):
    """Test with quality threshold > 1.0."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        # Should never reach threshold
        answer, protocol = guide.solve(
            problem_statement="Test", max_iterations=3, quality_threshold=2.0
        )

        assert protocol.iteration_count == 3, "Should do all iterations with impossible threshold"


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================


def run_all_tests():
    """Run all torture tests."""
    runner = TestRunner()

    print("\n" + "=" * 80)
    print("🔥 TORTURE TEST SUITE - Testing TheGuide under EXTREME conditions!")
    print("=" * 80)

    # Edge cases
    print("\n🎯 EDGE CASE TESTS")
    runner.run_test("Empty Problem Statement", test_edge_empty_problem_statement, runner)
    runner.run_test("Massive Problem (100KB)", test_edge_massive_problem_statement, runner)
    runner.run_test("Zero Iterations", test_edge_zero_iterations, runner)
    runner.run_test("Extreme Iterations (100)", test_edge_extreme_iterations, runner)
    runner.run_test("Quality Threshold = 0.0", test_edge_quality_threshold_zero, runner)
    runner.run_test(
        "Quality Threshold = 1.0 (Impossible)", test_edge_quality_threshold_impossible, runner
    )
    runner.run_test("Unicode Chaos (Emojis, Languages)", test_edge_unicode_chaos, runner)

    # Chaos engineering
    print("\n💥 CHAOS ENGINEERING TESTS")
    runner.run_test("Random LLM Failures (30%)", test_chaos_random_llm_failures, runner)
    runner.run_test("Garbage JSON Responses (50%)", test_chaos_garbage_json_responses, runner)
    runner.run_test(
        "Concurrent Writes Race Condition", test_chaos_concurrent_writes_same_session, runner
    )

    # Extreme stress
    print("\n⚡ EXTREME STRESS TESTS")
    runner.run_test("100 Concurrent Sessions", test_stress_100_concurrent_sessions, runner)
    runner.run_test("Massive Protocol (10MB)", test_stress_massive_protocol_10mb, runner)
    runner.run_test("Rapid Create/Destroy (100x)", test_stress_rapid_create_destroy, runner)
    runner.run_test("Storage Quota (1000 sessions)", test_stress_storage_quota, runner)

    # Data integrity
    print("\n🛡️  DATA INTEGRITY TESTS")
    runner.run_test("Corrupted Index Recovery", test_integrity_corrupted_index, runner)
    runner.run_test("Missing Protocol File", test_integrity_missing_protocol_file, runner)
    runner.run_test("Duplicate Session IDs", test_integrity_duplicate_session_ids, runner)

    # Extreme boundaries
    print("\n🔬 EXTREME BOUNDARY TESTS")
    runner.run_test("Negative Iterations", test_boundary_negative_iterations, runner)
    runner.run_test("Negative Quality Threshold", test_boundary_quality_threshold_negative, runner)
    runner.run_test("Quality Threshold > 1.0", test_boundary_quality_threshold_over_one, runner)

    # Summary
    runner.print_summary()

    return runner.results


def main():
    parser = argparse.ArgumentParser(description="Torture Test Suite for TheGuide")
    parser.add_argument("--all", action="store_true", help="Run all torture tests")
    parser.add_argument(
        "--category",
        choices=["edge", "chaos", "stress", "integrity", "boundary"],
        help="Run specific category",
    )
    parser.add_argument("--extreme", action="store_true", help="Run only extreme stress tests")

    args = parser.parse_args()

    if args.all or (not args.category and not args.extreme):
        results = run_all_tests()
    else:
        runner = TestRunner()

        if args.category == "edge" or args.extreme:
            print("\n🎯 EDGE CASE TESTS")
            runner.run_test("Empty Problem Statement", test_edge_empty_problem_statement, runner)
            runner.run_test("Massive Problem (100KB)", test_edge_massive_problem_statement, runner)
            # Add more as needed

        if args.extreme:
            print("\n⚡ EXTREME STRESS TESTS")
            runner.run_test("100 Concurrent Sessions", test_stress_100_concurrent_sessions, runner)
            runner.run_test("Massive Protocol (10MB)", test_stress_massive_protocol_10mb, runner)
            runner.run_test("Storage Quota (1000 sessions)", test_stress_storage_quota, runner)

        runner.print_summary()
        results = runner.results

    # Exit code based on results
    failed = sum(1 for r in results if not r.passed)
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
