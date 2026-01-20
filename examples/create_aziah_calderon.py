"""
Create Aziah Calderon - Teleport Massive Employee

Creates Aziah Calderon as a Being, generates his CV, resume, application,
and assigns him to Teleport Massive Corporation.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from waft.being import BeingSystem
from waft.core.spawn_with_cv import spawn_being_with_cv
from waft.core.teleport_massive_corp import TeleportMassiveCorp
from waft.templates.typst.wrappers.brilliant_cv import generate_brilliant_cv

console = Console()


def main():
    """Create Aziah Calderon and generate all his documentation."""
    project_path = Path(__file__).parent.parent

    console.print(
        Panel.fit(
            "[bold red]Creating Aziah Calderon[/bold red]\n"
            "[dim]Born 1997 | Joining Teleport Massive January 18, 2026[/dim]",
            border_style="red",
        )
    )
    console.print()

    # Aziah's background
    birth_year = 1997
    birth_date = f"{birth_year}-03-15"  # March 15, 1997
    join_date = "2026-01-18"
    current_age = 2026 - birth_year  # 29 years old

    console.print("[yellow]→[/yellow] Creating Being: Aziah Calderon")
    console.print(f"   Born: {birth_date} (Age: {current_age})")
    console.print(f"   Joining: {join_date}")
    console.print()

    # Skills appropriate for someone joining a quantum teleportation startup
    # He's 29, so he'd have some experience but not too senior
    initial_skills = {
        "quantum_physics": 65.0,
        "quantum_computing": 60.0,
        "research": 70.0,
        "data_analysis": 68.0,
        "python": 72.0,
        "mathematics": 75.0,
        "problem_solving": 70.0,
        "communication": 65.0,
        "teamwork": 60.0,
        "documentation": 55.0,
    }

    # Spawn Aziah as a Being
    result = spawn_being_with_cv(
        project_path=project_path,
        reality_id="bureaucracy_realm",
        initial_skills=initial_skills,
        generate_pdf=False,
    )

    being = result["being"]
    being.custom_name = "Aziah Calderon"
    being_system = BeingSystem(project_path=project_path)
    being_system.save_being(being)

    console.print(f"[green]✓[/green] Created Being: {being.being_id}")
    console.print(f"   Name: [cyan]{being.custom_name}[/cyan]")
    console.print()

    # Add background memories (work experience)
    console.print("[yellow]→[/yellow] Adding background and work experience...")

    # Education
    being.record_memory(
        "Bachelor of Science in Physics, specializing in Quantum Mechanics. Graduated with honors. Thesis on quantum entanglement applications.",
        memory_type="education",
        metadata={
            "title": "Bachelor of Science in Physics",
            "institution": "State University",
            "timestamp": "2015-09-01T00:00:00",
            "end_timestamp": "2019-06-15T00:00:00",
            "location": "United States",
            "details": [
                "Specialized in Quantum Mechanics",
                "Graduated with honors (Magna Cum Laude)",
                "Thesis: 'Quantum Entanglement Applications in Information Theory'",
                "Relevant coursework: Quantum Computing, Advanced Mathematics, Statistical Mechanics",
            ],
            "tags": ["education", "physics", "quantum"],
        },
    )

    being.record_memory(
        "Master of Science in Quantum Physics. Focused on quantum teleportation protocols and theoretical foundations.",
        memory_type="education",
        metadata={
            "title": "Master of Science in Quantum Physics",
            "institution": "Tech Institute",
            "timestamp": "2019-09-01T00:00:00",
            "end_timestamp": "2021-06-15T00:00:00",
            "location": "United States",
            "details": [
                "Focused on quantum teleportation protocols",
                "Research in theoretical quantum mechanics",
                "Published 2 papers on quantum state transfer",
                "Graduate research assistant",
            ],
            "tags": ["education", "graduate", "quantum", "research"],
        },
    )

    # Work Experience
    being.record_memory(
        "Research Assistant at Quantum Research Lab. Worked on quantum state manipulation and teleportation experiments.",
        memory_type="work",
        metadata={
            "title": "Research Assistant",
            "institution": "Quantum Research Lab",
            "timestamp": "2021-07-01T00:00:00",
            "end_timestamp": "2023-12-31T00:00:00",
            "location": "Research Facility",
            "details": [
                "Conducted quantum state manipulation experiments",
                "Assisted in quantum teleportation protocol development",
                "Analyzed experimental data and wrote research reports",
                "Collaborated with international research teams",
                "Published findings in peer-reviewed journals",
            ],
            "tags": ["experience", "work", "research", "quantum"],
        },
    )

    being.record_memory(
        "Junior Quantum Engineer at Tech Startup. Developed quantum algorithms and worked on early-stage teleportation research.",
        memory_type="work",
        metadata={
            "title": "Junior Quantum Engineer",
            "institution": "QuantumTech Innovations",
            "timestamp": "2024-01-15T00:00:00",
            "end_timestamp": "2025-12-31T00:00:00",
            "location": "San Francisco, CA",
            "details": [
                "Developed quantum algorithms for state transfer",
                "Worked on early-stage teleportation research",
                "Built simulation tools for quantum systems",
                "Collaborated with engineering team on prototype development",
                "Presented research findings to investors",
            ],
            "tags": ["experience", "work", "engineering", "startup", "quantum"],
        },
    )

    # Add lessons learned
    being.learn_lesson(
        "Quantum teleportation requires perfect entanglement. Even small decoherence can cause catastrophic failures.",
        outcome="success",
        metadata={
            "title": "Quantum Entanglement Precision",
            "tags": ["quantum", "technical", "research"],
        },
    )

    being.learn_lesson(
        "Startups move fast, but quantum research requires patience. Finding the balance is key.",
        outcome="partial",
        metadata={"title": "Startup vs Research Pace", "tags": ["career", "startup", "workplace"]},
    )

    # Save Being with all memories
    being_system.save_being(being)
    console.print(
        f"[green]✓[/green] Added {len(being.memories)} memories and {len(being.lessons_learned)} lessons"
    )
    console.print()

    # Generate CV
    console.print("[yellow]→[/yellow] Generating CV and resume...")
    personnel_dir = result["personnel_file_path"]
    cv_typ_path = generate_brilliant_cv(being=being, output_dir=personnel_dir, language="en")
    console.print(f"   [green]✓[/green] CV generated: {cv_typ_path.name}")

    # Create application documents
    console.print("[yellow]→[/yellow] Creating application documents...")

    # Job Application
    application_path = personnel_dir / "job_application.md"
    application_content = f"""# Job Application - Aziah Calderon

