#!/usr/bin/env python3
"""
Generate Scientific Session Recap PDF - Self-Examination Enabled

Demonstrates PDFs as scientific research tools with:
- Self-examination and quality analysis
- Hypothesis testing
- Research capabilities
- Evolutionary learning
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution.scientific_pdf_generator import generate_scientific_pdf
from src.waft.evolution.pdf_research_tool import PDFResearchTool


def get_session_content() -> str:
    """Get comprehensive session content."""
    from examples.generate_session_recap_pdf_waft import get_session_content
    return get_session_content()


def main():
    """Generate scientific PDF with self-examination."""
    print("=" * 80)
    print("🔬 Generating Scientific Session Recap PDF")
    print("   With Self-Examination & Research Capabilities")
    print("=" * 80)
    
    # Generate PDF with scientific mode
    pdf_path = generate_scientific_pdf(
        content=get_session_content(),
        title="WAFT v0.5.3 MVP: Karma Economy & Source Consciousness",
        style="clinical_standard",
        scientific_mode=True,
        open_pdf=True
    )
    
    print(f"\n✅ PDF generated: {pdf_path}")
    
    # Research tool analysis
    print("\n📊 Research Tool Analysis:")
    print("-" * 80)
    
    research_tool = PDFResearchTool()
    
    # Analyze trends
    trends = research_tool.analyze_trends(time_period="30 days")
    if "message" not in trends:
        print(f"\n📈 Trends (last 30 days):")
        print(f"   Quality Trend: {trends.get('quality_trend', 'N/A')}")
        print(f"   Average Quality: {trends.get('average_quality', 0):.2f}")
        for insight in trends.get("insights", []):
            print(f"   • {insight}")
    
    # Identify patterns
    patterns = research_tool.identify_patterns()
    if "message" not in patterns:
        print(f"\n🔍 Patterns Identified:")
        if patterns.get("styling_patterns", {}).get("most_common"):
            print(f"   Most Common Style: {patterns['styling_patterns']['most_common'][0]}")
        if patterns.get("quality_patterns", {}).get("average"):
            print(f"   Average Quality: {patterns['quality_patterns']['average']:.2f}")
        if patterns.get("content_patterns", {}).get("common_gaps"):
            print(f"   Common Gaps: {len(patterns['content_patterns']['common_gaps'])}")
    
    # Accumulate knowledge
    knowledge = research_tool.accumulate_knowledge()
    print(f"\n🧠 Knowledge Base:")
    print(f"   Total PDFs: {knowledge.get('total_pdfs', 0)}")
    print(f"   Total Hypotheses: {knowledge.get('total_hypotheses', 0)}")
    print(f"   Total Findings: {knowledge.get('total_findings', 0)}")
    
    print("\n" + "=" * 80)
    print("🎉 Scientific PDF Generated with Self-Examination!")
    print("=" * 80)
    print("✨ Features Enabled:")
    print("   ✅ Self-examination and quality analysis")
    print("   ✅ Hypothesis testing capabilities")
    print("   ✅ Research tool integration")
    print("   ✅ Evolutionary learning")
    print("=" * 80)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
