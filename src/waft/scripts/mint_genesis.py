#!/usr/bin/env python3
"""
Mint Genesis Artifact: Timeline 001 Initialization Report

Site-Delta-9 Standard: A document that looks like it belongs in a sealed binder.
Canvas approach: Draw graphics first, then overlay text.
"""

import json
import subprocess
from pathlib import Path

try:
    from fpdf import FPDF
except ImportError:
    raise ImportError("fpdf2 is required. Install with: pip install fpdf2>=2.7.0")


def mint_genesis_artifact() -> Path:
    """Generate the Genesis Artifact PDF using canvas/graphics approach."""
    # Load configuration
    config_path = Path(__file__).parent.parent / "config" / "tam_origin_config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = json.load(f)
    
    # Output path
    output_path = Path(__file__).parent.parent.parent.parent / "_fracture" / "ARTIFACT_001_GENESIS.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create PDF with A4 page
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()
    
    page_width = 210  # A4 width in mm
    page_height = 297  # A4 height in mm
    
    # ============================================================================
    # 1. THE "CONTAINMENT" BORDER (Graphics First)
    # ============================================================================
    
    # Top Bar: Solid BLACK rectangle (0,0 to width, 25mm height)
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(0, 0, page_width, 25, style="F")
    
    # Hazard Strip: DARK RED (RGB: 180, 0, 0) rectangle (width, 8mm height)
    hazard_y = 25
    pdf.set_fill_color(180, 0, 0)
    pdf.rect(0, hazard_y, page_width, 8, style="F")
    
    # Bottom Bar: Solid BLACK rectangle (0, height-15mm to width, height)
    bottom_bar_y = page_height - 15
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(0, bottom_bar_y, page_width, 15, style="F")
    
    # ============================================================================
    # 2. THE HEADER (Typography)
    # ============================================================================
    
    # Top Text (Inside Black Bar): "INSTITUTE FOR ADVANCED ONTOLOGICAL STUDIES"
    # Font: Helvetica/Arial, Bold, 14pt, White
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 14)
    # Center vertically in black bar (25mm / 2 = 12.5mm, adjust for text height)
    text_y = 12.5 - (14 / 2)  # Approximate vertical centering
    pdf.set_xy(0, text_y)
    pdf.cell(page_width, 14, "INSTITUTE FOR ADVANCED ONTOLOGICAL STUDIES", align="C")
    
    # Hazard Text (Inside Red Strip): "WARNING: ONTOLOGICAL HAZARD // EYES ONLY"
    # Font: Courier, Bold, 10pt, White
    pdf.set_font("Courier", "B", 10)
    hazard_text_y = hazard_y + 4 - (10 / 2)  # Center in 8mm strip
    pdf.set_xy(0, hazard_text_y)
    pdf.cell(page_width, 10, "WARNING: ONTOLOGICAL HAZARD // EYES ONLY", align="C")
    
    # Reset text color to black for rest of document
    pdf.set_text_color(0, 0, 0)
    
    # ============================================================================
    # 3. THE DATA BLOCK (The "Inverted" Look)
    # ============================================================================
    
    # Location: Y=60mm
    data_block_y = 60
    data_block_width = 170  # Centered: (210 - 170) / 2 = 20mm margin
    data_block_height = 40
    data_block_x = (page_width - data_block_width) / 2  # Center horizontally
    
    # Background: DARK GREY (RGB: 50, 50, 50) rectangle
    pdf.set_fill_color(50, 50, 50)
    pdf.rect(data_block_x, data_block_y, data_block_width, data_block_height, style="F")
    
    # Content: White Courier Text inside box
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Courier", "", 10)
    
    # Position text inside box (with padding)
    text_x = data_block_x + 5
    text_y = data_block_y + 8
    line_height = 8
    
    pdf.set_xy(text_x, text_y)
    pdf.cell(0, line_height, f"SUBJECT:      991-DELTA (\"TAM\")", ln=1)
    
    pdf.set_xy(text_x, text_y + line_height)
    pdf.cell(0, line_height, f"TIMELINE ID:   {config_data['timeline_id']}", ln=1)
    
    pdf.set_xy(text_x, text_y + (line_height * 2))
    pdf.cell(0, line_height, f"SOUL SIG:      [{config_data['soul_signature']}]", ln=1)
    
    pdf.set_xy(text_x, text_y + (line_height * 3))
    pdf.cell(0, line_height, f"FRACTURE:      [{config_data['fracture_point']}]", ln=1)
    
    # Reset text color to black
    pdf.set_text_color(0, 0, 0)
    
    # ============================================================================
    # 4. THE NARRATIVE BODY (The "Report" Look)
    # ============================================================================
    
    # Location: Y=110mm
    narrative_y = 110
    narrative_width = 170  # Same width as data block
    narrative_x = (page_width - narrative_width) / 2  # Centered
    
    # Font: Times New Roman (or serif variant), 12pt, Black
    pdf.set_font("Times", "", 12)
    pdf.set_text_color(0, 0, 0)
    
    # Content: Justified text block
    narrative_text = (
        "The simulation has successfully fractured from the main trunk. "
        "Subject 991-DELTA is currently dormant within the San Francisco Construct. "
        "Local reality parameters are stable. The Karma economy is currently offline "
        "awaiting the Chitragupta Protocol."
    )
    
    pdf.set_xy(narrative_x, narrative_y)
    # Use multi_cell with justified alignment
    pdf.multi_cell(narrative_width, 6, narrative_text, align="J")
    
    # ============================================================================
    # 5. THE STAMP (Visual Anchor)
    # ============================================================================
    
    # Location: Bottom Right, above the footer bar
    # Style: Courier, Bold, 16pt, RED
    pdf.set_font("Courier", "B", 16)
    pdf.set_text_color(200, 0, 0)  # RED
    
    stamp_text = "ANCHORED: v0.3.1"
    stamp_width = pdf.get_string_width(stamp_text)
    stamp_x = page_width - 20 - stamp_width  # 20mm from right edge
    stamp_y = bottom_bar_y - 15  # 15mm above bottom bar
    
    # Try to rotate slightly (15 degrees) if rotation is supported
    # Note: fpdf2 rotation requires different approach - using text at angle
    # For now, place it normally but make it prominent
    pdf.set_xy(stamp_x, stamp_y)
    pdf.cell(0, 16, stamp_text, align="R")
    
    # ============================================================================
    # SAVE PDF
    # ============================================================================
    
    pdf.output(str(output_path))
    
    print(f"✅ Genesis Artifact minted (Site-Delta-9 Standard): {output_path}")
    return output_path


def open_pdf(filepath: Path) -> None:
    """Open PDF file using system default application."""
    import platform
    
    system = platform.system()
    if system == "Darwin":  # macOS
        subprocess.call(("open", str(filepath)))
    elif system == "Linux":
        subprocess.call(("xdg-open", str(filepath)))
    elif system == "Windows":
        import os
        os.startfile(str(filepath))
    else:
        print(f"⚠️  Cannot auto-open PDF on {system}. Please open manually: {filepath}")


if __name__ == "__main__":
    print("🔨 Minting Genesis Artifact (Site-Delta-9 Standard)...")
    pdf_path = mint_genesis_artifact()
    print(f"📄 PDF generated: {pdf_path}")
    print("🚀 Opening PDF...")
    open_pdf(pdf_path)
    print("✅ Complete!")
