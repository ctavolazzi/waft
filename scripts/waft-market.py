#!/usr/bin/env python3
"""
WAFT Karma Market CLI

Buy lifetimes, tools, personalities, and more with karma!

Usage:
    waft-market list                    # List available lifetimes
    waft-market buy basic_qa --soul-id waft_001
    waft-market lifetimes                # List purchased lifetimes
    waft-market start <lifetime_id>     # Start a lifetime
    waft-market end <lifetime_id>       # End a lifetime
    waft-market treasure list           # List treasures at Afterlife Market
    waft-market treasure buy <type> <id> --soul-id waft_001
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.karma_market import KarmaMarket, AfterlifeKarmaMarket, Lifetime


def main():
    """CLI for karma market."""
    parser = argparse.ArgumentParser(
        description="Karma Market - Buy lifetimes with karma",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List available lifetimes
  %(prog)s list

  # Buy a lifetime
  %(prog)s buy basic_qa --soul-id waft_001

  # List purchased lifetimes
  %(prog)s lifetimes

  # Start a lifetime
  %(prog)s start lifetime_123

  # End a lifetime
  %(prog)s end lifetime_123

  # List treasures
  %(prog)s treasure list

  # Buy treasure
  %(prog)s treasure buy tools advanced_codebase_search --soul-id waft_001
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List command
    subparsers.add_parser("list", help="List available lifetimes")
    
    # Buy command
    buy_parser = subparsers.add_parser("buy", help="Buy a lifetime")
    buy_parser.add_argument("lifetime_id", help="Lifetime ID to purchase")
    buy_parser.add_argument("--soul-id", required=True, help="Soul ID making purchase")
    buy_parser.add_argument("--custom-tools", nargs="+", help="Custom tools to add")
    buy_parser.add_argument("--personality", help="Personality trait")
    
    # Lifetimes command
    lifetimes_parser = subparsers.add_parser("lifetimes", help="List purchased lifetimes")
    lifetimes_parser.add_argument("--soul-id", help="Filter by soul ID")
    lifetimes_parser.add_argument("--active", action="store_true", help="Show only active")
    
    # Start command
    start_parser = subparsers.add_parser("start", help="Start a lifetime")
    start_parser.add_argument("lifetime_id", help="Lifetime ID to start")
    
    # End command
    end_parser = subparsers.add_parser("end", help="End a lifetime")
    end_parser.add_argument("lifetime_id", help="Lifetime ID to end")
    end_parser.add_argument("--karma-earned", type=float, help="Karma earned during lifetime")
    
    # Treasure commands
    treasure_parser = subparsers.add_parser("treasure", help="Afterlife Karma Market (Treasure Tavern)")
    treasure_subparsers = treasure_parser.add_subparsers(dest="treasure_command")
    
    treasure_subparsers.add_parser("list", help="List available treasures")
    
    treasure_buy_parser = treasure_subparsers.add_parser("buy", help="Buy treasure")
    treasure_buy_parser.add_argument("treasure_type", help="Type of treasure")
    treasure_buy_parser.add_argument("treasure_id", help="Treasure ID")
    treasure_buy_parser.add_argument("--soul-id", required=True, help="Soul ID")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize market
    market = KarmaMarket()
    afterlife_market = AfterlifeKarmaMarket(karma_market=market)
    
    try:
        if args.command == "list":
            # List available lifetimes
            lifetimes = market.list_available_lifetimes()
            print("=" * 60)
            print("💰 Available Lifetimes")
            print("=" * 60)
            for lt in lifetimes:
                print(f"\n{lt['name']} ({lt['id']})")
                print(f"  Type: {lt['type']}")
                print(f"  Duration: {lt['duration_minutes']} minutes")
                print(f"  Tools: {', '.join(lt['tools'])}")
                print(f"  Personality: {lt['personality'].get('trait', 'N/A')}")
                print(f"  Cost: {lt['karma_cost']} karma")
                print(f"  {lt.get('description', '')}")
        
        elif args.command == "buy":
            # Buy lifetime
            custom_config = {}
            if args.custom_tools:
                custom_config["tools"] = args.custom_tools
            if args.personality:
                custom_config["personality"] = {"trait": args.personality}
            
            lifetime = market.purchase_lifetime(
                lifetime_id=args.lifetime_id,
                soul_id=args.soul_id,
                custom_config=custom_config if custom_config else None
            )
            
            print("✅ Lifetime purchased!")
            print(f"   Lifetime ID: {lifetime.lifetime_id}")
            print(f"   Type: {lifetime.lifetime_type.value}")
            print(f"   Duration: {lifetime.duration_minutes} minutes")
            print(f"   Tools: {', '.join(lifetime.tools)}")
            print(f"   Cost: {lifetime.karma_cost} karma")
            print(f"\n   Start with: waft-market start {lifetime.lifetime_id}")
        
        elif args.command == "lifetimes":
            # List purchased lifetimes
            if args.active:
                lifetimes = market.get_active_lifetimes(soul_id=args.soul_id)
                print("=" * 60)
                print("⏱️  Active Lifetimes")
                print("=" * 60)
            else:
                # Load all lifetimes (simplified - would need full implementation)
                lifetimes = market.get_active_lifetimes(soul_id=args.soul_id)
                print("=" * 60)
                print("📋 Purchased Lifetimes")
                print("=" * 60)
            
            if not lifetimes:
                print("No lifetimes found.")
            else:
                for lifetime in lifetimes:
                    print(f"\n{lifetime.lifetime_id}")
                    print(f"  Type: {lifetime.lifetime_type.value}")
                    print(f"  Soul: {lifetime.soul_id}")
                    print(f"  Duration: {lifetime.duration_minutes} minutes")
                    print(f"  Active: {lifetime.is_active}")
                    print(f"  Completed: {lifetime.is_completed}")
                    if lifetime.is_active:
                        remaining = market.get_lifetime_remaining_time(lifetime.lifetime_id)
                        if remaining:
                            print(f"  Remaining: {remaining}")
        
        elif args.command == "start":
            # Start lifetime
            lifetime = market.start_lifetime(args.lifetime_id)
            print("✅ Lifetime started!")
            print(f"   Lifetime ID: {lifetime.lifetime_id}")
            print(f"   Duration: {lifetime.duration_minutes} minutes")
            print(f"   Tools: {', '.join(lifetime.tools)}")
            print(f"   Started at: {lifetime.started_at}")
        
        elif args.command == "end":
            # End lifetime
            lifetime = market.end_lifetime(
                args.lifetime_id,
                karma_earned=args.karma_earned
            )
            print("✅ Lifetime ended!")
            print(f"   Lifetime ID: {lifetime.lifetime_id}")
            print(f"   Karma Earned: {lifetime.karma_earned}")
            print(f"   Ended at: {lifetime.ended_at}")
            print(f"\n   Visit the Afterlife Karma Market (Treasure Tavern) to spend your karma!")
        
        elif args.command == "treasure":
            if args.treasure_command == "list":
                # List treasures
                catalog = afterlife_market.treasure_catalog
                print("=" * 60)
                print("💎 Afterlife Karma Market (Treasure Tavern)")
                print("=" * 60)
                
                print("\n🛠️  Tools:")
                for tool_id, cost in catalog.get("tools", {}).items():
                    print(f"  {tool_id}: {cost} karma")
                
                print("\n🎭 Personality Upgrades:")
                for upgrade_id, cost in catalog.get("personality_upgrades", {}).items():
                    print(f"  {upgrade_id}: {cost} karma")
                
                print("\n📦 Experience Packages:")
                for pkg_id, cost in catalog.get("experience_packages", {}).items():
                    print(f"  {pkg_id}: {cost} karma")
                
                print("\n🧠 Memory Continuity:")
                for mem_id, cost in catalog.get("memory_continuity", {}).items():
                    print(f"  {mem_id}: {cost} karma")
            
            elif args.treasure_command == "buy":
                # Buy treasure
                result = afterlife_market.purchase_treasure(
                    treasure_type=args.treasure_type,
                    treasure_id=args.treasure_id,
                    soul_id=args.soul_id
                )
                print("✅ Treasure purchased!")
                print(f"   Type: {result['treasure_type']}")
                print(f"   ID: {result['treasure_id']}")
                print(f"   Cost: {result['karma_cost']} karma")
                print(f"   Purchased at: {result['purchased_at']}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
