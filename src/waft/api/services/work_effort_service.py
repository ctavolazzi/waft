"""
Work Effort Service - Handles file system operations for work efforts.

Manages the file-based work effort system with YAML frontmatter parsing.
"""

import re
import secrets
import shutil
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml

from ...logging import get_logger
from ...utils import _validate_path_in_storage

logger = get_logger(__name__)

# Security constants
MAX_FRONTMATTER_SIZE = 10 * 1024  # 10KB max for YAML frontmatter
MAX_DESCRIPTION_SIZE = 10 * 1024  # 10KB max for description
MAX_TITLE_SIZE = 200  # Already enforced by Pydantic


class WorkEffortService:
    """Service for managing work efforts via file system operations."""

    def __init__(self, project_path: Path):
        """
        Initialize work effort service.

        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.work_efforts_dir = project_path / "_work_efforts"

    def _validate_work_effort_id(self, we_id: str) -> bool:
        """Validate work effort ID format: WE-YYMMDD-xxxx"""
        pattern = r'^WE-\d{6}-[a-z0-9]{4}$'
        return bool(re.match(pattern, we_id))

    def _validate_path_in_work_efforts(self, file_path: Path) -> bool:
        """
        CRITICAL: Validate file path is within work efforts directory.
        
        Prevents path traversal attacks.
        
        Args:
            file_path: File path to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Ensure work_efforts_dir exists
            if not self.work_efforts_dir.exists():
                return False
            
            # Get relative path from work_efforts_dir
            try:
                relative_path = file_path.relative_to(self.work_efforts_dir)
            except ValueError:
                # Path is not relative to work_efforts_dir
                return False
            
            # Use existing validation utility
            return _validate_path_in_storage(relative_path, self.work_efforts_dir)
        except (OSError, ValueError):
            return False

    def _generate_work_effort_id(self) -> str:
        """Generate a new work effort ID: WE-YYMMDD-xxxx"""
        date_str = datetime.now().strftime('%y%m%d')
        random_suffix = ''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(4))
        we_id = f"WE-{date_str}-{random_suffix}"

        # Ensure uniqueness
        counter = 1
        while self._work_effort_exists(we_id):
            random_suffix = ''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(4))
            we_id = f"WE-{date_str}-{random_suffix}"
            counter += 1
            if counter > 100:  # Safety limit
                raise ValueError("Could not generate unique work effort ID")

        return we_id

    def _work_effort_exists(self, we_id: str) -> bool:
        """Check if work effort exists."""
        we_dir = self.work_efforts_dir / we_id
        return we_dir.exists() and we_dir.is_dir()

    def _generate_slug(self, title: str) -> str:
        """Generate filesystem-safe slug from title."""
        # Convert to lowercase, replace spaces with hyphens
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)  # Remove special chars
        slug = re.sub(r'\s+', '-', slug)  # Replace spaces with hyphens
        slug = re.sub(r'-+', '-', slug)  # Collapse multiple hyphens
        slug = slug.strip('-')  # Remove leading/trailing hyphens
        return slug[:50]  # Limit length

    def _parse_frontmatter(self, content: str) -> tuple[Dict[str, Any], str]:
        """
        Parse YAML frontmatter from markdown content.

        CRITICAL: Limits YAML size to prevent Billion Laughs attack.

        Returns:
            Tuple of (frontmatter_dict, markdown_content)
        """
        # Match YAML frontmatter (--- blocks)
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if frontmatter_match:
            frontmatter_text = frontmatter_match.group(1)
            
            # CRITICAL: Limit YAML size to prevent DoS attacks
            if len(frontmatter_text) > MAX_FRONTMATTER_SIZE:
                logger.warning(f"Frontmatter too large: {len(frontmatter_text)} bytes (max {MAX_FRONTMATTER_SIZE})")
                return {}, content
            
            try:
                frontmatter = yaml.safe_load(frontmatter_text) or {}
                markdown_content = content[frontmatter_match.end():].strip()
                return frontmatter, markdown_content
            except yaml.YAMLError as e:
                logger.warning(f"Failed to parse frontmatter: {e}")
                return {}, content
        return {}, content

    def _write_frontmatter(self, frontmatter: Dict[str, Any], content: str) -> str:
        """Write YAML frontmatter and content to markdown format."""
        frontmatter_text = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
        return f"---\n{frontmatter_text}---\n\n{content}\n"

    def create_work_effort(
        self,
        title: str,
        description: str = "",
        status: str = "active",
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new work effort.

        Args:
            title: Work effort title
            description: Work effort description
            status: Initial status (active, paused, completed)
            tags: Optional tags

        Returns:
            Work effort data dictionary
        """
        # Generate ID and slug
        we_id = self._generate_work_effort_id()
        slug = self._generate_slug(title)
        we_dir_name = f"{we_id}_{slug}" if slug else we_id

        # Create directory
        we_dir = self.work_efforts_dir / we_dir_name
        
        # CRITICAL: Validate path before creation
        if not self._validate_path_in_work_efforts(we_dir):
            raise ValueError(f"Invalid work effort path: {we_dir_name} (path traversal detected)")
        
        we_dir.mkdir(parents=True, exist_ok=True)
        
        # CRITICAL: Set restrictive permissions (owner only)
        try:
            we_dir.chmod(0o700)  # Owner read/write/execute only
        except OSError:
            logger.warning(f"Could not set permissions on {we_dir}")

        # Create tickets subdirectory
        tickets_dir = we_dir / "tickets"
        tickets_dir.mkdir(exist_ok=True)
        
        # CRITICAL: Set restrictive permissions
        try:
            os.chmod(tickets_dir, 0o700)
        except OSError:
            logger.warning(f"Could not set permissions on {tickets_dir}")

        # Create index file
        index_file = we_dir / f"{we_id}_index.md"

        # Prepare frontmatter
        now = datetime.now().isoformat()
        frontmatter = {
            "id": we_id,
            "title": title,
            "status": status,
            "created": now,
            "created_by": "api",
            "last_updated": now,
            "tags": tags or []
        }

        # Create markdown content
        markdown_content = f"# {we_id}: {title}\n\n## Objective\n{description}\n\n## Tickets\n\n| ID | Title | Status |\n|----|-------|--------|\n\n## Commits\n\n- (populated as work progresses)\n\n## Related\n\n- Docs: (to be linked)\n- PRs: (to be added)\n"

        # Write file atomically
        content = self._write_frontmatter(frontmatter, markdown_content)
        temp_file = index_file.with_suffix('.tmp')
        temp_file.write_text(content, encoding='utf-8')
        temp_file.replace(index_file)

        logger.info(f"Created work effort: {we_id}")

        return {
            "id": we_id,
            "title": title,
            "description": description,
            "status": status,
            "tags": tags or [],
            "created": now,
            "created_by": "api",
            "last_updated": now,
            "path": str(we_dir.relative_to(self.project_path))
        }

    def get_work_effort(self, we_id: str) -> Optional[Dict[str, Any]]:
        """
        Get work effort by ID.

        Args:
            we_id: Work effort ID

        Returns:
            Work effort data or None if not found
        """
        if not self._validate_work_effort_id(we_id):
            return None

        # Find work effort directory (may have slug suffix)
        # CRITICAL: Validate directory iteration and reject symlinks
        we_dir = None
        try:
            for item in self.work_efforts_dir.iterdir():
                # Reject symlinks (security: prevent following symlinks outside project)
                if item.is_symlink():
                    logger.warning(f"Skipping symlink in work_efforts: {item.name}")
                    continue
                
                if item.is_dir() and item.name.startswith(we_id):
                    # CRITICAL: Validate path before using
                    if not self._validate_path_in_work_efforts(item):
                        logger.warning(f"Invalid work effort path detected: {item}")
                        continue
                    we_dir = item
                    break
        except (OSError, PermissionError) as e:
            logger.error(f"Error iterating work_efforts directory: {e}")
            return None

        if not we_dir:
            return None

        # Find index file
        index_file = we_dir / f"{we_id}_index.md"
        if not index_file.exists():
            # Try alternative naming
            index_file = we_dir / "index.md"
            if not index_file.exists():
                return None

        try:
            content = index_file.read_text(encoding='utf-8')
            frontmatter, markdown_content = self._parse_frontmatter(content)

            # Extract title from markdown if not in frontmatter
            if 'title' not in frontmatter:
                title_match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
                if title_match:
                    frontmatter['title'] = title_match.group(1)

            frontmatter['path'] = str(we_dir.relative_to(self.project_path))
            return frontmatter
        except (OSError, UnicodeDecodeError) as e:
            logger.error(f"Failed to read work effort {we_id}: {e}")
            return None

    def update_work_effort(
        self,
        we_id: str,
        updates: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Update work effort frontmatter.

        Args:
            we_id: Work effort ID
            updates: Dictionary of fields to update

        Returns:
            Updated work effort data or None if not found
        """
        if not self._validate_work_effort_id(we_id):
            return None

        # Find work effort directory
        we_dir = None
        for item in self.work_efforts_dir.iterdir():
            if item.is_dir() and item.name.startswith(we_id):
                we_dir = item
                break

        if not we_dir:
            return None

        # Find index file
        index_file = we_dir / f"{we_id}_index.md"
        if not index_file.exists():
            index_file = we_dir / "index.md"
            if not index_file.exists():
                return None

        try:
            # Read current content
            content = index_file.read_text(encoding='utf-8')
            frontmatter, markdown_content = self._parse_frontmatter(content)

            # Update frontmatter
            frontmatter.update(updates)
            frontmatter['last_updated'] = datetime.now().isoformat()

            # Write atomically
            new_content = self._write_frontmatter(frontmatter, markdown_content)
            temp_file = index_file.with_suffix('.tmp')
            temp_file.write_text(new_content, encoding='utf-8')
            temp_file.replace(index_file)

            frontmatter['path'] = str(we_dir.relative_to(self.project_path))
            return frontmatter
        except (OSError, UnicodeDecodeError) as e:
            logger.error(f"Failed to update work effort {we_id}: {e}")
            return None

    def delete_work_effort(self, we_id: str) -> bool:
        """
        Delete work effort directory.

        Args:
            we_id: Work effort ID

        Returns:
            True if deleted, False if not found
        """
        if not self._validate_work_effort_id(we_id):
            return False

        # Find work effort directory
        # CRITICAL: Validate directory iteration and reject symlinks
        we_dir = None
        try:
            for item in self.work_efforts_dir.iterdir():
                # Reject symlinks (security: prevent following symlinks outside project)
                if item.is_symlink():
                    logger.warning(f"Skipping symlink in work_efforts: {item.name}")
                    continue
                
                if item.is_dir() and item.name.startswith(we_id):
                    # CRITICAL: Validate path before deletion
                    if not self._validate_path_in_work_efforts(item):
                        logger.warning(f"Invalid work effort path detected for deletion: {item}")
                        continue
                    we_dir = item
                    break
        except (OSError, PermissionError) as e:
            logger.error(f"Error iterating work_efforts directory: {e}")
            return False

        if not we_dir:
            return False

        try:
            shutil.rmtree(we_dir)
            logger.info(f"Deleted work effort: {we_id}")
            return True
        except OSError as e:
            logger.error(f"Failed to delete work effort {we_id}: {e}")
            return False

    def list_work_efforts(
        self,
        status: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50,
        offset: int = 0
    ) -> tuple[List[Dict[str, Any]], int]:
        """
        List work efforts with filtering and pagination.

        Args:
            status: Filter by status
            tags: Filter by tags (must have all)
            limit: Maximum results (default 50, max 100)
            offset: Pagination offset

        Returns:
            Tuple of (work_efforts_list, total_count)
        """
        if not self.work_efforts_dir.exists():
            return [], 0

        work_efforts = []
        limit = min(limit, 100)  # Cap at 100

        # Scan directories
        # CRITICAL: Handle errors and reject symlinks
        try:
            items = list(self.work_efforts_dir.iterdir())
        except (OSError, PermissionError) as e:
            logger.error(f"Error listing work_efforts directory: {e}")
            return [], 0
        
        for item in items:
            # Reject symlinks (security)
            if item.is_symlink():
                logger.warning(f"Skipping symlink in work_efforts: {item.name}")
                continue
            
            if not item.is_dir() or not item.name.startswith("WE-"):
                continue

            # Extract WE ID from directory name
            we_id_match = re.match(r'^(WE-\d{6}-[a-z0-9]{4})', item.name)
            if not we_id_match:
                continue

            we_id = we_id_match.group(1)
            we_data = self.get_work_effort(we_id)
            if not we_data:
                continue

            # Apply filters
            if status and we_data.get('status') != status:
                continue

            if tags:
                we_tags = we_data.get('tags', [])
                if not all(tag in we_tags for tag in tags):
                    continue

            work_efforts.append(we_data)

        # Sort by last_updated (most recent first)
        work_efforts.sort(key=lambda w: w.get('last_updated', ''), reverse=True)

        total_count = len(work_efforts)

        # Apply pagination
        paginated = work_efforts[offset:offset + limit]

        return paginated, total_count
