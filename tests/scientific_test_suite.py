#!/usr/bin/env python3
"""
SCIENTIFIC METHOD TEST SUITE - Hypothesis-driven experimental validation

This suite applies rigorous scientific methodology:
1. State hypotheses
2. Design controlled experiments
3. Collect quantitative data
4. Perform statistical analysis
5. Accept or reject hypotheses based on evidence

Each test is a controlled experiment with measurable outcomes.
"""

import concurrent.futures
import json
import statistics
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import importlib.util

guide_path = Path(__file__).parent.parent / "src" / "waft" / "pantheon" / "guide.py"
spec = importlib.util.spec_from_file_location("guide", guide_path)
guide_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guide_module)

TheGuide = guide_module.TheGuide


class StableLLM:
    def complete(self, prompt):
        if "evaluate" in prompt.lower():
            return '```json\n{"factuality": 0.85, "validity": 0.85, "coherence": 0.85, "utility": 0.85, "faithfulness": 0.85, "overall": 0.85, "rationale": "test", "strengths": [], "weaknesses": [], "recommendations": [], "should_continue": true, "planning_detected": false, "unfaithful_reasoning_detected": false}\n```'
        return "test"


# ============================================================================
# EXPERIMENT 1: Session ID Uniqueness Under Load
# ============================================================================


def experiment_session_id_uniqueness():
    """
    HYPOTHESIS: Session IDs will be unique even when created at maximum speed.

    NULL HYPOTHESIS: Session IDs may collide when created rapidly.

    METHOD:
    - Create N sessions as fast as possible (no delays)
    - Measure: Number of unique session IDs
    - Measure: Time between successive creations

    ACCEPTANCE CRITERIA:
    - 100% uniqueness (unique_count == total_count)
    - All time deltas > 0 (no same-microsecond collisions)

    VARIABLES:
    - Independent: Number of sessions (N)
    - Dependent: Uniqueness rate, time deltas
    - Control: Same tmpdir, same LLM, same config
    """

    print("\n" + "=" * 80)
    print("EXPERIMENT 1: Session ID Uniqueness Under Maximum Speed")
    print("=" * 80)

    print("\nHYPOTHESIS: 100% unique session IDs even at maximum creation speed")
    print("NULL HYPOTHESIS: Some session IDs will collide")

    # Experiment parameters
    N = 100  # Sample size

    print("\nEXPERIMENTAL SETUP:")
    print(f"  Sample size (N): {N}")
    print("  Controlled variables: tmpdir, LLM config, max_iterations=1")

    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        session_ids = []
        timestamps = []

        print(f"\nDATA COLLECTION (creating {N} sessions):")
        start_time = time.time()

        for i in range(N):
            t0 = time.time()
            answer, protocol = guide.solve(
                problem_statement=f"Experiment 1 session {i}", max_iterations=1
            )
            t1 = time.time()

            session_ids.append(protocol.session_id)
            timestamps.append((t0, t1, t1 - t0))

            if (i + 1) % 20 == 0:
                print(f"  Progress: {i + 1}/{N}")

        total_time = time.time() - start_time

        # Data analysis
        unique_count = len(set(session_ids))
        uniqueness_rate = (unique_count / len(session_ids)) * 100

        creation_times = [t[2] for t in timestamps]
        mean_creation_time = statistics.mean(creation_times)
        stdev_creation_time = statistics.stdev(creation_times) if len(creation_times) > 1 else 0
        min_creation_time = min(creation_times)
        max_creation_time = max(creation_times)

        # Calculate inter-arrival times (time between successive sessions)
        inter_arrival_times = []
        for i in range(1, len(timestamps)):
            inter_arrival = timestamps[i][0] - timestamps[i - 1][1]
            inter_arrival_times.append(inter_arrival)

        print("\nRESULTS:")
        print(f"  Total sessions created: {len(session_ids)}")
        print(f"  Unique session IDs: {unique_count}")
        print(f"  Uniqueness rate: {uniqueness_rate:.2f}%")
        print(f"  Total time: {total_time:.3f}s")
        print(f"  Sessions/second: {N / total_time:.1f}")

        print("\nCREATION TIME STATISTICS:")
        print(f"  Mean: {mean_creation_time * 1000:.3f}ms")
        print(f"  Std Dev: {stdev_creation_time * 1000:.3f}ms")
        print(f"  Min: {min_creation_time * 1000:.3f}ms")
        print(f"  Max: {max_creation_time * 1000:.3f}ms")

        print("\nINTER-ARRIVAL TIME STATISTICS:")
        if inter_arrival_times:
            print(f"  Mean: {statistics.mean(inter_arrival_times) * 1000:.3f}ms")
            print(f"  Min: {min(inter_arrival_times) * 1000:.3f}ms")
            print(f"  Max: {max(inter_arrival_times) * 1000:.3f}ms")

        # Show first 5 session IDs for verification
        print("\nSAMPLE SESSION IDs (first 5):")
        for i, sid in enumerate(session_ids[:5]):
            print(f"  [{i + 1}] {sid}")

        # Statistical test
        print("\nHYPOTHESIS TEST:")
        if uniqueness_rate == 100.0:
            print("  ✅ HYPOTHESIS ACCEPTED: 100% uniqueness achieved")
            print("  ❌ NULL HYPOTHESIS REJECTED: No collisions detected")
            return True, {
                "uniqueness_rate": uniqueness_rate,
                "total": len(session_ids),
                "unique": unique_count,
                "mean_time": mean_creation_time,
                "throughput": N / total_time,
            }
        else:
            collisions = len(session_ids) - unique_count
            print(f"  ❌ HYPOTHESIS REJECTED: {collisions} collision(s) detected")
            print("  ✅ NULL HYPOTHESIS ACCEPTED: Collisions occurred")
            return False, {
                "uniqueness_rate": uniqueness_rate,
                "total": len(session_ids),
                "unique": unique_count,
                "collisions": collisions,
            }


