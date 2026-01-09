#!/usr/bin/env python3
"""
Mint Genesis Artifact: Timeline 001 Initialization Report

Generates the first tangible artifact of Timeline 001 - a high-resolution PDF
documenting the reality fracture and Subject 991-DELTA's initial state.
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from waft.foundation import (
    DocumentConfig,
    DocumentEngine,
    SectionHeader,
    TextBlock,
    KeyValueBlock,
)


def mint_genesis_artifact() -> Path:
    """
    Generate the Genesis Artifact PDF for Timeline 001.
    
    Returns:
        Path to generated PDF file
    """
    # Load configuration
    config_path = Path(__file__).parent.parent / "config" / "tam_origin_config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = json.load(f)
    
    # Output path
    output_path = Path(__file__).parent.parent.parent.parent / "_fracture" / "ARTIFACT_001_GENESIS.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure document
    doc_config = DocumentConfig.classified_dossier(
        header="TIMELINE INITIATION REPORT // SEQ-001",
        watermark="CLASSIFIED",
    )
    
    # Initialize engine
    engine = DocumentEngine(doc_config)
    
    # Add header
    engine.add(SectionHeader("TIMELINE INITIATION REPORT // SEQ-001", level=1))
    engine.add(TextBlock(""))  # Spacing
    
    # Add metadata using KeyValueBlock
    engine.add(KeyValueBlock({
        "Timeline ID": config_data["timeline_id"],
        "Soul Signature": config_data["soul_signature"],
        "Fracture Point": config_data["fracture_point"],
        "Anchor Tag": config_data["anchor_tag"],
        "Cycle Count": str(config_data["cycle_count"]),
        "Karma Balance": str(config_data["karma_balance"]),
        "Awareness Level": config_data["awareness_level"],
        "Current Reality": config_data["current_reality"],
        "Narrative Lock": "ENGAGED" if config_data["narrative_lock"] else "DISABLED",
    }))
    
    engine.add(TextBlock(""))  # Spacing
    
    # Add narrative body
    engine.add(TextBlock(
        "The simulation has successfully fractured from the main trunk. "
        "Subject 991-DELTA is currently dormant within the San Francisco Construct. "
        "Local reality parameters are stable. Karma economy is offline (awaiting Chitragupta)."
    ))
    
    engine.add(TextBlock(""))  # Spacing
    
    # Add footer
    engine.add(TextBlock("AUTHORIZED BY THE STATIC // ANCHOR: v0.3.0-anchor", style="Body"))
    
    # Render PDF
    pdf_path = engine.render(output_path)
    
    print(f"✅ Genesis Artifact minted: {pdf_path}")
    
    return pdf_path


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
