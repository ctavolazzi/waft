#!/usr/bin/env python3
"""
WAFT Karmic Wager CLI

Place bets on hypotheses, fitness outcomes, study results, and more using karma.

Usage:
    waft-bet hypothesis "Component evolution improves quality" 100
    waft-bet fitness "Fitness > 0.8" 50 --threshold 0.8
    waft-bet stats
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.karmic_wager import (
    KarmicWagerSystem,
    WagerType,
    wager_on_hypothesis,
    wager_on_fitness,
    wager_on_study_outcome
)


def main():
    """CLI for karmic wagers."""
    parser = argparse.ArgumentParser(
        description="Place karmic wagers on WAFT hypotheses and outcomes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Bet on hypothesis
  %(prog)s hypothesis "Component evolution improves quality" 100

  # Bet on fitness score
  %(prog)s fitness "Fitness above 0.8" 50 --threshold 0.8 --direction above

  # Bet on study outcome
  %(prog)s study "Study will succeed" 75 --min-findings 3

  # View stats
  %(prog)s stats

  # List active wagers
  %(prog)s list
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Hypothesis wager
    hyp_parser = subparsers.add_parser("hypothesis", help="Bet on hypothesis")
    hyp_parser.add_argument("hypothesis", help="The hypothesis")
    hyp_parser.add_argument("karma", type=float, help="Karma amount to wager")
    hyp_parser.add_argument("--prediction", choices=["confirmed", "refuted"], default="confirmed",
                           help="Predict confirmed or refuted (default: confirmed)")
    hyp_parser.add_argument("--odds", type=float, default=2.0,
                           help="Payout multiplier (default: 2.0)")
    
    # Fitness wager
    fit_parser = subparsers.add_parser("fitness", help="Bet on fitness score")
    fit_parser.add_argument("description", help="Description of fitness being measured")
    fit_parser.add_argument("karma", type=float, help="Karma amount to wager")
    fit_parser.add_argument("--threshold", type=float, required=True,
                           help="Fitness threshold")
    fit_parser.add_argument("--direction", choices=["above", "below"], default="above",
                           help="Direction: above or below threshold (default: above)")
    fit_parser.add_argument("--odds", type=float, default=1.5,
                           help="Payout multiplier (default: 1.5)")
    
    # Study outcome wager
    study_parser = subparsers.add_parser("study", help="Bet on study outcome")
    study_parser.add_argument("description", help="Description of study")
    study_parser.add_argument("karma", type=float, help="Karma amount to wager")
    study_parser.add_argument("--min-findings", type=int, default=1,
                            help="Minimum findings for success (default: 1)")
    study_parser.add_argument("--min-conclusions", type=int, default=1,
                            help="Minimum conclusions for success (default: 1)")
    study_parser.add_argument("--odds", type=float, default=1.5,
                            help="Payout multiplier (default: 1.5)")
    
    # Stats command
    subparsers.add_parser("stats", help="Show wager statistics")
    
    # List command
    subparsers.add_parser("list", help="List active wagers")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize wager system
    wager_system = KarmicWagerSystem()
    
    try:
        if args.command == "hypothesis":
            wager = wager_on_hypothesis(
                wager_system,
                hypothesis=args.hypothesis,
                karma_amount=args.karma,
                prediction=(args.prediction == "confirmed"),
                odds=args.odds
            )
            print(f"✅ Wager placed!")
            print(f"   ID: {wager.wager_id}")
            print(f"   Hypothesis: {args.hypothesis}")
            print(f"   Prediction: {args.prediction}")
            print(f"   Karma: {args.karma}")
            print(f"   Potential payout: {args.karma * args.odds} karma")
            
        elif args.command == "fitness":
            wager = wager_on_fitness(
                wager_system,
                description=args.description,
                karma_amount=args.karma,
                threshold=args.threshold,
                direction=args.direction,
                odds=args.odds
            )
            print(f"✅ Wager placed!")
            print(f"   ID: {wager.wager_id}")
            print(f"   Description: {args.description}")
            print(f"   Fitness {args.direction} {args.threshold}")
            print(f"   Karma: {args.karma}")
            print(f"   Potential payout: {args.karma * args.odds} karma")
            
        elif args.command == "study":
            wager = wager_on_study_outcome(
                wager_system,
                study_description=args.description,
                karma_amount=args.karma,
                success_criteria={
                    "min_findings": args.min_findings,
                    "min_conclusions": args.min_conclusions
                },
                odds=args.odds
            )
            print(f"✅ Wager placed!")
            print(f"   ID: {wager.wager_id}")
            print(f"   Study: {args.description}")
            print(f"   Karma: {args.karma}")
            print(f"   Potential payout: {args.karma * args.odds} karma")
            
        elif args.command == "stats":
            stats = wager_system.get_wager_stats()
            print("=" * 60)
            print("💰 Karmic Wager Statistics")
            print("=" * 60)
            print(f"Total Wagered: {stats['total_wagered']:.1f} karma")
            print(f"Total Won: {stats['total_won']:.1f} karma")
            print(f"Total Lost: {stats['total_lost']:.1f} karma")
            print(f"Net Karma: {stats['net_karma']:.1f} karma")
            print(f"Win Rate: {stats['win_rate']:.1%}")
            print(f"Won: {stats['won_count']} | Lost: {stats['lost_count']}")
            print(f"Active Wagers: {stats['active_wagers']}")
            print(f"Total Wagers: {stats['total_wagers']}")
            
        elif args.command == "list":
            wagers = wager_system.get_active_wagers()
            if not wagers:
                print("No active wagers.")
            else:
                print("=" * 60)
                print(f"💰 Active Wagers ({len(wagers)})")
                print("=" * 60)
                for wager in wagers:
                    print(f"\n{wager.wager_id}")
                    print(f"  Type: {wager.wager_type.value}")
                    print(f"  Description: {wager.description}")
                    print(f"  Karma: {wager.karma_amount}")
                    print(f"  Created: {wager.created_at}")
        
        return 0
        
    except InsufficientKarmaError as e:
        print(f"❌ {e}")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