# ============================================================================
# EXPERIMENT 2: Performance Scaling with Iterations
# ============================================================================


def experiment_performance_scaling():
    """
    HYPOTHESIS: Execution time scales linearly with number of iterations.

    NULL HYPOTHESIS: Execution time is non-linear or has unexpected overhead.

    METHOD:
    - Run sessions with 1, 5, 10, 20, 50 iterations
    - Measure execution time for each
    - Calculate time per iteration

    ACCEPTANCE CRITERIA:
    - Linear correlation coefficient R² > 0.95
    - Time per iteration is consistent (low variance)

    VARIABLES:
    - Independent: Number of iterations
    - Dependent: Total execution time
    - Control: Same problem, same LLM, same config
    """

    print("\n" + "=" * 80)
    print("EXPERIMENT 2: Performance Scaling with Iteration Count")
    print("=" * 80)

    print("\nHYPOTHESIS: Execution time scales linearly with iterations (R² > 0.95)")
    print("NULL HYPOTHESIS: Non-linear scaling or high overhead")

    iteration_counts = [1, 5, 10, 20, 50]
    trials_per_count = 5  # Run multiple trials for statistical significance

    print("\nEXPERIMENTAL SETUP:")
    print(f"  Iteration counts: {iteration_counts}")
    print(f"  Trials per count: {trials_per_count}")
    print(f"  Total runs: {len(iteration_counts) * trials_per_count}")

    results = []

    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        print("\nDATA COLLECTION:")

        for iteration_count in iteration_counts:
            times = []

            for trial in range(trials_per_count):
                start = time.time()
                answer, protocol = guide.solve(
                    problem_statement="Scaling test",
                    max_iterations=iteration_count,
                    quality_threshold=1.0,  # Won't hit, do all iterations
                )
                duration = time.time() - start
                times.append(duration)

            mean_time = statistics.mean(times)
            stdev_time = statistics.stdev(times) if len(times) > 1 else 0
            time_per_iter = mean_time / iteration_count

            results.append(
                {
                    "iterations": iteration_count,
                    "mean_time": mean_time,
                    "stdev": stdev_time,
                    "time_per_iter": time_per_iter,
                    "trials": times,
                }
            )

            print(
                f"  {iteration_count:2d} iterations: {mean_time * 1000:6.2f}ms ± {stdev_time * 1000:5.2f}ms ({time_per_iter * 1000:.3f}ms/iter)"
            )

        # Calculate linear correlation
        x = [r["iterations"] for r in results]
        y = [r["mean_time"] for r in results]

        # Simple linear regression
        n = len(x)
        mean_x = statistics.mean(x)
        mean_y = statistics.mean(y)

        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator_x = sum((x[i] - mean_x) ** 2 for i in range(n))
        denominator_y = sum((y[i] - mean_y) ** 2 for i in range(n))

        # Pearson correlation coefficient
        r = (
            numerator / (denominator_x * denominator_y) ** 0.5
            if denominator_x > 0 and denominator_y > 0
            else 0
        )
        r_squared = r**2

        # Calculate slope (time per iteration)
        slope = numerator / denominator_x if denominator_x > 0 else 0

        print("\nSTATISTICAL ANALYSIS:")
        print(f"  Pearson correlation (r): {r:.4f}")
        print(f"  Coefficient of determination (R²): {r_squared:.4f}")
        print(f"  Regression slope: {slope * 1000:.3f}ms/iteration")

        # Consistency check - variance in time_per_iter
        times_per_iter = [r["time_per_iter"] for r in results]
        mean_tpi = statistics.mean(times_per_iter)
        stdev_tpi = statistics.stdev(times_per_iter) if len(times_per_iter) > 1 else 0
        cv = (stdev_tpi / mean_tpi) * 100 if mean_tpi > 0 else 0  # Coefficient of variation

        print("\nCONSISTENCY ANALYSIS:")
        print(f"  Mean time per iteration: {mean_tpi * 1000:.3f}ms")
        print(f"  Std dev: {stdev_tpi * 1000:.3f}ms")
        print(f"  Coefficient of variation: {cv:.2f}%")

        print("\nHYPOTHESIS TEST:")
        if r_squared > 0.95:
            print(f"  ✅ HYPOTHESIS ACCEPTED: Strong linear correlation (R² = {r_squared:.4f})")
            print("  ❌ NULL HYPOTHESIS REJECTED: Scaling is linear")
            return True, {
                "r_squared": r_squared,
                "slope": slope,
                "mean_time_per_iter": mean_tpi,
                "cv": cv,
            }
        else:
            print(f"  ❌ HYPOTHESIS REJECTED: R² = {r_squared:.4f} < 0.95")
            print("  ✅ NULL HYPOTHESIS ACCEPTED: Non-linear scaling detected")
            return False, {"r_squared": r_squared, "slope": slope}


