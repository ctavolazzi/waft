"""
WAFT HTML Template with Integrated PDF Conversion
=================================================

Multipurpose, functional HTML template designed for clarity and utility.
Works for reports, documentation, summaries, and any structured content.

Design Principles:
- Information-first: Content is king
- Clean and readable: No visual noise
- Flexible: Adapts to any content type
- Print-friendly: Looks great on paper
- Fast to scan: Clear hierarchy and structure
"""

from datetime import datetime
from pathlib import Path

from jinja2 import Template

WAFT_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} | WAFT</title>
    <style>
        /* ============================================
           WAFT Multipurpose Template
           Clean, functional, information-first design
           ============================================ */

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            background: #ffffff;
            padding: 0;
            font-size: 15px;
        }

        /* Container */
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0;
        }

        /* Content Wrapper - supports sidebar layout */
        .content-wrapper {
            display: flex;
            min-height: calc(100vh - 200px);
        }

        /* Sidebar Navigation */
        .sidebar {
            width: 250px;
            background: #f8f9fa;
            padding: 1.5rem;
            border-right: 1px solid #e5e5e5;
            position: fixed;
            left: 0;
            top: 0;
            height: 100vh;
            overflow-y: auto;
            flex-shrink: 0;
        }

        .sidebar h3 {
            margin-top: 0;
            font-size: 1.1rem;
            color: #000;
            margin-bottom: 1rem;
        }

        .sidebar nav ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .sidebar nav li {
            margin-bottom: 0.5rem;
        }

        .sidebar nav a {
            color: #0066cc;
            text-decoration: none;
            display: block;
            padding: 4px 0;
        }

        .sidebar nav a:hover {
            text-decoration: underline;
        }

        /* Main Content */
        .main-content {
            margin-left: 250px;
            padding: 2rem;
            flex: 1;
            max-width: calc(100% - 250px);
        }

        @media (max-width: 768px) {
            .sidebar {
                position: relative;
                width: 100%;
                height: auto;
            }
            .main-content {
                margin-left: 0;
                max-width: 100%;
            }
        }

        /* Header - Minimal and functional */
        .header {
            border-bottom: 2px solid #e5e5e5;
            padding-bottom: 1rem;
            margin-bottom: 2rem;
        }

        .header h1 {
            font-size: 1.75rem;
            font-weight: 600;
            color: #000;
            margin-bottom: 0.25rem;
            letter-spacing: -0.02em;
        }

        .header .meta {
            font-size: 0.875rem;
            color: #666;
            margin-top: 0.5rem;
        }

        .header .meta-item {
            display: inline-block;
            margin-right: 1rem;
        }

        /* Content Sections */
        .section {
            margin-bottom: 2.5rem;
        }

        .section-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: #000;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #e5e5e5;
        }

        /* Typography */
        h1 {
            font-size: 1.5rem;
            font-weight: 600;
            color: #000;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }

        h2 {
            font-size: 1.25rem;
            font-weight: 600;
            color: #000;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }

        h3 {
            font-size: 1.1rem;
            font-weight: 500;
            color: #333;
            margin-top: 1.25rem;
            margin-bottom: 0.5rem;
        }

        p {
            margin-bottom: 1rem;
            color: #333;
        }

        ul, ol {
            margin-left: 1.5rem;
            margin-bottom: 1rem;
        }

        li {
            margin-bottom: 0.5rem;
            color: #333;
        }

        /* Lists - Clean and scannable */
        .list-item {
            padding: 0.75rem 0;
            border-bottom: 1px solid #f0f0f0;
        }

        .list-item:last-child {
            border-bottom: none;
        }

        .list-item-title {
            font-weight: 500;
            color: #000;
            margin-bottom: 0.25rem;
        }

        .list-item-meta {
            font-size: 0.875rem;
            color: #666;
        }

        /* Tables - Clean and readable */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            font-size: 0.9375rem;
        }

        th {
            text-align: left;
            font-weight: 600;
            color: #000;
            padding: 0.75rem;
            border-bottom: 2px solid #e5e5e5;
            background: #fafafa;
        }

        td {
            padding: 0.75rem;
            border-bottom: 1px solid #f0f0f0;
            color: #333;
        }

        tr:hover {
            background: #fafafa;
        }

        /* Code */
        code {
            font-family: 'SF Mono', 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 0.875em;
            background: #f5f5f5;
            padding: 0.125rem 0.375rem;
            border-radius: 3px;
            color: #d73a49;
        }

        pre {
            background: #f5f5f5;
            padding: 1rem;
            border-radius: 4px;
            overflow-x: auto;
            margin: 1rem 0;
            border: 1px solid #e5e5e5;
        }

        pre code {
            background: transparent;
            padding: 0;
            color: #333;
        }

        /* Badges/Tags - Subtle and functional */
        .badge {
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 500;
            padding: 0.25rem 0.5rem;
            border-radius: 3px;
            background: #f0f0f0;
            color: #666;
            border: 1px solid #e0e0e0;
        }

        .badge-proven { background: #d4edda; color: #155724; border-color: #c3e6cb; }
        .badge-disproven { background: #f8d7da; color: #721c24; border-color: #f5c6cb; }
        .badge-inconclusive { background: #fff3cd; color: #856404; border-color: #ffeaa7; }
        .badge-completed { background: #d4edda; color: #155724; border-color: #c3e6cb; }
        .badge-active { background: #cce5ff; color: #004085; border-color: #b3d9ff; }
        .badge-paused { background: #fff3cd; color: #856404; border-color: #ffeaa7; }
        .badge-open { background: #e9ecef; color: #495057; border-color: #dee2e6; }

        /* Links */
        a {
            color: #0066cc;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        /* Footer - Minimal */
        .footer {
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid #e5e5e5;
            font-size: 0.875rem;
            color: #666;
            text-align: center;
        }

        /* Grid/Stats - For data visualization */
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }

        .stat-card {
            padding: 1rem;
            background: #fafafa;
            border: 1px solid #e5e5e5;
            border-radius: 4px;
        }

        .stat-value {
            font-size: 1.5rem;
            font-weight: 600;
            color: #000;
        }

        .stat-label {
            font-size: 0.875rem;
            color: #666;
            margin-top: 0.25rem;
        }

        /* Print optimizations */
        @media print {
            body {
                background: white;
            }

            .container {
                padding: 0;
            }

            .section {
                page-break-inside: avoid;
            }

            h1, h2 {
                page-break-after: avoid;
            }
        }

        /* PDF-specific page rules */
        @page {
            size: letter;
            margin: 0.75in;

            @top-right {
                content: "{{ title }}";
                font-size: 9pt;
                color: #666;
            }

            @bottom-center {
                content: "Page " counter(page);
                font-size: 9pt;
                color: #666;
            }
        }

        @page :first {
            @top-right { content: none; }
            @bottom-center { content: none; }
        }

        /* Responsive */
        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }

            table {
                font-size: 0.875rem;
            }

            th, td {
                padding: 0.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ title }}</h1>
            <div class="meta">
                <span class="meta-item">Generated: {{ timestamp }}</span>
                <span class="meta-item">WAFT</span>
            </div>
        </div>

        <div class="content-wrapper">
            {{ content }}
        </div>

        <div class="footer">
            <p>Generated by WAFT (Wave Agent Framework & Tools)</p>
        </div>
    </div>
</body>
</html>
"""


def generate_waft_html(
    title: str,
    content: str,
    output_path: Path,
    timestamp: str | None = None,
    pdf_available: bool = True,
    **kwargs,
) -> Path:
    """
    Generate WAFT multipurpose HTML document.

    Args:
        title: Document title
        content: HTML content (markdown will be converted)
        output_path: Where to save HTML file
        timestamp: Optional timestamp (defaults to now)
        pdf_available: Whether PDF conversion is available
        **kwargs: Additional template variables

    Returns:
        Path to generated HTML file
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    template = Template(WAFT_HTML_TEMPLATE)
    html_output = template.render(
        title=title, content=content, timestamp=timestamp, pdf_available=pdf_available, **kwargs
    )

    output_path.write_text(html_output)
    return output_path


def convert_waft_html_to_pdf(
    html_path: Path, output_path: Path | None = None, optimize: bool = True
) -> Path:
    """
    Convert WAFT HTML document to PDF using WeasyPrint.

    This is WAFT's integrated PDF conversion algorithm.

    Args:
        html_path: Path to HTML file
        output_path: Optional output path (defaults to html_path with .pdf extension)
        optimize: Whether to optimize PDF output

    Returns:
        Path to generated PDF file

    Raises:
        ImportError: If WeasyPrint is not available
        Exception: If PDF conversion fails
    """
    try:
        from weasyprint import HTML
    except ImportError:
        raise ImportError(
            "WeasyPrint required for PDF conversion. Install with: pip install weasyprint"
        )

    if output_path is None:
        output_path = html_path.with_suffix(".pdf")
    else:
        output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # WAFT PDF Conversion Algorithm
    html_doc = HTML(filename=str(html_path), base_url=str(html_path.parent))

    # Generate PDF with optimizations
    html_doc.write_pdf(str(output_path), presentational_hints=True, optimize_images=optimize)

    # Post-process to add blank page markers (if utility available)
    try:
        from ..utils import process_pdf_for_blank_pages

        process_pdf_for_blank_pages(output_path)
    except (ImportError, Exception):
        # Non-critical - continue without blank page markers
        pass

    return output_path


def generate_waft_html_with_pdf(
    title: str,
    content: str,
    html_output_path: Path,
    pdf_output_path: Path | None = None,
    **kwargs,
) -> dict[str, Path]:
    """
    Generate WAFT HTML and automatically convert to PDF.

    This is the complete WAFT workflow: HTML → PDF.

    Args:
        title: Document title
        content: HTML content
        html_output_path: Where to save HTML
        pdf_output_path: Optional PDF path (defaults to html_path with .pdf)
        **kwargs: Additional template variables

    Returns:
        Dict with 'html' and 'pdf' keys pointing to generated files
    """
    # Generate HTML
    html_path = generate_waft_html(
        title=title, content=content, output_path=html_output_path, **kwargs
    )

    # Convert to PDF
    try:
        if pdf_output_path is None:
            pdf_output_path = html_path.with_suffix(".pdf")

        pdf_path = convert_waft_html_to_pdf(html_path, pdf_output_path)

        return {"html": html_path, "pdf": pdf_path}
    except ImportError:
        # WeasyPrint not available - return HTML only
        return {"html": html_path, "pdf": None}
    except Exception as e:
        # PDF conversion failed - return HTML only
        print(f"⚠️  PDF conversion failed: {e}")
        return {"html": html_path, "pdf": None}
