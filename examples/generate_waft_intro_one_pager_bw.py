#!/usr/bin/env python3
"""
Generate WAFT Introduction One-Pager - Black & White Edition
=============================================================

Creates a beautiful, printer-friendly black and white 2-page PDF handout
that introduces WAFT to first-time viewers. Uses only grayscale colors
(black, white, grays) for elegant, cost-effective printing.

Features:
- Comprehensive error handling and validation
- Cross-platform support
- CLI interface
- Logging and observability
- Beautiful grayscale design optimized for first-time viewers
"""

import sys
import argparse
import logging
import platform
import tempfile
import webbrowser
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
import traceback

sys.path.insert(0, str(Path(__file__).parent.parent))

# Import TwoPageGenerator early for class definition
try:
    from src.waft.evolution import TwoPageGenerator
except ImportError:
    # Will be imported later in generate_one_pager if needed
    TwoPageGenerator = None

# Version information
SCRIPT_VERSION = "1.0.0"
SCRIPT_NAME = "WAFT Intro One-Pager (Black & White)"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def check_dependencies() -> Dict[str, bool]:
    """
    Check for required dependencies.
    
    Returns:
        Dictionary with dependency names as keys and availability as values
    """
    dependencies = {
        'weasyprint': False,
        'pypdf': False,
        'jinja2': False,
    }
    
    # Check WeasyPrint
    try:
        from weasyprint import HTML, __version__
        dependencies['weasyprint'] = True
        logger.debug(f"WeasyPrint {__version__} available")
    except ImportError:
        logger.warning("WeasyPrint not available - PDF generation will fail")
    
    # Check pypdf
    try:
        from pypdf import PdfReader
        dependencies['pypdf'] = True
        logger.debug("pypdf available")
    except ImportError:
        logger.warning("pypdf not available - page counting will fail")
    
    # Check jinja2
    try:
        from jinja2 import Template
        dependencies['jinja2'] = True
        logger.debug("jinja2 available")
    except ImportError:
        logger.warning("jinja2 not available - template rendering will fail")
    
    return dependencies


def check_python_version() -> bool:
    """Check if Python version is 3.10 or higher."""
    import sys
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        logger.error(f"Python 3.10+ required, found {version.major}.{version.minor}")
        return False
    logger.debug(f"Python {version.major}.{version.minor}.{version.micro} OK")
    return True


def validate_content(content: str) -> tuple[bool, Optional[str]]:
    """
    Validate content for generation.
    
    Args:
        content: Content string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not content:
        return False, "Content is empty"
    
    if not isinstance(content, str):
        return False, "Content must be a string"
    
    # Check reasonable length (100-5000 words)
    word_count = len(content.split())
    if word_count < 100:
        logger.warning(f"Content is short ({word_count} words) - may not fill 2 pages")
    elif word_count > 5000:
        logger.warning(f"Content is very long ({word_count} words) - may not fit in 2 pages")
    
    return True, None


def validate_output_path(output_path: Path) -> tuple[bool, Optional[str]]:
    """
    Validate output path is writable.
    
    Args:
        output_path: Path to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Check parent directory exists or can be created
        parent = output_path.parent
        if not parent.exists():
            try:
                parent.mkdir(parents=True, exist_ok=True)
                logger.debug(f"Created output directory: {parent}")
            except (PermissionError, OSError) as e:
                return False, f"Cannot create output directory: {e}"
        
        # Check if parent is writable
        if not parent.is_dir():
            return False, f"Output path parent is not a directory: {parent}"
        
        # Try to create a test file
        test_file = parent / ".waft_test_write"
        try:
            test_file.write_text("test")
            test_file.unlink()
        except (PermissionError, OSError) as e:
            return False, f"Output directory is not writable: {e}"
        
        return True, None
    except Exception as e:
        return False, f"Error validating output path: {e}"


