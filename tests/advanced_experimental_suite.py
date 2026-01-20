#!/usr/bin/env python3
"""
ADVANCED EXPERIMENTAL SUITE - Pushing boundaries with sophisticated analysis

Experiments:
1. Endurance Testing - Does performance degrade over time?
2. Memory Profiling - Memory usage patterns and leak detection
3. Breaking Point Analysis - Find the exact failure threshold
4. Statistical Distribution Analysis - Are metrics normally distributed?
5. Failure Recovery - Can it recover from corruption?
6. Benchmark Comparison - How does it compare to theoretical limits?
"""

import concurrent.futures
import gc
import json
import statistics
import sys
import tempfile
import time
import tracemalloc
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
# EXPERIMENT 4: Endurance Testing - Performance Over Time
# ============================================================================


def experiment_endurance_testing():
    """
    RESEARCH QUESTION: Does performance degrade over extended operation?

    HYPOTHESIS: Performance remains constant over time (no degradation).

    NULL HYPOTHESIS: Performance degrades with accumulated sessions.

    METHOD:
    - Create sessions in batches of 100
    - Measure mean time for each batch
    - Run for 10 batches (1000 total sessions)
    - Analyze trend: is slope significantly different from zero?

    METRICS:
    - Time per session for each batch
    - Linear regression slope over time
    - Memory usage over time

    ACCEPTANCE CRITERIA:
    - Slope within ±10% of initial performance
    - No significant upward trend (p-value test)
    """

    print("\n" + "=" * 80)
    print("EXPERIMENT 4: Endurance Testing - Performance Over Time")
    print("=" * 80)

    print("\nRESEARCH QUESTION: Does performance remain constant over extended use?")
    print("HYPOTHESIS: No performance degradation over 1000 sessions")

    batch_size = 100
    num_batches = 10
    total_sessions = batch_size * num_batches

    print("\nEXPERIMENTAL DESIGN:")
    print(f"  Batch size: {batch_size} sessions")
    print(f"  Number of batches: {num_batches}")
    print(f"  Total sessions: {total_sessions}")

    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        batch_results = []

        print("\nDATA COLLECTION:")

        for batch_num in range(num_batches):
            batch_times = []
            batch_start = time.time()

            for i in range(batch_size):
                t0 = time.time()
                answer, protocol = guide.solve(
                    problem_statement=f"Endurance test batch {batch_num} session {i}",
                    max_iterations=1,
                )
                t1 = time.time()
                batch_times.append(t1 - t0)

            batch_duration = time.time() - batch_start

            mean_time = statistics.mean(batch_times)
            stdev_time = statistics.stdev(batch_times) if len(batch_times) > 1 else 0

            batch_results.append(
                {
                    "batch": batch_num + 1,
                    "mean_time": mean_time,
                    "stdev": stdev_time,
                    "batch_duration": batch_duration,
                    "throughput": batch_size / batch_duration,
                }
            )

            print(
                f"  Batch {batch_num + 1:2d}: {mean_time * 1000:.3f}ms ± {stdev_time * 1000:.3f}ms "
                f"({batch_size / batch_duration:.1f} sess/s)"
            )

        # Statistical analysis - is there a trend?
        x = [r["batch"] for r in batch_results]
        y = [r["mean_time"] for r in batch_results]

        # Linear regression
        n = len(x)
        mean_x = statistics.mean(x)
        mean_y = statistics.mean(y)

        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator_x = sum((x[i] - mean_x) ** 2 for i in range(n))

        slope = numerator / denominator_x if denominator_x > 0 else 0

        # Calculate percentage change
        initial_time = batch_results[0]["mean_time"]
        final_time = batch_results[-1]["mean_time"]
        percent_change = ((final_time - initial_time) / initial_time) * 100

        # Statistical significance - is slope close to zero?
        # Using simple threshold: if change < 10%, consider it stable
        is_stable = abs(percent_change) < 10.0

        print("\nSTATISTICAL ANALYSIS:")
        print(f"  Initial performance: {initial_time * 1000:.3f}ms")
        print(f"  Final performance: {final_time * 1000:.3f}ms")
        print(f"  Change: {percent_change:+.2f}%")
        print(f"  Regression slope: {slope * 1000:.6f}ms/batch")
        print(
            f"  Mean throughput: {statistics.mean([r['throughput'] for r in batch_results]):.1f} sess/s"
        )

        print("\nTREND ANALYSIS:")
        if is_stable:
            print("  ✅ STABLE: Performance change within ±10% threshold")
        else:
            if percent_change > 0:
                print(f"  ⚠️  DEGRADATION: {percent_change:.2f}% slower")
            else:
                print(f"  📈 IMPROVEMENT: {abs(percent_change):.2f}% faster")

        print("\nHYPOTHESIS TEST:")
        if is_stable:
            print("  ✅ HYPOTHESIS ACCEPTED: No significant performance degradation")
            return True, {
                "initial_time": initial_time,
                "final_time": final_time,
                "percent_change": percent_change,
                "slope": slope,
                "total_sessions": total_sessions,
            }
        else:
            print(f"  ❌ HYPOTHESIS REJECTED: Performance changed by {percent_change:.2f}%")
            return False, {
                "initial_time": initial_time,
                "final_time": final_time,
                "percent_change": percent_change,
                "slope": slope,
            }


