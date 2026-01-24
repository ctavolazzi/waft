"""
Case File Renderer CLI - Easy PDF generation from case files.

Converts markdown case files to Typst using the case_brief.typ template structure.
"""
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from ..templates.typst.compiler import TypstCompiler
from ..utils import resolve_project_path

console = Console()


def parse_markdown_case_file(markdown_content: str) -> dict:
    # Store raw markdown for later use
    data = {
        "metadata": {},
        "sections": {},
        "evidence_items": [],
        "key_findings": [],
        "_raw_markdown": markdown_content,  # Store for Files section parsing
    }

    lines = markdown_content.split("\n")
    i = 0
    current_section = None
    current_evidence = None
    in_code_block = False
    code_block_content = []
    code_block_lang = ""

    while i < len(lines):
        line = lines[i]

        # Extract metadata
        if "**Case ID**:" in line:
            data["metadata"]["case_id"] = line.split("**Case ID**:")[1].strip()
        elif "**Generated**:" in line or "**Investigation Date**:" in line:
            date_str = line.split(":")[1].strip() if ":" in line else ""
            data["metadata"]["case_date"] = date_str
        elif "**Claim**:" in line:
            data["metadata"]["claim"] = line.split("**Claim**:")[1].strip()
        elif "**Verdict**:" in line:
            verdict = line.split("**Verdict**:")[1].strip()
            data["metadata"]["verdict"] = re.sub(r"✅|❌|⚠️|\*\*", "", verdict).strip()
        elif "**Confidence**:" in line:
            data["metadata"]["confidence"] = line.split("**Confidence**:")[1].strip()
        elif "**Evidence Quality**:" in line:
            data["metadata"]["evidence_quality"] = line.split("**Evidence Quality**:")[1].strip()

        # Extract title from first H1
        if line.startswith("# ") and "title" not in data["metadata"]:
            title = line[2:].strip()
            title = re.sub(r"^Proof Case File:\s*", "", title, flags=re.IGNORECASE)
            data["metadata"]["title"] = title

        # Skip "---" separator lines early (before other processing)
        if line.strip() == "---":
            i += 1
            continue
        
        # Handle code blocks
        if line.startswith("```"):
            if in_code_block:
                # End code block
                if current_evidence:
                    current_evidence["code"] = {
                        "language": code_block_lang,
                        "content": "\n".join(code_block_content),
                    }
                in_code_block = False
                code_block_content = []
                code_block_lang = ""
            else:
                in_code_block = True
                code_block_lang = line[3:].strip() if len(line) > 3 else ""
            i += 1
            continue

        if in_code_block:
            code_block_content.append(line)
            i += 1
            continue

        # Handle sections
        if line.startswith("## "):
            section_title = line[3:].strip()
            # Normalize section title for key (handle "Files Created/Modified")
            current_section = section_title.lower().replace(" ", "_").replace("/", "_")
            data["sections"][current_section] = {"title": section_title, "content": []}
            current_evidence = None
            current_subsection = None
        elif line.startswith("### "):
            subsection_title = line[4:].strip()
            # Check if it's an evidence item (numbered)
            if re.match(r"^\d+\.\s+", subsection_title):
                # New evidence item
                match = re.match(r"^(\d+)\.\s+(.+)$", subsection_title)
                if match:
                    evidence_num = match.group(1)
                    evidence_title = match.group(2)
                    current_evidence = {
                        "number": evidence_num,
                        "title": evidence_title,
                        "file": None,
                        "lines": None,
                        "code": None,
                        "finding": None,
                    }
                    data["evidence_items"].append(current_evidence)
                    current_subsection = None  # Evidence items aren't subsections
            else:
                # Regular subsection - create subsection object and track it
                if current_section:
                    subsection_obj = {"type": "subsection", "title": subsection_title, "content": []}
                    data["sections"][current_section]["content"].append(subsection_obj)
                    # Track current subsection so we can add content to it
                    current_subsection = subsection_obj
                else:
                    current_subsection = None
        elif line.startswith("#### "):
            subsubsection_title = line[5:].strip()
            if current_section:
                data["sections"][current_section]["content"].append(
                    {"type": "subsubsection", "title": subsubsection_title, "content": []}
                )
        elif line.strip().startswith("**File**:") or line.strip().startswith("*File*:"):
            file_ref = line.strip().split(":")[1].strip() if ":" in line else ""
            # Remove backticks from file reference
            file_ref = file_ref.replace("`", "").strip()
            if current_evidence:
                current_evidence["file"] = file_ref
        elif line.strip().startswith("**Lines**:") or line.strip().startswith("*Lines*:"):
            lines_ref = line.strip().split(":")[1].strip() if ":" in line else ""
            if current_evidence:
                current_evidence["lines"] = lines_ref
        elif line.strip().startswith("**Finding**:") or line.strip().startswith("*Finding*:"):
            finding = line.strip().split(":")[1].strip() if ":" in line else ""
            if current_evidence:
                current_evidence["finding"] = finding
        elif line.strip().startswith("- ") and "Key Achievements" in str(data["sections"].get("verdict", {}).get("content", [])):
            # Key findings/achievements
            finding = line.strip()[2:].strip()
            data["key_findings"].append(finding)
        elif line.strip() and current_section and not line.strip().startswith(("#", "**File", "**Lines", "**Finding", "**Code")):
            # Regular content - add to current subsection if exists, otherwise to section
            if current_section not in data["sections"]:
                data["sections"][current_section] = {"title": current_section, "content": []}
            
            # Add to subsection content if we have a current subsection
            # Also check if last item in section is a subsection
            section_content = data["sections"][current_section]["content"]
            if current_subsection and isinstance(current_subsection, dict):
                # Use the tracked subsection
                if "content" not in current_subsection:
                    current_subsection["content"] = []
                current_subsection["content"].append(line.strip())
            elif section_content and isinstance(section_content[-1], dict) and section_content[-1].get("type") == "subsection":
                # Last item is a subsection, add to it
                section_content[-1].setdefault("content", []).append(line.strip())
            else:
                # Add to section content directly
                if not isinstance(section_content, list):
                    data["sections"][current_section]["content"] = []
                data["sections"][current_section]["content"].append(line.strip())

        i += 1

    return data


