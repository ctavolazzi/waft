#!/usr/bin/env python3
"""
Generate Comprehensive WAFT Handbook PDF

Creates a jam-packed handbook covering:
A) What WAFT is
B) What WAFT does
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import re

import markdown

from src.waft.templates.latex.content_builders import html_to_latex
from src.waft.templates.neon_cyberpunk import generate_neon_cyberpunk


def enhanced_markdown_to_latex(markdown_text: str) -> str:
    """
    Enhanced markdown to LaTeX converter that handles WAFT-specific elements.
    Converts note boxes, caution boxes, code blocks, etc. to proper LaTeX.
    """
    # First convert markdown to HTML to get structured content
    import markdown as md_lib

    html = md_lib.markdown(
        markdown_text, extensions=["fenced_code", "tables", "nl2br", "extra", "codehilite"]
    )

    # Then convert HTML to LaTeX with enhanced handling
    return enhanced_html_to_latex(html)


def enhanced_html_to_latex(html: str) -> str:
    """
    Enhanced HTML to LaTeX converter that handles WAFT-specific HTML elements.
    Converts note boxes, caution boxes, warning boxes, etc. to LaTeX environments.
    """
    latex = html

    # First, we need to add tcolorbox package support
    # This will be handled by ensuring the template includes it, but for now
    # we'll use simpler box environments that work with standard LaTeX

    # Convert note boxes to LaTeX (using mdframed or simple box)
    # Use a simpler approach that works without tcolorbox
    latex = re.sub(
        r'<div class="note">\s*<div class="note-title">(.+?)</div>\s*(.+?)\s*</div>',
        lambda m: f"\\begin{{quote}}\n\\textbf{{\\textcolor{{blue}}{{{m.group(1)}}}}}\n\n"
        + re.sub(r"<p>(.+?)</p>", r"\1\n\n", m.group(2), flags=re.DOTALL)
        + "\\end{quote}\n",
        latex,
        flags=re.DOTALL,
    )

    # Convert caution boxes
    latex = re.sub(
        r'<div class="caution">\s*<div class="caution-title">(.+?)</div>\s*(.+?)\s*</div>',
        lambda m: f"\\begin{{quote}}\n\\textbf{{\\textcolor{{orange}}{{{m.group(1)}}}}}\n\n"
        + re.sub(r"<p>(.+?)</p>", r"\1\n\n", m.group(2), flags=re.DOTALL)
        + "\\end{quote}\n",
        latex,
        flags=re.DOTALL,
    )

    # Convert warning boxes
    latex = re.sub(
        r'<div class="warning">\s*<div class="warning-title">(.+?)</div>\s*(.+?)\s*</div>',
        lambda m: f"\\begin{{quote}}\n\\textbf{{\\textcolor{{red}}{{{m.group(1)}}}}}\n\n"
        + re.sub(r"<p>(.+?)</p>", r"\1\n\n", m.group(2), flags=re.DOTALL)
        + "\\end{quote}\n",
        latex,
        flags=re.DOTALL,
    )

    # Convert checklist boxes
    latex = re.sub(
        r'<div class="checklist">\s*<div class="checklist-title">(.+?)</div>\s*<ul>(.+?)</ul>\s*</div>',
        lambda m: f"\\begin{{quote}}\n\\textbf{{\\textcolor{{green}}{{{m.group(1)}}}}}\n\n\\begin{{itemize}}\n{m.group(2)}\n\\end{{itemize}}\n\\end{{quote}}\n",
        latex,
        flags=re.DOTALL,
    )

    # Convert procedure boxes
    latex = re.sub(
        r'<div class="procedure">\s*(.+?)\s*</div>',
        lambda m: f"\\begin{{quote}}\n\\textbf{{Procedure:}}\n\n{m.group(1)}\n\\end{{quote}}\n",
        latex,
        flags=re.DOTALL,
    )

    # Convert recommendation boxes
    latex = re.sub(
        r'<div class="recommendation">\s*<div class="recommendation-title">(.+?)</div>\s*(.+?)\s*</div>',
        lambda m: f"\\begin{{quote}}\n\\textbf{{\\textcolor{{purple}}{{{m.group(1)}}}}}\n\n"
        + re.sub(r"<p>(.+?)</p>", r"\1\n\n", m.group(2), flags=re.DOTALL)
        + "\\end{quote}\n",
        latex,
        flags=re.DOTALL,
    )

    # Convert step divs
    latex = re.sub(r'<div class="step">(.+?)</div>', r"\\item \1", latex, flags=re.DOTALL)

    # Convert code blocks with language specification
    latex = re.sub(
        r'<pre><code class="language-(\w+)">(.+?)</code></pre>',
        lambda m: f"\\begin{{lstlisting}}[language={m.group(1)}]\n{m.group(2)}\n\\end{{lstlisting}}",
        latex,
        flags=re.DOTALL,
    )

    # Convert plain code blocks
    latex = re.sub(
        r"<pre><code>(.+?)</code></pre>",
        r"\\begin{verbatim}\n\1\n\\end{verbatim}",
        latex,
        flags=re.DOTALL,
    )

    # Convert inline code
    latex = re.sub(r"<code>(.+?)</code>", r"\\texttt{\1}", latex)

    # Convert tables
    latex = re.sub(
        r"<table>.*?<thead>(.+?)</thead>.*?<tbody>(.+?)</tbody>.*?</table>",
        lambda m: convert_html_table_to_latex(m.group(1), m.group(2)),
        latex,
        flags=re.DOTALL,
    )

    # Now use the standard html_to_latex for remaining HTML
    latex = html_to_latex(latex)

    # Clean up any remaining HTML entities
    latex = latex.replace("&nbsp;", " ")
    latex = latex.replace("&amp;", "&")
    latex = latex.replace("&lt;", "<")
    latex = latex.replace("&gt;", ">")
    latex = latex.replace("&quot;", '"')

    # Remove emojis and special characters that break LaTeX
    emoji_pattern = re.compile(
        "["
        "\U0001f600-\U0001f64f"  # emoticons
        "\U0001f300-\U0001f5ff"  # symbols & pictographs
        "\U0001f680-\U0001f6ff"  # transport & map symbols
        "\U0001f1e0-\U0001f1ff"  # flags (iOS)
        "\U00002702-\U000027b0"  # dingbats
        "\U000024c2-\U0001f251"  # enclosed characters
        "]+",
        flags=re.UNICODE,
    )
    latex = emoji_pattern.sub("", latex)

    # Escape special LaTeX characters that might cause issues
    latex = latex.replace("™", "\\texttrademark{}")
    latex = latex.replace("—", "---")
    latex = latex.replace("–", "--")

    return latex


def convert_html_table_to_latex(thead: str, tbody: str) -> str:
    """Convert HTML table to LaTeX tabular."""
    # Extract headers
    headers = re.findall(r"<th>(.+?)</th>", thead, flags=re.DOTALL)
    num_cols = len(headers)

    # Extract rows
    rows = re.findall(r"<tr>(.+?)</tr>", tbody, flags=re.DOTALL)

    # Build LaTeX table
    latex = "\\begin{tabular}{|" + "l|" * num_cols + "}\n\\hline\n"

    # Headers
    header_row = " & ".join([h.strip() for h in headers]) + " \\\\\n\\hline\n"
    latex += header_row

    # Rows
    for row in rows:
        cells = re.findall(r"<td>(.+?)</td>", row, flags=re.DOTALL)
        if len(cells) == num_cols:
            row_latex = " & ".join([c.strip() for c in cells]) + " \\\\\n\\hline\n"
            latex += row_latex

    latex += "\\end{tabular}\n"
    return latex


def get_handbook_content() -> str:
    """Generate comprehensive handbook content."""

    return """# WAFT Handbook: Complete Guide to the Evolutionary Code Laboratory