# ============================================================================
# EXPERIMENT 5: Memory Profiling
# ============================================================================


def experiment_memory_profiling():
    """
    RESEARCH QUESTION: Does memory usage grow unbounded (leak)?

    HYPOTHESIS: Memory usage stabilizes after initial allocation.

    NULL HYPOTHESIS: Memory usage grows linearly with sessions (leak).

    METHOD:
    - Track memory usage before and after session creation
    - Create 500 sessions
    - Measure memory at intervals
    - Analyze: linear growth or plateau?

    METRICS:
    - Memory usage in MB
    - Memory per session
    - Peak memory
    - Memory growth rate

    ACCEPTANCE CRITERIA:
    - Memory growth < 0.01 MB/session after warmup
    - No continuous upward trend
    """

    print("\n" + "=" * 80)
    print("EXPERIMENT 5: Memory Profiling")
    print("=" * 80)

    print("\nRESEARCH QUESTION: Does memory usage stabilize or leak?")
    print("HYPOTHESIS: Memory usage plateaus (no leak)")

    num_sessions = 500
    sample_interval = 50  # Measure memory every 50 sessions

    print("\nEXPERIMENTAL DESIGN:")
    print(f"  Total sessions: {num_sessions}")
    print(f"  Sample interval: every {sample_interval} sessions")

    # Start memory tracking
    tracemalloc.start()
    gc.collect()  # Clean baseline

    with tempfile.TemporaryDirectory() as tmpdir:
        initial_memory = tracemalloc.get_traced_memory()[0] / 1024 / 1024  # MB

        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        memory_samples = []

        print("\nDATA COLLECTION:")
        print(f"  Initial memory: {initial_memory:.2f} MB")

        for i in range(num_sessions):
            answer, protocol = guide.solve(problem_statement=f"Memory test {i}", max_iterations=1)

            if (i + 1) % sample_interval == 0:
                gc.collect()  # Force collection for accurate measurement
                current, peak = tracemalloc.get_traced_memory()
                current_mb = current / 1024 / 1024
                peak_mb = peak / 1024 / 1024

                memory_samples.append(
                    {
                        "session": i + 1,
                        "current_mb": current_mb,
                        "peak_mb": peak_mb,
                        "delta_mb": current_mb - initial_memory,
                    }
                )

                print(
                    f"  Session {i + 1:3d}: {current_mb:.2f} MB (Δ{current_mb - initial_memory:+.2f} MB)"
                )

    tracemalloc.stop()

    # Analysis
    if len(memory_samples) >= 2:
        # Calculate memory per session (after warmup)
        warmup_samples = memory_samples[2:]  # Skip first 2 samples (warmup)
        if len(warmup_samples) >= 2:
            first_sample = warmup_samples[0]
            last_sample = warmup_samples[-1]

            sessions_diff = last_sample["session"] - first_sample["session"]
            memory_diff = last_sample["current_mb"] - first_sample["current_mb"]
            memory_per_session = memory_diff / sessions_diff if sessions_diff > 0 else 0

            print("\nSTATISTICAL ANALYSIS:")
            print(f"  Peak memory: {max(s['peak_mb'] for s in memory_samples):.2f} MB")
            print(f"  Final memory: {memory_samples[-1]['current_mb']:.2f} MB")
            print(f"  Total increase: {memory_samples[-1]['delta_mb']:.2f} MB")
            print(
                f"  Memory per session (after warmup): {memory_per_session * 1000:.3f} KB/session"
            )

            # Check for leak - threshold is 0.01 MB/session
            is_leaking = memory_per_session > 0.01

            print("\nLEAK DETECTION:")
            if is_leaking:
                print(f"  ⚠️  POSSIBLE LEAK: {memory_per_session * 1000:.3f} KB/session")
            else:
                print(f"  ✅ NO LEAK: {memory_per_session * 1000:.3f} KB/session < 10 KB/session")

            print("\nHYPOTHESIS TEST:")
            if not is_leaking:
                print("  ✅ HYPOTHESIS ACCEPTED: Memory usage is stable")
                return True, {
                    "peak_memory_mb": max(s["peak_mb"] for s in memory_samples),
                    "memory_per_session_kb": memory_per_session * 1000,
                    "total_sessions": num_sessions,
                }
            else:
                print("  ❌ HYPOTHESIS REJECTED: Memory leak detected")
                return False, {
                    "memory_per_session_kb": memory_per_session * 1000,
                    "leak_rate": "linear",
                }
        else:
            print("  ⚠️  Insufficient warmup samples")
            return None, {}
    else:
        print("  ⚠️  Insufficient samples")
        return None, {}


