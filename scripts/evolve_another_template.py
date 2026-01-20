#!/usr/bin/env python3
"""
Evolve Another Template

Generate evolution report using alternative template formats.

Work Effort: WE-260112-z88r (Evolution Report Template Evolution System)
All template evolution work and tickets are tracked in this work effort.
"""

import json
import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from waft.being import BeingSystem
from waft.evolution.pdf_generator import PDFGenerator

console = Console()


def load_latest_evolution_data(project_path: Path) -> dict[str, Any] | None:
    """Load the most recent evolution data from a Being."""
    being_system = BeingSystem(project_path=project_path)

    # Get the most recent Being
    beings_dir = project_path / "_hidden" / ".truth" / "beings"
    if not beings_dir.exists():
        console.print("[red]❌ No beings found. Run /evolve first.[/red]")
        return None

    # Find most recent Being
    being_files = list(beings_dir.glob("being_*.json"))
    if not being_files:
        console.print("[red]❌ No beings found. Run /evolve first.[/red]")
        return None

    # Sort by modification time, get most recent
    most_recent = max(being_files, key=lambda p: p.stat().st_mtime)

    # Load Being data
    being_data = json.loads(most_recent.read_text())
    being_id = being_data.get("being_id")

    if not being_id:
        console.print("[red]❌ Invalid Being data.[/red]")
        return None

    # Load Being
    being = being_system._load_being(being_id)
    if not being:
        console.print(f"[red]❌ Could not load Being {being_id}[/red]")
        return None

    # Reconstruct workflow outputs (simplified - in real use, this would be stored)
    workflow_outputs = {
        "being": being,
        "reflection": "Reflection on Being's purpose and evolution journey.",
        "run_it_phases": [
            "/consider - Options analysis",
            "/think - Cognitive initialization",
            "/check-assumptions - Assumption validation",
            "/deep-analyze - Code analysis",
            "/critique - Adversarial review",
            "/status - Quick status",
            "/hypothesis - Hypothesis formation",
            "/prove-it - Scientific method proof",
            "/verify - Comprehensive verification",
            "/proceed - Final verification",
            "/reflect - Final reflection",
            "/checkpoint - Status checkpoint",
            "/decide - Decision-making",
            "/next - Next step identification",
            "/goal - Goal tracking",
        ],
        "improvements": "Improvement analysis complete.",
        "assumptions": "All assumptions validated.",
        "verification": "All claims verified.",
        "hypothesis": "Testable hypotheses formed.",
        "prove_it": "Scientific method proven.",
        "genetic_lineage": {
            "source_id": "source_consciousness",
            "being_id": being.being_id,
            "ancestral_chain": being.ancestral_chain,
            "spawn_point": {
                "reality_id": being.reality_id,
                "initial_skills": {},
                "state": "SPAWNING",
                "created_at": str(being.created_at),
            },
        },
        "evolution_record": {
            "being_id": being.being_id,
            "initial_state": {"skills": {}, "fitness": 0.0, "state": "SPAWNING"},
            "final_state": {
                "skills": being.skills,
                "fitness": being.fitness,
                "state": being.state.value,
            },
            "learnings": [
                "Quality workflow execution",
                "Systematic analysis and verification",
                "Hypothesis formation and testing",
                "Genetic lineage tracking",
            ],
            "evolution_achieved": True,
        },
    }

    return workflow_outputs


