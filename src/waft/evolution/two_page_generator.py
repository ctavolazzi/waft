"""
Two-Page PDF Generator: Evolutionary Document Synthesis

This module generates exactly 2-page PDFs (one double-sided sheet) from
distilled chat conversations using evolved styling genomes.

The generator:
1. Takes DistilledChat (ideas) + StylingGenome (design)
2. Generates HTML with exactly 2 pages
3. Enforces hard 2-page constraint
4. Evaluates fitness (readability, completeness, constraint, aesthetics)
5. Records evolutionary events for tracking

This is the core of the one-pager evolution system.
"""

import hashlib
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from jinja2 import Template

from .chat_distiller import DistilledChat
from .styling_genome import StylingGenome
from ..core.agent.state import EvolutionaryEvent, EvolutionaryEventType


# HTML template for 2-page PDFs with evolutionary styling
TWO_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        /* Page setup - EXACTLY 2 pages */
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

        /* Page break control */
        .page-break {
            page-break-after: always;
        }

        /* Typography */
        h1 {
            font-size: {{ font.size_h1 }}pt;
            color: {{ color.heading }};
            margin-top: 0;
            margin-bottom: {{ margin.section_spacing }}pt;
        }

        h2 {
            font-size: {{ font.size_h2 }}pt;
            color: {{ color.heading }};
            margin-top: {{ margin.section_spacing }}pt;
            margin-bottom: {{ margin.paragraph_spacing }}pt;
        }

        h3 {
            font-size: {{ font.size_h3 }}pt;
            color: {{ color.heading }};
            margin-top: {{ margin.paragraph_spacing }}pt;
            margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;
        }

        p {
            margin: 0 0 {{ margin.paragraph_spacing }}pt 0;
        }

        /* Lists */
        ul, ol {
            margin: 0 0 {{ margin.paragraph_spacing }}pt 0;
            padding-left: 20pt;
        }

        li {
            margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;
        }

        /* Code blocks */
        code {
            font-family: monospace;
            font-size: {{ font.size_code }}pt;
            background: {{ color.code_bg }};
            color: {{ color.code_text }};
            padding: 2pt 4pt;
            border-radius: 2pt;
        }

        /* Sections */
        .section {
            margin-bottom: {{ margin.section_spacing }}pt;
        }

        /* Ideas */
        .idea {
            margin-bottom: {{ margin.paragraph_spacing }}pt;
            padding-left: 10pt;
            border-left: 2pt solid {{ color.accent }};
        }

        .idea-category {
            font-weight: bold;
            color: {{ color.accent }};
            font-size: {{ font.size_h3 - 1 }}pt;
        }

        .idea-content {
            margin-top: {{ margin.paragraph_spacing / 2 }}pt;
        }

        /* Metadata */
        .metadata {
            font-size: {{ font.size_body - 1 }}pt;
            color: {{ color.text }}88;
            margin-top: {{ margin.section_spacing }}pt;
        }

        /* Scientific name */
        .scientific-name {
            font-style: italic;
            color: {{ color.accent }};
        }

        /* Layout variations */
        {% if layout.columns == 2 %}
        .content {
            column-count: 2;
            column-gap: 20pt;
        }
        {% endif %}

        /* Density variations */
        {% if layout.density == 'compact' %}
        body { line-height: 1.4; }
        {% elif layout.density == 'spacious' %}
        body { line-height: 1.8; }
        {% endif %}
    </style>
