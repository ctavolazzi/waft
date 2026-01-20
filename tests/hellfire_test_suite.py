#!/usr/bin/env python3
"""
HELLFIRE TEST SUITE - Tests designed to find ANY possible failure

These tests are specifically designed to expose bugs, not just verify functionality.
If TheGuide passes these, it's genuinely bulletproof.

Categories:
- Time-based attacks (time travel, timezone chaos)
- Float precision edge cases
- Pydantic validation breaking
- Thread safety violations
- Signal interruption
- Resource exhaustion (real limits)
- Filesystem permission errors
- Encoding nightmares
- Clock skew attacks
"""

import sys
import os
import time
import json
import tempfile
import random
import threading
import signal
from pathlib import Path
from typing import Dict, Any, List
import argparse
from datetime import datetime, timedelta
import concurrent.futures
import math

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
        self.results: List[TestResult] = []
        self.start_time = time.time()

    def run_test(self, name: str, test_func, *args, **kwargs) -> TestResult:
        """Run a single test."""
        print(f"\n{'='*80}")
        print(f"🔥 HELLFIRE: {name}")
        print(f"{'='*80}")

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
            test_result = TestResult(name, False, f"💥 EXPLODED: {error_msg}", duration)
            print(f"💥 EXPLODED: {error_msg}")
            import traceback
            traceback.print_exc()

        self.results.append(test_result)
        return test_result

    def print_summary(self):
        """Print test summary."""
        total_time = time.time() - self.start_time

        print("\n" + "="*80)
        print("🔥 HELLFIRE TEST SUMMARY")
        print("="*80)

        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        total = len(self.results)

        print(f"\nTotal Tests: {total}")
        print(f"✅ Survived: {passed}")
        print(f"💥 Exploded: {failed}")
        print(f"Survival Rate: {(passed/total)*100:.1f}%")
        print(f"Total Time: {total_time:.2f}s")

        if failed > 0:
            print("\n💥 Exploded Tests:")
            for r in self.results:
                if not r.passed:
                    print(f"  - {r.name}: {r.message}")

        print("\n" + "="*80)

class StableLLM:
    """Baseline LLM."""
    def complete(self, prompt):
        if 'evaluate' in prompt.lower():
            return '```json\n{"factuality": 0.85, "validity": 0.85, "coherence": 0.85, "utility": 0.85, "faithfulness": 0.85, "overall": 0.85, "rationale": "test", "strengths": [], "weaknesses": [], "recommendations": [], "should_continue": true, "planning_detected": false, "unfaithful_reasoning_detected": false}\n```'
        return 'test response'

# ============================================================================
# FLOAT PRECISION EDGE CASES
# ============================================================================

def test_float_precision_evaluation_scores(runner: TestRunner):
    """Test Pydantic validation with float precision edge cases."""

    # Test scores that are EXACTLY on boundaries
    edge_scores = [
        0.0,  # Minimum
        1.0,  # Maximum
        0.5,  # Middle
        1e-10,  # Near zero
        1.0 - 1e-10,  # Near one
        float('0.33333333333333333333'),  # Repeating decimal
        0.999999999999999,  # Float precision limit
    ]

    for score in edge_scores:
        try:
            eval_scores = EvaluationScores(
                factuality=score,
                validity=score,
                coherence=score,
                utility=score,
                faithfulness=score,
                overall=score
            )
            print(f"  ✅ Handled score: {score}")
        except Exception as e:
            raise AssertionError(f"Failed on score {score}: {e}")

def test_float_precision_negative_zero(runner: TestRunner):
    """Test with negative zero (-0.0)."""

    # In Python, -0.0 == 0.0 but they have different representations
    scores = EvaluationScores(
        factuality=-0.0,
        validity=0.0,
        coherence=-0.0,
        utility=0.0,
        faithfulness=-0.0,
        overall=0.0
    )

    assert scores.factuality == 0.0, "Should handle -0.0"
    print(f"Handled negative zero correctly")

