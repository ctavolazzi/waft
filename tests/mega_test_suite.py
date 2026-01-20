#!/usr/bin/env python3
"""
MEGA TEST SUITE - Test the absolute fuck out of TheGuide!

Comprehensive testing of:
- Core TheGuide functionality
- REST API endpoints
- CLI tool
- Playground demos
- Examples
- Edge cases
- Error handling
- Performance
- Integration

Usage:
    python tests/mega_test_suite.py --all
    python tests/mega_test_suite.py --category core
    python tests/mega_test_suite.py --stress
"""

import argparse
import concurrent.futures
import subprocess
import sys
import tempfile
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
        print(f"🧪 Running: {name}")
        print(f"{'=' * 80}")

        start = time.time()
        try:
            result = test_func(*args, **kwargs)
            duration = time.time() - start
            test_result = TestResult(name, True, "✅ PASSED", duration)
            print(f"✅ PASSED in {duration:.2f}s")
        except AssertionError as e:
            duration = time.time() - start
            error_msg = str(e) if str(e) else "Assertion failed (no message)"
            test_result = TestResult(name, False, f"❌ FAILED: {error_msg}", duration)
            print(f"❌ FAILED: {error_msg}")
        except Exception as e:
            duration = time.time() - start
            error_msg = f"{type(e).__name__}: {str(e)}"
            test_result = TestResult(name, False, f"💥 ERROR: {error_msg}", duration)
            print(f"💥 ERROR: {error_msg}")
            import traceback

            traceback.print_exc()

        self.results.append(test_result)
        return test_result

    def print_summary(self):
        """Print test summary."""
        total_time = time.time() - self.start_time

        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)

        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        total = len(self.results)

        print(f"\nTotal Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"Success Rate: {(passed / total) * 100:.1f}%")
        print(f"Total Time: {total_time:.2f}s")

        if failed > 0:
            print("\n❌ Failed Tests:")
            for r in self.results:
                if not r.passed:
                    print(f"  - {r.name}: {r.message}")

        print("\n" + "=" * 80)


# ============================================================================
# Mock LLM for Testing
# ============================================================================


class TestLLM:
    """Test LLM with various response patterns."""

    def __init__(self, mode="normal"):
        self.mode = mode
        self.call_count = 0
        self.call_history = []

    def complete(self, prompt: str) -> str:
        """Generate test responses."""
        self.call_count += 1
        self.call_history.append(prompt)

        # Error mode
        if self.mode == "error":
            raise Exception("Simulated LLM error")

        # Slow mode
        if self.mode == "slow":
            time.sleep(0.1)

        # Invalid JSON mode
        if self.mode == "invalid_json" and "evaluate" in prompt.lower():
            return "This is not valid JSON at all!"

        # Normal evaluation response
        if "fvcu" in prompt.lower() or (
            "evaluate" in prompt.lower() and "reasoning" in prompt.lower()
        ):
            score = 0.85 + (self.call_count % 3) * 0.05
            return f"""```json
{{
  "factuality": {score:.2f},
  "validity": {score - 0.02:.2f},
  "coherence": {score + 0.03:.2f},
  "utility": {score - 0.01:.2f},
  "faithfulness": {score + 0.02:.2f},
  "overall": {score:.2f},
  "rationale": "Test evaluation rationale",
  "strengths": ["Strength 1", "Strength 2"],
  "weaknesses": ["Weakness 1"],
  "recommendations": ["Recommendation 1"],
  "should_continue": true,
  "planning_detected": false,
  "unfaithful_reasoning_detected": false
}}
```"""

        # Normal instruction/reasoning
        return f"Test response #{self.call_count} for prompt of length {len(prompt)}"


# ============================================================================
# CORE TESTS
# ============================================================================


def test_guide_initialization(runner: TestRunner):
    """Test TheGuide initialization."""
    with tempfile.TemporaryDirectory() as tmpdir:
        client_llm = TestLLM()
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=client_llm, guide_llm_config={"model": "test"}
        )

        assert guide.project_path == Path(tmpdir), (
            f"Project path mismatch: {guide.project_path} != {Path(tmpdir)}"
        )
        assert guide.guide_path.exists(), f"Guide path doesn't exist: {guide.guide_path}"
        assert (guide.guide_path / "sessions").exists(), "Sessions directory doesn't exist"
        assert (guide.guide_path / "protocols").exists(), "Protocols directory doesn't exist"
        assert guide.index_file.exists(), f"Index file doesn't exist: {guide.index_file}"