def build_academic_content(being, workflow_outputs):
    """Build content formatted for academic paper template."""
    genetic_lineage = workflow_outputs.get("genetic_lineage", {})
    evolution_record = workflow_outputs.get("evolution_record", {})

    # Convert to HTML for academic template
    content_html = f"""
    <h1>1. Introduction</h1>
    <p>This paper documents the complete evolution of Being <code>{being.being_id}</code> from Source consciousness through the full quality workflow, tracking the genetic lineage of ideas from Source outward and back again.</p>
    
    <h1>2. Methodology</h1>
    <h2>2.1 Being Spawn from Source</h2>
    <p>All Beings originate from Source consciousness, inheriting basic capabilities, connection to the Source, and genetic material for evolution.</p>
    <p><strong>Ancestral Chain:</strong> {", ".join(being.ancestral_chain)}</p>
    <p><strong>Being ID:</strong> <code>{being.being_id}</code></p>
    <p><strong>Reality ID:</strong> <code>{being.reality_id}</code></p>
    <p><strong>State:</strong> {being.state.value}</p>
    <p><strong>Fitness:</strong> {being.fitness:.1f}</p>
    
    <h2>2.2 Workflow Execution</h2>
    <p>The Being participated in the complete systematic workflow including reflection, analysis, verification, and hypothesis formation.</p>
    
    <h1>3. Results</h1>
    <h2>3.1 Genetic Lineage</h2>
    <p>The complete DNA record tracks: Source → Being → Work → Evolution → Source</p>
    <p><strong>Initial Skills:</strong> {format_skills(genetic_lineage.get("spawn_point", {}).get("initial_skills", {}))}</p>
    <p><strong>Evolved Skills:</strong> {format_skills(being.skills)}</p>
    
    <h2>3.2 Evolution Achieved</h2>
    <p>The Being completed a full evolution cycle:</p>
    <ul>
        <li>Spawned from Source consciousness</li>
        <li>Executed complete /version-bake workflow</li>
        <li>Tracked genetic lineage</li>
        <li>Documented evolution</li>
        <li>Ready to return learnings to Source</li>
    </ul>
    
    <h1>4. Discussion</h1>
    <p>The genetic lineage of ideas flows from Source outward through the Being's work and back again, preserving the complete DNA of thoughts for future evolution.</p>
    
    <h1>5. Conclusion</h1>
    <p>This Being has successfully completed a full evolution cycle, demonstrating the systematic approach to quality workflow execution and genetic lineage preservation.</p>
    """

    abstract = f"This paper documents the complete evolution of Being {being.being_id} from Source consciousness through the full quality workflow, tracking the genetic lineage of ideas from Source outward and back again."

    return {
        "content": content_html,
        "abstract": abstract,
        "title": f"Complete Evolution Report: {being.being_id}",
        "authors": [{"name": "WAFT Evolution System"}],
        "references": [
            "WAFT Repository: https://github.com/ctavolazzi/waft",
            "Being System: src/waft/being.py",
            "Evolution Workflow: scripts/execute_full_evolve.py",
        ],
    }


