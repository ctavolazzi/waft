#!/usr/bin/env python3
"""
Mint Genesis Artifact: Timeline 001 Initialization Report

Generates the first tangible artifact of Timeline 001 using direct FPDF positioning.
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
    """Generate the Genesis Artifact PDF for Timeline 001."""
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
    
    # Set font: Courier (monospaced)
    pdf.set_font("Courier", "B", 14)
    
    # Header: "TIMELINE INITIATION REPORT // SEQ-001"
    pdf.set_xy(margin, margin)
    pdf.cell(0, 10, "TIMELINE INITIATION REPORT // SEQ-001", ln=1, align="L")
    
    # Spacing
    pdf.ln(5)
    
    # Metadata Box: Black rectangle with white text
    box_y = pdf.get_y()
    box_width = 170  # A4 width (210mm) - 2*20mm margins
    box_height = 50
    box_x = margin
    
    # Draw black rectangle
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(box_x, box_y, box_width, box_height, style="F")
    
    # White text inside box
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Courier", "", 10)
    
    # Position text inside box (with padding)
    text_x = box_x + 5
    text_y = box_y + 8
    line_height = 12
    
    pdf.set_xy(text_x, text_y)
    pdf.cell(0, line_height, f"Timeline ID: {config_data['timeline_id']}", ln=1)
    
    pdf.set_xy(text_x, text_y + line_height)
    pdf.cell(0, line_height, f"Soul Signature: {config_data['soul_signature']}", ln=1)
    
    pdf.set_xy(text_x, text_y + (line_height * 2))
    pdf.cell(0, line_height, f"Fracture Point: {config_data['fracture_point']}", ln=1)
    
    # Reset text color to black
    pdf.set_text_color(0, 0, 0)
    
    # Move below box
    pdf.set_y(box_y + box_height + 10)
    
    # Body Text
    pdf.set_font("Courier", "", 11)
    body_text = (
        "The simulation has successfully fractured from the main trunk. "
        "Subject 991-DELTA is currently dormant within the San Francisco Construct. "
        "Local reality parameters are stable. Karma economy is offline (awaiting Chitragupta)."
    )
    
    # Word wrap the body text
    pdf.set_x(margin)
    pdf.multi_cell(box_width, 6, body_text, align="L")
    
    # Footer
    pdf.set_font("Courier", "", 10)
    pdf.ln(10)
    pdf.set_x(margin)
    pdf.cell(0, 8, "AUTHORIZED BY THE STATIC // ANCHOR: v0.3.0-anchor", align="L")
    
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
    print("🔨 Minting Genesis Artifact...")
    pdf_path = mint_genesis_artifact()
    print(f"📄 PDF generated: {pdf_path}")
    print("🚀 Opening PDF...")
    open_pdf(pdf_path)
    print("✅ Complete!")
