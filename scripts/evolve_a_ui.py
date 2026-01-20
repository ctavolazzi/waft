#!/usr/bin/env python3
"""
Evolve a UI - Context-Aware UI Generation

Scans work efforts and evolves a UI for whatever is happening in the chat instance.
"""

import re
import subprocess
import sys
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.waft.evolution.document_evolution_engine import DocumentEvolutionEngine


def scan_work_efforts(project_path: Path) -> list[dict[str, Any]]:
    """Scan _work_efforts directory for active work efforts."""
    work_efforts = []
    work_efforts_path = project_path / "_work_efforts"

    if not work_efforts_path.exists():
        return work_efforts

    for we_dir in work_efforts_path.iterdir():
        if not we_dir.is_dir() or not we_dir.name.startswith("WE-"):
            continue

        we_id = we_dir.name.split("_")[0] if "_" in we_dir.name else we_dir.name

        # Try to read index file
        index_file = we_dir / f"{we_id}_index.md"
        if not index_file.exists():
            # Try alternative index names
            for alt_name in ["index.md", f"{we_dir.name}_index.md"]:
                alt_file = we_dir / alt_name
                if alt_file.exists():
                    index_file = alt_file
                    break

        if not index_file.exists():
            continue

        try:
            content = index_file.read_text(encoding="utf-8")

            # Extract frontmatter
            metadata = {}
            if "---" in content:
                frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
                if frontmatter_match:
                    frontmatter = frontmatter_match.group(1)
                    for line in frontmatter.split("\n"):
                        if ":" in line:
                            key, value = line.split(":", 1)
                            metadata[key.strip()] = value.strip()

            # Determine status
            status = metadata.get("status", "unknown").lower()
            if status in ["active", "in_progress", "open"]:
                work_efforts.append(
                    {
                        "id": we_id,
                        "title": metadata.get("title", we_dir.name),
                        "status": status,
                        "path": str(we_dir.relative_to(project_path)),
                        "metadata": metadata,
                        "description": content[:500] if len(content) > 500 else content,
                    }
                )
        except Exception as e:
            print(f"  ⚠️  Error reading {we_dir.name}: {e}")

    return work_efforts


