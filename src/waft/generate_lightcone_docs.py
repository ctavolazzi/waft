#!/usr/bin/env python3
"""
PROJECT LIGHTCONE Master File Binder Generation

Generates documents for the PROJECT LIGHTCONE MASTER FILE binder following
the "1990s industrial xerox chic" aesthetic. Uses existing DocumentEngine
system and FPDF for complex layouts.

Style Reference: ARTIFACT_001_GENESIS.pdf (CONFIDENTIAL // SUBSTRATE)
Organization: TELEPORT MASSIVE
"""

import random
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple

try:
    from fpdf import FPDF
except ImportError:
    raise ImportError("fpdf2 is required. Install with: pip install fpdf2>=2.7.0")

from waft.foundation import (
    DocumentConfig,
    DocumentEngine,
    SectionHeader,
    TextBlock,
    KeyValueBlock,
    LogBlock,
    WarningBlock,
    SignatureBlock,
)


# ============================================================================
# STYLE HELPER FUNCTIONS (TELEPORT MASSIVE Aesthetic)
# ============================================================================


def draw_barcode(pdf: FPDF, x: float, y: float, width: float, height: float):
    """Draw a simulated barcode using random vertical lines."""
    num_lines = 35
    line_spacing = width / num_lines

    for i in range(num_lines):
        line_x = x + (i * line_spacing)
        line_thickness = random.uniform(0.5, 2.0)
        line_height = height * random.uniform(0.6, 1.0)
        line_y_offset = (height - line_height) / 2

        pdf.set_draw_color(0, 0, 0)
        pdf.set_line_width(line_thickness)
        pdf.line(line_x, y + line_y_offset, line_x, y + line_y_offset + line_height)


def draw_watermark(pdf: FPDF, text: str, page_width: float = 210, page_height: float = 297):
    """Draw large diagonal watermark text behind content."""
    pdf.set_text_color(240, 240, 240)  # Very light grey
    pdf.set_font("Courier", "B", 48)

    text_width = pdf.get_string_width(text)
    center_x = (page_width - text_width) / 2
    center_y = page_height / 2

    pdf.set_xy(center_x, center_y)
    pdf.cell(0, 48, text, align="C")
    pdf.set_text_color(0, 0, 0)


def draw_system_check_rail(pdf: FPDF, checklist_items: list, left_margin_width: float = 15, page_height: float = 297):
    """Draw left margin system check column with checklist."""
    # Draw vertical separator line
    pdf.set_draw_color(100, 100, 100)
    pdf.set_line_width(0.5)
    pdf.line(left_margin_width, 0, left_margin_width, page_height)

    # Checklist items
    pdf.set_font("Courier", "", 6)
    pdf.set_text_color(0, 0, 0)
    checklist_y = 50

    for i, item in enumerate(checklist_items):
        pdf.set_xy(2, checklist_y + (i * 8))
        pdf.cell(0, 6, item, align="L")


