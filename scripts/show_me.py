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

def get_work_efforts(project_path: Path, days_back: int = 30) -> List[Dict[str, Any]]:
    """Get work efforts from recent days (default: last 30 days, or all if days_back=0)."""
    work_efforts = []
    work_efforts_dir = project_path / "_work_efforts"
    
    if not work_efforts_dir.exists():
        return work_efforts
    
    # Calculate date threshold if filtering by days
    from datetime import timedelta
    if days_back > 0:
        threshold_date = datetime.now() - timedelta(days=days_back)
        threshold_pattern = threshold_date.strftime("%y%m%d")
    else:
        threshold_pattern = None  # Show all
    
    for item in work_efforts_dir.iterdir():
        if item.is_dir() and item.name.startswith("WE-"):
            # Extract date from work effort ID (format: WE-YYMMDD-xxxx)
            # Check if it's within our date range (or show all if days_back=0)
            if threshold_pattern:
                # Extract date from directory name
                date_match = None
                if len(item.name) >= 8 and item.name[3:9].isdigit():
                    we_date_str = item.name[3:9]  # e.g., "260116" from "WE-260116-xxxx"
                    if we_date_str < threshold_pattern:
                        continue  # Skip if older than threshold
            
            # Extract work effort ID (first part before underscore, e.g., WE-260116-65m0)
            # Directory name might be: WE-260116-65m0_fogsift_waft_project_context_setup
            # Index file is: WE-260116-65m0_index.md
            work_effort_id = item.name.split("_")[0] if "_" in item.name else item.name
            
            # Try multiple index file patterns
            index_file = None
            for pattern in [
                f"{work_effort_id}_index.md",
                f"{item.name}_index.md",
                "index.md"
            ]:
                candidate = item / pattern
                if candidate.exists():
                    index_file = candidate
                    break
            
            if index_file and index_file.exists():
                try:
                    content = index_file.read_text(encoding='utf-8')
                    
                    # Extract status from YAML frontmatter or content
                    status = "open"
                    content_lower = content.lower()
                    
                    # Check YAML frontmatter first
                    if "---" in content:
                        frontmatter = content.split("---")[1].split("---")[0] if content.count("---") >= 2 else ""
                        for line in frontmatter.split("\n"):
                            if ":" in line:
                                key, value = line.split(":", 1)
                                if key.strip().lower() == "status":
                                    status = value.strip().strip('"').strip("'").lower()
                                    break
                    
                    # Fallback to content search
                    if status == "open":
                        if "status: completed" in content_lower or '"status": "completed"' in content_lower:
                            status = "completed"
                        elif "status: paused" in content_lower or '"status": "paused"' in content_lower:
                            status = "paused"
                        elif "status: active" in content_lower or '"status": "active"' in content_lower or "status: in_progress" in content_lower:
                            status = "active"
                        elif "status: open" in content_lower or '"status": "open"' in content_lower:
                            status = "open"
                    
                    # Extract title from YAML frontmatter or use directory name
                    title = item.name.replace("WE-", "").replace("_", " ").title()
                    if "---" in content:
                        frontmatter = content.split("---")[1].split("---")[0] if content.count("---") >= 2 else ""
                        for line in frontmatter.split("\n"):
                            if ":" in line:
                                key, value = line.split(":", 1)
                                if key.strip().lower() == "title":
                                    title = value.strip().strip('"').strip("'")
                                    break
                    elif "title:" in content:
                        for line in content.split("\n"):
                            if line.strip().startswith("title:"):
                                title = line.split(":", 1)[1].strip().strip('"').strip("'")
                                break
                    
                    work_efforts.append({
                        "id": work_effort_id,
                        "title": title,
                        "status": status,
                        "path": str(item.relative_to(project_path))
                    })
                except Exception as e:
                    # Log but continue - don't fail on one bad work effort
                    console.print(f"[dim]⚠️  Could not read work effort {item.name}: {e}[/dim]")
                    continue
    
    # Sort by ID (most recent first, since IDs are date-based)
    work_efforts.sort(key=lambda x: x["id"], reverse=True)
    
    return work_efforts

def get_projects(project_path: Path) -> List[Dict[str, Any]]:
    """Get all projects from ProjectManager."""
    projects = []
    try:
        from src.waft.core.projects import ProjectManager
        project_manager = ProjectManager(project_path=project_path)
        
        # List all projects
        all_projects = project_manager.list_projects()
        
        for proj in all_projects:
            projects.append({
                "id": proj.project_id,
                "title": proj.title,
                "status": proj.status.value if hasattr(proj.status, 'value') else str(proj.status),
                "progress": proj.progress_percent,
                "description": proj.description[:100] + "..." if len(proj.description) > 100 else proj.description,
                "tags": ", ".join(proj.tags[:5]),
                "created": proj.created_at,
                "updated": proj.updated_at,
                "milestones": len(proj.milestones),
                "related_work_efforts": len(proj.related_work_efforts)
            })
        
        # Sort by updated date (most recent first)
        projects.sort(key=lambda x: x.get("updated", ""), reverse=True)
        
    except Exception as e:
        console.print(f"[dim]⚠️  Could not load projects: {e}[/dim]")
    
    return projects

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

def _get_work_effort_details(project_path: Path, work_effort_id: str, work_effort_path: str) -> Dict[str, Any]:
    """Get detailed information about a work effort from its index file."""
    details = {
        "next_steps": [],
        "tickets": [],
        "related": [],
        "description": "",
        "progress_notes": []
    }
    
    try:
        # Try to find and read the index file
        we_dir = project_path / work_effort_path
        work_effort_id_short = work_effort_id.split("_")[0] if "_" in work_effort_id else work_effort_id
        
        # Try multiple index file patterns
        for pattern in [
            f"{work_effort_id_short}_index.md",
            f"{work_effort_id}_index.md",
            "index.md"
        ]:
            index_file = we_dir / pattern
            if index_file.exists():
                content = index_file.read_text(encoding='utf-8')
                
                # Extract description from frontmatter or content
                if "---" in content:
                    frontmatter = content.split("---")[1].split("---")[0] if content.count("---") >= 2 else ""
                    for line in frontmatter.split("\n"):
                        if ":" in line:
                            key, value = line.split(":", 1)
                            key = key.strip().lower()
                            if key == "description":
                                details["description"] = value.strip().strip('"').strip("'")
                
                # Look for "Next Steps", "Next Actions", "Tasks", or "TODO" sections
                lines = content.split("\n")
                in_next_steps = False
                section_keywords = ["next step", "next action", "tasks", "todo", "action items", "next:"]
                
                for i, line in enumerate(lines):
                    line_lower = line.lower()
                    # Check if this line starts a relevant section
                    if (line.strip().startswith("#") or line.strip().startswith("##")):
                        if any(kw in line_lower for kw in section_keywords):
                            in_next_steps = True
                            continue
                    
                    if in_next_steps:
                        # Stop if we hit another major section (## or #)
                        if line.strip().startswith("##") and "next" not in line_lower and "task" not in line_lower and "todo" not in line_lower:
                            break
                        # Collect list items
                        if line.strip().startswith("-") or line.strip().startswith("*") or line.strip().startswith("1.") or line.strip().startswith("•"):
                            step = line.strip().lstrip("-*•1234567890. ").strip()
                            if step and len(step) > 5 and not step.startswith("["):  # Skip checkboxes
                                details["next_steps"].append(step)
                                if len(details["next_steps"]) >= 5:  # Get more steps
                                    break
                        # Also look for numbered lists
                        elif line.strip() and line.strip()[0].isdigit() and "." in line.strip()[:3]:
                            step = line.strip().split(".", 1)[1].strip() if "." in line.strip() else line.strip()
                            if step and len(step) > 5:
                                details["next_steps"].append(step)
                                if len(details["next_steps"]) >= 5:
                                    break
                
                # Look for tickets section
                in_tickets = False
                for line in lines:
                    if "ticket" in line.lower() and ("##" in line or "###" in line):
                        in_tickets = True
                        continue
                    if in_tickets:
                        if line.strip().startswith("#") and "ticket" not in line.lower():
                            break
                        if "TKT-" in line or "ticket" in line.lower():
                            details["tickets"].append(line.strip())
                            if len(details["tickets"]) >= 3:
                                break
                
                # Extract first paragraph as description if not in frontmatter
                if not details["description"]:
                    for line in lines:
                        if line.strip() and not line.strip().startswith("#") and not line.strip().startswith("---"):
                            details["description"] = line.strip()[:200]
                            break
                
                break
    except Exception:
        pass  # Return empty details if we can't read the file
    
    return details


