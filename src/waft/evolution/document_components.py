"""
Document Components: Reusable building blocks for PDF generation

Components are the atomic units that can be combined to build documents.
Each component is a variable that can be tested, measured, and evolved.
"""

import html
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ComponentType(Enum):
    """Types of document components."""

    TITLE = "title"
    IMAGE = "image"
    ABSTRACT = "abstract"
    ATTRIBUTION = "attribution"
    METADATA = "metadata"
    SECTION = "section"
    PARAGRAPH = "paragraph"
    LIST = "list"
    TABLE = "table"
    CODE = "code"
    QUOTE = "quote"
    DIVIDER = "divider"


@dataclass
class DocumentComponent:
    """
    A reusable document component that can be tested and evolved.

    Components are variables - the system tries different combinations
    and learns what works.
    """

    component_type: ComponentType
    content: Any  # Can be str, List, Dict, etc.
    metadata: dict[str, Any] = field(default_factory=dict)

    # Layout properties
    size_estimate: float = 0.0  # Estimated space (0.0-1.0)
    priority: float = 1.0  # Importance (higher = more likely to include)

    # Learning data
    success_count: int = 0  # Times this component worked
    failure_count: int = 0  # Times this component failed
    avg_fitness: float = 0.0  # Average fitness when used

    def to_html(self, styling: dict[str, Any]) -> str:
        """Render component to HTML."""
        if self.component_type == ComponentType.TITLE:
            return f"<h1>{self.content}</h1>"
        elif self.component_type == ComponentType.ABSTRACT:
            return f'<div class="abstract"><div class="abstract-title">Abstract</div><p>{self.content}</p></div>'
        elif self.component_type == ComponentType.IMAGE:
            img_path = self.metadata.get("path", "")
            caption = self.metadata.get("caption", "")
            if img_path:
                return f'<div class="diagram"><img src="{img_path}" alt="{caption}" /><div class="figure-caption">{caption}</div></div>'
            return ""
        elif self.component_type == ComponentType.ATTRIBUTION:
            author = self.content.get("author", "") if isinstance(self.content, dict) else ""
            date = self.content.get("date", "") if isinstance(self.content, dict) else ""
            return f'<div class="author-info"><p style="margin: 0;">{author}</p><p style="margin: 2pt 0 0 0; font-size: {styling.get("font", {}).get("size_body", 10) - 1.5}pt;">{date}</p></div>'
        elif self.component_type == ComponentType.METADATA:
            # Render metadata block with document and generation info
            if not isinstance(self.content, dict):
                return ""

            metadata_items = []
            font_size = styling.get("font", {}).get("size_body", 11)
            small_font = font_size - 1.5

            # Document metadata
            if self.content.get("authors"):
                authors = self.content["authors"]
                if isinstance(authors, list):
                    authors_str = ", ".join(authors)
                else:
                    authors_str = str(authors)
                metadata_items.append(
                    f"<p><strong>Author(s):</strong> {html.escape(authors_str)}</p>"
                )

            if self.content.get("subject"):
                metadata_items.append(
                    f"<p><strong>Subject:</strong> {html.escape(str(self.content['subject']))}</p>"
                )

            if self.content.get("keywords"):
                keywords = self.content["keywords"]
                if isinstance(keywords, list):
                    keywords_str = ", ".join(keywords)
                else:
                    keywords_str = str(keywords)
                metadata_items.append(
                    f"<p><strong>Keywords:</strong> {html.escape(keywords_str)}</p>"
                )

            # Generation process metadata
            if self.content.get("generation_info"):
                gen_info = self.content["generation_info"]
                if isinstance(gen_info, dict):
                    gen_items = []
                    if gen_info.get("generator"):
                        gen_items.append(
                            f"<strong>Generator:</strong> {html.escape(str(gen_info['generator']))}"
                        )
                    if gen_info.get("style"):
                        gen_items.append(
                            f"<strong>Style:</strong> {html.escape(str(gen_info['style']))}"
                        )
                    if gen_info.get("timestamp"):
                        gen_items.append(
                            f"<strong>Generated:</strong> {html.escape(str(gen_info['timestamp']))}"
                        )
                    if gen_info.get("version"):
                        gen_items.append(
                            f"<strong>Version:</strong> {html.escape(str(gen_info['version']))}"
                        )
                    if gen_info.get("process"):
                        gen_items.append(
                            f"<strong>Process:</strong> {html.escape(str(gen_info['process']))}"
                        )

                    if gen_items:
                        metadata_items.append(
                            f'<p style="margin-top: {styling.get("margin", {}).get("paragraph_spacing", 8) / 2}pt; padding-top: {styling.get("margin", {}).get("paragraph_spacing", 8) / 2}pt; border-top: 1pt solid {styling.get("color", {}).get("border", "#cccccc")};">{" | ".join(gen_items)}</p>'
                        )

            if not metadata_items:
                return ""

            # Wrap in metadata container
            return f"""<div class="document-metadata" style="font-size: {small_font}pt; color: {styling.get("color", {}).get("text", "#000000")}88; margin: {styling.get("margin", {}).get("paragraph_spacing", 8)}pt 0; padding: {styling.get("margin", {}).get("paragraph_spacing", 8) / 2}pt; background: {styling.get("color", {}).get("code_bg", "#f5f5f5")}40; border-left: 3pt solid {styling.get("color", {}).get("accent", "#000000")};">
                {"".join(metadata_items)}
            </div>"""
        elif self.component_type == ComponentType.SECTION:
            level = self.metadata.get("level", 2)
            title = (
                self.content.get("title", "")
                if isinstance(self.content, dict)
                else str(self.content)
            )
            body = self.content.get("body", "") if isinstance(self.content, dict) else ""

            # Check for status component subtypes for special formatting
            component_subtype = self.metadata.get("component_subtype", "")

            # Check if this is a pillar section (special formatting)
            if (
                "pillar" in title.lower()
                or "substrate" in title.lower()
                or "physics" in title.lower()
                or "flight recorder" in title.lower()
            ):
                return f'<div class="pillar"><div class="pillar-title">{title}</div><div class="pillar-body">{body}</div></div>'

            # Status components get special formatting
            if component_subtype:
                return f'<div class="status-section status-{component_subtype}"><h{level}>{title}</h{level}><div class="status-body">{body}</div></div>'

            return f"<h{level}>{title}</h{level}><div>{body}</div>"
        elif self.component_type == ComponentType.PARAGRAPH:
            return f"<p>{self.content}</p>"
        elif self.component_type == ComponentType.TABLE:
            # Handle table component
            if isinstance(self.content, dict):
                headers = self.content.get("headers", [])
                rows = self.content.get("rows", [])
                table_class = self.content.get("class", "data-table")

                header_row = (
                    "<tr>" + "".join(f"<th>{html.escape(str(h))}</th>" for h in headers) + "</tr>"
                    if headers
                    else ""
                )
                body_rows = "".join(
                    "<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in row) + "</tr>"
                    for row in rows
                )
                return f'<table class="{table_class}">{header_row}{body_rows}</table>'
            return f"<table>{self.content}</table>"
        elif self.component_type == ComponentType.LIST:
            # Handle list component
            if isinstance(self.content, dict):
                items = self.content.get("items", [])
                ordered = self.content.get("ordered", False)
                tag = "ol" if ordered else "ul"
                list_items = "".join(f"<li>{html.escape(str(item))}</li>" for item in items)
                return f"<{tag}>{list_items}</{tag}>"
            return f"<ul><li>{self.content}</li></ul>"
        # Add more component types as needed
        return f"<div>{self.content}</div>"

    def estimate_size(self) -> float:
        """Estimate component size (0.0-1.0 of a page)."""
        if self.size_estimate > 0:
            return self.size_estimate

        # Rough estimates based on type
        estimates = {
            ComponentType.TITLE: 0.05,
            ComponentType.IMAGE: 0.15,
            ComponentType.ABSTRACT: 0.10,
            ComponentType.ATTRIBUTION: 0.03,
            ComponentType.METADATA: 0.08,
            ComponentType.SECTION: 0.20,
            ComponentType.PARAGRAPH: 0.08,
        }
        return estimates.get(self.component_type, 0.10)


