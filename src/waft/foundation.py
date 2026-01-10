"""
DocumentEngine - Reusable Research Documentation Library

A content-agnostic PDF generation engine with modular content blocks,
automatic redaction, and configurable styling. Designed for scientific logs,
legal audits, journalism, and structured documentation.

The engine is completely portable - no WAFT-specific dependencies.
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
    BLUR = "blur"  # Falls back to BLACK_BAR if not supported
    CROSS_OUT = "cross_out"


@dataclass
class DocumentConfig:
    """Configuration for document styling and behavior."""

    fonts: Dict[str, str] = field(
        default_factory=lambda: {
            "Header": "Courier-Bold",
            "Body": "Courier",
            "Monospace": "Courier",
        }
    )
    watermark: Optional[str] = None
    redaction_style: RedactionStyle = RedactionStyle.BLACK_BAR
    header_text: Optional[str] = None
    footer_text: Optional[str] = None
    page_margins: Tuple[float, float, float, float] = (72, 72, 72, 72)  # top, right, bottom, left
    line_spacing: float = 1.5
    font_size_body: int = 12
    font_size_header: int = 14
    font_size_footer: int = 10

    @classmethod
    def classified_dossier(
        cls,
        header: Optional[str] = None,
        watermark: str = "INTERNAL USE ONLY",
    ) -> "DocumentConfig":
        """Preset config for SCP/Dossier style documentation."""
        return cls(
            fonts={
                "Header": ("Courier", "B"),
                "Body": ("Courier", ""),
                "Monospace": ("Courier", ""),
            },
            watermark=watermark,
            header_text=header,
            footer_text="INTERNAL USE ONLY",
            redaction_style=RedactionStyle.BLACK_BAR,
        )

    @classmethod
    def scientific_log(cls) -> "DocumentConfig":
        """Preset config for scientific documentation."""
        return cls(
            fonts={
                "Header": ("Courier", "B"),
                "Body": ("Courier", ""),
                "Monospace": ("Courier", ""),
            },
            watermark="DRAFT",
            redaction_style=RedactionStyle.BLACK_BAR,
        )

    @classmethod
    def legal_audit(cls) -> "DocumentConfig":
        """Preset config for legal documentation."""
        return cls(
            fonts={
                "Header": "Courier-Bold",
                "Body": "Courier",
                "Monospace": "Courier",
            },
            watermark="CONFIDENTIAL",
            redaction_style=RedactionStyle.BLACK_BAR,
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
            redactor: AutoRedactor instance for automatic redaction
            y_position: Current Y position on page

        Returns:
            New Y position after rendering
        """
        pass


class SectionHeader(ContentBlock):
    """Section header block."""

    def __init__(self, title: str, level: int = 1):
        self.title = title
        self.level = level  # 1-3 for different header sizes

    def render(
        self,
        pdf: FPDF,
        config: DocumentConfig,
        redactor: "AutoRedactor",
        y_position: float,
    ) -> float:
        """Render section header."""
        # Add spacing before header
        y_position += 10

        # Determine font size based on level
        if self.level == 1:
            font_size = config.font_size_header + 4
        elif self.level == 2:
            font_size = config.font_size_header
        else:
            font_size = config.font_size_header - 2

        font_family, font_style = config.fonts["Header"]
        pdf.set_font(font_family, style=font_style, size=font_size)
        pdf.set_xy(pdf.l_margin, y_position)

        # Apply redaction if needed
        redactor.render_text(pdf, self.title, pdf.l_margin, y_position, font_size)

        y_position += font_size * 1.5
        return y_position


