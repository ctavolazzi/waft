"""
Flow-Way Typst Template Wrapper
================================

Python wrapper for Flow-Way Typst template.
A simple Typst template for creating modern documents, reports and notes with a clean design.

Category: report
Tags: [typst, modern, clean, report, notes]
Source: flow-way
"""

from pathlib import Path
from typing import Optional, Union, List
from ..compiler import TypstCompiler


def generate_flow_way(
    title: str,
    content: str,
    output_path: Path,
    subtitle: Optional[str] = None,
    authors: Union[str, List[str], None] = None,
    affiliation: Optional[str] = None,
    year: Optional[int] = None,
    logo: Optional[str] = None,
    lang: str = "en",
    toc: bool = False,
    toc_depth: Optional[int] = None,
    breaks: bool = False,
    main_color: str = "003F88",
    alpha: Union[int, float] = 60,
    **kwargs
) -> Path:
    """
    Generate PDF using Flow-Way Typst template.
    
    Args:
        title: Document title
        content: Main content (Typst markup)
        output_path: Where to save PDF
        subtitle: Optional subtitle
        authors: Author name(s) - can be string, list of strings, or None
        affiliation: Author affiliation
        year: Document year
        logo: Path to logo image file
        lang: Document language (default: "en")
        toc: Whether to include table of contents (default: False)
        toc_depth: Depth of table of contents (default: None)
        breaks: Whether to insert page breaks before top-level headings (default: False)
        main_color: Main color in hex format without # (default: "003F88")
        alpha: Alpha transparency for secondary elements, 0-100 (default: 60)
        **kwargs: Additional template parameters
        
    Returns:
        Path to generated PDF
    """
    # Get template directory
    template_dir = Path(__file__).parent.parent / "templates" / "flow-way"
    lib_path = template_dir / "src" / "lib.typ"
    
    if not lib_path.exists():
        raise FileNotFoundError(f"Flow-Way template not found: {lib_path}")
    
    # Format authors
    authors_str = ""
    if authors:
        if isinstance(authors, str):
            authors_str = f'"{authors}"'
        elif isinstance(authors, list):
            authors_list = ", ".join(f'"{a}"' for a in authors)
            authors_str = f"({authors_list})"
    
    # Format subtitle
    subtitle_str = f'"{subtitle}"' if subtitle else "none"
    
    # Format affiliation
    affiliation_str = f'"{affiliation}"' if affiliation else "none"
    
    # Format year
    year_str = str(year) if year else "none"
    
    # Format logo
    logo_str = f'image("{logo}")' if logo else "none"
    
    # Format toc_depth
    toc_depth_str = str(toc_depth) if toc_depth else "none"
    
    # Format alpha (convert to percentage if needed)
    if isinstance(alpha, float) and alpha <= 1.0:
        alpha_str = f"{int(alpha * 100)}%"
    elif isinstance(alpha, int):
        alpha_str = f"{alpha}%"
    else:
        alpha_str = f"{alpha}%"
    
    # Build Typst content
    # Use relative path from working directory
    lib_relative = Path("src") / "lib.typ"
    
    typst_content = f'''#import "{lib_relative.as_posix()}": *

#show: flow.with(
  title: "{title}",
  subtitle: {subtitle_str},
  authors: {authors_str if authors_str else "()"},
  affiliation: {affiliation_str},
  year: {year_str},
  logo: {logo_str},
  lang: "{lang}",
  toc: {str(toc).lower()},
  toc-depth: {toc_depth_str},
  breaks: {str(breaks).lower()},
  main-color: "{main_color}",
  alpha: {alpha_str}
)

{content}
'''
    
    # Compile to PDF
    # Use template dir as working dir so fonts and assets are accessible
    compiler = TypstCompiler()
    pdf_path = compiler.compile(
        typst_content,
        output_path,
        working_dir=template_dir
    )
    
    return pdf_path
