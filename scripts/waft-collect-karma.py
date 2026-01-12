#!/usr/bin/env python3
"""
WAFT Karma Collector CLI

Collect karma from completed life logs and experiences.

Usage:
    waft-collect-karma                    # Collect all pending
    waft-collect-karma --soul-id waft_001  # Collect for specific soul
    waft-collect-karma --file life_log.json --soul-id waft_001
    waft-collect-karma --stats             # Show collection statistics
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.karma_collector import KarmaCollector


def main():
    """CLI for karma collection."""
    parser = argparse.ArgumentParser(
        description="Collect karma from completed life logs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Collect all pending life logs
  %(prog)s

  # Collect for specific soul
  %(prog)s --soul-id waft_001

  # Collect from specific file
  %(prog)s --file life_log.json --soul-id waft_001

  # Show statistics
  %(prog)s --stats
        """
    )
    
    parser.add_argument(
        "--soul-id",
        help="Soul ID to collect karma for (collects all if not specified)"
    )
    
    parser.add_argument(
        "--file",
        type=Path,
        help="Path to specific life log file to collect from"
    )
    
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show collection statistics"
    )
    
    parser.add_argument(
        "--project-path",
        type=Path,
        help="Project path (defaults to current directory)"
    )
    
    args = parser.parse_args()
    
    # Initialize collector
    collector = KarmaCollector(project_path=args.project_path)
    
    try:
        if args.stats:
            # Show statistics
            stats = collector.get_collection_stats()
            print("=" * 60)
            print("💰 Karma Collection Statistics")
            print("=" * 60)
            print(f"Total Collected: {stats['total_collected']} lifetimes")
            print(f"Total Karma Collected: {stats['total_karma_collected']:.2f} karma")
            print(f"Pending Life Logs: {stats['pending_life_logs']}")
            print(f"Souls in Akasha: {stats['souls_in_akasha']}")
            
        elif args.file:
            # Collect from specific file
            if not args.soul_id:
                print("❌ Error: --soul-id required when using --file")
                return 1
            
            result = collector.collect_from_life_log_file(args.file, args.soul_id)
            print("✅ Karma collected!")
            print(f"   Soul ID: {result['soul_id']}")
            print(f"   Lifetime ID: {result['lifetime_id']}")
            print(f"   Karma Collected: {result['karma_collected']:.2f}")
            print(f"   Total Karma: {result['total_karma']:.2f}")
            
        else:
            # Collect all pending
            print("🔍 Scanning for pending life logs...")
            results = collector.collect_all_pending(soul_id=args.soul_id)
            
            if not results:
                print("✅ No pending life logs to collect.")
            else:
                print(f"✅ Collected karma from {len(results)} life log(s):")
                total_karma = 0.0
                for result in results:
                    print(f"\n   Soul: {result['soul_id']}")
                    print(f"   Lifetime: {result['lifetime_id']}")
                    print(f"   Karma: {result['karma_collected']:.2f}")
                    print(f"   Total: {result['total_karma']:.2f}")
                    total_karma += result['karma_collected']
                
                print(f"\n💰 Total karma collected: {total_karma:.2f}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