</head>
<body>
    <!-- PAGE 1 -->
    <div class="page-1">
        <h1>{{ title }}</h1>

        <p><strong>Summary:</strong> {{ summary }}</p>

        <div class="metadata">
            <p><strong>Genome:</strong> <span class="scientific-name">{{ styling_genome_name }}</span> ({{ styling_genome_id[:8] }}...)</p>
            <p><strong>Generated:</strong> {{ generated_at }}</p>
            <p><strong>Total Ideas:</strong> {{ total_ideas }}</p>
        </div>

        <div class="section">
            <h2>Key Ideas</h2>

            {% for idea in top_ideas[:page_1_ideas] %}
            <div class="idea">
                <div class="idea-category">{{ idea.category|upper }}</div>
                <div class="idea-content">{{ idea.content }}</div>
                <div class="metadata">
                    <span class="scientific-name">{{ idea.scientific_name }}</span>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <!-- Page break -->
    <div class="page-break"></div>

    <!-- PAGE 2 -->
    <div class="page-2">
        <div class="section">
            <h2>Additional Insights</h2>

            {% for idea in top_ideas[page_1_ideas:] %}
            <div class="idea">
                <div class="idea-category">{{ idea.category|upper }}</div>
                <div class="idea-content">{{ idea.content }}</div>
                <div class="metadata">
                    <span class="scientific-name">{{ idea.scientific_name }}</span>
                </div>
            </div>
            {% endfor %}
        </div>

        <div class="section">
            <h2>Metrics</h2>
            <ul>
                <li><strong>Decisions:</strong> {{ metrics.decisions }}</li>
                <li><strong>Insights:</strong> {{ metrics.insights }}</li>
                <li><strong>Actions:</strong> {{ metrics.actions }}</li>
                <li><strong>Concepts:</strong> {{ metrics.concepts }}</li>
                <li><strong>Questions:</strong> {{ metrics.questions }}</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""


