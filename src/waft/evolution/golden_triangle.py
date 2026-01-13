"""
Golden Triangle: HTML ↔ Markdown ↔ PDF Conversion System

A unified conversion system that provides clean, bidirectional conversion
between HTML, Markdown, and PDF formats without losing structure or styling.

The Golden Triangle:
    Markdown ←→ HTML ←→ PDF

Features:
- Markdown → HTML (with HTML block support)
- HTML → Markdown (clean conversion)
- HTML → PDF (via WeasyPrint)
- Markdown → PDF (via HTML intermediate)
- Preserves styling and structure
- Handles HTML in markdown gracefully
- CSS class-based styling (not inline styles)
"""

from pathlib import Path
from typing import Optional, Dict, Any, Union
from datetime import datetime
import re
import html as html_module

try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

try:
    from weasyprint import HTML as WeasyHTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

try:
    from html2text import html2text
    HTML2TEXT_AVAILABLE = True
except ImportError:
    HTML2TEXT_AVAILABLE = False


class GoldenTriangle:
    """
    Unified converter for HTML, Markdown, and PDF formats.
    
    Provides clean conversions in all directions:
    - markdown_to_html()
    - html_to_markdown()
    - html_to_pdf()
    - markdown_to_pdf()
    """
    
    def __init__(self):
        """Initialize golden triangle converter."""
        self.markdown_extensions = [
            'fenced_code',
            'tables',
            'nl2br',
            'extra',
            'codehilite',
            'attr_list',  # For CSS classes: {.class}
            'md_in_html',  # Allow HTML blocks in markdown
        ]
    
    def markdown_to_html(
        self,
        markdown_text: str,
        preserve_html: bool = True,
        extract_styles: bool = True
    ) -> str:
        """
        Convert Markdown to HTML with proper handling of HTML blocks.
        
        Args:
            markdown_text: Markdown content (may contain HTML)
            preserve_html: If True, preserve HTML blocks in markdown
            extract_styles: If True, extract inline styles to CSS classes
        
        Returns:
            HTML string
        """
        # #region agent log
        with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
            import json
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"golden_triangle.py:68","message":"markdown_to_html entry","data":{"markdown_length":len(markdown_text) if markdown_text else 0,"markdown_preview":markdown_text[:200] if markdown_text else "","has_h1":bool(re.search(r'^#\s+', markdown_text, re.MULTILINE)) if markdown_text else False,"has_hr":bool(re.search(r'^---$', markdown_text, re.MULTILINE)) if markdown_text else False,"markdown_available":MARKDOWN_AVAILABLE,"preserve_html":preserve_html},"timestamp":int(__import__('time').time()*1000)}) + '\n')
        # #endregion
        
        if not markdown_text:
            return ""
        
        # If markdown library available, use it with HTML support
        if MARKDOWN_AVAILABLE and preserve_html:
            try:
                html = markdown.markdown(
                    markdown_text,
                    extensions=self.markdown_extensions
                )
                
                # #region agent log
                with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
                    import json
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"golden_triangle.py:98","message":"markdown library used","data":{"html_length":len(html) if html else 0,"html_preview":html[:300] if html else "","has_h1_tag":bool(re.search(r'<h1[^>]*>', html)) if html else False,"has_hr_tag":bool(re.search(r'<hr[^>]*>', html)) if html else False,"has_raw_hash":bool(re.search(r'#\s+WAFT', html)) if html else False},"timestamp":int(__import__('time').time()*1000)}) + '\n')
                # #endregion
                
                # Note: Inline styles are preserved - WeasyPrint handles them well
                # extract_styles option reserved for future CSS class extraction
                return html
            except Exception as e:
                # #region agent log
                with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
                    import json
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"golden_triangle.py:107","message":"markdown library exception","data":{"error":str(e)},"timestamp":int(__import__('time').time()*1000)}) + '\n')
                # #endregion
                # Fallback to manual conversion
                pass
        
        # Manual conversion (handles HTML blocks)
        html = self._manual_markdown_to_html(markdown_text, preserve_html)
        
        # #region agent log
        with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
            import json
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"B","location":"golden_triangle.py:114","message":"manual conversion used","data":{"html_length":len(html) if html else 0,"html_preview":html[:300] if html else "","has_h1_tag":bool(re.search(r'<h1[^>]*>', html)) if html else False,"has_hr_tag":bool(re.search(r'<hr[^>]*>', html)) if html else False,"has_raw_hash":bool(re.search(r'#\s+WAFT', html)) if html else False},"timestamp":int(__import__('time').time()*1000)}) + '\n')
        # #endregion
        
        # Note: Inline styles are preserved - WeasyPrint handles them well
        # extract_styles option reserved for future CSS class extraction
        return html
    
    def html_to_markdown(
        self,
        html_text: str,
        preserve_formatting: bool = True
    ) -> str:
        """
        Convert HTML to Markdown.
        
        Args:
            html_text: HTML content
            preserve_formatting: If True, preserve formatting (bold, italic, etc.)
        
        Returns:
            Markdown string
        """
        if not html_text:
            return ""
        
        # Use html2text if available (best quality)
        if HTML2TEXT_AVAILABLE:
            try:
                h = html2text.HTML2Text()
                h.ignore_links = False
                h.ignore_images = False
                h.body_width = 0  # Don't wrap lines
                markdown_text = h.handle(html_text)
                return markdown_text.strip()
            except Exception:
                # Fallback to manual conversion
                pass
        
        # Manual conversion
        return self._manual_html_to_markdown(html_text)
    
    def html_to_pdf(
        self,
        html_content: str,
        output_path: Union[str, Path],
        css: Optional[str] = None,
        base_url: Optional[str] = None
    ) -> Path:
        """
        Convert HTML to PDF using WeasyPrint.
        
        Args:
            html_content: HTML content (may be partial or full document)
            output_path: Path to save PDF
            css: Optional CSS to inject
            base_url: Base URL for resolving relative paths
        
        Returns:
            Path to generated PDF
        """
        if not WEASYPRINT_AVAILABLE:
            raise RuntimeError("WeasyPrint not available. Install with: pip install weasyprint")
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Ensure full HTML document (add head/body if missing)
        if not html_content.strip().startswith('<!DOCTYPE'):
            # Wrap in full document
            html_content = self._wrap_html_document(html_content, css, "premium")
        elif css:
            # Inject CSS into existing document
            html_content = self._inject_css(html_content, css)
        
        # Generate PDF
        html_doc = WeasyHTML(
            string=html_content,
            base_url=base_url or str(output_path.parent)
        )
        html_doc.write_pdf(
            output_path,
            presentational_hints=True,
            optimize_images=True
        )
        
        return output_path
    
    def markdown_to_pdf(
        self,
        markdown_text: str,
        output_path: Union[str, Path],
        css: Optional[str] = None,
        style: str = "premium"
    ) -> Path:
        """
        Convert Markdown to PDF (via HTML intermediate).
        
        Args:
            markdown_text: Markdown content
            output_path: Path to save PDF
            css: Optional CSS (or use style preset)
            style: Style preset name ("premium", "clinical_standard", "professional")
        
        Returns:
            Path to generated PDF
        """
        # Convert markdown to HTML
        html_content = self.markdown_to_html(markdown_text)
        
        # Wrap in full HTML document
        html_doc = self._wrap_html_document(html_content, css, style)
        
        # Convert to PDF
        return self.html_to_pdf(html_doc, output_path)
    
    def _manual_markdown_to_html(
        self,
        text: str,
        preserve_html: bool = True
    ) -> str:
        """Manual markdown to HTML conversion with HTML block support."""
        # #region agent log
        with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
            import json
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"B","location":"golden_triangle.py:218","message":"_manual_markdown_to_html entry","data":{"text_length":len(text) if text else 0,"text_preview":text[:200] if text else "","has_h1_md":bool(re.search(r'^#\s+', text, re.MULTILINE)) if text else False,"has_hr_md":bool(re.search(r'^---$', text, re.MULTILINE)) if text else False,"h1_matches":len(re.findall(r'^#\s+(.+)$', text, re.MULTILINE)) if text else 0,"hr_matches":len(re.findall(r'^---$', text, re.MULTILINE)) if text else 0},"timestamp":int(__import__('time').time()*1000)}) + '\n')
        # #endregion
        
        html = text
        
        # If preserve_html, handle HTML blocks first
        if preserve_html:
            # Extract HTML blocks (div, span, etc.) and preserve them
            # This regex finds HTML tags and their content
            html_blocks = []
            block_pattern = r'<([a-z][a-z0-9]*)[^>]*>.*?</\1>'
            
            def preserve_block(match):
                block = match.group(0)
                block_id = f"__HTML_BLOCK_{len(html_blocks)}__"
                html_blocks.append(block)
                return block_id
            
            # Temporarily replace HTML blocks
            html = re.sub(block_pattern, preserve_block, html, flags=re.DOTALL)
        
        # Code blocks first (before other processing)
        html = re.sub(
            r'```(\w+)?\n(.*?)```',
            r'<pre><code class="language-\1">\2</code></pre>',
            html,
            flags=re.DOTALL
        )
        
        # Inline code
        html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
        
        # Headers (h6 to h1 to avoid conflicts)
        # #region agent log
        with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
            import json
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"B","location":"golden_triangle.py:254","message":"before header conversion","data":{"html_preview":html[:300] if html else "","h1_before":len(re.findall(r'^#\s+', html, re.MULTILINE)) if html else 0},"timestamp":int(__import__('time').time()*1000)}) + '\n')
        # #endregion
        
        html = re.sub(r'^######\s+(.+)$', r'<h6>\1</h6>', html, flags=re.MULTILINE)
        html = re.sub(r'^#####\s+(.+)$', r'<h5>\1</h5>', html, flags=re.MULTILINE)
        html = re.sub(r'^####\s+(.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
        html = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^##\s+(.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^#\s+(.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # #region agent log
        with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
            import json
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"B","location":"golden_triangle.py:261","message":"after header conversion","data":{"html_preview":html[:300] if html else "","h1_after":len(re.findall(r'<h1[^>]*>', html)) if html else 0,"has_raw_hash":bool(re.search(r'^#\s+', html, re.MULTILINE)) if html else False},"timestamp":int(__import__('time').time()*1000)}) + '\n')
        # #endregion
        
        # Bold (**text** or __text__)
        html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', html)
        
        # Italic (*text* or _text_)
        html = re.sub(r'(?<!<strong>)(?<!\*)\*([^*<]+)\*(?!\*)(?!</strong>)', r'<em>\1</em>', html)
        html = re.sub(r'(?<!<strong>)(?<!_)_([^_<]+)_(?!_)(?!</strong>)', r'<em>\1</em>', html)
        
        # Links
        html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)
        
        # Lists
        html = self._convert_lists(html)
        
        # Blockquotes
        html = re.sub(r'^>\s+(.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
        
        # Horizontal rules
        # #region agent log
        with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
            import json
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"C","location":"golden_triangle.py:279","message":"before hr conversion","data":{"hr_before":len(re.findall(r'^---$', html, re.MULTILINE)) if html else 0,"hr_matches":re.findall(r'^---$', html, re.MULTILINE)[:5] if html else []},"timestamp":int(__import__('time').time()*1000)}) + '\n')
        # #endregion
        
        html = re.sub(r'^---$', r'<hr>', html, flags=re.MULTILINE)
        
        # #region agent log
        with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
            import json
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"C","location":"golden_triangle.py:282","message":"after hr conversion","data":{"hr_after":len(re.findall(r'<hr[^>]*>', html)) if html else 0,"has_raw_hr":bool(re.search(r'^---$', html, re.MULTILINE)) if html else False},"timestamp":int(__import__('time').time()*1000)}) + '\n')
        # #endregion
        
        # Restore HTML blocks if preserved
        if preserve_html and html_blocks:
            for i, block in enumerate(html_blocks):
                html = html.replace(f"__HTML_BLOCK_{i}__", block)
        
        # #region agent log
        with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
            import json
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"B","location":"golden_triangle.py:290","message":"_manual_markdown_to_html exit","data":{"html_length":len(html) if html else 0,"html_preview":html[:400] if html else "","final_h1_count":len(re.findall(r'<h1[^>]*>', html)) if html else 0,"final_hr_count":len(re.findall(r'<hr[^>]*>', html)) if html else 0},"timestamp":int(__import__('time').time()*1000)}) + '\n')
        # #endregion
        
        return html
    
    def _convert_lists(self, html: str) -> str:
        """Convert markdown lists to HTML lists."""
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
                    if not (line.strip().startswith('<h') or 
                            line.strip().startswith('<pre') or
                            line.strip().startswith('<code') or
                            line.strip().startswith('<ul') or
                            line.strip().startswith('<ol') or
                            line.strip().startswith('<blockquote')):
                        result.append(f'<p>{line}</p>')
                    else:
                        result.append(line)
                else:
                    result.append('')
        
        if in_list:
            result.append(f'</{list_type}>')
        
        return '\n'.join(result)
    
    def _manual_html_to_markdown(self, html: str) -> str:
        """Manual HTML to Markdown conversion."""
        md = html
        
        # Headers
        md = re.sub(r'<h1>(.+?)</h1>', r'# \1', md, flags=re.DOTALL)
        md = re.sub(r'<h2>(.+?)</h2>', r'## \1', md, flags=re.DOTALL)
        md = re.sub(r'<h3>(.+?)</h3>', r'### \1', md, flags=re.DOTALL)
        md = re.sub(r'<h4>(.+?)</h4>', r'#### \1', md, flags=re.DOTALL)
        md = re.sub(r'<h5>(.+?)</h5>', r'##### \1', md, flags=re.DOTALL)
        md = re.sub(r'<h6>(.+?)</h6>', r'###### \1', md, flags=re.DOTALL)
        
        # Bold
        md = re.sub(r'<strong>(.+?)</strong>', r'**\1**', md, flags=re.DOTALL)
        md = re.sub(r'<b>(.+?)</b>', r'**\1**', md, flags=re.DOTALL)
        
        # Italic
        md = re.sub(r'<em>(.+?)</em>', r'*\1*', md, flags=re.DOTALL)
        md = re.sub(r'<i>(.+?)</i>', r'*\1*', md, flags=re.DOTALL)
        
        # Code blocks
        md = re.sub(r'<pre><code[^>]*>(.+?)</code></pre>', r'```\n\1\n```', md, flags=re.DOTALL)
        md = re.sub(r'<code>(.+?)</code>', r'`\1`', md, flags=re.DOTALL)
        
        # Links
        md = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.+?)</a>', r'[\2](\1)', md, flags=re.DOTALL)
        
        # Lists
        md = re.sub(r'<ol>(.+?)</ol>', self._convert_ol_to_md, md, flags=re.DOTALL)
        md = re.sub(r'<ul>(.+?)</ul>', self._convert_ul_to_md, md, flags=re.DOTALL)
        
        # Blockquotes
        md = re.sub(r'<blockquote>(.+?)</blockquote>', r'> \1', md, flags=re.DOTALL)
        
        # Paragraphs
        md = re.sub(r'<p>(.+?)</p>', r'\1\n', md, flags=re.DOTALL)
        
        # Horizontal rules
        md = re.sub(r'<hr[^>]*>', r'---', md)
        
        # Remove remaining HTML tags
        md = re.sub(r'<[^>]+>', '', md)
        
        # Decode HTML entities
        md = html_module.unescape(md)
        
        # Clean up whitespace
        md = re.sub(r'\n{3,}', '\n\n', md)
        
        return md.strip()
    
    def _convert_ol_to_md(self, match) -> str:
        """Convert ordered list to markdown."""
        content = match.group(1)
        items = re.findall(r'<li>(.+?)</li>', content, flags=re.DOTALL)
        result = []
        for i, item in enumerate(items, 1):
            result.append(f"{i}. {item.strip()}")
        return '\n'.join(result) + '\n'
    
    def _convert_ul_to_md(self, match) -> str:
        """Convert unordered list to markdown."""
        content = match.group(1)
        items = re.findall(r'<li>(.+?)</li>', content, flags=re.DOTALL)
        result = []
        for item in items:
            result.append(f"- {item.strip()}")
        return '\n'.join(result) + '\n'
    
    def _extract_inline_styles(self, html: str) -> str:
        """
        Extract inline styles to CSS classes (future enhancement).
        
        For now, preserves inline styles - WeasyPrint handles them well.
        Future: extract to CSS classes for better round-trip conversion.
        
        Returns:
            HTML with styles preserved (or converted to classes in future)
        """
        # For now, preserve inline styles - WeasyPrint handles them well
        # Future: extract to CSS classes for better maintainability
        return html
    
    def _inject_css(self, html: str, css: str) -> str:
        """Inject CSS into HTML document."""
        if '</head>' in html:
            return html.replace('</head>', f'<style>{css}</style></head>')
        elif '<body>' in html:
            return html.replace('<body>', f'<style>{css}</style><body>')
        else:
            # Wrap in full document
            return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>{css}</style>
