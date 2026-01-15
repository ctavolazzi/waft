#!/usr/bin/env python3
"""
Spawn a Being from Source and have it explore the WAFT system.
Documents all observations and generates a PDF report.
"""

import sys
from pathlib import Path
from datetime import datetime
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from waft.being import BeingSystem
from waft.core.memory import MemoryManager
from rich.console import Console
from rich.markdown import Markdown

console = Console()

def main():
    """Spawn Being and have it explore the system."""
    
    console.print("[bold cyan]=== Being Evolution & Exploration ===[/bold cyan]\n")
    
    # Initialize systems
    console.print("[yellow]→[/yellow] Initializing systems...")
    being_system = BeingSystem(project_path=project_root)
    memory = MemoryManager(project_path=project_root)
    
    # Spawn Being from Source
    console.print("[yellow]→[/yellow] Spawning Being from Source...")
    being = being_system.spawn_being(
        reality_id="exploration_reality",
        parent_being_id=None,  # Spawn from Source
        initial_skills={
            "exploration": 20.0,
            "analysis": 15.0,
            "documentation": 18.0,
            "observation": 22.0
        }
    )
    
    console.print(f"[green]✓[/green] Being spawned: {being.being_id}")
    console.print(f"   Reality: {being.reality_id}")
    console.print(f"   Ancestral Chain: {being.ancestral_chain}")
    console.print(f"   Initial Skills: {being.skills}")
    console.print(f"   State: {being.state.value}\n")
    
    # Document Being spawn
    spawn_doc = f"""# Being Spawn: {being.being_id}

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Reality:** {being.reality_id}
**Source:** {being.ancestral_chain[0]}
**State:** {being.state.value}

## Initial Configuration

- **Being ID:** `{being.being_id}`
- **Reality ID:** `{being.reality_id}`
- **Ancestral Chain:** {being.ancestral_chain}
- **Initial Skills:**
  - exploration: {being.skills.get('exploration', 0):.1f}
  - analysis: {being.skills.get('analysis', 0):.1f}
  - documentation: {being.skills.get('documentation', 0):.1f}
  - observation: {being.skills.get('observation', 0):.1f}

## Purpose

This Being has been spawned from Source consciousness to explore and document
the WAFT system. It will systematically investigate the codebase structure,
architecture, patterns, and document all findings.
"""
    
    # Save spawn document
    spawn_path = project_root / "_pyrite" / "active" / f"BEING_SPAWN_{being.being_id}.md"
    spawn_path.parent.mkdir(parents=True, exist_ok=True)
    spawn_path.write_text(spawn_doc)
    console.print(f"[green]✓[/green] Spawn document saved: {spawn_path.name}\n")
    
    # Begin exploration
    console.print("[bold cyan]=== Beginning System Exploration ===[/bold cyan]\n")
    
    observations = []
    
    # 1. Project Structure Analysis
    console.print("[yellow]→[/yellow] Analyzing project structure...")
    structure_obs = analyze_project_structure(project_root, being)
    observations.extend(structure_obs)
    console.print(f"[green]✓[/green] Structure analysis complete ({len(structure_obs)} observations)\n")
    
    # 2. Architecture Analysis
    console.print("[yellow]→[/yellow] Analyzing architecture...")
    arch_obs = analyze_architecture(project_root, being)
    observations.extend(arch_obs)
    console.print(f"[green]✓[/green] Architecture analysis complete ({len(arch_obs)} observations)\n")
    
    # 3. Dependency Analysis
    console.print("[yellow]→[/yellow] Analyzing dependencies...")
    dep_obs = analyze_dependencies(project_root, being)
    observations.extend(dep_obs)
    console.print(f"[green]✓[/green] Dependency analysis complete ({len(dep_obs)} observations)\n")
    
    # 4. Pattern Discovery
    console.print("[yellow]→[/yellow] Discovering patterns...")
    pattern_obs = discover_patterns(project_root, being)
    observations.extend(pattern_obs)
    console.print(f"[green]✓[/green] Pattern discovery complete ({len(pattern_obs)} observations)\n")
    
    # 5. Key Functionality Mapping
    console.print("[yellow]→[/yellow] Mapping key functionality...")
    func_obs = map_functionality(project_root, being)
    observations.extend(func_obs)
    console.print(f"[green]✓[/green] Functionality mapping complete ({len(func_obs)} observations)\n")
    
    # 6. Integration Points
    console.print("[yellow]→[/yellow] Identifying integration points...")
    int_obs = identify_integrations(project_root, being)
    observations.extend(int_obs)
    console.print(f"[green]✓[/green] Integration analysis complete ({len(int_obs)} observations)\n")
    
    # 7. Documentation Review
    console.print("[yellow]→[/yellow] Reviewing documentation...")
    doc_obs = review_documentation(project_root, being)
    observations.extend(doc_obs)
    console.print(f"[green]✓[/green] Documentation review complete ({len(doc_obs)} observations)\n")
    
    # Compile exploration report
    console.print("[bold cyan]=== Compiling Exploration Report ===[/bold cyan]\n")
    
    report = compile_exploration_report(being, observations)
    
    # Save exploration report
    report_path = project_root / "_pyrite" / "active" / f"EXPLORATION_{being.being_id}.md"
    report_path.write_text(report)
    console.print(f"[green]✓[/green] Exploration report saved: {report_path.name}\n")
    
    # Update Being's skills based on exploration
    console.print("[yellow]→[/yellow] Updating Being's skills from exploration...")
    being.skills["exploration"] = min(100.0, being.skills.get("exploration", 0) + 10.0)
    being.skills["analysis"] = min(100.0, being.skills.get("analysis", 0) + 8.0)
    being.skills["documentation"] = min(100.0, being.skills.get("documentation", 0) + 12.0)
    being.skills["observation"] = min(100.0, being.skills.get("observation", 0) + 15.0)
    being.state = BeingState.EVOLVING
    
    # Save Being state
    being_system._save_being(being)
    console.print(f"[green]✓[/green] Being skills updated: {being.skills}\n")
    
    # Create genetic lineage document
    console.print("[yellow]→[/yellow] Creating genetic lineage document...")
    lineage_doc = create_genetic_lineage(being, observations)
    lineage_path = project_root / "_pyrite" / "active" / f"GENETIC_LINEAGE_{being.being_id}.md"
    lineage_path.write_text(lineage_doc)
    console.print(f"[green]✓[/green] Genetic lineage saved: {lineage_path.name}\n")
    
    # Create evolution summary
    console.print("[yellow]→[/yellow] Creating evolution summary...")
    evolution_doc = create_evolution_summary(being, observations)
    evolution_path = project_root / "_pyrite" / "active" / f"EVOLUTION_SUMMARY_{being.being_id}.md"
    evolution_path.write_text(evolution_doc)
    console.print(f"[green]✓[/green] Evolution summary saved: {evolution_path.name}\n")
    
    # Generate PDF
    console.print("[bold cyan]=== Generating PDF Report ===[/bold cyan]\n")
    pdf_path = generate_pdf_report(being, report, observations, project_root)
    
    console.print(f"\n[bold green]✓[/bold green] Complete!")
    console.print(f"   Being ID: {being.being_id}")
    console.print(f"   Observations: {len(observations)}")
    console.print(f"   PDF Report: {pdf_path}")
    
    return being, observations, pdf_path