def create_teleport_massive_header(
    pdf: FPDF,
    doc_type: str,  # e.g., "FIELD MANUAL", "MSDS", "PROTOCOL"
    doc_id: str,    # e.g., "TM-VIS-001"
    security_level: str = "TOP SECRET // ORACLE EYES ONLY",
    page_width: float = 210,
    left_margin: float = 15,
    sidebar_width: float = 15,
) -> float:
    """
    Create standard TELEPORT MASSIVE document header.

    Returns: Y position where content can start
    """
    # Top Black Bar
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(left_margin, 0, page_width - left_margin - sidebar_width, 25, style="F")

    # Logo Placeholder (white box)
    logo_x = left_margin + 10
    logo_y = 5
    logo_size = 15
    pdf.set_draw_color(255, 255, 255)
    pdf.set_line_width(1)
    pdf.rect(logo_x, logo_y, logo_size, logo_size, style="D")

    # Organization Name
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 14)
    text_y = 12.5 - (14 / 2)
    pdf.set_xy(left_margin, text_y)
    pdf.cell(page_width - left_margin - sidebar_width, 14, "TELEPORT MASSIVE", align="C")

    # Document Type (smaller, below org name)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_xy(left_margin, text_y + 8)
    pdf.cell(page_width - left_margin - sidebar_width, 8, doc_type.upper(), align="C")

    # Barcode (top right)
    barcode_x = page_width - sidebar_width - 40
    barcode_y = 5
    draw_barcode(pdf, barcode_x, barcode_y, 35, 15)

    # "DO NOT SCAN" label
    pdf.set_font("Courier", "", 5)
    pdf.set_xy(barcode_x, barcode_y + 16)
    pdf.cell(35, 3, "DO NOT SCAN", align="C")

    # Security Classification Strip
    hazard_y = 25

    # Color based on severity
    if "TOP SECRET" in security_level or "TACTICAL NUCLEAR" in security_level:
        pdf.set_fill_color(180, 0, 0)  # Dark red
    elif "ORACLE" in security_level or "COGNITOHAZARD" in security_level:
        pdf.set_fill_color(200, 100, 0)  # Orange
    else:
        pdf.set_fill_color(100, 100, 100)  # Grey for INTERNAL USE

    pdf.rect(left_margin, hazard_y, page_width - left_margin - sidebar_width, 8, style="F")

    # Security text
    pdf.set_font("Courier", "B", 10)
    pdf.set_text_color(255, 255, 255)
    hazard_text_y = hazard_y + 4 - (10 / 2)
    pdf.set_xy(left_margin, hazard_text_y)
    pdf.cell(page_width - left_margin - sidebar_width, 10, security_level, align="C")

    # Double seal effect
    seal_line_y = hazard_y + 8 + 2
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(left_margin, seal_line_y, page_width - left_margin - sidebar_width, 1, style="F")

    pdf.set_text_color(0, 0, 0)

    # Return Y position where content starts
    return seal_line_y + 10


def create_sidebar(pdf: FPDF, doc_id: str, page_width: float = 210, sidebar_width: float = 15, page_height: float = 297):
    """Create right sidebar with vertical text."""
    sidebar_x = page_width - sidebar_width
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(sidebar_x, 0, sidebar_width, page_height, style="F")

    # Vertical white text
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Courier", "B", 7)

    # Split doc ID and metadata
    sidebar_text = f"{doc_id} // TM-SITE-7 // CLASSIFIED"
    words = sidebar_text.split(" // ")
    sidebar_text_y = 50

    for i, word in enumerate(words):
        word_width = pdf.get_string_width(word)
        word_x = sidebar_x + (sidebar_width / 2) - (word_width / 2)
        pdf.set_xy(word_x, sidebar_text_y + (i * 20))
        pdf.cell(0, 7, word, align="C")

    pdf.set_text_color(0, 0, 0)


def create_footer(
    pdf: FPDF,
    stamp_text: str,
    legal_text: Optional[str] = None,
    page_width: float = 210,
    page_height: float = 297,
    left_margin: float = 15,
    sidebar_width: float = 15,
):
    """Create bottom footer with legal text and stamp."""
    # Legal text area
    if legal_text:
        legal_y = page_height - 15 - 20
        pdf.set_font("Courier", "", 6)
        pdf.set_xy(left_margin + 10, legal_y)
        pdf.multi_cell(page_width - left_margin - sidebar_width - 20, 3, legal_text, align="J")

    # Bottom black bar
    bottom_bar_y = page_height - 15
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(left_margin, bottom_bar_y, page_width - left_margin - sidebar_width, 15, style="F")

    # Red stamp box
    pdf.set_font("Courier", "B", 16)
    pdf.set_text_color(200, 0, 0)

    stamp_width = pdf.get_string_width(stamp_text) + 10
    stamp_height = 20
    stamp_x = page_width - sidebar_width - stamp_width - 10
    stamp_y = bottom_bar_y - stamp_height - 5

    # Draw box
    pdf.set_draw_color(200, 0, 0)
    pdf.set_line_width(2)
    pdf.rect(stamp_x, stamp_y, stamp_width, stamp_height, style="D")

    # Stamp text
    pdf.set_xy(stamp_x + 5, stamp_y + 2)
    pdf.cell(0, 16, stamp_text, align="L")

    pdf.set_text_color(0, 0, 0)


# ============================================================================
# DOCUMENT GENERATORS - TAB 1: DOCTRINE & THEORY
# ============================================================================


