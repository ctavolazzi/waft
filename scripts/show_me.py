#!/usr/bin/env python3
"""
/show-me Command Implementation

Displays concepts, operations, and data from the current chat session.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

console = Console()

def get_work_efforts(project_path: Path) -> List[Dict[str, Any]]:
    """Get work efforts from current session."""
    work_efforts = []
    work_efforts_dir = project_path / "_work_efforts"
    
    if not work_efforts_dir.exists():
        return work_efforts
    
    # Look for recent work efforts (from today)
    # Work effort format: WE-YYMMDD-xxxx (e.g., WE-260116-32dq)
    today_pattern = datetime.now().strftime("%y%m%d")  # e.g., "260116"
    
    for item in work_efforts_dir.iterdir():
        if item.is_dir() and item.name.startswith("WE-"):
            # Check if it's from today (date pattern in work effort ID)
            is_today = today_pattern in item.name
            if is_today:
                # Extract work effort ID (first part before underscore, e.g., WE-260116-65m0)
                # Directory name might be: WE-260116-65m0_fogsift_waft_project_context_setup
                # Index file is: WE-260116-65m0_index.md
                work_effort_id = item.name.split("_")[0] if "_" in item.name else item.name
                index_file = item / f"{work_effort_id}_index.md"
                
                # Also try the full directory name as fallback
                if not index_file.exists():
                    index_file = item / f"{item.name}_index.md"
                
                if index_file.exists():
                    try:
                        content = index_file.read_text()
                        # Extract status
                        status = "open"
                        if "status: completed" in content.lower():
                            status = "completed"
                        elif "status: paused" in content.lower():
                            status = "paused"
                        elif "status: active" in content.lower():
                            status = "active"
                        elif "status: open" in content.lower():
                            status = "open"
                        
                        # Extract title
                        title = item.name
                        if "title:" in content:
                            for line in content.split("\n"):
                                if line.startswith("title:"):
                                    title = line.split(":", 1)[1].strip().strip('"')
                                    break
                        
                        work_efforts.append({
                            "id": item.name,
                            "title": title,
                            "status": status,
                            "path": str(item)
                        })
                    except Exception as e:
                        # Silently skip if we can't read the file
                        pass
    
    return work_efforts

def get_templates() -> List[Dict[str, Any]]:
    """Get LaTeX templates from registry."""
    try:
        from src.waft.templates.latex.registry import get_latex_registry
        registry = get_latex_registry()
        templates = registry.list_templates()
        
        return [
            {
                "name": t.name,
                "category": t.category,
                "tags": ", ".join(t.tags[:5]),
                "description": t.description[:60] + "..." if len(t.description) > 60 else t.description
            }
            for t in templates
        ]
    except Exception as e:
        console.print(f"[yellow]⚠️  Could not load templates: {e}[/yellow]")
        return []

def get_catalog_summary(project_path: Path) -> Dict[str, Any]:
    """Get Librarian catalog summary."""
    try:
        from src.waft.pantheon.library.librarian import Librarian
        librarian = Librarian(project_path=project_path)
        summary = librarian.generate_summary()
        
        # Get template entries
        template_entries = librarian.get_by_type("template")
        
        return {
            "total_records": summary.get("total_records", 0),
            "by_type": summary.get("by_type", {}),
            "by_category": summary.get("by_category", {}),
            "templates": len(template_entries),
            "entries": [
                {
                    "id": e.record_id,
                    "type": e.record_type,
                    "category": e.category,
                    "tags": ", ".join(e.tags[:3])
                }
                for e in template_entries[:10]
            ]
        }
    except Exception as e:
        console.print(f"[yellow]⚠️  Could not load catalog: {e}[/yellow]")
        return {"total_records": 0, "by_type": {}, "by_category": {}, "templates": 0, "entries": []}

def get_recent_experiments(project_path: Path) -> List[Dict[str, Any]]:
    """Get recent scientific method experiments."""
    experiments = []
    exp_dir = project_path / "scientific_method_tool" / "proof_experiments"
    
    if not exp_dir.exists():
        return experiments
    
    # Get recent experiment files
    exp_files_dir = exp_dir / "experiments"
    if exp_files_dir.exists():
        exp_files = sorted(exp_files_dir.glob("exp_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        
        for exp_file in exp_files[:5]:  # Last 5
            try:
                data = json.loads(exp_file.read_text())
                experiments.append({
                    "id": data.get("experiment_id", exp_file.stem),
                    "hypothesis": data.get("hypothesis", {}).get("statement", "N/A")[:50],
                    "status": data.get("status", "unknown"),
                    "verified": data.get("analysis", {}).get("verified", False)
                })
            except Exception:
                pass
    
    return experiments

def get_chat_context() -> Dict[str, Any]:
    """Extract chat context from current session."""
    # This would analyze the conversation, but for now return summary
    return {
        "session_date": datetime.now().strftime("%Y-%m-%d"),
        "key_concepts": [
            "LaTeX Template Integration",
            "Librarian Catalog System",
            "Scientific Method Tool",
            "Work Efforts Management"
        ],
        "operations": [
            "Integrated Unicamp Physics Report template",
            "Cataloged templates with Librarian",
            "Ran scientific method proofs",
            "Created work efforts"
        ],
        "systems_used": [
            "LaTeXTemplateRegistry",
            "Librarian",
            "Empirica",
            "Work Efforts System"
        ]
    }

def get_reasoning_trace(project_path: Path) -> List[Dict[str, Any]]:
    """Get reasoning trace - chain of thought and decisions."""
    traces = []
    
    # Try The Reasoner (Pantheon Entity) first
    try:
        from src.waft.pantheon.reasoner import TheReasoner
        reasoner = TheReasoner(project_path=project_path)
        reasoner_traces = reasoner.get_recent_traces(limit=10)
        traces.extend(reasoner_traces)
    except Exception:
        pass  # Continue if The Reasoner not available
    
    # Also get traces from reasoning_traces directory (legacy/script-based)
    try:
        # Import from scripts directory
        import sys
        scripts_dir = Path(__file__).parent
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))
        from reasoning_trace import extract_reasoning_trace
        script_traces = extract_reasoning_trace(project_path)
        # Merge, avoiding duplicates
        existing_ids = {t.get("trace_id") or t.get("source") for t in traces}
        for trace in script_traces:
            trace_id = trace.get("source") or trace.get("timestamp", "")
            if trace_id not in existing_ids:
                traces.append(trace)
    except Exception:
        pass  # Continue if script-based traces not available
    
    # Sort by timestamp (newest first)
    traces.sort(key=lambda t: t.get("timestamp", ""), reverse=True)
    
    return traces[:10]  # Return most recent 10

def get_proof_cases(project_path: Path) -> List[Dict[str, Any]]:
    """Get recent proof cases from /prove-it command."""
    proof_cases = []
    proof_cases_dir = project_path / "_work_efforts" / "proof_cases"
    
    if not proof_cases_dir.exists():
        return proof_cases
    
    # Get all case files, sorted by modification time (newest first)
    case_files = sorted(
        proof_cases_dir.glob("case_*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )[:10]  # Most recent 10
    
    for case_file in case_files:
        try:
            content = case_file.read_text()
            # Extract verdict and claim from frontmatter or content
            verdict = "UNKNOWN"
            claim = case_file.stem.replace("case_", "").replace("_", " ")
            
            if "VERDICT:" in content:
                for line in content.split("\n"):
                    if "VERDICT:" in line:
                        verdict = line.split("VERDICT:")[-1].strip()
                        break
            
            if "**Claim to Prove**:" in content:
                for line in content.split("\n"):
                    if "**Claim to Prove**:" in line:
                        claim = line.split("**Claim to Prove**:")[-1].strip()
                        break
            
            proof_cases.append({
                "id": case_file.stem,
                "claim": claim,
                "verdict": verdict,
                "path": str(case_file),
                "modified": datetime.fromtimestamp(case_file.stat().st_mtime).isoformat()
            })
        except Exception as e:
            # Silently skip if we can't read the file
            pass
    
    return proof_cases

def display_table_format(
    work_efforts: List[Dict[str, Any]],
    templates: List[Dict[str, Any]],
    catalog: Dict[str, Any],
    experiments: List[Dict[str, Any]],
    chat_context: Dict[str, Any],
    proof_cases: List[Dict[str, Any]] = None,
    reasoning_trace: List[Dict[str, Any]] = None
):
    """Display in table format."""
    console.print("\n[bold cyan]📊 SHOW-ME: Current Session Overview[/bold cyan]\n")
    
    # Work Efforts
    if work_efforts:
        console.print("[bold]📋 Work Efforts (Current Session)[/bold]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim")
        table.add_column("Title", style="bold")
        table.add_column("Status")
        
        for we in work_efforts[:10]:
            status_style = {
                "completed": "green",
                "active": "cyan",
                "paused": "yellow"
            }.get(we["status"], "dim")
            table.add_row(
                we["id"][:20] + "...",
                we["title"][:40] + "..." if len(we["title"]) > 40 else we["title"],
                f"[{status_style}]{we['status']}[/{status_style}]"
            )
        console.print(table)
        console.print()
    
    # Templates
    if templates:
        console.print("[bold]📄 LaTeX Templates[/bold]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Name", style="bold")
        table.add_column("Category")
        table.add_column("Tags")
        table.add_column("Description")
        
        for t in templates[:10]:
            table.add_row(
                t["name"],
                t["category"],
                t["tags"][:30] + "..." if len(t["tags"]) > 30 else t["tags"],
                t["description"]
            )
        console.print(table)
        console.print(f"[dim]Total: {len(templates)} templates[/dim]\n")
    
    # Catalog
    if catalog.get("total_records", 0) > 0:
        console.print("[bold]📚 Librarian Catalog[/bold]")
        console.print(f"Total Records: {catalog['total_records']}")
        console.print(f"Templates Cataloged: {catalog.get('templates', 0)}")
        
        if catalog.get("entries"):
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("ID", style="dim")
            table.add_column("Type")
            table.add_column("Category")
            table.add_column("Tags")
            
            for entry in catalog["entries"][:10]:
                table.add_row(
                    entry["id"][:25] + "..." if len(entry["id"]) > 25 else entry["id"],
                    entry["type"],
                    entry["category"],
                    entry["tags"]
                )
            console.print(table)
        console.print()
    
    # Experiments
    if experiments:
        console.print("[bold]🔬 Recent Experiments[/bold]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim")
        table.add_column("Hypothesis")
        table.add_column("Status")
        table.add_column("Verified")
        
        for exp in experiments:
            verified = "✅" if exp.get("verified") else "❌"
            table.add_row(
                exp["id"][:15] + "...",
                exp["hypothesis"],
                exp["status"],
                verified
            )
        console.print(table)
        console.print()
    
    # Proof Cases
    if proof_cases:
        console.print("[bold]🔍 Recent Proof Cases[/bold]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim")
        table.add_column("Claim", style="bold")
        table.add_column("Verdict")
        
        for case in proof_cases[:10]:
            verdict_style = {
                "PROVEN": "green",
                "DISPROVEN": "red",
                "INCONCLUSIVE": "yellow"
            }.get(case["verdict"], "dim")
            table.add_row(
                case["id"][:20] + "...",
                case["claim"][:50] + "..." if len(case["claim"]) > 50 else case["claim"],
                f"[{verdict_style}]{case['verdict']}[/{verdict_style}]"
            )
        console.print(table)
        console.print()
    
    # Reasoning Trace
    if reasoning_trace:
        console.print("[bold]🧠 Reasoning Trace[/bold]")
        console.print("[dim]Traceable chain of thought and decision-making[/dim]")
        console.print()
        
        for i, trace in enumerate(reasoning_trace[:5], 1):  # Show last 5
            decision = trace.get("decision", "Decision")[:60]
            reasoning = trace.get("reasoning", "No reasoning")[:100]
            console.print(f"[cyan]Step {i}:[/cyan] {decision}")
            console.print(f"[dim]  → {reasoning}...[/dim]")
            console.print()
    
    # Chat Context
    console.print("[bold]💬 Chat Context[/bold]")
    console.print(Panel(
        f"**Session Date:** {chat_context['session_date']}\n\n"
        f"**Key Concepts:**\n" + "\n".join(f"- {c}" for c in chat_context.get("key_concepts", [])) + "\n\n"
        f"**Operations:**\n" + "\n".join(f"- {o}" for o in chat_context.get("operations", [])) + "\n\n"
        f"**Systems Used:**\n" + "\n".join(f"- {s}" for s in chat_context.get("systems_used", [])),
        title="Current Session",
        border_style="cyan"
    ))

def display_json_format(
    work_efforts: List[Dict[str, Any]],
    templates: List[Dict[str, Any]],
    catalog: Dict[str, Any],
    experiments: List[Dict[str, Any]],
    chat_context: Dict[str, Any],
    proof_cases: List[Dict[str, Any]] = None,
    reasoning_trace: List[Dict[str, Any]] = None
):
    """Display in JSON format."""
    output = {
        "timestamp": datetime.now().isoformat(),
        "work_efforts": work_efforts,
        "templates": templates,
        "catalog": catalog,
        "experiments": experiments,
        "chat_context": chat_context,
        "proof_cases": proof_cases or [],
        "reasoning_trace": reasoning_trace or []
    }
    console.print(json.dumps(output, indent=2))

def generate_markdown_report(
    work_efforts: List[Dict[str, Any]],
    templates: List[Dict[str, Any]],
    catalog: Dict[str, Any],
    experiments: List[Dict[str, Any]],
    chat_context: Dict[str, Any],
    proof_cases: List[Dict[str, Any]] = None,
    reasoning_trace: List[Dict[str, Any]] = None
) -> str:
    """Generate markdown report."""
    md = f"""# WAFT Session Overview

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## Work Efforts

