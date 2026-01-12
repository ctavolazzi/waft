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
from .document_components import (
    DocumentComponent, DocumentLayout, ComponentType,
    ComponentBuilder, LayoutAlgorithm
)
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

        /* Ideas - prose presentation with varied formatting */
        .idea {
            margin-bottom: {{ margin.paragraph_spacing * 1.2 }}pt;
            padding: {{ margin.paragraph_spacing * 0.8 }}pt 0;
            page-break-inside: avoid;
        }

        /* Alternate between different visual styles */
        .idea:nth-child(odd) {
            padding-left: {{ margin.paragraph_spacing }}pt;
            border-left: 2pt solid {{ color.accent }};
            background: {{ color.code_bg }}10;
        }

        .idea:nth-child(even) {
            padding-left: 0;
            border-left: none;
            background: transparent;
            border-top: 1pt solid {{ color.text }}20;
            padding-top: {{ margin.paragraph_spacing * 0.6 }}pt;
            margin-top: {{ margin.paragraph_spacing * 0.4 }}pt;
        }

        .idea:nth-child(3n) {
            padding-left: 0;
            border-left: none;
            background: {{ color.code_bg }}08;
            border-radius: 3pt;
            padding: {{ margin.paragraph_spacing * 0.6 }}pt;
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

    def __init__(self, weasyprint_available: bool = False, max_iterations: int = 5, allowed_pages: int = 2):
        """
        Initialize generator.

        Args:
            weasyprint_available: Whether WeasyPrint is available
            max_iterations: Max attempts to achieve target pages
            allowed_pages: Target page count (default: 2, can be any number)
        """
        self.weasyprint_available = weasyprint_available
        self.max_iterations = max_iterations
        self.allowed_pages = allowed_pages  # Configurable page count

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
        target_pages: Optional[int] = None,
        convert_to_png: bool = False,
        png_dpi: int = 300,
        collect_metrics: bool = False,
        metrics_dir: Optional[Path] = None,
        use_component_system: bool = True,
    ) -> Dict[str, Any]:
        """
        Generate PDF with configurable page constraint and component-based layout.

        Uses adaptive algorithm with component system:
        1. Build components from distilled content
        2. Generate multiple layout configurations
        3. Test each layout
        4. Learn what works
        5. Select best layout

        Args:
            distilled_chat: Distilled conversation
            styling_genome: Styling configuration
            output_path: Optional output path
            target_pages: Target page count (default: uses self.allowed_pages)
            convert_to_png: If True, automatically convert PDF to PNG images after generation (default: False)
            png_dpi: DPI for PNG conversion if convert_to_png is True (default: 300)
            use_component_system: Use new component-based system (default: True)

        Returns:
            Dictionary with results and accurate fitness metrics
        """
        # Use instance allowed_pages if target_pages not specified
        if target_pages is None:
            target_pages = self.allowed_pages

        print(f"\n🔬 TwoPageGenerator: Adaptive generation for {target_pages} pages")

        # Use component system if enabled
        if use_component_system:
            return self._generate_with_components(
                distilled_chat=distilled_chat,
                styling_genome=styling_genome,
                output_path=output_path,
                target_pages=target_pages,
                convert_to_png=convert_to_png,
                png_dpi=png_dpi,
                collect_metrics=collect_metrics,
                metrics_dir=metrics_dir,
            )

        # Fall back to original algorithm
        return self._generate_legacy(
            distilled_chat=distilled_chat,
            styling_genome=styling_genome,
            output_path=output_path,
            target_pages=target_pages,
            convert_to_png=convert_to_png,
            png_dpi=png_dpi,
            collect_metrics=collect_metrics,
            metrics_dir=metrics_dir,
        )

    def _generate_with_components(
        self,
        distilled_chat: DistilledChat,
        styling_genome: StylingGenome,
        output_path: Optional[Path],
        target_pages: int,
        convert_to_png: bool,
        png_dpi: int,
        collect_metrics: bool,
        metrics_dir: Optional[Path],
    ) -> Dict[str, Any]:
        """Generate using component-based system."""
        from datetime import datetime

        builder = ComponentBuilder()
        algorithm = LayoutAlgorithm(allowed_pages=target_pages)

        # Build components from content
        components = []

        # 1. Title component
        components.append(builder.build_title_component(distilled_chat.title))

        # 2. Image component (if available)
        images_dir = Path(__file__).parent.parent.parent / "_work_efforts" / "one_pagers" / "images"
        three_pillars_path = images_dir / "three_pillars.png"
        if three_pillars_path.exists():
            def to_file_url(path: Path) -> str:
                return path.absolute().as_uri()
            components.append(builder.build_image_component(
                to_file_url(three_pillars_path),
                "Figure 1: The Three Pillars of WAFT Architecture"
            ))

        # 3. Abstract component
        components.append(builder.build_abstract_component(distilled_chat.summary))

        # 4. Attribution component
        components.append(builder.build_attribution_component(
            "WAFT Research Team",
            datetime.utcnow().strftime("%Y-%m-%d")
        ))

        # 5. Section components from ideas
        all_ideas = distilled_chat.get_top_ideas(n=50, min_importance=0.1)

        # Group ideas into sections intelligently
        # Try to find pillar-related ideas
        substrate_ideas = [idea for idea in all_ideas if 'substrate' in idea.content.lower() or 'code is dna' in idea.content.lower()][:1]
        physics_ideas = [idea for idea in all_ideas if 'scint' in idea.content.lower() or 'physics' in idea.content.lower() or 'fitness' in idea.content.lower()][:1]
        flight_recorder_ideas = [idea for idea in all_ideas if 'flight recorder' in idea.content.lower() or 'lineage' in idea.content.lower() or 'phylogenetic' in idea.content.lower()][:1]

        # Build sections
        if all_ideas:
            components.append(builder.build_section_component("Introduction", all_ideas[:1], level=2))

        if substrate_ideas or physics_ideas or flight_recorder_ideas:
            # Architecture section with pillars
            components.append(builder.build_section_component("Architecture", [], level=2))

            if substrate_ideas:
                components.append(builder.build_section_component("The Substrate", substrate_ideas, level=3))
            if physics_ideas:
                components.append(builder.build_section_component("The Physics", physics_ideas, level=3))
            if flight_recorder_ideas:
                components.append(builder.build_section_component("The Flight Recorder", flight_recorder_ideas, level=3))

        # Methodology and conclusion from remaining ideas
        remaining_ideas = [idea for idea in all_ideas[1:] if idea not in substrate_ideas + physics_ideas + flight_recorder_ideas]
        if remaining_ideas:
            split = len(remaining_ideas) // 2
            if split > 0:
                components.append(builder.build_section_component("Methodology", remaining_ideas[:split], level=2))
            if len(remaining_ideas) > split:
                components.append(builder.build_section_component("Conclusion", remaining_ideas[split:], level=2))

        # Generate layout configurations
        print(f"  Building {len(components)} components...")
        layouts = algorithm.generate_layouts(components, max_attempts=self.max_iterations)
        print(f"  Generated {len(layouts)} layout configurations to test")

        # Test each layout
        best_layout = None
        best_fitness = 0.0

        for i, layout in enumerate(layouts):
            print(f"  Testing layout {i+1}/{len(layouts)} ({layout.metadata.get('strategy', 'unknown')})...")

            # Render HTML from layout
            html_content = self._render_html_from_layout(
                layout=layout,
                distilled_chat=distilled_chat,
                styling_genome=styling_genome,
            )

            # Count pages
            page_count = self._count_pages(html_content, output_path)

            # Test and learn
            learning_data = algorithm.test_layout(layout, page_count)
            print(f"    → {page_count} pages, fitness: {learning_data['fitness']:.3f}")

            if learning_data['fitness'] > best_fitness:
                best_fitness = learning_data['fitness']
                best_layout = layout
                best_layout.metadata['html_content'] = html_content

        if best_layout is None:
            raise RuntimeError("Failed to generate any valid layout")

        print(f"  ✓ Best layout: {best_layout.metadata.get('strategy')}, fitness: {best_fitness:.3f}")

        # Get learning summary
        learning_summary = algorithm.get_learning_summary()
        print(f"  Learning: {learning_summary['successful']}/{learning_summary['total_tests']} successful")

        # Save output
        pdf_path = None
        if output_path and best_layout.metadata.get('html_content'):
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Save HTML
            html_path = Path(str(output_path).replace('.pdf', '.html'))
            html_path.write_text(best_layout.metadata['html_content'])
            print(f"  ✓ HTML saved: {html_path}")

            # Generate PDF
            if self.weasyprint_available:
                self.HTML(string=best_layout.metadata['html_content']).write_pdf(output_path)
                pdf_path = str(output_path)
                print(f"  ✓ PDF saved: {output_path}")

        # Count ideas shown
        ideas_shown = 0
        for comp in best_layout.components:
            if comp.component_type == ComponentType.SECTION:
                ideas_shown += comp.metadata.get('idea_count', 0)

        # Evaluate fitness
        fitness_metrics = self._evaluate_fitness(
            distilled_chat=distilled_chat,
            ideas_shown=ideas_shown,
            styling_genome=styling_genome,
            page_count=best_layout.page_count or target_pages,
            target_pages=target_pages,
        )

        return {
            'success': True,
            'pdf_path': pdf_path,
            'html_path': str(html_path) if output_path else None,
            'page_count': best_layout.page_count,
            'target_pages': target_pages,
            'fitness': fitness_metrics,
            'layout': best_layout,
            'learning_summary': learning_summary,
        }

    def _generate_legacy(
        self,
        distilled_chat: DistilledChat,
        styling_genome: StylingGenome,
        output_path: Optional[Path],
        target_pages: int,
        convert_to_png: bool,
        png_dpi: int,
        collect_metrics: bool,
        metrics_dir: Optional[Path],
    ) -> Dict[str, Any]:
        """Original generation algorithm (fallback)."""
        # Original implementation continues here...
        print(f"  Using legacy algorithm...")

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

    def _render_html_from_layout(
        self,
        layout: DocumentLayout,
        distilled_chat: DistilledChat,
        styling_genome: StylingGenome,
        custom_template: Optional[str] = None,
    ) -> str:
        """Render HTML from a component-based layout."""
        from jinja2 import Template

        # Build science paper template structure
        styling_dict = {
            'font': styling_genome.genes.font.to_dict(),
            'margin': styling_genome.genes.margin.to_dict(),
            'color': styling_genome.genes.color.to_dict(),
        }

        # Render components in order
        component_htmls = []
        for comp in layout.components:
            html = comp.to_html(styling_dict)
            if html:  # Only add non-empty components
                component_htmls.append(html)

        # Use custom template if provided, otherwise use default science paper template
        if custom_template:
            template_str = custom_template
        else:
            # Default science paper template
            template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
    <style>
        @page {
            size: letter;
            margin: {{ margin.top }}mm {{ margin.right }}mm {{ margin.bottom }}mm {{ margin.left }}mm;
            @top-right {
                content: "Page " counter(page);
                font-family: "Helvetica Neue", "Arial", sans-serif;
                font-size: {{ font.size_body - 2 }}pt;
                color: {{ color.text }};
                opacity: 0.6;
            }
        }
        @page :first {
            @top-right { content: none; }
        }
        body {
            font-family: {{ font.family }};
            font-size: {{ font.size_body }}pt;
            line-height: {{ font.line_height }};
            color: {{ color.text }};
            background: {{ color.background }};
        }
        h1 {
            font-family: "Helvetica Neue", "Arial", sans-serif;
            font-size: {{ font.size_h1 }}pt;
            text-align: center;
            margin-bottom: {{ margin.paragraph_spacing }}pt;
        }
        .abstract {
            background: {{ color.code_bg }};
            border-left: 3pt solid {{ color.border }};
            padding: {{ margin.paragraph_spacing }}pt;
            margin: {{ margin.paragraph_spacing }}pt 0;
        }
        .abstract-title {
            font-family: "Helvetica Neue", "Arial", sans-serif;
            font-weight: 700;
            font-size: {{ font.size_h3 }}pt;
            margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;
            text-transform: uppercase;
        }
        .author-info {
            font-size: {{ font.size_body - 1 }}pt;
            text-align: center;
            margin: {{ margin.paragraph_spacing }}pt 0;
            opacity: 0.7;
        }
        .diagram {
            text-align: center;
            margin: {{ margin.paragraph_spacing }}pt 0;
        }
        .diagram img {
            max-width: 60%;
            max-height: 80pt;
            height: auto;
            border: 0.5pt solid {{ color.border }};
        }
        .figure-caption {
            font-size: {{ font.size_body - 1.5 }}pt;
            font-style: italic;
            text-align: center;
            margin-top: 3pt;
        }
        h2 {
            font-family: "Helvetica Neue", "Arial", sans-serif;
            font-size: {{ font.size_h2 }}pt;
            font-weight: 600;
            margin-top: {{ margin.section_spacing }}pt;
            margin-bottom: {{ margin.paragraph_spacing }}pt;
        }
        h2::before {
            counter-increment: section;
            content: counter(section) ". ";
        }
        body {
            counter-reset: section;
        }
        p {
            margin: 0 0 {{ margin.paragraph_spacing }}pt 0;
            text-align: justify;
        }
        .pillar {
            border-left: 4pt solid {{ color.border }};
            padding: {{ margin.paragraph_spacing }}pt;
            margin: {{ margin.paragraph_spacing }}pt 0;
        }
        .pillar-title {
            font-family: "Helvetica Neue", "Arial", sans-serif;
            font-weight: 700;
            font-size: {{ font.size_h3 }}pt;
            margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;
            text-transform: uppercase;
        }
        .pillar-body {
            margin-top: {{ margin.paragraph_spacing / 2 }}pt;
        }
        /* Status Components Styling */
        .status-section {
            margin: {{ margin.section_spacing }}pt 0;
        }
        .status-body {
            margin-top: {{ margin.paragraph_spacing / 2 }}pt;
        }
        .epistemic-state {
            background: {{ color.code_bg }};
            border-left: 3pt solid {{ color.accent }};
            padding: {{ margin.paragraph_spacing }}pt;
            margin: {{ margin.paragraph_spacing }}pt 0;
        }
        .moon-phase {
            display: flex;
            align-items: center;
            gap: 8pt;
            margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;
        }
        .moon-emoji {
            font-size: {{ font.size_h2 }}pt;
        }
        .moon-desc {
            font-weight: 600;
            color: {{ color.text }};
        }
        .epistemic-phase {
            text-align: center;
            margin: {{ margin.paragraph_spacing }}pt 0;
        }
        .phase-badge {
            display: inline-block;
            padding: 6pt 12pt;
            background: {{ color.accent }};
            color: {{ color.background }};
            font-weight: 700;
            font-size: {{ font.size_h3 }}pt;
            border-radius: 4pt;
            margin: 0;
        }
        /* Table Styling */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: {{ margin.paragraph_spacing }}pt 0;
            font-size: {{ font.size_body }}pt;
        }
        table th {
            background: {{ color.code_bg }};
            font-family: "Helvetica Neue", "Arial", sans-serif;
            font-weight: 600;
            padding: 6pt 8pt;
            text-align: left;
            border-bottom: 2pt solid {{ color.border }};
        }
        table td {
            padding: 6pt 8pt;
            border-bottom: 1pt solid {{ color.border }};
        }
        table tr:last-child td {
            border-bottom: none;
        }
        .gamification-table, .health-table, .metrics-table, .grouped-metrics-table {
            font-size: {{ font.size_body - 1 }}pt;
        }
        .flight-events {
            list-style: none;
            padding-left: 0;
        }
        .flight-events li {
            margin: 4pt 0;
            padding-left: 12pt;
            text-indent: -12pt;
        }
        .flight-events li::before {
            content: "▸ ";
            color: {{ color.accent }};
            font-weight: bold;
        }
        
        /* Progress Bar (inspired by AI-DnD quest progress) */
        .progress-container {
            margin: {{ margin.paragraph_spacing }}pt 0;
        }
        .progress-label {
            font-size: {{ font.size_body }}pt;
            font-weight: bold;
            margin-bottom: 4pt;
            color: {{ color.text }};
        }
        .progress-bar {
            width: 100%;
            height: 10pt;
            background: {{ color.code_bg }};
            border-radius: 5pt;
            overflow: hidden;
            border: 1pt solid {{ color.text }}20;
        }
        .progress-fill {
            height: 100%;
            background: {{ color.accent }};
            transition: width 0.3s;
            border-radius: 5pt;
        }
        .progress-text {
            font-size: {{ font.size_body - 1 }}pt;
            color: {{ color.text }}88;
            margin-top: 2pt;
            text-align: right;
        }
        
        /* Status Badges (inspired by AI-DnD status effects) */
        .status-badges {
            display: flex;
            flex-wrap: wrap;
            gap: 4pt;
            margin: {{ margin.paragraph_spacing / 2 }}pt 0;
        }
        .status-badge {
            padding: 3pt 8pt;
            border-radius: 4pt;
            font-size: {{ font.size_body - 1 }}pt;
            display: inline-block;
            border: 1pt solid;
            white-space: nowrap;
        }
        .status-badge.status-good {
            background: #e8f5e9;
            color: #2e7d32;
            border-color: #4caf50;
        }
        .status-badge.status-warning {
            background: #fff3e0;
            color: #e65100;
            border-color: #ff9800;
        }
        .status-badge.status-error {
            background: #ffebee;
            color: #c62828;
            border-color: #f44336;
        }
        .status-badge.status-info {
            background: {{ color.code_bg }};
            color: {{ color.text }};
            border-color: {{ color.accent }};
        }
        
        /* Grouped Metrics (inspired by AI-DnD inventory display) */
        .metrics-group {
            margin: {{ margin.paragraph_spacing }}pt 0;
        }
        .group-description {
            font-size: {{ font.size_body - 1 }}pt;
            color: {{ color.text }}88;
            margin-bottom: 6pt;
            font-style: italic;
        }
        .grouped-metrics-table {
            width: 100%;
            border-collapse: collapse;
            font-size: {{ font.size_body - 1 }}pt;
        }
        .grouped-metrics-table td {
            padding: 6pt 8pt;
            border-bottom: 1pt solid {{ color.text }}20;
        }
        .grouped-metrics-table tr:last-child td {
            border-bottom: none;
        }
        .grouped-metrics-table .metric-label {
            font-weight: 500;
            color: {{ color.text }};
            width: 60%;
        }
        .grouped-metrics-table .metric-value {
            text-align: right;
            font-weight: 600;
            color: {{ color.text }};
        }
        .grouped-metrics-table .metric-value.status-good {
            color: #2e7d32;
        }
        .grouped-metrics-table .metric-value.status-warning {
            color: #e65100;
        }
        .grouped-metrics-table .metric-value.status-error {
            color: #c62828;
        }
        .grouped-metrics-table .metric-value.status-info {
            color: {{ color.accent }};
        }
        .grouped-metrics-table .metric-unit {
            font-size: {{ font.size_body - 2 }}pt;
            color: {{ color.text }}88;
            font-weight: normal;
            margin-left: 2pt;
        }
        
        /* Git Summary & Work Efforts Summary */
        .git-summary, .work-efforts-summary {
            margin: {{ margin.paragraph_spacing }}pt 0;
        }
    </style>
</head>
<body>
    {% for component_html in components %}
    {{ component_html }}
    {% endfor %}
</body>
</html>
"""

        context = {
            'title': distilled_chat.title,
            'components': component_htmls,
            **styling_dict,
        }

        template = Template(template_str)
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
