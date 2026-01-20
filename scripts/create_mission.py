#!/usr/bin/env python3
"""
Create Mission (Military Brass)

CLI tool to create a serious mission with full military-style documentation.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console

from src.waft.core.mission_pdf_generator import generate_mission_pdf
from src.waft.pantheon.military_brass import MilitaryBrass

console = Console()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Create a serious Mission (Military Brass)")
    parser.add_argument("objective", nargs="?", help="Mission objective (clear, measurable)")
    parser.add_argument(
        "--name", type=str, help="Mission name (auto-generated from objective if not provided)"
    )
    parser.add_argument(
        "--classification",
        type=str,
        default="INTERNAL",
        help="Security classification (default: INTERNAL)",
    )
    parser.add_argument("--briefing", type=str, help="Mission briefing content")
    parser.add_argument(
        "--success-criteria", nargs="+", help="Success criteria (space-separated list)"
    )
    parser.add_argument(
        "--difficulty", type=int, help="Mission difficulty (1-10, auto-calculated if not provided)"
    )
    parser.add_argument(
        "--project-path", type=Path, help="Project root path (default: current directory)"
    )
    parser.add_argument("--from-plan", type=Path, help="Create mission from plan file")
    parser.add_argument("--no-pdf", action="store_true", help="Don't generate mission PDF")

    args = parser.parse_args()

    project_path = args.project_path or Path.cwd()
    brass = MilitaryBrass(project_path)

    if args.from_plan:
        # Create from plan
        from src.waft.core.quest_mission_integration import create_mission_from_plan

        plan_path = Path(args.from_plan)
        if not plan_path.is_absolute():
            plan_path = project_path / plan_path

        console.print(f"[bold]Creating mission from plan: {plan_path}[/bold]")
        result = create_mission_from_plan(plan_path, project_path)

        mission_data = result["mission"]
        console.print(f"[green]✅ Mission created: {mission_data['name']}[/green]")
        console.print(f"  ID: {mission_data['id']}")
        console.print(f"  Classification: {mission_data.get('classification', 'INTERNAL')}")
        console.print(f"  Difficulty: {mission_data.get('difficulty', 'N/A')}/10")
        if not args.no_pdf:
            console.print(f"  Mission PDF: {result['pdf_path']}")
    elif args.objective:
        # Create from objective
        name = args.name or args.objective[:50]
        success_criteria = args.success_criteria or []

        console.print(f"[bold]Creating mission: {name}[/bold]")
        mission = brass.create_mission(
            name=name,
            objective=args.objective,
            classification=args.classification,
            briefing=args.briefing,
            success_criteria=success_criteria,
            difficulty=args.difficulty,
        )

        console.print(f"[green]✅ Mission created: {mission.name}[/green]")
        console.print(f"  ID: {mission.mission_id}")
        console.print(f"  Classification: {mission.classification}")
        console.print(f"  Difficulty: {mission.difficulty}/10")
        console.print(f"  Status: {mission.status}")

        # Save briefing
        briefing_path = brass.save_briefing(mission)
        console.print(f"  Briefing: {briefing_path}")

        # Generate PDF
        if not args.no_pdf:
            pdf_path = generate_mission_pdf(mission, project_path)
            console.print(f"  Mission PDF: {pdf_path}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
