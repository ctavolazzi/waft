"""
Utility functions - Helper functions for common operations.

These "little guys" help with repetitive tasks like path resolution,
file operations, formatting, and validation.
"""

from pathlib import Path
from typing import Optional


def resolve_project_path(path: Optional[str] = None) -> Path:
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


def is_inside_waft_project(path: Path) -> tuple[bool, Optional[Path]]:
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


def validate_project_name(name: str) -> tuple[bool, Optional[str]]:
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
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_-]*$', name):
        return False, "Project name must be a valid identifier (letters, numbers, hyphens, underscores only, starting with letter or underscore)"

    # Reserved names
    reserved = ['con', 'prn', 'aux', 'nul', 'com1', 'com2', 'com3', 'com4', 'com5', 'com6', 'com7', 'com8', 'com9', 'lpt1', 'lpt2', 'lpt3', 'lpt4', 'lpt5', 'lpt6', 'lpt7', 'lpt8', 'lpt9']
    if name.lower() in reserved:
        return False, f"Project name '{name}' is reserved"

    return True, None


def validate_package_name(package: str) -> tuple[bool, Optional[str]]:
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
    match = re.match(r'^([a-zA-Z0-9_-]+(?:\[[^\]]+\])?)', package)
    if not match:
        return False, "Invalid package name format"

    package_name = match.group(1)

    # Basic validation
    if len(package_name) > 200:
        return False, "Package name is too long"

    return True, None


def validate_waft_project(project_path: Path) -> tuple[bool, Optional[str]]:
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


def parse_toml_field(file_path: Path, field: str) -> Optional[str]:
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
    from datetime import datetime

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
        '/': '_',
        '\\': '_',
        ':': '-',
        '*': '_',
        '?': '_',
        '"': '_',
        '<': '_',
        '>': '_',
        '|': '_'
    }
    
    for unsafe, safe_char in replacements.items():
        safe = safe.replace(unsafe, safe_char)
    
    # Remove leading/trailing spaces and dots (Windows issue)
    safe = safe.strip(' .')
    
    # Limit length for filesystem
    if len(safe) > 200:
        safe = safe[:200]
    
    return safe


def generate_headline_title(claim: str, verdict: Optional[str] = None) -> str:
    """
    Generate headline-style title from claim.
    Target: ~7 words for gist, ~14 words total, most important info first.
    Properly handles special characters.
    """
    import re
    
    if not claim:
        return "Proof Case"
    
    # Clean up claim - remove markdown, extra whitespace
    claim = re.sub(r'\*\*|`|_', '', claim)  # Remove markdown formatting
    claim = re.sub(r'\s+', ' ', claim).strip()  # Normalize whitespace
    
    # Remove common prefixes that don't add info
    claim = re.sub(r'^(?:The\s+|A\s+|An\s+)', '', claim, flags=re.IGNORECASE)
    
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
            if word.lower() in ['is', 'are', 'was', 'were', 'does', 'has', 'have']:
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
        gist = subject + verb + outcome_words[:7 - len(subject) - len(verb)]
        
        # If room, add more context (up to 14 words total)
        if len(gist) < 14:
            remaining = outcome_words[7 - len(subject) - len(verb):]
            added = []
            for word in remaining:
                if word.lower() in ['and', 'or', 'but', 'where', 'when', 'which', 'that']:
                    if len(gist) + len(added) < 12:
                        added.append(word)
                    break
                if any(punct in word for punct in ['.', ',', ';', ':', '!', '?']):
                    break
                if len(gist) + len(added) < 14:
                    added.append(word)
                else:
                    break
            title = ' '.join(gist + added)
        else:
            title = ' '.join(gist)
    
    # Add verdict if provided (short form, no repetition)
    if verdict:
        verdict_clean = re.sub(r'✅|❌|⚠️|\*\*', '', verdict).strip()
        verdict_short = verdict_clean.split()[0] if verdict_clean else ""
        if verdict_short and verdict_short not in title.upper():
            title = f"{title} ({verdict_short})"
    
    return title


