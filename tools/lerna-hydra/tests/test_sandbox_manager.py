"""Tier 1 tests: SandboxManager — path-jailed file CRUD."""
import os
from pathlib import Path

import pytest

from sandbox_manager import SandboxManager


class TestSafePath:
    """Path validation — the security boundary."""

    def test_relative_path_allowed(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir)
        result = sm._safe_path("index.html")
        assert result == sandbox_dir / "index.html"

    def test_nested_relative_allowed(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir)
        result = sm._safe_path("src/main.py")
        assert result == sandbox_dir / "src" / "main.py"

    def test_traversal_blocked(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir)
        with pytest.raises(ValueError, match="escapes sandbox"):
            sm._safe_path("../../../etc/passwd")

    def test_absolute_path_blocked(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir)
        with pytest.raises(ValueError, match="escapes sandbox"):
            sm._safe_path("/etc/passwd")

    def test_dot_dot_in_middle_blocked(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir)
        with pytest.raises(ValueError, match="escapes sandbox"):
            sm._safe_path("src/../../etc/passwd")

    def test_symlink_escape_blocked(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir)
        # Create symlink pointing outside sandbox
        link = sandbox_dir / "escape_link"
        link.symlink_to("/etc")
        with pytest.raises(ValueError, match="escapes sandbox"):
            sm._safe_path("escape_link/passwd")


class TestListFiles:
    def test_list_root(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir)
        entries = sm.list_files(".")
        names = {e["name"] for e in entries}
        assert "index.html" in names
        assert "README.md" in names
        assert "src" in names

    def test_list_subdir(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir)
        entries = sm.list_files("src")
        assert len(entries) == 1
        assert entries[0]["name"] == "main.py"
        assert entries[0]["type"] == "file"

    def test_list_includes_type_and_size(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir)
        entries = sm.list_files(".")
        src_entry = next(e for e in entries if e["name"] == "src")
        assert src_entry["type"] == "dir"
        html_entry = next(e for e in entries if e["name"] == "index.html")
        assert html_entry["type"] == "file"
        assert html_entry["size"] > 0

    def test_list_nonexistent_raises(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir)
        with pytest.raises(FileNotFoundError):
            sm.list_files("nonexistent")


class TestReadFile:
    def test_read_existing(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir)
        content = sm.read_file("index.html")
        assert "<h1>Sandbox</h1>" in content

    def test_read_nested(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir)
        content = sm.read_file("src/main.py")
        assert "hello" in content

    def test_read_nonexistent_raises(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir)
        with pytest.raises(FileNotFoundError):
            sm.read_file("ghost.txt")


class TestWriteFile:
    def test_write_creates_file(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir)
        result = sm.write_file("new.txt", "hello world")
        assert result["ok"] is True
        assert (sandbox_dir / "new.txt").read_text() == "hello world"

    def test_write_creates_parent_dirs(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir)
        sm.write_file("a/b/c.txt", "deep")
        assert (sandbox_dir / "a" / "b" / "c.txt").read_text() == "deep"

    def test_write_overwrites_existing(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir)
        sm.write_file("index.html", "<html><body>new</body></html>")
        assert "new" in (sandbox_dir / "index.html").read_text()

    def test_write_enforces_file_size_limit(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir, max_file_bytes=1024)
        with pytest.raises(ValueError, match="exceeds.*limit"):
            sm.write_file("big.txt", "x" * 2048)

    def test_write_enforces_total_size_limit(self, empty_sandbox):
        sm = SandboxManager(empty_sandbox, max_total_bytes=100)
        sm.write_file("a.txt", "x" * 50)
        with pytest.raises(ValueError, match="total.*limit"):
            sm.write_file("b.txt", "x" * 60)


class TestDeleteFile:
    def test_delete_existing(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir)
        sm.delete_file("README.md")
        assert not (sandbox_dir / "README.md").exists()

    def test_delete_returns_result(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir)
        result = sm.delete_file("README.md")
        assert result["ok"] is True

    def test_delete_nonexistent_raises(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir)
        with pytest.raises(FileNotFoundError):
            sm.delete_file("ghost.txt")


class TestSandboxSize:
    def test_get_total_size(self, sandbox_dir):
        sm = SandboxManager(sandbox_dir)
        size = sm.get_total_size()
        assert size > 0
