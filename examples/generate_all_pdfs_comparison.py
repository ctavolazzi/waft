"""
Generate ArXiv-Ready Academic Paper PDF from Markdown

Transforms a markdown file into a publication-ready ArXiv academic paper PDF
using the academic paper template with two-column layout, proper typography,
and academic formatting standards.
"""

import re
import sys
from datetime import datetime
from pathlib import Path

import markdown

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.templates.academic_paper import generate_academic_paper


def extract_arxiv_metadata(md_content: str) -> dict:
    """
    Extract ArXiv metadata from markdown content.

    Supports:
    - YAML frontmatter (between --- markers)
    - Structured markdown sections (## Abstract, **Authors**:, etc.)
    - First H1 as title

    Args:
        md_content: Full markdown content

    Returns:
        Dictionary with title, abstract, authors, affiliations, email, year, references
    """
    metadata = {
        "title": "",
        "abstract": "",
        "authors": [],
        "affiliations": [],
        "email": None,
        "year": str(datetime.now().year),
        "references": [],
    }

    lines = md_content.split("\n")

    # Try to extract YAML frontmatter first
    frontmatter = {}
    if lines and lines[0].strip() == "---":
        i = 1
        current_key = None
        current_value = []
        while i < len(lines) and lines[i].strip() != "---":
            line = lines[i]
            line_stripped = line.strip()

            # Check if this is a new key-value pair
            if (
                ":" in line_stripped
                and not line_stripped.startswith("-")
                and not line_stripped.startswith(" ")
            ):
                # Save previous key-value if exists
                if current_key and current_value:
                    frontmatter[current_key] = (
                        "\n".join(current_value).strip().strip('"').strip("'")
                    )

                # Start new key-value
                key, value = line_stripped.split(":", 1)
                current_key = key.strip().lower()
                value_stripped = value.strip().strip('"').strip("'")
                if value_stripped:
                    current_value = [value_stripped]
                else:
                    current_value = []
            elif current_key:
                # Continuation of current value (indented or list item)
                if line_stripped.startswith("-") or line_stripped.startswith(" "):
                    current_value.append(line_stripped.lstrip("- ").strip().strip('"').strip("'"))
                elif line_stripped:
                    current_value.append(line_stripped.strip().strip('"').strip("'"))

            i += 1

        # Save last key-value
        if current_key and current_value:
            frontmatter[current_key] = "\n".join(current_value).strip().strip('"').strip("'")

        # Skip the closing ---
        if i < len(lines):
            i += 1

    # Extract from frontmatter if available
    if frontmatter:
        metadata["title"] = frontmatter.get("title", "").strip()
        metadata["abstract"] = frontmatter.get("abstract", "").strip()

        # Handle authors (can be string or list in YAML)
        if "authors" in frontmatter:
            authors_value = frontmatter["authors"]
            if isinstance(authors_value, str):
                # Split by comma or newline
                authors_list = [a.strip() for a in re.split(r"[,\n]", authors_value) if a.strip()]
                metadata["authors"] = [{"name": author} for author in authors_list]
            elif isinstance(authors_value, list):
                metadata["authors"] = [
                    {"name": str(a).strip()} for a in authors_value if str(a).strip()
                ]

        # Handle affiliations
        if "affiliations" in frontmatter:
            affil_value = frontmatter["affiliations"]
            if isinstance(affil_value, str):
                metadata["affiliations"] = [
                    a.strip() for a in re.split(r"[,\n]", affil_value) if a.strip()
                ]
            elif isinstance(affil_value, list):
                metadata["affiliations"] = [str(a).strip() for a in affil_value if str(a).strip()]

        metadata["email"] = frontmatter.get("email", "").strip() or None
        year_value = frontmatter.get("year", "")
        if year_value:
            metadata["year"] = str(year_value).strip()

    # Extract from markdown structure if not in frontmatter
    # Title: First H1
    if not metadata["title"]:
        for line in lines:
            if line.startswith("# ") and not line.startswith("##"):
                metadata["title"] = line[2:].strip()
                break

    # Abstract: Look for ## Abstract section
    if not metadata["abstract"]:
        in_abstract = False
        abstract_lines = []
        for line in lines:
            line_stripped = line.strip()
            if line_stripped.lower().startswith("## abstract"):
                in_abstract = True
                continue
            elif in_abstract:
                # Stop at next major section (##) or horizontal rule
                if line_stripped.startswith("##") or line_stripped.startswith("---"):
                    break
                # Collect all non-empty lines in abstract
                if line_stripped:
                    abstract_lines.append(line_stripped)
        if abstract_lines:
            # Join with spaces, clean up multiple spaces
            abstract_text = " ".join(abstract_lines)
            # Remove markdown formatting from abstract
            abstract_text = re.sub(r"\*\*([^*]+)\*\*", r"\1", abstract_text)  # Remove bold
            abstract_text = re.sub(r"\*([^*]+)\*", r"\1", abstract_text)  # Remove italic
            metadata["abstract"] = abstract_text

    # Authors: Look for **Authors**: pattern or **Author**: pattern
    if not metadata["authors"]:
        for line in lines:
            line_lower = line.lower()
            if "**authors**" in line_lower or "**author**" in line_lower:
                # Extract after colon
                if ":" in line:
                    authors_str = line.split(":", 1)[1].strip()
                    # Remove markdown formatting
                    authors_str = re.sub(r"\*\*([^*]+)\*\*", r"\1", authors_str)
                    authors_str = re.sub(r"\*([^*]+)\*", r"\1", authors_str)
                    # Handle single author or comma-separated
                    if authors_str:
                        # Split by comma, but be smart about it
                        authors_list = [a.strip() for a in authors_str.split(",")]
                        metadata["authors"] = [
                            {"name": author} for author in authors_list if author
                        ]
                break

    # Affiliations: Look for **Affiliation**: pattern
    if not metadata["affiliations"]:
        for line in lines:
            if "**affiliation" in line.lower():
                if ":" in line:
                    affil_str = line.split(":", 1)[1].strip()
                    metadata["affiliations"] = [a.strip() for a in affil_str.split(",")]
                break

    # Email: Look for **Email**: pattern
    if not metadata["email"]:
        for line in lines:
            if "**email**" in line.lower():
                if ":" in line:
                    metadata["email"] = line.split(":", 1)[1].strip()
                break

    # References: Look for ## References section
    if not metadata["references"]:
        in_references = False
        for line in lines:
            line_stripped = line.strip()
            line_lower = line_stripped.lower()

            if line_lower.startswith("## references") or line_lower.startswith("# references"):
                in_references = True
                continue
            elif in_references:
                # Stop at next major section
                if line_stripped.startswith("##") and not line_lower.startswith("## references"):
                    break
                if line_stripped.startswith("# ") and not line_lower.startswith("# references"):
                    break

                # Skip empty lines and section markers
                if not line_stripped or line_stripped.startswith("---"):
                    continue

                # Handle [1] format (most common in academic papers)
                if line_stripped.startswith("[") and "]" in line_stripped:
                    # Extract everything after the closing bracket
                    parts = line_stripped.split("]", 1)
                    if len(parts) == 2:
                        ref = parts[1].strip()
                        if ref and len(ref) > 10:  # Reasonable reference length
                            metadata["references"].append(ref)

                # Handle numbered format (1. or 1) or bulleted (-)
                elif line_stripped and (
                    line_stripped[0].isdigit() or line_stripped.startswith("-")
                ):
                    # Remove numbering/bullets and parentheses
                    ref = re.sub(r"^[\d\.\-\s\)]+", "", line_stripped)
                    if ref and len(ref) > 10:
                        metadata["references"].append(ref)

                # Handle plain text references (if they look substantial)
                elif len(line_stripped) > 20 and not line_stripped.startswith("#"):
                    # Check if it looks like a citation (has author names, year, etc.)
                    if any(
                        indicator in line_stripped
                        for indicator in [",", ".", "(", ")", "et al", "Journal", "Proceedings"]
                    ):
                        metadata["references"].append(line_stripped)

    # Fallback: If no abstract found, use first substantial paragraph(s)
    if not metadata["abstract"]:
        paragraph_lines = []
        collecting = False
        in_code_block = False
        skipped_sections = [
            "date",
            "time",
            "session",
            "what we",
            "key insights",
            "next steps",
            "created",
            "modified",
        ]
        code_indicators = [
            "=",
            "(",
            ")",
            "[",
            "]",
            "{",
            "}",
            "def ",
            "class ",
            "import ",
            "from ",
            "return ",
            "print(",
        ]

        for line in lines:
            line_stripped = line.strip()
            line_lower = line_stripped.lower()

            # Track code blocks
            if line_stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            # Skip headers, empty lines, metadata lines, horizontal rules, list items, code
            if (
                line_stripped
                and not line_stripped.startswith("#")
                and not line_stripped.startswith("**")
                and not line_stripped.startswith("---")
                and not line_stripped.startswith("- ")  # Skip list items
                and not line_stripped.startswith("* ")  # Skip list items
                and not line_stripped.startswith("`")  # Skip inline code markers
                and not any(section in line_lower for section in skipped_sections)
                and ":" not in line_stripped  # Skip metadata-like lines
                and not any(
                    indicator in line_stripped for indicator in code_indicators
                )  # Skip code-like lines
                and not line_stripped.startswith("```")
            ):  # Skip code block markers
                # Start collecting if we find a substantial paragraph (prose, not code)
                # Look for natural language indicators (common words, sentence structure)
                # But be more lenient - just avoid obvious code patterns
                is_likely_code = any(
                    indicator in line_stripped
                    for indicator in [
                        "=",
                        "(",
                        ")",
                        "[",
                        "]",
                        "{",
                        "}",
                        "def ",
                        "class ",
                        "import ",
                        "from ",
                        "return ",
                        "print(",
                        "->",
                        "::",
                    ]
                )

                has_natural_language = any(
                    word in line_lower
                    for word in [
                        "the",
                        "and",
                        "or",
                        "is",
                        "are",
                        "was",
                        "were",
                        "a",
                        "an",
                        "to",
                        "of",
                        "in",
                        "on",
                        "at",
                        "for",
                        "with",
                        "we",
                        "this",
                        "that",
                        "system",
                        "provides",
                        "features",
                    ]
                )

                if (
                    len(line_stripped) > 80
                    and not line_stripped[0].isdigit()  # Skip numbered items
                    and not is_likely_code  # Skip obvious code
                    and (has_natural_language or len(line_stripped) > 120)
                ):  # Either has natural language or is long enough
                    collecting = True

                if collecting:
                    paragraph_lines.append(line_stripped)
                    # Stop after collecting 2-3 sentences or hitting a reasonable length
                    if len(paragraph_lines) >= 2 or len(" ".join(paragraph_lines)) > 300:
                        break

        if paragraph_lines:
            abstract_text = " ".join(paragraph_lines)
            # Clean up markdown formatting
            abstract_text = re.sub(r"\*\*([^*]+)\*\*", r"\1", abstract_text)
            abstract_text = re.sub(r"\*([^*]+)\*", r"\1", abstract_text)
            abstract_text = re.sub(r"`([^`]+)`", r"\1", abstract_text)  # Remove inline code
            # Limit to reasonable abstract length (typically 150-250 words)
            words = abstract_text.split()
            if len(words) > 250:
                abstract_text = " ".join(words[:250]) + "..."
            elif len(abstract_text) < 50:
                # Too short, try to get more
                abstract_text = None
            if abstract_text:
                metadata["abstract"] = abstract_text

        # Final fallback: Just get first substantial non-code line
        if not metadata["abstract"]:
            for line in lines:
                line_stripped = line.strip()
                if (
                    line_stripped
                    and len(line_stripped) > 100
                    and not line_stripped.startswith("#")
                    and not line_stripped.startswith("```")
                    and not line_stripped.startswith("- ")
                    and not line_stripped.startswith("* ")
                    and "=" not in line_stripped  # Skip code-like
                    and not line_stripped.startswith("`")
                    and " " in line_stripped
                ):  # Has spaces (not all one word)
                    # Clean and use as abstract
                    abstract_text = line_stripped
                    abstract_text = re.sub(r"\*\*([^*]+)\*\*", r"\1", abstract_text)
                    abstract_text = re.sub(r"\*([^*]+)\*", r"\1", abstract_text)
                    abstract_text = re.sub(r"`([^`]+)`", r"\1", abstract_text)
                    if len(abstract_text) > 50:
                        metadata["abstract"] = abstract_text[:500]
                        break

    # Fallback: If no title, use filename or default
    if not metadata["title"]:
        metadata["title"] = "Research Paper"

    # Fallback: If no authors, use default
    if not metadata["authors"]:
        metadata["authors"] = [{"name": "Author"}]

    return metadata


