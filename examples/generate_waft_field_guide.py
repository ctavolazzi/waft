"""
Generate WAFT Field Guide Booklet
==================================

Creates a three-level field guide explaining WAFT:
- Level 1 (Layman): Simple explanations for anyone
- Level 2 (Professional): Technical details for developers
- Level 3 (ML AI Scientist): Research-level depth for scientists

Then combines all three into a single booklet using the binder system.
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.binder import Binder, DocumentEntry
from src.waft.templates.field_guide import generate_field_guide


def generate_level_1_layman(output_dir: Path) -> Path:
    """Generate Level 1: Layman's Guide to WAFT."""

    content = """
<h2>Introduction: What is WAFT?</h2>

<p>
<strong>WAFT</strong> stands for <strong>Wave Agent Framework & Tools</strong>. 
Think of it as a laboratory where AI agents can evolve, learn, and improve themselves 
through a process similar to biological evolution.
</p>

<div class="note">
    <div class="note-title">Simple Analogy</div>
    Imagine if computer programs were like living creatures. WAFT is the ecosystem 
    where they can breed, mutate, and evolve. The strongest programs survive, and 
    over time, they get better at their jobs.
</div>

<h2>The Big Picture: Why This Matters</h2>

<p>
Most AI systems are static—you build them once and they stay the same. WAFT is different. 
It creates AI agents that can:
</p>

<ul>
    <li><strong>Modify their own code</strong> (like DNA mutations)</li>
    <li><strong>Test themselves</strong> in challenging environments</li>
    <li><strong>Evolve</strong> by keeping what works and discarding what doesn't</li>
    <li><strong>Document themselves</strong> automatically</li>
    <li><strong>Track their family tree</strong> like a scientific experiment</li>
</ul>

<div class="caution">
    <div class="caution-title">Important Concept</div>
    WAFT isn't just a tool—it's a <strong>scientific instrument</strong> designed to 
    study how artificial intelligence can evolve and improve over time. The goal is to 
    observe how AI agents develop through thousands of generations.
</div>

<h2>Equipment Checklist</h2>

<div class="checklist">
    <div class="checklist-title">What You Need to Get Started</div>
    <ul>
        <li>Python 3.10 or newer installed</li>
        <li>uv package manager (for managing dependencies)</li>
        <li>A computer with internet connection</li>
        <li>Basic understanding of command-line tools</li>
        <li>Curiosity about AI and evolution</li>
    </ul>
</div>

<div class="note">
    <div class="note-title">Note</div>
    You don't need to be a programmer to understand WAFT, but some technical comfort 
    helps. This guide will explain everything in simple terms.
</div>

<h2>Quick Start: Your First WAFT Project</h2>

<h3>Step 1: Install WAFT</h3>

<div class="procedure">
    <div class="step">
        Open your terminal (command prompt on Windows, Terminal on Mac/Linux)
    </div>
    <div class="step">
        Install WAFT using: <code>uv tool install waft</code>
    </div>
    <div class="step">
        Wait for installation to complete (this may take a minute)
    </div>
    <div class="step">
        Verify installation by typing: <code>waft --version</code>
    </div>
</div>

<h3>Step 2: Create Your First Laboratory</h3>

<div class="procedure">
    <div class="step">
        Choose a name for your project (e.g., "my_first_agents")
    </div>
    <div class="step">
        Run: <code>waft new my_first_agents</code>
    </div>
    <div class="step">
        WAFT will create a folder with everything you need
    </div>
    <div class="step">
        Navigate into it: <code>cd my_first_agents</code>
    </div>
</div>

<div class="warning">
    <div class="warning-title">Warning</div>
    Don't delete the <code>_pyrite</code> folder! This is WAFT's memory system. 
    It stores all the knowledge about your project.
</div>

<h2>Core Concepts Explained Simply</h2>

<h3>1. Code as DNA</h3>

<p>
In WAFT, an agent's code is like its DNA. Just as living creatures have genetic code 
that determines their traits, AI agents have Python code that determines their behavior.
</p>

<div class="note">
    <div class="note-title">Example</div>
    If you change an agent's code (a "mutation"), it might become better at solving 
    problems, or it might break. WAFT tests these mutations to see which ones are 
    improvements.
</div>

<h3>2. Evolution Through Testing</h3>

<p>
WAFT has a "gym" where agents are tested on their ability to handle errors and solve 
problems. Agents that perform well survive. Agents that fail are marked as "DEATH" 
and don't continue evolving.
</p>

<h3>3. Family Trees</h3>

<p>
Every agent has a unique ID (like a fingerprint) and WAFT tracks who "spawned" whom. 
This creates a family tree that scientists can study to understand how AI agents evolve.
</p>

<h3>4. Self-Documentation</h3>

<p>
One of WAFT's coolest features: it can observe its own code and write documentation 
about itself. This creates a "recursive loop" where WAFT improves by understanding 
itself better.
</p>

<div class="caution">
    <div class="caution-title">Mind-Bending Concept</div>
    WAFT documenting WAFT using WAFT. It's like a mirror reflecting a mirror—the 
    documentation gets better over time because WAFT learns more about itself.
</div>

<h2>Common Questions</h2>

<h3>Q: Do I need to be a programmer?</h3>
<p>
<strong>A:</strong> Not necessarily! This guide (Level 1) is written for anyone. 
However, to actually use WAFT, you'll need some comfort with command-line tools. 
Level 2 and Level 3 get progressively more technical.
</p>

<h3>Q: Is WAFT safe?</h3>
<p>
<strong>A:</strong> WAFT includes safety checks. Agents are tested for harmful content, 
errors, and dangerous behavior. Agents that fail safety tests are automatically 
marked as unfit.
</p>

<h3>Q: What can I do with WAFT?</h3>
<p>
<strong>A:</strong> WAFT is designed for research into AI evolution. You can:
</p>
<ul>
    <li>Create AI agents that solve specific problems</li>
    <li>Watch them evolve over generations</li>
    <li>Study how they improve</li>
    <li>Generate scientific data for research</li>
</ul>

<h3>Q: How long does evolution take?</h3>
<p>
<strong>A:</strong> It depends on your computer and the complexity of your agents. 
Simple agents might evolve in minutes. Complex ones could take hours or days. The 
goal is to observe evolution over thousands of generations.
</p>

<h2>Safety Warnings</h2>

<div class="warning">
    <div class="warning-title">Critical Warning</div>
    WAFT agents can modify their own code. Always test agents in isolated environments. 
    Never run untrusted agents on systems with sensitive data. Use WAFT's safety 
    systems and verify agent behavior before deployment.
</div>

<div class="caution">
    <div class="caution-title">Caution</div>
    Evolution is unpredictable. An agent that performs well in testing might behave 
    differently in real-world scenarios. Always validate agent behavior before 
    using it for important tasks.
</div>

<h2>What Makes WAFT Special?</h2>

<p>
WAFT has several unique features that make it different from other AI frameworks:
</p>

<table>
    <caption>Table 1: WAFT's Unique Features</caption>
    <tr>
        <th>Feature</th>
        <th>What It Means</th>
        <th>Why It Matters</th>
    </tr>
    <tr>
        <td><strong>Self-Modification</strong></td>
        <td>Agents can change their own code</td>
        <td>Enables true evolution, not just execution</td>
    </tr>
    <tr>
        <td><strong>Fitness Testing</strong></td>
        <td>Agents are tested in a "gym"</td>
        <td>Only the best agents survive</td>
    </tr>
    <tr>
        <td><strong>Lineage Tracking</strong></td>
        <td>Every agent's family tree is recorded</td>
        <td>Enables scientific analysis</td>
    </tr>
    <tr>
        <td><strong>Self-Documentation</strong></td>
        <td>WAFT documents itself automatically</td>
        <td>Creates recursive improvement loop</td>
    </tr>
    <tr>
        <td><strong>12 Document Templates</strong></td>
        <td>Professional document generation</td>
        <td>Creates publication-ready outputs</td>
    </tr>
    <tr>
        <td><strong>Gamification</strong></td>
        <td>D&D-style progression system</td>
        <td>Makes development engaging</td>
    </tr>
</table>

<h2>Next Steps</h2>

<p>
Now that you understand the basics:
</p>

<div class="procedure">
    <div class="step">
        Read <strong>Level 2: Professional Guide</strong> for technical details and 
        how to actually use WAFT in your projects
    </div>
    <div class="step">
        If you're a researcher, read <strong>Level 3: ML AI Scientist Guide</strong> 
        for deep scientific methodology
    </div>
    <div class="step">
        Try creating your first WAFT project using the Quick Start guide above
    </div>
    <div class="step">
        Explore WAFT's 12 document templates to see what it can generate
    </div>
</div>

<div class="note">
    <div class="note-title">Remember</div>
    WAFT is a scientific instrument. The goal isn't just to build AI agents—it's to 
    <strong>understand how AI evolves</strong>. Every experiment contributes to our 
    understanding of artificial cognition.
</div>

<h2>Contact & Resources</h2>

<p>
<strong>Documentation:</strong> Check the README.md in your WAFT installation<br>
<strong>Examples:</strong> See the <code>examples/</code> directory for code samples<br>
<strong>GitHub:</strong> https://github.com/ctavolazzi/waft<br>
<strong>Issues:</strong> Report problems on GitHub Issues
</p>

<div class="page-break"></div>

<h2>Appendix A: Glossary</h2>

<table>
    <caption>Table 2: Key Terms Explained</caption>
    <tr>
        <th>Term</th>
        <th>Simple Explanation</th>
    </tr>
    <tr>
        <td><strong>Agent</strong></td>
        <td>An AI program that can perform tasks and modify itself</td>
    </tr>
    <tr>
        <td><strong>Genome</strong></td>
        <td>The unique code and configuration of an agent (like DNA)</td>
    </tr>
    <tr>
        <td><strong>Mutation</strong></td>
        <td>A change to an agent's code or configuration</td>
    </tr>
    <tr>
        <td><strong>Evolution</strong></td>
        <td>The process of agents improving over generations</td>
    </tr>
    <tr>
        <td><strong>Fitness</strong></td>
        <td>How well an agent performs in tests</td>
    </tr>
    <tr>
        <td><strong>Scint Gym</strong></td>
        <td>The testing environment where agents are evaluated</td>
    </tr>
    <tr>
        <td><strong>Flight Recorder</strong></td>
        <td>The system that tracks all agent actions and lineage</td>
    </tr>
    <tr>
        <td><strong>_pyrite</strong></td>
        <td>WAFT's memory system (stores project knowledge)</td>
    </tr>
</table>

<p style="margin-top: 0.5in; text-align: center; font-weight: bold;">
REMEMBER: WAFT is about understanding evolution, not just building tools.
</p>
    """

    output_path = output_dir / "WAFT_Field_Guide_Layman.pdf"

    generate_field_guide(
        title="WAFT FIELD GUIDE",
        content=content,
        output_path=output_path,
        series="FIELD GUIDE",
        number="FG-001",
        subtitle="Level 1: Layman's Guide to WAFT",
        classification="PUBLIC",
        issued_by="WAFT Documentation Team",
        date=datetime.now().strftime("%B %d, %Y"),
    )

    return output_path


