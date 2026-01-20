"""
Banned Words System: Enforces word restrictions across the codebase.

This tool helps maintain word restrictions by:
1. Checking for banned words in code and documentation
2. Providing alternatives
3. Enforcing replacements
"""

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class BannedWord:
    """Represents a banned word with its replacement."""

    word: str
    replacement: str
    reason: str = ""
    case_sensitive: bool = False


class BannedWordsSystem:
    """System for managing and enforcing banned words."""

    def __init__(self, project_path: Path):
        """
        Initialize banned words system.

        Args:
            project_path: Path to project root
        """
        self.project_path = Path(project_path)
        self.banned_words: list[BannedWord] = []

        # Initialize with default banned words
        self._load_default_bans()

    def _load_default_bans(self):
        """Load default banned words."""
        self.banned_words = [
            BannedWord(
                word="manifesto",
                replacement="report",
                reason="Banned by user request",
                case_sensitive=False,
            ),
        ]

    def add_ban(self, word: str, replacement: str, reason: str = "", case_sensitive: bool = False):
        """
        Add a banned word.

        Args:
            word: Word to ban
            replacement: Replacement word
            reason: Reason for ban
            case_sensitive: Whether ban is case-sensitive
        """
        self.banned_words.append(
            BannedWord(
                word=word, replacement=replacement, reason=reason, case_sensitive=case_sensitive
            )
        )

    def check_text(self, text: str) -> list[dict]:
        """
        Check text for banned words.

        Args:
            text: Text to check

        Returns:
            List of violations with line numbers and context
        """
        violations = []
        lines = text.split("\n")

        for line_num, line in enumerate(lines, 1):
            for ban in self.banned_words:
                if ban.case_sensitive:
                    pattern = re.escape(ban.word)
                else:
                    pattern = re.escape(ban.word)
                    line_lower = line.lower()
                    if ban.word.lower() in line_lower:
                        # Find all occurrences
                        matches = list(re.finditer(re.escape(ban.word), line_lower, re.IGNORECASE))
                        for match in matches:
                            violations.append(
                                {
                                    "line": line_num,
                                    "word": ban.word,
                                    "replacement": ban.replacement,
                                    "context": line.strip(),
                                    "reason": ban.reason,
                                }
                            )

        return violations

    def scan_file(self, file_path: Path) -> list[dict]:
        """
        Scan a file for banned words.

        Args:
            file_path: Path to file

        Returns:
            List of violations
        """
        if not file_path.exists():
            return []

        try:
            text = file_path.read_text(encoding="utf-8")
            violations = self.check_text(text)
            for v in violations:
                v["file"] = str(file_path)
            return violations
        except Exception as e:
            return [{"file": str(file_path), "error": str(e)}]

    def scan_directory(self, directory: Path, patterns: list[str] = None) -> list[dict]:
        """
        Scan directory for banned words.

        Args:
            directory: Directory to scan
            patterns: File patterns to include (e.g., ["*.py", "*.md"])

        Returns:
            List of all violations
        """
        if patterns is None:
            patterns = ["*.py", "*.md", "*.txt", "*.json", "*.yaml", "*.yml"]

        all_violations = []

        for pattern in patterns:
            for file_path in directory.rglob(pattern):
                # Skip common exclusions
                if any(
                    excluded in str(file_path)
                    for excluded in [".git", "__pycache__", "node_modules", ".venv"]
                ):
                    continue

                violations = self.scan_file(file_path)
                all_violations.extend(violations)

        return all_violations

    def replace_in_text(self, text: str) -> str:
        """
        Replace banned words in text.

        Args:
            text: Text to process

        Returns:
            Text with banned words replaced
        """
        result = text

        for ban in self.banned_words:
            if ban.case_sensitive:
                result = result.replace(ban.word, ban.replacement)
            else:
                # Case-insensitive replacement, preserving original case
                pattern = re.compile(re.escape(ban.word), re.IGNORECASE)
                result = pattern.sub(ban.replacement, result)

        return result

    def replace_in_file(self, file_path: Path) -> bool:
        """
        Replace banned words in file.

        Args:
            file_path: Path to file

        Returns:
            True if replacements were made
        """
        if not file_path.exists():
            return False

        try:
            original_text = file_path.read_text(encoding="utf-8")
            new_text = self.replace_in_text(original_text)

            if original_text != new_text:
                file_path.write_text(new_text, encoding="utf-8")
                return True
            return False
        except Exception:
            return False

    def get_banned_words(self) -> list[str]:
        """Get list of all banned words."""
        return [ban.word for ban in self.banned_words]

    def get_replacements(self) -> dict[str, str]:
        """Get mapping of banned words to replacements."""
        return {ban.word: ban.replacement for ban in self.banned_words}
