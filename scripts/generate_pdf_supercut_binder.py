#!/usr/bin/env python3
"""
Generate PDF Supercut Binder

Systematically goes through each PDF generator in WAFT, generates a real PDF,
saves it to a folder, then combines all PDFs into one big binder PDF.
"""

import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Real content for PDF generation
REAL_CONTENT = """
# WAFT PDF Generation System - Complete Documentation

**Generated**: {timestamp}

## System Overview

WAFT provides comprehensive PDF generation capabilities through multiple generators, each optimized for different use cases. This document demonstrates the actual output from each generator in the system.

## Key Features

- Multiple generator classes with different capabilities
- Preset styling configurations
- Component-based adaptive layouts
- Scientific research tools
- Template system for specialized documents
- Foundation system for block-based generation

## Technical Architecture

The WAFT PDF generation system uses:
- WeasyPrint for HTML/CSS to PDF conversion
- FPDF2 for pure Python PDF generation
- Adaptive algorithms for constraint satisfaction
- Evolutionary styling genomes
- Component-based document structures

## Use Cases

1. **Research Documents**: Scientific papers, lab notebooks, research reports
2. **Technical Documentation**: Field guides, manuals, technical memos
3. **Professional Reports**: Clinical standards, status reports, summaries
4. **One-Pagers**: Quick summaries, overviews, handouts
5. **Evolutionary Documents**: Self-improving content with learning

## Conclusion

This document was generated using the {generator_name} generator, demonstrating the actual output quality and formatting capabilities of the WAFT system.
"""


def generate_pdfgenerator_pdfs(output_dir: Path) -> list[Path]:
    """Generate PDFs from PDFGenerator with all styles."""
    print("📄 PDFGenerator...")

    from src.waft.evolution.pdf_generator import PDFGenerator

    pdfs = []
    styles = ["clinical_standard", "premium", "professional"]

    for style in styles:
        print(f"   - {style}")
        pdf_path = output_dir / f"pdfgenerator_{style}.pdf"

        content = REAL_CONTENT.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            generator_name=f"PDFGenerator ({style})",
        )

        generator = PDFGenerator.from_content(
            content=content, title=f"PDFGenerator - {style.replace('_', ' ').title()}", style=style
        )
        generator.save(pdf_path, convert_to_png=False, open_pdf=False)
        pdfs.append(pdf_path)

    return pdfs


def generate_scientific_pdf(output_dir: Path) -> list[Path]:
    """Generate PDF from ScientificPDFGenerator."""
    print("📄 ScientificPDFGenerator...")

    try:
        from src.waft.evolution.scientific_pdf_generator import ScientificPDFGenerator

        pdfs = []
        pdf_path = output_dir / "scientific_pdfgenerator.pdf"

        content = REAL_CONTENT.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            generator_name="ScientificPDFGenerator",
        )

        generator = ScientificPDFGenerator.from_content(
            content=content,
            title="ScientificPDFGenerator - Research Tools",
            style="clinical_standard",
            scientific_mode=True,
        )
        generator.save(pdf_path, convert_to_png=False, open_pdf=False)
        pdfs.append(pdf_path)

        return pdfs
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
        return []


def generate_component_pdf(output_dir: Path) -> list[Path]:
    """Generate PDF from ComponentPDFGenerator."""
    print("📄 ComponentPDFGenerator...")

    try:
        from src.waft.evolution.component_generator import ComponentPDFGenerator

        pdfs = []
        pdf_path = output_dir / "component_pdfgenerator.pdf"

        content = REAL_CONTENT.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            generator_name="ComponentPDFGenerator",
        )

        generator = ComponentPDFGenerator()
        result = generator.generate_one_pager(
            content=content,
            title="ComponentPDFGenerator - Adaptive Layout",
            output_path=pdf_path,
            allowed_pages=2,
            convert_to_png=False,
        )

        pdf_path_result = result.get("pdf_path")
        if pdf_path_result:
            pdf_path_obj = (
                Path(pdf_path_result) if isinstance(pdf_path_result, str) else pdf_path_result
            )
            if pdf_path_obj.exists():
                pdfs.append(pdf_path_obj)

        return pdfs
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
        return []