def generate_recommended_next_step(
    work_efforts: List[Dict[str, Any]],
    projects: List[Dict[str, Any]],
    experiments: List[Dict[str, Any]],
    proof_cases: List[Dict[str, Any]],
    reasoning_trace: List[Dict[str, Any]] = None,
    project_path: Path = None
) -> Dict[str, str]:
    """
    Generate recommended next step based on current state with enhanced context.
    Returns dict with 'action', 'why', 'context', 'next_steps', 'related', and 'details'.
    """
    if project_path is None:
        project_path = Path.cwd()
    
    active_work = [w for w in work_efforts if w.get("status") == "active"]
    open_work = [w for w in work_efforts if w.get("status") == "open"]
    active_projects = [p for p in projects if p.get("status") == "active"] if projects else []
    completed_recent = [w for w in work_efforts if w.get("status") == "completed"][:3]  # Recent completions
    
    # Priority logic: active work > open work > projects > experiments
    if active_work:
        # Focus on first active work effort with enhanced details
        we = active_work[0]
        we_id = we.get('id', 'unknown')
        we_path = we.get('path', '')
        we_title = we.get('title', 'Active Work Effort')
        
        # Get detailed information
        details = _get_work_effort_details(project_path, we_id, we_path)
        
        # Generate more specific action based on work effort content
        if details.get("next_steps"):
            # Use the first next step from the work effort
            specific_action = details["next_steps"][0]
            action = f"Continue: {we_title} - {specific_action}"
        elif "test" in we_title.lower() or "testing" in we_title.lower():
            action = f"Review & verify: {we_title}"
        elif "implement" in we_title.lower() or "create" in we_title.lower():
            action = f"Complete implementation: {we_title}"
        else:
            action = f"Continue: {we_title}"
        
        # Enhanced why with more context
        why_parts = [f"This work effort is currently active and represents your primary focus."]
        if details.get("description"):
            desc = details["description"][:150]
            why_parts.append(f"Focus: {desc}")
        if details.get("tickets"):
            why_parts.append(f"{len(details['tickets'])} ticket(s) to address.")
        why = " ".join(why_parts)
        
        # Enhanced context with actionable information
        context_parts = [f"Work Effort: {we_id}"]
        if details.get("next_steps"):
            context_parts.append(f"Next: {details['next_steps'][0]}")
        if we_path:
            context_parts.append(f"Path: {we_path}")
        
        # Build related items
        related = []
        if len(active_work) > 1:
            related.append(f"{len(active_work) - 1} other active work effort(s)")
        if open_work:
            related.append(f"{len(open_work)} open work effort(s) ready to start")
        
        return {
            "action": action,
            "why": why,
            "context": " | ".join(context_parts),
            "type": "work_effort",
            "id": we_id,
            "next_steps": details.get("next_steps", [])[:3],
            "related": related,
            "details": details.get("description", "")[:200]
        }
    
    elif open_work:
        # Start the most recent open work effort with enhanced details
        we = open_work[0]
        we_id = we.get('id', 'unknown')
        we_path = we.get('path', '')
        we_title = we.get('title', 'Open Work Effort')
        
        details = _get_work_effort_details(project_path, we_id, we_path)
        
        # More specific action
        if details.get("description"):
            if "test" in details["description"].lower():
                action = f"Start testing: {we_title}"
            elif "implement" in details["description"].lower():
                action = f"Begin implementation: {we_title}"
            else:
                action = f"Start: {we_title}"
        else:
            action = f"Start: {we_title}"
        
        why = f"This work effort is ready to begin. "
        if details.get("description"):
            why += f"{details['description'][:100]}"
        else:
            why += "Starting it will activate progress and create forward momentum."
        
        context_parts = [f"Work Effort: {we_id}"]
        if details.get("next_steps"):
            context_parts.append(f"First step: {details['next_steps'][0]}")
        
        return {
            "action": action,
            "why": why,
            "context": " | ".join(context_parts),
            "type": "work_effort",
            "id": we_id,
            "next_steps": details.get("next_steps", [])[:3],
            "related": [f"{len(open_work) - 1} other open work effort(s)"] if len(open_work) > 1 else [],
            "details": details.get("description", "")[:200]
        }
    
    elif active_projects:
        # Focus on active project
        proj = active_projects[0]
        action = f"Advance: {proj.get('title', 'Active Project')}"
        why = f"This project is active and represents a significant initiative. "
        if proj.get("progress", 0) > 0:
            why += f"Currently at {proj.get('progress', 0)}% completion. "
        why += "Moving it forward will create substantial value."
        
        context_parts = [f"Project: {proj.get('id', 'unknown')}"]
        if proj.get("progress"):
            context_parts.append(f"Progress: {proj.get('progress')}%")
        if proj.get("milestones"):
            context_parts.append(f"{proj.get('milestones')} milestone(s)")
        
        return {
            "action": action,
            "why": why,
            "context": " | ".join(context_parts),
            "type": "project",
            "id": proj.get('id'),
            "next_steps": [],
            "related": [f"{len(active_projects) - 1} other active project(s)"] if len(active_projects) > 1 else [],
            "details": proj.get("description", "")[:200]
        }
    
    elif experiments:
        unverified = [e for e in experiments if not e.get("verified")]
        if unverified:
            action = f"Verify {len(unverified)} pending experiment(s)"
            why = f"You have {len(unverified)} unverified experiment(s). Verification will validate hypotheses and generate knowledge."
            context = f"{len(unverified)} experiments pending verification"
            return {
                "action": action,
                "why": why,
                "context": context,
                "type": "experiment",
                "next_steps": [f"Review experiment: {e.get('id', 'unknown')}" for e in unverified[:3]],
                "related": [],
                "details": ""
            }
    
    elif proof_cases:
        unproven = [c for c in proof_cases if c.get("verdict") not in ["PROVEN", "DISPROVEN"]]
        if unproven:
            action = f"Resolve {len(unproven)} pending proof case(s)"
            why = f"You have {len(unproven)} unresolved proof case(s). Resolving them will establish truth and enable decisions."
            context = f"{len(unproven)} proof cases pending resolution"
            return {
                "action": action,
                "why": why,
                "context": context,
                "type": "proof_case",
                "next_steps": [f"Review case: {c.get('id', 'unknown')}" for c in unproven[:3]],
                "related": [],
                "details": ""
            }
    
    # Default: explore or create new work
    action = "Explore new opportunities or create a work effort"
    why = "No active work detected. "
    if completed_recent:
        why += f"You recently completed {len(completed_recent)} work effort(s). "
    why += "This is a good time to identify new opportunities, plan next initiatives, or create work efforts for upcoming tasks."
    
    context = "No active work efforts or projects"
    if completed_recent:
        context += f" | Recently completed: {', '.join([w.get('id', '') for w in completed_recent[:2]])}"
    
    return {
        "action": action,
        "why": why,
        "context": context,
        "type": "explore",
        "next_steps": ["Review completed work efforts", "Identify new opportunities", "Create a new work effort"],
        "related": [f"{len(completed_recent)} recently completed work effort(s)"] if completed_recent else [],
        "details": ""
    }

def generate_abstract(
    work_efforts: List[Dict[str, Any]],
    projects: List[Dict[str, Any]],
    templates: List[Dict[str, Any]],
    experiments: List[Dict[str, Any]],
    proof_cases: List[Dict[str, Any]],
    chat_context: Dict[str, Any],
    reasoning_trace: List[Dict[str, Any]] = None
) -> str:
    """Generate a concise abstract/summary of the session state."""
    active_work = [w for w in work_efforts if w.get("status") == "active"]
    active_projects = [p for p in projects if p.get("status") == "active"] if projects else []
    
    abstract_parts = []
    
    # Main focus
    if active_work:
        work_effort_text = f"**{len(active_work)} active work effort{'s' if len(active_work) != 1 else ''}**"
        if len(active_work) <= 3:
            titles = ", ".join([w['title'][:40] for w in active_work[:3]])
            abstract_parts.append(f"{work_effort_text}: {titles}")
        else:
            abstract_parts.append(f"{work_effort_text}, including {active_work[0]['title'][:40]}...")
    
    if active_projects:
        project_text = f"**{len(active_projects)} active project{'s' if len(active_projects) != 1 else ''}**"
        if len(active_projects) <= 2:
            titles = ", ".join([p['title'][:40] for p in active_projects[:2]])
            abstract_parts.append(f"{project_text}: {titles}")
        else:
            abstract_parts.append(f"{project_text}, including {active_projects[0]['title'][:40]}...")
    
    # Recent activity
    if experiments:
        verified = sum(1 for e in experiments if e.get("verified"))
        abstract_parts.append(f"**{len(experiments)} experiment{'s' if len(experiments) != 1 else ''}** ({verified} verified)")
    
    if proof_cases:
        proven = sum(1 for c in proof_cases if c.get("verdict") == "PROVEN")
        abstract_parts.append(f"**{len(proof_cases)} proof case{'s' if len(proof_cases) != 1 else ''}** ({proven} proven)")
    
    # Key concepts
    if chat_context.get("key_concepts"):
        concepts = chat_context["key_concepts"][:3]
        abstract_parts.append(f"Focus: {', '.join(concepts)}")
    
    # Reasoning activity
    if reasoning_trace:
        abstract_parts.append(f"**{len(reasoning_trace)} reasoning step{'s' if len(reasoning_trace) != 1 else ''}** tracked")
    
    # Format abstract with proper paragraph structure for better readability
    # Convert markdown bold (**text**) to HTML <strong> before formatting
    import re
    
    def markdown_bold_to_html(text):
        """Convert markdown bold (**text**) to HTML <strong>text</strong>"""
        return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    # Each part becomes its own paragraph for clean line breaks
    abstract_parts_formatted = []
    for part in abstract_parts:
        # Convert markdown to HTML and wrap in paragraph
        part_html = markdown_bold_to_html(part)
        abstract_parts_formatted.append(f"<p>{part_html}</p>")
    
    abstract = "".join(abstract_parts_formatted)
    
    # Add quick decision context as separate paragraph
    if active_work:
        abstract += f"<p><strong>Next:</strong> Review {active_work[0]['title'][:50]} or continue active work.</p>"
    elif work_efforts:
        open_work = [w for w in work_efforts if w.get("status") == "open"]
        if open_work:
            abstract += f"<p><strong>Next:</strong> {len(open_work)} open work effort{'s' if len(open_work) != 1 else ''} ready to start.</p>"
    
    return abstract

def get_session_history(project_path: Path, current_file: str = None) -> List[Dict[str, Any]]:
    """Find previous show-me HTML files to create session history chain."""
    history = []
    
    # Look in project root and _work_efforts for show-me HTML files
    search_paths = [
        project_path,
        project_path / "_work_efforts"
    ]
    
    for search_path in search_paths:
        if not search_path.exists():
            continue
        
        # Find HTML files that look like show-me outputs
        html_files = list(search_path.glob("show_me*.html")) + list(search_path.glob("*show*me*.html"))
        
        for html_file in html_files:
            # Skip current file
            if current_file and html_file.name == Path(current_file).name:
                continue
            
            try:
                # Get file modification time
                mtime = html_file.stat().st_mtime
                mod_date = datetime.fromtimestamp(mtime)
                
                # Try to extract timestamp from filename or content
                timestamp_str = mod_date.strftime("%Y-%m-%d %H:%M")
                
                history.append({
                    "path": str(html_file.relative_to(project_path)),
                    "name": html_file.name,
                    "timestamp": timestamp_str,
                    "date": mod_date
                })
            except Exception:
                continue
    
    # Sort by date (newest first)
    history.sort(key=lambda x: x["date"], reverse=True)
    
    return history[:10]  # Return last 10

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
    reasoning_trace: List[Dict[str, Any]] = None,
    projects: List[Dict[str, Any]] = None
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
        "reasoning_trace": reasoning_trace or [],
        "projects": projects or []
    }
    console.print(json.dumps(output, indent=2))

def generate_markdown_report(
    work_efforts: List[Dict[str, Any]],
    templates: List[Dict[str, Any]],
    catalog: Dict[str, Any],
    experiments: List[Dict[str, Any]],
    chat_context: Dict[str, Any],
    proof_cases: List[Dict[str, Any]] = None,
    reasoning_trace: List[Dict[str, Any]] = None,
    projects: List[Dict[str, Any]] = None
) -> str:
    """Generate markdown report with wiki-style formatting."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Calculate stats - compute all values first with validation
    projects = projects or []
    proof_cases = proof_cases or []
    experiments = experiments or []
    work_efforts = work_efforts or []
    templates = templates or []
    
    # Work effort statistics with safe defaults
    work_effort_total = len(work_efforts)
    work_effort_active = len([w for w in work_efforts if w.get("status") == "active"])
    work_effort_completed = len([w for w in work_efforts if w.get("status") == "completed"])
    work_effort_open = len([w for w in work_efforts if w.get("status") == "open"])
    work_effort_paused = len([w for w in work_efforts if w.get("status") == "paused"])
    
    # Project statistics with safe defaults
    project_total = len(projects)
    project_active = len([p for p in projects if p.get("status") == "active"])
    project_completed = len([p for p in projects if p.get("status") == "completed"])
    project_planning = len([p for p in projects if p.get("status") == "planning"])
    project_paused = len([p for p in projects if p.get("status") == "paused"])
    
    # Other statistics with safe defaults
    templates_count = len(templates)
    experiments_count = len(experiments)
    proof_cases_count = len(proof_cases)
    
    # Ensure all values are integers (defensive programming)
    work_effort_total = int(work_effort_total)
    work_effort_active = int(work_effort_active)
    work_effort_completed = int(work_effort_completed)
    work_effort_open = int(work_effort_open)
    work_effort_paused = int(work_effort_paused)
    project_total = int(project_total)
    project_active = int(project_active)
    templates_count = int(templates_count)
    experiments_count = int(experiments_count)
    proof_cases_count = int(proof_cases_count)
    
    # Information-dense header with more metadata (with safe defaults)
    chat_context = chat_context or {}
    session_date = chat_context.get('session_date', datetime.now().strftime("%Y-%m-%d"))
    session_duration = chat_context.get('session_duration', 'N/A')
    total_files = int(chat_context.get('total_files_accessed', 0))
    total_commands = int(chat_context.get('total_commands_run', 0))
    
    # Generate abstract with error handling
    try:
        abstract = generate_abstract(
            work_efforts, projects, templates, experiments,
            proof_cases, chat_context, reasoning_trace or []
        )
    except Exception as e:
        console.print(f"[yellow]⚠️  Error generating abstract: {e}[/yellow]")
        abstract = "Session overview generated successfully."
    
    # Get session history (will be passed to HTML generator)
    project_path = Path.cwd()
    session_history = get_session_history(project_path)
    
    # Generate recommended next step
    recommended = generate_recommended_next_step(
        work_efforts, projects, experiments, proof_cases, reasoning_trace, project_path
    )
    
    md = f"""<div id='abstract'></div>