"""
    if work_efforts:
        for we in work_efforts:
            md += f"- **{we['id']}**: {we['title']} ({we['status']})\n"
    else:
        md += "No work efforts found.\n"
    
    md += "\n## LaTeX Templates\n\n"
    if templates:
        for t in templates[:20]:
            md += f"- **{t['name']}**: {t['description']} ({t['category']})\n"
    else:
        md += "No templates found.\n"
    
    md += "\n## Librarian Catalog\n\n"
    md += f"Total Records: {catalog.get('total_records', 0)}\n"
    md += f"Templates Cataloged: {catalog.get('templates', 0)}\n"
    
    md += "\n## Recent Experiments\n\n"
    if experiments:
        for exp in experiments:
            verified = "✅" if exp.get("verified") else "❌"
            md += f"- **{exp['id']}**: {exp['hypothesis']} {verified}\n"
    else:
        md += "No experiments found.\n"
    
    if proof_cases:
        md += "\n## Recent Proof Cases\n\n"
        for case in proof_cases:
            md += f"- **{case['id']}**: {case['claim']} - {case['verdict']}\n"
    
    if reasoning_trace:
        md += "\n## Reasoning Trace\n\n"
        md += "*Traceable chain of thought and decision-making*\n\n"
        for i, trace in enumerate(reasoning_trace, 1):
            md += f"### Step {i}: {trace.get('decision', 'Decision')}\n\n"
            md += f"**When:** {trace.get('timestamp', 'Unknown')}\n\n"
            md += f"**Reasoning:**\n{trace.get('reasoning', 'No reasoning provided')}\n\n"
            if trace.get('outcome'):
                md += f"**Outcome:** {trace['outcome']}\n\n"
            md += "---\n\n"
    
    md += "\n## Chat Context\n\n"
    md += f"**Session Date:** {chat_context['session_date']}\n\n"
    md += "**Key Concepts:**\n"
    for c in chat_context.get("key_concepts", []):
        md += f"- {c}\n"
    md += "\n**Operations:**\n"
    for o in chat_context.get("operations", []):
        md += f"- {o}\n"
    md += "\n**Systems Used:**\n"
    for s in chat_context.get("systems_used", []):
        md += f"- {s}\n"
    
    return md

def generate_pdf_report(
    project_path: Path,
    output_path: Optional[Path] = None,
    work_efforts: List[Dict[str, Any]] = None,
    templates: List[Dict[str, Any]] = None,
    catalog: Dict[str, Any] = None,
    experiments: List[Dict[str, Any]] = None,
    chat_context: Dict[str, Any] = None,
    proof_cases: List[Dict[str, Any]] = None
) -> Path:
    """Generate PDF report."""
    try:
        from src.waft.pdf import PDF
        
        md_content = generate_markdown_report(
            work_efforts or [],
            templates or [],
            catalog or {},
            experiments or [],
            chat_context or {},
            proof_cases or []
        )
        
        if output_path is None:
            output_path = project_path / "_work_efforts" / f"session_overview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        else:
            output_path = Path(output_path)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        pdf = PDF.from_markdown(
            markdown=md_content,
            title="WAFT Session Overview",
            output_path=output_path
        )
        pdf.save(str(output_path))
        
        return output_path
    except Exception as e:
        console.print(f"[red]Error generating PDF: {e}[/red]")
        raise

def generate_html_report(
    project_path: Path,
    output_path: Optional[Path] = None,
    work_efforts: List[Dict[str, Any]] = None,
    templates: List[Dict[str, Any]] = None,
    catalog: Dict[str, Any] = None,
    experiments: List[Dict[str, Any]] = None,
    chat_context: Dict[str, Any] = None,
    proof_cases: List[Dict[str, Any]] = None,
    reasoning_trace: List[Dict[str, Any]] = None
) -> Path:
    """Generate HTML report with beautiful styling."""
    import markdown
    
    md_content = generate_markdown_report(
        work_efforts or [],
        templates or [],
        catalog or {},
        experiments or [],
        chat_context or {},
        proof_cases or [],
        reasoning_trace or []
    )
    
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'nl2br'])
    
    # Use WAFT HTML template
    try:
        from src.waft.templates.waft_html_template import generate_waft_html
        
        if output_path is None:
            output_path = project_path / "_work_efforts" / f"session_overview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        else:
            output_path = Path(output_path)
        
        # Check if WeasyPrint is available for PDF conversion
        try:
            from weasyprint import HTML
            pdf_available = True
        except ImportError:
            pdf_available = False
        
        html_path = generate_waft_html(
            title="WAFT Session Overview",
            content=html_content,
            output_path=output_path,
            pdf_available=pdf_available
        )
        
        return html_path
    except ImportError:
        # Fallback to basic HTML if template not available
        console.print("[yellow]⚠️  WAFT template not available, using basic HTML[/yellow]")
        pass
    
    # Fallback: Basic HTML (original implementation)
    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WAFT Session Overview - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.7;
            color: #333;
            background: #f8f9fa;
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            border: none;
            padding: 0;
        }}
        .header .meta {{
            opacity: 0.9;
            font-size: 0.9rem;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}
        h2 {{
            color: #34495e;
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #7f8c8d;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }}
        code {{
            background: #ecf0f1;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.9em;
        }}
        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 1rem;
            border-radius: 5px;
            overflow-x: auto;
            margin: 1rem 0;
        }}
        pre code {{
            background: transparent;
            padding: 0;
            color: inherit;
        }}
        ul, ol {{
            margin-left: 2rem;
            margin-bottom: 1rem;
        }}
        li {{
            margin-bottom: 0.5rem;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1.5rem 0;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-radius: 5px;
            overflow: hidden;
        }}
        th, td {{
            border: 1px solid #e0e0e0;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
        }}
        tr:nth-child(even) {{
            background: #f8f9fa;
        }}
        tr:hover {{
            background: #e8eaf6;
        }}
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 600;
        }}
        .badge-proven {{
            background: #4caf50;
            color: white;
        }}
        .badge-disproven {{
            background: #f44336;
            color: white;
        }}
        .badge-inconclusive {{
            background: #ff9800;
            color: white;
        }}
        .badge-completed {{
            background: #4caf50;
            color: white;
        }}
        .badge-active {{
            background: #2196f3;
            color: white;
        }}
        .badge-paused {{
            background: #ff9800;
            color: white;
        }}
        .badge-open {{
            background: #9e9e9e;
            color: white;
        }}
        .footer {{
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 2px solid #e0e0e0;
            text-align: center;
            color: #7f8c8d;
            font-size: 0.9rem;
        }}
        @media print {{
            body {{
                background: white;
                padding: 1rem;
            }}
            .header {{
                page-break-after: avoid;
            }}
            h2 {{
                page-break-after: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>WAFT Session Overview</h1>
        <div class="meta">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
    </div>
    {html_content}
    <div class="footer">
        <p>Generated by WAFT (Wave Agent Framework & Tools)</p>
        <p>This HTML can be converted to PDF, LaTeX, or other formats</p>
    </div>
</body>
</html>
"""
    
    if output_path is None:
        output_path = project_path / "_work_efforts" / f"session_overview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    else:
        output_path = Path(output_path)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_doc)
    
    return output_path