class TwoPageGenerator:
    """
    Generates exactly 2-page PDFs from distilled chats with evolved styling.

    This is the core component that combines:
    - ChatDistiller output (ideas as genes)
    - StylingGenome (design as genes)
    - Hard 2-page constraint enforcement
    - Fitness evaluation
    """

    def __init__(self, weasyprint_available: bool = False):
        """
        Initialize generator.

        Args:
            weasyprint_available: Whether WeasyPrint is available for PDF generation
        """
        self.weasyprint_available = weasyprint_available

        if weasyprint_available:
            try:
                from weasyprint import HTML
                self.HTML = HTML
            except ImportError:
                self.weasyprint_available = False

    def generate(
        self,
        distilled_chat: DistilledChat,
        styling_genome: StylingGenome,
        output_path: Optional[Path] = None,
        page_1_ideas: int = 5,
    ) -> Dict[str, Any]:
        """
        Generate 2-page PDF from distilled chat with styling genome.

        Args:
            distilled_chat: Distilled conversation
            styling_genome: Styling configuration
            output_path: Optional output path for PDF
            page_1_ideas: Number of ideas to show on page 1

        Returns:
            Dictionary with generation results and fitness metrics
        """
        # Get top ideas
        top_ideas = distilled_chat.get_top_ideas(n=15, min_importance=0.3)

        # Prepare template context
        context = {
            "title": distilled_chat.title,
            "summary": distilled_chat.summary,
            "total_ideas": distilled_chat.total_ideas,
            "metrics": {
                "decisions": distilled_chat.decisions_count,
                "insights": distilled_chat.insights_count,
                "actions": distilled_chat.actions_count,
                "concepts": distilled_chat.concepts_count,
                "questions": distilled_chat.questions_count,
            },
            "top_ideas": [idea.to_dict() for idea in top_ideas],
            "page_1_ideas": page_1_ideas,

            # Styling genome
            "font": styling_genome.genes.font.to_dict(),
            "margin": styling_genome.genes.margin.to_dict(),
            "color": styling_genome.genes.color.to_dict(),
            "layout": styling_genome.genes.layout.to_dict(),
            "styling_genome_name": styling_genome.scientific_name,
            "styling_genome_id": styling_genome.genome_id,

            # Metadata
            "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        }

        # Render HTML
        template = Template(TWO_PAGE_TEMPLATE)
        html_content = template.render(**context)

        # Generate PDF if WeasyPrint available and output path specified
        pdf_path = None
        if output_path and self.weasyprint_available:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            self.HTML(string=html_content).write_pdf(output_path)
            pdf_path = str(output_path)

        # Save HTML fallback
        if output_path:
            html_path = Path(str(output_path).replace('.pdf', '.html'))
            html_path.write_text(html_content)

        # Evaluate fitness
        fitness_metrics = self._evaluate_fitness(
            distilled_chat=distilled_chat,
            top_ideas=top_ideas,
            styling_genome=styling_genome,
            html_content=html_content,
        )

        # Record evolutionary event
        self._record_generation_event(
            distilled_chat=distilled_chat,
            styling_genome=styling_genome,
            fitness_metrics=fitness_metrics,
            output_path=pdf_path,
        )

        return {
            "success": True,
            "pdf_path": pdf_path,
            "html_content": html_content,
            "fitness_metrics": fitness_metrics,
            "ideas_included": len(top_ideas),
            "styling_genome_id": styling_genome.genome_id,
        }

    def _evaluate_fitness(
        self,
        distilled_chat: DistilledChat,
        top_ideas: list,
        styling_genome: StylingGenome,
        html_content: str,
    ) -> Dict[str, float]:
        """
        Evaluate fitness of generated 2-page PDF.

        Fitness components:
        - Readability (35%): Font size, line height, spacing
        - Completeness (30%): How many ideas included
        - Constraint satisfaction (25%): Meets 2-page constraint
        - Aesthetic appeal (10%): Color contrast, layout balance

        Args:
            distilled_chat: Original distilled chat
            top_ideas: Ideas included in PDF
            styling_genome: Styling used
            html_content: Generated HTML

        Returns:
            Dictionary of fitness metrics (0.0-1.0 each)
        """
        # Readability score (based on font size and line height)
        body_size = styling_genome.genes.font.size_body
        line_height = styling_genome.genes.font.line_height

        # Optimal: 11-12pt body, 1.5-1.6 line height
        size_score = 1.0 - abs(body_size - 11.5) / 10.0
        height_score = 1.0 - abs(line_height - 1.55) / 1.0
        readability = (size_score + height_score) / 2
        readability = max(0.0, min(1.0, readability))

        # Completeness score (how many ideas included vs total)
        ideas_ratio = len(top_ideas) / max(distilled_chat.total_ideas, 1)
        completeness = min(ideas_ratio * 1.5, 1.0)  # Boost if we got most ideas

        # Constraint satisfaction (estimate 2-page compliance)
        # This is a rough estimate based on content length
        content_length = len(html_content)
        # Optimal range: 8000-12000 chars for 2 pages
        if 8000 <= content_length <= 12000:
            constraint = 1.0
        elif 6000 <= content_length <= 15000:
            constraint = 0.8
        else:
            constraint = 0.5

        # Aesthetic appeal (very simple heuristic)
        # Check if colors have good contrast
        bg_is_light = styling_genome.genes.color.background.lower() in ["#ffffff", "#fff"]
        text_is_dark = styling_genome.genes.color.text.lower() in ["#000000", "#000"]
        contrast_score = 1.0 if (bg_is_light and text_is_dark) else 0.7

        # Check layout density
        density = styling_genome.genes.layout.density
        density_score = {"compact": 0.8, "normal": 1.0, "spacious": 0.7}.get(density, 0.5)

        aesthetics = (contrast_score + density_score) / 2

        return {
            "readability": readability,
            "completeness": completeness,
            "constraint_satisfaction": constraint,
            "aesthetic_appeal": aesthetics,
            "overall": (
                readability * 0.35 +
                completeness * 0.30 +
                constraint * 0.25 +
                aesthetics * 0.10
            )
        }

    def _record_generation_event(
        self,
        distilled_chat: DistilledChat,
        styling_genome: StylingGenome,
        fitness_metrics: Dict[str, float],
        output_path: Optional[str],
    ):
        """
        Record PDF generation as evolutionary event.

        Args:
            distilled_chat: Source chat
            styling_genome: Styling used
            fitness_metrics: Fitness scores
            output_path: Output file path
        """
        event = EvolutionaryEvent(
            timestamp=datetime.utcnow(),
            genome_id=styling_genome.genome_id,
            parent_id=styling_genome.parent_id,
            generation=styling_genome.generation,
            event_type=EvolutionaryEventType.GYM_EVAL,
            payload={
                "event": "two_page_generation",
                "chat_title": distilled_chat.title,
                "chat_ideas": distilled_chat.total_ideas,
                "output_path": output_path,
                "styling_genome": styling_genome.scientific_name,
            },
            fitness_metrics=fitness_metrics,
            agent_id=f"two_page_generator_{styling_genome.genome_id[:8]}",
            lineage_path=styling_genome.lineage_path,
        )

        styling_genome.flight_recorder.append(event)
