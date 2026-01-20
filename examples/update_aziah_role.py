"""
Update Aziah Calderon's Role and Promotion

Updates Aziah to Lead Scientist (first hiring round), then promotes him
to Head of Research & Development.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from waft.being import BeingSystem
from waft.core.teleport_massive_corp import TeleportMassiveCorp

console = Console()


def main():
    """Update Aziah's role and create promotion documentation."""
    project_path = Path(__file__).parent.parent

    console.print(
        Panel.fit(
            "[bold cyan]Updating Aziah Calderon's Role[/bold cyan]\n"
            "[dim]Lead Scientist → Head of Research & Development[/dim]",
            border_style="cyan",
        )
    )
    console.print()

    # Find Aziah
    being_system = BeingSystem(project_path=project_path)
    aziah_id = "being_20260119_021114_3e6f3a88"  # From previous creation

    try:
        aziah = being_system._load_being(aziah_id)
        console.print(f"[green]✓[/green] Loaded Aziah: {aziah.custom_name}")
    except Exception as e:
        console.print(f"[red]Error loading Aziah: {e}[/red]")
        return 1

    # Initialize Teleport Massive
    corp = TeleportMassiveCorp(project_path=project_path)

    # Update role to Lead Scientist (initial hire)
    console.print("[yellow]→[/yellow] Setting initial role: Lead Scientist...")

    # Remove old assignment and create new one
    manifest = json.loads(corp.manifest_path.read_text(encoding="utf-8"))
    manifest["employees"] = [e for e in manifest["employees"] if e["being_id"] != aziah_id]

    # Assign as Lead Scientist (first hiring round)
    initial_assignment = {
        "being_id": aziah_id,
        "role": "Lead Scientist",
        "department": "Research & Development",
        "title": "Lead Scientist",
        "level": 7,  # Senior level
        "assigned_at": "2026-01-18T00:00:00",
        "status": "active",
        "hiring_round": "First Hiring Round - January 2026",
        "cohort": "Founding Research Team",
    }
    manifest["employees"].append(initial_assignment)

    # Ensure R&D department exists
    rnd_dept = next(
        (d for d in manifest["departments"] if d["name"] == "Research & Development"), None
    )
    if not rnd_dept:
        manifest["departments"].append(
            {
                "name": "Research & Development",
                "created_at": "2026-01-18T00:00:00",
                "employees": [aziah_id],
            }
        )
    elif aziah_id not in rnd_dept["employees"]:
        rnd_dept["employees"].append(aziah_id)

    corp.manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    console.print(
        Panel(
            "[bold]Initial Role Assignment[/bold]\n\n"
            "Name: [cyan]Aziah Calderon[/cyan]\n"
            "Role: [yellow]Lead Scientist[/yellow]\n"
            "Department: [yellow]Research & Development[/yellow]\n"
            "Level: [yellow]7 (Senior)[/yellow]\n"
            "Hiring Round: [yellow]First Hiring Round - January 2026[/yellow]\n"
            "Cohort: [yellow]Founding Research Team[/yellow]",
            border_style="green",
        )
    )
    console.print()

    # Create promotion record
    promotion_date = "2026-02-15"  # Promoted about a month later

    console.print("[yellow]→[/yellow] Creating promotion to Head of R&D...")

    # Update to Head of R&D
    for emp in manifest["employees"]:
        if emp["being_id"] == aziah_id:
            emp["role"] = "Head of Research & Development"
            emp["title"] = "Head of Research & Development"
            emp["level"] = 9  # Executive level
            emp["promoted_at"] = f"{promotion_date}T00:00:00"
            emp["previous_role"] = "Lead Scientist"
            emp["promotion_reason"] = (
                "Exceptional performance and leadership in early research phase"
            )
            break

    corp.manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    console.print(
        Panel(
            f"[bold]Promotion Record[/bold]\n\n"
            f"Name: [cyan]Aziah Calderon[/cyan]\n"
            f"Previous Role: [yellow]Lead Scientist[/yellow]\n"
            f"New Role: [bold yellow]Head of Research & Development[/bold yellow]\n"
            f"Promotion Date: [yellow]{promotion_date}[/yellow]\n"
            f"New Level: [yellow]9 (Executive)[/yellow]\n"
            f"Reason: Exceptional performance and leadership",
            border_style="yellow",
        )
    )
    console.print()

    # Create hiring round documentation
    console.print("[yellow]→[/yellow] Creating first hiring round documentation...")

    hiring_round_path = corp.docs_path / "first_hiring_round_january_2026.md"
    hiring_round_content = f"""# First Hiring Round - January 2026

**Date**: January 18, 2026
**Purpose**: Establish core Research & Development team
**Positions Filled**: 3 Lead Scientists

## Overview

Teleport Massive's first major hiring initiative focused on building the foundational Research & Development team. Three Lead Scientists were hired to establish the core research capabilities needed for quantum teleportation technology development.

## Hired Candidates

### 1. Aziah Calderon
- **Position**: Lead Scientist
- **Background**: MS Quantum Physics, 4+ years research experience
- **Specialization**: Quantum teleportation protocols
- **Status**: Promoted to Head of R&D on {promotion_date}

### 2. [To be assigned]
- **Position**: Lead Scientist
- **Status**: Pending assignment

### 3. [To be assigned]
- **Position**: Lead Scientist
- **Status**: Pending assignment

## Hiring Criteria

- Advanced degree in Physics, Quantum Mechanics, or related field
- Minimum 3 years research experience
- Demonstrated expertise in quantum systems
- Strong problem-solving and analytical skills
- Ability to work in fast-paced startup environment

## Outcomes

The first hiring round successfully established the Research & Development department with three highly qualified Lead Scientists. This team formed the foundation for Teleport Massive's core technology development.

## Notes

All three Lead Scientists were part of the "Founding Research Team" cohort, playing critical roles in the early development phase of Teleport Massive's teleportation technology.
"""
    hiring_round_path.write_text(hiring_round_content, encoding="utf-8")
    console.print(f"   [green]✓[/green] Hiring Round Doc: {hiring_round_path.name}")

    # Create promotion announcement
    promotion_path = (
        corp.docs_path / f"promotion_aziah_calderon_{promotion_date.replace('-', '')}.md"
    )
    promotion_content = f"""# Promotion Announcement - Aziah Calderon

**Date**: {promotion_date}
**Employee**: Aziah Calderon
**Previous Role**: Lead Scientist
**New Role**: Head of Research & Development

## Promotion Details

Effective {promotion_date}, Aziah Calderon has been promoted from Lead Scientist to Head of Research & Development.

## Rationale

Aziah has demonstrated exceptional performance and leadership during the critical early research phase. His expertise in quantum teleportation protocols, combined with his ability to coordinate research efforts, makes him the ideal candidate to lead the Research & Development department.

## Responsibilities

As Head of Research & Development, Aziah will be responsible for:

- Leading all research and development initiatives
- Coordinating the Research & Development team
- Setting research priorities and strategic direction
- Overseeing quantum teleportation protocol development
- Reporting directly to executive leadership
- Managing research budgets and resources

## Impact

This promotion recognizes Aziah's critical contributions to Teleport Massive's core technology development and positions him to drive the company's research agenda forward.

## Notes

Aziah was one of three Lead Scientists hired in the first hiring round (January 18, 2026). His rapid promotion reflects both his exceptional capabilities and the company's growth trajectory.
"""
    promotion_path.write_text(promotion_content, encoding="utf-8")
    console.print(f"   [green]✓[/green] Promotion Announcement: {promotion_path.name}")

    # Update employee profile
    personnel_dir = Path(f"_hidden/.truth/beings/{aziah_id}/personnel")
    if personnel_dir.exists():
        profile_path = personnel_dir / "employee_profile.md"
        if profile_path.exists():
            profile_content = profile_path.read_text(encoding="utf-8")
            # Update the role information
            profile_content = profile_content.replace(
                "**Position**: Quantum Teleportation Research Engineer",
                "**Position**: Head of Research & Development",
            )
            profile_content = profile_content.replace(
                "**Level**: 3 (Junior-Mid Level)", "**Level**: 9 (Executive Level)"
            )
            profile_content += f"""

## Promotion History

### Head of Research & Development
- **Start Date**: {promotion_date}
- **Previous Role**: Lead Scientist
- **Reason**: Exceptional performance and leadership

### Lead Scientist
- **Start Date**: 2026-01-18
- **Hiring Round**: First Hiring Round - January 2026
- **Cohort**: Founding Research Team
- **Status**: Promoted
"""
            profile_path.write_text(profile_content, encoding="utf-8")
            console.print("   [green]✓[/green] Updated Employee Profile")

    console.print()

    # Display final status
    final_table = Table(
        title="Aziah Calderon - Current Status", show_header=True, header_style="bold magenta"
    )
    final_table.add_column("Property", style="cyan")
    final_table.add_column("Value", style="white")

    final_table.add_row("Name", "Aziah Calderon")
    final_table.add_row("Current Role", "Head of Research & Development")
    final_table.add_row("Department", "Research & Development")
    final_table.add_row("Level", "9 (Executive)")
    final_table.add_row("Hire Date", "2026-01-18")
    final_table.add_row("Initial Role", "Lead Scientist")
    final_table.add_row("Promotion Date", promotion_date)
    final_table.add_row("Hiring Round", "First Hiring Round - January 2026")
    final_table.add_row("Cohort", "Founding Research Team")

    console.print(final_table)
    console.print()

    console.print(
        Panel.fit(
            "[bold]✓ Aziah Calderon Updated![/bold]\n\n"
            f"Current Role: [bold yellow]Head of Research & Development[/bold yellow]\n"
            f"Level: [yellow]9 (Executive)[/yellow]\n"
            f"Promoted: {promotion_date}\n\n"
            f"Ready for the story to begin! 🚀",
            border_style="green",
        )
    )

    return 0


if __name__ == "__main__":
    import json

    sys.exit(main())
