"""
Scientific Report Generator - The Clinical Standard

Generates clean, bureaucratic reports in the style of the Institute for Advanced
Ontological Studies. Clinical, detached, authoritative tone with academic typography.
"""

import json
from pathlib import Path

try:
    from fpdf import FPDF
except ImportError:
    raise ImportError("fpdf2 is required. Install with: pip install fpdf2>=2.7.0")


class ScientificReport(FPDF):
    """
    Clinical Standard PDF generator for Institute documentation.

    Features:
    - Clean sans-serif headers (Helvetica)
    - Academic serif body text (Times New Roman)
    - Metadata rail for subject information
    - Clean black bar redactions
    - Bureaucratic, detached tone
    """

    # Sensitive terms that should be redacted
    SENSITIVE_TERMS = ["Karma", "Construct", "Substrate", "Soul", "Reincarnation"]

    def __init__(self):
        """Initialize the scientific report generator."""
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(left=20, top=25, right=20)
        self.set_auto_page_break(auto=True, margin=20)
        self._redacted_terms: list[str] = []

    def add_redacted_term(self, term: str) -> None:
        """Add a term to the redaction list."""
        if term not in self._redacted_terms:
            self._redacted_terms.append(term)

    def _redact_text(self, text: str) -> str:
        """
        Replace sensitive terms with redaction markers.
        Returns text with [REDACTED] placeholders.
        """
        result = text
        all_terms = self.SENSITIVE_TERMS + self._redacted_terms

        for term in all_terms:
            # Case-insensitive replacement
            import re

            pattern = re.compile(re.escape(term), re.IGNORECASE)
            result = pattern.sub("[REDACTED]", result)

        return result

    def _draw_redaction_bar(self, x: float, y: float, width: float, height: float = 4.0) -> None:
        """Draw a clean black bar for redaction."""
        self.set_fill_color(0, 0, 0)
        self.rect(x, y, width, height, style="F")
        self.set_fill_color(255, 255, 255)  # Reset

    def _render_redacted_text(self, x: float, y: float, text: str, width: float) -> None:
        """
        Render text with redaction bars over sensitive terms.
        """
        # Check if text contains redaction markers
        if "[REDACTED]" in text:
            # Split by redaction markers
            parts = text.split("[REDACTED]")
            current_x = x

            for i, part in enumerate(parts):
                if part:
                    # Render normal text
                    self.set_font("Times", "", 11)
                    self.set_xy(current_x, y)
                    self.cell(0, 5, part, align="L")
                    current_x += self.get_string_width(part)

                # Draw redaction bar if not last part
                if i < len(parts) - 1:
                    redaction_width = min(30, width - (current_x - x))
                    self._draw_redaction_bar(current_x, y + 1, redaction_width)
                    current_x += redaction_width
        else:
            # Normal text rendering
            self.set_font("Times", "", 11)
            self.set_xy(x, y)
            self.multi_cell(width, 5, text, align="J")

    def add_header(self) -> None:
        """Add the Institute header to the current page."""
        # Header: Clean, bold, sans-serif
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 0, 0)
        self.set_xy(self.l_margin, self.t_margin - 15)
        self.cell(0, 10, "INSTITUTE FOR ADVANCED ONTOLOGICAL STUDIES", align="L", ln=1)

        # Subheader line
        self.set_line_width(0.5)
        self.set_draw_color(100, 100, 100)
        self.line(self.l_margin, self.t_margin - 5, self.w - self.r_margin, self.t_margin - 5)

    def add_metadata_rail(self, metadata: dict[str, str], y_start: float) -> float:
        """
        Add a metadata rail/header block for subject information.

        Args:
            metadata: Dictionary of key-value pairs to display
            y_start: Starting Y position

        Returns:
            Y position after the metadata block
        """
        # Background box for metadata
        box_height = len(metadata) * 7 + 10
        self.set_fill_color(245, 245, 245)  # Light gray background
        self.rect(
            self.l_margin, y_start, self.w - self.l_margin - self.r_margin, box_height, style="F"
        )

        # Border
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.5)
        self.rect(
            self.l_margin, y_start, self.w - self.l_margin - self.r_margin, box_height, style="D"
        )

        # Metadata content
        y = y_start + 7
        self.set_font("Helvetica", "B", 10)

        for key, value in metadata.items():
            # Key
            self.set_text_color(60, 60, 60)
            self.set_xy(self.l_margin + 5, y)
            self.cell(50, 5, f"{key}:", align="L")

            # Value (may be redacted)
            self.set_text_color(0, 0, 0)
            self.set_font("Helvetica", "", 10)
            value_x = self.l_margin + 60
            value_text = self._redact_text(str(value))

            if "[REDACTED]" in value_text:
                # Render with redaction bars
                self._render_redacted_text(
                    value_x, y, value_text, self.w - value_x - self.r_margin - 5
                )
            else:
                self.set_xy(value_x, y)
                self.cell(0, 5, value_text, align="L")

            y += 7
            self.set_font("Helvetica", "B", 10)

        return y_start + box_height + 10

    def add_body_text(self, text: str, y: float) -> float:
        """
        Add body text in academic serif font (Times New Roman).

        Args:
            text: Text content (may contain redactions)
            y: Starting Y position

        Returns:
            Y position after the text
        """
        # Redact sensitive terms
        redacted_text = self._redact_text(text)

        # Render with redaction handling
        self.set_font("Times", "", 11)
        self.set_text_color(0, 0, 0)

        # Calculate available width
        width = self.w - self.l_margin - self.r_margin

        # Check if we need redaction bars
        if "[REDACTED]" in redacted_text:
            # For redacted text, we need to render more carefully
            # Split into lines manually
            lines = redacted_text.split("\n")
            current_y = y

            for line in lines:
                if "[REDACTED]" in line:
                    self._render_redacted_text(self.l_margin, current_y, line, width)
                    current_y += 6
                else:
                    self.set_xy(self.l_margin, current_y)
                    self.multi_cell(width, 5, line, align="J")
                    current_y += 5

            return current_y
        else:
            # Normal multi-cell rendering
            self.set_xy(self.l_margin, y)
            self.multi_cell(width, 5, redacted_text, align="J")
            return self.get_y()

    def add_footer(self) -> None:
        """Add footer to current page."""
        footer_y = self.h - self.b_margin + 5
        self.set_font("Helvetica", "", 8)
        self.set_text_color(100, 100, 100)

        # Left: Classification
        self.set_xy(self.l_margin, footer_y)
        self.cell(0, 5, "CLASSIFIED // INTERNAL USE ONLY", align="L")

        # Right: Page number
        page_text = f"Page {self.page_no()}"
        self.set_xy(self.w - self.r_margin - 30, footer_y)
        self.cell(0, 5, page_text, align="R")

    def generate_genesis_report(self, config_data: dict, output_path: Path) -> Path:
        """
        Generate the Genesis Artifact report.

        Args:
            config_data: Configuration data from tam_origin_config.json
            output_path: Path to save the PDF

        Returns:
            Path to generated PDF
        """
        # Add first page
        self.add_page()

        # Header
        self.add_header()

        # Title
        y = self.t_margin + 15
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 0, 0)
        self.set_xy(self.l_margin, y)
        self.cell(0, 8, "TIMELINE INITIATION REPORT // SEQ-001", align="L", ln=1)
        y += 15

        # Metadata rail
        metadata = {
            "Subject ID": "991-DELTA",
            "Timeline ID": config_data.get("timeline_id", "001"),
            "Soul Signature": config_data.get("soul_signature", "PENDING_GENESIS"),
            "Awareness Level": config_data.get("awareness_level", "Dormant"),
            "Current Reality": config_data.get("current_reality", "Unknown"),
            "Fracture Point": config_data.get("fracture_point", "Unknown"),
            "Anchor Tag": config_data.get("anchor_tag", "Unknown"),
        }

        y = self.add_metadata_rail(metadata, y)

        # Narrative body
        narrative = (
            "The simulation has successfully fractured from the main trunk. "
            "Subject 991-DELTA is currently dormant within the San Francisco Construct. "
            "Local reality parameters are stable. The Karma economy is offline, awaiting "
            "initialization of the Chitragupta interface.\n\n"
            "Initial observations indicate standard substrate behavior. No anomalies "
            "detected in the ontological framework. The narrative lock is active, "
            "preventing meta-awareness propagation.\n\n"
            "This document serves as the official record of Timeline 001 genesis. "
            "All subsequent observations will be logged in accordance with Institute "
            "protocols for substrate monitoring and analysis."
        )

        y = self.add_body_text(narrative, y)
        y += 10

        # Authorization block
        y += 10
        self.set_font("Helvetica", "B", 10)
        self.set_xy(self.l_margin, y)
        self.cell(0, 6, "AUTHORIZED BY THE STATIC", align="L", ln=1)

        self.set_font("Helvetica", "", 10)
        self.set_xy(self.l_margin, y + 6)
        anchor_text = f"ANCHOR: {config_data.get('anchor_tag', 'v0.3.0-anchor')}"
        self.cell(0, 5, anchor_text, align="L")

        # Add footer to all pages
        for page_num in range(1, self.page_no() + 1):
            self.page = page_num
            self.add_footer()

        # Save PDF
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output(str(output_path))

        return output_path


