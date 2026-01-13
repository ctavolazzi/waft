"""
Flexible PDF Generator - No Page Constraints

A flexible PDF generator designed for evolving formatting ideas and testing
markdown-to-PDF conversion improvements. No page limits, full markdown support,
and comprehensive CSS styling for proper typography.

Use this instead of TwoPageGenerator when you need:
- No page constraints
- Full markdown content rendering
- Testing formatting improvements
- Evolving CSS styling
"""

from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from jinja2 import Template
import re

from .styling_genome import StylingGenome
from .chat_distiller import ChatDistiller, DistilledChat


# Flexible HTML template - no page constraints, full markdown support
FLEXIBLE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        @page {
            size: letter;
            margin: {{ margin.top }}mm {{ margin.right }}mm {{ margin.bottom }}mm {{ margin.left }}mm;
        }

        body {
            font-family: {{ font.family }};
            font-size: {{ font.size_body }}pt;
            line-height: {{ font.line_height }};
            color: {{ color.text }};
            background: {{ color.background }};
            margin: 0;
            padding: 0;
        }

        /* Prevent orphans/widows */
        p, li {
            orphans: 2;
            widows: 2;
        }

        /* Typography */
        h1 {
            font-size: {{ font.size_h1 }}pt;
            color: {{ color.heading }};
            margin-top: 0;
            margin-bottom: {{ margin.section_spacing }}pt;
            page-break-after: avoid;
            border-bottom: 2pt solid {{ color.accent }};
            padding-bottom: 4pt;
        }

        h2 {
            font-size: {{ font.size_h2 }}pt;
            color: {{ color.heading }};
            margin-top: {{ margin.section_spacing }}pt;
            margin-bottom: {{ margin.paragraph_spacing * 0.75 }}pt;
            page-break-after: avoid;
            border-bottom: 1pt solid {{ color.accent }};
            padding-bottom: 2pt;
        }

        h2 + p, h2 + ul, h2 + ol, h2 + blockquote {
            margin-top: {{ margin.paragraph_spacing * 0.5 }}pt;
        }

        h3 {
            font-size: {{ font.size_h3 }}pt;
            color: {{ color.heading }};
            margin-top: {{ margin.paragraph_spacing }}pt;
            margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;
            page-break-after: avoid;
        }

        h4, h5, h6 {
            font-size: {{ font.size_h3 - 1 }}pt;
            color: {{ color.heading }};
            margin-top: {{ margin.paragraph_spacing * 0.75 }}pt;
            margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;
            page-break-after: avoid;
        }

        p {
            margin: 0 0 {{ margin.paragraph_spacing }}pt 0;
        }

        p:empty {
            display: none;
            margin: 0;
            padding: 0;
        }

        /* Lists - improved spacing */
        ul, ol {
            margin: {{ margin.paragraph_spacing }}pt 0 {{ margin.paragraph_spacing }}pt 0;
            padding-left: 20pt;
        }

        li {
            margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;
            word-wrap: break-word;
            overflow-wrap: break-word;
            hyphens: auto;
        }

        /* Nested lists */
        ul ul, ol ol, ul ol, ol ul {
            margin-top: {{ margin.paragraph_spacing / 2 }}pt;
            margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;
            padding-left: 30pt;
        }

        ul ul ul, ol ol ol {
            padding-left: 40pt;
        }

        /* Code blocks - preserve formatting */
        code {
            font-family: monospace;
            font-size: {{ font.size_code }}pt;
            background: {{ color.code_bg }}80;
            color: {{ color.code_text }};
            padding: 1pt 3pt;
            border-radius: 2pt;
        }

        pre {
            background: {{ color.code_bg }};
            padding: {{ margin.paragraph_spacing / 2 }}pt;
            border-left: 3pt solid {{ color.accent }};
            font-size: {{ font.size_code }}pt;
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow-wrap: break-word;
            overflow-x: auto;
            page-break-inside: avoid;
            margin: {{ margin.paragraph_spacing }}pt 0;
        }

        pre code {
            white-space: pre;
            display: block;
            background: {{ color.code_bg }};
            padding: {{ margin.paragraph_spacing / 2 }}pt;
        }

        /* Blockquotes */
        blockquote {
            border-left: 4pt solid {{ color.accent }};
            background: {{ color.code_bg }}20;
            padding: {{ margin.paragraph_spacing / 2 }}pt {{ margin.paragraph_spacing }}pt;
            margin: {{ margin.paragraph_spacing }}pt 0;
            padding-left: {{ margin.paragraph_spacing }}pt;
            font-style: italic;
            color: {{ color.text }}dd;
            page-break-inside: avoid;
        }

        blockquote p {
            margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;
        }

        blockquote p:last-child {
            margin-bottom: 0;
        }

        /* Links */
        a {
            color: {{ color.accent }};
            text-decoration: underline;
        }

        a:visited {
            color: {{ color.accent }}aa;
        }

        /* Horizontal rules */
        hr {
            border: none;
            border-top: 1pt solid {{ color.text }}33;
            margin: {{ margin.paragraph_spacing }}pt 0 {{ margin.paragraph_spacing }}pt 0;
            padding: 0;
            height: 0;
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: {{ margin.paragraph_spacing }}pt 0;
            font-size: {{ font.size_body - 1 }}pt;
            page-break-inside: avoid;
        }

        th {
            background: {{ color.heading }};
            color: {{ color.background }};
            border: 1pt solid {{ color.text }};
            padding: 6pt 8pt;
            text-align: left;
            font-weight: bold;
        }

        td {
            border: 1pt solid {{ color.text }}33;
            padding: 6pt 8pt;
        }

        tr:nth-child(even) {
            background: {{ color.code_bg }};
        }

        /* Emphasis combinations */
        strong {
            font-weight: bold;
        }

        em {
            font-style: italic;
        }

        strong em, em strong {
            font-weight: bold;
            font-style: italic;
        }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>
    
    {% if metadata %}
    <div style="font-size: {{ font.size_body - 2 }}pt; color: {{ color.text }}88; margin-bottom: {{ margin.paragraph_spacing }}pt;">
        {% for key, value in metadata.items() %}
        <p><strong>{{ key }}:</strong> {{ value }}</p>
        {% endfor %}
    </div>
    {% endif %}

    <div class="content">
        {{ content|safe }}
    </div>