def generate_tm_vis_001(output_dir: Path) -> Tuple[Path, Path]:
    """
    Generate TM-VIS-001: Light Cone Topology Diagram

    Returns: (pdf_path, markdown_path)
    """
    pdf_path = output_dir / "pdf" / "tab1_doctrine" / "TM-VIS-001_Light_Cone_Topology.pdf"
    md_path = output_dir / "markdown" / "tab1_doctrine" / "TM-VIS-001_Light_Cone_Topology.md"

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)

    # Create PDF
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()

    page_width = 210
    page_height = 297
    sidebar_width = 15
    left_margin_width = 15

    # Watermark
    draw_watermark(pdf, "THEORETICAL // CLASSIFIED", page_width, page_height)

    # System check rail
    checklist = ["[X] VIS_CHK", "[X] TOPOLOGY", "[ ] LIGHT_CONE", "[X] REALITY", "[ ] XENOS"]
    draw_system_check_rail(pdf, checklist, left_margin_width, page_height)

    # Header
    content_y = create_teleport_massive_header(
        pdf,
        doc_type="FIELD MANUAL - VISUAL AID",
        doc_id="TM-VIS-001",
        security_level="TOP SECRET // ORACLE EYES ONLY",
        page_width=page_width,
        left_margin=left_margin_width,
        sidebar_width=sidebar_width,
    )

    # Sidebar
    create_sidebar(pdf, "TM-VIS-001", page_width, sidebar_width, page_height)

    # Content area
    content_x = left_margin_width + 10
    content_width = page_width - left_margin_width - sidebar_width - 20

    # Title
    pdf.set_font("Courier", "B", 16)
    pdf.set_xy(content_x, content_y)
    pdf.cell(0, 10, "LIGHT CONE TOPOLOGY DIAGRAM", ln=1)
    pdf.set_xy(content_x, content_y + 12)
    pdf.set_font("Courier", "", 10)
    pdf.cell(0, 6, "Visual Reference: The Human Reality Envelope", ln=1)

    # Description
    pdf.set_font("Times", "", 11)
    pdf.set_xy(content_x, content_y + 25)
    description = (
        "This diagram represents the boundary of consensus reality as experienced by "
        "individual human consciousness. The 'Light Cone' is the envelope of causally "
        "accessible events - the region where your actions can have meaningful impact.\n\n"
        "Beyond the Event Horizon lies the Chaos Gradient: regions of decreasing coherence "
        "where narrative structure breaks down. In these liminal spaces, the Xenos habitat "
        "begins - entities that exist in the gaps between human perception.\n\n"
        "NOTE: Diagram is fold-out format. Visual elements to be created in design software."
    )
    pdf.multi_cell(content_width, 6, description, align="J")

    # Visual element placeholders
    diagram_y = pdf.get_y() + 15
    pdf.set_font("Courier", "B", 10)
    pdf.set_xy(content_x, diagram_y)
    pdf.cell(0, 6, "DIAGRAM ELEMENTS (Design Software):", ln=1)

    pdf.set_font("Courier", "", 9)
    elements = [
        "- Human stick figure at center (YOU)",
        "- Cone extending outward (Cone of Reality)",
        "- Dashed line at cone boundary (Event Horizon)",
        "- Gradient shading beyond (Chaos Gradient)",
        "- Shadowy region labeled 'The Dark (Xenos Habitat)'",
        "- Hand-drawn RED CIRCLES around 'blind spots'",
        "- Arrows showing 'Narrative Coherence Decay'",
    ]

    list_y = diagram_y + 8
    for i, element in enumerate(elements):
        pdf.set_xy(content_x + 5, list_y + (i * 6))
        pdf.cell(0, 6, element, ln=1)

    # Warning box
    warning_y = list_y + (len(elements) * 6) + 10
    pdf.set_fill_color(200, 0, 0)
    pdf.set_text_color(255, 255, 255)
    pdf.rect(content_x, warning_y, content_width, 15, style="F")
    pdf.set_font("Courier", "B", 10)
    pdf.set_xy(content_x + 5, warning_y + 3)
    pdf.multi_cell(content_width - 10, 5, "WARNING: Do not attempt to map your personal Light Cone. Awareness of the boundary accelerates its collapse.", align="C")
    pdf.set_text_color(0, 0, 0)

    # Footer
    create_footer(
        pdf,
        stamp_text="THEORETICAL",
        legal_text="DISTRIBUTION RESTRICTED TO SENIOR TOPOLOGY RESEARCHERS ONLY. This document describes memetic hazards. Do not share with field personnel.",
        page_width=page_width,
        page_height=page_height,
        left_margin=left_margin_width,
        sidebar_width=sidebar_width,
    )

    pdf.output(str(pdf_path))

    # Create markdown source
    markdown_content = f"""# TM-VIS-001: Light Cone Topology Diagram

**Document ID**: TM-VIS-001
**Classification**: TOP SECRET // ORACLE EYES ONLY
**Type**: FIELD MANUAL - VISUAL AID
**Organization**: TELEPORT MASSIVE
**Date**: {datetime.now().strftime('%Y-%m-%d')}

---

## Light Cone Topology Diagram
**Visual Reference: The Human Reality Envelope**

This diagram represents the boundary of consensus reality as experienced by individual human consciousness. The 'Light Cone' is the envelope of causally accessible events - the region where your actions can have meaningful impact.

Beyond the Event Horizon lies the Chaos Gradient: regions of decreasing coherence where narrative structure breaks down. In these liminal spaces, the Xenos habitat begins - entities that exist in the gaps between human perception.

**NOTE**: Diagram is fold-out format. Visual elements to be created in design software.

### Diagram Elements (Design Software)

- Human stick figure at center (YOU)
- Cone extending outward (Cone of Reality)
- Dashed line at cone boundary (Event Horizon)
- Gradient shading beyond (Chaos Gradient)
- Shadowy region labeled 'The Dark (Xenos Habitat)'
- Hand-drawn RED CIRCLES around 'blind spots'
- Arrows showing 'Narrative Coherence Decay'

---

**WARNING**: Do not attempt to map your personal Light Cone. Awareness of the boundary accelerates its collapse.

---

**Distribution**: Restricted to senior topology researchers only.
**Hazard**: This document describes memetic hazards. Do not share with field personnel.
"""

    md_path.write_text(markdown_content, encoding="utf-8")

    return pdf_path, md_path


