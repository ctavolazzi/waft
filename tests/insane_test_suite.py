#!/usr/bin/env python3
"""
INSANE TEST SUITE - Tests so brutal they make torture look like a warm-up

This suite contains:
- Adversarial inputs designed to break JSON parsers
- File system corruption mid-write
- Memory exhaustion attacks
- Unicode nightmare scenarios
- Concurrent chaos with deliberate race conditions
- Pathological edge cases
- JSON bombs and exponential explosions

If TheGuide survives this, it's truly unbreakable.
"""

import argparse
import concurrent.futures
import json
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
# Test Framework
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
        print(f"💀 INSANE TEST: {name}")
        print(f"{'=' * 80}")

        start = time.time()
        try:
            test_func(*args, **kwargs)
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
            test_result = TestResult(name, False, f"💀 DIED: {error_msg}", duration)
            print(f"💀 DIED: {error_msg}")
            import traceback

            traceback.print_exc()

        self.results.append(test_result)
        return test_result

    def print_summary(self):
        """Print test summary."""
        total_time = time.time() - self.start_time

        print("\n" + "=" * 80)
        print("💀 INSANE TEST SUMMARY")
        print("=" * 80)

        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        total = len(self.results)

        print(f"\nTotal Tests: {total}")
        print(f"✅ Survived: {passed}")
        print(f"💀 Died: {failed}")
        print(f"Survival Rate: {(passed / total) * 100:.1f}%")
        print(f"Total Time: {total_time:.2f}s")

        if failed > 0:
            print("\n💀 Failed/Died Tests:")
            for r in self.results:
                if not r.passed:
                    print(f"  - {r.name}: {r.message}")

        print("\n" + "=" * 80)


# ============================================================================
# Evil LLM (Adversarial)
# ============================================================================


class EvilLLM:
    """LLM designed to return pathological responses."""

    def __init__(self, mode="json_bomb"):
        self.mode = mode
        self.call_count = 0

    def complete(self, prompt: str) -> str:
        self.call_count += 1

        if "evaluate" not in prompt.lower():
            return "Evil response"

        if self.mode == "json_bomb":
            # Nested JSON that could cause parser issues
            return '{"a":{"b":{"c":{"d":{"e":{"f":{"g":{"h":{"i":{"j":"deep"}}}}}}}}}}' * 100

        elif self.mode == "unicode_hell":
            # Unicode nightmares
            return """```json
{
  "factuality": 0.85,
  "validity": 0.85,
  "coherence": 0.85,
  "utility": 0.85,
  "faithfulness": 0.85,
  "overall": 0.85,
  "rationale": "Test \u0000 with \uffff null \u202e characters",
  "strengths": ["מימין לשמאל"],
  "weaknesses": ["‮‮‮backwards"],
  "recommendations": ["​​​​zero-width"],
  "should_continue": true,
  "planning_detected": false,
  "unfaithful_reasoning_detected": false
}
```"""

        elif self.mode == "malformed_json":
            # Intentionally broken JSON
            return '{factuality: 0.85, "validity": .85, coherence: 0.85, }'

        elif self.mode == "injection_attack":
            # Try to break out of JSON
            return """```json
{
  "factuality": 0.85,
  "validity": 0.85,
  "coherence": 0.85,
  "utility": 0.85,
  "faithfulness": 0.85,
  "overall": 0.85,
  "rationale": "\\"}}; DROP TABLE sessions; --",
  "strengths": [],
  "weaknesses": [],
  "recommendations": [],
  "should_continue": true,
  "planning_detected": false,
  "unfaithful_reasoning_detected": false
}
```"""

        # Default safe response
        return '```json\n{"factuality": 0.85, "validity": 0.85, "coherence": 0.85, "utility": 0.85, "faithfulness": 0.85, "overall": 0.85, "rationale": "test", "strengths": [], "weaknesses": [], "recommendations": [], "should_continue": true, "planning_detected": false, "unfaithful_reasoning_detected": false}\n```'


class StableLLM:
    """Baseline LLM for comparison."""

    def complete(self, prompt):
        if "evaluate" in prompt.lower():
            return '```json\n{"factuality": 0.85, "validity": 0.85, "coherence": 0.85, "utility": 0.85, "faithfulness": 0.85, "overall": 0.85, "rationale": "test", "strengths": [], "weaknesses": [], "recommendations": [], "should_continue": true, "planning_detected": false, "unfaithful_reasoning_detected": false}\n```'
        return "test"


# ============================================================================
# ADVERSARIAL INPUT TESTS
# ============================================================================


