"""Pytest configuration and fixtures."""

import shutil
import tempfile
from pathlib import Path

import pytest


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


@pytest.fixture
def sample_work_efforts_dir(temp_project_path):
    """Create a temporary work efforts structure with sample data."""
    work_efforts_dir = temp_project_path / "_work_efforts"
    work_efforts_dir.mkdir(parents=True)

    # Copy test data work efforts
    test_data_dir = Path(__file__).parent / "test_data" / "work_efforts"
    if test_data_dir.exists():
        import shutil

        for we_dir in test_data_dir.iterdir():
            if we_dir.is_dir():
                shutil.copytree(we_dir, work_efforts_dir / we_dir.name)

    yield work_efforts_dir


@pytest.fixture
def sample_projects_data():
    """Mock project data for testing."""
    return [
        {
            "id": "proj-001",
            "title": "Test Project 1",
            "status": "active",
            "progress": 75.0,
            "description": "A test project",
            "tags": "test, example",
            "created": "2026-01-17T10:00:00Z",
            "updated": "2026-01-17T14:00:00Z",
            "milestones": 3,
            "related_work_efforts": 2,
        },
        {
            "id": "proj-002",
            "title": "Test Project 2",
            "status": "open",
            "progress": 0.0,
            "description": "Another test project",
            "tags": "test",
            "created": "2026-01-16T10:00:00Z",
            "updated": "2026-01-16T10:00:00Z",
            "milestones": 0,
            "related_work_efforts": 0,
        },
    ]


@pytest.fixture
def sample_templates_data():
    """Mock template registry data for testing."""
    return [
        {
            "name": "test_template_1",
            "category": "academic",
            "tags": "paper, research",
            "description": "A test template for academic papers",
        },
        {
            "name": "test_template_2",
            "category": "business",
            "tags": "report, presentation",
            "description": "A test template for business reports with a very long description that should be truncated",
        },
    ]


@pytest.fixture
def sample_experiments_data():
    """Mock experiment data for testing."""
    return [
        {
            "id": "exp-001",
            "title": "Test Experiment 1",
            "date": "2026-01-17",
            "verified": True,
            "path": "_experiments/test_exp_1.json",
        },
        {
            "id": "exp-002",
            "title": "Test Experiment 2",
            "date": "2026-01-16",
            "verified": False,
            "path": "_experiments/test_exp_2.json",
        },
    ]


@pytest.fixture
def sample_proof_cases_data():
    """Mock proof case data for testing."""
    return [
        {
            "id": "proof-001",
            "title": "Test Proof Case 1",
            "verdict": "PROVEN",
            "date": "2026-01-17",
            "path": "_work_efforts/proof_cases/case_20260117_001.md",
        },
        {
            "id": "proof-002",
            "title": "Test Proof Case 2",
            "verdict": "PENDING",
            "date": "2026-01-16",
            "path": "_work_efforts/proof_cases/case_20260116_001.md",
        },
    ]


@pytest.fixture
def sample_session_history_files(temp_project_path):
    """Create mock session history HTML files."""
    history_dir = temp_project_path / "_work_efforts"
    history_dir.mkdir(parents=True, exist_ok=True)

    # Create sample HTML files
    files = []
    for i in range(3):
        filename = f"show_me_20260117_120{i}00.html"
        filepath = history_dir / filename
        filepath.write_text(f"<html><body>Session {i}</body></html>")
        files.append(filepath)

    yield files