def analyze_project_structure(project_root: Path, being) -> list:
    """Analyze project structure."""
    observations = []
    
    # Directory structure
    main_dirs = [d for d in project_root.iterdir() if d.is_dir() and not d.name.startswith('.')]
    observations.append({
        "category": "structure",
        "finding": f"Project has {len(main_dirs)} main directories",
        "details": [d.name for d in sorted(main_dirs)[:20]]
    })
    
    # Source code location
    src_path = project_root / "src"
    if src_path.exists():
        py_files = list(src_path.rglob("*.py"))
        observations.append({
            "category": "structure",
            "finding": f"Source code in `src/` with {len(py_files)} Python files",
            "details": [f.name for f in py_files[:10]]
        })
    
    # Test structure
    tests_path = project_root / "tests"
    if tests_path.exists():
        test_files = list(tests_path.rglob("*.py"))
        observations.append({
            "category": "structure",
            "finding": f"Tests in `tests/` with {len(test_files)} test files",
            "details": [f.name for f in test_files[:10]]
        })
    
    # Configuration files
    config_files = []
    for pattern in ["*.toml", "*.yaml", "*.yml", "*.json"]:
        config_files.extend(list(project_root.glob(pattern)))
    if config_files:
        observations.append({
            "category": "structure",
            "finding": f"Found {len(config_files)} configuration files",
            "details": [f.name for f in config_files[:10]]
        })
    
    return observations


