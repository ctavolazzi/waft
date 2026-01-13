#!/usr/bin/env python3
"""
Comprehensive PDF Library Comparison Generator

Creates self-documenting PDFs for each major PDF library, explaining:
- How each library works
- Why you'd use it
- Code examples
- Pros and cons
- Use cases

Then generates a master comparison report showing all options.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# Try to import all PDF libraries (some may not be installed)
PDF_LIBRARIES = {
    "reportlab": {
        "name": "ReportLab",
        "import": "from reportlab.lib.pagesizes import letter\nfrom reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer\nfrom reportlab.lib.styles import getSampleStyleSheet",
        "installed": False,
    },
    "weasyprint": {
        "name": "WeasyPrint",
        "import": "from weasyprint import HTML, CSS",
        "installed": False,
    },
    "borb": {
        "name": "Borb",
        "import": "from borb.pdf import Document, Page, Paragraph, PDF\nfrom decimal import Decimal",
        "installed": False,
    },
    "fpdf2": {
        "name": "fpdf2",
        "import": "from fpdf import FPDF",
        "installed": False,
    },
    "pypdf": {
        "name": "PyPDF",
        "import": "from pypdf import PdfReader, PdfWriter",
        "installed": False,
    },
    "pymupdf": {
        "name": "PyMuPDF (fitz)",
        "import": "import fitz  # PyMuPDF",
        "installed": False,
    },
    "matplotlib": {
        "name": "Matplotlib",
        "import": "from matplotlib.backends.backend_pdf import PdfPages\nimport matplotlib.pyplot as plt",
        "installed": False,
    },
    "pillow": {
        "name": "Pillow (PIL)",
        "import": "from PIL import Image",
        "installed": False,
    },
    "jinja2_weasyprint": {
        "name": "Jinja2 + WeasyPrint",
        "import": "from jinja2 import Template\nfrom weasyprint import HTML",
        "installed": False,
    },
}

# Check which libraries are installed
for lib_key, lib_info in PDF_LIBRARIES.items():
    try:
        if lib_key == "reportlab":
            import reportlab
            lib_info["installed"] = True
        elif lib_key == "weasyprint":
            import weasyprint
            lib_info["installed"] = True
        elif lib_key == "borb":
            import borb
            lib_info["installed"] = True
        elif lib_key == "fpdf2":
            import fpdf
            lib_info["installed"] = True
        elif lib_key == "pypdf":
            import pypdf
            lib_info["installed"] = True
        elif lib_key == "pymupdf":
            import fitz
            lib_info["installed"] = True
        elif lib_key == "matplotlib":
            import matplotlib
            lib_info["installed"] = True
        elif lib_key == "pillow":
            from PIL import Image
            lib_info["installed"] = True
        elif lib_key == "jinja2_weasyprint":
            try:
                from jinja2 import Template
                from weasyprint import HTML
                lib_info["installed"] = True
            except ImportError:
                pass
    except ImportError:
        pass


def generate_reportlab_pdf(output_path: Path):
    """Generate self-documenting PDF using ReportLab."""
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
        
        doc = SimpleDocTemplate(str(output_path), pagesize=letter,
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=72)
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#0d47a1'),
            spaceAfter=30,
            alignment=TA_CENTER,
        )
        
        code_style = ParagraphStyle(
            'Code',
            parent=styles['Normal'],
            fontName='Courier',
            fontSize=9,
            leftIndent=20,
            rightIndent=20,
            backColor=colors.HexColor('#f5f7fa'),
            borderColor=colors.HexColor('#0d47a1'),
            borderWidth=1,
            borderPadding=10,
        )
        
        story = []
        
        # Title
        story.append(Paragraph("ReportLab: Professional PDF Generation", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # What is ReportLab?
        story.append(Paragraph("<b>What is ReportLab?</b>", styles['Heading2']))
        story.append(Paragraph(
            "ReportLab is the industry standard for programmatic PDF generation in Python. "
            "It provides a powerful Platypus framework for automatic text flow and page breaks, "
            "professional typography control, and a low-level Canvas API for precise positioning.",
            styles['Normal']
        ))
        story.append(Spacer(1, 0.2*inch))
        
        # Why use ReportLab?
        story.append(Paragraph("<b>Why Use ReportLab?</b>", styles['Heading2']))
        pros = [
            "✅ <b>Platypus Framework</b> - Automatic text flow and page breaks",
            "✅ <b>Professional Typography</b> - Kerning, leading, tracking control",
            "✅ <b>Flowables</b> - Content blocks that position themselves",
            "✅ <b>Stylesheets</b> - Separate content from formatting",
            "✅ <b>Advanced Tables</b> - Spanning cells, conditional formatting",
            "✅ <b>Canvas API</b> - Low-level control when needed",
            "✅ <b>Production Proven</b> - Used by major companies worldwide",
            "✅ <b>Pure Python</b> - No system dependencies",
            "✅ <b>Small File Sizes</b> - Efficient PDF generation",
        ]
        for pro in pros:
            story.append(Paragraph(pro, styles['Normal']))
            story.append(Spacer(1, 0.05*inch))
        
        story.append(Spacer(1, 0.2*inch))
        
        # How it works
        story.append(Paragraph("<b>How It Works</b>", styles['Heading2']))
        story.append(Paragraph(
            "ReportLab uses an object-oriented approach where you build a 'story' of flowable "
            "objects (Paragraph, Table, Image, etc.) and then build the document. The Platypus "
            "framework automatically handles page breaks, text wrapping, and positioning.",
            styles['Normal']
        ))
        story.append(Spacer(1, 0.1*inch))
        
        # Code example
        code_example = """# Create document