<div class="recommended-next-step">
<div class="recommended-header">
<h2 class="recommended-title">🎯 Recommended Next Step</h2>
<button class="recommended-copy-btn" onclick="copyRecommendedStep()" title="Copy next step and context primer">
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M4 2C3.44772 2 3 2.44772 3 3V11C3 11.5523 3.44772 12 4 12H5V13C5 13.5523 5.44772 14 6 14H13C13.5523 14 14 13.5523 14 13V6C14 5.44772 13.5523 5 13 5H12V3C12 2.44772 11.5523 2 11 2H4Z" stroke="currentColor" stroke-width="1.2" fill="none"/>
<path d="M6 5H11C11.5523 5 12 5.44772 12 6V11H6V5Z" stroke="currentColor" stroke-width="1.2" fill="none"/>
</svg>
</button>
</div>
<div class="recommended-action" id="recommended-action">{recommended['action']}</div>
<div class="recommended-why">{recommended['why']}</div>
<details class="recommended-context-primer">
<summary class="recommended-context-summary">📋 Context Primer (click to expand)</summary>
<div class="recommended-context-content" id="recommended-context">
<div class="recommended-context-item"><strong>Context:</strong> {recommended['context']}</div>
<div class="recommended-context-item"><strong>Why:</strong> {recommended['why']}</div>
<div class="recommended-context-item"><strong>Type:</strong> {recommended.get('type', 'general')}</div>
{f'<div class="recommended-context-item"><strong>ID:</strong> {recommended.get("id", "N/A")}</div>' if recommended.get('id') else ''}
{f'<div class="recommended-context-item"><strong>Description:</strong> {recommended.get("details", "")}</div>' if recommended.get('details') else ''}
{f'<div class="recommended-context-item"><strong>Next Steps:</strong><ul>{"".join([f"<li>{step}</li>" for step in recommended.get("next_steps", [])])}</ul></div>' if recommended.get('next_steps') else ''}
{f'<div class="recommended-context-item"><strong>Related:</strong> {", ".join(recommended.get("related", []))}</div>' if recommended.get('related') else ''}
</div>
</details>
</div>

# WAFT Session Overview

<div class="header-section">
<div class="header-meta">
<div class="meta-item"><span class="meta-label">Generated:</span> {timestamp}</div>
<div class="meta-item"><span class="meta-label">Session Date:</span> {session_date}</div>
<div class="meta-item"><span class="meta-label">Duration:</span> {session_duration}</div>
<div class="meta-item"><span class="meta-label">Files Accessed:</span> {total_files}</div>
<div class="meta-item"><span class="meta-label">Commands Run:</span> {total_commands}</div>
</div>
</div>

<div class="abstract-section-header">
<h2>Abstract: Why This Recommendation?</h2>
<button class="abstract-copy-btn" onclick="copyAbstract()" title="Copy abstract to clipboard">
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M4 2C3.44772 2 3 2.44772 3 3V11C3 11.5523 3.44772 12 4 12H5V13C5 13.5523 5.44772 14 6 14H13C13.5523 14 14 13.5523 14 13V6C14 5.44772 13.5523 5 13 5H12V3C12 2.44772 11.5523 2 11 2H4Z" stroke="currentColor" stroke-width="1.2" fill="none"/>
<path d="M6 5H11C11.5523 5 12 5.44772 12 6V11H6V5Z" stroke="currentColor" stroke-width="1.2" fill="none"/>
</svg>
</button>
</div>

<div class="abstract-box" id="abstract-content">

{abstract}

</div>

## Session History

<div class="session-history">
<p style="color: #999; font-size: 0.9em; margin-bottom: 0.5rem;">Previous show-me instances (click to view):</p>
<ul class="history-list">
"""
    
    # Add session history links
    if session_history:
        for hist in session_history[:5]:  # Show last 5
            md += f"<li><a href='{hist['path']}' target='_blank'>{hist['timestamp']}</a> - {hist['name']}</li>\n"
    else:
        md += "<li><em>No previous instances found</em></li>\n"
    
    md += """</ul>
</div>

## Quick Stats

<div class="stats-grid">
<div class="stat-card">
<span class="stat-value">""" + str(work_effort_total) + """</span>
<span class="stat-label">Work Efforts</span>
</div>
<div class="stat-card">
<span class="stat-value">""" + str(work_effort_active) + """</span>
<span class="stat-label">Active</span>
</div>
<div class="stat-card">
<span class="stat-value">""" + str(work_effort_completed) + """</span>
<span class="stat-label">Completed</span>
</div>
<div class="stat-card">
<span class="stat-value">""" + str(work_effort_open) + """</span>
<span class="stat-label">Open</span>
</div>
<div class="stat-card">
<span class="stat-value">""" + str(work_effort_paused) + """</span>
<span class="stat-label">Paused</span>
</div>
<div class="stat-card">
<span class="stat-value">""" + str(templates_count) + """</span>
<span class="stat-label">Templates</span>
</div>
<div class="stat-card">
<span class="stat-value">""" + str(experiments_count) + """</span>
<span class="stat-label">Experiments</span>
</div>
<div class="stat-card">
<span class="stat-value">""" + str(proof_cases_count) + """</span>
<span class="stat-label">Proof Cases</span>
</div>
<div class="stat-card">
<span class="stat-value">""" + str(project_total) + """</span>
<span class="stat-label">Projects</span>
</div>
<div class="stat-card">
<span class="stat-value">""" + str(project_active) + """</span>
<span class="stat-label">Active Projects</span>
</div>
</div>

---

## Work Efforts