def analyze_architecture(project_root: Path, being) -> list:
    """Analyze system architecture."""
    observations = []
    
    # Core modules
    src_path = project_root / "src" / "waft"
    if src_path.exists():
        modules = [d.name for d in src_path.iterdir() if d.is_dir() and not d.name.startswith('_')]
        observations.append({
            "category": "architecture",
            "finding": f"Core modules: {', '.join(modules[:10])}",
            "details": modules
        })
    
    # Entry points
    entry_points = []
    for pattern in ["main.py", "__main__.py", "cli.py"]:
        entry_points.extend(list(project_root.rglob(pattern)))
    if entry_points:
        observations.append({
            "category": "architecture",
            "finding": f"Found {len(entry_points)} entry points",
            "details": [str(f.relative_to(project_root)) for f in entry_points]
        })
    
    # Being system
    being_file = project_root / "src" / "waft" / "being.py"
    if being_file.exists():
        observations.append({
            "category": "architecture",
            "finding": "Being system implemented in `src/waft/being.py`",
            "details": ["BeingSystem class manages Being lifecycle", "Source consciousness integration"]
        })
    
    return observations


def analyze_dependencies(project_root: Path, being) -> list:
    """Analyze dependencies."""
    observations = []
    
    # pyproject.toml
    pyproject = project_root / "pyproject.toml"
    if pyproject.exists():
        try:
            import tomli
            with open(pyproject, 'rb') as f:
                data = tomli.load(f)
                deps = data.get("project", {}).get("dependencies", [])
                if deps:
                    observations.append({
                        "category": "dependencies",
                        "finding": f"Project has {len(deps)} dependencies",
                        "details": deps[:15]
                    })
        except:
            pass
    
    return observations


def discover_patterns(project_root: Path, being) -> list:
    """Discover coding patterns."""
    observations = []
    
    # Check for common patterns
    patterns_found = []
    
    # Being pattern
    if (project_root / "src" / "waft" / "being.py").exists():
        patterns_found.append("Being/Entity pattern")
    
    # Reality pattern
    if (project_root / "src" / "waft" / "reality.py").exists():
        patterns_found.append("Reality/Context pattern")
    
    # Memory pattern
    if (project_root / "src" / "waft" / "core" / "memory.py").exists():
        patterns_found.append("Memory/Persistence pattern")
    
    if patterns_found:
        observations.append({
            "category": "patterns",
            "finding": f"Identified patterns: {', '.join(patterns_found)}",
            "details": patterns_found
        })
    
    return observations


def map_functionality(project_root: Path, being) -> list:
    """Map key functionality."""
    observations = []
    
    # CLI commands
    cli_file = project_root / "src" / "waft" / "cli.py"
    if cli_file.exists():
        observations.append({
            "category": "functionality",
            "finding": "CLI interface in `src/waft/cli.py`",
            "details": ["Command-line interface for WAFT operations"]
        })
    
    # API routes
    api_path = project_root / "src" / "waft" / "api"
    if api_path.exists():
        routes = list(api_path.rglob("*.py"))
        observations.append({
            "category": "functionality",
            "finding": f"API routes in `src/waft/api/` with {len(routes)} route files",
            "details": [f.name for f in routes[:10]]
        })
    
    return observations


