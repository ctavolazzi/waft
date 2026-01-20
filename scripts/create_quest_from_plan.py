#!/usr/bin/env python3
"""
Create Quest from Plan

CLI tool to create a quest from a plan document.
Can be used manually or as a hook after plan creation.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console

from src.waft.core.plan_quest_integration import (
    create_quests_for_all_plans,
    hook_into_plan_creation,
)

console = Console()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Create Quest from Plan document")
    parser.add_argument(
        "plan_path", nargs="?", type=Path, help="Path to plan file (optional if using --all)"
    )
    parser.add_argument("--all", action="store_true", help="Create quests for all plans")
    parser.add_argument(
        "--plans-dir", type=Path, help="Plans directory (default: _work_efforts/Plans/)"
    )
    parser.add_argument(
        "--project-path", type=Path, help="Project root path (default: current directory)"
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        default=True,
        help="Skip plans that already have quests (default: True)",
    )
    parser.add_argument(
        "--no-skip-existing",
        action="store_false",
        dest="skip_existing",
        help="Create quests even if they already exist",
    )

    args = parser.parse_args()

    project_path = args.project_path or Path.cwd()

    if args.all:
        # Create quests for all plans
        console.print("[bold]Creating quests for all plans...[/bold]")
        quests = create_quests_for_all_plans(
            plans_dir=args.plans_dir, project_path=project_path, skip_existing=args.skip_existing
        )

        console.print(f"[green]✅ Created {len(quests)} quests[/green]")
        for quest in quests:
            console.print(f"  • {quest['name']} (ID: {quest['id']})")
    elif args.plan_path:
        # Create quest from specific plan
        plan_path = Path(args.plan_path)
        if not plan_path.is_absolute():
            plan_path = project_path / plan_path

        console.print(f"[bold]Creating quest from plan: {plan_path}[/bold]")

        quest = hook_into_plan_creation(plan_path, project_path)

        if quest:
            console.print(f"[green]✅ Quest created: {quest['name']}[/green]")
            console.print(f"  ID: {quest['id']}")
            console.print(f"  Difficulty: {quest['difficulty']}/10")
            console.print(f"  Rewards: {quest['loot_table']}")
            console.print(f"  Todos: {len(quest['todos'])}")
        else:
            console.print("[red]❌ Failed to create quest[/red]")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