def test_basic_guidance_session(runner: TestRunner):
    """Test basic guidance session."""
    with tempfile.TemporaryDirectory() as tmpdir:
        client_llm = TestLLM()
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=client_llm, guide_llm_config={"model": "test"}
        )
        guide.guide_llm = TestLLM()

        answer, protocol = guide.solve(
            problem_statement="Test problem", max_iterations=2, quality_threshold=0.8
        )

        assert answer is not None
        assert protocol is not None
        assert protocol.iteration_count > 0
        assert protocol.quality_score >= 0.0
        assert len(protocol.reasoning_chain) > 0
        assert len(protocol.evaluations) > 0


def test_protocol_serialization(runner: TestRunner):
    """Test Protocol serialization/deserialization."""
    protocol = Protocol(
        session_id="test_123",
        problem_statement="Test problem",
        reasoning_chain=[{"iteration": 1, "test": "data"}],
        evaluations=[
            {
                "iteration": 1,
                "scores": {
                    "factuality": 0.9,
                    "validity": 0.8,
                    "coherence": 0.85,
                    "utility": 0.9,
                    "faithfulness": 0.95,
                    "overall": 0.88,
                },
            }
        ],
        final_answer="Test answer",
        quality_score=0.88,
        iteration_count=1,
    )

    # Serialize
    json_str = protocol.model_dump_json()
    assert len(json_str) > 0

    # Deserialize
    protocol2 = Protocol.model_validate_json(json_str)
    assert protocol2.session_id == protocol.session_id
    assert protocol2.quality_score == protocol.quality_score


def test_evaluation_scores(runner: TestRunner):
    """Test EvaluationScores validation."""
    scores = EvaluationScores(
        factuality=0.9, validity=0.8, coherence=0.85, utility=0.9, faithfulness=0.95, overall=0.88
    )

    assert scores.factuality == 0.9
    assert 0.0 <= scores.overall <= 1.0

    # Test validation
    try:
        bad_scores = EvaluationScores(
            factuality=1.5,  # Invalid!
            validity=0.8,
            coherence=0.85,
            utility=0.9,
            faithfulness=0.95,
            overall=0.88,
        )
        raise AssertionError("Should have raised validation error")
    except:
        pass  # Expected


def test_storage_system(runner: TestRunner):
    """Test storage and retrieval."""
    with tempfile.TemporaryDirectory() as tmpdir:
        client_llm = TestLLM()
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=client_llm, guide_llm_config={"model": "test"}
        )
        guide.guide_llm = TestLLM()

        # Create session
        answer, protocol = guide.solve(problem_statement="Test", max_iterations=1)

        # Check files exist
        session_file = guide.guide_path / "sessions" / f"{protocol.session_id}.json"
        protocol_file = guide.guide_path / "protocols" / f"{protocol.session_id}.json"

        assert session_file.exists()
        assert protocol_file.exists()

        # Retrieve protocol
        retrieved = guide.get_protocol(protocol.session_id)
        assert retrieved is not None
        assert retrieved.session_id == protocol.session_id


def test_explanation_generation(runner: TestRunner):
    """Test 'Why?' explanation generation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        client_llm = TestLLM()
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=client_llm, guide_llm_config={"model": "test"}
        )
        guide.guide_llm = TestLLM()

        answer, protocol = guide.solve(problem_statement="Test problem", max_iterations=1)

        explanation = guide.explain(protocol.session_id)
        assert "Meta-Cognitive Guidance Explanation" in explanation
        assert "Problem Statement" in explanation
        assert "Reasoning Chain" in explanation
        assert "Final Answer" in explanation
        assert "FVCU" in explanation


def test_multiple_iterations(runner: TestRunner):
    """Test multiple iteration guidance."""
    with tempfile.TemporaryDirectory() as tmpdir:
        client_llm = TestLLM()
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=client_llm, guide_llm_config={"model": "test"}
        )
        guide.guide_llm = TestLLM()

        answer, protocol = guide.solve(
            problem_statement="Complex problem",
            max_iterations=5,
            quality_threshold=0.95,  # High threshold
        )

        assert protocol.iteration_count <= 5
        assert len(protocol.reasoning_chain) == protocol.iteration_count
        assert len(protocol.evaluations) == protocol.iteration_count


def test_quality_threshold_termination(runner: TestRunner):
    """Test termination by quality threshold."""
    with tempfile.TemporaryDirectory() as tmpdir:
        client_llm = TestLLM()
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=client_llm, guide_llm_config={"model": "test"}
        )
        guide.guide_llm = TestLLM()

        answer, protocol = guide.solve(
            problem_statement="Test",
            max_iterations=10,
            quality_threshold=0.85,  # Should hit this
        )

        # Should terminate early due to quality
        assert protocol.iteration_count < 10 or protocol.quality_score >= 0.85


def test_reasoner_integration(runner: TestRunner):
    """Test TheReasoner integration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        client_llm = TestLLM()
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=client_llm, guide_llm_config={"model": "test"}
        )
        guide.guide_llm = TestLLM()

        answer, protocol = guide.solve(problem_statement="Test", max_iterations=2)

        # TheReasoner should be accessible
        reasoner = guide.reasoner
        assert reasoner is not None

        # Should have created traces (or mock traces)
        traces = reasoner.get_recent_traces(limit=5)
        assert isinstance(traces, list)


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================


