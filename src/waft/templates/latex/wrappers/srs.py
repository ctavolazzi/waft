"""
SRS LaTeX Template Wrapper
===========================

Python wrapper for Ashad001 SRS (Software Requirements Specification) template.
Auto-discovered by LaTeXTemplateRegistry.

category: specification
tags: [latex, pdf, srs, requirements, specification]
source: ashad001
"""

from pathlib import Path
from ..compiler import LaTeXCompiler
from ..content_builders import build_report_content


def generate_srs(
    title: str,
    content: str,
    output_path: Path,
    software_name: str = "Software Name",
    course_code: str = "CS-CODE",
    course_name: str = "COURSE_NAME",
    instructor: str = "INSTRUCTOR/SUPERVISOR NAME",
    members: list = None,
    introduction: str = "",
    motivation: str = "",
    stakeholders: str = "",
    assumptions_dependencies: str = "",
    functional_requirements: str = "",
    operating_environment: str = "",
    non_functional_requirements: str = "",
    constraints: str = "",
    architecture_design: str = "",
    revision_history: str = "",
    **kwargs
) -> Path:
    """
    Generate PDF using SRS LaTeX template.

    Args:
        title: Document title
        content: Main content (markdown or HTML)
        output_path: Where to save PDF
        software_name: Name of the software
        course_code: Course code (e.g., CS-CODE)
        course_name: Course name
        instructor: Instructor/supervisor name
        members: List of team member names
        introduction: Introduction section content
        motivation: Motivation subsection content
        stakeholders: Stakeholders subsection content
        assumptions_dependencies: Assumptions and dependencies subsection content
        functional_requirements: Functional requirements section content
        operating_environment: Operating environment subsection content
        non_functional_requirements: Non-functional requirements section content
        constraints: Constraints section content
        architecture_design: Architecture design section content
        revision_history: Revision history section content
        **kwargs: Additional template parameters

    Returns:
        Path to generated PDF
    """
    # Get template path (from wrappers/ to project root, then to templates/)
    template_dir = Path(__file__).parent.parent.parent.parent.parent.parent / "templates" / "ashad001-latex-templates" / "SRS Template"
    template_file = template_dir / "main.tex"

    if not template_file.exists():
        raise FileNotFoundError(f"SRS template not found: {template_file}")

    # Load template
    template_content = template_file.read_text(encoding="utf-8")

    # Prepare members (default to empty list if not provided)
    if members is None:
        members = []

    # Ensure we have at least 3 member slots
    while len(members) < 3:
        members.append("")

    # Build LaTeX content from markdown/HTML
    latex_content = build_report_content(
        title=title,
        content=content,
        **kwargs
    )

    # Replace placeholders in template (templates use hardcoded placeholders, not Jinja2)
    filled_latex = template_content

    # Replace title and header placeholders
    filled_latex = filled_latex.replace("SOFTWARE NAME", software_name)
    filled_latex = filled_latex.replace("CS-CODE", course_code)
    filled_latex = filled_latex.replace("COURSE_NAME", course_name)
    filled_latex = filled_latex.replace("INSTRUCTOR/SUPERVISOR NAME", instructor)

    # Replace member placeholders
    filled_latex = filled_latex.replace("MEMBER1", members[0] if len(members) > 0 else "MEMBER1")
    filled_latex = filled_latex.replace("MEMBER2", members[1] if len(members) > 1 else "MEMBER2")
    filled_latex = filled_latex.replace("MEMBER3", members[2] if len(members) > 2 else "MEMBER3")

    # Replace section content
    if introduction:
        filled_latex = filled_latex.replace("\\section{Introduction}", f"\\section{{Introduction}}\n\n{introduction}")
    if motivation:
        filled_latex = filled_latex.replace("\\subsection{Motivation}", f"\\subsection{{Motivation}}\n\n{motivation}")
    if stakeholders:
        filled_latex = filled_latex.replace("\\subsection{Stakeholders}", f"\\subsection{{Stakeholders}}\n\n{stakeholders}")
    if assumptions_dependencies:
        filled_latex = filled_latex.replace("\\subsection{Assumptions and Dependencies}", f"\\subsection{{Assumptions and Dependencies}}\n\n{assumptions_dependencies}")
    if functional_requirements:
        filled_latex = filled_latex.replace("\\section{Functional Requirements}", f"\\section{{Functional Requirements}}\n\n{functional_requirements}")
    if operating_environment:
        filled_latex = filled_latex.replace("\\subsection{Operating Environment}", f"\\subsection{{Operating Environment}}\n\n{operating_environment}")
    if non_functional_requirements:
        filled_latex = filled_latex.replace("\\section{Non-functional Requirements}", f"\\section{{Non-functional Requirements}}\n\n{non_functional_requirements}")
    if constraints:
        filled_latex = filled_latex.replace("\\section{Constraints}", f"\\section{{Constraints}}\n\n{constraints}")
    if architecture_design:
        filled_latex = filled_latex.replace("\\section{Architecture Design}", f"\\section{{Architecture Design}}\n\n{architecture_design}")
    if revision_history:
        filled_latex = filled_latex.replace("\\section{Revision History}", f"\\section{{Revision History}}\n\n{revision_history}")

    # Compile to PDF
    compiler = LaTeXCompiler(compiler="pdflatex")
    pdf_path = compiler.compile(
        filled_latex,
        output_path,
        working_dir=template_dir,
        runs=2
    )

    return pdf_path