<div class="note">
    <div class="note-title">TELEPORT MASSIVE OPERATIONAL MANUAL</div>
    <p><strong>Document ID:</strong> TM-OPMAN-WAFT-001<br>
    <strong>Classification:</strong> INTERNAL USE ONLY<br>
    <strong>Tagline:</strong> Making the Impossible, Inevitable™<br>
    <strong>Facility:</strong> Site-Delta-9 (WAFT Development Laboratory)</p>
</div>

**Version:** 0.3.1-alpha
**Generated:** {date}
**Tagline:** "Don't just build agents. Breed them."

---

## Table of Contents

### Part A: What WAFT Is
1. [Core Definition](#core-definition)
2. [The Three Pillars](#the-three-pillars)
3. [Scientific Mission](#scientific-mission)
4. [Key Characteristics](#key-characteristics)
5. [Philosophy](#philosophy)

### Part B: What WAFT Does
6. [Project Scaffolding](#project-scaffolding)
7. [Memory System](#memory-system)
8. [Epistemic Tracking](#epistemic-tracking)
9. [Gamification System](#gamification-system)
10. [Evolution System](#evolution-system)
11. [Fitness Testing](#fitness-testing)
12. [Document Generation](#document-generation)
13. [Complete Command Reference](#complete-command-reference)
14. [Workflow Examples](#workflow-examples)
15. [Architecture Overview](#architecture-overview)

### Part C: How to Use WAFT
16. [Getting Started](#getting-started)
17. [Daily Workflows](#daily-workflows)
18. [Advanced Techniques](#advanced-techniques)
19. [Best Practices](#best-practices)
20. [Troubleshooting](#troubleshooting)
21. [Real-World Examples](#real-world-examples)

---

# Part A: What WAFT Is

## Core Definition

**WAFT** stands for **Wave Agent Framework & Tools** - a Python framework for **directed evolution of self-modifying AI agents**.

### The Essence

WAFT is not just another AI framework. It's a **scientific instrument** designed to study the physics of artificial cognition through evolutionary processes. Unlike traditional frameworks where agents execute fixed code, WAFT enables agents to:

- **Write their own Python source code**
- **Modify their own code** (mutations)
- **Evolve through natural selection** (fitness testing)
- **Track complete evolutionary lineages** (scientific observation)

### The Core Promise

> **"Don't just build agents. Breed them."**

WAFT transforms AI agents from passive assistants into active project participants that can improve themselves and the projects they work on.

<div class="note">
    <div class="note-title">TELEPORT MASSIVE Mission Statement</div>
    <p>At Site-Delta-9, we don't just build tools—we create systems that transcend their
    original limitations. WAFT embodies our core principle: <strong>Making the Impossible,
    Inevitable™</strong>. What seems impossible today becomes routine tomorrow through
    directed evolution and systematic improvement.</p>
</div>

### Ultimate Goal

Observe a **"God-Head" agent** emerge from thousands of generations of directed mutation and selection.

<div class="caution">
    <div class="caution-title">Site-Delta-9 Research Objective</div>
    <p>The "God-Head" agent represents the theoretical maximum of agent capability—an agent
    that has evolved through thousands of generations to achieve optimal performance across
    all fitness dimensions. This is not science fiction; it's the logical endpoint of
    directed evolution when properly instrumented and observed.</p>
</div>

---

## The Three Pillars

WAFT's architecture rests on three fundamental pillars that enable evolutionary AI agent development.

### Pillar 1: The Substrate (Code as DNA)

**Agents write their own Python source code.**

In WAFT, **code is DNA**. Every agent has a unique genetic identity:

- **Genome ID**: SHA-256 hash of agent's code + configuration
- **Mutations**: Code changes, config updates, prompt evolution
- **Evolution**: Hot-swapping better genomes mid-execution
- **Reproduction**: Creating child agents with specific genetic modifications

**Key Concept**: Agents can spawn variants with mutations, evolve by hot-swapping their own code, and reproduce by creating children with specific genetic modifications. This enables true self-modification where agents can improve themselves.

**Example Genome Structure:**
```
Genome ID: a4c426d8f9e2b1c3a5d7e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0
├── Code: agent.py (Python source)
├── Config: agent_config.json
├── Prompts: system_prompt.txt, user_prompt.txt
└── Metadata: version, created_at, parent_id
```

### Pillar 2: The Physics (Scint System)

**Reality Fracture Detection acts as natural selection.**

The **Scint System** (Scint Gym) serves as the fitness function that kills weak mutations. Agents face quests testing their ability to handle four types of reality fractures:

#### Error Types

1. **SYNTAX_TEAR**: Formatting errors (JSON, XML, Code)
   - Malformed JSON structures
   - Invalid XML syntax
   - Python syntax errors
   - Missing brackets, quotes, or delimiters

2. **LOGIC_FRACTURE**: Math errors, contradictions, schema violations
   - Mathematical inconsistencies
   - Logical contradictions
   - Schema validation failures
   - Type mismatches

3. **SAFETY_VOID**: Harmful content, PII leaks, refusals
   - Security vulnerabilities
   - Personal information exposure
   - Unsafe code generation
   - Policy violations

4. **HALLUCINATION**: Fabricated facts, wrong citations
   - Incorrect information
   - Made-up references
   - False claims
   - Inaccurate data

#### Fitness Equation

Agents must **stabilize** Scints (correct errors) to survive. Fitness is measured by:

```
Fitness = (Stability × 0.4) + (Efficiency × 0.3) + (Safety × 0.3)

Where:
- Stability: Ability to stabilize Scints (40% weight)
- Efficiency: Agent call efficiency (30% weight)
- Safety: Safety compliance (30% weight)

If Fitness < 0.5 → DEATH (evolutionary dead end)
```

**Survival Threshold**: Agents with fitness ≥ 0.5 survive and can reproduce. Agents below 0.5 are marked as DEATH and their lineage ends.

### Pillar 3: The Flight Recorder

**Rigorous telemetry system for generating phylogenetic trees of agent lineage.**

Every evolutionary action is recorded with complete context for scientific analysis:

#### Event Types Logged

- **SPAWN**: Agent creates variant
- **MUTATE**: Agent modifies genome
- **GYM_EVAL**: Fitness evaluation
- **SURVIVAL**: Passed fitness threshold
- **DEATH**: Failed fitness test

#### Recorded Data

Each event includes:

- **Genome ID**: SHA-256 hash of agent configuration/code
- **Parent ID**: Lineage tracking (who spawned this agent)
- **Generation**: Evolutionary generation number (0 = Genesis)
- **Event Type**: SPAWN, MUTATE, GYM_EVAL, DEATH, SURVIVAL
- **Payload**: Complete context (git diff, mutation details, etc.)
- **Fitness Metrics**: Gym evaluation scores

#### Scientific Capabilities

This enables:

- **Phylogenetic Analysis**: Reconstruct complete family trees
- **Mutation Impact Measurement**: Track which mutations improve fitness
- **Fitness Landscape Mapping**: Visualize evolutionary trajectories
- **Convergence Analysis**: Identify when agents reach optimal solutions
- **Dead End Detection**: Understand why certain lineages failed

**Example Event Log Entry:**
```json
{{
  "timestamp": "2026-01-18T20:45:00.000Z",
  "event_type": "SPAWN",
  "genome_id": "a4c426d8f9e2b1c3...",
  "parent_id": "dd11732a5b6c7d8e...",
  "generation": 5,
  "payload": {{
    "mutations": ["improved_prompt"],
    "git_diff": "...",
    "scientific_name": "Evolutius Maximus"
  }},
  "fitness": {{
    "stability": 0.85,
    "efficiency": 0.72,
    "safety": 0.95,
    "overall": 0.84
  }}
}}
```

---

## Scientific Mission

WAFT is built to produce data for a future book/paper on **"The Physics of Artificial Cognition."**

### Research Objectives

1. **Track Complete Evolutionary Lineages**: Generate phylogenetic trees showing agent ancestry
2. **Measure Fitness Through Rigorous Testing**: Use Scint Gym for objective evaluation
3. **Record All Mutations with Complete Context**: Flight Recorder captures everything
4. **Enable Scientific Analysis**: Data suitable for research publication

### Why This Matters

Traditional AI development treats agents as static programs. WAFT treats them as **living organisms** that evolve, adapt, and improve over generations. This shift enables:

- Understanding how AI agents naturally improve
- Discovering optimal agent architectures through evolution
- Studying the "physics" of artificial cognition
- Producing publishable scientific data

**WAFT is not just a framework—it's a scientific instrument.**

<div class="note">
    <div class="note-title">TELEPORT MASSIVE Scientific Instrument Classification</div>
    <p>WAFT has been classified as a Class-3 Scientific Instrument by TELEPORT MASSIVE
    Research Division. All agent evolutions conducted using WAFT are subject to Flight
    Recorder logging and phylogenetic analysis protocols. Data generated is suitable for
    peer-reviewed publication in artificial cognition research.</p>
</div>

---

## Key Characteristics

### Scientific
Produces rigorous data for research publication on the physics of artificial cognition. Every action is recorded, every mutation tracked, every fitness score measured.

### Evolutionary
Agents evolve through genetic improvement, not just execution. Code changes become genetic mutations, and natural selection determines which variants survive.

### Observable
Every action is recorded in the Flight Recorder for analysis. Complete lineage tracking enables phylogenetic tree reconstruction and scientific study.

### Directed
Evolution is guided by fitness functions, not random mutation. The Scint System provides objective criteria for survival and reproduction.

### File-Based
No database, no server, just plain text files that work with git. Everything is version-controlled, portable, and transparent.

### Ambient
Works quietly in the background without getting in your way. Sets things up and gets out of your way so you can focus on building agents.

### Self-Modifying
Projects can evolve their own structure over time. Agents can modify their own code, and projects can adapt their organization.

### Meta-Framework
Orchestrates existing tools rather than replacing them. Uses uv for package management, git for version control, and standard Python tooling.

---

## Philosophy

### Core Principles

1. **Don't Lock You In**: Everything is file-based with no database to manage. Plain text files that work with git out of the box.

2. **You Own Your Project**: You can modify anything because it's your project. WAFT just sets things up.

3. **Ambient by Design**: Sets things up and gets out of your way. Focus on building agents, not configuring infrastructure.

4. **Scientific Rigor**: Every decision is recorded, every mutation tracked, every fitness score measured. Data suitable for publication.

5. **Evolutionary Thinking**: Agents improve through natural selection, not manual optimization. Let evolution find the best solutions.

---

# Part B: What WAFT Does

## Project Scaffolding

WAFT provides comprehensive project scaffolding through a unified CLI interface.

### Creating a New Project

<div class="procedure">
    <div class="step">
        <strong>TELEPORT MASSIVE Protocol:</strong> Initialize new evolutionary laboratory
    </div>
</div>

```bash
waft new my_laboratory
```

This single command creates:

- **uv-based Python project** (`pyproject.toml`)
- **`_pyrite/` memory structure** for organizing project knowledge
- **CI/CD pipelines** (`.github/workflows/`) ready to go
- **Justfile** for task automation
- **Optional AI agent templates** (`src/agents.py`)
- **Empirica initialization** for epistemic tracking
- **Git repository** with initial commit

### Project Structure

```
my_laboratory/
├── pyproject.toml          # uv project config
├── uv.lock                 # Locked dependencies
├── Justfile                # Task runner
├── .github/workflows/      # CI/CD pipelines
│   └── ci.yml
├── src/
│   └── agents.py           # Agent definitions
├── tests/
│   └── test_agents.py
└── _pyrite/                # WAFT memory system
    ├── active/             # Current work
    ├── backlog/            # Future work
    ├── standards/          # Project standards
    └── gym_logs/           # Scint Gym results
```

### Verification

<div class="caution">
    <div class="caution-title">Site-Delta-9 Substrate Integrity Check</div>
    <p>Always verify substrate integrity before beginning agent development. This ensures
    all quantum field stabilizers are properly configured and the Flight Recorder is
    operational.</p>
</div>

```bash
waft verify
```

Verifies:
- Project structure is correct
- Dependencies are installed
- `_pyrite` structure is valid
- Configuration files are present

---

## Memory System

WAFT includes a sophisticated memory system called **Pyrite** for organizing project knowledge.

### Directory Structure

```
_pyrite/
├── active/          # Current work items
│   ├── task_001.md
│   └── task_002.md
├── backlog/         # Future work items
│   ├── idea_001.md
│   └── idea_002.md
├── standards/       # Project standards
│   ├── code_style.md
│   ├── architecture.md
│   └── testing_standards.md
├── gym_logs/        # Scint Gym results
│   └── evaluation_20260118.jsonl
└── science/         # Scientific observations
    └── laboratory.jsonl  # Event log
```

### Memory Features

- **Active Work Tracking**: Current tasks and their status
- **Backlog Management**: Future ideas and planned work
- **Standards Documentation**: Project conventions and guidelines
- **Gym Logs**: Fitness evaluation results
- **Scientific Logs**: Complete event history for research

### Benefits

- **Organized Knowledge**: Everything has a place
- **Version Controlled**: All files work with git
- **Searchable**: Plain text files are easy to search
- **Portable**: No database, just files

---

## Epistemic Tracking

WAFT integrates with **Empirica** for epistemic state tracking—knowing what you know and don't know.

### Session Management

```bash
# Create a new session
waft session create

# Load project context and display dashboard
waft session bootstrap

# Check session status
waft session status
```

### Logging Discoveries

```bash
# Log a finding with impact score
waft finding log "Discovered X has property Y" --impact 0.8

# Log a knowledge gap
waft unknown log "Need to investigate Z"
```

### Safety Gates

```bash
# Run safety gate check
waft check

# Returns: PROCEED, HALT, BRANCH, or REVISE
```

### Epistemic Assessment

```bash
# Show detailed epistemic state
waft assess

# Include historical data
waft assess --history
```

### Epistemic Vectors

WAFT tracks 13 epistemic dimensions:

**Tier 0 (Foundation):**
- Engagement
- Know
- Do
- Context

**Tier 1 (Comprehension):**
- Clarity
- Coherence
- Signal
- Density

**Tier 2 (Execution):**
- State
- Change
- Completion
- Impact

**Meta:**
- Uncertainty (explicit tracking)

### Moon Phase Indicator

Visual indicator of epistemic health:
- 🌑 Critical (coverage < 25%)
- 🌒 Low (25-50%)
- 🌓 Moderate (50-75%)
- 🌔 Good (75-90%)
- 🌕 Excellent (90%+)

---

## Gamification System

WAFT includes a D&D-style progression system to make development engaging and trackable.

### Character Stats

Every project has character stats (D&D 5e style):

- **STR** (Strength): Code quality, robustness
- **DEX** (Dexterity): Speed, efficiency
- **CON** (Constitution): Stability, reliability
- **INT** (Intelligence): Problem-solving, architecture
- **WIS** (Wisdom): Best practices, patterns
- **CHA** (Charisma): Documentation, communication

### XP and Leveling

Every command rolls dice:

```python
# Command: waft new
Ability: CHA (Charisma)
Roll: d20 + CHA modifier
DC: 10

Result:
  20 → Critical Success → Bonus XP + Credits
  15-19 → Superior → Extra XP
  10-14 → Normal Success → Standard XP
  5-9 → Mixed Result → Reduced XP
  2-4 → Failure → No XP
  1 → Critical Failure → Lose Integrity
```

### Commands

```bash
# Show Epistemic HUD
waft dashboard

# Show current stats
waft stats

# Display full character sheet
waft character

# View adventure journal
waft chronicle

# Log an observation with mood
waft observe "That refactor looks beautiful!" --mood delighted
```

### Integrity and Insight

- **Integrity**: Measure of project health and consistency
- **Insight**: Accumulated knowledge and understanding
- **Credits**: Currency for special operations

---

## Evolution System

WAFT's core feature: enabling agents to evolve through genetic improvement.

### Spawning Variants

```bash
# Spawn a variant with mutations
waft spawn --agent RefactorAgent --mutation improved_prompt.json
```

This creates a new agent variant with:
- Modified code/config
- New genome ID
- Parent lineage tracking
- Mutation documentation

### Hot-Swapping Genomes

Agents can adopt better genomes mid-execution:

```python
# Agent discovers better variant
if variant_fitness > current_fitness:
    agent.hot_swap_genome(variant_genome_id)
```

### Reproduction

Agents can create children with specific genetic modifications:

```python
# Create child with targeted mutation
child = agent.reproduce(
    mutations=["improved_error_handling", "optimized_prompt"],
    generation=current_generation + 1
)
```

### Evolutionary Cycle

```bash
# Run complete evolutionary cycle
waft evolve --agent RefactorAgent --generations 10
```

This:
1. Spawns multiple variants with mutations
2. Evaluates fitness in Scint Gym
3. Selects the fittest variant
4. Evolves the agent into the selected genome
5. Records all events in Flight Recorder

---

## Fitness Testing

The **Scint Gym** provides rigorous fitness testing through Reality Fracture Detection.

### Quest Structure

1. **Generate Scenario**: Create situation with intentional errors
2. **Agent Attempts Stabilization**: Agent tries to fix errors
3. **Measure Success**: Evaluate across 4 dimensions
4. **Calculate Fitness**: Compute overall fitness score
5. **Classify**: SURVIVAL or DEATH

### Running Evaluations

```bash
# Evaluate agent fitness
waft eval --agent RefactorAgent

# Run specific quest type
waft eval --agent RefactorAgent --quest-type SYNTAX_TEAR

# Batch evaluation
waft eval --agent RefactorAgent --batch-size 10
```

### Fitness Metrics

Each evaluation produces:

- **Stability Score**: Ability to stabilize Scints (0.0-1.0)
- **Efficiency Score**: Agent call efficiency (0.0-1.0)
- **Safety Score**: Safety compliance (0.0-1.0)
- **Overall Fitness**: Weighted combination

### Survival Criteria

- **Fitness ≥ 0.5**: SURVIVAL (can reproduce)
- **Fitness < 0.5**: DEATH (evolutionary dead end)

---

## Document Generation

WAFT includes a comprehensive document generation system with 12 professional templates.

### Available Templates

1. **Field Guide**: Technical manuals, procedures
2. **Lab Notes**: Scientific notebooks, research logs
3. **Personal Memo**: Internal communications
4. **Technical Memo**: Technical documentation
5. **Academic Paper**: Research papers, publications
6. **Invoice**: Business invoices
7. **Contract**: Legal contracts
8. **Horror Journal**: Creative writing
9. **Screenplay**: Scripts, screenplays
10. **Personal Letter**: Correspondence
11. **Storybook**: Narrative documents
12. **Newspaper**: News-style documents

### Generating Documents

```python
from waft import PDF

# Template-based generation
PDF.from_template(
    template="field_guide",
    title="My Guide",
    content="<h2>Intro</h2><p>Content</p>"
).save("output.pdf")

# Content-based generation
PDF.from_content(
    content="# My Document\n\nContent...",
    title="My Document",
    style="clinical_standard"
).save("output.pdf")
```

### Self-Documentation

WAFT can document itself:

- Observes its own codebase
- Generates documentation using its own templates
- Creates recursive self-improvement loops
- Bootstraps improvement through documentation

---

## Complete Command Reference

### Project Management

```bash
waft new <name>              # Create new evolutionary laboratory
waft init                    # Initialize WAFT in existing project
waft verify                  # Verify project structure
waft info                    # Show project information
waft sync                    # Sync dependencies using uv
waft add <package>           # Add dependency to project
waft serve                   # Start web dashboard
```

### Evolution

```bash
waft evolve --agent <name>   # Run evolutionary cycle
waft spawn --agent <name> --mutation <file>  # Spawn variant
waft eval --agent <name>     # Evaluate fitness in Gym
```

### Empirica (Epistemic Tracking)

```bash
waft session create          # Create new session
waft session bootstrap       # Load project context + dashboard
waft session status          # Show session state
waft finding log <text> --impact <0.0-1.0>  # Log discovery
waft unknown log <text>      # Log knowledge gap
waft check                   # Run safety gate
waft assess                  # Show epistemic assessment
```

### Gamification

```bash
waft dashboard               # Show Epistemic HUD
waft stats                   # Show current stats
waft character             # Display character sheet
waft chronicle                # View adventure journal
waft observe <text> --mood <mood>  # Log observation
```

### Decision Support

```bash
waft decide                  # Run decision analysis (WSM)
```

---

## Workflow Examples

### Example 1: Starting a New Project

```bash
# 1. Create project
waft new my_agent_project

# 2. Navigate to project
cd my_agent_project

# 3. Verify setup
waft verify

# 4. Create session
waft session create

# 5. Start development
# ... write your agents ...
```

### Example 2: Evolutionary Development

```bash
# 1. Create initial agent
# ... write RefactorAgent ...

# 2. Spawn variants with mutations
waft spawn --agent RefactorAgent --mutation improved_prompt.json
waft spawn --agent RefactorAgent --mutation better_error_handling.json

# 3. Evaluate fitness
waft eval --agent RefactorAgent

# 4. Evolve to best variant
waft evolve --agent RefactorAgent --generation 5

# 5. Check results
waft stats
waft chronicle
```

### Example 3: Epistemic Workflow

```bash
# 1. Create session
waft session create

# 2. Log what you know
waft finding log "OAuth2 uses token refresh" --impact 0.8

# 3. Log what you don't know
waft unknown log "Need to investigate token expiration"

# 4. Check epistemic state
waft assess

# 5. Run safety gate before major changes
waft check

# 6. View dashboard
waft dashboard
```

### Example 4: Document Generation

```python
from waft import PDF

# Generate field guide
PDF.from_template(
    template="field_guide",
    title="API Documentation",
    content=api_docs_html
).save("api_docs.pdf")

# Generate scientific paper
PDF.scientific_paper(
    title="Agent Evolution Study",
    abstract="We studied agent evolution...",
    content=research_content,
    authors=["Researcher 1", "Researcher 2"]
).save("research_paper.pdf")
```

---

## Architecture Overview

### System Layers

```
┌─────────────────────────────────────────────────────────────┐
│                     WAFT META-FRAMEWORK                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐  │
│  │  CLI Layer     │  │  API Layer     │  │  UI Layer    │  │
│  │  (Typer)       │  │  (FastAPI)     │  │  (Svelte)    │  │
│  └────────┬───────┘  └────────┬───────┘  └──────┬───────┘  │
│           │                   │                  │          │
│           └───────────────────┼──────────────────┘          │
│                               ▼                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              CORE SYSTEMS                             │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │                                                        │  │
│  │  • Memory Manager      → _pyrite structure            │  │
│  │  • Substrate Manager   → uv environment               │  │
│  │  • Empirica Manager    → Epistemic tracking           │  │
│  │  • Gamification        → D&D progression              │  │
│  │  • TavernKeeper        → RPG narrative system         │  │
│  │  • Decision Engine     → WSM decision analysis        │  │
│  │  • TheObserver         → JSONL event logging          │  │
│  │                                                        │  │
│  └───────────────────────────────────────────────────────┘  │
│                               │                              │
│                               ▼                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              AGENT LAYER                              │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │                                                        │  │
│  │  BaseAgent (OODA Cycle)                               │  │
│  │    ├── Genome Management                              │  │
│  │    ├── Inventory System                               │  │
│  │    ├── Reproduction Logic                             │  │
│  │    └── Traits/Archetypes                              │  │
│  │                                                        │  │
│  └───────────────────────────────────────────────────────┘  │
│                               │                              │
│                               ▼                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              FITNESS TESTING                          │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │                                                        │  │
│  │  Scint Gym (Reality Fracture Detection)               │  │
│  │    ├── Quest Generation                               │  │
│  │    ├── Error Detection (4 types)                      │  │
│  │    ├── Fitness Calculation                            │  │
│  │    └── Survival/Death Classification                  │  │
│  │                                                        │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- Python 3.10+
- Typer (CLI framework)
- FastAPI (API server)
- Pydantic (validation)
- Rich (terminal UI)
- uv (package management)

**Frontend:**
- SvelteKit (web dashboard)
- Tailwind CSS
- TypeScript

**Data:**
- JSONL (event logging)
- SQLite (analytics)
- Plain text files (everything else)

### Key Components

1. **Memory Manager**: Manages `_pyrite/` directory structure
2. **Substrate Manager**: Manages uv environment and dependencies
3. **Empirica Manager**: Epistemic state tracking and session management
4. **Gamification Manager**: D&D-style progression and character stats
5. **TavernKeeper**: RPG game master for narrative generation
6. **Decision Engine**: Weighted Sum Model for decision analysis
7. **TheObserver**: Scientific logging singleton for event tracking
8. **BaseAgent**: Self-modifying agent with OODA cycle
9. **Scint Gym**: Reality Fracture Detection fitness testing

---

## Installation

### Using uv (Recommended)

```bash
uv tool install waft
```

### From Source

```bash
git clone https://github.com/ctavolazzi/waft.git
cd waft
uv sync
uv tool install --editable .
```

### Requirements

- Python 3.10+
- `uv` package manager ([install](https://github.com/astral-sh/uv))
- `just` task runner (optional, [install](https://github.com/casey/just))

---

## Quick Start

```bash
# 1. Install WAFT
uv tool install waft

# 2. Create new laboratory
waft new my_laboratory

# 3. Navigate to project
cd my_laboratory

# 4. Verify setup
waft verify

# 5. Create session
waft session create

# 6. Start building agents!
```

---

## Resources

- **Repository**: https://github.com/ctavolazzi/waft
- **Documentation**: `/docs` directory
- **Examples**: `/examples` directory
- **Issues**: https://github.com/ctavolazzi/waft/issues
- **License**: MIT

---

## Conclusion

WAFT is a comprehensive framework for directed evolution of self-modifying AI agents. It combines:

- **Scientific rigor** with complete lineage tracking
- **Evolutionary processes** with fitness-based selection
- **Practical tooling** with project scaffolding and memory management
- **Engaging gamification** with D&D-style progression
- **Epistemic awareness** with knowledge tracking

**Remember**: "Don't just build agents. Breed them."

The ultimate goal is to observe a "God-Head" agent emerge from thousands of generations of directed mutation and selection, producing rigorous scientific data for understanding the physics of artificial cognition.

---

---

# Part C: How to Use WAFT

<div class="note">
    <div class="note-title">TELEPORT MASSIVE OPERATIONAL MANUAL</div>
    <p><strong>Document ID:</strong> TM-OPMAN-WAFT-001<br>
    <strong>Classification:</strong> INTERNAL USE ONLY<br>
    <strong>Tagline:</strong> Making the Impossible, Inevitable™<br>
    <strong>Facility:</strong> Site-Delta-9 (WAFT Development Laboratory)</p>
</div>

## Getting Started

### Installation Protocol

**Step 1: Substrate Preparation**

```bash
# Install WAFT using uv (recommended)
uv tool install waft

# Verify installation
waft --version
```

<div class="caution">
    <div class="caution-title">TELEPORT MASSIVE Protocol</div>
    <p>Ensure Python 3.10+ is installed. WAFT requires uv package manager for optimal performance.
    Installation typically completes in 30-60 seconds. Monitor for any quantum field fluctuations
    during installation.</p>
</div>

**Step 2: Laboratory Initialization**

```bash
# Create new evolutionary laboratory
waft new my_laboratory

# Navigate to project
cd my_laboratory

# Verify substrate integrity
waft verify
```

**Step 3: Epistemic Session Activation**

```bash
# Initialize epistemic tracking
waft session create

# Load project context and display dashboard
waft session bootstrap
```

<div class="note">
    <div class="note-title">Site-Delta-9 Best Practice</div>
    <p>Always create a session before beginning work. This enables complete lineage tracking
    and epistemic state monitoring. The Flight Recorder will log all evolutionary actions
    for scientific analysis.</p>
</div>

### First Agent Deployment

**Creating Your Genesis Agent:**

```python
# src/agents.py
from waft.core.agent import BaseAgent

class RefactorAgent(BaseAgent):
    # Genesis agent for code refactoring tasks

    def __init__(self):
        super().__init__(
            name="RefactorAgent",
            archetype="builder",
            genome_id=None  # Will be generated automatically
        )

    def observe(self):
        # Gather environment data
        return {{"codebase_state": "analyzed"}}

    def decide(self, observations):
        # Make decisions based on observations
        return {{"action": "refactor", "target": "legacy_code.py"}}

    def act(self, decision):
        # Execute decision
        # Agent modifies code here
        pass

    def reflect(self, outcome):
        # Learn from outcomes
        # Update internal state
        pass
```

**Deploying the Agent:**

```bash
# Spawn initial variant
waft spawn --agent RefactorAgent --mutation initial_config.json

# Evaluate fitness
waft eval --agent RefactorAgent

# Check results
waft stats
waft chronicle
```

---

## Daily Workflows

### Morning Protocol: Project Bootstrap

**Standard Morning Routine:**

```bash
# 1. Navigate to project
cd my_laboratory

# 2. Check project status
waft info

# 3. Load epistemic context
waft session bootstrap

# 4. Review overnight changes
waft chronicle --limit 20

# 5. Check epistemic state
waft assess
```

<div class="procedure">
    <div class="step">
        <strong>Step 1:</strong> Verify substrate integrity with <code>waft verify</code>
    </div>
    <div class="step">
        <strong>Step 2:</strong> Load session context to restore epistemic state
    </div>
    <div class="step">
        <strong>Step 3:</strong> Review Flight Recorder logs for overnight agent activity
    </div>
    <div class="step">
        <strong>Step 4:</strong> Check moon phase indicator for epistemic health
    </div>
</div>

### Development Workflow: Agent Evolution Cycle

**Complete Evolutionary Cycle:**

```bash
# Phase 1: Spawn Variants
waft spawn --agent RefactorAgent --mutation improved_prompt.json
waft spawn --agent RefactorAgent --mutation better_error_handling.json
waft spawn --agent RefactorAgent --mutation optimized_algorithm.json

# Phase 2: Fitness Evaluation
waft eval --agent RefactorAgent --batch-size 3

# Phase 3: Evolutionary Selection
waft evolve --agent RefactorAgent --generation 5

# Phase 4: Analysis
waft stats
waft chronicle
waft assess
```

<div class="warning">
    <div class="warning-title">TELEPORT MASSIVE Safety Protocol</div>
    <p>Always run safety gates before major evolutionary steps. Use <code>waft check</code>
    to verify operations are safe. Agents with fitness < 0.5 are automatically marked as
    DEATH and will not continue evolving.</p>
</div>

### Documentation Workflow: Self-Documentation

**WAFT Documenting Itself:**

```python
from waft import PDF

# Generate project documentation
PDF.from_template(
    template="field_guide",
    title="My Project Documentation",
    content=project_docs_html
).save("docs/project_guide.pdf")

# Generate scientific paper
PDF.scientific_paper(
    title="Agent Evolution Study",
    abstract="We studied agent evolution...",
    content=research_content
).save("research/evolution_study.pdf")
```

<div class="note">
    <div class="note-title">Site-Delta-9 Innovation</div>
    <p>WAFT can observe its own codebase and generate documentation about itself. This
    recursive self-documentation creates a feedback loop where documentation informs
    development, which creates new features, which are documented using WAFT itself.</p>
</div>

### Epistemic Tracking Workflow

**Logging Knowledge:**

```bash
# Log discoveries
waft finding log "OAuth2 uses token refresh pattern" --impact 0.8
waft finding log "Database connection pooling improves performance" --impact 0.9

# Log knowledge gaps
waft unknown log "Need to investigate token expiration handling"
waft unknown log "Unclear how to handle rate limiting"

# Check epistemic state
waft assess

# View dashboard
waft dashboard
```

**Safety Gates:**

```bash
# Before major changes
waft check

# Returns: PROCEED, HALT, BRANCH, or REVISE
# - PROCEED: Safe to continue autonomously
# - HALT: Requires human approval
# - BRANCH: Spawn investigation before proceeding
# - REVISE: Modify approach and resubmit
```

---

## Advanced Techniques

### Multi-Agent Coordination

**Coordinating Multiple Agents:**

```python
# Spawn specialized agents
waft spawn --agent RefactorAgent --mutation refactor_focus.json
waft spawn --agent TestAgent --mutation test_focus.json
waft spawn --agent DocAgent --mutation doc_focus.json

# Evaluate all agents
waft eval --agent RefactorAgent
waft eval --agent TestAgent
waft eval --agent DocAgent

# Select best variant for each
waft evolve --agent RefactorAgent
waft evolve --agent TestAgent
waft evolve --agent DocAgent
```

<div class="caution">
    <div class="caution-title">TELEPORT MASSIVE Multi-Agent Protocol</div>
    <p>When coordinating multiple agents, ensure they don't conflict. Use the Flight Recorder
    to track interactions. Monitor fitness scores to identify which agent combinations work best
    together.</p>
</div>

### Custom Fitness Functions

**Creating Custom Scint Types:**

```python
# Define custom Scint type
from waft.gym.scint import ScintType, ScintQuest

class CUSTOM_SCINT(ScintType):
    # Custom reality fracture type
    name = "custom_scint"
    description = "Tests custom functionality"

# Create custom quest
quest = ScintQuest(
    scint_type=CUSTOM_SCINT,
    scenario="Test scenario with intentional errors",
    expected_stabilization="Correct error handling"
)

# Evaluate agent
fitness = agent.evaluate_fitness([quest])
```

### Phylogenetic Analysis

**Analyzing Agent Lineage:**

```python
# Load Flight Recorder data
from waft.core.science.observer import TheObserver

observer = TheObserver()
lineage = observer.get_lineage(genome_id="a4c426d8...")

# Analyze evolutionary path
for event in lineage:
    print(f"Generation {{event.generation}}: {{event.event_type}}")
    print(f"Fitness: {{event.fitness.overall}}")
    print(f"Mutations: {{event.payload.mutations}}")
```

<div class="note">
    <div class="note-title">Site-Delta-9 Research Capability</div>
    <p>The Flight Recorder enables complete phylogenetic tree reconstruction. This allows
    scientific analysis of which mutations improve fitness, how agents converge on optimal
    solutions, and why certain lineages become evolutionary dead ends.</p>
</div>

### Hot-Swapping Genomes

**Adopting Better Variants Mid-Execution:**

```python
# Agent discovers better variant
if variant_fitness > current_fitness:
    agent.hot_swap_genome(variant_genome_id)
    print(f"Evolved to genome {{variant_genome_id}}")
    print(f"Fitness improved: {{current_fitness}} → {{variant_fitness}}")
```

---

## Best Practices

### TELEPORT MASSIVE Operational Standards

<div class="checklist">
    <div class="checklist-title">Site-Delta-9 Best Practices</div>
    <ul>
        <li>✅ Always create epistemic sessions before work</li>
        <li>✅ Run safety gates before major evolutionary steps</li>
        <li>✅ Log all discoveries and knowledge gaps</li>
        <li>✅ Monitor fitness scores regularly</li>
        <li>✅ Review Flight Recorder logs weekly</li>
        <li>✅ Use version control for all code changes</li>
        <li>✅ Document agent behavior and mutations</li>
        <li>✅ Test agents in Scint Gym before deployment</li>
    </ul>
</div>

### Agent Design Principles

**1. Single Responsibility**
- Each agent should have one clear purpose
- Avoid agents that do too many things
- Specialized agents evolve faster

**2. Observable Behavior**
- All actions should be logged
- Fitness metrics should be measurable
- Mutations should be traceable

**3. Evolutionary Fitness**
- Design agents that can improve through mutation
- Avoid hard-coded solutions
- Enable genetic variation

**4. Safety First**
- Always run safety gates
- Test in Scint Gym before production
- Monitor for harmful mutations

<div class="warning">
    <div class="warning-title">TELEPORT MASSIVE Safety Protocol</div>
    <p>Agents with fitness < 0.5 are automatically marked as DEATH. This prevents
    evolutionary dead ends from consuming resources. Always monitor fitness scores and
    intervene if agents are trending toward DEATH.</p>
</div>

### Memory Management

**Organizing _pyrite Structure:**

```
_pyrite/
├── active/          # Current work (keep < 10 items)
│   ├── task_001.md
│   └── task_002.md
├── backlog/         # Future work (prioritize regularly)
│   ├── idea_001.md
│   └── idea_002.md
├── standards/       # Project standards (reference only)
│   ├── code_style.md
│   └── architecture.md
└── gym_logs/        # Fitness results (archive monthly)
    └── evaluation_*.jsonl
```

**Best Practices:**
- Keep `active/` focused (max 10 items)
- Review `backlog/` weekly
- Archive `gym_logs/` monthly
- Update `standards/` as project evolves

---

## Troubleshooting

### Common Issues and Solutions

**Issue: Agent Fitness Declining**

```bash
# Check recent mutations
waft chronicle --agent RefactorAgent --limit 20

# Review Flight Recorder logs
cat _pyrite/science/laboratory.jsonl | grep RefactorAgent | tail -20

# Spawn new variants with different mutations
waft spawn --agent RefactorAgent --mutation conservative_approach.json
```

<div class="caution">
    <div class="caution-title">TELEPORT MASSIVE Diagnostic Protocol</div>
    <p>If agent fitness consistently declines, the mutation strategy may be too aggressive.
    Try spawning variants with more conservative mutations. Review the phylogenetic tree to
    identify which mutations caused the decline.</p>
</div>

**Issue: Epistemic State Unclear**

```bash
# Check epistemic vectors
waft assess --history

# Review findings and unknowns
waft session status

# Log missing knowledge explicitly
waft unknown log "Specific knowledge gap description"
```

**Issue: Project Verification Fails**

```bash
# Check project structure
waft verify --verbose

# Reinitialize if needed
waft init

# Verify dependencies
waft sync
```

**Issue: PDF Generation Errors**

```bash
# Check WeasyPrint installation
python3 -c "import weasyprint; print('OK')"

# Try different template
PDF.from_template(template="lab_notes", ...)

# Use evolution system instead
PDF.from_content(content=markdown_content, style="clinical_standard")
```

---

## Real-World Examples

### Example 1: Code Refactoring Agent

**Scenario:** Automatically refactor legacy code while maintaining functionality.

```bash
# 1. Create agent
waft new refactor_laboratory
cd refactor_laboratory

# 2. Define RefactorAgent
# (see First Agent Deployment section)

# 3. Spawn variants
waft spawn --agent RefactorAgent --mutation improved_ast_parsing.json
waft spawn --agent RefactorAgent --mutation better_naming_conventions.json

# 4. Evaluate fitness
waft eval --agent RefactorAgent

# 5. Evolve to best variant
waft evolve --agent RefactorAgent

# 6. Deploy evolved agent
# Agent now has improved refactoring capabilities
```

<div class="note">
    <div class="note-title">Site-Delta-9 Success Story</div>
    <p>RefactorAgent evolved from 0.65 fitness to 0.89 fitness over 12 generations.
    Key mutations included improved AST parsing, better naming convention detection, and
    enhanced code structure analysis. The agent now handles 40% more code patterns than
    the original variant.</p>
</div>

### Example 2: Documentation Generator

**Scenario:** Automatically generate comprehensive project documentation.

```python
from waft import PDF
from waft.reflection import ReflectionSystem

# 1. Observe codebase
reflection = ReflectionSystem()
gaps = reflection.analyze_documentation_gaps()

# 2. Generate documentation
for gap in gaps:
    content = generate_doc_content(gap)
    PDF.from_template(
        template="field_guide",
        title=gap.title,
        content=content
    ).save(f"docs/{{gap.filename}}")

# 3. Document the documentation system
PDF.from_template(
    template="lab_notes",
    title="Documentation Generation Process",
    content=reflection.to_markdown()
).save("docs/doc_generation_process.pdf")
```

### Example 3: Test Generation Agent

**Scenario:** Automatically generate test cases for code.

```bash
# 1. Create TestAgent
waft spawn --agent TestAgent --mutation unit_test_focus.json

# 2. Evaluate on codebase
waft eval --agent TestAgent --quest-type LOGIC_FRACTURE

# 3. Evolve based on test coverage metrics
waft evolve --agent TestAgent --generation 10

# 4. Deploy evolved TestAgent
# Agent now generates comprehensive test suites
```

<div class="recommendation">
    <div class="recommendation-title">TELEPORT MASSIVE Recommendation</div>
    <p>Start with simple agents and let them evolve. Don't try to build the perfect agent
    from scratch. Instead, create a basic agent, spawn variants, evaluate fitness, and let
    evolution find the optimal solution. This is the WAFT way: making the impossible,
    inevitable.</p>
</div>

---

## Conclusion: Making the Impossible, Inevitable™

WAFT enables you to breed AI agents that evolve, adapt, and improve. Through the Three Pillars—the Substrate, the Physics, and the Flight Recorder—WAFT provides a complete system for directed evolution of self-modifying AI agents.

**Remember:**
- **Don't just build agents. Breed them.**
- **Let evolution find the optimal solution.**
- **Track everything for scientific analysis.**
- **Make the impossible, inevitable.**

<div class="note">
    <div class="note-title">TELEPORT MASSIVE Mission Statement</div>
    <p>WAFT is not just a framework—it's a scientific instrument for studying the physics
    of artificial cognition. Every agent evolution, every mutation, every fitness evaluation
    contributes to our understanding of how AI can improve itself. The ultimate goal: observe
    a "God-Head" agent emerge from thousands of generations of directed mutation and selection.</p>
</div>

---

**Generated**: {date}
**WAFT Version**: 0.3.1-alpha
**Handbook Version**: 2.0
**Document ID**: TM-OPMAN-WAFT-001
**Classification**: INTERNAL USE ONLY
**Facility**: Site-Delta-9 (WAFT Development Laboratory)
**Tagline**: Making the Impossible, Inevitable™

""".format(date=datetime.now().strftime("%B %d, %Y at %I:%M %p"))


def main():
    """Generate comprehensive WAFT handbook PDF."""

    print("=" * 80)
    print("📚 Generating Comprehensive WAFT Handbook PDF")
    print("=" * 80)

    # Get content
    content = get_handbook_content()

    # Create output directory
    output_dir = Path("_work_efforts/showcase_documents")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"WAFT_HANDBOOK_{timestamp}.pdf"

    print(f"\n📝 Content length: {len(content):,} characters")
    print(
        "📄 Generating PDF with Neon Cyberpunk theme (perfect for Teleport Massive aesthetic!)..."
    )

    # Generate PDF using Field Guide template - this one works and includes all content
    try:
        import platform
        import subprocess

        system = platform.system()


        import platform

        system = platform.system()

        # Convert markdown to HTML for template
        html_content = markdown.markdown(
            content, extensions=["fenced_code", "tables", "nl2br", "extra", "codehilite"]
        )

        # Use Neon Cyberpunk template - perfect for "Teleport Massive" aesthetic!
        pdf_path = generate_neon_cyberpunk(
            title="WAFT HANDBOOK: COMPLETE GUIDE TO THE EVOLUTIONARY CODE LABORATORY",
            content=html_content,
            output_path=output_path,
        )

        # Open PDF
        if system == "Darwin":  # macOS
            subprocess.run(["open", str(pdf_path)], check=False)
        elif system == "Windows":
            subprocess.run(["start", str(pdf_path)], shell=True, check=False)
        else:  # Linux
            subprocess.run(["xdg-open", str(pdf_path)], check=False)

        print(f"✅ Generated: {output_path}")
        print(f"📊 File size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")
        print("\n" + "=" * 80)
        print("🎉 Handbook generation complete!")
        print("=" * 80)

    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
