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

