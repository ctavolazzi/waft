"""
Icicle Typst Template Wrapper
==============================

Python wrapper for Icicle Typst template.
Christmas-themed puzzle game where you navigate Typst Guys to reach the helicopter pad.

Category: game
Tags: [typst, game, interactive, puzzle, christmas]
Source: typst-templates
"""

from pathlib import Path

from ..compiler import TypstCompiler


def generate_icicle(
    content: str, output_path: Path, levels: list[str] | None = None, **kwargs
) -> Path:
    """
    Generate PDF using Icicle Typst template (interactive puzzle game).

    Note: This is an interactive game template. Best viewed with typst watch.
    Move with WASD keys.

    Args:
        content: Game input content
        output_path: Where to save PDF
        levels: Optional list of level definition strings (optional)
        **kwargs: Additional template parameters

    Returns:
        Path to generated PDF
    """
    # Format levels if provided
    levels_str = ""
    if levels:
        # Levels would need to be formatted as Typst array
        # For now, we'll just include them in content
        pass

    # Build Typst content
    typst_content = f"""#import "@preview/icicle:0.1.0": game
#show: game

{content}
"""

    # Compile to PDF
    compiler = TypstCompiler()
    pdf_path = compiler.compile(typst_content, output_path)

    return pdf_path