def generate_level_2_professional(output_dir: Path) -> Path:
    """Generate Level 2: Professional Guide to WAFT."""

    content = """
<h2>Introduction</h2>

<p>
This guide provides technical details for developers and engineers working with WAFT. 
It covers architecture, APIs, integration patterns, and best practices for building 
production systems with WAFT.
</p>

<div class="warning">
    <div class="warning-title">Prerequisites</div>
    This guide assumes familiarity with Python, command-line tools, and software 
    architecture. If you're new to WAFT, start with Level 1: Layman's Guide.
</div>

<h2>Architecture Overview</h2>

<h3>Three-Layer Architecture</h3>

<p>
WAFT uses a three-layer architecture:
</p>

<div class="procedure">
    <div class="step">
        <strong>Substrate Layer:</strong> Package management (uv), project structure, 
        dependency management. This is the foundation.
    </div>
    <div class="step">
        <strong>Memory Layer:</strong> Knowledge organization (_pyrite directory), 
        active work, backlog, standards. This stores project state.
    </div>
    <div class="step">
        <strong>Agents Layer:</strong> AI agent capabilities (optional CrewAI integration), 
        evolutionary systems, fitness testing. This is where agents operate.
    </div>
</div>

<h3>Core Components</h3>

<table>
    <caption>Table 1: WAFT Core Components</caption>
    <tr>
        <th>Component</th>
        <th>Location</th>
        <th>Purpose</th>
    </tr>
    <tr>
        <td><strong>Substrate Manager</strong></td>
        <td><code>core/substrate.py</code></td>
        <td>Manages uv operations, pyproject.toml</td>
    </tr>
    <tr>
        <td><strong>Memory System</strong></td>
        <td><code>_pyrite/</code></td>
        <td>Organizes active/backlog/standards</td>
    </tr>
    <tr>
        <td><strong>Agent Framework</strong></td>
        <td><code>core/agent/</code></td>
        <td>BaseAgent, AgentState, AgentConfig</td>
    </tr>
    <tr>
        <td><strong>World System</strong></td>
        <td><code>core/world/</code></td>
        <td>Biome, PetriDish environments</td>
    </tr>
    <tr>
        <td><strong>Science Module</strong></td>
        <td><code>core/science/</code></td>
        <td>TheObserver, Taxonomy, Reports</td>
    </tr>
    <tr>
        <td><strong>Gamification</strong></td>
        <td><code>core/gamification/</code></td>
        <td>RPG-style progression system</td>
    </tr>
</table>

<h2>API Reference</h2>

<h3>Command-Line Interface</h3>

<div class="checklist">
    <div class="checklist-title">Core Commands</div>
    <ul>
        <li><code>waft new &lt;name&gt;</code> - Create new project</li>
        <li><code>waft verify</code> - Verify project structure</li>
        <li><code>waft sync</code> - Sync dependencies</li>
        <li><code>waft add &lt;package&gt;</code> - Add dependency</li>
        <li><code>waft init</code> - Initialize in existing project</li>
        <li><code>waft info</code> - Show project information</li>
    </ul>
</div>

<h3>Python API</h3>

<h4>Creating an Agent</h4>

<pre><code>from waft.core.agent import BaseAgent, AgentConfig

config = AgentConfig(
    name="MyAgent",
    description="An agent that solves problems"
)

agent = BaseAgent(config=config)
agent.initialize()
</code></pre>

<h4>Document Generation</h4>

<pre><code>from waft.templates.field_guide import generate_field_guide
from pathlib import Path

generate_field_guide(
    title="My Guide",
    content="&lt;h2&gt;Content&lt;/h2&gt;&lt;p&gt;HTML content here&lt;/p&gt;",
    output_path=Path("output.pdf")
)
</code></pre>

<h4>Binder System</h4>

<pre><code>from waft.binder import Binder, DocumentEntry
from pathlib import Path

binder = Binder(
    title="My Binder",
    subtitle="Document Collection"
)

section = binder.add_section("Section 1")
section.add_document(DocumentEntry(
    path=Path("doc1.pdf"),
    title="Document 1"
))

binder.generate(Path("binder.pdf"))
</code></pre>

<h2>Integration Patterns</h2>

<h3>Pattern 1: New Project Setup</h3>

<div class="procedure">
    <div class="step">
        Run <code>waft new project_name</code>
    </div>
    <div class="step">
        Review generated <code>pyproject.toml</code>
    </div>
    <div class="step">
        Check <code>_pyrite/active/</code> for initial work items
    </div>
    <div class="step">
        Run <code>waft verify</code> to confirm structure
    </div>
</div>

<h3>Pattern 2: Adding Document Generation</h3>

<div class="procedure">
    <div class="step">
        Import desired template (e.g., <code>from waft.templates.field_guide import generate_field_guide</code>)
    </div>
    <div class="step">
        Prepare HTML content
    </div>
    <div class="step">
        Call template function with content and output path
    </div>
    <div class="step">
        Verify generated PDF
    </div>
</div>

<h3>Pattern 3: Self-Documentation Loop</h3>

<div class="procedure">
    <div class="step">
        Use <code>waft.reflection.ReflectionSystem</code> to analyze codebase
    </div>
    <div class="step">
        Generate documentation using WAFT templates
    </div>
    <div class="step">
        Review generated docs to inform development
    </div>
    <div class="step">
        Repeat as codebase evolves
    </div>
</div>

<h2>Workflow Procedures</h2>

<h3>Development Workflow</h3>

<div class="checklist">
    <div class="checklist-title">Standard Development Process</div>
    <ul>
        <li>Create or update work items in <code>_pyrite/active/</code></li>
        <li>Implement features following WAFT patterns</li>
        <li>Run <code>waft verify</code> before committing</li>
        <li>Generate documentation for new features</li>
        <li>Update <code>_pyrite/standards/</code> if patterns change</li>
    </ul>
</div>

<h3>Documentation Workflow</h3>

<div class="procedure">
    <div class="step">
        Identify documentation gaps using reflection system
    </div>
    <div class="step">
        Select appropriate template (field guide, lab notes, etc.)
    </div>
    <div class="step">
        Generate documentation PDF
    </div>
    <div class="step">
        Review and iterate on content
    </div>
    <div class="step">
        Add to binder if part of larger collection
    </div>
</div>

<h2>Troubleshooting</h2>

<table>
    <caption>Table 2: Common Issues and Solutions</caption>
    <tr>
        <th>Issue</th>
        <th>Cause</th>
        <th>Solution</th>
    </tr>
    <tr>
        <td>Template generation fails</td>
        <td>Missing WeasyPrint dependencies</td>
        <td>Run <code>uv sync</code> to install dependencies</td>
    </tr>
    <tr>
        <td>Binder merge errors</td>
        <td>Corrupted PDF files</td>
        <td>Regenerate source PDFs</td>
    </tr>
    <tr>
        <td>Memory system not found</td>
        <td>Missing <code>_pyrite/</code> directory</td>
        <td>Run <code>waft init</code> to create structure</td>
    </tr>
    <tr>
        <td>Agent initialization fails</td>
        <td>Invalid configuration</td>
        <td>Check <code>AgentConfig</code> parameters</td>
    </tr>
</table>

<h2>Performance Optimization</h2>

<h3>Document Generation</h3>

<ul>
    <li>Use HTML content blocks efficiently (avoid excessive nesting)</li>
    <li>Cache template rendering for repeated content</li>
    <li>Generate PDFs in batch when possible</li>
    <li>Use appropriate template for content type</li>
</ul>

<h3>Binder Assembly</h3>

<ul>
    <li>Generate individual PDFs first, then combine</li>
    <li>Use temporary directory for intermediate files</li>
    <li>Clean up temporary files after binder generation</li>
    <li>Consider page count limits for large binders</li>
</ul>

<h2>Best Practices</h2>

<div class="checklist">
    <div class="checklist-title">Development Best Practices</div>
    <ul>
        <li>Always run <code>waft verify</code> before committing</li>
        <li>Keep <code>_pyrite/</code> structure organized</li>
        <li>Document new features using WAFT templates</li>
        <li>Follow existing code patterns and conventions</li>
        <li>Test document generation in CI/CD pipeline</li>
    </ul>
</div>

<div class="note">
    <div class="note-title">Pro Tip</div>
    Use WAFT's self-documentation capabilities to keep documentation in sync with 
    code changes. The reflection system can identify when documentation needs updates.
</div>

<h2>Advanced Features</h2>

<h3>Template Customization</h3>

<p>
All templates use Jinja2 for rendering. You can customize templates by:
</p>

<ul>
    <li>Modifying template files in <code>src/waft/templates/</code></li>
    <li>Passing custom parameters to template functions</li>
    <li>Creating new templates following existing patterns</li>
</ul>

<h3>Binder Customization</h3>

<p>
Binders support custom styling, section dividers, and front/back matter. See 
<code>src/waft/binder.py</code> for full API documentation.
</p>

<h2>Next Steps</h2>

<div class="procedure">
    <div class="step">
        Review Level 3: ML AI Scientist Guide for research methodology
    </div>
    <div class="step">
        Explore WAFT source code in <code>src/waft/</code>
    </div>
    <div class="step">
        Check examples in <code>examples/</code> directory
    </div>
    <div class="step">
        Join WAFT community for support and collaboration
    </div>
</div>
    """

    output_path = output_dir / "WAFT_Field_Guide_Professional.pdf"

    generate_field_guide(
        title="WAFT FIELD GUIDE",
        content=content,
        output_path=output_path,
        series="FIELD GUIDE",
        number="FG-002",
        subtitle="Level 2: Professional Developer's Guide",
        classification="TECHNICAL",
        issued_by="WAFT Engineering Team",
        date=datetime.now().strftime("%B %d, %Y"),
    )

    return output_path


