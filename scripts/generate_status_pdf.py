#!/usr/bin/env python3
"""
Generate Status PDF using Status Components
===========================================

Creates a PDF from WAFT status using the new status components system.
Demonstrates how to use StatusComponentBuilder for creating PDFs with
epistemic state, gamification, Flight Recorder events, etc.
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution.status_components import (
    StatusComponentBuilder,
    create_status_components_from_status_dict
)
from src.waft.evolution.document_components import ComponentBuilder, ComponentType
from src.waft.evolution.two_page_generator import TwoPageGenerator
from src.waft.evolution.styling_genome import (
    StylingGenome,
    StylingGenomeRegistry,
    StylingGene,
    FontGene,
    MarginGene,
    ColorGene,
    LayoutGene
)
from scripts.waft_status import check_status


def main():
    """Generate status PDF using status components."""
    print("📊 Generating WAFT Status PDF with Status Components...")
    print()
    
    # Get current status
    print("🔍 Checking system status...")
    project_path = Path.cwd()
    status = check_status(project_path=project_path, log_event=False)
    print("✓ Status check complete")
    print()
    
    # Create status components
    print("🧩 Building status components...")
    status_components = create_status_components_from_status_dict(status)
    print(f"✓ Created {len(status_components)} status components")
    for comp in status_components:
        comp_subtype = comp.metadata.get('component_subtype', 'standard')
        print(f"  - {comp.content.get('title', 'Unknown')} ({comp_subtype})")
    print()
    
    # Add title component
    builder = ComponentBuilder()
    title_component = builder.build_title_component("WAFT Kernel Status Report")
    
    # Add timestamp attribution
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    attribution_component = builder.build_attribution_component(
        "WAFT Kernel",
        timestamp
    )
    
    # Combine all components
    all_components = [title_component, attribution_component] + status_components
    
    # Get or create styling genome
    print("🎨 Setting up styling...")
    registry = StylingGenomeRegistry(registry_dir=Path("_genetics/status_pdfs"))
    
    # Create status-specific genome
    styling_genes = StylingGene(
        font=FontGene(family="'Times New Roman', 'Times', serif", size_body=11),
        margin=MarginGene(top=25.4, bottom=25.4, left=25.4, right=25.4),
        color=ColorGene(
            text="#000000",
            background="#FFFFFF",
            accent="#0066cc",
            code_bg="#f5f5f5",
            border="#cccccc"
        ),
        layout=LayoutGene(columns=1, density="normal"),
        name="Status Report - Clinical Standard"
    )
    genome = StylingGenome.from_genes(styling_genes)
    registry.register(genome)
    print(f"✓ Using: {genome.scientific_name}")
    print()
    
    # Generate PDF
    print("📄 Generating PDF...")
    generator = TwoPageGenerator(weasyprint_available=True)
    
    # Create a distilled chat object for the generator (minimal - just for structure)
    from src.waft.evolution.chat_distiller import ChatDistiller
    distiller = ChatDistiller()
    distilled = distiller.distill_text(
        "WAFT Kernel Status Report",
        title="WAFT Kernel Status Report"
    )
    
    # Create output path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(f"_work_efforts/showcase_documents/WAFT_Status_Components_{timestamp}.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Generate using components directly
    # We'll use the layout system
    from src.waft.evolution.document_components import DocumentLayout
    
    layout = DocumentLayout(
        components=all_components,
        allowed_pages=10,  # Allow more pages for status report
        metadata={'type': 'status_report'}
    )
    
    # Render HTML from layout
    html_content = generator._render_html_from_layout(
        layout=layout,
        distilled_chat=distilled,
        styling_genome=genome
    )
    
    # Generate PDF
    from weasyprint import HTML
    HTML(string=html_content).write_pdf(output_path)
    
    # Count pages
    from pypdf import PdfReader
    reader = PdfReader(output_path)
    page_count = len(reader.pages)
    
    print()
    print("=" * 60)
    print("✅ Status PDF Generated!")
    print("=" * 60)
    print(f"📄 Output: {output_path}")
    print(f"📊 Pages: {page_count}")
    print(f"🧩 Components: {len(all_components)}")
    print()
    
    # Open PDF
    import subprocess
    subprocess.run(["open", "-a", "Preview", str(output_path)])
    print(f"📖 PDF opened in Preview")
    print()
    
    return output_path


if __name__ == "__main__":
    main()
