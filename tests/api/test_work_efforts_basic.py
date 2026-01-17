"""
Basic tests for Work Efforts API endpoints.
"""

import pytest
from fastapi.testclient import TestClient


def test_create_work_effort(test_client: TestClient, auth_token: str):
    """Test creating a work effort via POST endpoint."""
    response = test_client.post(
        "/api/work-efforts",
        json={
            "title": "Test Work Effort",
            "description": "A test work effort",
            "status": "active",
            "tags": ["test"]
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Work Effort"
    assert data["status"] == "active"
    assert "id" in data
    assert data["id"].startswith("WE-")


def test_get_work_efforts(test_client: TestClient):
    """Test listing work efforts via GET endpoint."""
    response = test_client.get("/api/work-efforts")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)


def test_create_work_effort_requires_auth(test_client: TestClient):
    """Test that POST requires authentication."""
    response = test_client.post(
        "/api/work-efforts",
        json={
            "title": "Test Work Effort",
            "description": "A test work effort"
        }
    )
    assert response.status_code == 401


def test_get_work_effort_not_found(test_client: TestClient):
    """Test getting non-existent work effort returns 404."""
    response = test_client.get("/api/work-efforts/WE-000000-xxxx")
    assert response.status_code == 404
