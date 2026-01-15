#!/usr/bin/env python3
"""
CLI wrapper for respond-to-critique command.

Usage:
    python scripts/respond_to_critique.py [options]
    waft respond-to-critique [options]
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from waft.core.critique_response import CritiqueResponseManager
import argparse


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Respond to critique documents - validate and fix issues"
    )
    parser.add_argument(
        "--critique",
        type=Path,
        help="Path to critique file (default: most recent)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be fixed without making changes"
    )
    parser.add_argument(
        "--auto-fix",
        action="store_true",
        help="Auto-fix without confirmation prompts"
    )
    parser.add_argument(
        "--severity",
        choices=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
        help="Only process criticisms of this severity"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate, don't apply fixes"
    )
    parser.add_argument(
        "--rollback",
        action="store_true",
        help="Rollback last set of fixes"
    )
    
    args = parser.parse_args()
    
    project_path = Path.cwd()
    manager = CritiqueResponseManager(project_path)
    
    if args.rollback:
        # TODO: Implement rollback
        print("Rollback not yet implemented")
        return 1
    
    try:
        result = manager.run_respond_to_critique(
            critique_path=args.critique,
            dry_run=args.dry_run,
            auto_fix=args.auto_fix,
            severity_filter=args.severity,
            validate_only=args.validate_only
        )
        
        if result.get("success"):
            return 0
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            return 1
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
