#!/usr/bin/env python3
"""
Decision Matrix Calculator

Calculates weighted decision matrix scores for multiple options based on criteria.

Usage:
    python decision_matrix.py --criteria "Impact,Urgency,Blocking" --weights "0.4,0.3,0.3" --options "Option A,Option B,Option C"

    Or use interactive mode:
    python decision_matrix.py --interactive
"""

import argparse
import json


def calculate_weighted_score(scores: list[float], weights: list[float]) -> float:
    """Calculate weighted sum score."""
    if len(scores) != len(weights):
        raise ValueError("Scores and weights must have same length")
    if abs(sum(weights) - 1.0) > 0.01:
        raise ValueError(f"Weights must sum to 1.0 (got {sum(weights)})")

    return sum(score * weight for score, weight in zip(scores, weights))


def evaluate_options(
    options: list[str], criteria: list[str], weights: list[float], scores: dict[str, list[float]]
) -> list[tuple[str, float]]:
    """Evaluate all options and return ranked list."""
    results = []

    for option in options:
        if option not in scores:
            raise ValueError(f"Option '{option}' not found in scores")

        option_scores = scores[option]
        if len(option_scores) != len(criteria):
            raise ValueError(
                f"Option '{option}' has {len(option_scores)} scores, expected {len(criteria)}"
            )

        weighted_score = calculate_weighted_score(option_scores, weights)
        results.append((option, weighted_score))

    # Sort by score (descending)
    results.sort(key=lambda x: x[1], reverse=True)
    return results


def print_matrix(
    options: list[str],
    criteria: list[str],
    weights: list[float],
    scores: dict[str, list[float]],
    results: list[tuple[str, float]],
):
    """Print formatted decision matrix."""
    print("\n" + "=" * 80)
    print("DECISION MATRIX")
    print("=" * 80)

    # Header
    header = f"{'Option':<30}"
    for criterion in criteria:
        header += f"{criterion:<15}"
    header += f"{'Weighted Score':<15}"
    print(header)
    print("-" * 80)

    # Weights row
    weights_row = f"{'Weights':<30}"
    for weight in weights:
        weights_row += f"{weight:<15.2f}"
    weights_row += f"{'':<15}"
    print(weights_row)
    print("-" * 80)

    # Options and scores
    for option, weighted_score in results:
        row = f"{option:<30}"
        option_scores = scores[option]
        for score in option_scores:
            row += f"{score:<15.2f}"
        row += f"{weighted_score:<15.2f}"
        print(row)

    print("=" * 80)
    print(f"\n🏆 RECOMMENDED: {results[0][0]} (Score: {results[0][1]:.2f}/10)")
    print("=" * 80 + "\n")


def interactive_mode():
    """Interactive mode for entering decision matrix data."""
    print("\n" + "=" * 80)
    print("DECISION MATRIX CALCULATOR - Interactive Mode")
    print("=" * 80 + "\n")

    # Get criteria
    criteria_input = input("Enter criteria (comma-separated): ").strip()
    criteria = [c.strip() for c in criteria_input.split(",")]
    print(f"Criteria: {criteria}\n")

    # Get weights
    weights_input = input(
        f"Enter weights for {len(criteria)} criteria (comma-separated, must sum to 1.0): "
    ).strip()
    weights = [float(w.strip()) for w in weights_input.split(",")]

    if abs(sum(weights) - 1.0) > 0.01:
        print(f"⚠️  Warning: Weights sum to {sum(weights)}, not 1.0. Normalizing...")
        total = sum(weights)
        weights = [w / total for w in weights]

    print(f"Weights: {weights} (sum: {sum(weights):.2f})\n")

    # Get options
    options_input = input("Enter options (comma-separated): ").strip()
    options = [o.strip() for o in options_input.split(",")]
    print(f"Options: {options}\n")

    # Get scores for each option
    scores = {}
    print("Enter scores for each option (0-10 scale, comma-separated):")
    print("=" * 80)

    for option in options:
        print(f"\n{option}:")
        scores_input = input(f"  Scores for {len(criteria)} criteria: ").strip()
        option_scores = [float(s.strip()) for s in scores_input.split(",")]
        scores[option] = option_scores

    # Calculate and display results
    results = evaluate_options(options, criteria, weights, scores)
    print_matrix(options, criteria, weights, scores, results)

    return results


def main():
    parser = argparse.ArgumentParser(description="Decision Matrix Calculator")
    parser.add_argument("--criteria", type=str, help="Comma-separated list of criteria")
    parser.add_argument(
        "--weights", type=str, help="Comma-separated list of weights (must sum to 1.0)"
    )
    parser.add_argument("--options", type=str, help="Comma-separated list of options")
    parser.add_argument("--scores", type=str, help="JSON object mapping options to score arrays")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--output", type=str, help="Output file path (JSON format)")

    args = parser.parse_args()

    if args.interactive:
        results = interactive_mode()
        if args.output:
            with open(args.output, "w") as f:
                json.dump([{"option": opt, "score": score} for opt, score in results], f, indent=2)
        return

    if not all([args.criteria, args.weights, args.options, args.scores]):
        print(
            "Error: --criteria, --weights, --options, and --scores are required (or use --interactive)"
        )
        parser.print_help()
        return

    # Parse inputs
    criteria = [c.strip() for c in args.criteria.split(",")]
    weights = [float(w.strip()) for w in args.weights.split(",")]
    options = [o.strip() for o in args.options.split(",")]
    scores = json.loads(args.scores)

    # Normalize weights if needed
    if abs(sum(weights) - 1.0) > 0.01:
        print(f"⚠️  Warning: Weights sum to {sum(weights)}, not 1.0. Normalizing...")
        total = sum(weights)
        weights = [w / total for w in weights]

    # Calculate results
    results = evaluate_options(options, criteria, weights, scores)
    print_matrix(options, criteria, weights, scores, results)

    # Output to file if requested
    if args.output:
        with open(args.output, "w") as f:
            json.dump([{"option": opt, "score": score} for opt, score in results], f, indent=2)
        print(f"✅ Results saved to {args.output}")


if __name__ == "__main__":
    main()