@dataclass
class DocumentLayout:
    """
    A document layout configuration - a combination of components.

    The system tries different layouts and learns which work best.
    """

    components: list[DocumentComponent]
    allowed_pages: int = 2
    metadata: dict[str, Any] = field(default_factory=dict)

    # Learning data
    tested: bool = False
    page_count: int | None = None
    fitness: float = 0.0
    success: bool = False

    def estimate_total_size(self) -> float:
        """Estimate total size across all components."""
        return sum(comp.estimate_size() for comp in self.components)

    def to_html(self, styling: dict[str, Any]) -> str:
        """Render entire layout to HTML."""
        html_parts = []
        for comp in self.components:
            html_parts.append(comp.to_html(styling))
        return "\n".join(html_parts)


class ComponentBuilder:
    """
    Builds components from distilled content.

    Converts ideas into reusable components that can be tested.
    """

    @staticmethod
    def build_title_component(title: str) -> DocumentComponent:
        """Build title component."""
        return DocumentComponent(
            component_type=ComponentType.TITLE,
            content=title,
            size_estimate=0.05,
            priority=1.0,
        )

    @staticmethod
    def build_image_component(image_path: str, caption: str = "") -> DocumentComponent:
        """Build image component."""
        return DocumentComponent(
            component_type=ComponentType.IMAGE,
            content=image_path,
            metadata={"path": image_path, "caption": caption},
            size_estimate=0.15,
            priority=0.8,
        )

    @staticmethod
    def build_abstract_component(summary: str) -> DocumentComponent:
        """Build abstract component."""
        return DocumentComponent(
            component_type=ComponentType.ABSTRACT,
            content=summary,
            size_estimate=0.10,
            priority=0.9,
        )

    @staticmethod
    def build_attribution_component(author: str, date: str) -> DocumentComponent:
        """Build attribution component."""
        return DocumentComponent(
            component_type=ComponentType.ATTRIBUTION,
            content={"author": author, "date": date},
            size_estimate=0.03,
            priority=0.7,
        )

    @staticmethod
    def build_metadata_component(
        authors: str | list[str] | None = None,
        subject: str | None = None,
        keywords: str | list[str] | None = None,
        generation_info: dict[str, Any] | None = None,
    ) -> DocumentComponent:
        """
        Build metadata component with document and generation information.

        Args:
            authors: Author name(s) - can be string or list
            subject: Document subject/topic
            keywords: Keywords - can be string or list
            generation_info: Dictionary with generation process info:
                - generator: Generator name/version
                - style: Style preset used
                - timestamp: Generation timestamp
                - version: WAFT version
                - process: Description of generation process

        Returns:
            DocumentComponent for metadata
        """
        content = {}
        if authors:
            content["authors"] = authors
        if subject:
            content["subject"] = subject
        if keywords:
            content["keywords"] = keywords
        if generation_info:
            content["generation_info"] = generation_info

        return DocumentComponent(
            component_type=ComponentType.METADATA,
            content=content,
            size_estimate=0.08,
            priority=0.6,  # Lower priority - can be omitted if space is tight
        )

    @staticmethod
    def build_section_component(title: str, ideas: list[Any], level: int = 2) -> DocumentComponent:
        """Build section component from ideas."""
        # Combine ideas into section body
        if not ideas:
            body = ""
        else:
            # Clean and join idea content (preserve newlines for markdown)
            cleaned_ideas = []
            for idea in ideas:
                if hasattr(idea, "content"):
                    content = idea.content
                    # Clean markdown if needed
                    if isinstance(content, str):
                        cleaned_ideas.append(content)
                else:
                    cleaned_ideas.append(str(idea))
            # Join with newlines to preserve markdown structure (lists, paragraphs, etc.)
            body = "\n\n".join(cleaned_ideas)

        # #region agent log
        with open("/Users/ctavolazzi/Code/active/waft/.cursor/debug.log", "a") as f:
            import json

            f.write(
                json.dumps(
                    {
                        "sessionId": "debug-session",
                        "runId": "run1",
                        "hypothesisId": "A",
                        "location": "document_components.py:190",
                        "message": "build_section_component body created",
                        "data": {
                            "title": title,
                            "body_length": len(body) if body else 0,
                            "body_preview": body[:150] if body else "",
                            "ideas_count": len(ideas),
                        },
                        "timestamp": int(time.time() * 1000),
                    }
                )
                + "\n"
            )
        # #endregion

        return DocumentComponent(
            component_type=ComponentType.SECTION,
            content={"title": title, "body": body},
            metadata={"level": level, "idea_count": len(ideas)},
            size_estimate=min(0.5, 0.15 * max(1, len(ideas))),  # Cap at 0.5
            priority=0.8,
        )

    @staticmethod
    def build_paragraph_component(text: str) -> DocumentComponent:
        """Build paragraph component."""
        return DocumentComponent(
            component_type=ComponentType.PARAGRAPH,
            content=text,
            size_estimate=0.08,
            priority=0.6,
        )

    @staticmethod
    def build_list_component(items: list[str], ordered: bool = False) -> DocumentComponent:
        """Build list component."""
        return DocumentComponent(
            component_type=ComponentType.LIST,
            content={"items": items, "ordered": ordered},
            size_estimate=0.05 * len(items),
            priority=0.7,
        )

    @staticmethod
    def build_code_component(code: str, language: str = "") -> DocumentComponent:
        """Build code component."""
        return DocumentComponent(
            component_type=ComponentType.CODE,
            content=code,
            metadata={"language": language},
            size_estimate=0.15,
            priority=0.8,
        )

    @staticmethod
    def build_quote_component(quote: str, attribution: str = "") -> DocumentComponent:
        """Build quote component."""
        return DocumentComponent(
            component_type=ComponentType.QUOTE,
            content={"quote": quote, "attribution": attribution},
            size_estimate=0.10,
            priority=0.7,
        )

    @staticmethod
    def build_divider_component() -> DocumentComponent:
        """Build divider component."""
        return DocumentComponent(
            component_type=ComponentType.DIVIDER,
            content="",
            size_estimate=0.02,
            priority=0.5,
        )


