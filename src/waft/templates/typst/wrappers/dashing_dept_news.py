"""
Dashing Dept News Typst Template Wrapper
=========================================

Python wrapper for Dashing Dept News Typst template.
Newsletter layout for departmental news with hero image, main column, and sidebar.

Category: newsletter
Tags: [typst, newsletter, department, news]
Source: typst-templates
"""

from pathlib import Path
from typing import Optional, Dict
from ..compiler import TypstCompiler


def generate_dashing_dept_news(
    title: str,
    content: str,
    output_path: Path,
    edition: Optional[str] = None,
    hero_image: Optional[Dict[str, str]] = None,
    publication_info: Optional[str] = None,
    **kwargs
) -> Path:
    """
    Generate PDF using Dashing Dept News Typst template.
    
    Args:
        title: Newsletter title
        content: Main content (Typst markup)
        output_path: Where to save PDF
        edition: Edition information (optional)
        hero_image: Dictionary with 'image' and 'caption' keys (optional)
        publication_info: Publication information (optional)
        **kwargs: Additional template parameters
        
    Returns:
        Path to generated PDF
    """
    # Format edition
    edition_str = f"[{edition}]" if edition else "none"
    
    # Format hero image
    hero_image_str = "none"
    if hero_image:
        image_path = hero_image.get("image", "")
        caption = hero_image.get("caption", "")
        hero_image_str = f'(\n    image: image("{image_path}"),\n    caption: [{caption}],\n  )'
    
    # Format publication info
    publication_info_str = f"[{publication_info}]" if publication_info else "none"
    
    # Build Typst content
    typst_content = f'''#import "@preview/dashing-dept-news:0.1.1": newsletter, article

#show: newsletter.with(
  title: [{title}],
  edition: {edition_str},
  hero-image: {hero_image_str},
  publication-info: {publication_info_str},
)

{content}
'''
    
    # Compile to PDF
    compiler = TypstCompiler()
    pdf_path = compiler.compile(typst_content, output_path)
    
    return pdf_path
