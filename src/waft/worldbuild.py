"""
Worldbuilding Document Builder
==============================

Creates compelling worldbuilding documents (fantasy or factual) using
Foundation/TM formatting elements combined with field guide styling.

Supports:
- KeyValueBlock (metadata, parameters)
- WarningBlock (severity levels)
- SignatureBlock (authorization)
- SectionHeader (hierarchical)
- Summary boxes
- Tables
- Log blocks
"""

from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from datetime import datetime
import html as html_module

from .templates.worldbuild import generate_worldbuild_document, WORLDBUILD_TEMPLATE
from jinja2 import Template


class WorldbuildDocument:
    """
    Builder for worldbuilding documents with Foundation/TM elements.
    
    Perfect for:
    - Fantasy worldbuilding (lore, characters, locations)
    - Factual documentation (reports, manuals, guides)
    - SCP-style documentation
    - Corporate reports
    """
    
    def __init__(
        self,
        title: str,
        doc_id: Optional[str] = None,
        subtitle: Optional[str] = None,
        classification: str = "INTERNAL",
        issued_by: Optional[str] = None,
        date: Optional[str] = None,
        footer_notice: Optional[str] = None
    ):
        """
        Initialize worldbuilding document builder.
        
        Args:
            title: Document title
            doc_id: Document ID (auto-generated if not provided)
            subtitle: Optional subtitle
            classification: Security classification
            issued_by: Issuing organization
            date: Issue date (defaults to today)
            footer_notice: Footer notice text
        """
        self.title = title
        self.doc_id = doc_id or f"WB-{datetime.now().strftime('%Y%m%d')}"
        self.subtitle = subtitle
        self.classification = classification
        self.issued_by = issued_by
        self.date = date or datetime.now().strftime("%B %d, %Y")
        self.footer_notice = footer_notice
        
        self.blocks: List[Dict[str, Any]] = []
    
    def add_keyvalue_block(self, data: Dict[str, str], label: Optional[str] = None):
        """Add a key-value block (metadata, parameters, etc.)."""
        self.blocks.append({
            'type': 'keyvalue',
            'data': data,
            'label': label
        })
        return self
    
    def add_warning_block(self, message: str, severity: str = "WARNING"):
        """
        Add a warning block.
        
        Args:
            message: Warning message
            severity: "WARNING", "CAUTION", or "CRITICAL"
        """
        self.blocks.append({
            'type': 'warning',
            'message': message,
            'severity': severity.upper()
        })
        return self
    
    def add_signature_block(self, role: str, name: str, date: Optional[str] = None):
        """Add a signature block."""
        self.blocks.append({
            'type': 'signature',
            'role': role,
            'name': name,
            'date': date or self.date
        })
        return self
    
    def add_section_header(self, text: str, level: int = 2):
        """Add a section header."""
        self.blocks.append({
            'type': 'section',
            'text': text,
            'level': level
        })
        return self
    
    def add_summary_box(self, title: str, content: str):
        """Add a summary box."""
        self.blocks.append({
            'type': 'summary',
            'title': title,
            'content': content
        })
        return self
    
    def add_text(self, text: str):
        """Add plain text paragraph."""
        self.blocks.append({
            'type': 'text',
            'text': text
        })
        return self
    
    def add_table(self, headers: List[str], rows: List[List[str]], caption: Optional[str] = None):
        """Add a table."""
        self.blocks.append({
            'type': 'table',
            'headers': headers,
            'rows': rows,
            'caption': caption
        })
        return self
    
    def add_log_block(self, entries: List[str]):
        """Add a log block (terminal-style output)."""
        self.blocks.append({
            'type': 'log',
            'entries': entries
        })
        return self
    
    def add_markdown(self, markdown: str):
        """Add markdown content (converted to HTML)."""
        self.blocks.append({
            'type': 'markdown',
            'content': markdown
        })
        return self
    
    def _render_blocks(self) -> str:
        """Render all blocks to HTML."""
        html_parts = []
        
        for block in self.blocks:
            block_type = block['type']
            
            if block_type == 'keyvalue':
                html_parts.append(self._render_keyvalue_block(block))
            elif block_type == 'warning':
                html_parts.append(self._render_warning_block(block))
            elif block_type == 'signature':
                html_parts.append(self._render_signature_block(block))
            elif block_type == 'section':
                html_parts.append(self._render_section_header(block))
            elif block_type == 'summary':
                html_parts.append(self._render_summary_box(block))
            elif block_type == 'text':
                html_parts.append(f"<p>{html_module.escape(block['text'])}</p>")
            elif block_type == 'table':
                html_parts.append(self._render_table(block))
            elif block_type == 'log':
                html_parts.append(self._render_log_block(block))
            elif block_type == 'markdown':
                html_parts.append(self._render_markdown(block))
        
        return '\n'.join(html_parts)
    
    def _render_keyvalue_block(self, block: Dict[str, Any]) -> str:
        """Render key-value block."""
        label = block.get('label')
        data = block['data']
        
        html = '<div class="keyvalue-block">'
        if label:
            html += f'<div class="keyvalue-label">{html_module.escape(label)}</div>'
        for key, value in data.items():
            html += f'<div class="keyvalue-item">'
            html += f'<span class="keyvalue-key">{html_module.escape(str(key))}:</span> '
            html += f'<span class="keyvalue-value">{html_module.escape(str(value))}</span>'
            html += '</div>'
        html += '</div>'
        return html
    
    def _render_warning_block(self, block: Dict[str, Any]) -> str:
        """Render warning block."""
        message = block['message']
        severity = block.get('severity', 'WARNING').lower()
        
        severity_class = 'caution' if severity == 'caution' else ('critical' if severity == 'critical' else '')
        class_attr = f' class="{severity_class}"' if severity_class else ''
        
        html = f'<div class="warning-block{class_attr}">'
        html += f'<div class="warning-title">{severity.upper()}</div>'
        html += f'<p>{html_module.escape(message)}</p>'
        html += '</div>'
        return html
    
    def _render_signature_block(self, block: Dict[str, Any]) -> str:
        """Render signature block."""
        role = block['role']
        name = block['name']
        date = block.get('date', '')
        
        html = '<div class="signature-block">'
        html += '<div class="signature-line">'
        html += f'<div class="signature-role">{html_module.escape(role)}</div>'
        html += f'<div class="signature-name">{html_module.escape(name)}</div>'
        if date:
            html += f'<div class="signature-date">{html_module.escape(date)}</div>'
        html += '</div></div>'
        return html
    
    def _render_section_header(self, block: Dict[str, Any]) -> str:
        """Render section header."""
        text = block['text']
        level = block.get('level', 2)
        
        return f'<h{level}>{html_module.escape(text)}</h{level}>'
    
    def _render_summary_box(self, block: Dict[str, Any]) -> str:
        """Render summary box."""
        title = block['title']
        content = block['content']
        
        html = '<div class="summary-box">'
        html += f'<div class="summary-title">{html_module.escape(title)}</div>'
        html += f'<p>{html_module.escape(content)}</p>'
        html += '</div>'
        return html
    
    def _render_table(self, block: Dict[str, Any]) -> str:
        """Render table."""
        headers = block['headers']
        rows = block['rows']
        caption = block.get('caption')
        
        html = '<table>'
        if caption:
            html += f'<caption>{html_module.escape(caption)}</caption>'
        html += '<thead><tr>'
        for header in headers:
            html += f'<th>{html_module.escape(str(header))}</th>'
        html += '</tr></thead><tbody>'
        for row in rows:
            html += '<tr>'
            for cell in row:
                html += f'<td>{html_module.escape(str(cell))}</td>'
            html += '</tr>'
        html += '</tbody></table>'
        return html
    
    def _render_log_block(self, block: Dict[str, Any]) -> str:
        """Render log block."""
        entries = block['entries']
        
        html = '<div class="log-block">'
        for entry in entries:
            html += f'<div class="log-entry">{html_module.escape(str(entry))}</div>'
        html += '</div>'
        return html
    
    def _render_markdown(self, block: Dict[str, Any]) -> str:
        """Render markdown (simple conversion)."""
        content = block['content']
        # Simple markdown to HTML conversion
        lines = content.split('\n')
        html_parts = []
        in_list = False
        
        for line in lines:
            if line.startswith('# '):
                html_parts.append(f"<h2>{html_module.escape(line[2:].strip())}</h2>")
            elif line.startswith('## '):
                html_parts.append(f"<h3>{html_module.escape(line[3:].strip())}</h3>")
            elif line.startswith('- ') or line.startswith('* '):
                if not in_list:
                    html_parts.append('<ul>')
                    in_list = True
                html_parts.append(f"<li>{html_module.escape(line[2:].strip())}</li>")
            elif line.strip() == '':
                if in_list:
                    html_parts.append('</ul>')
                    in_list = False
                html_parts.append('<p></p>')
            else:
                if in_list:
                    html_parts.append('</ul>')
                    in_list = False
                html_parts.append(f"<p>{html_module.escape(line.strip())}</p>")
        
        if in_list:
            html_parts.append('</ul>')
        
        return '\n'.join(html_parts)
    
    def generate(self, output_path: Optional[Path] = None) -> Path:
        """
        Generate the PDF document.
        
        Args:
            output_path: Output path (defaults to _work_efforts/worldbuild/[title]_[date].pdf)
        
        Returns:
            Path to generated PDF
        """
        if output_path is None:
            safe_title = self.title.replace(' ', '_').replace('/', '_')[:50]
            output_path = Path(f"_work_efforts/worldbuild/{safe_title}_{datetime.now().strftime('%Y%m%d')}.pdf")
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Render all blocks to HTML
        content_html = self._render_blocks()
        
        # Generate PDF
        return generate_worldbuild_document(
            title=self.title,
            content=content_html,
            output_path=output_path,
            doc_id=self.doc_id,
            subtitle=self.subtitle,
            classification=self.classification,
            issued_by=self.issued_by,
            date=self.date,
            footer_notice=self.footer_notice
        )


