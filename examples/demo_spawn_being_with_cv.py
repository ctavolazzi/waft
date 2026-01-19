"""
Demo: Spawn Being with CV Generation

Demonstrates the new /spawn-with-cv functionality by creating a Being
with skills, memories, and experiences, then generating a professional CV.
"""

from pathlib import Path
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.core.spawn_with_cv import spawn_being_with_cv
from waft.being import BeingSystem
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def main():
    """Create a demo Being with CV."""
    project_path = Path(__file__).parent.parent
    
    console.print(Panel.fit(
        "[bold cyan]Being CV Generation Demo[/bold cyan]\n"
        "Creating a Being with skills, memories, and a professional CV...",
        border_style="cyan"
    ))
    console.print()
    
    # Create Being with interesting skills
    initial_skills = {
        "documentation": 75.0,
        "organization": 80.0,
        "bureaucracy": 70.0,
        "typst": 60.0,
        "python": 65.0,
        "project_management": 70.0,
        "communication": 75.0,
    }
    
    console.print("[yellow]→[/yellow] Spawning Being with skills...")
    console.print(f"   Skills: {', '.join(initial_skills.keys())}")
    console.print()
    
    # Spawn Being with CV
    try:
        result = spawn_being_with_cv(
            project_path=project_path,
            reality_id="bureaucracy_realm",
            initial_skills=initial_skills,
            generate_pdf=False  # Skip PDF for now due to template API
        )
        
        being = result["being"]
        personnel_dir = result["personnel_file_path"]
        cv_typ_path = result["cv_typ_path"]
        cv_pdf_path = result["cv_pdf_path"]
        bureaucracy_record = result["bureaucracy_record"]
        
        # Add some memories to make the CV more interesting
        console.print("[yellow]→[/yellow] Adding work experiences (memories)...")
        
        being.record_memory(
            "Senior Documentation Specialist at WAFT Framework. Led documentation efforts, created comprehensive API documentation, implemented automated documentation generation, and managed technical writing team of 3 Beings.",
            memory_type="work",
            metadata={
                "title": "Senior Documentation Specialist",
                "context": "WAFT Framework",
                "timestamp": "2025-01-15T10:00:00",
                "reality_id": "bureaucracy_realm",
                "details": [
                    "Led documentation efforts for WAFT framework",
                    "Created comprehensive API documentation",
                    "Implemented automated documentation generation",
                    "Managed technical writing team of 3 Beings"
                ],
                "tags": ["experience", "work", "leadership"]
            }
        )
        
        being.record_memory(
            "Bureaucracy System Architect at Bureaucracy Realm. Designed personnel file management system, implemented CV generation pipeline, created BureaucracyGod entity, and established realm governance protocols.",
            memory_type="work",
            metadata={
                "title": "Bureaucracy System Architect",
                "context": "Bureaucracy Realm",
                "timestamp": "2024-06-01T10:00:00",
                "reality_id": "bureaucracy_realm",
                "details": [
                    "Designed personnel file management system",
                    "Implemented CV generation pipeline",
                    "Created BureaucracyGod entity",
                    "Established realm governance protocols"
                ],
                "tags": ["experience", "work", "architecture"]
            }
        )
        
        being.record_memory(
            "Template Integration Expert. Integrated brilliant-cv template v3.1.1, created Being-to-CV mapping system, and developed automated CV generation workflow.",
            memory_type="achievement",
            metadata={
                "title": "Template Integration Expert",
                "context": "Typst Templates",
                "timestamp": "2024-03-01T10:00:00",
                "reality_id": "bureaucracy_realm",
                "details": [
                    "Integrated brilliant-cv template v3.1.1",
                    "Created Being-to-CV mapping system",
                    "Developed automated CV generation workflow"
                ],
                "tags": ["achievement", "expertise"]
            }
        )
        
        # Add lessons learned
        being.learn_lesson(
            "Well-documented systems enable better Being evolution. Comprehensive documentation helps Beings understand and evolve systems more effectively.",
            outcome="success",
            metadata={
                "title": "Documentation is Critical",
                "tags": ["documentation", "evolution"]
            }
        )
        
        being.learn_lesson(
            "Structured processes allow managing many Beings efficiently. Bureaucratic systems, while seemingly rigid, enable scalable Being management.",
            outcome="success",
            metadata={
                "title": "Bureaucracy Enables Scale",
                "tags": ["bureaucracy", "scale"]
            }
        )
        
        # Save Being with new memories
        being_system = BeingSystem(project_path=project_path)
        being_system.save_being(being)
        
        # Regenerate CV with new data
        console.print("[yellow]→[/yellow] Regenerating CV with updated Being data...")
        from waft.templates.typst.wrappers.brilliant_cv import generate_brilliant_cv
        
        cv_typ_path = generate_brilliant_cv(
            being=being,
            output_dir=personnel_dir,
            language="en"
        )
        
        console.print()
        console.print(Panel.fit(
            "[bold green]✓ Being Created Successfully![/bold green]",
            border_style="green"
        ))
        console.print()
        
        # Display Being information
        table = Table(title="Being Information", show_header=True, header_style="bold magenta")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Being ID", being.being_id)
        table.add_row("Name", being.custom_name or "N/A")
        table.add_row("Reality", being.reality_id)
        table.add_row("State", being.state.value)
        table.add_row("Fitness", f"{being.fitness:.2f}")
        table.add_row("Lifetimes", str(being.lifetimes))
        table.add_row("Skills Count", str(len(being.skills)))
        table.add_row("Memories Count", str(len(being.memories)))
        table.add_row("Lessons Count", str(len(being.lessons_learned)))
        
        console.print(table)
        console.print()
        
        # Display file locations
        file_table = Table(title="Generated Files", show_header=True, header_style="bold blue")
        file_table.add_column("File", style="cyan")
        file_table.add_column("Path", style="white")
        
        file_table.add_row("Personnel Directory", str(personnel_dir))
        file_table.add_row("CV Typst Source", str(cv_typ_path))
        if cv_pdf_path and cv_pdf_path.exists():
            file_table.add_row("CV PDF", str(cv_pdf_path))
        else:
            file_table.add_row("CV PDF", "[yellow]Not generated (template API needs adjustment)[/yellow]")
        
        console.print(file_table)
        console.print()
        
        # Display bureaucracy registration
        if bureaucracy_record:
            console.print(Panel(
                f"[bold]Bureaucracy Registration[/bold]\n\n"
                f"Being registered with BureaucracyGod\n"
                f"CV Version: {bureaucracy_record.cv_version}\n"
                f"Registered: {bureaucracy_record.registered_at}",
                border_style="yellow"
            ))
            console.print()
        
        # Display top skills
        if being.skills:
            skills_table = Table(title="Top Skills", show_header=True, header_style="bold green")
            skills_table.add_column("Skill", style="cyan")
            skills_table.add_column("Level", style="white", justify="right")
            
            top_skills = sorted(being.skills.items(), key=lambda x: x[1], reverse=True)[:5]
            for skill, level in top_skills:
                skills_table.add_row(skill.replace("_", " ").title(), f"{level:.1f}")
            
            console.print(skills_table)
            console.print()
        
        console.print(Panel.fit(
            "[bold]Next Steps[/bold]\n\n"
            f"1. View CV Typst source: [cyan]{cv_typ_path}[/cyan]\n"
            f"2. Check personnel file: [cyan]{personnel_dir}[/cyan]\n"
            f"3. Being ID: [cyan]{being.being_id}[/cyan]",
            border_style="blue"
        ))
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
