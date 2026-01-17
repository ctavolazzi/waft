"""
Example usage of the Formal Letter LaTeX template.

This demonstrates how to generate a formal WAFT letter PDF.
"""

from pathlib import Path
from src.waft.templates.latex.wrappers.formal_letter import generate_formal_letter

# Example 1: Basic letter
output_path = Path("example_letter.pdf")

generate_formal_letter(
    title="Formal Letter Example",
    content="""
This is an example of a formal business letter generated using the WAFT LaTeX template.

The template supports:
- Professional letterhead
- Complete recipient and sender information
- Subject lines
- Signature blocks
- Enclosures and CC notation

The letter body can contain **bold text** and *italic text* using markdown syntax.
""",
    output_path=output_path,
    date="January 16, 2026",
    sender_name="Dr. Jane Smith",
    sender_title="Lead Developer",
    sender_organization="WAFT Framework",
    sender_email="jane.smith@waft.dev",
    recipient_name="John Doe",
    recipient_title="Project Manager",
    recipient_organization="Example Corporation",
    subject="Re: WAFT Framework Integration",
    salutation="Dear John,",
    closing="Best regards",
    signature_name="Dr. Jane Smith",
    signature_title="Lead Developer",
    signature_organization="WAFT Framework",
    signature_email="jane.smith@waft.dev",
    letterhead="WAFT Framework",
    enclosures="Project Proposal, Technical Specifications",
    cc="team@waft.dev"
)

print(f"✅ Letter generated: {output_path}")