def create_worldbuild_document(
    title: str,
    content: Union[str, Dict[str, Any], List[Dict[str, Any]]],
    doc_id: Optional[str] = None,
    **kwargs
) -> Path:
    """
    Quick function to create a worldbuilding document.
    
    Args:
        title: Document title
        content: Content (string, dict with blocks, or list of block dicts)
        doc_id: Document ID
        **kwargs: Additional options (subtitle, classification, etc.)
    
    Returns:
        Path to generated PDF
    
    Example:
        # From markdown string
        create_worldbuild_document(
            "Character Profile",
            "# Character Name\\n\\nDescription here",
            doc_id="CHAR-001"
        )
        
        # From structured blocks
        create_worldbuild_document(
            "Location Guide",
            {
                'keyvalue': {'Population': '10,000', 'Region': 'North'},
                'text': 'Description text',
                'sections': [{'level': 2, 'text': 'History'}]
            }
        )
    """
    doc = WorldbuildDocument(title, doc_id=doc_id, **kwargs)
    
    if isinstance(content, str):
        # Markdown string
        doc.add_markdown(content)
    elif isinstance(content, dict):
        # Structured content
        if 'keyvalue' in content:
            doc.add_keyvalue_block(content['keyvalue'], content.get('keyvalue_label'))
        if 'text' in content:
            doc.add_text(content['text'])
        if 'sections' in content:
            for section in content['sections']:
                doc.add_section_header(section['text'], section.get('level', 2))
    elif isinstance(content, list):
        # List of blocks
        for block in content:
            block_type = block.get('type')
            if block_type == 'keyvalue':
                doc.add_keyvalue_block(block['data'], block.get('label'))
            elif block_type == 'warning':
                doc.add_warning_block(block['message'], block.get('severity', 'WARNING'))
            elif block_type == 'signature':
                doc.add_signature_block(block['role'], block['name'], block.get('date'))
            elif block_type == 'section':
                doc.add_section_header(block['text'], block.get('level', 2))
            elif block_type == 'text':
                doc.add_text(block['text'])
            elif block_type == 'table':
                doc.add_table(block['headers'], block['rows'], block.get('caption'))
            elif block_type == 'log':
                doc.add_log_block(block['entries'])
            elif block_type == 'summary':
                doc.add_summary_box(block['title'], block['content'])
    
    return doc.generate()
