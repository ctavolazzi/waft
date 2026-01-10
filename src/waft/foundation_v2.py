"""
DocumentEngine V2 - Professional Research Documentation System

Enhanced PDF generation engine with professional typography, advanced layout,
and print optimization. Designed for scientific institutions, clinical reports,
and professional documentation.

NEW IN V2:
- Professional typography (serif, sans-serif, monospace families)
- Advanced layout blocks (MetadataRail, CoverPage, RuleBlock, TableBlock)
- Clinical Standard preset (Times New Roman body, sans-serif headers)
- Better font management with fallbacks
- Print-ready formatting with professional margins
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from ..core.science.observer import TheObserver
    from ..core.tavern_keeper import TavernKeeper

try:
    from fpdf import FPDF
except ImportError:
    raise ImportError("fpdf2 is required. Install with: pip install fpdf2>=2.7.0")


class RedactionStyle(Enum):
    """Redaction rendering styles."""
    BLACK_BAR = "black_bar"
    BLUR = "blur"
    CROSS_OUT = "cross_out"


class FontFamily(Enum):
    """Professional font families."""
    SERIF = "serif"  # Times, Georgia (academic, traditional)
    SANS_SERIF = "sans_serif"  # Helvetica, Arial (modern, clean)
    MONOSPACE = "monospace"  # Courier (code, data)


@dataclass
class FontConfig:
    """Enhanced font configuration with family support."""
    serif_family: str = "Times"
    serif_bold: str = "Times-Bold"
    sans_family: str = "Helvetica"
    sans_bold: str = "Helvetica-Bold"
    mono_family: str = "Courier"
    mono_bold: str = "Courier-Bold"


@dataclass
class DocumentConfig:
    """Configuration for document styling and behavior."""

    # Font configuration
    font_config: FontConfig = field(default_factory=FontConfig)

    # Document metadata
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None

    # Header/Footer
    watermark: Optional[str] = None
    header_text: Optional[str] = None
    footer_text: Optional[str] = None

    # Layout
    page_margins: Tuple[float, float, float, float] = (72, 72, 72, 72)  # top, right, bottom, left (1 inch)
    line_spacing: float = 1.5

    # Typography
    font_size_title: int = 24
    font_size_h1: int = 18
    font_size_h2: int = 14
    font_size_h3: int = 12
    font_size_body: int = 11
    font_size_footer: int = 9

    # Body text font family
    body_font: FontFamily = FontFamily.SERIF
    header_font: FontFamily = FontFamily.SANS_SERIF

    # Redaction
    redaction_style: RedactionStyle = RedactionStyle.BLACK_BAR

    # Colors (RGB tuples)
    text_color: Tuple[int, int, int] = (0, 0, 0)
    header_color: Tuple[int, int, int] = (0, 0, 0)
    rule_color: Tuple[int, int, int] = (0, 0, 0)

    @classmethod
    def clinical_standard(
        cls,
        header: Optional[str] = None,
        watermark: Optional[str] = None,
    ) -> "DocumentConfig":
        """
        The Clinical Standard - Professional scientific documentation.

        - Times New Roman body (academic weight)
        - Helvetica headers (clean, modern)
        - Professional margins (1 inch)
        - Authoritative, institutional tone
        """
        return cls(
            font_config=FontConfig(
                serif_family="Times",
                serif_bold="Times-Bold",
                sans_family="Helvetica",
                sans_bold="Helvetica-Bold",
                mono_family="Courier",
                mono_bold="Courier-Bold",
            ),
            body_font=FontFamily.SERIF,
            header_font=FontFamily.SANS_SERIF,
            header_text=header,
            watermark=watermark,
            footer_text=None,
            line_spacing=1.4,
            font_size_title=22,
            font_size_h1=16,
            font_size_h2=14,
            font_size_h3=12,
            font_size_body=11,
            redaction_style=RedactionStyle.BLACK_BAR,
        )

    @classmethod
    def classified_dossier(
        cls,
        header: Optional[str] = None,
        watermark: str = "INTERNAL USE ONLY",
    ) -> "DocumentConfig":
        """SCP/Dossier style - monospace typewriter aesthetic."""
        return cls(
            body_font=FontFamily.MONOSPACE,
            header_font=FontFamily.MONOSPACE,
            header_text=header,
            watermark=watermark,
            footer_text="INTERNAL USE ONLY",
            redaction_style=RedactionStyle.BLACK_BAR,
        )

    @classmethod
    def scientific_journal(cls) -> "DocumentConfig":
        """Academic journal style - serif body, sans headers."""
        return cls(
            body_font=FontFamily.SERIF,
            header_font=FontFamily.SANS_SERIF,
            watermark="DRAFT",
            line_spacing=1.6,
            font_size_body=11,
        )


class ContentBlock(ABC):
    """Abstract base class for all content blocks."""

    @abstractmethod
    def render(
        self,
        pdf: FPDF,
        config: DocumentConfig,
        redactor: "AutoRedactor",
        y_position: float,
    ) -> float:
        """
        Render the content block to PDF.

        Args:
            pdf: FPDF instance
            config: Document configuration
            redactor: AutoRedactor instance
            y_position: Current Y position

        Returns:
            New Y position after rendering
        """
        pass

    def _check_page_break(self, pdf: FPDF, y_position: float, required_space: float = 100) -> float:
        """Check if we need a page break and return adjusted Y position."""
        if y_position > pdf.h - pdf.b_margin - required_space:
            pdf.add_page()
            return pdf.t_margin + 20
        return y_position

    def _get_font(self, config: DocumentConfig, family: FontFamily, bold: bool = False) -> Tuple[str, str]:
        """Get font family and style based on FontFamily enum."""
        fc = config.font_config

        if family == FontFamily.SERIF:
            return (fc.serif_bold if bold else fc.serif_family, "B" if bold else "")
        elif family == FontFamily.SANS_SERIF:
            return (fc.sans_bold if bold else fc.sans_family, "B" if bold else "")
        elif family == FontFamily.MONOSPACE:
            return (fc.mono_bold if bold else fc.mono_family, "B" if bold else "")
        else:
            return (fc.serif_family, "")


class CoverPage(ContentBlock):
    """Full cover page with institutional header."""

    def __init__(
        self,
        institution: str,
        division: Optional[str] = None,
        document_type: str = "RESEARCH REPORT",
        document_number: Optional[str] = None,
        classification: Optional[str] = None,
    ):
        self.institution = institution
        self.division = division
        self.document_type = document_type
        self.document_number = document_number
        self.classification = classification

    def render(
        self,
        pdf: FPDF,
        config: DocumentConfig,
        redactor: "AutoRedactor",
        y_position: float,
    ) -> float:
        """Render professional cover page."""
        # Start at top margin
        y = pdf.t_margin + 30

        # Institution name (large, bold, sans-serif)
        font_family, font_style = self._get_font(config, FontFamily.SANS_SERIF, bold=True)
        pdf.set_font(font_family, style=font_style, size=config.font_size_title)
        pdf.set_text_color(*config.header_color)

        # Center the institution name
        text_width = pdf.get_string_width(self.institution)
        x = (pdf.w - text_width) / 2
        pdf.text(x, y, self.institution)
        y += config.font_size_title * 1.5

        # Division (if provided)
        if self.division:
            pdf.set_font(font_family, style="", size=config.font_size_h2)
            text_width = pdf.get_string_width(self.division)
            x = (pdf.w - text_width) / 2
            pdf.text(x, y, self.division)
            y += config.font_size_h2 * 1.5

        # Add horizontal rule
        y += 20
        rule_margin = 100
        pdf.set_line_width(0.5)
        pdf.set_draw_color(*config.rule_color)
        pdf.line(rule_margin, y, pdf.w - rule_margin, y)
        y += 30

        # Document type (centered)
        pdf.set_font(font_family, style=font_style, size=config.font_size_h1)
        text_width = pdf.get_string_width(self.document_type)
        x = (pdf.w - text_width) / 2
        pdf.text(x, y, self.document_type)
        y += config.font_size_h1 * 2

        # Document number (if provided)
        if self.document_number:
            pdf.set_font(font_family, style="", size=config.font_size_h2)
            text_width = pdf.get_string_width(self.document_number)
            x = (pdf.w - text_width) / 2
            pdf.text(x, y, self.document_number)
            y += config.font_size_h2 * 1.5

        # Classification (if provided)
        if self.classification:
            y += 30
            pdf.set_font(font_family, style=font_style, size=config.font_size_h1)
            text_width = pdf.get_string_width(self.classification)
            x = (pdf.w - text_width) / 2
            pdf.text(x, y, self.classification)
            y += config.font_size_h1 * 1.5

        # Reset text color
        pdf.set_text_color(*config.text_color)

        # Add page break after cover
        pdf.add_page()
        return pdf.t_margin + 20


class MetadataRail(ContentBlock):
    """Metadata block with header styling (like a sidebar rail)."""

    def __init__(
        self,
        title: str,
        metadata: Dict[str, str],
        style: str = "header"  # "header" or "sidebar"
    ):
        self.title = title
        self.metadata = metadata
        self.style = style

    def render(
        self,
        pdf: FPDF,
        config: DocumentConfig,
        redactor: "AutoRedactor",
        y_position: float,
    ) -> float:
        """Render metadata rail."""
        y = self._check_page_break(pdf, y_position, 150)

        # Draw background box
        box_padding = 10
        box_x = pdf.l_margin
        box_w = pdf.w - pdf.l_margin - pdf.r_margin

        # Calculate box height
        line_height = config.font_size_body * 1.3
        num_lines = len(self.metadata) + 1  # +1 for title
        box_h = num_lines * line_height + box_padding * 2

        # Draw light gray background
        pdf.set_fill_color(240, 240, 240)
        pdf.rect(box_x, y - 5, box_w, box_h, style="F")

        # Title
        font_family, font_style = self._get_font(config, FontFamily.SANS_SERIF, bold=True)
        pdf.set_font(font_family, style=font_style, size=config.font_size_h3)
        pdf.set_xy(box_x + box_padding, y)
        pdf.cell(0, line_height, self.title, align="L")
        y += line_height * 1.2

        # Metadata entries
        font_family, font_style = self._get_font(config, config.body_font, bold=False)
        pdf.set_font(font_family, style=font_style, size=config.font_size_body - 1)

        key_width = box_w * 0.35
        for key, value in self.metadata.items():
            pdf.set_xy(box_x + box_padding, y)
            # Key (bold)
            pdf.set_font(font_family, style="B", size=config.font_size_body - 1)
            pdf.cell(key_width, line_height, f"{key}:", align="L")
            # Value
            pdf.set_font(font_family, style="", size=config.font_size_body - 1)
            pdf.set_xy(box_x + box_padding + key_width, y)
            redactor.render_text(pdf, str(value), box_x + box_padding + key_width, y + line_height * 0.7, config.font_size_body - 1)
            y += line_height

        return y + box_padding + 10


class RuleBlock(ContentBlock):
    """Horizontal rule for visual separation."""

    def __init__(self, thickness: float = 0.5, width_percent: float = 100.0):
        self.thickness = thickness
        self.width_percent = width_percent

    def render(
        self,
        pdf: FPDF,
        config: DocumentConfig,
        redactor: "AutoRedactor",
        y_position: float,
    ) -> float:
        """Render horizontal rule."""
        y = y_position + 10

        page_width = pdf.w - pdf.l_margin - pdf.r_margin
        rule_width = page_width * (self.width_percent / 100.0)
        rule_x = pdf.l_margin + (page_width - rule_width) / 2

        pdf.set_line_width(self.thickness)
        pdf.set_draw_color(*config.rule_color)
        pdf.line(rule_x, y, rule_x + rule_width, y)

        return y + 10


class SectionHeader(ContentBlock):
    """Section header block with improved typography."""

    def __init__(self, title: str, level: int = 1):
        self.title = title
        self.level = level  # 1-3

    def render(
        self,
        pdf: FPDF,
        config: DocumentConfig,
        redactor: "AutoRedactor",
        y_position: float,
    ) -> float:
        """Render section header."""
        y = y_position + (15 if self.level == 1 else 10)

        # Determine font size based on level
        if self.level == 1:
            font_size = config.font_size_h1
        elif self.level == 2:
            font_size = config.font_size_h2
        else:
            font_size = config.font_size_h3

        # Use header font (usually sans-serif)
        font_family, font_style = self._get_font(config, config.header_font, bold=True)
        pdf.set_font(font_family, style=font_style, size=font_size)
        pdf.set_text_color(*config.header_color)

        y = self._check_page_break(pdf, y, font_size * 3)
        pdf.set_xy(pdf.l_margin, y)

        # Apply redaction if needed
        redactor.render_text(pdf, self.title, pdf.l_margin, y, font_size)

        # Reset text color
        pdf.set_text_color(*config.text_color)

        y += font_size * 1.8
        return y


class TextBlock(ContentBlock):
    """Standard text paragraph with professional typography."""

    def __init__(self, content: str, font_family: Optional[FontFamily] = None, bold: bool = False):
        self.content = content
        self.font_family = font_family
        self.bold = bold

    def render(
        self,
        pdf: FPDF,
        config: DocumentConfig,
        redactor: "AutoRedactor",
        y_position: float,
    ) -> float:
        """Render text block with word wrapping."""
        if not self.content.strip():
            return y_position + config.font_size_body * 0.5

        # Use specified font or default to body font
        font_family = self.font_family if self.font_family else config.body_font
        font_name, font_style = self._get_font(config, font_family, bold=self.bold)
        pdf.set_font(font_name, style=font_style, size=config.font_size_body)

        page_width = pdf.w - pdf.l_margin - pdf.r_margin
        current_y = y_position

        # Handle multi-line content
        paragraphs = self.content.split("\n")

        for paragraph in paragraphs:
            if not paragraph.strip():
                current_y += config.font_size_body * 0.5
                continue

            # Check page break before paragraph
            current_y = self._check_page_break(pdf, current_y, config.font_size_body * 3)

            # Word-wrap paragraph
            words = paragraph.split()
            current_line = []
            line_width = 0

            for word in words:
                word_with_space = word + " "
                word_width = pdf.get_string_width(word_with_space)

                if line_width + word_width > page_width and current_line:
                    # Render current line
                    line_text = " ".join(current_line)
                    redactor.render_text(
                        pdf, line_text, pdf.l_margin, current_y + config.font_size_body * 0.75, config.font_size_body
                    )
                    current_y += config.font_size_body * config.line_spacing
                    current_line = [word]
                    line_width = pdf.get_string_width(word + " ")
                else:
                    current_line.append(word)
                    line_width += word_width

            # Render remaining line
            if current_line:
                line_text = " ".join(current_line)
                redactor.render_text(
                    pdf, line_text, pdf.l_margin, current_y + config.font_size_body * 0.75, config.font_size_body
                )
                current_y += config.font_size_body * config.line_spacing

        return current_y + 8


class KeyValueBlock(ContentBlock):
    """Key-value pairs with improved layout."""

    def __init__(self, data: Dict[str, str], label: Optional[str] = None):
        self.data = data
        self.label = label

    def render(
        self,
        pdf: FPDF,
        config: DocumentConfig,
        redactor: "AutoRedactor",
        y_position: float,
    ) -> float:
        """Render key-value pairs."""
        current_y = y_position
        line_height = config.font_size_body * 1.3

        if self.label:
            font_family, font_style = self._get_font(config, config.header_font, bold=True)
            pdf.set_font(font_family, style=font_style, size=config.font_size_h3)
            current_y = self._check_page_break(pdf, current_y, config.font_size_h3 * 1.5)
            pdf.set_xy(pdf.l_margin, current_y)
            redactor.render_text(pdf, self.label, pdf.l_margin, current_y + config.font_size_h3 * 0.7, config.font_size_h3)
            current_y += config.font_size_h3 * 1.8

        font_family, font_style = self._get_font(config, config.body_font, bold=False)
        pdf.set_font(font_family, style=font_style, size=config.font_size_body)
        page_width = pdf.w - pdf.l_margin - pdf.r_margin
        key_width = page_width * 0.3

        for key, value in self.data.items():
            current_y = self._check_page_break(pdf, current_y, line_height)

            # Key (bold)
            pdf.set_font(font_family, style="B", size=config.font_size_body)
            pdf.set_xy(pdf.l_margin, current_y)
            pdf.cell(key_width, line_height, f"{key}:", align="L")

            # Value
            pdf.set_font(font_family, style="", size=config.font_size_body)
            pdf.set_xy(pdf.l_margin + key_width, current_y)
            redactor.render_text(
                pdf, str(value), pdf.l_margin + key_width, current_y + line_height * 0.55, config.font_size_body
            )

            current_y += line_height

        return current_y + 10


class TableBlock(ContentBlock):
    """Simple table block for structured data."""

    def __init__(
        self,
        headers: List[str],
        rows: List[List[str]],
        column_widths: Optional[List[float]] = None,
    ):
        self.headers = headers
        self.rows = rows
        self.column_widths = column_widths

    def render(
        self,
        pdf: FPDF,
        config: DocumentConfig,
        redactor: "AutoRedactor",
        y_position: float,
    ) -> float:
        """Render simple table."""
        y = self._check_page_break(pdf, y_position, 100)

        page_width = pdf.w - pdf.l_margin - pdf.r_margin
        num_cols = len(self.headers)

        # Calculate column widths
        if self.column_widths:
            col_widths = self.column_widths
        else:
            col_widths = [page_width / num_cols] * num_cols

        line_height = config.font_size_body * 1.4
        font_family, font_style = self._get_font(config, config.body_font, bold=False)

        # Draw header row
        pdf.set_font(font_family, style="B", size=config.font_size_body)
        pdf.set_fill_color(220, 220, 220)
        x = pdf.l_margin

        for i, header in enumerate(self.headers):
            pdf.set_xy(x, y)
            pdf.cell(col_widths[i], line_height, header, border=1, align="C", fill=True)
            x += col_widths[i]

        y += line_height

        # Draw data rows
        pdf.set_font(font_family, style="", size=config.font_size_body - 1)
        for row in self.rows:
            y = self._check_page_break(pdf, y, line_height)
            x = pdf.l_margin

            for i, cell in enumerate(row):
                pdf.set_xy(x, y)
                pdf.cell(col_widths[i], line_height, str(cell), border=1, align="L")
                x += col_widths[i]

            y += line_height

        return y + 10


class WarningBlock(ContentBlock):
    """Warning block with border."""

    def __init__(self, text: str, severity: str = "WARNING"):
        self.text = text
        self.severity = severity

    def render(
        self,
        pdf: FPDF,
        config: DocumentConfig,
        redactor: "AutoRedactor",
        y_position: float,
    ) -> float:
        """Render warning block."""
        y = self._check_page_break(pdf, y_position, 80)
        y += 5

        border_margin = 10
        page_width = pdf.w - pdf.l_margin - pdf.r_margin
        border_x = pdf.l_margin + border_margin
        border_w = page_width - (border_margin * 2)

        # Calculate height
        font_family, font_style = self._get_font(config, config.body_font, bold=False)
        pdf.set_font(font_family, style=font_style, size=config.font_size_body)
        estimated_lines = max(2, len(self.text.split("\n")) + 1)
        text_height = config.font_size_body * estimated_lines * 1.4
        border_h = text_height + 15

        # Draw rectangle
        pdf.set_line_width(1)
        pdf.set_draw_color(200, 0, 0)
        pdf.rect(border_x, y, border_w, border_h)

        # Severity label
        font_family, font_style = self._get_font(config, FontFamily.SANS_SERIF, bold=True)
        pdf.set_font(font_family, style=font_style, size=config.font_size_body)
        pdf.set_text_color(200, 0, 0)
        pdf.set_xy(border_x + 5, y + 5)
        pdf.cell(0, config.font_size_body, f"[{self.severity}]", align="L")

        # Warning text
        pdf.set_text_color(*config.text_color)
        font_family, font_style = self._get_font(config, config.body_font, bold=False)
        pdf.set_font(font_family, style=font_style, size=config.font_size_body - 1)
        pdf.set_xy(border_x + 5, y + config.font_size_body + 10)
        redactor.render_text(
            pdf, self.text, border_x + 5, y + config.font_size_body + 10 + (config.font_size_body - 1) * 0.7, config.font_size_body - 1
        )

        return y + border_h + 15


class SignatureBlock(ContentBlock):
    """Signature/authorization block."""

    def __init__(self, role: str, name: str, timestamp: Optional[datetime] = None):
        self.role = role
        self.name = name
        self.timestamp = timestamp or datetime.now()

    def render(
        self,
        pdf: FPDF,
        config: DocumentConfig,
        redactor: "AutoRedactor",
        y_position: float,
    ) -> float:
        """Render signature block."""
        y = self._check_page_break(pdf, y_position, 50)
        y += 15

        font_family, font_style = self._get_font(config, config.body_font, bold=False)
        pdf.set_font(font_family, style=font_style, size=config.font_size_body)
        pdf.set_xy(pdf.l_margin, y)

        signature_text = f"{self.role}: {self.name}"
        redactor.render_text(pdf, signature_text, pdf.l_margin, y + config.font_size_body * 0.7, config.font_size_body)

        y += config.font_size_body * 1.5

        # Timestamp
        timestamp_text = self.timestamp.strftime("%B %d, %Y")
        pdf.set_xy(pdf.l_margin, y)
        redactor.render_text(pdf, timestamp_text, pdf.l_margin, y + config.font_size_body * 0.7, config.font_size_body)

        return y + config.font_size_body + 15


class LogBlock(ContentBlock):
    """Terminal/log output block."""

    def __init__(self, entries: List[str]):
        self.entries = entries

    def render(
        self,
        pdf: FPDF,
        config: DocumentConfig,
        redactor: "AutoRedactor",
        y_position: float,
    ) -> float:
        """Render log entries in monospace."""
        font_family, font_style = self._get_font(config, FontFamily.MONOSPACE, bold=False)
        pdf.set_font(font_family, style=font_style, size=config.font_size_body - 2)
        current_y = y_position

        for entry in self.entries:
            current_y = self._check_page_break(pdf, current_y, config.font_size_body)
            pdf.set_xy(pdf.l_margin, current_y)
            redactor.render_text(pdf, entry, pdf.l_margin, current_y + (config.font_size_body - 2) * 0.7, config.font_size_body - 2)
            current_y += (config.font_size_body - 2) * 1.4

        return current_y + 10


class AutoRedactor:
    """Automatic redaction engine."""

    def __init__(self, config: DocumentConfig):
        self.config = config
        self.sensitive_terms: List[str] = []

    def add_sensitive_terms(self, terms: List[str]) -> None:
        """Add terms to automatically redact."""
        self.sensitive_terms.extend(terms)

    def render_text(
        self, pdf: FPDF, text: str, x: float, y: float, font_size: int
    ) -> None:
        """Render text with automatic redaction."""
        if not self.sensitive_terms:
            pdf.text(x, y, text)
            return

        # Find all occurrences
        redactions = []
        text_lower = text.lower()
        for term in self.sensitive_terms:
            term_lower = term.lower()
            start = 0
            while True:
                pos = text_lower.find(term_lower, start)
                if pos == -1:
                    break
                redactions.append((pos, pos + len(term), term))
                start = pos + 1

        # Sort and merge overlapping
        redactions.sort(key=lambda r: r[0])
        merged_redactions = []
        for start, end, term in redactions:
            if merged_redactions and start < merged_redactions[-1][1]:
                merged_redactions[-1] = (
                    merged_redactions[-1][0],
                    max(merged_redactions[-1][1], end),
                    merged_redactions[-1][2] + "|" + term,
                )
            else:
                merged_redactions.append((start, end, term))

        # Render with redactions
        current_x = x
        last_end = 0

        for start, end, term in merged_redactions:
            # Normal text before redaction
            if start > last_end:
                normal_text = text[last_end:start]
                pdf.text(current_x, y, normal_text)
                current_x += pdf.get_string_width(normal_text)

            # Redacted text
            redacted_text = text[start:end]
            text_width = pdf.get_string_width(redacted_text)
            text_height = font_size * 0.85

            # White text (invisible but selectable)
            pdf.set_text_color(255, 255, 255)
            pdf.text(current_x, y, redacted_text)

            # Black rectangle
            pdf.set_fill_color(0, 0, 0)
            pdf.rect(current_x, y - text_height, text_width, text_height, style="F")

            # Restore color
            pdf.set_text_color(*self.config.text_color)

            current_x += text_width
            last_end = end

        # Remaining text
        if last_end < len(text):
            remaining_text = text[last_end:]
            pdf.text(current_x, y, remaining_text)


class DocumentEngine(FPDF):
    """Enhanced PDF generation engine with professional typography."""

    def __init__(self, config: DocumentConfig):
        """Initialize DocumentEngine V2."""
        super().__init__()
        self.config = config
        self.blocks: List[ContentBlock] = []
        self.redactor = AutoRedactor(config)
        self.total_pages = 0

        # Set metadata
        if config.title:
            self.set_title(config.title)
        if config.author:
            self.set_author(config.author)
        if config.subject:
            self.set_subject(config.subject)

        # Disable auto page break - we handle it manually
        self.set_auto_page_break(auto=False, margin=0)
        self.set_margins(
            left=config.page_margins[3],
            top=config.page_margins[0],
            right=config.page_margins[1],
        )

    def add(self, block: ContentBlock) -> "DocumentEngine":
        """Add a content block (fluent API)."""
        self.blocks.append(block)
        return self

    def add_sensitive_terms(self, terms: List[str]) -> "DocumentEngine":
        """Add terms to automatically redact."""
        self.redactor.add_sensitive_terms(terms)
        return self

    def render(self, output_path: Path) -> Path:
        """Render all blocks to PDF."""
        # Add first page
        self.add_page()

        # Render all blocks
        y_position = self.t_margin + 10

        for block in self.blocks:
            # Check if we need a new page
            if y_position > self.h - self.b_margin - 100:
                self._add_header_footer()
                if self.config.watermark:
                    self._add_watermark()
                self.add_page()
                y_position = self.t_margin + 10

            # Render block
            y_position = block.render(self, self.config, self.redactor, y_position)

        # Add headers/footers to all pages
        self.total_pages = self.page_no()
        for page_num in range(1, self.total_pages + 1):
            self.page = page_num
            self._add_header_footer()
            if self.config.watermark:
                self._add_watermark()

        # Output PDF
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output(str(output_path))

        return output_path

    def _add_header_footer(self) -> None:
        """Add headers and footers."""
        font_family, font_style = ContentBlock()._get_font(self.config, self.config.body_font, bold=False)

        if self.config.header_text:
            self.set_font(font_family, style=font_style, size=self.config.font_size_footer)
            self.set_xy(self.l_margin, self.t_margin - 10)
            self.cell(0, 10, self.config.header_text, align="L")

        if self.config.footer_text:
            self.set_font(font_family, style=font_style, size=self.config.font_size_footer)
            self.set_xy(self.l_margin, self.h - self.b_margin + 5)
            self.cell(0, 10, self.config.footer_text, align="L")

        # Page number
        page_text = f"Page {self.page_no()} of {self.total_pages or 1}"
        self.set_xy(self.w - self.r_margin - 50, self.h - self.b_margin + 5)
        self.cell(0, 10, page_text, align="R")

    def _add_watermark(self) -> None:
        """Add watermark."""
        if not self.config.watermark:
            return

        current_font = self.font_family
        current_size = self.font_size

        self.set_font("Helvetica", style="B", size=48)
        self.set_text_color(220, 220, 220)

        text_width = self.get_string_width(self.config.watermark)
        x = (self.w - text_width) / 2
        y = self.h / 2

        self.text(x, y, self.config.watermark)

        self.set_font(current_font, size=current_size)
        self.set_text_color(*self.config.text_color)


def generate_clinical_report_demo(output_path: Optional[Path] = None) -> Path:
    """
    Generate a demonstration report using the Clinical Standard preset.

    This showcases the professional typography, advanced layout blocks,
    and institutional styling of the V2 engine.
    """
    if output_path is None:
        output_path = Path("_work_efforts/CLINICAL_STANDARD_DEMO.pdf")

    # Configure for Clinical Standard
    config = DocumentConfig.clinical_standard(
        header="INSTITUTE FOR ADVANCED ONTOLOGICAL STUDIES",
        watermark=None,
    )

    # Initialize engine
    engine = DocumentEngine(config)

    # Set sensitive terms
    engine.add_sensitive_terms([
        "Fai Wei Tam",
        "991-DELTA",
        "San Francisco",
    ])

    # COVER PAGE
    engine.add(CoverPage(
        institution="INSTITUTE FOR ADVANCED ONTOLOGICAL STUDIES",
        division="Department of Computational Phenomenology",
        document_type="RESEARCH REPORT",
        document_number="Report No. 001-ALPHA",
        classification="INTERNAL USE ONLY",
    ))

    # METADATA RAIL
    engine.add(MetadataRail(
        title="Subject Information",
        metadata={
            "Subject ID": "991-DELTA",
            "Subject Name": "Fai Wei Tam",
            "Timeline": "001-ORIGIN-TAM",
            "Soul Signature": "0xA3F9B2C1",
            "Status": "DORMANT",
            "Location": "San Francisco, CA",
            "Last Updated": datetime(2026, 1, 10).strftime("%Y-%m-%d"),
        }
    ))

    # SECTION 1
    engine.add(SectionHeader("Executive Summary", level=1))
    engine.add(TextBlock(
        "This report documents the initial observations and baseline measurements "
        "for Subject 991-DELTA within the Wide-Area Functional Taxonomy (WAFT) framework. "
        "The subject has been successfully instantiated within Timeline 001 and is currently "
        "in a dormant state pending activation protocols."
    ))

    engine.add(RuleBlock(thickness=0.5, width_percent=80))

    # SECTION 2
    engine.add(SectionHeader("Methodology", level=1))
    engine.add(SectionHeader("Observation Protocol", level=2))
    engine.add(TextBlock(
        "All observations are conducted through non-invasive monitoring systems integrated "
        "within the simulation substrate. Measurements include:\n\n"
        "• Coherence metrics (baseline threshold: 0.85)\n"
        "• Temporal consistency markers\n"
        "• Narrative drift coefficients\n"
        "• Karmic accumulation rates"
    ))

    engine.add(SectionHeader("Data Collection", level=2))
    engine.add(TextBlock(
        "Data is collected via TheObserver subsystem and logged to immutable storage. "
        "All events are timestamped with nanosecond precision and cryptographically signed."
    ))

    # TABLE EXAMPLE
    engine.add(SectionHeader("Initial Measurements", level=1))
    engine.add(TableBlock(
        headers=["Parameter", "Value", "Unit", "Status"],
        rows=[
            ["Coherence", "0.87", "ratio", "NORMAL"],
            ["Karma Balance", "0", "units", "BASELINE"],
            ["Timeline Drift", "< 0.01", "σ", "STABLE"],
            ["Narrative Integrity", "1.00", "ratio", "OPTIMAL"],
        ],
    ))

    # WARNING
    engine.add(WarningBlock(
        "CRITICAL: Subject must not access this documentation. Any breach of containment "
        "may result in recursive self-awareness cascade. Maintain information asymmetry at all times.",
        severity="CRITICAL"
    ))

    # CONCLUSION
    engine.add(SectionHeader("Conclusions", level=1))
    engine.add(TextBlock(
        "Subject 991-DELTA presents as an ideal candidate for the reincarnation protocols. "
        "All baseline metrics fall within acceptable parameters. Authorization is recommended "
        "to proceed to Phase 2: Awakening."
    ))

    # SIGNATURE
    engine.add(RuleBlock(thickness=0.3, width_percent=50))
    engine.add(SignatureBlock(
        role="Principal Investigator",
        name="Dr. [REDACTED]",
        timestamp=datetime(2026, 1, 10),
    ))

    # APPENDIX
    engine.add(SectionHeader("Appendix A: System Logs", level=1))
    engine.add(LogBlock([
        "[2026-01-10 00:00:01] System initialization complete",
        "[2026-01-10 00:00:02] Subject 991-DELTA instantiated",
        "[2026-01-10 00:00:03] Timeline 001-ORIGIN-TAM created",
        "[2026-01-10 00:00:04] Location set: San Francisco, CA",
        "[2026-01-10 00:00:05] Subject Fai Wei Tam entering dormant state",
        "[2026-01-10 00:00:06] Baseline measurements recorded",
        "[2026-01-10 00:00:07] Awaiting activation signal",
    ]))

    # Render
    return engine.render(output_path)


if __name__ == "__main__":
    """Test the enhanced DocumentEngine V2."""
    print("Testing DocumentEngine V2 - Clinical Standard")
    output_path = generate_clinical_report_demo()
    print(f"✅ Generated: {output_path}")
    print(f"   File size: {output_path.stat().st_size / 1024:.1f} KB")