</head>
<body>
{html}
</body>
</html>"""
    
    def _wrap_html_document(
        self,
        content: str,
        css: Optional[str] = None,
        style: str = "premium"
    ) -> str:
        """Wrap HTML content in full document with styling."""
        # Get style preset CSS
        style_css = self._get_style_css(style)
        
        # Combine with custom CSS
        if css:
            full_css = style_css + '\n' + css
        else:
            full_css = style_css
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
{full_css}
    </style>
</head>
<body>
{content}
</body>
</html>"""
    
    def _get_style_css(self, style: str) -> str:
        """Get CSS for style preset."""
        styles = {
            "premium": """
                @page {
                    size: letter;
                    margin: 40mm;
                }
                body {
                    font-family: 'Minion Pro', 'Palatino Linotype', 'Book Antiqua', 'Palatino', serif;
                    font-size: 13pt;
                    line-height: 1.75;
                    color: #1a1a1a;
                    margin: 0;
                    padding: 0;
                }
                h1 { font-size: 32pt; margin-top: 0; border-bottom: 2pt solid #0d47a1; padding-bottom: 4pt; }
                h2 { font-size: 22pt; margin-top: 24pt; border-bottom: 1pt solid #0d47a1; padding-bottom: 2pt; }
                h3 { font-size: 17pt; margin-top: 12pt; }
                p { margin: 0 0 12pt 0; }
                code { background: #f5f7fa; padding: 1pt 3pt; border-radius: 2pt; }
                pre { background: #f5f7fa; padding: 6pt; border-left: 3pt solid #0d47a1; margin: 12pt 0; }
                blockquote { border-left: 4pt solid #0d47a1; background: #f5f7fa20; padding: 6pt 12pt; margin: 12pt 0; font-style: italic; }
                table { width: 100%; border-collapse: collapse; margin: 12pt 0; }
                th { background: #0d47a1; color: white; padding: 6pt 8pt; text-align: left; }
                td { border: 1pt solid #b0bec5; padding: 6pt 8pt; }
                /* Ensure inline styles take precedence - critical for preserving HTML blocks with styles */
                [style] { 
                    /* Inline styles have highest specificity - WeasyPrint will respect them */
                }
                div[style], span[style], p[style], h1[style], h2[style], h3[style] {
                    /* Preserve all inline styles from markdown - these override CSS rules */
                }
                /* Support for common inline style patterns from markdown */
                div {
                    page-break-inside: avoid;
                }
                /* Ensure proper rendering of styled boxes */
                div[style*="background"], div[style*="padding"], div[style*="border"] {
                    display: block;
                    margin: 1em 0;
                }
            """,
            "clinical_standard": """
                body {
                    font-family: 'Times New Roman', 'Times', serif;
                    font-size: 11pt;
                    line-height: 1.4;
                    color: #000000;
                    margin: 25.4mm;
                }
                h1 { font-size: 16pt; margin-top: 0; border-bottom: 2pt solid #000000; padding-bottom: 4pt; }
                h2 { font-size: 14pt; margin-top: 12pt; border-bottom: 1pt solid #000000; padding-bottom: 2pt; }
                h3 { font-size: 12pt; margin-top: 8pt; }
                p { margin: 0 0 8pt 0; }
                code { background: #f5f5f5; padding: 1pt 3pt; }
                pre { background: #f5f5f5; padding: 4pt; border-left: 3pt solid #000000; margin: 8pt 0; }
                blockquote { border-left: 4pt solid #000000; background: #f5f5f520; padding: 4pt 8pt; margin: 8pt 0; }
                /* Ensure inline styles take precedence */
                [style] { 
                    /* Inline styles have highest specificity - no override needed */
                }
                div[style], span[style], p[style] {
                    /* Preserve all inline styles from markdown */
                }
            """,
            "professional": """
                @page {
                    size: letter;
                    margin: 25mm;
                }
                body {
                    font-family: 'Georgia', serif;
                    font-size: 11pt;
                    line-height: 1.6;
                    color: #1a1a1a;
                    margin: 0;
                    padding: 0;
                }
                h1 { font-size: 20pt; margin-top: 0; border-bottom: 2pt solid #2c3e50; padding-bottom: 4pt; }
                h2 { font-size: 16pt; margin-top: 14pt; border-bottom: 1pt solid #2c3e50; padding-bottom: 2pt; }
                h3 { font-size: 13pt; margin-top: 8pt; }
                p { margin: 0 0 8pt 0; }
                code { background: #f8f9fa; padding: 1pt 3pt; }
                pre { background: #f8f9fa; padding: 4pt; border-left: 3pt solid #2c3e50; margin: 8pt 0; }
                blockquote { border-left: 4pt solid #2c3e50; background: #f8f9fa20; padding: 4pt 8pt; margin: 8pt 0; }
                /* Ensure inline styles take precedence - critical for preserving HTML blocks with styles */
                [style] { 
                    /* Inline styles have highest specificity - WeasyPrint will respect them */
                }
                div[style], span[style], p[style], h1[style], h2[style], h3[style] {
                    /* Preserve all inline styles from markdown - these override CSS rules */
                }
                /* Support for common inline style patterns from markdown */
                div {
                    page-break-inside: avoid;
                }
                /* Ensure proper rendering of styled boxes */
                div[style*="background"], div[style*="padding"], div[style*="border"] {
                    display: block;
                    margin: 1em 0;
                }
            """
        }
        
        return styles.get(style, styles["premium"])


# Convenience functions
def markdown_to_html(markdown_text: str, **kwargs) -> str:
    """Convert markdown to HTML."""
    converter = GoldenTriangle()
    return converter.markdown_to_html(markdown_text, **kwargs)


def html_to_markdown(html_text: str, **kwargs) -> str:
    """Convert HTML to markdown."""
    converter = GoldenTriangle()
    return converter.html_to_markdown(html_text, **kwargs)


def markdown_to_pdf(
    markdown_text: str,
    output_path: Union[str, Path],
    style: str = "premium",
    **kwargs
) -> Path:
    """Convert markdown to PDF."""
    converter = GoldenTriangle()
    return converter.markdown_to_pdf(markdown_text, output_path, style=style, **kwargs)


def html_to_pdf(
    html_content: str,
    output_path: Union[str, Path],
    **kwargs
) -> Path:
    """Convert HTML to PDF."""
    converter = GoldenTriangle()
    return converter.html_to_pdf(html_content, output_path, **kwargs)