def process_markdown_content(md_content: str, metadata: dict) -> str:
    """
    Process markdown content for academic paper.

    - Removes frontmatter/metadata sections
    - Removes Abstract section (handled by template)
    - Removes References section (handled by template)
    - Converts markdown to HTML
    - Preserves code blocks, tables, lists, formatting

    Args:
        md_content: Full markdown content
        metadata: Extracted metadata dictionary

    Returns:
        HTML content string
    """
    lines = md_content.split("\n")
    processed_lines = []

    # Skip YAML frontmatter
    skip_frontmatter = False
    if lines and lines[0].strip() == "---":
        skip_frontmatter = True
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        if i < len(lines):
            i += 1  # Skip closing ---
            lines = lines[i:]

    # Process lines, removing metadata sections
    skip_abstract = False
    skip_references = False
    skip_metadata_lines = False
    skip_frontmatter_done = False

    for i, line in enumerate(lines):
        line_stripped = line.strip()
        line_lower = line_stripped.lower()

        # Skip Abstract section (## Abstract or # Abstract)
        if line_lower.startswith("## abstract") or line_lower.startswith("# abstract"):
            skip_abstract = True
            continue
        elif skip_abstract:
            # Stop skipping when we hit next major section or horizontal rule
            if (
                line_stripped.startswith("##")
                or line_stripped.startswith("# ")
                or line_stripped.startswith("---")
            ):
                skip_abstract = False
                # Don't skip the section header itself
                if not line_lower.startswith("## abstract") and not line_lower.startswith(
                    "# abstract"
                ):
                    continue
            else:
                continue

        # Skip References section
        if line_lower.startswith("## references") or line_lower.startswith("# references"):
            skip_references = True
            continue
        elif skip_references:
            # References section continues until next major section
            if line_stripped.startswith("##") and not line_lower.startswith("## references"):
                skip_references = False
                # Don't skip the section header itself
                continue
            elif line_stripped.startswith("# ") and not line_lower.startswith("# references"):
                skip_references = False
                continue
            else:
                continue

        # Skip metadata lines (Authors, Email, etc. in markdown format)
        # Only skip if it's a standalone metadata line (not in code blocks or lists)
        if (
            not skip_metadata_lines
            and any(
                keyword in line_lower
                for keyword in [
                    "**authors**",
                    "**author**",
                    "**email**",
                    "**affiliation**",
                    "**date**",
                    "**version**",
                    "**category**",
                    "**keywords**",
                ]
            )
            and ":" in line
        ):
            # Check if this is a metadata line (has colon and keyword)
            skip_metadata_lines = True
            continue
        elif skip_metadata_lines:
            # Stop skipping metadata when we hit a blank line, section, or horizontal rule
            if (
                line_stripped == ""
                or line_stripped.startswith("##")
                or line_stripped.startswith("# ")
                or line_stripped.startswith("---")
            ):
                skip_metadata_lines = False
            else:
                # Continue skipping if it looks like continuation of metadata
                if ":" in line and any(
                    keyword in line_lower for keyword in ["**", "date", "time", "session"]
                ):
                    continue

        if skip_abstract or skip_references or skip_metadata_lines:
            continue

        processed_lines.append(line)

    # Join and convert to HTML
    processed_md = "\n".join(processed_lines)

    # Convert markdown to HTML with extensions
    html_content = markdown.markdown(
        processed_md,
        extensions=[
            "fenced_code",
            "tables",
            "nl2br",
            "extra",
            "codehilite",
            "md_in_html",  # Preserve HTML in markdown
        ],
    )

    return html_content