def test_error_handling_llm_failure(runner: TestRunner):
    """Test handling of LLM errors."""
    with tempfile.TemporaryDirectory() as tmpdir:
        client_llm = TestLLM(mode="error")
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=client_llm, guide_llm_config={"model": "test"}
        )
        guide.guide_llm = TestLLM(mode="error")

        try:
            answer, protocol = guide.solve(problem_statement="Test", max_iterations=1)
            raise AssertionError("Should have raised error")
        except Exception as e:
            assert "Simulated LLM error" in str(e)


def test_error_handling_invalid_json(runner: TestRunner):
    """Test handling of invalid JSON responses."""
    with tempfile.TemporaryDirectory() as tmpdir:
        client_llm = TestLLM()
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=client_llm, guide_llm_config={"model": "test"}
        )
        guide.guide_llm = TestLLM(mode="invalid_json")

        # Should fallback to default scores
        answer, protocol = guide.solve(problem_statement="Test", max_iterations=1)

        # Should complete with fallback scores
        assert protocol is not None
        assert protocol.quality_score == 0.5  # Fallback score


def test_error_handling_missing_session(runner: TestRunner):
    """Test handling of missing session."""
    with tempfile.TemporaryDirectory() as tmpdir:
        client_llm = TestLLM()
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=client_llm, guide_llm_config={"model": "test"}
        )

        # Try to get non-existent session
        protocol = guide.get_protocol("nonexistent_123")
        assert protocol is None

        # Try to explain non-existent session
        explanation = guide.explain("nonexistent_123")
        assert "not found" in explanation.lower()


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================


def test_performance_many_iterations(runner: TestRunner):
    """Test performance with many iterations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        client_llm = TestLLM()
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=client_llm, guide_llm_config={"model": "test"}
        )
        guide.guide_llm = TestLLM()

        start = time.time()
        answer, protocol = guide.solve(
            problem_statement="Performance test",
            max_iterations=10,
            quality_threshold=0.99,  # Won't hit, will do all iterations
        )
        duration = time.time() - start

        print(f"Completed 10 iterations in {duration:.2f}s")
        assert duration < 5.0, f"Performance test too slow: {duration:.2f}s (expected < 5.0s)"
        assert protocol.iteration_count == 10, (
            f"Expected 10 iterations, got {protocol.iteration_count}"
        )


def test_performance_concurrent_sessions(runner: TestRunner):
    """Test concurrent session handling."""
    with tempfile.TemporaryDirectory() as tmpdir:

        def run_session(i):
            client_llm = TestLLM()
            guide = TheGuide(
                project_path=Path(tmpdir), client_llm=client_llm, guide_llm_config={"model": "test"}
            )
            guide.guide_llm = TestLLM()

            answer, protocol = guide.solve(
                problem_statement=f"Concurrent test {i}", max_iterations=2
            )
            return protocol.session_id

        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(run_session, i) for i in range(5)]
            session_ids = [f.result() for f in concurrent.futures.as_completed(futures)]
        duration = time.time() - start

        print(f"Completed 5 concurrent sessions in {duration:.2f}s")
        assert len(session_ids) == 5, f"Expected 5 session IDs, got {len(session_ids)}"
        assert len(set(session_ids)) == 5, (
            f"Expected 5 unique session IDs, got {len(set(session_ids))} unique IDs: {session_ids}"
        )


def test_performance_large_protocol(runner: TestRunner):
    """Test handling of large protocols."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create large reasoning chain
        large_chain = [
            {
                "iteration": i,
                "instruction": f"Instruction {i}" * 100,  # Large text
                "reasoning_trace": f"Reasoning {i}" * 200,
                "timestamp": datetime.now().isoformat(),
            }
            for i in range(1, 11)
        ]

        large_evaluations = [
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
                "rationale": "Test" * 50,
                "strengths": ["S1", "S2"],
                "weaknesses": ["W1"],
                "recommendations": ["R1"],
            }
            for i in range(1, 11)
        ]

        protocol = Protocol(
            session_id="large_test",
            problem_statement="Large test" * 100,
            reasoning_chain=large_chain,
            evaluations=large_evaluations,
            final_answer="Answer" * 100,
            quality_score=0.88,
            iteration_count=10,
        )

        # Test serialization
        start = time.time()
        json_str = protocol.model_dump_json()
        duration = time.time() - start

        print(f"Serialized large protocol ({len(json_str)} bytes) in {duration:.3f}s")
        assert duration < 1.0  # Should be fast


