#!/usr/bin/env python3
"""
Generate WAFT Docs - Command Line Interface
===========================================

Command-line interface for generating WAFT documentation:
- Field guides (layman, professional, scientist)
- Printer-friendly versions
- Complete booklets
- Session summaries
- PDF redaction

Usage:
    python scripts/generate_waft_docs.py field-guide
    python scripts/generate_waft_docs.py field-guide --printer-friendly
    python scripts/generate_waft_docs.py booklet
    python scripts/generate_waft_docs.py session-summary
    python scripts/generate_waft_docs.py redact --input file.pdf --areas "100,200,300,400"
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from examples.generate_session_summary import generate_session_summary
from examples.generate_waft_field_guide import (
    generate_complete_booklet,
    generate_level_1_layman,
    generate_level_2_professional,
    generate_level_3_scientist,
)
from examples.generate_waft_field_guide_printer_friendly import (
    generate_field_guide_printer_friendly,
)
from src.waft.pdf_redactor import PDFRedactor


def generate_field_guides(output_dir: Path, printer_friendly: bool = False, level: str = None):
    """Generate field guides at specified levels."""
    output_dir.mkdir(parents=True, exist_ok=True)

    levels = {
        "layman": generate_level_1_layman,
        "professional": generate_level_2_professional,
        "scientist": generate_level_3_scientist,
    }

    if level:
        if level not in levels:
            print(
                f"Error: Invalid level '{level}'. Must be one of: layman, professional, scientist"
            )
            return False

        print(f"Generating Level: {level.capitalize()}...")
        if printer_friendly:
            # Use printer-friendly generator
            generate_field_guide_printer_friendly(level=level, output_dir=output_dir)
        else:
            # Use standard generator
            levels[level](output_dir)
        print(f"✓ Generated {level} field guide")
    else:
        # Generate all levels
        print("Generating all field guide levels...")
        for level_name, generator in levels.items():
            print(f"  - Generating {level_name}...")
            if printer_friendly:
                generate_field_guide_printer_friendly(level=level_name, output_dir=output_dir)
            else:
                generator(output_dir)
        print("✓ Generated all field guides")

    return True


def generate_booklet(output_dir: Path, printer_friendly: bool = False):
    """Generate complete booklet combining all field guides."""
    output_dir.mkdir(parents=True, exist_ok=True)

    print(
        f"Generating complete booklet ({'printer-friendly' if printer_friendly else 'standard'})..."
    )

    if printer_friendly:
        # Use printer-friendly booklet generator
        generate_complete_booklet_pf(output_dir)
        print("✓ Generated printer-friendly complete booklet")
    else:
        # Use standard booklet generator
        generate_complete_booklet(output_dir)
        print("✓ Generated complete booklet")

    return True


def generate_summary(output_dir: Path):
    """Generate session summary PDF."""
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Generating session summary...")
    generate_session_summary()
    print("✓ Generated session summary")

    return True


def redact_pdf(input_path: Path, output_path: Path, areas: list):
    """Redact specified areas in a PDF."""
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return False

    print(f"Redacting PDF: {input_path.name}")
    print(f"  Areas to redact: {len(areas)}")

    redactor = PDFRedactor(input_path)

    for i, area_str in enumerate(areas):
        # Parse area string: "x,y,width,height" or "x,y,width,height:label"
        parts = area_str.split(":")
        coords_str = parts[0]
        label = parts[1] if len(parts) > 1 else f"Area {i + 1}"

        try:
            x, y, width, height = map(float, coords_str.split(","))
            redactor.add_area_redaction(x, y, width, height, label=label)
            print(f"  - Added redaction: {label} at ({x}, {y}), size {width}x{height}")
        except ValueError as e:
            print(f"Error: Invalid area format '{area_str}': {e}")
            print("  Format should be: x,y,width,height or x,y,width,height:label")
            return False

    redactor.save(output_path)
    print(f"✓ Redacted PDF saved: {output_path}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate WAFT documentation: field guides, booklets, summaries, and redaction"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Field guide command
    fg_parser = subparsers.add_parser("field-guide", help="Generate field guides")
    fg_parser.add_argument(
        "--printer-friendly", action="store_true", help="Generate printer-friendly version"
    )
    fg_parser.add_argument(
        "--level",
        choices=["layman", "professional", "scientist"],
        help="Generate specific level only",
    )

    # Booklet command
    booklet_parser = subparsers.add_parser("booklet", help="Generate complete booklet")
    booklet_parser.add_argument(
        "--printer-friendly", action="store_true", help="Generate printer-friendly version"
    )

    # Session summary command
    subparsers.add_parser("session-summary", help="Generate session summary")

    # Redact command
    redact_parser = subparsers.add_parser("redact", help="Redact PDF")
    redact_parser.add_argument("--input", required=True, type=Path, help="Input PDF path")
    redact_parser.add_argument(
        "--output", type=Path, help="Output PDF path (default: input_redacted.pdf)"
    )
    redact_parser.add_argument(
        "--areas",
        nargs="+",
        required=True,
        help='Areas to redact: "x,y,width,height" or "x,y,width,height:label"',
    )

    # All command
    all_parser = subparsers.add_parser("all", help="Generate everything")
    all_parser.add_argument(
        "--printer-friendly", action="store_true", help="Include printer-friendly versions"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    output_dir = Path("_work_efforts/showcase_documents")

    print("=" * 60)
    print("WAFT Document Generator")
    print("=" * 60)
    print()

    success = True

    if args.command == "field-guide":
        success = generate_field_guides(
            output_dir, printer_friendly=args.printer_friendly, level=args.level
        )

    elif args.command == "booklet":
        success = generate_booklet(output_dir, printer_friendly=args.printer_friendly)

    elif args.command == "session-summary":
        success = generate_summary(output_dir)

    elif args.command == "redact":
        input_path = args.input
        output_path = args.output or input_path.parent / f"{input_path.stem}_redacted.pdf"
        success = redact_pdf(input_path, output_path, args.areas)

    elif args.command == "all":
        print("Generating complete documentation set...")
        print()

        # Generate standard field guides
        print("1. Generating standard field guides...")
        success = generate_field_guides(output_dir, printer_friendly=False)
        print()

        # Generate booklet
        if success:
            print("2. Generating complete booklet...")
            success = generate_booklet(output_dir, printer_friendly=False)
            print()

        # Generate printer-friendly versions if requested
        if success and args.printer_friendly:
            print("3. Generating printer-friendly field guides...")
            success = generate_field_guides(output_dir, printer_friendly=True)
            print()

        # Generate session summary
        if success:
            print("4. Generating session summary...")
            success = generate_summary(output_dir)
            print()

    print("=" * 60)
    if success:
        print("✓ Generation complete!")
        print(f"  Output directory: {output_dir}")
    else:
        print("✗ Generation failed - see errors above")
    print("=" * 60)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
