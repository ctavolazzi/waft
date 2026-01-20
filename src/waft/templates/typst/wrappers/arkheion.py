"""
Arkheion Typst Template Wrapper
================================

Python wrapper for Arkheion Typst template.
A Typst template inspired by arXiv style documents for academic papers.

Category: preprint
Tags: [typst, academic, arxiv, preprint, paper]
Source: arkheion
"""

from pathlib import Path

from ..compiler import TypstCompiler


def generate_arkheion(
    title: str,
    content: str,
    output_path: Path,
    authors: list[dict[str, str | None]],
    abstract: str = "",
    keywords: list[str] | None = None,
    date: str | None = None,
    bibliography: str | None = None,
    include_appendices: bool = False,
    **kwargs,
) -> Path:
    """
    Generate PDF using Arkheion Typst template (arXiv-style).

    Args:
        title: Document title
        content: Main content (Typst markup)
        output_path: Where to save PDF
        authors: List of author dictionaries, each with:
            - name: Author name (required)
            - email: Email address (optional)
            - affiliation: Affiliation (optional)
            - orcid: ORCID ID (optional)
        abstract: Abstract text
        keywords: List of keywords (optional)
        date: Date string (optional, e.g., "May 16, 2023")
        bibliography: Path to bibliography file (.bib) (optional)
        include_appendices: Whether to include appendices section (default: False)
        **kwargs: Additional template parameters

    Returns:
        Path to generated PDF

    Example:
        generate_arkheion(
            title="My Paper Title",
            content="# Introduction\\n\\nContent here...",
            output_path=Path("paper.pdf"),
            authors=[
                {"name": "John Doe", "email": "john@example.com", "affiliation": "University"},
                {"name": "Jane Smith", "orcid": "0000-0000-0000-0000"}
            ],
            abstract="This is the abstract.",
            keywords=["machine learning", "typst"],
            date="January 19, 2026"
        )
    """
    # Format authors
    authors_list = []
    for author in authors:
        author_dict = {}
        if "name" in author:
            author_dict["name"] = f'"{author["name"]}"'
        if "email" in author and author["email"]:
            author_dict["email"] = f'"{author["email"]}"'
        if "affiliation" in author and author["affiliation"]:
            author_dict["affiliation"] = f'"{author["affiliation"]}"'
        if "orcid" in author and author["orcid"]:
            author_dict["orcid"] = f'"{author["orcid"]}"'

        # Format as dictionary string
        author_str = ", ".join(f"{k}: {v}" for k, v in author_dict.items())
        authors_list.append(f"({author_str})")

    authors_str = "(\n    " + ",\n    ".join(authors_list) + ",\n  )"

    # Format abstract
    abstract_str = f"[{abstract}]" if abstract else "lorem(55)"

    # Format keywords
    keywords_str = "none"
    if keywords:
        keywords_list = ", ".join(f'"{k}"' for k in keywords)
        keywords_str = f"({keywords_list})"

    # Format date
    date_str = f'"{date}"' if date else "none"

    # Build Typst content
    typst_content = f'''#import "@preview/arkheion:0.1.1": arkheion, arkheion-appendices

#show: arkheion.with(
  title: "{title}",
  authors: {authors_str},
  abstract: {abstract_str},
  keywords: {keywords_str},
  date: {date_str},
)
#set cite(style: "chicago-author-date")
#show link: underline

{content}
'''

    # Add bibliography if provided
    if bibliography:
        typst_content += f'\n#bibliography("{bibliography}")'

    # Add appendices if requested
    if include_appendices:
        typst_content += """

// Create appendix section
#show: arkheion-appendices
=
"""

    # Compile to PDF
    compiler = TypstCompiler()
    pdf_path = compiler.compile(typst_content, output_path)

    return pdf_path