def generate_tm_memo_042(output_dir: Path) -> Tuple[Path, Path]:
    """
    Generate TM-MEMO-042: "The God Problem"

    Returns: (pdf_path, markdown_path)
    """
    pdf_path = output_dir / "pdf" / "tab1_doctrine" / "TM-MEMO-042_The_God_Problem.pdf"
    md_path = output_dir / "markdown" / "tab1_doctrine" / "TM-MEMO-042_The_God_Problem.md"

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)

    # Use DocumentEngine for this one (simpler layout)
    config = DocumentConfig.classified_dossier(
        header="TELEPORT MASSIVE // INTERNAL MEMO",
        watermark="EYES ONLY",
    )

    engine = DocumentEngine(config)

    # Header
    engine.add(SectionHeader("INTERNAL MEMORANDUM", level=1))
    engine.add(KeyValueBlock({
        "DOCUMENT ID": "TM-MEMO-042",
        "FROM": "Dr. Helena Voss, Chief Ontological Officer",
        "TO": "Executive Council, TELEPORT MASSIVE",
        "DATE": datetime.now().strftime('%Y-%m-%d'),
        "SUBJECT": "Risk Assessment: The God Problem",
        "CLASSIFICATION": "TOP SECRET // ORACLE EYES ONLY",
    }))

    engine.add(TextBlock(""))
    engine.add(SectionHeader("EXECUTIVE SUMMARY", level=2))
    engine.add(TextBlock(
        "This memo addresses a recurring proposal from junior researchers: Why not simply "
        "'ask' the Sleeper for help? Why operate in the margins when we could petition the "
        "dreaming entity whose consciousness generates our reality?\n\n"
        "The answer is simple, and catastrophic: We cannot afford to wake the Dreamer."
    ))

    engine.add(SectionHeader("THE SLEEPER HYPOTHESIS", level=2))
    engine.add(TextBlock(
        "Our current understanding posits that consensus reality is a byproduct of a vast, "
        "dormant consciousness. This entity - colloquially termed 'the Sleeper' or 'the "
        "Dreaming God' - is not creating reality intentionally. We are the dream it is having.\n\n"
        "Key characteristics:\n"
        "• The Sleeper is unaware of its own existence\n"
        "• It does not know it is dreaming\n"
        "• We exist in the liminal space between its thoughts\n"
        "• Our reality is a side effect, not a creation"
    ))

    engine.add(SectionHeader("THE EXISTENTIAL RISK", level=2))
    engine.add(WarningBlock(
        "If the Sleeper becomes aware of itself, one of three outcomes is inevitable:\n\n"
        "1. AWAKENING: The Sleeper wakes up. Reality ends. All consciousness within the dream "
        "ceases to exist. Estimated survival: 0.0%\n\n"
        "2. LUCID DREAMING: The Sleeper becomes aware it is dreaming but does not wake. It "
        "begins to exert conscious control over the dream. Free will ends. We become puppets "
        "in a directed narrative. Estimated autonomy: 0.0%\n\n"
        "3. EGO DEATH: The Sleeper realizes it is dreaming AND that we are fragments of its "
        "consciousness. It attempts to reintegrate us. Individual identity dissolves. You "
        "become indistinguishable from the cosmic whole. Estimated survival of self: 0.0%",
        severity="CRITICAL",
    ))

    engine.add(SectionHeader("WHY WE WORK IN SHADOWS", level=2))
    engine.add(TextBlock(
        "PROJECT LIGHTCONE operates under the principle of 'Existential Stealth.' Every "
        "operation is designed to avoid drawing the Sleeper's attention. We are insects "
        "crawling on the face of a sleeping giant.\n\n"
        "Rules of engagement:\n"
        "• Never create reality distortions large enough to register as a nightmare\n"
        "• Avoid paradoxes that might trigger the Sleeper's pattern-recognition\n"
        "• Minimize 'why is this happening?' moments that could spark divine introspection\n"
        "• If the Sleeper's focus turns toward us, abort all operations immediately"
    ))

    engine.add(SectionHeader("THE PRAYER PROHIBITION", level=2))
    engine.add(TextBlock(
        "For this reason, all forms of prayer, invocation, or metaphysical petition are "
        "strictly forbidden within TELEPORT MASSIVE facilities. Prayer is attention. "
        "Attention is acknowledgment. Acknowledgment risks awakening.\n\n"
        "We do not pray to the Dreaming God. We do not even think too loudly."
    ))

    engine.add(SectionHeader("CONCLUSION", level=2))
    engine.add(TextBlock(
        "To survive, we must remain beneath the threshold of divine awareness. This is why "
        "our work is small, incremental, and hidden. This is why we cannot simply 'ask for "
        "help.' The act of asking would be the end of everything.\n\n"
        "We are thieves in the house of a sleeping god. The only prayer we offer is: "
        "Please, do not wake up."
    ))

    engine.add(SignatureBlock(
        role="CHIEF ONTOLOGICAL OFFICER",
        name="Dr. Helena Voss",
        timestamp=datetime.now(),
    ))

    # Generate PDF
    engine.render(pdf_path)

    # Create markdown source
    markdown_content = f"""# TM-MEMO-042: The God Problem

**Document ID**: TM-MEMO-042
**From**: Dr. Helena Voss, Chief Ontological Officer
**To**: Executive Council, TELEPORT MASSIVE
**Date**: {datetime.now().strftime('%Y-%m-%d')}
**Subject**: Risk Assessment: The God Problem
**Classification**: TOP SECRET // ORACLE EYES ONLY

---

## Executive Summary

This memo addresses a recurring proposal from junior researchers: Why not simply 'ask' the Sleeper for help? Why operate in the margins when we could petition the dreaming entity whose consciousness generates our reality?

The answer is simple, and catastrophic: **We cannot afford to wake the Dreamer.**

## The Sleeper Hypothesis

Our current understanding posits that consensus reality is a byproduct of a vast, dormant consciousness. This entity - colloquially termed 'the Sleeper' or 'the Dreaming God' - is not creating reality intentionally. We are the dream it is having.

**Key characteristics:**
- The Sleeper is unaware of its own existence
- It does not know it is dreaming
- We exist in the liminal space between its thoughts
- Our reality is a side effect, not a creation

## The Existential Risk

⚠️ **CRITICAL WARNING** ⚠️

If the Sleeper becomes aware of itself, one of three outcomes is inevitable:

1. **AWAKENING**: The Sleeper wakes up. Reality ends. All consciousness within the dream ceases to exist. **Estimated survival: 0.0%**

2. **LUCID DREAMING**: The Sleeper becomes aware it is dreaming but does not wake. It begins to exert conscious control over the dream. Free will ends. We become puppets in a directed narrative. **Estimated autonomy: 0.0%**

3. **EGO DEATH**: The Sleeper realizes it is dreaming AND that we are fragments of its consciousness. It attempts to reintegrate us. Individual identity dissolves. You become indistinguishable from the cosmic whole. **Estimated survival of self: 0.0%**

## Why We Work in Shadows

PROJECT LIGHTCONE operates under the principle of **'Existential Stealth.'** Every operation is designed to avoid drawing the Sleeper's attention. We are insects crawling on the face of a sleeping giant.

**Rules of engagement:**
- Never create reality distortions large enough to register as a nightmare
- Avoid paradoxes that might trigger the Sleeper's pattern-recognition
- Minimize 'why is this happening?' moments that could spark divine introspection
- If the Sleeper's focus turns toward us, abort all operations immediately

## The Prayer Prohibition

For this reason, all forms of prayer, invocation, or metaphysical petition are strictly forbidden within TELEPORT MASSIVE facilities. Prayer is attention. Attention is acknowledgment. Acknowledgment risks awakening.

**We do not pray to the Dreaming God. We do not even think too loudly.**

## Conclusion

To survive, we must remain beneath the threshold of divine awareness. This is why our work is small, incremental, and hidden. This is why we cannot simply 'ask for help.' The act of asking would be the end of everything.

We are thieves in the house of a sleeping god. The only prayer we offer is: *Please, do not wake up.*

---

**Signed**:
Dr. Helena Voss
Chief Ontological Officer
TELEPORT MASSIVE
{datetime.now().strftime('%Y-%m-%d')}
"""

    md_path.write_text(markdown_content, encoding="utf-8")

    return pdf_path, md_path