def analyze_recent_activity(project_path: Path) -> dict[str, Any]:
    """Analyze recent activity from git and files."""
    activity = {
        "modified_files": [],
        "recent_commits": [],
        "current_branch": None,
        "git_status": {},
    }

    try:
        # Get git status
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            modified = []
            for line in result.stdout.strip().split("\n"):
                if line:
                    status = line[:2]
                    filename = line[3:]
                    modified.append({"status": status, "file": filename})
            activity["modified_files"] = modified[:20]  # Limit to 20

        # Get current branch
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            activity["current_branch"] = result.stdout.strip()

        # Get recent commits
        result = subprocess.run(
            ["git", "log", "--oneline", "-10"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            commits = []
            for line in result.stdout.strip().split("\n"):
                if line:
                    parts = line.split(" ", 1)
                    commits.append(
                        {
                            "hash": parts[0] if len(parts) > 0 else "",
                            "message": parts[1] if len(parts) > 1 else "",
                        }
                    )
            activity["recent_commits"] = commits
    except Exception as e:
        print(f"  ⚠️  Error analyzing git activity: {e}")

    return activity


def infer_chat_context(work_efforts: list[dict], recent_activity: dict) -> dict[str, Any]:
    """Infer chat context from work efforts and activity."""
    context = {
        "primary_focus": None,
        "work_type": "general",
        "themes": [],
        "ui_requirements": {"type": "dashboard", "components": [], "data_sources": []},
    }

    # Analyze work efforts
    if work_efforts:
        # Get most active work effort
        primary = work_efforts[0] if work_efforts else None
        if primary:
            context["primary_focus"] = primary["title"]
            context["themes"].append(primary["title"])

            # Determine work type from title/description
            title_lower = primary["title"].lower()
            desc_lower = primary.get("description", "").lower()

            if any(
                word in title_lower or word in desc_lower
                for word in ["bug", "fix", "error", "issue"]
            ):
                context["work_type"] = "bug_fix"
            elif any(
                word in title_lower or word in desc_lower
                for word in ["feature", "implement", "add", "create"]
            ):
                context["work_type"] = "feature"
            elif any(
                word in title_lower or word in desc_lower
                for word in ["research", "study", "analyze", "investigate"]
            ):
                context["work_type"] = "research"
            elif any(
                word in title_lower or word in desc_lower
                for word in ["refactor", "cleanup", "improve"]
            ):
                context["work_type"] = "refactor"

    # Analyze recent activity
    if recent_activity.get("modified_files"):
        file_types = {}
        for file_info in recent_activity["modified_files"][:10]:
            file_path = file_info.get("file", "")
            ext = Path(file_path).suffix.lower()
            file_types[ext] = file_types.get(ext, 0) + 1

        # Determine UI type based on file patterns
        if file_types.get(".py", 0) > 3:
            context["ui_requirements"]["type"] = "developer_dashboard"
        elif file_types.get(".md", 0) > 2:
            context["ui_requirements"]["type"] = "documentation_view"
        elif file_types.get(".html", 0) > 0 or file_types.get(".css", 0) > 0:
            context["ui_requirements"]["type"] = "frontend_dashboard"

    # Add work effort data to requirements
    context["ui_requirements"]["data_sources"].append("work_efforts")
    context["ui_requirements"]["components"].extend(
        ["work_effort_list", "status_board", "progress_tracker"]
    )

    return context


def generate_ui_requirements(context: dict[str, Any]) -> str:
    """Generate UI requirements specification."""
    requirements = f"""# UI Requirements - Evolved from Context

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Primary Focus**: {context.get("primary_focus", "General Project")}
**Work Type**: {context.get("work_type", "general")}

## Context Analysis

### Primary Focus
{context.get("primary_focus", "No specific focus identified")}

### Work Type
{context.get("work_type", "general")}

### Themes
{chr(10).join(f"- {theme}" for theme in context.get("themes", []))}

## UI Requirements

### Type
{context["ui_requirements"]["type"]}

### Components
{chr(10).join(f"- {comp}" for comp in context["ui_requirements"].get("components", []))}

### Data Sources
{chr(10).join(f"- {source}" for source in context["ui_requirements"].get("data_sources", []))}

## Design Principles

- Context-aware: Reflects current work state
- Adaptive: Evolves based on work type
- Informative: Shows relevant information
- Interactive: Allows exploration of work context
- Modern: Clean, professional design
"""
    return requirements


def evolve_ui_design(requirements: str, project_path: Path) -> dict[str, Any]:
    """Evolve UI design using WAFT evolution system."""
    print("  🧬 Evolving UI design...")

    evolution_dir = project_path / "_genetics" / "ui_evolution"
    evolution_dir.mkdir(parents=True, exist_ok=True)

    evolution_engine = DocumentEvolutionEngine(
        project_path=project_path,
        weasyprint_available=False,  # HTML generation doesn't need WeasyPrint
        max_iterations=3,
        default_allowed_pages=1,
        evolution_dir=evolution_dir,
        exploration_rate=0.3,
    )

    result = evolution_engine.generate_one_pager(
        content=requirements,
        title="Evolved UI - Context-Aware Dashboard",
        allowed_pages=1,
        use_science_paper_structure=False,
        use_evolved_components=True,
        author="WAFT UI Evolution System",
    )

    return result


def generate_ui_html(
    context: dict[str, Any],
    work_efforts: list[dict],
    recent_activity: dict,
    design_insights: dict | None = None,
) -> str:
    """Generate HTML/CSS for evolved UI."""

    # Default design if no insights
    if not design_insights:
        design_insights = {
            "color_scheme": {
                "primary": "#6366f1",
                "secondary": "#8b5cf6",
                "accent": "#ec4899",
                "background": "#f8fafc",
                "text": "#1e293b",
            },
            "typography": {
                "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
            },
        }

    colors = design_insights.get("color_scheme", {})
    typography = design_insights.get("typography", {})

    # Generate work effort cards
    work_effort_cards = ""
    for we in work_efforts[:5]:  # Limit to 5
        status_color = {
            "active": colors.get("primary", "#6366f1"),
            "in_progress": colors.get("accent", "#ec4899"),
            "open": colors.get("secondary", "#8b5cf6"),
        }.get(we.get("status", "active"), colors.get("primary", "#6366f1"))

        work_effort_cards += f"""
        <div class="work-effort-card">
            <div class="we-header">
                <h3>{we.get("title", we.get("id", "Unknown"))}</h3>
                <span class="status-badge" style="background: {status_color}">{we.get("status", "active")}</span>
            </div>
            <div class="we-id">{we.get("id", "")}</div>
            <div class="we-description">{we.get("description", "")[:200]}...</div>
        </div>
        """

    # Generate recent activity list
    activity_items = ""
    for file_info in recent_activity.get("modified_files", [])[:10]:
        status_icon = "📝" if "M" in file_info.get("status", "") else "➕"
        activity_items += f"""
        <div class="activity-item">
            <span class="activity-icon">{status_icon}</span>
            <span class="activity-file">{file_info.get("file", "")}</span>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Evolved UI - {context.get("primary_focus", "Project Dashboard")}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: {typography.get("font_family", "system-ui, sans-serif")};
            background: linear-gradient(135deg, {colors.get("primary", "#6366f1")} 0%, {colors.get("secondary", "#8b5cf6")} 100%);
            min-height: 100vh;
            padding: 20px;
            color: {colors.get("text", "#1e293b")};
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, {colors.get("primary", "#6366f1")} 0%, {colors.get("secondary", "#8b5cf6")} 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            font-size: 18px;
            opacity: 0.9;
        }}

        .context-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 14px;
            margin-top: 10px;
        }}

        .content {{
            padding: 40px;
        }}

        .section {{
            margin-bottom: 40px;
        }}

        .section-title {{
            font-size: 24px;
            margin-bottom: 20px;
            color: {colors.get("primary", "#6366f1")};
            border-bottom: 2px solid {colors.get("primary", "#6366f1")};
            padding-bottom: 10px;
        }}

        .work-efforts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }}

        .work-effort-card {{
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s ease;
        }}

        .work-effort-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
            border-color: {colors.get("primary", "#6366f1")};
        }}

        .we-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 10px;
        }}

        .we-header h3 {{
            font-size: 18px;
            color: {colors.get("text", "#1e293b")};
            flex: 1;
        }}

        .status-badge {{
            padding: 4px 12px;
            border-radius: 12px;
            color: white;
            font-size: 12px;
            font-weight: 600;
        }}

        .we-id {{
            font-size: 12px;
            color: #64748b;
            margin-bottom: 10px;
            font-family: monospace;
        }}

        .we-description {{
            font-size: 14px;
            color: #475569;
            line-height: 1.6;
        }}

        .activity-list {{
            background: #f8fafc;
            border-radius: 12px;
            padding: 20px;
        }}

        .activity-item {{
            display: flex;
            align-items: center;
            padding: 12px;
            border-bottom: 1px solid #e2e8f0;
        }}

        .activity-item:last-child {{
            border-bottom: none;
        }}

        .activity-icon {{
            font-size: 20px;
            margin-right: 12px;
        }}

        .activity-file {{
            font-family: monospace;
            font-size: 14px;
            color: {colors.get("text", "#1e293b")};
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}

        .info-card {{
            background: linear-gradient(135deg, {colors.get("primary", "#6366f1")} 0%, {colors.get("secondary", "#8b5cf6")} 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }}

        .info-card .value {{
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 8px;
        }}

        .info-card .label {{
            font-size: 14px;
            opacity: 0.9;
        }}

        @media (max-width: 768px) {{
            .work-efforts-grid {{
                grid-template-columns: 1fr;
            }}

            .content {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 Evolved UI Dashboard</h1>
            <div class="subtitle">Context-Aware Interface</div>
            <div class="context-badge">{context.get("work_type", "general").replace("_", " ").title()}</div>
        </div>

        <div class="content">
            <div class="section">
                <h2 class="section-title">Active Work Efforts</h2>
                <div class="work-efforts-grid">
                    {work_effort_cards if work_effort_cards else "<p>No active work efforts found.</p>"}
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Recent Activity</h2>
                <div class="activity-list">
                    {activity_items if activity_items else "<p>No recent activity found.</p>"}
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Project Info</h2>
                <div class="info-grid">
                    <div class="info-card">
                        <div class="value">{len(work_efforts)}</div>
                        <div class="label">Active Work Efforts</div>
                    </div>
                    <div class="info-card">
                        <div class="value">{len(recent_activity.get("modified_files", []))}</div>
                        <div class="label">Modified Files</div>
                    </div>
                    <div class="info-card">
                        <div class="value">{recent_activity.get("current_branch", "N/A")}</div>
                        <div class="label">Current Branch</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
    return html


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(description="Evolve a UI based on work efforts and context")
    parser.add_argument("--output", type=str, help="Output path for UI file")
    parser.add_argument("--work-effort", type=str, help="Focus on specific work effort")
    parser.add_argument("--type", type=str, help="UI type (dashboard, form, etc.)")
    parser.add_argument("--no-open", action="store_true", help="Don't open in browser")

    args = parser.parse_args()

    print("\n" + "=" * 70)
    print("🎨 EVOLVE A UI - Context-Aware UI Generation")
    print("=" * 70)
    print()

    # Step 1: Scan work efforts
    print("📋 Step 1: Scanning work efforts...")
    work_efforts = scan_work_efforts(project_root)
    print(f"  ✅ Found {len(work_efforts)} active work efforts")

    # Step 2: Analyze recent activity
    print("\n📊 Step 2: Analyzing recent activity...")
    recent_activity = analyze_recent_activity(project_root)
    print(f"  ✅ Found {len(recent_activity.get('modified_files', []))} modified files")

    # Step 3: Infer chat context
    print("\n🔍 Step 3: Inferring chat context...")
    context = infer_chat_context(work_efforts, recent_activity)
    print(f"  ✅ Primary focus: {context.get('primary_focus', 'General Project')}")
    print(f"  ✅ Work type: {context.get('work_type', 'general')}")

    # Step 4: Generate UI requirements
    print("\n📝 Step 4: Generating UI requirements...")
    requirements = generate_ui_requirements(context)

    # Step 5: Evolve UI design
    print("\n🧬 Step 5: Evolving UI design...")
    try:
        evolution_result = evolve_ui_design(requirements, project_root)
        design_insights = evolution_result.get("design_insights", {})
        print(f"  ✅ Evolution complete (fitness: {evolution_result.get('fitness', 'N/A')})")
    except Exception as e:
        print(f"  ⚠️  Evolution failed, using defaults: {e}")
        design_insights = None

    # Step 6: Generate HTML
    print("\n🎨 Step 6: Generating HTML/CSS...")
    html = generate_ui_html(context, work_efforts, recent_activity, design_insights)

    # Step 7: Save files
    print("\n💾 Step 7: Saving files...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = project_root / "_genetics" / "ui_evolution"
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = output_dir / f"{timestamp}_evolved_ui.html"

    output_path.write_text(html, encoding="utf-8")
    print(f"  ✅ Saved UI to: {output_path}")

    # Save context analysis
    context_path = output_dir / f"{timestamp}_context_analysis.md"
    context_path.write_text(requirements, encoding="utf-8")
    print(f"  ✅ Saved context analysis to: {context_path}")

    # Step 8: Open in browser
    if not args.no_open:
        print("\n🌐 Step 8: Opening in browser...")
        try:
            webbrowser.open(f"file://{output_path.absolute()}")
            print(f"  ✅ Opened: {output_path}")
        except Exception as e:
            print(f"  ⚠️  Could not open browser: {e}")
            print(f"  📄 Open manually: {output_path.absolute()}")

    print("\n" + "=" * 70)
    print("✅ UI EVOLUTION COMPLETE!")
    print("=" * 70)
    print(f"\n📁 UI File: {output_path.absolute()}")
    print(f"📋 Context: {context_path.absolute()}")
    print()

    return 0


if __name__ == "__main__":
    exit(main())
