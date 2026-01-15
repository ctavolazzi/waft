"""
Science-Bitch: Full Scientific Method Command

Runs the complete scientific method workflow:
1. Form hypothesis
2. Design experiment
3. Capture initial state (A)
4. Run experiment
5. Collect data (C)
6. Capture final state (B)
7. Analyze results
8. Generate reports
"""

from pathlib import Path
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime
import re
import subprocess
import platform
import markdown
import os
import json
import uuid
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Import scientific method tool
import sys

# Add project root to path for scientific_method_tool
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scientific_method_tool import (
    Hypothesis,
    Variable,
    VariableType,
    ExperimentManager,
    ExperimentLoop,
    ExperimentAnalyzer,
    IterationConfig,
)


class ScienceBitchManager:
    """Manages the full scientific method workflow."""
    
    def __init__(self, project_path: Path):
        """
        Initialize Science-Bitch manager.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.science_path = project_path / "_science"
        self.science_path.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.science_path / "experiments").mkdir(exist_ok=True)
        (self.science_path / "data").mkdir(exist_ok=True)
        (self.science_path / "reports").mkdir(exist_ok=True)
        (self.science_path / "tools").mkdir(exist_ok=True)
        
        self.console = Console()
        self.experiment_manager = ExperimentManager(self.science_path / "experiments")
        self.analyzer = ExperimentAnalyzer()
    
    def _capture_spacetime_context(self) -> Dict[str, Any]:
        """
        Capture ALL contextual data about the moment /science-bitch was invoked.
        This creates a true "artifact" of that point in spacetime.
        
        Returns:
            Dictionary with comprehensive context data
        """
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
                "path": str(self.project_path),
                "name": self.project_path.name,
                "absolute_path": str(self.project_path.absolute()),
            },
            "git": self._capture_git_state(),
            "system": self._capture_system_state(),
            "project_state": self._capture_project_state(),
            "environment": self._capture_environment_state(),
        }
        
        return context
    
    def _capture_git_state(self) -> Dict[str, Any]:
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
            # Check if git is initialized
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.project_path,
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
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                git_state["branch"] = result.stdout.strip()
            
            # Get current commit
            result = subprocess.run(
                ["git", "log", "-1", "--format=%H|%s|%an|%ad", "--date=iso"],
                cwd=self.project_path,
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
                cwd=self.project_path,
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
                cwd=self.project_path,
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
                        git_state["recent_commits"].append({
                            "hash": parts[0][:8],
                            "message": parts[1],
                            "author": parts[2],
                            "date": parts[3],
                        })
            
            # Get remote URL
            result = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                git_state["remote_url"] = result.stdout.strip()
            
            # Get commits ahead/behind
            result = subprocess.run(
                ["git", "rev-list", "--left-right", "--count", "HEAD...@{upstream}"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0 and result.stdout.strip():
                parts = result.stdout.strip().split("\t")
                if len(parts) == 2:
                    git_state["commits_behind"] = int(parts[0])
                    git_state["commits_ahead"] = int(parts[1])
        except Exception as e:
            git_state["error"] = str(e)
        
        return git_state
    
    def _capture_system_state(self) -> Dict[str, Any]:
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
        
        # Disk space (if on macOS/Linux)
        try:
            if platform.system() == "Darwin":
                result = subprocess.run(
                    ["df", "-h", str(self.project_path)],
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
    
    def _capture_project_state(self) -> Dict[str, Any]:
        """Capture project-specific state."""
        project_state = {
            "active_work_efforts": [],
            "recent_files": [],
            "project_structure": {},
        }
        
        # Check for active work efforts
        work_efforts_path = self.project_path / "_work_efforts"
        if work_efforts_path.exists():
            try:
                # Look for active work effort files
                for item in work_efforts_path.iterdir():
                    if item.is_file() and item.suffix == ".md":
                        # Check if it's an active work effort (heuristic)
                        content = item.read_text()[:500]
                        if "status" in content.lower() and ("active" in content.lower() or "in progress" in content.lower()):
                            project_state["active_work_efforts"].append({
                                "name": item.name,
                                "path": str(item.relative_to(self.project_path)),
                            })
            except Exception:
                pass
        
        # Get recent files (modified in last 24 hours)
        try:
            recent_files = []
            for root, dirs, files in os.walk(self.project_path):
                # Skip hidden and large directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', '__pycache__']]
                
                for file in files:
                    if file.startswith('.'):
                        continue
                    file_path = Path(root) / file
                    try:
                        mtime = file_path.stat().st_mtime
                        hours_ago = (datetime.now().timestamp() - mtime) / 3600
                        if hours_ago < 24:
                            recent_files.append({
                                "path": str(file_path.relative_to(self.project_path)),
                                "modified_hours_ago": round(hours_ago, 2),
                            })
                    except Exception:
                        pass
                
                if len(recent_files) > 50:  # Limit to 50 most recent
                    break
            
            project_state["recent_files"] = sorted(recent_files, key=lambda x: x["modified_hours_ago"])[:20]
        except Exception:
            pass
        
        return project_state
    
    def _capture_environment_state(self) -> Dict[str, Any]:
        """Capture environment variables and configuration."""
        env_state = {
            "python_path": os.environ.get("PYTHONPATH"),
            "virtual_env": os.environ.get("VIRTUAL_ENV"),
            "conda_env": os.environ.get("CONDA_DEFAULT_ENV"),
            "user": os.environ.get("USER") or os.environ.get("USERNAME"),
            "home": os.environ.get("HOME") or os.environ.get("USERPROFILE"),
        }
        
        # Check for WAFT-specific environment variables
        waft_vars = {k: v for k, v in os.environ.items() if k.startswith("WAFT") or k.startswith("EMPIRICA")}
        if waft_vars:
            env_state["waft_variables"] = {k: "***" if "key" in k.lower() or "secret" in k.lower() or "token" in k.lower() else v 
                                          for k, v in waft_vars.items()}
        
        return env_state