def validate_styling_parameters(font_sizes: Dict[str, int], margins: Dict[str, int]) -> tuple[bool, Optional[str]]:
    """
    Validate styling parameters are in reasonable ranges.
    
    Args:
        font_sizes: Dictionary of font size parameters
        margins: Dictionary of margin parameters
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Validate font sizes with different ranges for different elements
    size_ranges = {
        'body': (8, 14),
        'h1': (16, 32),  # Headers can be larger
        'h2': (12, 24),
        'h3': (10, 20),
        'code': (7, 12),
    }
    
    for name, size in font_sizes.items():
        if not isinstance(size, (int, float)):
            return False, f"Font size {name} must be numeric"
        min_size, max_size = size_ranges.get(name, (8, 24))
        if size < min_size or size > max_size:
            return False, f"Font size {name} ({size}pt) out of range ({min_size}-{max_size}pt)"
    
    # Validate margins (5-50mm)
    for name, margin in margins.items():
        if not isinstance(margin, (int, float)):
            return False, f"Margin {name} must be numeric"
        if margin < 5 or margin > 50:
            return False, f"Margin {name} ({margin}mm) out of range (5-50mm)"
    
    return True, None


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


class CustomTwoPageGenerator(TwoPageGenerator):
    """
    Custom generator that uses component system with custom grayscale template.
    """
    
    def _render_html_from_layout(
        self,
        layout,
        distilled_chat,
        styling_genome,
        custom_template=None,
    ) -> str:
        """Override to use custom grayscale template."""
        # Use the grayscale template from BlackWhiteWAFTGenerator
        bw_gen = BlackWhiteWAFTGenerator(weasyprint_available=self.weasyprint_available)
        
        # Convert layout components back to page_1_ideas and page_2_ideas format
        # for compatibility with existing template
        page_1_ideas = []
        page_2_ideas = []
        
        for comp in layout.components:
            if comp.component_type == ComponentType.SECTION:
                # Extract ideas from section content
                if isinstance(comp.content, dict):
                    body = comp.content.get('body', '')
                    if body:
                        # Create a simple idea-like object
                        from src.waft.evolution import IdeaGene
                        idea = IdeaGene(content=body, category='concept')
                        if len(page_1_ideas) < 4:
                            page_1_ideas.append(idea)
                        else:
                            page_2_ideas.append(idea)
        
        # Use the custom grayscale template
        return bw_gen._render_html(distilled_chat, styling_genome, page_1_ideas, page_2_ideas)


class BlackWhiteWAFTGenerator:
    """
    Black and white one-pager generator.
    
    Uses grayscale color scheme optimized for printer-friendly output.
    Extends TwoPageGenerator functionality with custom grayscale template.
    """
    
    def __init__(self, weasyprint_available: bool = False, max_iterations: int = 5):
        """Initialize generator."""
        self.weasyprint_available = weasyprint_available
        self.max_iterations = max_iterations
        if weasyprint_available:
            try:
                from weasyprint import HTML
                self.HTML = HTML
            except ImportError:
                self.weasyprint_available = False
                logger.warning("WeasyPrint import failed despite availability check")
    
    # Beautiful grayscale template optimized for first-time viewers
    GRAYSCALE_TEMPLATE = """
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
            
            @bottom-center {
                content: "WAFT Research Document | " counter(page);
                font-family: "Helvetica Neue", "Arial", sans-serif;
                font-size: {{ font.size_body - 3 }}pt;
                color: {{ color.text }};
                opacity: 0.5;
            }
        }
        
        @page :first {
            @top-right { content: none; }
            @bottom-center { content: none; }
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
            font-family: "Helvetica Neue", "Arial", sans-serif;
            font-size: {{ font.size_h1 }}pt;
            font-weight: 700;
            color: {{ color.heading }};
            margin-top: 0;
            margin-bottom: {{ margin.section_spacing }}pt;
            page-break-after: avoid;
            border-bottom: 2.5pt solid {{ color.border }};
            padding-bottom: 8pt;
            letter-spacing: -0.3pt;
            line-height: 1.2;
        }
        h2 {
            font-family: "Helvetica Neue", "Arial", sans-serif;
            font-size: {{ font.size_h2 }}pt;
            font-weight: 600;
            color: {{ color.heading }};
            margin-top: {{ margin.section_spacing }}pt;
            margin-bottom: {{ margin.paragraph_spacing }}pt;
            page-break-after: avoid;
            border-bottom: 1.5pt solid {{ color.border }};
            padding-bottom: 4pt;
            letter-spacing: -0.2pt;
        }
        h3 {
            font-family: "Helvetica Neue", "Arial", sans-serif;
            font-size: {{ font.size_h3 }}pt;
            font-weight: 600;
            color: {{ color.heading }};
            margin-top: {{ margin.paragraph_spacing + 2 }}pt;
            margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;
            page-break-after: avoid;
            letter-spacing: 0;
        }
        p { 
            margin: 0 0 {{ margin.paragraph_spacing }}pt 0; 
            text-align: justify;
            hyphens: auto;
        }
        ul, ol { 
            margin: 0 0 {{ margin.paragraph_spacing }}pt 0; 
            padding-left: 18pt; 
        }
        li { 
            margin-bottom: {{ margin.paragraph_spacing / 3 }}pt; 
        }
        .summary-box {
            background: {{ color.code_bg }};
            padding: {{ margin.paragraph_spacing + 2 }}pt;
            margin-bottom: {{ margin.section_spacing }}pt;
            border-left: 4pt solid {{ color.border }};
            border-top: 1pt solid {{ color.border }};
            border-right: 1pt solid {{ color.border }};
            border-bottom: 1pt solid {{ color.border }};
            page-break-inside: avoid;
            border-radius: 0;
        }
        .pillar {
            border-left: 4pt solid {{ color.border }};
            border-top: 1pt solid {{ color.border }};
            border-right: 1pt solid {{ color.border }};
            border-bottom: 1pt solid {{ color.border }};
            background: {{ color.background }};
            padding: {{ margin.paragraph_spacing }}pt;
            margin: {{ margin.paragraph_spacing }}pt 0;
            page-break-inside: avoid;
            border-radius: 0;
        }
        .pillar-title {
            font-family: "Helvetica Neue", "Arial", sans-serif;
            font-weight: 700;
            color: {{ color.heading }};
            font-size: {{ font.size_h3 }}pt;
            margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;
            text-transform: uppercase;
            letter-spacing: 1pt;
        }
        .pillar p {
            margin: 0;
            font-size: {{ font.size_body }}pt;
            line-height: 1.6;
        }
        .highlight-box {
            border-left: 4pt solid {{ color.border }};
            border-top: 1pt solid {{ color.border }};
            border-right: 1pt solid {{ color.border }};
            border-bottom: 1pt solid {{ color.border }};
            background: {{ color.code_bg }};
            padding: {{ margin.paragraph_spacing + 2 }}pt;
            margin: {{ margin.paragraph_spacing }}pt 0;
            page-break-inside: avoid;
            border-radius: 0;
        }
        .note-box {
            border-left: 5pt solid {{ color.border }};
            background: {{ color.code_bg }};
            padding: {{ margin.paragraph_spacing + 2 }}pt;
            margin: {{ margin.paragraph_spacing }}pt 0;
            page-break-inside: avoid;
            border-radius: 0;
        }
        .note-title {
            font-family: "Helvetica Neue", "Arial", sans-serif;
            font-weight: 700;
            color: {{ color.heading }};
            font-size: {{ font.size_h3 }}pt;
            margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;
            text-transform: uppercase;
            letter-spacing: 0.5pt;
        }
        .idea {
            margin-bottom: {{ margin.paragraph_spacing + 2 }}pt;
            padding: {{ margin.paragraph_spacing + 2 }}pt;
            border-left: 4pt solid {{ color.border }};
            background: {{ color.code_bg }};
            page-break-inside: avoid;
            border-radius: 0;
        }
        .idea-content {
            font-size: {{ font.size_body }}pt;
            line-height: 1.65;
            text-align: justify;
            margin: 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: {{ margin.paragraph_spacing + 2 }}pt 0;
            font-size: {{ font.size_body - 0.5 }}pt;
            page-break-inside: avoid;
        }
        th {
            font-family: "Helvetica Neue", "Arial", sans-serif;
            background: {{ color.heading }};
            color: {{ color.background }};
            border: 1pt solid {{ color.border }};
            padding: 7pt 8pt;
            text-align: left;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.3pt;
            font-size: {{ font.size_body - 1.5 }}pt;
        }
        td {
            border: 0.5pt solid {{ color.border }};
            padding: 6pt 8pt;
            background: {{ color.background }};
        }
        tr:nth-child(even) td {
            background: {{ color.code_bg }};
        }
        .metadata {
            font-size: {{ font.size_body - 2.5 }}pt;
            color: {{ color.text }};
            opacity: 0.65;
            line-height: 1.4;
            border-top: 0.5pt solid {{ color.border }};
            padding-top: {{ margin.paragraph_spacing / 2 }}pt;
            margin-top: {{ margin.paragraph_spacing + 2 }}pt;
            font-style: italic;
        }
        .divider {
            border-top: 1pt solid {{ color.border }};
            margin: {{ margin.paragraph_spacing + 4 }}pt 0;
            width: 60%;
            margin-left: auto;
            margin-right: auto;
        }
        code {
            font-family: 'Courier New', 'Monaco', monospace;
            font-size: {{ font.size_code }}pt;
            background: {{ color.code_bg }};
            color: {{ color.code_text }};
            padding: 3pt 5pt;
            border-radius: 0;
            border: 0.5pt solid {{ color.border }};
            font-weight: normal;
        }
        .key-features {
            margin: {{ margin.paragraph_spacing + 2 }}pt 0;
            page-break-inside: avoid;
        }
        .feature-list {
            margin-top: {{ margin.paragraph_spacing / 2 }}pt;
        }
        .feature-item {
            margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;
            padding-left: 8pt;
            border-left: 2pt solid {{ color.border }};
            padding-left: 10pt;
            font-size: {{ font.size_body - 0.5 }}pt;
            line-height: 1.5;
        }
        .feature-item strong {
            color: {{ color.heading }};
            font-weight: 600;
        }
        img {
            max-width: 100%;
            height: auto;
            page-break-inside: avoid;
            margin: {{ margin.paragraph_spacing / 2 }}pt 0;
        }
        .diagram {
            text-align: center;
            margin: {{ margin.paragraph_spacing }}pt 0;
            page-break-inside: avoid;
        }
        .diagram {
            text-align: center;
            margin: {{ margin.paragraph_spacing }}pt 0;
            page-break-inside: avoid;
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
            color: {{ color.text }};
            opacity: 0.8;
        }
        .author-info {
            font-size: {{ font.size_body - 1 }}pt;
            text-align: center;
            margin: {{ margin.paragraph_spacing }}pt 0;
            color: {{ color.text }};
            opacity: 0.7;
        }
        .abstract {
            background: {{ color.code_bg }};
            border-left: 3pt solid {{ color.border }};
            padding: {{ margin.paragraph_spacing }}pt;
            margin: {{ margin.paragraph_spacing }}pt 0;
            page-break-inside: avoid;
        }
        .abstract-title {
            font-family: "Helvetica Neue", "Arial", sans-serif;
            font-weight: 700;
            font-size: {{ font.size_h3 }}pt;
            margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;
            text-transform: uppercase;
            letter-spacing: 0.5pt;
        }
        .section-number {
            counter-increment: section;
        }
        body {
            counter-reset: section;
        }
        h2::before {
            content: counter(section) ". ";
            counter-increment: section;
        }
        .icon {
            display: inline-block;
            width: 24pt;
            height: 24pt;
            margin-right: 6pt;
            vertical-align: middle;
        }
        .footer {
            font-size: {{ font.size_body - 3.5 }}pt;
            color: {{ color.text }};
            opacity: 0.55;
            text-align: center;
            border-top: 0.5pt solid {{ color.border }};
            padding-top: 4pt;
            margin-top: {{ margin.paragraph_spacing + 4 }}pt;
            page-break-inside: avoid;
            font-style: italic;
            letter-spacing: 0.2pt;
        }
    </style>