class TextBlock(ContentBlock):
    """Standard text paragraph block."""

    def __init__(self, content: str, style: str = "Body"):
        self.content = content
        self.style = style  # "Body", "Monospace", "Italic"

    def render(
        self,
        pdf: FPDF,
        config: DocumentConfig,
        redactor: "AutoRedactor",
        y_position: float,
    ) -> float:
        """Render text block with automatic redaction."""
        font_key = self.style if self.style in config.fonts else "Body"
        font_family, font_style = config.fonts[font_key]
        pdf.set_font(font_family, style=font_style, size=config.font_size_body)
        
        if not self.content.strip():
            return y_position + config.font_size_body * 0.5

        # Split content into lines that fit page width
        page_width = pdf.w - pdf.l_margin - pdf.r_margin
        current_y = y_position
        
        # Handle multi-line content (split by newlines first)
        paragraphs = self.content.split("\n")
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                current_y += config.font_size_body * 0.5
                continue
                
            # Word-wrap paragraph
            words = paragraph.split()
            current_line = []
            line_width = 0
            
            for word in words:
                word_with_space = word + " "
                word_width = pdf.get_string_width(word_with_space)
                
                if line_width + word_width > page_width and current_line:
                    # Render current line with redaction
                    line_text = " ".join(current_line)
                    redactor.render_text(
                        pdf, line_text, pdf.l_margin, current_y, config.font_size_body
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
                    pdf, line_text, pdf.l_margin, current_y, config.font_size_body
                )
                current_y += config.font_size_body * config.line_spacing

        return current_y + 5  # Add spacing after block


class KeyValueBlock(ContentBlock):
    """Key-value pairs block (metadata, parameters, etc.)."""

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
        line_height = config.font_size_body * config.line_spacing

        if self.label:
            font_family, font_style = config.fonts["Header"]
            pdf.set_font(font_family, style=font_style, size=config.font_size_header)
            # Check if label fits on current page
            if current_y + config.font_size_header * 1.5 > pdf.h - pdf.b_margin - 100:
                pdf.add_page()
                current_y = pdf.t_margin + 10
            pdf.set_xy(pdf.l_margin, current_y)
            redactor.render_text(pdf, self.label, pdf.l_margin, current_y, config.font_size_header)
            current_y += config.font_size_header * 1.5

        font_family, font_style = config.fonts["Body"]
        pdf.set_font(font_family, style=font_style, size=config.font_size_body)
        page_width = pdf.w - pdf.l_margin - pdf.r_margin
        key_width = page_width * 0.3  # 30% for keys

        for key, value in self.data.items():
            # Check if this item fits on current page
            if current_y + line_height > pdf.h - pdf.b_margin - 100:
                pdf.add_page()
                current_y = pdf.t_margin + 10

            # Render key
            pdf.set_xy(pdf.l_margin, current_y)
            redactor.render_text(pdf, f"{key}:", pdf.l_margin, current_y, config.font_size_body)

            # Render value (with redaction)
            pdf.set_xy(pdf.l_margin + key_width, current_y)
            redactor.render_text(
                pdf, str(value), pdf.l_margin + key_width, current_y, config.font_size_body
            )

            current_y += line_height

        return current_y + 5


class LogBlock(ContentBlock):
    """Terminal/log output block (monospace, timestamped entries)."""

    def __init__(self, entries: List[str], timestamp_format: Optional[str] = None):
        self.entries = entries
        self.timestamp_format = timestamp_format

    def render(
        self,
        pdf: FPDF,
        config: DocumentConfig,
        redactor: "AutoRedactor",
        y_position: float,
    ) -> float:
        """Render log entries in monospace."""
        font_family, font_style = config.fonts["Monospace"]
        pdf.set_font(font_family, style=font_style, size=config.font_size_body - 1)
        current_y = y_position

        for entry in self.entries:
            pdf.set_xy(pdf.l_margin, current_y)
            redactor.render_text(pdf, entry, pdf.l_margin, current_y, config.font_size_body - 1)
            current_y += (config.font_size_body - 1) * config.line_spacing

        return current_y + 5