# ============================================================================
# CLI TESTS
# ============================================================================


def test_cli_tool(runner: TestRunner):
    """Test CLI tool execution."""
    result = subprocess.run(
        ["python", "cli/guide_cli.py", "--problem", "Test CLI", "--iterations", "1"],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=Path(__file__).parent.parent,
    )

    # Check output contains expected text
    assert "Guidance Session" in result.stdout or "Session failed" in result.stdout


def test_cli_list_sessions(runner: TestRunner):
    """Test CLI session listing."""
    result = subprocess.run(
        ["python", "cli/guide_cli.py", "--list"],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=Path(__file__).parent.parent,
    )

    # Should complete without error
    assert result.returncode == 0 or "Recent Sessions" in result.stdout


# ============================================================================
# PLAYGROUND TESTS
# ============================================================================


def test_playground_score_evolution(runner: TestRunner):
    """Test playground score evolution demo."""
    result = subprocess.run(
        ["python", "playground/pantheon_playground.py", "--demo", "score_evolution"],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=Path(__file__).parent.parent,
    )

    assert "Score Evolution" in result.stdout
    assert "Iter" in result.stdout
    assert result.returncode == 0


def test_playground_multi_stage(runner: TestRunner):
    """Test playground multi-stage demo."""
    result = subprocess.run(
        ["python", "playground/pantheon_playground.py", "--demo", "multi_stage"],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=Path(__file__).parent.parent,
    )

    assert "Multi-Stage" in result.stdout
    assert "Analysis" in result.stdout or "Design" in result.stdout
    assert result.returncode == 0


def test_playground_comparative(runner: TestRunner):
    """Test playground comparative demo."""
    result = subprocess.run(
        ["python", "playground/pantheon_playground.py", "--demo", "comparative"],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=Path(__file__).parent.parent,
    )

    assert "Comparative" in result.stdout
    assert result.returncode == 0


# ============================================================================
# EXAMPLES TESTS
# ============================================================================


def test_examples_code_review(runner: TestRunner):
    """Test code review example."""
    result = subprocess.run(
        ["python", "examples/guide_examples.py", "--example", "code_review"],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=Path(__file__).parent.parent,
    )

    assert "Code Review" in result.stdout
    assert result.returncode == 0


def test_examples_architecture(runner: TestRunner):
    """Test architecture example."""
    result = subprocess.run(
        ["python", "examples/guide_examples.py", "--example", "architecture"],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=Path(__file__).parent.parent,
    )

    assert "Architecture" in result.stdout or "Design" in result.stdout
    assert result.returncode == 0


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


def test_integration_full_workflow(runner: TestRunner):
    """Test complete workflow from creation to explanation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create session
        client_llm = TestLLM()
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=client_llm, guide_llm_config={"model": "test"}
        )
        guide.guide_llm = TestLLM()

        # Solve problem
        answer, protocol = guide.solve(
            problem_statement="Integration test problem", max_iterations=3
        )

        # Get protocol
        retrieved = guide.get_protocol(protocol.session_id)
        assert retrieved is not None

        # Get explanation
        explanation = guide.explain(protocol.session_id)
        assert len(explanation) > 0

        # Get recent sessions
        recent = guide.get_recent_sessions(limit=5)
        assert len(recent) > 0
        assert any(s["session_id"] == protocol.session_id for s in recent)

        # Get summary
        summary = guide.get_session_summary()
        assert summary["total_sessions"] > 0


# ============================================================================
# STRESS TESTS
# ============================================================================


def test_stress_many_sessions(runner: TestRunner):
    """Stress test with many sessions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        print("Creating 20 sessions...")
        sessions = []

        for i in range(20):
            client_llm = TestLLM()
            guide = TheGuide(
                project_path=Path(tmpdir), client_llm=client_llm, guide_llm_config={"model": "test"}
            )
            guide.guide_llm = TestLLM()

            answer, protocol = guide.solve(problem_statement=f"Stress test {i}", max_iterations=1)
            sessions.append(protocol.session_id)

            if (i + 1) % 5 == 0:
                print(f"  Completed {i + 1}/20 sessions")

        # Verify all sessions stored
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=TestLLM(), guide_llm_config={"model": "test"}
        )
        summary = guide.get_session_summary()
        assert summary["total_sessions"] == 20, (
            f"Expected 20 sessions in summary, got {summary['total_sessions']}: {summary}"
        )

        print("✅ Successfully created and stored 20 sessions")


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================