</head>
<body>
    <div class="page-1">
        <h1 style="text-align: center; margin-bottom: {{ margin.paragraph_spacing }}pt;">{{ title }}</h1>
        
        <div class="author-info">
            <p style="margin: 0;">WAFT Research Team</p>
            <p style="margin: 2pt 0 0 0; font-size: {{ font.size_body - 1.5 }}pt;">{{ generated_at }}</p>
        </div>
        
        <div class="abstract">
            <div class="abstract-title">Abstract</div>
            <p style="margin: 0; font-size: {{ font.size_body }}pt; line-height: 1.6; text-align: justify;">{{ summary }}</p>
        </div>
        
        <h2 class="section-number">Introduction</h2>
        {% if page_1_ideas|length > 0 %}
        <p>{{ page_1_ideas[0].content }}</p>
        {% endif %}
        
        <h2 class="section-number">Architecture</h2>
        
        <div class="diagram no-break">
            <img src="{{ three_pillars_image }}" alt="The Three Pillars: Substrate, Physics, Flight Recorder" />
            <div class="figure-caption">Figure 1: The Three Pillars of WAFT Architecture</div>
        </div>
        
        {% if page_1_ideas|length > 1 %}
        <div class="pillar no-break">
            <div class="pillar-title">The Substrate</div>
            <p>{{ page_1_ideas[1].content }}</p>
        </div>
        {% endif %}
        
        {% if page_1_ideas|length > 2 %}
        <div class="pillar no-break">
            <div class="pillar-title">The Physics</div>
            <p>{{ page_1_ideas[2].content }}</p>
        </div>
        {% endif %}
        
        {% if page_1_ideas|length > 3 %}
        <div class="pillar no-break">
            <div class="pillar-title">The Flight Recorder</div>
            <p>{{ page_1_ideas[3].content }}</p>
        </div>
        {% endif %}
    </div>
    <div class="page-break"></div>
    <div class="page-2">
        <h2 class="section-number">Methodology</h2>
        {% if page_2_ideas|length > 0 %}
        <p>{{ page_2_ideas[0].content }}</p>
        {% endif %}
        
        {% if page_2_ideas|length > 1 %}
        <h3>Implementation</h3>
        <p>{{ page_2_ideas[1].content }}</p>
        {% endif %}
        
        {% if page_2_ideas|length > 2 %}
        <h3>Key Characteristics</h3>
        <p>{{ page_2_ideas[2].content }}</p>
        {% endif %}
        
        <h2 class="section-number">Conclusion</h2>
        {% if page_2_ideas|length > 3 %}
        <p>{{ page_2_ideas[3].content }}</p>
        {% elif page_2_ideas|length > 0 %}
        <p>{{ page_2_ideas[0].content }}</p>
        {% endif %}
        <div class="footer">
            <p style="margin: 0;">{{ footer_text }}</p>
        </div>
    </div>
