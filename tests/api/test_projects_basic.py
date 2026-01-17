"""
Basic tests for Projects API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path


def test_create_project(test_client: TestClient, auth_token: str):
    """Test creating a project via POST endpoint."""
    response = test_client.post(
        "/api/projects",
        json={
            "title": "Test Project",
            "description": "A test project",
            "tags": ["test", "api"],
            "status": "planning"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Project"
    assert data["description"] == "A test project"
    assert "project_id" in data
    assert data["status"] == "planning"


def test_get_projects(test_client: TestClient):
    """Test listing projects via GET endpoint."""
    response = test_client.get("/api/projects")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_project_requires_auth(test_client: TestClient):
    """Test that POST requires authentication."""
    response = test_client.post(
        "/api/projects",
        json={
            "title": "Test Project",
            "description": "A test project"
        }
    )
    assert response.status_code == 401


def test_get_project_not_found(test_client: TestClient):
    """Test getting non-existent project returns 404."""
    response = test_client.get("/api/projects/nonexistent")
    assert response.status_code == 404
