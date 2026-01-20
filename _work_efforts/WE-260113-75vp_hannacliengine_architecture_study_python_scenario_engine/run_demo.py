"""
Run the scenario engine demo and generate a PDF.

This script:
1. Runs the demo scenario engine
2. Captures execution events
3. Generates a PDF report showing the scenario execution
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from demo_scenario_engine import run_demo_scenario

# Import PDF generator - try different methods
try:
    from waft.evolution.pdf_generator import PDFGenerator
except ImportError:
    # Fallback: use direct import
    import importlib.util

    pdf_gen_path = project_root / "src" / "waft" / "evolution" / "pdf_generator.py"
    spec = importlib.util.spec_from_file_location("pdf_generator", pdf_gen_path)
    pdf_generator = importlib.util.module_from_spec(spec)
    sys.modules["pdf_generator"] = pdf_generator
    spec.loader.exec_module(pdf_generator)
    PDFGenerator = pdf_generator.PDFGenerator

from rich.console import Console

console = Console()


def main():
    """Run demo and generate PDF."""
    work_effort_dir = Path(__file__).parent
    scenario_file = work_effort_dir / "demo_scenario.json"

    console.print("\n[bold cyan]🎮 Running Scenario Engine Demo[/bold cyan]\n")

    # Run the scenario
    engine = run_demo_scenario(scenario_file, auto_play=True)

    # Generate markdown
    markdown = engine.to_markdown()

    console.print("\n[bold green]✅ Scenario execution complete![/bold green]")
    console.print(f"[dim]Events captured: {len(engine.events)}[/dim]\n")

    # Generate PDF
    console.print("[bold cyan]📄 Generating PDF report...[/bold cyan]\n")

    output_path = work_effort_dir / "scenario_engine_demo_report.pdf"

    PDFGenerator.from_content(
        content=markdown,
        title="Scenario Engine Demo: The Mysterious Tavern",
        style="clinical_standard",
        author="WAFT Scenario Engine",
        subject="HannaCLIEngine Architecture Study - Demo Execution",
    ).save(str(output_path), open_pdf=False)

    console.print(f"\n[bold green]✅ PDF generated:[/bold green] {output_path}")
    console.print(f"[dim]File size: {output_path.stat().st_size / 1024:.1f} KB[/dim]\n")

    # Show summary
    console.print("[bold]Execution Summary:[/bold]")
    console.print(f"- Sequences executed: {len(engine.events)}")
    console.print("- Final containers:")
    for container, values in engine.containers.items():
        console.print(f"  • {container}: {len(values)} items")

    return output_path


if __name__ == "__main__":
    main()