def convert_backticks_to_monospace(text: str) -> str:
    """Convert markdown backticks to Typst monospace text."""
    # Replace `file_path` with #text(font: "mono")[file_path]
    def replace_backtick(match):
        content = match.group(1)
        return f'#text(font: "mono")[{content}]'
    
    return re.sub(r"`([^`]+)`", replace_backtick, text)


def generate_typst_from_parsed_data(data: dict) -> str:
    """Generate Typst content from parsed case file data."""
    metadata = data["metadata"]
    evidence_items = data["evidence_items"]
    key_findings = data["key_findings"]
    sections = data["sections"]

    # Set defaults
    case_id = metadata.get("case_id") or "case_unknown"
    case_date = metadata.get("case_date") or "Unknown date"
    claim = metadata.get("claim") or "No claim specified"
    verdict = metadata.get("verdict") or "INCONCLUSIVE"
    confidence = metadata.get("confidence") or "Unknown"
    evidence_quality = metadata.get("evidence_quality") or "Unknown"
    title = metadata.get("title", "Proof Case")

    # Determine verdict color
    if "PROVEN" in verdict.upper():
        verdict_color = "27ae60"
    elif "DISPROVEN" in verdict.upper():
        verdict_color = "e74c3c"
    else:
        verdict_color = "f39c12"

    # Escape special characters in claim
    claim_escaped = claim.replace('"', '\\"').replace("$", "\\$")

    # Build Typst content
    typst = f"""#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering

// Page border for WAFT template identification
#show: s6t5-page-bordering.with(
  margin: (left: 0.75in, right: 0.75in, top: 1in, bottom: 1in),
  expand: 15pt,
  space-top: 15pt,
  space-bottom: 15pt,
  stroke-header: none,
  stroke-footer: none,
  header: "",
  footer: "",
)

#set text(font: "Times New Roman", size: 11pt)
#set par(leading: 0.65em)
#set heading(numbering: "1.")

// Case Brief Metadata
#let case-id = "{case_id}"
#let case-date = "{case_date}"
#let claim = "{claim_escaped}"
#let verdict = "{verdict}"
#let confidence = "{confidence}"
#let evidence-quality = "{evidence_quality}"

= CASE BRIEF: PROOF OF CLAIM

#align(center)[
  #text(size: 18pt, weight: "bold")[{title}]
  
  #v(0.3in)
  
  #text(size: 10pt)[Case ID: #case-id]
  #text(size: 10pt)[Date: #case-date]
]

#v(0.5in)

== Executive Summary

#block(
  fill: rgb("2c3e50"),
  inset: 8pt,
  radius: 4pt,
  text(fill: white, weight: "bold", size: 14pt)[VERDICT: #verdict]
)

#v(0.2in)

*Claim:* #claim

#v(0.1in)

*Confidence Level:* #confidence
*Evidence Quality:* #evidence-quality

"""

    # Add key findings if available
    if key_findings:
        typst += "=== Key Findings\n\n"
        for finding in key_findings:
            # Convert markdown bold to plain text
            finding_clean = re.sub(r"\*\*([^*]+)\*\*", lambda m: m.group(1), finding)
            finding_clean = finding_clean.replace("✅", "").replace("❌", "").replace("⚠️", "").strip()
            typst += f"- {finding_clean}\n"
        typst += "\n"

    # Add Claim Statement section
    if "claim_statement" in sections or "Claim Statement" in str(sections):
        typst += "== Claim Statement\n\n"
        claim_content = sections.get("claim_statement", {}).get("content", [])
        if isinstance(claim_content, list):
            for line in claim_content:
                if isinstance(line, str) and line.strip():
                    # Convert markdown bold to Typst italic
                    # Use a function to avoid $1 being interpreted incorrectly
                    def replace_bold(match):
                        return f"*{match.group(1)}*"
                    line_clean = re.sub(r"\*\*([^*]+)\*\*", replace_bold, line)
                    # Only convert backticks if they look like file paths
                    if "`" in line_clean and ("/" in line_clean or ".py" in line_clean or ".md" in line_clean):
                        line_clean = convert_backticks_to_monospace(line_clean)
                    typst += f"{line_clean}\n\n"

    # Add Investigation Details
    typst += "== Investigation Details\n\n"

    # Methodology
    if "investigation_methodology" in sections:
        typst += "=== Methodology\n\n"
        methodology = sections["investigation_methodology"].get("content", [])
        if isinstance(methodology, list):
            for line in methodology:
                if line.strip() and line.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
                    item = re.sub(r"^\d+\.\s+", "", line.strip())
                    typst += f"{item}\n\n"

    # Files Examined
    typst += "=== Files Examined\n\n"
    files_examined = set()
    for evidence in evidence_items:
        if evidence.get("file"):
            # Clean file path (remove backticks if present)
            file_path = evidence["file"].replace("`", "").strip()
            files_examined.add(file_path)
    for file_path in sorted(files_examined):
        # Format file path as monospace text
        typst += f"- #text(font: \"mono\")[{file_path}]\n"
    typst += "\n"

    # Code Evidence
    if evidence_items:
        typst += "=== Code Evidence\n\n"
        for evidence in evidence_items:
            typst += f"==== {evidence['number']}. {evidence['title']}\n\n"
            if evidence.get("file"):
                # Clean file path
                file_path = evidence["file"].replace("`", "").strip()
                # Use monospace text instead of code block to avoid parsing issues
                typst += f"*Location:* #text(font: \"mono\")[{file_path}]"
                if evidence.get("lines"):
                    typst += f"  \n*Lines:* {evidence['lines']}"
                typst += "\n\n"
            if evidence.get("code"):
                code = evidence["code"]
                # Format code block - ensure proper indentation
                code_lines = code['content'].split('\n')
                formatted_code = '\n'.join(code_lines)
                typst += f"#block(\n  fill: rgb(\"f8f9fa\"),\n  inset: 10pt,\n  radius: 4pt,\n)[\n```{code['language']}\n{formatted_code}\n```\n]\n\n"
            if evidence.get("finding"):
                # Convert markdown bold to Typst italic
                finding_clean = re.sub(r"\*\*([^*]+)\*\*", lambda m: f"*{m.group(1)}*", evidence["finding"])
                typst += f"*Finding:* {finding_clean}\n\n"

    # Evidence Summary (if exists)
    if "evidence" in sections:
        evidence_content = sections["evidence"].get("content", [])
        if evidence_content:
            typst += "== Evidence Summary\n\n"
            # Add summary content if available

    # Verdict section
    typst += "== Verdict\n\n"
    typst += f"""#align(center)[
  #block(
    fill: rgb("{verdict_color}"),
    inset: 16pt,
    radius: 6pt,
    text(fill: white, weight: "bold", size: 18pt)[✅ VERDICT: #verdict]
  )
]

#v(0.3in)

The claim that *#claim* is **#verdict** with #confidence confidence.

"""

    # Add reasoning and limitations from verdict section if available
    if "verdict" in sections:
        verdict_content = sections["verdict"].get("content", [])
        if isinstance(verdict_content, list):
            in_reasoning = False
            in_limitations = False
            for line in verdict_content:
                if isinstance(line, str):
                    if "**Reasoning**:" in line or "*Reasoning*:" in line:
                        in_reasoning = True
                        in_limitations = False
                        typst += "*Reasoning:*\n"
                    elif "**Limitations**:" in line or "*Limitations*:" in line:
                        in_limitations = True
                        in_reasoning = False
                        typst += "\n*Limitations:*\n"
                    elif (in_reasoning or in_limitations) and line.strip().startswith("- "):
                        item = line.strip()[2:].strip()
                        # Skip file paths (they belong in Files section, not Limitations)
                        # Check for backticks with file path patterns
                        if "`" in item and ("/" in item or "\\" in item or ".py" in item or ".md" in item or ".toml" in item or "src/waft" in item or "__init__" in item):
                            continue
                        item_clean = re.sub(r"\*\*([^*]+)\*\*", r"*$1*", item)
                        item_clean = convert_backticks_to_monospace(item_clean)
                        typst += f"- {item_clean}\n"
                    elif (in_reasoning or in_limitations) and line.strip() and not line.strip().startswith(("###", "##", "---")):
                        # Stop at "---" separator (next section starts)
                        if line.strip() == "---":
                            break
                        line_clean = convert_backticks_to_monospace(line.strip())
                        typst += f"{line_clean}\n\n"

    typst += f"""
*Confidence Level:* #confidence

*Evidence Quality:* #evidence-quality

"""

    # Files Created/Modified
    files_section_key = None
    for key in sections.keys():
        if "file" in key.lower() or "created" in key.lower() or "modified" in key.lower():
            files_section_key = key
            break
    
    if files_section_key:
        typst += "== Files Created/Modified\n\n"
        # Parse the original markdown to get file lists (more reliable than parsed structure)
        raw_markdown = data.get("_raw_markdown", "")
        markdown_lines = raw_markdown.split("\n") if raw_markdown else []
        in_files_section = False
        in_new_files = False
        in_modified_files = False
        
        for line in markdown_lines:
            if line.startswith("## Files Created/Modified"):
                in_files_section = True
                continue
            elif in_files_section and line.startswith("## "):
                # End of files section
                break
            elif in_files_section and ("### New Files:" in line or "**New Files**:" in line):
                typst += "=== New Files\n\n"
                in_new_files = True
                in_modified_files = False
            elif in_files_section and ("### Modified Files:" in line or "**Modified Files**:" in line):
                typst += "\n=== Modified Files\n\n"
                in_new_files = False
                in_modified_files = True
            elif in_files_section and (in_new_files or in_modified_files) and line.strip().startswith("- "):
                # Extract file path from list item
                item_text = line.strip()[2:].strip()
                # Remove backticks and extract file path
                file_path = re.sub(r"`([^`]+)`", r"\1", item_text)
                # Remove parenthetical notes but keep them
                note_match = re.search(r"\(([^)]+)\)", file_path)
                note = note_match.group(1) if note_match else None
                file_path = re.sub(r"\s*\(.*?\)$", "", file_path).strip()
                # Format as monospace (no backticks)
                typst += f"- #text(font: \"mono\")[{file_path}]"
                if note:
                    typst += f" ({note})"
                typst += "\n"

    # Next Steps
    if "next_steps" in sections:
        typst += "== Next Steps\n\n"
        next_steps = sections["next_steps"].get("content", [])
        if isinstance(next_steps, list):
            for line in next_steps:
                if isinstance(line, str) and line.strip().startswith(("1.", "2.", "3.", "4.")):
                    # Remove numbered list prefix and convert bold
                    item = re.sub(r"^\d+\.\s+\*\*([^*]+)\*\*", lambda m: m.group(1), line.strip())
                    item = re.sub(r"^\d+\.\s+", "", item)
                    item = convert_backticks_to_monospace(item)
                    typst += f"{item}\n\n"

    # Footer
    typst += f"""#v(0.5in)

#align(center)[
  #text(size: 9pt, style: "italic")[
    Case Brief Generated: {case_date} \
    Case ID: #case-id \
    Investigator: Terry (AI Assistant) \
    Status: ✅ #verdict
  ]
]
"""

    # Final pass: Convert any remaining backticks in list items that look like file paths
    # Only process lines that are list items (start with "- ") to avoid breaking template syntax
    # Skip lines inside code blocks
    lines = typst.split('\n')
    converted_lines = []
    in_code_block = False
    for line in lines:
        # Track code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            converted_lines.append(line)
            continue
        
        # Don't process code block content
        if in_code_block:
            converted_lines.append(line)
            continue
        
        # Only convert if it's a list item with backticks that looks like a file path
        if line.strip().startswith("- ") and "`" in line:
            # Check if it looks like a file path
            if "/" in line or "\\" in line or ".py" in line or ".md" in line or ".toml" in line or "__init__" in line or "src/waft" in line:
                # Convert backticks to monospace, but preserve the "- " prefix
                prefix = "- "
                content = line.strip()[2:].strip()
                converted_content = convert_backticks_to_monospace(content)
                line = prefix + converted_content
        converted_lines.append(line)
    typst = "\n".join(converted_lines)

    return typst


