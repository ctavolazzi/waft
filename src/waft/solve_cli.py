#!/usr/bin/env python3
"""
META-COGNITIVE CLI TOOL

Command-line interface for the meta-cognitive problem-solving system.
Simple, usable, predictable.

Usage:
    python solve_cli.py "Your problem here"
    python solve_cli.py "Your problem" --mode smart
    python solve_cli.py "Your problem" --mode voting --iterations 5
    python solve_cli.py "Your problem" --json output.json
"""

import argparse
import sys
import json
from pathlib import Path

from demo_api import MetaCognitiveAPI, ProblemInput, GuideMode


def run_comparison(api: MetaCognitiveAPI, problem: str, max_iterations: int):
    """Compare all modes side-by-side."""
    print("="*80)
    print("MODE COMPARISON")
    print("="*80)
    print(f"\nProblem: {problem}")
    print(f"Max iterations: {max_iterations}\n")

    modes = ['basic', 'strict', 'lenient', 'smart', 'voting', 'ensemble']
    mode_map = {
        'basic': GuideMode.BASIC,
        'strict': GuideMode.STRICT,
        'lenient': GuideMode.LENIENT,
        'smart': GuideMode.SMART,
        'voting': GuideMode.VOTING,
        'ensemble': GuideMode.ENSEMBLE,
    }

    results = []
    for mode_name in modes:
        input_data = ProblemInput(
            problem=problem,
            mode=mode_map[mode_name],
            max_iterations=max_iterations
        )
        output = api.solve(input_data)
        results.append((mode_name, output))
        print(f"  {mode_name:12s}: quality={output.quality_report.final_quality:.3f}, " +
              f"grade={output.quality_report.grade}, " +
              f"iterations={output.quality_report.iterations_used}, " +
              f"efficiency={output.quality_report.efficiency:.3f}")

    print("\n" + "="*80)
    best = max(results, key=lambda x: x[1].quality_report.final_quality)
    print(f"🏆 Best mode: {best[0]} (quality={best[1].quality_report.final_quality:.3f})")
    print("="*80)


def run_benchmark(api: MetaCognitiveAPI):
    """Run quick benchmark test."""
    import time

    print("="*80)
    print("QUICK BENCHMARK")
    print("="*80)

    print("\nTesting consistency (5 runs)...")
    problem = "What is machine learning?"
    qualities = []
    for i in range(5):
        input_data = ProblemInput(problem=problem, mode=GuideMode.BASIC, max_iterations=3)
        output = api.solve(input_data)
        qualities.append(output.quality_report.final_quality)
        print(f"  Run {i+1}: {qualities[i]:.3f}")

    import statistics
    variance = statistics.variance(qualities) if len(qualities) > 1 else 0
    print(f"  Variance: {variance:.6f} ({'PASS' if variance < 0.01 else 'FAIL'})")

    print("\nTesting performance (10 solves)...")
    start = time.time()
    for i in range(10):
        input_data = ProblemInput(problem=f"Test {i}", mode=GuideMode.BASIC, max_iterations=3)
        api.solve(input_data)
    elapsed = time.time() - start
    print(f"  Total time: {elapsed:.3f}s")
    print(f"  Average: {elapsed/10:.3f}s per solve")
    print(f"  Throughput: {10/elapsed:.1f} solves/sec")

    print("\nTesting determinism...")
    input1 = ProblemInput(problem="Test determinism", mode=GuideMode.BASIC, max_iterations=3)
    out1 = api.solve(input1)
    out2 = api.solve(input1)
    match = out1.quality_report.final_quality == out2.quality_report.final_quality
    print(f"  Output 1: {out1.quality_report.final_quality:.3f}")
    print(f"  Output 2: {out2.quality_report.final_quality:.3f}")
    print(f"  Match: {'PASS' if match else 'FAIL'}")

    print("\n" + "="*80)
    print("✅ Benchmark complete")
    print("="*80)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Meta-Cognitive Problem Solving CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "What is recursion?"
  %(prog)s "Explain quantum computing" --mode smart
  %(prog)s "Best programming paradigm?" --mode voting
  %(prog)s "Complex problem" --mode ensemble --iterations 10
  %(prog)s "API test" --json output.json
  %(prog)s "Test" --verbose