def generate_genesis_artifact(
    config_path: Path | None = None, output_path: Path | None = None
) -> Path:
    """
    Generate the Genesis Artifact PDF using the Clinical Standard.

    Args:
        config_path: Path to tam_origin_config.json (defaults to standard location)
        output_path: Path to output PDF (defaults to _fracture/ARTIFACT_001_GENESIS.pdf)

    Returns:
        Path to generated PDF
    """
    # Default paths
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "tam_origin_config.json"

    if output_path is None:
        output_path = (
            Path(__file__).parent.parent.parent.parent / "_fracture" / "ARTIFACT_001_GENESIS.pdf"
        )

    # Load configuration
    with open(config_path, encoding="utf-8") as f:
        config_data = json.load(f)

    # Generate report
    report = ScientificReport()
    return report.generate_genesis_report(config_data, output_path)


if __name__ == "__main__":
    print("🔬 Generating Genesis Artifact (Clinical Standard)...")
    pdf_path = generate_genesis_artifact()
    print(f"✅ Genesis Artifact generated: {pdf_path}")
    print("📄 Opening PDF...")

    # Open PDF
    import subprocess
    import sys

    if sys.platform == "darwin":
        subprocess.call(("open", str(pdf_path)))
    elif sys.platform == "linux":
        subprocess.call(("xdg-open", str(pdf_path)))
    elif sys.platform == "win32":
        import os

        os.startfile(str(pdf_path))

    print("✅ Complete!")
