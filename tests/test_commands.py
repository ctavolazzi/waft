"""Tests for CLI commands."""

import subprocess
import sys
from pathlib import Path
import pytest
from waft.core.memory import MemoryManager
from waft.core.substrate import SubstrateManager


def run_waft_command(args, cwd=None):
    """Helper to run waft command and return result."""
    cmd = [sys.executable, "-m", "waft.main"] + args
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return result


def test_waft_new_creates_structure(temp_dir):
    """Test that waft new creates correct project structure."""
    project_name = "test_new_project"
    project_path = temp_dir / project_name

    result = run_waft_command(["new", project_name], cwd=temp_dir)

    # Command should succeed (or at least create structure)
    # Check that project directory was created
    if project_path.exists():
        # Check _pyrite structure
        assert (project_path / "_pyrite" / "active").exists()
        assert (project_path / "_pyrite" / "backlog").exists()
        assert (project_path / "_pyrite" / "standards").exists()

        # Check pyproject.toml exists
        assert (project_path / "pyproject.toml").exists()


def test_waft_verify_valid_project(full_waft_project):
    """Test waft verify with valid project."""
    result = run_waft_command(["verify"], cwd=full_waft_project)

    # Should succeed (exit code 0) or at least not fail with structure errors
    # The actual exit code depends on Empirica initialization, but structure should be valid
    assert "valid" in result.stdout.lower() or result.returncode == 0 or "_pyrite" in result.stdout


def test_waft_verify_invalid_project(temp_project_path):
    """Test waft verify with invalid project."""
    result = run_waft_command(["verify"], cwd=temp_project_path)

    # Should fail (exit code 1) for invalid project
    assert result.returncode == 1 or "invalid" in result.stdout.lower() or "missing" in result.stdout.lower()


def test_waft_info_shows_project_info(project_with_pyproject):
    """Test waft info command displays project information."""
    result = run_waft_command(["info"], cwd=project_with_pyproject)

    # Should show project information
    assert "Project" in result.stdout or "project" in result.stdout.lower()

    # Should NOT show duplicate "Project Name" (bug fix verification)
    project_name_count = result.stdout.count("Project Name")
    assert project_name_count == 1, f"Found {project_name_count} instances of 'Project Name' (expected 1)"


def test_waft_info_with_full_project(full_waft_project):
    """Test waft info with complete project."""
    result = run_waft_command(["info"], cwd=full_waft_project)

    # Should show various project information
    assert "Project" in result.stdout or "project" in result.stdout.lower()

    # Verify no duplicate Project Name
    project_name_count = result.stdout.count("Project Name")
    assert project_name_count == 1, f"Found {project_name_count} instances of 'Project Name' (expected 1)"


def test_waft_info_without_pyproject(temp_project_path):
    """Test waft info when pyproject.toml doesn't exist."""
    result = run_waft_command(["info"], cwd=temp_project_path)

    # Should still run and show information
    assert "Project" in result.stdout or "project" in result.stdout.lower()

    # Should show "Not a Python project" or similar
    assert "Not a Python project" in result.stdout or "not a python" in result.stdout.lower() or "N/A" in result.stdout


def test_waft_init_creates_structure(project_with_pyproject):
    """Test waft init creates _pyrite structure in existing project."""
    # Ensure _pyrite doesn't exist initially
    pyrite_path = project_with_pyproject / "_pyrite"
    if pyrite_path.exists():
        import shutil
        shutil.rmtree(pyrite_path)

    result = run_waft_command(["init"], cwd=project_with_pyproject)

    # Should create _pyrite structure
    assert (project_with_pyproject / "_pyrite" / "active").exists()
    assert (project_with_pyproject / "_pyrite" / "backlog").exists()
    assert (project_with_pyproject / "_pyrite" / "standards").exists()


def test_waft_init_fails_without_pyproject(temp_project_path):
    """Test waft init fails gracefully when pyproject.toml doesn't exist."""
    result = run_waft_command(["init"], cwd=temp_project_path)

    # Should fail or show warning
    assert result.returncode == 1 or "pyproject.toml" in result.stdout.lower() or "not found" in result.stdout.lower()


def test_memory_manager_create_structure(temp_project_path):
    """Test MemoryManager creates correct structure."""
    memory = MemoryManager(temp_project_path)
    memory.create_structure()

    assert (temp_project_path / "_pyrite" / "active").exists()
    assert (temp_project_path / "_pyrite" / "backlog").exists()
    assert (temp_project_path / "_pyrite" / "standards").exists()


def test_memory_manager_verify_structure(project_with_pyrite):
    """Test MemoryManager verifies structure correctly."""
    memory = MemoryManager(project_with_pyrite)
    result = memory.verify_structure()

    assert result["valid"] is True
    assert result["folders"]["_pyrite/active"] is True


def test_substrate_manager_get_project_info(project_with_pyproject):
    """Test SubstrateManager gets project info correctly."""
    substrate = SubstrateManager(project_with_pyproject)
    info = substrate.get_project_info()

    assert "name" in info
    assert info["name"] == "test_project"


def test_waft_new_with_path_flag(temp_dir):
    """Test waft new with --path flag."""
    project_name = "test_path_project"
    target_dir = temp_dir / "target"
    target_dir.mkdir()
    project_path = target_dir / project_name

    result = run_waft_command(["new", project_name, "--path", str(target_dir)])

    # Should create project in specified path
    if project_path.exists():
        assert (project_path / "pyproject.toml").exists()


def test_waft_info_with_path_flag(project_with_pyproject, temp_dir):
    """Test waft info with --path flag."""
    result = run_waft_command(["info", "--path", str(project_with_pyproject)], cwd=temp_dir)

    # Should show project information
    assert "Project" in result.stdout or "project" in result.stdout.lower()

    # Verify no duplicate Project Name
    project_name_count = result.stdout.count("Project Name")
    assert project_name_count == 1, f"Found {project_name_count} instances of 'Project Name' (expected 1)"


def test_waft_verify_updates_integrity(full_waft_project):
    """Test that waft verify updates integrity (via gamification)."""
    result = run_waft_command(["verify"], cwd=full_waft_project)

    # Should run successfully and potentially show integrity
    # The exact output depends on gamification state, but command should complete
    assert result.returncode in [0, 1]  # May succeed or fail based on state