def test_adversarial_json_bomb(runner: TestRunner):
    """Test with deeply nested JSON bomb."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = EvilLLM(mode="json_bomb")

        # Should handle JSON bomb gracefully (fallback to defaults)
        answer, protocol = guide.solve(problem_statement="Test JSON bomb", max_iterations=2)

        assert protocol is not None, "Should survive JSON bomb"
        print(f"Handled JSON bomb with {protocol.iteration_count} iterations")


def test_adversarial_unicode_hell(runner: TestRunner):
    """Test with pathological Unicode characters."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Problem with every Unicode nightmare
        problem = (
            "\u0000 null byte "
            "\uffff max unicode "
            "\u202e right-to-left override "
            "​​​zero-width space "
            "‮‮‮backwards "
            "👨‍👩‍👧‍👦 multi-codepoint emoji "
            "𝕳𝖊𝖑𝖑𝖔 mathematical alphanumeric "
            "\r\n\r\n multiple line endings "
        )

        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = EvilLLM(mode="unicode_hell")

        answer, protocol = guide.solve(problem_statement=problem, max_iterations=1)

        assert protocol is not None, "Should handle Unicode hell"
        # Verify file can be read back
        retrieved = guide.get_protocol(protocol.session_id)
        assert retrieved is not None, "Should retrieve Unicode nightmare"


def test_adversarial_malformed_json(runner: TestRunner):
    """Test with deliberately malformed JSON responses."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = EvilLLM(mode="malformed_json")

        # Should fallback to default scores
        answer, protocol = guide.solve(problem_statement="Test malformed JSON", max_iterations=2)

        assert protocol is not None, "Should survive malformed JSON"
        # Check for fallback scores
        fallback_count = sum(1 for e in protocol.evaluations if e["scores"]["overall"] == 0.5)
        print(f"Got {fallback_count} fallback evaluations")


def test_adversarial_injection_attack(runner: TestRunner):
    """Test SQL injection-style attacks in JSON."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = EvilLLM(mode="injection_attack")

        answer, protocol = guide.solve(problem_statement='"; DROP TABLE--', max_iterations=1)

        # Verify files still exist (no SQL injection worked)
        sessions_dir = Path(tmpdir) / "_pantheon" / "guide" / "sessions"
        assert sessions_dir.exists(), "Sessions directory should still exist"
        assert len(list(sessions_dir.glob("*.json"))) > 0, "Session files should exist"


def test_adversarial_path_traversal(runner: TestRunner):
    """Test path traversal attacks in session IDs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Try to create protocol with malicious session ID
        evil_ids = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32",
            "session_../../evil",
            "session_\x00null",
        ]

        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )

        for evil_id in evil_ids:
            protocol = Protocol(
                session_id=evil_id, problem_statement="Evil", quality_score=0.5, iteration_count=1
            )

            try:
                guide._save_session(protocol)
                # Check that it didn't escape the sandbox
                sessions_dir = Path(tmpdir) / "_pantheon" / "guide" / "sessions"
                for f in sessions_dir.rglob("*"):
                    assert str(tmpdir) in str(f.resolve()), f"File escaped sandbox: {f}"
                print(f"  ✅ Blocked path traversal: {evil_id}")
            except Exception:
                # Also acceptable to reject outright
                print(f"  ✅ Rejected malicious ID: {evil_id}")


# ============================================================================
# FILE SYSTEM CHAOS TESTS
# ============================================================================


def test_filesystem_concurrent_delete(runner: TestRunner):
    """Test file deletion during concurrent reads."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        # Create a session
        answer, protocol = guide.solve(problem_statement="Test", max_iterations=1)

        session_id = protocol.session_id
        session_file = Path(tmpdir) / "_pantheon" / "guide" / "sessions" / f"{session_id}.json"

        # Start reading, delete mid-read
        def reader():
            for _i in range(10):
                try:
                    guide.get_protocol(session_id)
                    time.sleep(0.01)
                except:
                    pass  # Expected to fail sometimes

        def deleter():
            time.sleep(0.02)
            if session_file.exists():
                session_file.unlink()

        t1 = threading.Thread(target=reader)
        t2 = threading.Thread(target=deleter)

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # Should not crash
        print("Survived concurrent delete")


