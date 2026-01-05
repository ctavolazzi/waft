"""
GitHub Integration - Commands for GitHub repository management.
"""

import subprocess
import json
from pathlib import Path
from typing import Optional, Dict, Any


class GitHubManager:
    """Manages GitHub integration for projects."""

    def __init__(self, project_path: Path):
        """
        Initialize the GitHubManager.

        Args:
            project_path: Path to project root
        """
        self.project_path = project_path

    def is_initialized(self) -> bool:
        """Check if git repository is initialized."""
        return (self.project_path / ".git").exists()

    def get_remote_url(self) -> Optional[str]:
        """Get GitHub remote URL if configured."""
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    def init_repository(self) -> bool:
        """Initialize git repository if not already initialized."""
        if self.is_initialized():
            return True

        try:
            subprocess.run(
                ["git", "init"],
                cwd=self.project_path,
                capture_output=True,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get repository status."""
        status = {
            "initialized": self.is_initialized(),
            "remote_url": self.get_remote_url(),
        }

        if self.is_initialized():
            try:
                # Get branch name
                result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                status["branch"] = result.stdout.strip()

                # Get commit count
                result = subprocess.run(
                    ["git", "rev-list", "--count", "HEAD"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                status["commits"] = int(result.stdout.strip())
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass

        return status