**Position Applied For**: Quantum Teleportation Research Engineer  
**Date**: {join_date}  
**Applicant**: Aziah Calderon  
**Date of Birth**: {birth_date}  
**Age**: {current_age}

## Cover Letter

Dear Teleport Massive Hiring Team,

I am writing to express my strong interest in the Quantum Teleportation Research Engineer position at Teleport Massive. With a Master's degree in Quantum Physics and over four years of experience in quantum research and engineering, I am excited about the opportunity to contribute to your groundbreaking work in teleportation technology.

My background includes hands-on experience with quantum state manipulation, teleportation protocols, and quantum algorithm development. At QuantumTech Innovations, I worked on early-stage teleportation research and developed simulation tools that advanced our understanding of quantum state transfer.

I am particularly drawn to Teleport Massive's mission of revolutionizing transportation through instant teleportation. The technical challenges and potential impact of this technology align perfectly with my research interests and career goals.

I am eager to bring my expertise in quantum mechanics, research methodology, and problem-solving to your team. I believe my combination of theoretical knowledge and practical experience makes me an ideal candidate for this role.

Thank you for considering my application. I look forward to the opportunity to discuss how I can contribute to Teleport Massive's success.

Sincerely,  
Aziah Calderon

## Application Details

- **Position**: Quantum Teleportation Research Engineer
- **Desired Start Date**: {join_date}
- **Salary Expectations**: Competitive, based on experience
- **Availability**: Immediate
- **Work Authorization**: Authorized to work in the United States

## References

Available upon request.
"""
    application_path.write_text(application_content, encoding="utf-8")
    console.print(f"   [green]✓[/green] Job Application: {application_path.name}")

    # Resume (simplified version)
    resume_path = personnel_dir / "resume.md"
    resume_content = f"""# Aziah Calderon - Resume

**Email**: aziah.calderon@email.com  
**Phone**: (555) 123-4567  
**Location**: San Francisco, CA  
**Date of Birth**: {birth_date}  
**Age**: {current_age}

## Professional Summary

Quantum Physics researcher and engineer with {current_age - 22} years of experience in quantum mechanics, teleportation protocols, and algorithm development. Seeking to contribute expertise to Teleport Massive's revolutionary teleportation technology.

## Education

**Master of Science in Quantum Physics**  
Tech Institute | 2019-2021  
- Focus: Quantum teleportation protocols
- Published 2 research papers
- Graduate research assistant