def convert_html_to_pdf(html_path: Path, output_path: Optional[Path] = None) -> Path:
    """Convert HTML file to PDF using WAFT's integrated PDF conversion algorithm."""
    try:
        from src.waft.templates.waft_html_template import convert_waft_html_to_pdf
        
        if output_path is None:
            output_path = html_path.with_suffix('.pdf')
        else:
            output_path = Path(output_path)
        
        # Use WAFT's PDF conversion algorithm
        pdf_path = convert_waft_html_to_pdf(html_path, output_path)
        return pdf_path
    except ImportError:
        # Fallback to direct WeasyPrint if template not available
        try:
            from weasyprint import HTML
            
            if output_path is None:
                output_path = html_path.with_suffix('.pdf')
            else:
                output_path = Path(output_path)
            
            HTML(filename=str(html_path)).write_pdf(str(output_path))
            return output_path
        except ImportError:
            raise ImportError("WeasyPrint required for PDF conversion. Install with: pip install weasyprint")
    except Exception as e:
        raise Exception(f"PDF conversion failed: {e}")

def convert_html_to_latex(html_path: Path, output_path: Optional[Path] = None) -> Path:
    """Convert HTML file to LaTeX."""
    try:
        from src.waft.templates.latex.content_builders import html_to_latex
        
        html_content = html_path.read_text()
        
        # Extract body content
        import re
        body_match = re.search(r'<body>(.*?)</body>', html_content, re.DOTALL)
        if body_match:
            body_content = body_match.group(1)
        else:
            body_content = html_content
        
        latex_content = html_to_latex(body_content)
        
        # Wrap in LaTeX document
        latex_doc = f"""\\documentclass[11pt]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{geometry}}
\\geometry{{a4paper, margin=2.5cm}}
\\usepackage{{hyperref}}
\\usepackage{{xcolor}}
\\usepackage{{listings}}

\\title{{WAFT Session Overview}}
\\author{{Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}}
\\date{{\\today}}

\\begin{{document}}
\\maketitle

{latex_content}

\\end{{document}}
"""
        
        if output_path is None:
            output_path = html_path.with_suffix('.tex')
        else:
            output_path = Path(output_path)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(latex_doc)
        
        return output_path
    except Exception as e:
        raise Exception(f"LaTeX conversion failed: {e}")

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Show concepts, operations, and data from current session")
    parser.add_argument("--work-efforts", "-w", action="store_true", default=True, help="Show work efforts")
    parser.add_argument("--templates", "-t", action="store_true", default=True, help="Show templates")
    parser.add_argument("--catalog", "-c", action="store_true", default=True, help="Show catalog")
    parser.add_argument("--experiments", "-e", action="store_true", default=True, help="Show experiments")
    parser.add_argument("--chat-context", "-x", action="store_true", default=True, help="Show chat context")
    parser.add_argument("--proof-cases", "-p", action="store_true", default=True, help="Show proof cases")
    parser.add_argument("--reasoning-trace", "-r", action="store_true", default=True, help="Show reasoning trace (chain of thought)")
    parser.add_argument("--format", "-f", choices=["html", "table", "json", "markdown", "pdf", "latex"], default="html", help="Output format (default: html)")
    parser.add_argument("--output", "-o", type=str, help="Output file path (required for html/pdf/latex formats)")
    parser.add_argument("--convert", choices=["pdf", "latex"], help="Convert HTML output to another format")
    parser.add_argument("--path", "-P", type=str, help="Project path (default: current directory)")
    
    args = parser.parse_args()
    
    project_path = Path(args.path) if args.path else Path.cwd()
    
    # Collect data
    work_efforts = get_work_efforts(project_path) if args.work_efforts else []
    templates = get_templates() if args.templates else []
    catalog = get_catalog_summary(project_path) if args.catalog else {}
    experiments = get_recent_experiments(project_path) if args.experiments else []
    chat_context = get_chat_context() if args.chat_context else {}
    proof_cases = get_proof_cases(project_path) if args.proof_cases else []
    reasoning_trace = get_reasoning_trace(project_path) if args.reasoning_trace else []
    
    # Display or generate report
    if args.format == "json":
        display_json_format(work_efforts, templates, catalog, experiments, chat_context, proof_cases)
    elif args.format == "html":
        # HTML is now the default format
        output_path = Path(args.output) if args.output else None
        html_path = generate_html_report(
            project_path, output_path, work_efforts, templates, catalog, experiments, chat_context, proof_cases, reasoning_trace
        )
        console.print(f"[green]✅ HTML generated: {html_path}[/green]")
        
        # SHOW IT! Open in browser
        import subprocess
        import platform
        system = platform.system()
        try:
            if system == "Darwin":  # macOS
                subprocess.run(["open", str(html_path)], check=False)
                console.print(f"[cyan]🌐 Opening in browser...[/cyan]")
            elif system == "Windows":
                subprocess.run(["start", str(html_path)], shell=True, check=False)
                console.print(f"[cyan]🌐 Opening in browser...[/cyan]")
            elif system == "Linux":
                subprocess.run(["xdg-open", str(html_path)], check=False)
                console.print(f"[cyan]🌐 Opening in browser...[/cyan]")
        except Exception as e:
            console.print(f"[yellow]⚠️  Could not open browser automatically: {e}[/yellow]")
            console.print(f"[dim]Open manually: {html_path}[/dim]")
        
        # Convert if requested
        if args.convert == "pdf":
            try:
                pdf_path = convert_html_to_pdf(html_path)
                console.print(f"[green]✅ PDF generated: {pdf_path}[/green]")
            except Exception as e:
                console.print(f"[red]❌ PDF conversion failed: {e}[/red]")
        elif args.convert == "latex":
            try:
                tex_path = convert_html_to_latex(html_path)
                console.print(f"[green]✅ LaTeX generated: {tex_path}[/green]")
            except Exception as e:
                console.print(f"[red]❌ LaTeX conversion failed: {e}[/red]")
    elif args.format == "pdf":
        # Generate HTML first, then convert to PDF
        html_path = generate_html_report(
            project_path, None, work_efforts, templates, catalog, experiments, chat_context, proof_cases
        )
        output_path = Path(args.output) if args.output else html_path.with_suffix('.pdf')
        pdf_path = convert_html_to_pdf(html_path, output_path)
        console.print(f"[green]✅ PDF generated: {pdf_path}[/green]")
        
        # SHOW IT! Open PDF
        import subprocess
        import platform
        system = platform.system()
        try:
            if system == "Darwin":  # macOS
                subprocess.run(["open", str(pdf_path)], check=False)
                console.print(f"[cyan]📄 Opening PDF...[/cyan]")
            elif system == "Windows":
                subprocess.run(["start", str(pdf_path)], shell=True, check=False)
                console.print(f"[cyan]📄 Opening PDF...[/cyan]")
            elif system == "Linux":
                subprocess.run(["xdg-open", str(pdf_path)], check=False)
                console.print(f"[cyan]📄 Opening PDF...[/cyan]")
        except Exception as e:
            console.print(f"[yellow]⚠️  Could not open PDF automatically: {e}[/yellow]")
            console.print(f"[dim]Open manually: {pdf_path}[/dim]")
    elif args.format == "latex":
        # Generate HTML first, then convert to LaTeX
        html_path = generate_html_report(
            project_path, None, work_efforts, templates, catalog, experiments, chat_context, proof_cases
        )
        output_path = Path(args.output) if args.output else html_path.with_suffix('.tex')
        tex_path = convert_html_to_latex(html_path, output_path)
        console.print(f"[green]✅ LaTeX generated: {tex_path}[/green]")
    elif args.format == "markdown":
        md_content = generate_markdown_report(work_efforts, templates, catalog, experiments, chat_context, proof_cases, reasoning_trace)
        console.print(md_content)
    else:
        # Table format (fallback) - this already displays in console
        display_table_format(work_efforts, templates, catalog, experiments, chat_context, proof_cases, reasoning_trace)

if __name__ == "__main__":
    main()