class LayoutAlgorithm:
    """
    Algorithm that tries different component combinations.

    "Fuck around and find out" - tests layouts, records results, learns.
    """

    def __init__(self, allowed_pages: int = 2):
        self.allowed_pages = allowed_pages
        self.learning_log: list[dict[str, Any]] = []

    def generate_layouts(
        self, components: list[DocumentComponent], max_attempts: int = 10
    ) -> list[DocumentLayout]:
        """
        Generate multiple layout configurations to test.

        Tries different combinations of components.
        """
        layouts = []

        # Sort components by priority
        sorted_components = sorted(components, key=lambda c: c.priority, reverse=True)

        # Strategy 1: Include all high-priority components
        high_priority = [c for c in sorted_components if c.priority >= 0.8]
        if high_priority:
            layouts.append(
                DocumentLayout(
                    components=high_priority,
                    allowed_pages=self.allowed_pages,
                    metadata={"strategy": "high_priority"},
                )
            )

        # Strategy 2: Science paper structure (Title → Image → Abstract → Attribution → Sections)
        science_paper_components = []
        for comp_type in [
            ComponentType.TITLE,
            ComponentType.IMAGE,
            ComponentType.ABSTRACT,
            ComponentType.ATTRIBUTION,
            ComponentType.SECTION,
        ]:
            matching = [c for c in sorted_components if c.component_type == comp_type]
            if matching:
                science_paper_components.extend(matching[:2])  # Max 2 of each type

        if science_paper_components:
            layouts.append(
                DocumentLayout(
                    components=science_paper_components,
                    allowed_pages=self.allowed_pages,
                    metadata={"strategy": "science_paper"},
                )
            )

        # Strategy 3: Greedy - add components until size limit
        greedy_components = []
        total_size = 0.0
        for comp in sorted_components:
            comp_size = comp.estimate_size()
            if total_size + comp_size <= self.allowed_pages * 1.0:  # Allow slight overflow
                greedy_components.append(comp)
                total_size += comp_size

        if greedy_components:
            layouts.append(
                DocumentLayout(
                    components=greedy_components,
                    allowed_pages=self.allowed_pages,
                    metadata={"strategy": "greedy"},
                )
            )

        # Strategy 4-N: Random combinations (for exploration)
        import random

        for _ in range(max_attempts - 3):
            num_components = random.randint(3, min(len(sorted_components), 10))
            selected = random.sample(sorted_components, num_components)
            layouts.append(
                DocumentLayout(
                    components=selected,
                    allowed_pages=self.allowed_pages,
                    metadata={"strategy": "random"},
                )
            )

        return layouts

    def test_layout(self, layout: DocumentLayout, actual_page_count: int) -> dict[str, Any]:
        """
        Test a layout and record results.

        Returns learning data about what worked/didn't work.
        """
        success = actual_page_count == layout.allowed_pages
        page_diff = abs(actual_page_count - layout.allowed_pages)

        # Calculate fitness (1.0 = perfect, 0.0 = terrible)
        if success:
            fitness = 1.0
        else:
            # Penalize based on how far off we are
            fitness = max(0.0, 1.0 - (page_diff * 0.3))

        layout.tested = True
        layout.page_count = actual_page_count
        layout.fitness = fitness
        layout.success = success

        # Record learning data
        learning_entry = {
            "layout": layout,
            "success": success,
            "fitness": fitness,
            "page_count": actual_page_count,
            "target_pages": layout.allowed_pages,
            "strategy": layout.metadata.get("strategy", "unknown"),
            "components_used": [c.component_type.value for c in layout.components],
        }

        self.learning_log.append(learning_entry)

        # Update component learning data
        for comp in layout.components:
            if success:
                comp.success_count += 1
                comp.avg_fitness = (
                    comp.avg_fitness * (comp.success_count - 1) + fitness
                ) / comp.success_count
            else:
                comp.failure_count += 1

        return learning_entry

    def get_best_layout(self) -> DocumentLayout | None:
        """Get the best layout from tested layouts."""
        tested = [l for l in self.learning_log if l["layout"].tested]
        if not tested:
            return None

        best = max(tested, key=lambda x: x["fitness"])
        return best["layout"]

    def get_learning_summary(self) -> dict[str, Any]:
        """Get summary of what was learned."""
        if not self.learning_log:
            return {"total_tests": 0}

        successful = [l for l in self.learning_log if l["success"]]
        failed = [l for l in self.learning_log if not l["success"]]

        # Analyze strategies
        strategy_performance = {}
        for entry in self.learning_log:
            strategy = entry["strategy"]
            if strategy not in strategy_performance:
                strategy_performance[strategy] = {"success": 0, "total": 0, "avg_fitness": 0.0}
            strategy_performance[strategy]["total"] += 1
            if entry["success"]:
                strategy_performance[strategy]["success"] += 1
            strategy_performance[strategy]["avg_fitness"] += entry["fitness"]

        for strategy in strategy_performance:
            total = strategy_performance[strategy]["total"]
            if total > 0:
                strategy_performance[strategy]["avg_fitness"] /= total

        return {
            "total_tests": len(self.learning_log),
            "successful": len(successful),
            "failed": len(failed),
            "success_rate": len(successful) / len(self.learning_log) if self.learning_log else 0.0,
            "strategy_performance": strategy_performance,
            "best_fitness": max(l["fitness"] for l in self.learning_log)
            if self.learning_log
            else 0.0,
        }
