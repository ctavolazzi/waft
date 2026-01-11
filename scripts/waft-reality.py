#!/usr/bin/env python3
"""
WAFT Reality System CLI

Manage realities - simulation environments where beings can learn and evolve.

Usage:
    waft-reality create learning --config config.json
    waft-reality start <reality_id>
    waft-reality end <reality_id>
    waft-reality list
    waft-reality spawn <reality_id> --being-id being_123
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.reality import RealitySystem, RealityType


def main():
    """CLI for reality system."""
    parser = argparse.ArgumentParser(
        description="Reality System - Simulation Environments",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a reality")
    create_parser.add_argument("reality_type", choices=[rt.value for rt in RealityType])
    create_parser.add_argument("--config", type=Path, help="Configuration file")
    
    # Start command
    start_parser = subparsers.add_parser("start", help="Start a reality")
    start_parser.add_argument("reality_id", help="Reality ID")
    
    # End command
    end_parser = subparsers.add_parser("end", help="End a reality")
    end_parser.add_argument("reality_id", help="Reality ID")
    
    # List command
    subparsers.add_parser("list", help="List realities")
    
    # Spawn command
    spawn_parser = subparsers.add_parser("spawn", help="Spawn being into reality")
    spawn_parser.add_argument("reality_id", help="Reality ID")
    spawn_parser.add_argument("--being-id", help="Being ID")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    reality_system = RealitySystem()
    
    try:
        if args.command == "create":
            config = {}
            if args.config:
                import json
                with open(args.config, "r") as f:
                    config = json.load(f)
            
            reality = reality_system.create_reality(
                reality_type=RealityType(args.reality_type),
                configuration=config
            )
            print(f"✅ Reality created: {reality.reality_id}")
        
        elif args.command == "start":
            reality = reality_system.start_reality(args.reality_id)
            print(f"✅ Reality started: {reality.reality_id}")
        
        elif args.command == "end":
            reality = reality_system.end_reality(args.reality_id)
            print(f"✅ Reality ended: {reality.reality_id}")
        
        elif args.command == "list":
            realities = reality_system.get_active_realities()
            print(f"Active Realities: {len(realities)}")
            for r in realities:
                print(f"  {r.reality_id} ({r.reality_type.value})")
        
        elif args.command == "spawn":
            result = reality_system.spawn_being_into_reality(
                args.reality_id,
                args.being_id or f"being_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            print(f"✅ Being spawned: {result['being_id']}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    from datetime import datetime
    sys.exit(main())
