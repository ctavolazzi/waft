"""
Improved PDF Creation Algorithms

Enhancements to PDF generation based on comparison of WeasyPrint, ReportLab, and FPDF2.
Focuses on WeasyPrint improvements since it's the chosen library.
"""

import re
from html import unescape
from pathlib import Path

import markdown


class PDFContentProcessor:
    """Enhanced content processing for PDF generation."""

    @staticmethod
    def clean_html_content(html: str) -> str:
        """
        Clean HTML content to remove formatting artifacts.

        Fixes:
        - Double-encoded HTML entities
        - Lingering markdown syntax
        - Inline styles that cause black bars
        - Normalize whitespace
        """
        # Unescape HTML entities
        html = unescape(html)

        # Fix double-encoded entities
        html = html.replace("&amp;amp;", "&amp;")
        html = html.replace("&amp;lt;", "&lt;")
        html = html.replace("&amp;gt;", "&gt;")
        html = html.replace("&amp;quot;", "&quot;")
        html = html.replace("&amp;#39;", "&#39;")

        # Remove inline styles that cause black bars
        html = re.sub(
            r'style="[^"]*background[^"]*(?:black|#000|#000000|rgb\(0,\s*0,\s*0\))[^"]*"',
            "",
            html,
            flags=re.IGNORECASE,
        )

        # Remove background-color from inline styles
        html = re.sub(
            r"background-color\s*:\s*(?:black|#000|#000000|rgb\(0,\s*0,\s*0\))\s*;?",
            "",
            html,
            flags=re.IGNORECASE,
        )

        # Remove background from inline styles
        html = re.sub(
            r"background\s*:\s*(?:black|#000|#000000|rgb\(0,\s*0,\s*0\))\s*;?",
            "",
            html,
            flags=re.IGNORECASE,
        )

        # Normalize br tags
        html = re.sub(r"<br\s*/?>", "<br>", html, flags=re.IGNORECASE)
        html = re.sub(r"<br>\s*<br>\s*<br>+", "<br><br>", html)

        # Normalize hr tags
        html = re.sub(r"<hr\s*/?>", "<hr>", html, flags=re.IGNORECASE)

        # Remove empty style attributes
        html = re.sub(r'style="\s*"', "", html)
        html = re.sub(r'class="\s*"', "", html)

        # Remove lingering markdown syntax
        html = re.sub(r"```(\w+)?\n", "<pre><code>", html)
        html = re.sub(r"```\s*", "</code></pre>", html)
        html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)

        # Clean up whitespace
        html = re.sub(r"\n\s*\n\s*\n+", "\n\n", html)

        return html

    @staticmethod
    def enhance_markdown_for_pdf(markdown_content: str) -> str:
        """
        Enhance markdown content before conversion to HTML.

        Adds:
        - Better table formatting
        - Code block preservation
        - List improvements
        - Section dividers
        """
        # Preserve code blocks
        code_blocks = []
        code_pattern = r"```(\w+)?\n(.*?)```"

        def replace_code(match):
            lang = match.group(1) or ""
            code = match.group(2)
            idx = len(code_blocks)
            code_blocks.append((lang, code))
            return f"<CODE_BLOCK_{idx}>"

        # Extract code blocks
        markdown_content = re.sub(code_pattern, replace_code, markdown_content, flags=re.DOTALL)

        # Enhance tables (ensure proper markdown table format)
        # Tables should already be in markdown format, but ensure spacing
        markdown_content = re.sub(r"\|(.+)\|\n\|([\s\-:]+)\|\n", r"|\1|\n|\2|\n", markdown_content)

        # Enhance headers (add spacing)
        markdown_content = re.sub(
            r"^(#{1,6})\s+(.+)$", r"\1 \2", markdown_content, flags=re.MULTILINE
        )

        # Enhance lists (ensure proper spacing)
        markdown_content = re.sub(r"^(\s*[-*+])\s+", r"\1 ", markdown_content, flags=re.MULTILINE)

        # Restore code blocks
        for idx, (lang, code) in enumerate(code_blocks):
            markdown_content = markdown_content.replace(
                f"<CODE_BLOCK_{idx}>", f"```{lang}\n{code}```"
            )

        return markdown_content

    @staticmethod
    def markdown_to_html(markdown_content: str, extensions: list | None = None) -> str:
        """
        Convert markdown to HTML with enhanced processing.

        Args:
            markdown_content: Markdown text
            extensions: Optional list of markdown extensions

        Returns:
            Clean HTML content
        """
        if extensions is None:
            extensions = ["fenced_code", "tables", "nl2br", "extra", "codehilite"]

        # Enhance markdown first
        enhanced_md = PDFContentProcessor.enhance_markdown_for_pdf(markdown_content)

        # Convert to HTML
        html = markdown.markdown(enhanced_md, extensions=extensions)

        # Clean HTML
        html = PDFContentProcessor.clean_html_content(html)

        return html


