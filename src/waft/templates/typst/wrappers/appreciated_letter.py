"""
Appreciated Letter Typst Template Wrapper
==========================================

Python wrapper for Appreciated Letter Typst template.
A basic letter with sender and recipient address, ready for DIN DL windowed envelope.

Category: letter
Tags: [typst, letter, business, personal]
Source: typst-templates
"""

from pathlib import Path

from ..compiler import TypstCompiler


def generate_appreciated_letter(
    content: str,
    output_path: Path,
    sender: str | None = None,
    recipient: str | None = None,
    date: str | None = None,
    subject: str | None = None,
    name: str | None = None,
    **kwargs,
) -> Path:
    """
    Generate PDF using Appreciated Letter Typst template.

    Args:
        content: Letter body content (Typst markup)
        output_path: Where to save PDF
        sender: Sender address (displayed at top)
        recipient: Recipient address (displayed near top)
        date: Date and possibly place (flushed right after address)
        subject: Subject line for the letter
        name: Name the letter closes with
        **kwargs: Additional template parameters

    Returns:
        Path to generated PDF
    """
    # Format parameters
    sender_str = f"[{sender}]" if sender else "none"
    recipient_str = f"[{recipient}]" if recipient else "none"
    date_str = f"[{date}]" if date else "none"
    subject_str = f"[{subject}]" if subject else "none"
    name_str = f"[{name}]" if name else "none"

    # Build Typst content
    typst_content = f"""#import "@preview/appreciated-letter:0.1.0": letter

#show: letter.with(
  sender: {sender_str},
  recipient: {recipient_str},
  date: {date_str},
  subject: {subject_str},
  name: {name_str},
)

{content}
"""

    # Compile to PDF
    compiler = TypstCompiler()
    pdf_path = compiler.compile(typst_content, output_path)

    return pdf_path