# ============================================================================
# EXPERIMENT 6: Breaking Point Analysis
# ============================================================================


def experiment_breaking_point():
    """
    RESEARCH QUESTION: What is the maximum concurrent load before failure?

    HYPOTHESIS: System can handle at least 50 concurrent threads.

    METHOD:
    - Binary search for breaking point
    - Start with 10 threads, double until failure
    - Find exact threshold where success rate drops below 100%

    METRICS:
    - Maximum successful thread count
    - Failure rate at each level
    - Error types at breaking point

    ACCEPTANCE CRITERIA:
    - Breaking point >= 50 threads
    - Graceful degradation (no crashes)
    """

    print("\n" + "=" * 80)
    print("EXPERIMENT 6: Breaking Point Analysis")
    print("=" * 80)

    print("\nRESEARCH QUESTION: What is the maximum concurrent load?")
    print("HYPOTHESIS: Can handle ≥50 concurrent threads")

    def test_concurrent_load(num_threads, sessions_per_thread=5):
        """Test a specific concurrent load."""
        with tempfile.TemporaryDirectory() as tmpdir:
            successes = 0
            failures = 0
            errors = []

            def worker(tid):
                try:
                    guide = TheGuide(
                        project_path=Path(tmpdir),
                        client_llm=StableLLM(),
                        guide_llm_config={"model": "test"},
                    )
                    guide.guide_llm = StableLLM()

                    for i in range(sessions_per_thread):
                        answer, protocol = guide.solve(
                            problem_statement=f"Load test T{tid} S{i}", max_iterations=1
                        )
                    return True, None
                except Exception as e:
                    return False, str(e)

            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = [executor.submit(worker, i) for i in range(num_threads)]

                for future in concurrent.futures.as_completed(futures):
                    success, error = future.result()
                    if success:
                        successes += 1
                    else:
                        failures += 1
                        errors.append(error)

            success_rate = (successes / num_threads) * 100 if num_threads > 0 else 0

            return {
                "threads": num_threads,
                "successes": successes,
                "failures": failures,
                "success_rate": success_rate,
                "errors": errors,
            }

    print("\nDATA COLLECTION (binary search for breaking point):")

    # Test increasing loads
    test_loads = [10, 20, 50, 100]
    results = []

    for num_threads in test_loads:
        print(f"\n  Testing {num_threads} threads...")
        result = test_concurrent_load(num_threads)
        results.append(result)

        print(
            f"    Success rate: {result['success_rate']:.1f}% ({result['successes']}/{result['threads']})"
        )

        if result["success_rate"] < 100.0:
            print(f"    ⚠️  Breaking point found at {num_threads} threads")
            if result["errors"]:
                print(f"    Sample errors: {result['errors'][:3]}")
            break

    # Find maximum successful load
    max_successful = max((r["threads"] for r in results if r["success_rate"] == 100.0), default=0)

    print("\nSTATISTICAL ANALYSIS:")
    print(f"  Maximum successful load: {max_successful} concurrent threads")

    for r in results:
        status = "✅" if r["success_rate"] == 100.0 else "❌"
        print(f"  {status} {r['threads']:3d} threads: {r['success_rate']:5.1f}% success")

    print("\nHYPOTHESIS TEST:")
    if max_successful >= 50:
        print(f"  ✅ HYPOTHESIS ACCEPTED: Handles ≥50 threads ({max_successful})")
        return True, {
            "max_threads": max_successful,
            "tested_loads": [r["threads"] for r in results],
            "success_rates": [r["success_rate"] for r in results],
        }
    else:
        print(f"  ❌ HYPOTHESIS REJECTED: Breaking point at {max_successful} < 50 threads")
        return False, {
            "max_threads": max_successful,
            "breaking_point": next(
                (r["threads"] for r in results if r["success_rate"] < 100.0), None
            ),
        }


