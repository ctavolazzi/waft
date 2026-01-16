"""
Assignment LaTeX Template Wrapper
==================================

Python wrapper for XuehaiPan Assignment template.
Auto-discovered by LaTeXTemplateRegistry.
"""

from pathlib import Path
from jinja2 import Template
from ..compiler import LaTeXCompiler
from ..content_builders import build_assignment_content


def generate_assignment(
    title: str,
    content: str,
    output_path: Path,
    author: str = "Author",
    student_id: str = "",
    course: str = "",
    lecturer: str = "",
    institute: str = "",
    date: str = "",
    **kwargs
) -> Path:
    """
    Generate PDF using Assignment LaTeX template.
    
    Args:
        title: Assignment title
        content: Main content (markdown or HTML)
        output_path: Where to save PDF
        author: Student name
        student_id: Student ID
        course: Course name
        lecturer: Lecturer name
        institute: Institute/school name
        date: Due date
        **kwargs: Additional template parameters
        
    Returns:
        Path to generated PDF
    """
    # Get template path
    template_dir = Path(__file__).parent.parent / "templates" / "xuehai" / "Assignment"
    template_file = template_dir / "main.tex"
    
    if not template_file.exists():
        raise FileNotFoundError(f"Assignment template not found: {template_file}")
    
    # Load template
    template_content = template_file.read_text(encoding="utf-8")
    
    # Build LaTeX content
    latex_content = build_assignment_content(
        title=title,
        content=content,
        author=author,
        course=course,
        date=date,
        **kwargs
    )
    
    # Create Jinja2 template from LaTeX template
    # Replace the content section with our content
    jinja_template = Template(template_content)
    
    # Fill template variables
    filled_latex = jinja_template.render(
        title=title,
        author=author,
        studentid=student_id,
        course=course,
        lecturer=lecturer,
        institute=institute,
        date=date or r"\today",
        content=latex_content,
        **kwargs
    )
    
    # Compile to PDF
    compiler = LaTeXCompiler(compiler="xelatex")  # Assignment template uses xelatex
    pdf_path = compiler.compile(
        filled_latex,
        output_path,
        working_dir=template_dir,
        runs=2
    )
    
    return pdf_path
