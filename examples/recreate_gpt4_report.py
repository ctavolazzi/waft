"""
Recreate GPT-4 Technical Report
================================

Demonstrates DocumentBuilder's ability to analyze and recreate PDFs from scratch.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.document_builder import DocumentBuilder


def main():
    """Recreate the GPT-4 Technical Report."""

    print("📄 Analyzing GPT-4 Technical Report...")
    print("   Source: GPT-4-Techincal-Report.pdf")

    # Analyze the PDF
    builder = DocumentBuilder.from_pdf("GPT-4-Techincal-Report.pdf")

    print("\n✅ Analysis complete:")
    print(f"   Title: {builder.config.title}")
    print(f"   Detected Template: {builder.config.template}")
    print(f"   Pages: {builder._analysis.page_count}")
    print(f"   Sections Found: {len(builder._analysis.sections)}")
    print(f"   Is Academic: {builder._analysis.styling_hints.get('is_academic')}")
    print(f"   Is LaTeX: {builder._analysis.styling_hints.get('is_laTeX')}")

    # Recreate the PDF
    output_path = Path("GPT-4-Techincal-Report_RECREATED.pdf")
    print("\n🔄 Recreating PDF...")
    print(f"   Output: {output_path}")

    try:
        result_path = builder.recreate(output_path)
        print("\n✅ PDF recreated successfully!")
        print(f"   📄 {result_path.absolute()}")

        # Verify page count
        from pypdf import PdfReader

        reader = PdfReader(str(result_path))
        print(f"   Pages: {len(reader.pages)} (original: {builder._analysis.page_count})")

    except Exception as e:
        print(f"\n❌ Error during recreation: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