def find_files_recursive(directory: Path, pattern: str = "*", exclude_dirs: Optional[list[str]] = None) -> list[Path]:
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
        '/': '_',
        '\\': '_',
        ':': '-',
        '*': '_',
        '?': '_',
        '"': '_',
        '<': '_',
        '>': '_',
        '|': '_'
    }
    
    for unsafe, safe_char in replacements.items():
        safe = safe.replace(unsafe, safe_char)
    
    # Remove leading/trailing spaces and dots (Windows issue)
    safe = safe.strip(' .')
    
    # Limit length for filesystem
    if len(safe) > 200:
        safe = safe[:200]
    
    return safe


def generate_headline_title(claim: str, verdict: Optional[str] = None) -> str:
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
    claim = re.sub(r'\*\*|`|_', '', claim)  # Remove markdown formatting
    claim = re.sub(r'\s+', ' ', claim).strip()  # Normalize whitespace
    
    # Remove common prefixes that don't add info
    claim = re.sub(r'^(?:The\s+|A\s+|An\s+)', '', claim, flags=re.IGNORECASE)
    
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
            if word.lower() in ['is', 'are', 'was', 'were', 'does', 'has', 'have']:
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
        gist = subject + verb + outcome_words[:7 - len(subject) - len(verb)]
        
        # If room, add more context (up to 14 words total)
        if len(gist) < 14:
            remaining = outcome_words[7 - len(subject) - len(verb):]
            added = []
            for word in remaining:
                if word.lower() in ['and', 'or', 'but', 'where', 'when', 'which', 'that']:
                    if len(gist) + len(added) < 12:
                        added.append(word)
                    break
                if any(punct in word for punct in ['.', ',', ';', ':', '!', '?']):
                    break
                if len(gist) + len(added) < 14:
                    added.append(word)
                else:
                    break
            title = ' '.join(gist + added)
        else:
            title = ' '.join(gist)
    
    # Add verdict if provided (short form, no repetition)
    if verdict:
        verdict_clean = re.sub(r'✅|❌|⚠️|\*\*', '', verdict).strip()
        verdict_short = verdict_clean.split()[0] if verdict_clean else ""
        if verdict_short and verdict_short not in title.upper():
            title = f"{title} ({verdict_short})"
    
    return title

