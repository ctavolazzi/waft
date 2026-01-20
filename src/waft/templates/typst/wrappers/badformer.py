"""
Badformer Typst Template Wrapper
==================================

Python wrapper for Badformer Typst template.
Retro-inspired wireframing platformer game playable in Typst editor.

Category: game
Tags: [typst, game, interactive, platformer]
Source: typst-templates
"""

from pathlib import Path
from typing import Optional
from ..compiler import TypstCompiler


def generate_badformer(
    content: str,
    output_path: Path,
    **kwargs
) -> Path:
    """
    Generate PDF using Badformer Typst template (interactive game).
    
    Note: This is an interactive game template. Best viewed with typst watch.
    
    Args:
        content: Game input content (typically read from a file)
        output_path: Where to save PDF
        **kwargs: Additional template parameters
        
    Returns:
        Path to generated PDF
    """
    # Build Typst content
    typst_content = f'''#import "@preview/badformer:0.1.0": game
#show: game(read("main.typ"))

{content}
'''
    
    # Compile to PDF
    compiler = TypstCompiler()
    pdf_path = compiler.compile(typst_content, output_path)
    
    return pdf_path
