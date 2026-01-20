"""
Cereal Words Typst Template Wrapper
====================================

Python wrapper for Cereal Words Typst template.
Word puzzle game where you find hidden words in jumbled letters.

Category: game
Tags: [typst, game, interactive, puzzle, word]
Source: typst-templates
"""

from pathlib import Path

from ..compiler import TypstCompiler


def generate_cereal_words(content: str, output_path: Path, **kwargs) -> Path:
    """
    Generate PDF using Cereal Words Typst template (interactive word puzzle game).

    Note: This is an interactive game template. Best viewed with typst watch.

    Args:
        content: Game input content (words to find)
        output_path: Where to save PDF
        **kwargs: Additional template parameters

    Returns:
        Path to generated PDF
    """
    # Build Typst content
    typst_content = f"""#import "@preview/cereal-words:0.1.0": game
#show: game

{content}
"""

    # Compile to PDF
    compiler = TypstCompiler()
    pdf_path = compiler.compile(typst_content, output_path)

    return pdf_path