doc = SimpleDocTemplate("output.pdf", pagesize=letter)

# Get styles
styles = getSampleStyleSheet()

# Build story (content)
story = []
story.append(Paragraph("Title", styles['Heading1']))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("Body text...", styles['BodyText']))

# Generate PDF
doc.build(story)"""
        
        story.append(Paragraph("<b>Basic Example:</b>", styles['Heading3']))
        story.append(Paragraph(f"<pre>{code_example}</pre>", code_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Use cases
        story.append(Paragraph("<b>Best Use Cases</b>", styles['Heading2']))
        use_cases = [
            "📄 Professional documents with precise typography",
            "📊 Data-heavy reports with complex tables",
            "📑 Multi-page reports with automatic pagination",
            "🏢 Enterprise applications requiring production-grade PDFs",
            "📈 Financial reports and legal documents",
            "🎓 Academic papers requiring precise formatting",
        ]
        for case in use_cases:
            story.append(Paragraph(case, styles['Normal']))
            story.append(Spacer(1, 0.05*inch))
        
        story.append(PageBreak())
        
        # Cons and limitations
        story.append(Paragraph("<b>Limitations & Considerations</b>", styles['Heading2']))
        cons = [
            "⚠️ <b>Learning Curve</b> - Medium complexity (1-2 days to master)",
            "⚠️ <b>Manual Markdown Parsing</b> - Must parse markdown yourself",
            "⚠️ <b>Limited CSS Support</b> - Uses ReportLab styles, not CSS",
            "⚠️ <b>More Code</b> - More verbose than HTML-based approaches",
            "⚠️ <b>No HTML Input</b> - Must convert HTML to ReportLab objects manually",
        ]
        for con in cons:
            story.append(Paragraph(con, styles['Normal']))
            story.append(Spacer(1, 0.05*inch))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Installation
        story.append(Paragraph("<b>Installation</b>", styles['Heading2']))
        story.append(Paragraph(
            "<code>pip install reportlab</code>",
            code_style
        ))
        story.append(Paragraph(
            "No system dependencies required - pure Python!",
            styles['Normal']
        ))
        
        # Build PDF
        doc.build(story)
        return True
    except ImportError:
        return False


def generate_weasyprint_pdf(output_path: Path):
    """Generate self-documenting PDF using WeasyPrint."""
    try:
        from weasyprint import HTML, CSS
        from io import StringIO
        
        # Build HTML content piece by piece to avoid parsing issues
        html_parts = [
            "<!DOCTYPE html>",
            "<html lang=\"en\">",
            "<head>",
            "    <meta charset=\"UTF-8\">",
            "    <title>WeasyPrint: HTML/CSS to PDF</title>",
            "    <style>",
            "        @page {",
            "            size: letter;",
            "            margin: 1in;",
            "        }",
            "        body {",
            "            font-family: 'Times New Roman', serif;",
            "            font-size: 11pt;",  # CSS value, not Python
            "            line-height: 1.6;",
            "            color: #1a1a1a;",
            "        }",
            "        h1 {",
            "            font-size: 24pt;",
            "            color: #0d47a1;",
            "            text-align: center;",
            "            margin-bottom: 30pt;",
            "            border-bottom: 3pt solid #0d47a1;",
            "            padding-bottom: 10pt;",
            "        }",
            "        h2 {",
            "            font-size: 18pt;",
            "            color: #0d47a1;",
            "            margin-top: 24pt;",
            "            margin-bottom: 12pt;",
            "            border-bottom: 1pt solid #0d47a1;",
            "            padding-bottom: 4pt;",
            "        }",
            "        h3 {",
            "            font-size: 14pt;",
            "            color: #000;",
            "            margin-top: 18pt;",
            "            margin-bottom: 8pt;",
            "        }",
            "        p {",
            "            margin-bottom: 12pt;",
            "            text-align: justify;",
            "        }",
            "        .pros {",
            "            background: #f5f7fa;",
            "            border-left: 4pt solid #0d47a1;",
            "            padding: 12pt;",
            "            margin: 12pt 0;",
            "        }",
            "        .pros li {",
            "            margin-bottom: 6pt;",
            "        }",
            "        code {",
            "            font-family: 'Courier New', monospace;",
            "            font-size: 9pt;",
            "            background: #f5f7fa;",
            "            padding: 2pt 4pt;",
            "            border: 1pt solid #0d47a1;",
            "            border-radius: 2pt;",
            "        }",
            "        pre {",
            "            background: #f5f7fa;",
            "            border: 1pt solid #0d47a1;",
            "            border-left: 4pt solid #0d47a1;",
            "            padding: 12pt;",
            "            margin: 12pt 0;",
            "            font-size: 9pt;",
            "            overflow-x: auto;",
            "            page-break-inside: avoid;",
            "        }",
            "        .use-case {",
            "            background: #f5f7fa;",
            "            padding: 8pt;",
            "            margin: 6pt 0;",
            "            border-radius: 3pt;",
            "        }",
            "        .cons {",
            "            background: #fff3cd;",
            "            border-left: 4pt solid #ffc107;",
            "            padding: 12pt;",
            "            margin: 12pt 0;",
            "        }",
            "    </style>",
            "</head>",
            "<body>",
            "    <h1>WeasyPrint: HTML/CSS to PDF</h1>",
            "    ",
            "    <h2>What is WeasyPrint?</h2>",
            "    <p>",
            "        WeasyPrint converts HTML and CSS to beautiful PDFs. It renders HTML/CSS like a browser ",
            "        and outputs professional PDFs with excellent typography. If you know HTML and CSS, ",
            "        you already know how to use WeasyPrint.",
            "    </p>",
            "    ",
            "    <h2>Why Use WeasyPrint?</h2>",
            "    <div class=\"pros\">",
            "        <ul>",
            "            <li><strong>Modern Web Standards</strong> - HTML5 + CSS3 support</li>",
            "            <li><strong>Excellent Typography</strong> - Uses HarfBuzz for text shaping</li>",
            "            <li><strong>Familiar Syntax</strong> - If you know CSS, you're done</li>",
            "            <li><strong>Automatic Pagination</strong> - CSS Paged Media support</li>",
            "            <li><strong>Print-Ready</strong> - Professional typesetting out of the box</li>",
            "            <li><strong>Template Engines</strong> - Works with Jinja2, Django templates, etc.</li>",
            "            <li><strong>Preview in Browser</strong> - Debug HTML before PDF generation</li>",
            "            <li><strong>CSS Grid/Flexbox</strong> - Modern layout capabilities</li>",
            "        </ul>",
            "    </div>",
            "    ",
            "    <h2>How It Works</h2>",
            "    <p>",
            "        WeasyPrint takes HTML content (string or file) and CSS styling, renders it like a browser ",
            "        would, and converts the rendered output to PDF. It supports CSS Paged Media for print-specific ",
            "        features like page breaks, headers, footers, and page numbering.",
            "    </p>",
            "    ",
            "    <h3>Basic Example:</h3>",
            "    <pre>from weasyprint import HTML\n\nhtml_content = \"\"\"\n&lt;html&gt;\n&lt;head&gt;\n    &lt;style&gt;\n        @page { size: letter; margin: 1in; }\n        body { font-family: serif; }\n        h1 { color: #0d47a1; }\n    &lt;/style&gt;\n&lt;/head&gt;\n&lt;body&gt;\n    &lt;h1&gt;My Document&lt;/h1&gt;\n    &lt;p&gt;Content here...&lt;/p&gt;\n&lt;/body&gt;\n&lt;/html&gt;\n\"\"\"\n\nHTML(string=html_content).write_pdf(\"output.pdf\")</pre>",
            "    ",
            "    <h2>Best Use Cases</h2>",
            "    <div class=\"use-case\">",
            "        <strong>📄 Web Content to PDF</strong> - Convert HTML pages to PDF",
            "    </div>",
            "    <div class=\"use-case\">",
            "        <strong>📝 Markdown to PDF</strong> - Markdown → HTML → PDF pipeline",
            "    </div>",
            "    <div class=\"use-case\">",
            "        <strong>🎨 Template-Based Documents</strong> - Jinja2 + WeasyPrint for dynamic content",
            "    </div>",
            "    <div class=\"use-case\">",
            "        <strong>🌐 Web Scraping to PDF</strong> - Scrape web pages and convert to PDF",
            "    </div>",
            "    <div class=\"use-case\">",
            "        <strong>📊 Reports from HTML</strong> - Generate reports using HTML/CSS",
            "    </div>",
            "    <div class=\"use-case\">",
            "        <strong>🎯 Rapid Prototyping</strong> - Quick PDF generation with familiar web tech",
            "    </div>",
            "    ",
            "    <h2>Limitations & Considerations</h2>",
            "    <div class=\"cons\">",
            "        <ul>",
            "            <li><strong>System Dependencies</strong> - Requires Cairo, Pango (may need installation)</li>",
            "            <li><strong>Larger File Sizes</strong> - PDFs tend to be larger than ReportLab</li>",
            "            <li><strong>Slower Generation</strong> - HTML rendering adds overhead</li>",
            "            <li><strong>CSS Print Quirks</strong> - Some CSS features behave differently in print</li>",
            "            <li><strong>Less PDF Control</strong> - Less control over PDF internals</li>",
            "        </ul>",
            "    </div>",
            "    ",
            "    <h2>Installation</h2>",
            "    <p>",
            "        <code>pip install weasyprint</code>",
            "    </p>",
            "    <p>",
            "        <strong>Note:</strong> May require system dependencies (Cairo, Pango, GDK-PixBuf) ",
            "        depending on your platform. Check WeasyPrint documentation for platform-specific ",
            "        installation instructions.",
            "    </p>",
            "    ",
            "    <h2>When to Choose WeasyPrint</h2>",
            "    <p>",
            "        Choose WeasyPrint if you're comfortable with HTML/CSS, have HTML/Markdown content, ",
            "        want rapid development, need web-to-PDF conversion, or are building template-based systems. ",
            "        It's perfect for teams with web development backgrounds.",
            "    </p>",
            "</body>",
            "</html>",
        ]
        html_content = "\n".join(html_parts)
        
        HTML(string=html_content).write_pdf(str(output_path))
        return True
    except ImportError:
        return False

def generate_fpdf2_pdf(output_path: Path):
    """Generate self-documenting PDF using fpdf2."""
    try:
        from fpdf import FPDF
        
        class SelfDocumentingPDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 24)
                self.set_text_color(13, 71, 161)  # #0d47a1
                self.cell(0, 20, 'fpdf2: Simple PDF Generation', 0, 1, 'C')
                self.ln(10)
            
            def footer(self):
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                self.set_text_color(128, 128, 128)
                self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
            
            def section_title(self, title):
                self.set_font('Arial', 'B', 16)
                self.set_text_color(13, 71, 161)
                self.cell(0, 12, title, 0, 1, 'L')
                self.ln(3)
            
            def body_text(self, text):
                self.set_font('Arial', '', 11)
                self.set_text_color(0, 0, 0)
                self.multi_cell(0, 6, text, 0, 'J')
                self.ln(5)
            
            def code_block(self, code):
                self.set_font('Courier', '', 9)
                self.set_fill_color(245, 247, 250)  # #f5f7fa
                self.set_draw_color(13, 71, 161)
                self.set_text_color(0, 0, 0)
                # Draw box
                x = self.get_x()
                y = self.get_y()
                self.rect(x, y, 190, 40, 'DF')
                self.set_xy(x + 5, y + 5)
                self.multi_cell(180, 5, code, 0, 'L')
                self.ln(10)
            
            def pro_item(self, text):
                self.set_font('Arial', '', 11)
                self.set_text_color(0, 128, 0)
                self.cell(5, 6, '[OK]', 0, 0)
                self.set_text_color(0, 0, 0)
                self.multi_cell(0, 6, text, 0, 'L')
                self.ln(3)
        
        pdf = SelfDocumentingPDF()
        pdf.add_page()
        
        # Title already in header
        
        pdf.section_title("What is fpdf2?")
        pdf.body_text(
            "fpdf2 is a pure Python library for PDF generation with a simple, straightforward API. "
            "It's lightweight, has no external dependencies, and is perfect for basic to moderate "
            "PDF generation needs. You control positioning manually, giving you precise control "
            "over layout."
        )
        pdf.ln(5)
        
        pdf.section_title("Why Use fpdf2?")
        pdf.pro_item("Pure Python - No system dependencies")
        pdf.pro_item("Simple API - Easy to learn and use")
        pdf.pro_item("Lightweight - Small footprint")
        pdf.pro_item("Manual Control - Precise positioning")
        pdf.pro_item("Good for Basic PDFs - Perfect for simple documents")
        pdf.pro_item("Active Development - Well-maintained project")
        pdf.ln(5)
        
        pdf.section_title("How It Works")
        pdf.body_text(
            "fpdf2 uses a canvas-based approach where you set fonts, colors, and positions, "
            "then draw text, shapes, and images. You manually control page breaks and positioning, "
            "giving you complete control but requiring more code for complex layouts."
        )
        pdf.ln(5)
        
        pdf.section_title("Basic Example:")
        code = """from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(40, 10, 'Hello World!')