class PDFStylingEnhancer:
    """Enhanced CSS styling for PDF generation."""

    @staticmethod
    def get_clean_header_styles() -> str:
        """Get CSS that ensures no black bars on headers."""
        return """
        /* Ensure NO black bars on headers */
        h1, h2, h3, h4, h5, h6 {
            background: transparent !important;
            background-color: transparent !important;
            background-image: none !important;
            border: none !important;
            color: #1a1a1a !important;
            padding: 0 !important;
            margin: 0.5in 0 0.3in 0 !important;
        }

        h1 {
            font-size: 32pt !important;
            font-weight: 300 !important;
            line-height: 1.2 !important;
            letter-spacing: -1px !important;
        }

        h2 {
            font-size: 22pt !important;
            font-weight: 500 !important;
            line-height: 1.3 !important;
            border-bottom: 2px solid #3498db !important;
            padding-bottom: 0.12in !important;
            margin-top: 0.7in !important;
            margin-bottom: calc(25pt * 0.75) !important;  /* 75% of paragraph spacing */
        }

        /* Connect first element after header */
        h2 + p, h2 + ul, h2 + ol {
            margin-top: calc(25pt * 0.5) !important;  /* 50% of paragraph spacing */
        }

        h3 {
            font-size: 17pt !important;
            font-weight: 500 !important;
            line-height: 1.4 !important;
            margin-top: 0.5in !important;
            margin-bottom: 0.25in !important;
        }

        /* Remove any inline styles that might add backgrounds */
        * {
            background-color: transparent !important;
        }

        body {
            background-color: #ffffff !important;
        }
        """

    @staticmethod
    def get_enhanced_table_styles() -> str:
        """Get enhanced CSS for table styling."""
        return """
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.4in 0;
            font-size: 10pt;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-radius: 4px;
            overflow: hidden;
        }

        th {
            background: #34495e !important;
            color: #ffffff !important;
            border: none;
            padding: 0.2in 0.25in;
            text-align: left;
            font-weight: 600;
            font-size: 10.5pt;
            letter-spacing: 0.3px;
        }

        td {
            border: none;
            border-bottom: 1px solid #e9ecef;
            padding: 0.15in 0.25in;
            color: #2c3e50;
            background: #ffffff !important;
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:nth-child(even) td {
            background: #f8f9fa !important;
        }
        """

    @staticmethod
    def get_enhanced_typography() -> str:
        """Get enhanced typography CSS with high-priority formatting fixes."""
        # Paragraph spacing constant (0.35in = ~25pt)
        paragraph_spacing = "0.35in"
        paragraph_spacing_pt = "25pt"

        return f"""
        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.75;
            color: #2c2c2c;
            text-align: justify;
            hyphens: auto;
        }}

        /* Paragraphs - consistent spacing */
        p {{
            margin: 0 0 {paragraph_spacing} 0;
            text-align: justify;
            line-height: 1.75;
        }}

        p:first-child {{
            margin-top: 0;
        }}

        p:empty {{
            display: none;
            margin: 0;
            padding: 0;
        }}

        /* HIGH PRIORITY FIX #1: List Spacing - consistent vertical rhythm */
        ul, ol {{
            margin: {paragraph_spacing} 0 {paragraph_spacing} 0;
            padding-left: 20pt;
        }}

        li {{
            margin-bottom: calc({paragraph_spacing_pt} / 2);
            word-wrap: break-word;
            overflow-wrap: break-word;
            hyphens: auto;
        }}

        /* Nested lists - proper indentation hierarchy */
        ul ul, ol ol, ul ol, ol ul {{
            margin-top: calc({paragraph_spacing_pt} / 2);
            margin-bottom: calc({paragraph_spacing_pt} / 2);
            padding-left: 25pt;
        }}

        ul ul ul, ol ol ol {{
            padding-left: 30pt;
        }}

        /* Bold/Italic in lists */
        li strong, li em {{
            font-weight: bold;
            font-style: normal;
        }}

        li em {{
            font-style: italic;
        }}

        li strong em, li em strong {{
            font-weight: bold;
            font-style: italic;
        }}

        /* HIGH PRIORITY FIX #2: Paragraph spacing after headers */
        h2 {{
            margin-bottom: calc({paragraph_spacing_pt} * 0.75) !important;
        }}

        h2 + p, h2 + ul, h2 + ol, h2 + blockquote {{
            margin-top: calc({paragraph_spacing_pt} * 0.5);
        }}

        h3 + p, h3 + ul, h3 + ol {{
            margin-top: calc({paragraph_spacing_pt} * 0.5);
        }}

        /* HIGH PRIORITY FIX #3: Code block line breaks - preserve formatting */
        code {{
            font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
            font-size: 9.5pt;
            background: #f8f9fa80;
            padding: 1pt 3pt;
            border-radius: 3px;
            color: #e83e8c;
            border: 1px solid #e9ecef;
        }}

        pre {{
            background: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 0.3in;
            margin: {paragraph_spacing} 0;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 9.5pt;
            line-height: 1.6;
            white-space: pre-wrap !important;
            word-wrap: break-word;
            overflow-wrap: break-word;
            page-break-inside: avoid;
        }}

        pre code {{
            white-space: pre !important;
            display: block;
            background: transparent;
            padding: 0;
            color: #2c3e50;
            border: none;
        }}

        /* Inline code vs block code distinction */
        code:not(pre code) {{
            background: #f8f9fa80;
            padding: 1pt 3pt;
        }}

        /* HIGH PRIORITY FIX #4: Horizontal rules spacing */
        hr {{
            border: none;
            border-top: 1pt solid #2c2c2c33;
            margin: {paragraph_spacing} 0 {paragraph_spacing} 0;
            padding: 0;
            height: 0;
        }}

        /* HIGH PRIORITY FIX #5: Link styling */
        a {{
            color: #3498db;
            text-decoration: underline;
        }}

        a:visited {{
            color: #2980b9aa;
        }}

        /* Blockquotes - enhanced styling */
        blockquote {{
            border-left: 4px solid #3498db;
            background: #f8f9fa20;
            padding: calc({paragraph_spacing_pt} / 2) {paragraph_spacing};
            margin: {paragraph_spacing} 0;
            padding-left: {paragraph_spacing};
            font-style: italic;
            color: #2c2c2cdd;
            border-radius: 0 4px 4px 0;
            page-break-inside: avoid;
        }}

        blockquote p {{
            margin-bottom: calc({paragraph_spacing_pt} / 2);
        }}

        blockquote p:last-child {{
            margin-bottom: 0;
        }}

        /* Table cell padding - increased for readability */
        th, td {{
            padding: 6pt 8pt !important;
        }}
        """

    @staticmethod
    def get_page_styling() -> str:
        """Get page-level CSS styling."""
        return """
        @page {
            size: letter;
            margin: 0.75in;
            @top-center {
                content: "WAFT D&D Binder";
                font-family: 'Helvetica Neue', sans-serif;
                font-size: 9pt;
                color: #7f8c8d;
            }
            @bottom-center {
                content: "Page " counter(page);
                font-family: 'Helvetica Neue', sans-serif;
                font-size: 9pt;
                color: #7f8c8d;
            }
        }

        @page :first {
            @top-center { content: none; }
            @bottom-center { content: none; }
        }
        """

    @staticmethod
    def get_complete_styles() -> str:
        """Get complete enhanced CSS for PDF generation."""
        return (
            PDFStylingEnhancer.get_page_styling()
            + PDFStylingEnhancer.get_clean_header_styles()
            + PDFStylingEnhancer.get_enhanced_typography()
            + PDFStylingEnhancer.get_enhanced_table_styles()
        )


