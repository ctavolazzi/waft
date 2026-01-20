#!/usr/bin/env python3
"""
Example: Generate Status PDF Using Status Components
====================================================

Quick example showing how to use status components to generate a PDF
with epistemic state, gamification, Flight Recorder events, etc.
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.waft_status import check_status
from src.waft.evolution.document_components import ComponentBuilder, DocumentLayout
from src.waft.evolution.status_components import create_status_components_from_status_dict
from src.waft.evolution.styling_genome import (
    ColorGene,
    FontGene,
    LayoutGene,
    MarginGene,
    StylingGene,
    StylingGenome,
    StylingGenomeRegistry,
)
from src.waft.evolution.two_page_generator import TwoPageGenerator


def main():
    """Generate status PDF using status components."""
    print("📊 Generating Status PDF with Components...")

    # Get status
    status = check_status(Path.cwd(), log_event=False)

    # Create components
    status_components = create_status_components_from_status_dict(status)

    # Add title
    builder = ComponentBuilder()
    title = builder.build_title_component("WAFT Kernel Status Report")
    timestamp = builder.build_attribution_component(
        "WAFT Kernel", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    # Combine
    all_components = [title, timestamp] + status_components

    # Create layout
    layout = DocumentLayout(components=all_components, allowed_pages=10)

    # Get styling
    registry = StylingGenomeRegistry(registry_dir=Path("_genetics/status_pdfs"))
    styling_genes = StylingGene(
        font=FontGene(family="'Times New Roman', 'Times', serif", size_body=11),
        margin=MarginGene(top=25.4, bottom=25.4, left=25.4, right=25.4),
        color=ColorGene(text="#000000", background="#FFFFFF", accent="#0066cc"),
        layout=LayoutGene(columns=1, density="normal"),
        name="Status Report",
    )
    genome = StylingGenome.from_genes(styling_genes)
    registry.register(genome)

    # Generate PDF
    generator = TwoPageGenerator(weasyprint_available=True)
    from src.waft.evolution.chat_distiller import ChatDistiller

    distiller = ChatDistiller()
    distilled = distiller.distill_text("WAFT Kernel Status Report", title="Status Report")

    output_path = Path("_work_efforts/showcase_documents/status_example.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    html_content = generator._render_html_from_layout(layout, distilled, genome)
    from weasyprint import HTML

    HTML(string=html_content).write_pdf(output_path)

    print(f"✅ Generated: {output_path}")
    return output_path


if __name__ == "__main__":
    main()
