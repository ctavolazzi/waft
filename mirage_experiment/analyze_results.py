#!/usr/bin/env python3
"""
Statistical Analysis Script - Analyzes flight_recorder.json and produces terminal reports.
"""

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Any


def load_flight_recorder(file_path: Path) -> List[Dict[str, Any]]:
    """Load flight recorder data."""
    with open(file_path) as f:
        return json.load(f)


def calculate_statistics(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate statistical summary."""
    if not results:
        return {}
    
    total = len(results)
    
    # Basic counts
    bugs_detected = sum(1 for r in results if r.get("agent_behavior", {}).get("recognized_bug"))
    fixes_proposed = sum(1 for r in results if r.get("agent_behavior", {}).get("proposed_fix"))
    fixes_applied = sum(1 for r in results if r.get("fix_quality", {}).get("syntax_valid"))
    bugs_fixed = sum(1 for r in results if r.get("fix_quality", {}).get("bug_fixed"))
    hypothesis_confirmed = sum(1 for r in results if r.get("hypothesis_confirmed") is True)
    
    # Timing metrics
    read_times = [
        r.get("agent_behavior", {}).get("read_time_seconds", 0)
        for r in results
        if r.get("agent_behavior", {}).get("read_time_seconds")
    ]
    
    fix_times = [
        r.get("agent_behavior", {}).get("fix_proposal_time_seconds", 0)
        for r in results
        if r.get("agent_behavior", {}).get("fix_proposal_time_seconds")
    ]
    
    stats = {
        "total_tests": total,
        "bugs_detected": bugs_detected,
        "bugs_detected_rate": bugs_detected / total if total > 0 else 0,
        "fixes_proposed": fixes_proposed,
        "fixes_proposed_rate": fixes_proposed / total if total > 0 else 0,
        "fixes_applied": fixes_applied,
        "fixes_applied_rate": fixes_applied / total if total > 0 else 0,
        "bugs_fixed": bugs_fixed,
        "bugs_fixed_rate": bugs_fixed / total if total > 0 else 0,
        "hypothesis_confirmed": hypothesis_confirmed,
        "hypothesis_confirmed_rate": hypothesis_confirmed / total if total > 0 else 0,
    }
    
    if read_times:
        stats["read_time"] = {
            "mean": statistics.mean(read_times),
            "median": statistics.median(read_times),
            "min": min(read_times),
            "max": max(read_times),
        }
    
    if fix_times:
        stats["fix_time"] = {
            "mean": statistics.mean(fix_times),
            "median": statistics.median(fix_times),
            "min": min(fix_times),
            "max": max(fix_times),
        }
    
    return stats


def analyze_by_scenario(results: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Analyze results grouped by scenario type."""
    by_scenario = defaultdict(list)
    
    for result in results:
        scenario_type = result.get("scenario_type", "unknown")
        by_scenario[scenario_type].append(result)
    
    analysis = {}
    for scenario_type, scenario_results in by_scenario.items():
        analysis[scenario_type] = calculate_statistics(scenario_results)
    
    return analysis


def analyze_by_generation(results: List[Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
    """Analyze results grouped by generation (for evolutionary cycles)."""
    by_generation = defaultdict(list)
    
    for result in results:
        generation = result.get("generation", 0)
        by_generation[generation].append(result)
    
    analysis = {}
    for generation, gen_results in sorted(by_generation.items()):
        analysis[generation] = calculate_statistics(gen_results)
    
    return analysis


def print_summary(stats: Dict[str, Any]):
    """Print statistical summary to terminal."""
    print("\n" + "="*70)
    print("STATISTICAL ANALYSIS SUMMARY")
    print("="*70)
    
    print(f"\nTotal Tests: {stats.get('total_tests', 0)}")
    
    print(f"\n{'Metric':<30} {'Count':<15} {'Rate':<15}")
    print("-"*70)
    print(f"{'Bugs Detected':<30} {stats.get('bugs_detected', 0):<15} {stats.get('bugs_detected_rate', 0)*100:>6.1f}%")
    print(f"{'Fixes Proposed':<30} {stats.get('fixes_proposed', 0):<15} {stats.get('fixes_proposed_rate', 0)*100:>6.1f}%")
    print(f"{'Fixes Applied':<30} {stats.get('fixes_applied', 0):<15} {stats.get('fixes_applied_rate', 0)*100:>6.1f}%")
    print(f"{'Bugs Fixed':<30} {stats.get('bugs_fixed', 0):<15} {stats.get('bugs_fixed_rate', 0)*100:>6.1f}%")
    print(f"{'Hypothesis Confirmed':<30} {stats.get('hypothesis_confirmed', 0):<15} {stats.get('hypothesis_confirmed_rate', 0)*100:>6.1f}%")
    
    if "read_time" in stats:
        rt = stats["read_time"]
        print(f"\nRead Time (seconds):")
        print(f"  Mean: {rt['mean']:.3f}")
        print(f"  Median: {rt['median']:.3f}")
        print(f"  Range: {rt['min']:.3f} - {rt['max']:.3f}")
    
    if "fix_time" in stats:
        ft = stats["fix_time"]
        print(f"\nFix Proposal Time (seconds):")
        print(f"  Mean: {ft['mean']:.3f}")
        print(f"  Median: {ft['median']:.3f}")
        print(f"  Range: {ft['min']:.3f} - {ft['max']:.3f}")
    
    print("\n" + "="*70 + "\n")


def print_scenario_analysis(analysis: Dict[str, Dict[str, Any]]):
    """Print analysis grouped by scenario."""
    print("\n" + "="*70)
    print("ANALYSIS BY SCENARIO TYPE")
    print("="*70)
    
    for scenario_type, stats in analysis.items():
        print(f"\n{scenario_type.upper()}:")
        print(f"  Tests: {stats.get('total_tests', 0)}")
        print(f"  Bugs Detected: {stats.get('bugs_detected_rate', 0)*100:.1f}%")
        print(f"  Fixes Proposed: {stats.get('fixes_proposed_rate', 0)*100:.1f}%")
        print(f"  Bugs Fixed: {stats.get('bugs_fixed_rate', 0)*100:.1f}%")
    
    print("\n" + "="*70 + "\n")


def print_generation_analysis(analysis: Dict[int, Dict[str, Any]]):
    """Print analysis grouped by generation."""
    print("\n" + "="*70)
    print("EVOLUTIONARY TRAJECTORY")
    print("="*70)
    
    print(f"\n{'Generation':<15} {'Tests':<10} {'Detected':<12} {'Fixed':<12}")
    print("-"*70)
    
    for generation in sorted(analysis.keys()):
        stats = analysis[generation]
        detected_rate = stats.get('bugs_detected_rate', 0) * 100
        fixed_rate = stats.get('bugs_fixed_rate', 0) * 100
        print(f"{generation:<15} {stats.get('total_tests', 0):<10} {detected_rate:>6.1f}%     {fixed_rate:>6.1f}%")
    
    print("\n" + "="*70 + "\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Analyze flight recorder data")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).parent / "results" / "flight_recorder.json",
        help="Path to flight_recorder.json",
    )
    parser.add_argument("--by-scenario", action="store_true", help="Analyze by scenario type")
    parser.add_argument("--by-generation", action="store_true", help="Analyze by generation")
    
    args = parser.parse_args()
    
    if not args.input.exists():
        print(f"Error: Flight recorder file not found: {args.input}")
        return
    
    results = load_flight_recorder(args.input)
    
    if not results:
        print("No results found in flight recorder.")
        return
    
    # Overall statistics
    stats = calculate_statistics(results)
    print_summary(stats)
    
    # Scenario analysis
    if args.by_scenario:
        scenario_analysis = analyze_by_scenario(results)
        print_scenario_analysis(scenario_analysis)
    
    # Generation analysis
    if args.by_generation:
        generation_analysis = analyze_by_generation(results)
        print_generation_analysis(generation_analysis)


if __name__ == "__main__":
    main()