Modes:
  basic      - Simple iterative refinement (default)
  strict     - High standards, precise evaluation
  lenient    - Flexible, exploratory
  smart      - Auto-selects strategy per problem
  adaptive   - Learns from history
  voting     - Multiple guides vote for consensus
  ensemble   - All strategies, pick best result
        """
    )

    parser.add_argument(
        'problem',
        type=str,
        help='Problem to solve (enclose in quotes)'
    )

    parser.add_argument(
        '--mode',
        type=str,
        default='basic',
        choices=['basic', 'strict', 'lenient', 'smart', 'adaptive', 'voting', 'ensemble'],
        help='Guide mode (default: basic)'
    )

    parser.add_argument(
        '--iterations',
        type=int,
        default=10,
        help='Maximum iterations (default: 10)'
    )

    parser.add_argument(
        '--threshold',
        type=float,
        default=0.8,
        help='Quality threshold (default: 0.8)'
    )

    parser.add_argument(
        '--json',
        type=str,
        default=None,
        metavar='FILE',
        help='Export result to JSON file'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed iteration history'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Only show final answer'
    )

    parser.add_argument(
        '--compare',
        action='store_true',
        help='Compare all modes side-by-side'
    )

    parser.add_argument(
        '--benchmark',
        action='store_true',
        help='Run quick benchmark test'
    )

    args = parser.parse_args()

    # Convert mode string to enum
    mode_map = {
        'basic': GuideMode.BASIC,
        'strict': GuideMode.STRICT,
        'lenient': GuideMode.LENIENT,
        'smart': GuideMode.SMART,
        'adaptive': GuideMode.ADAPTIVE,
        'voting': GuideMode.VOTING,
        'ensemble': GuideMode.ENSEMBLE,
    }
    mode = mode_map[args.mode]

    # Create API
    api = MetaCognitiveAPI()

    # Handle special modes
    if args.benchmark:
        run_benchmark(api)
        return

    if args.compare:
        run_comparison(api, args.problem, args.iterations)
        return

    # Normal solve mode
    input_data = ProblemInput(
        problem=args.problem,
        mode=mode,
        max_iterations=args.iterations,
        quality_threshold=args.threshold
    )

    # Solve
    if not args.quiet:
        print(f"Solving: '{args.problem}'")
        print(f"Mode: {args.mode}, Max iterations: {args.iterations}")
        print()

    output = api.solve(input_data)

    # Display results
    if args.quiet:
        # Only final answer
        print(output.final_answer)
    else:
        # Standard output
        print("="*80)
        print("SOLUTION")
        print("="*80)
        print(f"\nProblem: {output.problem}")
        print(f"Mode: {output.mode}")
        print(f"\nFinal Answer:\n{output.final_answer}")
        print(f"\n{'='*80}")
        print("QUALITY REPORT")
        print("="*80)
        print(f"\nFinal Quality:     {output.quality_report.final_quality:.3f}")
        print(f"Grade:             {output.quality_report.grade}")
        print(f"Iterations Used:   {output.quality_report.iterations_used}")
        print(f"Efficiency:        {output.quality_report.efficiency:.3f}")
        print(f"Improvement Rate:  {output.quality_report.improvement_rate:.3f}")
        print(f"Convergence Speed: {output.quality_report.convergence_speed:.3f}")
        print(f"Consistency:       {output.quality_report.consistency:.3f}")

        if args.verbose:
            print(f"\n{'='*80}")
            print("ITERATION HISTORY")
            print("="*80)
            for step in output.step_history:
                print(f"\nIteration {step['iteration']}:")
                print(f"  Quality: {step['quality']:.3f}")
                print(f"  Answer: {step['answer'][:100]}..." if len(step['answer']) > 100 else f"  Answer: {step['answer']}")
                print(f"  Dimensions:")
                for dim, value in step['dimensions'].items():
                    print(f"    {dim:12s}: {value:.3f}")

        print()

    # Export JSON if requested
    if args.json:
        json_str = api.to_json(output)
        Path(args.json).write_text(json_str)
        if not args.quiet:
            print(f"✅ Exported to {args.json}")

    # Exit with appropriate code
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
