#!/usr/bin/env python3
"""
PDF-me Command - Generate PDF from Markdown

Generates professional PDFs from markdown files and opens them (not prints).
"""

import subprocess
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from waft.evolution.pdf_generator import PDFGenerator
from waft.utils import escape_title_for_pdf


def extract_title(file_path: Path) -> str:
    """Extract title from filename."""
    return file_path.stem.replace("_", " ").replace("-", " ").title()


def parse_args(args: list) -> dict:
    """Parse command line arguments."""
    parsed = {
        "file_path": None,
        "title": None,
        "output": None,
        "style": "clinical_standard",
        "no_open": False,
    }

    i = 0
    while i < len(args):
        arg = args[i]

        if arg.startswith("title:"):
            parsed["title"] = arg.split(":", 1)[1].strip("\"'")
        elif arg == "--title" and i + 1 < len(args):
            i += 1
            parsed["title"] = args[i].strip("\"'")
        elif arg == "--output" and i + 1 < len(args):
            i += 1
            parsed["output"] = args[i]
        elif arg == "--style" and i + 1 < len(args):
            i += 1
            parsed["style"] = args[i]
        elif arg == "--no-open":
            parsed["no_open"] = True
        elif not arg.startswith("--") and not parsed["file_path"]:
            parsed["file_path"] = arg

        i += 1

    return parsed


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: pdf-me <file_path> [options]")
        print("\nOptions:")
        print('  --title "Title" or title:"Title"  Custom PDF title')
        print("  --output <path>                    Custom output path")
        print(
            "  --style <style>                    PDF style (clinical_standard/premium/professional)"
        )
        print("  --no-open                          Don't open PDF automatically")
        sys.exit(1)

    # Parse arguments
    parsed = parse_args(sys.argv[1:])

    if not parsed["file_path"]:
        print("❌ Error: File path required")
        sys.exit(1)

    file_path = Path(parsed["file_path"])
    if not file_path.is_absolute():
        file_path = Path.cwd() / file_path

    if not file_path.exists():
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)

    # Read markdown content
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

    # Determine title
    title_raw = parsed["title"] or extract_title(file_path)

    # Escape title for PDF rendering (preserves special chars like /, -, etc.)
    title_escaped = escape_title_for_pdf(title_raw)

    # Determine output path
    if parsed["output"]:
        output_path = Path(parsed["output"])
        if not output_path.is_absolute():
            output_path = Path.cwd() / output_path
    else:
        output_path = file_path.with_suffix(".pdf")

    # Generate PDF
    print(f"📄 Generating PDF from: {file_path}")
    print(f"📝 Title: {title_raw}")
    print(f"🎨 Style: {parsed['style']}")

    try:
        generator = PDFGenerator.from_content(
            content=content, title=title_escaped, style=parsed["style"]
        )

        generator.save(output_path)
        print(f"✅ PDF generated: {output_path}")

        # Open PDF (not print)
        if not parsed["no_open"]:
            print("🔍 Opening PDF...")
            try:
                # macOS
                subprocess.run(["open", str(output_path)], check=True)
                print("✅ PDF opened in Preview")
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    # Linux
                    subprocess.run(["xdg-open", str(output_path)], check=True)
                    print("✅ PDF opened")
                except (subprocess.CalledProcessError, FileNotFoundError):
                    try:
                        # Windows
                        subprocess.run(["start", str(output_path)], shell=True, check=True)
                        print("✅ PDF opened")
                    except:
                        print("⚠️  Could not open PDF automatically")
                        print(f"   PDF saved at: {output_path}")

    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
