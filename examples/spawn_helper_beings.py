"""
Spawn helper beings to assist with development tasks.

Creates a team of specialized beings with different skills and personalities.
"""

from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.being import BeingSystem
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def spawn_helper_team():
    """Spawn a team of helper beings with different specializations."""
    
    console.print("\n[bold bright_blue]╔════════════════════════════════════════╗[/bold bright_blue]")
    console.print("[bold bright_blue]║[/bold bright_blue]  [bold white]SPAWNING HELPER BEINGS[/bold white]  [bold bright_blue]║[/bold bright_blue]")
    console.print("[bold bright_blue]╚════════════════════════════════════════╝[/bold bright_blue]\n")
    
    # Initialize Being System
    project_path = Path(__file__).parent.parent
    being_system = BeingSystem(project_path=project_path)
    
    # Define helper beings with different specializations
    helpers = [
        {
            "name": "Code Analyst",
            "personality_type": "analytical",
            "skills": {
                "code_analysis": 45.0,
                "reasoning": 40.0,
                "pattern_recognition": 35.0,
                "debugging": 30.0
            },
            "description": "Specializes in analyzing code, finding patterns, and debugging"
        },
        {
            "name": "Documentation Specialist",
            "personality_type": "systematic",
            "skills": {
                "documentation": 50.0,
                "writing": 45.0,
                "organization": 40.0,
                "communication": 35.0
            },
            "description": "Helps with documentation, writing, and organizing information"
        },
        {
            "name": "Test Engineer",
            "personality_type": "systematic",
            "skills": {
                "testing": 45.0,
                "quality_assurance": 40.0,
                "automation": 35.0,
                "debugging": 30.0
            },
            "description": "Focuses on testing, QA, and ensuring code quality"
        },
        {
            "name": "Research Assistant",
            "personality_type": "analytical",
            "skills": {
                "research": 50.0,
                "investigation": 45.0,
                "information_gathering": 40.0,
                "analysis": 35.0
            },
            "description": "Helps with research, investigation, and information gathering"
        },
        {
            "name": "Creative Problem Solver",
            "personality_type": "creative",
            "skills": {
                "creativity": 45.0,
                "problem_solving": 40.0,
                "innovation": 35.0,
                "design": 30.0
            },
            "description": "Brings creative solutions and innovative approaches"
        }
    ]
    
    spawned_beings = []
    
    for helper in helpers:
        console.print(f"[bold cyan]Spawning {helper['name']}...[/bold cyan]")
        
        # Spawn being
        being = being_system.spawn_being(
            reality_id="helper_reality",
            initial_skills=helper["skills"]
        )
        
        # Set personality type (need to update after creation)
        being.personality_type = helper["personality_type"]
        being_system._save_being(being)
        
        spawned_beings.append({
            "being": being,
            "helper_info": helper
        })
        
        console.print(f"  [green]✓[/green] {being.being_id}")
        console.print(f"  [dim]  Personality: {being.personality_type}[/dim]")
        console.print(f"  [dim]  Stamina: {being.stamina:.1f}/{being.stamina_max:.1f}[/dim]")
        console.print(f"  [dim]  Skills: {len(being.skills)}[/dim]\n")
    
    # Display summary table
    console.print("\n[bold cyan]Helper Team Summary[/bold cyan]\n")
    
    table = Table(title="Spawned Helper Beings")
    table.add_column("Name", style="cyan")
    table.add_column("Being ID", style="dim")
    table.add_column("Personality", style="magenta")
    table.add_column("Top Skill", style="green")
    table.add_column("Stamina", justify="right", style="yellow")
    
    for item in spawned_beings:
        being = item["being"]
        helper = item["helper_info"]
        
        # Get top skill
        if being.skills:
            top_skill = max(being.skills.items(), key=lambda x: x[1])
            top_skill_display = f"{top_skill[0]}: {top_skill[1]:.1f}"
        else:
            top_skill_display = "None"
        
        table.add_row(
            helper["name"],
            being.being_id[:20] + "..." if len(being.being_id) > 20 else being.being_id,
            being.personality_type,
            top_skill_display,
            f"{being.stamina:.1f}"
        )
    
    console.print(table)
    
    # Display detailed skills
    console.print("\n[bold cyan]Detailed Skills[/bold cyan]\n")
    
    for item in spawned_beings:
        being = item["being"]
        helper = item["helper_info"]
        
        skills_table = Table(title=f"{helper['name']} Skills")
        skills_table.add_column("Skill", style="cyan")
        skills_table.add_column("Level", justify="right", style="green")
        
        for skill_name, skill_level in sorted(being.skills.items(), key=lambda x: x[1], reverse=True):
            skills_table.add_row(skill_name, f"{skill_level:.1f}")
        
        console.print(skills_table)
        console.print(f"[dim]{helper['description']}[/dim]\n")
    
    console.print(f"[bold green]✓ Successfully spawned {len(spawned_beings)} helper beings![/bold green]\n")
    
    return spawned_beings


if __name__ == "__main__":
    spawn_helper_team()
