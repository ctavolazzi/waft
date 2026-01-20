#!/usr/bin/env python3
"""
Generate WAFT Introduction One-Pager Handout
=============================================

Creates a beautiful 2-page PDF handout that introduces WAFT to first-time learners,
showcasing the visual features of the TwoPageGenerator system including visual boxes,
tables, typography, and adaptive content selection.
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Any

from jinja2 import Template
from weasyprint import HTML

from src.waft.evolution import (
    ChatDistiller,
    ColorGene,
    DistilledChat,
    FontGene,
    IdeaGene,
    LayoutGene,
    MarginGene,
    StylingGene,
    StylingGenome,
    StylingGenomeRegistry,
    TwoPageGenerator,
)


def get_waft_explanation_content() -> str:
    """
    WAFT explanation content structured as prose for ChatDistiller.

    Written as natural paragraphs that explain WAFT to newcomers,
    covering all key concepts in a beginner-friendly way.
    """
    return """
# WAFT: The Evolutionary Code Laboratory

## What is WAFT?

WAFT is a Python framework for directed evolution of self-modifying AI agents. Think of it as an operating system for AI agent research projects. Instead of just building agents that execute code, WAFT enables you to breed agents that can modify their own code, evolve through mutations, and be tested in fitness systems with complete lineage tracking for scientific research.

## The Core Promise

Don't just build agents. Breed them. WAFT transforms AI agents from passive assistants into active project participants that can improve themselves and the projects they work on. The ultimate goal is to observe a God-Head agent emerge from thousands of generations of directed mutation and selection.

## The Three Pillars

The Substrate represents agents that write their own Python source code. In WAFT, code is DNA. Each agent has a unique genome ID which is a SHA-256 hash of their code and configuration. Agents can spawn variants with mutations, evolve by hot-swapping their own code, and reproduce by creating children with specific genetic modifications. This enables true self-modification where agents can improve themselves.

The Physics is the Scint System, which acts as a fitness function through Reality Fracture Detection. This system serves as natural selection that kills weak mutations. Agents face quests that test their ability to handle four types of errors: SYNTAX_TEAR for formatting errors, LOGIC_FRACTURE for math errors and contradictions, SAFETY_VOID for harmful content, and HALLUCINATION for fabricated facts. Agents must stabilize these errors to survive, and fitness is measured by stability, efficiency, and safety scores.

The Flight Recorder is a rigorous telemetry system for generating phylogenetic trees of agent lineage. Every evolutionary action is recorded with complete context including genome ID, parent ID, generation number, event type, payload with complete context, and fitness metrics. This enables reconstruction of complete family trees for scientific publication, allowing phylogenetic analysis, mutation impact measurement, fitness landscape mapping, and convergence analysis.

## Key Characteristics

WAFT is scientific because it produces rigorous data for research publication on the physics of artificial cognition. It is evolutionary because agents evolve through genetic improvement, not just execution. It is observable because every action is recorded in the Flight Recorder for analysis. It is directed because evolution is guided by fitness functions, not random mutation.

## How It Works

WAFT provides project scaffolding through a unified CLI interface. You run one command to create a fully configured project with best practices built in. The system uses uv for fast Python package management, creates a _pyrite memory structure for organizing project knowledge, includes CI/CD pipelines ready to go, and provides optional AI agent templates. Everything is file-based with no database, no server, just plain text files that work with git.

## Quick Start

Install WAFT using uv tool install waft. Create a new evolutionary laboratory with waft new my_laboratory. Verify the substrate with waft verify. The system sets up everything you need including project structure, dependencies, CI/CD, and documentation templates. You can then spawn variants with mutations, evaluate fitness in the Gym, and evolve into the fittest variant.

## What Makes It Unique

WAFT is ambient, working quietly in the background without getting in your way. It is self-modifying, allowing projects to evolve their own structure over time. It is a meta-framework that orchestrates existing tools rather than replacing them. Everything is file-based, making it git-friendly and portable. The system includes gamification with D&D-style progression, epistemic tracking to know what you know and don't know, and scientific observation with complete lineage tracking.

## The Scientific Mission

WAFT is built to produce data for a future book or paper on the Physics of Artificial Cognition. The system is designed to track complete evolutionary lineages as phylogenetic trees, measure fitness through rigorous testing in the Scint Gym, record all mutations with complete context in the Flight Recorder, and enable scientific analysis of agent evolution patterns. This makes WAFT not just a framework but a scientific instrument.

