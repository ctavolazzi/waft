"""
Pytest fixtures for API tests.
"""

import shutil
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.waft.api.main import create_app
from src.waft.api.services.work_effort_service import WorkEffortService
from src.waft.core.projects import ProjectManager


@pytest.fixture
def temp_project_path():
    """Create a temporary project directory."""
    temp_dir = tempfile.mkdtemp()
    project_path = Path(temp_dir)

    # Create _work_efforts directory
    (project_path / "_work_efforts").mkdir(exist_ok=True)

    yield project_path

    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def project_manager(temp_project_path):
    """Create a ProjectManager instance."""
    return ProjectManager(temp_project_path)


@pytest.fixture
def work_effort_service(temp_project_path):
    """Create a WorkEffortService instance."""
    return WorkEffortService(temp_project_path)


@pytest.fixture
def test_client(temp_project_path):
    """Create a FastAPI test client."""
    app = create_app(temp_project_path)
    return TestClient(app)


@pytest.fixture
def auth_token(temp_project_path):
    """Create a test authentication token."""
    from src.waft.api.auth import get_or_create_token

    return get_or_create_token(temp_project_path)
