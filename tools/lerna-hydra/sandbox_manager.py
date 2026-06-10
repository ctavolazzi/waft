"""SandboxManager — path-jailed file CRUD for Lerna Hydra.

All file operations are confined to a single root directory.
No symlink escape, no path traversal, size limits enforced.
"""
from pathlib import Path
from typing import Any


# Defaults
DEFAULT_MAX_FILE_BYTES = 1_048_576      # 1 MB per file
DEFAULT_MAX_TOTAL_BYTES = 52_428_800    # 50 MB total sandbox


class SandboxManager:
    def __init__(
        self,
        root: Path,
        max_file_bytes: int = DEFAULT_MAX_FILE_BYTES,
        max_total_bytes: int = DEFAULT_MAX_TOTAL_BYTES,
    ):
        self.root = Path(root).resolve()
        self.max_file_bytes = max_file_bytes
        self.max_total_bytes = max_total_bytes

    def _safe_path(self, relative: str) -> Path:
        """Resolve path and verify it stays within sandbox.

        Resolves symlinks, normalizes .., and checks the result
        is still under self.root. Raises ValueError on escape.
        """
        # Block absolute paths immediately
        if relative.startswith("/"):
            raise ValueError(f"Path escapes sandbox: {relative}")

        target = (self.root / relative).resolve()
        if not str(target).startswith(str(self.root)):
            raise ValueError(f"Path escapes sandbox: {relative}")
        return target

    def list_files(self, relative_dir: str = ".") -> list[dict[str, Any]]:
        """List entries in a sandbox directory."""
        target = self._safe_path(relative_dir)
        if not target.exists():
            raise FileNotFoundError(f"Directory not found: {relative_dir}")
        if not target.is_dir():
            raise NotADirectoryError(f"Not a directory: {relative_dir}")

        entries = []
        for child in sorted(target.iterdir()):
            entry = {"name": child.name}
            if child.is_dir():
                entry["type"] = "dir"
                entry["size"] = 0
            else:
                entry["type"] = "file"
                entry["size"] = child.stat().st_size
            entries.append(entry)
        return entries

    def read_file(self, relative_path: str) -> str:
        """Read a text file from the sandbox."""
        target = self._safe_path(relative_path)
        if not target.exists():
            raise FileNotFoundError(f"File not found: {relative_path}")
        return target.read_text(encoding="utf-8")

    def write_file(self, relative_path: str, content: str) -> dict[str, Any]:
        """Write a text file in the sandbox. Creates parent dirs."""
        target = self._safe_path(relative_path)
        content_bytes = content.encode("utf-8")

        # Per-file size limit
        if len(content_bytes) > self.max_file_bytes:
            raise ValueError(
                f"File size ({len(content_bytes)} bytes) exceeds limit "
                f"({self.max_file_bytes} bytes)"
            )

        # Total sandbox size limit (current size + new content - existing file size)
        existing_size = target.stat().st_size if target.exists() else 0
        new_total = self.get_total_size() - existing_size + len(content_bytes)
        if new_total > self.max_total_bytes:
            raise ValueError(
                f"Write would push total sandbox size ({new_total} bytes) "
                f"over total limit ({self.max_total_bytes} bytes)"
            )

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content_bytes)
        return {"ok": True, "path": relative_path, "bytes": len(content_bytes)}

    def delete_file(self, relative_path: str) -> dict[str, Any]:
        """Delete a file from the sandbox."""
        target = self._safe_path(relative_path)
        if not target.exists():
            raise FileNotFoundError(f"File not found: {relative_path}")
        target.unlink()
        return {"ok": True, "path": relative_path}

    def get_total_size(self) -> int:
        """Sum of all file sizes in the sandbox."""
        total = 0
        for f in self.root.rglob("*"):
            if f.is_file():
                total += f.stat().st_size
        return total