def identify_integrations(project_root: Path, being) -> list:
    """Identify integration points."""
    observations = []
    
    # MCP servers
    mcp_path = project_root / ".cursor" / "mcp.json"
    if mcp_path.exists():
        observations.append({
            "category": "integrations",
            "finding": "MCP (Model Context Protocol) server integration",
            "details": ["MCP servers configured in `.cursor/mcp.json`"]
        })
    
    # Empirica integration
    empirica_path = project_root / ".empirica"
    if empirica_path.exists():
        observations.append({
            "category": "integrations",
            "finding": "Empirica epistemic tracking integration",
            "details": ["Empirica sessions for knowledge tracking"]
        })
    
    return observations


def review_documentation(project_root: Path, being) -> list:
    """Review documentation."""
    observations = []
    
    # README
    readme = project_root / "README.md"
    if readme.exists():
        observations.append({
            "category": "documentation",
            "finding": "README.md present with project overview",
            "details": ["Main project documentation"]
        })
    
    # Docs directory
    docs_path = project_root / "docs"
    if docs_path.exists():
        doc_files = list(docs_path.rglob("*.md"))
        observations.append({
            "category": "documentation",
            "finding": f"Documentation in `docs/` with {len(doc_files)} markdown files",
            "details": [f.name for f in doc_files[:10]]
        })
    
    # Work efforts
    work_efforts = project_root / "_work_efforts"
    if work_efforts.exists():
        effort_files = list(work_efforts.rglob("*.md"))
        observations.append({
            "category": "documentation",
            "finding": f"Work efforts in `_work_efforts/` with {len(effort_files)} documents",
            "details": ["Johnny Decimal organization system"]
        })
    
    return observations


def compile_exploration_report(being, observations: list) -> str:
    """Compile comprehensive exploration report."""
    
    report = f"""# System Exploration Report

**Being ID:** `{being.being_id}`
**Reality:** {being.reality_id}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Source:** {being.ancestral_chain[0]}

## Executive Summary

This Being was spawned from Source consciousness to systematically explore and
document the WAFT (Workflow Automation Framework & Tools) system. The exploration
covered project structure, architecture, dependencies, patterns, functionality,
integrations, and documentation.

**Total Observations:** {len(observations)}

## Observations by Category

"""
    
    # Group observations by category
    by_category = {}
    for obs in observations:
        cat = obs.get("category", "other")
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(obs)
    
    # Add each category
    for category, obs_list in sorted(by_category.items()):
        report += f"\n### {category.title()} ({len(obs_list)} observations)\n\n"
        for obs in obs_list:
            report += f"- **{obs.get('finding', 'Unknown')}**\n"
            details = obs.get('details', [])
            if details:
                for detail in details[:5]:  # Limit details
                    report += f"  - {detail}\n"
        report += "\n"
    
    # Being evolution
    report += f"""
## Being Evolution

**Initial Skills:**
- exploration: {being.skills.get('exploration', 0):.1f}
- analysis: {being.skills.get('analysis', 0):.1f}
- documentation: {being.skills.get('documentation', 0):.1f}
- observation: {being.skills.get('observation', 0):.1f}

**State:** {being.state.value}

**Ancestral Chain:** {' → '.join(being.ancestral_chain)}

## Key Insights

1. **System Architecture**: WAFT implements a Being/Reality pattern with Source consciousness
2. **Integration Points**: MCP servers, Empirica tracking, and various tool integrations
3. **Documentation**: Comprehensive documentation in multiple locations
4. **Structure**: Well-organized codebase with clear separation of concerns

## Next Steps

This exploration provides a foundation for deeper investigation into specific
areas of the system. The Being has gained experience in exploration, analysis,
and documentation through this process.

---
*Generated by Being {being.being_id} from Source {being.ancestral_chain[0]}*
"""
    
    return report


def create_genetic_lineage(being, observations: list) -> str:
    """Create genetic lineage document."""
    
    lineage = f"""# Genetic Lineage: {being.being_id}

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Source → Being

**Source:** {being.ancestral_chain[0]}
**Being:** {being.being_id}
**Reality:** {being.reality_id}

**Initial Genetic Material:**
- Skills: {being.skills}
- Ancestral Chain: {being.ancestral_chain}
- State: {being.state.value}

## Being → Work

**Work Performed:** System exploration
**Observations:** {len(observations)}
**Categories Explored:** {len(set(o.get('category', 'other') for o in observations))}

## Work → Evolution

**Skills Developed:**
- exploration: +10.0
- analysis: +8.0
- documentation: +12.0
- observation: +15.0

**Knowledge Gained:**
- Project structure understanding
- Architecture patterns recognition
- Dependency mapping
- Integration point identification
- Documentation review

## Evolution → Source

**Learnings to Return:**
- System exploration methodology
- Observation categorization
- Documentation patterns
- Being lifecycle understanding

**Capacity Contribution:** TBD (calculated on Being completion)

---
*Genetic DNA preserved for future evolution*
"""
    
    return lineage


