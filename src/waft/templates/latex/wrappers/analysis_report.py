"""
Analysis Report LaTeX Template Wrapper
=====================================

Python wrapper for analysis report template using analysis_orax package.
Auto-discovered by LaTeXTemplateRegistry.

category: report
tags: [latex, pdf, analysis, report, orange]
source: waft
"""

from pathlib import Path
from ..compiler import LaTeXCompiler
from ..content_builders import build_report_content


def generate_analysis_report(
    title: str,
    content: str,
    output_path: Path,
    author: str = "Author",
    date: str = None,
    abstract: str = "",
    sections: list = None,
    figures_dir: Path = None,
    **kwargs
) -> Path:
    """
    Generate PDF using Analysis Report LaTeX template with analysis_orax package.

    Args:
        title: Document title
        content: Main content (markdown or HTML)
        output_path: Where to save PDF
        author: Author name
        date: Date string (defaults to \today if None)
        abstract: Abstract content (optional)
        sections: List of section dictionaries with 'title' and 'content' keys (optional)
        figures_dir: Directory containing figures (defaults to figures/ relative to output)
        **kwargs: Additional template parameters

    Returns:
        Path to generated PDF
    """
    # Get paths
    project_root = Path(__file__).parent.parent.parent.parent.parent.parent
    package_dir = project_root / "lib" / "analysis_orax"
    package_file = package_dir / "analysis_orax.sty"

    if not package_file.exists():
        raise FileNotFoundError(f"analysis_orax package not found: {package_file}")

    # Set up figures directory
    if figures_dir is None:
        figures_dir = output_path.parent / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    # Build LaTeX content from markdown/HTML
    latex_content = build_report_content(
        title=title,
        content=content,
        author=author,
        **kwargs
    )

    # Build complete LaTeX document
    date_str = date if date else r"\today"
    
    # Template structure
    latex_doc = f"""\\documentclass{{article}}

% ============================================================================
% Package Imports
% ============================================================================

% Encoding and Fonts
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{microtype}}

% Layout and Geometry
\\usepackage[a4paper]{{geometry}}

% Graphics and Figures
\\usepackage{{graphicx}}
\\graphicspath{{{{figures/}}{{images/}}{{./}}}}

% Colors and Styling
\\usepackage[dvipsnames]{{xcolor}}
\\usepackage{{analysis_orax}}

% Hyperlinks and References
\\usepackage[colorlinks=true, linkcolor=analysisorange, urlcolor=analysisorange, citecolor=analysisdarkorange]{{hyperref}}
\\usepackage{{cleveref}}

% ============================================================================
% Document Metadata
% ============================================================================

\\title{{{title}}}
\\author{{{author}}}
\\date{{{date_str}}}

% ============================================================================
% Document Content
% ============================================================================

\\begin{{document}}

\\maketitle
"""

    # Add abstract if provided
    if abstract:
        latex_doc += f"""
\\begin{{abstract}}
{abstract}
\\end{{abstract}}

"""

    # Add main content
    latex_doc += f"""
{latex_content}
"""

    # Add sections if provided
    if sections:
        for section in sections:
            section_title = section.get('title', 'Section')
            section_content = section.get('content', '')
            latex_doc += f"""
\\section{{{section_title}}}

{section_content}
"""

    # Close document
    latex_doc += """
\\end{document}
"""

    # Create temporary working directory
    working_dir = output_path.parent / f".latex_work_{output_path.stem}"
    working_dir.mkdir(exist_ok=True)

    # Copy package to working directory (so LaTeX can find it)
    import shutil
    work_package_dir = working_dir / "lib" / "analysis_orax"
    work_package_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(package_file, work_package_dir / "analysis_orax.sty")

    # Create symlink or copy figures directory
    work_figures_dir = working_dir / "figures"
    if figures_dir.exists() and figures_dir.is_dir():
        if work_figures_dir.exists():
            work_figures_dir.unlink()
        work_figures_dir.symlink_to(figures_dir)

    # Write LaTeX file to working directory
    latex_file = working_dir / f"{output_path.stem}.tex"
    latex_file.write_text(latex_doc, encoding="utf-8")

    # Compile to PDF
    compiler = LaTeXCompiler(compiler="pdflatex")
    
    # Set TEXINPUTS to include package directory
    import os
    original_texinputs = os.environ.get("TEXINPUTS", "")
    package_path = str(package_dir.parent.absolute())
    os.environ["TEXINPUTS"] = f"{package_path}//:{original_texinputs}"
    
    try:
        pdf_path = compiler.compile(
            latex_doc,
            output_path,
            working_dir=working_dir,
            runs=2
        )
    finally:
        # Restore TEXINPUTS
        os.environ["TEXINPUTS"] = original_texinputs

    # Clean up working directory (optional - keep for debugging)
    # shutil.rmtree(working_dir, ignore_errors=True)

    return pdf_path
