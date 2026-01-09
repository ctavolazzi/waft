"""Tests for MemoryManager."""

from pathlib import Path
from waft.core.memory import MemoryManager


def test_memory_manager_init(temp_project_path):
    """Test MemoryManager initialization."""
    manager = MemoryManager(temp_project_path)
    assert manager.project_path == temp_project_path
    assert manager.pyrite_path == temp_project_path / "_pyrite"


def test_create_structure(temp_project_path):
    """Test _pyrite structure creation."""
    manager = MemoryManager(temp_project_path)
    manager.create_structure()

    assert (temp_project_path / "_pyrite").exists()
    assert (temp_project_path / "_pyrite" / "active").exists()
    assert (temp_project_path / "_pyrite" / "backlog").exists()
    assert (temp_project_path / "_pyrite" / "standards").exists()

    # Check .gitkeep files
    assert (temp_project_path / "_pyrite" / "active" / ".gitkeep").exists()
    assert (temp_project_path / "_pyrite" / "backlog" / ".gitkeep").exists()
    assert (temp_project_path / "_pyrite" / "standards" / ".gitkeep").exists()


def test_verify_structure_valid(project_with_pyrite):
    """Test structure verification with valid structure."""
    manager = MemoryManager(project_with_pyrite)
    result = manager.verify_structure()

    assert result["valid"] is True
    assert result["folders"]["_pyrite/active"] is True
    assert result["folders"]["_pyrite/backlog"] is True
    assert result["folders"]["_pyrite/standards"] is True


def test_verify_structure_invalid(temp_project_path):
    """Test structure verification with missing structure."""
    manager = MemoryManager(temp_project_path)
    result = manager.verify_structure()

    assert result["valid"] is False
    assert result["folders"]["_pyrite/active"] is False
    assert result["folders"]["_pyrite/backlog"] is False
    assert result["folders"]["_pyrite/standards"] is False


def test_get_active_files(project_with_pyrite):
    """Test getting active files."""
    manager = MemoryManager(project_with_pyrite)

    # Initially empty
    files = manager.get_active_files()
    assert len(files) == 0

    # Add a file
    test_file = project_with_pyrite / "_pyrite" / "active" / "test.md"
    test_file.write_text("# Test")

    files = manager.get_active_files()
    assert len(files) == 1
    assert test_file in files


def test_get_backlog_files(project_with_pyrite):
    """Test getting backlog files."""
    manager = MemoryManager(project_with_pyrite)

    # Initially empty
    files = manager.get_backlog_files()
    assert len(files) == 0

    # Add a file
    test_file = project_with_pyrite / "_pyrite" / "backlog" / "future.md"
    test_file.write_text("# Future")

    files = manager.get_backlog_files()
    assert len(files) == 1
    assert test_file in files


def test_get_standards_files(project_with_pyrite):
    """Test getting standards files."""
    manager = MemoryManager(project_with_pyrite)

    # Initially empty
    files = manager.get_standards_files()
    assert len(files) == 0

    # Add a file
    test_file = project_with_pyrite / "_pyrite" / "standards" / "style.md"
    test_file.write_text("# Style")

    files = manager.get_standards_files()
    assert len(files) == 1
    assert test_file in files


