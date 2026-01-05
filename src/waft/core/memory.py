"""
Memory Manager - Handles _pyrite folder protocol.

The "memory" is the persistent structure that organizes project knowledge:
- active/ - Current work
- backlog/ - Future work
- standards/ - Project standards and protocols
"""

from pathlib import Path
from typing import Dict


class MemoryManager:
    """Manages the _pyrite memory structure."""

    REQUIRED_FOLDERS = [
        "active",
        "backlog",
        "standards",
    ]

    def __init__(self, project_path: Path):
        """
        Initialize the memory manager.

        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.pyrite_path = project_path / "_pyrite"

    def create_structure(self) -> None:
        """Create the full _pyrite directory structure."""
        # Ensure project path exists (uv init should have created it, but be safe)
        self.project_path.mkdir(parents=True, exist_ok=True)

        # Create _pyrite root (with parents=True to ensure project_path exists)
        self.pyrite_path.mkdir(parents=True, exist_ok=True)

        # Create required subfolders
        for folder in self.REQUIRED_FOLDERS:
            (self.pyrite_path / folder).mkdir(parents=True, exist_ok=True)

        # Create .gitkeep files to ensure folders are tracked
        for folder in self.REQUIRED_FOLDERS:
            gitkeep = self.pyrite_path / folder / ".gitkeep"
            if not gitkeep.exists():
                gitkeep.write_text("# This file ensures the folder is tracked by git\n")

    def verify_structure(self) -> Dict:
        """
        Verify the _pyrite structure is valid.

        Returns:
            Dictionary with 'valid' bool and 'folders' dict
        """
        result = {
            "valid": True,
            "folders": {},
        }

        # Check if _pyrite exists
        if not self.pyrite_path.exists():
            result["valid"] = False
            for folder in self.REQUIRED_FOLDERS:
                result["folders"][f"_pyrite/{folder}"] = False
            return result

        # Check each required folder
        for folder in self.REQUIRED_FOLDERS:
            folder_path = self.pyrite_path / folder
            exists = folder_path.exists() and folder_path.is_dir()
            result["folders"][f"_pyrite/{folder}"] = exists

            if not exists:
                result["valid"] = False

        return result

    def get_active_files(self) -> list[Path]:
        """
        Get all files in the active directory.

        Returns:
            List of file paths in _pyrite/active/
        """
        active_path = self.pyrite_path / "active"
        if not active_path.exists():
            return []
        return [f for f in active_path.iterdir() if f.is_file() and f.name != ".gitkeep"]

    def get_backlog_files(self) -> list[Path]:
        """
        Get all files in the backlog directory.

        Returns:
            List of file paths in _pyrite/backlog/
        """
        backlog_path = self.pyrite_path / "backlog"
        if not backlog_path.exists():
            return []
        return [f for f in backlog_path.iterdir() if f.is_file() and f.name != ".gitkeep"]

    def get_standards_files(self) -> list[Path]:
        """
        Get all files in the standards directory.

        Returns:
            List of file paths in _pyrite/standards/
        """
        standards_path = self.pyrite_path / "standards"
        if not standards_path.exists():
            return []
        return [f for f in standards_path.iterdir() if f.is_file() and f.name != ".gitkeep"]

    def get_all_files(self, recursive: bool = False) -> list[Path]:
        """
        Get all files in _pyrite directory.

        Args:
            recursive: If True, include files in subdirectories

        Returns:
            List of file paths in _pyrite/
        """
        if not self.pyrite_path.exists():
            return []

        if recursive:
            # Recursive: use rglob to find all files
            return [
                f for f in self.pyrite_path.rglob("*")
                if f.is_file() and f.name != ".gitkeep"
            ]
        else:
            # Non-recursive: combine all category files
            return (
                self.get_active_files() +
                self.get_backlog_files() +
                self.get_standards_files()
            )

    def get_files_by_extension(self, extension: str, recursive: bool = False) -> list[Path]:
        """
        Get files matching a specific extension.

        Args:
            extension: File extension (e.g., ".md", ".txt")
            recursive: If True, search subdirectories

        Returns:
            List of matching file paths
        """
        all_files = self.get_all_files(recursive=recursive)
        # Ensure extension starts with dot
        ext = extension if extension.startswith(".") else f".{extension}"
        return [f for f in all_files if f.suffix == ext]

