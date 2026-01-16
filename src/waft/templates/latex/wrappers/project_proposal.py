"""
Project Proposal LaTeX Template Wrapper
=======================================

Python wrapper for Ashad001 Project Proposal template.
Auto-discovered by LaTeXTemplateRegistry.

category: proposal
tags: [latex, pdf, project, proposal]
source: ashad001
"""

from pathlib import Path
from ..compiler import LaTeXCompiler
from ..content_builders import build_report_content


def generate_project_proposal(
    title: str,
    content: str,
    output_path: Path,
    project_name: str = "PROJECT NAME",
    course_code: str = "CS-CODE",
    course_name: str = "COURSE_NAME",
    members: list = None,
    department: str = "Department of Computer Science",
    introduction: str = "",
    objectives: str = "",
    methodology: str = "",
    evaluation: str = "",
    expected_outcome: str = "",
    conclusion: str = "",
    **kwargs
) -> Path:
    """
    Generate PDF using Project Proposal LaTeX template.

    Args:
        title: Document title
        content: Main content (markdown or HTML)
        output_path: Where to save PDF
        project_name: Project name
        course_code: Course code (e.g., CS-CODE)
        course_name: Course name
        members: List of dicts with 'name' and 'email' keys
        department: Department name
        introduction: Introduction section content
        objectives: Objectives section content
        methodology: Methodology section content
        evaluation: Evaluation subsection content
        expected_outcome: Expected outcome section content
        conclusion: Conclusion section content
        **kwargs: Additional template parameters

    Returns:
        Path to generated PDF
    """
    # Get template path (from wrappers/ to project root, then to templates/)
    template_dir = Path(__file__).parent.parent.parent.parent.parent.parent / "templates" / "ashad001-latex-templates" / "Project Proposal Template"
    template_file = template_dir / "main.tex"

    if not template_file.exists():
        raise FileNotFoundError(f"Project Proposal template not found: {template_file}")

    # Load template
    template_content = template_file.read_text(encoding="utf-8")

    # Prepare members (default to empty list if not provided)
    if members is None:
        members = []

    # Ensure we have at least 3 member slots
    while len(members) < 3:
        members.append({"name": "", "email": ""})

    # Build LaTeX content from markdown/HTML
    latex_content = build_report_content(
        title=title,
        content=content,
        **kwargs
    )

    # Replace placeholders in template (templates use hardcoded placeholders, not Jinja2)
    filled_latex = template_content

    # Replace header placeholders
    filled_latex = filled_latex.replace("CS-CODE", course_code)
    filled_latex = filled_latex.replace("COURSE_NAME", course_name)
    filled_latex = filled_latex.replace("PROJECT NAME", project_name)
    filled_latex = filled_latex.replace("Department of Computer Science", department)

    # Replace member placeholders
    member1_name = members[0].get("name", "") if isinstance(members[0], dict) else members[0] if len(members) > 0 else "MEMBER1"
    member1_email = members[0].get("email", "") if isinstance(members[0], dict) else ""
    filled_latex = filled_latex.replace("MEMBER1", member1_name)
    filled_latex = filled_latex.replace("MEMBER1@gmail.com", member1_email or "MEMBER1@gmail.com")

    member2_name = members[1].get("name", "") if isinstance(members[1], dict) else members[1] if len(members) > 1 else "MEMBER2"
    member2_email = members[1].get("email", "") if isinstance(members[1], dict) else ""
    filled_latex = filled_latex.replace("MEMBER2", member2_name)
    filled_latex = filled_latex.replace("MEMBER2@gmail.com", member2_email or "MEMBER2@gmail.com")

    member3_name = members[2].get("name", "") if isinstance(members[2], dict) else members[2] if len(members) > 2 else "MEMBER3"
    member3_email = members[2].get("email", "") if isinstance(members[2], dict) else ""
    filled_latex = filled_latex.replace("MEMBER3", member3_name)
    filled_latex = filled_latex.replace("MEMBER3@gmail.com", member3_email or "MEMBER3@gmail.com")

    # Replace section content
    if introduction:
        filled_latex = filled_latex.replace("\\section{Introduction}", f"\\section{{Introduction}}\n\n{introduction}")
    if objectives:
        filled_latex = filled_latex.replace("\\section{Objectives}", f"\\section{{Objectives}}\n\n{objectives}")
    if methodology:
        filled_latex = filled_latex.replace("\\section{Methodology}", f"\\section{{Methodology}}\n\n{methodology}")
    if evaluation:
        filled_latex = filled_latex.replace("\\subsection{Evaluation}", f"\\subsection{{Evaluation}}\n\n{evaluation}")
    if expected_outcome:
        filled_latex = filled_latex.replace("\\section{Expected Outcome}", f"\\section{{Expected Outcome}}\n\n{expected_outcome}")
    if conclusion:
        filled_latex = filled_latex.replace("\\section{Conclusion}", f"\\section{{Conclusion}}\n\n{conclusion}")

    # Compile to PDF
    compiler = LaTeXCompiler(compiler="pdflatex")
    pdf_path = compiler.compile(
        filled_latex,
        output_path,
        working_dir=template_dir,
        runs=2
    )

    return pdf_path