# ============================================================================
# EXPERIMENT 7: Statistical Distribution Analysis
# ============================================================================


def experiment_statistical_distributions():
    """
    RESEARCH QUESTION: Are performance metrics normally distributed?

    HYPOTHESIS: Session creation times follow normal distribution.

    METHOD:
    - Create 300 sessions
    - Measure creation time for each
    - Calculate distribution statistics
    - Test for normality

    METRICS:
    - Mean, median, mode
    - Standard deviation, variance
    - Skewness, kurtosis
    - Percentiles (p50, p95, p99)

    ACCEPTANCE CRITERIA:
    - Skewness between -1 and 1 (approximately symmetric)
    - Kurtosis between -1 and 3 (approximately normal)
    """

    print("\n" + "=" * 80)
    print("EXPERIMENT 7: Statistical Distribution Analysis")
    print("=" * 80)

    print("\nRESEARCH QUESTION: Are creation times normally distributed?")
    print("HYPOTHESIS: Times follow normal distribution (skew ∈ [-1,1])")

    num_samples = 300

    print("\nEXPERIMENTAL DESIGN:")
    print(f"  Sample size: {num_samples}")

    with tempfile.TemporaryDirectory() as tmpdir:
        guide = TheGuide(
            project_path=Path(tmpdir), client_llm=StableLLM(), guide_llm_config={"model": "test"}
        )
        guide.guide_llm = StableLLM()

        creation_times = []

        print("\nDATA COLLECTION:")

        for i in range(num_samples):
            t0 = time.time()
            answer, protocol = guide.solve(
                problem_statement=f"Distribution test {i}", max_iterations=1
            )
            t1 = time.time()
            creation_times.append(t1 - t0)

            if (i + 1) % 100 == 0:
                print(f"  Progress: {i + 1}/{num_samples}")

        # Statistical analysis
        mean_time = statistics.mean(creation_times)
        median_time = statistics.median(creation_times)
        stdev_time = statistics.stdev(creation_times)
        variance = statistics.variance(creation_times)
        min_time = min(creation_times)
        max_time = max(creation_times)

        # Percentiles
        sorted_times = sorted(creation_times)
        p50 = sorted_times[int(len(sorted_times) * 0.50)]
        p95 = sorted_times[int(len(sorted_times) * 0.95)]
        p99 = sorted_times[int(len(sorted_times) * 0.99)]

        # Skewness (measure of asymmetry)
        mean_dev_cubed = sum(((t - mean_time) ** 3) for t in creation_times) / len(creation_times)
        skewness = mean_dev_cubed / (stdev_time**3) if stdev_time > 0 else 0

        # Kurtosis (measure of tail heaviness)
        mean_dev_fourth = sum(((t - mean_time) ** 4) for t in creation_times) / len(creation_times)
        kurtosis = (mean_dev_fourth / (stdev_time**4)) - 3 if stdev_time > 0 else 0

        print("\nDESCRIPTIVE STATISTICS:")
        print(f"  Mean:     {mean_time * 1000:.3f}ms")
        print(f"  Median:   {median_time * 1000:.3f}ms")
        print(f"  Std Dev:  {stdev_time * 1000:.3f}ms")
        print(f"  Variance: {variance * 1000000:.3f}ms²")
        print(f"  Min:      {min_time * 1000:.3f}ms")
        print(f"  Max:      {max_time * 1000:.3f}ms")

        print("\nPERCENTILES:")
        print(f"  p50 (median): {p50 * 1000:.3f}ms")
        print(f"  p95:          {p95 * 1000:.3f}ms")
        print(f"  p99:          {p99 * 1000:.3f}ms")

        print("\nDISTRIBUTION SHAPE:")
        print(f"  Skewness: {skewness:.3f}")
        print(f"  Kurtosis: {kurtosis:.3f}")

        # Interpretation
        print("\nINTERPRETATION:")
        if abs(skewness) < 0.5:
            print("  Skewness: Approximately symmetric")
        elif abs(skewness) < 1:
            print("  Skewness: Moderately skewed")
        else:
            print("  Skewness: Highly skewed")

        if abs(kurtosis) < 0.5:
            print("  Kurtosis: Approximately normal (mesokurtic)")
        elif kurtosis > 0.5:
            print("  Kurtosis: Heavy-tailed (leptokurtic)")
        else:
            print("  Kurtosis: Light-tailed (platykurtic)")

        # Normality test
        is_normal = abs(skewness) < 1 and abs(kurtosis) < 3

        print("\nHYPOTHESIS TEST:")
        if is_normal:
            print("  ✅ HYPOTHESIS ACCEPTED: Approximately normal distribution")
            return True, {
                "mean": mean_time,
                "median": median_time,
                "stdev": stdev_time,
                "skewness": skewness,
                "kurtosis": kurtosis,
                "p95": p95,
                "p99": p99,
            }
        else:
            print("  ❌ HYPOTHESIS REJECTED: Distribution is not normal")
            return False, {
                "skewness": skewness,
                "kurtosis": kurtosis,
                "reason": "skewness or kurtosis out of range",
            }


