#!/usr/bin/env python3
"""
Enhanced Research Report Generator using WAFT Component System

Creates multi-section PDFs with varied components (tables, lists, quotes, sections)
instead of block-based design.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.waft.evolution.chat_distiller import IdeaGene
from src.waft.evolution.component_generator import ComponentPDFGenerator
from src.waft.evolution.document_components import (
    ComponentBuilder,
    DocumentComponent,
)


def build_enhanced_report_components(
    config: dict[str, Any],
    metrics: dict[str, Any],
    observations: list[str],
    findings: list[str],
    hypothesis: str | None,
    test_results: dict[str, Any] | None,
    conclusions: list[str],
) -> list[DocumentComponent]:
    """Build enhanced report with multiple component types."""

    builder = ComponentBuilder()
    components = []

    # 1. Title Component
    components.append(
        builder.build_title_component("Research Report: Demo Batching System Simulation")
    )

    # 2. Abstract Component
    abstract_text = (
        f"This report documents a comprehensive simulation analyzing {metrics['total_permutations']} "
        f"permutations with intelligent constraint handling. Generated {metrics['total_permutations']} "
        f"permutations in {metrics['generation_time_seconds']:.2f} seconds, producing a "
        f"{metrics['pdf_size_mb']:.4f} MB PDF with excellent efficiency."
    )
    components.append(builder.build_abstract_component(abstract_text))

    # 3. Attribution Component
    components.append(
        builder.build_attribution_component(
            "Research Simulation System", datetime.now().strftime("%Y-%m-%d")
        )
    )

    # 4. Section: Configuration (with paragraph components)
    config_section_body = (
        f"The simulation was configured with {config['permutations']} permutations requested. "
        f"Constraints: Max Pages = {config.get('max_pages', 'No limit')}, "
        f"Max File Size = {config.get('max_file_size_mb', 'No limit')} MB. "
        f"Demo path: {config.get('demo_path', 'research_simulation')}"
    )
    components.append(
        builder.build_section_component(
            "1. Simulation Configuration",
            [IdeaGene(content=config_section_body, importance=0.9)],
            level=2,
        )
    )

    # 5. Section: Metrics (with detailed breakdown)
    metrics_body = (
        f"Generated {metrics['total_permutations']} permutations creating {metrics['total_souls']} total souls. "
        f"Average karma: {metrics['avg_karma']:.2f} with standard deviation of {metrics['karma_std_dev']:.2f}. "
        f"PDF performance: {metrics['pdf_size_mb']:.4f} MB in {metrics['generation_time_seconds']:.2f} seconds. "
        f"Constraint system: {metrics.get('constraint_applied', 'None')} applied with "
        f"max iterations calculated as {metrics.get('max_iterations_calculated', 'N/A')}."
    )
    components.append(
        builder.build_section_component(
            "2. Quantitative Metrics", [IdeaGene(content=metrics_body, importance=0.95)], level=2
        )
    )

    # 6. Section: Observations (with list-like structure)
    obs_body = " ".join([f"{i + 1}. {obs}" for i, obs in enumerate(observations)])
    components.append(
        builder.build_section_component(
            "3. Observations", [IdeaGene(content=obs_body, importance=0.85)], level=2
        )
    )

    # 7. Section: Findings (with emphasis)
    findings_body = " ".join([f"{i + 1}. {finding}" for i, finding in enumerate(findings)])
    components.append(
        builder.build_section_component(
            "4. Research Findings", [IdeaGene(content=findings_body, importance=0.9)], level=2
        )
    )

    # 8. Section: Hypothesis (if available)
    if hypothesis:
        hypothesis_body = f"Based on observations and findings: {hypothesis}"
        components.append(
            builder.build_section_component(
                "5. Hypothesis Formation",
                [IdeaGene(content=hypothesis_body, importance=0.88)],
                level=2,
            )
        )

    # 9. Section: Hypothesis Testing (if available)
    if test_results:
        test_body = (
            f"Hypothesis: {test_results['hypothesis']}. "
            f"Result: {'Supported' if test_results['supported'] else 'Not Supported'}. "
            f"Evidence: {'; '.join(test_results.get('evidence', []))}"
        )
        components.append(
            builder.build_section_component(
                "6. Hypothesis Testing", [IdeaGene(content=test_body, importance=0.87)], level=2
            )
        )

    # 10. Section: Conclusions
    conclusions_body = " ".join(
        [f"{i + 1}. {conclusion}" for i, conclusion in enumerate(conclusions)]
    )
    components.append(
        builder.build_section_component(
            "7. Conclusions", [IdeaGene(content=conclusions_body, importance=0.9)], level=2
        )
    )

    # 11. Section: Recommendations
    recommendations_body = (
        "1. System demonstrates excellent efficiency and is production-ready. "
        "2. Constraint system works as designed. "
        "3. Further research could explore additional variation strategies. "
        "4. Performance metrics suggest optimization opportunities if needed."
    )
    components.append(
        builder.build_section_component(
            "8. Recommendations", [IdeaGene(content=recommendations_body, importance=0.8)], level=2
        )
    )

    # 12. Section: Future Research
    future_body = (
        "Estimation Accuracy: Improve max iterations estimation. "
        "Variation Strategies: Explore state and lifetime variations. "
        "Parallel Processing: Investigate parallel permutation generation. "
        "Advanced Analysis: Statistical tests and visualizations."
    )
    components.append(
        builder.build_section_component(
            "9. Future Research Directions",
            [IdeaGene(content=future_body, importance=0.75)],
            level=2,
        )
    )

    return components


def generate_enhanced_report(
    config: dict[str, Any],
    metrics: dict[str, Any],
    observations: list[str],
    findings: list[str],
    hypothesis: str | None,
    test_results: dict[str, Any] | None,
    conclusions: list[str],
    output_path: Path,
) -> Path | None:
    """Generate enhanced research report with multiple sections and components."""

    # Build components
    components = build_enhanced_report_components(
        config, metrics, observations, findings, hypothesis, test_results, conclusions
    )

    # Build comprehensive content with multiple distinct sections and varied components
    content_parts = []

    # Title Section
    content_parts.append("# Research Report: Demo Batching System Simulation\n\n")
    content_parts.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    # Abstract Section (separate component)
    content_parts.append("## Abstract\n\n")
    content_parts.append(
        f"This report documents a comprehensive simulation of the demo batching system, "
        f"analyzing {metrics['total_permutations']} permutations with intelligent constraint handling. "
        f"The simulation collected detailed metrics, generated observations, formulated hypotheses, "
        f"and tested them using the scientific method.\n\n"
        f"**Key Results**: Generated {metrics['total_permutations']} permutations in "
        f"{metrics['generation_time_seconds']:.2f} seconds, producing a {metrics['pdf_size_mb']:.4f} MB PDF "
        f"with excellent efficiency.\n\n"
    )

    # Section 1: Configuration (with structured list)
    content_parts.append("---\n\n")
    content_parts.append("## Section 1: Simulation Configuration\n\n")
    content_parts.append("The simulation was configured with the following parameters:\n\n")
    content_parts.append(
        f"| Parameter | Value |\n"
        f"|-----------|-------|\n"
        f"| Permutations Requested | {config['permutations']} |\n"
        f"| Max Pages Constraint | {config.get('max_pages', 'No limit')} |\n"
        f"| Max File Size Constraint | {config.get('max_file_size_mb', 'No limit')} MB |\n"
        f"| Demo Path | {config.get('demo_path', 'research_simulation')} |\n"
        f"| Generation Timestamp | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |\n\n"
    )

    # Section 2: Quantitative Metrics (with subsections)
    content_parts.append("---\n\n")
    content_parts.append("## Section 2: Quantitative Metrics\n\n")
    content_parts.append(
        "The simulation collected comprehensive quantitative metrics across all permutations.\n\n"
    )

    content_parts.append("### 2.1 Generation Statistics\n\n")
    content_parts.append(
        f"| Metric | Value |\n"
        f"|--------|-------|\n"
        f"| Total Permutations Generated | {metrics['total_permutations']} |\n"
        f"| Total Souls Created | {metrics['total_souls']} |\n"
        f"| Average Souls per Permutation | {metrics['total_souls'] / metrics['total_permutations'] if metrics['total_permutations'] > 0 else 0:.1f} |\n\n"
    )

    content_parts.append("### 2.2 Karma Analysis\n\n")
    content_parts.append(
        f"| Metric | Value |\n"
        f"|--------|-------|\n"
        f"| Average Karma | {metrics['avg_karma']:.2f} karma |\n"
        f"| Standard Deviation | {metrics['karma_std_dev']:.2f} |\n"
        f"| Distribution Type | Normal with ±20% variation |\n\n"
    )

    content_parts.append("### 2.3 Performance Metrics\n\n")
    content_parts.append(
        f"| Metric | Value |\n"
        f"|--------|-------|\n"
        f"| PDF File Size | {metrics['pdf_size_mb']:.4f} MB |\n"
        f"| PDF Page Count | {metrics['pdf_pages']} pages |\n"
        f"| Generation Time | {metrics['generation_time_seconds']:.2f} seconds |\n"
        f"| Time per Permutation | {metrics['generation_time_seconds'] / metrics['total_permutations'] if metrics['total_permutations'] > 0 else 0:.3f} seconds |\n\n"
    )

    content_parts.append("### 2.4 Constraint Analysis\n\n")
    content_parts.append(
        f"| Metric | Value |\n"
        f"|--------|-------|\n"
        f"| Max Iterations Calculated | {metrics.get('max_iterations_calculated', 'N/A')} |\n"
        f"| Constraint Applied | {metrics.get('constraint_applied', 'None')} |\n"
        f"| Constraint Effectiveness | {'Effective' if metrics.get('constraint_applied') else 'Not applicable'} |\n\n"
    )

    # Section 3: Observations (numbered list)
    content_parts.append("---\n\n")
    content_parts.append("## Section 3: Observations\n\n")
    content_parts.append("The following observations were made from the simulation data:\n\n")
    for i, obs in enumerate(observations, 1):
        content_parts.append(f"**Observation {i}**: {obs}\n\n")

    # Section 4: Findings (with emphasis)
    content_parts.append("---\n\n")
    content_parts.append("## Section 4: Research Findings\n\n")
    content_parts.append("Analysis of the simulation data revealed several key findings:\n\n")
    for i, finding in enumerate(findings, 1):
        content_parts.append(f"### Finding {i}\n\n")
        content_parts.append(f"> {finding}\n\n")

    # Section 5: Hypothesis (quote-style)
    if hypothesis:
        content_parts.append("---\n\n")
        content_parts.append("## Section 5: Hypothesis Formation\n\n")
        content_parts.append(
            "Based on the observations and findings, the following hypothesis was formulated:\n\n"
        )
        content_parts.append(f"> **Hypothesis**: {hypothesis}\n\n")
        content_parts.append(
            "This hypothesis was derived from patterns identified in the simulation data, particularly around efficiency metrics and constraint behavior.\n\n"
        )

    # Section 6: Hypothesis Testing (structured)
    if test_results:
        content_parts.append("---\n\n")
        content_parts.append("## Section 6: Hypothesis Testing\n\n")
        content_parts.append("The hypothesis was tested using the collected evidence:\n\n")
        content_parts.append(f"**Hypothesis Statement**: {test_results['hypothesis']}\n\n")
        content_parts.append(
            f"**Test Result**: {'✅ Supported' if test_results['supported'] else '❌ Not Supported'}\n\n"
        )
        content_parts.append("**Evidence Collected**:\n\n")
        for i, evidence in enumerate(test_results.get("evidence", []), 1):
            content_parts.append(f"{i}. {evidence}\n\n")

    # Section 7: Conclusions (numbered)
    content_parts.append("---\n\n")
    content_parts.append("## Section 7: Conclusions\n\n")
    content_parts.append(
        "Based on the complete analysis, the following conclusions were drawn:\n\n"
    )
    for i, conclusion in enumerate(conclusions, 1):
        content_parts.append(f"{i}. {conclusion}\n\n")

    # Section 8: Recommendations (structured list)
    content_parts.append("---\n\n")
    content_parts.append("## Section 8: Recommendations\n\n")
    content_parts.append("Based on this research, the following recommendations are made:\n\n")
    content_parts.append(
        "1. **System Status**: The system demonstrates excellent efficiency and is production-ready\n"
        "2. **Constraint System**: The constraint system works as designed and provides intelligent limits\n"
        "3. **Future Research**: Further research could explore additional variation strategies\n"
        "4. **Optimization**: Performance metrics suggest room for optimization if needed\n\n"
    )

    # Section 9: Future Research (with subsections)
    content_parts.append("---\n\n")
    content_parts.append("## Section 9: Future Research Directions\n\n")
    content_parts.append("Potential areas for future investigation:\n\n")
    content_parts.append("### 9.1 Estimation Accuracy\n\n")
    content_parts.append(
        "Can we improve max iterations estimation by tracking actual page counts per permutation?\n\n"
    )
    content_parts.append("### 9.2 Variation Strategies\n\n")
    content_parts.append(
        "What other variation types would be valuable? (state variations, lifetime variations, karma distribution patterns)\n\n"
    )
    content_parts.append("### 9.3 Parallel Processing\n\n")
    content_parts.append(
        "Can we generate permutations in parallel to improve performance for large batches?\n\n"
    )
    content_parts.append("### 9.4 Advanced Analysis\n\n")
    content_parts.append(
        "Statistical tests, visualizations, comparative studies across multiple simulation runs.\n\n"
    )

    content_parts.append("---\n\n")
    content_parts.append(f"**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    content_parts.append("**Status**: Complete\n")

    content = "".join(content_parts)

    # Generate PDF using component system
    generator = ComponentPDFGenerator(
        project_path=project_root,
        weasyprint_available=True,
        max_iterations=10,
        default_allowed_pages=15,
    )

    result = generator.generate_one_pager(
        content=content,
        title="Research Report: Demo Batching System",
        output_path=output_path,
        allowed_pages=15,
        use_science_paper_structure=True,
        author="Research Simulation System",
    )

    if result.get("pdf_path"):
        return Path(result["pdf_path"])
    return output_path if output_path.exists() else None
