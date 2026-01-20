#!/usr/bin/env python3
"""
Generate Printer-Friendly Demo Booklets
========================================

Creates printer-friendly (black and white) versions of all demo booklets.
Uses the printer-friendly helper to convert templates.
"""

import sys
from datetime import datetime
from pathlib import Path

from jinja2 import Template
from weasyprint import HTML

sys.path.insert(0, str(Path(__file__).parent.parent))



def create_printer_friendly_advanced_demo(
    demo_dir: Path, framework_doc=None, pdf_binder=None
) -> Path:
    """Create printer-friendly version of advanced demo booklet."""

    # Original template with colors
    original_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>WAFT Advanced Demonstration</title>
    <style>
        @page {
            size: letter;
            margin: 0.75in;
            
            @top-center {
                content: "WAFT Advanced Demonstration";
                font-family: 'Times New Roman', serif;
                font-size: 9pt;
                color: #000;
            }
            
            @bottom-center {
                content: "Page " counter(page);
                font-family: 'Times New Roman', serif;
                font-size: 9pt;
                color: #000;
            }
        }
        
        @page :first {
            @top-center { content: none; }
        }
        
        body {
            font-family: 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #000;
            background: #fff;
        }
        
        .cover {
            text-align: center;
            padding-top: 2in;
        }
        
        .cover h1 {
            font-size: 32pt;
            font-weight: bold;
            margin-bottom: 0.3in;
            letter-spacing: 3px;
        }
        
        .cover .subtitle {
            font-size: 18pt;
            color: #000;
            margin-bottom: 0.5in;
        }
        
        h1 {
            font-size: 20pt;
            font-weight: bold;
            margin-top: 0.5in;
            margin-bottom: 0.3in;
            border-bottom: 3px solid #000;
            padding-bottom: 0.1in;
        }
        
        h2 {
            font-size: 16pt;
            font-weight: bold;
            margin-top: 0.4in;
            margin-bottom: 0.2in;
            color: #000;
        }
        
        .highlight-box {
            background: #fff;
            border-left: 4px solid #000;
            border: 2px solid #000;
            padding: 0.2in;
            margin: 0.2in 0;
        }
        
        .tool-card {
            background: #fff;
            border: 1px solid #000;
            padding: 0.2in;
            margin: 0.2in 0;
        }
        
        .tool-title {
            font-weight: bold;
            font-size: 13pt;
            color: #000;
            margin-bottom: 0.1in;
        }
        
        code {
            font-family: 'Courier New', monospace;
            font-size: 10pt;
            background: #f5f5f5;
            padding: 0.05in;
            border: 1px solid #000;
        }
    </style>
