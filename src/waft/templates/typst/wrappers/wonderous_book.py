"""
Wonderous Book Typst Template Wrapper
======================================

Python wrapper for Wonderous Book Typst template.
Book template for fiction with title page, table of contents, and chapter template.

Category: book
Tags: [typst, book, fiction, novel]
Source: typst-templates
"""

from pathlib import Path
from typing import Optional, Union, List
from ..compiler import TypstCompiler


def generate_wonderous_book(
    title: str,
    content: str,
    output_path: Path,
    author: Union[str, List[str]],
    paper_size: str = "iso-b5",
    dedication: Optional[str] = None,
    publishing_info: Optional[str] = None,
    **kwargs
) -> Path:
    """
    Generate PDF using Wonderous Book Typst template.
    
    Args:
        title: Book title
        content: Main content (Typst markup)
        output_path: Where to save PDF
        author: Author name(s) - can be string or list of strings
        paper_size: Paper size string (default: "iso-b5")
        dedication: Dedication text (optional)
        publishing_info: Publishing information (optional)
        **kwargs: Additional template parameters
        
    Returns:
        Path to generated PDF
    """
    # Format author
    if isinstance(author, str):
        author_str = f'"{author}"'
    elif isinstance(author, list):
        authors_list = ", ".join(f'"{a}"' for a in author)
        author_str = f"({authors_list})"
    else:
        author_str = '"Author"'
    
    # Format dedication
    dedication_str = f"[{dedication}]" if dedication else "none"
    
    # Format publishing info
    publishing_info_str = f"[{publishing_info}]" if publishing_info else "none"
    
    # Build Typst content
    typst_content = f'''#import "@preview/wonderous-book:0.1.2": book

#show: book.with(
  title: [{title}],
  author: {author_str},
  paper-size: "{paper_size}",
  dedication: {dedication_str},
  publishing-info: {publishing_info_str},
)

{content}
'''
    
    # Compile to PDF
    compiler = TypstCompiler()
    pdf_path = compiler.compile(typst_content, output_path)
    
    return pdf_path
