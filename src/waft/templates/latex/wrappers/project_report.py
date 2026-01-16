"""
Project Report LaTeX Template Wrapper
======================================

Python wrapper for Ashad001 Project Report templates.
Supports both Template 1 and Template 2.
Auto-discovered by LaTeXTemplateRegistry.

category: report
tags: [latex, pdf, project, report]
source: ashad001
"""

from pathlib import Path
from ..compiler import LaTeXCompiler
from ..content_builders import build_report_content


def generate_project_report(
    title: str,
    content: str,
    output_path: Path,
    project_name: str = "PROJECT NAME",
    course_code: str = "CS-CODE",
    course_name: str = "COURSE NAME",
    members: list = None,
    major: str = "MAJOR",
    template_version: int = 1,
    abstract: str = "",
    introduction: str = "",
    background: str = "",
    project_specification: str = "",
    problem_analysis: str = "",
    solution_design: str = "",
    implementation_testing: str = "",
    project_breakdown: str = "",
    results: str = "",
    experimental_setup: str = "",
    conclusion: str = "",
    **kwargs
) -> Path:
    """
    Generate PDF using Project Report LaTeX template.

    Args:
        title: Document title
        content: Main content (markdown or HTML)
        output_path: Where to save PDF
        project_name: Project name
        course_code: Course code (e.g., CS-CODE)
        course_name: Course name
        members: List of dicts with 'name', 'id', 'email' keys (Template 1) or 'name', 'email' (Template 2)
        major: Major/department name (Template 1 only)
        template_version: Which template to use (1 or 2, default: 1)
        abstract: Abstract content (Template 2 only)
        introduction: Introduction section content
        background: Background section content
        project_specification: Project specification section content (Template 1 only)
        problem_analysis: Problem analysis section content (Template 1 only)
        solution_design: Solution design section content (Template 1 only)
        implementation_testing: Implementation & testing section content (Template 1 only)
        project_breakdown: Project breakdown structure section content (Template 1 only)
        results: Results section content (Template 1 only)
        experimental_setup: Experimental setup section content (Template 2 only)
        conclusion: Conclusion section content
        **kwargs: Additional template parameters

    Returns:
        Path to generated PDF
    """
    # Select template directory based on version
    if template_version == 1:
        template_subdir = "Project Report Template 1"
    elif template_version == 2:
        template_subdir = "Project Report Template 2"
    else:
        raise ValueError(f"Invalid template_version: {template_version}. Must be 1 or 2.")

    # Get template path (from wrappers/ to project root, then to templates/)
    template_dir = Path(__file__).parent.parent.parent.parent.parent.parent / "templates" / "ashad001-latex-templates" / template_subdir
    template_file = template_dir / "main.tex"

    if not template_file.exists():
        raise FileNotFoundError(f"Project Report template {template_version} not found: {template_file}")

    # Load template
    template_content = template_file.read_text(encoding="utf-8")

    # Prepare members (default to empty list if not provided)
    if members is None:
        members = []

    # Ensure we have at least 3 member slots
    while len(members) < 3:
        members.append({"name": "", "id": "", "email": ""})

    # Build LaTeX content from markdown/HTML
    latex_content = build_report_content(
        title=title,
        content=content,
        **kwargs
    )

    # Replace placeholders in template (templates use hardcoded placeholders, not Jinja2)
    filled_latex = template_content

    if template_version == 1:
        # Template 1 uses: CS-CODE, COURSE NAME, PROJECT NAME, Member 1, ID, member1@gmail.com, MAJOR
        filled_latex = filled_latex.replace("CS-CODE", course_code)
        filled_latex = filled_latex.replace("COURSE NAME", course_name)
        filled_latex = filled_latex.replace("PROJECT NAME", project_name)
        filled_latex = filled_latex.replace("MAJOR", major)

        # Replace member placeholders
        member1_name = members[0].get("name", "") if isinstance(members[0], dict) else "Member 1"
        member1_id = members[0].get("id", "") if isinstance(members[0], dict) else "ID"
        member1_email = members[0].get("email", "") if isinstance(members[0], dict) else "member1@gmail.com"
        filled_latex = filled_latex.replace("Member 1", member1_name)
        filled_latex = filled_latex.replace("ID", member1_id, 1)  # Replace first occurrence
        filled_latex = filled_latex.replace("member1@gmail.com", member1_email)

        member2_name = members[1].get("name", "") if isinstance(members[1], dict) else "Member 2"
        member2_id = members[1].get("id", "") if isinstance(members[1], dict) else "ID"
        member2_email = members[1].get("email", "") if isinstance(members[1], dict) else "member2@gmail.com"
        filled_latex = filled_latex.replace("Member 2", member2_name)
        filled_latex = filled_latex.replace("ID", member2_id, 1)  # Replace second occurrence
        filled_latex = filled_latex.replace("member2@gmail.com", member2_email)

        member3_name = members[2].get("name", "") if isinstance(members[2], dict) else "Member 3"
        member3_id = members[2].get("id", "") if isinstance(members[2], dict) else "ID"
        member3_email = members[2].get("email", "") if isinstance(members[2], dict) else "member3@gmail.com"
        filled_latex = filled_latex.replace("Member 3", member3_name)
        filled_latex = filled_latex.replace("ID", member3_id, 1)  # Replace third occurrence
        filled_latex = filled_latex.replace("member3@gmail.com", member3_email)

        # Replace section content
        if introduction:
            filled_latex = filled_latex.replace("\\section*{Introduction}", f"\\section*{{Introduction}}\n\n{introduction}")
        if background:
            filled_latex = filled_latex.replace("\\section*{Background}", f"\\section*{{Background}}\n\n{background}")
        if project_specification:
            filled_latex = filled_latex.replace("\\section*{Project Specification}", f"\\section*{{Project Specification}}\n\n{project_specification}")
        if problem_analysis:
            filled_latex = filled_latex.replace("\\section*{Problem Analysis}", f"\\section*{{Problem Analysis}}\n\n{problem_analysis}")
        if solution_design:
            filled_latex = filled_latex.replace("\\section*{Solution Design}", f"\\section*{{Solution Design}}\n\n{solution_design}")
        if implementation_testing:
            filled_latex = filled_latex.replace("\\section*{Implementation \\& Testing}", f"\\section*{{Implementation \\& Testing}}\n\n{implementation_testing}")
        if project_breakdown:
            filled_latex = filled_latex.replace("\\section*{Project Breakdown Structure}", f"\\section*{{Project Breakdown Structure}}\n\n{project_breakdown}")
        if results:
            filled_latex = filled_latex.replace("\\section*{Results}", f"\\section*{{Results}}\n\n{results}")
        if conclusion:
            filled_latex = filled_latex.replace("\\section*{Conclusion}", f"\\section*{{Conclusion}}\n\n{conclusion}")
    else:
        # Template 2 uses: CS_CODE, COURSE_NAME, PROJECT TITLE, MEMBER1, MEMBER1@gmail.com
        filled_latex = filled_latex.replace("CS_CODE", course_code)
        filled_latex = filled_latex.replace("COURSE_NAME", course_name)
        filled_latex = filled_latex.replace("PROJECT TITLE", project_name)

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
        filled_latex = filled_latex.replace("MEMBER@gmail.com", member3_email or "MEMBER@gmail.com")

        # Replace section content
        if abstract:
            # Abstract is in center environment
            filled_latex = filled_latex.replace("% Abstract will be in center", f"{abstract}")
        if introduction:
            filled_latex = filled_latex.replace("\\section{Introduction}", f"\\section{{Introduction}}\n\n{introduction}")
        if background:
            filled_latex = filled_latex.replace("\\section{Background}", f"\\section{{Background}}\n\n{background}")
        if implementation_testing:
            filled_latex = filled_latex.replace("\\section{Implementation and Execution}", f"\\section{{Implementation and Execution}}\n\n{implementation_testing}")
        if experimental_setup:
            filled_latex = filled_latex.replace("\\section{Experimental Setup}", f"\\section{{Experimental Setup}}\n\n{experimental_setup}")
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