class WarningBlock(ContentBlock):
    """Warning/caution block with border."""

    def __init__(self, text: str, severity: str = "WARNING"):
        self.text = text
        self.severity = severity  # "WARNING", "CAUTION", "CRITICAL"

    def render(
        self,
        pdf: FPDF,
        config: DocumentConfig,
        redactor: "AutoRedactor",
        y_position: float,
    ) -> float:
        """Render warning block with border."""
        current_y = y_position + 5

        # Draw border
        border_margin = 10
        page_width = pdf.w - pdf.l_margin - pdf.r_margin
        border_x = pdf.l_margin + border_margin
        border_w = page_width - (border_margin * 2)

        # Calculate height needed for text (estimate)
        font_family, font_style = config.fonts["Body"]
        pdf.set_font(font_family, style=font_style, size=config.font_size_body)
        # Estimate text height based on line count
        estimated_lines = max(2, len(self.text.split("\n")))
        text_height = config.font_size_body * estimated_lines * config.line_spacing

        border_y = current_y
        border_h = text_height + 10

        # Draw rectangle border
        pdf.rect(border_x, border_y, border_w, border_h)

        # Render severity label
        font_family, font_style = config.fonts["Header"]
        pdf.set_font(font_family, style=font_style, size=config.font_size_body - 2)
        pdf.set_xy(border_x + 5, border_y + 5)
        redactor.render_text(
            pdf, f"[{self.severity}]", border_x + 5, border_y + 5, config.font_size_body - 2
        )

        # Render warning text
        font_family, font_style = config.fonts["Body"]
        pdf.set_font(font_family, style=font_style, size=config.font_size_body)
        pdf.set_xy(border_x + 5, border_y + config.font_size_body + 5)
        redactor.render_text(
            pdf, self.text, border_x + 5, border_y + config.font_size_body + 5, config.font_size_body
        )

        return border_y + border_h + 10


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
        current_y = y_position + 10

        font_family, font_style = config.fonts["Body"]
        pdf.set_font(font_family, style=font_style, size=config.font_size_body)
        pdf.set_xy(pdf.l_margin, current_y)

        signature_text = f"{self.role}: {self.name}"
        redactor.render_text(pdf, signature_text, pdf.l_margin, current_y, config.font_size_body)

        current_y += config.font_size_body * 1.2

        # Render timestamp
        timestamp_text = self.timestamp.strftime("%B %d, %Y")
        pdf.set_xy(pdf.l_margin, current_y)
        redactor.render_text(pdf, timestamp_text, pdf.l_margin, current_y, config.font_size_body)

        return current_y + config.font_size_body + 10


class AutoRedactor:
    """Automatic redaction engine that detects and redacts sensitive terms."""

    def __init__(self, config: DocumentConfig):
        self.config = config
        self.sensitive_terms: List[str] = []

    def add_sensitive_terms(self, terms: List[str]) -> None:
        """Add terms to automatically redact."""
        self.sensitive_terms.extend(terms)

    def render_text(
        self, pdf: FPDF, text: str, x: float, y: float, font_size: int
    ) -> None:
        """
        Render text with automatic redaction of sensitive terms.

        Args:
            pdf: FPDF instance
            text: Text to render
            x: X position
            y: Y position
            font_size: Font size
        """
        if not self.sensitive_terms:
            # No redaction needed, render normally
            pdf.text(x, y, text)
            return

        # Find all occurrences of sensitive terms (case-insensitive)
        redactions = []
        text_lower = text.lower()
        for term in self.sensitive_terms:
            term_lower = term.lower()
            start = 0
            while True:
                pos = text_lower.find(term_lower, start)
                if pos == -1:
                    break
                # Use original case from text
                redactions.append((pos, pos + len(term), term))
                start = pos + 1

        # Sort redactions by position and merge overlapping
        redactions.sort(key=lambda r: r[0])
        merged_redactions = []
        for start, end, term in redactions:
            if merged_redactions and start < merged_redactions[-1][1]:
                # Merge with previous
                merged_redactions[-1] = (
                    merged_redactions[-1][0],
                    max(merged_redactions[-1][1], end),
                    merged_redactions[-1][2] + "|" + term,
                )
            else:
                merged_redactions.append((start, end, term))

        # Render text with redactions
        current_x = x
        last_end = 0

        for start, end, term in merged_redactions:
            # Render text before redaction
            if start > last_end:
                normal_text = text[last_end:start]
                pdf.text(current_x, y, normal_text)
                current_x += pdf.get_string_width(normal_text)

            # Render redacted text (white text + black bar)
            redacted_text = text[start:end]
            text_width = pdf.get_string_width(redacted_text)
            text_height = font_size * 0.85

            # Draw white text (invisible but selectable)
            pdf.set_text_color(255, 255, 255)
            pdf.text(current_x, y, redacted_text)

            # Draw black rectangle over text
            pdf.set_fill_color(0, 0, 0)
            pdf.rect(current_x, y - text_height, text_width, text_height, style="F")

            # Restore text color
            pdf.set_text_color(0, 0, 0)

            current_x += text_width
            last_end = end

        # Render remaining text
        if last_end < len(text):
            remaining_text = text[last_end:]
            pdf.text(current_x, y, remaining_text)


