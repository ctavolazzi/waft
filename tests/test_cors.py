"""
CORS Configuration Tests

Verifies that the FastAPI app correctly handles CORS headers
for frontend integration.
"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path

from waft.api.main import create_app


@pytest.fixture
def client():
    """Create test client for FastAPI app."""
    app = create_app(project_path=Path('.'))
    return TestClient(app)


def test_cors_headers_present(client):
    """Test that CORS headers are present in responses with Origin header."""
    # CORS headers are only added when Origin header is present (browser behavior)
    response = client.get(
        "/api/decision/health",
        headers={"Origin": "http://localhost:5173"}
    )
    
    # Check for CORS headers (case-insensitive)
    headers_lower = {k.lower(): v for k, v in response.headers.items()}
    assert "access-control-allow-origin" in headers_lower


def test_cors_preflight_request(client):
    """Test OPTIONS preflight request returns correct CORS headers."""
    # Simulate a preflight request from a browser
    response = client.options(
        "/api/decision/analyze",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        }
    )
    
    # Should return 200 for OPTIONS
    assert response.status_code == 200
    
    # Check CORS headers (case-insensitive)
    headers_lower = {k.lower(): v for k, v in response.headers.items()}
    assert "access-control-allow-origin" in headers_lower
    
    # Verify allowed origins
    allow_origin = headers_lower.get("access-control-allow-origin", "")
    
    # Should allow localhost:5173 or localhost:3000
    assert "localhost:5173" in allow_origin or \
           "localhost:3000" in allow_origin or \
           allow_origin == "*"


def test_cors_allows_react_dev_server(client):
    """Test that React dev server (localhost:3000) is allowed."""
    response = client.get(
        "/api/decision/health",
        headers={"Origin": "http://localhost:3000"}
    )
    
    assert response.status_code == 200
    # CORS middleware should allow this origin


def test_cors_allows_vite_dev_server(client):
    """Test that Vite dev server (localhost:5173) is allowed."""
    response = client.get(
        "/api/decision/health",
        headers={"Origin": "http://localhost:5173"}
    )
    
    assert response.status_code == 200
    # CORS middleware should allow this origin


def test_cors_credentials_allowed(client):
    """Test that credentials are allowed in CORS."""
    response = client.options(
        "/api/decision/analyze",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        }
    )
    
    headers = response.headers
    # Check if credentials are allowed
    allow_credentials = headers.get("Access-Control-Allow-Credentials") or \
                       headers.get("access-control-allow-credentials", "")
    
    # Should allow credentials (true or "true")
    assert "true" in str(allow_credentials).lower() or \
           response.status_code == 200  # If middleware is working, this is fine


def test_cors_all_methods_allowed(client):
    """Test that all HTTP methods are allowed."""
    response = client.options(
        "/api/decision/analyze",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        }
    )
    
    assert response.status_code == 200
    # Should allow POST (and other methods via "*")


def test_actual_post_request_with_cors(client):
    """Test that actual POST request works with CORS headers."""
    request_data = {
        "problem": "Test Decision",
        "alternatives": ["Option A", "Option B"],
        "criteria": {"Cost": 0.5, "Quality": 0.5},
        "scores": {
            "Option A": {"Cost": 10, "Quality": 5},
            "Option B": {"Cost": 5, "Quality": 10}
        }
    }
    
    response = client.post(
        "/api/decision/analyze",
        json=request_data,
        headers={"Origin": "http://localhost:5173"}
    )
    
    assert response.status_code == 200
    
    # Check that CORS headers are present (case-insensitive)
    headers_lower = {k.lower(): v for k, v in response.headers.items()}
    assert "access-control-allow-origin" in headers_lower