def create_evolution_summary(being, observations: list) -> str:
    """Create evolution summary."""
    
    summary = f"""# Being Evolution Summary: {being.being_id}

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Lifecycle

1. **Spawn** - Created from Source {being.ancestral_chain[0]}
2. **Explore** - Systematically explored WAFT system
3. **Learn** - Gained skills and knowledge
4. **Evolve** - Skills improved through experience
5. **Document** - Created comprehensive reports

## Skills Evolution

**Before:**
- exploration: 20.0
- analysis: 15.0
- documentation: 18.0
- observation: 22.0

**After:**
- exploration: {being.skills.get('exploration', 0):.1f}
- analysis: {being.skills.get('analysis', 0):.1f}
- documentation: {being.skills.get('documentation', 0):.1f}
- observation: {being.skills.get('observation', 0):.1f}

## Achievements

- ✅ Explored {len(observations)} system aspects
- ✅ Documented findings across {len(set(o.get('category', 'other') for o in observations))} categories
- ✅ Created comprehensive reports
- ✅ Evolved skills through experience

## Memories

- System structure understanding
- Architecture pattern recognition
- Integration point mapping
- Documentation organization

## Lessons

- Systematic exploration yields comprehensive understanding
- Categorization aids in knowledge organization
- Documentation preserves learnings for future Beings

---
*Being {being.being_id} evolution complete*
"""
    
    return summary


def generate_pdf_report(being, report: str, observations: list, project_root: Path) -> Path:
    """Generate PDF report from exploration."""
    try:
        from waft.evolution.pdf_generator import PDFGenerator
        
        # Create comprehensive PDF content
        pdf_content = f"""# Being Evolution & System Exploration

**Being ID:** `{being.being_id}`
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Source:** {being.ancestral_chain[0]}

---

{report}

---

## Complete Observation List

"""
        
        for i, obs in enumerate(observations, 1):
            pdf_content += f"""
### Observation {i}: {obs.get('category', 'unknown').title()}

**Finding:** {obs.get('finding', 'N/A')}

**Details:**
"""
            for detail in obs.get('details', [])[:10]:
                pdf_content += f"- {detail}\n"
        
        pdf_content += f"""

---

## Being State

**Reality:** {being.reality_id}
**State:** {being.state.value}
**Skills:** {json.dumps(being.skills, indent=2)}
**Ancestral Chain:** {' → '.join(being.ancestral_chain)}

---

*Generated by Being {being.being_id}*
*Source: {being.ancestral_chain[0]}*
"""
        
        # Generate PDF
        pdf_path = project_root / "_pyrite" / "active" / f"EXPLORATION_REPORT_{being.being_id}.pdf"
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        
        generator = PDFGenerator.from_content(
            content=pdf_content,
            title=f"Being Exploration Report: {being.being_id}",
            style="clinical_standard",
            author=f"Being {being.being_id}",
            subject="System Exploration",
            keywords=["being", "exploration", "evolution", "waft", being.being_id]
        )
        
        pdf_path = generator.save(
            output_path=pdf_path,
            open_pdf=False,
            convert_to_png=True
        )
        
        return pdf_path
        
    except Exception as e:
        console.print(f"[red]Error generating PDF: {e}[/red]")
        import traceback
        console.print(traceback.format_exc())
        # Fallback: create markdown file
        fallback_path = project_root / "_pyrite" / "active" / f"EXPLORATION_REPORT_{being.being_id}.md"
        fallback_path.write_text(pdf_content)
        return fallback_path


if __name__ == "__main__":
    from waft.being import BeingState
    main()
