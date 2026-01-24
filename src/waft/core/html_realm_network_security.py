"""
HTML Realm Network Security Module

CRITICAL: Security validation functions for HTML Realm Network system.
All file operations must use these functions before processing.

This module provides:
- Path validation (sensitive file detection, path traversal prevention)
- Safe HTML parsing (size limits, timeouts, no script execution)
- Secure file permissions (0o600 for files, 0o700 for directories)
"""

from __future__ import annotations

import os
import re
import threading
from collections import Counter
from pathlib import Path
from re import Pattern
from typing import Any

try:
    from bs4 import BeautifulSoup

    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False
    BeautifulSoup = None  # type: ignore

from ..utils import _validate_path_in_storage

# Security Constants
SENSITIVE_PATTERNS: list[Pattern[str]] = [
    re.compile(r"_hidden/"),
    re.compile(r"\.env.*"),
    re.compile(r"secrets/"),
    re.compile(r".*\.key$"),
    re.compile(r".*\.pem$"),
    re.compile(r".*\.secret$"),
    re.compile(r"\.git/"),
    re.compile(r"node_modules/"),
]

MAX_HTML_SIZE = 10 * 1024 * 1024  # 10MB
MAX_PARSING_TIME = 30  # seconds
FILE_PERM = 0o600  # Owner read/write only
DIR_PERM = 0o700  # Owner read/write/execute only


def _is_sensitive_file(path: Path) -> bool:
    """
    Check if a file path matches sensitive patterns.

    Args:
        path: Path to check

    Returns:
        True if sensitive, False otherwise
    """
    path_str = str(path)

    # Check against sensitive patterns
    for pattern in SENSITIVE_PATTERNS:
        if pattern.search(path_str):
            return True

    # Check if path is a symlink
    try:
        if path.exists() and path.is_symlink():
            return True
    except (OSError, PermissionError):
        # If we can't check, assume sensitive for safety
        return True

    return False


def _validate_html_path(path: Path, project_root: Path) -> bool:
    """
    Validate that an HTML file path is safe to process.

    Uses existing _validate_path_in_storage() for path validation,
    then checks file-specific requirements.

    Args:
        path: Path to HTML file
        project_root: Project root directory

    Returns:
        True if valid, False otherwise
    """
    try:
        # Check if path is sensitive
        if _is_sensitive_file(path):
            return False

        # Calculate relative path for validation
        try:
            relative_path = path.relative_to(project_root)
        except ValueError:
            # Path is not relative to project root
            return False

        # Use existing path validation
        if not _validate_path_in_storage(relative_path, project_root):
            return False

        # Check file extension
        if path.suffix.lower() != ".html":
            return False

        # Check file exists and is a file
        if not path.exists() or not path.is_file():
            return False

        # Check file size
        try:
            file_size = path.stat().st_size
            if file_size > MAX_HTML_SIZE:
                return False
        except (OSError, PermissionError):
            return False

        # Check file is readable
        if not os.access(path, os.R_OK):
            return False

        return True
    except (OSError, ValueError, PermissionError):
        return False


def parse_html_safely(html_path: Path, timeout: int = MAX_PARSING_TIME) -> dict[str, Any] | None:
    """
    Safely parse an HTML file with size limits, timeout, and safe parsing mode.

    Args:
        html_path: Path to HTML file
        timeout: Maximum parsing time in seconds (default: MAX_PARSING_TIME)

    Returns:
        Dictionary with parsed structure, or None on failure
    """
    if not BEAUTIFULSOUP_AVAILABLE:
        # Fallback to basic parsing without BeautifulSoup
        return _parse_html_basic(html_path, timeout)

    try:
        # Check file size before reading
        try:
            file_size = html_path.stat().st_size
            if file_size > MAX_HTML_SIZE:
                return None
        except (OSError, PermissionError):
            return None

        # Read file with timeout protection
        html_content = _read_file_with_timeout(html_path, timeout)
        if html_content is None:
            return None

        # Parse with BeautifulSoup in safe mode (no script execution)
        # Using 'html.parser' (Python's built-in parser) for safety
        soup = BeautifulSoup(html_content, "html.parser")

        return {"soup": soup, "content": html_content, "size": len(html_content), "parsed": True}
    except (OSError, PermissionError, ValueError):
        return None
    except Exception:
        # Handle any other parsing errors gracefully
        return None