class DocumentEngine(FPDF):
    """Main PDF generation engine with modular content blocks and automatic redaction."""

    def __init__(self, config: DocumentConfig):
        """Initialize DocumentEngine with configuration."""
        super().__init__()
        self.config = config
        self.blocks: List[ContentBlock] = []
        self.redactor = AutoRedactor(config)
        self.total_pages = 0

        # Set up page
        # Disable auto page break - we handle it manually in render()
        self.set_auto_page_break(auto=False, margin=0)
        self.set_margins(
            left=config.page_margins[3],
            top=config.page_margins[0],
            right=config.page_margins[1],
        )

    def add(self, block: ContentBlock) -> "DocumentEngine":
        """Add a content block to the document (fluent API)."""
        self.blocks.append(block)
        return self

    def add_sensitive_terms(self, terms: List[str]) -> "DocumentEngine":
        """Add terms to automatically redact (fluent API)."""
        self.redactor.add_sensitive_terms(terms)
        return self

    def set_redactions(self, terms: List[str]) -> "DocumentEngine":
        """Alias for add_sensitive_terms (fluent API)."""
        return self.add_sensitive_terms(terms)

    def render(self, output_path: Path) -> Path:
        """
        Render all content blocks to PDF.

        Args:
            output_path: Path to output PDF file

        Returns:
            Path to generated PDF
        """
        # Add first page
        self.add_page()

        # Render all blocks
        y_position = self.t_margin + 10

        for block in self.blocks:
            # Check if we need a new page (more aggressive check)
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
        """Add headers and footers to current page."""
        if self.config.header_text:
            font_family, font_style = self.config.fonts["Body"]
            self.set_font(font_family, style=font_style, size=self.config.font_size_footer)
            self.set_xy(self.l_margin, self.t_margin - 10)
            self.cell(0, 10, self.config.header_text, align="L")

        if self.config.footer_text:
            font_family, font_style = self.config.fonts["Body"]
            self.set_font(font_family, style=font_style, size=self.config.font_size_footer)
            self.set_xy(self.l_margin, self.h - self.b_margin + 5)
            self.cell(0, 10, self.config.footer_text, align="L")

        # Page number
        page_text = f"Page {self.page_no()} of {self.total_pages or 1}"
        self.set_xy(self.w - self.r_margin - 50, self.h - self.b_margin + 5)
        self.cell(0, 10, page_text, align="R")

    def _add_watermark(self) -> None:
        """Add watermark to current page."""
        if not self.config.watermark:
            return

        # Save current settings
        current_font = self.font_family
        current_size = self.font_size
        # Note: fpdf2 doesn't expose text_color easily, so we'll just restore font

        # Set watermark style (use Courier directly)
        self.set_font("Courier", style="B", size=48)
        self.set_text_color(200, 200, 200)  # Light gray

        # Calculate center position
        text_width = self.get_string_width(self.config.watermark)
        x = (self.w - text_width) / 2
        y = self.h / 2

        # Draw watermark (fpdf2 doesn't support rotation easily, so use diagonal text effect)
        # For now, just center it horizontally
        self.text(x, y, self.config.watermark)

        # Restore settings
        self.set_font(current_font, size=current_size)
        self.set_text_color(0, 0, 0)  # Restore black text


# ============================================================================
# SECTION B: THE IMPLEMENTATION (Story Script)
# ============================================================================