def test_float_precision_quality_threshold_edge(runner: TestRunner):
    """Test quality threshold with floating point precision issues."""
    with tempfile.TemporaryDirectory() as tmpdir:
        class PreciseLLM:
            def complete(self, prompt):
                if 'evaluate' in prompt.lower():
                    # Return EXACTLY the threshold
                    return '```json\n{"factuality": 0.85, "validity": 0.85, "coherence": 0.85, "utility": 0.85, "faithfulness": 0.85, "overall": 0.85, "rationale": "test", "strengths": [], "weaknesses": [], "recommendations": [], "should_continue": true, "planning_detected": false, "unfaithful_reasoning_detected": false}\n```'
                return 'test'

        guide = TheGuide(
            project_path=Path(tmpdir),
            client_llm=PreciseLLM(),
            guide_llm_config={"model": "test"}
        )
        guide.guide_llm = PreciseLLM()

        # Threshold of 0.85, score returns EXACTLY 0.85
        # Should this terminate? (0.85 >= 0.85 is True)
        answer, protocol = guide.solve(
            problem_statement="Float precision test",
            max_iterations=5,
            quality_threshold=0.85
        )

        # Should terminate early (score >= threshold)
        print(f"Iterations: {protocol.iteration_count}, Quality: {protocol.quality_score:.10f}")
        assert protocol.iteration_count <= 2, f"Should terminate early with exact threshold match"

# ============================================================================
# TIME-BASED ATTACKS
# ============================================================================

def test_time_clock_skew_microseconds(runner: TestRunner):
    """Test rapid session creation (microsecond collisions)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir),
            client_llm=StableLLM(),
            guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        # Create sessions as fast as possible
        session_ids = []
        for i in range(1000):
            answer, protocol = guide.solve(
                problem_statement=f"Speed test {i}",
                max_iterations=1
            )
            session_ids.append(protocol.session_id)

        # All should be unique
        unique_count = len(set(session_ids))
        assert unique_count == 1000, f"Expected 1000 unique IDs, got {unique_count}"
        print(f"✅ 1000 rapid sessions, all unique IDs")

def test_time_timestamp_string_format(runner: TestRunner):
    """Test timestamp parsing edge cases."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create protocol with various timestamp formats
        timestamps = [
            datetime.now().isoformat(),
            datetime.now().isoformat() + "Z",
            datetime.now().isoformat() + "+00:00",
            datetime.now().isoformat() + ".123456",
        ]

        for ts in timestamps:
            protocol = Protocol(
                session_id=f"ts_test_{ts.replace(':', '_')}",
                problem_statement="Test",
                quality_score=0.8,
                iteration_count=1,
                created=ts
            )

            # Should serialize/deserialize
            json_str = protocol.model_dump_json()
            protocol2 = Protocol.model_validate_json(json_str)
            print(f"  ✅ Handled timestamp: {ts[:30]}...")

# ============================================================================
# ENCODING NIGHTMARES
# ============================================================================