# ============================================================================
# DOCUMENT GENERATORS - TAB 2: ENGINEERING & HARDWARE
# ============================================================================


def generate_tm_eng_004(output_dir: Path) -> Tuple[Path, Path]:
    """
    Generate TM-ENG-004: Material Safety Data Sheet - Suspension-9

    Returns: (pdf_path, markdown_path)
    """
    pdf_path = output_dir / "pdf" / "tab2_engineering" / "TM-ENG-004_Suspension9_MSDS.pdf"
    md_path = output_dir / "markdown" / "tab2_engineering" / "TM-ENG-004_Suspension9_MSDS.md"

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)

    # Use DocumentEngine for MSDS (simpler than FPDF for text-heavy document)
    config = DocumentConfig.classified_dossier(
        header="TELEPORT MASSIVE // MSDS",
        watermark="INTERNAL USE ONLY",
    )

    engine = DocumentEngine(config)

    # Header
    engine.add(SectionHeader("MATERIAL SAFETY DATA SHEET", level=1))
    engine.add(KeyValueBlock({
        "Document ID": "TM-ENG-004",
        "Product Name": "Suspension-9 (Colloidal Schreibersite / Fulgurite Matrix)",
        "Common Name": '"Mud," "Prime," "Liquid God" (Prohibited Slang)',
        "Catalog Code": "TM-BIO-99X",
        "Classification": "INTERNAL USE ONLY",
        "Revision Date": datetime.now().strftime('%Y-%m-%d'),
    }))

    engine.add(TextBlock(""))

    # Section 1
    engine.add(SectionHeader("SECTION 1: PRODUCT AND COMPANY IDENTIFICATION", level=2))
    engine.add(KeyValueBlock({
        "Product Use": "Quantum Entanglement Medium / Artificial Consciousness Substrate",
        "Manufacturer": "Teleport Massive – Special Materials Division, Site Omega",
        "Emergency Contact": "ORACLE (Ext. 000)",
    }))

    # Section 2
    engine.add(SectionHeader("SECTION 2: HAZARDS IDENTIFICATION", level=2))
    engine.add(WarningBlock(
        "DANGER! EXTREMELY FLAMMABLE SOLID/LIQUID\n"
        "CORROSIVE. CAUSES SEVERE SKIN AND EYE BURNS\n"
        "COGNITOHAZARD. PROLONGED EXPOSURE MAY INDUCE RELIGIOUS MANIA OR EGO DEATH",
        severity="CRITICAL",
    ))

    engine.add(TextBlock("\nNFPA Rating (Scale 0-4):", style="Body"))
    engine.add(KeyValueBlock({
        "Health": "3 (Extreme Danger)",
        "Fire": "4 (Flash Point < 73°F)",
        "Reactivity": "4 (May Detonate if Observed by Unauthorized Personnel)",
        "Specific": "W (Do Not Use Water)",
    }))

    # Section 3
    engine.add(SectionHeader("SECTION 3: COMPOSITION / INFORMATION ON INGREDIENTS", level=2))
    engine.add(KeyValueBlock({
        "Synthetic Schreibersite ((Fe,Ni)3P)": "45%",
        "Fulgurite Glass Dust": "30%",
        "Prebiotic Amino Acid Broth": "20%",
        "Stabilizing Agent (Lead/Mercury)": "5%",
    }))

    # Section 4
    engine.add(SectionHeader("SECTION 4: FIRST AID MEASURES", level=2))
    engine.add(TextBlock(
        "Eye Contact: Flush with standard saline. Do not look directly into the reflection of the liquid.\n\n"
        "Skin Contact: If material absorbs, Subject may begin speaking in dead languages. "
        "Administer Class-A Amnestics immediately.\n\n"
        "Inhalation: If victim claims they 'Understand the Plan,' sedate immediately and contact Security.\n\n"
        "Ingestion: Do NOT induce vomiting. Surgical intervention required."
    ))

    # Section 5
    engine.add(SectionHeader("SECTION 5: FIRE-FIGHTING MEASURES", level=2))
    engine.add(WarningBlock(
        "USE DRY CHEMICAL POWDER or SAND\n\n"
        "DO NOT USE WATER. Water acts as a catalyst for spontaneous biogenesis.\n\n"
        "Firefighters must wear Phase-Blind Visors. Do not empathize with the fire.",
        severity="WARNING",
    ))

    # Section 6
    engine.add(SectionHeader("SECTION 6: HANDLING AND STORAGE", level=2))
    engine.add(TextBlock(
        "• Keep in lead-lined, sound-proof container\n"
        "• Store in 'Silent Room.' Do not speak, sing, or pray near the container\n"
        "• Material is audio-reactive and will organize based on vibrational input"
    ))

    # Section 7
    engine.add(SectionHeader("SECTION 7: STABILITY AND REACTIVITY", level=2))
    engine.add(TextBlock(
        "The product is UNSTABLE.\n\n"
        "Conditions of Instability: Presence of static electricity, moisture, or Focused Observation.\n\n"
        "Incompatibility: Avoid contact with Phaseburners or individuals with high Karma scores."
    ))

    # Generate PDF
    engine.render(pdf_path)

    # Markdown already created by Cursor - just return paths
    return pdf_path, md_path