def generate_template_pdfs(output_dir: Path) -> list[Path]:
    """Generate PDFs from template system."""
    print("📄 Template System...")

    pdfs = []
    content_html = REAL_CONTENT.format(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), generator_name="Template System"
    ).replace("\n", "<br>")

    # Field Guide
    try:
        from src.waft.templates.field_guide import generate_field_guide

        print("   - Field Guide")
        pdf_path = output_dir / "template_field_guide.pdf"
        generate_field_guide(
            title="WAFT Field Guide",
            content=f"<div>{content_html}</div>",
            output_path=pdf_path,
            series="FIELD GUIDE",
            number="FG-001",
        )
        if pdf_path.exists():
            pdfs.append(pdf_path)
    except Exception as e:
        print(f"   ⚠️  Field Guide error: {e}")

    # Lab Notes
    try:
        from src.waft.templates.lab_notes import generate_lab_notes

        print("   - Lab Notes")
        pdf_path = output_dir / "template_lab_notes.pdf"
        generate_lab_notes(
            title="WAFT Lab Notes",
            content=f"<div>{content_html}</div>",
            output_path=pdf_path,
            lab_id="LAB-001",
            date=datetime.now().strftime("%Y-%m-%d"),
        )
        if pdf_path.exists():
            pdfs.append(pdf_path)
    except Exception as e:
        print(f"   ⚠️  Lab Notes error: {e}")

    # Technical Memo
    try:
        from src.waft.templates.tm_report import generate_tm_report

        print("   - Technical Memo")
        pdf_path = output_dir / "template_technical_memo.pdf"
        generate_tm_report(
            title="WAFT Technical Memo",
            content=f"<div>{content_html}</div>",
            output_path=pdf_path,
            doc_id="TM-001",
        )
        if pdf_path.exists():
            pdfs.append(pdf_path)
    except Exception as e:
        print(f"   ⚠️  Technical Memo error: {e}")

    return pdfs


def generate_foundation_pdf(output_dir: Path) -> list[Path]:
    """Generate PDF from Foundation system."""
    print("📄 Foundation System...")

    try:
        from src.waft.foundation import (
            DocumentConfig,
            DocumentEngine,
            SectionHeaderBlock,
            TextBlock,
        )

        pdfs = []
        pdf_path = output_dir / "foundation_document.pdf"

        engine = DocumentEngine(config=DocumentConfig())

        # Add content blocks
        content = REAL_CONTENT.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            generator_name="Foundation System (FPDF2)",
        )

        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        for para in paragraphs:
            if para.startswith("#"):
                engine.blocks.append(SectionHeaderBlock(para.replace("#", "").strip()))
            else:
                engine.blocks.append(TextBlock(para))

        engine.render(pdf_path)

        if pdf_path.exists():
            pdfs.append(pdf_path)

        return pdfs
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
        return []


def combine_pdfs(pdf_files: list[Path], output_path: Path) -> Path:
    """Combine all PDFs into a single binder PDF."""
    print(f"\n📚 Combining {len(pdf_files)} PDFs into binder...")

    # Try PyPDF2 first
    try:
        from PyPDF2 import PdfMerger

        merger = PdfMerger()

        for pdf_file in sorted(pdf_files):
            if pdf_file.exists():
                print(f"   - Adding: {pdf_file.name}")
                try:
                    merger.append(str(pdf_file))
                except Exception as e:
                    print(f"      ⚠️  Error: {e}")

        merger.write(str(output_path))
        merger.close()

        # Count pages
        try:
            from PyPDF2 import PdfReader

            reader = PdfReader(str(output_path))
            page_count = len(reader.pages)
        except:
            page_count = "unknown"

        print(f"\n✅ Binder created: {output_path}")
        print(f"   - Pages: {page_count}")
        print(f"   - PDFs: {len([p for p in pdf_files if p.exists()])}")

        return output_path
    except ImportError:
        # Fallback: Use pdf_image_converter
        print("   ⚠️  PyPDF2 not available, using image conversion...")

        try:
            from src.waft.evolution.pdf_image_converter import convert_images_to_pdf, pdf_to_pngs

            all_pngs = []
            temp_dir = output_path.parent / "temp_pngs"
            temp_dir.mkdir(exist_ok=True)

            for pdf_file in sorted(pdf_files):
                if pdf_file.exists():
                    print(f"   - Converting: {pdf_file.name}")
                    try:
                        pngs = pdf_to_pngs(pdf_file, temp_dir, dpi=300)
                        all_pngs.extend(pngs)
                    except Exception as e:
                        print(f"      ⚠️  Error: {e}")

            # Combine PNGs into PDF
            convert_images_to_pdf(all_pngs, output_path, page_size=(8.5, 11.0), dpi=300, crop=True)

            # Cleanup
            import shutil

            shutil.rmtree(temp_dir, ignore_errors=True)

            print(f"\n✅ Binder created: {output_path}")
            print(f"   - Pages: {len(all_pngs)}")
            return output_path
        except Exception as e:
            print(f"\n❌ Error creating binder: {e}")
            raise