## Project Structure

A WAFT laboratory includes pyproject.toml for uv project configuration, uv.lock for locked dependencies, a _pyrite directory for the memory system with active, backlog, and standards folders, GitHub Actions workflows for CI/CD pipelines, a Justfile for task running, and source code organized in a standard Python project structure. Everything is designed to be file-based and git-friendly.

## Commands Overview

The waft new command creates a new evolutionary laboratory with all necessary structure. The waft verify command verifies the project structure is correct. The waft evolve command runs the evolutionary cycle for a target agent, spawning variants, evaluating fitness, and selecting the fittest. The waft sync command syncs project dependencies. The waft add command adds dependencies to the project. The waft info command shows information about the WAFT project. The waft serve command starts a web dashboard for visualization.

## Philosophy

WAFT doesn't lock you in. It's all file-based with no database to manage. Everything is plain text that works with git out of the box. You can modify anything because it's your project, and WAFT just set it up. The system is designed to be ambient, setting things up and getting out of your way so you can focus on building agents rather than configuring infrastructure.

## Resources

The WAFT repository is available on GitHub for exploration and contribution. Comprehensive documentation covers the AI SDK vision, agent interface design, evolutionary architecture, and state of the art research. The system is MIT licensed and actively developed. You can start with the quick start guide, explore examples, read the documentation, and join the community to learn more about breeding AI agents.
"""


class EnhancedWAFTGenerator(TwoPageGenerator):
    """
    Enhanced generator with prettier template using visual boxes.

    Uses pillar boxes, highlight boxes, and note boxes to showcase
    WAFT's visual features more prominently.
    """

    # Enhanced template with visual boxes
    ENHANCED_TEMPLATE = """
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
        p, li { orphans: 2; widows: 2; }
        .page-break { page-break-after: always; break-after: page; }
        .no-break { page-break-inside: avoid; break-inside: avoid; }
        h1 {
            font-size: {{ font.size_h1 }}pt;
            color: {{ color.heading }};
            margin-top: 0;
            margin-bottom: {{ margin.section_spacing }}pt;
            page-break-after: avoid;
            border-bottom: 3pt solid {{ color.accent }};
            padding-bottom: 6pt;
        }
        h2 {
            font-size: {{ font.size_h2 }}pt;
            color: {{ color.heading }};
            margin-top: {{ margin.section_spacing }}pt;
            margin-bottom: {{ margin.paragraph_spacing }}pt;
            page-break-after: avoid;
            border-bottom: 2pt solid {{ color.accent }};
            padding-bottom: 3pt;
        }
        h3 {
            font-size: {{ font.size_h3 }}pt;
            color: {{ color.heading }};
            margin-top: {{ margin.paragraph_spacing }}pt;
            margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;
            page-break-after: avoid;
        }
        p { margin: 0 0 {{ margin.paragraph_spacing }}pt 0; }
        ul, ol { margin: 0 0 {{ margin.paragraph_spacing }}pt 0; padding-left: 15pt; }
        li { margin-bottom: {{ margin.paragraph_spacing / 3 }}pt; }
        .summary-box {
            background: {{ color.code_bg }};
            padding: {{ margin.paragraph_spacing }}pt;
            margin-bottom: {{ margin.section_spacing }}pt;
            border-left: 5pt solid {{ color.accent }};
            border-top: 2pt solid {{ color.accent }};
            border-right: 2pt solid {{ color.accent }};
            border-bottom: 2pt solid {{ color.accent }};
            page-break-inside: avoid;
        }
        .pillar {
            border: 2pt solid {{ color.accent }};
            background: {{ color.background }};
            padding: {{ margin.paragraph_spacing / 1.5 }}pt;
            margin: {{ margin.paragraph_spacing / 1.5 }}pt 0;
            page-break-inside: avoid;
            border-radius: 3pt;
        }
        .pillar-title {
            font-weight: bold;
            color: {{ color.accent }};
            font-size: {{ font.size_h3 - 1 }}pt;
            margin-bottom: {{ margin.paragraph_spacing / 3 }}pt;
            text-transform: uppercase;
            letter-spacing: 0.3pt;
        }
        .pillar p {
            margin: 0;
            font-size: {{ font.size_body - 0.5 }}pt;
            line-height: 1.4;
        }
        .highlight-box {
            border: 2pt solid {{ color.accent }};
            background: {{ color.code_bg }};
            padding: {{ margin.paragraph_spacing }}pt;
            margin: {{ margin.paragraph_spacing }}pt 0;
            page-break-inside: avoid;
            border-radius: 3pt;
        }
        .note-box {
            border-left: 5pt solid {{ color.accent }};
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
        .idea {
            margin-bottom: {{ margin.paragraph_spacing }}pt;
            padding: {{ margin.paragraph_spacing }}pt;
            border-left: 3pt solid {{ color.accent }};
            background: {{ color.code_bg }}20;
            page-break-inside: avoid;
        }
        .idea-content {
            font-size: {{ font.size_body }}pt;
            line-height: 1.6;
            text-align: justify;
            margin: 0;
        }
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
            padding: 6pt;
            text-align: left;
            font-weight: bold;
        }
        td {
            border: 1pt solid {{ color.text }}33;
            padding: 6pt;
        }
        tr:nth-child(even) { background: {{ color.code_bg }}; }
        .metadata {
            font-size: {{ font.size_body - 2 }}pt;
            color: {{ color.text }}88;
            line-height: 1.3;
            border-top: 1pt solid {{ color.text }}33;
            padding-top: {{ margin.paragraph_spacing / 2 }}pt;
            margin-top: {{ margin.paragraph_spacing }}pt;
        }
        .divider {
            border-top: 2pt solid {{ color.accent }};
            margin: {{ margin.paragraph_spacing }}pt 0;
        }
        code {
            font-family: monospace;
            font-size: {{ font.size_code }}pt;
            background: {{ color.code_bg }};
            color: {{ color.code_text }};
            padding: 2pt 4pt;
            border-radius: 2pt;
        }
    </style>
