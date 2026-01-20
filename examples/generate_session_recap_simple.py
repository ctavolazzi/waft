#!/usr/bin/env python3
"""
Generate Session Recap PDF - Simple Composable API

Demonstrates the new modular, composable PDF generation system.
Much less boilerplate!
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution.pdf_generator import PDFGenerator, generate_pdf


def get_session_content() -> str:
    """Get comprehensive session content."""
    from examples.generate_session_recap_pdf_waft import get_session_content

    return get_session_content()


def main():
    """Generate PDF using simple composable API."""
    print("=" * 80)
    print("📄 Generating Session Recap PDF - Simple Composable API")
    print("=" * 80)

    # Get content
    content = get_session_content()

    # Option 1: Super simple - one function call
    print("\n✨ Option 1: One-liner function call")
    output_path = generate_pdf(
        content=content,
        title="WAFT v0.5.3 MVP: Karma Economy & Source Consciousness",
        style="clinical_standard",
        open_pdf=True,
    )
    print(f"✅ Generated: {output_path}")

    # Option 2: Builder pattern with customization
    print("\n✨ Option 2: Builder pattern with customization")
    generator = PDFGenerator.from_content(
        content=content,
        title="WAFT v0.5.3 MVP: Karma Economy & Source Consciousness",
        style="clinical_standard",
        font_size=12,  # Override preset
        margins=(30, 30, 30, 30),  # Override margins
    )

    # Add custom CSS
    generator.with_custom_css("""
    <style>
        h1 { color: #0d47a1; }
        .note-box { border-left: 5pt solid #0d47a1; }
    </style>
    """)

    output_path2 = generator.save(
        output_path=Path("_work_efforts/session_recaps/KARMA_ECONOMY_SIMPLE.pdf"),
        open_pdf=False,  # Don't open this one
    )
    print(f"✅ Generated: {output_path2}")

    # Option 3: From file
    print("\n✨ Option 3: From file")
    # Save content to temp file for demo
    temp_file = Path("_work_efforts/session_recaps/temp_content.md")
    temp_file.parent.mkdir(parents=True, exist_ok=True)
    temp_file.write_text(content)

    from src.waft.evolution.pdf_generator import generate_pdf_from_file

    output_path3 = generate_pdf_from_file(file_path=temp_file, style="premium", open_pdf=False)
    print(f"✅ Generated: {output_path3}")

    print("\n" + "=" * 80)
    print("🎉 All PDFs generated with simple, composable API!")
    print("=" * 80)
    print("✨ Benefits:")
    print("   • Much less boilerplate")
    print("   • Preset styles (clinical_standard, premium, professional)")
    print("   • Easy customization")
    print("   • Builder pattern support")
    print("   • File-based generation")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
