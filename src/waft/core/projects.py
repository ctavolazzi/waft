"""
Projects - Long-Term Project Management System

Manages long-term projects that can be worked on incrementally over time.
Provides foundation for managing complex, multi-session work.
"""

import json
import re
import shutil
from datetime import datetime
from enum import Enum
from pathlib import Path
from threading import Lock
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict

from ..utils import _validate_path_in_storage
from ..logging import get_logger

logger = get_logger(__name__)


class ProjectStatus(Enum):
    """Project status."""
    PLANNING = "planning"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


@dataclass
class Milestone:
    """Project milestone."""
    milestone_id: str
    title: str
    description: str = ""
    target_date: Optional[str] = None
    completed: bool = False
    completed_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Milestone":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class ProgressEntry:
    """Progress entry for a work session."""
    entry_id: str
    timestamp: str
    progress_delta: float  # Change in progress percentage
    notes: str = ""
    work_effort_id: Optional[str] = None
    session_duration: Optional[float] = None  # Minutes spent

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProgressEntry":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class Project:
    """Project data model."""
    project_id: str
    title: str
    description: str = ""
    status: ProjectStatus = ProjectStatus.PLANNING
    created_at: str = ""
    updated_at: str = ""
    progress_percent: float = 0.0
    tags: List[str] = field(default_factory=list)
    milestones: List[Milestone] = field(default_factory=list)
    progress_entries: List[ProgressEntry] = field(default_factory=list)
    related_work_efforts: List[str] = field(default_factory=list)
    notes: str = ""
    version: int = 1  # Schema version for migrations

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['status'] = self.status.value
        data['milestones'] = [m.to_dict() for m in self.milestones]
        data['progress_entries'] = [e.to_dict() for e in self.progress_entries]
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        """Create from dictionary."""
        # Convert status string to enum
        if isinstance(data.get('status'), str):
            data['status'] = ProjectStatus(data['status'])

        # Convert milestones
        if 'milestones' in data:
            data['milestones'] = [Milestone.from_dict(m) for m in data['milestones']]

        # Convert progress entries
        if 'progress_entries' in data:
            data['progress_entries'] = [ProgressEntry.from_dict(e) for e in data['progress_entries']]

        return cls(**data)


