"""
Substrate Manager - Handles uv commands and environment management.

The "substrate" is the foundation layer that manages the Python environment
through uv commands (init, sync, add, etc.).
"""

import subprocess
from pathlib import Path
from typing import Optional

from ..utils import parse_toml_field


class SubstrateManager:
    """Manages the uv substrate (environment layer)."""

    def __init__(self, project_path: Optional[Path] = None):
        """
        Initialize the substrate manager.

        Args:
            project_path: Optional path to project root. If provided, methods can use
                         this as default, but still accept project_path parameter.
        """
        self.project_path = project_path

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

    def sync(self, project_path: Optional[Path] = None) -> bool:
        """
        Run uv sync to install dependencies.

        Args:
            project_path: Path to project root. If None, uses self.project_path.

        Returns:
            True if successful, False otherwise
        """
        project_path = project_path or self.project_path
        if project_path is None:
            raise ValueError("project_path must be provided either in __init__ or as parameter")
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

    def add_dependency(self, package: str, project_path: Optional[Path] = None) -> bool:
        """
        Add a dependency using uv add.

        Args:
            package: Package name (e.g., "pytest>=7.0.0")
            project_path: Path to project root. If None, uses self.project_path.

        Returns:
            True if successful, False otherwise
        """
        project_path = project_path or self.project_path
        if project_path is None:
            raise ValueError("project_path must be provided either in __init__ or as parameter")
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

    def verify_lock(self, project_path: Optional[Path] = None) -> bool:
        """
        Check if uv.lock exists.

        Args:
            project_path: Path to project root. If None, uses self.project_path.

        Returns:
            True if uv.lock exists, False otherwise
        """
        project_path = project_path or self.project_path
        if project_path is None:
            raise ValueError("project_path must be provided either in __init__ or as parameter")
        lock_file = project_path / "uv.lock"
        return lock_file.exists()

    def get_project_info(self, project_path: Optional[Path] = None) -> dict:
        """
        Get basic project information from pyproject.toml.

        Args:
            project_path: Path to project root. If None, uses self.project_path.

        Returns:
            Dictionary with project info (name, version, etc.)
        """
        project_path = project_path or self.project_path
        if project_path is None:
            raise ValueError("project_path must be provided either in __init__ or as parameter")
        pyproject_path = project_path / "pyproject.toml"
        if not pyproject_path.exists():
            return {}

        info = {}
        name = parse_toml_field(pyproject_path, "name")
        if name:
            info["name"] = name

        version = parse_toml_field(pyproject_path, "version")
        if version:
            info["version"] = version

        return info

