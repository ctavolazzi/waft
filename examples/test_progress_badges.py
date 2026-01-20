#!/usr/bin/env python3
"""
Test script for new progress bar and status badges components.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from weasyprint import HTML

from src.waft.evolution.chat_distiller import ChatDistiller
from src.waft.evolution.document_components import DocumentLayout
from src.waft.evolution.status_components import StatusComponentBuilder
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
    """Test progress bars and badges."""
    print("🧪 Testing Progress Bars and Status Badges...")

    builder = StatusComponentBuilder()

    # Create test components
    components = []

    # Title
    from src.waft.evolution.document_components import ComponentBuilder

    comp_builder = ComponentBuilder()
    components.append(comp_builder.build_title_component("AI-DnD Pattern Integration Test"))
    components.append(comp_builder.build_attribution_component("WAFT", "2026-01-11"))

    # Progress bars
    components.append(builder.build_progress_bar_component("Work Effort Progress", 3, 5))
    components.append(
        builder.build_progress_bar_component("Epistemic Knowledge", 65, 100, show_fraction=False)
    )
    components.append(builder.build_progress_bar_component("Gamification Level", 450, 1000))

    # Status badges
    health_badges = [
        {"label": "Pyrite Valid", "status": "good", "icon": "✅"},
        {"label": "Lock File", "status": "good", "icon": "🔒"},
        {"label": "Structure Valid", "status": "good", "icon": "📁"},
        {"label": "No Tests", "status": "warning", "icon": "⚠️"},
    ]
    components.append(builder.build_status_badges_component(health_badges, "System Health"))

    epistemic_badges = [
        {"label": "Moderate Coverage", "status": "info", "icon": "🌓"},
        {"label": "65% Knowledge", "status": "good", "icon": "📊"},
        {"label": "35% Uncertainty", "status": "warning", "icon": "❓"},
    ]
    components.append(builder.build_status_badges_component(epistemic_badges, "Epistemic State"))

    # Create layout
    layout = DocumentLayout(components=components, allowed_pages=10)

    # Get styling
    registry = StylingGenomeRegistry(registry_dir=Path("_genetics/status_pdfs"))
    styling_genes = StylingGene(
        font=FontGene(family="'Times New Roman', 'Times', serif", size_body=11),
        margin=MarginGene(top=25.4, bottom=25.4, left=25.4, right=25.4),
        color=ColorGene(text="#000000", background="#FFFFFF", accent="#0066cc"),
        layout=LayoutGene(columns=1, density="normal"),
        name="Test Pattern",
    )
    genome = StylingGenome.from_genes(styling_genes)
    registry.register(genome)

    # Generate PDF
    generator = TwoPageGenerator(weasyprint_available=True)
    distiller = ChatDistiller()
    distilled = distiller.distill_text("AI-DnD Pattern Integration Test", title="Pattern Test")

    output_path = Path("_work_efforts/showcase_documents/ai_dnd_patterns_test.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    html_content = generator._render_html_from_layout(layout, distilled, genome)
    HTML(string=html_content).write_pdf(output_path)

    print(f"✅ Generated: {output_path}")

    # Open PDF
    import subprocess

    subprocess.run(["open", str(output_path)])

    return output_path


if __name__ == "__main__":
    main()
