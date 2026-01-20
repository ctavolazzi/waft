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

import html
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from jinja2 import Template
from weasyprint import HTML

from .evolution.document_components import (
    ComponentBuilder,
    ComponentType,
    DocumentComponent,
)
from .templates.briefing import BRIEFING_TEMPLATE
from .templates.one_pager import ONE_PAGER_TEMPLATE


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
        content: str | Path | dict[str, Any] | list[Any],
        title: str | None = None,
        subtitle: str | None = None,
        output_path: Path | None = None,
        **kwargs,
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

    def _detect_title(self, content: str | Path | dict | list) -> str:
        """Detect title from content."""
        if isinstance(content, Path):
            return content.stem.replace("_", " ").title()
        elif isinstance(content, dict):
            return content.get("title", content.get("name", "One-Pager"))
        elif isinstance(content, str):
            # Try to extract from markdown or HTML
            if content.startswith("# "):
                return content.split("\n")[0].replace("# ", "").strip()
            elif "<h1>" in content:
                match = re.search(r"<h1>(.*?)</h1>", content)
                if match:
                    return match.group(1).strip()
            return "One-Pager"
        else:
            return "One-Pager"

    def _process_content(self, content: str | Path | dict | list) -> str:
        """Process content into HTML format."""
        # Load from file if Path
        if isinstance(content, Path):
            text = content.read_text()
            # Detect file type
            if content.suffix == ".md":
                return self._markdown_to_html(text)
            elif content.suffix in [".json", ".yaml", ".yml"]:
                return self._structured_to_html(content.read_text(), content.suffix)
            elif content.suffix in [".py", ".js", ".ts", ".html", ".css"]:
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
            if content.strip().startswith("#"):
                return self._markdown_to_html(content)
            elif content.strip().startswith("<"):
                return content  # Already HTML
            elif content.strip().startswith("{") or content.strip().startswith("["):
                return self._structured_to_html(content, ".json")
            else:
                return self._text_to_html(content)

        return f"<p>{html.escape(str(content))}</p>"

    def _markdown_to_html(self, markdown: str) -> str:
        """Convert markdown to visual, story-driven HTML."""
        # #region agent log
        with open("/Users/ctavolazzi/Code/active/waft/.cursor/debug.log", "a") as f:
            import json

            f.write(
                json.dumps(
                    {
                        "sessionId": "debug-session",
                        "runId": "run1",
                        "hypothesisId": "B",
                        "location": "one_pager.py:121",
                        "message": "_markdown_to_html entry",
                        "data": {
                            "markdown_length": len(markdown) if markdown else 0,
                            "markdown_preview": markdown[:150] if markdown else "",
                            "has_bold": bool(re.search(r"\*\*|__", markdown))
                            if markdown
                            else False,
                            "has_lists": bool(re.search(r"^[-*]\s", markdown, re.MULTILINE))
                            if markdown
                            else False,
                        },
                        "timestamp": int(__import__("time").time() * 1000),
                    }
                )
                + "\n"
            )
        # #endregion

        html_parts = []
        lines = markdown.split("\n")
        in_code_block = False
        code_lines = []
        in_list = False
        list_type = "ul"
        in_section = False
        section_count = 0  # Track sections for style rotation
        header_count = 0  # Track headers for style rotation
        para_count = 0  # Track paragraphs for style rotation

        for _i, line in enumerate(lines):
            # Code blocks
            if line.strip().startswith("```"):
                if in_list:
                    html_parts.append(f"</{list_type}>")
                    in_list = False
                if in_code_block:
                    # End code block - rotate styles
                    code_styles = ["", "boxed", "minimal"]
                    style = code_styles[section_count % len(code_styles)]
                    pre_class = f' class="{style}"' if style else ""
                    code_html = f"<pre{pre_class}><code>{html.escape(''.join(code_lines).rstrip())}</code></pre>"
                    html_parts.append(code_html)
                    code_lines = []
                    in_code_block = False
                    section_count += 1
                else:
                    # Start code block
                    line.strip()[3:].strip()
                    in_code_block = True
                continue

            if in_code_block:
                code_lines.append(line + "\n")
                continue

            # Headers - Use diverse section styles
            if line.startswith("# "):
                if in_list:
                    html_parts.append(f"</{list_type}>")
                    in_list = False
                if in_section:
                    html_parts.append("</div>")
                # Rotate through section styles
                section_styles = [
                    "story-section primary",
                    "boxed-section",
                    "highlight-section",
                    "minimal-section",
                ]
                style = section_styles[section_count % len(section_styles)]
                html_parts.append(f'<div class="{style}">')
                html_parts.append(f"<h1>{self._process_inline_markdown(line[2:].strip())}</h1>")
                in_section = True
                section_count += 1
            elif line.startswith("## "):
                if in_list:
                    html_parts.append(f"</{list_type}>")
                    in_list = False
                if in_section:
                    html_parts.append("</div>")
                # Rotate through section styles
                section_styles = [
                    "story-section secondary",
                    "boxed-section",
                    "callout-section",
                    "minimal-section",
                ]
                style = section_styles[section_count % len(section_styles)]
                html_parts.append(f'<div class="{style}">')
                # Rotate header styles
                header_variants = ["", "boxed"]
                variant = header_variants[header_count % len(header_variants)]
                h2_class = f' class="{variant}"' if variant else ""
                html_parts.append(
                    f"<h2{h2_class}>{self._process_inline_markdown(line[3:].strip())}</h2>"
                )
                in_section = True
                section_count += 1
                header_count += 1
            elif line.startswith("### "):
                if in_list:
                    html_parts.append(f"</{list_type}>")
                    in_list = False
                # Rotate h3 styles
                h3_variants = ["", "highlight"]
                variant = h3_variants[header_count % len(h3_variants)]
                h3_class = f' class="{variant}"' if variant else ""
                html_parts.append(
                    f"<h3{h3_class}>{self._process_inline_markdown(line[4:].strip())}</h3>"
                )
                header_count += 1
            elif line.startswith("#### "):
                if in_list:
                    html_parts.append(f"</{list_type}>")
                    in_list = False
                # Rotate h4 styles
                h4_variants = ["", "underlined"]
                variant = h4_variants[header_count % len(h4_variants)]
                h4_class = f' class="{variant}"' if variant else ""
                html_parts.append(
                    f"<h4{h4_class}>{self._process_inline_markdown(line[5:].strip())}</h4>"
                )
                header_count += 1
            # Lists
            elif line.strip().startswith("- ") or line.strip().startswith("* "):
                if not in_list:
                    html_parts.append("<ul>")
                    in_list = True
                    list_type = "ul"
                content = self._process_inline_markdown(line.strip()[2:].strip())
                html_parts.append(f"<li>{content}</li>")
            elif re.match(r"^\d+\.\s", line.strip()):
                if not in_list or list_type != "ol":
                    if in_list:
                        html_parts.append(f"</{list_type}>")
                    html_parts.append("<ol>")
                    in_list = True
                    list_type = "ol"
                content = re.sub(r"^\d+\.\s", "", line.strip())
                content = self._process_inline_markdown(content)
                html_parts.append(f"<li>{content}</li>")
            # Horizontal rule
            elif line.strip() == "---" or line.strip() == "***":
                if in_list:
                    html_parts.append(f"</{list_type}>")
                    in_list = False
                html_parts.append("<hr>")
            # Regular paragraph - Use consistent styling (no rotation for cleaner look)
            elif line.strip():
                if in_list:
                    html_parts.append(f"</{list_type}>")
                    in_list = False
                content = self._process_inline_markdown(line.strip())
                # Use consistent paragraph styling (no rotation)
                html_parts.append(f"<p>{content}</p>")
                para_count += 1

        # Close any open structures
        if in_code_block and code_lines:
            code_styles = ["", "boxed", "minimal"]
            style = code_styles[section_count % len(code_styles)]
            pre_class = f' class="{style}"' if style else ""
            code_html = (
                f"<pre{pre_class}><code>{html.escape(''.join(code_lines).rstrip())}</code></pre>"
            )
            html_parts.append(code_html)
        if in_list:
            html_parts.append(f"</{list_type}>")
        if in_section:
            html_parts.append("</div>")

        result = "\n".join(html_parts)

        # #region agent log
        with open("/Users/ctavolazzi/Code/active/waft/.cursor/debug.log", "a") as f:
            import json

            f.write(
                json.dumps(
                    {
                        "sessionId": "debug-session",
                        "runId": "run1",
                        "hypothesisId": "B",
                        "location": "one_pager.py:263",
                        "message": "_markdown_to_html exit",
                        "data": {
                            "result_length": len(result) if result else 0,
                            "result_preview": result[:200] if result else "",
                            "has_html_tags": bool(re.search(r"<[^>]+>", result))
                            if result
                            else False,
                            "has_strong_tags": bool(re.search(r"<strong>", result))
                            if result
                            else False,
                            "has_list_tags": bool(re.search(r"<[uo]l>", result))
                            if result
                            else False,
                        },
                        "timestamp": int(__import__("time").time() * 1000),
                    }
                )
                + "\n"
            )
        # #endregion

        return result

    def _process_inline_markdown(self, text: str) -> str:
        """Process inline markdown (bold, italic, links, code)."""
        # #region agent log
        with open("/Users/ctavolazzi/Code/active/waft/.cursor/debug.log", "a") as f:
            import json

            f.write(
                json.dumps(
                    {
                        "sessionId": "debug-session",
                        "runId": "post-fix",
                        "hypothesisId": "C",
                        "location": "one_pager.py:265",
                        "message": "_process_inline_markdown entry",
                        "data": {
                            "text_length": len(text) if text else 0,
                            "text_preview": text[:100] if text else "",
                            "has_bold_markers": bool(re.search(r"\*\*|__", text))
                            if text
                            else False,
                            "has_underscores": bool("_" in text) if text else False,
                        },
                        "timestamp": int(__import__("time").time() * 1000),
                    }
                )
                + "\n"
            )
        # #endregion

        # Process markdown BEFORE escaping to preserve structure
        # Then escape the content parts

        # Code (inline) - process first, escape content
        def escape_code(match):
            return f"<code>{html.escape(match.group(1))}</code>"

        text = re.sub(r"`([^`]+)`", escape_code, text)

        # Bold - process, escape content
        def escape_bold(match):
            return f"<strong>{html.escape(match.group(1))}</strong>"

        text = re.sub(r"\*\*([^*]+)\*\*", escape_bold, text)
        text = re.sub(r"__([^_]+)__", escape_bold, text)

        # Italic - process, escape content (but avoid conflicts with bold and code/filenames)
        def escape_italic(match):
            return f"<em>{html.escape(match.group(1))}</em>"

        # Only match single * that aren't part of **
        # For _, be more careful - don't match if surrounded by alphanumeric (likely code/filename)
        text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", escape_italic, text)
        # Only match _italic_ when NOT in code-like context (not surrounded by alphanumeric)
        text = re.sub(r"(?<![a-zA-Z0-9])_([^_]+)_(?![a-zA-Z0-9])", escape_italic, text)

        # Links - process, escape both text and URL
        def escape_link(match):
            return f'<a href="{html.escape(match.group(2))}">{html.escape(match.group(1))}</a>'

        text = re.sub(r"\[([^\]]+)\]\(([^\)]+)\)", escape_link, text)

        # Escape any remaining HTML that wasn't part of markdown
        # Split by HTML tags, escape non-tag parts
        parts = re.split(r"(<[^>]+>)", text)
        result = []
        for part in parts:
            if part.startswith("<") and part.endswith(">"):
                result.append(part)  # Already HTML tag
            else:
                result.append(html.escape(part))  # Escape plain text
        final_result = "".join(result)

        # #region agent log
        with open("/Users/ctavolazzi/Code/active/waft/.cursor/debug.log", "a") as f:
            import json

            f.write(
                json.dumps(
                    {
                        "sessionId": "debug-session",
                        "runId": "post-fix",
                        "hypothesisId": "C",
                        "location": "one_pager.py:304",
                        "message": "_process_inline_markdown exit",
                        "data": {
                            "result_length": len(final_result) if final_result else 0,
                            "result_preview": final_result[:150] if final_result else "",
                            "has_strong_tags": bool(re.search(r"<strong>", final_result))
                            if final_result
                            else False,
                            "has_incorrect_em_tags": bool(
                                re.search(
                                    r"<em>latex</em>|<em>self</em>|<em>batch</em>", final_result
                                )
                            )
                            if final_result
                            else False,
                            "preserves_underscores": bool(
                                "test_latex" in final_result or "test_self" in final_result
                            )
                            if final_result
                            else False,
                        },
                        "timestamp": int(__import__("time").time() * 1000),
                    }
                )
                + "\n"
            )
        # #endregion

        return final_result

    def _text_to_html(self, text: str) -> str:
        """Convert plain text to HTML."""
        paragraphs = text.split("\n\n")
        html_parts = []

        for para in paragraphs:
            para = para.strip()
            if para:
                # Preserve line breaks within paragraph
                para = para.replace("\n", "<br>")
                html_parts.append(f"<p>{html.escape(para)}</p>")

        return "\n".join(html_parts)

    def _code_to_html(self, code: str, lang: str) -> str:
        """Convert code to HTML."""
        escaped = html.escape(code)
        return f"<h3>Code ({lang})</h3><pre><code>{escaped}</code></pre>"

    def _structured_to_html(self, data: str, format_type: str) -> str:
        """Convert JSON/YAML to HTML."""
        try:
            import json

            if format_type == ".json":
                obj = json.loads(data)
                return self._dict_to_html(obj) if isinstance(obj, dict) else self._list_to_html(obj)
        except:
            pass

        # Fallback: code block
        return (
            f"<h3>Structured Data ({format_type})</h3><pre><code>{html.escape(data)}</code></pre>"
        )

    def _dict_to_html(self, data: dict[str, Any]) -> str:
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
                html_parts.append(
                    f"<p><strong>{html.escape(str(key))}:</strong> {html.escape(str(value))}</p>"
                )

        return "\n".join(html_parts)

    def _list_to_html(self, data: list[Any]) -> str:
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
        return "\n".join(html_parts)

    def generate(
        self,
        output_path: Path | None = None,
        use_study_gym: bool = False,
        save_html_preview: bool = False,
        open_in_browser: bool = False,
    ) -> Path:
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
            output_path = self.output_path or Path(
                f"_work_efforts/one_pagers/{self.title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Use briefing template if flagged
        if hasattr(self, "use_briefing_template") and self.use_briefing_template:
            template = Template(BRIEFING_TEMPLATE)
            context = {
                "title": self.title,
                "subtitle": self.subtitle,
                "content": self.html_content,
                "series": getattr(self, "briefing_series", "BRIEFING"),
                "number": getattr(self, "briefing_number", "BG-001"),
                "classification": getattr(self, "briefing_classification", "INTERNAL"),
                "issued_by": getattr(self, "briefing_issued_by", "WAFT System"),
                "date": getattr(self, "briefing_date", datetime.now().strftime("%B %d, %Y")),
            }
        else:
            # Standard one-pager template
            template = Template(ONE_PAGER_TEMPLATE)
            context = {
                "title": self.title,
                "subtitle": self.subtitle,
                "content": self.html_content,
            }

        # Add components if using from_components/from_sections
        if hasattr(self, "components"):
            # Use DocumentComponent.to_html() for ALL component types
            # This leverages WAFT's full document component system
            styling_dict = {
                "font": {"size_body": 10, "size_title": 18},
                "margin": {"top": 0.5, "bottom": 0.5},
                "color": {"text": "#000", "background": "#fff"},
            }

            # Render all components using their to_html() methods
            component_htmls = []
            sections = []  # Keep for backward compatibility with template

            for comp in self.components:
                if comp.component_type == ComponentType.SECTION:
                    # Process section components with markdown support
                    title = (
                        comp.content.get("title", "")
                        if isinstance(comp.content, dict)
                        else str(comp.content)
                    )
                    body = comp.content.get("body", "") if isinstance(comp.content, dict) else ""

                    # #region agent log
                    with open("/Users/ctavolazzi/Code/active/waft/.cursor/debug.log", "a") as f:
                        import json

                        f.write(
                            json.dumps(
                                {
                                    "sessionId": "debug-session",
                                    "runId": "overview-debug",
                                    "hypothesisId": "A",
                                    "location": "one_pager.py:447",
                                    "message": "Section processing",
                                    "data": {
                                        "title": title,
                                        "body_length": len(body) if body else 0,
                                        "body_preview": body[:200] if body else "",
                                        "body_starts_with_dash": body.strip().startswith("-")
                                        if body
                                        else False,
                                    },
                                    "timestamp": int(__import__("time").time() * 1000),
                                }
                            )
                            + "\n"
                        )
                    # #endregion

                    # Process body content - convert markdown to HTML
                    # If body already contains HTML tags, skip markdown processing
                    if body:
                        if body.strip().startswith("<") and (
                            "<dl>" in body or "<ul>" in body or "<ol>" in body or "<table>" in body
                        ):
                            # Already HTML, use as-is (but still process inline markdown in it)
                            body_html = body
                        else:
                            body_html = self._markdown_to_html(body)

                        # #region agent log
                        with open("/Users/ctavolazzi/Code/active/waft/.cursor/debug.log", "a") as f:
                            import json

                            f.write(
                                json.dumps(
                                    {
                                        "sessionId": "debug-session",
                                        "runId": "overview-debug",
                                        "hypothesisId": "B",
                                        "location": "one_pager.py:456",
                                        "message": "Markdown processing result",
                                        "data": {
                                            "body_html_length": len(body_html) if body_html else 0,
                                            "body_html_preview": body_html[:300]
                                            if body_html
                                            else "",
                                            "has_ul_tags": bool(re.search(r"<ul>", body_html))
                                            if body_html
                                            else False,
                                            "has_p_tags": bool(re.search(r"<p[^>]*>", body_html))
                                            if body_html
                                            else False,
                                        },
                                        "timestamp": int(__import__("time").time() * 1000),
                                    }
                                )
                                + "\n"
                            )
                        # #endregion
                    else:
                        body_html = ""

                    section_dict = {
                        "title": title,
                        "content": body_html,
                        "level": comp.metadata.get("level", 2),
                    }
                    sections.append(section_dict)

                    # Also add to component_htmls for full component rendering with proper section styling
                    level = comp.metadata.get("level", 2)
                    section_html = f'<section class="section"><h{level}>{html.escape(title)}</h{level}><div class="section-content">{body_html}</div></section>'
                    component_htmls.append(section_html)
                else:
                    # Use component's to_html() method for all other types
                    html_output = comp.to_html(styling_dict)
                    if html_output:
                        # For components with markdown content, process it
                        if comp.component_type == ComponentType.ABSTRACT:
                            # Abstract content is in <p> tag, need to process markdown in the paragraph
                            content = str(comp.content)
                            if re.search(r"\*\*|__|- |`", content):
                                processed = self._markdown_to_html(content)
                                # Replace the escaped content in the <p> tag
                                html_output = html_output.replace(
                                    f"<p>{html.escape(content)}</p>", f"<p>{processed}</p>"
                                )
                        elif comp.component_type == ComponentType.PARAGRAPH:
                            content = str(comp.content)
                            if re.search(r"\*\*|__|- |`", content):
                                processed = self._markdown_to_html(content)
                                html_output = html_output.replace(
                                    f"<p>{html.escape(content)}</p>", f"<p>{processed}</p>"
                                )
                        component_htmls.append(html_output)

            # Pass both sections (for template compatibility) and component_htmls (for full rendering)
            context["sections"] = sections
            context["component_htmls"] = component_htmls
            context["content"] = None

        # Add any additional variables
        if hasattr(self, "variables"):
            context.update(self.variables)

        # #region agent log
        with open("/Users/ctavolazzi/Code/active/waft/.cursor/debug.log", "a") as f:
            import json

            f.write(
                json.dumps(
                    {
                        "sessionId": "debug-session",
                        "runId": "run1",
                        "hypothesisId": "D",
                        "location": "one_pager.py:430",
                        "message": "Template context before render",
                        "data": {
                            "has_sections": "sections" in context
                            and context["sections"] is not None,
                            "sections_count": len(context.get("sections", []))
                            if context.get("sections")
                            else 0,
                            "has_content": bool(context.get("content")),
                        },
                        "timestamp": int(__import__("time").time() * 1000),
                    }
                )
                + "\n"
            )
        # #endregion

        html_output = template.render(**context)

        # #region agent log
        with open("/Users/ctavolazzi/Code/active/waft/.cursor/debug.log", "a") as f:
            import json

            f.write(
                json.dumps(
                    {
                        "sessionId": "debug-session",
                        "runId": "run1",
                        "hypothesisId": "D",
                        "location": "one_pager.py:440",
                        "message": "HTML output after render",
                        "data": {
                            "html_length": len(html_output) if html_output else 0,
                            "html_preview": html_output[:300] if html_output else "",
                            "has_section_tags": bool(re.search(r"<section", html_output))
                            if html_output
                            else False,
                        },
                        "timestamp": int(__import__("time").time() * 1000),
                    }
                )
                + "\n"
            )
        # #endregion

        # Save HTML preview if requested
        if save_html_preview or open_in_browser:
            html_path = output_path.with_suffix(".html")
            html_path.write_text(html_output)
            if open_in_browser:
                import webbrowser

                html_path_abs = html_path.absolute()
                webbrowser.open(f"file://{html_path_abs}")

        # Generate PDF directly
        HTML(string=html_output).write_pdf(str(output_path))

        # Convert PDF to image for screenshot if requested
        if open_in_browser:
            try:
                from .evolution.pdf_image_converter import pdf_to_pngs

                # Convert first page to PNG (save directly to same directory as PDF)
                img_path = output_path.with_suffix(".png")
                png_paths = pdf_to_pngs(
                    output_path, output_dir=output_path.parent, dpi=150, format="png"
                )
                if png_paths:
                    # Copy first page to main PNG file for easy access
                    import shutil

                    shutil.copy(png_paths[0], img_path)
                    print(f"📸 Screenshot saved: {img_path}")
            except Exception:
                # Fallback: try direct conversion
                try:
                    import fitz  # PyMuPDF

                    doc = fitz.open(str(output_path))
                    if len(doc) > 0:
                        page = doc[0]
                        pix = page.get_pixmap(
                            matrix=fitz.Matrix(2, 2)
                        )  # 2x zoom for better quality
                        img_path = output_path.with_suffix(".png")
                        pix.save(str(img_path))
                        doc.close()
                        print(f"📸 Screenshot saved: {img_path}")
                except Exception:
                    pass  # No PDF to image converter available

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
        with open(output_path, "wb") as f:
            writer.write(f)

        return output_path

    def _adjust_css_for_constraints(
        self, html: str, font_scale: float, margin_scale: float, spacing_scale: float
    ) -> str:
        """Adjust CSS to meet page count constraints."""
        import re

        # Adjust font sizes
        def adjust_font(match):
            size_str = match.group(1)
            try:
                if "pt" in size_str:
                    size = float(size_str.replace("pt", "").strip())
                    new_size = size * font_scale
                    return f"font-size: {new_size:.1f}pt;"
                elif "px" in size_str:
                    size = float(size_str.replace("px", "").strip())
                    new_size = size * font_scale
                    return f"font-size: {new_size:.1f}px;"
            except:
                pass
            return match.group(0)

        html = re.sub(r"font-size:\s*([0-9.]+(?:pt|px));", adjust_font, html)

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

        html = re.sub(r"line-height:\s*([0-9.]+);", adjust_line_height, html)

        # Adjust margins
        def adjust_margin_values(match):
            margin_declaration = match.group(0)
            margin_values = re.findall(r"([0-9.]+)in", margin_declaration)
            if margin_values:
                adjusted_values = [f"{float(v) * margin_scale:.3f}in" for v in margin_values]
                result = margin_declaration
                for _i, (orig, adj) in enumerate(zip(margin_values, adjusted_values, strict=False)):
                    result = result.replace(f"{orig}in", adj, 1)
                return result
            return margin_declaration

        html = re.sub(r"margin:\s*([0-9.\s]+in[^;]*);", adjust_margin_values, html)

        return html

    def _study_generation(
        self, html_content: str, initial_page_count: int, target_pages: int, output_path: Path
    ) -> dict[str, Any]:
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
        from .study_gym import ChallengeGenerator, StudyGym

        # Start Study Gym session
        gym = StudyGym(output_dir=Path("_work_efforts/study_gym"))

        # Create challenge config for this generation
        challenge_config = ChallengeGenerator.generate_challenge(
            "page_constraint",
            {
                "target_pages": target_pages,
                "content": html_content[:1000],  # Sample for challenge
            },
        )
        challenge_config["actual_content"] = html_content
        challenge_config["title"] = self.title

        session = gym.start_session(challenge_config)

        # OBSERVE: Record what happened
        word_count = len(re.sub(r"<[^>]+>", "", html_content).split())
        char_count = len(re.sub(r"<[^>]+>", "", html_content))

        gym.observe(
            action="initial_generation",
            result={
                "page_count": initial_page_count,
                "target_pages": target_pages,
                "difference": initial_page_count - target_pages,
            },
            notes=f"Generated PDF with {initial_page_count} pages (target: {target_pages})",
            page_count=initial_page_count,
            target_pages=target_pages,
            word_count=word_count,
            content_length=len(html_content),
            char_count=char_count,
        )

        # QUESTION: Analyze why
        page_diff = initial_page_count - target_pages

        # HYPOTHESIZE: Form hypothesis about what caused the page count
        if page_diff > 0:
            # Too many pages
            gym.form_hypothesis(
                statement=f"Content is too long, causing {page_diff} extra pages",
                reasoning=f"Word count: {word_count}, Character count: {char_count}. Content length likely exceeds what can fit in {target_pages} pages.",
                assumptions=[
                    "Font size and margins are at default values",
                    "Content density is normal",
                    "No pre-processing was applied",
                ],
                test_plan="Condense content or reduce font size/margins to fit target pages",
                confidence=0.7 if page_diff > 1 else 0.5,
            )
        elif page_diff < 0:
            # Too few pages
            gym.form_hypothesis(
                statement=f"Content is too short, resulting in {abs(page_diff)} fewer pages",
                reasoning=f"Word count: {word_count}, Character count: {char_count}. Content length is insufficient for {target_pages} pages.",
                assumptions=[
                    "Font size and margins are at default values",
                    "Content density is normal",
                ],
                test_plan="Expand content or increase font size/margins to reach target pages",
                confidence=0.7,
            )
        else:
            # Perfect!
            gym.form_hypothesis(
                statement="Content length is appropriate for target page count",
                reasoning=f"Word count: {word_count} resulted in exactly {target_pages} pages.",
                assumptions=[
                    "Font size and margins are at default values",
                    "Content density is normal",
                ],
                test_plan="No correction needed",
                confidence=0.9,
            )

        # ANALYZE: Form findings
        findings = []
        if page_diff != 0:
            findings.append(
                f"Page count mismatch: {initial_page_count} pages vs target {target_pages} ({page_diff:+d})"
            )
            findings.append(f"Content metrics: {word_count} words, {char_count} characters")

            if page_diff > 0:
                findings.append(
                    f"Content needs reduction: approximately {int((page_diff / initial_page_count) * 100)}% reduction needed"
                )
            else:
                findings.append(
                    f"Content needs expansion: approximately {int((abs(page_diff) / target_pages) * 100)}% expansion needed"
                )

        for finding in findings:
            gym.record_finding(finding)

        # CONCLUDE: Form conclusions
        conclusions = []
        if page_diff > 0:
            reduction_needed = (page_diff / initial_page_count) * 100
            conclusions.append(
                f"Content must be reduced by approximately {reduction_needed:.1f}% to fit {target_pages} pages"
            )
            conclusions.append(
                "Options: condense content, reduce font size, reduce margins, or reduce spacing"
            )
        elif page_diff < 0:
            expansion_needed = (abs(page_diff) / target_pages) * 100
            conclusions.append(
                f"Content must be expanded by approximately {expansion_needed:.1f}% to reach {target_pages} pages"
            )
            conclusions.append(
                "Options: expand content, increase font size, increase margins, or increase spacing"
            )
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
            "recommendations": self._generate_recommendations(
                page_diff, word_count, initial_page_count, target_pages
            ),
            "study_report": str(report_path),
            "session_id": session.session_id,
        }

    def _generate_recommendations(
        self, page_diff: int, word_count: int, actual_pages: int, target_pages: int
    ) -> list[str]:
        """Generate specific recommendations based on study findings."""
        recommendations = []

        if page_diff > 0:
            # Too many pages - need to reduce
            reduction_pct = (page_diff / actual_pages) * 100

            if reduction_pct > 30:
                recommendations.append("Aggressive content condensation needed (>30% reduction)")
                recommendations.append(
                    "Consider: Remove less critical sections, truncate paragraphs, condense lists"
                )
            elif reduction_pct > 15:
                recommendations.append("Moderate content condensation needed (15-30% reduction)")
                recommendations.append(
                    "Consider: Condense paragraphs, reduce list items, tighten spacing"
                )
            else:
                recommendations.append("Minor adjustments needed (<15% reduction)")
                recommendations.append(
                    "Consider: Slight font reduction, margin reduction, or spacing reduction"
                )

            recommendations.append(
                f"Target word count: approximately {int(word_count * (target_pages / actual_pages))} words"
            )

        elif page_diff < 0:
            # Too few pages - need to expand
            expansion_pct = (abs(page_diff) / target_pages) * 100

            if expansion_pct > 30:
                recommendations.append("Significant content expansion needed (>30% expansion)")
                recommendations.append(
                    "Consider: Add summary sections, expand descriptions, add examples"
                )
            elif expansion_pct > 15:
                recommendations.append("Moderate content expansion needed (15-30% expansion)")
                recommendations.append("Consider: Expand paragraphs, add details, increase spacing")
            else:
                recommendations.append("Minor adjustments needed (<15% expansion)")
                recommendations.append(
                    "Consider: Slight font increase, margin increase, or spacing increase"
                )

        else:
            recommendations.append("No corrections needed - content is appropriately sized")

        return recommendations

    def _apply_corrections(
        self, html_content: str, study_result: dict[str, Any], actual_page_count: int
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
        text_length = len(re.sub(r"<[^>]+>", "", html))
        word_count = len(re.sub(r"<[^>]+>", "", html).split())

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
        text = re.sub(r"<[^>]+>", " ", html)
        words = text.split()

        if len(words) <= target_words:
            return html

        # Strategy: Keep headers, first paragraph of each section, and key lists
        lines = html.split("\n")
        condensed = []
        in_important_section = False
        words_used = 0

        for line in lines:
            # Always keep headers
            if re.match(r"<h[1-6]", line):
                condensed.append(line)
                in_important_section = True
                continue

            # Keep code blocks (they're important)
            if "<pre>" in line or "<code>" in line:
                condensed.append(line)
                words_used += len(re.sub(r"<[^>]+>", "", line).split())
                continue

            # Keep first paragraph after headers
            if in_important_section and "<p>" in line:
                line_words = len(re.sub(r"<[^>]+>", "", line).split())
                if words_used + line_words <= target_words:
                    condensed.append(line)
                    words_used += line_words
                    in_important_section = False
                else:
                    # Truncate paragraph
                    para_text = re.sub(r"<[^>]+>", "", line)
                    para_words = para_text.split()
                    if para_words:
                        truncated = " ".join(para_words[: min(50, len(para_words))])
                        condensed.append(f"<p>{truncated}...</p>")
                        words_used += min(50, len(para_words))
                    in_important_section = False
                continue

            # Keep lists (they're usually important)
            if "<li>" in line or "<ul>" in line or "</ul>" in line:
                line_words = len(re.sub(r"<[^>]+>", "", line).split())
                if words_used + line_words <= target_words:
                    condensed.append(line)
                    words_used += line_words
                continue

            # Skip other content if we're over target
            if words_used >= target_words:
                continue

            # Add line if we have room
            line_words = len(re.sub(r"<[^>]+>", "", line).split())
            if words_used + line_words <= target_words:
                condensed.append(line)
                words_used += line_words

        # Add condensation notice
        condensed.append("""
        <hr>
        <p><em>Note: This document has been condensed for one-pager format. Full content available in source.</em></p>
        """)

        return "\n".join(condensed)

    @classmethod
    def from_file(cls, file_path: str | Path, **kwargs) -> "OnePager":
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
    def from_dict(cls, data: dict[str, Any], **kwargs) -> "OnePager":
        """Create one-pager from dictionary."""
        return cls(content=data, **kwargs)

    @classmethod
    def from_text(cls, text: str, **kwargs) -> "OnePager":
        """Create one-pager from plain text."""
        return cls(content=text, **kwargs)

    @classmethod
    def from_components(
        cls,
        components: list[DocumentComponent],
        title: str | None = None,
        subtitle: str | None = None,
        variables: dict[str, Any] | None = None,
        **kwargs,
    ) -> "OnePager":
        """
        Create one-pager from DocumentComponent list (using WAFT's document model).

        Args:
            components: List of DocumentComponent objects
            title: Document title
            subtitle: Document subtitle
            variables: Additional variables to pass to template
            **kwargs: Additional OnePager options

        Example:
            from waft.evolution.document_components import ComponentBuilder

            components = [
                ComponentBuilder.build_title_component("My Report"),
                ComponentBuilder.build_section_component("Overview", ["Summary text..."]),
                ComponentBuilder.build_section_component("Results", ["Results text..."])
            ]

            OnePager.from_components(
                components=components,
                title="My Report",
                variables={'date': '2026-01-11'}
            )
        """
        # Store components and variables for template rendering
        instance = cls.__new__(cls)
        instance.raw_content = components
        instance.title = title or "One-Pager"
        instance.subtitle = subtitle
        instance.output_path = kwargs.get("output_path")
        instance.kwargs = kwargs
        instance.components = components
        instance.variables = variables or {}

        # Store components for template rendering
        # Content will be processed during generate() when we have access to _markdown_to_html
        instance.html_content = ""  # Will be built during template rendering
        return instance

    @classmethod
    def from_sections(
        cls,
        sections: list[dict[str, Any]],
        title: str | None = None,
        subtitle: str | None = None,
        variables: dict[str, Any] | None = None,
        **kwargs,
    ) -> "OnePager":
        """
        Create one-pager from structured sections and variables.

        Args:
            sections: List of section dicts with 'title' and 'content' keys
            title: Document title
            subtitle: Document subtitle
            variables: Additional variables to pass to template
            **kwargs: Additional OnePager options

        Example:
            OnePager.from_sections(
                sections=[
                    {'title': 'Overview', 'content': 'Summary text...'},
                    {'title': 'Results', 'content': 'Results text...'}
                ],
                title="My Report",
                variables={'date': '2026-01-11', 'author': 'John Doe'}
            )
        """
        # Convert section dicts to DocumentComponents and use from_components
        builder = ComponentBuilder()
        components = []

        # Add title component if provided
        if title:
            components.append(builder.build_title_component(title))

        # Convert sections to section components
        for section in sections:
            title_text = section.get("title", "")
            content = section.get("content", "")
            level = section.get("level", 2)

            # Convert content to list (section components expect list of ideas/content)
            content_list = [content] if isinstance(content, str) else content

            components.append(
                builder.build_section_component(title=title_text, ideas=content_list, level=level)
            )

        # Use from_components to create the instance
        return cls.from_components(
            components=components, title=title, subtitle=subtitle, variables=variables, **kwargs
        )

    @classmethod
    def from_briefing(
        cls,
        chat_context: dict[str, Any] | None = None,
        include_system_status: bool = True,
        title: str | None = None,
        subtitle: str | None = None,
        output_path: Path | None = None,
        **kwargs,
    ) -> "OnePager":
        """
        Create a briefing one-pager with system status and chat context.

        This generates a field guide style 2-page briefing document that includes:
        - Current system status (git, work efforts, health)
        - Chat context (what we're doing, recent topics)
        - Larger context (project state, epistemic state)

        Args:
            chat_context: Optional dict with chat context (topics, current_task, etc.)
            include_system_status: Whether to gather system status (default: True)
            title: Document title (default: "SESSION BRIEFING")
            subtitle: Document subtitle
            output_path: Output PDF path
            **kwargs: Additional options (series, number, classification, etc.)

        Example:
            OnePager.from_briefing(
                chat_context={
                    'current_task': 'Implementing feature X',
                    'recent_topics': ['API design', 'Testing'],
                    'next_steps': ['Write tests', 'Update docs']
                }
            ).generate()
        """
        from datetime import datetime

        # Gather system status if requested
        status_content = ""
        if include_system_status:
            try:
                from scripts.waft_status import check_status, format_status_content

                project_path = Path.cwd()
                status = check_status(
                    project_path=project_path, log_event=False, save_snapshot=False
                )
                # Use professional level for briefing (good balance)
                status_content = format_status_content(status, level="professional")
            except Exception as e:
                status_content = f"<div class='caution'><div class='caution-title'>Status Check Unavailable</div>Could not gather system status: {str(e)}</div>"

        # Build briefing content
        briefing_html = []

        # Chat Context Section
        if chat_context:
            briefing_html.append("<h2>Current Session Context</h2>")

            if chat_context.get("current_task"):
                briefing_html.append(
                    f"<div class='status-box'><div class='status-title'>Current Task</div><p><strong>{html.escape(str(chat_context['current_task']))}</strong></p></div>"
                )

            if chat_context.get("recent_topics"):
                topics = chat_context["recent_topics"]
                if isinstance(topics, list):
                    topics_html = "<ul>"
                    for topic in topics[:5]:  # Limit to 5 most recent
                        topics_html += f"<li>{html.escape(str(topic))}</li>"
                    topics_html += "</ul>"
                    briefing_html.append(f"<h3>Recent Topics</h3>{topics_html}")

            if chat_context.get("key_decisions"):
                decisions = chat_context["key_decisions"]
                if isinstance(decisions, list):
                    decisions_html = "<ul>"
                    for decision in decisions[:5]:
                        decisions_html += f"<li>{html.escape(str(decision))}</li>"
                    decisions_html += "</ul>"
                    briefing_html.append(f"<h3>Key Decisions</h3>{decisions_html}")

            if chat_context.get("next_steps"):
                steps = chat_context["next_steps"]
                if isinstance(steps, list):
                    steps_html = "<ol>"
                    for step in steps[:5]:
                        steps_html += f"<li>{html.escape(str(step))}</li>"
                    steps_html += "</ol>"
                    briefing_html.append(f"<h3>Next Steps</h3>{steps_html}")

        # System Status Section
        if status_content:
            briefing_html.append("<h2>System Status</h2>")
            briefing_html.append(status_content)

        # Combine content
        content_html = "\n".join(briefing_html)

        # Create instance with briefing template
        instance = cls.__new__(cls)
        instance.raw_content = content_html
        instance.title = title or "SESSION BRIEFING"
        instance.subtitle = (
            subtitle or f"Generated {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        )
        instance.output_path = output_path
        instance.kwargs = kwargs
        instance.html_content = content_html
        instance.use_briefing_template = True  # Flag to use briefing template
        instance.briefing_series = kwargs.get("series", "BRIEFING")
        instance.briefing_number = kwargs.get("number", f"BG-{datetime.now().strftime('%Y%m%d')}")
        instance.briefing_classification = kwargs.get("classification", "INTERNAL")
        instance.briefing_issued_by = kwargs.get("issued_by", "WAFT System")
        instance.briefing_date = kwargs.get("date", datetime.now().strftime("%B %d, %Y"))

        return instance


def create_one_pager(
    content: str | Path | dict | list,
    title: str | None = None,
    output_path: Path | None = None,
    **kwargs,
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
