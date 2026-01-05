"""
Substrate Manager - Handles uv commands and environment management.

The "substrate" is the foundation layer that manages the Python environment
through uv commands (init, sync, add, etc.).
"""

import subprocess
from pathlib import Path
from typing import Optional


class SubstrateManager:
    """Manages the uv substrate (environment layer)."""

    def __init__(self):
        """Initialize the substrate manager."""
        pass

    def init_project(self, name: str, target_path: Path) -> bool:
        """
        Initialize a new uv project.

        Args:
            name: Project name
            target_path: Directory where project will be created

        Returns:
            True if successful, False otherwise
        """
        try:
            project_path = target_path / name

            # Create project directory if it doesn't exist
            project_path.mkdir(parents=True, exist_ok=True)

            # Check if project already initialized
            if (project_path / "pyproject.toml").exists():
                # Project already initialized, that's okay
                return True

            # Run uv init inside the project directory
            result = subprocess.run(
                ["uv", "init", "--name", name, "--no-readme"],
                cwd=project_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return True
        except subprocess.CalledProcessError as e:
            # If project already exists, that's okay
            if "already initialized" in e.stderr.lower() or "already exists" in e.stderr.lower():
                return True
            print(f"Error: {e.stderr}")
            return False
        except FileNotFoundError:
            print("Error: uv not found. Please install uv first.")
            return False

    def sync(self, project_path: Path) -> bool:
        """
        Run uv sync to install dependencies.

        Args:
            project_path: Path to project root

        Returns:
            True if successful, False otherwise
        """
        try:
            subprocess.run(
                ["uv", "sync"],
                cwd=project_path,
                check=True,
                capture_output=True,
            )
            return True
        except subprocess.CalledProcessError:
            return False
        except FileNotFoundError:
            return False

    def add_dependency(self, project_path: Path, package: str) -> bool:
        """
        Add a dependency using uv add.

        Args:
            project_path: Path to project root
            package: Package name (e.g., "pytest>=7.0.0")

        Returns:
            True if successful, False otherwise
        """
        try:
            subprocess.run(
                ["uv", "add", package],
                cwd=project_path,
                check=True,
                capture_output=True,
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def verify_lock(self, project_path: Path) -> bool:
        """
        Check if uv.lock exists.

        Args:
            project_path: Path to project root

        Returns:
            True if uv.lock exists, False otherwise
        """
        lock_file = project_path / "uv.lock"
        return lock_file.exists()
