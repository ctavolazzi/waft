#!/usr/bin/env python3
"""
Generate Status PDF Using Typed StatusState
===========================================

Demonstrates using the new typed StatusState classes with computed properties
for generating status PDFs with enhanced metrics.
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from weasyprint import HTML

from scripts.waft_status import check_status
from src.waft.core.status_state import StatusState
from src.waft.evolution.chat_distiller import ChatDistiller
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
    """Generate status PDF using typed state."""
    print("📊 Generating Status PDF with Typed StatusState...")
    print()

    # Get status dict
    print("🔍 Checking system status...")
    status_dict = check_status(project_path=Path.cwd(), log_event=False)
    print("✓ Status check complete")
    print()

    # Create typed state
    print("🔧 Creating typed StatusState...")
    typed_state = StatusState.from_dict(status_dict)
    print(f"✓ Epistemic coverage: {typed_state.epistemic.coverage_pct:.1f}%")
    print(f"✓ Epistemic health: {typed_state.epistemic.health_status}")
    print(f"✓ Gamification integrity: {typed_state.gamification.integrity_status}")
    print(f"✓ Project health: {typed_state.project_health.health_status}")
    print(
        f"✓ Overall health: {typed_state.overall_health_status} ({typed_state.overall_health_score:.1f})"
    )
    print()

    # Create components with typed state
    print("🧩 Building status components (with typed state)...")
    status_components = create_status_components_from_status_dict(
        status_dict, typed_state=typed_state
    )
    print(f"✓ Created {len(status_components)} status components")
    print()

    # Add title and attribution
    builder = ComponentBuilder()
    title_component = builder.build_title_component("WAFT Kernel Status Report (Typed State)")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    attribution_component = builder.build_attribution_component("WAFT Kernel", timestamp)

    # Add computed metrics component
    from src.waft.evolution.status_components import StatusComponentBuilder

    status_builder = StatusComponentBuilder()

    # Overall health badge
    health_badge = [
        {
            "label": f"Overall Health: {typed_state.overall_health_status}",
            "status": "good" if typed_state.overall_health_score >= 75 else "warning",
            "icon": "💎",
        }
    ]
    components = [title_component, attribution_component] + status_components
    components.append(status_builder.build_status_badges_component(health_badge, "System Overview"))

    # Create layout
    layout = DocumentLayout(components=components, allowed_pages=10)

    # Get styling
    print("🎨 Setting up styling...")
    registry = StylingGenomeRegistry(registry_dir=Path("_genetics/status_pdfs"))
    styling_genes = StylingGene(
        font=FontGene(family="'Times New Roman', 'Times', serif", size_body=11),
        margin=MarginGene(top=25.4, bottom=25.4, left=25.4, right=25.4),
        color=ColorGene(text="#000000", background="#FFFFFF", accent="#0066cc"),
        layout=LayoutGene(columns=1, density="normal"),
        name="Status Report - Typed State",
    )
    genome = StylingGenome.from_genes(styling_genes)
    registry.register(genome)
    print(f"✓ Using: {genome.scientific_name}")
    print()

    # Generate PDF
    print("📄 Generating PDF...")
    generator = TwoPageGenerator(weasyprint_available=True)
    distiller = ChatDistiller()
    distilled = distiller.distill_text(
        "WAFT Kernel Status Report (Typed State)", title="Status Report"
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(f"_work_efforts/showcase_documents/WAFT_Status_TypedState_{timestamp}.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    html_content = generator._render_html_from_layout(layout, distilled, genome)
    HTML(string=html_content).write_pdf(output_path)

    # Count pages
    from pypdf import PdfReader

    reader = PdfReader(output_path)
    page_count = len(reader.pages)

    print()
    print("=" * 60)
    print("✅ Status PDF Generated with Typed State!")
    print("=" * 60)
    print(f"📄 Output: {output_path}")
    print(f"📊 Pages: {page_count}")
    print(f"🧩 Components: {len(components)}")
    print()
    print("Key Features:")
    print(f"  ✓ Epistemic coverage: {typed_state.epistemic.coverage_pct:.1f}%")
    print(f"  ✓ Overall health: {typed_state.overall_health_status}")
    print("  ✓ Computed properties used throughout")
    print()

    # Open PDF
    import subprocess

    subprocess.run(["open", "-a", "Preview", str(output_path)])
    print("📖 PDF opened in Preview")
    print()

    return output_path


if __name__ == "__main__":
    main()