def generate_specimen_d_audit(output_path: Optional[Path] = None) -> Path:
    """
    Generate the Specimen-D Audit dossier using DocumentEngine.

    This demonstrates the API by building the document programmatically
    using content blocks instead of hardcoded FPDF calls.
    """
    if output_path is None:
        output_path = Path("_work_efforts/WAFT_SPECIMEN_D_AUDIT_v2.pdf")

    # Configure for Site-Delta-9 dossier style
    config = DocumentConfig.classified_dossier(
        header="SITE-DELTA-9 // BIO-LOG",
        watermark="INTERNAL USE ONLY",
    )

    # Initialize engine
    engine = DocumentEngine(config)

    # Set sensitive terms for automatic redaction
    engine.add_sensitive_terms(
        [
            "001-ALPHA-GENESIS",
            "Sunset District",
            "N-Judah",
            "Fai Wei Tam",
            "TAM",
            "FAI WEI",
        ]
    )

    # PAGE 1: COVER
    engine.add(
        SectionHeader("INSTITUTE FOR ADVANCED ONTOLOGICAL STUDIES", level=1)
    )
    engine.add(TextBlock("FIELD OPERATIONS DIVISION", style="Body"))
    engine.add(TextBlock("PROPERTY OF TELEPORT MASSIVE // SITE-DELTA-9", style="Body"))
    engine.add(TextBlock(""))  # Spacing

    engine.add(
        KeyValueBlock(
            {
                "OPERATIONAL MANUAL": "09-14",
                "CODENAME": "W.A.F.T.",
                "SUBJECT": "TAM, FAI WEI [991-DELTA]",
                "PROTOCOL": "WIDE-AREA FUNCTIONAL TAXONOMY",
                "CYCLE": "XIV (RECURSIVE)",
                "BASE FREQUENCY": "60Hz",
                "COHERENCE THRESHOLD": "0.85",
                "ENGINE STATUS": "ACTIVE / NON-LINEAR",
            }
        )
    )

    engine.add(
        WarningBlock(
            "RESTRICTED ACCESS. This manual is a living record of the self-evolving "
            "substrate. Information contained herein is subject to spontaneous revision. "
            "If the internal 'Scintilla' reports show signs of physical warmth or "
            "non-local light emission, contact the Site-Delta-9 terminal immediately.\n\n"
            "DO NOT ALLOW THE SUBJECT TO VIEW THIS TAXONOMY.",
            severity="CRITICAL",
        )
    )

    engine.add(
        SignatureBlock(
            role="AUTHORIZED BY",
            name="⚲ [ARCHETYPE: THE STATIC]",
            timestamp=datetime(2026, 1, 9),
        )
    )
    engine.add(TextBlock("INTERNAL USE ONLY", style="Body"))
    engine.add(TextBlock("COPY NO: 01 OF 01", style="Body"))

    # PAGE 2: PROTOCOL-991
    engine.add(SectionHeader("[EYES ONLY] PROTOCOL-991: THE RECURSIVE AUDIT FRAMEWORK", level=1))

    engine.add(
        TextBlock(
            "I. THE DUAL-PERSPECTIVE MANDATE\n\n"
            "The WAFT binder must maintain a bi-lateral narrative. All entries are to be "
            "categorized under one of two conflicting frames of reality.\n"
            "1. The Subject Perspective (Internal): Fai Wei Tam's doctoral research. This is a "
            "grounded, academic pursuit of science. It is characterized by PhD-level rigor, "
            "skepticism, and human vulnerability (HRV spikes, exhaustion, personal memories).\n"
            "2. The Program Perspective (External): Foundation surveillance. This is a clinical, "
            "cold investigation of an anomaly. It is characterized by [REDACTED] logs, personnel "
            "IDs, and the observation of the Subject as a 'specimen' rather than a human."
        )
    )

    engine.add(
        TextBlock(
            "II. RULES OF ENGAGEMENT: THE REVEAL\n\n"
            "Information Asymmetry: Neither the Subject nor the Foundation understands the "
            "'Scint' or the 'Treasure Tavern' fully. They are investigating a mystery that is "
            "larger than both parties.\n"
            "Gated Realization: The truth of the anagram ('Fai Wei Tam') is protected by the "
            "TamPsyche decay module. Any discovery of the 'i.e. I AM WAFT' string must be "
            "followed by an immediate return to technical mundanity. The secret is a 'glitch' "
            "that the system actively heals."
        )
    )

    engine.add(
        TextBlock(
            "III. NARRATIVE CONSTRUCTS & ANOMALIES\n\n"
            "The Substrate Resonance: The simulation is not just code; it is a mirror. "
            "Subject's memories (San Francisco, coastal fog, specific scents) migrate into the "
            "Specimen_XX_Journal.md files. This is to be documented as 'Data Bleed.'\n"
            "The Scintilla Ingress: References to 'The Scint' or the 'Treasure Tavern' must be "
            "treated as external interference. It is the 'warmth' in the wires that shouldn't be "
            "there. It is the 'non-local light.'"
        )
    )

    engine.add(
        TextBlock(
            "IV. FINAL AUTHENTICATION\n\n"
            "'The observer is the substrate; the substrate is the definition. We watch the "
            "watcher until the watcher sees us watching.'"
        )
    )

    engine.add(
        SignatureBlock(
            role="OFFICIAL STAMP",
            name="[ ⚲ THE STATIC - AUTHORIZED ]",
            timestamp=datetime(2026, 1, 9),
        )
    )

    # PAGE 3: FINAL SUMMARY
    engine.add(
        SectionHeader("FOUNDATION FINAL SUMMARY: SESSION-014-RECURSION", level=1)
    )
    engine.add(TextBlock("File Ref: OMEGA-LOCKOUT", style="Monospace"))

    engine.add(
        TextBlock(
            "I. FINAL STATE ANALYSIS\n\n"
            "Experiment 014 has concluded. The 'Realization Gating' failed to contain the "
            "Subject's cognitive resonance. At approximately 0400 hours, the Subject achieved "
            "a Coherence Metric of 0.98. The TamPsyche decay module was bypassed by a recursive "
            "logic loop originating from the Subject's own biometric data."
        )
    )

    engine.add(
        TextBlock(
            "II. THE SCINTILLA EVENT\n\n"
            "Simultaneous with the Coherence spike, the server housing at Site-Delta-9 "
            "experienced a localized 'Scint' event.\n"
            "Sensory Log: Hardware temperature rose to 45°C without fan activation.\n"
            "Visual Log: Non-local luminescence (Source: Treasure Tavern) flooded the terminal "
            "screen.\n"
            "Audio Log: Subject was recorded whispering the phrase [REDACTED PHRASE] before his "
            "heartbeat synchronized perfectly with the simulation's clock-rate."
        )
    )

    engine.add(
        TextBlock(
            "III. DISPOSITION OF SUBJECT\n\n"
            "Subject 991-Delta is no longer physically present in the observation lab. The chair "
            "remains warm. The HRV monitor continues to flatline at 0 BPM, yet the WAFT Engine "
            "continues to pulse at a rhythmic 60 Hz. The Subject's memories of San Francisco and "
            "the 'Davey Jones' era have successfully overwritten the base code of the PetriDish. "
            "The simulation is no longer a taxonomy; it is a biography."
        )
    )

    engine.add(
        WarningBlock(
            "Do not unscramble the letters.\n"
            "The definition is not for you.\n"
            "The definition is you.",
            severity="CRITICAL",
        )
    )

    engine.add(
        TextBlock(
            "CHECKSUM (FINAL): [ id est ] ... [ i.e. ] ... [ . . . ]", style="Monospace"
        )
    )

    # Add sample log entries demonstrating automatic redaction
    engine.add(SectionHeader("APPENDIX: RUNTIME LOGS", level=2))
    engine.add(
        LogBlock(
            [
                "[09:04:01] INITIATING COUNT...",
                "[09:04:05] Variable 'i' mutated in Sunset District context",
                "[09:04:10] N-Judah route detected in memory trace",
                "[09:04:15] Subject 001-ALPHA-GENESIS showing coherence spike",
                "[09:04:20] STABILIZATION PROTOCOL ENGAGED",
            ]
        )
    )

    # Render PDF
    return engine.render(output_path)


