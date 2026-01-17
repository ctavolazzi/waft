"""
Unicamp Physics Report LaTeX Template Wrapper
=============================================

Python wrapper for Unicamp Physics Experimental IV lab report template.
Brazilian Portuguese academic report template from Instituto de Física Gleb Wataghin.

Category: report
Tags: [latex, pdf, academic, brazilian, portuguese, physics, lab-report, unicamp]
Source: unicamp-physics-report
"""

from pathlib import Path
from typing import Optional, List, Dict, Any
from jinja2 import Template
from ..compiler import LaTeXCompiler
from ..content_builders import markdown_to_latex


def generate_unicamp_report(
    title: str,
    content: str,
    output_path: Path,
    professor: str = "Prof. Dr. Flávio Caldas da Cruz",
    authors: Optional[List[str]] = None,
    course: str = "Física Experimental IV",
    institution: str = "Instituto de Física Gleb Wataghin, Unicamp",
    abstract: str = "",
    introduction: str = "",
    methodology: str = "",
    results: str = "",
    discussion: str = "",
    conclusion: str = "",
    figures: Optional[List[Dict[str, Any]]] = None,
    tables: Optional[List[Dict[str, Any]]] = None,
    bibliography: Optional[str] = None,
    **kwargs
) -> Path:
    """
    Generate PDF using Unicamp Physics Report LaTeX template.
    
    Args:
        title: Report title (e.g., "Relatório I")
        content: Main content (markdown or HTML) - used if sections not provided
        output_path: Where to save PDF
        professor: Professor name
        authors: List of author names with student IDs (e.g., ["Caroline Guimarães 155006"])
        course: Course name
        institution: Institution name
        abstract: Abstract text
        introduction: Introduction section content
        methodology: Methodology section content
        results: Results section content
        discussion: Discussion section content
        conclusion: Conclusion section content
        figures: List of figure dicts with keys: path, caption, label, width
        tables: List of table dicts with keys: format, content, caption, label
        bibliography: Bibliography file name (without .bib extension)
        **kwargs: Additional template parameters
        
    Returns:
        Path to generated PDF
        
    Example:
        >>> from pathlib import Path
        >>> generate_unicamp_report(
        ...     title="Relatório I",
        ...     content="# Introduction\\n\\nThis is the report...",
        ...     output_path=Path("report.pdf"),
        ...     authors=["Student Name 123456"],
        ...     abstract="This report presents..."
        ... )
    """
    # Get template path (from project root)
    project_root = Path(__file__).parent.parent.parent.parent.parent
    template_dir = project_root / "templates" / "unicamp-physics-report"
    template_file = template_dir / "main.tex"
    
    if not template_file.exists():
        raise FileNotFoundError(f"Unicamp report template not found: {template_file}")
    
    # Load template
    template_content = template_file.read_text(encoding="utf-8")
    
    # Default authors if not provided
    if authors is None:
        authors = ["Author Name StudentID"]
    
    # Format authors for LaTeX
    authors_latex = "\\\\\n".join(authors)
    
    # Convert content sections to LaTeX if provided as markdown
    def convert_section(text: str) -> str:
        if not text:
            return ""
        # Check if already LaTeX or markdown
        if text.strip().startswith("\\"):
            return text  # Already LaTeX
        return markdown_to_latex(text)
    
    # Use provided sections or convert content
    introduction_latex = convert_section(introduction) if introduction else convert_section(content)
    methodology_latex = convert_section(methodology)
    results_latex = convert_section(results)
    discussion_latex = convert_section(discussion)
    conclusion_latex = convert_section(conclusion)
    
    # Convert abstract
    abstract_latex = convert_section(abstract) if abstract else ""
    
    # Create Jinja2 template from LaTeX template
    jinja_template = Template(template_content)
    
    # Fill template variables
    filled_latex = jinja_template.render(
        title=title,
        course=course,
        institution=institution,
        professor=professor,
        authors=authors_latex,
        abstract=abstract_latex,
        introduction=introduction_latex,
        methodology=methodology_latex,
        results=results_latex,
        discussion=discussion_latex,
        conclusion=conclusion_latex,
        figures=figures or [],
        tables=tables or [],
        bibliography=bibliography,
        **kwargs
    )
    
    # Compile to PDF
    compiler = LaTeXCompiler(compiler="pdflatex")
    pdf_path = compiler.compile(
        filled_latex,
        output_path,
        working_dir=template_dir,
        runs=2
    )
    
    return pdf_path