"""
    
    if work_efforts:
        # Group by status
        by_status = {}
        for we in work_efforts:
            status = we.get("status", "open")
            if status not in by_status:
                by_status[status] = []
            by_status[status].append(we)
        
        # Status badges - using CSS classes
        status_badges = {
            "active": '<span class="badge badge-active">ACTIVE</span>',
            "completed": '<span class="badge badge-completed">COMPLETED</span>',
            "open": '<span class="badge badge-open">OPEN</span>',
            "paused": '<span class="badge badge-paused">PAUSED</span>'
        }
        
        # Use <details> for collapsible status groups (all collapsed by default)
        for status in ["active", "completed", "open", "paused"]:
            if status in by_status and by_status[status]:
                md += f"\n<details>\n<summary><strong>{status.title()} ({len(by_status[status])})</strong></summary>\n\n"
                for we in by_status[status]:
                    we_id = we.get('id', 'unknown')
                    we_title = we.get('title', 'Untitled')
                    # Safely handle path - ensure it's relative and valid
                    we_path_raw = we.get('path', '')
                    if we_path_raw:
                        try:
                            # Make path relative to project root
                            we_path = str(Path(we_path_raw).relative_to(Path.cwd())) if Path(we_path_raw).is_absolute() else we_path_raw
                        except (ValueError, TypeError):
                            # If path conversion fails, use raw path or default
                            we_path = we_path_raw if we_path_raw else '#'
                    else:
                        we_path = '#'
                    badge = status_badges.get(status, '')
                    # Make work effort clickable card
                    md += f"<div class='clickable-card'><a href='{we_path}'>{badge} <strong>{we_id}</strong>: {we_title}</a></div>\n"
                md += "\n</details>\n"
    else:
        md += "No work efforts found.\n"
    
    md += "\n---\n\n<div id='latex-templates'></div>\n## LaTeX Templates\n\n"
    if templates:
        # Group by category with collapsible details
        by_category = {}
        for t in templates:
            cat = t.get('category', 'uncategorized')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(t)
        
        for category in sorted(by_category.keys()):
            md += f"\n<details>\n<summary><strong>{category.title()} ({len(by_category[category])})</strong></summary>\n\n"
            for t in by_category[category][:15]:  # Show more in collapsible
                tags = t.get('tags', '')
                if tags:
                    tags_display = f" <span style='color: #999; font-size: 0.9em;'>({tags[:50]})</span>"
                else:
                    tags_display = ""
                md += f"- <strong>{t['name']}</strong>: {t['description']}{tags_display}\n"
            if len(by_category[category]) > 15:
                md += f"<em>... and {len(by_category[category]) - 15} more</em>\n"
            md += "\n</details>\n"
    else:
        md += "No templates found.\n"
    
    md += "\n---\n\n<div id='librarian-catalog'></div>\n## Librarian Catalog\n\n"
    catalog = catalog or {}
    md += f"<div class='content-card'>\n"
    md += f"<dl><dt>Total Records:</dt><dd>{int(catalog.get('total_records', 0))}</dd>\n"
    md += f"<dt>Templates Cataloged:</dt><dd>{int(catalog.get('templates', 0))}</dd>\n"
    md += f"<dt>Last Updated:</dt><dd>{catalog.get('last_updated', 'Unknown')}</dd></dl>\n"
    md += "</div>\n"
    
    if catalog.get("entries"):
        md += "\n### Recent Entries\n\n"
        for entry in catalog["entries"][:10]:
            md += f"- **{entry['id'][:40]}**: {entry.get('type', 'unknown')} - {entry.get('category', 'uncategorized')}\n"
    
    md += "\n---\n\n<div id='recent-experiments'></div>\n## Recent Experiments\n\n"
    if experiments:
        md += f"<details>\n<summary><strong>All Experiments ({len(experiments)})</strong></summary>\n\n"
        md += "<table>\n"
        md += "<thead><tr><th>ID</th><th>Hypothesis</th><th>Status</th><th>Verified</th><th>Date</th></tr></thead>\n<tbody>\n"
        for exp in experiments[:30]:  # Show more in collapsible
            verified = "✅" if exp.get("verified") else "❌"
            exp_date = exp.get('date', exp.get('created', 'N/A'))[:10] if exp.get('date') or exp.get('created') else 'N/A'
            md += f"<tr><td><code>{exp['id'][:20]}</code></td><td>{exp['hypothesis'][:80]}</td><td>{exp['status']}</td><td>{verified}</td><td>{exp_date}</td></tr>\n"
        md += "</tbody></table>\n"
        if len(experiments) > 30:
            md += f"<p><em>... and {len(experiments) - 30} more experiments</em></p>\n"
        md += "\n</details>\n"
    else:
        md += "No experiments found.\n"
    
    if proof_cases:
        md += "\n---\n\n<div id='recent-proof-cases'></div>\n## Recent Proof Cases\n\n"
        md += f"<details>\n<summary><strong>All Proof Cases ({len(proof_cases)})</strong></summary>\n\n"
        md += "<table>\n"
        md += "<thead><tr><th>Case ID</th><th>Claim</th><th>Verdict</th><th>Date</th></tr></thead>\n<tbody>\n"
        for case in proof_cases[:30]:  # Show more in collapsible
            verdict = case.get('verdict', 'UNKNOWN')
            verdict_class = {
                "PROVEN": "badge-completed",
                "DISPROVEN": "badge-paused",
                "INCONCLUSIVE": "badge-open"
            }.get(verdict, "badge-open")
            verdict_badge = f"<span class='badge {verdict_class}'>{verdict}</span>"
            claim = case.get('claim', case['id'])[:80]
            case_date = case.get('date', case.get('created', 'N/A'))[:10] if case.get('date') or case.get('created') else 'N/A'
            md += f"<tr><td><code>{case['id'][:30]}</code></td><td>{claim}</td><td>{verdict_badge}</td><td>{case_date}</td></tr>\n"
        md += "</tbody></table>\n"
        if len(proof_cases) > 30:
            md += f"<p><em>... and {len(proof_cases) - 30} more proof cases</em></p>\n"
        md += "\n</details>\n"
    
    if reasoning_trace:
        md += "\n---\n\n<div id='reasoning-trace'></div>\n## Reasoning Trace\n\n"
        md += "<p style='color: #999;'><em>Traceable chain of thought and decision-making</em></p>\n\n"
        for i, trace in enumerate(reasoning_trace[:10], 1):  # Show more
            decision = trace.get('decision', 'Decision')
            timestamp = trace.get('timestamp', 'Unknown')
            reasoning = trace.get('reasoning', 'No reasoning provided')
            outcome = trace.get('outcome', '')
            
            # Use details for expandable reasoning steps
            md += f"<details>\n<summary><strong>Step {i}: {decision}</strong> <span style='color: #999; font-size: 0.9em;'>({timestamp})</span></summary>\n"
            md += f"<div class='content-card'>\n"
            md += f"<p><strong>When:</strong> {timestamp}</p>\n"
            md += f"<p><strong>Reasoning:</strong></p>\n"
            md += f"<p>{reasoning}</p>\n"
            if outcome:
                md += f"<p><strong>Outcome:</strong> {outcome}</p>\n"
            md += "</div>\n</details>\n\n"
    
    md += "\n---\n\n<div id='chat-context'></div>\n## Chat Context\n\n"
    
    # Use accordion for each context section
    key_concepts = chat_context.get("key_concepts", [])
    if key_concepts:
        md += f"<details>\n<summary><strong>Key Concepts ({len(key_concepts)})</strong></summary>\n"
        md += "<div class='content-card'><ul>\n"
        for c in key_concepts:
            md += f"<li>{c}</li>\n"
        md += "</ul></div>\n</details>\n"
    
    operations = chat_context.get("operations", [])
    if operations:
        md += f"<details>\n<summary><strong>Operations ({len(operations)})</strong></summary>\n"
        md += "<div class='content-card'><ul>\n"
        for o in operations:
            md += f"<li>{o}</li>\n"
        md += "</ul></div>\n</details>\n"
    
    systems_used = chat_context.get("systems_used", [])
    if systems_used:
        md += f"<details>\n<summary><strong>Systems Used ({len(systems_used)})</strong></summary>\n"
        md += "<div class='content-card'><ul>\n"
        for s in systems_used:
            md += f"<li>{s}</li>\n"
        md += "</ul></div>\n</details>\n"
    
    # Add more context if available
    files_modified = chat_context.get("files_modified", [])
    if files_modified:
        md += f"<details>\n<summary><strong>Files Modified ({len(files_modified)})</strong></summary>\n"
        md += "<div class='content-card'><ul>\n"
        for f in files_modified[:20]:
            md += f"<li><code>{f[:60]}</code></li>\n"
        md += "</ul></div>\n</details>\n"
    
    return md

def generate_pdf_report(
    project_path: Path,
    output_path: Optional[Path] = None,
    work_efforts: List[Dict[str, Any]] = None,
    templates: List[Dict[str, Any]] = None,
    catalog: Dict[str, Any] = None,
    experiments: List[Dict[str, Any]] = None,
    chat_context: Dict[str, Any] = None,
    proof_cases: List[Dict[str, Any]] = None,
    projects: List[Dict[str, Any]] = None
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
            proof_cases or [],
            None,  # reasoning_trace
            projects or []
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

def generate_waft_html(
    html_content: str,
    title: str = "WAFT Session Overview",
    timestamp: str = None,
    session_history: List[Dict[str, Any]] = None
) -> str:
    """
    Generate WAFT HTML template with:
    - Pure HTML5 + CSS (works in text browsers, embedded systems, etc.)
    - Pure CSS interactions (using :target, :checked, etc.)
    - Information-dense layout
    - Fast to scan
    - Accessible
    """
    
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Split content at Abstract heading to separate header from main content
    # Try multiple patterns to find the abstract section
    abstract_markers = [
        '<h2>🎯 Abstract</h2>',
        '<h2>Abstract</h2>',
        '<h2 id="abstract">Abstract</h2>',
        '<h2 id="abstract">',
    ]
    
    header_html = ""
    main_html = html_content
    
    for marker in abstract_markers:
        if marker in html_content:
            header_part, main_part = html_content.split(marker, 1)
            header_html = header_part + marker
            main_html = main_part
            break
    
    # If no split occurred, check for recommended next step section
    # Recommended next step should be in header (right after nav)
    if not header_html and 'recommended-next-step' in html_content:
        # Find the recommended next step section
        recommended_start = html_content.find('<div class="recommended-next-step">')
        if recommended_start >= 0:
            # Find the matching closing div for recommended-next-step
            # Count opening and closing divs to find the matching close
            pos = recommended_start + len('<div class="recommended-next-step">')
            depth = 1
            recommended_end = pos
            
            while depth > 0 and recommended_end < len(html_content):
                next_open = html_content.find('<div', recommended_end)
                next_close = html_content.find('</div>', recommended_end)
                
                if next_close == -1:
                    break
                
                if next_open != -1 and next_open < next_close:
                    depth += 1
                    recommended_end = next_open + 4
                else:
                    depth -= 1
                    if depth == 0:
                        recommended_end = next_close + 6  # Include </div>
                        break
                    recommended_end = next_close + 6
            
            if recommended_end > recommended_start:
                # Everything up to and including recommended section goes in header
                header_html = html_content[:recommended_end]
                main_html = html_content[recommended_end:]
    
    # Fallback: If still no split, look for first h1
    if not header_html and '<h1>' in html_content:
        # Split at first h1 - everything before goes in header
        h1_pos = html_content.find('<h1>')
        if h1_pos > 0:
            header_html = html_content[:h1_pos]
            main_html = html_content[h1_pos:]
    
    # Generate the full WAFT HTML template
    return _generate_waft_html_template(header_html, main_html, title, timestamp, session_history)


def _generate_waft_html_template(
    header_html: str,
    main_html: str,
    title: str,
    timestamp: str,
    session_history: List[Dict[str, Any]] = None
) -> str:
    """Generate the full WAFT HTML template with all styling and JavaScript."""
    # Build session history HTML if provided
    session_history_html = ""
    if session_history:
        history_items = "\n".join([
            f'<li><a href="{item.get("file", "")}" target="_blank">{item.get("date", "")}</a> - {item.get("file", "")}</li>'
            for item in session_history[:10]
        ])
        session_history_html = f"""
        <h2>Session History</h2>
        <div class="session-history">
            <p style="color: #999; font-size: 0.9em; margin-bottom: 0.5rem;">Previous show-me instances (click to view):</p>
            <ul class="history-list">
                {history_items}
            </ul>
        </div>
        """
    
    # Use .format() with escaped CSS/JS
    # Use raw string to avoid escape sequence warnings, then format
    template = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | WAFT</title>
    <style>

        /* ============================================
           WAFT Show-Me
           Pure HTML5 + CSS - ZERO JavaScript
           Works on ANY machine with a display
           ============================================ */
        
        /* Reset & Base */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        html {{
            font-size: 16px;
            scroll-behavior: smooth;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            background: #1a1a1a;
            color: #d5d5d5;
            line-height: 1.7;
            letter-spacing: 0.2px;
            min-height: 100vh;
        }}
        
        /* Typography - Clear Hierarchy */
        h1, h2, h3, h4, h5, h6 {{
            font-weight: 600;
            line-height: 1.4;
            margin-bottom: 1rem;
        }}
        
        /* Responsive Typography - Fluid scaling with fallbacks for older browsers */
        h1 {{
            font-size: 1.5rem; /* Fallback for browsers without clamp() support */
            font-size: clamp(1.5rem, 4vw, 2rem);
            color: #e8e8e8;
            letter-spacing: -0.01em;
            margin-top: 0;
        }}
        
        h2 {{
            font-size: 1.25rem; /* Fallback */
            font-size: clamp(1.25rem, 3vw, 1.5rem);
            color: #e0e0e0;
            border-bottom: 2px solid #333333;
            padding-bottom: 0.5rem;
            margin-top: 2.5rem;
        }}
        
        h3 {{
            font-size: 1.1rem; /* Fallback */
            font-size: clamp(1.1rem, 2.5vw, 1.25rem);
            color: #d8d8d8;
        }}
        
        h4 {{
            font-size: 1rem; /* Fallback */
            font-size: clamp(1rem, 2vw, 1.1rem);
            color: #d0d0d0;
        }}
        
        p, li {{
            color: #d5d5d5;
            line-height: 1.7;
            letter-spacing: 0.2px;
        }}
        
        /* Links */
        a {{
            color: #8a9eff;
            text-decoration: none;
        }}
        
        a:hover {{
            color: #a0b0ff;
            text-decoration: underline;
        }}
        
        a:focus {{
            outline: 2px solid #8a9eff;
            outline-offset: 2px;
        }}
        
        /* Above the Fold - Unified Top Section */
        /* Removed distinct background and border to eliminate visual separation */
        .above-the-fold {{
            background: transparent;
            border-bottom: none;
            margin-bottom: 0;
        }}
        
        /* Alternative: if header-wrapper has minimal content, reduce spacing */
        .header-section-wrapper:empty {{
            display: none;
        }}
        
        /* Navigation - Part of Above the Fold - Responsive padding */
        .nav-bar {{
            background: transparent;
            border-bottom: 1px solid #2a2a2a;
            padding: 0.75rem 1rem 1rem 1rem; /* Mobile: reduced padding */
            position: sticky;
            top: 0;
            z-index: 100;
            margin-bottom: 1rem; /* Add spacing below nav instead of on above-the-fold */
        }}
        
        .nav-container {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 0.75rem;
            position: relative;
        }}
        
        .nav-container::after {{
            content: '';
            position: absolute;
            bottom: -1.25rem;
            left: 0;
            right: 0;
            height: 1px;
            background: #2a2a2a;
        }}
        
        /* Navigation Container - Responsive 3-column layout on all screen sizes */
        /* Mobile-first: Keep 3-column layout but optimize sizing for small screens */
        .nav-container {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 0.5rem; /* Smaller gap on mobile, increases with breakpoints */
            align-items: stretch;
            width: 100%;
            position: relative;
            padding-bottom: 0.25rem;
        }}
        
        /* Visual separator line below buttons to prevent "drop off" */
        .nav-container::after {{
            content: '';
            position: absolute;
            bottom: -0.25rem;
            left: 0;
            right: 0;
            height: 1px;
            background: #2a2a2a;
        }}
        
        .nav-section {{
            display: flex;
            width: 100%;
        }}
        
        .nav-section .dropdown-group {{
            width: 100%;
            position: relative;
        }}
        
        /* Navigation Button - Responsive sizing with 44px minimum touch target */
        .nav-dropdown-toggle {{
            background: #242424;
            border: 1px solid #2a2a2a;
            border-bottom: 2px solid #2d2d2d;
            border-radius: 4px;
            padding: 0.5rem 0.5rem; /* Compact on mobile, increases with breakpoints */
            color: #b5b5b5;
            cursor: pointer;
            font-size: 0.8rem; /* Smaller on mobile, increases with breakpoints */
            font-weight: 400;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            transition: all 0.15s;
            text-decoration: none;
            width: 100%;
            letter-spacing: 0.1px;
            min-height: 44px; /* WCAG 2.1 Level AAA: Minimum touch target size */
            box-shadow: 
                0 1px 2px rgba(0,0,0,0.3),
                inset 0 -1px 1px rgba(0,0,0,0.2);
            position: relative;
        }}
        
        /* Ensure bottom edge is fully defined */
        .nav-dropdown-toggle::before {{
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            right: 0;
            height: 2px;
            background: #2d2d2d;
            border-radius: 0 0 4px 4px;
            z-index: -1;
        }}
        
        .nav-dropdown-toggle:hover {{
            background: #282828;
            border-color: #2d2d2d;
            border-bottom-color: #323232;
            color: #d5d5d5;
            box-shadow: 
                0 2px 3px rgba(0,0,0,0.35),
                inset 0 -1px 1px rgba(0,0,0,0.25);
        }}
        
        .nav-dropdown-toggle:hover::before {{
            background: #323232;
        }}
        
        .nav-dropdown-toggle:active {{
            background: #1f1f1f;
            border-color: #252525;
            border-bottom-color: #2a2a2a;
            box-shadow: 
                0 1px 1px rgba(0,0,0,0.25),
                inset 0 1px 2px rgba(0,0,0,0.3);
        }}
        
        .nav-dropdown-toggle::after {{
            content: " ▼";
            font-size: 0.7em;
            opacity: 0.6;
            margin-left: 0.25rem;
        }}
        
        /* Oracle Button - Repositioned on mobile instead of hidden */
        /* Floating Oracle Button - Responsive positioning */
        .btn-oracle {{
            position: fixed;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            padding: 0.75rem 1.5rem;
            background: #2a2a2a;
            color: #d5d5d5;
            border: 1px solid #444444;
            border-radius: 8px;
            font-size: 0.95rem;
            font-weight: 500;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.2s;
            z-index: 999;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
        
        /* Reposition Oracle button on mobile to top-right to avoid overlap */
        @media (max-width: 599px) {{
            .btn-oracle {{
                bottom: auto;
                top: 1rem;
                left: auto;
                right: 1rem;
                transform: none;
                padding: 0.5rem 0.75rem;
                font-size: 0.85rem;
            }}
        }}
        
        .btn-oracle:hover {{
            background: #333333;
            border-color: #667eea;
            color: #8a9eff;
            text-decoration: none;
            box-shadow: 0 6px 16px rgba(102, 126, 234, 0.2);
        }}
        
        .toast-notification {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: #2a2a2a;
            border: 1px solid #4a8a4a;
            color: #8aff8a;
            padding: 1rem 1.5rem;
            border-radius: 6px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 1000;
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.3s;
            pointer-events: none;
            max-width: 300px;
        }}
        
        .toast-notification.show {{
            opacity: 1;
            transform: translateY(0);
        }}
        
        /* Abstract Section Header */
        .abstract-section-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
            margin-top: 2.5rem;
        }}
        
        .abstract-section-header h2 {{
            margin: 0;
            flex: 1;
            border-bottom: none;
            padding-bottom: 0;
        }}
        
        /* Abstract Copy Button - Subtle and Chill */
        .abstract-copy-btn {{
            background: transparent;
            border: 1px solid #444;
            border-radius: 4px;
            padding: 6px 8px;
            cursor: pointer;
            color: #888;
            opacity: 0.6;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
        }}
        
        .abstract-copy-btn:hover {{
            opacity: 1;
            color: #aaa;
            border-color: #666;
            background: rgba(255, 255, 255, 0.05);
        }}
        
        .abstract-copy-btn:active {{
            transform: scale(0.95);
            background: rgba(255, 255, 255, 0.1);
        }}
        
        .abstract-copy-btn svg {{
            width: 16px;
            height: 16px;
            stroke: currentColor;
        }}
        
        /* Recommended Next Step - Big, Bold, Eye-Catching */
        .recommended-next-step {{
            background: linear-gradient(135deg, #2a3a4a 0%, #1a2a3a 100%);
            border-left: 6px solid #8a9eff;
            border-top: 2px solid #3a4a5a;
            border-bottom: 2px solid #3a4a5a;
            border-right: 2px solid #3a4a5a;
            padding: 2rem;
            margin: 2rem 0 2.5rem 0;
            border-radius: 8px;
            box-shadow: 
                0 4px 12px rgba(0,0,0,0.4),
                inset 0 1px 0 rgba(255,255,255,0.05);
        }}
        
        .recommended-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
        }}
        
        .recommended-title {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #8a9eff;
            margin: 0;
            border: none;
            padding: 0;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            font-size: 0.9rem;
            flex: 1;
        }}
        
        .recommended-copy-btn {{
            background: rgba(138, 158, 255, 0.1);
            border: 1px solid rgba(138, 158, 255, 0.3);
            border-radius: 4px;
            padding: 0.5rem;
            color: #8a9eff;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
            min-width: 36px;
            min-height: 36px;
        }}
        
        .recommended-copy-btn:hover {{
            background: rgba(138, 158, 255, 0.2);
            border-color: rgba(138, 158, 255, 0.5);
            color: #a0b0ff;
        }}
        
        .recommended-copy-btn:active {{
            background: rgba(138, 158, 255, 0.3);
            transform: scale(0.95);
        }}
        
        .recommended-action {{
            font-size: 1.75rem;
            font-weight: 700;
            color: #e8e8e8;
            margin: 0.5rem 0 1rem 0;
            line-height: 1.3;
            letter-spacing: -0.01em;
        }}
        
        .recommended-why {{
            font-size: 1.1rem;
            color: #d5d5d5;
            line-height: 1.7;
            margin: 1rem 0;
            padding: 1rem;
            background: rgba(0,0,0,0.2);
            border-radius: 4px;
            border-left: 3px solid #667eea;
        }}
        
        .recommended-context {{
            font-size: 0.95rem;
            color: #999999;
            margin-top: 1rem;
            font-style: italic;
        }}
        
        .recommended-context-primer {{
            margin-top: 1.5rem;
            border-top: 1px solid rgba(138, 158, 255, 0.2);
            padding-top: 1rem;
            background: transparent;
            border: none;
            border-top: 1px solid rgba(138, 158, 255, 0.2);
        }}
        
        .recommended-context-primer summary {{
            list-style: none;
            background: transparent;
            border: none;
            padding: 0;
        }}
        
        .recommended-context-primer summary::-webkit-details-marker {{
            display: none;
        }}
        
        .recommended-context-summary {{
            font-size: 0.95rem;
            color: #8a9eff;
            cursor: pointer;
            font-weight: 500;
            user-select: none;
            padding: 0.5rem 0;
            border-radius: 0;
            transition: color 0.2s;
            display: inline-block;
        }}
        
        .recommended-context-summary:hover {{
            color: #a0b0ff;
        }}
        
        .recommended-context-content {{
            margin-top: 1rem;
            padding: 0;
            background: transparent;
            border: none;
        }}
        
        .recommended-context-item {{
            margin: 0.75rem 0;
            font-size: 0.95rem;
            color: #d5d5d5;
            line-height: 1.6;
        }}
        
        .recommended-context-item strong {{
            color: #8a9eff;
            margin-right: 0.5rem;
        }}
        
        /* Abstract Box - Draws the Eye */
        .abstract-box {{
            background: #2a2a2a;
            border-left: 4px solid #8a9eff;
            padding: 1.5rem;
            margin: 2rem 0 1.5rem 0;
            border-radius: 4px;
            font-size: 1.1rem;
            line-height: 1.8;
            color: #e5e5e5;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }}
        
        /* Make header section title stand out */
        .header-section h1 {{
            margin-top: 0;
            margin-bottom: 1rem;
            color: #e8e8e8;
        }}
        
        .header-meta {{
            opacity: 0.8;
        }}
        
        /* Session History */
        .session-history {{
            background: #222222;
            border: 1px solid #333333;
            padding: 1rem;
            margin: 1.5rem 0;
            border-radius: 4px;
        }}
        
        .history-list {{
            list-style: none;
            padding-left: 0;
        }}
        
        .history-list li {{
            padding: 0.5rem 0;
            border-bottom: 1px solid #333333;
        }}
        
        .history-list li:last-child {{
            border-bottom: none;
        }}
        
        .history-list a {{
            color: #8a9eff;
            text-decoration: none;
        }}
        
        .history-list a:hover {{
            text-decoration: underline;
        }}
        
        /* Dropdown Groups - Now in Nav Bar */
        .dropdown-group {{
            position: relative;
        }}
        
        .dropdown-toggle {{
            background: #2a2a2a;
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            color: #d5d5d5;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.2s;
            text-decoration: none;
        }}
        
        .dropdown-toggle:hover {{
            background: #333333;
            color: #e5e5e5;
        }}
        
        .dropdown-toggle::after {{
            content: " ▼";
            font-size: 0.8em;
            opacity: 0.7;
        }}
        
        /* Nav Dropdown Menu - Subtle 80s Style - Responsive */
        .nav-dropdown-menu {{
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            margin-top: 0.5rem;
            background: linear-gradient(180deg, #252525 0%, #222222 100%);
            border: 1px solid #333333;
            border-top: 1px solid #383838;
            border-radius: 6px;
            box-shadow: 
                0 3px 8px rgba(0,0,0,0.4),
                inset 0 1px 0 rgba(255,255,255,0.03);
            opacity: 0;
            visibility: hidden;
            transform: translateY(-10px);
            transition: all 0.2s;
            pointer-events: none;
            z-index: 1001;
            overflow: hidden;
            max-height: 70vh; /* Prevent overflow on small screens */
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
        }}
        
        .nav-dropdown-menu::before {{
            content: "";
            position: absolute;
            top: -8px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 8px solid transparent;
            border-right: 8px solid transparent;
            border-bottom: 8px solid #2a2a2a;
        }}
        
        /* Regular Dropdown Menu (for Copy/Save) */
        .dropdown-menu {{
            position: absolute;
            top: 100%;
            right: 0;
            margin-top: 0.5rem;
            background: #2a2a2a;
            border: 1px solid #333333;
            border-radius: 6px;
            min-width: 180px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            opacity: 0;
            visibility: hidden;
            transform: translateY(-10px);
            transition: all 0.2s;
            pointer-events: none;
            z-index: 1001;
        }}
        
        .dropdown-menu::before {{
            content: "";
            position: absolute;
            top: -8px;
            right: 1rem;
            width: 0;
            height: 0;
            border-left: 8px solid transparent;
            border-right: 8px solid transparent;
            border-bottom: 8px solid #2a2a2a;
        }}
        
        /* Show dropdown when target is active */
        .dropdown-menu:target,
        .nav-dropdown-menu:target {{
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
            pointer-events: auto;
        }}
        
        .nav-dropdown-item {{
            display: block;
            padding: 0.75rem 1rem;
            color: #d5d5d5;
            text-decoration: none;
            border-bottom: 1px solid #2a2a2a;
            border-top: 1px solid #2d2d2d;
            transition: all 0.15s;
            cursor: pointer;
            text-align: center;
            background: #242424;
            font-weight: 400;
            letter-spacing: 0.1px;
        }}
        
        .nav-dropdown-item:first-child {{
            border-radius: 6px 6px 0 0;
            border-top: none;
        }}
        
        .nav-dropdown-item:last-child {{
            border-bottom: none;
            border-radius: 0 0 6px 6px;
        }}
        
        .nav-dropdown-item:hover {{
            background: #2d2d2d;
            color: #e5e5e5;
            border-top-color: #333333;
        }}
        
        .nav-dropdown-item:active {{
            background: #1f1f1f;
        }}
        
        /* Dropdown backdrop for top nav */
        .dropdown-backdrop {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1000;
            display: none;
        }}
        
        .dropdown-menu:target ~ .dropdown-backdrop {{
            display: block;
        }}
        
        .dropdown-item {{
            display: block;
            padding: 0.75rem 1rem;
            color: #d5d5d5;
            text-decoration: none;
            border-bottom: 1px solid #333333;
            transition: all 0.2s;
            cursor: pointer;
        }}
        
        .dropdown-item:first-child {{
            border-radius: 6px 6px 0 0;
        }}
        
        .dropdown-item:last-child {{
            border-bottom: none;
            border-radius: 0 0 6px 6px;
        }}
        
        .dropdown-item:hover {{
            background: #333333;
            color: #e5e5e5;
        }}
        
        /* CSS-Only Modal using :target */
        .modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
            z-index: 1000;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }}
        
        .modal:target {{
            display: flex;
        }}
        
        .modal-content {{
            background: #2a2a2a;
            border-radius: 10px;
            padding: 2rem;
            max-width: 600px;
            width: 100%;
            max-height: 80vh;
            overflow-y: auto;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
            border: 1px solid #333333;
            position: relative;
        }}
        
        .modal-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }}
        
        .modal-header h2 {{
            margin: 0;
            color: #e8e8e8;
            border: none;
            padding: 0;
        }}
        
        .modal-close {{
            background: #333333;
            border: none;
            color: #b5b5b5;
            font-size: 1.5rem;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            cursor: pointer;
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: center;
            line-height: 1;
        }}
        
        .modal-close:hover {{
            background: #3a3a3a;
            color: #e8e8e8;
        }}
        
        /* Form Styles */
        .form-group {{
            margin-bottom: 1.5rem;
        }}
        
        .form-label {{
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            color: #e5e5e5;
        }}
        
        .form-textarea {{
            width: 100%;
            padding: 0.75rem;
            border: 2px solid #333333;
            border-radius: 6px;
            font-size: 1rem;
            font-family: inherit;
            resize: vertical;
            background: #1a1a1a;
            color: #d5d5d5;
        }}
        
        .form-textarea:focus {{
            outline: none;
            border-color: #8a9eff;
        }}
        
        .form-actions {{
            display: flex;
            gap: 1rem;
        }}
        
        .btn-primary {{
            flex: 1;
            padding: 0.75rem 1.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #e8e8e8;
            border: none;
            border-radius: 6px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
        }}
        
        .btn-secondary {{
            padding: 0.75rem 1.5rem;
            background: #333333;
            color: #d5d5d5;
            border: none;
            border-radius: 6px;
            font-size: 1rem;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }}
        
        .btn-primary:hover {{
            opacity: 0.9;
        }}
        
        .btn-secondary:hover {{
            background: #3a3a3a;
        }}
        
        /* Main Content - Responsive padding */
        .main-content {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 1rem; /* Mobile: reduced padding */
        }}
        
        /* Header Section Wrapper - Responsive padding */
        .header-section-wrapper {{
            padding: 1rem 1rem 1.5rem 1rem; /* Mobile: reduced padding */
        }}
        
        .header-section-wrapper .header-section {{
            background: transparent;
            padding: 0;
            border: none;
            margin-bottom: 0;
        }}
        
        .header-section-wrapper h1 {{
            margin-top: 0;
            margin-bottom: 1rem;
            color: #e8e8e8;
            font-size: 2rem;
        }}
        
        .header-section-wrapper .header-meta {{
            opacity: 0.75;
            font-size: 0.9rem;
        }}
        
        .header-meta {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 0.75rem;
        }}
        
        .meta-item {{
            color: #aaaaaa;
            font-size: 0.95rem;
        }}
        
        .meta-label {{
            color: #e5e5e5;
            font-weight: 600;
        }}
        
        /* Stats Grid - Responsive columns */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr); /* Mobile: 2 columns minimum */
            gap: 1rem;
            margin: 1.5rem 0;
        }}
        
        .stat-card {{
            background: #252525;
            padding: 1rem;
            border-radius: 4px;
            border: 1px solid #333333;
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 1.5rem;
            font-weight: 600;
            color: #e5e5e5;
            display: block;
            letter-spacing: 0.3px;
        }}
        
        .stat-label {{
            color: #999999;
            font-size: 0.85rem;
            letter-spacing: 0.2px;
            margin-top: 0.5rem;
        }}
        
        /* Content Cards */
        .content-card {{
            background: #222222;
            padding: 1rem;
            border-radius: 4px;
            border: 1px solid #333333;
            margin: 1rem 0;
        }}
        
        /* Reasoning Trace Section Styling */
        #reasoning-trace {{
            scroll-margin-top: 2rem;
        }}
        
        #reasoning-trace + h2 {{
            margin-top: 3rem;
            border-bottom: 2px solid #333333;
            padding-bottom: 0.5rem;
        }}
        
        #reasoning-trace + h2 ~ details {{
            margin-bottom: 1rem;
        }}
        
        #reasoning-trace + h2 ~ details summary {{
            background: #242424;
            padding: 0.75rem 1rem;
            border: 1px solid #2a2a2a;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 500;
            display: block;
        }}
        
        #reasoning-trace + h2 ~ details summary:hover {{
            background: #282828;
            border-color: #2d2d2d;
        }}
        
        /* Chat Context Section Styling */
        #chat-context {{
            scroll-margin-top: 2rem;
        }}
        
        #chat-context + h2 {{
            margin-top: 3rem;
            border-bottom: 2px solid #333333;
            padding-bottom: 0.5rem;
        }}
        
        #chat-context + h2 ~ details {{
            margin-bottom: 1rem;
        }}
        
        #chat-context + h2 ~ details summary {{
            background: #242424;
            padding: 0.75rem 1rem;
            border: 1px solid #2a2a2a;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 500;
            display: block;
        }}
        
        #chat-context + h2 ~ details summary:hover {{
            background: #282828;
            border-color: #2d2d2d;
        }}
        
        /* Table Wrapper - Horizontal scroll on mobile */
        .table-wrapper {{
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            margin: 1rem 0;
        }}
        
        /* Tables - Information Dense with Responsive Sizing */
        table {{
            width: 100%;
            border-collapse: collapse;
            background: #222222;
            border: 1px solid #333333;
            margin: 0;
            font-size: 0.9rem;
        }}
        
        th {{
            background: #2a2a2a;
            color: #e5e5e5;
            padding: 0.75rem;
            text-align: left;
            border-bottom: 2px solid #333333;
            border: 1px solid #333333;
            letter-spacing: 0.3px;
            font-weight: 600;
        }}
        
        td {{
            color: #d5d5d5;
            padding: 0.75rem;
            border-bottom: 1px solid #333333;
            border: 1px solid #333333;
            background: #222222;
            letter-spacing: 0.2px;
            line-height: 1.6;
        }}
        
        tr:nth-child(even) td {{
            background: #252525;
        }}
        
        tr:hover td {{
            background: #2d2d2d;
        }}
        
        /* Code */
        code {{
            background: #252525;
            color: #d8d8d8;
            border: 1px solid #333333;
            letter-spacing: 0.3px;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: 'SF Mono', 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 0.9em;
        }}
        
        pre {{
            background: #1f1f1f;
            color: #d5d5d5;
            border: 1px solid #333333;
            line-height: 1.6;
            letter-spacing: 0.2px;
            padding: 1rem;
            border-radius: 4px;
            overflow-x: auto;
            margin: 1rem 0;
        }}
        
        pre code {{
            background: transparent;
            border: none;
            padding: 0;
        }}
        
        /* Lists */
        ul, ol {{
            margin-left: 1.5rem;
            margin-bottom: 1rem;
        }}
        
        li {{
            margin-bottom: 0.5rem;
        }}
        
        /* Badges */
        .badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: bold;
            border: 1px solid;
        }}
        
        .badge-active {{
            background: #2a3a4a;
            color: #8a9eff;
            border-color: #3a4a5a;
        }}
        
        .badge-completed {{
            background: #2a3a2a;
            color: #8aff8a;
            border-color: #3a4a3a;
        }}
        
        .badge-open {{
            background: #2a2a2a;
            color: #b0b0b0;
            border-color: #3a3a3a;
        }}
        
        .badge-paused {{
            background: #4a3a2a;
            color: #ffaa8a;
            border-color: #5a4a3a;
        }}
        
        /* Footer */
        .footer {{
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid #333333;
            text-align: center;
            color: #999999;
            font-size: 0.875rem;
        }}
        
        /* Information Dense Sections */
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin: 1.5rem 0;
        }}
        
        .info-card {{
            background: #222222;
            padding: 1rem;
            border-radius: 4px;
            border: 1px solid #333333;
        }}
        
        .info-card h4 {{
            margin-top: 0;
            margin-bottom: 0.75rem;
            color: #e0e0e0;
        }}
        
        .info-card ul {{
            margin-left: 1.25rem;
        }}
        
        .info-card li {{
            margin-bottom: 0.25rem;
            font-size: 0.9rem;
        }}
        
        /* Print Styles */
        @media print {{
            .nav-bar {{
                display: none;
            }}
            
            body {{
                background: white;
                color: black;
            }}
            
            .main-content {{
                max-width: 100%;
                padding: 0;
            }}
        }}
        
        /* ============================================
           RESPONSIVE BREAKPOINTS
           Mobile-first approach: base styles for mobile,
           then enhance for larger screens
           Breakpoints: 600px (tablet), 1024px (desktop)
           ============================================ */
        
        /* Mobile: < 600px - Compact sizing, optimized for small screens */
        @media (max-width: 599px) {{
            /* Navigation: Keep 3-column but with tighter spacing */
            .nav-container {{
                gap: 0.25rem;
                padding: 0.75rem 0.5rem;
            }}
            
            .nav-dropdown-toggle {{
                padding: 0.5rem 0.5rem;
                font-size: 0.8rem;
                min-height: 44px; /* Ensure touch target */
            }}
            
            /* Tables: Smaller font and padding on mobile */
            table {{
                font-size: 0.85rem;
            }}
            
            th, td {{
                padding: 0.5rem;
            }}
            
            /* Stats grid: 2 columns on mobile */
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
                gap: 0.75rem;
            }}
            
            /* Header: Reduced padding */
            .header-section-wrapper {{
                padding: 1rem 1rem 1.5rem 1rem;
            }}
        }}
        
        /* Tablet: 600px - 1023px - Medium sizing */
        @media (min-width: 600px) and (max-width: 1023px) {{
            .nav-bar {{
                padding: 0.875rem 1.5rem 1.125rem 1.5rem;
            }}
            
            .nav-container {{
                gap: 0.5rem;
            }}
            
            .nav-dropdown-toggle {{
                padding: 0.625rem 0.75rem;
                font-size: 0.85rem;
            }}
            
            .main-content {{
                padding: 1.5rem;
            }}
            
            .header-section-wrapper {{
                padding: 1.25rem 1.5rem 1.75rem 1.5rem;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}
        
        /* Desktop: 1024px+ - Full sizing, all features visible */
        @media (min-width: 1024px) {{
            .nav-bar {{
                padding: 1rem 2rem 1.25rem 2rem;
            }}
            
            .nav-container {{
                gap: 0.75rem;
            }}
            
            .nav-dropdown-toggle {{
                padding: 0.75rem 1rem;
                font-size: 0.9rem;
            }}
            
            .main-content {{
                padding: 2rem;
            }}
            
            .header-section-wrapper {{
                padding: 1.5rem 2rem 2rem 2rem;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            }}
        }}
        
        /* Very Small Screens: < 360px - Extra compact for smallest devices */
        @media (max-width: 359px) {{
            .nav-dropdown-toggle {{
                font-size: 0.75rem;
                padding: 0.4rem 0.4rem;
                /* Text may truncate, but buttons remain usable */
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            
            .stats-grid {{
                grid-template-columns: 1fr; /* Single column on very small screens */
            }}
        }}
        
        /* Accessibility: No italics for astigmatism */
        em, i {{
            font-style: normal;
            font-weight: 500;
        }}
        
        /* Definition Lists for Key-Value Pairs */
        dl {{
            margin: 1rem 0;
        }}
        
        dt {{
            font-weight: 600;
            color: #e5e5e5;
            margin-top: 0.75rem;
        }}
        
        dd {{
            margin-left: 1.5rem;
            color: #d5d5d5;
        }}
        
        /* HTML5 <details> and <summary> - Native Collapsible Sections */
        details {{
            background: #222222;
            border: 1px solid #333333;
            border-radius: 4px;
            margin: 1rem 0;
            padding: 0;
        }}
        
        summary {{
            padding: 1rem;
            cursor: pointer;
            font-weight: 600;
            color: #e5e5e5;
            list-style: none;
            user-select: none;
        }}
        
        summary::-webkit-details-marker {{
            display: none;
        }}
        
        summary::before {{
            content: "▶ ";
            display: inline-block;
            margin-right: 0.5rem;
            transition: transform 0.2s;
            color: #8a9eff;
        }}
        
        details[open] summary::before {{
            transform: rotate(90deg);
        }}
        
        details[open] summary {{
            border-bottom: 1px solid #333333;
        }}
        
        details > *:not(summary) {{
            padding: 1rem;
            padding-top: 0.5rem;
        }}
        
        /* CSS-Only Tabs using :target */
        .tabs {{
            border-bottom: 2px solid #333333;
            margin: 1.5rem 0;
        }}
        
        .tab-nav {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}
        
        .tab-link {{
            padding: 0.5rem 1rem;
            background: #222222;
            color: #b5b5b5;
            text-decoration: none;
            border: 1px solid #333333;
            border-bottom: none;
            border-radius: 4px 4px 0 0;
            transition: all 0.2s;
        }}
        
        .tab-link:hover {{
            background: #252525;
            color: #e5e5e5;
        }}
        
        .tab-panel {{
            display: none;
            padding: 1rem;
            background: #222222;
            border: 1px solid #333333;
            border-top: none;
        }}
        
        .tab-panel:target {{
            display: block;
        }}
        
        /* First tab visible by default */
        .tabs .tab-panel:first-of-type {{
            display: block;
        }}
        
        .tabs .tab-panel:target ~ .tab-panel {{
            display: none;
        }}
        
        /* CSS-Only Filter Toggle using :checked */
        .filter-toggle {{
            display: none;
        }}
        
        .filter-label {{
            display: inline-block;
            padding: 0.5rem 1rem;
            background: #222222;
            border: 1px solid #333333;
            border-radius: 4px;
            cursor: pointer;
            color: #b5b5b5;
            margin: 0.25rem;
        }}
        
        .filter-label:hover {{
            background: #252525;
            color: #e5e5e5;
        }}
        
        .filter-toggle:checked + .filter-label {{
            background: #2a3a4a;
            color: #8a9eff;
            border-color: #3a4a5a;
        }}
        
        /* Show/hide filtered content */
        .filterable {{
            display: none;
        }}
        
        #filter-all:checked ~ * .filterable {{
            display: block;
        }}
        
        #filter-active:checked ~ * .filterable[data-status="active"] {{
            display: block;
        }}
        
        #filter-completed:checked ~ * .filterable[data-status="completed"] {{
            display: block;
        }}
        
        #filter-open:checked ~ * .filterable[data-status="open"] {{
            display: block;
        }}
        
        /* CSS-Only Accordion using :checked */
        .accordion-toggle {{
            display: none;
        }}
        
        .accordion-label {{
            display: block;
            padding: 1rem;
            background: #222222;
            border: 1px solid #333333;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
            color: #e5e5e5;
            margin-bottom: 0.5rem;
        }}
        
        .accordion-label::after {{
            content: " ▼";
            float: right;
            transition: transform 0.2s;
        }}
        
        .accordion-toggle:checked + .accordion-label::after {{
            transform: rotate(180deg);
        }}
        
        .accordion-content {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease-out;
            background: #1f1f1f;
            border: 1px solid #333333;
            border-top: none;
            border-radius: 0 0 4px 4px;
        }}
        
        .accordion-toggle:checked ~ .accordion-content {{
            max-height: 2000px;
            padding: 1rem;
        }}
        
        /* Clickable Cards with :target */
        .clickable-card {{
            display: block;
            background: #222222;
            border: 1px solid #333333;
            border-radius: 4px;
            padding: 1rem;
            margin: 0.5rem 0;
            text-decoration: none;
            color: inherit;
            transition: all 0.2s;
        }}
        
        .clickable-card:hover {{
            background: #252525;
            border-color: #8a9eff;
            transform: translateX(4px);
        }}
        
        .clickable-card:target {{
            background: #2a2a2a;
            border-color: #8a9eff;
            border-width: 2px;
        }}
        
        /* Expandable Rows in Tables */
        .expandable-row {{
            cursor: pointer;
        }}
        
        .expandable-row:hover {{
            background: #2d2d2d;
        }}
        
        .row-details {{
            display: none;
        }}
        
        .row-details:target {{
            display: table-row;
        }}
        
        /* Sortable Table Headers (via URL params - server-side) */
        .sortable-header {{
            position: relative;
            padding-right: 1.5rem;
        }}
        
        .sortable-header a {{
            color: inherit;
            text-decoration: none;
        }}
        
        .sortable-header a::after {{
            content: " ↕";
            position: absolute;
            right: 0.5rem;
            color: #666;
            font-size: 0.8em;
        }}
        
        /* CSS-Only Search Highlight (using :target) */
        .search-result:target {{
            background: #2a3a4a;
            border-left: 4px solid #8a9eff;
            padding-left: calc(1rem - 4px);
        }}
    
    </style>
</head>
<body>

    <!-- Above the Fold - Unified Top Section -->
    <section id="above-the-fold" class="above-the-fold">
        <nav class="nav-bar" role="navigation" aria-label="Main navigation">
            <div class="nav-container">
                <!-- Section 1: Primary Navigation -->
                <div class="nav-section">
                    <div class="dropdown-group">
                        <a href="#nav-primary" class="nav-dropdown-toggle">Overview</a>
                        <div id="nav-primary" class="nav-dropdown-menu">
                            <a href="#quick-stats" class="nav-dropdown-item">Quick Stats</a>
                            <a href="#work-efforts" class="nav-dropdown-item">Work Efforts</a>
                            <a href="#projects" class="nav-dropdown-item">Projects</a>
                            <a href="#abstract" class="nav-dropdown-item">Abstract</a>
                        </div>
                        <a href="#" class="dropdown-backdrop" onclick="window.location.hash=''; return false;"></a>
                    </div>
                </div>
                
                <!-- Section 2: Secondary Navigation -->
                <div class="nav-section">
                    <div class="dropdown-group">
                        <a href="#nav-secondary" class="nav-dropdown-toggle">Resources</a>
                        <div id="nav-secondary" class="nav-dropdown-menu">
                            <a href="#latex-templates" class="nav-dropdown-item">Templates</a>
                            <a href="#librarian-catalog" class="nav-dropdown-item">Catalog</a>
                            <a href="#recent-experiments" class="nav-dropdown-item">Experiments</a>
                            <a href="#recent-proof-cases" class="nav-dropdown-item">Proof Cases</a>
                        </div>
                        <a href="#" class="dropdown-backdrop" onclick="window.location.hash=''; return false;"></a>
                    </div>
                </div>
                
                <!-- Section 3: Actions -->
                <div class="nav-section">
                    <div class="dropdown-group">
                        <a href="#nav-actions" class="nav-dropdown-toggle">Actions</a>
                        <div id="nav-actions" class="nav-dropdown-menu">
                            <a href="#copy-html" class="nav-dropdown-item" onclick="copyHTML(); return false;">Copy HTML</a>
                            <a href="#copy-text" class="nav-dropdown-item" onclick="copyText(); return false;">Copy Text</a>
                            <a href="#save-html" class="nav-dropdown-item" onclick="saveHTML(); return false;">Save HTML</a>
                            <a href="#save-text" class="nav-dropdown-item" onclick="saveText(); return false;">Save Text</a>
                            <a href="#reasoning-trace" class="nav-dropdown-item">Reasoning</a>
                            <a href="#chat-context" class="nav-dropdown-item">Context</a>
                        </div>
                        <a href="#" class="dropdown-backdrop" onclick="window.location.hash=''; return false;"></a>
                    </div>
                </div>
            </div>
        </nav>

        
        <!-- Header Section - Inside Above the Fold -->
        <div class="header-section-wrapper">
            {header_html}
        </div>
    </section>
    
    <main class="main-content">
        {main_html}
        {session_history_html}
        <footer class="footer">
            <p>Generated by WAFT (Wave Agent Framework & Tools) v0.9.2 | {timestamp}</p>
        </footer>
    </main>
    
    <!-- Floating Oracle Button - Bottom Center -->
    <a href="oracle.html" target="_blank" class="btn-oracle">🔮 Consult the Oracle</a>
    <!-- Oracle Modal - CSS-only using :target -->
    <div class="modal" id="oracle-modal" role="dialog" aria-labelledby="oracle-title">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="oracle-title">🔮 Consult the Oracle</h2>
                <a href="#" class="modal-close" aria-label="Close modal">&times;</a>
            </div>
            <form action="http://localhost:8000/api/oracle/consult" method="POST" target="_blank">
                <div class="form-group">
                    <label for="oracle-question" class="form-label">Your Question:</label>
                    <textarea 
                        id="oracle-question" 
                        name="question" 
                        rows="4" 
                        class="form-textarea"
                        placeholder="Ask the Oracle anything about your project, code, or decisions..."
                        required
                    ></textarea>
                </div>
                <div class="form-actions">
                    <button type="submit" class="btn-primary">Consult (Opens in New Tab)</button>
                    <a href="#" class="btn-secondary">Cancel</a>
                </div>
            </form>
            <div style="margin-top: 1.5rem; padding: 1rem; background: #1f1f1f; border-radius: 6px; border: 1px solid #333333;">
                <p style="margin-bottom: 0.5rem; color: #d5d5d5; font-size: 0.9rem;"><strong style="color: #e5e5e5;">Alternative:</strong> Use the command line:</p>
                <pre style="margin: 0; background: #1a1a1a; padding: 0.75rem; border-radius: 4px;"><code>waft oracle "your question here"</code></pre>
            </div>
        </div>
    <!-- Toast Notification -->
    <div id="toast" class="toast-notification"></div>
    
    <!-- Minimal JavaScript for Copy/Save (graceful degradation) -->
    <script>

        // Wrap tables in scrollable container for horizontal scrolling on mobile
        (function() {{
            document.querySelectorAll('table').forEach(table => {{
                if (!table.parentElement.classList.contains('table-wrapper')) {{
                    const wrapper = document.createElement('div');
                    wrapper.className = 'table-wrapper';
                    table.parentNode.insertBefore(wrapper, table);
                    wrapper.appendChild(table);
                }}
            }});
        }})();
    

        // Show toast notification
        function showToast(message, duration = 2000) {{
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(() => {{
                toast.classList.remove('show');
            }}, duration);
        }}
        
        // Close dropdown after action
        function closeDropdowns() {{
            window.location.hash = '';
        }}
        
        // Copy HTML to clipboard
        async function copyHTML() {{
            try {{
                const html = document.documentElement.outerHTML;
                await navigator.clipboard.writeText(html);
                showToast('✅ HTML copied to clipboard!');
                closeDropdowns();
            }} catch (err) {{
                // Fallback: select text and prompt user to copy
                const textarea = document.createElement('textarea');
                textarea.value = document.documentElement.outerHTML;
                textarea.style.position = 'fixed';
                textarea.style.opacity = '0';
                document.body.appendChild(textarea);
                textarea.select();
                try {{
                    document.execCommand('copy');
                    showToast('✅ HTML copied to clipboard!');
                }} catch (e) {{
                    showToast('❌ Copy failed. Use Save HTML instead.');
                }}
                document.body.removeChild(textarea);
            }}
        }}
        
        // Copy text-only to clipboard
        async function copyText() {{
            try {{
                // Get all text content, preserving some structure
                const mainContent = document.querySelector('.main-content');
                const text = extractTextContent(mainContent);
                await navigator.clipboard.writeText(text);
                showToast('✅ Text copied to clipboard!');
                closeDropdowns();
            }} catch (err) {{
                // Fallback
                const textarea = document.createElement('textarea');
                const mainContent = document.querySelector('.main-content');
                textarea.value = extractTextContent(mainContent);
                textarea.style.position = 'fixed';
                textarea.style.opacity = '0';
                document.body.appendChild(textarea);
                textarea.select();
                try {{
                    document.execCommand('copy');
                    showToast('✅ Text copied to clipboard!');
                }} catch (e) {{
                    showToast('❌ Copy failed. Use Save Text instead.');
                }}
                document.body.removeChild(textarea);
            }}
        }}
        
        // Extract readable text content
        function extractTextContent(element) {{
            let text = '';
            const walker = document.createTreeWalker(
                element,
                NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT,
                null,
                false
            );
            
            let node;
            while (node = walker.nextNode()) {{
                if (node.nodeType === Node.TEXT_NODE) {{
                    const content = node.textContent.trim();
                    if (content) {{
                        text += content + '\n';
                    }}
                }} else if (node.nodeType === Node.ELEMENT_NODE) {{
                    const tagName = node.tagName.toLowerCase();
                    if (['h1', 'h2', 'h3', 'h4', 'h5', 'h6'].includes(tagName)) {{
                        text += '\n\n' + node.textContent.trim() + '\n';
                    }} else if (tagName === 'p' || tagName === 'li') {{
                        text += node.textContent.trim() + '\n';
                    }} else if (tagName === 'tr') {{
                        const cells = Array.from(node.querySelectorAll('td, th')).map(cell => cell.textContent.trim());
                        text += cells.join(' | ') + '\n';
                    }}
                }}
            }}
            
            // Clean up excessive newlines
            return text.replace(/\n{{3,}}/g, '\n\n').trim();
        }}
        
        // Save HTML as file
        function saveHTML() {{
            const html = document.documentElement.outerHTML;
            const blob = new Blob([html], {{ type: 'text/html' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'waft-session-overview-' + new Date().toISOString().slice(0, 10) + '.html';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            showToast('💾 HTML file saved!');
            closeDropdowns();
        }}
        
        // Save text as file
        function saveText() {{
            const mainContent = document.querySelector('.main-content');
            const text = extractTextContent(mainContent);
            const blob = new Blob([text], {{ type: 'text/plain' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'waft-session-overview-' + new Date().toISOString().slice(0, 10) + '.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            showToast('📝 Text file saved!');
            closeDropdowns();
        }}
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {{
            // Ctrl/Cmd + Shift + H = Copy HTML
            if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'H') {{
                e.preventDefault();
                copyHTML();
            }}
            // Ctrl/Cmd + Shift + T = Copy Text
            if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'T') {{
                e.preventDefault();
                copyText();
            }}
            // Ctrl/Cmd + Shift + S = Save HTML
            if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'S') {{
                e.preventDefault();
                saveHTML();
            }}
        }});
        
        /* Copy Abstract Function */
        function copyAbstract() {{
            const abstractBox = document.getElementById('abstract-content');
            if (!abstractBox) {{
                console.error('Abstract content not found');
                return;
            }}
            
            // Get text content, stripping HTML but preserving line breaks
            let text = abstractBox.innerText || abstractBox.textContent || '';
            
            // Clean up extra whitespace
            text = text.trim().replace(/\s+/g, ' ');
            
            // Copy to clipboard
            if (navigator.clipboard && navigator.clipboard.writeText) {{
                navigator.clipboard.writeText(text).then(() => {{
                    // Visual feedback
                    const btn = document.querySelector('.abstract-copy-btn');
                    if (btn) {{
                        const originalHTML = btn.innerHTML;
                        btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M13 4L6 11L3 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
                        btn.style.color = '#8a9eff';
                        setTimeout(() => {{
                            btn.innerHTML = originalHTML;
                            btn.style.color = '';
                        }}, 1500);
                    }}
                }}).catch(err => {{
                    console.error('Failed to copy:', err);
                }});
            }} else {{
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = text;
                textArea.style.position = 'fixed';
                textArea.style.opacity = '0';
                document.body.appendChild(textArea);
                textArea.select();
                try {{
                    document.execCommand('copy');
                    const btn = document.querySelector('.abstract-copy-btn');
                    if (btn) {{
                        const originalHTML = btn.innerHTML;
                        btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M13 4L6 11L3 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
                        btn.style.color = '#8a9eff';
                        setTimeout(() => {{
                            btn.innerHTML = originalHTML;
                            btn.style.color = '';
                        }}, 1500);
                    }}
                }} catch (err) {{
                    console.error('Fallback copy failed:', err);
                }}
                document.body.removeChild(textArea);
            }}
        }}
        
        function copyRecommendedStep() {{
            const actionEl = document.getElementById('recommended-action');
            const contextEl = document.getElementById('recommended-context');
            
            if (!actionEl) {{
                console.error('Recommended action not found');
                return;
            }}
            
            // Get action text
            let actionText = actionEl.innerText || actionEl.textContent || '';
            
            // Get context text (if available)
            let contextText = '';
            if (contextEl) {{
                contextText = contextEl.innerText || contextEl.textContent || '';
            }}
            
            // Combine action and context
            let combinedText = actionText.trim();
            if (contextText.trim()) {{
                combinedText += '\n\n--- Context Primer ---\n' + contextText.trim();
            }}
            
            // Copy to clipboard
            if (navigator.clipboard && navigator.clipboard.writeText) {{
                navigator.clipboard.writeText(combinedText).then(() => {{
                    // Visual feedback
                    const btn = document.querySelector('.recommended-copy-btn');
                    if (btn) {{
                        const originalHTML = btn.innerHTML;
                        btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M13 4L6 11L3 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
                        btn.style.color = '#8a9eff';
                        setTimeout(() => {{
                            btn.innerHTML = originalHTML;
                            btn.style.color = '';
                        }}, 1500);
                    }}
                }}).catch(err => {{
                    console.error('Failed to copy:', err);
                }});
            }} else {{
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = combinedText;
                textArea.style.position = 'fixed';
                textArea.style.opacity = '0';
                document.body.appendChild(textArea);
                textArea.select();
                try {{
                    document.execCommand('copy');
                    const btn = document.querySelector('.recommended-copy-btn');
                    if (btn) {{
                        const originalHTML = btn.innerHTML;
                        btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M13 4L6 11L3 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
                        btn.style.color = '#8a9eff';
                        setTimeout(() => {{
                            btn.innerHTML = originalHTML;
                            btn.style.color = '';
                        }}, 1500);
                    }}
                }} catch (err) {{
                    console.error('Fallback copy failed:', err);
                }}
                document.body.removeChild(textArea);
            }}
        }}
    
    </script>
</body>
</html>"""
    
    return template.format(
        title=title,
        timestamp=timestamp,
        header_html=header_html,
        main_html=main_html,
        session_history_html=session_history_html
    )