"""
Code Extraction Utilities for Case Files

Extracts code references from case files and creates a Code Examples section.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict


def extract_code_references(case_content: str) -> Dict[str, List[Dict[str, any]]]:
    """
    Extract code references from case file content.
    
    Returns:
        Dictionary with:
        - 'inline_snippets': Short code snippets used inline
        - 'file_references': Files referenced with line numbers
        - 'code_blocks': Full code blocks that should be in examples
    """
    references = {
        'inline_snippets': [],
        'file_references': [],
        'code_blocks': []
    }
    
    # Pattern 1: File references with line numbers
    # Example: "**File**: `src/waft/pantheon/magistrate.py`  **Lines**: 199-201"
    file_pattern = r'\*\*File\*\*:\s*`([^`]+)`\s*\*\*Lines\*\*:\s*([0-9,\-\s]+)'
    
    for match in re.finditer(file_pattern, case_content):
        file_path = match.group(1)
        lines_str = match.group(2)
        
        # Parse line numbers
        line_numbers = []
        for part in lines_str.split(','):
            part = part.strip()
            if '-' in part:
                start, end = part.split('-')
                line_numbers.extend(range(int(start), int(end) + 1))
            else:
                line_numbers.append(int(part))
        
        references['file_references'].append({
            'file': file_path,
            'lines': sorted(set(line_numbers)),
            'context': match.group(0)
        })
    
    # Pattern 2: Code blocks with language
    # Example: ```python\ncode\n```
    code_block_pattern = r'```(\w+)?\n(.*?)```'
    
    for match in re.finditer(code_block_pattern, case_content, re.DOTALL):
        language = match.group(1) or 'text'
        code = match.group(2).strip()
        
        # Skip very short snippets (already inline)
        if len(code.split('\n')) > 3:
            references['code_blocks'].append({
                'language': language,
                'code': code,
                'context': match.group(0)[:100]  # First 100 chars for context
            })
    
    # Pattern 3: Inline code snippets (short)
    # Example: `self.pantheon_path = project_path / "_pantheon"`
    inline_pattern = r'`([^`\n]{10,100})`'
    
    for match in re.finditer(inline_pattern, case_content):
        snippet = match.group(1)
        # Only include if it looks like code (has operators, etc.)
        if any(op in snippet for op in ['=', '(', ')', '.', '/', ':', '->', 'import', 'def', 'class']):
            references['inline_snippets'].append({
                'snippet': snippet,
                'context': match.group(0)
            })
    
    return references


def read_code_from_file(file_path: Path, lines: List[int], context_lines: int = 2) -> Optional[str]:
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
        content = file_path.read_text(encoding='utf-8')
        content_lines = content.split('\n')
        
        # Get range of lines to extract
        min_line = max(0, min(lines) - context_lines - 1)
        max_line = min(len(content_lines), max(lines) + context_lines)
        
        # Extract code
        extracted_lines = content_lines[min_line:max_line]
        
        # Build code with line numbers
        code_parts = []
        for i, line in enumerate(extracted_lines, start=min_line + 1):
            marker = '>>>' if i in lines else '   '
            code_parts.append(f"{marker} {i:4d} | {line}")
        
        return '\n'.join(code_parts)
    except Exception:
        return None


def build_code_examples_section(
    case_content: str,
    project_path: Path,
    max_examples: int = 20
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
    section.append("Code snippets in the document reference these examples (e.g., 'See Example 1').")
    section.append("")
    section.append("---")
    section.append("")
    
    example_num = 1
    
    # Group file references by file
    files_by_path = defaultdict(list)
    for ref in references['file_references']:
        files_by_path[ref['file']].extend(ref['lines'])
    
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
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'jsx',
            '.tsx': 'tsx',
            '.css': 'css',
            '.html': 'html',
            '.md': 'markdown',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.toml': 'toml',
            '.sh': 'bash',
            '.sql': 'sql'
        }
        language = language_map.get(ext, 'text')
        
        section.append(f"### Example {example_num}: {file_path_str}")
        section.append("")
        section.append(f"**File**: `{file_path_str}`")
        section.append(f"**Lines**: {', '.join(map(str, unique_lines[:10]))}{'...' if len(unique_lines) > 10 else ''}")
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
    for code_block in references['code_blocks'][:max_examples - example_num + 1]:
        section.append(f"### Example {example_num}: Code Block")
        section.append("")
        section.append(f"**Language**: {code_block['language']}")
        section.append("")
        section.append("```" + code_block['language'])
        section.append(code_block['code'])
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
    
    return '\n'.join(section)


def add_code_examples_to_case_file(
    case_file_path: Path,
    project_path: Path
) -> bool:
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
    
    content = case_file_path.read_text(encoding='utf-8')
    
    # Check if Code Examples section already exists
    if '## CODE EXAMPLES' in content or '## Code Examples' in content:
        return False  # Already has examples
    
    # Build examples section
    examples_section = build_code_examples_section(content, project_path)
    
    if not examples_section:
        return False  # No code references found
    
    # Add before the final line or at the end
    # Look for common ending patterns
    ending_patterns = [
        r'\*This case file was automatically generated',
        r'## Conclusion',
        r'## CONCLUSION',
        r'\*\*Case Status\*\*'
    ]
    
    insert_position = len(content)
    for pattern in ending_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            insert_position = match.start()
            break
    
    # Insert examples section
    new_content = (
        content[:insert_position].rstrip() + 
        '\n\n' + 
        examples_section + 
        '\n\n' + 
        content[insert_position:].lstrip()
    )
    
    case_file_path.write_text(new_content, encoding='utf-8')
    return True


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
    output_path: Optional[Path] = None,
    marker_text: str = "[ THIS PAGE IS BLANK ON PURPOSE ]"
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
                align=1  # Center alignment
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
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
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
        with open(output_path, 'wb') as output_file:
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

