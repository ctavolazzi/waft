#!/usr/bin/env python3
"""
Mint Genesis Artifact: Timeline 001 Initialization Report

Generates the first tangible artifact of Timeline 001 in Site-Delta-9 style:
Heavy, bureaucratic, and dangerous.
"""

import json
import subprocess
import sys
from pathlib import Path

try:
    from fpdf import FPDF
except ImportError:
    raise ImportError("fpdf2 is required. Install with: pip install fpdf2>=2.7.0")


def mint_genesis_artifact() -> Path:
    """Generate the Genesis Artifact PDF for Timeline 001 in Site-Delta-9 style."""
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
    
    # Set margins: 20mm
    margin = 20
    pdf.set_margins(left=margin, top=margin, right=margin)
    page_width = 210  # A4 width
    content_width = page_width - (2 * margin)
    
    # ============================================================================
    # 1. TOP BORDER: Heavy black bar (5mm thick)
    # ============================================================================
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(0, 0, page_width, 5, style="F")
    
    # ============================================================================
    # 2. WARNING STRIP: Red strip with white text
    # ============================================================================
    warning_y = 5
    warning_height = 8
    pdf.set_fill_color(200, 0, 0)  # Red
    pdf.rect(0, warning_y, page_width, warning_height, style="F")
    
    # White text in warning strip
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Courier", "B", 10)
    pdf.set_xy(0, warning_y + 2)
    pdf.cell(page_width, warning_height, "WARNING: ONTOLOGICAL HAZARD // DO NOT DISTRIBUTE", align="C")
    
    # Reset text color
    pdf.set_text_color(0, 0, 0)
    
    # ============================================================================
    # 3. HEADER SECTION
    # ============================================================================
    header_start_y = warning_y + warning_height + 15
    
    # Title: "TIMELINE INITIATION REPORT" (Courier-Bold, 24pt)
    pdf.set_font("Courier", "B", 24)
    pdf.set_xy(margin, header_start_y)
    pdf.cell(content_width, 12, "TIMELINE INITIATION REPORT", align="L")
    
    # Subtitle: "SEQUENCE: 001 // ORIGIN POINT" (Courier, 12pt)
    pdf.set_font("Courier", "", 12)
    pdf.set_xy(margin, header_start_y + 15)
    pdf.cell(content_width, 8, "SEQUENCE: 001 // ORIGIN POINT", align="L")
    
    # ============================================================================
    # 4. THE "BLACK BOX" (Metadata)
    # ============================================================================
    box_y = header_start_y + 30
    box_height = 50
    box_x = margin
    
    # Draw filled black rectangle
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(box_x, box_y, content_width, box_height, style="F")
    
    # White text inside box
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Courier", "", 10)
    
    # Position text inside box (with padding)
    text_x = box_x + 5
    text_y = box_y + 8
    line_height = 10
    
    pdf.set_xy(text_x, text_y)
    pdf.cell(0, line_height, f"SUBJECT: 991-DELTA (\"TAM\")", ln=1)
    
    pdf.set_xy(text_x, text_y + line_height)
    pdf.cell(0, line_height, f"TIMELINE_ID: {config_data['timeline_id']}", ln=1)
    
    pdf.set_xy(text_x, text_y + (line_height * 2))
    pdf.cell(0, line_height, f"SOUL_SIG: [{config_data['soul_signature']}]", ln=1)
    
    pdf.set_xy(text_x, text_y + (line_height * 3))
    pdf.cell(0, line_height, f"FRACTURE_POINT: [{config_data['fracture_point']}]", ln=1)
    
    # Reset text color to black
    pdf.set_text_color(0, 0, 0)
    
    # ============================================================================
    # 5. THE NARRATIVE BODY (Serif font)
    # ============================================================================
    body_y = box_y + box_height + 15
    pdf.set_y(body_y)
    
    # Use Times (serif) for body text
    pdf.set_font("Times", "", 11)
    body_text = (
        "The simulation has successfully fractured from the main trunk. "
        "Subject 991-DELTA is currently dormant within the San Francisco Construct. "
        "Local reality parameters are stable. The Karma economy is currently offline."
    )
    
    # Word wrap the body text
    pdf.set_x(margin)
    pdf.multi_cell(content_width, 6, body_text, align="L")
    
    # ============================================================================
    # 6. THE "STAMP" (Bottom right, rotated/bold/red)
    # ============================================================================
    # Get current Y position and calculate stamp position
    current_y = pdf.get_y()
    stamp_text = "ANCHORED: v0.3.1"
    
    # Position stamp in bottom right
    pdf.set_font("Courier", "B", 12)
    pdf.set_text_color(200, 0, 0)  # Red
    
    # Calculate text width to position from right
    text_width = pdf.get_string_width(stamp_text)
    stamp_x = page_width - margin - text_width
    stamp_y = 280  # Near bottom of A4 page (297mm - margin)
    
    pdf.set_xy(stamp_x, stamp_y)
    pdf.cell(0, 8, stamp_text, align="R")
    
    # Reset text color
    pdf.set_text_color(0, 0, 0)
    
    # ============================================================================
    # 7. FOOTER: Centered, small courier
    # ============================================================================
    pdf.set_font("Courier", "", 9)
    pdf.set_text_color(0, 0, 0)
    footer_y = 290
    pdf.set_xy(0, footer_y)
    pdf.cell(page_width, 5, "PROPERTY OF TELEPORT MASSIVE // SITE-DELTA-9", align="C")
    
    # Save PDF
    pdf.output(str(output_path))
    
    print(f"✅ Genesis Artifact minted: {output_path}")
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
    print("🔨 Minting Genesis Artifact (Site-Delta-9 Style)...")
    pdf_path = mint_genesis_artifact()
    print(f"📄 PDF generated: {pdf_path}")
    print("🚀 Opening PDF...")
    open_pdf(pdf_path)
    print("✅ Complete!")
