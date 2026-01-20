#!/usr/bin/env python3
"""
Convert PNG Images to PDF Binder

Converts a folder of PNG images (8.5 x 11 inch) into a PDF binder.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution import convert_images_to_pdf


def main():
    """Convert PNG images to PDF binder."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert PNG images to PDF binder (8.5 x 11 inches)"
    )
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Directory containing PNG images",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output PDF path (default: input_dir/binder.pdf)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="DPI for PDF (default: 300)",
    )
    parser.add_argument(
        "--no-crop",
        action="store_true",
        help="Don't crop images, scale to fit instead",
    )

    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"❌ Error: Directory not found: {input_dir}")
        sys.exit(1)

    # Find all PNG files
    png_files = sorted(input_dir.glob("*.png"))
    if not png_files:
        print(f"❌ Error: No PNG files found in {input_dir}")
        sys.exit(1)

    print(f"📁 Found {len(png_files)} PNG images")
    for png_file in png_files:
        print(f"   - {png_file.name}")
    print()

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_dir / "binder.pdf"

    print(f"📄 Converting to PDF: {output_path}")
    print("   - Page size: 8.5 x 11 inches")
    print(f"   - DPI: {args.dpi}")
    print(f"   - Crop to size: {not args.no_crop}")
    print()

    try:
        result_path = convert_images_to_pdf(
            png_files,
            output_path,
            page_size=(8.5, 11.0),
            dpi=args.dpi,
            crop=not args.no_crop,
        )

        print(f"✅ PDF created: {result_path}")
        print(f"   - Pages: {len(png_files)}")

        # Open the PDF
        import subprocess

        subprocess.run(["open", "-a", "Preview", str(result_path)])
        print("📖 PDF opened in Preview")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