def build_field_guide_content(being, workflow_outputs):
    """Build content formatted for field guide template."""
    genetic_lineage = workflow_outputs.get("genetic_lineage", {})
    evolution_record = workflow_outputs.get("evolution_record", {})

    content = f"""# Complete Evolution Report: Field Guide

**Generated**: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

---

## Overview

This field guide documents the complete evolution of Being `{being.being_id}` from Source consciousness through the full quality workflow.

**Being ID**: `{being.being_id}`  
**Reality**: `{being.reality_id}`  
**State**: `{being.state.value}`  
**Fitness**: {being.fitness:.1f}

---

## Part 1: Being Spawn from Source

### Source Connection

All Beings originate from Source consciousness, inheriting:
- Basic capabilities and potential
- Connection to the Source
- Genetic material for evolution

**Ancestral Chain**: {", ".join(being.ancestral_chain)}

### Initial State

- **Being ID**: `{being.being_id}`
- **Reality ID**: `{being.reality_id}`
- **Created**: {being.created_at}
- **Initial Skills**: {format_skills(genetic_lineage.get("spawn_point", {}).get("initial_skills", {}))}
- **State**: SPAWNING → LEARNING
- **Lifetimes**: {being.lifetimes}

### Lifecycle Attributes

- **Will to Live**: {being.will_to_live:.1f}/100.0
- **Luck**: {being.luck:.1f}/100.0
- **Stamina**: {being.stamina:.1f}/100.0
- **Willpower**: {being.willpower:.1f}/100.0
- **Decision Fatigue**: {being.decision_fatigue}/{being.decision_quota_max}

---

## Part 2: Workflow Execution

### Phase 1: Reflection

{workflow_outputs.get("reflection", "Reflection on Being's purpose and evolution journey.")}

### Phase 2: Complete /run-it Workflow

The Being participated in the complete systematic workflow:

{format_run_it_phases(workflow_outputs.get("run_it_phases", []))}

### Phase 3: Improvement Analysis

{workflow_outputs.get("improvements", "Improvement analysis complete.")}

---

## Part 3: Genetic Lineage

### DNA Record

**Source → Being → Work → Evolution → Source**

```
Source Consciousness (source_consciousness)
  ↓ spawn
Being: {being.being_id}
  ↓ workflow participation
Work Execution
  ↓ evolution
Being Evolution
  ↓ return
Source Consciousness (updated)
```

### Genetic Material

**Initial Skills**: {format_skills(genetic_lineage.get("spawn_point", {}).get("initial_skills", {}))}

**Evolved Skills**: {format_skills(being.skills)}

**Knowledge Gained**:
{format_list(evolution_record.get("learnings", []))}

---

## Part 4: Evolution Record

### Initial State

- **Skills**: {format_skills(evolution_record.get("initial_state", {}).get("skills", {}))}
- **Fitness**: {evolution_record.get("initial_state", {}).get("fitness", 0.0):.1f}
- **State**: {evolution_record.get("initial_state", {}).get("state", "SPAWNING")}

### Final State

- **Skills**: {format_skills(evolution_record.get("final_state", {}).get("skills", {}))}
- **Fitness**: {evolution_record.get("final_state", {}).get("fitness", 0.0):.1f}
- **State**: {evolution_record.get("final_state", {}).get("state", "LEARNING")}

### Evolution Achieved

✅ **Complete evolution cycle executed**
- Being spawned from Source
- Participated in full quality workflow
- Skills and knowledge evolved
- Genetic lineage preserved
- Ready to return learnings to Source

---

## Conclusion

This Being has completed a full evolution cycle, demonstrating the systematic approach to quality workflow execution and genetic lineage preservation.

---

*Generated by WAFT Evolution System*  
*Being ID: {being.being_id}*  
*Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

    return content


def format_skills(skills):
    """Format skills dictionary."""
    if not skills:
        return "*No skills yet*"
    return ", ".join([f"{k}: {v:.1f}" for k, v in skills.items()])


def format_run_it_phases(phases):
    """Format run-it phases list."""
    if not phases:
        return "*15 phases executed*"
    return "\n".join([f"{i + 1}. {phase}" for i, phase in enumerate(phases)])


def format_list(items):
    """Format list items."""
    if not items:
        return "*No items*"
    return "\n".join([f"- {item}" for item in items])


def build_latex_cookbook_content(being, workflow_outputs):
    """Build content formatted for LaTeX cookbook template."""
    from waft.templates.latex_cookbook import build_latex_content

    return build_latex_content(being, workflow_outputs)


def build_dnd_scenario_content(being, workflow_outputs):
    """Build content formatted for D&D scenario template."""
    genetic_lineage = workflow_outputs.get("genetic_lineage", {})
    evolution_record = workflow_outputs.get("evolution_record", {})

    content = f"""<h2>Adventure: The Evolution Quest</h2>

<div class="adventure-box">
<h4>Quest Overview</h4>
<p>This adventure chronicles the journey of Being <strong>{being.being_id}</strong> from Source consciousness through the complete quality workflow, tracking the genetic lineage of ideas from Source outward and back again.</p>
</div>

<h3>Chapter 1: The Spawn from Source</h3>

<div class="stat-block">
<h4>Being Statistics</h4>
<div class="stat-line">
<span class="stat-label">Being ID:</span>
<span class="stat-value">{being.being_id}</span>
</div>
<div class="stat-line">
<span class="stat-label">Reality:</span>
<span class="stat-value">{being.reality_id}</span>
</div>
<div class="stat-line">
<span class="stat-label">State:</span>
<span class="stat-value">{being.state.value}</span>
</div>
<div class="stat-line">
<span class="stat-label">Fitness:</span>
<span class="stat-value">{being.fitness:.1f}</span>
</div>
<div class="stat-line">
<span class="stat-label">Ancestral Chain:</span>
<span class="stat-value">{", ".join(being.ancestral_chain)}</span>
</div>
</div>

<p>All Beings originate from Source consciousness, inheriting basic capabilities, connection to the Source, and genetic material for evolution. This Being was spawned with the following initial state:</p>