</body>
</html>
"""
    
    
    def _clean_markdown(self, text: str) -> str:
        """Clean markdown formatting from text."""
        import re
        # Remove markdown links but keep text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        # Remove markdown bold/italic
        text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^\*]+)\*', r'\1', text)
        # Remove code blocks
        text = re.sub(r'`([^`]+)`', r'\1', text)
        return text
    
    def _render_html(
        self,
        distilled_chat,
        styling_genome,
        page_1_ideas: List,
        page_2_ideas: List,
    ) -> str:
        """Render HTML template with grayscale styling."""
        from jinja2 import Template
        
        def clean_idea(idea) -> Dict[str, Any]:
            idea_dict = idea.to_dict()
            idea_dict['content'] = self._clean_markdown(idea_dict.get('content', ''))
            return idea_dict
        
        # Create footer text with metadata
        footer_text = (
            f"{SCRIPT_NAME} v{SCRIPT_VERSION} | "
            f"Genome: {styling_genome.genome_id[:8]}... | "
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        
        # Get image paths (file:// URLs for WeasyPrint)
        images_dir = Path(__file__).parent.parent / "_work_efforts" / "one_pagers" / "images"
        three_pillars_path = images_dir / "three_pillars.png"
        evolution_tree_path = images_dir / "evolution_tree.png"
        code_dna_path = images_dir / "code_dna.png"
        
        def to_file_url(path: Path) -> str:
            """Convert Path to file:// URL for WeasyPrint."""
            if path.exists():
                return path.absolute().as_uri()
            return ""
        
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
            "footer_text": footer_text,
            "three_pillars_image": to_file_url(three_pillars_path),
            "evolution_tree_image": to_file_url(evolution_tree_path),
            "code_dna_image": to_file_url(code_dna_path),
        }
        
        template = Template(self.GRAYSCALE_TEMPLATE)
        return template.render(**context)