class ProjectManager:
    """Manages projects with file-based storage and security measures."""

    # Input size limits
    MAX_TITLE_LENGTH = 200
    MAX_DESCRIPTION_LENGTH = 10000
    MAX_NOTES_LENGTH = 10000
    MAX_TAGS = 20
    MAX_TAG_LENGTH = 50
    MAX_MILESTONES = 100
    MAX_PROGRESS_ENTRIES = 1000

    def __init__(self, project_path: Path):
        """
        Initialize project manager.

        Args:
            project_path: Path to project root
        """
        self.project_path = Path(project_path)
        self.projects_dir = self.project_path / "_pyrite" / ".waft" / "projects"
        self.projects_dir.mkdir(parents=True, exist_ok=True)

        # CRITICAL: Set directory permissions (0o700)
        try:
            self.projects_dir.chmod(0o700)
        except (OSError, PermissionError):
            pass  # Ignore on Windows or if permissions can't be set

        # File lock for concurrent access
        self._lock = Lock()

        # Create .gitkeep if needed
        gitkeep = self.projects_dir / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.write_text("# This file ensures the folder is tracked by git\n")

    def _validate_project_id(self, project_id: str) -> bool:
        """
        Validate project ID for security.

        CRITICAL: Rejects path traversal, null bytes, and invalid characters.

        Args:
            project_id: Project ID to validate

        Returns:
            True if valid, False otherwise
        """
        if not project_id:
            return False

        # Reject path traversal
        if '..' in project_id or '/' in project_id or '\\' in project_id:
            return False

        # Reject null bytes
        if '\x00' in project_id:
            return False

        # Reject control characters
        if any(ord(c) < 32 and c not in '\t\n\r' for c in project_id):
            return False

        # Only allow safe filename characters
        if not re.match(r'^[a-zA-Z0-9_-]+$', project_id):
            return False

        return True

    def _validate_path_in_project(self, file_path: Path) -> bool:
        """
        Validate file path is within project directory.

        CRITICAL: Security validation to prevent path traversal.

        Args:
            file_path: File path to validate

        Returns:
            True if valid, False otherwise
        """
        return _validate_path_in_storage(file_path.relative_to(self.project_path), self.project_path)

    def _validate_input(self, title: str, description: str, tags: List[str], progress_percent: float) -> None:
        """
        Validate user inputs.

        CRITICAL: Input validation to prevent DoS and data corruption.

        Args:
            title: Project title
            description: Project description
            tags: Project tags
            progress_percent: Progress percentage

        Raises:
            ValueError: If validation fails
        """
        # Validate title
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if len(title) > self.MAX_TITLE_LENGTH:
            raise ValueError(f"Title exceeds maximum length of {self.MAX_TITLE_LENGTH} characters")
        if any(ord(c) < 32 and c not in '\t\n\r' for c in title):
            raise ValueError("Title contains invalid control characters")

        # Validate description
        if len(description) > self.MAX_DESCRIPTION_LENGTH:
            raise ValueError(f"Description exceeds maximum length of {self.MAX_DESCRIPTION_LENGTH} characters")

        # Validate tags
        if len(tags) > self.MAX_TAGS:
            raise ValueError(f"Maximum {self.MAX_TAGS} tags allowed")
        for tag in tags:
            if len(tag) > self.MAX_TAG_LENGTH:
                raise ValueError(f"Tag exceeds maximum length of {self.MAX_TAG_LENGTH} characters")
            if any(ord(c) < 32 and c not in '\t\n\r' for c in tag):
                raise ValueError(f"Tag contains invalid control characters: {tag}")

        # Validate progress percentage
        if not isinstance(progress_percent, (int, float)):
            raise ValueError("Progress percentage must be a number")
        if progress_percent < 0.0 or progress_percent > 100.0:
            raise ValueError("Progress percentage must be between 0.0 and 100.0")
        if progress_percent != progress_percent:  # Check for NaN
            raise ValueError("Progress percentage cannot be NaN")
        if progress_percent == float('inf') or progress_percent == float('-inf'):
            raise ValueError("Progress percentage cannot be infinity")

    def _check_disk_space(self) -> bool:
        """
        Check available disk space.

        Returns:
            True if sufficient space available, False otherwise
        """
        try:
            stat = shutil.disk_usage(self.projects_dir)
            # Require at least 1MB free
            return stat.free >= 1024 * 1024
        except (OSError, ValueError):
            return True  # Assume OK if check fails

    def create_project(
        self,
        title: str,
        description: str = "",
        tags: Optional[List[str]] = None,
        status: ProjectStatus = ProjectStatus.PLANNING
    ) -> Project:
        """
        Create a new project.

        CRITICAL: Validates inputs and sets file permissions.

        Args:
            title: Project title
            description: Project description
            tags: Project tags
            status: Initial project status

        Returns:
            Created Project instance

        Raises:
            ValueError: If validation fails
            OSError: If file cannot be written
        """
        # Validate inputs
        tags = tags or []
        self._validate_input(title, description, tags, 0.0)

        # Check disk space
        if not self._check_disk_space():
            raise OSError("Insufficient disk space")

        # Generate project ID
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        project_id = f"proj_{timestamp}"

        # Ensure unique ID
        counter = 1
        while (self.projects_dir / f"{project_id}.json").exists():
            project_id = f"proj_{timestamp}_{counter}"
            counter += 1

        # Create project
        project = Project(
            project_id=project_id,
            title=title,
            description=description,
            status=status,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            tags=tags,
            progress_percent=0.0
        )

        # Save project
        self._save_project(project)

        logger.info(f"Created project: {project_id} - {title}")
        return project

    def get_project(self, project_id: str) -> Optional[Project]:
        """
        Get project by ID.

        CRITICAL: Validates project_id and file paths.

        Args:
            project_id: Project ID

        Returns:
            Project instance or None if not found

        Raises:
            ValueError: If project_id is invalid
        """
        # Validate project_id
        if not self._validate_project_id(project_id):
            raise ValueError(f"Invalid project_id: {project_id} (contains path traversal or invalid characters)")

        project_file = self.projects_dir / f"{project_id}.json"

        # Validate path
        if not self._validate_path_in_project(project_file):
            raise ValueError(f"Path traversal detected: {project_file}")

        if not project_file.exists():
            return None

        return self._load_project(project_file)

    def update_project(self, project: Project) -> None:
        """
        Update existing project.

        CRITICAL: Creates backup, validates inputs, uses atomic writes.

        Args:
            project: Project instance to update

        Raises:
            ValueError: If validation fails
            OSError: If file cannot be written
        """
        # Validate project_id
        if not self._validate_project_id(project.project_id):
            raise ValueError(f"Invalid project_id: {project.project_id}")

        # Validate inputs
        self._validate_input(project.title, project.description, project.tags, project.progress_percent)

        # Validate milestones count
        if len(project.milestones) > self.MAX_MILESTONES:
            raise ValueError(f"Maximum {self.MAX_MILESTONES} milestones allowed")

        # Validate progress entries count (keep last N)
        if len(project.progress_entries) > self.MAX_PROGRESS_ENTRIES:
            project.progress_entries = project.progress_entries[-self.MAX_PROGRESS_ENTRIES:]

        # Validate notes length
        if len(project.notes) > self.MAX_NOTES_LENGTH:
            raise ValueError(f"Notes exceed maximum length of {self.MAX_NOTES_LENGTH} characters")

        # Check disk space
        if not self._check_disk_space():
            raise OSError("Insufficient disk space")

        # Update timestamp
        project.updated_at = datetime.now().isoformat()

        # Create backup before update
        project_file = self.projects_dir / f"{project.project_id}.json"
        if project_file.exists():
            backup_file = project_file.with_suffix('.json.bak')
            try:
                shutil.copy2(project_file, backup_file)
            except (IOError, OSError):
                logger.warning(f"Could not create backup for {project.project_id}")

        # Save project
        self._save_project(project)

        logger.info(f"Updated project: {project.project_id}")

    def delete_project(self, project_id: str) -> bool:
        """
        Delete project.

        CRITICAL: Validates project_id and file paths.

        Args:
            project_id: Project ID to delete

        Returns:
            True if deleted, False if not found

        Raises:
            ValueError: If project_id is invalid
        """
        # Validate project_id
        if not self._validate_project_id(project_id):
            raise ValueError(f"Invalid project_id: {project_id}")

        project_file = self.projects_dir / f"{project_id}.json"

        # Validate path
        if not self._validate_path_in_project(project_file):
            raise ValueError(f"Path traversal detected: {project_file}")

        if not project_file.exists():
            return False

        try:
            project_file.unlink()
            logger.info(f"Deleted project: {project_id}")
            return True
        except (IOError, OSError) as e:
            logger.error(f"Failed to delete project {project_id}: {e}")
            raise OSError(f"Failed to delete project {project_id}: {e}")

    def list_projects(
        self,
        status: Optional[ProjectStatus] = None,
        tags: Optional[List[str]] = None
    ) -> List[Project]:
        """
        List all projects, optionally filtered.

        Args:
            status: Filter by status
            tags: Filter by tags (projects must have all specified tags)

        Returns:
            List of Project instances
        """
        projects = []

        if not self.projects_dir.exists():
            return projects

        for project_file in self.projects_dir.glob("*.json"):
            # Skip backup files
            if project_file.name.endswith('.bak'):
                continue

            try:
                project = self._load_project(project_file)

                # Apply filters
                if status and project.status != status:
                    continue

                if tags:
                    if not all(tag in project.tags for tag in tags):
                        continue

                projects.append(project)
            except (json.JSONDecodeError, ValueError, OSError) as e:
                logger.warning(f"Failed to load project from {project_file}: {e}")
                continue

        # Sort by updated_at (most recent first)
        projects.sort(key=lambda p: p.updated_at, reverse=True)

        return projects

    def _save_project(self, project: Project) -> None:
        """
        Save project to disk with security measures.

        CRITICAL: Uses file locking, atomic writes, and sets permissions.

        Args:
            project: Project instance to save

        Raises:
            OSError: If file cannot be written
        """
        project_file = self.projects_dir / f"{project.project_id}.json"

        # Validate path
        if not self._validate_path_in_project(project_file):
            raise ValueError(f"Path traversal detected: {project_file}")

        with self._lock:
            try:
                # Write to temp file first (atomic write)
                temp_file = project_file.with_suffix('.tmp')
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(project.to_dict(), f, indent=2, ensure_ascii=False)

                # CRITICAL: Set file permissions (0o600)
                try:
                    temp_file.chmod(0o600)
                except (OSError, PermissionError):
                    pass  # Ignore on Windows

                # Atomic rename
                temp_file.replace(project_file)

                # CRITICAL: Set file permissions on final file
                try:
                    project_file.chmod(0o600)
                except (OSError, PermissionError):
                    pass  # Ignore on Windows

            except (IOError, OSError, PermissionError) as e:
                # Clean up temp file on error
                if temp_file.exists():
                    try:
                        temp_file.unlink()
                    except:
                        pass
                raise OSError(f"Failed to save project {project.project_id}: {e}")

    def _load_project(self, project_file: Path) -> Project:
        """
        Load project from disk with security measures.

        CRITICAL: Validates file paths and handles errors.

        Args:
            project_file: Path to project file

        Returns:
            Project instance

        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If file is corrupted
            OSError: If file cannot be read
        """
        if not project_file.exists():
            raise FileNotFoundError(f"Project file not found: {project_file}")

        try:
            with open(project_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Validate JSON structure
            if not isinstance(data, dict):
                raise json.JSONDecodeError("Project data must be a dictionary", project_file, 0)

            # Validate required fields
            required_fields = ['project_id', 'title', 'status', 'created_at', 'updated_at']
            for field in required_fields:
                if field not in data:
                    raise json.JSONDecodeError(f"Missing required field: {field}", project_file, 0)

            return Project.from_dict(data)

        except json.JSONDecodeError as e:
            logger.error(f"Corrupted project file {project_file}: {e}")
            raise
        except (IOError, OSError, PermissionError) as e:
            logger.error(f"Failed to load project from {project_file}: {e}")
            raise OSError(f"Failed to load project: {e}")