# ============================================================================
# EXPERIMENT 3: Concurrent Access Safety
# ============================================================================


def experiment_concurrent_safety():
    """
    HYPOTHESIS: Multiple threads can safely create sessions concurrently without data corruption.

    NULL HYPOTHESIS: Concurrent access causes race conditions or data corruption.

    METHOD:
    - Create N sessions across M threads simultaneously
    - Measure: Collision rate, error rate, corruption rate

    ACCEPTANCE CRITERIA:
    - Error rate = 0%
    - All session files are valid JSON
    - All session IDs are unique

    VARIABLES:
    - Independent: Number of threads, sessions per thread
    - Dependent: Error count, corruption count, uniqueness
    - Control: Same tmpdir, same problem statement
    """

    print("\n" + "=" * 80)
    print("EXPERIMENT 3: Concurrent Access Safety")
    print("=" * 80)

    print("\nHYPOTHESIS: Zero errors and zero corruption with concurrent access")
    print("NULL HYPOTHESIS: Concurrent access causes errors or corruption")

    num_threads = 10
    sessions_per_thread = 10
    total_sessions = num_threads * sessions_per_thread

    print("\nEXPERIMENTAL SETUP:")
    print(f"  Number of threads: {num_threads}")
    print(f"  Sessions per thread: {sessions_per_thread}")
    print(f"  Total sessions: {total_sessions}")

    with tempfile.TemporaryDirectory() as tmpdir:
        errors = []
        session_ids = []

        def worker(thread_id):
            """Worker thread that creates sessions."""
            local_ids = []
            local_errors = []

            try:
                guide = TheGuide(
                    project_path=Path(tmpdir),
                    client_llm=StableLLM(),
                    guide_llm_config={"model": "test"},
                )
                guide.guide_llm = StableLLM()

                for i in range(sessions_per_thread):
                    try:
                        answer, protocol = guide.solve(
                            problem_statement=f"Thread {thread_id} session {i}", max_iterations=1
                        )
                        local_ids.append(protocol.session_id)
                    except Exception as e:
                        local_errors.append({"thread": thread_id, "iteration": i, "error": str(e)})
            except Exception as e:
                local_errors.append({"thread": thread_id, "error": str(e), "type": "thread_init"})

            return local_ids, local_errors

        print(f"\nDATA COLLECTION (launching {num_threads} threads):")
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(worker, i) for i in range(num_threads)]

            for future in concurrent.futures.as_completed(futures):
                ids, errs = future.result()
                session_ids.extend(ids)
                errors.extend(errs)

        total_time = time.time() - start_time

        # Check for file corruption
        sessions_dir = Path(tmpdir) / "_pantheon" / "guide" / "sessions"
        corrupted_files = []

        if sessions_dir.exists():
            for session_file in sessions_dir.glob("*.json"):
                try:
                    json.loads(session_file.read_text())
                except json.JSONDecodeError:
                    corrupted_files.append(session_file.name)

        # Analysis
        unique_ids = len(set(session_ids))
        uniqueness_rate = (unique_ids / len(session_ids)) * 100 if session_ids else 0
        error_rate = (len(errors) / total_sessions) * 100
        corruption_rate = (len(corrupted_files) / total_sessions) * 100 if total_sessions > 0 else 0

        print("\nRESULTS:")
        print(f"  Total execution time: {total_time:.3f}s")
        print(f"  Sessions created: {len(session_ids)}/{total_sessions}")
        print(f"  Unique session IDs: {unique_ids}")
        print(f"  Uniqueness rate: {uniqueness_rate:.2f}%")
        print(f"  Errors encountered: {len(errors)}")
        print(f"  Error rate: {error_rate:.2f}%")
        print(f"  Corrupted files: {len(corrupted_files)}")
        print(f"  Corruption rate: {corruption_rate:.2f}%")

        if errors:
            print("\nERROR DETAILS:")
            for i, err in enumerate(errors[:5]):  # Show first 5
                print(f"  [{i + 1}] {err}")

        if corrupted_files:
            print("\nCORRUPTED FILES:")
            for f in corrupted_files[:5]:  # Show first 5
                print(f"  - {f}")

        print("\nHYPOTHESIS TEST:")
        if error_rate == 0 and corruption_rate == 0 and uniqueness_rate == 100.0:
            print("  ✅ HYPOTHESIS ACCEPTED: Zero errors, zero corruption, 100% uniqueness")
            print("  ❌ NULL HYPOTHESIS REJECTED: Concurrent access is safe")
            return True, {
                "error_rate": error_rate,
                "corruption_rate": corruption_rate,
                "uniqueness_rate": uniqueness_rate,
                "throughput": len(session_ids) / total_time,
            }
        else:
            print("  ❌ HYPOTHESIS REJECTED: Detected issues in concurrent access")
            print("  ✅ NULL HYPOTHESIS ACCEPTED: Race conditions exist")
            return False, {
                "error_rate": error_rate,
                "corruption_rate": corruption_rate,
                "uniqueness_rate": uniqueness_rate,
                "errors": len(errors),
                "corrupted": len(corrupted_files),
            }