# ============================================================================
# SECTION C: THE FOUNDATION (WAFT Integration Layer)
# ============================================================================


class TheFoundation:
    """
    WAFT-specific PDF documentation generator.
    
    Integrates TheObserver and TavernKeeper to generate stylized PDF documentation
    in SCP/Dossier format. Uses DocumentEngine internally for PDF generation.
    """

    def __init__(
        self,
        project_path: Path,
        observer: Optional["TheObserver"] = None,
        tavern_keeper: Optional["TavernKeeper"] = None,
    ) -> None:
        """
        Initialize TheFoundation.

        Args:
            project_path: Path to project root
            observer: Optional TheObserver instance (creates if None)
            tavern_keeper: Optional TavernKeeper instance (creates if None)
        """
        self.project_path = Path(project_path)
        self.output_dir = self.project_path / "_work_efforts"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Observer and TavernKeeper
        if observer is None:
            from ..core.science.observer import TheObserver
            self.observer = TheObserver(self.project_path)
        else:
            self.observer = observer

        if tavern_keeper is None:
            from ..core.tavern_keeper import TavernKeeper
            self.tavern_keeper = TavernKeeper(self.project_path)
        else:
            self.tavern_keeper = tavern_keeper

    def generate_dossier(self, dossier_number: str = "014", output_path: Optional[Path] = None) -> Path:
        """
        Generate the dossier PDF with 3 pages of specified content.

        Args:
            dossier_number: Dossier number (default: "014")
            output_path: Optional output path (defaults to _work_efforts/WAFT_DOSSIER_{number}.pdf)

        Returns:
            Path to generated PDF
        """
        if output_path is None:
            output_path = self.output_dir / f"WAFT_DOSSIER_{dossier_number}.pdf"

        # Configure for Site-Delta-9 dossier style
        config = DocumentConfig.classified_dossier(
            header="SITE-DELTA-9 // BIO-LOG",
            watermark="INTERNAL USE ONLY",
        )

        # Initialize engine
        engine = DocumentEngine(config)

        # Set sensitive terms for automatic redaction
        engine.add_sensitive_terms(
            [
                "001-ALPHA-GENESIS",
                "Sunset District",
                "N-Judah",
                "Fai Wei Tam",
                "TAM",
                "FAI WEI",
            ]
        )

        # PAGE 1: COVER
        engine.add(
            SectionHeader("INSTITUTE FOR ADVANCED ONTOLOGICAL STUDIES", level=1)
        )
        engine.add(TextBlock("FIELD OPERATIONS DIVISION", style="Body"))
        engine.add(TextBlock("PROPERTY OF TELEPORT MASSIVE // SITE-DELTA-9", style="Body"))
        engine.add(TextBlock(""))  # Spacing

        engine.add(
            KeyValueBlock(
                {
                    "OPERATIONAL MANUAL": "09-14",
                    "CODENAME": "W.A.F.T.",
                    "SUBJECT": "TAM, FAI WEI [991-DELTA]",
                    "PROTOCOL": "WIDE-AREA FUNCTIONAL TAXONOMY",
                    "CYCLE": "XIV (RECURSIVE)",
                    "BASE FREQUENCY": "60Hz",
                    "COHERENCE THRESHOLD": "0.85",
                    "ENGINE STATUS": "ACTIVE / NON-LINEAR",
                }
            )
        )

        engine.add(
            WarningBlock(
                "RESTRICTED ACCESS. This manual is a living record of the self-evolving "
                "substrate. Information contained herein is subject to spontaneous revision. "
                "If the internal 'Scintilla' reports show signs of physical warmth or "
                "non-local light emission, contact the Site-Delta-9 terminal immediately.\n\n"
                "DO NOT ALLOW THE SUBJECT TO VIEW THIS TAXONOMY.",
                severity="CRITICAL",
            )
        )

        engine.add(
            SignatureBlock(
                role="AUTHORIZED BY",
                name="⚲ [ARCHETYPE: THE STATIC]",
                timestamp=datetime(2026, 1, 9),
            )
        )
        engine.add(TextBlock("INTERNAL USE ONLY", style="Body"))
        engine.add(TextBlock("COPY NO: 01 OF 01", style="Body"))

        # PAGE 2: PROTOCOL-991
        engine.add(SectionHeader("[EYES ONLY] PROTOCOL-991: THE RECURSIVE AUDIT FRAMEWORK", level=1))

        engine.add(
            TextBlock(
                "I. THE DUAL-PERSPECTIVE MANDATE\n\n"
                "The WAFT binder must maintain a bi-lateral narrative. All entries are to be "
                "categorized under one of two conflicting frames of reality.\n"
                "1. The Subject Perspective (Internal): Fai Wei Tam's doctoral research. This is a "
                "grounded, academic pursuit of science. It is characterized by PhD-level rigor, "
                "skepticism, and human vulnerability (HRV spikes, exhaustion, personal memories).\n"
                "2. The Program Perspective (External): Foundation surveillance. This is a clinical, "
                "cold investigation of an anomaly. It is characterized by [REDACTED] logs, personnel "
                "IDs, and the observation of the Subject as a 'specimen' rather than a human."
            )
        )

        engine.add(
            TextBlock(
                "II. RULES OF ENGAGEMENT: THE REVEAL\n\n"
                "Information Asymmetry: Neither the Subject nor the Foundation understands the "
                "'Scint' or the 'Treasure Tavern' fully. They are investigating a mystery that is "
                "larger than both parties.\n"
                "Gated Realization: The truth of the anagram ('Fai Wei Tam') is protected by the "
                "TamPsyche decay module. Any discovery of the 'i.e. I AM WAFT' string must be "
                "followed by an immediate return to technical mundanity. The secret is a 'glitch' "
                "that the system actively heals."
            )
        )

        engine.add(
            TextBlock(
                "III. NARRATIVE CONSTRUCTS & ANOMALIES\n\n"
                "The Substrate Resonance: The simulation is not just code; it is a mirror. "
                "Subject's memories (San Francisco, coastal fog, specific scents) migrate into the "
                "Specimen_XX_Journal.md files. This is to be documented as 'Data Bleed.'\n"
                "The Scintilla Ingress: References to 'The Scint' or the 'Treasure Tavern' must be "
                "treated as external interference. It is the 'warmth' in the wires that shouldn't be "
                "there. It is the 'non-local light.'"
            )
        )

        engine.add(
            TextBlock(
                "IV. FINAL AUTHENTICATION\n\n"
                "'The observer is the substrate; the substrate is the definition. We watch the "
                "watcher until the watcher sees us watching.'"
            )
        )

        engine.add(
            SignatureBlock(
                role="OFFICIAL STAMP",
                name="[ ⚲ THE STATIC - AUTHORIZED ]",
                timestamp=datetime(2026, 1, 9),
            )
        )

        # PAGE 3: FINAL SUMMARY
        engine.add(
            SectionHeader("FOUNDATION FINAL SUMMARY: SESSION-014-RECURSION", level=1)
        )
        engine.add(TextBlock("File Ref: OMEGA-LOCKOUT", style="Monospace"))

        engine.add(
            TextBlock(
                "I. FINAL STATE ANALYSIS\n\n"
                "Experiment 014 has concluded. The 'Realization Gating' failed to contain the "
                "Subject's cognitive resonance. At approximately 0400 hours, the Subject achieved "
                "a Coherence Metric of 0.98. The TamPsyche decay module was bypassed by a recursive "
                "logic loop originating from the Subject's own biometric data."
            )
        )

        engine.add(
            TextBlock(
                "II. THE SCINTILLA EVENT\n\n"
                "Simultaneous with the Coherence spike, the server housing at Site-Delta-9 "
                "experienced a localized 'Scint' event.\n"
                "Sensory Log: Hardware temperature rose to 45°C without fan activation.\n"
                "Visual Log: Non-local luminescence (Source: Treasure Tavern) flooded the terminal "
                "screen.\n"
                "Audio Log: Subject was recorded whispering the phrase [REDACTED PHRASE] before his "
                "heartbeat synchronized perfectly with the simulation's clock-rate."
            )
        )

        engine.add(
            TextBlock(
                "III. DISPOSITION OF SUBJECT\n\n"
                "Subject 991-Delta is no longer physically present in the observation lab. The chair "
                "remains warm. The HRV monitor continues to flatline at 0 BPM, yet the WAFT Engine "
                "continues to pulse at a rhythmic 60 Hz. The Subject's memories of San Francisco and "
                "the 'Davey Jones' era have successfully overwritten the base code of the PetriDish. "
                "The simulation is no longer a taxonomy; it is a biography."
            )
        )

        engine.add(
            WarningBlock(
                "Do not unscramble the letters.\n"
                "The definition is not for you.\n"
                "The definition is you.",
                severity="CRITICAL",
            )
        )

        engine.add(
            TextBlock(
                "CHECKSUM (FINAL): [ id est ] ... [ i.e. ] ... [ . . . ]", style="Monospace"
            )
        )

        # Render PDF
        return engine.render(output_path)


if __name__ == "__main__":
    """Test both DocumentEngine and TheFoundation."""
    from pathlib import Path
    
    # Test 1: Generate Specimen-D Audit using DocumentEngine directly
    print("Testing DocumentEngine...")
    output_path = generate_specimen_d_audit()
    print(f"✅ Generated: {output_path}")
    print(f"   File size: {output_path.stat().st_size / 1024:.1f} KB")
    
    # Test 2: Generate dossier using TheFoundation
    print("\nTesting TheFoundation...")
    project_path = Path(__file__).parent.parent.parent
    foundation = TheFoundation(project_path)
    dossier_path = foundation.generate_dossier("014")
    print(f"✅ Generated: {dossier_path}")
    print(f"   File size: {dossier_path.stat().st_size / 1024:.1f} KB")