def generate_html_report(
    project_path: Path,
    output_path: Optional[Path] = None,
    work_efforts: List[Dict[str, Any]] = None,
    templates: List[Dict[str, Any]] = None,
    catalog: Dict[str, Any] = None,
    experiments: List[Dict[str, Any]] = None,
    chat_context: Dict[str, Any] = None,
    proof_cases: List[Dict[str, Any]] = None,
    reasoning_trace: List[Dict[str, Any]] = None,
    projects: List[Dict[str, Any]] = None
) -> Path:
    """Generate HTML report with clean WAFT design."""
    import markdown
    
    md_content = generate_markdown_report(
        work_efforts or [],
        templates or [],
        catalog or {},
        experiments or [],
        chat_context or {},
        proof_cases or [],
        reasoning_trace or [],
        projects or []
    )
    
    # Use markdown with HTML preservation
    # Convert markdown to HTML, preserving raw HTML tags
    html_content = markdown.markdown(
        md_content, 
        extensions=['tables', 'fenced_code', 'nl2br', 'attr_list', 'md_in_html'],
        extension_configs={
            'markdown.extensions.tables': {},
            'markdown.extensions.fenced_code': {},
            'markdown.extensions.nl2br': {},
            'markdown.extensions.md_in_html': {},
        }
    )
    
    # Ensure abstract HTML line breaks are preserved (markdown might convert <br> to <p>)
    # Replace any <p><br></p> patterns with just <br> for cleaner formatting
    import re
    html_content = re.sub(r'<p>\s*<br>\s*</p>', '<br>', html_content)
    html_content = re.sub(r'<p>\s*<br>\s*', '<br>', html_content)
    
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
    
    # Add IDs to sections for navigation (before markdown conversion)
    md_content = md_content.replace('## Quick Stats', '## Quick Stats {#quick-stats}')
    md_content = md_content.replace('## Work Efforts', '## Work Efforts {#work-efforts}')
    md_content = md_content.replace('## Projects', '## Projects {#projects}')
    md_content = md_content.replace('## LaTeX Templates', '## LaTeX Templates {#latex-templates}')
    md_content = md_content.replace('## Librarian Catalog', '## Librarian Catalog {#librarian-catalog}')
    md_content = md_content.replace('## Recent Experiments', '## Recent Experiments {#recent-experiments}')
    md_content = md_content.replace('## Recent Proof Cases', '## Recent Proof Cases {#recent-proof-cases}')
    md_content = md_content.replace('## Reasoning Trace', '## Reasoning Trace {#reasoning-trace}')
    md_content = md_content.replace('## Chat Context', '## Chat Context {#chat-context}')
    
    # Use WAFT HTML template generator (from this file)
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Get session history for this report
    project_path = Path.cwd()
    current_file = str(output_path.name) if output_path else None
    session_history = get_session_history(project_path, current_file)
    full_html = generate_waft_html(
        html_content=html_content,
        title="WAFT Session Overview",
        timestamp=timestamp_str,
        session_history=session_history
    )
    
    # Write to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
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
    # Get work efforts - show all by default (days_back=0), or last 30 days
    work_efforts = get_work_efforts(project_path, days_back=0) if args.work_efforts else []
    templates = get_templates() if args.templates else []
    catalog = get_catalog_summary(project_path) if args.catalog else {}
    experiments = get_recent_experiments(project_path) if args.experiments else []
    chat_context = get_chat_context() if args.chat_context else {}
    proof_cases = get_proof_cases(project_path) if args.proof_cases else []
    reasoning_trace = get_reasoning_trace(project_path) if args.reasoning_trace else []
    projects = get_projects(project_path) if args.work_efforts else []  # Show projects when work efforts are shown
    
    # Display or generate report
    if args.format == "json":
        display_json_format(work_efforts, templates, catalog, experiments, chat_context, proof_cases, projects=projects)
    elif args.format == "html":
        # HTML is now the default format
        output_path = Path(args.output) if args.output else None
        html_path = generate_html_report(
            project_path, output_path, work_efforts, templates, catalog, experiments, chat_context, proof_cases, reasoning_trace, projects
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
            project_path, None, work_efforts, templates, catalog, experiments, chat_context, proof_cases, projects
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
            project_path, None, work_efforts, templates, catalog, experiments, chat_context, proof_cases, projects
        )
        output_path = Path(args.output) if args.output else html_path.with_suffix('.tex')
        tex_path = convert_html_to_latex(html_path, output_path)
        console.print(f"[green]✅ LaTeX generated: {tex_path}[/green]")
    elif args.format == "markdown":
        md_content = generate_markdown_report(work_efforts, templates, catalog, experiments, chat_context, proof_cases, reasoning_trace, projects)
        console.print(md_content)
    else:
        # Table format (fallback) - this already displays in console
        display_table_format(work_efforts, templates, catalog, experiments, chat_context, proof_cases, reasoning_trace, projects)

if __name__ == "__main__":
    main()
