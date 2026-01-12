#!/usr/bin/env python3
"""
Generate PDF from another-cycle command documentation.
Uses Foundation V1 (FPDF2) for pure Python PDF generation.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.foundation import (
    DocumentEngine,
    DocumentConfig,
    SectionHeader,
    TextBlock,
)

def clean_unicode(text: str) -> str:
    """Replace Unicode characters with ASCII equivalents."""
    replacements = {
        '→': '->',
        '←': '<-',
        '✅': '[OK]',
        '❌': '[X]',
        '⚠️': '[!]',
        '🚧': '[IN PROGRESS]',
        '📄': '',
        '✨': '*',
        '🎯': '*',
        '💡': '*',
        '🚀': '*',
        '📊': '',
        '🔍': '',
        '🌊': '~',
        '🔥': '*',
        '💎': '*',
        '🌑': '*',
        '🎲': '*',
        '📋': '',
        '📁': '',
        '🎉': '*',
    }
    for unicode_char, ascii_char in replacements.items():
        text = text.replace(unicode_char, ascii_char)
    return text

def markdown_to_blocks(content: str):
    """Convert markdown to document blocks."""
    blocks = []
    lines = content.split('\n')
    current_paragraph = []
    
    for line in lines:
        # Clean Unicode characters
        line = clean_unicode(line)
        
        # Headers
        if line.startswith('# '):
            if current_paragraph:
                blocks.append(TextBlock('\n'.join(current_paragraph)))
                current_paragraph = []
            blocks.append(SectionHeader(line[2:], level=1))
        elif line.startswith('## '):
            if current_paragraph:
                blocks.append(TextBlock('\n'.join(current_paragraph)))
                current_paragraph = []
            blocks.append(SectionHeader(line[3:], level=2))
        elif line.startswith('### '):
            if current_paragraph:
                blocks.append(TextBlock('\n'.join(current_paragraph)))
                current_paragraph = []
            blocks.append(SectionHeader(line[4:], level=3))
        elif line.startswith('---'):
            # Horizontal rule - skip
            if current_paragraph:
                blocks.append(TextBlock('\n'.join(current_paragraph)))
                current_paragraph = []
        elif line.strip() == '':
            if current_paragraph:
                blocks.append(TextBlock('\n'.join(current_paragraph)))
                current_paragraph = []
        else:
            current_paragraph.append(line)
    
    if current_paragraph:
        blocks.append(TextBlock('\n'.join(current_paragraph)))
    
    return blocks

def main():
    """Generate PDF from another-cycle.md."""
    project_root = Path(__file__).parent.parent
    command_file = project_root / ".cursor" / "commands" / "another-cycle.md"
    
    if not command_file.exists():
        print(f"❌ Command file not found: {command_file}")
        return
    
    print(f"📄 Reading command file: {command_file}")
    content = command_file.read_text()
    
    print("📝 Converting markdown to document blocks...")
    blocks = markdown_to_blocks(content)
    
    print("📄 Generating PDF...")
    
    # Create document config
    config = DocumentConfig(
        fonts={
            "Header": ("Helvetica", "B"),
            "Body": ("Helvetica", ""),
            "Monospace": ("Courier", ""),
        },
        watermark=None,
        header_text="Another Cycle Command",
        footer_text="WAFT Command Documentation",
        page_margins=(72, 72, 72, 72),  # 1 inch margins
        line_spacing=1.5,
        font_size_body=11,
        font_size_header=16,
        font_size_footer=9,
    )
    
    # Create document engine
    engine = DocumentEngine(config)
    
    # Add blocks
    for block in blocks:
        engine.add(block)
    
    # Generate PDF
    output_path = project_root / "_work_efforts" / "another_cycle_command.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"💾 Saving PDF to: {output_path}")
    engine.render(output_path)
    
    print(f"✅ PDF generated successfully: {output_path}")
    return output_path

if __name__ == "__main__":
    main()