class ImprovedPDFGenerator:
    """Improved PDF generator with enhanced algorithms."""

    def __init__(self):
        self.content_processor = PDFContentProcessor()
        self.styling_enhancer = PDFStylingEnhancer()

    def generate_from_markdown(
        self,
        markdown_content: str,
        title: str,
        output_path: Path,
        template_html: str | None = None,
        custom_css: str | None = None,
    ) -> Path:
        """
        Generate PDF from markdown with improved algorithms.

        Args:
            markdown_content: Markdown text
            title: Document title
            output_path: Output PDF path
            template_html: Optional HTML template (Jinja2 format)
            custom_css: Optional additional CSS

        Returns:
            Path to generated PDF
        """
        from jinja2 import Template
        from weasyprint import HTML

        # Process markdown to HTML
        html_content = self.content_processor.markdown_to_html(markdown_content)

        # Get enhanced CSS
        base_css = self.styling_enhancer.get_complete_styles()
        if custom_css:
            base_css += f"\n/* Custom CSS */\n{custom_css}\n"

        # Use template or create default
        if template_html:
            template = Template(template_html)
            full_html = template.render(title=title, content=html_content, css=base_css)
        else:
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>{title}</title>
                <style>
                {base_css}
                </style>
            </head>
            <body>
                <h1>{title}</h1>
                {html_content}
            </body>
            </html>
            """

        # Generate PDF
        HTML(string=full_html).write_pdf(str(output_path))

        return output_path

    def generate_binder(
        self, sections: dict[str, str], title: str, output_path: Path, toc: bool = True
    ) -> Path:
        """
        Generate a multi-section binder PDF.

        Args:
            sections: Dictionary of section_name -> markdown_content
            title: Binder title
            output_path: Output PDF path
            toc: Include table of contents

        Returns:
            Path to generated PDF
        """
        from weasyprint import HTML

        # Process all sections
        processed_sections = {}
        for section_name, markdown_content in sections.items():
            processed_sections[section_name] = self.content_processor.markdown_to_html(
                markdown_content
            )

        # Build HTML
        toc_html = ""
        if toc:
            toc_html = "<div class='toc-page'><h1>Table of Contents</h1><ul>"
            for section_name in sections.keys():
                toc_html += f"<li><a href='#{section_name}'>{section_name}</a></li>"
            toc_html += "</ul></div>"

        sections_html = ""
        for section_name, html_content in processed_sections.items():
            sections_html += f"<div class='section' id='{section_name}'>"
            sections_html += f"<h1>{section_name}</h1>"
            sections_html += html_content
            sections_html += "</div>"

        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <style>
            {self.styling_enhancer.get_complete_styles()}
            .toc-page {{
                page-break-after: always;
            }}
            .section {{
                page-break-before: always;
            }}
            </style>
        </head>
        <body>
            <div class="cover-page">
                <h1>{title}</h1>
            </div>
            {toc_html}
            {sections_html}
        </body>
        </html>
        """

        # Generate PDF
        HTML(string=full_html).write_pdf(str(output_path))

        return output_path