</head>
<body>
    <div class="page-1">
        <h1>{{ title }}</h1>
        <div class="summary-box">
            <strong>Summary:</strong> {{ summary }}
        </div>
        <div class="metadata">
            <p><strong>Generated:</strong> {{ generated_at }} | <strong>Ideas:</strong> {{ total_ideas }}</p>
        </div>
        <h2>What is WAFT?</h2>
        {% if page_1_ideas|length > 0 %}
        <div class="idea no-break">
            <p class="idea-content">{{ page_1_ideas[0].content[:300] }}{% if page_1_ideas[0].content|length > 300 %}...{% endif %}</p>
        </div>
        {% endif %}
        <h2>The Three Pillars</h2>
        {% if page_1_ideas|length > 1 %}
        <div class="pillar no-break">
            <div class="pillar-title">The Substrate</div>
            <p>{{ page_1_ideas[1].content[:200] }}{% if page_1_ideas[1].content|length > 200 %}...{% endif %}</p>
        </div>
        {% endif %}
        {% if page_1_ideas|length > 2 %}
        <div class="pillar no-break">
            <div class="pillar-title">The Physics</div>
            <p>{{ page_1_ideas[2].content[:200] }}{% if page_1_ideas[2].content|length > 200 %}...{% endif %}</p>
        </div>
        {% endif %}
        {% if page_1_ideas|length > 3 %}
        <div class="pillar no-break">
            <div class="pillar-title">The Flight Recorder</div>
            <p>{{ page_1_ideas[3].content[:200] }}{% if page_1_ideas[3].content|length > 200 %}...{% endif %}</p>
        </div>
        {% endif %}
    </div>
    <div class="page-break"></div>
    <div class="page-2">
        <h2>How It Works</h2>
        {% if page_2_ideas|length > 0 %}
        <div class="idea no-break">
            <p class="idea-content">{{ page_2_ideas[0].content[:250] }}{% if page_2_ideas[0].content|length > 250 %}...{% endif %}</p>
        </div>
        {% endif %}
        <div class="note-box no-break">
            <div class="note-title">Quick Start</div>
            <p style="margin: 0; font-size: {{ font.size_body - 0.5 }}pt;">Install: <code>uv tool install waft</code> | Create: <code>waft new my_lab</code> | Verify: <code>waft verify</code></p>
        </div>
        {% if page_2_ideas|length > 1 %}
        <div class="highlight-box no-break">
            <p style="margin: 0; font-size: {{ font.size_body - 0.5 }}pt;"><strong>Unique:</strong> {{ page_2_ideas[1].content[:180] }}{% if page_2_ideas[1].content|length > 180 %}...{% endif %}</p>
        </div>
        {% endif %}
        <div class="divider"></div>
        <div class="metrics">
            <h3>Content Breakdown</h3>
            <table>
                <tr><th>Type</th><th>Count</th></tr>
                <tr><td>Decisions</td><td>{{ metrics.decisions }}</td></tr>
                <tr><td>Insights</td><td>{{ metrics.insights }}</td></tr>
                <tr><td>Actions</td><td>{{ metrics.actions }}</td></tr>
                <tr><td>Concepts</td><td>{{ metrics.concepts }}</td></tr>
                <tr><td>Questions</td><td>{{ metrics.questions }}</td></tr>
            </table>
        </div>
    </div>
