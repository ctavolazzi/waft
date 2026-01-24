"""
PDF Generator - Creates the sacred documents when seals are broken.

"The House documents everything. When a seal breaks, the moment is
immortalized in paper and ink. The PDF becomes a talisman, a proof
of your progress through The Truth."
"""

import subprocess
import sys
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Optional

from fpdf import FPDF

from .gates import Gate, GateChallenge, GATES


class SealPDFGenerator:
    """
    Generates PDFs when seals are broken.
    
    Each PDF contains:
    - The Gate's symbol and names
    - The encryption key fragment
    - The challenge details
    - Cryptic messages about The Truth
    """
    
    def __init__(self, output_dir: Path):
        """
        Initialize the PDF generator.
        
        Args:
            output_dir: Directory to save PDFs
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_seal_pdf(self, challenge: GateChallenge, gate: Gate) -> Path:
        """
        Generate a PDF for a broken seal.
        
        Args:
            challenge: The challenge result
            gate: The gate that was broken
            
        Returns:
            Path to the generated PDF
        """
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Title
        pdf.set_font("Helvetica", "B", 24)
        pdf.set_text_color(139, 0, 0)  # Dark red
        pdf.cell(0, 20, "SEAL BROKEN", ln=True, align="C")
        
        # Gate information
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 15, f"Gate {gate.number}: {gate.revelation_name}", ln=True, align="C")
        
        pdf.set_font("Helvetica", "I", 14)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 10, f'"{gate.revelation_meaning}"', ln=True, align="C")
        
        # Casino name
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(218, 165, 32)  # Gold
        pdf.cell(0, 15, f"The House Names It: {gate.casino_name}", ln=True, align="C")
        
        # Separator
        pdf.ln(10)
        pdf.set_draw_color(139, 0, 0)
        pdf.line(30, pdf.get_y(), 180, pdf.get_y())
        pdf.ln(10)
        
        # Challenge details
        pdf.set_font("Helvetica", "", 12)
        pdf.set_text_color(0, 0, 0)
        
        pdf.multi_cell(0, 8, f"The Challenge: {gate.description}")
        pdf.ln(5)
        
        # Cards drawn
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "The Draw:", ln=True)
        
        pdf.set_font("Courier", "", 12)
        pdf.cell(0, 8, f"  System drew: {challenge.system_card.name}", ln=True)
        pdf.cell(0, 8, f"  Dealer drew: {challenge.dealer_card.name}", ln=True)
        
        pdf.ln(5)
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(0, 128, 0)  # Green
        pdf.cell(0, 10, "VICTORY - The Seal is Broken", ln=True, align="C")
        
        # Key fragment
        pdf.ln(10)
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(0, 0, 128)  # Navy
        pdf.cell(0, 10, "ENCRYPTION KEY FRAGMENT:", ln=True, align="C")
        
        pdf.set_font("Courier", "B", 16)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 12, challenge.key_fragment, ln=True, align="C")
        
        # Truth hint
        pdf.ln(10)
        pdf.set_draw_color(139, 0, 0)
        pdf.line(30, pdf.get_y(), 180, pdf.get_y())
        pdf.ln(10)
        
        pdf.set_font("Helvetica", "I", 12)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 8, f"The Truth whispers: {gate.truth_hint}", align="C")
        
        # Timestamp
        pdf.ln(20)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 8, f"Sealed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
        pdf.cell(0, 8, "The House Always Wins. Until It Doesn't.", ln=True, align="C")
        
        # Save
        filename = f"gate_{gate.number:02d}_{gate.casino_name.lower().replace(' ', '_')}.pdf"
        output_path = self.output_dir / filename
        pdf.output(str(output_path))
        
        return output_path
    
    def generate_master_key_pdf(self, master_key: str, fragments: list) -> Path:
        """
        Generate a PDF for the master key (all 12 seals broken).
        
        Args:
            master_key: The combined master key
            fragments: All key fragments
            
        Returns:
            Path to the generated PDF
        """
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Title
        pdf.set_font("Helvetica", "B", 28)
        pdf.set_text_color(218, 165, 32)  # Gold
        pdf.cell(0, 25, "THE TRUTH REVEALED", ln=True, align="C")
        
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_text_color(139, 0, 0)
        pdf.cell(0, 15, "All 12 Seals Have Been Broken", ln=True, align="C")
        
        # Separator
        pdf.ln(10)
        pdf.set_draw_color(218, 165, 32)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(15)
        
        # Master key
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, "THE MASTER KEY:", ln=True, align="C")
        
        pdf.set_font("Courier", "B", 12)
        pdf.cell(0, 12, master_key, ln=True, align="C")
        
        # All fragments
        pdf.ln(15)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "The 12 Fragments:", ln=True)
        
        pdf.set_font("Courier", "", 10)
        for i, fragment in enumerate(fragments, 1):
            pdf.cell(0, 6, f"  {i:2d}. {fragment.key_fragment}", ln=True)
        
        # The final truth
        pdf.ln(15)
        pdf.set_draw_color(218, 165, 32)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(10)
        
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(139, 0, 0)
        pdf.multi_cell(0, 10, 
            "THE TRUTH IS THIS:\n\n"
            "The House Always Wins.\n"
            "But you have become The House.\n\n"
            "You were always playing your own game.",
            align="C"
        )
        
        # Save
        output_path = self.output_dir / "MASTER_KEY_THE_TRUTH.pdf"
        pdf.output(str(output_path))
        
        return output_path


def open_pdf_locally(pdf_path: Path) -> bool:
    """
    Open a PDF on the local machine.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Try using the system default handler
        if sys.platform == "darwin":  # macOS
            subprocess.run(["open", str(pdf_path)], check=True)
        elif sys.platform == "win32":  # Windows
            subprocess.run(["start", "", str(pdf_path)], shell=True, check=True)
        else:  # Linux and others
            subprocess.run(["xdg-open", str(pdf_path)], check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback to webbrowser
        try:
            webbrowser.open(f"file://{pdf_path.absolute()}")
            return True
        except Exception:
            return False