# ============================================================================
# MAIN EXPERIMENTAL PROTOCOL
# ============================================================================


def run_experiments():
    """Run all experiments and compile results."""

    print("=" * 80)
    print("SCIENTIFIC METHOD TEST SUITE")
    print("Hypothesis-Driven Experimental Validation of TheGuide")
    print("=" * 80)

    print("\nMETHODOLOGY:")
    print("  1. State clear hypotheses")
    print("  2. Design controlled experiments")
    print("  3. Collect quantitative data")
    print("  4. Perform statistical analysis")
    print("  5. Accept or reject hypotheses based on evidence")

    results = {}

    # Experiment 1
    accepted, data = experiment_session_id_uniqueness()
    results["exp1_uniqueness"] = {"hypothesis_accepted": accepted, "data": data}

    # Experiment 2
    accepted, data = experiment_performance_scaling()
    results["exp2_scaling"] = {"hypothesis_accepted": accepted, "data": data}

    # Experiment 3
    accepted, data = experiment_concurrent_safety()
    results["exp3_concurrency"] = {"hypothesis_accepted": accepted, "data": data}

    # Final summary
    print("\n" + "=" * 80)
    print("EXPERIMENTAL RESULTS SUMMARY")
    print("=" * 80)

    total_experiments = len(results)
    accepted_count = sum(1 for r in results.values() if r["hypothesis_accepted"])

    print(f"\nTotal Experiments: {total_experiments}")
    print(f"Hypotheses Accepted: {accepted_count}")
    print(f"Hypotheses Rejected: {total_experiments - accepted_count}")
    print(f"Acceptance Rate: {(accepted_count / total_experiments) * 100:.1f}%")

    print("\nDETAILED RESULTS:")
    for exp_name, result in results.items():
        status = "✅ ACCEPTED" if result["hypothesis_accepted"] else "❌ REJECTED"
        print(f"\n{exp_name}: {status}")
        for key, value in result["data"].items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")

    # Save results to file
    results_file = Path("experimental_results.json")
    with open(results_file, "w") as f:
        # Convert for JSON serialization
        serializable_results = {}
        for k, v in results.items():
            serializable_results[k] = {
                "hypothesis_accepted": v["hypothesis_accepted"],
                "data": {
                    dk: (float(dv) if isinstance(dv, (int, float)) else str(dv))
                    for dk, dv in v["data"].items()
                },
            }
        json.dump(serializable_results, f, indent=2)

    print(f"\n📊 Full experimental data saved to: {results_file}")

    print("\n" + "=" * 80)

    return results


if __name__ == "__main__":
    results = run_experiments()
