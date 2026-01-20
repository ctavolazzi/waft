"""
Security Utilities
==================

CRITICAL security functions for path validation and input sanitization.
"""

from pathlib import Path

from markdown import markdown

# Optional: bleach for HTML sanitization (security)
try:
    import bleach

    BLEACH_AVAILABLE = True
except ImportError:
    BLEACH_AVAILABLE = False


def validate_path(path: Path, project_root: Path) -> Path:
    """
    Validate path is within project root (CRITICAL security function).

    Prevents path traversal attacks and unauthorized file access.

    Args:
        path: Path to validate
        project_root: Project root directory

    Returns:
        Resolved, validated path

    Raises:
        ValueError: If path is outside project root or contains path traversal
    """
    # Convert to Path if string
    if isinstance(path, str):
        path = Path(path)
    if isinstance(project_root, str):
        project_root = Path(project_root).resolve()

    # Check for path traversal in original path
    if ".." in path.parts:
        raise ValueError(f"Path traversal detected: {path}")

    # Resolve path (follows symlinks)
    try:
        resolved = path.resolve(strict=True)
    except FileNotFoundError:
        # Path doesn't exist yet, but we can still validate the parent
        resolved = path.resolve()

    # Check if resolved path is within project root
    try:
        resolved.relative_to(project_root.resolve())
    except ValueError:
        raise ValueError(f"Path outside project root: {path} (resolved: {resolved})")

    # Check for null bytes or control characters
    path_str = str(path)
    if "\x00" in path_str:
        raise ValueError(f"Path contains null byte: {path}")
    if any(ord(c) < 32 and c not in "\t\n\r" for c in path_str):
        raise ValueError(f"Path contains control characters: {path}")

    return resolved


def sanitize_content(content: str, max_size: int = 10 * 1024 * 1024) -> str:
    """
    Sanitize markdown/HTML content (CRITICAL security function).

    Prevents XSS, code execution, and resource exhaustion attacks.

    Args:
        content: Content to sanitize
        max_size: Maximum content size in bytes (default: 10MB)

    Returns:
        Sanitized HTML content

    Raises:
        ValueError: If content exceeds maximum size
    """
    # Check file size
    content_bytes = content.encode("utf-8")
    if len(content_bytes) > max_size:
        raise ValueError(
            f"Content exceeds maximum size: {len(content_bytes)} bytes (max: {max_size})"
        )

    # Convert markdown to HTML
    html = markdown(content, extensions=["extra", "codehilite"])

    # Post-process: Fix markdown syntax inside HTML divs (markdown doesn't process inside HTML blocks)
    # Convert **text** to <strong>text</strong> in step divs
    import re

    def fix_step_bold(html_content):
        def process_step(match):
            step_html = match.group(1)
            # Replace **text** with <strong>text</strong>
            step_html = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", step_html)
            return f'<div class="step">\n{step_html}\n</div>'

        pattern = r'<div class="step">\n(.*?)\n</div>'
        return re.sub(pattern, process_step, html_content, flags=re.DOTALL)

    html = fix_step_bold(html)

    # Sanitize HTML - allow only safe tags (if bleach is available)
    if BLEACH_AVAILABLE:
        allowed_tags = [
            "p",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "ul",
            "ol",
            "li",
            "strong",
            "em",
            "b",
            "i",
            "u",
            "code",
            "pre",
            "blockquote",
            "img",
            "a",
            "table",
            "thead",
            "tbody",
            "tr",
            "td",
            "th",
            "div",
            "span",
            "br",
            "hr",
        ]

        allowed_attrs = {
            "img": ["src", "alt", "title", "width", "height"],
            "a": ["href", "title"],
            "code": ["class"],
            "pre": ["class"],
        }

        # Clean HTML
        sanitized = bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs, strip=True)
        return sanitized
    else:
        # Fallback: return HTML without sanitization (less secure but functional)
        # Note: Only use this if you trust your content sources
        import warnings

        warnings.warn(
            "bleach not installed - HTML sanitization skipped. "
            "Install with: pip install bleach>=6.0.0",
            UserWarning,
        )
        return html


def validate_image_path(image_path: str, project_root: Path) -> Path | None:
    """
    Validate image path in markdown content.

    Args:
        image_path: Image path from markdown
        project_root: Project root directory

    Returns:
        Validated Path if valid, None otherwise
    """
    if not image_path:
        return None

    try:
        # Remove query strings and fragments
        clean_path = image_path.split("?")[0].split("#")[0]

        # Convert to Path
        path = Path(clean_path)

        # Validate path
        validated = validate_path(path, project_root)

        # Check if file exists and is an image
        if validated.exists() and validated.suffix.lower() in [
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".webp",
            ".svg",
        ]:
            return validated

        return None

    except (ValueError, Exception):
        return None


def validate_metadata(
    title: str, topic: str | None = None, allowed_topics: list | None = None
) -> dict:
    """
    Validate metadata (title, topic, etc.).

    Args:
        title: Document title
        topic: Topic (optional)
        allowed_topics: List of allowed topics

    Returns:
        Dictionary with validated metadata

    Raises:
        ValueError: If validation fails
    """
    errors = []

    # Validate title
    if not title or not title.strip():
        errors.append("Title cannot be empty")
    elif len(title) > 200:
        errors.append(f"Title too long: {len(title)} characters (max: 200)")
    else:
        # Sanitize title (remove HTML)
        title = bleach.clean(title, tags=[], strip=True)

    # Validate topic
    if topic and allowed_topics:
        if topic not in allowed_topics:
            errors.append(f"Topic '{topic}' not in allowed list: {allowed_topics}")

    if errors:
        raise ValueError("Metadata validation failed: " + "; ".join(errors))

    return {"title": title, "topic": topic}