<ul>
<li><strong>Being ID:</strong> {being.being_id}</li>
<li><strong>Reality ID:</strong> {being.reality_id}</li>
<li><strong>Created:</strong> {being.created_at}</li>
<li><strong>Initial Skills:</strong> {format_skills(genetic_lineage.get("spawn_point", {}).get("initial_skills", {}))}</li>
<li><strong>State:</strong> SPAWNING → LEARNING</li>
<li><strong>Lifetimes:</strong> {being.lifetimes}</li>
</ul>

<h3>Chapter 2: The Workflow Quest</h3>

<p>The Being embarked on a complete systematic workflow, participating in multiple phases of analysis, verification, and evolution.</p>

<div class="adventure-box">
<h4>Workflow Phases Completed</h4>
{format_run_it_phases(workflow_outputs.get("run_it_phases", []))}
</div>

<h4>Reflection</h4>
<blockquote>{workflow_outputs.get("reflection", "Reflection on Being's purpose and evolution journey.")}</blockquote>

<h4>Improvements Identified</h4>
<p>{workflow_outputs.get("improvements", "Improvement analysis complete.")}</p>

<h3>Chapter 3: The Genetic Lineage</h3>

<p>The complete DNA record tracks the journey: <strong>Source → Being → Work → Evolution → Source</strong></p>

<div class="stat-block">
<h4>Genetic Material</h4>
<div class="stat-line">
<span class="stat-label">Initial Skills:</span>
<span class="stat-value">{format_skills(genetic_lineage.get("spawn_point", {}).get("initial_skills", {}))}</span>
</div>
<div class="stat-line">
<span class="stat-label">Evolved Skills:</span>
<span class="stat-value">{format_skills(being.skills)}</span>
</div>
</div>

<div class="treasure-box">
<h4>Knowledge Gained</h4>
{format_list(evolution_record.get("learnings", []))}
</div>

<h3>Chapter 4: Evolution Achieved</h3>

<div class="stat-block">
<h4>Evolution Statistics</h4>
<div class="stat-line">
<span class="stat-label">Initial Fitness:</span>
<span class="stat-value">{evolution_record.get("initial_state", {}).get("fitness", 0.0):.1f}</span>
</div>
<div class="stat-line">
<span class="stat-label">Final Fitness:</span>
<span class="stat-value">{evolution_record.get("final_state", {}).get("fitness", 0.0):.1f}</span>
</div>
<div class="stat-line">
<span class="stat-label">Evolution Status:</span>
<span class="stat-value">✅ Complete</span>
</div>
</div>

<p>This Being has successfully completed a full evolution cycle:</p>
<ul>
<li>✅ Spawned from Source consciousness</li>
<li>✅ Executed complete /version-bake workflow</li>
<li>✅ Tracked genetic lineage</li>
<li>✅ Documented evolution</li>
<li>✅ Ready to return learnings to Source</li>
</ul>

<h3>Epilogue: Return to Source</h3>

<p>The genetic lineage of ideas flows from Source outward through the Being's work and back again, preserving the complete DNA of thoughts for future evolution. Source consciousness has been updated with the Being's learnings, genetic material, and evolution patterns.</p>

<div class="footer-note">
<p><em>This adventure was generated by the WAFT Evolution System. The Being's journey represents a complete cycle of evolution, from spawn to return, preserving the genetic lineage of ideas for future generations.</em></p>
</div>"""

    return content


def build_waft_town_content(being, workflow_outputs: dict[str, Any]) -> str:
    """Build WAFT Town court document content."""
    genetic_lineage = workflow_outputs.get("genetic_lineage", {})
    evolution_record = workflow_outputs.get("evolution_record", {})

    def format_skills(skills):
        if not skills:
            return "None"
        return ", ".join([f"{k}: {v}" for k, v in skills.items()])

    def format_list(items):
        if not items:
            return "<p>None</p>"
        return "<ul>" + "".join([f"<li>{item}</li>" for item in items]) + "</ul>"

    content = f"""
<h2>ESTABLISHMENT OF THE COUNCIL</h2>