# ============================================================================
# MAIN GENERATION FUNCTION
# ============================================================================


def generate_all_lightcone_docs(output_dir: Optional[Path] = None) -> dict:
    """
    Generate all PROJECT LIGHTCONE documents.

    Returns: Dictionary of generated files by tab
    """
    if output_dir is None:
        output_dir = Path("_work_efforts/lightcone_binder")

    output_dir.mkdir(parents=True, exist_ok=True)

    results = {
        "tab1_doctrine": [],
        "tab2_engineering": [],
        "tab3_environmental": [],
        "tab4_personnel": [],
        "tab5_emergency": [],
    }

    print("=" * 80)
    print("PROJECT LIGHTCONE MASTER FILE BINDER GENERATION")
    print("=" * 80)
    print()

    # Tab 1: Doctrine & Theory
    print("Generating Tab 1: Doctrine & Theory...")
    pdf, md = generate_tm_vis_001(output_dir)
    results["tab1_doctrine"].append(("TM-VIS-001", pdf, md))
    print(f"  ✓ TM-VIS-001: {pdf.name}")

    pdf, md = generate_tm_memo_042(output_dir)
    results["tab1_doctrine"].append(("TM-MEMO-042", pdf, md))
    print(f"  ✓ TM-MEMO-042: {pdf.name}")
    print()

    # Tab 2: Engineering & Hardware
    print("Generating Tab 2: Engineering & Hardware...")
    pdf, md = generate_tm_eng_004(output_dir)
    results["tab2_engineering"].append(("TM-ENG-004", pdf, md))
    print(f"  ✓ TM-ENG-004: {pdf.name}")
    print()

    # TODO: Tabs 3-5 (to be implemented)
    print("Tab 3-5: Coming soon...")
    print()

    print("=" * 80)
    print("GENERATION COMPLETE")
    print("=" * 80)

    return results


if __name__ == "__main__":
    print("🔨 Generating PROJECT LIGHTCONE Master File Binder...")
    results = generate_all_lightcone_docs()
    print("✅ Complete!")