pdf.output('output.pdf')"""
        pdf.code_block(code)
        
        pdf.section_title("Best Use Cases")
        pdf.pro_item("Simple documents with basic formatting")
        pdf.pro_item("When you need minimal dependencies")
        pdf.pro_item("Quick PDF generation for simple reports")
        pdf.pro_item("Embedded systems or constrained environments")
        pdf.pro_item("Learning PDF generation basics")
        pdf.ln(5)
        
        pdf.section_title("Limitations & Considerations")
        pdf.set_text_color(255, 140, 0)  # Orange
        pdf.cell(5, 6, '[!]', 0, 0)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 6, "Manual positioning required - more code for complex layouts", 0, 'L')
        pdf.ln(3)
        pdf.set_text_color(255, 140, 0)
        pdf.cell(5, 6, '[!]', 0, 0)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 6, "Limited automatic text flow - must handle wrapping yourself", 0, 'L')
        pdf.ln(3)
        pdf.set_text_color(255, 140, 0)
        pdf.cell(5, 6, '[!]', 0, 0)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 6, "Basic typography support - no advanced features", 0, 'L')
        pdf.ln(3)
        pdf.set_text_color(255, 140, 0)
        pdf.cell(5, 6, '[!]', 0, 0)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 6, "No CSS/template support - must code everything", 0, 'L')
        pdf.ln(10)
        
        pdf.section_title("Installation")
        pdf.code_block("pip install fpdf2")
        pdf.body_text("No system dependencies required - pure Python!")
        
        pdf.output(str(output_path))
        return True
    except ImportError:
        return False

def generate_master_comparison(output_dir: Path):
    """Generate master comparison PDF showing all libraries."""
    try:
        from weasyprint import HTML
        
        # Build comparison table data
        libraries_data = []
        for lib_key, lib_info in PDF_LIBRARIES.items():
            if lib_info["installed"]:
                libraries_data.append({
                    "name": lib_info["name"],
                    "key": lib_key,
                    "installed": True,
                })
            else:
                libraries_data.append({
                    "name": lib_info["name"],
                    "key": lib_key,
                    "installed": False,
                })
        
        # Generate HTML for master comparison - use format() instead of f-string to avoid CSS parsing issues
        html_template = """
        @page {{
            size: letter;
            margin: 0.75in;
        }}
        body {{
            font-family: 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #1a1a1a;
        }}
        h1 {{
            font-size: 28pt;
            color: #0d47a1;
            text-align: center;
            margin-bottom: 20pt;
            border-bottom: 4pt solid #0d47a1;
            padding-bottom: 10pt;
        }}
        h2 {{
            font-size: 18pt;
            color: #0d47a1;
            margin-top: 24pt;
            margin-bottom: 12pt;
            border-bottom: 2pt solid #0d47a1;
            padding-bottom: 4pt;
        }}
        h3 {{
            font-size: 14pt;
            color: #000;
            margin-top: 16pt;
            margin-bottom: 8pt;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 16pt 0;
            font-size: 10pt;
        }}
        th {{
            background: #0d47a1;
            color: white;
            padding: 8pt;
            text-align: left;
            font-weight: bold;
            border: 1pt solid #0d47a1;
        }}
        td {{
            padding: 6pt 8pt;
            border: 1pt solid #ccc;
        }}
        tr:nth-child(even) {{
            background: #f5f7fa;
        }}
        .installed {{
            color: #28a745;
            font-weight: bold;
        }}
        .not-installed {{
            color: #dc3545;
            font-style: italic;
        }}
        .library-section {{
            page-break-inside: avoid;
            margin: 20pt 0;
            padding: 12pt;
            background: #f5f7fa;
            border-left: 4pt solid #0d47a1;
        }}
        .library-section h3 {{
            margin-top: 0;
            color: #0d47a1;
        }}
        code {{
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            background: #f5f7fa;
            padding: 2pt 4pt;
            border-radius: 2pt;
        }}
        .summary-box {{
            background: #e3f2fd;
            border: 2pt solid #0d47a1;
            padding: 16pt;
            margin: 20pt 0;
            border-radius: 4pt;
        }}
        .summary-box h3 {{
            margin-top: 0;
            color: #0d47a1;
        }}
    
            This document provides a comprehensive comparison of all major PDF generation 
            libraries available for Python. Each library has its own self-documenting PDF 
            that explains how it works, why you'd use it, and includes code examples.
        </p>
        <p>
            <strong>Generated:</strong> {gen_time}
        </p>
    </div>
    
    <h2>Available Libraries</h2>
    
    <table>
        <thead>
            <tr>
                <th>Library</th>
                <th>Status</th>
                <th>Primary Use Case</th>
                <th>Complexity</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>ReportLab</strong></td>
                <td class="{{reportlab_class}}">
                    {{reportlab_status}}
                </td>
                <td>Professional programmatic PDFs</td>
                <td>Medium</td>
            </tr>
            <tr>
                <td><strong>WeasyPrint</strong></td>
                <td class="{{weasyprint_class}}">
                    {{weasyprint_status}}
                </td>
                <td>HTML/CSS to PDF</td>
                <td>Low (if you know HTML/CSS)</td>
            </tr>
            <tr>
                <td><strong>Borb</strong></td>
                <td class="{{borb_class}}">
                    {{borb_status}}
                </td>
                <td>Modern Python PDF library</td>
                <td>Medium</td>
            </tr>
            <tr>
                <td><strong>fpdf2</strong></td>
                <td class="{{fpdf2_class}}">
                    {{fpdf2_status}}
                </td>
                <td>Simple, lightweight PDFs</td>
                <td>Low</td>
            </tr>
            <tr>
                <td><strong>PyPDF</strong></td>
                <td class="{{pypdf_class}}">
                    {{pypdf_status}}
                </td>
                <td>PDF reading/manipulation</td>
                <td>Low</td>
            </tr>
            <tr>
                <td><strong>PyMuPDF (fitz)</strong></td>
                <td class="{{pymupdf_class}}">
                    {{pymupdf_status}}
                </td>
                <td>PDF reading/rendering</td>
                <td>Medium</td>
            </tr>
            <tr>
                <td><strong>Matplotlib</strong></td>
                <td class="{{matplotlib_class}}">
                    {{matplotlib_status}}
                </td>
                <td>Charts/plots to PDF</td>
                <td>Low</td>
            </tr>
            <tr>
                <td><strong>Pillow (PIL)</strong></td>
                <td class="{{pillow_class}}">
                    {{pillow_status}}
                </td>
                <td>Image to PDF conversion</td>
                <td>Low</td>
            </tr>
            <tr>
                <td><strong>Jinja2 + WeasyPrint</strong></td>
                <td class="{{jinja2_weasyprint_class}}">
                    {{jinja2_weasyprint_status}}
                </td>
                <td>Template-based PDF generation</td>
                <td>Low (if you know templates)</td>
            </tr>
        </tbody>
    </table>
    
    <h2>Quick Decision Guide</h2>
    
    <div class="library-section">
    
    
    
    
    
    
        Individual self-documenting PDFs have been generated for each library. Each PDF explains:
    
    
            or <strong>ReportLab</strong> if you need programmatic control and smaller file sizes.
            separation of content and presentation.
