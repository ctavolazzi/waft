"""
Utility functions - Helper functions for common operations.

These "little guys" help with repetitive tasks like path resolution,
file operations, formatting, and validation.
"""

import json
import logging
import os
import shutil
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any


def resolve_project_path(path: str | None = None) -> Path:
    """
    Resolve project path from optional string or default to current directory.

    Args:
        path: Optional path string. If None, uses current directory.

    Returns:
        Resolved Path object

    Raises:
        ValueError: If path doesn't exist or is not a directory
    """
    resolved = Path(path) if path else Path.cwd()

    # Validate path exists
    if not resolved.exists():
        raise ValueError(f"Path does not exist: {resolved}")

    # Validate path is a directory
    if not resolved.is_dir():
        raise ValueError(f"Path is not a directory: {resolved}")

    return resolved


def is_waft_project(path: Path) -> bool:
    """
    Check if a path is a Waft project (has _pyrite directory).

    Args:
        path: Path to check

    Returns:
        True if path is a Waft project, False otherwise
    """
    if not path.exists() or not path.is_dir():
        return False
    return (path / "_pyrite").exists()


def is_inside_waft_project(path: Path) -> tuple[bool, Path | None]:
    """
    Check if a path is inside a Waft project.

    Args:
        path: Path to check

    Returns:
        Tuple of (is_inside, waft_project_path)
        - is_inside: True if path is inside a Waft project
        - waft_project_path: Path to the Waft project root, or None
    """
    current = path.resolve()

    # Walk up the directory tree looking for _pyrite
    for parent in [current] + list(current.parents):
        if is_waft_project(parent):
            return True, parent

    return False, None


def validate_project_name(name: str) -> tuple[bool, str | None]:
    """
    Validate a project name.

    Args:
        name: Project name to validate

    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if name is valid
        - error_message: None if valid, error description if invalid
    """
    if not name:
        return False, "Project name cannot be empty"

    if len(name) > 100:
        return False, "Project name is too long (max 100 characters)"

    # Check for valid Python identifier (allowing hyphens and underscores)
    import re

    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_-]*$", name):
        return (
            False,
            "Project name must be a valid identifier (letters, numbers, hyphens, underscores only, starting with letter or underscore)",
        )

    # Reserved names
    reserved = [
        "con",
        "prn",
        "aux",
        "nul",
        "com1",
        "com2",
        "com3",
        "com4",
        "com5",
        "com6",
        "com7",
        "com8",
        "com9",
        "lpt1",
        "lpt2",
        "lpt3",
        "lpt4",
        "lpt5",
        "lpt6",
        "lpt7",
        "lpt8",
        "lpt9",
    ]
    if name.lower() in reserved:
        return False, f"Project name '{name}' is reserved"

    return True, None


def validate_package_name(package: str) -> tuple[bool, str | None]:
    """
    Validate a package name for dependency addition.

    Args:
        package: Package name (may include version specifier)

    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if package name is valid
        - error_message: None if valid, error description if invalid
    """
    if not package:
        return False, "Package name cannot be empty"

    # Extract package name (before version specifiers)
    import re

    match = re.match(r"^([a-zA-Z0-9_-]+(?:\[[^\]]+\])?)", package)
    if not match:
        return False, "Invalid package name format"

    package_name = match.group(1)

    # Basic validation
    if len(package_name) > 200:
        return False, "Package name is too long"

    return True, None


def validate_waft_project(project_path: Path) -> tuple[bool, str | None]:
    """
    Validate that a path is a Waft project.

    Args:
        project_path: Path to check

    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if valid Waft project
        - error_message: None if valid, error description if invalid
    """
    if not project_path.exists():
        return False, f"Path does not exist: {project_path}"

    if not project_path.is_dir():
        return False, f"Path is not a directory: {project_path}"

    pyrite_path = project_path / "_pyrite"
    if not pyrite_path.exists():
        return False, "Not a Waft project: _pyrite directory not found"

    pyproject_path = project_path / "pyproject.toml"
    if not pyproject_path.exists():
        return False, "Not a Python project: pyproject.toml not found"

    return True, None


def parse_toml_field(file_path: Path, field: str) -> str | None:
    """
    Parse a simple field from a TOML file using regex.

    This is a lightweight alternative to full TOML parsing for simple cases.
    For complex TOML, use a proper TOML library.

    Args:
        file_path: Path to TOML file
        field: Field name to extract (e.g., "name", "version")

    Returns:
        Field value as string, or None if not found
    """
    if not file_path.exists():
        return None

    try:
        content = file_path.read_text()
        import re

        # Pattern: field = "value" or field = 'value'
        pattern = rf'{field}\s*=\s*["\']([^"\']+)["\']'
        match = re.search(pattern, content)
        if match:
            return match.group(1)
        return None
    except Exception:
        return None


def safe_read_file(file_path: Path, default: str = "") -> str:
    """
    Safely read a file, returning default if it doesn't exist or can't be read.

    Args:
        file_path: Path to file
        default: Default value to return on error

    Returns:
        File contents as string, or default if error
    """
    try:
        if file_path.exists() and file_path.is_file():
            return file_path.read_text()
        return default
    except Exception:
        return default


def safe_write_file(file_path: Path, content: str, create_dirs: bool = True) -> bool:
    """
    Safely write a file, creating directories if needed.

    Args:
        file_path: Path to file
        content: Content to write
        create_dirs: If True, create parent directories

    Returns:
        True if successful, False otherwise
    """
    try:
        if create_dirs:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return True
    except Exception:
        return False


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted string (e.g., "1.5 KB", "3.2 MB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def format_relative_path(path: Path, base: Path) -> str:
    """
    Format a path relative to a base path.

    Args:
        path: Path to format
        base: Base path

    Returns:
        Relative path string, or absolute if not relative
    """
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path.resolve())


