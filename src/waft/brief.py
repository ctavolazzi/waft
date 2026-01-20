"""
Brief Document Builder
======================

Creates full binder-ready brief documents with TM-ARCH-009 style cover page.
Combines briefing content (system status + chat context) with professional formatting.

Perfect for:
- Session briefs
- Project briefs
- Status reports
- Handoff documents
- Binder-ready documentation
"""

import html as html_module
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from .templates.brief import generate_brief_document
from .utils import escape_title_for_filename, escape_title_for_pdf


class BriefDocument:
    """
    Builder for full brief documents with cover page.

    Creates binder-ready documents with:
    - TM-ARCH-009 style cover page
    - Briefing content (system status + chat context)
    - Professional formatting
    - Multiple pages
    """

    def __init__(
        self,
        title: str,
        doc_id: str | None = None,
        subtitle: str | None = None,
        classification: str = "INTERNAL",
        cover_header: str | None = None,
        cover_metadata: dict[str, str] | None = None,
        cover_warning: dict[str, str] | None = None,
        cover_signature: dict[str, str] | None = None,
        cover_footer: str | None = None,
        cover_badge: str | None = None,
        include_system_status: bool = True,
        chat_context: dict[str, Any] | None = None,
    ):
        """
        Initialize brief document builder.

        Args:
            title: Document title
            doc_id: Document ID (auto-generated if not provided)
            subtitle: Optional subtitle
            classification: Security classification
            cover_header: Cover page header (e.g., "TELEPORT MASSIVE")
            cover_metadata: Dict of key-value pairs for cover
            cover_warning: Dict with 'message' and 'severity' for cover warning
            cover_signature: Dict with 'role', 'name', 'date' for cover signature
            cover_footer: Footer text for cover
            cover_badge: Optional corner badge text (e.g., "V1.0", "DRAFT")
            include_system_status: Whether to gather system status
            chat_context: Optional dict with chat context
        """
        self.title = title
        self.doc_id = doc_id or f"BRIEF-{datetime.now().strftime('%Y%m%d')}"
        self.subtitle = subtitle
        self.classification = classification
        self.cover_header = cover_header
        self.cover_metadata = cover_metadata or {}
        self.cover_warning = cover_warning
        self.cover_signature = cover_signature
        self.cover_footer = cover_footer
        self.cover_badge = cover_badge
        self.include_system_status = include_system_status
        self.chat_context = chat_context or {}

        self.content_blocks: list[str] = []

    def add_section_header(self, text: str, level: int = 2):
        """Add a section header."""
        tag = f"h{level}"
        self.content_blocks.append(f"<{tag}>{html_module.escape(text)}</{tag}>")
        return self

    def add_text(self, text: str):
        """Add plain text paragraph."""
        self.content_blocks.append(f"<p>{html_module.escape(text)}</p>")
        return self

    def add_status_box(self, title: str, content: str):
        """Add a status box."""
        html_content = f"""
        <div class="status-box">
            <div class="status-title">{html_module.escape(title)}</div>
            <p>{html_module.escape(content)}</p>
        </div>
        """
        self.content_blocks.append(html_content)
        return self

    def add_note(self, title: str, content: str):
        """Add a note box."""
        html_content = f"""
        <div class="note">
            <div class="note-title">{html_module.escape(title)}</div>
            <p>{html_module.escape(content)}</p>
        </div>
        """
        self.content_blocks.append(html_content)
        return self

    def add_table(self, headers: list[str], rows: list[list[str]]):
        """Add a table."""
        html_str = "<table><thead><tr>"
        for header in headers:
            html_str += f"<th>{html_module.escape(str(header))}</th>"
        html_str += "</tr></thead><tbody>"
        for row in rows:
            html_str += "<tr>"
            for cell in row:
                html_str += f"<td>{html_module.escape(str(cell))}</td>"
            html_str += "</tr>"
        html_str += "</tbody></table>"
        self.content_blocks.append(html_str)
        return self

    def add_markdown(self, markdown_content: str):
        """Add markdown content with proper code block support."""
        try:
            import markdown as md_lib

            html_content = md_lib.markdown(
                markdown_content,
                extensions=["fenced_code", "tables", "nl2br", "extra", "codehilite"],
                extension_configs={
                    "codehilite": {"css_class": "highlight", "use_pygments": True, "linenums": True}
                },
            )
            self.content_blocks.append(html_content)
        except ImportError:
            # Fallback: simple conversion without markdown library
            lines = markdown_content.split("\n")
            html_parts = []
            in_list = False
            in_code = False
            code_lines = []
            code_lang = ""

            for line in lines:
                # Code block start
                if line.startswith("```"):
                    if in_code:
                        # End code block
                        code_content = "\n".join(code_lines)
                        html_parts.append(
                            f'<pre><code class="language-{code_lang}">{html_module.escape(code_content)}</code></pre>'
                        )
                        code_lines = []
                        code_lang = ""
                        in_code = False
                    else:
                        # Start code block
                        code_lang = line[3:].strip() or "text"
                        in_code = True
                    continue

                if in_code:
                    code_lines.append(line)
                    continue

                # Headers
                if line.startswith("# "):
                    html_parts.append(f"<h2>{html_module.escape(line[2:].strip())}</h2>")
                elif line.startswith("## "):
                    html_parts.append(f"<h3>{html_module.escape(line[3:].strip())}</h3>")
                elif line.startswith("### "):
                    html_parts.append(f"<h4>{html_module.escape(line[4:].strip())}</h4>")
                elif line.startswith("- ") or line.startswith("* "):
                    if not in_list:
                        html_parts.append("<ul>")
                        in_list = True
                    html_parts.append(f"<li>{html_module.escape(line[2:].strip())}</li>")
                elif line.strip() == "":
                    if in_list:
                        html_parts.append("</ul>")
                        in_list = False
                else:
                    if in_list:
                        html_parts.append("</ul>")
                        in_list = False
                    # Inline code
                    line_escaped = re.sub(
                        r"`([^`]+)`", r"<code>\1</code>", html_module.escape(line)
                    )
                    html_parts.append(f"<p>{line_escaped}</p>")

            if in_list:
                html_parts.append("</ul>")
            if in_code:
                code_content = "\n".join(code_lines)
                html_parts.append(
                    f'<pre><code class="language-{code_lang}">{html_module.escape(code_content)}</code></pre>'
                )

            self.content_blocks.append("\n".join(html_parts))

        return self

    def _build_briefing_content(self) -> str:
        """Build briefing content from system status and chat context."""
        content_parts = []

        # Chat Context Section
        if self.chat_context:
            content_parts.append("<h2>Current Session Context</h2>")

            if self.chat_context.get("current_task"):
                content_parts.append(f"""
                <div class="status-box">
                    <div class="status-title">Current Task</div>
                    <p><strong>{html_module.escape(str(self.chat_context["current_task"]))}</strong></p>
                </div>
                """)

            if self.chat_context.get("recent_topics"):
                topics = self.chat_context["recent_topics"]
                if isinstance(topics, list):
                    topics_html = "<h3>Recent Topics</h3><ul>"
                    for topic in topics[:10]:
                        topics_html += f"<li>{html_module.escape(str(topic))}</li>"
                    topics_html += "</ul>"
                    content_parts.append(topics_html)

            if self.chat_context.get("key_decisions"):
                decisions = self.chat_context["key_decisions"]
                if isinstance(decisions, list):
                    decisions_html = "<h3>Key Decisions</h3><ul>"
                    for decision in decisions[:10]:
                        decisions_html += f"<li>{html_module.escape(str(decision))}</li>"
                    decisions_html += "</ul>"
                    content_parts.append(decisions_html)

            if self.chat_context.get("next_steps"):
                steps = self.chat_context["next_steps"]
                if isinstance(steps, list):
                    steps_html = "<h3>Next Steps</h3><ol>"
                    for step in steps[:10]:
                        steps_html += f"<li>{html_module.escape(str(step))}</li>"
                    steps_html += "</ol>"
                    content_parts.append(steps_html)

        # System Status Section
        if self.include_system_status:
            try:
                from scripts.waft_status import check_status, format_status_content

                project_path = Path.cwd()
                status = check_status(
                    project_path=project_path, log_event=False, save_snapshot=False
                )
                # Use professional level for brief
                status_content = format_status_content(status, level="professional")
                content_parts.append("<h2>System Status</h2>")
                content_parts.append(status_content)
            except Exception as e:
                content_parts.append(f"""
                <div class="note">
                    <div class="note-title">Status Check Unavailable</div>
                    <p>Could not gather system status: {html_module.escape(str(e))}</p>
                </div>
                """)

        return "\n".join(content_parts)

    def generate(self, output_path: Path | None = None) -> Path:
        """
        Generate the full brief PDF.

        Args:
            output_path: Output path (defaults to _work_efforts/briefs/[title]_[date].pdf)

        Returns:
            Path to generated PDF
        """
        if output_path is None:
            # Use proper filename escaping (preserves title for PDF, escapes for filename)
            safe_title = escape_title_for_filename(self.title)[:50]
            output_path = Path(
                f"_work_efforts/briefs/{safe_title}_{datetime.now().strftime('%Y%m%d')}.pdf"
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Build content
        content_html = "\n".join(self.content_blocks)

        # Add briefing content if no custom content provided
        if not self.content_blocks:
            content_html = self._build_briefing_content()
        else:
            # Add briefing content after custom content
            briefing_content = self._build_briefing_content()
            if briefing_content:
                content_html += "\n" + briefing_content

        # Escape title for PDF rendering (preserves special chars like /, -, etc.)
        title_escaped = escape_title_for_pdf(self.title)
        subtitle_escaped = escape_title_for_pdf(self.subtitle) if self.subtitle else None

        # Generate PDF
        return generate_brief_document(
            title=title_escaped,
            content=content_html,
            output_path=output_path,
            doc_id=self.doc_id,
            subtitle=subtitle_escaped,
            classification=self.classification,
            cover_header=self.cover_header,
            cover_metadata=self.cover_metadata,
            cover_warning=self.cover_warning,
            cover_signature=self.cover_signature,
            cover_footer=self.cover_footer,
            cover_badge=self.cover_badge,
        )


def create_brief(
    title: str,
    chat_context: dict[str, Any] | None = None,
    include_system_status: bool = True,
    doc_id: str | None = None,
    **kwargs,
) -> Path:
    """
    Quick function to create a brief document.

    Args:
        title: Document title
        chat_context: Optional dict with chat context
        include_system_status: Whether to gather system status
        doc_id: Document ID
        **kwargs: Additional options (subtitle, classification, cover_*, etc.)

    Returns:
        Path to generated PDF

    Example:
        create_brief(
            "Session Brief",
            chat_context={
                'current_task': 'Implementing feature X',
                'recent_topics': ['API design', 'Testing']
            },
            doc_id="BRIEF-001",
            cover_header="TELEPORT MASSIVE",
            cover_metadata={"OPERATIONAL MANUAL": "09-14", "CODENAME": "W.A.F.T."}
        )
    """
    doc = BriefDocument(
        title,
        doc_id=doc_id,
        include_system_status=include_system_status,
        chat_context=chat_context,
        **kwargs,
    )
    return doc.generate()
