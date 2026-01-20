#!/usr/bin/env python3
"""
CLI wrapper for critique-and-revise command.

Usage:
    python scripts/critique_and_revise_plan.py [options]
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from waft.core.critique_and_revise import CritiqueAndReviseManager
import argparse


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Critique and revise plan documents - validate and revise plans based on critiques"
    )
    parser.add_argument(
        "--plan",
        type=Path,
        help="Path to plan file (default: most recent)"
    )
    parser.add_argument(
        "--plan-name",
        type=str,
        help="Name of plan to find (partial match)"
    )
    parser.add_argument(
        "--critique",
        type=Path,
        help="Path to critique file (default: most recent)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show revisions without applying"
    )
    parser.add_argument(
        "--severity",
        choices=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
        help="Only revise criticisms of this severity"
    )
    parser.add_argument(
        "--rollback",
        action="store_true",
        help="Rollback last revision"
    )
    
    args = parser.parse_args()
    
    project_path = Path.cwd()
    manager = CritiqueAndReviseManager(project_path)
    
    if args.rollback:
        result = manager.rollback_last_revision()
        return 0 if result.get("success") else 1
    
    try:
        result = manager.run_critique_and_revise(
            plan_path=args.plan,
            plan_name=args.plan_name,
            dry_run=args.dry_run,
            severity_filter=args.severity,
            critique_path=args.critique
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
