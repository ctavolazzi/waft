#!/usr/bin/env python3
"""
Generate Test PDFs for Evolutionary Iteration Process

Generates test PDFs with different styling configurations for comparison testing.
Creates PNG screenshots automatically for visual comparison.

Usage:
    python tools/generate_test_pdfs.py --count 5 --output test_outputs/
    python tools/generate_test_pdfs.py --styles clinical_standard,premium --output test_outputs/
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.waft.evolution.pdf_generator import generate_pdf


def generate_test_pdfs(
    count: int = 5, output_dir: Path = None, styles: list = None, title_prefix: str = "Test PDF"
) -> list[Path]:
    """
    Generate test PDFs with PNG screenshots.

    Args:
        count: Number of PDFs to generate
        output_dir: Output directory (default: _work_efforts/one_pagers/test/)
        styles: List of style names (default: all available styles)
        title_prefix: Prefix for PDF titles

    Returns:
        List of generated PDF paths
    """
    if output_dir is None:
        output_dir = project_root / "_work_efforts" / "one_pagers" / "test"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if styles is None:
        styles = ["clinical_standard", "premium", "professional"]

    # Test content
    test_content = """# Test Document

This is a test document for the evolutionary iteration process.

## Section 1: Introduction

The evolutionary iteration process enables evidence-based debugging through visual verification.

## Section 2: Features

- Visual verification
- Before/after comparison
- Iterative improvement
- Evidence-based debugging

## Section 3: Conclusion

This process creates a feedback loop that enables rapid improvement.
"""

    generated_pdfs = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for i in range(count):
        style = styles[i % len(styles)]
        title = f"{title_prefix} {i + 1} - {style}"
        output_path = output_dir / f"test_{timestamp}_{i + 1:03d}_{style}.pdf"

        print(f"Generating {title}...")

        try:
            pdf_path = generate_pdf(
                content=test_content,
                title=title,
                output_path=output_path,
                style=style,
                convert_to_png=True,  # Enable PNG conversion
                png_dpi=300,
                open_pdf=False,
            )
            generated_pdfs.append(pdf_path)
            print(f"  ✅ Generated: {pdf_path}")
            print(f"  📸 PNG: {pdf_path.with_suffix('.png')}")
        except Exception as e:
            print(f"  ❌ Failed: {e}")

    return generated_pdfs


def main():
    parser = argparse.ArgumentParser(description="Generate test PDFs for comparison")
    parser.add_argument(
        "--count", type=int, default=5, help="Number of PDFs to generate (default: 5)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output directory (default: _work_efforts/one_pagers/test/)",
    )
    parser.add_argument(
        "--styles", type=str, default=None, help="Comma-separated list of styles (default: all)"
    )
    parser.add_argument(
        "--prefix", type=str, default="Test PDF", help="Title prefix (default: 'Test PDF')"
    )

    args = parser.parse_args()

    styles = None
    if args.styles:
        styles = [s.strip() for s in args.styles.split(",")]

    print(f"Generating {args.count} test PDFs...")
    print(f"Output: {args.output or '_work_efforts/one_pagers/test/'}")
    print(f"Styles: {styles or 'all available'}")
    print()

    pdfs = generate_test_pdfs(
        count=args.count, output_dir=args.output, styles=styles, title_prefix=args.prefix
    )

    print()
    print(f"✅ Generated {len(pdfs)} PDFs with PNG screenshots")
    print(f"📁 Location: {args.output or '_work_efforts/one_pagers/test/'}")
    print()
    print("Next steps:")
    print("  - Compare PDFs visually")
    print("  - Use comparison tools (when available)")
    print("  - Analyze differences")
    print("  - Iterate and improve")


if __name__ == "__main__":
    main()