def open_pdf(pdf_path: Path):
    """Open PDF in default viewer."""
    system = platform.system()
    if system == "Darwin":  # macOS
        subprocess.run(["open", "-a", "Preview", str(pdf_path)])
    elif system == "Linux":
        subprocess.run(["xdg-open", str(pdf_path)])
    elif system == "Windows":
        subprocess.run(["start", str(pdf_path)], shell=True)


def main():
    """Generate supercut binder PDF."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate comprehensive PDF binder from all WAFT generators"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("pdf_supercut_binder.pdf"),
        help="Output binder PDF path (default: pdf_supercut_binder.pdf)",
    )
    parser.add_argument(
        "--pdfs-dir",
        type=Path,
        default=Path("_generated_pdfs"),
        help="Directory to save individual PDFs (default: _generated_pdfs)",
    )
    parser.add_argument(
        "--keep-pdfs", action="store_true", help="Keep individual PDFs after creating binder"
    )

    args = parser.parse_args()

    # Create PDFs directory
    pdfs_dir = args.pdfs_dir
    pdfs_dir.mkdir(exist_ok=True)

    print("🎬 WAFT PDF Supercut Binder Generator")
    print("=" * 60)
    print(f"PDFs directory: {pdfs_dir}")
    print(f"Output binder: {args.output}")
    print()

    all_pdfs = []

    # Generate PDFs from all generators
    try:
        all_pdfs.extend(generate_pdfgenerator_pdfs(pdfs_dir))
    except Exception as e:
        print(f"   ❌ PDFGenerator error: {e}")

    try:
        all_pdfs.extend(generate_scientific_pdf(pdfs_dir))
    except Exception as e:
        print(f"   ❌ ScientificPDFGenerator error: {e}")

    try:
        all_pdfs.extend(generate_component_pdf(pdfs_dir))
    except Exception as e:
        print(f"   ❌ ComponentPDFGenerator error: {e}")

    try:
        all_pdfs.extend(generate_template_pdfs(pdfs_dir))
    except Exception as e:
        print(f"   ❌ Template system error: {e}")

    try:
        all_pdfs.extend(generate_foundation_pdf(pdfs_dir))
    except Exception as e:
        print(f"   ❌ Foundation system error: {e}")

    # Filter to existing PDFs
    existing_pdfs = []
    for p in all_pdfs:
        if isinstance(p, str):
            p = Path(p)
        if isinstance(p, Path) and p.exists():
            existing_pdfs.append(p)

    if not existing_pdfs:
        print("\n❌ No PDFs were generated!")
        sys.exit(1)

    print(f"\n✅ Generated {len(existing_pdfs)} PDFs in {pdfs_dir}")

    # Combine into binder
    binder_path = combine_pdfs(existing_pdfs, args.output)

    # Cleanup
    if not args.keep_pdfs:
        print(f"\n🧹 Cleaning up PDFs directory: {pdfs_dir}")
        import shutil

        shutil.rmtree(pdfs_dir, ignore_errors=True)
    else:
        print(f"\n📁 Individual PDFs kept in: {pdfs_dir}")

    # Open binder
    print("\n📖 Opening binder PDF...")
    open_pdf(binder_path)

    print(f"\n✅ Complete! Binder PDF: {binder_path}")


if __name__ == "__main__":
    main()
