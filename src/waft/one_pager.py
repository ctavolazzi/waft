"""
One-Pager Creator
=================

A tool for creating crystalized, printable one-pagers from any content.
Designed for academic nerds who love physical binders full of paper.

Philosophy:
-----------
"Physical constellation of crystallized knowledge inside spacetime 
through the refraction of light" - Christopher Tavolazzi

This tool creates 2-page (front/back) printable documents that can be
added to binders for physical knowledge management.
"""

from pathlib import Path
from typing import Optional, Union, Dict, Any, List
from datetime import datetime
import re
import html

from .document_builder import DocumentBuilder
from .templates.one_pager import ONE_PAGER_TEMPLATE
from jinja2 import Template
from weasyprint import HTML


class OnePager:
    """
    Create a one-pager (2-page front/back) from any content.
    
    Features:
    - Automatic content condensation
    - Smart formatting for readability
    - Printer-friendly by default
    - Handles markdown, HTML, plain text, code, JSON, etc.
    """
    
    def __init__(
        self,
        content: Union[str, Path, Dict[str, Any], List[Any]],
        title: Optional[str] = None,
        subtitle: Optional[str] = None,
        output_path: Optional[Path] = None,
        **kwargs
    ):
        """
        Initialize one-pager creator.
        
        Args:
            content: Content to convert (string, file path, dict, list, etc.)
            title: Document title (auto-detected if not provided)
            subtitle: Document subtitle
            output_path: Output PDF path
            **kwargs: Additional DocumentBuilder options
        """
        self.raw_content = content
        self.title = title or self._detect_title(content)
        self.subtitle = subtitle
        self.output_path = output_path
        self.kwargs = kwargs
        
        # Process content into HTML
        self.html_content = self._process_content(content)
    
    def _detect_title(self, content: Union[str, Path, Dict, List]) -> str:
        """Detect title from content."""
        if isinstance(content, Path):
            return content.stem.replace('_', ' ').title()
        elif isinstance(content, dict):
            return content.get('title', content.get('name', 'One-Pager'))
        elif isinstance(content, str):
            # Try to extract from markdown or HTML
            if content.startswith('# '):
                return content.split('\n')[0].replace('# ', '').strip()
            elif '<h1>' in content:
                match = re.search(r'<h1>(.*?)</h1>', content)
                if match:
                    return match.group(1).strip()
            return "One-Pager"
        else:
            return "One-Pager"
    
    def _process_content(self, content: Union[str, Path, Dict, List]) -> str:
        """Process content into HTML format."""
        # Load from file if Path
        if isinstance(content, Path):
            text = content.read_text()
            # Detect file type
            if content.suffix == '.md':
                return self._markdown_to_html(text)
            elif content.suffix in ['.json', '.yaml', '.yml']:
                return self._structured_to_html(content.read_text(), content.suffix)
            elif content.suffix in ['.py', '.js', '.ts', '.html', '.css']:
                return self._code_to_html(text, content.suffix)
            else:
                return self._text_to_html(text)
        
        # Handle different content types
        if isinstance(content, dict):
            return self._dict_to_html(content)
        elif isinstance(content, list):
            return self._list_to_html(content)
        elif isinstance(content, str):
            # Detect format
            if content.strip().startswith('#'):
                return self._markdown_to_html(content)
            elif content.strip().startswith('<'):
                return content  # Already HTML
            elif content.strip().startswith('{') or content.strip().startswith('['):
                return self._structured_to_html(content, '.json')
            else:
                return self._text_to_html(content)
        
        return f"<p>{html.escape(str(content))}</p>"
    
    def _markdown_to_html(self, markdown: str) -> str:
        """Convert markdown to visual, story-driven HTML."""
        html_parts = []
        lines = markdown.split('\n')
        in_code_block = False
        code_lang = ''
        code_lines = []
        in_list = False
        list_type = 'ul'
        in_section = False
        section_count = 0  # Track sections for style rotation
        header_count = 0  # Track headers for style rotation
        list_count = 0  # Track lists for style rotation
        para_count = 0  # Track paragraphs for style rotation
        
        for i, line in enumerate(lines):
            # Code blocks
            if line.strip().startswith('```'):
                if in_list:
                    html_parts.append(f"</{list_type}>")
                    in_list = False
                if in_code_block:
                    # End code block - rotate styles
                    code_styles = ['', 'boxed', 'minimal']
                    style = code_styles[section_count % len(code_styles)]
                    pre_class = f' class="{style}"' if style else ''
                    code_html = f"<pre{pre_class}><code>{html.escape(''.join(code_lines).rstrip())}</code></pre>"
                    html_parts.append(code_html)
                    code_lines = []
                    in_code_block = False
                    section_count += 1
                else:
                    # Start code block
                    code_lang = line.strip()[3:].strip()
                    in_code_block = True
                continue
            
            if in_code_block:
                code_lines.append(line + '\n')
                continue
            
            # Headers - Use diverse section styles
            if line.startswith('# '):
                if in_list:
                    html_parts.append(f"</{list_type}>")
                    in_list = False
                if in_section:
                    html_parts.append("</div>")
                # Rotate through section styles
                section_styles = ['story-section primary', 'boxed-section', 'highlight-section', 'minimal-section']
                style = section_styles[section_count % len(section_styles)]
                html_parts.append(f'<div class="{style}">')
                html_parts.append(f"<h1>{self._process_inline_markdown(line[2:].strip())}</h1>")
                in_section = True
                section_count += 1
            elif line.startswith('## '):
                if in_list:
                    html_parts.append(f"</{list_type}>")
                    in_list = False
                if in_section:
                    html_parts.append("</div>")
                # Rotate through section styles
                section_styles = ['story-section secondary', 'boxed-section', 'callout-section', 'minimal-section']
                style = section_styles[section_count % len(section_styles)]
                html_parts.append(f'<div class="{style}">')
                # Rotate header styles
                header_variants = ['', 'boxed']
                variant = header_variants[header_count % len(header_variants)]
                h2_class = f' class="{variant}"' if variant else ''
                html_parts.append(f"<h2{h2_class}>{self._process_inline_markdown(line[3:].strip())}</h2>")
                in_section = True
                section_count += 1
                header_count += 1
            elif line.startswith('### '):
                if in_list:
                    html_parts.append(f"</{list_type}>")
                    in_list = False
                # Rotate h3 styles
                h3_variants = ['', 'highlight']
                variant = h3_variants[header_count % len(h3_variants)]
                h3_class = f' class="{variant}"' if variant else ''
                html_parts.append(f"<h3{h3_class}>{self._process_inline_markdown(line[4:].strip())}</h3>")
                header_count += 1
            elif line.startswith('#### '):
                if in_list:
                    html_parts.append(f"</{list_type}>")
                    in_list = False
                # Rotate h4 styles
                h4_variants = ['', 'underlined']
                variant = h4_variants[header_count % len(h4_variants)]
                h4_class = f' class="{variant}"' if variant else ''
                html_parts.append(f"<h4{h4_class}>{self._process_inline_markdown(line[5:].strip())}</h4>")
                header_count += 1
            # Lists
            elif line.strip().startswith('- ') or line.strip().startswith('* '):
                if not in_list:
                    html_parts.append("<ul>")
                    in_list = True
                    list_type = 'ul'
                content = self._process_inline_markdown(line.strip()[2:].strip())
                html_parts.append(f"<li>{content}</li>")
            elif re.match(r'^\d+\.\s', line.strip()):
                if not in_list or list_type != 'ol':
                    if in_list:
                        html_parts.append(f"</{list_type}>")
                    html_parts.append("<ol>")
                    in_list = True
                    list_type = 'ol'
                content = re.sub(r'^\d+\.\s', '', line.strip())
                content = self._process_inline_markdown(content)
                html_parts.append(f"<li>{content}</li>")
            # Horizontal rule
            elif line.strip() == '---' or line.strip() == '***':
                if in_list:
                    html_parts.append(f"</{list_type}>")
                    in_list = False
                html_parts.append("<hr>")
            # Regular paragraph - Use diverse paragraph styles
            elif line.strip():
                if in_list:
                    html_parts.append(f"</{list_type}>")
                    in_list = False
                content = self._process_inline_markdown(line.strip())
                # Rotate through paragraph styles
                para_styles = ['', 'indented', 'highlight', 'compact']
                style = para_styles[para_count % len(para_styles)]
                p_class = f' class="{style}"' if style else ''
                html_parts.append(f"<p{p_class}>{content}</p>")
                para_count += 1
        
        # Close any open structures
        if in_code_block and code_lines:
            code_styles = ['', 'boxed', 'minimal']
            style = code_styles[section_count % len(code_styles)]
            pre_class = f' class="{style}"' if style else ''
            code_html = f"<pre{pre_class}><code>{html.escape(''.join(code_lines).rstrip())}</code></pre>"
            html_parts.append(code_html)
        if in_list:
            html_parts.append(f"</{list_type}>")
        if in_section:
            html_parts.append("</div>")
        
        return '\n'.join(html_parts)
    
    def _process_inline_markdown(self, text: str) -> str:
        """Process inline markdown (bold, italic, links, code)."""
        # Escape HTML first
        text = html.escape(text)
        
        # Code (inline)
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        
        # Bold
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', text)
        
        # Italic
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
        text = re.sub(r'_([^_]+)_', r'<em>\1</em>', text)
        
        # Links
        text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
        
        return text
    
    def _text_to_html(self, text: str) -> str:
        """Convert plain text to HTML."""
        paragraphs = text.split('\n\n')
        html_parts = []
        
        for para in paragraphs:
            para = para.strip()
            if para:
                # Preserve line breaks within paragraph
                para = para.replace('\n', '<br>')
                html_parts.append(f"<p>{html.escape(para)}</p>")
        
        return '\n'.join(html_parts)
    
    def _code_to_html(self, code: str, lang: str) -> str:
        """Convert code to HTML."""
        escaped = html.escape(code)
        return f"<h3>Code ({lang})</h3><pre><code>{escaped}</code></pre>"
    
    def _structured_to_html(self, data: str, format_type: str) -> str:
        """Convert JSON/YAML to HTML."""
        try:
            import json
            if format_type == '.json':
                obj = json.loads(data)
                return self._dict_to_html(obj) if isinstance(obj, dict) else self._list_to_html(obj)
        except:
            pass
        
        # Fallback: code block
        return f"<h3>Structured Data ({format_type})</h3><pre><code>{html.escape(data)}</code></pre>"
    
    def _dict_to_html(self, data: Dict[str, Any]) -> str:
        """Convert dictionary to HTML."""
        html_parts = []
        
        for key, value in data.items():
            if isinstance(value, dict):
                html_parts.append(f"<h3>{html.escape(str(key))}</h3>")
                html_parts.append(self._dict_to_html(value))
            elif isinstance(value, list):
                html_parts.append(f"<h3>{html.escape(str(key))}</h3>")
                html_parts.append(self._list_to_html(value))
            else:
                html_parts.append(f"<p><strong>{html.escape(str(key))}:</strong> {html.escape(str(value))}</p>")
        
        return '\n'.join(html_parts)
    
    def _list_to_html(self, data: List[Any]) -> str:
        """Convert list to HTML."""
        html_parts = ["<ul>"]
        
        for item in data:
            if isinstance(item, dict):
                html_parts.append("<li>")
                html_parts.append(self._dict_to_html(item))
                html_parts.append("</li>")
            elif isinstance(item, list):
                html_parts.append("<li>")
                html_parts.append(self._list_to_html(item))
                html_parts.append("</li>")
            else:
                html_parts.append(f"<li>{html.escape(str(item))}</li>")
        
        html_parts.append("</ul>")
        return '\n'.join(html_parts)
    
    def generate(self, output_path: Optional[Path] = None, use_study_gym: bool = False) -> Path:
        """
        Generate the one-pager PDF (exactly 2 pages).
        
        Simple approach: Generate PDF directly, ensure content starts on page 1.
        
        Args:
            output_path: Output path (uses default if not provided)
            use_study_gym: Whether to use Study Gym (disabled by default for simplicity)
            
        Returns:
            Path to generated PDF
        """
        if output_path is None:
            output_path = self.output_path or Path(f"_work_efforts/one_pagers/{self.title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf")
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Simple template rendering
        template = Template(ONE_PAGER_TEMPLATE)
        html_output = template.render(
            title=self.title,
            content=self.html_content,
            subtitle=self.subtitle
        )
        
        # Generate PDF directly
        HTML(string=html_output).write_pdf(str(output_path))
        
        return output_path
    
    def _remove_blank_pages(self, pdf_path: Path) -> Path:
        """Remove blank pages from PDF, keeping only first 2 pages with content."""
        from pypdf import PdfReader, PdfWriter
        
        reader = PdfReader(str(pdf_path))
        writer = PdfWriter()
        
        pages_to_keep = []
        for page_num, page in enumerate(reader.pages):
            # Check if page has meaningful content (more than just whitespace)
            text = page.extract_text().strip()
            # Keep page if it has substantial content (more than 10 characters)
            if len(text) > 10:
                pages_to_keep.append((page_num, page))
        
        # Keep only first 2 pages with content
        for page_num, page in pages_to_keep[:2]:
            writer.add_page(page)
        
        # Write to new file
        output_path = pdf_path.parent / f"{pdf_path.stem}_cleaned.pdf"
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        return output_path
    
    def _adjust_css_for_constraints(
        self,
        html: str,
        font_scale: float,
        margin_scale: float,
        spacing_scale: float
    ) -> str:
        """Adjust CSS to meet page count constraints."""
        import re
        
        # Adjust font sizes
        def adjust_font(match):
            size_str = match.group(1)
            try:
                if 'pt' in size_str:
                    size = float(size_str.replace('pt', '').strip())
                    new_size = size * font_scale
                    return f"font-size: {new_size:.1f}pt;"
                elif 'px' in size_str:
                    size = float(size_str.replace('px', '').strip())
                    new_size = size * font_scale
                    return f"font-size: {new_size:.1f}px;"
            except:
                pass
            return match.group(0)
        
        html = re.sub(
            r'font-size:\s*([0-9.]+(?:pt|px));',
            adjust_font,
            html
        )
        
        # Adjust line-height
        def adjust_line_height(match):
            lh_str = match.group(1)
            try:
                lh = float(lh_str)
                new_lh = lh * spacing_scale
                return f"line-height: {new_lh:.2f};"
            except:
                pass
            return match.group(0)
        
        html = re.sub(
            r'line-height:\s*([0-9.]+);',
            adjust_line_height,
            html
        )
        
        # Adjust margins
        def adjust_margin_values(match):
            margin_declaration = match.group(0)
            margin_values = re.findall(r'([0-9.]+)in', margin_declaration)
            if margin_values:
                adjusted_values = [f"{float(v) * margin_scale:.3f}in" for v in margin_values]
                result = margin_declaration
                for i, (orig, adj) in enumerate(zip(margin_values, adjusted_values)):
                    result = result.replace(f"{orig}in", adj, 1)
                return result
            return margin_declaration
        
        html = re.sub(
            r'margin:\s*([0-9.\s]+in[^;]*);',
            adjust_margin_values,
            html
        )
        
        return html
    
    def _study_generation(
        self,
        html_content: str,
        initial_page_count: int,
        target_pages: int,
        output_path: Path
    ) -> Dict[str, Any]:
        """
        Study the generation using Study Gym to understand what happened.
        
        Args:
            html_content: The HTML content that was generated
            initial_page_count: Actual page count from initial generation
            target_pages: Target page count (2)
            output_path: Path where PDF was generated
            
        Returns:
            Study result with findings and recommendations
        """
        from .study_gym import StudyGym, ChallengeGenerator
        
        # Start Study Gym session
        gym = StudyGym(output_dir=Path("_work_efforts/study_gym"))
        
        # Create challenge config for this generation
        challenge_config = ChallengeGenerator.generate_challenge(
            "page_constraint",
            {
                "target_pages": target_pages,
                "content": html_content[:1000]  # Sample for challenge
            }
        )
        challenge_config["actual_content"] = html_content
        challenge_config["title"] = self.title
        
        session = gym.start_session(challenge_config)
        
        # OBSERVE: Record what happened
        word_count = len(re.sub(r'<[^>]+>', '', html_content).split())
        char_count = len(re.sub(r'<[^>]+>', '', html_content))
        
        gym.observe(
            action="initial_generation",
            result={
                "page_count": initial_page_count,
                "target_pages": target_pages,
                "difference": initial_page_count - target_pages
            },
            notes=f"Generated PDF with {initial_page_count} pages (target: {target_pages})",
            page_count=initial_page_count,
            target_pages=target_pages,
            word_count=word_count,
            content_length=len(html_content),
            char_count=char_count
        )
        
        # QUESTION: Analyze why
        page_diff = initial_page_count - target_pages
        
        # HYPOTHESIZE: Form hypothesis about what caused the page count
        if page_diff > 0:
            # Too many pages
            hypothesis = gym.form_hypothesis(
                statement=f"Content is too long, causing {page_diff} extra pages",
                reasoning=f"Word count: {word_count}, Character count: {char_count}. Content length likely exceeds what can fit in {target_pages} pages.",
                assumptions=[
                    "Font size and margins are at default values",
                    "Content density is normal",
                    "No pre-processing was applied"
                ],
                test_plan="Condense content or reduce font size/margins to fit target pages",
                confidence=0.7 if page_diff > 1 else 0.5
            )
        elif page_diff < 0:
            # Too few pages
            hypothesis = gym.form_hypothesis(
                statement=f"Content is too short, resulting in {abs(page_diff)} fewer pages",
                reasoning=f"Word count: {word_count}, Character count: {char_count}. Content length is insufficient for {target_pages} pages.",
                assumptions=[
                    "Font size and margins are at default values",
                    "Content density is normal"
                ],
                test_plan="Expand content or increase font size/margins to reach target pages",
                confidence=0.7
            )
        else:
            # Perfect!
            hypothesis = gym.form_hypothesis(
                statement="Content length is appropriate for target page count",
                reasoning=f"Word count: {word_count} resulted in exactly {target_pages} pages.",
                assumptions=[
                    "Font size and margins are at default values",
                    "Content density is normal"
                ],
                test_plan="No correction needed",
                confidence=0.9
            )
        
        # ANALYZE: Form findings
        findings = []
        if page_diff != 0:
            findings.append(f"Page count mismatch: {initial_page_count} pages vs target {target_pages} ({page_diff:+d})")
            findings.append(f"Content metrics: {word_count} words, {char_count} characters")
            
            if page_diff > 0:
                findings.append(f"Content needs reduction: approximately {int((page_diff / initial_page_count) * 100)}% reduction needed")
            else:
                findings.append(f"Content needs expansion: approximately {int((abs(page_diff) / target_pages) * 100)}% expansion needed")
        
        for finding in findings:
            gym.record_finding(finding)
        
        # CONCLUDE: Form conclusions
        conclusions = []
        if page_diff > 0:
            reduction_needed = (page_diff / initial_page_count) * 100
            conclusions.append(f"Content must be reduced by approximately {reduction_needed:.1f}% to fit {target_pages} pages")
            conclusions.append("Options: condense content, reduce font size, reduce margins, or reduce spacing")
        elif page_diff < 0:
            expansion_needed = (abs(page_diff) / target_pages) * 100
            conclusions.append(f"Content must be expanded by approximately {expansion_needed:.1f}% to reach {target_pages} pages")
            conclusions.append("Options: expand content, increase font size, increase margins, or increase spacing")
        else:
            conclusions.append(f"Content is appropriately sized for {target_pages} pages")
        
        for conclusion in conclusions:
            gym.conclude(conclusion)
        
        # End session and save
        report_path = gym.end_session()
        
        # Return study result with recommendations
        return {
            "needs_correction": page_diff != 0,
            "page_diff": page_diff,
            "word_count": word_count,
            "char_count": char_count,
            "findings": findings,
            "conclusions": conclusions,
            "recommendations": self._generate_recommendations(page_diff, word_count, initial_page_count, target_pages),
            "study_report": str(report_path),
            "session_id": session.session_id
        }
    
    def _generate_recommendations(
        self,
        page_diff: int,
        word_count: int,
        actual_pages: int,
        target_pages: int
    ) -> List[str]:
        """Generate specific recommendations based on study findings."""
        recommendations = []
        
        if page_diff > 0:
            # Too many pages - need to reduce
            reduction_pct = (page_diff / actual_pages) * 100
            
            if reduction_pct > 30:
                recommendations.append("Aggressive content condensation needed (>30% reduction)")
                recommendations.append("Consider: Remove less critical sections, truncate paragraphs, condense lists")
            elif reduction_pct > 15:
                recommendations.append("Moderate content condensation needed (15-30% reduction)")
                recommendations.append("Consider: Condense paragraphs, reduce list items, tighten spacing")
            else:
                recommendations.append("Minor adjustments needed (<15% reduction)")
                recommendations.append("Consider: Slight font reduction, margin reduction, or spacing reduction")
            
            recommendations.append(f"Target word count: approximately {int(word_count * (target_pages / actual_pages))} words")
        
        elif page_diff < 0:
            # Too few pages - need to expand
            expansion_pct = (abs(page_diff) / target_pages) * 100
            
            if expansion_pct > 30:
                recommendations.append("Significant content expansion needed (>30% expansion)")
                recommendations.append("Consider: Add summary sections, expand descriptions, add examples")
            elif expansion_pct > 15:
                recommendations.append("Moderate content expansion needed (15-30% expansion)")
                recommendations.append("Consider: Expand paragraphs, add details, increase spacing")
            else:
                recommendations.append("Minor adjustments needed (<15% expansion)")
                recommendations.append("Consider: Slight font increase, margin increase, or spacing increase")
        
        else:
            recommendations.append("No corrections needed - content is appropriately sized")
        
        return recommendations
    
    def _apply_corrections(
        self,
        html_content: str,
        study_result: Dict[str, Any],
        actual_page_count: int
    ) -> str:
        """
        Apply corrections based on study findings.
        
        Args:
            html_content: Original HTML content (not full template)
            study_result: Result from _study_generation()
            actual_page_count: Actual page count from initial generation
            
        Returns:
            Corrected HTML content (ready for template rendering)
        """
        page_diff = study_result.get("page_diff", 0)
        word_count = study_result.get("word_count", 0)
        target_pages = 2
        
        if page_diff > 0:
            # Too many pages - need to reduce
            # Calculate exact reduction needed: if 3 pages -> 2 pages, need 33% reduction
            # But be more aggressive to account for margins/spacing
            reduction_factor = target_pages / actual_page_count
            # Apply 20% extra reduction to be safe
            target_words = int(word_count * reduction_factor * 0.80)
            
            # Condense content
            corrected_content = self._condense_content(html_content, target_words=target_words)
            
            return corrected_content
        
        elif page_diff < 0:
            # Too few pages - need to expand
            # Add padding content
            padding = """
            <hr>
            <h3>Additional Information</h3>
            <p>This document has been formatted as a one-pager for easy printing and physical storage in binders.</p>
            <p><strong>Purpose:</strong> Crystallized knowledge for physical constellation in spacetime.</p>
            <p><strong>Format:</strong> 2-page front/back printable document.</p>
            <p><strong>Study Findings:</strong> Content was expanded to meet 2-page requirement based on Study Gym analysis.</p>
            """
            corrected_content = html_content + padding
            
            return corrected_content
        
        else:
            # Perfect - no corrections needed
            return html_content
    
    def _ensure_sufficient_content(self, html: str) -> str:
        """Ensure content is appropriate for 2 pages (expand if short, condense if long)."""
        # Estimate content length
        text_length = len(re.sub(r'<[^>]+>', '', html))
        word_count = len(re.sub(r'<[^>]+>', '', html).split())
        
        # If content is very short, add some padding
        if text_length < 500 or word_count < 100:
            padding = """
            <hr>
            <h3>Summary</h3>
            <p>This document has been formatted as a one-pager for easy printing and physical storage in binders.</p>
            <p><strong>Purpose:</strong> Crystallized knowledge for physical constellation in spacetime.</p>
            <p><strong>Format:</strong> 2-page front/back printable document.</p>
            """
            html = html + padding
        
        # If content is very long, condense it
        elif word_count > 2000:
            html = self._condense_content(html, target_words=1500)
        
        return html
    
    def _condense_content(self, html: str, target_words: int = 1500) -> str:
        """Intelligently condense content while preserving key information."""
        # Extract text and structure
        text = re.sub(r'<[^>]+>', ' ', html)
        words = text.split()
        
        if len(words) <= target_words:
            return html
        
        # Strategy: Keep headers, first paragraph of each section, and key lists
        lines = html.split('\n')
        condensed = []
        in_important_section = False
        words_used = 0
        
        for line in lines:
            # Always keep headers
            if re.match(r'<h[1-6]', line):
                condensed.append(line)
                in_important_section = True
                continue
            
            # Keep code blocks (they're important)
            if '<pre>' in line or '<code>' in line:
                condensed.append(line)
                words_used += len(re.sub(r'<[^>]+>', '', line).split())
                continue
            
            # Keep first paragraph after headers
            if in_important_section and '<p>' in line:
                line_words = len(re.sub(r'<[^>]+>', '', line).split())
                if words_used + line_words <= target_words:
                    condensed.append(line)
                    words_used += line_words
                    in_important_section = False
                else:
                    # Truncate paragraph
                    para_text = re.sub(r'<[^>]+>', '', line)
                    para_words = para_text.split()
                    if para_words:
                        truncated = ' '.join(para_words[:min(50, len(para_words))])
                        condensed.append(f"<p>{truncated}...</p>")
                        words_used += min(50, len(para_words))
                    in_important_section = False
                continue
            
            # Keep lists (they're usually important)
            if '<li>' in line or '<ul>' in line or '</ul>' in line:
                line_words = len(re.sub(r'<[^>]+>', '', line).split())
                if words_used + line_words <= target_words:
                    condensed.append(line)
                    words_used += line_words
                continue
            
            # Skip other content if we're over target
            if words_used >= target_words:
                continue
            
            # Add line if we have room
            line_words = len(re.sub(r'<[^>]+>', '', line).split())
            if words_used + line_words <= target_words:
                condensed.append(line)
                words_used += line_words
        
        # Add condensation notice
        condensed.append("""
        <hr>
        <p><em>Note: This document has been condensed for one-pager format. Full content available in source.</em></p>
        """)
        
        return '\n'.join(condensed)
    
    @classmethod
    def from_file(cls, file_path: Union[str, Path], **kwargs) -> "OnePager":
        """Create one-pager from file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return cls(content=path, **kwargs)
    
    @classmethod
    def from_markdown(cls, markdown: str, **kwargs) -> "OnePager":
        """Create one-pager from markdown string."""
        return cls(content=markdown, **kwargs)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> "OnePager":
        """Create one-pager from dictionary."""
        return cls(content=data, **kwargs)
    
    @classmethod
    def from_text(cls, text: str, **kwargs) -> "OnePager":
        """Create one-pager from plain text."""
        return cls(content=text, **kwargs)


def create_one_pager(
    content: Union[str, Path, Dict, List],
    title: Optional[str] = None,
    output_path: Optional[Path] = None,
    **kwargs
) -> Path:
    """
    Quick function to create a one-pager.
    
    Example:
        create_one_pager(
            "# My Document\\n\\nContent here",
            title="My One-Pager",
            output_path="output.pdf"
        )
    """
    pager = OnePager(content, title=title, output_path=output_path, **kwargs)
    return pager.generate()
