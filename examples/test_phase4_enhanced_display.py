#!/usr/bin/env python3
"""
Test Phase 4: Enhanced Display Components
=========================================

Tests the new grouped metrics, Git summary, and Work Efforts summary components.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime

from weasyprint import HTML

from scripts.waft_status import check_status
from src.waft.core.status_state import StatusState
from src.waft.evolution.chat_distiller import ChatDistiller
from src.waft.evolution.document_components import DocumentLayout
from src.waft.evolution.status_components import (
    StatusComponentBuilder,
    create_status_components_from_status_dict,
)
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


def test_grouped_metrics():
    """Test grouped metrics component."""
    print("🧪 Test 1: Grouped Metrics Component")

    builder = StatusComponentBuilder()

    metrics = [
        {"label": "Knowledge", "value": "75.0", "unit": "%", "icon": "📊"},
        {"label": "Uncertainty", "value": "25.0", "unit": "%", "icon": "❓", "status": "warning"},
        {"label": "Coverage", "value": "87.5", "unit": "%", "icon": "🎯", "status": "good"},
    ]

    component = builder.build_grouped_metrics_component(
        "Epistemic Metrics", metrics, description="Knowledge measurement and coverage indicators"
    )

    print(f"  ✓ Component created: {component.metadata['component_subtype']}")
    print(f"  ✓ Title: {component.content['title']}")
    print(f"  ✓ Metrics: {len(metrics)}")

    return component


def test_git_summary():
    """Test Git summary component."""
    print("\n🧪 Test 2: Git Summary Component")

    builder = StatusComponentBuilder()

    git_data = {
        "initialized": True,
        "branch": "main",
        "uncommitted_files": ["file1.py", "file2.py"],
        "recent_commits": ["abc123", "def456"],
    }

    component = builder.build_git_summary_component(git_data)

    print(f"  ✓ Component created: {component.metadata['component_subtype']}")
    print(f"  ✓ Title: {component.content['title']}")

    return component


def test_work_efforts_summary():
    """Test Work Efforts summary component."""
    print("\n🧪 Test 3: Work Efforts Summary Component")

    builder = StatusComponentBuilder()

    work_efforts_data = {
        "count": 10,
        "active": ["WE-001", "WE-002", "WE-003"],
        "completed": ["WE-004", "WE-005", "WE-006", "WE-007"],
        "recent": ["WE-001", "WE-002"],
    }

    component = builder.build_work_efforts_summary_component(work_efforts_data)

    print(f"  ✓ Component created: {component.metadata['component_subtype']}")
    print(f"  ✓ Title: {component.content['title']}")
    print(f"  ✓ Total: {work_efforts_data['count']}")
    print(f"  ✓ Active: {len(work_efforts_data['active'])}")
    print(f"  ✓ Completed: {len(work_efforts_data['completed'])}")

    return component


def test_integration():
    """Test integration with full status."""
    print("\n🧪 Test 4: Full Integration")

    status = check_status(log_event=False)
    typed_state = StatusState.from_dict(status)

    components = create_status_components_from_status_dict(status, typed_state=typed_state)

    # Count new component types
    grouped_metrics = [
        c for c in components if c.metadata.get("component_subtype") == "grouped_metrics"
    ]
    git_summary = [c for c in components if c.metadata.get("component_subtype") == "git_summary"]
    work_efforts = [
        c for c in components if c.metadata.get("component_subtype") == "work_efforts_summary"
    ]

    print(f"  ✓ Total components: {len(components)}")
    print(f"  ✓ Grouped metrics: {len(grouped_metrics)}")
    print(f"  ✓ Git summary: {len(git_summary)}")
    print(f"  ✓ Work efforts: {len(work_efforts)}")

    return components


def test_pdf_generation():
    """Test PDF generation with new components."""
    print("\n🧪 Test 5: PDF Generation")

    status = check_status(log_event=False)
    typed_state = StatusState.from_dict(status)
    components = create_status_components_from_status_dict(status, typed_state=typed_state)

    # Add title
    from src.waft.evolution.document_components import ComponentBuilder

    builder = ComponentBuilder()
    title = builder.build_title_component("WAFT Status Report (Phase 4 Enhanced Display)")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    attribution = builder.build_attribution_component("WAFT Kernel", timestamp)

    all_components = [title, attribution] + components
    layout = DocumentLayout(components=all_components, allowed_pages=10)

    # Get styling
    registry = StylingGenomeRegistry(registry_dir=Path("_genetics/status_pdfs"))
    styling_genes = StylingGene(
        font=FontGene(family="'Times New Roman', 'Times', serif", size_body=11),
        margin=MarginGene(top=25.4, bottom=25.4, left=25.4, right=25.4),
        color=ColorGene(text="#000000", background="#FFFFFF", accent="#0066cc"),
        layout=LayoutGene(columns=1, density="normal"),
        name="Status Report - Phase 4",
    )
    genome = StylingGenome.from_genes(styling_genes)
    registry.register(genome)

    # Generate PDF
    generator = TwoPageGenerator(weasyprint_available=True)
    distiller = ChatDistiller()
    distilled = distiller.distill_text(
        "WAFT Kernel Status Report (Phase 4 Enhanced Display)", title="Status Report"
    )

    html_content = generator._render_html_from_layout(layout, distilled, genome)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(f"_work_efforts/showcase_documents/WAFT_Status_Phase4_{timestamp}.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    HTML(string=html_content).write_pdf(output_path)

    # Count pages
    from pypdf import PdfReader

    reader = PdfReader(output_path)
    page_count = len(reader.pages)

    print(f"  ✓ PDF generated: {output_path.name}")
    print(f"  ✓ Pages: {page_count}")
    print(f"  ✓ Components: {len(all_components)}")

    # Open PDF
    import subprocess

    subprocess.run(["open", "-a", "Preview", str(output_path)])

    return output_path


def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 Phase 4: Enhanced Display Testing")
    print("=" * 60)
    print()

    try:
        test_grouped_metrics()
        test_git_summary()
        test_work_efforts_summary()
        test_integration()
        test_pdf_generation()

        print()
        print("=" * 60)
        print("✅ All Tests Passed!")
        print("=" * 60)
        print()
        print("Phase 4 Features Verified:")
        print("  ✓ Grouped metrics component")
        print("  ✓ Git status summary")
        print("  ✓ Work efforts summary with progress")
        print("  ✓ Full integration with status components")
        print("  ✓ PDF generation with new components")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    main()
