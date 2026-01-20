"""
Presentation LaTeX Template Wrapper
===================================

Python wrapper for XuehaiPan Presentation template.
Auto-discovered by LaTeXTemplateRegistry.
"""

from pathlib import Path

from jinja2 import Template

from ..compiler import LaTeXCompiler
from ..content_builders import build_presentation_content


def generate_presentation(
    title: str,
    content: str,
    output_path: Path,
    author: str = "Author",
    subtitle: str = "",
    institute: str = "",
    date: str = "",
    subject: str = "",
    **kwargs,
) -> Path:
    """
    Generate PDF using Presentation LaTeX template.

    Args:
        title: Presentation title
        content: Main content (markdown or HTML) - will be split into slides
        output_path: Where to save PDF
        author: Author name
        subtitle: Optional subtitle
        institute: Institute name
        date: Date
        subject: Subject/topic
        **kwargs: Additional template parameters

    Returns:
        Path to generated PDF
    """
    # Get template path
    template_dir = Path(__file__).parent.parent / "templates" / "xuehai" / "Presentation"
    template_file = template_dir / "main.tex"

    if not template_file.exists():
        raise FileNotFoundError(f"Presentation template not found: {template_file}")

    # Load template
    template_content = template_file.read_text(encoding="utf-8")

    # Build LaTeX content
    latex_content = build_presentation_content(
        title=title, content=content, author=author, **kwargs
    )

    # Create Jinja2 template from LaTeX template
    jinja_template = Template(template_content)

    # Fill template variables
    filled_latex = jinja_template.render(
        title=title,
        subtitle=subtitle,
        author=author,
        institute=institute,
        date=date or r"\today",
        subject=subject,
        content=latex_content,
        **kwargs,
    )

    # Compile to PDF
    compiler = LaTeXCompiler(compiler="xelatex")  # Presentation template uses xelatex
    pdf_path = compiler.compile(filled_latex, output_path, working_dir=template_dir, runs=2)

    return pdf_path
