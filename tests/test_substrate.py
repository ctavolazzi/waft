"""Tests for SubstrateManager."""

import pytest
from pathlib import Path
from waft.core.substrate import SubstrateManager


def test_substrate_manager_init():
    """Test SubstrateManager initialization."""
    manager = SubstrateManager()
    assert manager.project_path is None

    project_path = Path("/tmp/test")
    manager = SubstrateManager(project_path)
    assert manager.project_path == project_path


def test_verify_lock_exists(full_waft_project):
    """Test lock file verification when it exists."""
    manager = SubstrateManager(full_waft_project)
    assert manager.verify_lock() is True


def test_verify_lock_missing(temp_project_path):
    """Test lock file verification when it doesn't exist."""
    manager = SubstrateManager(temp_project_path)
    assert manager.verify_lock() is False


def test_get_project_info_valid(project_with_pyproject):
    """Test getting project info from valid pyproject.toml."""
    manager = SubstrateManager(project_with_pyproject)
    info = manager.get_project_info()

    assert "name" in info
    assert info["name"] == "test_project"
    assert "version" in info
    assert info["version"] == "0.1.0"


def test_get_project_info_invalid(project_with_invalid_pyproject):
    """Test getting project info from invalid pyproject.toml."""
    manager = SubstrateManager(project_with_invalid_pyproject)
    info = manager.get_project_info()

    # Should return empty dict if parsing fails
    assert info == {}


def test_get_project_info_missing(temp_project_path):
    """Test getting project info when pyproject.toml doesn't exist."""
    manager = SubstrateManager(temp_project_path)
    info = manager.get_project_info()

    assert info == {}


def test_get_project_info_with_path(project_with_pyproject, temp_dir):
    """Test getting project info with explicit path parameter."""
    manager = SubstrateManager()  # No default path
    info = manager.get_project_info(project_with_pyproject)

    assert "name" in info
    assert info["name"] == "test_project"


def test_verify_lock_with_path(full_waft_project, temp_dir):
    """Test verify_lock with explicit path parameter."""
    manager = SubstrateManager()  # No default path
    assert manager.verify_lock(full_waft_project) is True
    assert manager.verify_lock(temp_dir) is False


def test_substrate_manager_requires_path():
    """Test that methods raise ValueError when no path provided."""
    manager = SubstrateManager()  # No default path

    with pytest.raises(ValueError):
        manager.sync()

    with pytest.raises(ValueError):
        manager.add_dependency("pytest")

    with pytest.raises(ValueError):
        manager.verify_lock()

    with pytest.raises(ValueError):
        manager.get_project_info()

