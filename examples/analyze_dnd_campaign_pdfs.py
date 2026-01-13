"""
Analyze D&D Campaign PDFs
==========================

Uses ScientificPDFGenerator to analyze the quality of generated campaign PDFs
and document findings for PDF evolution.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.evolution.scientific_pdf_generator import ScientificPDFGenerator
from src.waft.evolution.pdf_generator import PDFGenerator


def analyze_pdf(pdf_path: Path, title: str):
    """Analyze a single PDF and return analysis results."""
    print(f"\n📊 Analyzing: {title}")
    print(f"   File: {pdf_path.name}")
    
    if not pdf_path.exists():
        print(f"   ❌ PDF not found: {pdf_path}")
        return None
    
    try:
        # Read the PDF content (we'll analyze the markdown source)
        # For now, we'll create a ScientificPDFGenerator from the markdown
        # and analyze it
        
        # Find corresponding markdown file
        md_name = pdf_path.stem.replace(".pdf", "") + ".md"
        md_path = pdf_path.parent / md_name
        
        if not md_path.exists():
            print(f"   ⚠️  Markdown source not found: {md_name}")
            return None
        
        # Create generator from markdown
        content = md_path.read_text()
        
        # Determine style based on document type
        if "players_guide" in pdf_path.stem:
            style = "premium"
        elif "dm_guide" in pdf_path.stem:
            style = "clinical_standard"
        elif "encounters" in pdf_path.stem:
            style = "clinical_standard"
        elif "world_map" in pdf_path.stem:
            style = "premium"
        elif "npcs" in pdf_path.stem:
            style = "clinical_standard"
        else:
            style = "clinical_standard"
        
        # Create scientific generator
        generator = ScientificPDFGenerator.from_content(
            content=content,
            title=title,
            style=style,
            scientific_mode=True
        )
        
        # Analyze quality
        analysis = generator.analyze_quality()
        
        print(f"   ✅ Analysis complete")
        print(f"   Quality Score: {analysis.get('quality_score', 'N/A')}")
        print(f"   Readability: {analysis.get('readability_score', 'N/A')}")
        print(f"   Completeness: {analysis.get('completeness_score', 'N/A')}")
        
        # Get gaps
        gaps = analysis.get('gaps', [])
        if gaps:
            print(f"   Gaps identified: {len(gaps)}")
            for gap in gaps[:3]:  # Show first 3
                print(f"      - {gap}")
        
        # Get suggestions
        suggestions = analysis.get('suggestions', [])
        if suggestions:
            print(f"   Suggestions: {len(suggestions)}")
            for suggestion in suggestions[:3]:  # Show first 3
                print(f"      - {suggestion}")
        
        return {
            'title': title,
            'pdf_path': pdf_path,
            'analysis': analysis,
            'file_size_kb': pdf_path.stat().st_size / 1024
        }
        
    except Exception as e:
        print(f"   ❌ Error analyzing PDF: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Analyze all campaign PDFs."""
    print("=" * 60)
    print("D&D Campaign PDF Quality Analysis")
    print("=" * 60)
    
    work_effort_dir = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution"
    
    pdfs_to_analyze = [
        ("Player's Guide", work_effort_dir / "campaign_players_guide.pdf"),
        ("DM Guide", work_effort_dir / "campaign_dm_guide.pdf"),
        ("Encounter Sheets", work_effort_dir / "campaign_encounters.pdf"),
        ("World Map", work_effort_dir / "campaign_world_map.pdf"),
        ("NPC Cards", work_effort_dir / "campaign_npcs.pdf"),
    ]
    
    results = []
    
    for title, pdf_path in pdfs_to_analyze:
        result = analyze_pdf(pdf_path, title)
        if result:
            results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Analysis Summary")
    print("=" * 60)
    
    if results:
        print(f"\nAnalyzed {len(results)} PDFs:")
        for result in results:
            print(f"\n   {result['title']}:")
            print(f"      Size: {result['file_size_kb']:.1f} KB")
            analysis = result['analysis']
            if 'quality_score' in analysis:
                print(f"      Quality: {analysis['quality_score']:.2f}/1.0")
            if 'readability_score' in analysis:
                print(f"      Readability: {analysis['readability_score']:.2f}/1.0")
            if 'completeness_score' in analysis:
                print(f"      Completeness: {analysis['completeness_score']:.2f}/1.0")
        
        # Save results to JSON
        results_file = work_effort_dir / "pdf_analysis_results.json"
        import json
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n✅ Analysis results saved to: {results_file}")
    else:
        print("\n❌ No PDFs were successfully analyzed")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
