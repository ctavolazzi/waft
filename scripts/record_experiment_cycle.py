#!/usr/bin/env python3
"""
Record Experiment Cycle - Scientific Method Workflow

Records observations from experiments, generates PDF reports, and prepares for next iteration.
Automates: observe → document → analyze → iterate

Usage:
    python scripts/record_experiment_cycle.py \
        --experiment "Title Generation Algorithm" \
        --cycle 1 \
        --observations-file _work_efforts/proof_cases/observations.md \
        --test-cases "test1,test2,test3"
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from src.waft.brief import BriefDocument


def generate_observations_pdf(
    observations_file: Path,
    experiment_name: str,
    cycle: int,
    output_dir: Optional[Path] = None
) -> Path:
    """
    Generate PDF report from observations markdown file.
    
    Args:
        observations_file: Path to observations markdown file
        experiment_name: Name of the experiment
        cycle: Cycle/iteration number
        output_dir: Output directory (defaults to observations_file parent)
    
    Returns:
        Path to generated PDF
    """
    if output_dir is None:
        output_dir = observations_file.parent
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Read observations
    observations = observations_file.read_text()
    
    # Generate PDF
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"{experiment_name.replace(' ', '_')}_Cycle{cycle}_{timestamp}.pdf"
    
    doc = BriefDocument(
        title=f"{experiment_name} - Experiment Cycle {cycle}",
        doc_id=f"EXPERIMENT-{timestamp}",
        subtitle=f"Observations and Analysis - Ready for Iteration {cycle + 1}",
        classification="INTERNAL",
        cover_header="EXPERIMENT REPORT",
        cover_metadata={
            "EXPERIMENT": experiment_name,
            "CYCLE": str(cycle),
            "DATE": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "STATUS": "Observations Complete",
            "NEXT": f"Iteration {cycle + 1}"
        },
        cover_warning={
            "message": f"EXPERIMENTAL FINDINGS - Ready for next iteration cycle",
            "severity": "INFO"
        },
        cover_footer="ITERATIVE IMPROVEMENT PROCESS",
        include_system_status=False
    )
    
    # Convert markdown to HTML
    try:
        import markdown
        html_content = markdown.markdown(
            observations,
            extensions=['fenced_code', 'tables', 'nl2br', 'extra', 'codehilite']
        )
    except ImportError:
        import re
        html_content = observations
        html_content = re.sub(r'^#\s+(.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'^##\s+(.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html_content)
        html_content = re.sub(r'\n', '<br>\n', html_content)
    
    doc.content_blocks.append(html_content)
    
    # Generate PDF
    pdf_path = doc.generate(output_path)
    return pdf_path


def generate_preparation_pdf(
    preparation_file: Path,
    experiment_name: str,
    next_cycle: int,
    output_dir: Optional[Path] = None
) -> Path:
    """
    Generate PDF from iteration preparation document.
    
    Args:
        preparation_file: Path to preparation markdown file
        experiment_name: Name of the experiment
        next_cycle: Next cycle/iteration number
        output_dir: Output directory (defaults to preparation_file parent)
    
    Returns:
        Path to generated PDF
    """
    if output_dir is None:
        output_dir = preparation_file.parent
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Read preparation
    preparation = preparation_file.read_text()
    
    # Generate PDF
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"Iteration{next_cycle}_Preparation_{timestamp}.pdf"
    
    doc = BriefDocument(
        title=f"Iteration {next_cycle} Preparation - {experiment_name}",
        doc_id=f"PREP-{timestamp}",
        subtitle="Starting Conditions and Improvement Plan",
        classification="INTERNAL",
        cover_header="ITERATION PREPARATION",
        cover_metadata={
            "EXPERIMENT": experiment_name,
            "CYCLE": str(next_cycle),
            "DATE": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "STATUS": "Ready to Begin",
            "PRIORITY": "High - Key Improvements Identified"
        },
        cover_warning={
            "message": f"ITERATION {next_cycle} - Same starting conditions, improved approach",
            "severity": "INFO"
        },
        cover_footer="ITERATIVE IMPROVEMENT PROCESS",
        include_system_status=False
    )
    
    # Convert markdown to HTML
    try:
        import markdown
        html_content = markdown.markdown(
            preparation,
            extensions=['fenced_code', 'tables', 'nl2br', 'extra', 'codehilite']
        )
    except ImportError:
        import re
        html_content = preparation
        html_content = re.sub(r'^#\s+(.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'^##\s+(.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html_content)
        html_content = re.sub(r'\n', '<br>\n', html_content)
    
    doc.content_blocks.append(html_content)
    
    # Generate PDF
    pdf_path = doc.generate(output_path)
    return pdf_path


def open_pdf_on_desktop(pdf_path: Path) -> None:
    """
    Open PDF on desktop (macOS).
    
    Args:
        pdf_path: Path to PDF file
    """
    import subprocess
    import platform
    
    if platform.system() == "Darwin":  # macOS
        subprocess.run(["open", str(pdf_path)])
    elif platform.system() == "Linux":
        subprocess.run(["xdg-open", str(pdf_path)])
    elif platform.system() == "Windows":
        subprocess.run(["start", str(pdf_path)], shell=True)


def main():
    parser = argparse.ArgumentParser(
        description="Record experiment cycle and generate PDF reports"
    )
    parser.add_argument(
        "--experiment",
        required=True,
        help="Name of the experiment"
    )
    parser.add_argument(
        "--cycle",
        type=int,
        required=True,
        help="Current cycle/iteration number"
    )
    parser.add_argument(
        "--observations-file",
        type=Path,
        required=True,
        help="Path to observations markdown file"
    )
    parser.add_argument(
        "--preparation-file",
        type=Path,
        help="Path to preparation markdown file (optional)"
    )
    parser.add_argument(
        "--open",
        action="store_true",
        default=True,
        help="Open PDFs on desktop (default: True)"
    )
    parser.add_argument(
        "--no-open",
        dest="open",
        action="store_false",
        help="Don't open PDFs on desktop"
    )
    
    args = parser.parse_args()
    
    # Generate observations PDF
    print(f"Generating observations PDF for cycle {args.cycle}...")
    obs_pdf = generate_observations_pdf(
        args.observations_file,
        args.experiment,
        args.cycle
    )
    print(f"✅ Observations PDF: {obs_pdf}")
    
    if args.open:
        open_pdf_on_desktop(obs_pdf)
        print(f"   Opened on desktop")
    
    # Generate preparation PDF if provided
    if args.preparation_file and args.preparation_file.exists():
        next_cycle = args.cycle + 1
        print(f"Generating preparation PDF for iteration {next_cycle}...")
        prep_pdf = generate_preparation_pdf(
            args.preparation_file,
            args.experiment,
            next_cycle
        )
        print(f"✅ Preparation PDF: {prep_pdf}")
        
        if args.open:
            open_pdf_on_desktop(prep_pdf)
            print(f"   Opened on desktop")
    
    print("\n✅ Experiment cycle documentation complete!")


if __name__ == "__main__":
    main()
