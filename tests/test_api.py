"""
Tests for Decision Engine API endpoints.

Tests the FastAPI integration with the hardened Decision Engine.
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


def test_health_endpoint(client):
    """Test the /api/decision/health endpoint."""
    response = client.get("/api/decision/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "1.0"
    assert data["core"] == "diamond_plated"
    assert data["engine"] == "iron_core"


def test_analyze_endpoint_scenario_a(client):
    """Test /api/decision/analyze with Scenario A (Dominant Option)."""
    request_data = {
        "problem": "Test Decision - Dominant Option",
        "alternatives": ["SuperCar", "Junker"],
        "criteria": {
            "Speed": 0.5,
            "Comfort": 0.5
        },
        "scores": {
            "SuperCar": {"Speed": 10.0, "Comfort": 10.0},
            "Junker": {"Speed": 1.0, "Comfort": 1.0}
        },
        "methodology": "WSM"
    }
    
    response = client.post("/api/decision/analyze", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify structure
    assert "rankings" in data
    assert "recommendation" in data
    assert "detailed_analysis" in data
    assert "sensitivity_warnings" in data
    assert "is_robust" in data
    
    # Verify SuperCar wins (dominant option)
    assert len(data["rankings"]) == 2
    assert data["rankings"][0]["name"] == "SuperCar"
    assert data["rankings"][0]["rank"] == 1
    assert data["rankings"][0]["score"] == 10.0
    assert data["recommendation"] == "SuperCar"
    
    # Verify detailed analysis
    assert len(data["detailed_analysis"]) == 2
    supercar_analysis = next(a for a in data["detailed_analysis"] if a["name"] == "SuperCar")
    assert supercar_analysis["total_score"] == 10.0
    assert supercar_analysis["rank"] == 1


def test_analyze_endpoint_invalid_data(client):
    """Test /api/decision/analyze with invalid data (should return 400)."""
    request_data = {
        "problem": "Test Decision",
        "alternatives": ["Option A"],
        "criteria": {
            "Cost": 0.99  # Doesn't sum to 1.0
        },
        "scores": {
            "Option A": {"Cost": 10.0}
        }
    }
    
    response = client.post("/api/decision/analyze", json=request_data)
    
    assert response.status_code == 400
    # Error message comes from Iron Core validation
    assert "sum to 1.0" in response.json()["detail"]


def test_analyze_endpoint_missing_scores(client):
    """Test /api/decision/analyze with missing scores (should return 400)."""
    request_data = {
        "problem": "Test Decision",
        "alternatives": ["Option A", "Option B"],
        "criteria": {
            "Cost": 1.0
        },
        "scores": {
            "Option A": {"Cost": 10.0}
            # Missing Option B score
        }
    }
    
    response = client.post("/api/decision/analyze", json=request_data)
    
    assert response.status_code == 400
    assert "Missing score" in response.json()["detail"]


def test_analyze_endpoint_sensitivity_analysis(client):
    """Test that sensitivity analysis works via API."""
    request_data = {
        "problem": "Test Decision with Sensitivity",
        "alternatives": ["Ferrari", "Toyota"],
        "criteria": {
            "Cost": 0.9,
            "Fun": 0.1
        },
        "scores": {
            "Ferrari": {"Cost": 1, "Fun": 10},
            "Toyota": {"Cost": 10, "Fun": 5}
        },
        "show_sensitivity": True
    }
    
    response = client.post("/api/decision/analyze", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    # Should have sensitivity information
    assert "is_robust" in data
    # Toyota should win (Cost-focused)
    assert data["rankings"][0]["name"] == "Toyota"


def test_analyze_endpoint_dirty_data_sanitization(client):
    """Test that dirty data (strings, whitespace) is sanitized via API."""
    request_data = {
        "problem": "Test Decision",
        "alternatives": ["  Option A  ", "Option B"],
        "criteria": {
            "  Cost  ": "0.5",  # String weight, whitespace
            "Quality": 0.5
        },
        "scores": {
            "  Option A  ": {"  Cost  ": "10", "Quality": 5},  # String scores, whitespace
            "Option B": {"  Cost  ": 5, "Quality": 9}
        }
    }
    
    response = client.post("/api/decision/analyze", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify sanitization worked (names should be trimmed)
    assert len(data["rankings"]) == 2
    # Option A should be sanitized (whitespace trimmed)
    option_a = next(r for r in data["rankings"] if "Option A" in r["name"])
    assert option_a["name"] == "Option A"  # Whitespace trimmed
