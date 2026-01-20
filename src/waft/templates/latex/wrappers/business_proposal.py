"""
Business Proposal LaTeX Template Wrapper
=========================================

Python wrapper for Ashad001 Business Proposal template.
Auto-discovered by LaTeXTemplateRegistry.

category: proposal
tags: [latex, pdf, business, proposal]
source: ashad001
"""

from pathlib import Path

from ..compiler import LaTeXCompiler
from ..content_builders import build_report_content


def generate_business_proposal(
    title: str,
    content: str,
    output_path: Path,
    business_name: str = "Business Name",
    location: str = "Location/University",
    members: list = None,
    introduction: str = "",
    rationale: str = "",
    proposed_solutions: str = "",
    workflow_budget: str = "",
    budget_breakdown: str = "",
    business_model: str = "",
    conclusion: str = "",
    final_message: str = "",
    slogan: str = "",
    **kwargs,
) -> Path:
    """
    Generate PDF using Business Proposal LaTeX template.

    Args:
        title: Document title
        content: Main content (markdown or HTML)
        output_path: Where to save PDF
        business_name: Business/company name
        location: Location or university name
        members: List of dicts with 'name', 'position', 'email' keys
        introduction: Introduction section content
        rationale: Rationale section content
        proposed_solutions: Proposed solutions section content
        workflow_budget: Workflow & budget allocation section content
        budget_breakdown: Budget breakdown section content
        business_model: Business model section content
        conclusion: Conclusion section content
        final_message: Final message section content
        slogan: Slogan text
        **kwargs: Additional template parameters

    Returns:
        Path to generated PDF
    """
    # Get template path (from wrappers/ to project root, then to templates/)
    template_dir = (
        Path(__file__).parent.parent.parent.parent.parent.parent
        / "templates"
        / "ashad001-latex-templates"
        / "Business Proposal Template"
    )
    template_file = template_dir / "main.tex"

    if not template_file.exists():
        raise FileNotFoundError(f"Business Proposal template not found: {template_file}")

    # Load template
    template_content = template_file.read_text(encoding="utf-8")

    # Prepare members (default to empty list if not provided)
    if members is None:
        members = []

    # Ensure we have at least 5 member slots (template supports up to 5)
    while len(members) < 5:
        members.append({"name": "", "position": "", "email": ""})

    # Build LaTeX content from markdown/HTML
    build_report_content(title=title, content=content, **kwargs)

    # Replace placeholders in template (templates use hardcoded placeholders, not Jinja2)
    filled_latex = template_content

    # Replace business name and location
    filled_latex = filled_latex.replace("{Buissness Name}", business_name)
    filled_latex = filled_latex.replace("Location/University", location)

    # Replace member information
    filled_latex = filled_latex.replace("Member 1", members[0].get("name", "Member 1"))
    filled_latex = filled_latex.replace("Position/ID", members[0].get("position", "Position/ID"))
    filled_latex = filled_latex.replace(
        "member1@gmail.com", members[0].get("email", "member1@gmail.com")
    )

    filled_latex = filled_latex.replace("Member 2", members[1].get("name", "Member 2"))
    filled_latex = filled_latex.replace(
        "Position/ID", members[1].get("position", "Position/ID"), 1
    )  # Replace second occurrence
    filled_latex = filled_latex.replace(
        "member2@gmail.com", members[1].get("email", "member2@gmail.com")
    )

    filled_latex = filled_latex.replace("Member 3", members[2].get("name", "Member 3"))
    filled_latex = filled_latex.replace(
        "Position/ID", members[2].get("position", "Position/ID"), 1
    )  # Replace third occurrence
    filled_latex = filled_latex.replace(
        "member3@gmail.com", members[2].get("email", "member3@gmail.com")
    )

    filled_latex = filled_latex.replace("Member 4", members[3].get("name", "Member 4"))
    filled_latex = filled_latex.replace(
        "Position/ID", members[3].get("position", "Position/ID"), 1
    )  # Replace fourth occurrence
    filled_latex = filled_latex.replace(
        "member4@gmail.com", members[3].get("email", "member4@gmail.com")
    )

    filled_latex = filled_latex.replace("Member 5", members[4].get("name", "Member 5"))
    filled_latex = filled_latex.replace(
        "Position/ID", members[4].get("position", "Position/ID"), 1
    )  # Replace fifth occurrence
    filled_latex = filled_latex.replace(
        "member5@gmail.com", members[4].get("email", "member5@gmail.com")
    )

    # Replace section content
    if introduction:
        filled_latex = filled_latex.replace("INTRODUCTION", introduction)
    if rationale:
        filled_latex = filled_latex.replace("RATIONAL", rationale)
    if proposed_solutions:
        # Find the Proposed Solutions section and insert content
        filled_latex = filled_latex.replace(
            "\\section{Proposed Solutions }",
            f"\\section{{Proposed Solutions}}\n\n{proposed_solutions}",
        )
    if workflow_budget:
        filled_latex = filled_latex.replace(
            "\\section{Workflow \\& Budget Allocation}",
            f"\\section{{Workflow \\& Budget Allocation}}\n\n{workflow_budget}",
        )
    if budget_breakdown:
        filled_latex = filled_latex.replace(
            "\\section{Budget Breakdown}", f"\\section{{Budget Breakdown}}\n\n{budget_breakdown}"
        )
    if business_model:
        filled_latex = filled_latex.replace(
            "\\section{Business Model}", f"\\section{{Business Model}}\n\n{business_model}"
        )
    if conclusion:
        filled_latex = filled_latex.replace(
            "\\section{Conclusion}", f"\\section{{Conclusion}}\n\n{conclusion}"
        )
    if final_message:
        filled_latex = filled_latex.replace("[Final Message]", final_message)
    if slogan:
        filled_latex = filled_latex.replace("Slogan to invite", slogan)

    # Compile to PDF
    compiler = LaTeXCompiler(compiler="pdflatex")
    pdf_path = compiler.compile(filled_latex, output_path, working_dir=template_dir, runs=2)

    return pdf_path
