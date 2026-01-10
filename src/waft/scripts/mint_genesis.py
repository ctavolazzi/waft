#!/usr/bin/env python3
"""
Mint Genesis Artifact: Timeline 001 Initialization Report

Level 4 Clearance: Maximalist bureaucratic aesthetic.
Dense, cluttered, official - a document that feels heavy with bureaucracy.
"""

import json
import subprocess
from pathlib import Path
import math

try:
    from fpdf import FPDF
except ImportError:
    raise ImportError("fpdf2 is required. Install with: pip install fpdf2>=2.7.0")


def mint_genesis_artifact() -> Path:
    """Generate the Genesis Artifact PDF with maximalist bureaucratic aesthetic."""
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
    # 1. THE "WATERMARK" LAYER (Draw First, Behind Everything)
    # ============================================================================
    
    # Massive, light grey text centered and rotated 45 degrees
    pdf.set_text_color(240, 240, 240)  # Very light grey
    pdf.set_font("Courier", "B", 48)
    watermark_text = "CONFIDENTIAL // SUBSTRATE"
    
    # Calculate center position
    text_width = pdf.get_string_width(watermark_text)
    center_x = (page_width - text_width) / 2
    center_y = page_height / 2
    
    # Rotate 45 degrees (fpdf2 doesn't support rotation directly, so we'll use a workaround)
    # For now, place it large and centered - rotation would require more complex math
    pdf.set_xy(center_x, center_y)
    pdf.cell(0, 48, watermark_text, align="C")
    
    # Reset text color
    pdf.set_text_color(0, 0, 0)
    
    # ============================================================================
    # 2. THE "SIDEBAR" (Technical Rail)
    # ============================================================================
    
    # 15mm wide vertical column on far right edge
    sidebar_width = 15
    sidebar_x = page_width - sidebar_width
    
    # Fill with black (from top black bar to bottom)
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(sidebar_x, 0, sidebar_width, page_height, style="F")
    
    # Vertical white text (rotated 90 degrees) - simulate with vertical positioning
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Courier", "B", 8)
    sidebar_text = "SITE-DELTA-9 // OMEGA-LOCKOUT // SEQ-001"
    
    # Position text vertically down the sidebar (simulating rotation)
    # Split text and position each character/word vertically
    words = sidebar_text.split(" // ")
    sidebar_text_y = 50
    for i, word in enumerate(words):
        pdf.set_xy(sidebar_x + 2, sidebar_text_y + (i * 15))
        # Write vertically by positioning each character
        pdf.cell(sidebar_width - 4, 8, word, align="C")
    
    # Reset text color
    pdf.set_text_color(0, 0, 0)
    
    # ============================================================================
    # 3. THE HEADER COMPLEX
    # ============================================================================
    
    # Top Black Bar: Solid BLACK rectangle (0,0 to width, 25mm height)
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(0, 0, page_width, 25, style="F")
    
    # Logo Placeholder: Hollow circle (15mm diameter) in top left
    logo_x = 10
    logo_y = 5
    logo_diameter = 15
    pdf.set_draw_color(255, 255, 255)  # White circle
    pdf.set_line_width(1)
    pdf.circle(logo_x + logo_diameter/2, logo_y + logo_diameter/2, logo_diameter/2, style="D")
    
    # Top Text (Inside Black Bar): "INSTITUTE FOR ADVANCED ONTOLOGICAL STUDIES"
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 14)
    text_y = 12.5 - (14 / 2)
    pdf.set_xy(0, text_y)
    pdf.cell(page_width, 14, "INSTITUTE FOR ADVANCED ONTOLOGICAL STUDIES", align="C")
    
    # Hazard Strip: DARK RED (RGB: 180, 0, 0) rectangle (width, 8mm height)
    hazard_y = 25
    pdf.set_fill_color(180, 0, 0)
    pdf.rect(0, hazard_y, page_width, 8, style="F")
    
    # Hazard Text (Inside Red Strip)
    pdf.set_font("Courier", "B", 10)
    hazard_text_y = hazard_y + 4 - (10 / 2)
    pdf.set_xy(0, hazard_text_y)
    pdf.cell(page_width, 10, "WARNING: ONTOLOGICAL HAZARD // EYES ONLY", align="C")
    
    # Second thin black line 2mm below Red Strip (double seal effect)
    seal_line_y = hazard_y + 8 + 2
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(0, seal_line_y, page_width, 1, style="F")  # 1mm thick line
    
    # Reset text color
    pdf.set_text_color(0, 0, 0)
    
    # ============================================================================
    # 4. THE DATA GRID (2x2 Grid of Black Boxes)
    # ============================================================================
    
    # Grid location: Y=50mm (below header complex)
    grid_y = 50
    grid_width = 170  # Total width (excluding sidebar)
    grid_height = 50  # Total height
    grid_x = (page_width - sidebar_width - grid_width) / 2  # Center in available space
    
    cell_width = grid_width / 2
    cell_height = grid_height / 2
    
    # Cell 1 (Top Left): SUBJECT: 991-DELTA
    cell1_x = grid_x
    cell1_y = grid_y
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(cell1_x, cell1_y, cell_width, cell_height, style="F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Courier", "B", 10)
    pdf.set_xy(cell1_x + 5, cell1_y + 15)
    pdf.cell(0, 8, "SUBJECT:", ln=1)
    pdf.set_xy(cell1_x + 5, cell1_y + 25)
    pdf.cell(0, 8, "991-DELTA", ln=1)
    
    # Thick white border between cells (vertical line)
    pdf.set_draw_color(255, 255, 255)
    pdf.set_line_width(2)
    pdf.line(cell1_x + cell_width, cell1_y, cell1_x + cell_width, cell1_y + grid_height)
    
    # Cell 2 (Top Right): TIMELINE: 001
    cell2_x = grid_x + cell_width
    cell2_y = grid_y
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(cell2_x, cell2_y, cell_width, cell_height, style="F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Courier", "B", 10)
    pdf.set_xy(cell2_x + 5, cell2_y + 15)
    pdf.cell(0, 8, "TIMELINE:", ln=1)
    pdf.set_xy(cell2_x + 5, cell2_y + 25)
    pdf.cell(0, 8, config_data['timeline_id'], ln=1)
    
    # Thick white border between rows (horizontal line)
    pdf.set_draw_color(255, 255, 255)
    pdf.set_line_width(2)
    pdf.line(grid_x, grid_y + cell_height, grid_x + grid_width, grid_y + cell_height)
    
    # Cell 3 (Bottom Left): STATUS: UN-AWAKENED
    cell3_x = grid_x
    cell3_y = grid_y + cell_height
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(cell3_x, cell3_y, cell_width, cell_height, style="F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Courier", "B", 10)
    pdf.set_xy(cell3_x + 5, cell3_y + 15)
    pdf.cell(0, 8, "STATUS:", ln=1)
    pdf.set_xy(cell3_x + 5, cell3_y + 25)
    pdf.cell(0, 8, "UN-AWAKENED", ln=1)
    
    # Cell 4 (Bottom Right): FRACTURE: [TIMESTAMP]
    cell4_x = grid_x + cell_width
    cell4_y = grid_y + cell_height
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(cell4_x, cell4_y, cell_width, cell_height, style="F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Courier", "B", 9)
    pdf.set_xy(cell4_x + 5, cell4_y + 12)
    pdf.cell(0, 7, "FRACTURE:", ln=1)
    pdf.set_xy(cell4_x + 5, cell4_y + 22)
    pdf.cell(0, 7, config_data['fracture_point'][:16], ln=1)  # Truncate if too long
    
    # Reset text color
    pdf.set_text_color(0, 0, 0)
    
    # ============================================================================
    # 5. THE NARRATIVE BODY (The "Typewriter" Look)
    # ============================================================================
    
    # Reference Line above body text
    narrative_start_y = grid_y + grid_height + 20
    pdf.set_font("Courier", "", 9)
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(grid_x, narrative_start_y)
    pdf.cell(0, 6, "REF: [FR-001-ORIGIN] // BY: THE ARCHITECT", align="L")
    
    # Narrative body text
    narrative_y = narrative_start_y + 10
    narrative_width = grid_width
    narrative_x = grid_x
    
    pdf.set_font("Times", "", 12)
    narrative_text = (
        "The simulation has successfully fractured from the main trunk. "
        "Subject 991-DELTA is currently dormant within the San Francisco Construct. "
        "Local reality parameters are stable. The Karma economy is currently offline "
        "awaiting the Chitragupta Protocol."
    )
    
    pdf.set_xy(narrative_x, narrative_y)
    pdf.multi_cell(narrative_width, 6, narrative_text, align="J")
    
    # ============================================================================
    # 6. THE FOOTER COMPLEX (The "Legal" Block)
    # ============================================================================
    
    # Legal text block above bottom bar
    legal_y = page_height - 15 - 20  # 20mm above bottom bar
    pdf.set_font("Courier", "", 6)  # Tiny text
    pdf.set_text_color(0, 0, 0)
    legal_text = (
        "WARNING: This document contains cognitohazardous material. "
        "Unauthorized access will result in immediate termination of the viewer's "
        "employment and biological functions. By reading this, you agree to the Terms of Existence."
    )
    
    pdf.set_xy(grid_x, legal_y)
    pdf.multi_cell(grid_width, 3, legal_text, align="J")
    
    # Bottom Bar: Solid BLACK rectangle
    bottom_bar_y = page_height - 15
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(0, bottom_bar_y, page_width, 15, style="F")
    
    # ============================================================================
    # 7. THE STAMP (With Box)
    # ============================================================================
    
    # Red stamp with box around it
    pdf.set_font("Courier", "B", 16)
    pdf.set_text_color(200, 0, 0)  # RED
    
    stamp_text = "ANCHORED: v0.3.1"
    stamp_width = pdf.get_string_width(stamp_text) + 10  # Add padding
    stamp_height = 20
    stamp_x = page_width - sidebar_width - stamp_width - 10
    stamp_y = bottom_bar_y - stamp_height - 5
    
    # Draw box around stamp
    pdf.set_draw_color(200, 0, 0)  # Red border
    pdf.set_line_width(2)
    pdf.rect(stamp_x, stamp_y, stamp_width, stamp_height, style="D")
    
    # Stamp text inside box
    pdf.set_xy(stamp_x + 5, stamp_y + 2)
    pdf.cell(0, 16, stamp_text, align="L")
    
    # ============================================================================
    # SAVE PDF
    # ============================================================================
    
    pdf.output(str(output_path))
    
    print(f"✅ Genesis Artifact minted (Level 4 Clearance): {output_path}")
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
    print("🔨 Minting Genesis Artifact (Level 4 Clearance - Maximalist)...")
    pdf_path = mint_genesis_artifact()
    print(f"📄 PDF generated: {pdf_path}")
    print("🚀 Opening PDF...")
    open_pdf(pdf_path)
    print("✅ Complete!")