def validate_pdf_output(pdf_path: Path) -> tuple[bool, Dict[str, Any]]:
    """
    Validate generated PDF output.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Tuple of (is_valid, validation_report)
    """
    report = {
        'exists': False,
        'readable': False,
        'page_count': None,
        'file_size': 0,
        'structure_valid': False,
        'errors': [],
    }
    
    try:
        # Check file exists
        if not pdf_path.exists():
            report['errors'].append(f"PDF file does not exist: {pdf_path}")
            return False, report
        
        report['exists'] = True
        
        # Check file size
        file_size = pdf_path.stat().st_size
        report['file_size'] = file_size
        
        if file_size == 0:
            report['errors'].append("PDF file is empty")
            return False, report
        
        if file_size < 10240:  # 10KB
            report['errors'].append(f"PDF file is suspiciously small ({file_size} bytes)")
            # Don't fail, just warn
        
        # Check if readable
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(pdf_path))
            report['readable'] = True
            
            # Check page count
            page_count = len(reader.pages)
            report['page_count'] = page_count
            
            if page_count != 2:
                report['errors'].append(f"Expected 2 pages, found {page_count}")
            
            # Check structure (try to read first page)
            try:
                first_page = reader.pages[0]
                text = first_page.extract_text()
                if not text or len(text.strip()) < 10:
                    report['errors'].append("PDF appears to have no extractable text")
                else:
                    report['structure_valid'] = True
            except Exception as e:
                report['errors'].append(f"Error reading PDF structure: {e}")
            
        except ImportError:
            report['errors'].append("pypdf not available for validation")
        except Exception as e:
            report['errors'].append(f"Error reading PDF: {e}")
            logger.error(f"PDF validation error: {e}", exc_info=True)
        
        # Overall validation
        is_valid = (
            report['exists'] and
            report['readable'] and
            report['page_count'] == 2 and
            report['structure_valid']
        )
        
        return is_valid, report
        
    except Exception as e:
        report['errors'].append(f"Validation error: {e}")
        logger.error(f"PDF validation failed: {e}", exc_info=True)
        return False, report


