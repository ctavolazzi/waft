"""
Unequivocal AMS Typst Template Wrapper
=======================================

Python wrapper for Unequivocal AMS Typst template.
Single-column paper template for American Mathematical Society with theorem and proof functions.

Category: paper
Tags: [typst, academic, ams, mathematics, paper, theorem]
Source: typst-templates
"""

from pathlib import Path
from typing import Optional, List, Dict
from ..compiler import TypstCompiler


def generate_unequivocal_ams(
    title: str,
    content: str,
    output_path: Path,
    authors: List[Dict[str, Optional[str]]],
    abstract: Optional[str] = None,
    paper_size: str = "us-letter",
    bibliography: Optional[str] = None,
    **kwargs
) -> Path:
    """
    Generate PDF using Unequivocal AMS Typst template.
    
    Args:
        title: Paper title
        content: Main content (Typst markup)
        output_path: Where to save PDF
        authors: List of author dictionaries with keys:
            - name: Author name (required)
            - department: Department (optional)
            - organization: Organization (optional)
            - location: Location (optional)
            - email: Email (optional)
            - url: URL (optional)
        abstract: Abstract text (optional)
        paper_size: Paper size string (default: "us-letter")
        bibliography: Path to bibliography file (.bib) (optional)
        **kwargs: Additional template parameters
        
    Returns:
        Path to generated PDF
    """
    # Format authors
    authors_list = []
    for author in authors:
        author_dict = {}
        if "name" in author:
            author_dict["name"] = f'"{author["name"]}"'
        if "department" in author and author["department"]:
            author_dict["department"] = f'[{author["department"]}]'
        if "organization" in author and author["organization"]:
            author_dict["organization"] = f'[{author["organization"]}]'
        if "location" in author and author["location"]:
            author_dict["location"] = f'[{author["location"]}]'
        if "email" in author and author["email"]:
            author_dict["email"] = f'"{author["email"]}"'
        if "url" in author and author["url"]:
            author_dict["url"] = f'"{author["url"]}"'
        
        author_str = ", ".join(f"{k}: {v}" for k, v in author_dict.items())
        authors_list.append(f"({author_str})")
    
    authors_str = "(\n    " + ",\n    ".join(authors_list) + ",\n  )"
    
    # Format abstract
    abstract_str = f"lorem(100)" if abstract is None else f"[{abstract}]"
    
    # Format bibliography
    bibliography_str = f'bibliography("{bibliography}")' if bibliography else "none"
    
    # Build Typst content
    typst_content = f'''#import "@preview/unequivocal-ams:0.1.2": ams-article, theorem, proof

#show: ams-article.with(
  title: [{title}],
  authors: {authors_str},
  abstract: {abstract_str},
  paper-size: "{paper_size}",
  bibliography: {bibliography_str},
)

{content}
'''
    
    # Compile to PDF
    compiler = TypstCompiler()
    pdf_path = compiler.compile(typst_content, output_path)
    
    return pdf_path
