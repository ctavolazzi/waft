"""
Generate D&D Campaign PDF Evolution Report
==========================================

Creates a comprehensive PDF report documenting the PDF evolution testing process
and findings from the D&D campaign document generation.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.evolution.pdf_generator import PDFGenerator


def main():
    """Generate evolution report PDF."""
    print("📄 Generating D&D Campaign PDF Evolution Report...")
    
    findings_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "pdf_evolution_findings.md"
    output_path = project_root / "_work_efforts" / "WE-260112-jqkn_d_d_campaign_pdf_evolution" / "pdf_evolution_report.pdf"
    
    if not findings_path.exists():
        print(f"❌ Findings document not found: {findings_path}")
        return 1
    
    content = findings_path.read_text()
    
    generator = PDFGenerator.from_content(
        content=content,
        title="D&D Campaign PDF Evolution Report",
        style="premium",
        output_path=output_path
    )
    
    result = generator.save(
        output_path=output_path,
        convert_to_png=True,
        png_dpi=300
    )
    
    print(f"✅ Evolution report generated: {result}")
    print(f"   📄 {output_path.name}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