def generate_arxiv_pdf(md_file: Path, output_path: Path) -> Path:
    """
    Generate ArXiv-ready PDF from markdown file.

    Args:
        md_file: Path to input markdown file
        output_path: Path to output PDF file

    Returns:
        Path to generated PDF
    """
    # Read markdown file
    md_content = md_file.read_text(encoding="utf-8")

    # Extract metadata
    print("📋 Extracting metadata...")
    metadata = extract_arxiv_metadata(md_content)

    print(f"   Title: {metadata['title']}")
    print(f"   Authors: {len(metadata['authors'])} author(s)")
    print(f"   Abstract: {len(metadata['abstract'])} characters")
    print(f"   References: {len(metadata['references'])} reference(s)")

    # Process content
    print("🔄 Processing markdown content...")
    html_content = process_markdown_content(md_content, metadata)

    # Generate PDF using academic paper template
    print("📄 Generating ArXiv PDF...")
    pdf_path = generate_academic_paper(
        title=metadata["title"],
        content=html_content,
        output_path=output_path,
        abstract=metadata["abstract"],
        authors=metadata["authors"],
        affiliations=metadata["affiliations"] if metadata["affiliations"] else None,
        email=metadata["email"],
        conference="arXiv",
        year=metadata["year"],
        references=metadata["references"] if metadata["references"] else None,
    )

    return pdf_path


