"""
Charged IEEE Typst Template Wrapper
====================================

Python wrapper for Charged IEEE Typst template.
Two-column paper template for IEEE proceedings with tight spacing and numeric citations.

Category: paper
Tags: [typst, academic, ieee, conference, paper]
Source: typst-templates
"""

from pathlib import Path

from ..compiler import TypstCompiler


def generate_charged_ieee(
    title: str,
    content: str,
    output_path: Path,
    authors: list[dict[str, str | None]],
    abstract: str | None = None,
    index_terms: list[str] | None = None,
    paper_size: str = "us-letter",
    bibliography: str | None = None,
    figure_supplement: str = "Fig.",
    **kwargs,
) -> Path:
    """
    Generate PDF using Charged IEEE Typst template.

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
        abstract: Abstract text (optional)
        index_terms: List of index terms (optional)
        paper_size: Paper size string (default: "us-letter")
        bibliography: Path to bibliography file (.bib) (optional)
        figure_supplement: How figures are referred to (default: "Fig.")
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
            author_dict["department"] = f"[{author['department']}]"
        if "organization" in author and author["organization"]:
            author_dict["organization"] = f"[{author['organization']}]"
        if "location" in author and author["location"]:
            author_dict["location"] = f"[{author['location']}]"
        if "email" in author and author["email"]:
            author_dict["email"] = f'"{author["email"]}"'

        author_str = ", ".join(f"{k}: {v}" for k, v in author_dict.items())
        authors_list.append(f"({author_str})")

    authors_str = "(\n    " + ",\n    ".join(authors_list) + ",\n  )"

    # Format abstract
    abstract_str = f"[{abstract}]" if abstract else "none"

    # Format index terms
    index_terms_str = "()"
    if index_terms:
        terms_list = ", ".join(f'"{term}"' for term in index_terms)
        index_terms_str = f"({terms_list})"

    # Format bibliography
    bibliography_str = f'bibliography("{bibliography}")' if bibliography else "none"

    # Build Typst content
    typst_content = f'''#import "@preview/charged-ieee:0.1.4": ieee

#show: ieee.with(
  title: [{title}],
  authors: {authors_str},
  abstract: {abstract_str},
  index-terms: {index_terms_str},
  paper-size: "{paper_size}",
  bibliography: {bibliography_str},
  figure-supplement: [{figure_supplement}],
)

{content}
'''

    # Compile to PDF
    compiler = TypstCompiler()
    pdf_path = compiler.compile(typst_content, output_path)

    return pdf_path