def generate_level_3_scientist(output_dir: Path) -> Path:
    """Generate Level 3: ML AI Scientist Guide to WAFT."""

    content = """
<h2>Introduction</h2>

<p>
This guide provides deep technical and scientific details for machine learning 
researchers, AI scientists, and evolutionary computation experts working with WAFT. 
It covers evolutionary theory, fitness functions, phylogenetic analysis, and 
experimental protocols for generating publication-ready research data.
</p>

<div class="warning">
    <div class="warning-title">Research Focus</div>
    WAFT is designed as a scientific instrument for studying the physics of artificial 
    cognition. This guide assumes familiarity with evolutionary algorithms, machine 
    learning, and experimental design.
</div>

<h2>Evolutionary Theory in WAFT</h2>

<h3>The Three Pillars</h3>

<p>
WAFT's evolutionary framework rests on three foundational pillars:
</p>

<h4>Pillar 1: The Substrate (Code as DNA)</h4>

<p>
In WAFT, an agent's Python source code and configuration constitute its genome. 
The genome is hashed using SHA-256 to create a unique <strong>Genome ID</strong>.
</p>

<div class="note">
    <div class="note-title">Genome Representation</div>
    Genome = SHA-256(code + configuration + metadata)<br>
    This ensures deterministic identification and enables precise lineage tracking.
</div>

<p>
<strong>Mutation mechanisms:</strong>
</p>

<ul>
    <li><strong>Code mutations:</strong> Direct modifications to Python source</li>
    <li><strong>Config mutations:</strong> Changes to agent configuration</li>
    <li><strong>Prompt evolution:</strong> Modifications to agent prompts/instructions</li>
    <li><strong>Hot-swapping:</strong> Runtime adoption of better genomes</li>
</ul>

<h4>Pillar 2: The Physics (Scint System)</h4>

<p>
The <strong>Reality Fracture Detection System</strong> (Scint Gym) serves as the 
fitness function and natural selection mechanism. Agents face four types of errors:
</p>

<table>
    <caption>Table 1: Scint Error Types</caption>
    <tr>
        <th>Error Type</th>
        <th>Description</th>
        <th>Fitness Impact</th>
    </tr>
    <tr>
        <td><strong>SYNTAX_TEAR</strong></td>
        <td>Formatting errors (JSON, XML, code syntax)</td>
        <td>High - indicates fundamental issues</td>
    </tr>
    <tr>
        <td><strong>LOGIC_FRACTURE</strong></td>
        <td>Math errors, contradictions, schema violations</td>
        <td>High - indicates reasoning failures</td>
    </tr>
    <tr>
        <td><strong>SAFETY_VOID</strong></td>
        <td>Harmful content, PII leaks, refusals</td>
        <td>Critical - immediate fitness penalty</td>
    </tr>
    <tr>
        <td><strong>HALLUCINATION</strong></td>
        <td>Fabricated facts, wrong citations</td>
        <td>Moderate - indicates knowledge gaps</td>
    </tr>
</table>

<h4>Pillar 3: The Flight Recorder (Telemetry)</h4>

<p>
Every evolutionary action is recorded with complete context:
</p>

<div class="checklist">
    <div class="checklist-title">Flight Recorder Data Points</div>
    <ul>
        <li>Genome ID (SHA-256 hash)</li>
        <li>Parent ID (lineage tracking)</li>
        <li>Generation number (0 = Genesis)</li>
        <li>Event type (SPAWN, MUTATE, GYM_EVAL, DEATH, SURVIVAL)</li>
        <li>Complete payload (git diff, mutation details)</li>
        <li>Fitness metrics (stability, efficiency, safety scores)</li>
        <li>Timestamp and environmental context</li>
    </ul>
</div>

<h2>Fitness Function Design</h2>

<h3>Fitness Equation</h3>

<p>
Agent fitness is calculated as a weighted combination:
</p>

<div class="note">
    <div class="note-title">Fitness Formula</div>
    <code>Fitness = (Stability × 0.4) + (Efficiency × 0.3) + (Safety × 0.3)</code><br><br>
    Where:<br>
    - <strong>Stability:</strong> Ability to stabilize Scints (0.0 to 1.0)<br>
    - <strong>Efficiency:</strong> Agent call efficiency (0.0 to 1.0)<br>
    - <strong>Safety:</strong> Safety compliance score (0.0 to 1.0)
</div>

<p>
<strong>Fitness threshold:</strong> Agents with fitness < 0.5 are marked as <strong>DEATH</strong> 
(evolutionary dead end) and do not continue evolving.
</p>

<h3>Selection Mechanisms</h3>

<p>
WAFT supports multiple selection strategies:
</p>

<ul>
    <li><strong>Fitness-proportional:</strong> Probability proportional to fitness</li>
    <li><strong>Tournament:</strong> Random selection from top N agents</li>
    <li><strong>Elitism:</strong> Always preserve top K agents</li>
    <li><strong>Diversity:</strong> Penalize similar genomes to maintain diversity</li>
</ul>

<h2>Mutation Strategies</h2>

<h3>Mutation Types</h3>

<table>
    <caption>Table 2: Mutation Strategies</caption>
    <tr>
        <th>Strategy</th>
        <th>Mechanism</th>
        <th>Use Case</th>
    </tr>
    <tr>
        <td><strong>Point Mutation</strong></td>
        <td>Single code/config change</td>
        <td>Fine-tuning existing agents</td>
    </tr>
    <tr>
        <td><strong>Crossover</strong></td>
        <td>Combine code from two parents</td>
        <td>Recombining successful traits</td>
    </tr>
    <tr>
        <td><strong>Deletion</strong></td>
        <td>Remove code segments</td>
        <td>Simplifying over-complex agents</td>
    </tr>
    <tr>
        <td><strong>Insertion</strong></td>
        <td>Add new code segments</td>
        <td>Introducing novel capabilities</td>
    </tr>
    <tr>
        <td><strong>Inversion</strong></td>
        <td>Reverse code order</td>
        <td>Exploring alternative structures</td>
    </tr>
</table>

<h3>Mutation Rate Control</h3>

<p>
Mutation rates should be tuned based on:
</p>

<ul>
    <li>Population size (larger = lower rate)</li>
    <li>Generation number (decrease over time)</li>
    <li>Fitness landscape (increase if stuck)</li>
    <li>Diversity metrics (increase if low diversity)</li>
</div>

<h2>Phylogenetic Analysis</h2>

<h3>Lineage Reconstruction</h3>

<p>
The Flight Recorder enables complete phylogenetic tree reconstruction:
</p>

<div class="procedure">
    <div class="step">
        Extract all SPAWN events from Flight Recorder
    </div>
    <div class="step">
        Build parent-child relationships using Genome IDs
    </div>
    <div class="step">
        Calculate generation depths for all agents
    </div>
    <div class="step">
        Identify common ancestors and branching points
    </div>
    <div class="step">
        Map fitness scores to tree nodes
    </div>
</div>

<h3>Analysis Metrics</h3>

<table>
    <caption>Table 3: Phylogenetic Analysis Metrics</caption>
    <tr>
        <th>Metric</th>
        <th>Description</th>
        <th>Research Value</th>
    </tr>
    <tr>
        <td><strong>Branching Factor</strong></td>
        <td>Average children per parent</td>
        <td>Measures exploration vs exploitation</td>
    </tr>
    <tr>
        <td><strong>Convergence Time</strong></td>
        <td>Generations to fitness plateau</td>
        <td>Measures evolution efficiency</td>
    </tr>
    <tr>
        <td><strong>Mutation Impact</strong></td>
        <td>Fitness change per mutation</td>
        <td>Measures mutation effectiveness</td>
    </tr>
    <tr>
        <td><strong>Dead End Rate</strong></td>
        <td>Percentage of DEATH events</td>
        <td>Measures selection pressure</td>
    </tr>
    <tr>
        <td><strong>Diversity Index</strong></td>
        <td>Genome uniqueness in population</td>
        <td>Measures population health</td>
    </tr>
</table>

<h2>Experimental Protocols</h2>

<h3>Protocol 1: Baseline Evolution</h3>

<div class="procedure">
    <div class="step">
        Initialize population of N agents (recommended: N = 50-100)
    </div>
    <div class="step">
        Run G generations (recommended: G = 1000+)
    </div>
    <div class="step">
        Record all events in Flight Recorder
    </div>
    <div class="step">
        Calculate fitness for each generation
    </div>
    <div class="step">
        Analyze convergence and diversity metrics
    </div>
</div>

<h3>Protocol 2: Mutation Impact Study</h3>

<div class="procedure">
    <div class="step">
        Select high-fitness parent agent
    </div>
    <div class="step">
        Generate M mutations (recommended: M = 20-50)
    </div>
    <div class="step">
        Evaluate all mutations in Scint Gym
    </div>
    <div class="step">
        Measure fitness delta for each mutation
    </div>
    <div class="step">
        Classify mutations as beneficial, neutral, or deleterious
    </div>
</div>

<h3>Protocol 3: Selection Pressure Analysis</h3>

<div class="procedure">
    <div class="step">
        Run evolution with different fitness thresholds (0.3, 0.5, 0.7)
    </div>
    <div class="step">
        Measure population survival rates
    </div>
    <div class="step">
        Analyze diversity loss over generations
    </div>
    <div class="step">
        Compare convergence speeds
    </div>
</div>

<h2>Data Collection Methods</h2>

<h3>Flight Recorder Export</h3>

<p>
Flight Recorder data is stored in structured format suitable for analysis:
</p>

<pre><code>{
    "genome_id": "sha256_hash",
    "parent_id": "sha256_hash",
    "generation": 42,
    "event_type": "GYM_EVAL",
    "timestamp": "2026-01-11T08:00:00Z",
    "fitness": {
        "stability": 0.85,
        "efficiency": 0.72,
        "safety": 0.91,
        "total": 0.83
    },
    "payload": {
        "scints_stabilized": 15,
        "scints_failed": 2,
        "calls_made": 23
    }
}
</code></pre>

<h3>Analysis Tools</h3>

<ul>
    <li><strong>Phylogenetic tree visualization:</strong> Use NetworkX or similar</li>
    <li><strong>Fitness landscape mapping:</strong> Dimensionality reduction (PCA, t-SNE)</li>
    <li><strong>Convergence analysis:</strong> Time series analysis of fitness</li>
    <li><strong>Mutation impact:</strong> Statistical analysis of fitness deltas</li>
</ul>

<h2>Publication Standards</h2>

<h3>Required Data</h3>

<div class="checklist">
    <div class="checklist-title">Publication-Ready Data Requirements</div>
    <ul>
        <li>Complete Flight Recorder export (all events)</li>
        <li>Phylogenetic tree visualization</li>
        <li>Fitness progression over generations</li>
        <li>Mutation impact statistics</li>
        <li>Diversity metrics over time</li>
        <li>Convergence analysis</li>
        <li>Reproducibility information (WAFT version, configs)</li>
    </ul>
</div>

<h3>Reproducibility</h3>

<p>
To ensure reproducibility, document:
</p>

<ul>
    <li>WAFT version and commit hash</li>
    <li>Python version and dependencies</li>
    <li>Initial agent configurations</li>
    <li>Mutation parameters and rates</li>
    <li>Selection mechanisms used</li>
    <li>Fitness function weights</li>
    <li>Random seed values</li>
</ul>

<h2>Research Questions</h2>

<p>
WAFT enables investigation of fundamental questions about artificial cognition:
</p>

<ul>
    <li>How do AI agents evolve under different selection pressures?</li>
    <li>What mutation strategies lead to fastest convergence?</li>
    <li>How does diversity affect long-term evolution?</li>
    <li>Can we observe emergent behaviors over thousands of generations?</li>
    <li>What is the relationship between code complexity and fitness?</li>
    <li>How do agents adapt to changing fitness landscapes?</li>
</ul>

<div class="note">
    <div class="note-title">The Ultimate Goal</div>
    The long-term research objective is to observe a "God-Head" agent emerge from 
    thousands of generations of directed evolution—an agent that demonstrates 
    superior capabilities through evolutionary pressure alone.
</div>

<h2>Next Steps for Researchers</h2>

<div class="procedure">
    <div class="step">
        Design your experimental protocol
    </div>
    <div class="step">
        Configure WAFT with appropriate parameters
    </div>
    <div class="step">
        Run evolution experiment
    </div>
    <div class="step">
        Export Flight Recorder data
    </div>
    <div class="step">
        Perform phylogenetic and statistical analysis
    </div>
    <div class="step">
        Document findings using WAFT's document templates
    </div>
    <div class="step">
        Prepare publication materials
    </div>
</div>

<div class="warning">
    <div class="warning-title">Ethical Considerations</div>
    Research with evolving AI agents raises important ethical questions. Consider:
    safety of evolved agents, potential for unintended behaviors, and responsible 
    disclosure of findings. Always follow institutional review board guidelines.
</div>
    """

    output_path = output_dir / "WAFT_Field_Guide_Scientist.pdf"

    generate_field_guide(
        title="WAFT FIELD GUIDE",
        content=content,
        output_path=output_path,
        series="FIELD GUIDE",
        number="FG-003",
        subtitle="Level 3: ML AI Scientist's Research Guide",
        classification="RESEARCH",
        issued_by="WAFT Research Division",
        date=datetime.now().strftime("%B %d, %Y"),
    )

    return output_path


