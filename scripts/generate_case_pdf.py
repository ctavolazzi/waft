#!/usr/bin/env python3
"""
Generate PDF Binder from Case File
"""

import re
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

import markdown

from src.waft.brief import BriefDocument
from src.waft.utils import (
    add_code_examples_to_case_file,
    escape_title_for_filename,
    generate_headline_title,
)


def generate_case_pdf(case_file_path: Path, output_path: Path | None = None) -> Path:
    """Generate PDF binder from case file."""

    # Add code examples section if not present
    project_root = Path(__file__).parent.parent
    add_code_examples_to_case_file(case_file_path, project_root)

    # Read case file (may have been updated with code examples)
    case_content = case_file_path.read_text(encoding="utf-8")

    # Extract case ID, claim, and verdict from content
    case_id = None
    claim = None
    verdict = None

    for line in case_content.split("\n"):
        if line.startswith("**Case ID**:"):
            case_id = line.split("**Case ID**:")[1].strip()
        elif line.startswith("**Claim**:"):
            claim = line.split("**Claim**:")[1].strip()
        elif line.startswith("**Verdict**:"):
            verdict = line.split("**Verdict**:")[1].strip()
            # Clean up verdict (remove emoji, extra formatting)
            verdict = re.sub(r"✅|❌|⚠️|\*\*", "", verdict).strip()

    # Generate headline-style title
    title = (
        generate_headline_title(claim, verdict)
        if claim
        else f"Proof Case {case_id}"
        if case_id
        else "Proof Case"
    )

    # Determine cover classification based on verdict
    if verdict and "PROVEN" in verdict.upper():
        classification = "VERIFIED"
        cover_warning = {
            "message": "CLAIM VERIFIED - Evidence supports the claim beyond reasonable doubt",
            "severity": "INFO",
        }
    elif verdict and "DISPROVEN" in verdict.upper():
        classification = "REFUTED"
        cover_warning = {
            "message": "CLAIM DISPROVEN - Evidence contradicts the claim",
            "severity": "CRITICAL",
        }
    else:
        classification = "INCONCLUSIVE"
        cover_warning = {
            "message": "INSUFFICIENT EVIDENCE - Cannot definitively prove or disprove",
            "severity": "WARNING",
        }

    # Convert markdown to HTML with proper code highlighting
    try:
        html_content = markdown.markdown(
            case_content,
            extensions=[
                "fenced_code",  # Code blocks
                "tables",  # Tables
                "nl2br",  # Line breaks
                "extra",  # Extra features
                "codehilite",  # Syntax highlighting
                "pymdownx.superfences",  # Better code fences
                "pymdownx.highlight",  # Better highlighting
            ],
            extension_configs={
                "codehilite": {
                    "css_class": "highlight",
                    "use_pygments": True,
                    "linenums": True,
                    "noclasses": False,
                }
            },
        )
    except ImportError:
        # Fallback: basic conversion
        html_content = case_content
        # Code blocks
        html_content = re.sub(
            r"```(\w+)?\n(.*?)```",
            r'<pre><code class="language-\1">\2</code></pre>',
            html_content,
            flags=re.DOTALL,
        )
        # Inline code
        html_content = re.sub(r"`([^`]+)`", r"<code>\1</code>", html_content)
        # Headers
        html_content = re.sub(r"^#\s+(.+)$", r"<h1>\1</h1>", html_content, flags=re.MULTILINE)
        html_content = re.sub(r"^##\s+(.+)$", r"<h2>\1</h2>", html_content, flags=re.MULTILINE)
        html_content = re.sub(r"^###\s+(.+)$", r"<h3>\1</h3>", html_content, flags=re.MULTILINE)
        # Bold
        html_content = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", html_content)
        # Paragraphs
        html_content = re.sub(r"^(.+)$", r"<p>\1</p>", html_content, flags=re.MULTILINE)

    # Generate PDF using BriefDocument (proper escaping built-in)
    print("📄 Generating PDF binder from case file...")
    print(f"   Case file: {case_file_path}")
    print(f"   Title: {title}")

    verdict_short = verdict.split()[0] if verdict else "PROVEN"
    doc = BriefDocument(
        title=title,  # Will be escaped automatically in generate()
        doc_id=f"PROOF-{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        subtitle=f"Verdict: {verdict_short} | Confidence: 100%",
        classification=classification,
        cover_header="PROOF CASE BRIEF",
        cover_metadata={
            "CLAIM": claim[:100] if claim and len(claim) > 100 else (claim or "Proof Case"),
            "VERDICT": verdict_short,
            "CONFIDENCE": "100%",
            "DATE": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
        cover_warning=cover_warning,
        cover_footer="EVIDENCE-BASED VERIFICATION",
        include_system_status=False,
    )

    # Add content
    doc.content_blocks.append(html_content)

    # Generate PDF
    if output_path is None:
        safe_title = escape_title_for_filename(title)[:50]
        output_path = (
            case_file_path.parent
            / f"PROOF_CASE_{safe_title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )

    pdf_path = doc.generate(output_path=output_path)

    print(f"✅ PDF generated: {pdf_path}")
    return Path(pdf_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate PDF binder from case file")
    parser.add_argument("case_file", type=str, help="Path to case file")
    parser.add_argument("--output", type=str, help="Output PDF path")

    args = parser.parse_args()

    case_file = Path(args.case_file)
    if not case_file.exists():
        print(f"❌ Case file not found: {case_file}")
        sys.exit(1)

    output = Path(args.output) if args.output else None
    pdf_path = generate_case_pdf(case_file, output)

    print(f"\n✅ PDF binder generated: {pdf_path}")