def ensure_directory(path: Path) -> None:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path
    """
    path.mkdir(parents=True, exist_ok=True)


def get_file_metadata(file_path: Path) -> dict:
    """
    Get metadata about a file.

    Args:
        file_path: Path to file

    Returns:
        Dictionary with metadata:
        - exists: bool
        - size: int (bytes)
        - extension: str
        - name: str
        - modified: float (timestamp) or None
    """

    metadata = {
        "exists": file_path.exists(),
        "size": 0,
        "extension": file_path.suffix,
        "name": file_path.name,
        "modified": None,
    }

    if file_path.exists() and file_path.is_file():
        stat = file_path.stat()
        metadata["size"] = stat.st_size
        metadata["modified"] = stat.st_mtime

    return metadata


def filter_files_by_extension(files: list[Path], extension: str) -> list[Path]:
    """
    Filter a list of files by extension.

    Args:
        files: List of file paths
        extension: Extension to filter by (with or without leading dot)

    Returns:
        Filtered list of files
    """
    ext = extension if extension.startswith(".") else f".{extension}"
    return [f for f in files if f.suffix == ext]


# Title Escaping Utilities
def escape_title_for_pdf(title: str, preserve_special: bool = True) -> str:
    """
    Escape title for HTML/PDF rendering.

    Escapes HTML special characters (< > & " ') while preserving
    special characters that should render as-is in PDFs.

    Args:
        title: Title string to escape
        preserve_special: If True, preserves special chars like /, -, _, etc.

    Returns:
        Properly escaped title safe for HTML/PDF rendering

    Examples:
        >>> escape_title_for_pdf("pantheon/ is central database")
        'pantheon/ is central database'

        >>> escape_title_for_pdf("X < Y & Z")
        'X &lt; Y &amp; Z'
    """
    if not title:
        return ""

    # HTML escape handles: < > & " '
    # This preserves: / - _ . : ( ) [ ] { } + = * ? ! @ # $ % ^ | \\ ~ `
    import html as html_module

    escaped = html_module.escape(title)

    return escaped


def escape_title_for_filename(title: str) -> str:
    """
    Escape title for use in filenames (safe filesystem characters only).

    Replaces problematic characters with safe alternatives.
    """
    if not title:
        return "untitled"

    # Replace filesystem-unsafe characters
    safe = title
    replacements = {
        "/": "_",
        "\\": "_",
        ":": "-",
        "*": "_",
        "?": "_",
        '"': "_",
        "<": "_",
        ">": "_",
        "|": "_",
    }

    for unsafe, safe_char in replacements.items():
        safe = safe.replace(unsafe, safe_char)

    # Remove leading/trailing spaces and dots (Windows issue)
    safe = safe.strip(" .")

    # Limit length for filesystem
    if len(safe) > 200:
        safe = safe[:200]

    return safe


def generate_headline_title(claim: str, verdict: str | None = None) -> str:
    """
    Generate headline-style title from claim.
    Target: ~7 words for gist, ~14 words total, most important info first.
    Properly handles special characters.
    """
    import re

    if not claim:
        return "Proof Case"

    # Clean up claim - remove markdown, extra whitespace
    claim = re.sub(r"\*\*|`|_", "", claim)  # Remove markdown formatting
    claim = re.sub(r"\s+", " ", claim).strip()  # Normalize whitespace

    # Remove common prefixes that don't add info
    claim = re.sub(r"^(?:The\s+|A\s+|An\s+)", "", claim, flags=re.IGNORECASE)

    # Extract key words - focus on the core assertion
    words = claim.split()

    # If already concise (14 words or less), use it
    if len(words) <= 14:
        title = claim
    else:
        # Extract key concepts: subject + verb + key outcome
        # Find subject (first noun phrase, usually 1-2 words)
        # Find verb and key outcome
        subject_end = 0
        verb_idx = -1
        for i, word in enumerate(words):
            if word.lower() in ["is", "are", "was", "were", "does", "has", "have"]:
                subject_end = i
                verb_idx = i
                break
            if i >= 3:  # Subject usually 1-3 words
                break

        # Get subject
        subject = words[:subject_end] if subject_end > 0 else words[:1]

        # Get verb and key outcome (after verb, up to 7 words total including subject + verb)
        if verb_idx >= 0:
            verb = [words[verb_idx]]
            outcome_start = verb_idx + 1
        else:
            verb = []
            outcome_start = len(subject)

        outcome_words = words[outcome_start:]

        # Build gist: subject + verb + key outcome (target 7 words)
        gist = subject + verb + outcome_words[: 7 - len(subject) - len(verb)]

        # If room, add more context (up to 14 words total)
        if len(gist) < 14:
            remaining = outcome_words[7 - len(subject) - len(verb) :]
            added = []
            for word in remaining:
                if word.lower() in ["and", "or", "but", "where", "when", "which", "that"]:
                    if len(gist) + len(added) < 12:
                        added.append(word)
                    break
                if any(punct in word for punct in [".", ",", ";", ":", "!", "?"]):
                    break
                if len(gist) + len(added) < 14:
                    added.append(word)
                else:
                    break
            title = " ".join(gist + added)
        else:
            title = " ".join(gist)

    # Add verdict if provided (short form, no repetition)
    if verdict:
        verdict_clean = re.sub(r"✅|❌|⚠️|\*\*", "", verdict).strip()
        verdict_short = verdict_clean.split()[0] if verdict_clean else ""
        if verdict_short and verdict_short not in title.upper():
            title = f"{title} ({verdict_short})"

    return title


def find_files_recursive(
    directory: Path, pattern: str = "*", exclude_dirs: list[str] | None = None
) -> list[Path]:
    """
    Find files recursively in a directory.

    Args:
        directory: Directory to search
        pattern: Glob pattern (default: "*")
        exclude_dirs: List of directory names to exclude (e.g., [".git", "__pycache__"])

    Returns:
        List of matching file paths
    """
    if not directory.exists():
        return []

    exclude_dirs = exclude_dirs or []
    files = []

    for item in directory.rglob(pattern):
        if item.is_file():
            # Check if any parent directory is excluded
            should_exclude = False
            for parent in item.parents:
                if parent.name in exclude_dirs:
                    should_exclude = True
                    break
            if not should_exclude:
                files.append(item)

    return files


# Title Escaping Utilities
def escape_title_for_pdf(title: str, preserve_special: bool = True) -> str:
    """
    Escape title for HTML/PDF rendering.

    Escapes HTML special characters (< > & " ') while preserving
    special characters that should render as-is in PDFs (/, -, _, etc.).

    Args:
        title: Title string to escape
        preserve_special: If True, preserves special chars like /, -, _, etc.
                         (always True - parameter for future use)

    Returns:
        Properly escaped title safe for HTML/PDF rendering

    Examples:
        >>> escape_title_for_pdf("pantheon/ is central database")
        'pantheon/ is central database'

        >>> escape_title_for_pdf("X < Y & Z")
        'X &lt; Y &amp; Z'

        >>> escape_title_for_pdf("File: /path/to/file.txt")
        'File: /path/to/file.txt'
    """
    if not title:
        return ""

    # HTML escape handles: < > & " '
    # This preserves: / - _ . : ( ) [ ] { } + = * ? ! @ # $ % ^ | \\ ~ `
    import html as html_module

    escaped = html_module.escape(title)

    return escaped


def escape_title_for_filename(title: str) -> str:
    """
    Escape title for use in filenames (safe filesystem characters only).

    Replaces problematic characters with safe alternatives:
    - / → _
    - \\ → _
    - : → -
    - * → _
    - ? → _
    - " → _
    - < → _
    - > → _
    - | → _

    Args:
        title: Title string to escape for filename

    Returns:
        Safe filename string

    Examples:
        >>> escape_title_for_filename("pantheon/ is central")
        'pantheon_ is central'

        >>> escape_title_for_filename("File: test.txt")
        'File- test.txt'
    """
    if not title:
        return "untitled"

    # Replace filesystem-unsafe characters
    safe = title
    replacements = {
        "/": "_",
        "\\": "_",
        ":": "-",
        "*": "_",
        "?": "_",
        '"': "_",
        "<": "_",
        ">": "_",
        "|": "_",
    }

    for unsafe, safe_char in replacements.items():
        safe = safe.replace(unsafe, safe_char)

    # Remove leading/trailing spaces and dots (Windows issue)
    safe = safe.strip(" .")

    # Limit length for filesystem
    if len(safe) > 200:
        safe = safe[:200]

    return safe


def generate_headline_title(claim: str, verdict: str | None = None) -> str:
    """
    Generate headline-style title from claim.
    Target: ~7 words for gist, ~14 words total, most important info first.
    Properly handles special characters.

    Args:
        claim: The claim statement
        verdict: Optional verdict (PROVEN/DISPROVEN/INCONCLUSIVE)

    Returns:
        Headline-style title (properly formatted, not yet escaped)

    Examples:
        >>> generate_headline_title("_pantheon/ is the central database")
        'pantheon/ is the central database'

        >>> generate_headline_title("X < Y", "PROVEN")
        'X < Y (PROVEN)'
    """
    import re

    if not claim:
        return "Proof Case"

    # Clean up claim - remove markdown, extra whitespace
    claim = re.sub(r"\*\*|`|_", "", claim)  # Remove markdown formatting
    claim = re.sub(r"\s+", " ", claim).strip()  # Normalize whitespace

    # Remove common prefixes that don't add info
    claim = re.sub(r"^(?:The\s+|A\s+|An\s+)", "", claim, flags=re.IGNORECASE)

    # Extract key words - focus on the core assertion
    words = claim.split()

    # If already concise (14 words or less), use it
    if len(words) <= 14:
        title = claim
    else:
        # Extract key concepts: subject + verb + key outcome
        # Find subject (first noun phrase, usually 1-2 words)
        # Find verb and key outcome
        subject_end = 0
        verb_idx = -1
        for i, word in enumerate(words):
            if word.lower() in ["is", "are", "was", "were", "does", "has", "have"]:
                subject_end = i
                verb_idx = i
                break
            if i >= 3:  # Subject usually 1-3 words
                break

        # Get subject
        subject = words[:subject_end] if subject_end > 0 else words[:1]

        # Get verb and key outcome (after verb, up to 7 words total including subject + verb)
        if verb_idx >= 0:
            verb = [words[verb_idx]]
            outcome_start = verb_idx + 1
        else:
            verb = []
            outcome_start = len(subject)

        outcome_words = words[outcome_start:]

        # Build gist: subject + verb + key outcome (target 7 words)
        gist = subject + verb + outcome_words[: 7 - len(subject) - len(verb)]

        # If room, add more context (up to 14 words total)
        if len(gist) < 14:
            remaining = outcome_words[7 - len(subject) - len(verb) :]
            added = []
            for word in remaining:
                if word.lower() in ["and", "or", "but", "where", "when", "which", "that"]:
                    if len(gist) + len(added) < 12:
                        added.append(word)
                    break
                if any(punct in word for punct in [".", ",", ";", ":", "!", "?"]):
                    break
                if len(gist) + len(added) < 14:
                    added.append(word)
                else:
                    break
            title = " ".join(gist + added)
        else:
            title = " ".join(gist)

    # Add verdict if provided (short form, no repetition)
    if verdict:
        verdict_clean = re.sub(r"✅|❌|⚠️|\*\*", "", verdict).strip()
        verdict_short = verdict_clean.split()[0] if verdict_clean else ""
        if verdict_short and verdict_short not in title.upper():
            title = f"{title} ({verdict_short})"

    return title


"""
Code Extraction Utilities for Case Files

Extracts code references from case files and creates a Code Examples section.
"""

import re
from collections import defaultdict
from pathlib import Path


def extract_code_references(case_content: str) -> dict[str, list[dict[str, any]]]:
    """
    Extract code references from case file content.

    Returns:
        Dictionary with:
        - 'inline_snippets': Short code snippets used inline
        - 'file_references': Files referenced with line numbers
        - 'code_blocks': Full code blocks that should be in examples
    """
    references = {"inline_snippets": [], "file_references": [], "code_blocks": []}

    # Pattern 1: File references with line numbers
    # Example: "**File**: `src/waft/pantheon/magistrate.py`  **Lines**: 199-201"
    file_pattern = r"\*\*File\*\*:\s*`([^`]+)`\s*\*\*Lines\*\*:\s*([0-9,\-\s]+)"

    for match in re.finditer(file_pattern, case_content):
        file_path = match.group(1)
        lines_str = match.group(2)

        # Parse line numbers
        line_numbers = []
        for part in lines_str.split(","):
            part = part.strip()
            if "-" in part:
                start, end = part.split("-")
                line_numbers.extend(range(int(start), int(end) + 1))
            else:
                line_numbers.append(int(part))

        references["file_references"].append(
            {"file": file_path, "lines": sorted(set(line_numbers)), "context": match.group(0)}
        )

    # Pattern 2: Code blocks with language
    # Example: ```python\ncode\n```
    code_block_pattern = r"```(\w+)?\n(.*?)```"

    for match in re.finditer(code_block_pattern, case_content, re.DOTALL):
        language = match.group(1) or "text"
        code = match.group(2).strip()

        # Skip very short snippets (already inline)
        if len(code.split("\n")) > 3:
            references["code_blocks"].append(
                {
                    "language": language,
                    "code": code,
                    "context": match.group(0)[:100],  # First 100 chars for context
                }
            )

    # Pattern 3: Inline code snippets (short)
    # Example: `self.pantheon_path = project_path / "_pantheon"`
    inline_pattern = r"`([^`\n]{10,100})`"

    for match in re.finditer(inline_pattern, case_content):
        snippet = match.group(1)
        # Only include if it looks like code (has operators, etc.)
        if any(
            op in snippet for op in ["=", "(", ")", ".", "/", ":", "->", "import", "def", "class"]
        ):
            references["inline_snippets"].append({"snippet": snippet, "context": match.group(0)})

    return references


def read_code_from_file(file_path: Path, lines: list[int], context_lines: int = 2) -> str | None:
    """
    Read code from a file at specified line numbers with context.

    Args:
        file_path: Path to source file
        lines: List of line numbers to extract
        context_lines: Number of context lines before/after

    Returns:
        Code snippet with line numbers, or None if file doesn't exist
    """
    if not file_path.exists():
        return None

    try:
        content = file_path.read_text(encoding="utf-8")
        content_lines = content.split("\n")

        # Get range of lines to extract
        min_line = max(0, min(lines) - context_lines - 1)
        max_line = min(len(content_lines), max(lines) + context_lines)

        # Extract code
        extracted_lines = content_lines[min_line:max_line]

        # Build code with line numbers
        code_parts = []
        for i, line in enumerate(extracted_lines, start=min_line + 1):
            marker = ">>>" if i in lines else "   "
            code_parts.append(f"{marker} {i:4d} | {line}")

        return "\n".join(code_parts)
    except Exception:
        return None


def build_code_examples_section(
    case_content: str, project_path: Path, max_examples: int = 20
) -> str:
    """
    Build a Code Examples section for a case file.

    Args:
        case_content: The case file content
        project_path: Project root path
        max_examples: Maximum number of examples to include

    Returns:
        Markdown section with code examples
    """
    references = extract_code_references(case_content)

    if not any(references.values()):
        return ""

    section = []
    section.append("## CODE EXAMPLES")
    section.append("")
    section.append("This section contains the actual code referenced in the case file above.")
    section.append(
        "Code snippets in the document reference these examples (e.g., 'See Example 1')."
    )
    section.append("")
    section.append("---")
    section.append("")

    example_num = 1

    # Group file references by file
    files_by_path = defaultdict(list)
    for ref in references["file_references"]:
        files_by_path[ref["file"]].extend(ref["lines"])

    # Add file-based examples
    for file_path_str, all_lines in list(files_by_path.items())[:max_examples]:
        # Resolve file path
        if Path(file_path_str).is_absolute():
            file_path = Path(file_path_str)
        else:
            file_path = project_path / file_path_str

        if not file_path.exists():
            continue

        # Get unique sorted lines
        unique_lines = sorted(set(all_lines))

        # Read code
        code = read_code_from_file(file_path, unique_lines)
        if not code:
            continue

        # Determine language from extension
        ext = file_path.suffix
        language_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".jsx": "jsx",
            ".tsx": "tsx",
            ".css": "css",
            ".html": "html",
            ".md": "markdown",
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".toml": "toml",
            ".sh": "bash",
            ".sql": "sql",
        }
        language = language_map.get(ext, "text")

        section.append(f"### Example {example_num}: {file_path_str}")
        section.append("")
        section.append(f"**File**: `{file_path_str}`")
        section.append(
            f"**Lines**: {', '.join(map(str, unique_lines[:10]))}{'...' if len(unique_lines) > 10 else ''}"
        )
        section.append("")
        section.append("```" + language)
        section.append(code)
        section.append("```")
        section.append("")
        section.append("---")
        section.append("")

        example_num += 1
        if example_num > max_examples:
            break

    # Add code blocks from case content
    for code_block in references["code_blocks"][: max_examples - example_num + 1]:
        section.append(f"### Example {example_num}: Code Block")
        section.append("")
        section.append(f"**Language**: {code_block['language']}")
        section.append("")
        section.append("```" + code_block["language"])
        section.append(code_block["code"])
        section.append("```")
        section.append("")
        section.append("---")
        section.append("")

        example_num += 1
        if example_num > max_examples:
            break

    if example_num == 1:
        return ""  # No examples found

    section.append("")
    section.append("*End of Code Examples*")
    section.append("")

    return "\n".join(section)


def add_code_examples_to_case_file(case_file_path: Path, project_path: Path) -> bool:
    """
    Add Code Examples section to an existing case file.

    Args:
        case_file_path: Path to case file
        project_path: Project root path

    Returns:
        True if examples were added, False otherwise
    """
    if not case_file_path.exists():
        return False

    content = case_file_path.read_text(encoding="utf-8")

    # Check if Code Examples section already exists
    if "## CODE EXAMPLES" in content or "## Code Examples" in content:
        return False  # Already has examples

    # Build examples section
    examples_section = build_code_examples_section(content, project_path)

    if not examples_section:
        return False  # No code references found

    # Add before the final line or at the end
    # Look for common ending patterns
    ending_patterns = [
        r"\*This case file was automatically generated",
        r"## Conclusion",
        r"## CONCLUSION",
        r"\*\*Case Status\*\*",
    ]

    insert_position = len(content)
    for pattern in ending_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            insert_position = match.start()
            break

    # Insert examples section
    new_content = (
        content[:insert_position].rstrip()
        + "\n\n"
        + examples_section
        + "\n\n"
        + content[insert_position:].lstrip()
    )

    case_file_path.write_text(new_content, encoding="utf-8")
    return True


# ============================================================================
# External Drive Storage System
# ============================================================================

# Logger for storage operations
_storage_logger = logging.getLogger(__name__)


def _validate_project_name(project_name: str) -> bool:
    """
    CRITICAL: Security validation for project_name.

    Validates project_name is safe for filesystem use.

    Args:
        project_name: Project name to validate

    Returns:
        True if valid, False otherwise
    """
    if not project_name:
        return False

    # Length limit (255 characters for filesystem compatibility)
    if len(project_name) > 255:
        return False

    # Reject path traversal and dangerous characters
    if any(c in project_name for c in ["..", "/", "\\", "\x00"]):
        return False

    # Reject control characters (except tab, newline, carriage return)
    if any(ord(c) < 32 and c not in ["\t", "\n", "\r"] for c in project_name):
        return False

    # Allow only: alphanumeric + underscore + hyphen
    if not project_name.replace("_", "").replace("-", "").isalnum():
        return False

    return True


def classify_content_type(path: Path) -> str:
    """
    Classify content type as 'core' or 'augmented'.

    Args:
        path: Path to classify

    Returns:
        'core' or 'augmented'
    """
    path_str = str(path).replace("\\", "/")  # Normalize path separators

    # Core content patterns (stays local)
    core_patterns = [
        "src/",
        "pyproject.toml",
        "uv.lock",
        ".cursor/",
        ".empirica/",
        "_pyrite/active/",
        "_pyrite/standards/",
        # Note: _work_efforts/ is augmented (PDFs go to external drive)
    ]

    # Check if path matches core patterns
    for pattern in core_patterns:
        if pattern in path_str:
            return "core"

    # Augmented content patterns (routes to external drive)
    augmented_patterns = [
        "_experiments/",
        "_genetics/",
        "_science/",
        "_science_textbook/",
        "_archive/",
        "_epic_run/",
        "_notebook/",
        "_pantheon/",
        "_probe_data/",
        "_temp_",
        "NARRATIVE-WAFT/",
        "experiments/",
        "scientific_method_tool/",
        "WAFT-",
        "-Research/",
        "demo_output/",
        "advanced_demo_output/",
        "session_recaps/",  # PDF outputs in _work_efforts
        "evolved/",  # Evolved PDFs in _pyrite
        "oracle/",  # Oracle insights PDFs
        "_work_efforts/",  # Work efforts (augmented - contains PDFs, experiments, etc.)
    ]

    # Check for PDF files specifically (always augmented)
    if path_str.endswith(".pdf"):
        # Check if it's in a core directory that should stay local
        if any(core in path_str for core in ["src/", "pyproject.toml", ".cursor/", ".empirica/"]):
            return "core"
        # All other PDFs are augmented
        return "augmented"

    # Check if path matches augmented patterns
    for pattern in augmented_patterns:
        if pattern in path_str:
            return "augmented"

    # Default to local (safe fallback)
    return "core"


def is_augmented_content(path: Path) -> bool:
    """
    Convenience function to check if content should go to external drive.

    Args:
        path: Path to check

    Returns:
        True if content should go to external drive
    """
    return classify_content_type(path) == "augmented"


def detect_external_drive(drive_name: str = "Easystore") -> Path | None:
    """
    Detect external drive and validate it's available and writable.

    Args:
        drive_name: Name of the external drive (default: "Easystore")

    Returns:
        Path to external drive if available and writable, None otherwise
    """
    drive_path = Path(f"/Volumes/{drive_name}")

    # Check if drive exists
    if not drive_path.exists():
        _storage_logger.debug(f"External drive not found: {drive_path}")
        return None

    # Check if it's a directory
    if not drive_path.is_dir():
        _storage_logger.warning(f"External drive path is not a directory: {drive_path}")
        return None

    # Check if it's writable
    if not os.access(drive_path, os.W_OK):
        _storage_logger.warning(f"External drive is not writable: {drive_path}")
        return None

    # Check if it's readable
    if not os.access(drive_path, os.R_OK):
        _storage_logger.warning(f"External drive is not readable: {drive_path}")
        return None

    # Check for symlinks (security)
    try:
        if drive_path.is_symlink():
            _storage_logger.warning(
                f"External drive path is a symlink (security risk): {drive_path}"
            )
            return None
    except (OSError, ValueError):
        pass  # Some systems don't support is_symlink()

    return drive_path


def get_external_drive_base(project_name: str | None = None) -> Path | None:
    """
    Get base path on external drive for project storage.

    CRITICAL: Validates project_name and resolved path for security.

    Args:
        project_name: Project name (auto-detected from current directory if None)

    Returns:
        Base path on external drive, or None if drive not available

    Raises:
        ValueError: If project_name is invalid
    """
    # Detect external drive
    drive_path = detect_external_drive()
    if not drive_path:
        return None

    # Auto-detect project name if not provided
    if project_name is None:
        project_name = Path.cwd().name
        if not project_name or project_name == ".":
            project_name = "waft"

    # CRITICAL: Validate project_name
    if not _validate_project_name(project_name):
        raise ValueError(f"Invalid project_name: {project_name} (contains unsafe characters)")

    # Build base path
    base_path = drive_path / "waft" / project_name

    # CRITICAL: Validate resolved path is within /Volumes/Easystore/waft/
    try:
        resolved = base_path.resolve()
        expected_base = (drive_path / "waft").resolve()

        # Check path is within expected base
        if not str(resolved).startswith(str(expected_base)):
            raise ValueError(f"Path traversal detected: {resolved} not within {expected_base}")

        # CRITICAL: Check for symlinks before creating
        if resolved.is_symlink():
            raise ValueError(f"Symlink detected in path: {resolved}")

        # Create directory structure if it doesn't exist
        resolved.mkdir(parents=True, exist_ok=True)

        # CRITICAL: Set directory permissions (0o700)
        try:
            resolved.chmod(0o700)
            # Also set parent directories
            for parent in resolved.parents:
                if parent.exists() and str(parent).startswith(str(drive_path)):
                    try:
                        parent.chmod(0o700)
                    except (OSError, PermissionError):
                        pass  # Ignore if permissions can't be set
        except (OSError, PermissionError):
            _storage_logger.warning(f"Could not set permissions on {resolved}")

        return resolved
    except (OSError, ValueError) as e:
        _storage_logger.error(f"Error creating external drive base path: {e}")
        return None


def _validate_path_in_storage(relative_path: Path, base_path: Path) -> bool:
    """
    CRITICAL: Security validation for paths in storage.

    Validates path is within storage base directory.

    Args:
        relative_path: Relative path to validate
        base_path: Base storage path

    Returns:
        True if valid, False otherwise
    """
    try:
        # Reject absolute paths
        if relative_path.is_absolute():
            return False

        # Reject path traversal
        if ".." in relative_path.parts:
            return False

        # Reject null bytes
        if "\x00" in str(relative_path):
            return False

        # Resolve and check
        resolved = (base_path / relative_path).resolve()
        base_resolved = base_path.resolve()

        # Check path is within base
        if not str(resolved).startswith(str(base_resolved)):
            return False

        # Check for symlinks in path components
        current = base_path
        for part in relative_path.parts:
            current = current / part
            if current.exists() and current.is_symlink():
                return False

        return True
    except (OSError, ValueError):
        return False


def get_storage_path(
    relative_path: Path,
    project_path: Path | None = None,
    content_type: str | None = None,
    realm_name: str | None = None,
) -> Path:
    """
    Primary storage path resolver.

    Routes content based on type:
    - Core content → local project
    - Augmented content → external drive (if available)
    - If realm_name provided, routes to External Drive Realm structure

    CRITICAL: Validates paths and sets permissions for security.

    Args:
        relative_path: Relative path from project root
        project_path: Project root path (default: current directory)
        content_type: Content type ('core' or 'augmented'), auto-detected if None
        realm_name: Optional realm name for realm-based routing (e.g., "Universe", "Earth")

    Returns:
        Resolved absolute path where content should be stored

    Raises:
        ValueError: If path validation fails
    """
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)

    # Classify content if not provided
    if content_type is None:
        content_type = classify_content_type(relative_path)

    # Route based on content type
    if content_type == "core":
        # Core content stays local
        output_path = project_path / relative_path
    else:
        # Augmented content routes to external drive
        # If realm_name provided, use External Drive Realm Entity
        if realm_name:
            try:
                from .pantheon.external_drive_realm import ExternalDriveRealm

                realm = ExternalDriveRealm(project_path)
                realm_storage = realm.route_content_to_realm(
                    content_path=relative_path,
                    realm_name=realm_name,
                    project_name=project_path.name,
                )
                if realm_storage:
                    output_path = realm_storage
                    _storage_logger.info(
                        f"Routing augmented content to realm '{realm_name}': {output_path}"
                    )
                else:
                    # Fallback to standard routing
                    external_base = get_external_drive_base()
                    if external_base:
                        if not _validate_path_in_storage(relative_path, external_base):
                            _storage_logger.warning(
                                f"Path validation failed for {relative_path}, falling back to local"
                            )
                            output_path = project_path / relative_path
                        else:
                            output_path = external_base / relative_path
                            _storage_logger.info(
                                f"Routing augmented content to external drive: {output_path}"
                            )
                    else:
                        _storage_logger.warning(
                            f"External drive not available, storing augmented content locally: {relative_path}"
                        )
                        output_path = project_path / relative_path
            except Exception as e:
                _storage_logger.warning(
                    f"Realm routing failed: {e}, falling back to standard routing"
                )
                # Fallback to standard routing
                external_base = get_external_drive_base()
                if external_base:
                    if not _validate_path_in_storage(relative_path, external_base):
                        _storage_logger.warning(
                            f"Path validation failed for {relative_path}, falling back to local"
                        )
                        output_path = project_path / relative_path
                    else:
                        output_path = external_base / relative_path
                        _storage_logger.info(
                            f"Routing augmented content to external drive: {output_path}"
                        )
                else:
                    _storage_logger.warning(
                        f"External drive not available, storing augmented content locally: {relative_path}"
                    )
                    output_path = project_path / relative_path
        else:
            # Standard routing (no realm)
            external_base = get_external_drive_base()
            if external_base:
                # CRITICAL: Validate path before use
                if not _validate_path_in_storage(relative_path, external_base):
                    _storage_logger.warning(
                        f"Path validation failed for {relative_path}, falling back to local"
                    )
                    output_path = project_path / relative_path
                else:
                    output_path = external_base / relative_path
                    _storage_logger.info(
                        f"Routing augmented content to external drive: {output_path}"
                    )
            else:
                # Fallback to local with warning
                _storage_logger.warning(
                    f"External drive not available, storing augmented content locally: {relative_path}"
                )
                output_path = project_path / relative_path

    # Create directory structure
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # CRITICAL: Set directory permissions (0o700)
        try:
            output_path.parent.chmod(0o700)
        except (OSError, PermissionError):
            pass  # Ignore on Windows or if permissions can't be set
    except (OSError, PermissionError) as e:
        _storage_logger.error(f"Error creating directory structure: {e}")
        raise

    # Check available disk space (basic check)
    try:
        stat = shutil.disk_usage(output_path.parent)
        if stat.free < 1024 * 1024:  # Less than 1MB free
            _storage_logger.warning(f"Low disk space on {output_path.parent}")
    except (OSError, ValueError):
        pass  # Ignore if disk space check fails

    return output_path.resolve()


def track_pdf_move(old_path: Path, new_path: Path, project_path: Path | None = None) -> None:
    """
    Track a PDF file move/rename operation in the storage registry.

    Use this when moving or renaming PDF files to maintain traceability.

    Args:
        old_path: Old path (relative or absolute)
        new_path: New path (relative or absolute)
        project_path: Project root path (default: current directory)
    """
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)

    # Convert to relative paths
    try:
        if old_path.is_absolute():
            old_rel = old_path.relative_to(project_path)
        else:
            old_rel = old_path

        if new_path.is_absolute():
            new_rel = new_path.relative_to(project_path)
        else:
            new_rel = new_path
    except ValueError:
        # Paths outside project, skip tracking
        return

    # Register the move
    registry = StorageRegistry(project_path)
    registry.track_move(str(old_rel), str(new_rel))


def find_pdf_location(pdf_path: str, project_path: Path | None = None) -> str | None:
    """
    Find the current location of a PDF file.

    Convenience function to trace PDF locations.

    Args:
        pdf_path: Relative path to PDF or filename
        project_path: Project root path (default: current directory)

    Returns:
        Current absolute path where PDF is stored, or None if not found

    Example:
        >>> find_pdf_location("session_recap_20260115.pdf")
        '/Volumes/Easystore/waft/active-waft/_work_efforts/session_recaps/session_recap_20260115.pdf'
    """
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)

    registry = StorageRegistry(project_path)
    return registry.get_pdf_location(pdf_path)


def trace_pdf(pdf_path: str, project_path: Path | None = None) -> dict[str, Any]:
    """
    Get full trace information for a PDF file.

    Shows current location, history of moves, and all locations it's been at.

    Args:
        pdf_path: Relative path to PDF or filename
        project_path: Project root path (default: current directory)

    Returns:
        Dictionary with trace information:
        - found: bool
        - current_location: str
        - content_type: str
        - history: list of operations
        - all_locations: list of all locations
        - move_count: int

    Example:
        >>> trace = trace_pdf("session_recap_20260115.pdf")
        >>> print(trace['current_location'])
        '/Volumes/Easystore/waft/active-waft/_work_efforts/session_recaps/...'
        >>> print(trace['history'])
        [{'operation': 'created', 'location': '...', 'timestamp': '...'}, ...]
    """
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)

    registry = StorageRegistry(project_path)
    return registry.trace_pdf(pdf_path)


def resolve_output_path(output_path: Path, project_path: Path | None = None) -> Path:
    """
    Convenience wrapper for get_storage_path().

    Handles both relative and absolute paths.
    Maintains backward compatibility.

    CRITICAL: Validates paths before resolution.

    Args:
        output_path: Output path (relative or absolute)
        project_path: Project root path (default: current directory)

    Returns:
        Resolved absolute path where content should be stored
    """
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)

    # If absolute path, check if it's within project
    if output_path.is_absolute():
        try:
            resolved = output_path.resolve()
            project_resolved = project_path.resolve()
            if str(resolved).startswith(str(project_resolved)):
                # It's within project, make it relative
                relative = resolved.relative_to(project_resolved)
                return get_storage_path(relative, project_path)
            else:
                # It's outside project, use as-is (but log warning)
                _storage_logger.warning(f"Absolute path outside project: {output_path}")
                return resolved
        except (ValueError, OSError):
            # Can't resolve, use as-is
            return output_path

    # Relative path - use get_storage_path
    return get_storage_path(output_path, project_path)


class StorageRegistry:
    """
    Storage registry to track where content is stored.

    Maintains manifest of storage locations for system awareness.
    Tracks file movements, locations, and provides tracing capabilities.
    """

    def __init__(self, project_path: Path | None = None):
        """
        Initialize storage registry.

        Args:
            project_path: Project root path (default: current directory)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)

        self.project_path = project_path
        self.registry_file = project_path / "_pyrite" / ".storage_registry.json"
        self.audit_log_file = project_path / "_pyrite" / ".storage_audit_log.jsonl"
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)

        # CRITICAL: Set directory permissions (0o700)
        try:
            self.registry_file.parent.chmod(0o700)
        except (OSError, PermissionError):
            pass

        # File lock for concurrent access
        self._lock = Lock()

        # Load registry
        self.registry = self._load_registry()

    def _load_registry(self) -> dict[str, Any]:
        """Load registry from file."""
        if not self.registry_file.exists():
            return {}

        try:
            with open(self.registry_file) as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            _storage_logger.warning(f"Error loading registry: {e}, starting with empty registry")
            return {}

    def _save_registry(self) -> bool:
        """
        Save registry to file.

        CRITICAL: Uses file locking and sets permissions.
        """
        with self._lock:
            try:
                # Write to temp file first (atomic write)
                temp_file = self.registry_file.with_suffix(".tmp")
                with open(temp_file, "w") as f:
                    json.dump(self.registry, f, indent=2)

                # CRITICAL: Set file permissions (0o600)
                try:
                    temp_file.chmod(0o600)
                except (OSError, PermissionError):
                    pass

                # Atomic rename
                temp_file.replace(self.registry_file)

                # CRITICAL: Set file permissions on final file
                try:
                    self.registry_file.chmod(0o600)
                except (OSError, PermissionError):
                    pass

                return True
            except OSError as e:
                _storage_logger.error(f"Error saving registry: {e}")
                return False

    def query_audit_log(
        self,
        content_path: str | None = None,
        operation: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """
        Query audit log for file operations.

        Args:
            content_path: Filter by content path (partial match)
            operation: Filter by operation type
            date_from: Filter by date (ISO format, inclusive)
            date_to: Filter by date (ISO format, inclusive)
            limit: Maximum number of results

        Returns:
            List of audit log entries
        """
        if not self.audit_log_file.exists():
            return []

        results = []
        try:
            with open(self.audit_log_file) as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        entry = json.loads(line)

                        # Apply filters
                        if content_path and content_path not in entry.get("content_path", ""):
                            continue
                        if operation and entry.get("operation") != operation:
                            continue
                        if date_from and entry.get("timestamp", "") < date_from:
                            continue
                        if date_to and entry.get("timestamp", "") > date_to:
                            continue

                        results.append(entry)
                        if len(results) >= limit:
                            break
                    except json.JSONDecodeError:
                        continue

            # Return most recent first
            return list(reversed(results))
        except OSError as e:
            _storage_logger.warning(f"Error reading audit log: {e}")
            return []

    def register(
        self,
        content_path: str,
        storage_location: str,
        content_type: str,
        operation: str = "created",
    ) -> None:
        """
        Register content in storage registry.

        Args:
            content_path: Relative path to content
            storage_location: Where content is stored (absolute path)
            content_type: Content type ('core' or 'augmented')
            operation: Operation type ('created', 'moved', 'updated')
        """
        timestamp = datetime.now().isoformat()

        # Check if this is an update to existing entry
        existing = self.registry.get(content_path)
        if existing:
            # Track movement if location changed
            if existing.get("storage_location") != storage_location:
                self._log_audit(
                    content_path=content_path,
                    operation="moved",
                    old_location=existing.get("storage_location"),
                    new_location=storage_location,
                    content_type=content_type,
                )
                operation = "moved"
            else:
                operation = "updated"
        else:
            # New file
            self._log_audit(
                content_path=content_path,
                operation="created",
                location=storage_location,
                content_type=content_type,
            )

        # Update registry
        self.registry[content_path] = {
            "storage_location": storage_location,
            "content_type": content_type,
            "timestamp": timestamp,
            "last_operation": operation,
            "history": existing.get("history", []) if existing else [],
        }

        # Add to history
        self.registry[content_path]["history"].append(
            {"operation": operation, "location": storage_location, "timestamp": timestamp}
        )

        # Keep history limited (last 50 entries)
        if len(self.registry[content_path]["history"]) > 50:
            self.registry[content_path]["history"] = self.registry[content_path]["history"][-50:]

        self._save_registry()

    def find_content(self, content_path: str) -> dict[str, Any] | None:
        """
        Find content in registry.

        Args:
            content_path: Relative path to content

        Returns:
            Registry entry or None if not found
        """
        return self.registry.get(content_path)

    def list_external_content(self) -> list[dict[str, Any]]:
        """
        List all content stored on external drive.

        Returns:
            List of registry entries for external content
        """
        return [
            {"content_path": path, **info}
            for path, info in self.registry.items()
            if info.get("content_type") == "augmented"
        ]

    def _log_audit(
        self,
        content_path: str,
        operation: str,
        location: str | None = None,
        old_location: str | None = None,
        new_location: str | None = None,
        content_type: str | None = None,
    ) -> None:
        """
        Log audit entry for file operations.

        Args:
            content_path: Relative path to content
            operation: Operation type ('created', 'moved', 'deleted', 'updated')
            location: Current location (for created/updated)
            old_location: Previous location (for moved)
            new_location: New location (for moved)
            content_type: Content type
        """
        try:
            audit_entry = {
                "timestamp": datetime.now().isoformat(),
                "content_path": content_path,
                "operation": operation,
                "content_type": content_type,
            }

            if operation == "moved":
                audit_entry["old_location"] = old_location
                audit_entry["new_location"] = new_location
            else:
                audit_entry["location"] = location

            # Append to audit log (JSONL format)
            with self._lock:
                with open(self.audit_log_file, "a") as f:
                    f.write(json.dumps(audit_entry) + "\n")
        except Exception as e:
            _storage_logger.warning(f"Failed to log audit entry: {e}")

    def trace_pdf(self, pdf_path: str) -> dict[str, Any]:
        """
        Trace a PDF file - find its current location and full history.

        Args:
            pdf_path: Relative path to PDF or filename

        Returns:
            Dictionary with trace information:
            - found: bool
            - current_location: str (if found)
            - content_type: str
            - history: list of operations
            - all_locations: list of all locations it's been at
        """
        # Try exact match first
        entry = self.registry.get(pdf_path)

        # If not found, try searching by filename
        if not entry:
            pdf_name = Path(pdf_path).name
            for path, info in self.registry.items():
                if Path(path).name == pdf_name and Path(path).suffix == ".pdf":
                    entry = info
                    pdf_path = path
                    break

        if not entry:
            return {"found": False, "pdf_path": pdf_path, "message": "PDF not found in registry"}

        # Get all unique locations from history
        all_locations = set()
        all_locations.add(entry.get("storage_location"))
        for hist_entry in entry.get("history", []):
            if "location" in hist_entry:
                all_locations.add(hist_entry["location"])
            if "new_location" in hist_entry:
                all_locations.add(hist_entry["new_location"])
            if "old_location" in hist_entry:
                all_locations.add(hist_entry["old_location"])

        return {
            "found": True,
            "pdf_path": pdf_path,
            "current_location": entry.get("storage_location"),
            "content_type": entry.get("content_type"),
            "last_operation": entry.get("last_operation"),
            "created_at": entry.get("timestamp"),
            "history": entry.get("history", []),
            "all_locations": sorted(all_locations),
            "move_count": sum(1 for h in entry.get("history", []) if h.get("operation") == "moved"),
        }

    def find_pdfs(
        self,
        pattern: str | None = None,
        content_type: str | None = None,
        location: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """
        Find PDFs matching criteria.

        Args:
            pattern: Filename pattern to search (e.g., "session_recap", "*.pdf")
            content_type: Filter by content type ('core' or 'augmented')
            location: Filter by storage location (partial match)
            date_from: Filter by date (ISO format, inclusive)
            date_to: Filter by date (ISO format, inclusive)
            limit: Maximum number of results to return

        Returns:
            List of matching PDF entries with trace information
        """
        results = []

        for content_path, info in self.registry.items():
            # Only PDFs
            if not content_path.endswith(".pdf"):
                continue

            # Filter by pattern
            if pattern:
                if pattern not in content_path and pattern not in Path(content_path).name:
                    continue

            # Filter by content type
            if content_type and info.get("content_type") != content_type:
                continue

            # Filter by location
            if location and location not in info.get("storage_location", ""):
                continue

            # Filter by date
            if date_from or date_to:
                file_date = info.get("timestamp", "")
                if date_from and file_date < date_from:
                    continue
                if date_to and file_date > date_to:
                    continue

            # Get trace info
            trace = self.trace_pdf(content_path)
            results.append(trace)

            # Apply limit
            if len(results) >= limit:
                break

        return results

    def get_pdf_location(self, pdf_path: str) -> str | None:
        """
        Get current location of a PDF.

        Args:
            pdf_path: Relative path to PDF or filename

        Returns:
            Current absolute path where PDF is stored, or None if not found
        """
        trace = self.trace_pdf(pdf_path)
        if trace.get("found"):
            return trace.get("current_location")
        return None

    def track_move(self, old_path: str, new_path: str, content_type: str | None = None) -> None:
        """
        Track a file move/rename operation.

        Args:
            old_path: Old relative path
            new_path: New relative path
            content_type: Content type (auto-detected if None)
        """
        # Find old entry
        old_entry = self.registry.get(old_path)
        if not old_entry:
            # Try to find by filename
            old_name = Path(old_path).name
            for path, info in list(self.registry.items()):
                if Path(path).name == old_name:
                    old_path = path
                    old_entry = info
                    break

        if old_entry:
            old_location = old_entry.get("storage_location")

            # Determine new location
            if content_type is None:
                content_type = classify_content_type(Path(new_path))

            # Resolve new storage location
            new_storage = get_storage_path(Path(new_path), self.project_path, content_type)
            new_location = str(new_storage)

            # Update registry
            self.register(
                content_path=new_path,
                storage_location=new_location,
                content_type=content_type,
                operation="moved",
            )

            # Remove old entry
            if old_path != new_path:
                del self.registry[old_path]
                self._save_registry()

            # Log audit
            self._log_audit(
                content_path=new_path,
                operation="moved",
                old_location=old_location,
                new_location=new_location,
                content_type=content_type,
            )

    def get_storage_stats(self) -> dict[str, Any]:
        """
        Get storage statistics.

        Returns:
            Dictionary with storage statistics
        """
        total = len(self.registry)
        pdfs = sum(1 for path in self.registry.keys() if path.endswith(".pdf"))
        core = sum(1 for info in self.registry.values() if info.get("content_type") == "core")
        augmented = sum(
            1 for info in self.registry.values() if info.get("content_type") == "augmented"
        )

        # Count PDFs by location
        external_pdfs = 0
        local_pdfs = 0
        for path, info in self.registry.items():
            if path.endswith(".pdf"):
                location = info.get("storage_location", "")
                if "/Volumes/" in location:
                    external_pdfs += 1
                else:
                    local_pdfs += 1

        return {
            "total_content": total,
            "total_pdfs": pdfs,
            "core_content": core,
            "augmented_content": augmented,
            "pdfs_on_external": external_pdfs,
            "pdfs_local": local_pdfs,
            "external_drive_available": detect_external_drive() is not None,
        }


# ============================================================================
# PDF Blank Page Handler
# ============================================================================

try:
    import fitz  # PyMuPDF

    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    from weasyprint import HTML

    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

from pypdf import PdfReader, PdfWriter


def is_page_blank(page) -> bool:
    """
    Check if a PDF page is blank (has no meaningful content).

    Args:
        page: pypdf Page object

    Returns:
        True if page is blank, False otherwise
    """
    try:
        text = page.extract_text().strip()
        # Consider page blank if it has less than 10 characters of text
        # (allowing for headers/footers that might be on every page)
        return len(text) < 10
    except Exception:
        # If extraction fails, assume not blank (safer)
        return False


def add_blank_page_marker(
    pdf_path: Path,
    output_path: Path | None = None,
    marker_text: str = "[ THIS PAGE IS BLANK ON PURPOSE ]",
) -> Path:
    """
    Add blank page markers to all blank pages in a PDF.

    Args:
        pdf_path: Path to input PDF
        output_path: Path to output PDF (default: overwrites input)
        marker_text: Text to display on blank pages

    Returns:
        Path to output PDF
    """
    if output_path is None:
        output_path = pdf_path

    reader = PdfReader(str(pdf_path))

    # Check if we have any blank pages
    blank_pages = []
    for page_num, page in enumerate(reader.pages):
        if is_page_blank(page):
            blank_pages.append(page_num)

    if not blank_pages:
        # No blank pages, return as-is
        return output_path

    # Use PyMuPDF if available (best option)
    if PYMUPDF_AVAILABLE:
        doc = fitz.open(str(pdf_path))

        for page_num in blank_pages:
            page = doc[page_num]
            page_rect = page.rect

            # Insert text centered
            page.insert_text(
                page_rect.center,  # Center point (x, y tuple)
                marker_text,
                fontsize=12,
                color=(0.5, 0.5, 0.5),  # Gray color
                align=1,  # Center alignment
            )

        # Save updated PDF
        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(str(output_path))
        doc.close()
        return output_path

    # Fallback: Use WeasyPrint to create overlay pages
    if WEASYPRINT_AVAILABLE:
        writer = PdfWriter()

        # Create overlay HTML for blank page marker
        overlay_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                @page {{
                    size: letter;
                    margin: 0;
                }}
                body {{
                    margin: 0;
                    padding: 0;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    font-family: Helvetica, Arial, sans-serif;
                    font-size: 12pt;
                    color: #808080;
                }}
            </style>
        </head>
        <body>
            {marker_text}
        </body>
        </html>
        """

        # Generate overlay PDF
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            overlay_path = Path(tmp.name)
            HTML(string=overlay_html).write_pdf(overlay_path)
            overlay_reader = PdfReader(str(overlay_path))
            overlay_page = overlay_reader.pages[0]
            overlay_path.unlink()  # Clean up temp file

        # Process all pages
        for page_num, page in enumerate(reader.pages):
            if page_num in blank_pages:
                # Merge overlay onto blank page
                page.merge_page(overlay_page)
            writer.add_page(page)

        # Write output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as output_file:
            writer.write(output_file)

        return output_path

    # Final fallback: Graceful degradation
    print("⚠️  Neither PyMuPDF nor WeasyPrint available - blank page markers skipped")
    return output_path


def process_pdf_for_blank_pages(pdf_path: Path) -> Path:
    """
    Process PDF to add blank page markers (convenience function).

    Args:
        pdf_path: Path to PDF file

    Returns:
        Path to processed PDF (same file, updated in place)
    """
    return add_blank_page_marker(pdf_path, output_path=pdf_path)
