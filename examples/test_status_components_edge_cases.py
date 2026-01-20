#!/usr/bin/env python3
"""
Test Status Components: Edge Cases and Various Scenarios
========================================================

Tests status components with:
- Missing data scenarios
- Empty states
- Extreme values
- Different combinations
- Error conditions
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from weasyprint import HTML

from src.waft.evolution.chat_distiller import ChatDistiller
from src.waft.evolution.document_components import ComponentBuilder, DocumentLayout
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


def test_scenario_1_empty_state():
    """Test with completely empty status."""
    print("🧪 Test 1: Empty State")

    status = {
        "epistemic_phase": "Unknown",
        "epistemic_state": {},
        "gamification_state": {},
        "flight_recorder_events": [],
        "project_health": {},
        "git_status": {},
    }

    components = create_status_components_from_status_dict(status)
    print(f"  ✓ Generated {len(components)} components (should handle gracefully)")
    return components, "Empty State Test"


def test_scenario_2_missing_epistemic():
    """Test with missing epistemic data."""
    print("🧪 Test 2: Missing Epistemic Data")

    status = {
        "epistemic_phase": "Unknown",
        "epistemic_state": {"initialized": False, "message": "Not available"},
        "gamification_state": {"available": True, "level": 3, "integrity": 87.5, "insight": 450.0},
        "flight_recorder_events": [],
        "project_health": {"pyrite_valid": True, "lock_exists": True},
        "git_status": {"branch": "main"},
    }

    components = create_status_components_from_status_dict(status)
    print(f"  ✓ Generated {len(components)} components")
    return components, "Missing Epistemic Test"


def test_scenario_3_extreme_values():
    """Test with extreme values."""
    print("🧪 Test 3: Extreme Values")

    builder = StatusComponentBuilder()
    components = []

    # Progress bar with 0/0
    components.append(builder.build_progress_bar_component("Zero Total", 0, 0))

    # Progress bar with 100/100
    components.append(builder.build_progress_bar_component("Complete", 100, 100))

    # Progress bar with over 100%
    components.append(builder.build_progress_bar_component("Over Complete", 150, 100))

    # Progress bar with negative
    components.append(builder.build_progress_bar_component("Negative", -5, 10))

    # Many badges
    many_badges = [{"label": f"Badge {i}", "status": "info", "icon": "🔷"} for i in range(20)]
    components.append(builder.build_status_badges_component(many_badges, "Many Badges"))

    print(f"  ✓ Generated {len(components)} components with extreme values")
    return components, "Extreme Values Test"


def test_scenario_4_full_status():
    """Test with complete, realistic status."""
    print("🧪 Test 4: Full Realistic Status")

    status = {
        "epistemic_phase": "Active Development",
        "epistemic_state": {
            "initialized": True,
            "moon_phase": "🌓",
            "moon_phase_desc": "Moderate (65% coverage)",
            "knowledge_pct": 65.0,
            "uncertainty_pct": 35.0,
        },
        "gamification_state": {
            "available": True,
            "level": 3,
            "integrity": 87.5,
            "insight": 450.0,
            "achievements_count": 2,
        },
        "flight_recorder_events": [
            {"event_type": "spawn", "timestamp": "2026-01-11T10:00:00", "genome_id": "test-1"},
            {"event_type": "mutate", "timestamp": "2026-01-11T10:05:00", "genome_id": "test-1"},
            {"event_type": "spawn", "timestamp": "2026-01-11T10:10:00", "genome_id": "test-2"},
        ],
        "project_health": {"pyrite_valid": True, "structure_valid": True, "lock_exists": True},
        "git_status": {"branch": "main", "uncommitted": 3},
    }

    components = create_status_components_from_status_dict(status)
    print(f"  ✓ Generated {len(components)} components")
    return components, "Full Status Test"


def test_scenario_5_mixed_states():
    """Test with mixed valid/invalid states."""
    print("🧪 Test 5: Mixed States")

    status = {
        "epistemic_phase": "Data Gathering",
        "epistemic_state": {
            "initialized": True,
            "moon_phase": "🌑",
            "moon_phase_desc": "Critical (15% coverage)",
            "knowledge_pct": 15.0,
            "uncertainty_pct": 85.0,
        },
        "gamification_state": {"available": False},
        "flight_recorder_events": [
            {"event_type": "error", "timestamp": "2026-01-11T10:00:00", "genome_id": "error-1"},
        ],
        "project_health": {"pyrite_valid": False, "structure_valid": True, "lock_exists": False},
        "git_status": {},
    }

    components = create_status_components_from_status_dict(status)
    print(f"  ✓ Generated {len(components)} components")
    return components, "Mixed States Test"


def generate_test_pdf(components, title, output_name):
    """Generate PDF from components."""
    builder = ComponentBuilder()
    all_components = [
        builder.build_title_component(title),
        builder.build_attribution_component(
            "WAFT Test Suite", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ),
    ] + components

    layout = DocumentLayout(components=all_components, allowed_pages=10)

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

    generator = TwoPageGenerator(weasyprint_available=True)
    distiller = ChatDistiller()
    distilled = distiller.distill_text(title, title=title)

    output_path = Path(f"_work_efforts/showcase_documents/edge_case_test_{output_name}.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    html_content = generator._render_html_from_layout(layout, distilled, genome)
    HTML(string=html_content).write_pdf(output_path)

    return output_path


def main():
    """Run all edge case tests."""
    print("=" * 60)
    print("🧪 Status Components Edge Case Testing")
    print("=" * 60)
    print()

    test_results = []

    # Run all test scenarios
    scenarios = [
        test_scenario_1_empty_state,
        test_scenario_2_missing_epistemic,
        test_scenario_3_extreme_values,
        test_scenario_4_full_status,
        test_scenario_5_mixed_states,
    ]

    for i, scenario_func in enumerate(scenarios, 1):
        try:
            components, title = scenario_func()
            output_name = f"scenario_{i:02d}"
            pdf_path = generate_test_pdf(components, title, output_name)
            test_results.append(
                {
                    "scenario": i,
                    "title": title,
                    "components": len(components),
                    "status": "✅ PASS",
                    "pdf": str(pdf_path),
                }
            )
            print(f"  📄 Generated: {pdf_path.name}")
        except Exception as e:
            test_results.append(
                {
                    "scenario": i,
                    "title": scenario_func.__name__,
                    "status": f"❌ FAIL: {str(e)}",
                    "pdf": None,
                }
            )
            print(f"  ❌ Error: {e}")
        print()

    # Summary
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    for result in test_results:
        print(f"Scenario {result['scenario']}: {result['title']}")
        print(f"  Status: {result['status']}")
        if "components" in result:
            print(f"  Components: {result['components']}")
        if result.get("pdf"):
            print(f"  PDF: {result['pdf']}")
        print()

    passed = sum(1 for r in test_results if "✅" in r["status"])
    total = len(test_results)
    print(f"✅ Passed: {passed}/{total}")

    if passed == total:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {total - passed} test(s) failed")

    return test_results


if __name__ == "__main__":
    main()
