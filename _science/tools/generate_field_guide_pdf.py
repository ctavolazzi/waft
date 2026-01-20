#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from waft.evolution.pdf_generator import PDFGenerator

content = Path("/Users/ctavolazzi/Code/active/waft/_science/reports/field_guide.md").read_text()
generator = PDFGenerator.from_content(
    content=content, title="Science-Bitch Field Guide", style="clinical_standard"
)
pdf_path = generator.save(
    output_path=Path("/Users/ctavolazzi/Code/active/waft/_science/reports/field_guide.pdf"),
    open_pdf=False,
    convert_to_png=False,
)
print(f"✅ PDF generated: {pdf_path}")