def main():
    """Generate ArXiv-ready PDF from markdown."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate ArXiv-ready academic paper PDF from markdown"
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="_temp_pdf_samples/session_recap_2026-01-12.md",
        help="Input markdown file path (default: _temp_pdf_samples/session_recap_2026-01-12.md)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output PDF path (default: input filename + _arxiv.pdf in same directory as input)",
    )
    parser.add_argument("--open", action="store_true", help="Open PDF after generation")

    args = parser.parse_args()

    # Input file
    md_file = Path(args.input)
    if not md_file.exists():
        print(f"❌ Error: Markdown file not found: {md_file}")
        return

    print(f"📄 Source markdown: {md_file}")
    print()

    # Output path
    if args.output:
        output_path = Path(args.output)
    else:
        # Default: input filename + _arxiv.pdf in same directory as input
        output_path = md_file.parent / f"{md_file.stem}_arxiv.pdf"

    print(f"📤 Output PDF: {output_path}")
    print()

    # Generate PDF
    try:
        pdf_path = generate_arxiv_pdf(md_file, output_path)

        print()
        print("=" * 60)
        print("✅ ArXiv PDF Generation Complete!")
        print("=" * 60)
        print()

        if pdf_path.exists():
            size = pdf_path.stat().st_size / 1024  # KB
            print(f"📄 Generated: {pdf_path}")
            print(f"📊 Size: {size:.1f} KB")
            print()

            # Open PDF if requested
            if args.open:
                print("📂 Opening PDF...")
                import platform
                import subprocess

                try:
                    if platform.system() == "Darwin":  # macOS
                        subprocess.run(["open", str(pdf_path)], check=False)
                    elif platform.system() == "Windows":
                        subprocess.run(["start", str(pdf_path)], shell=True, check=False)
                    else:  # Linux
                        subprocess.run(["xdg-open", str(pdf_path)], check=False)
                    print(f"  ✅ Opened: {pdf_path}")
                except Exception as e:
                    print(f"  ⚠️  Could not open PDF: {e}")
        else:
            print("❌ PDF generation failed - file not found")

    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        import traceback

        traceback.print_exc()
        return


if __name__ == "__main__":
    main()
