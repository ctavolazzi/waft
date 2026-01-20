#!/usr/bin/env python3
"""
Generate Science-Bitch PDF with full spacetime context.
This creates a true "artifact" of the moment /science-bitch was invoked.
"""

import json
import os
import platform
import subprocess
import sys
import uuid
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

import markdown

from src.waft.templates.academic_paper import generate_academic_paper


def capture_spacetime_context(project_path: Path) -> dict:
    """Capture ALL contextual data about this moment."""
    context = {
        "artifact_metadata": {
            "generation_id": str(uuid.uuid4()),
            "artifact_type": "science-bitch-invocation",
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "timezone": str(datetime.now().astimezone().tzinfo),
        },
        "spacetime": {
            "timestamp": datetime.now().isoformat(),
            "timestamp_unix": datetime.now().timestamp(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "timezone": str(datetime.now().astimezone().tzinfo),
        },
        "project": {
            "path": str(project_path),
            "name": project_path.name,
            "absolute_path": str(project_path.absolute()),
        },
        "git": capture_git_state(project_path),
        "system": capture_system_state(project_path),
        "project_state": capture_project_state(project_path),
        "environment": capture_environment_state(),
    }
    return context


def capture_git_state(project_path: Path) -> dict:
    """Capture comprehensive git state."""
    git_state = {
        "initialized": False,
        "branch": None,
        "commit_hash": None,
        "commit_message": None,
        "commit_author": None,
        "commit_date": None,
        "uncommitted_files": [],
        "staged_files": [],
        "unstaged_files": [],
        "untracked_files": [],
        "uncommitted_count": 0,
        "recent_commits": [],
        "remote_url": None,
        "commits_ahead": 0,
        "commits_behind": 0,
    }

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return git_state

        git_state["initialized"] = True

        # Get current branch
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            git_state["branch"] = result.stdout.strip()

        # Get current commit
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H|%s|%an|%ad", "--date=iso"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            parts = result.stdout.strip().split("|")
            if len(parts) >= 4:
                git_state["commit_hash"] = parts[0]
                git_state["commit_message"] = parts[1]
                git_state["commit_author"] = parts[2]
                git_state["commit_date"] = parts[3]

        # Get uncommitted files
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                if not line.strip():
                    continue
                status_code = line[:2]
                filename = line[3:].strip()

                git_state["uncommitted_files"].append(filename)

                if status_code[0] != " ":
                    git_state["staged_files"].append(filename)
                if status_code[1] != " ":
                    git_state["unstaged_files"].append(filename)
                if status_code == "??":
                    git_state["untracked_files"].append(filename)

            git_state["uncommitted_count"] = len(git_state["uncommitted_files"])

        # Get recent commits (last 5)
        result = subprocess.run(
            ["git", "log", "-5", "--format=%H|%s|%an|%ad", "--date=iso"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                if not line.strip():
                    continue
                parts = line.split("|")
                if len(parts) >= 4:
                    git_state["recent_commits"].append(
                        {
                            "hash": parts[0][:8],
                            "message": parts[1],
                            "author": parts[2],
                            "date": parts[3],
                        }
                    )

        # Get remote URL
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            git_state["remote_url"] = result.stdout.strip()
    except Exception as e:
        git_state["error"] = str(e)

    return git_state


def capture_system_state(project_path: Path) -> dict:
    """Capture system state information."""
    system_state = {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "working_directory": str(Path.cwd()),
    }

    try:
        if platform.system() == "Darwin":
            result = subprocess.run(
                ["df", "-h", str(project_path)],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                if len(lines) > 1:
                    parts = lines[1].split()
                    if len(parts) >= 5:
                        system_state["disk_usage"] = {
                            "total": parts[1],
                            "used": parts[2],
                            "available": parts[3],
                            "percent": parts[4],
                        }
    except Exception:
        pass

    return system_state


def capture_project_state(project_path: Path) -> dict:
    """Capture project-specific state."""
    project_state = {
        "active_work_efforts": [],
        "recent_files": [],
    }

    # Check for active work efforts
    work_efforts_path = project_path / "_work_efforts"
    if work_efforts_path.exists():
        try:
            for item in work_efforts_path.iterdir():
                if item.is_file() and item.suffix == ".md":
                    content = item.read_text()[:500]
                    if "status" in content.lower() and (
                        "active" in content.lower() or "in progress" in content.lower()
                    ):
                        project_state["active_work_efforts"].append(
                            {
                                "name": item.name,
                                "path": str(item.relative_to(project_path)),
                            }
                        )
        except Exception:
            pass

    return project_state


def capture_environment_state() -> dict:
    """Capture environment variables and configuration."""
    env_state = {
        "python_path": os.environ.get("PYTHONPATH"),
        "virtual_env": os.environ.get("VIRTUAL_ENV"),
        "conda_env": os.environ.get("CONDA_DEFAULT_ENV"),
        "user": os.environ.get("USER") or os.environ.get("USERNAME"),
        "home": os.environ.get("HOME") or os.environ.get("USERPROFILE"),
    }

    waft_vars = {
        k: v for k, v in os.environ.items() if k.startswith("WAFT") or k.startswith("EMPIRICA")
    }
    if waft_vars:
        env_state["waft_variables"] = {
            k: "***" if "key" in k.lower() or "secret" in k.lower() or "token" in k.lower() else v
            for k, v in waft_vars.items()
        }

    return env_state


def format_context_for_abstract(context: dict) -> str:
    """Format context data into a readable abstract/metadata section."""
    lines = []

    # Artifact Metadata
    artifact = context["artifact_metadata"]
    lines.append(f"**Artifact ID**: {artifact['generation_id'][:8]}...")
    lines.append(f"**Type**: {artifact['artifact_type']}")
    lines.append(f"**Version**: {artifact['version']}")

    # Spacetime
    st = context["spacetime"]
    lines.append(f"**Timestamp**: {st['timestamp']}")
    lines.append(f"**Date**: {st['date']} {st['time']} ({st['timezone']})")

    # Project
    proj = context["project"]
    lines.append(f"**Project**: {proj['name']}")
    lines.append(f"**Path**: {proj['path']}")

    # Git
    git = context["git"]
    if git["initialized"]:
        lines.append(f"**Git Branch**: {git['branch']}")
        if git["commit_hash"]:
            lines.append(f"**Commit**: {git['commit_hash'][:8]} - {git['commit_message'][:50]}...")
        lines.append(f"**Uncommitted Files**: {git['uncommitted_count']}")
        if git["uncommitted_files"]:
            lines.append(f"  - {', '.join(git['uncommitted_files'][:5])}")
            if len(git["uncommitted_files"]) > 5:
                lines.append(f"  - ... and {len(git['uncommitted_files']) - 5} more")

    # System
    sys_state = context["system"]
    lines.append(f"**Platform**: {sys_state['platform']} {sys_state['platform_release']}")
    lines.append(f"**Python**: {sys_state['python_version']}")
    if "disk_usage" in sys_state:
        disk = sys_state["disk_usage"]
        lines.append(f"**Disk**: {disk['used']} / {disk['total']} ({disk['percent']})")

    # Project State
    proj_state = context["project_state"]
    if proj_state["active_work_efforts"]:
        lines.append(f"**Active Work Efforts**: {len(proj_state['active_work_efforts'])}")
        for we in proj_state["active_work_efforts"][:3]:
            lines.append(f"  - {we['name']}")

    return "\n\n".join(lines)


def main():
    """Generate PDF with full spacetime context."""
    project_path = Path.cwd()
    science_path = project_path / "_science"
    reports_path = science_path / "reports"
    reports_path.mkdir(parents=True, exist_ok=True)

    # Capture context
    print("📊 Capturing spacetime context...")
    context = capture_spacetime_context(project_path)

    # Save context JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    context_json_path = reports_path / f"context_{timestamp}.json"
    context_json_path.write_text(json.dumps(context, indent=2))
    print(f"✅ Context saved: {context_json_path}")

    # Read the guide markdown
    guide_md_path = reports_path / "COMPLETE_SCIENCE_BITCH_GUIDE.md"
    if not guide_md_path.exists():
        print(f"❌ Guide not found: {guide_md_path}")
        return 1

    content = guide_md_path.read_text()

    # Convert markdown to HTML
    html_content = markdown.markdown(
        content, extensions=["fenced_code", "tables", "nl2br", "extra", "codehilite"]
    )

    # Format context as abstract
    context_abstract = format_context_for_abstract(context)

    # Generate PDF
    pdf_path = reports_path / f"SCIENCE_BITCH_ARTIFACT_{timestamp}.pdf"
    print(f"📄 Generating PDF: {pdf_path}")

    generated_path = generate_academic_paper(
        title="Science-Bitch: Complete Scientific Method Workflow Tool",
        content=html_content,
        output_path=pdf_path,
        abstract=context_abstract,
        authors=[{"name": "WAFT Research Team"}],
        email="waft@example.com",
        conference="arXiv",
        year=str(datetime.now().year),
        references=[],
        model_name="Auto",
        generation_date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        spacetime_context=context,  # Pass full context
    )

    if generated_path and generated_path.exists():
        size = generated_path.stat().st_size / 1024
        print(f"✅ PDF generated: {generated_path}")
        print(f"   Size: {size:.1f} KB")

        # Open PDF
        if platform.system() == "Darwin":
            subprocess.run(["open", str(generated_path)], check=False)
        elif platform.system() == "Windows":
            subprocess.run(["start", str(generated_path)], shell=True, check=False)
        else:
            subprocess.run(["xdg-open", str(generated_path)], check=False)

        return 0
    else:
        print("❌ PDF generation failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