def case_render_cmd(
    case_file: str = typer.Argument(..., help="Path to case file (.md or .typ)"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output PDF path"),
    open_pdf: bool = typer.Option(False, "--open", help="Open PDF after generation"),
    desktop: bool = typer.Option(False, "--desktop", help="Copy PDF to desktop"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path"),
):
    """
    Render a case file to PDF.
    
    Supports both .md (markdown) and .typ (Typst) case files.
    Automatically converts markdown to Typst using the case_brief.typ template structure.
    
    Examples:
        waft case-render case_20260121_080648.md
        waft case-render case_20260121_080648.typ --open
        waft case-render case_20260121_080648.md --desktop --open
    """
    project_path = resolve_project_path(path)
    case_path = Path(case_file)

    # Resolve relative paths
    if not case_path.is_absolute():
        if (project_path / case_path).exists():
            case_path = project_path / case_path
        elif (project_path / "_work_efforts" / "proof_cases" / case_path).exists():
            case_path = project_path / "_work_efforts" / "proof_cases" / case_path
        elif (project_path / "_work_efforts" / "proof_cases" / case_path.name).exists():
            case_path = project_path / "_work_efforts" / "proof_cases" / case_path.name

    if not case_path.exists():
        console.print(f"[red]❌ Case file not found: {case_path}[/red]")
        raise typer.Exit(1)

    console.print(f"[green]📄 Rendering case file: {case_path.name}[/green]")

    # Read content
    content = case_path.read_text(encoding="utf-8")

    # Convert to Typst if markdown
    if case_path.suffix == ".md":
        console.print("[dim]Converting markdown to Typst using case_brief template structure...[/dim]")
        parsed_data = parse_markdown_case_file(content)
        typst_content = generate_typst_from_parsed_data(parsed_data)
    elif case_path.suffix == ".typ":
        typst_content = content
    else:
        console.print(f"[red]❌ Unsupported file type: {case_path.suffix}[/red]")
        console.print("[yellow]Supported: .md, .typ[/yellow]")
        raise typer.Exit(1)

    # Determine output path
    if output:
        output_pdf = Path(output)
    else:
        output_pdf = case_path.with_suffix(".pdf")

    # Compile to PDF
    try:
        compiler = TypstCompiler()
        compiler.compile(
            typst_content=typst_content,
            output_path=output_pdf,
            working_dir=None,
        )
        console.print(f"[green]✅ PDF generated: {output_pdf}[/green]")
    except Exception as e:
        console.print(f"[red]❌ Compilation failed: {e}[/red]")
        console.print(f"[dim]Error details: {str(e)[:200]}[/dim]")
        raise typer.Exit(1)

    # Copy to desktop if requested
    if desktop:
        desktop_pdf = Path.home() / "Desktop" / output_pdf.name
        shutil.copy2(output_pdf, desktop_pdf)
        console.print(f"[green]📋 Copied to desktop: {desktop_pdf}[/green]")
        output_pdf = desktop_pdf

    # Open PDF if requested
    if open_pdf:
        console.print("[dim]Opening PDF...[/dim]")
        try:
            subprocess.run(["open", str(output_pdf)], check=False)
        except Exception as e:
            console.print(f"[yellow]⚠️  Could not open PDF: {e}[/yellow]")
            console.print(f"[dim]PDF is at: {output_pdf}[/dim]")


# Export the command function for main.py
__all__ = ["case_render_cmd"]