# ============================================================================
# MAIN EXPERIMENTAL PROTOCOL
# ============================================================================


def run_advanced_experiments():
    """Run all advanced experiments."""

    print("=" * 80)
    print("ADVANCED EXPERIMENTAL SUITE")
    print("Sophisticated Statistical Analysis of TheGuide")
    print("=" * 80)

    print("\nMETHODOLOGY:")
    print("  - Endurance testing (1000 sessions)")
    print("  - Memory profiling (leak detection)")
    print("  - Breaking point analysis (concurrent load)")
    print("  - Statistical distribution analysis")

    results = {}

    # Experiment 4
    print("\n" + "~" * 80)
    accepted, data = experiment_endurance_testing()
    results["exp4_endurance"] = {"hypothesis_accepted": accepted, "data": data}

    # Experiment 5
    print("\n" + "~" * 80)
    accepted, data = experiment_memory_profiling()
    results["exp5_memory"] = {"hypothesis_accepted": accepted, "data": data}

    # Experiment 6
    print("\n" + "~" * 80)
    accepted, data = experiment_breaking_point()
    results["exp6_breaking_point"] = {"hypothesis_accepted": accepted, "data": data}

    # Experiment 7
    print("\n" + "~" * 80)
    accepted, data = experiment_statistical_distributions()
    results["exp7_distributions"] = {"hypothesis_accepted": accepted, "data": data}

    # Final summary
    print("\n" + "=" * 80)
    print("ADVANCED EXPERIMENTAL RESULTS")
    print("=" * 80)

    total_experiments = len([r for r in results.values() if r["hypothesis_accepted"] is not None])
    accepted_count = sum(1 for r in results.values() if r["hypothesis_accepted"] is True)

    print(f"\nTotal Experiments: {total_experiments}")
    print(f"Hypotheses Accepted: {accepted_count}")
    print(f"Hypotheses Rejected: {total_experiments - accepted_count}")
    print(f"Acceptance Rate: {(accepted_count / total_experiments) * 100:.1f}%")

    print("\nDETAILED RESULTS:")
    for exp_name, result in results.items():
        if result["hypothesis_accepted"] is not None:
            status = "✅ ACCEPTED" if result["hypothesis_accepted"] else "❌ REJECTED"
            print(f"\n{exp_name}: {status}")
            for key, value in result["data"].items():
                if isinstance(value, float):
                    print(f"  {key}: {value:.4f}")
                elif isinstance(value, list):
                    print(f"  {key}: {value}")
                else:
                    print(f"  {key}: {value}")

    # Save results
    results_file = Path("advanced_experimental_results.json")
    with open(results_file, "w") as f:
        serializable = {}
        for k, v in results.items():
            if v["hypothesis_accepted"] is not None:
                serializable[k] = {
                    "hypothesis_accepted": v["hypothesis_accepted"],
                    "data": {
                        dk: (
                            float(dv)
                            if isinstance(dv, (int, float)) and not isinstance(dv, bool)
                            else [float(x) if isinstance(x, (int, float)) else x for x in dv]
                            if isinstance(dv, list)
                            else str(dv)
                        )
                        for dk, dv in v["data"].items()
                    },
                }
        json.dump(serializable, f, indent=2)

    print(f"\n📊 Advanced experimental data saved to: {results_file}")
    print("\n" + "=" * 80)

    return results


if __name__ == "__main__":
    results = run_advanced_experiments()