**Bachelor of Science in Physics**  
State University | 2015-2019  
- Specialization: Quantum Mechanics
- Graduated Magna Cum Laude
- Thesis on quantum entanglement

## Professional Experience

**Junior Quantum Engineer**  
QuantumTech Innovations | Jan 2024 - Dec 2025  
- Developed quantum algorithms for state transfer
- Built simulation tools for quantum systems
- Collaborated on prototype development

**Research Assistant**  
Quantum Research Lab | Jul 2021 - Dec 2023  
- Conducted quantum state manipulation experiments
- Assisted in teleportation protocol development
- Published findings in peer-reviewed journals

## Skills

- Quantum Physics & Mechanics
- Quantum Computing
- Python Programming
- Data Analysis
- Research Methodology
- Problem Solving
- Mathematical Modeling

## Publications

- "Quantum State Transfer in Noisy Environments" (2023)
- "Entanglement Protocols for Long-Distance Teleportation" (2022)
"""
    resume_path.write_text(resume_content, encoding="utf-8")
    console.print(f"   [green]✓[/green] Resume: {resume_path.name}")

    # Employee Profile
    profile_path = personnel_dir / "employee_profile.md"
    profile_content = f"""# Employee Profile - Aziah Calderon

**Employee ID**: {being.being_id}  
**Full Name**: Aziah Calderon  
**Date of Birth**: {birth_date}  
**Age**: {current_age}  
**Hire Date**: {join_date}  
**Department**: Research & Development  
**Position**: Quantum Teleportation Research Engineer  
**Level**: 3 (Junior-Mid Level)

## Personal Information

- **Name**: Aziah Calderon
- **Born**: {birth_date} ({current_age} years old)
- **Nationality**: American
- **Education**: MS Quantum Physics, BS Physics

## Employment History

### Teleport Massive Corporation
- **Start Date**: {join_date}
- **Position**: Quantum Teleportation Research Engineer
- **Department**: Research & Development
- **Status**: Active

### Previous Employment
- QuantumTech Innovations (2024-2025)
- Quantum Research Lab (2021-2023)

## Skills Assessment

- Quantum Physics: 65/100
- Quantum Computing: 60/100
- Research: 70/100
- Data Analysis: 68/100
- Python: 72/100
- Mathematics: 75/100

## Notes

New hire joining the Research & Development team. Strong background in quantum mechanics and teleportation protocols. Expected to contribute to core technology development.
"""
    profile_path.write_text(profile_content, encoding="utf-8")
    console.print(f"   [green]✓[/green] Employee Profile: {profile_path.name}")

    console.print()

    # Assign to Teleport Massive
    console.print("[yellow]→[/yellow] Assigning to Teleport Massive...")
    corp = TeleportMassiveCorp(project_path=project_path)

    role_assignment = corp.assign_being_role(
        being_id=being.being_id,
        role="Quantum Teleportation Research Engineer",
        department="Research & Development",
        title="Junior Quantum Engineer",
        level=3,
    )

    console.print(
        Panel(
            f"[bold]Role Assignment[/bold]\n\n"
            f"Name: [cyan]Aziah Calderon[/cyan]\n"
            f"Being ID: [dim]{being.being_id}[/dim]\n"
            f"Role: [yellow]{role_assignment['role']}[/yellow]\n"
            f"Department: [yellow]{role_assignment['department']}[/yellow]\n"
            f"Title: [yellow]{role_assignment['title']}[/yellow]\n"
            f"Level: [yellow]{role_assignment['level']}[/yellow]\n"
            f"Start Date: [yellow]{join_date}[/yellow]",
            border_style="green",
        )
    )
    console.print()

    # Display summary
    table = Table(
        title="Aziah Calderon - Documentation", show_header=True, header_style="bold magenta"
    )
    table.add_column("Document", style="cyan")
    table.add_column("Path", style="white")

    table.add_row("CV (Typst)", str(cv_typ_path))
    table.add_row("Job Application", str(application_path))
    table.add_row("Resume", str(resume_path))
    table.add_row("Employee Profile", str(profile_path))

    console.print(table)
    console.print()

    console.print(
        Panel.fit(
            "[bold]✓ Aziah Calderon Created Successfully![/bold]\n\n"
            f"Born: {birth_date} (Age {current_age})\n"
            f"Joined Teleport Massive: {join_date}\n"
            f"Position: Quantum Teleportation Research Engineer\n"
            f"Department: Research & Development\n\n"
            f"All documentation generated in:\n"
            f"[cyan]{personnel_dir}[/cyan]",
            border_style="green",
        )
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
