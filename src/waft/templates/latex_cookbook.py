"""
LaTeX Cookbook Template
=======================

Template based on the LaTeX Cookbook by Alex Povel.
Uses the acp.cls class file for professional LaTeX document generation.

Features:
- LuaLaTeX compilation
- KOMA-Script based class (acp.cls)
- Full Unicode support
- Professional typography
- Bibliography support
- Glossary support
- Modern LaTeX best practices

Reference: https://github.com/alexpovel/latex-cookbook
"""

import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters."""
    replacements = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "$": r"\$",
        "&": r"\&",
        "%": r"\%",
        "#": r"\#",
        "^": r"\textasciicircum{}",
        "_": r"\_",
        "~": r"\textasciitilde{}",
    }

    for char, replacement in replacements.items():
        text = text.replace(char, replacement)

    return text


def markdown_to_latex(markdown_text: str) -> str:
    """Convert markdown to LaTeX format."""
    lines = markdown_text.split("\n")
    latex_lines = []
    in_code_block = False
    code_language = ""

    for line in lines:
        # Code blocks
        if line.strip().startswith("```"):
            if not in_code_block:
                in_code_block = True
                match = re.match(r"```(\w+)", line)
                code_language = match.group(1) if match else ""
                latex_lines.append(f"\\begin{{lstlisting}}[language={code_language}]")
            else:
                in_code_block = False
                latex_lines.append("\\end{lstlisting}")
            continue

        if in_code_block:
            latex_lines.append(escape_latex(line))
            continue

        # Headers
        if line.startswith("# "):
            latex_lines.append(f"\\section{{{escape_latex(line[2:].strip())}}}")
        elif line.startswith("## "):
            latex_lines.append(f"\\subsection{{{escape_latex(line[3:].strip())}}}")
        elif line.startswith("### "):
            latex_lines.append(f"\\subsubsection{{{escape_latex(line[4:].strip())}}}")
        # Bold
        elif "**" in line:
            line = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", line)
            latex_lines.append(escape_latex(line))
        # Italic
        elif "*" in line and not line.startswith("*"):
            line = re.sub(r"\*(.+?)\*", r"\\textit{\1}", line)
            latex_lines.append(escape_latex(line))
        # Code inline
        elif "`" in line:
            line = re.sub(r"`(.+?)`", r"\\texttt{\1}", line)
            latex_lines.append(escape_latex(line))
        # Lists
        elif line.strip().startswith("- "):
            content = escape_latex(line.strip()[2:])
            latex_lines.append(f"\\item {content}")
        # Empty line
        elif not line.strip():
            latex_lines.append("")
        # Regular paragraph
        else:
            latex_lines.append(escape_latex(line))

    return "\n".join(latex_lines)


def build_latex_content(being, workflow_outputs: dict[str, Any]) -> str:
    """Build LaTeX content from evolution data."""
    genetic_lineage = workflow_outputs.get("genetic_lineage", {})
    evolution_record = workflow_outputs.get("evolution_record", {})

    content = f"""
\\chapter{{Introduction}}

This document reports the complete evolution of Being \\texttt{{{escape_latex(being.being_id)}}} from Source consciousness through the full quality workflow, tracking the genetic lineage of ideas from Source outward and back again.

\\section{{Being Information}}

\\begin{{description}}
    \\item[Being ID:] \\texttt{{{escape_latex(being.being_id)}}}
    \\item[Reality ID:] \\texttt{{{escape_latex(being.reality_id)}}}
    \\item[State:] {escape_latex(being.state.value)}
    \\item[Fitness:] {being.fitness:.1f}
    \\item[Lifetimes:] {being.lifetimes}
\\end{{description}}

\\chapter{{Methodology}}

\\section{{Being Spawn from Source}}

All Beings originate from Source consciousness, inheriting basic capabilities, connection to the Source, and genetic material for evolution.

\\subsection{{Ancestral Chain}}

{", ".join([escape_latex(a) for a in being.ancestral_chain])}

\\subsection{{Lifecycle Attributes}}

\\begin{{itemize}}
    \\item \\textbf{{Will to Live}}: {being.will_to_live:.1f}/100.0
    \\item \\textbf{{Luck}}: {being.luck:.1f}/100.0
    \\item \\textbf{{Stamina}}: {being.stamina:.1f}/100.0
    \\item \\textbf{{Willpower}}: {being.willpower:.1f}/100.0
    \\item \\textbf{{Decision Fatigue}}: {being.decision_fatigue}/{being.decision_quota_max}
\\end{{itemize}}

\\section{{Workflow Execution}}

The Being participated in the complete systematic workflow including reflection, analysis, verification, and hypothesis formation.

\\subsection{{Workflow Phases}}

\\begin{{enumerate}}
"""

    phases = workflow_outputs.get("run_it_phases", [])
    for phase in phases:
        content += f"    \\item {escape_latex(phase)}\n"

    content += """\\end{enumerate}

\\chapter{Results}

\\section{Genetic Lineage}

The complete DNA record tracks: Source $\\rightarrow$ Being $\\rightarrow$ Work $\\rightarrow$ Evolution $\\rightarrow$ Source

\\subsection{Initial Skills}