</head>
<body>
    <div class="cover">
        <h1>WAFT</h1>
        <div class="subtitle">Advanced Demonstration</div>
        <div class="subtitle" style="font-size: 14pt; margin-top: 0.3in;">
            World Architecture Framework & Templates
        </div>
        <div style="font-size: 12pt; color: #000; margin-top: 1.5in;">
            {{ date }}
        </div>
        <div style="font-size: 10pt; margin-top: 0.5in; font-weight: bold;">
            [PRINTER FRIENDLY VERSION]
        </div>
    </div>
    
    <h1>Introduction</h1>
    <p>
        This booklet documents WAFT's advanced capabilities, including self-documentation
        and intelligent PDF organization. These tools demonstrate WAFT's recursive
        self-improvement through documentation.
    </p>
    
    <h1>Demonstration 1: Framework Self-Documentation</h1>
    
    <div class="tool-card">
        <div class="tool-title">Framework Documentation Generator</div>
        <p>
            WAFT can inspect its own codebase and generate comprehensive documentation
            about how it functions. This is <strong>recursive self-documentation</strong> -
            the system describing itself.
        </p>
        <p><strong>Key Features:</strong></p>
        <ul>
            <li>Recursively scans WAFT's codebase</li>
            <li>Extracts information about modules, classes, functions</li>
            <li>Generates documentation based on actual findings</li>
            <li><strong>NO HARDCODED CONTENT</strong> - everything is discovered</li>
        </ul>
        {% if framework_doc %}
        <p><strong>Generated:</strong> Framework documentation PDF created</p>
        {% endif %}
    </div>
    
    <h1>Demonstration 2: PDF Binder Organization</h1>
    
    <div class="tool-card">
        <div class="tool-title">PDF Binder Organizer</div>
        <p>
            WAFT can recursively scan any directory, find all PDFs, extract metadata,
            and organize them into intelligent booklets (max 25 pages each).
        </p>
        <p><strong>Key Features:</strong></p>
        <ul>
            <li>Recursive directory scanning</li>
            <li>Metadata extraction (title, author, pages, dates)</li>
            <li>Smart booklet assembly (max 25 pages each)</li>
            <li>Full binder creation with all PDFs</li>
            <li>Comprehensive JSON metadata</li>
        </ul>
        {% if pdf_binder %}
        <p><strong>Generated:</strong> PDF binder with organized booklets</p>
        {% endif %}
    </div>
    
    <h1>Demonstration 3: Meta-Cognitive Integration</h1>
    
    <div class="highlight-box">
        <h2>The Recursive Loop</h2>
        <ol>
            <li><strong>WAFT generates documents</strong> → Creates PDFs</li>
            <li><strong>WAFT organizes documents</strong> → Creates binders</li>
            <li><strong>WAFT documents itself</strong> → Creates framework docs</li>
            <li><strong>WAFT tracks its work</strong> → Uses _pyrite system</li>
            <li><strong>WAFT improves</strong> → Based on observations</li>
            <li><strong>Cycle repeats</strong> → Continuous enhancement</li>
        </ol>
    </div>
    
    <h2>Key Insight</h2>
    <p>
        These tools demonstrate WAFT's ability to:
    </p>
    <ul>
        <li><strong>Observe itself</strong> (framework documentation)</li>
        <li><strong>Organize knowledge</strong> (PDF binder)</li>
        <li><strong>Track its work</strong> (_pyrite system)</li>
        <li><strong>Improve recursively</strong> (feedback loops)</li>
    </ul>
    
    <h1>Conclusion</h1>
    <p>
        This advanced demonstration showcases WAFT's recursive self-improvement
        capabilities. The system can observe itself, organize its knowledge, and
        continuously improve through documentation and feedback loops.
    </p>
    
    <div class="highlight-box">
        <p style="text-align: center; font-style: italic; margin-top: 0.5in;">
            <strong>WAFT documenting WAFT using WAFT.</strong><br>
            Recursive self-improvement through documentation.
        </p>
    </div>
</body>
</html>
"""

    template = Template(original_template)
    html_content = template.render(
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        framework_doc=framework_doc is not None,
        pdf_binder=pdf_binder is not None,
    )

    booklet_path = demo_dir / "WAFT_Advanced_Demo_Booklet_PrinterFriendly.pdf"

    HTML(string=html_content).write_pdf(str(booklet_path))

    return booklet_path


def main():
    """Generate printer-friendly demo booklets."""
    print("=" * 80)
    print("WAFT Demo Printer-Friendly Generator")
    print("=" * 80)
    print()

    # Check for existing demo directories
    demo_dir = Path("advanced_demo_output")
    if not demo_dir.exists():
        print(f"⚠️  Demo directory not found: {demo_dir}")
        print("   Run the advanced demo first to generate source files.")
        return

    print(f"Generating printer-friendly demo booklets in: {demo_dir}")
    print()

    # Check for existing demo files
    framework_doc = None
    pdf_binder = None

    framework_doc_path = demo_dir / "WAFT_Framework_Documentation.pdf"
    if framework_doc_path.exists():
        framework_doc = framework_doc_path

    pdf_binder_path = demo_dir / "PDF_Binder.pdf"
    if pdf_binder_path.exists():
        pdf_binder = pdf_binder_path

    # Generate printer-friendly advanced demo
    print("Generating printer-friendly advanced demo booklet...")
    booklet_path = create_printer_friendly_advanced_demo(demo_dir, framework_doc, pdf_binder)

    size_kb = booklet_path.stat().st_size / 1024
    print(f"  ✅ Generated: {booklet_path.name}")
    print(f"     Size: {size_kb:.1f} KB")
    print()

    print("=" * 80)
    print("Printer-friendly generation complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
