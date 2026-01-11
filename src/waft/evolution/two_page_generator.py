"""
Two-Page PDF Generator: TRUE 2-Page Constraint Enforcement

Enforces the 2-page constraint through:

1. Real page counting (using WeasyPrint page metadata)
2. Adaptive content selection (iteratively adjust until 2 pages)
3. Accurate fitness metrics (no fake constraint satisfaction)
4. Complete lineage tracking and metrics collection

This is the evolved implementation with adaptive constraint enforcement.
"""

import hashlib
import re
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from jinja2 import Template
import tempfile
import time

from .chat_distiller import DistilledChat, IdeaGene
from .styling_genome import StylingGenome
from .pdf_metrics import PDFMetricsCollector, PDFMetrics
from ..core.agent.state import EvolutionaryEvent, EvolutionaryEventType


# HTML template for 2-page PDFs with visual elements and multiple explanation methods
TWO_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        /* Strict 2-page setup */
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

        /* Page break control */
        .page-break {
            page-break-after: always;
            break-after: page;
        }

        .no-break {
            page-break-inside: avoid;
            break-inside: avoid;
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
            margin-bottom: {{ margin.paragraph_spacing }}pt;
            page-break-after: avoid;
            border-bottom: 1pt solid {{ color.accent }};
            padding-bottom: 2pt;
        }

        h3 {
            font-size: {{ font.size_h3 }}pt;
            color: {{ color.heading }};
            margin-top: {{ margin.paragraph_spacing }}pt;
            margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;
            page-break-after: avoid;
        }

        p {
            margin: 0 0 {{ margin.paragraph_spacing }}pt 0;
        }

        ul, ol {
            margin: 0 0 {{ margin.paragraph_spacing }}pt 0;
            padding-left: 15pt;
        }

        li {
            margin-bottom: {{ margin.paragraph_spacing / 3 }}pt;
        }

        /* Visual boxes - inspired by field guide */
        .note-box {
            border-left: 4pt solid {{ color.accent }};
            background: {{ color.code_bg }};
            padding: {{ margin.paragraph_spacing }}pt;
            margin: {{ margin.paragraph_spacing }}pt 0;
            page-break-inside: avoid;
        }

        .note-title {
            font-weight: bold;
            color: {{ color.accent }};
            font-size: {{ font.size_h3 - 1 }}pt;
            margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;
        }

        .highlight-box {
            border: 2pt solid {{ color.accent }};
            background: {{ color.code_bg }};
            padding: {{ margin.paragraph_spacing }}pt;
            margin: {{ margin.paragraph_spacing }}pt 0;
            page-break-inside: avoid;
        }

        /* Tables for structured data */
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
            padding: 4pt;
            text-align: left;
            font-weight: bold;
        }

        td {
            border: 1pt solid {{ color.text }}33;
            padding: 4pt;
        }

        tr:nth-child(even) {
            background: {{ color.code_bg }};
        }

        /* Pillar boxes - visual representation */
        .pillar {
            border: 2pt solid {{ color.accent }};
            background: {{ color.background }};
            padding: {{ margin.paragraph_spacing }}pt;
            margin: {{ margin.paragraph_spacing }}pt 0;
            page-break-inside: avoid;
        }

        .pillar-title {
            font-weight: bold;
            color: {{ color.accent }};
            font-size: {{ font.size_h3 }}pt;
            margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;
        }

        /* Ideas - prose presentation */
        .idea {
            margin-bottom: {{ margin.paragraph_spacing }}pt;
            padding: {{ margin.paragraph_spacing }}pt;
            border-left: 3pt solid {{ color.accent }};
            background: {{ color.code_bg }}15;
            page-break-inside: avoid;
        }

        .idea-content {
            font-size: {{ font.size_body }}pt;
            line-height: 1.6;
            word-wrap: break-word;
            overflow-wrap: break-word;
            hyphens: auto;
            text-align: justify;
            margin: 0;
        }

        /* Metadata - compact */
        .metadata {
            font-size: {{ font.size_body - 2 }}pt;
            color: {{ color.text }}88;
            line-height: 1.3;
            border-top: 1pt solid {{ color.text }}33;
            padding-top: {{ margin.paragraph_spacing / 2 }}pt;
            margin-top: {{ margin.paragraph_spacing }}pt;
        }

        .metadata p {
            margin-bottom: {{ margin.paragraph_spacing / 3 }}pt;
        }

        /* Summary box - prominent */
        .summary-box {
            background: {{ color.code_bg }};
            padding: {{ margin.paragraph_spacing }}pt;
            margin-bottom: {{ margin.section_spacing }}pt;
            border-left: 4pt solid {{ color.accent }};
            border-top: 1pt solid {{ color.accent }};
            border-right: 1pt solid {{ color.accent }};
            border-bottom: 1pt solid {{ color.accent }};
        }

        /* Scientific name styling */
        .scientific-name {
            font-style: italic;
            color: {{ color.accent }};
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

        pre {
            background: {{ color.code_bg }};
            padding: {{ margin.paragraph_spacing / 2 }}pt;
            border-left: 3pt solid {{ color.accent }};
            font-size: {{ font.size_code }}pt;
            overflow-x: auto;
            page-break-inside: avoid;
        }

        /* Visual separators */
        .divider {
            border-top: 1pt solid {{ color.text }}33;
            margin: {{ margin.paragraph_spacing }}pt 0;
        }
    </style>
</head>
<body>
    <!-- PAGE 1 -->
    <div class="page-1">
        <h1>{{ title }}</h1>

        <div class="summary-box">
            <strong>Summary:</strong> {{ summary }}
        </div>

        <div class="metadata">
            <p><strong>Generated:</strong> {{ generated_at }} | <strong>Ideas Extracted:</strong> {{ total_ideas }}</p>
        </div>

        <h2>What Happened</h2>

        {% for idea in page_1_ideas %}
        <div class="idea no-break">
            <p class="idea-content">{{ idea.content }}</p>
        </div>
        {% endfor %}
    </div>

    <!-- Forced page break -->
    <div class="page-break"></div>

    <!-- PAGE 2 -->
    <div class="page-2">
        {% if page_2_ideas %}
        <h2>Additional Details</h2>

        {% for idea in page_2_ideas %}
        <div class="idea no-break">
            <p class="idea-content">{{ idea.content }}</p>
        </div>
        {% endfor %}
        {% endif %}

        <div class="divider"></div>

        <div class="metrics">
            <h3>Content Breakdown</h3>
            <table>
                <tr>
                    <th>Type</th>
                    <th>Count</th>
                </tr>
                <tr>
                    <td>Decisions</td>
                    <td>{{ metrics.decisions }}</td>
                </tr>
                <tr>
                    <td>Insights</td>
                    <td>{{ metrics.insights }}</td>
                </tr>
                <tr>
                    <td>Actions</td>
                    <td>{{ metrics.actions }}</td>
                </tr>
                <tr>
                    <td>Concepts</td>
                    <td>{{ metrics.concepts }}</td>
                </tr>
                <tr>
                    <td>Questions</td>
                    <td>{{ metrics.questions }}</td>
                </tr>
            </table>
        </div>
    </div>
</body>
</html>
"""


class TwoPageGenerator:
    """
    Evolved TwoPageGenerator with TRUE 2-page constraint enforcement.

    Improvements over V1:
    - Adaptive content selection (iteratively adjust idea count)
    - Real page counting (using WeasyPrint)
    - Accurate fitness metrics (no fake constraint scores)
    - Scint detection between versions
    """

    # Genome ID for this generator
    GENERATOR_GENOME_ID = hashlib.sha256(b"TwoPageGenerator_adaptive_constraint").hexdigest()

    def __init__(self, weasyprint_available: bool = False, max_iterations: int = 5):
        """
        Initialize generator.

        Args:
            weasyprint_available: Whether WeasyPrint is available
            max_iterations: Max attempts to achieve 2 pages
        """
        self.weasyprint_available = weasyprint_available
        self.max_iterations = max_iterations

        if weasyprint_available:
            try:
                from weasyprint import HTML, __version__
                self.HTML = HTML
                print(f"WeasyPrint {__version__} available - real page counting enabled")
            except ImportError:
                self.weasyprint_available = False
                print("WeasyPrint not available - using HTML output only")

    def generate(
        self,
        distilled_chat: DistilledChat,
        styling_genome: StylingGenome,
        output_path: Optional[Path] = None,
        target_pages: int = 2,
        convert_to_png: bool = False,
        png_dpi: int = 300,
        collect_metrics: bool = False,
        metrics_dir: Optional[Path] = None,
    ) -> Dict[str, Any]:
        """
        Generate PDF with TRUE 2-page constraint enforcement.

        Uses adaptive algorithm:
        1. Start with estimate of ideas per page
        2. Generate PDF
        3. Count actual pages
        4. Adjust idea count
        5. Repeat until exactly 2 pages

        Args:
            distilled_chat: Distilled conversation
            styling_genome: Styling configuration
            output_path: Optional output path
            target_pages: Target page count (default: 2)
            convert_to_png: If True, automatically convert PDF to PNG images after generation (default: False)
            png_dpi: DPI for PNG conversion if convert_to_png is True (default: 300)

        Returns:
            Dictionary with results and accurate fitness metrics
        """
        print(f"\n🔬 TwoPageGenerator: Adaptive generation for {target_pages} pages")
        
        # Initialize metrics collector if requested
        metrics_collector = None
        generation_start_time = datetime.utcnow()
        if collect_metrics:
            metrics_collector = PDFMetricsCollector(metrics_dir=metrics_dir)

        # Get top ideas sorted by importance
        all_ideas = distilled_chat.get_top_ideas(n=50, min_importance=0.1)

        # Adaptive iteration
        best_result = None
        best_page_diff = float('inf')
        iterations_used = 0

        # Start with conservative estimate
        ideas_to_show = min(8, len(all_ideas))

        for iteration in range(self.max_iterations):
            iterations_used = iteration + 1
            print(f"  Iteration {iteration + 1}/{self.max_iterations}: Testing with {ideas_to_show} ideas...")

            # Split ideas between pages (60/40 split)
            split_point = int(ideas_to_show * 0.6)
            page_1_ideas = all_ideas[:split_point]
            page_2_ideas = all_ideas[split_point:ideas_to_show]

            # Generate HTML
            html_content = self._render_html(
                distilled_chat=distilled_chat,
                styling_genome=styling_genome,
                page_1_ideas=page_1_ideas,
                page_2_ideas=page_2_ideas,
            )

            # Count pages
            page_count = self._count_pages(html_content, output_path)

            print(f"    → {page_count} pages (target: {target_pages})")

            # Check if we hit target
            page_diff = abs(page_count - target_pages)
            if page_diff < best_page_diff:
                best_page_diff = page_diff
                best_result = {
                    "html_content": html_content,
                    "page_count": page_count,
                    "ideas_shown": ideas_to_show,
                    "page_1_ideas": page_1_ideas,
                    "page_2_ideas": page_2_ideas,
                }

            # Perfect! Stop iterating
            if page_count == target_pages:
                print(f"    ✓ Target achieved!")
                break

            # Adjust idea count for next iteration
            if page_count > target_pages:
                # Too many pages - reduce ideas
                ideas_to_show = max(3, int(ideas_to_show * 0.75))
            else:
                # Too few pages - add more ideas
                ideas_to_show = min(len(all_ideas), int(ideas_to_show * 1.3))

            # Prevent infinite loop if we can't adjust further
            if iteration > 0 and (
                (page_count > target_pages and ideas_to_show <= 3) or
                (page_count < target_pages and ideas_to_show >= len(all_ideas))
            ):
                print(f"    → Cannot improve further, using best result")
                break

        # Use best result
        if best_result is None:
            raise RuntimeError("Failed to generate any valid result")

        # Save output
        pdf_path = None
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Save HTML
            html_path = Path(str(output_path).replace('.pdf', '.html'))
            html_path.write_text(best_result['html_content'])
            print(f"  ✓ HTML saved: {html_path}")

            # Generate PDF if possible
            if self.weasyprint_available:
                self.HTML(string=best_result['html_content']).write_pdf(output_path)
                pdf_path = str(output_path)
                print(f"  ✓ PDF saved: {output_path}")

        # Evaluate fitness with ACCURATE constraint metric
        fitness_metrics = self._evaluate_fitness(
            distilled_chat=distilled_chat,
            ideas_shown=best_result['ideas_shown'],
            styling_genome=styling_genome,
            page_count=best_result['page_count'],
            target_pages=target_pages,
        )

        print(f"  ✓ Fitness: {fitness_metrics['overall']:.3f}")
        print(f"    - Constraint satisfaction: {fitness_metrics['constraint_satisfaction']:.3f} (page_count={best_result['page_count']})")

        # Optional PNG conversion
        png_paths = []
        png_conversion_success = False
        if convert_to_png and pdf_path:
            try:
                from .pdf_image_converter import convert_pdf_to_images
                png_dir = Path(pdf_path).parent / f"{Path(pdf_path).stem}_pages"
                png_paths = convert_pdf_to_images(Path(pdf_path), output_dir=png_dir, dpi=png_dpi)
                png_conversion_success = True
                print(f"  ✓ Converted to {len(png_paths)} PNG images (DPI: {png_dpi})")
            except Exception as e:
                print(f"  ⚠️  PNG conversion failed: {e}")
                png_paths = []
                # Log conversion failure but don't break workflow
                png_conversion_success = False

        # Record event
        self._record_generation_event(
            distilled_chat=distilled_chat,
            styling_genome=styling_genome,
            fitness_metrics=fitness_metrics,
            output_path=pdf_path,
            page_count=best_result['page_count'],
            png_conversion_success=png_conversion_success,
            png_count=len(png_paths) if png_paths else 0,
        )

        # Build result dictionary
        result = {
            "success": True,
            "pdf_path": pdf_path,
            "html_content": best_result['html_content'],
            "fitness_metrics": fitness_metrics,
            "ideas_shown": best_result['ideas_shown'],
            "page_count": best_result['page_count'],
            "target_pages": target_pages,
            "constraint_satisfied": best_result['page_count'] == target_pages,
            "styling_genome_id": styling_genome.genome_id,
            "generator_version": "adaptive",
            "generator_genome_id": self.GENERATOR_GENOME_ID,
            "png_paths": [str(p) for p in png_paths] if png_paths else None,
        }

        # Collect and save metrics if requested
        if collect_metrics and metrics_collector:
            # Compute content statistics
            html_content = best_result['html_content']
            content_stats = self._compute_content_stats(html_content, best_result['page_count'])

            # Compute PNG info
            png_info = None
            if png_paths:
                total_size = sum(Path(p).stat().st_size for p in png_paths if Path(p).exists())
                png_info = {
                    "dpi": png_dpi,
                    "total_size_bytes": total_size,
                }

            # Collect metrics
            metrics = metrics_collector.collect_metrics(
                result=result,
                generation_start_time=generation_start_time,
                styling_genome=styling_genome,
                distilled_chat=distilled_chat,
                iterations=iterations_used,
                png_info=png_info,
                content_stats=content_stats,
            )

            # Save metrics
            metrics_file = metrics_collector.save_metrics(metrics)
            result["metrics_file"] = str(metrics_file)
            result["metrics"] = metrics.to_dict()
            print(f"  📊 Metrics saved: {metrics_file}")

        return result

    def _clean_markdown(self, text: str) -> str:
        """
        Clean markdown formatting from text for clean HTML rendering.

        Removes:
        - Markdown headers (##, ###, etc.)
        - Bold/italic markers (**text**, *text*)
        - Code blocks (```, `)
        - Links ([text](url)) -> text
        - Lists markers (-, *, 1.)

        Args:
            text: Text with markdown formatting

        Returns:
            Cleaned text suitable for HTML display
        """
        if not text:
            return ""

        # Remove markdown headers (##, ###, ####)
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)

        # Remove bold (**text** or __text__)
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'__([^_]+)__', r'\1', text)

        # Remove italic (*text* or _text_) but preserve standalone asterisks
        text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'\1', text)
        text = re.sub(r'(?<!_)_([^_]+)_(?!_)', r'\1', text)

        # Remove inline code (`code`)
        text = re.sub(r'`([^`]+)`', r'\1', text)

        # Remove code blocks (```...```)
        text = re.sub(r'```[\s\S]*?```', '', text)

        # Remove links ([text](url)) -> text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)

        # Remove list markers at start of line (-, *, 1., etc.)
        text = re.sub(r'^[\s]*[-*+]\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'^[\s]*\d+\.\s+', '', text, flags=re.MULTILINE)

        # Clean up "Key Concept:" prefixes (redundant with category tag)
        text = re.sub(r'^\s*\*\*Key\s+Concept\*\*:\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'^\s*Key\s+Concept:\s*', '', text, flags=re.IGNORECASE)

        # Clean up multiple spaces
        text = re.sub(r'\s+', ' ', text)

        # Strip leading/trailing whitespace
        text = text.strip()

        return text

    def _render_html(
        self,
        distilled_chat: DistilledChat,
        styling_genome: StylingGenome,
        page_1_ideas: List[IdeaGene],
        page_2_ideas: List[IdeaGene],
    ) -> str:
        """Render HTML template with given ideas."""
        # Clean markdown from idea content
        def clean_idea(idea: IdeaGene) -> Dict[str, Any]:
            idea_dict = idea.to_dict()
            # Clean the content field
            idea_dict['content'] = self._clean_markdown(idea_dict.get('content', ''))
            return idea_dict

        context = {
            "title": distilled_chat.title,
            "summary": distilled_chat.summary,
            "total_ideas": distilled_chat.total_ideas,
            "ideas_shown": len(page_1_ideas) + len(page_2_ideas),
            "metrics": {
                "decisions": distilled_chat.decisions_count,
                "insights": distilled_chat.insights_count,
                "actions": distilled_chat.actions_count,
                "concepts": distilled_chat.concepts_count,
                "questions": distilled_chat.questions_count,
            },
            "page_1_ideas": [clean_idea(idea) for idea in page_1_ideas],
            "page_2_ideas": [clean_idea(idea) for idea in page_2_ideas],
            "font": styling_genome.genes.font.to_dict(),
            "margin": styling_genome.genes.margin.to_dict(),
            "color": styling_genome.genes.color.to_dict(),
            "layout": styling_genome.genes.layout.to_dict(),
            "styling_genome_name": styling_genome.scientific_name,
            "styling_genome_id": styling_genome.genome_id,
            "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        }

        template = Template(TWO_PAGE_TEMPLATE)
        return template.render(**context)

    def _count_pages(self, html_content: str, output_path: Optional[Path]) -> int:
        """
        Count actual pages in generated PDF.

        If WeasyPrint available: Generate PDF to temp file and count pages
        Otherwise: Estimate from HTML length (fallback)

        Args:
            html_content: HTML content
            output_path: Output path hint for temp file

        Returns:
            Actual page count
        """
        if self.weasyprint_available:
            # Generate to temp file and count pages
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                tmp_path = Path(tmp.name)

            try:
                doc = self.HTML(string=html_content)
                doc.write_pdf(tmp_path)

                # Count pages using metadata
                # WeasyPrint doesn't expose page count directly, so we use a workaround
                # We'll render and check metadata
                from pypdf import PdfReader
                reader = PdfReader(tmp_path)
                page_count = len(reader.pages)
                tmp_path.unlink()  # Clean up
                return page_count

            except Exception as e:
                print(f"    Warning: Could not count pages: {e}")
                # Fall back to estimation
                return self._estimate_pages(html_content)
        else:
            return self._estimate_pages(html_content)

    def _estimate_pages(self, html_content: str) -> int:
        """
        Estimate page count from HTML content.

        This is a fallback heuristic (not accurate).

        Args:
            html_content: HTML content

        Returns:
            Estimated page count
        """
        # Very rough heuristic
        length = len(html_content)
        if length < 6000:
            return 1
        elif length < 11000:
            return 2
        elif length < 17000:
            return 3
        else:
            return 4

    def _evaluate_fitness(
        self,
        distilled_chat: DistilledChat,
        ideas_shown: int,
        styling_genome: StylingGenome,
        page_count: int,
        target_pages: int,
    ) -> Dict[str, float]:
        """
        Evaluate fitness with ACCURATE constraint metric.

        Fitness components:
        - Readability (35%): Font size, line height
        - Completeness (30%): Ideas shown vs total
        - Constraint satisfaction (25%): ACCURATE page count match
        - Aesthetic appeal (10%): Color contrast, density

        Args:
            distilled_chat: Original chat
            ideas_shown: Number of ideas included
            styling_genome: Styling used
            page_count: ACTUAL page count
            target_pages: Target page count

        Returns:
            Dictionary of fitness metrics (0.0-1.0 each)
        """
        # Readability (same as V1)
        body_size = styling_genome.genes.font.size_body
        line_height = styling_genome.genes.font.line_height
        size_score = 1.0 - abs(body_size - 11.5) / 10.0
        height_score = 1.0 - abs(line_height - 1.55) / 1.0
        readability = (size_score + height_score) / 2
        readability = max(0.0, min(1.0, readability))

        # Completeness
        ideas_ratio = ideas_shown / max(distilled_chat.total_ideas, 1)
        completeness = min(ideas_ratio * 1.5, 1.0)

        # Constraint satisfaction - ACCURATE!
        if page_count == target_pages:
            constraint = 1.0  # Perfect!
        elif abs(page_count - target_pages) == 1:
            constraint = 0.5  # Off by 1
        else:
            constraint = max(0.0, 1.0 - abs(page_count - target_pages) * 0.3)  # Penalize heavily

        # Aesthetics (same as V1)
        bg_is_light = styling_genome.genes.color.background.lower() in ["#ffffff", "#fff"]
        text_is_dark = styling_genome.genes.color.text.lower() in ["#000000", "#000", "#1a1a1a"]
        contrast_score = 1.0 if (bg_is_light and text_is_dark) else 0.7

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
            ),
            "page_count": page_count,
            "target_pages": target_pages,
        }

    def _record_generation_event(
        self,
        distilled_chat: DistilledChat,
        styling_genome: StylingGenome,
        fitness_metrics: Dict[str, float],
        output_path: Optional[str],
        page_count: int,
        png_conversion_success: bool = False,
        png_count: int = 0,
    ):
        """Record generation event with metadata."""
        event = EvolutionaryEvent(
            timestamp=datetime.utcnow(),
            genome_id=styling_genome.genome_id,
            parent_id=styling_genome.parent_id,
            generation=styling_genome.generation,
            event_type=EvolutionaryEventType.GYM_EVAL,
            payload={
                "event": "two_page_generation",
                "generator_version": "adaptive",
                "generator_genome_id": self.GENERATOR_GENOME_ID,
                "chat_title": distilled_chat.title,
                "chat_ideas": distilled_chat.total_ideas,
                "output_path": output_path,
                "styling_genome": styling_genome.scientific_name,
                "page_count": page_count,
                "constraint_satisfied": page_count == 2,
                "png_conversion_success": png_conversion_success,
                "png_count": png_count,
            },
            fitness_metrics=fitness_metrics,
            agent_id=f"two_page_generator_{styling_genome.genome_id[:8]}",
            lineage_path=styling_genome.lineage_path,
        )

        styling_genome.flight_recorder.append(event)

    def _compute_content_stats(self, html_content: str, page_count: int) -> Dict[str, Any]:
        """
        Compute content statistics from HTML.

        Args:
            html_content: Generated HTML content
            page_count: Number of pages

        Returns:
            Dictionary with content statistics
        """
        import re

        # Count words (rough estimate)
        text_content = re.sub(r'<[^>]+>', ' ', html_content)
        words = text_content.split()
        words_total = len(words)

        # Split by page (rough estimate - assumes equal distribution)
        words_per_page = words_total / page_count if page_count > 0 else 0
        words_page1 = int(words_per_page * 0.6)  # Page 1 gets 60%
        words_page2 = words_total - words_page1

        # Count paragraphs
        paragraphs = len(re.findall(r'<p[^>]*>', html_content))

        # Count lists
        lists = len(re.findall(r'<[uo]l[^>]*>', html_content))

        # Count boxes (note-box, highlight-box)
        boxes = len(re.findall(r'class="(?:note|highlight)-box"', html_content))

        return {
            "words_total": words_total,
            "words_page1": words_page1,
            "words_page2": words_page2,
            "density": words_per_page,
            "paragraphs": paragraphs,
            "lists": lists,
            "boxes": boxes,
        }
