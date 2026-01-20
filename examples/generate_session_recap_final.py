#!/usr/bin/env python3
"""
Generate Session Recap PDF - Final Simple Version

Using the new composable PDF generator.
Before: ~600 lines of boilerplate
After: ~10 lines of code
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution.pdf_generator import generate_pdf


def get_session_content() -> str:
    """Get comprehensive session content."""
    from examples.generate_session_recap_pdf_waft import get_session_content

    return get_session_content()


def main():
    """Generate PDF - super simple now!"""

    # That's it! One function call.
    generate_pdf(
        content=get_session_content(),
        title="WAFT v0.5.3 MVP: Karma Economy & Source Consciousness",
        style="clinical_standard",  # or "premium" or "professional"
        open_pdf=True,
    )

    print("✅ Done! PDF generated and opened.")


if __name__ == "__main__":
    sys.exit(main())
