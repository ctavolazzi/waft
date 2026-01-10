#!/usr/bin/env python3
"""
Mint Genesis Artifact: Timeline 001 Initialization Report

The Kafka Protocol: Maximalist density with visual noise.
Simulates a high-security government document - cluttered, bureaucratic, dangerous.
"""

import json
import subprocess
import random
from pathlib import Path

try:
    from fpdf import FPDF
except ImportError:
    raise ImportError("fpdf2 is required. Install with: pip install fpdf2>=2.7.0")


def draw_barcode(pdf, x, y, width, height):
    """Draw a simulated barcode using random vertical lines."""
    num_lines = 35
    line_spacing = width / num_lines
    
    for i in range(num_lines):
        line_x = x + (i * line_spacing)
        # Random thickness (0.5mm to 2mm)
        line_thickness = random.uniform(0.5, 2.0)
        # Random height (60% to 100% of barcode height)
        line_height = height * random.uniform(0.6, 1.0)
        line_y_offset = (height - line_height) / 2
        
        pdf.set_draw_color(0, 0, 0)
        pdf.set_line_width(line_thickness)
        pdf.line(line_x, y + line_y_offset, line_x, y + line_y_offset + line_height)


def mint_genesis_artifact() -> Path:
    """Generate the Genesis Artifact PDF with Kafka Protocol density."""
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
    sidebar_width = 15  # Right sidebar width
    left_margin_width = 15  # Left margin column width
    
    # ============================================================================
    # 1. THE "WATERMARK" LAYER (Draw First, Behind Everything)
    # ============================================================================
    
    pdf.set_text_color(240, 240, 240)  # Very light grey
    pdf.set_font("Courier", "B", 48)
    watermark_text = "CONFIDENTIAL // SUBSTRATE"
    
    text_width = pdf.get_string_width(watermark_text)
    center_x = (page_width - text_width) / 2
    center_y = page_height / 2
    
    pdf.set_xy(center_x, center_y)
    pdf.cell(0, 48, watermark_text, align="C")
    pdf.set_text_color(0, 0, 0)
    
    # ============================================================================
    # 2. THE "SYSTEM CHECK" RAIL (Left Margin Column)
    # ============================================================================
    
    # Draw thin vertical line separating left margin
    pdf.set_draw_color(100, 100, 100)  # Grey line
    pdf.set_line_width(0.5)
    pdf.line(left_margin_width, 0, left_margin_width, page_height)
    
    # Checklist items in left margin column
    pdf.set_font("Courier", "", 6)
    pdf.set_text_color(0, 0, 0)
    checklist_y = 50
    checklist_items = [
        "[X] MEM_CHK",
        "[X] BIO_SIG",
        "[ ] KARMA",
        "[X] ONTOLOGY",
        "[ ] SOUL_SYNC"
    ]
    
    for i, item in enumerate(checklist_items):
        pdf.set_xy(2, checklist_y + (i * 8))
        pdf.cell(0, 6, item, align="L")
    
    # ============================================================================
    # 3. THE HEADER COMPLEX
    # ============================================================================
    
    # Top Black Bar: Adjust for left margin
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(left_margin_width, 0, page_width - left_margin_width - sidebar_width, 25, style="F")
    
    # Logo Placeholder: Square in top left of header area
    logo_x = left_margin_width + 10
    logo_y = 5
    logo_size = 15
    pdf.set_draw_color(255, 255, 255)
    pdf.set_line_width(1)
    pdf.rect(logo_x, logo_y, logo_size, logo_size, style="D")
    
    # Top Text (Inside Black Bar)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 14)
    text_y = 12.5 - (14 / 2)
    pdf.set_xy(left_margin_width, text_y)
    pdf.cell(page_width - left_margin_width - sidebar_width, 14, "INSTITUTE FOR ADVANCED ONTOLOGICAL STUDIES", align="C")
    
    # Barcode (Top Right corner, inside header area)
    barcode_x = page_width - sidebar_width - 40
    barcode_y = 5
    barcode_width = 35
    barcode_height = 15
    draw_barcode(pdf, barcode_x, barcode_y, barcode_width, barcode_height)
    
    # "DO NOT SCAN" label below barcode
    pdf.set_font("Courier", "", 5)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(barcode_x, barcode_y + barcode_height + 1)
    pdf.cell(barcode_width, 3, "DO NOT SCAN", align="C")
    
    # Hazard Strip
    hazard_y = 25
    pdf.set_fill_color(180, 0, 0)
    pdf.rect(left_margin_width, hazard_y, page_width - left_margin_width - sidebar_width, 8, style="F")
    
    # Hazard Text
    pdf.set_font("Courier", "B", 10)
    hazard_text_y = hazard_y + 4 - (10 / 2)
    pdf.set_xy(left_margin_width, hazard_text_y)
    pdf.cell(page_width - left_margin_width - sidebar_width, 10, "WARNING: ONTOLOGICAL HAZARD // EYES ONLY", align="C")
    
    # Double seal effect
    seal_line_y = hazard_y + 8 + 2
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(left_margin_width, seal_line_y, page_width - left_margin_width - sidebar_width, 1, style="F")
    
    pdf.set_text_color(0, 0, 0)
    
    # ============================================================================
    # 4. THE SIDEBAR (Technical Rail) - Fixed Clipping
    # ============================================================================
    
    sidebar_x = page_width - sidebar_width
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(sidebar_x, 0, sidebar_width, page_height, style="F")
    
    # Vertical white text - moved inward by 5mm to prevent clipping
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Courier", "B", 7)
    sidebar_text = "SITE-DELTA-9 // OMEGA-LOCKOUT // SEQ-001"
    
    # Split and position vertically with proper spacing
    words = sidebar_text.split(" // ")
    sidebar_text_y = 50
    for i, word in enumerate(words):
        # Center text in sidebar (sidebar_width / 2 - half text width)
        word_width = pdf.get_string_width(word)
        word_x = sidebar_x + (sidebar_width / 2) - (word_width / 2)
        pdf.set_xy(word_x, sidebar_text_y + (i * 20))
        pdf.cell(0, 7, word, align="C")
    
    pdf.set_text_color(0, 0, 0)
    
    # ============================================================================
    # 5. THE "INVERTED" DATA GRID (2x2 Grid with Thick Borders)
    # ============================================================================
    
    grid_y = 50
    content_width = page_width - left_margin_width - sidebar_width - 20  # Account for margins
    grid_width = content_width
    grid_height = 50
    grid_x = left_margin_width + 10
    
    cell_width = grid_width / 2
    cell_height = grid_height / 2
    
    # Cell 1 (Top Left): SUBJECT - Black background, white label, black value background
    cell1_x = grid_x
    cell1_y = grid_y
    
    # Black background for label area
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(cell1_x, cell1_y, cell_width, 12, style="F")
    
    # White label text
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Courier", "B", 9)
    pdf.set_xy(cell1_x + 3, cell1_y + 3)
    pdf.cell(0, 8, "SUBJECT:", ln=1)
    
    # White background for value area
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(cell1_x, cell1_y + 12, cell_width, cell_height - 12, style="F")
    
    # Black value text
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Courier", "B", 10)
    pdf.set_xy(cell1_x + 3, cell1_y + 18)
    pdf.cell(0, 8, "991-DELTA", ln=1)
    
    # Cell 2 (Top Right): TIMELINE
    cell2_x = grid_x + cell_width
    cell2_y = grid_y
    
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(cell2_x, cell2_y, cell_width, 12, style="F")
    
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Courier", "B", 9)
    pdf.set_xy(cell2_x + 3, cell2_y + 3)
    pdf.cell(0, 8, "TIMELINE:", ln=1)
    
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(cell2_x, cell2_y + 12, cell_width, cell_height - 12, style="F")
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Courier", "B", 10)
    pdf.set_xy(cell2_x + 3, cell2_y + 18)
    pdf.cell(0, 8, config_data['timeline_id'], ln=1)
    
    # Thick white vertical border (1mm)
    pdf.set_draw_color(255, 255, 255)
    pdf.set_line_width(1)
    pdf.line(cell1_x + cell_width, cell1_y, cell1_x + cell_width, cell1_y + grid_height)
    
    # Cell 3 (Bottom Left): STATUS
    cell3_x = grid_x
    cell3_y = grid_y + cell_height
    
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(cell3_x, cell3_y, cell_width, 12, style="F")
    
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Courier", "B", 9)
    pdf.set_xy(cell3_x + 3, cell3_y + 3)
    pdf.cell(0, 8, "STATUS:", ln=1)
    
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(cell3_x, cell3_y + 12, cell_width, cell_height - 12, style="F")
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Courier", "B", 9)
    pdf.set_xy(cell3_x + 3, cell3_y + 18)
    pdf.cell(0, 8, "UN-AWAKENED", ln=1)
    
    # Cell 4 (Bottom Right): FRACTURE
    cell4_x = grid_x + cell_width
    cell4_y = grid_y + cell_height
    
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(cell4_x, cell4_y, cell_width, 12, style="F")
    
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Courier", "B", 9)
    pdf.set_xy(cell4_x + 3, cell4_y + 3)
    pdf.cell(0, 8, "FRACTURE:", ln=1)
    
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(cell4_x, cell4_y + 12, cell_width, cell_height - 12, style="F")
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Courier", "B", 8)
    pdf.set_xy(cell4_x + 3, cell4_y + 18)
    pdf.cell(0, 7, config_data['fracture_point'][:16], ln=1)
    
    # Thick white horizontal border (1mm)
    pdf.set_draw_color(255, 255, 255)
    pdf.set_line_width(1)
    pdf.line(grid_x, grid_y + cell_height, grid_x + grid_width, grid_y + cell_height)
    
    pdf.set_text_color(0, 0, 0)
    
    # ============================================================================
    # 6. THE NARRATIVE (With Manual Redaction)
    # ============================================================================
    
    narrative_start_y = grid_y + grid_height + 20
    pdf.set_font("Courier", "", 9)
    pdf.set_xy(grid_x, narrative_start_y)
    pdf.cell(0, 6, "REF: [FR-001-ORIGIN] // BY: THE ARCHITECT", align="L")
    
    narrative_y = narrative_start_y + 10
    narrative_width = grid_width
    narrative_x = grid_x
    
    pdf.set_font("Times", "", 12)
    narrative_text = (
        "The simulation has successfully fractured from the main trunk. "
        "Subject 991-DELTA is currently dormant within the San Francisco Construct. "
        "Local reality parameters are stable. The Karma economy is currently offline."
    )
    
    # Print text first
    pdf.set_xy(narrative_x, narrative_y)
    pdf.multi_cell(narrative_width, 6, narrative_text, align="J")
    
    # Manual redaction: Black rectangles over "San Francisco Construct" and "Karma economy"
    # Approximate positions based on text layout
    # "San Francisco Construct" appears around line 2
    redaction1_y = narrative_y + 6  # Second line
    redaction1_x = narrative_x + 60  # Approximate position
    redaction1_width = 50  # Approximate width
    redaction1_height = 7
    
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(redaction1_x, redaction1_y, redaction1_width, redaction1_height, style="F")
    
    # "Karma economy" appears around line 3
    redaction2_y = narrative_y + 12  # Third line
    redaction2_x = narrative_x + 10  # Approximate position
    redaction2_width = 35  # Approximate width
    redaction2_height = 7
    
    pdf.rect(redaction2_x, redaction2_y, redaction2_width, redaction2_height, style="F")
    
    # ============================================================================
    # 7. THE "HANDWRITTEN" NOTE (Simulated)
    # ============================================================================
    
    note_y = narrative_y + 30
    note_x = grid_x + 20
    
    # Use Times Italic, Blue, rotated -5 degrees (simulated by offset)
    pdf.set_font("Times", "I", 10)
    pdf.set_text_color(0, 0, 200)  # Blue
    
    # Simulate rotation by offsetting position slightly
    note_text = "He doesn't suspect a thing. -C."
    pdf.set_xy(note_x + 2, note_y + 1)  # Slight offset to simulate rotation
    pdf.cell(0, 8, note_text, align="L")
    
    pdf.set_text_color(0, 0, 0)
    
    # ============================================================================
    # 8. THE FOOTER COMPLEX
    # ============================================================================
    
    legal_y = page_height - 15 - 20
    pdf.set_font("Courier", "", 6)
    legal_text = (
        "WARNING: This document contains cognitohazardous material. "
        "Unauthorized access will result in immediate termination of the viewer's "
        "employment and biological functions. By reading this, you agree to the Terms of Existence."
    )
    
    pdf.set_xy(grid_x, legal_y)
    pdf.multi_cell(grid_width, 3, legal_text, align="J")
    
    # Bottom Bar
    bottom_bar_y = page_height - 15
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(left_margin_width, bottom_bar_y, page_width - left_margin_width - sidebar_width, 15, style="F")
    
    # ============================================================================
    # 9. THE STAMP (With Box)
    # ============================================================================
    
    pdf.set_font("Courier", "B", 16)
    pdf.set_text_color(200, 0, 0)
    
    stamp_text = "ANCHORED: v0.3.1"
    stamp_width = pdf.get_string_width(stamp_text) + 10
    stamp_height = 20
    stamp_x = page_width - sidebar_width - stamp_width - 10
    stamp_y = bottom_bar_y - stamp_height - 5
    
    # Draw box around stamp
    pdf.set_draw_color(200, 0, 0)
    pdf.set_line_width(2)
    pdf.rect(stamp_x, stamp_y, stamp_width, stamp_height, style="D")
    
    # Stamp text inside box
    pdf.set_xy(stamp_x + 5, stamp_y + 2)
    pdf.cell(0, 16, stamp_text, align="L")
    
    # ============================================================================
    # SAVE PDF
    # ============================================================================
    
    pdf.output(str(output_path))
    
    print(f"✅ Genesis Artifact minted (Kafka Protocol): {output_path}")
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
    print("🔨 Minting Genesis Artifact (Kafka Protocol - Maximalist Density)...")
    pdf_path = mint_genesis_artifact()
    print(f"📄 PDF generated: {pdf_path}")
    print("🚀 Opening PDF...")
    open_pdf(pdf_path)
    print("✅ Complete!")