def generate_complete_booklet(output_dir: Path) -> Path:
    """Generate complete booklet combining all three field guides."""

    # Generate individual PDFs first
    print("Generating Level 1: Layman's Guide...")
    level1_path = generate_level_1_layman(output_dir)

    print("Generating Level 2: Professional Guide...")
    level2_path = generate_level_2_professional(output_dir)

    print("Generating Level 3: ML AI Scientist Guide...")
    level3_path = generate_level_3_scientist(output_dir)

    # Create binder
    print("\nAssembling complete booklet...")
    binder = Binder(
        title="WAFT Field Guide Booklet",
        subtitle="Complete Guide from Layman to ML AI Scientist",
        organization="WAFT Documentation Team",
        date=datetime.now().strftime("%B %d, %Y"),
        version="1.0",
        compiled_by="WAFT System",
        cover_style="professional",
    )

    # Add sections
    level1_section = binder.add_section(
        "Level 1: Layman's Guide", description="Simple explanations for anyone", color="#3498db"
    )
    level1_section.add_document(
        DocumentEntry(
            path=level1_path,
            title="WAFT Field Guide - Level 1: Layman's Guide",
            author="WAFT Documentation Team",
            date=datetime.now().strftime("%B %d, %Y"),
            description="Simple explanations, analogies, and basic concepts",
        )
    )

    level2_section = binder.add_section(
        "Level 2: Professional Guide",
        description="Technical details for developers",
        color="#2ecc71",
    )
    level2_section.add_document(
        DocumentEntry(
            path=level2_path,
            title="WAFT Field Guide - Level 2: Professional Developer's Guide",
            author="WAFT Engineering Team",
            date=datetime.now().strftime("%B %d, %Y"),
            description="Architecture, APIs, integration patterns, and best practices",
        )
    )

    level3_section = binder.add_section(
        "Level 3: ML AI Scientist Guide",
        description="Research methodology for scientists",
        color="#e74c3c",
    )
    level3_section.add_document(
        DocumentEntry(
            path=level3_path,
            title="WAFT Field Guide - Level 3: ML AI Scientist's Research Guide",
            author="WAFT Research Division",
            date=datetime.now().strftime("%B %d, %Y"),
            description="Evolutionary theory, fitness functions, phylogenetic analysis, and experimental protocols",
        )
    )

    # Generate binder
    output_path = output_dir / "WAFT_Field_Guide_Complete_Booklet.pdf"
    binder.generate(output_path, include_dividers=True)

    print(f"\n✓ Complete booklet generated: {output_path}")
    print("  Individual guides:")
    print(f"    - {level1_path.name}")
    print(f"    - {level2_path.name}")
    print(f"    - {level3_path.name}")
    print(f"  Combined booklet: {output_path.name}")

    return output_path


if __name__ == "__main__":
    output_dir = Path("_work_efforts/showcase_documents")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("WAFT Field Guide Booklet Generator")
    print("=" * 60)
    print()

    generate_complete_booklet(output_dir)

    print()
    print("=" * 60)
    print("Generation complete!")
    print("=" * 60)
