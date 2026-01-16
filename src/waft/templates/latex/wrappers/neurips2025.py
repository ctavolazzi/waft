"""
NeurIPS 2025 LaTeX Template Wrapper
====================================

Python wrapper for XuehaiPan NeurIPS 2025 template.
Auto-discovered by LaTeXTemplateRegistry.
"""

from pathlib import Path
from jinja2 import Template
from ..compiler import LaTeXCompiler
from ..content_builders import build_neurips2025_content


def generate_neurips2025(
    title: str,
    content: str,
    output_path: Path,
    authors: str = "",
    abstract: str = "",
    track: str = "default",
    **kwargs
) -> Path:
    """
    Generate PDF using NeurIPS 2025 LaTeX template.
    
    Args:
        title: Paper title
        content: Main content (markdown or HTML)
        output_path: Where to save PDF
        authors: Author names (LaTeX formatted)
        abstract: Abstract text
        track: Track option (default, main, position, dandb, creativeai, etc.)
        **kwargs: Additional template parameters
        
    Returns:
        Path to generated PDF
    """
    # Get template path
    template_dir = Path(__file__).parent.parent / "templates" / "xuehai" / "NeurIPS2025"
    template_file = template_dir / "neurips_2025.tex"
    
    if not template_file.exists():
        raise FileNotFoundError(f"NeurIPS 2025 template not found: {template_file}")
    
    # Load template
    template_content = template_file.read_text(encoding="utf-8")
    
    # Build LaTeX content
    latex_content = build_neurips2025_content(
        title=title,
        content=content,
        authors=authors,
        abstract=abstract,
        **kwargs
    )
    
    # Create Jinja2 template from LaTeX template
    jinja_template = Template(template_content)
    
    # Fill template variables
    filled_latex = jinja_template.render(
        title=title,
        authors=authors,
        abstract=abstract,
        track=track,
        content=latex_content,
        **kwargs
    )
    
    # Compile to PDF
    compiler = LaTeXCompiler(compiler="xelatex")  # NeurIPS template uses xelatex
    pdf_path = compiler.compile(
        filled_latex,
        output_path,
        working_dir=template_dir,
        runs=2
    )
    
    return pdf_path