</body>
</html>
"""

    def _render_html(
        self,
        distilled_chat: DistilledChat,
        styling_genome: StylingGenome,
        page_1_ideas: list[IdeaGene],
        page_2_ideas: list[IdeaGene],
    ) -> str:
        """Render enhanced HTML template with visual boxes."""

        def clean_idea(idea: IdeaGene) -> dict[str, Any]:
            idea_dict = idea.to_dict()
            idea_dict["content"] = self._clean_markdown(idea_dict.get("content", ""))
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
            "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        }

        template = Template(self.ENHANCED_TEMPLATE)
        return template.render(**context)


def main():
    """Generate WAFT introduction one-pager handout."""
    print("🔬 Creating WAFT Introduction One-Pager Handout...")
    print()

    # Get WAFT explanation content
    print("📝 Preparing WAFT explanation content...")
    content = get_waft_explanation_content()

    # Distill content into ideas
    print("📝 Distilling content into ideas...")
    distiller = ChatDistiller()
    distilled = distiller.distill_text(content, title="WAFT: The Evolutionary Code Laboratory")

    print(f"✓ Extracted {distilled.total_ideas} ideas")
    print(f"  - Concepts: {distilled.concepts_count}")
    print(f"  - Actions: {distilled.actions_count}")
    print(f"  - Decisions: {distilled.decisions_count}")
    print(f"  - Insights: {distilled.insights_count}")
    print(f"  - Questions: {distilled.questions_count}")
    print()

    # Create professional styling genome
    print("🎨 Creating professional styling genome...")
    registry = StylingGenomeRegistry(registry_dir=Path("_genetics/waft_intro_handouts"))

    # Create professional genome optimized for handouts
    professional_genes = StylingGene(
        font=FontGene(
            family="sans-serif",
            size_body=11,
            size_h1=24,
            size_h2=18,
            size_h3=14,
            size_code=10,
            line_height=1.55,
        ),
        margin=MarginGene(
            top=20,
            bottom=20,
            left=20,
            right=20,
            paragraph_spacing=10,
            section_spacing=15,
        ),
        color=ColorGene(
            text="#000000",
            background="#FFFFFF",
            heading="#1a1a1a",
            accent="#0066cc",  # Professional blue accent
            code_bg="#f5f5f5",
            code_text="#333333",
            border="#cccccc",
        ),
        layout=LayoutGene(
            columns=1,
            density="normal",
            toc_enabled=False,
            page_numbers=True,
            header_enabled=True,
            footer_enabled=True,
        ),
        name="WAFT Intro Handout Professional",
    )
    genome = StylingGenome.from_genes(professional_genes)
    registry.register(genome)
    print(f"✓ Using: {genome.scientific_name} ({genome.genome_id[:8]}...)")
    print()

    # Generate with enhanced generator
    print("📄 Generating 2-page PDF with enhanced visual features...")
    generator = EnhancedWAFTGenerator(weasyprint_available=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(f"_work_efforts/one_pagers/WAFT_Intro_Handout_Enhanced_{timestamp}.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Get top ideas for pages - optimized for 2 pages with visual boxes
    all_ideas = distilled.get_top_ideas(n=10, min_importance=0.3)

    # Use adaptive selection similar to parent class
    best_result = None
    best_page_diff = float("inf")
    ideas_to_show = 5

    for _iteration in range(5):
        split_point = min(4, ideas_to_show)
        page_1_ideas = all_ideas[:split_point]
        page_2_ideas = all_ideas[split_point:ideas_to_show]

        # Render and count pages
        html_content = generator._render_html(distilled, genome, page_1_ideas, page_2_ideas)

        # Generate temp PDF to count pages
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        HTML(string=html_content).write_pdf(str(tmp_path))

        from pypdf import PdfReader

        reader = PdfReader(str(tmp_path))
        page_count = len(reader.pages)
        tmp_path.unlink()

        page_diff = abs(page_count - 2)
        if page_diff < best_page_diff:
            best_page_diff = page_diff
            best_result = (page_1_ideas, page_2_ideas, page_count)

        if page_count == 2:
            break

        # Adjust for next iteration
        if page_count > 2:
            ideas_to_show = max(3, ideas_to_show - 1)
        else:
            ideas_to_show = min(len(all_ideas), ideas_to_show + 1)

    if best_result:
        page_1_ideas, page_2_ideas, page_count = best_result
    else:
        # Fallback: use very compact selection
        page_1_ideas = all_ideas[:4]
        page_2_ideas = all_ideas[4:6] if len(all_ideas) > 4 else []
        # Final render to get actual page count
        html_content = generator._render_html(distilled, genome, page_1_ideas, page_2_ideas)
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        HTML(string=html_content).write_pdf(str(tmp_path))
        from pypdf import PdfReader

        reader = PdfReader(str(tmp_path))
        page_count = len(reader.pages)
        tmp_path.unlink()

    # Render HTML
    html_content = generator._render_html(distilled, genome, page_1_ideas, page_2_ideas)

    # Save HTML
    html_path = output_path.with_suffix(".html")
    html_path.write_text(html_content)
    print(f"  ✓ HTML saved: {html_path}")

    # Generate PDF
    HTML(string=html_content).write_pdf(str(output_path))
    print(f"  ✓ PDF saved: {output_path}")

    # Count pages
    from pypdf import PdfReader

    reader = PdfReader(str(output_path))
    page_count = len(reader.pages)

    # Convert to PNG
    png_paths = []
    try:
        from src.waft.evolution.pdf_image_converter import convert_pdf_to_images

        png_dir = output_path.parent / f"{output_path.stem}_pages"
        png_paths = convert_pdf_to_images(output_path, output_dir=png_dir, dpi=300)
        print(f"  ✓ Converted to {len(png_paths)} PNG images (DPI: 300)")
    except Exception as e:
        print(f"  ⚠️  PNG conversion failed: {e}")

    # Evaluate fitness
    fitness_metrics = generator._evaluate_fitness(
        distilled_chat=distilled,
        ideas_shown=len(page_1_ideas) + len(page_2_ideas),
        styling_genome=genome,
        page_count=page_count,
        target_pages=2,
    )

    result = {
        "success": True,
        "pdf_path": str(output_path),
        "html_content": html_content,
        "fitness_metrics": fitness_metrics,
        "ideas_shown": len(page_1_ideas) + len(page_2_ideas),
        "page_count": page_count,
        "target_pages": 2,
        "constraint_satisfied": page_count == 2,
        "png_paths": [str(p) for p in png_paths] if png_paths else None,
    }

    print()
    print("=" * 60)
    print("✅ WAFT Introduction One-Pager Created (Enhanced)!")
    print("=" * 60)
    print(f"📄 Output: {output_path}")
    print(f"📊 Pages: {result['page_count']}/2")
    print(f"🎯 Constraint satisfied: {result['constraint_satisfied']}")
    print(f"💪 Fitness: {result['fitness_metrics']['overall']:.3f}")
    print(f"   - Readability: {result['fitness_metrics']['readability']:.3f}")
    print(f"   - Completeness: {result['fitness_metrics']['completeness']:.3f}")
    print(f"   - Constraint: {result['fitness_metrics']['constraint_satisfaction']:.3f}")
    print(f"   - Aesthetics: {result['fitness_metrics']['aesthetic_appeal']:.3f}")
    print(f"🧬 Ideas shown: {result['ideas_shown']}/{distilled.total_ideas}")
    print("🎨 Visual features: Pillar boxes, Highlight boxes, Note boxes, Tables")

    # Show PNG info if generated
    if result.get("png_paths"):
        print(f"🖼️  PNG images: {len(result['png_paths'])} pages")
        for i, png_path in enumerate(result["png_paths"], 1):
            print(f"   - {Path(png_path).name} (page {i})")

    print()

    if result["constraint_satisfied"]:
        print("✅ Perfect 2-page handout with enhanced visuals!")
    else:
        print(f"⚠️ Generated {result['page_count']} pages (expected 2)")

    print()
    print("Ready for printing and distribution!")
    print()

    # Open the PDF
    try:
        import subprocess

        subprocess.run(["open", "-a", "Preview", str(output_path)])
        print("📖 PDF opened in Preview")
    except Exception:
        print(f"📖 PDF saved to: {output_path}")


if __name__ == "__main__":
    main()