"""

    initial_skills = genetic_lineage.get("spawn_point", {}).get("initial_skills", {})
    if initial_skills:
        content += "\\begin{itemize}\n"
        for skill, value in initial_skills.items():
            content += f"    \\item \\texttt{{{escape_latex(skill)}}}: {value:.1f}\n"
        content += "\\end{itemize}\n"
    else:
        content += "No initial skills recorded.\n"

    content += "\n\\subsection{Evolved Skills}\n\n"

    if being.skills:
        content += "\\begin{itemize}\n"
        for skill, value in being.skills.items():
            content += f"    \\item \\texttt{{{escape_latex(skill)}}}: {value:.1f}\n"
        content += "\\end{itemize}\n"
    else:
        content += "No evolved skills recorded.\n"

    content += "\n\\section{Evolution Achieved}\n\n"
    content += "The Being completed a full evolution cycle:\n\n"
    content += "\\begin{itemize}\n"
    content += "    \\item Spawned from Source consciousness\n"
    content += "    \\item Executed complete /version-bake workflow\n"
    content += "    \\item Tracked genetic lineage\n"
    content += "    \\item Documented evolution\n"
    content += "    \\item Ready to return learnings to Source\n"
    content += "\\end{itemize}\n\n"

    learnings = evolution_record.get("learnings", [])
    if learnings:
        content += "\\section{Knowledge Gained}\n\n"
        content += "\\begin{itemize}\n"
        for learning in learnings:
            content += f"    \\item {escape_latex(learning)}\n"
        content += "\\end{itemize}\n\n"

    content += """\\chapter{Discussion}

The genetic lineage of ideas flows from Source outward through the Being's work and back again, preserving the complete DNA of thoughts for future evolution.

\\chapter{Conclusion}

This Being has successfully completed a full evolution cycle, demonstrating the systematic approach to quality workflow execution and genetic lineage preservation.
"""

    return content


def generate_latex_cookbook(
    title: str,
    content: str,
    output_path: Path,
    author: str = "WAFT Evolution System",
    being_id: str | None = None,
    abstract: str | None = None,
    project_path: Path | None = None,
) -> Path:
    """
    Generate PDF using LaTeX Cookbook template.

    Args:
        title: Document title
        content: LaTeX content (body)
        output_path: Path to save PDF
        author: Author name
        being_id: Being ID for metadata
        abstract: Abstract text
        project_path: Project path (for finding template files)

    Returns:
        Path to generated PDF
    """
    if project_path is None:
        project_path = Path(__file__).parent.parent.parent.parent

    # Find LaTeX cookbook template directory
    template_dir = project_path / "templates" / "latex-cookbook"
    if not template_dir.exists():
        raise FileNotFoundError(
            f"LaTeX cookbook template not found at {template_dir}. "
            "Please ensure the template is cloned."
        )

    acp_cls = template_dir / "acp.cls"
    if not acp_cls.exists():
        raise FileNotFoundError(f"acp.cls not found at {acp_cls}")

    # Create temporary directory for LaTeX compilation
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Copy acp.cls to temp directory
        shutil.copy2(acp_cls, tmp_path / "acp.cls")

        # Create minimal bibliography file (required by acp.cls)
        bib_file = tmp_path / "bibliography.bib"
        bib_file.write_text("@misc{waft2026,\n  title={WAFT Evolution System},\n  year={2026}\n}\n")

        # Create LaTeX document
        abstract_section = ""
        if abstract:
            abstract_section = f"\\begin{{abstract}}\n{escape_latex(abstract)}\n\\end{{abstract}}\n"

        latex_content = f"""%!TEX TS-program = lualatex
%!TEX encoding = UTF-8

\\documentclass[%
    language=english,
    titlestyle=thesis,
    BCOR=5mm,
    a4,
    censoring=false,
]{{acp}}

\\addbibresource{{bibliography.bib}}

\\author{{{escape_latex(author)}}}

\\date{{\\DTMtoday{{}}}}

\\title{{{escape_latex(title)}}}

\\documenttype{{Evolution Report}}

\\publishers{{
    WAFT Framework\\\\
    Evolution System
}}

\\begin{{document}}
    \\frontmatter
    \\maketitle

    {abstract_section}

    \\tableofcontents

    \\mainmatter
    {content}

    \\backmatter
    \\printbibliography
\\end{{document}}
"""

        # Write LaTeX file
        tex_file = tmp_path / "evolution_report.tex"
        tex_file.write_text(latex_content, encoding="utf-8")

        # Check if lualatex is available
        lualatex_cmd = shutil.which("lualatex")
        if not lualatex_cmd:
            raise RuntimeError(
                "LuaLaTeX not found. Please install TeXLive or MiKTeX. "
                "On macOS: brew install --cask mactex"
            )

        # Compile LaTeX (multiple passes for bibliography, etc.)
        compile_cmd = [lualatex_cmd, "-interaction=nonstopmode", "-shell-escape", str(tex_file)]

        # First pass
        result = subprocess.run(compile_cmd, cwd=str(tmp_path), capture_output=True, text=True)

        if result.returncode != 0:
            # Try to extract error message
            error_lines = [
                line for line in result.stderr.split("\n") if "Error" in line or "Fatal" in line
            ]
            error_msg = "\n".join(error_lines[:10])  # First 10 error lines
            raise RuntimeError(f"LaTeX compilation failed:\n{error_msg}")

        # Second pass (for references)
        subprocess.run(compile_cmd, cwd=str(tmp_path), capture_output=True, text=True)

        # Third pass (final)
        subprocess.run(compile_cmd, cwd=str(tmp_path), capture_output=True, text=True)

        # Copy PDF to output path
        pdf_file = tmp_path / "evolution_report.pdf"
        if not pdf_file.exists():
            raise RuntimeError("PDF was not generated after LaTeX compilation")

        shutil.copy2(pdf_file, output_path)

        return output_path