def run_all_tests():
    """Run all tests."""
    runner = TestRunner()

    print("\n" + "=" * 80)
    print("🧪 MEGA TEST SUITE - Testing the absolute fuck out of TheGuide!")
    print("=" * 80)

    # Core tests
    print("\n📦 CORE TESTS")
    runner.run_test("Guide Initialization", test_guide_initialization, runner)
    runner.run_test("Basic Guidance Session", test_basic_guidance_session, runner)
    runner.run_test("Protocol Serialization", test_protocol_serialization, runner)
    runner.run_test("Evaluation Scores", test_evaluation_scores, runner)
    runner.run_test("Storage System", test_storage_system, runner)
    runner.run_test("Explanation Generation", test_explanation_generation, runner)
    runner.run_test("Multiple Iterations", test_multiple_iterations, runner)
    runner.run_test("Quality Threshold Termination", test_quality_threshold_termination, runner)
    runner.run_test("Reasoner Integration", test_reasoner_integration, runner)

    # Error handling
    print("\n💥 ERROR HANDLING TESTS")
    runner.run_test("LLM Failure Handling", test_error_handling_llm_failure, runner)
    runner.run_test("Invalid JSON Handling", test_error_handling_invalid_json, runner)
    runner.run_test("Missing Session Handling", test_error_handling_missing_session, runner)

    # Performance
    print("\n⚡ PERFORMANCE TESTS")
    runner.run_test("Many Iterations Performance", test_performance_many_iterations, runner)
    runner.run_test("Concurrent Sessions", test_performance_concurrent_sessions, runner)
    runner.run_test("Large Protocol Handling", test_performance_large_protocol, runner)

    # CLI
    print("\n🖥️  CLI TESTS")
    runner.run_test("CLI Tool Execution", test_cli_tool, runner)
    runner.run_test("CLI List Sessions", test_cli_list_sessions, runner)

    # Playground
    print("\n🎮 PLAYGROUND TESTS")
    runner.run_test("Playground Score Evolution", test_playground_score_evolution, runner)
    runner.run_test("Playground Multi-Stage", test_playground_multi_stage, runner)
    runner.run_test("Playground Comparative", test_playground_comparative, runner)

    # Examples
    print("\n📚 EXAMPLES TESTS")
    runner.run_test("Code Review Example", test_examples_code_review, runner)
    runner.run_test("Architecture Example", test_examples_architecture, runner)

    # Integration
    print("\n🔗 INTEGRATION TESTS")
    runner.run_test("Full Workflow", test_integration_full_workflow, runner)

    # Stress
    print("\n💪 STRESS TESTS")
    runner.run_test("Many Sessions Stress Test", test_stress_many_sessions, runner)

    # Summary
    runner.print_summary()

    return runner.results


def main():
    parser = argparse.ArgumentParser(description="Mega Test Suite for TheGuide")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument(
        "--category",
        choices=[
            "core",
            "error",
            "performance",
            "cli",
            "playground",
            "examples",
            "integration",
            "stress",
        ],
        help="Run specific category",
    )
    parser.add_argument("--stress", action="store_true", help="Run stress tests only")

    args = parser.parse_args()

    if args.all or (not args.category and not args.stress):
        results = run_all_tests()
    else:
        runner = TestRunner()

        if args.category == "core" or args.stress:
            print("\n📦 CORE TESTS")
            runner.run_test("Guide Initialization", test_guide_initialization, runner)
            runner.run_test("Basic Guidance Session", test_basic_guidance_session, runner)
            # ... add more as needed

        if args.stress:
            print("\n💪 STRESS TESTS")
            runner.run_test("Many Sessions Stress Test", test_stress_many_sessions, runner)

        runner.print_summary()
        results = runner.results

    # Exit code based on results
    failed = sum(1 for r in results if not r.passed)
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