"""
        
        # Format template with generated time and library statuses
        gen_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        format_vars = {
            'gen_time': gen_time,
            'reportlab_class': 'installed' if PDF_LIBRARIES['reportlab']['installed'] else 'not-installed',
            'reportlab_status': '✅ Installed' if PDF_LIBRARIES['reportlab']['installed'] else '❌ Not Installed',
            'weasyprint_class': 'installed' if PDF_LIBRARIES['weasyprint']['installed'] else 'not-installed',
            'weasyprint_status': '✅ Installed' if PDF_LIBRARIES['weasyprint']['installed'] else '❌ Not Installed',
            'borb_class': 'installed' if PDF_LIBRARIES['borb']['installed'] else 'not-installed',
            'borb_status': '✅ Installed' if PDF_LIBRARIES['borb']['installed'] else '❌ Not Installed',
            'fpdf2_class': 'installed' if PDF_LIBRARIES['fpdf2']['installed'] else 'not-installed',
            'fpdf2_status': '✅ Installed' if PDF_LIBRARIES['fpdf2']['installed'] else '❌ Not Installed',
            'pypdf_class': 'installed' if PDF_LIBRARIES['pypdf']['installed'] else 'not-installed',
            'pypdf_status': '✅ Installed' if PDF_LIBRARIES['pypdf']['installed'] else '❌ Not Installed',
            'pymupdf_class': 'installed' if PDF_LIBRARIES['pymupdf']['installed'] else 'not-installed',
            'pymupdf_status': '✅ Installed' if PDF_LIBRARIES['pymupdf']['installed'] else '❌ Not Installed',
            'matplotlib_class': 'installed' if PDF_LIBRARIES['matplotlib']['installed'] else 'not-installed',
            'matplotlib_status': '✅ Installed' if PDF_LIBRARIES['matplotlib']['installed'] else '❌ Not Installed',
            'pillow_class': 'installed' if PDF_LIBRARIES['pillow']['installed'] else 'not-installed',
            'pillow_status': '✅ Installed' if PDF_LIBRARIES['pillow']['installed'] else '❌ Not Installed',
            'jinja2_weasyprint_class': 'installed' if PDF_LIBRARIES['jinja2_weasyprint']['installed'] else 'not-installed',
            'jinja2_weasyprint_status': '✅ Installed' if PDF_LIBRARIES['jinja2_weasyprint']['installed'] else '❌ Not Installed',
        }
        html_content = html_template.format(**format_vars)
        
        output_path = output_dir / "pdf_library_comparison_master.pdf"
        HTML(string=html_content).write_pdf(str(output_path))
        print(f"✅ Generated master comparison: {output_path}")
        return True
    except ImportError:
        print("⚠️  WeasyPrint not available for master comparison")
        return False

def main():
    """Generate all self-documenting PDFs."""
    output_dir = project_root / "_temp_pdf_samples" / "pdf_library_comparison"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("📚 Generating Comprehensive PDF Library Comparison...")
    print(f"Output directory: {output_dir}\n")
    
    results = {}
    
    # Generate ReportLab PDF
    if PDF_LIBRARIES["reportlab"]["installed"]:
        print("📄 Generating ReportLab self-documenting PDF...")
        result = generate_reportlab_pdf(output_dir / "pdf_library_reportlab.pdf")
        results["reportlab"] = result
        if result:
            print("  ✅ ReportLab PDF generated\n")
        else:
            print("  ❌ Failed to generate ReportLab PDF\n")
    else:
        print("  ⚠️  ReportLab not installed, skipping\n")
    
    # Generate WeasyPrint PDF
    if PDF_LIBRARIES["weasyprint"]["installed"]:
        print("📄 Generating WeasyPrint self-documenting PDF...")
        result = generate_weasyprint_pdf(output_dir / "pdf_library_weasyprint.pdf")
        results["weasyprint"] = result
        if result:
            print("  ✅ WeasyPrint PDF generated\n")
        else:
            print("  ❌ Failed to generate WeasyPrint PDF\n")
    else:
        print("  ⚠️  WeasyPrint not installed, skipping\n")
    
    # Generate fpdf2 PDF
    if PDF_LIBRARIES["fpdf2"]["installed"]:
        print("📄 Generating fpdf2 self-documenting PDF...")
        result = generate_fpdf2_pdf(output_dir / "pdf_library_fpdf2.pdf")
        results["fpdf2"] = result
        if result:
            print("  ✅ fpdf2 PDF generated\n")
        else:
            print("  ❌ Failed to generate fpdf2 PDF\n")
    else:
        print("  ⚠️  fpdf2 not installed, skipping\n")
    
    # Generate master comparison
    print("📊 Generating master comparison PDF...")
    generate_master_comparison(output_dir)
    
    # Summary
    print("\n" + "="*60)
    print("📚 PDF Library Comparison Generation Complete!")
    print("="*60)
    print(f"\nGenerated PDFs in: {output_dir}")
    print("\nGenerated files:")
    for lib_key, result in results.items():
        if result:
            print(f"  ✅ pdf_library_{lib_key}.pdf")
    print("  ✅ pdf_library_comparison_master.pdf")
    print("\nEach PDF is self-documenting and explains:")
    print("  • What the library is")
    print("  • Why you'd use it")
    print("  • How it works (with code examples)")
    print("  • Best use cases")
    print("  • Limitations and considerations")
    print("  • Installation instructions")


if __name__ == "__main__":
    main()
