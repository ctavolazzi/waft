"""
Essay LaTeX Template Wrapper
============================

Python wrapper for XuehaiPan Essay template.
Auto-discovered by LaTeXTemplateRegistry.
"""

from pathlib import Path
from jinja2 import Template
from ..compiler import LaTeXCompiler
from ..content_builders import build_essay_content


def generate_essay(
    title: str,
    content: str,
    output_path: Path,
    author: str = "Author",
    institution: str = "",
    date: str = "",
    abstract: str = "",
    keywords: str = "",
    **kwargs
) -> Path:
    """
    Generate PDF using Essay LaTeX template.
    
    Args:
        title: Essay title
        content: Main content (markdown or HTML)
        output_path: Where to save PDF
        author: Author name
        institution: Institution name
        date: Date (defaults to \today)
        abstract: Abstract text
        keywords: Keywords (comma-separated)
        **kwargs: Additional template parameters
        
    Returns:
        Path to generated PDF
    """
    # Get template path
    template_dir = Path(__file__).parent.parent / "templates" / "xuehai" / "Essay"
    template_file = template_dir / "main.tex"
    
    if not template_file.exists():
        raise FileNotFoundError(f"Essay template not found: {template_file}")
    
    # Load template
    template_content = template_file.read_text(encoding="utf-8")
    
    # Build LaTeX content
    latex_content = build_essay_content(
        title=title,
        content=content,
        author=author,
        **kwargs
    )
    
    # Create Jinja2 template from LaTeX template
    jinja_template = Template(template_content)
    
    # Fill template variables
    filled_latex = jinja_template.render(
        title=title,
        author=author,
        institution=institution,
        date=date or r"\today",
        abstract=abstract,
        keywords=keywords,
        content=latex_content,
        **kwargs
    )
    
    # Compile to PDF
    compiler = LaTeXCompiler(compiler="xelatex")  # Essay template uses xelatex
    pdf_path = compiler.compile(
        filled_latex,
        output_path,
        working_dir=template_dir,
        runs=2
    )
    
    return pdf_path
