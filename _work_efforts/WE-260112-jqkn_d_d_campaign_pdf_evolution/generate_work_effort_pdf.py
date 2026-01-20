"""
Generate Complete Work Effort PDF
=================================

Converts the entire work effort into a comprehensive PDF document including:
- All markdown files
- Generated PDFs (as references)
- Screenshots/PNG files
- Analysis results
- Code examples
- Complete documentation

Output: A single comprehensive PDF documenting the entire work effort.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.waft.evolution.scientific_pdf_generator import ScientificPDFGenerator


def collect_work_effort_content(work_effort_dir: Path):
    """Collect all content from the work effort."""
    content_sections = []

    # 1. Index/Overview
    index_file = work_effort_dir / "WE-260112-jqkn_index.md"
    if index_file.exists():
        content_sections.append(
            {"title": "Work Effort Overview", "content": index_file.read_text(), "type": "overview"}
        )

    # 2. Campaign Content Files
    campaign_files = [
        ("Player's Guide", "campaign_players_guide.md"),
        ("Dungeon Master's Guide", "campaign_dm_guide.md"),
        ("Encounter Reference", "campaign_encounters.md"),
        ("World Map & Locations", "campaign_world_map.md"),
        ("NPC Reference Cards", "campaign_npcs.md"),
    ]

    for title, filename in campaign_files:
        file_path = work_effort_dir / filename
        if file_path.exists():
            content_sections.append(
                {
                    "title": title,
                    "content": file_path.read_text(),
                    "type": "campaign_content",
                    "source_file": filename,
                }
            )

    # 3. Findings and Analysis
    findings_file = work_effort_dir / "pdf_evolution_findings.md"
    if findings_file.exists():
        content_sections.append(
            {
                "title": "PDF Evolution Findings",
                "content": findings_file.read_text(),
                "type": "analysis",
            }
        )

    # 4. Analysis Results (JSON summary)
    analysis_file = work_effort_dir / "pdf_analysis_results.json"
    if analysis_file.exists():
        try:
            analysis_data = json.loads(analysis_file.read_text())
            analysis_summary = format_analysis_summary(analysis_data)
            content_sections.append(
                {
                    "title": "Quality Analysis Results",
                    "content": analysis_summary,
                    "type": "analysis",
                }
            )
        except Exception as e:
            print(f"Warning: Could not parse analysis JSON: {e}")

    # 5. Generated PDFs (list as references)
    pdf_files = list(work_effort_dir.glob("*.pdf"))
    if pdf_files:
        pdf_list = format_pdf_references(pdf_files, work_effort_dir)
        content_sections.append(
            {"title": "Generated PDFs", "content": pdf_list, "type": "references"}
        )

    # 6. Screenshots/PNG Files (list as references)
    png_files = list(work_effort_dir.glob("*.png"))
    if png_files:
        png_list = format_png_references(png_files, work_effort_dir)
        content_sections.append(
            {"title": "Screenshots & Visual References", "content": png_list, "type": "references"}
        )

    # 7. Code Examples
    code_files = [
        ("PDF Generation Script", "examples/generate_dnd_campaign_pdfs.py"),
        ("PDF Analysis Script", "examples/analyze_dnd_campaign_pdfs.py"),
        ("Evolution Report Script", "examples/generate_dnd_evolution_report.py"),
    ]

    code_content = []
    for title, rel_path in code_files:
        file_path = project_root / rel_path
        if file_path.exists():
            code_content.append(f"## {title}\n\n")
            code_content.append(f"**File:** `{rel_path}`\n\n")
            code_content.append("```python\n")
            code_content.append(file_path.read_text())
            code_content.append("\n```\n\n")

    if code_content:
        content_sections.append(
            {"title": "Code Examples", "content": "".join(code_content), "type": "code"}
        )

    return content_sections


def format_analysis_summary(analysis_data):
    """Format analysis JSON data as markdown."""
    content = ["## Quality Analysis Summary\n\n"]

    if isinstance(analysis_data, list):
        for item in analysis_data:
            title = item.get("title", "Unknown")
            file_size = item.get("file_size_kb", 0)
            analysis = item.get("analysis", {})

            content.append(f"### {title}\n\n")
            content.append(f"**File Size:** {file_size:.1f} KB\n\n")

            scores = analysis.get("scores", {})
            if scores:
                content.append("**Scores:**\n")
                for key, value in scores.items():
                    content.append(f"- {key.title()}: {value:.2f}\n")
                content.append("\n")

            gaps = analysis.get("gaps", [])
            if gaps:
                content.append("**Gaps Identified:**\n")
                for gap in gaps[:5]:  # Limit to 5
                    content.append(f"- {gap}\n")
                content.append("\n")

            suggestions = analysis.get("suggestions", [])
            if suggestions:
                content.append("**Suggestions:**\n")
                for suggestion in suggestions[:3]:  # Limit to 3
                    content.append(f"- {suggestion}\n")
                content.append("\n")

            content.append("---\n\n")

    return "".join(content)


def format_pdf_references(pdf_files, work_effort_dir):
    """Format PDF file list as markdown."""
    content = ["## Generated PDF Documents\n\n"]
    content.append("The following PDFs were generated as part of this work effort:\n\n")

    for pdf_file in sorted(pdf_files):
        size_kb = pdf_file.stat().st_size / 1024
        rel_path = pdf_file.relative_to(work_effort_dir)
        content.append(f"- **{pdf_file.stem}**\n")
        content.append(f"  - File: `{rel_path}`\n")
        content.append(f"  - Size: {size_kb:.1f} KB\n\n")

    return "".join(content)


def format_png_references(png_files, work_effort_dir):
    """Format PNG file list as markdown."""
    content = ["## Screenshots & Visual References\n\n"]
    content.append("The following screenshots were generated for visual verification:\n\n")

    for png_file in sorted(png_files):
        size_kb = png_file.stat().st_size / 1024
        rel_path = png_file.relative_to(work_effort_dir)
        content.append(f"- **{png_file.stem}**\n")
        content.append(f"  - File: `{rel_path}`\n")
        content.append(f"  - Size: {size_kb:.1f} KB\n\n")

    content.append(
        "\n*Note: PNG files are visual representations of generated PDFs for quality verification.*\n"
    )

    return "".join(content)


def build_complete_document(content_sections):
    """Build complete markdown document from all sections."""
    doc_parts = []

    # Title and metadata
    doc_parts.append("# D&D Campaign PDF Evolution - Complete Work Effort\n\n")
    doc_parts.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    doc_parts.append("---\n\n")

    # Table of Contents
    doc_parts.append("## Table of Contents\n\n")
    for i, section in enumerate(content_sections, 1):
        doc_parts.append(
            f"{i}. [{section['title']}](#{section['title'].lower().replace(' ', '-').replace('&', '')})\n"
        )
    doc_parts.append("\n---\n\n")

    # Add all sections
    for section in content_sections:
        doc_parts.append(f"# {section['title']}\n\n")

        # Add section metadata if available
        if "source_file" in section:
            doc_parts.append(f"*Source: {section['source_file']}*\n\n")

        doc_parts.append(section["content"])
        doc_parts.append("\n\n---\n\n")

    # Appendices
    doc_parts.append("# Appendices\n\n")
    doc_parts.append("## Work Effort Information\n\n")
    doc_parts.append("- **Work Effort ID:** WE-260112-jqkn\n")
    doc_parts.append("- **Title:** D&D Campaign PDF Evolution\n")
    doc_parts.append("- **Purpose:** Test and evolve PDF generator with diverse document types\n")
    doc_parts.append("- **Status:** Active\n\n")

    doc_parts.append("## Files Included\n\n")
    doc_parts.append("This document consolidates all content from the work effort, including:\n\n")
    doc_parts.append("- Campaign planning documents\n")
    doc_parts.append("- Generated PDFs (referenced)\n")
    doc_parts.append("- Quality analysis results\n")
    doc_parts.append("- Evolution findings\n")
    doc_parts.append("- Code examples\n")
    doc_parts.append("- Screenshots and visual references\n\n")

    return "".join(doc_parts)


def main():
    """Generate complete work effort PDF."""
    print("=" * 60)
    print("Work Effort PDF Generator")
    print("=" * 60)

    work_effort_dir = Path(__file__).parent
    output_path = work_effort_dir / "WE-260112-jqkn_COMPLETE.pdf"

    print(f"\n📁 Work Effort Directory: {work_effort_dir}")
    print(f"📄 Output PDF: {output_path.name}\n")

    # Collect all content
    print("📚 Collecting work effort content...")
    content_sections = collect_work_effort_content(work_effort_dir)
    print(f"   ✅ Found {len(content_sections)} sections")

    # Build complete document
    print("\n📝 Building complete document...")
    complete_content = build_complete_document(content_sections)

    # Save intermediate markdown (for debugging)
    md_path = work_effort_dir / "WE-260112-jqkn_COMPLETE.md"
    md_path.write_text(complete_content)
    print(f"   ✅ Saved markdown: {md_path.name}")

    # Generate PDF
    print("\n📄 Generating PDF...")
    try:
        generator = ScientificPDFGenerator.from_content(
            content=complete_content,
            title="D&D Campaign PDF Evolution - Complete Work Effort",
            style="premium",
            output_path=output_path,
            scientific_mode=True,
        )

        generator.save(output_path=output_path, convert_to_png=True, png_dpi=300)

        # Analyze the generated PDF
        print("\n📊 Analyzing generated PDF...")
        analysis = generator.analyze_quality()

        print("\n✅ Complete work effort PDF generated!")
        print(f"   📄 {output_path.name}")
        print(f"   📊 Size: {output_path.stat().st_size / 1024:.1f} KB")

        if "quality_score" in analysis:
            print(f"   ⭐ Quality Score: {analysis['quality_score']:.2f}/1.0")

        # Summary
        print("\n" + "=" * 60)
        print("📋 Document Summary")
        print("=" * 60)
        print(f"   Sections: {len(content_sections)}")
        print("   Content Types:")
        for section in content_sections:
            print(f"      - {section['title']} ({section['type']})")

        print(f"\n✅ Complete! PDF ready at: {output_path}")

        return 0

    except Exception as e:
        print(f"\n❌ Error generating PDF: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