def generate_one_pager(
    content: Optional[str] = None,
    output_path: Optional[Path] = None,
    open_pdf: bool = False,
    verbose: bool = False,
) -> Dict[str, Any]:
    """
    Generate black and white WAFT one-pager.
    
    Args:
        content: Optional custom content (uses default if None)
        output_path: Optional output path (uses default if None)
        open_pdf: Whether to open PDF after generation
        verbose: Enable verbose logging
        
    Returns:
        Dictionary with generation results
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info(f"Starting {SCRIPT_NAME} generation (v{SCRIPT_VERSION})")
    
    # Check Python version
    if not check_python_version():
        return {
            'success': False,
            'error': 'Python 3.10+ required',
        }
    
    # Check dependencies
    logger.info("Checking dependencies...")
    deps = check_dependencies()
    
    if not deps['weasyprint']:
        error_msg = (
            "WeasyPrint is required but not installed.\n"
            "Install with: pip install weasyprint\n"
            "Or: uv pip install weasyprint"
        )
        logger.error(error_msg)
        return {
            'success': False,
            'error': error_msg,
            'dependencies': deps,
        }
    
    if not deps['pypdf']:
        logger.warning("pypdf not available - page counting will be limited")
    
    if not deps['jinja2']:
        error_msg = (
            "jinja2 is required but not installed.\n"
            "Install with: pip install jinja2"
        )
        logger.error(error_msg)
        return {
            'success': False,
            'error': error_msg,
            'dependencies': deps,
        }
    
    logger.info("All required dependencies available")
    
    # Get content
    if content is None:
        logger.debug("Using default WAFT explanation content")
        content = get_waft_explanation_content()
    else:
        logger.debug("Using provided custom content")
    
    # Validate content
    is_valid, error_msg = validate_content(content)
    if not is_valid:
        logger.error(f"Content validation failed: {error_msg}")
        return {
            'success': False,
            'error': f"Content validation failed: {error_msg}",
        }
    
    # Set up output path
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path(f"_work_efforts/one_pagers/WAFT_Intro_BW_{timestamp}.pdf")
    
    # Validate output path
    is_valid, error_msg = validate_output_path(output_path)
    if not is_valid:
        logger.error(f"Output path validation failed: {error_msg}")
        return {
            'success': False,
            'error': f"Output path validation failed: {error_msg}",
        }
    
    # Ensure output directory exists
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create output directory: {e}")
        return {
            'success': False,
            'error': f"Failed to create output directory: {e}",
        }
    
    # Import required modules
    try:
        from src.waft.evolution import (
            ChatDistiller,
            StylingGenome,
            StylingGenomeRegistry,
            StylingGene,
            FontGene,
            MarginGene,
            ColorGene,
            LayoutGene,
        )
        from src.waft.evolution.document_components import DocumentLayout, ComponentType
        from weasyprint import HTML
        from jinja2 import Template
    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        return {
            'success': False,
            'error': f"Import error: {e}",
        }
    
    # Distill content
    logger.info("Distilling content into ideas...")
    try:
        distiller = ChatDistiller()
        distilled = distiller.distill_text(content, title="WAFT: The Evolutionary Code Laboratory")
        logger.info(f"Extracted {distilled.total_ideas} ideas")
        logger.debug(f"  - Concepts: {distilled.concepts_count}")
        logger.debug(f"  - Actions: {distilled.actions_count}")
        logger.debug(f"  - Decisions: {distilled.decisions_count}")
        logger.debug(f"  - Insights: {distilled.insights_count}")
        logger.debug(f"  - Questions: {distilled.questions_count}")
    except Exception as e:
        logger.error(f"Content distillation failed: {e}", exc_info=True)
        return {
            'success': False,
            'error': f"Content distillation failed: {e}",
        }
    
    # Create grayscale styling genome
    logger.info("Creating grayscale styling genome...")
    try:
        # Refined grayscale color scheme with elegant palette
        grayscale_colors = ColorGene(
            text="#1a1a1a",        # Soft black (easier on eyes than pure black)
            background="#FFFFFF",  # Pure white background
            heading="#000000",     # Pure black for strong headings
            accent="#4a4a4a",      # Medium gray for accents (more visible than #333)
            code_bg="#f8f8f8",    # Very light gray for code blocks (softer than #f5f5f5)
            code_text="#1a1a1a",   # Soft black for code text
            border="#2a2a2a",      # Dark gray borders (softer than pure black)
        )
        
        # Refined typography with better hierarchy
        font_sizes = {
            'body': 10.5,  # Slightly smaller for better fit
            'h1': 26,      # Larger, more impactful
            'h2': 16,      # Better proportion
            'h3': 13,      # Refined
            'code': 9.5,   # Slightly smaller
        }
        margins = {
            'top': 18,     # Tighter top margin
            'bottom': 18,
            'left': 22,    # More left margin for elegance
            'right': 22,
        }
        
        is_valid, error_msg = validate_styling_parameters(font_sizes, margins)
        if not is_valid:
            logger.error(f"Styling validation failed: {error_msg}")
            return {
                'success': False,
                'error': f"Styling validation failed: {error_msg}",
            }
        
        grayscale_genes = StylingGene(
            font=FontGene(
                family="Georgia, serif",  # Elegant serif for body (falls back to serif)
                size_body=10,
                size_h1=24,
                size_h2=15,
                size_h3=12,
                size_code=9,
                line_height=1.5,  # Tighter line spacing to fit more content
            ),
            margin=MarginGene(
                top=16,
                bottom=16,
                left=20,
                right=20,
                paragraph_spacing=8,  # Tighter spacing
                section_spacing=12,    # Tighter section spacing
            ),
            color=grayscale_colors,
            layout=LayoutGene(
                columns=1,
                density="normal",
                toc_enabled=False,
                page_numbers=True,
                header_enabled=True,
                footer_enabled=True,
            ),
            name="WAFT Intro Handout Black & White",
        )
        
        genome = StylingGenome.from_genes(grayscale_genes)
        
        # Try to register (but don't fail if filesystem is read-only)
        try:
            registry = StylingGenomeRegistry(registry_dir=Path("_genetics/waft_intro_handouts_bw"))
            registry.register(genome)
            logger.debug(f"Registered genome: {genome.scientific_name} ({genome.genome_id[:8]}...)")
        except Exception as e:
            logger.warning(f"Failed to register genome (filesystem may be read-only): {e}")
            # Continue anyway
        
    except Exception as e:
        logger.error(f"Failed to create styling genome: {e}", exc_info=True)
        return {
            'success': False,
            'error': f"Styling genome creation failed: {e}",
        }
    
    # Generate PDF using TwoPageGenerator with custom renderer
    logger.info("Generating 2-page PDF...")
    try:
        from src.waft.evolution import TwoPageGenerator
        
        # Create a custom generator that uses our grayscale template
        class CustomTwoPageGenerator(TwoPageGenerator):
            def _render_html(self, distilled_chat, styling_genome, page_1_ideas, page_2_ideas):
                # Use BlackWhiteWAFTGenerator's render method
                bw_gen = BlackWhiteWAFTGenerator(weasyprint_available=self.weasyprint_available)
                return bw_gen._render_html(distilled_chat, styling_genome, page_1_ideas, page_2_ideas)
        
        generator = CustomTwoPageGenerator(weasyprint_available=True, max_iterations=5, allowed_pages=2)
        
        # Use the generator's generate method
        result = generator.generate(
            distilled_chat=distilled,
            styling_genome=genome,
            output_path=output_path,
            target_pages=2,
            convert_to_png=False,
        )
        
        if not result.get('success', False):
            logger.error("PDF generation failed")
            return {
                'success': False,
                'error': result.get('error', 'Unknown error during PDF generation'),
                'result': result,
            }
        
        logger.info(f"PDF generated: {output_path}")
        
    except Exception as e:
        logger.error(f"PDF generation failed: {e}", exc_info=True)
        
        # Fallback: Try to generate HTML at least
        try:
            logger.info("Attempting HTML fallback...")
            bw_generator = BlackWhiteWAFTGenerator(weasyprint_available=False)
            all_ideas = distilled.get_top_ideas(n=10, min_importance=0.3)
            page_1_ideas = all_ideas[:4]
            page_2_ideas = all_ideas[4:6] if len(all_ideas) > 4 else []
            
            html_content = bw_generator._render_html(
                distilled,
                genome,
                page_1_ideas,
                page_2_ideas,
            )
            
            html_path = output_path.with_suffix('.html')
            html_path.write_text(html_content, encoding='utf-8')
            logger.info(f"HTML fallback saved: {html_path}")
            
            return {
                'success': False,
                'error': f"PDF generation failed: {e}",
                'html_path': str(html_path),
                'fallback': True,
            }
        except Exception as fallback_error:
            logger.error(f"HTML fallback also failed: {fallback_error}", exc_info=True)
            return {
                'success': False,
                'error': f"PDF generation failed: {e}. HTML fallback also failed: {fallback_error}",
            }
    
    # Validate output
    logger.info("Validating PDF output...")
    is_valid, validation_report = validate_pdf_output(output_path)
    
    if validation_report['errors']:
        for error in validation_report['errors']:
            logger.warning(f"Validation warning: {error}")
    
    if not is_valid:
        logger.warning("PDF validation found issues, but continuing...")
    
    # Open PDF if requested
    if open_pdf and output_path.exists():
        try:
            system = platform.system()
            if system == "Darwin":  # macOS
                import subprocess
                subprocess.run(["open", "-a", "Preview", str(output_path)], check=False)
            elif system == "Windows":
                import os
                os.startfile(str(output_path))
            else:  # Linux and others
                webbrowser.open(f"file://{output_path.absolute()}")
            logger.info("PDF opened in default viewer")
        except Exception as e:
            logger.warning(f"Failed to open PDF: {e}")
    
    # Prepare result
    result = {
        'success': True,
        'pdf_path': str(output_path),
        'page_count': validation_report.get('page_count', result.get('page_count', 0)),
        'file_size': validation_report.get('file_size', 0),
        'validation': validation_report,
        'genome_id': genome.genome_id[:8] if 'genome' in locals() else None,
        'version': SCRIPT_VERSION,
    }
    
    logger.info("Generation complete!")
    return result


def main():
    """Main entry point with CLI interface."""
    parser = argparse.ArgumentParser(
        description=f"{SCRIPT_NAME} - Generate beautiful black & white WAFT introduction one-pager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s
  %(prog)s --output my_waft_intro.pdf
  %(prog)s --content custom_content.md --verbose
  %(prog)s --validate-only
        """
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output PDF path (default: _work_efforts/one_pagers/WAFT_Intro_BW_[timestamp].pdf)'
    )
    
    parser.add_argument(
        '--content', '-c',
        type=str,
        help='Path to custom content file (default: use built-in WAFT explanation)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging (DEBUG level)'
    )
    
    parser.add_argument(
        '--open',
        action='store_true',
        help='Open PDF in default viewer after generation'
    )
    
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate existing PDF (requires --output)'
    )
    
    args = parser.parse_args()
    
    # Handle validate-only mode
    if args.validate_only:
        if not args.output:
            print("Error: --validate-only requires --output to specify PDF to validate")
            sys.exit(1)
        
        pdf_path = Path(args.output)
        if not pdf_path.exists():
            print(f"Error: PDF file not found: {pdf_path}")
            sys.exit(1)
        
        is_valid, report = validate_pdf_output(pdf_path)
        
        print("\n" + "=" * 60)
        print("PDF Validation Report")
        print("=" * 60)
        print(f"File: {pdf_path}")
        print(f"Exists: {report['exists']}")
        print(f"Readable: {report['readable']}")
        print(f"Page Count: {report.get('page_count', 'N/A')}")
        print(f"File Size: {report.get('file_size', 0):,} bytes")
        print(f"Structure Valid: {report['structure_valid']}")
        
        if report['errors']:
            print("\nErrors/Warnings:")
            for error in report['errors']:
                print(f"  - {error}")
        
        if is_valid:
            print("\n✅ PDF is valid!")
            sys.exit(0)
        else:
            print("\n❌ PDF validation failed")
            sys.exit(1)
    
    # Load custom content if provided
    content = None
    if args.content:
        try:
            content_path = Path(args.content)
            if not content_path.exists():
                print(f"Error: Content file not found: {content_path}")
                sys.exit(1)
            content = content_path.read_text(encoding='utf-8')
            logger.info(f"Loaded custom content from: {content_path}")
        except Exception as e:
            print(f"Error reading content file: {e}")
            sys.exit(1)
    
    # Set output path
    output_path = None
    if args.output:
        output_path = Path(args.output)
    
    # Generate
    try:
        result = generate_one_pager(
            content=content,
            output_path=output_path,
            open_pdf=args.open,
            verbose=args.verbose,
        )
        
        if result['success']:
            print("\n" + "=" * 60)
            print(f"✅ {SCRIPT_NAME} Created Successfully!")
            print("=" * 60)
            print(f"📄 Output: {result['pdf_path']}")
            print(f"📊 Pages: {result.get('page_count', 'N/A')}/2")
            print(f"📦 Size: {result.get('file_size', 0):,} bytes")
            if result.get('genome_id'):
                print(f"🧬 Genome: {result['genome_id']}...")
            print(f"🔖 Version: {result.get('version', 'N/A')}")
            
            if result.get('validation', {}).get('errors'):
                print("\n⚠️  Validation Warnings:")
                for error in result['validation']['errors']:
                    print(f"   - {error}")
            
            print("\n✅ Ready for printing and distribution!")
            sys.exit(0)
        else:
            print(f"\n❌ Generation failed: {result.get('error', 'Unknown error')}")
            if result.get('html_path'):
                print(f"📄 HTML fallback saved: {result['html_path']}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if args.verbose:
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