</body>
</html>
"""


class FlexiblePDFGenerator:
    """
    Flexible PDF generator with no page constraints.
    
    Designed for:
    - Testing formatting improvements
    - Evolving CSS styling
    - Full markdown content rendering
    - No page limits
    """
    
    def __init__(
        self,
        styling_genome: StylingGenome,
        weasyprint_available: bool = True
    ):
        """
        Initialize flexible PDF generator.
        
        Args:
            styling_genome: Styling configuration
            weasyprint_available: Whether WeasyPrint is available
        """
        self.styling_genome = styling_genome
        self.weasyprint_available = weasyprint_available
        
        if weasyprint_available:
            try:
                from weasyprint import HTML, __version__
                self.HTML = HTML
                print(f"WeasyPrint {__version__} available")
            except ImportError:
                self.weasyprint_available = False
                print("WeasyPrint not available - HTML output only")
    
    def _markdown_to_html(self, text: str) -> str:
        """
        Convert markdown to HTML with comprehensive formatting support.
        
        Handles:
        - Headers (h1-h6)
        - Bold/italic (including nested)
        - Code (inline and blocks)
        - Lists (ordered, unordered, nested)
        - Links
        - Blockquotes
        - Horizontal rules
        - Tables (if markdown library available)
        """
        if not text:
            return ""
        
        # Try markdown library first (best quality)
        try:
            import markdown
            html = markdown.markdown(
                text,
                extensions=['fenced_code', 'tables', 'nl2br', 'extra', 'codehilite']
            )
            return html
        except ImportError:
            # Fallback: manual conversion
            pass
        
        # Manual conversion (comprehensive fallback)
        html = text
        
        # Code blocks first (before other processing)
        html = re.sub(
            r'```(\w+)?\n(.*?)```',
            r'<pre><code class="language-\1">\2</code></pre>',
            html,
            flags=re.DOTALL
        )
        
        # Inline code
        html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
        
        # Blockquotes (process before paragraphs)
        html = re.sub(
            r'^>\s+(.+)$',
            r'<blockquote>\1</blockquote>',
            html,
            flags=re.MULTILINE
        )
        
        # Headers (h6 to h1 to avoid conflicts)
        html = re.sub(r'^######\s+(.+)$', r'<h6>\1</h6>', html, flags=re.MULTILINE)
        html = re.sub(r'^#####\s+(.+)$', r'<h5>\1</h5>', html, flags=re.MULTILINE)
        html = re.sub(r'^####\s+(.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
        html = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^##\s+(.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^#\s+(.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # Bold (**text** or __text__)
        html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', html)
        
        # Italic (*text* or _text_) - careful with nested emphasis
        html = re.sub(r'(?<!<strong>)(?<!\*)\*([^*<]+)\*(?!\*)(?!</strong>)', r'<em>\1</em>', html)
        html = re.sub(r'(?<!<strong>)(?<!_)_([^_<]+)_(?!_)(?!</strong>)', r'<em>\1</em>', html)
        
        # Links
        html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)
        
        # Lists - process line by line
        lines = html.split('\n')
        result = []
        in_list = False
        list_type = None
        
        for line in lines:
            # Ordered list
            if re.match(r'^\s*\d+\.\s+', line):
                if not in_list or list_type != 'ol':
                    if in_list:
                        result.append(f'</{list_type}>')
                    result.append('<ol>')
                    in_list = True
                    list_type = 'ol'
                item_text = re.sub(r'^\s*\d+\.\s+', '', line)
                result.append(f'<li>{item_text}</li>')
            # Unordered list
            elif re.match(r'^\s*[-*+]\s+', line):
                if not in_list or list_type != 'ul':
                    if in_list:
                        result.append(f'</{list_type}>')
                    result.append('<ul>')
                    in_list = True
                    list_type = 'ul'
                item_text = re.sub(r'^\s*[-*+]\s+', '', line)
                result.append(f'<li>{item_text}</li>')
            else:
                if in_list:
                    result.append(f'</{list_type}>')
                    in_list = False
                    list_type = None
                if line.strip():
                    # Don't wrap if already HTML tag
                    if not (line.strip().startswith('<h') or 
                            line.strip().startswith('<pre') or
                            line.strip().startswith('<code') or
                            line.strip().startswith('<ul') or
                            line.strip().startswith('<ol') or
                            line.strip().startswith('<blockquote') or
                            line.strip().startswith('<hr') or
                            line.strip().startswith('<table')):
                        result.append(f'<p>{line}</p>')
                    else:
                        result.append(line)
                else:
                    result.append('')
        
        if in_list:
            result.append(f'</{list_type}>')
        
        html = '\n'.join(result)
        
        # Horizontal rules
        html = re.sub(r'^---$', r'<hr>', html, flags=re.MULTILINE)
        html = re.sub(r'^\*\*\*$', r'<hr>', html, flags=re.MULTILINE)
        
        return html
    
    def _render_html(
        self,
        content: str,
        title: str,
        metadata: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Render HTML from markdown content.
        
        Args:
            content: Markdown content
            title: Document title
            metadata: Optional metadata dict
            
        Returns:
            HTML string
        """
        # Convert markdown to HTML
        html_content = self._markdown_to_html(content)
        
        # Get styling values
        font = self.styling_genome.genes.font
        margin = self.styling_genome.genes.margin
        color = self.styling_genome.genes.color
        
        # Render template
        template = Template(FLEXIBLE_TEMPLATE)
        html = template.render(
            title=title,
            content=html_content,
            metadata=metadata or {},
            font={
                'family': font.family,
                'size_body': font.size_body,
                'size_h1': font.size_h1,
                'size_h2': font.size_h2,
                'size_h3': font.size_h3,
                'size_code': font.size_code,
                'line_height': font.line_height
            },
            margin={
                'top': margin.top,
                'right': margin.right,
                'bottom': margin.bottom,
                'left': margin.left,
                'section_spacing': margin.section_spacing,
                'paragraph_spacing': margin.paragraph_spacing
            },
            color={
                'text': color.text,
                'background': color.background,
                'heading': color.heading,
                'accent': color.accent,
                'code_bg': color.code_bg,
                'code_text': color.code_text
            }
        )
        
        return html
    
    def generate(
        self,
        content: str,
        title: str,
        output_path: Path,
        metadata: Optional[Dict[str, str]] = None
    ) -> Path:
        """
        Generate PDF from markdown content.
        
        Args:
            content: Markdown content
            title: Document title
            output_path: Output PDF path
            metadata: Optional metadata dict
            
        Returns:
            Path to generated PDF
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Render HTML
        html_content = self._render_html(content, title, metadata)
        
        # Save HTML
        html_path = output_path.with_suffix('.html')
        html_path.write_text(html_content)
        
        # Generate PDF
        if self.weasyprint_available:
            self.HTML(string=html_content, base_url=str(output_path.parent)).write_pdf(
                output_path,
                presentational_hints=True,
                optimize_images=True
            )
            print(f"✅ PDF generated: {output_path}")
        else:
            print(f"⚠️  WeasyPrint not available - HTML saved: {html_path}")
        
        return output_path
    
    @classmethod
    def from_content(
        cls,
        content: str,
        title: str,
        style: str = "clinical_standard",
        **overrides
    ) -> "FlexiblePDFGenerator":
        """
        Create flexible PDF generator from content.
        
        Args:
            content: Markdown content
            title: Document title
            style: Preset style name
            **overrides: Style overrides
            
        Returns:
            FlexiblePDFGenerator instance
        """
        from .pdf_generator import PDFGenerator
        
        # Get preset
        if style not in PDFGenerator.PRESETS:
            raise ValueError(f"Unknown style: {style}")
        
        preset = PDFGenerator.PRESETS[style].copy()
        
        # Apply overrides
        if "font_size" in overrides:
            preset["font"]["size_body"] = overrides.pop("font_size")
        if "margins" in overrides:
            margins = overrides.pop("margins")
            if isinstance(margins, (int, float)):
                preset["margin"]["top"] = preset["margin"]["bottom"] = preset["margin"]["left"] = preset["margin"]["right"] = margins
            elif len(margins) == 4:
                preset["margin"]["top"], preset["margin"]["right"], preset["margin"]["bottom"], preset["margin"]["left"] = margins
        
        # Create styling genome
        from .styling_genome import StylingGenome, StylingGene, FontGene, MarginGene, ColorGene, LayoutGene
        
        styling_genes = StylingGene(
            font=FontGene(**preset["font"]),
            margin=MarginGene(**preset["margin"]),
            color=ColorGene(**preset["color"]),
            layout=LayoutGene(
                columns=1,
                density="normal",
                toc_enabled=False,
                page_numbers=True,
                header_enabled=False,
                footer_enabled=False
            ),
            name=f"{style.title()} - {title[:30]}"
        )
        
        genome = StylingGenome.from_genes(styling_genes)
        
        return cls(styling_genome=genome, weasyprint_available=True)
    
    def save(
        self,
        content: str,
        title: str,
        output_path: Path,
        metadata: Optional[Dict[str, str]] = None
    ) -> Path:
        """
        Generate and save PDF.
        
        Args:
            content: Markdown content
            title: Document title
            output_path: Output PDF path
            metadata: Optional metadata
            
        Returns:
            Path to generated PDF
        """
        return self.generate(content, title, output_path, metadata)