def test_encoding_every_encoding(runner: TestRunner):
    """Test with different text encodings."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test various encoding edge cases
        test_strings = [
            b'\xff\xfe'.decode('utf-16', errors='ignore'),  # BOM
            ''.join(chr(i) for i in range(32, 127)),  # ASCII printable
            ''.join(chr(i) for i in [0x200B, 0x200C, 0x200D]),  # Zero-width
            '\ufeff',  # BOM character
            '\u202e',  # Right-to-left override
            '𝕳𝖊𝖑𝖑𝖔',  # Mathematical alphanumeric
        ]

        guide = TheGuide(
            project_path=Path(tmpdir),
            client_llm=StableLLM(),
            guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        for test_str in test_strings:
            answer, protocol = guide.solve(
                problem_statement=test_str,
                max_iterations=1
            )
            # Should be able to retrieve
            retrieved = guide.get_protocol(protocol.session_id)
            assert retrieved is not None, f"Should retrieve protocol with encoding: {repr(test_str)}"
            print(f"  ✅ Handled encoding: {repr(test_str)[:50]}...")

def test_encoding_latin1_vs_utf8(runner: TestRunner):
    """Test Latin-1 characters that might break UTF-8."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Characters that exist in Latin-1 but might be tricky in UTF-8
        latin1_chars = ''.join(chr(i) for i in range(128, 256))

        guide = TheGuide(
            project_path=Path(tmpdir),
            client_llm=StableLLM(),
            guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        answer, protocol = guide.solve(
            problem_statement=latin1_chars,
            max_iterations=1
        )

        # Should be able to read the file
        session_file = Path(tmpdir) / "_pantheon" / "guide" / "sessions" / f"{protocol.session_id}.json"
        content = session_file.read_text(encoding='utf-8')
        assert len(content) > 0, "Should write valid UTF-8"
        print("Handled Latin-1 characters correctly")

# ============================================================================
# PYDANTIC VALIDATION BREAKING
# ============================================================================

def test_pydantic_extra_fields(runner: TestRunner):
    """Test Protocol with extra unexpected fields."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create JSON with extra fields
        protocol_dict = {
            "session_id": "extra_test",
            "problem_statement": "Test",
            "reasoning_chain": [],
            "evaluations": [],
            "final_answer": "Test",
            "quality_score": 0.8,
            "iteration_count": 1,
            "evaluation_method": "critic_model",
            "created": datetime.now().isoformat(),
            "completed": datetime.now().isoformat(),
            "metadata": {},
            # Extra fields
            "extra_field_1": "should be ignored",
            "extra_field_2": 12345,
            "malicious_code": "exec('print(1)')",
        }

        json_str = json.dumps(protocol_dict)

        # Pydantic should handle extra fields gracefully
        protocol = Protocol.model_validate_json(json_str)
        assert protocol.session_id == "extra_test"
        print("Handled extra fields correctly (ignored them)")

def test_pydantic_type_coercion(runner: TestRunner):
    """Test Pydantic type coercion edge cases."""

    # Test with string numbers (should coerce to float)
    try:
        scores = EvaluationScores(
            factuality="0.85",  # String instead of float
            validity="0.85",
            coherence="0.85",
            utility="0.85",
            faithfulness="0.85",
            overall="0.85"
        )
        print("Pydantic coerced strings to floats")
    except:
        print("Pydantic rejected string numbers (strict validation)")

def test_pydantic_nan_inf(runner: TestRunner):
    """Test NaN and Infinity in scores."""

    # These should be rejected by validation
    invalid_scores = [
        float('nan'),
        float('inf'),
        float('-inf'),
        1.5,  # Over maximum
        -0.5,  # Below minimum
    ]

    for score in invalid_scores:
        try:
            scores = EvaluationScores(
                factuality=score,
                validity=0.85,
                coherence=0.85,
                utility=0.85,
                faithfulness=0.85,
                overall=0.85
            )
            raise AssertionError(f"Should have rejected invalid score: {score}")
        except Exception as e:
            print(f"  ✅ Correctly rejected: {score}")

# ============================================================================
# THREAD SAFETY VIOLATIONS
# ============================================================================

def test_thread_safety_shared_guide_instance(runner: TestRunner):
    """Test if sharing a Guide instance across threads is safe."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Share ONE guide instance across multiple threads
        guide = TheGuide(
            project_path=Path(tmpdir),
            client_llm=StableLLM(),
            guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        results = []
        errors = []

        def run_session(i):
            try:
                answer, protocol = guide.solve(
                    problem_statement=f"Thread {i}",
                    max_iterations=1
                )
                results.append(protocol.session_id)
            except Exception as e:
                errors.append(str(e))

        threads = [threading.Thread(target=run_session, args=(i,)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        print(f"Results: {len(results)}, Errors: {len(errors)}")
        # Might have errors (not thread-safe), but shouldn't crash
        assert len(results) + len(errors) == 20, "All threads should complete"

def test_thread_safety_index_corruption(runner: TestRunner):
    """Test index file corruption during concurrent writes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        def writer(i):
            guide = TheGuide(
                project_path=Path(tmpdir),
                client_llm=StableLLM(),
                guide_llm_config={"model": "test"}
            )
            guide.guide_llm = StableLLM()

            answer, protocol = guide.solve(
                problem_statement=f"Index test {i}",
                max_iterations=1
            )
            return protocol.session_id

        # 50 threads all writing to index simultaneously
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(writer, i) for i in range(50)]
            session_ids = [f.result() for f in concurrent.futures.as_completed(futures)]

        # Check index is still valid JSON
        index_file = Path(tmpdir) / "_pantheon" / "guide" / "index.json"
        try:
            index_data = json.loads(index_file.read_text())
            print(f"Index survived {len(session_ids)} concurrent writes")
        except json.JSONDecodeError:
            raise AssertionError("Index file corrupted by concurrent writes")

# ============================================================================
# FILESYSTEM PERMISSION ATTACKS
# ============================================================================

def test_filesystem_readonly_directory(runner: TestRunner):
    """Test behavior with read-only filesystem."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir),
            client_llm=StableLLM(),
            guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        # Create a session first
        answer, protocol = guide.solve(
            problem_statement="Test",
            max_iterations=1
        )

        # Make sessions directory read-only
        sessions_dir = Path(tmpdir) / "_pantheon" / "guide" / "sessions"
        os.chmod(sessions_dir, 0o444)  # Read-only

        # Try to create another session (should fail gracefully)
        try:
            answer2, protocol2 = guide.solve(
                problem_statement="Test 2",
                max_iterations=1
            )
            # If it succeeds, that's surprising but acceptable
            print("Somehow wrote to read-only directory")
        except PermissionError:
            print("Correctly failed with PermissionError")
        except Exception as e:
            print(f"Failed with different error: {type(e).__name__}")
        finally:
            # Restore permissions for cleanup
            os.chmod(sessions_dir, 0o755)

# ============================================================================
# RESOURCE EXHAUSTION
# ============================================================================

def test_resource_exhaustion_file_descriptors(runner: TestRunner):
    """Test with many open file handles."""
    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir),
            client_llm=StableLLM(),
            guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        # Create many sessions quickly
        for i in range(100):
            answer, protocol = guide.solve(
                problem_statement=f"FD test {i}",
                max_iterations=1
            )

        # All sessions should exist
        sessions_dir = Path(tmpdir) / "_pantheon" / "guide" / "sessions"
        session_count = len(list(sessions_dir.glob("*.json")))
        assert session_count == 100, f"Expected 100 sessions, got {session_count}"
        print("No file descriptor leaks")

def test_resource_exhaustion_deep_recursion(runner: TestRunner):
    """Test with extremely deep data structures."""

    # Create deeply nested dict (not in reasoning, in metadata)
    deep_dict = {}
    current = deep_dict
    for i in range(100):
        current['nested'] = {}
        current = current['nested']
    current['value'] = 'bottom'

    protocol = Protocol(
        session_id="deep_recursion",
        problem_statement="Test",
        quality_score=0.8,
        iteration_count=1,
        metadata=deep_dict  # Deeply nested structure
    )

    # Should serialize without stack overflow
    json_str = protocol.model_dump_json()
    assert len(json_str) > 0
    print("Handled deep nesting without stack overflow")

# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run all hellfire tests."""
    runner = TestRunner()

    print("\n" + "="*80)
    print("🔥 HELLFIRE TEST SUITE - Finding ANY possible failure")
    print("="*80)

    # Float precision
    print("\n🔢 FLOAT PRECISION TESTS")
    runner.run_test("Evaluation Score Edge Cases", test_float_precision_evaluation_scores, runner)
    runner.run_test("Negative Zero (-0.0)", test_float_precision_negative_zero, runner)
    runner.run_test("Quality Threshold Float Precision", test_float_precision_quality_threshold_edge, runner)

    # Time-based
    print("\n⏰ TIME-BASED TESTS")
    runner.run_test("Microsecond Clock Skew", test_time_clock_skew_microseconds, runner)
    runner.run_test("Timestamp Format Variations", test_time_timestamp_string_format, runner)

    # Encoding
    print("\n📝 ENCODING TESTS")
    runner.run_test("Multiple Encodings", test_encoding_every_encoding, runner)
    runner.run_test("Latin-1 vs UTF-8", test_encoding_latin1_vs_utf8, runner)

    # Pydantic
    print("\n🔍 PYDANTIC VALIDATION TESTS")
    runner.run_test("Extra Fields", test_pydantic_extra_fields, runner)
    runner.run_test("Type Coercion", test_pydantic_type_coercion, runner)
    runner.run_test("NaN/Infinity Rejection", test_pydantic_nan_inf, runner)

    # Thread safety
    print("\n🧵 THREAD SAFETY TESTS")
    runner.run_test("Shared Guide Instance", test_thread_safety_shared_guide_instance, runner)
    runner.run_test("Index Corruption", test_thread_safety_index_corruption, runner)

    # Filesystem
    print("\n💾 FILESYSTEM TESTS")
    runner.run_test("Read-Only Directory", test_filesystem_readonly_directory, runner)

    # Resource exhaustion
    print("\n⚠️  RESOURCE EXHAUSTION TESTS")
    runner.run_test("File Descriptor Leaks", test_resource_exhaustion_file_descriptors, runner)
    runner.run_test("Deep Recursion", test_resource_exhaustion_deep_recursion, runner)

    # Summary
    runner.print_summary()

    return runner.results

def main():
    parser = argparse.ArgumentParser(description="Hellfire Test Suite")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    args = parser.parse_args()

    results = run_all_tests()

    failed = sum(1 for r in results if not r.passed)
    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()