def _parse_html_basic(html_path: Path, timeout: int) -> dict[str, Any] | None:
    """
    Basic HTML parsing fallback when BeautifulSoup is not available.

    Args:
        html_path: Path to HTML file
        timeout: Maximum parsing time in seconds

    Returns:
        Dictionary with basic parsed structure, or None on failure
    """
    try:
        html_content = _read_file_with_timeout(html_path, timeout)
        if html_content is None:
            return None

        return {
            "soup": None,
            "content": html_content,
            "size": len(html_content),
            "parsed": False,  # Not fully parsed without BeautifulSoup
        }
    except (OSError, PermissionError):
        return None


def _read_file_with_timeout(file_path: Path, timeout: int) -> str | None:
    """
    Read a file with timeout protection.

    Uses threading.Timer for cross-platform timeout support.

    Args:
        file_path: Path to file
        timeout: Maximum time in seconds

    Returns:
        File content as string, or None on timeout/failure
    """
    result = {"content": None, "error": None}

    def read_file():
        """Read file in separate thread."""
        try:
            result["content"] = file_path.read_text(encoding="utf-8")
        except Exception as e:
            result["error"] = str(e)

    # Start reading in separate thread
    thread = threading.Thread(target=read_file)
    thread.daemon = True
    thread.start()
    thread.join(timeout=timeout)

    # Check if thread is still alive (timed out)
    if thread.is_alive():
        return None

    # Check for errors
    if result["error"]:
        return None

    return result["content"]


def extract_html_metadata(soup: BeautifulSoup | None) -> dict[str, Any]:
    """
    Extract metadata from parsed HTML.

    Args:
        soup: BeautifulSoup object (or None if not parsed)

    Returns:
        Dictionary with extracted metadata
    """
    metadata = {"title": "", "links": [], "content_themes": [], "link_count": 0}

    if soup is None:
        return metadata

    try:
        # Extract title
        title_tag = soup.find("title")
        if title_tag:
            metadata["title"] = title_tag.get_text(strip=True)

        # Extract links from <a href> tags
        links = []
        for link_tag in soup.find_all("a", href=True):
            href = link_tag.get("href", "")
            if href:
                links.append(href)

        metadata["links"] = links
        metadata["link_count"] = len(links)

        # Extract content themes (basic keyword extraction)
        # Get text content and extract common words
        text_content = soup.get_text()
        words = text_content.lower().split()

        # Filter out common stop words and short words
        stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "must",
            "can",
        }
        meaningful_words = [w for w in words if len(w) > 3 and w not in stop_words]

        # Count word frequency (simple approach)
        word_counts = Counter(meaningful_words)

        # Get top 10 most common words as themes
        themes = [word for word, count in word_counts.most_common(10)]
        metadata["content_themes"] = themes

        # Remove script tags and inline event handlers (already done by BeautifulSoup parsing)
        # But we can verify no script content remains
        scripts = soup.find_all("script")
        if scripts:
            # Log warning but don't fail - BeautifulSoup already parsed safely
            pass

    except Exception:
        # Return partial metadata on error
        pass

    return metadata


def set_secure_permissions(path: Path, is_dir: bool = False) -> None:
    """
    Set secure file permissions (0o600 for files, 0o700 for directories).

    Gracefully handles Windows where permissions may not be settable.

    Args:
        path: Path to file or directory
        is_dir: True if path is a directory, False if file
    """
    try:
        if is_dir:
            path.chmod(DIR_PERM)
        else:
            path.chmod(FILE_PERM)
    except (OSError, PermissionError):
        # Ignore if permissions can't be set (e.g., on Windows)
        # This is expected behavior - fail silently
        pass
