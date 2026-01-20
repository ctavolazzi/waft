#!/usr/bin/env python3
"""
Example: Enable PDF Metrics Collection

Demonstrates how to enable metrics collection for PDF generation
to support evolution with quality data.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution import (
    ChatDistiller,
    ColorGene,
    FontGene,
    LayoutGene,
    MarginGene,
    StylingGene,
    StylingGenome,
    TwoPageGenerator,
)


def main():
    """Example: Generate PDF with metrics collection enabled."""

    # Sample chat content
    chat_content = """
    # Example Chat Session
    
    We discussed implementing a new feature for user authentication.
    The decision was made to use OAuth2 for security and flexibility.
    We learned that token refresh is critical for long sessions.
    """

    # Distill chat
    distiller = ChatDistiller()
    distilled = distiller.distill_text(chat_content, title="Example Session")

    # Create styling genome
    styling_genes = StylingGene(
        font=FontGene(family="sans-serif", size_body=11),
        margin=MarginGene(top=20, bottom=20, left=20, right=20),
        color=ColorGene(text="#000000", background="#FFFFFF", accent="#0066cc"),
        layout=LayoutGene(columns=1, density="normal"),
    )
    genome = StylingGenome.from_genes(styling_genes)

    # Generate PDF WITH METRICS COLLECTION
    generator = TwoPageGenerator(weasyprint_available=True)
    output_path = Path("example_with_metrics.pdf")

    result = generator.generate(
        distilled_chat=distilled,
        styling_genome=genome,
        output_path=output_path,
        target_pages=2,
        collect_metrics=True,  # ✅ Enable metrics collection
        metrics_dir=Path("_pyrite/metrics/pdf"),  # Optional: custom directory
    )

    # Access metrics from result
    if "metrics" in result:
        metrics = result["metrics"]
        print("\n📊 Metrics Collected:")
        print(f"  Quality Grade: {metrics['quality_grade']}")
        print(f"  Quality Score: {metrics['quality_score']:.3f}")
        print(f"  Fitness Overall: {metrics['fitness_overall']:.3f}")
        print(f"  Generation Time: {metrics['generation_time_seconds']:.2f}s")
        print(f"  Iterations Used: {metrics['iterations_used']}")
        print(f"  Constraint Satisfied: {metrics['constraint_satisfied']}")
        print(f"  Metrics File: {result['metrics_file']}")

    print(f"\n✅ PDF generated: {output_path}")
    print("📊 Metrics saved to _pyrite/metrics/pdf/")


if __name__ == "__main__":
    main()
