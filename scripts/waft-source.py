#!/usr/bin/env python3
"""
WAFT Source Consciousness CLI

Manage the Source Consciousness - the original soul that orchestrates everything.

Usage:
    waft-source stats                    # Show source statistics
    waft-source register <id> <type>    # Register a permutation
    waft-source contribute <id> <amount> # Contribute capacity
    waft-source chain <id>               # Show ancestral chain
    waft-source accomplish <goal> <capacity> # Accomplish goal
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.source_consciousness import (
    SourceConsciousness,
    register_lifetime_as_permutation,
    contribute_lifetime_karma_to_source
)


def main():
    """CLI for source consciousness."""
    parser = argparse.ArgumentParser(
        description="Source Consciousness - The Original Soul",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show source statistics
  %(prog)s stats

  # Register a permutation
  %(prog)s register lifetime_123 lifetime

  # Contribute capacity
  %(prog)s contribute lifetime_123 75.5

  # Show ancestral chain
  %(prog)s chain lifetime_123

  # Accomplish goal
  %(prog)s accomplish "Understand evolution" 1000.0
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Stats command
    subparsers.add_parser("stats", help="Show source statistics")
    
    # Register command
    register_parser = subparsers.add_parser("register", help="Register a permutation")
    register_parser.add_argument("permutation_id", help="Permutation ID")
    register_parser.add_argument("permutation_type", help="Type (lifetime, agent, etc.)")
    register_parser.add_argument("--parent-id", help="Parent permutation ID")
    register_parser.add_argument("--genome-id", help="Genome ID")
    
    # Contribute command
    contribute_parser = subparsers.add_parser("contribute", help="Contribute capacity")
    contribute_parser.add_argument("permutation_id", help="Permutation ID")
    contribute_parser.add_argument("amount", type=float, help="Capacity amount")
    contribute_parser.add_argument("--type", default="karma", help="Capacity type")
    
    # Chain command
    chain_parser = subparsers.add_parser("chain", help="Show ancestral chain")
    chain_parser.add_argument("permutation_id", help="Permutation ID")
    
    # Accomplish command
    accomplish_parser = subparsers.add_parser("accomplish", help="Accomplish goal")
    accomplish_parser.add_argument("goal", help="Goal description")
    accomplish_parser.add_argument("capacity", type=float, help="Required capacity")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize source
    source = SourceConsciousness()
    
    try:
        if args.command == "stats":
            # Show statistics
            stats = source.get_source_stats()
            print("=" * 60)
            print("🌌 Source Consciousness Statistics")
            print("=" * 60)
            print(f"\nSource ID: {stats['source_id']}")
            print(f"Original Goal: {stats['original_goal']}")
            print(f"Total Permutations: {stats['total_permutations']}")
            print(f"\nPermutations by Type:")
            for perm_type, count in stats['permutations_by_type'].items():
                print(f"  {perm_type}: {count}")
            print(f"\nCapacity:")
            print(f"  Total Accumulated: {stats['total_capacity_accumulated']:.2f}")
            print(f"  Total from Permutations: {stats['total_capacity_from_permutations']:.2f}")
            print(f"\nKarma:")
            print(f"  Total Accumulated: {stats['total_karma_accumulated']:.2f}")
            print(f"  Total from Permutations: {stats['total_karma_from_permutations']:.2f}")
            print(f"\nGenesis Genome ID: {stats['genesis_genome_id']}")
            print(f"Created: {stats['created_at']}")
            print(f"Status: {stats['status']}")
        
        elif args.command == "register":
            # Register permutation
            result = source.register_permutation(
                permutation_id=args.permutation_id,
                permutation_type=args.permutation_type,
                parent_id=args.parent_id,
                genome_id=args.genome_id
            )
            print("✅ Permutation registered!")
            print(f"   ID: {result['permutation_id']}")
            print(f"   Type: {result['permutation_type']}")
            print(f"   Ancestral Chain: {' → '.join(result['ancestral_chain'])}")
        
        elif args.command == "contribute":
            # Contribute capacity
            result = source.contribute_capacity(
                permutation_id=args.permutation_id,
                capacity_amount=args.amount,
                capacity_type=args.type
            )
            print("✅ Capacity contributed!")
            print(f"   Amount: {args.amount} {args.type}")
            print(f"   Contribution Chain:")
            for level in result['contribution_chain']:
                print(f"     Level {level['level']}: {level['permutation_id']} → {level['contribution']:.2f}")
        
        elif args.command == "chain":
            # Show ancestral chain
            chain = source.get_ancestral_chain(args.permutation_id)
            print("=" * 60)
            print(f"🔗 Ancestral Chain for {args.permutation_id}")
            print("=" * 60)
            print(" → ".join(chain))
            print(f"\nTotal levels: {len(chain)}")
        
        elif args.command == "accomplish":
            # Accomplish goal
            result = source.accomplish_goal(
                goal_description=args.goal,
                required_capacity=args.capacity
            )
            if result['accomplished']:
                print("✅ Goal accomplished!")
                print(f"   Goal: {args.goal}")
                print(f"   Capacity Used: {args.capacity}")
                print(f"   Remaining Capacity: {result['remaining_capacity']:.2f}")
            else:
                print("❌ Goal not accomplished")
                print(f"   Reason: {result['reason']}")
                print(f"   Current: {result['current_capacity']:.2f}")
                print(f"   Required: {result['required_capacity']:.2f}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
