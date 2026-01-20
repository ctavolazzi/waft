"""
PDF Redactor - Storytelling Tool
=================================

A fun tool for redacting information in PDFs. Perfect for creating
classified documents, mystery stories, or redacted reports!

Usage:
    from waft.pdf_redactor import redact_pdf

    # Simple usage
    redact_pdf(
        input_pdf="document.pdf",
        terms=["CLASSIFIED", "Agent Name", "Location Alpha"],
        output_pdf="redacted.pdf"
    )

    # Advanced usage
    from waft.pdf_redactor import PDFRedactor

    redactor = PDFRedactor("document.pdf")
    redactor.add_text_redaction("CLASSIFIED", x=100, y=700, width=200, height=20)
    redactor.add_text_redaction("TOP SECRET", x=100, y=650, width=200, height=20)
    redactor.save("redacted.pdf")
"""

from dataclasses import dataclass
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
    from reportlab.lib.colors import black
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False


@dataclass
class RedactionArea:
    """An area to redact in a PDF."""

    x: float  # X position (points from left)
    y: float  # Y position (points from bottom)
    width: float
    height: float
    label: str | None = None  # Optional label for the redaction


class PDFRedactor:
    """
    Redact information from PDFs - perfect for storytelling!

    This creates black rectangles over specified areas in PDFs.
    Great for creating classified documents, mystery stories, or redacted reports.
    """

    def __init__(self, pdf_path: str | Path):
        """
        Initialize redactor.

        Args:
            pdf_path: Path to PDF to redact
        """
        if not HAS_DEPS:
            raise ImportError(
                "Required packages not installed. Install with:\n  pip install pypdf reportlab"
            )

        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {self.pdf_path}")

        self.reader = PdfReader(str(self.pdf_path))
        self.redaction_areas: list[RedactionArea] = []

    def add_text_redaction(
        self, text: str, x: float, y: float, width: float | None = None, height: float | None = None
    ) -> "PDFRedactor":
        """
        Add a text redaction area.

        Args:
            text: Text being redacted (for reference)
            x: X position in points (from left)
            y: Y position in points (from bottom of page)
            width: Width of redaction box (auto if None)
            height: Height of redaction box (auto if None)

        Returns:
            Self for fluent API
        """
        # Default size for text redaction
        if width is None:
            width = len(text) * 6  # Approximate width
        if height is None:
            height = 12  # Approximate height

        self.redaction_areas.append(RedactionArea(x=x, y=y, width=width, height=height, label=text))
        return self

    def add_area_redaction(
        self, x: float, y: float, width: float, height: float, label: str | None = None
    ) -> "PDFRedactor":
        """
        Add a rectangular area to redact.

        Args:
            x: X position (points from left)
            y: Y position (points from bottom)
            width: Width of redaction box
            height: Height of redaction box
            label: Optional label for this redaction

        Returns:
            Self for fluent API
        """
        self.redaction_areas.append(
            RedactionArea(x=x, y=y, width=width, height=height, label=label)
        )
        return self

    def save(self, output_path: str | Path | None = None) -> Path:
        """
        Save redacted PDF with black rectangles over redacted areas.

        Args:
            output_path: Where to save (default: adds _redacted suffix)

        Returns:
            Path to saved PDF
        """
        if output_path is None:
            output_path = self.pdf_path.parent / f"{self.pdf_path.stem}_redacted.pdf"
        else:
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Get page dimensions from first page
        first_page = self.reader.pages[0]
        page_width = float(first_page.mediabox.width)
        page_height = float(first_page.mediabox.height)
        num_pages = len(self.reader.pages)

        # Create overlay PDF with black rectangles
        overlay_path = output_path.parent / f"{output_path.stem}_overlay_temp.pdf"
        c = canvas.Canvas(str(overlay_path), pagesize=(page_width, page_height))

        # Draw black rectangles for each page
        for page_num in range(num_pages):
            for area in self.redaction_areas:
                # Draw black rectangle
                c.setFillColor(black)
                c.rect(area.x, area.y, area.width, area.height, fill=1, stroke=0)

            c.showPage()

        c.save()

        # Merge overlay with original PDF
        writer = PdfWriter()

        for page_num, page in enumerate(self.reader.pages):
            # Add original page
            writer.add_page(page)

            # Add overlay page (if it exists)
            try:
                overlay_reader = PdfReader(str(overlay_path))
                if page_num < len(overlay_reader.pages):
                    overlay_page = overlay_reader.pages[page_num]
                    page.merge_page(overlay_page)
            except Exception:
                pass

        # Write merged PDF
        with open(output_path, "wb") as f:
            writer.write(f)

        # Clean up overlay
        if overlay_path.exists():
            overlay_path.unlink()

        return output_path


def redact_pdf(
    input_pdf: str | Path,
    terms: list[str] | None = None,
    areas: list[tuple[float, float, float, float]] | None = None,
    output_pdf: str | Path | None = None,
) -> Path:
    """
    Quick redaction function - simplest API.

    Args:
        input_pdf: PDF to redact
        terms: List of terms to redact (requires manual positioning for now)
        areas: List of (x, y, width, height) tuples to redact
        output_pdf: Where to save (optional)

    Returns:
        Path to redacted PDF

    Example:
        # Redact specific areas
        redact_pdf(
            "document.pdf",
            areas=[(100, 700, 200, 20), (100, 650, 200, 20)],
            output_pdf="redacted.pdf"
        )
    """
    redactor = PDFRedactor(input_pdf)

    if areas:
        for x, y, width, height in areas:
            redactor.add_area_redaction(x, y, width, height)

    if terms:
        # Note: For automatic term finding, you'd need text extraction
        # For now, terms are just for reference
        print(f"Note: Terms to redact: {terms}")
        print("   Use add_area_redaction() with coordinates for now.")
        print("   Future: Automatic term detection coming soon!")

    return redactor.save(output_pdf)
