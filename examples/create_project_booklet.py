#!/usr/bin/env python3
"""
WAFT Project Booklet Generator

Creates a comprehensive booklet containing all PDFs in the project,
organized into logical sections with cover, table of contents, and dividers.
"""

from pathlib import Path
from datetime import datetime
from typing import List, Dict
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.binder import Binder, DocumentEntry
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def find_all_pdfs(project_root: Path) -> List[Path]:
    """Find all PDF files in the project."""
    pdfs = []
    for pdf_path in project_root.rglob("*.pdf"):
        # Skip temp files and very small files (likely empty)
        if pdf_path.stat().st_size > 1000:  # At least 1KB
            pdfs.append(pdf_path)
    return sorted(pdfs)


def categorize_pdf(pdf_path: Path, project_root: Path) -> Dict[str, str]:
    """Categorize a PDF into a section based on its path."""
    rel_path = pdf_path.relative_to(project_root)
    path_str = str(rel_path)
    
    # Extract title from filename
    title = pdf_path.stem.replace("_", " ").title()
    
    # Determine section based on path
    if "docs/" in path_str:
        section = "Documentation"
        description = "Project documentation and guides"
    elif "showcase_documents" in path_str or "wild_showcase" in path_str:
        section = "Showcase Documents"
        description = "Example documents demonstrating WAFT templates"
    elif "lightcone_binder" in path_str:
        section = "Project Lightcone"
        description = "PROJECT LIGHTCONE Master File documents"
    elif "demo" in path_str.lower():
        section = "Demos"
        description = "Demonstration outputs and examples"
    elif "_work_efforts" in path_str:
        section = "Work Efforts"
        description = "Work effort documentation and reports"
    elif "_fracture" in path_str:
        section = "Artifacts"
        description = "Historical artifacts and genesis documents"
    else:
        section = "Other"
        description = "Miscellaneous documents"
    
    return {
        "section": section,
        "title": title,
        "description": description,
        "path": pdf_path
    }


def create_project_booklet(project_root: Path, output_path: Path) -> Path:
    """
    Create a comprehensive booklet containing all project PDFs.
    
    Args:
        project_root: Root directory of the project
        output_path: Where to save the booklet
        
    Returns:
        Path to generated booklet
    """
    console.print("\n[bold cyan]📚 WAFT Project Booklet Generator[/bold cyan]\n")
    
    # Find all PDFs
    console.print("  [cyan]🔍[/cyan] Scanning for PDF files...")
    all_pdfs = find_all_pdfs(project_root)
    console.print(f"     [green]✅[/green] Found [bold]{len(all_pdfs)}[/bold] PDF files\n")
    
    if not all_pdfs:
        console.print("[yellow]⚠️[/yellow]  No PDF files found in project")
        return None
    
    # Categorize PDFs
    console.print("  [cyan]📂[/cyan] Categorizing PDFs...")
    categorized = {}
    for pdf_path in all_pdfs:
        info = categorize_pdf(pdf_path, project_root)
        section = info["section"]
        if section not in categorized:
            categorized[section] = []
        categorized[section].append(info)
    
    console.print(f"     [green]✅[/green] Organized into [bold]{len(categorized)}[/bold] sections\n")
    
    # Create binder
    binder = Binder(
        title="WAFT Project Collection",
        subtitle="Complete Documentation and Showcase",
        organization="WAFT - World Architecture Framework & Templates",
        date=datetime.now().strftime("%B %d, %Y"),
        version="1.0",
        compiled_by="WAFT System",
        cover_style="professional"
    )
    
    # Define section colors
    section_colors = {
        "Documentation": "#2c3e50",
        "Showcase Documents": "#3498db",
        "Project Lightcone": "#e74c3c",
        "Demos": "#9b59b6",
        "Work Efforts": "#f39c12",
        "Artifacts": "#1abc9c",
        "Other": "#95a5a6"
    }
    
    # Add sections and documents
    console.print("  [cyan]📖[/cyan] Building booklet structure...\n")
    
    # Order sections logically
    section_order = [
        "Documentation",
        "Showcase Documents",
        "Project Lightcone",
        "Demos",
        "Work Efforts",
        "Artifacts",
        "Other"
    ]
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Adding documents...", total=len(all_pdfs))
        
        for section_name in section_order:
            if section_name not in categorized:
                continue
            
            # Add section
            section = binder.add_section(
                name=section_name,
                description=categorized[section_name][0]["description"],
                color=section_colors.get(section_name, "#2c3e50")
            )
            
            # Add documents in this section
            for pdf_info in sorted(categorized[section_name], key=lambda x: x["title"]):
                try:
                    doc_entry = DocumentEntry(
                        path=pdf_info["path"],
                        title=pdf_info["title"],
                        section=section_name,
                        description=pdf_info.get("description")
                    )
                    section.add_document(doc_entry)
                    progress.update(task, advance=1)
                except Exception as e:
                    console.print(f"     [yellow]⚠️[/yellow]  Skipping {pdf_info['title']}: {e}")
    
    # Generate booklet
    console.print("\n  [cyan]📄[/cyan] Generating booklet...\n")
    
    try:
        with console.status("[bold cyan]Creating PDF booklet...[/bold cyan]"):
            binder.generate(output_path, include_dividers=True)
        
        size_mb = output_path.stat().st_size / (1024 * 1024)
        console.print(f"  [green]✅[/green] Booklet generated: [bold]{output_path}[/bold]")
        console.print(f"     Size: [bold]{size_mb:.2f} MB[/bold]")
        console.print(f"     Sections: [bold]{len(binder.sections)}[/bold]")
        console.print(f"     Documents: [bold]{len(all_pdfs)}[/bold]\n")
        
        return output_path
        
    except Exception as e:
        console.print(f"  [red]❌[/red] Error generating booklet: {e}")
        import traceback
        console.print(f"     [dim]{traceback.format_exc()}[/dim]")
        return None


def open_pdf(pdf_path: Path):
    """Open PDF using system default application."""
    try:
        import platform
        import subprocess
        
        system = platform.system()
        if system == "Darwin":  # macOS
            subprocess.run(["open", str(pdf_path)], check=True)
        elif system == "Windows":
            subprocess.run(["start", str(pdf_path)], shell=True, check=True)
        else:  # Linux
            subprocess.run(["xdg-open", str(pdf_path)], check=True)
        return True
    except Exception as e:
        console.print(f"  [yellow]⚠️[/yellow]  Could not open PDF: {e}")
        return False


if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    output_path = project_root / "WAFT_Project_Booklet.pdf"
    
    console.print("=" * 80)
    console.print("[bold]WAFT Project Booklet Generator[/bold]")
    console.print("=" * 80)
    console.print()
    console.print(f"Project root: [cyan]{project_root}[/cyan]")
    console.print(f"Output: [cyan]{output_path}[/cyan]")
    console.print()
    
    booklet_path = create_project_booklet(project_root, output_path)
    
    if booklet_path:
        console.print("  [cyan]📖[/cyan] Opening booklet...")
        if open_pdf(booklet_path):
            console.print("     [green]✅[/green] Booklet opened")
        console.print()
        console.print("[bold green]🎉 Complete![/bold green]\n")
    else:
        console.print("[bold red]❌ Failed to generate booklet[/bold red]\n")
        sys.exit(1)