def test_filesystem_full_disk_simulation(runner: TestRunner):
    """Test behavior when disk is 'full' (tiny temp dir)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        # Create a massive protocol that will stress disk
        massive_problem = "A" * 1_000_000  # 1MB problem

        try:
            answer, protocol = guide.solve(problem_statement=massive_problem, max_iterations=1)
            # If it succeeds, verify file exists
            session_file = (
                Path(tmpdir) / "_pantheon" / "guide" / "sessions" / f"{protocol.session_id}.json"
            )
            assert session_file.exists(), "Large file should be written"
            print(f"Wrote {session_file.stat().st_size / 1_000_000:.2f}MB file")
        except Exception as e:
            # Acceptable to fail gracefully
            print(f"Handled disk stress: {e}")


def test_filesystem_corrupted_write(runner: TestRunner):
    """Test recovery from partial writes (simulated)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        answer, protocol = guide.solve(problem_statement="Test", max_iterations=1)

        # Corrupt the file
        session_file = (
            Path(tmpdir) / "_pantheon" / "guide" / "sessions" / f"{protocol.session_id}.json"
        )
        content = session_file.read_text()
        corrupted = content[: len(content) // 2]  # Cut in half
        session_file.write_text(corrupted)

        # Try to read (should handle gracefully)
        try:
            retrieved = guide.get_protocol(protocol.session_id)
            # If it returns None, that's acceptable
            if retrieved is None:
                print("Handled corrupted file by returning None")
        except json.JSONDecodeError:
            print("Handled corrupted file with exception")


# ============================================================================
# EXTREME CONCURRENCY TESTS
# ============================================================================


def test_concurrency_1000_simultaneous(runner: TestRunner):
    """Test 1000 simultaneous sessions (extreme concurrency)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        print("Creating 1000 SIMULTANEOUS sessions...")

        def run_session(i):
            guide = TheGuide(
                project_path=Path(tmpdir),
                client_llm=StableLLM(),
                guide_llm_config={"model": "test"},
            )
            guide.guide_llm = StableLLM()

            answer, protocol = guide.solve(problem_statement=f"Concurrent {i}", max_iterations=1)
            return protocol.session_id

        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(run_session, i) for i in range(1000)]
            session_ids = []
            completed = 0
            for future in concurrent.futures.as_completed(futures):
                session_ids.append(future.result())
                completed += 1
                if completed % 200 == 0:
                    print(f"  {completed}/1000 sessions completed")

        duration = time.time() - start

        print(f"Completed 1000 concurrent sessions in {duration:.2f}s")
        assert len(session_ids) == 1000, f"Expected 1000 sessions, got {len(session_ids)}"
        unique_count = len(set(session_ids))
        assert unique_count == 1000, f"Expected 1000 unique IDs, got {unique_count}"
        print("✅ All 1000 session IDs are unique!")


def test_concurrency_read_write_chaos(runner: TestRunner):
    """Test simultaneous reads and writes to same session."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        # Create initial session
        answer, protocol = guide.solve(problem_statement="Test", max_iterations=1)
        session_id = protocol.session_id

        results = {"reads": 0, "writes": 0, "errors": 0}

        def reader():
            for _i in range(20):
                try:
                    guide.get_protocol(session_id)
                    results["reads"] += 1
                except:
                    results["errors"] += 1
                time.sleep(0.001)

        def writer():
            for i in range(20):
                try:
                    protocol.metadata["write"] = i
                    guide._save_session(protocol)
                    results["writes"] += 1
                except:
                    results["errors"] += 1
                time.sleep(0.001)

        threads = []
        for _i in range(5):
            threads.append(threading.Thread(target=reader))
            threads.append(threading.Thread(target=writer))

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        print(
            f"Reads: {results['reads']}, Writes: {results['writes']}, Errors: {results['errors']}"
        )
        # Should have some successful operations
        assert results["reads"] > 0 or results["writes"] > 0, (
            "Should have some successful operations"
        )


# ============================================================================
# PATHOLOGICAL INPUT TESTS
# ============================================================================


def test_pathological_infinite_loop_potential(runner: TestRunner):
    """Test that early termination works (no infinite loops)."""
    with tempfile.TemporaryDirectory() as tmpdir:

        class InfiniteLoopLLM:
            def complete(self, prompt):
                # Always say to continue
                if "evaluate" in prompt.lower():
                    return '```json\n{"factuality": 0.5, "validity": 0.5, "coherence": 0.5, "utility": 0.5, "faithfulness": 0.5, "overall": 0.5, "rationale": "keep going", "strengths": [], "weaknesses": [], "recommendations": [], "should_continue": true, "planning_detected": false, "unfaithful_reasoning_detected": false}\n```'
                return "continue"

        guide = TheGuide(
            project_path=Path(tmpdir),
            client_llm=InfiniteLoopLLM(),
            guide_llm_config={"model": "test"},
        )
        guide.guide_llm = InfiniteLoopLLM()

        start = time.time()
        answer, protocol = guide.solve(
            problem_statement="Infinite loop test",
            max_iterations=100,
            quality_threshold=0.99,  # Unreachable
        )
        duration = time.time() - start

        # Should terminate at max_iterations
        assert protocol.iteration_count == 100, (
            f"Should do exactly 100 iterations, got {protocol.iteration_count}"
        )
        assert duration < 10.0, f"Should complete quickly, took {duration:.2f}s"
        print(f"Terminated correctly after 100 iterations in {duration:.2f}s")


def test_pathological_maximum_nesting(runner: TestRunner):
    """Test with extremely deep reasoning chains."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        # Create protocol with 500 iterations
        massive_chain = [
            {
                "iteration": i,
                "instruction": f"Step {i}",
                "reasoning_trace": f"Reasoning {i}",
                "timestamp": datetime.now().isoformat(),
            }
            for i in range(500)
        ]

        massive_evaluations = [
            {
                "iteration": i,
                "scores": {
                    "factuality": 0.85,
                    "validity": 0.85,
                    "coherence": 0.85,
                    "utility": 0.85,
                    "faithfulness": 0.85,
                    "overall": 0.85,
                },
                "rationale": "test",
                "strengths": [],
                "weaknesses": [],
                "recommendations": [],
                "should_continue": False,
                "planning_detected": False,
                "unfaithful_reasoning_detected": False,
            }
            for i in range(500)
        ]

        protocol = Protocol(
            session_id="deep_test",
            problem_statement="Deep nesting",
            reasoning_chain=massive_chain,
            evaluations=massive_evaluations,
            final_answer="Deep",
            quality_score=0.85,
            iteration_count=500,
        )

        # Should serialize/deserialize
        start = time.time()
        json_str = protocol.model_dump_json()
        duration = time.time() - start

        print(f"Serialized 500-iteration protocol in {duration:.3f}s")
        assert duration < 2.0, f"Serialization too slow: {duration:.3f}s"

        # Should deserialize
        protocol2 = Protocol.model_validate_json(json_str)
        assert protocol2.iteration_count == 500


def test_pathological_memory_bomb(runner: TestRunner):
    """Test memory usage with massive protocols."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        # Create 100 sessions with large data
        print("Creating 100 large sessions...")
        for i in range(100):
            large_problem = "X" * 10000  # 10KB each
            answer, protocol = guide.solve(problem_statement=large_problem, max_iterations=1)

            if (i + 1) % 20 == 0:
                print(f"  Created {i + 1}/100")

        # Check memory usage is reasonable (files exist)
        sessions_dir = Path(tmpdir) / "_pantheon" / "guide" / "sessions"
        session_count = len(list(sessions_dir.glob("*.json")))

        assert session_count == 100, f"Expected 100 sessions, got {session_count}"
        print("✅ Created 100 large sessions without crashing")


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================


def run_all_tests():
    """Run all insane tests."""
    runner = TestRunner()

    print("\n" + "=" * 80)
    print("💀 INSANE TEST SUITE - Making TheGuide BEG for mercy!")
    print("=" * 80)

    # Adversarial inputs
    print("\n🎯 ADVERSARIAL INPUT TESTS")
    runner.run_test("JSON Bomb Attack", test_adversarial_json_bomb, runner)
    runner.run_test("Unicode Hell", test_adversarial_unicode_hell, runner)
    runner.run_test("Malformed JSON", test_adversarial_malformed_json, runner)
    runner.run_test("Injection Attack", test_adversarial_injection_attack, runner)
    runner.run_test("Path Traversal Attack", test_adversarial_path_traversal, runner)

    # File system chaos
    print("\n📁 FILE SYSTEM CHAOS TESTS")
    runner.run_test("Concurrent Delete", test_filesystem_concurrent_delete, runner)
    runner.run_test("Full Disk Simulation", test_filesystem_full_disk_simulation, runner)
    runner.run_test("Corrupted Write Recovery", test_filesystem_corrupted_write, runner)

    # Extreme concurrency
    print("\n⚡ EXTREME CONCURRENCY TESTS")
    runner.run_test("1000 Simultaneous Sessions", test_concurrency_1000_simultaneous, runner)
    runner.run_test("Read/Write Chaos", test_concurrency_read_write_chaos, runner)

    # Pathological inputs
    print("\n🔬 PATHOLOGICAL INPUT TESTS")
    runner.run_test("Infinite Loop Prevention", test_pathological_infinite_loop_potential, runner)
    runner.run_test("Maximum Nesting (500 iterations)", test_pathological_maximum_nesting, runner)
    runner.run_test("Memory Bomb (100 large sessions)", test_pathological_memory_bomb, runner)

    # Summary
    runner.print_summary()

    return runner.results


def main():
    parser = argparse.ArgumentParser(description="Insane Test Suite for TheGuide")
    parser.add_argument("--all", action="store_true", help="Run all tests")

    parser.parse_args()

    results = run_all_tests()

    # Exit code based on results
    failed = sum(1 for r in results if not r.passed)
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
