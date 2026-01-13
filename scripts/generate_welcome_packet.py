#!/usr/bin/env python3
"""
Generate HTML and PDF versions of the WAFT Welcome Packet.

Usage:
    python scripts/generate_welcome_packet.py
"""

from pathlib import Path
from datetime import datetime
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.pdf import PDF
from src.waft.evolution.golden_triangle import GoldenTriangle


def generate_html_version(markdown_content: str, output_path: Path) -> Path:
    """Generate HTML version of the welcome packet."""
    # #region agent log
    with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
        import json
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"D","location":"generate_welcome_packet.py:20","message":"generate_html_version entry","data":{"markdown_length":len(markdown_content) if markdown_content else 0,"markdown_preview":markdown_content[:200] if markdown_content else ""},"timestamp":int(__import__('time').time()*1000)}) + '\n')
    # #endregion
    
    converter = GoldenTriangle()
    html_content = converter.markdown_to_html(markdown_content)
    
    # #region agent log
    with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
        import json
        import re
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"D","location":"generate_welcome_packet.py:25","message":"after markdown_to_html","data":{"html_length":len(html_content) if html_content else 0,"html_preview":html_content[:400] if html_content else "","has_h1":bool(re.search(r'<h1[^>]*>', html_content)) if html_content else False,"has_hr":bool(re.search(r'<hr[^>]*>', html_content)) if html_content else False},"timestamp":int(__import__('time').time()*1000)}) + '\n')
    # #endregion
    
    # Wrap in a complete HTML document with styling
    html_document = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WAFT Welcome Packet</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #555;
            margin-top: 25px;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        pre code {{
            background-color: transparent;
            color: inherit;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin-left: 0;
            color: #555;
            font-style: italic;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        ul, ol {{
            margin-left: 20px;
        }}
        li {{
            margin-bottom: 8px;
        }}
        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #ecf0f1;
            color: #777;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
        <div class="footer">
            <p><strong>Version</strong>: 0.5.2<br>
            <strong>Last Updated</strong>: {datetime.now().strftime('%Y-%m-%d')}<br>
            <strong>License</strong>: MIT<br>
            <strong>Repository</strong>: <a href="https://github.com/ctavolazzi/waft">https://github.com/ctavolazzi/waft</a></p>
        </div>
    </div>
</body>
</html>"""
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_document, encoding='utf-8')
    return output_path


def generate_pdf_version(markdown_content: str, output_path: Path) -> Path:
    """Generate PDF version of the welcome packet using WAFT's PDF class."""
    # #region agent log
    with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
        import json
        import re
        f.write(json.dumps({"sessionId":"debug-session","runId":"post-fix","hypothesisId":"E","location":"generate_welcome_packet.py:134","message":"generate_pdf_version entry","data":{"markdown_length":len(markdown_content) if markdown_content else 0,"content_is_markdown":bool(re.search(r'^#\s+', markdown_content, re.MULTILINE)) if markdown_content else False,"content_is_html":bool(re.search(r'<[^>]+>', markdown_content)) if markdown_content else False},"timestamp":int(__import__('time').time()*1000)}) + '\n')
    # #endregion
    
    # Convert markdown to HTML first (template expects HTML, not markdown)
    converter = GoldenTriangle()
    html_content = converter.markdown_to_html(markdown_content)
    
    # #region agent log
    with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
        import json
        import re
        f.write(json.dumps({"sessionId":"debug-session","runId":"post-fix","hypothesisId":"E","location":"generate_welcome_packet.py:141","message":"after markdown_to_html for PDF","data":{"html_length":len(html_content) if html_content else 0,"html_preview":html_content[:300] if html_content else "","has_h1":bool(re.search(r'<h1[^>]*>', html_content)) if html_content else False,"has_hr":bool(re.search(r'<hr[^>]*>', html_content)) if html_content else False},"timestamp":int(__import__('time').time()*1000)}) + '\n')
    # #endregion
    
    # Use the field_guide template for a professional look
    pdf = PDF.from_template(
        template="field_guide",
        title="WAFT Welcome Packet",
        content=html_content,  # Pass HTML, not markdown
        series="WELCOME PACKET",
        number="WP-001",
        subtitle="Welcome to the Evolutionary Code Laboratory",
        output_path=output_path,
        printer_friendly=False
    )
    
    generated_path = pdf.save(str(output_path))
    
    # #region agent log
    with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
        import json
        f.write(json.dumps({"sessionId":"debug-session","runId":"post-fix","hypothesisId":"E","location":"generate_welcome_packet.py:160","message":"pdf.save complete","data":{"generated_path":str(generated_path)},"timestamp":int(__import__('time').time()*1000)}) + '\n')
    # #endregion
    
    return Path(generated_path)


def main():
    """Main function to generate both HTML and PDF versions."""
    # Paths
    project_root = Path(__file__).parent.parent
    markdown_file = project_root / "WAFT_WELCOME_PACKET.md"
    output_dir = project_root / "docs" / "welcome_packet"
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Read markdown content
    if not markdown_file.exists():
        print(f"Error: {markdown_file} not found!")
        return 1
    
    markdown_content = markdown_file.read_text(encoding='utf-8')
    
    # Generate HTML version
    print("Generating HTML version...")
    html_path = output_dir / "WAFT_WELCOME_PACKET.html"
    generate_html_version(markdown_content, html_path)
    print(f"✅ HTML version created: {html_path}")
    
    # Generate PDF version
    print("Generating PDF version...")
    pdf_path = output_dir / "WAFT_WELCOME_PACKET.pdf"
    try:
        generate_pdf_version(markdown_content, pdf_path)
        print(f"✅ PDF version created: {pdf_path}")
    except Exception as e:
        print(f"⚠️  PDF generation failed: {e}")
        print("   Trying alternative method...")
        # Fallback to simple markdown-to-PDF
        try:
            pdf = PDF.from_markdown(
                markdown=markdown_content,
                title="WAFT Welcome Packet",
                style="premium",
                output_path=pdf_path
            )
            generated_path = pdf.save(str(pdf_path))
            print(f"✅ PDF version created (fallback): {generated_path}")
        except Exception as e2:
            print(f"❌ PDF generation failed: {e2}")
            return 1
    
    print("\n✅ Welcome packet generation complete!")
    print(f"   HTML: {html_path}")
    print(f"   PDF: {pdf_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
