"""
Teleport Massive Corporation - Worldbuilding Demo

Creates a Being with a role in Teleport Massive and generates
corporate documentation using Typst templates.
"""

from pathlib import Path
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.core.spawn_with_cv import spawn_being_with_cv
from waft.core.teleport_massive_corp import TeleportMassiveCorp
from waft.being import BeingSystem
from waft.pantheon.bureaucracy_god import BureaucracyGod
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

console = Console()


def main():
    """Create Teleport Massive corporation worldbuilding demo."""
    project_path = Path(__file__).parent.parent
    
    console.print(Panel.fit(
        "[bold cyan]🚀 Teleport Massive Corporation[/bold cyan]\n"
        "[dim]Worldbuilding through Documentation[/dim]",
        border_style="cyan"
    ))
    console.print()
    
    # Initialize Teleport Massive
    console.print("[yellow]→[/yellow] Initializing Teleport Massive Corporation...")
    corp = TeleportMassiveCorp(project_path=project_path)
    console.print(f"   Corporate HQ: [cyan]{corp.corp_path}[/cyan]")
    console.print()
    
    # Create or load Being
    being_id = "being_20260119_020735_3e6f3a88"  # From previous demo
    being_system = BeingSystem(project_path=project_path)
    
    try:
        being = being_system._load_being(being_id)
        console.print(f"[green]✓[/green] Loaded existing Being: {being_id}")
    except:
        # Create new Being if doesn't exist
        console.print("[yellow]→[/yellow] Creating new Being for Teleport Massive...")
        result = spawn_being_with_cv(
            project_path=project_path,
            reality_id="bureaucracy_realm",
            initial_skills={
                "documentation": 85.0,
                "corporate_writing": 80.0,
                "bureaucracy": 90.0,
                "worldbuilding": 75.0,
                "typst": 70.0,
                "project_management": 75.0,
            },
            generate_pdf=False
        )
        being = result["being"]
        being_id = being.being_id
        console.print(f"[green]✓[/green] Created Being: {being_id}")
    
    console.print()
    
    # Assign role to Being
    console.print("[yellow]→[/yellow] Assigning role to Being...")
    role_assignment = corp.assign_being_role(
        being_id=being_id,
        role="Corporate Documentation Specialist",
        department="Bureaucracy & Documentation",
        title="Senior Documentation Architect",
        level=7
    )
    
    console.print(Panel(
        f"[bold]Role Assignment[/bold]\n\n"
        f"Being: [cyan]{being_id}[/cyan]\n"
        f"Role: [yellow]{role_assignment['role']}[/yellow]\n"
        f"Department: [yellow]{role_assignment['department']}[/yellow]\n"
        f"Title: [yellow]{role_assignment['title']}[/yellow]\n"
        f"Level: [yellow]{role_assignment['level']}[/yellow]",
        border_style="green"
    ))
    console.print()
    
    # Create corporate documents
    console.print("[yellow]→[/yellow] Generating corporate documentation...")
    
    # 1. Corporate Mission Statement
    mission_report = corp.create_corporate_report(
        report_type="mission",
        title="Corporate Mission Statement",
        content={
            "body": """
# Corporate Mission

Teleport Massive Corporation is dedicated to revolutionizing transportation 
through the development and deployment of instant teleportation technology. 
We believe that distance should never be a barrier to human connection, 
commerce, or exploration.

## Our Vision

A world where anyone can be anywhere, instantly. Where the boundaries of 
space and time dissolve, enabling unprecedented freedom of movement and 
opportunity.

## Core Values

- **Innovation**: Pushing the boundaries of what's possible
- **Safety**: Ensuring every teleportation is secure and reliable
- **Accessibility**: Making teleportation available to all
- **Sustainability**: Zero-emission transportation for a better planet
"""
        },
        author_being_id=being_id
    )
    console.print(f"   [green]✓[/green] Mission Statement: {mission_report.name}")
    
    # 2. Department Structure
    dept_report = corp.create_corporate_report(
        report_type="structure",
        title="Organizational Structure",
        content={
            "body": """
# Teleport Massive Organizational Structure

## Executive Leadership
- CEO: [To be assigned]
- CTO: [To be assigned]
- CFO: [To be assigned]

## Departments

### Bureaucracy & Documentation
- **Purpose**: Maintain corporate records, policies, and documentation
- **Head**: Senior Documentation Architect
- **Employees**: 1 (and growing)

### Research & Development
- **Purpose**: Develop and improve teleportation technology
- **Status**: Forming

### Operations
- **Purpose**: Manage teleportation network operations
- **Status**: Forming

### Legal & Compliance
- **Purpose**: Ensure regulatory compliance and safety standards
- **Status**: Forming
"""
        },
        author_being_id=being_id
    )
    console.print(f"   [green]✓[/green] Org Structure: {dept_report.name}")
    
    # 3. Worldbuilding Notes
    worldbuilding_path = corp.worldbuilding_path / "corporate_history.md"
    worldbuilding_path.write_text(f"""# Teleport Massive - Corporate History

## Founding

Teleport Massive was founded on {datetime.now().strftime('%B %d, %Y')} with a 
vision to revolutionize transportation through instant teleportation technology.

## Early Days

The corporation began in the Bureaucracy Realm, where meticulous documentation 
and structured processes enabled rapid growth and innovation.

## Key Milestones

- **{datetime.now().strftime('%Y-%m-%d')}**: Corporation founded
- **{datetime.now().strftime('%Y-%m-%d')}**: First employee hired (Being {being_id})
- **{datetime.now().strftime('%Y-%m-%d')}**: Bureaucracy & Documentation department established

## Technology

Teleport Massive's core technology enables instant transportation of matter 
across any distance. The technology is still in development, with safety and 
reliability being the top priorities.

## Future Plans

- Expand research and development capabilities
- Establish teleportation network infrastructure
- Develop safety protocols and regulatory compliance
- Scale operations globally
""", encoding="utf-8")
    console.print(f"   [green]✓[/green] Worldbuilding Notes: {worldbuilding_path.name}")
    
    console.print()
    
    # Display corporate structure
    structure = corp.get_corporate_structure()
    
    tree = Tree("[bold cyan]Teleport Massive Corporation[/bold cyan]")
    
    # Departments
    dept_branch = tree.add("[bold yellow]Departments[/bold yellow]")
    for dept in structure.get("departments", []):
        dept_node = dept_branch.add(f"[cyan]{dept['name']}[/cyan]")
        dept_node.add(f"Employees: {len(dept.get('employees', []))}")
    
    # Employees
    emp_branch = tree.add("[bold yellow]Employees[/bold yellow]")
    for emp in structure.get("employees", []):
        emp_node = emp_branch.add(f"[green]{emp['title']}[/green]")
        emp_node.add(f"Department: {emp['department']}")
        emp_node.add(f"Level: {emp['level']}")
        emp_node.add(f"Being ID: {emp['being_id']}")
    
    # Documents
    doc_branch = tree.add("[bold yellow]Documents[/bold yellow]")
    for doc in structure.get("documents", []):
        doc_branch.add(f"[dim]{doc['type']}: {doc['title']}[/dim]")
    
    console.print(tree)
    console.print()
    
    console.print(Panel.fit(
        "[bold]🎉 Teleport Massive Corporation Established![/bold]\n\n"
        f"Corporate HQ: [cyan]{corp.corp_path}[/cyan]\n"
        f"First Employee: [cyan]{being_id}[/cyan]\n"
        f"Documents Created: {len(structure.get('documents', []))}\n\n"
        "[dim]Ready for worldbuilding through documentation![/dim]",
        border_style="green"
    ))
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
