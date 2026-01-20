#!/usr/bin/env python3
"""
Priority Matrix Calculator

Calculates priority scores for work efforts based on Impact, Urgency, Blocking, and Effort.

Usage:
    python priority_matrix.py --work-efforts "WE-001,WE-002,WE-003" --output priority_matrix.md
"""

import argparse
import json
from pathlib import Path

# Default weights for priority calculation
DEFAULT_WEIGHTS = {
    "impact": 0.30,
    "urgency": 0.25,
    "blocking": 0.25,
    "effort": 0.20,  # Lower effort = higher score (inverted)
}


def calculate_priority_score(
    impact: float, urgency: float, blocking: float, effort: float, weights: dict[str, float] = None
) -> float:
    """Calculate priority score (0-10 scale)."""
    if weights is None:
        weights = DEFAULT_WEIGHTS

    # Invert effort (lower effort = higher score)
    effort_score = 10.0 - effort

    score = (
        impact * weights["impact"]
        + urgency * weights["urgency"]
        + blocking * weights["blocking"]
        + effort_score * weights["effort"]
    )

    return round(score, 2)


def determine_priority_level(score: float) -> tuple[str, str]:
    """Determine priority level from score."""
    if score >= 8.5:
        return "🔴", "CRITICAL"
    elif score >= 7.0:
        return "🟠", "HIGH"
    elif score >= 5.0:
        return "🟡", "MEDIUM"
    else:
        return "🟢", "LOW"


def print_priority_matrix(work_efforts: list[dict]):
    """Print formatted priority matrix."""
    print("\n" + "=" * 100)
    print("PRIORITY MATRIX")
    print("=" * 100)

    # Header
    header = f"{'Work Effort':<40} {'Impact':<10} {'Urgency':<10} {'Blocking':<10} {'Effort':<10} {'Score':<10} {'Priority':<15}"
    print(header)
    print("-" * 100)

    # Work efforts
    for we in work_efforts:
        priority_emoji, priority_level = determine_priority_level(we["score"])
        row = (
            f"{we['id']:<40} "
            f"{we['impact']:<10.2f} "
            f"{we['urgency']:<10.2f} "
            f"{we['blocking']:<10.2f} "
            f"{we['effort']:<10.2f} "
            f"{we['score']:<10.2f} "
            f"{priority_emoji} {priority_level:<12}"
        )
        print(row)

    print("=" * 100)
    print(
        f"\n🏆 HIGHEST PRIORITY: {work_efforts[0]['id']} (Score: {work_efforts[0]['score']:.2f}/10)"
    )
    print("=" * 100 + "\n")


def generate_markdown_report(work_efforts: list[dict], output_path: str):
    """Generate markdown priority matrix report."""
    content = "# Priority Matrix\n\n"
    content += f"**Generated**: {Path(__file__).stat().st_mtime}\n\n"
    content += "---\n\n"

    content += "## Priority Ranking\n\n"
    content += "| Priority | Work Effort | Impact | Urgency | Blocking | Effort | Score |\n"
    content += "|----------|-------------|--------|---------|----------|--------|-------|\n"

    for i, we in enumerate(work_efforts, 1):
        priority_emoji, priority_level = determine_priority_level(we["score"])
        content += (
            f"| {i}. {priority_emoji} {priority_level} | "
            f"`{we['id']}` | "
            f"{we['impact']:.2f} | "
            f"{we['urgency']:.2f} | "
            f"{we['blocking']:.2f} | "
            f"{we['effort']:.2f} | "
            f"**{we['score']:.2f}** |\n"
        )

    content += "\n---\n\n"
    content += "## Recommendations\n\n"
    content += f"**Highest Priority**: `{work_efforts[0]['id']}` (Score: {work_efforts[0]['score']:.2f}/10)\n\n"
    content += "**Execution Order**:\n"
    for i, we in enumerate(work_efforts, 1):
        priority_emoji, priority_level = determine_priority_level(we["score"])
        content += (
            f"{i}. {priority_emoji} `{we['id']}` - {priority_level} (Score: {we['score']:.2f})\n"
        )

    with open(output_path, "w") as f:
        f.write(content)

    print(f"✅ Priority matrix report saved to {output_path}")


def interactive_mode():
    """Interactive mode for entering work effort priorities."""
    print("\n" + "=" * 100)
    print("PRIORITY MATRIX CALCULATOR - Interactive Mode")
    print("=" * 100 + "\n")

    work_efforts = []

    while True:
        print(f"\nWork Effort #{len(work_efforts) + 1}:")
        we_id = input("  ID: ").strip()
        if not we_id:
            break

        impact = float(input("  Impact (0-10): "))
        urgency = float(input("  Urgency (0-10): "))
        blocking = float(input("  Blocking (0-10): "))
        effort = float(input("  Effort (0-10, higher = more effort): "))

        score = calculate_priority_score(impact, urgency, blocking, effort)
        priority_emoji, priority_level = determine_priority_level(score)

        work_efforts.append(
            {
                "id": we_id,
                "impact": impact,
                "urgency": urgency,
                "blocking": blocking,
                "effort": effort,
                "score": score,
                "priority": priority_level,
            }
        )

        print(f"  ✅ Score: {score:.2f}/10 ({priority_emoji} {priority_level})")

    # Sort by score (descending)
    work_efforts.sort(key=lambda x: x["score"], reverse=True)

    print_priority_matrix(work_efforts)

    return work_efforts


def main():
    parser = argparse.ArgumentParser(description="Priority Matrix Calculator")
    parser.add_argument("--work-efforts", type=str, help="Comma-separated list of work effort IDs")
    parser.add_argument(
        "--scores",
        type=str,
        help="JSON object mapping work effort IDs to score arrays [impact, urgency, blocking, effort]",
    )
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--output", type=str, help="Output file path (markdown format)")

    args = parser.parse_args()

    if args.interactive:
        work_efforts = interactive_mode()
        if args.output:
            generate_markdown_report(work_efforts, args.output)
        return

    if not all([args.work_efforts, args.scores]):
        print("Error: --work-efforts and --scores are required (or use --interactive)")
        parser.print_help()
        return

    # Parse inputs
    we_ids = [w.strip() for w in args.work_efforts.split(",")]
    scores_data = json.loads(args.scores)

    # Calculate priority scores
    work_efforts = []
    for we_id in we_ids:
        if we_id not in scores_data:
            raise ValueError(f"Work effort '{we_id}' not found in scores")

        impact, urgency, blocking, effort = scores_data[we_id]
        score = calculate_priority_score(impact, urgency, blocking, effort)
        priority_emoji, priority_level = determine_priority_level(score)

        work_efforts.append(
            {
                "id": we_id,
                "impact": impact,
                "urgency": urgency,
                "blocking": blocking,
                "effort": effort,
                "score": score,
                "priority": priority_level,
            }
        )

    # Sort by score (descending)
    work_efforts.sort(key=lambda x: x["score"], reverse=True)

    print_priority_matrix(work_efforts)

    # Generate report if requested
    if args.output:
        generate_markdown_report(work_efforts, args.output)


if __name__ == "__main__":
    main()
