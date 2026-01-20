#!/usr/bin/env python3
"""
Create Quest (Fae-Guided)

CLI tool to create a whimsical quest for open-ended, creative work.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console

from src.waft.pantheon.fae import Fae

console = Console()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Create a whimsical Quest (Fae-guided)")
    parser.add_argument(
        "description", nargs="?", help="Quest description (open-ended, creative work)"
    )
    parser.add_argument(
        "--name", type=str, help="Quest name (auto-generated from description if not provided)"
    )
    parser.add_argument(
        "--fae-guidance", type=str, help="Fae blessing/guidance (auto-generated if not provided)"
    )
    parser.add_argument(
        "--difficulty", type=int, help="Quest difficulty (1-10, auto-calculated if not provided)"
    )
    parser.add_argument(
        "--project-path", type=Path, help="Project root path (default: current directory)"
    )
    parser.add_argument("--from-plan", type=Path, help="Create quest from plan file")

    args = parser.parse_args()

    project_path = args.project_path or Path.cwd()
    fae = Fae(project_path)

    if args.from_plan:
        # Create from plan
        from src.waft.core.quest_mission_integration import create_quest_from_plan

        plan_path = Path(args.from_plan)
        if not plan_path.is_absolute():
            plan_path = project_path / plan_path

        console.print(f"[bold]Creating quest from plan: {plan_path}[/bold]")
        quest_data = create_quest_from_plan(plan_path, project_path)

        console.print(f"[green]✅ Quest created: {quest_data['name']}[/green]")
        console.print(f"  ID: {quest_data['id']}")
        console.print(f"  Fae Guidance: {quest_data.get('fae_guidance', 'N/A')}")
        console.print(f"  Difficulty: {quest_data.get('difficulty', 'N/A')}/10")
    elif args.description:
        # Create from description
        name = args.name or args.description[:50]

        console.print(f"[bold]Creating quest: {name}[/bold]")
        quest = fae.create_quest(
            name=name,
            description=args.description,
            fae_guidance=args.fae_guidance,
            difficulty=args.difficulty,
        )

        console.print(f"[green]✅ Quest created: {quest.name}[/green]")
        console.print(f"  ID: {quest.quest_id}")
        console.print(f"  Fae Guidance: {quest.fae_guidance}")
        console.print(f"  Difficulty: {quest.difficulty}/10")
        console.print(f"  Status: {quest.status}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