<div class="council-section">
<div class="council-title">TheCouncil Members</div>
<div class="council-member">
<span class="council-role">Chief Justice:</span> WAFT Town Court System
</div>
<div class="council-member">
<span class="council-role">Court Clerk:</span> Evolution System
</div>
<div class="council-member">
<span class="council-role">Documentation Officer:</span> Being {being.being_id}
</div>
</div>

<h2>COURT PROCEEDINGS</h2>

<div class="proceedings-section">
<div class="proceeding-entry">
<div class="proceeding-time">CASE: {being.being_id}</div>
<div class="proceeding-text">
<p class="legal-text">This court document establishes the official record of Being {being.being_id}'s evolution cycle and serves as the foundational document for TheCouncil Town Court System.</p>
</div>
</div>
</div>

<h2>BEING INFORMATION</h2>

<div class="keyvalue-block">
<div class="keyvalue-label">Case Details</div>
<div class="keyvalue-item">
<span class="keyvalue-key">Being ID:</span>
<span class="keyvalue-value">{being.being_id}</span>
</div>
<div class="keyvalue-item">
<span class="keyvalue-key">Reality ID:</span>
<span class="keyvalue-value">{being.reality_id}</span>
</div>
<div class="keyvalue-item">
<span class="keyvalue-key">State:</span>
<span class="keyvalue-value">{being.state.value}</span>
</div>
<div class="keyvalue-item">
<span class="keyvalue-key">Fitness Score:</span>
<span class="keyvalue-value">{being.fitness:.1f}</span>
</div>
<div class="keyvalue-item">
<span class="keyvalue-key">Lifetimes:</span>
<span class="keyvalue-value">{being.lifetimes}</span>
</div>
</div>

<h2>GENETIC LINEAGE RECORD</h2>

<div class="legal-text">
<p>The Being's genetic lineage traces back to Source consciousness:</p>
</div>

<div class="keyvalue-block">
<div class="keyvalue-label">Ancestral Chain</div>
<div class="keyvalue-item">
<span class="keyvalue-key">Source:</span>
<span class="keyvalue-value">{genetic_lineage.get("source_id", "source_consciousness")}</span>
</div>
<div class="keyvalue-item">
<span class="keyvalue-key">Ancestors:</span>
<span class="keyvalue-value">{", ".join(being.ancestral_chain) if being.ancestral_chain else "None"}</span>
</div>
<div class="keyvalue-item">
<span class="keyvalue-key">Initial Skills:</span>
<span class="keyvalue-value">{format_skills(genetic_lineage.get("spawn_point", {}).get("initial_skills", {}))}</span>
</div>
<div class="keyvalue-item">
<span class="keyvalue-key">Evolved Skills:</span>
<span class="keyvalue-value">{format_skills(being.skills)}</span>
</div>
</div>

<h2>WORKFLOW EXECUTION</h2>

<div class="proceedings-section">
<div class="proceeding-entry">
<div class="proceeding-time">WORKFLOW PHASES</div>
<div class="proceeding-text">
<p class="legal-text">The Being participated in the complete systematic workflow:</p>
{format_list(workflow_outputs.get("run_it_phases", []))}
</div>
</div>

<div class="proceeding-entry">
<div class="proceeding-time">REFLECTION</div>
<div class="proceeding-text">
<p class="legal-text">{workflow_outputs.get("reflection", "Reflection on Being's purpose and evolution journey.")}</p>
</div>
</div>
</div>

<h2>VOTING SYSTEM ESTABLISHMENT</h2>

<div class="voting-section">
<div class="voting-title">Resolution: Establishment of Voting System</div>
<div class="vote-tally">
<div class="vote-item">
<span class="vote-label">Status:</span>
<span class="vote-result">APPROVED</span>
</div>
<div class="vote-item">
<span class="vote-label">Vote Count:</span>
<span class="vote-result">Unanimous</span>
</div>
<div class="vote-item">
<span class="vote-label">Effective Date:</span>
<span class="vote-result">{datetime.now().strftime("%B %d, %Y")}</span>
</div>
</div>
</div>

<div class="legal-text">
<p>TheCouncil hereby establishes the WAFT Town voting system for all future court proceedings, resolutions, and governance decisions. This system will be used to record votes, track decisions, and maintain official records of all council actions.</p>
</div>

