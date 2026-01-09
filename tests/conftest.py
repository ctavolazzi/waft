"""Pytest configuration and fixtures."""

import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_project_path():
    """Create a temporary project directory."""
    temp_dir = tempfile.mkdtemp()
    project_path = Path(temp_dir) / "test_project"
    project_path.mkdir(parents=True)
    yield project_path
    shutil.rmtree(temp_dir)


@pytest.fixture
def temp_dir():
    """Create a temporary directory."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def project_with_pyproject(temp_project_path):
    """Create a project with valid pyproject.toml."""
    pyproject = temp_project_path / "pyproject.toml"
    pyproject.write_text(
        """[project]
name = "test_project"
version = "0.1.0"
description = "Test project"
"""
    )
    yield temp_project_path


@pytest.fixture
def project_with_invalid_pyproject(temp_project_path):
    """Create a project with invalid pyproject.toml."""
    pyproject = temp_project_path / "pyproject.toml"
    pyproject.write_text("invalid toml content {")
    yield temp_project_path


@pytest.fixture
def project_with_pyrite(temp_project_path):
    """Create a project with _pyrite structure."""
    pyrite_path = temp_project_path / "_pyrite"
    (pyrite_path / "active").mkdir(parents=True)
    (pyrite_path / "backlog").mkdir(parents=True)
    (pyrite_path / "standards").mkdir(parents=True)
    yield temp_project_path


@pytest.fixture
def full_waft_project(temp_project_path):
    """Create a complete waft project with all components."""
    # pyproject.toml
    pyproject = temp_project_path / "pyproject.toml"
    pyproject.write_text(
        """[project]
name = "test_project"
version = "0.1.0"
description = "Test project"
"""
    )

    # _pyrite structure
    pyrite_path = temp_project_path / "_pyrite"
    (pyrite_path / "active").mkdir(parents=True)
    (pyrite_path / "backlog").mkdir(parents=True)
    (pyrite_path / "standards").mkdir(parents=True)

    # uv.lock (empty file to simulate)
    (temp_project_path / "uv.lock").write_text("# Lock file")

    # Templates
    (temp_project_path / "Justfile").write_text("# Justfile")
    (temp_project_path / ".github" / "workflows").mkdir(parents=True)
    (temp_project_path / ".github" / "workflows" / "ci.yml").write_text("# CI workflow")
    (temp_project_path / "src").mkdir(parents=True)
    (temp_project_path / "src" / "agents.py").write_text("# agents.py")

    yield temp_project_path