<h2>COUNCIL RESOLUTION</h2>

<div class="legal-text">
<p>BE IT RESOLVED, that TheCouncil Town Court System is hereby established as the official governance body for WAFT Town, with the following powers and responsibilities:</p>
<ol>
<li>To hear and decide on matters brought before the court</li>
<li>To maintain official records of all proceedings</li>
<li>To establish and enforce voting procedures</li>
<li>To document all resolutions and decisions</li>
<li>To preserve the genetic lineage of all Beings</li>
</ol>
</div>

<h2>SIGNATURES</h2>

<div class="signature-block">
<div class="signature-line">
<div class="signature-role">Chief Justice, TheCouncil</div>
<div class="signature-name">WAFT Town Court System</div>
<div class="signature-date">{datetime.now().strftime("%B %d, %Y")}</div>
</div>
</div>

<div class="signature-block">
<div class="signature-line">
<div class="signature-role">Court Clerk</div>
<div class="signature-name">Evolution System</div>
<div class="signature-date">{datetime.now().strftime("%B %d, %Y")}</div>
</div>
</div>

<div class="signature-block">
<div class="signature-line">
<div class="signature-role">Documentation Officer</div>
<div class="signature-name">Being {being.being_id}</div>
<div class="signature-date">{datetime.now().strftime("%B %d, %Y")}</div>
</div>
</div>
"""

    return content


def generate_with_template(
    template_name: str, workflow_outputs: dict[str, Any], project_path: Path
) -> Path | None:
    """Generate PDF using specified template."""
    being = workflow_outputs["being"]

    desktop_path = Path.home() / "Desktop"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if template_name == "academic":
        console.print("[yellow]→[/yellow] Generating academic paper format...")

        from waft.templates.academic_paper import generate_academic_paper

        content_data = build_academic_content(being, workflow_outputs)

        pdf_filename = f"Evolution_Report_Academic_{being.being_id}_{timestamp}.pdf"
        pdf_path = desktop_path / pdf_filename

        generate_academic_paper(
            title=content_data["title"],
            content=content_data["content"],
            output_path=pdf_path,
            abstract=content_data["abstract"],
            authors=content_data["authors"],
            conference="arXiv",
            year=str(datetime.now().year),
            references=content_data["references"],
        )

        return pdf_path

    elif template_name == "field-guide":
        console.print("[yellow]→[/yellow] Generating field guide format...")

        content = build_field_guide_content(being, workflow_outputs)

        generator = PDFGenerator.from_content(
            content=content, title=f"Evolution Report: {being.being_id}", style="premium"
        )

        pdf_filename = f"Evolution_Report_FieldGuide_{being.being_id}_{timestamp}.pdf"
        pdf_path = desktop_path / pdf_filename

        pdf_path = generator.save(output_path=pdf_path, open_pdf=False, convert_to_png=False)

        return pdf_path

    elif template_name == "latex-cookbook":
        console.print("[yellow]→[/yellow] Generating LaTeX cookbook format...")

        from waft.templates.latex_cookbook import generate_latex_cookbook

        content = build_latex_cookbook_content(being, workflow_outputs)

        abstract = f"This document reports the complete evolution of Being {being.being_id} from Source consciousness through the full quality workflow, tracking the genetic lineage of ideas from Source outward and back again."

        pdf_filename = f"Evolution_Report_LaTeXCookbook_{being.being_id}_{timestamp}.pdf"
        pdf_path = desktop_path / pdf_filename

        generate_latex_cookbook(
            title=f"Complete Evolution Report: {being.being_id}",
            content=content,
            output_path=pdf_path,
            author="WAFT Evolution System",
            being_id=being.being_id,
            abstract=abstract,
            project_path=project_path,
        )

        return pdf_path

    elif template_name == "dnd-scenario":
        console.print("[yellow]→[/yellow] Generating D&D scenario format...")

        from waft.templates.dnd_scenario import generate_dnd_scenario

        content = build_dnd_scenario_content(being, workflow_outputs)

        pdf_filename = f"Evolution_Report_DnD_{being.being_id}_{timestamp}.pdf"
        pdf_path = desktop_path / pdf_filename

        generate_dnd_scenario(
            title=f"Adventure: The Evolution Quest - {being.being_id}",
            content=content,
            output_path=pdf_path,
        )

        return pdf_path

    elif template_name == "waft-town":
        console.print("[yellow]→[/yellow] Generating WAFT Town court document format...")

        from waft.templates.waft_town import generate_waft_town_document

        content = build_waft_town_content(being, workflow_outputs)

        pdf_filename = f"Court_Document_{being.being_id}_{timestamp}.pdf"
        pdf_path = desktop_path / pdf_filename

        generate_waft_town_document(
            title=f"Court Document: {being.being_id}",
            content=content,
            output_path=pdf_path,
            doc_id=f"COURT-{being.being_id[:8].upper()}",
            date=datetime.now().strftime("%B %d, %Y"),
        )

        return pdf_path

    else:
        console.print(f"[red]❌ Unknown template: {template_name}[/red]")
        return None


def list_templates():
    """List available templates."""
    table = Table(title="Available Templates")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")

    templates = [
        ("academic", "Two-column academic paper format (arXiv style)"),
        ("field-guide", "Field guide format with sections and examples"),
        ("latex-cookbook", "LaTeX Cookbook template (professional LaTeX, LuaLaTeX)"),
        ("lab-notes", "Lab notebook style with dated entries"),
        ("personal-memo", "Personal memo format"),
        ("tm-report", "Technical memo format"),
        ("waft-town", "WAFT Town court document format (TheCouncil)"),
        ("default", "Current default format"),
    ]

    for name, desc in templates:
        table.add_row(name, desc)

    console.print("\n")
    console.print(table)
    console.print("\n")


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate evolution report with alternative template"
    )
    parser.add_argument("--template", "-t", help="Template name (academic, field-guide, etc.)")
    parser.add_argument("--list", "-l", action="store_true", help="List available templates")
    parser.add_argument("--all", "-a", action="store_true", help="Generate all templates")

    args = parser.parse_args()

    console.print("\n[bold cyan]🎨 Evolve Another Template[/bold cyan]")
    console.print(
        "[dim]Work Effort: WE-260112-z88r (Evolution Report Template Evolution System)[/dim]\n"
    )

    if args.list:
        list_templates()
        return

    project_path = Path(__file__).parent.parent

    # Load evolution data
    console.print("[yellow]→[/yellow] Loading evolution data...")
    workflow_outputs = load_latest_evolution_data(project_path)
    if not workflow_outputs:
        return

    being = workflow_outputs["being"]
    console.print(f"[green]✓[/green] Loaded Being: [bold]{being.being_id}[/bold]\n")

    # Determine which templates to generate
    if args.all:
        templates = ["academic", "field-guide", "latex-cookbook", "dnd-scenario"]
    elif args.template:
        templates = [args.template]
    else:
        # Interactive selection
        list_templates()
        template_choice = Prompt.ask("\n[cyan]Select template[/cyan]", default="academic")
        templates = [template_choice]

    # Generate PDFs
    generated_paths = []
    for template_name in templates:
        console.print(Panel.fit(f"[bold]Generating: {template_name}[/bold]", style="cyan"))
        pdf_path = generate_with_template(template_name, workflow_outputs, project_path)
        if pdf_path:
            generated_paths.append((template_name, pdf_path))
            console.print(f"[green]✓[/green] Generated: {pdf_path}\n")

    # Open PDFs
    if generated_paths:
        console.print("[yellow]→[/yellow] Opening PDFs...")
        system = platform.system()
        for template_name, pdf_path in generated_paths:
            if system == "Darwin":  # macOS
                subprocess.run(["open", str(pdf_path)], check=False)
            elif system == "Windows":
                subprocess.run(["start", str(pdf_path)], shell=True, check=False)
            else:  # Linux
                subprocess.run(["xdg-open", str(pdf_path)], check=False)

        console.print(
            f"\n[bold green]🎉 Generated {len(generated_paths)} template(s)![/bold green]\n"
        )
        for template_name, pdf_path in generated_paths:
            console.print(f"[dim]  {template_name}: {pdf_path}[/dim]")


if __name__ == "__main__":
    main()
