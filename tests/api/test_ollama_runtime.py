import json

from fastapi.testclient import TestClient


def test_health_endpoint_available(test_client: TestClient):
    response = test_client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_ollama_tags_endpoint(test_client: TestClient):
    response = test_client.get("/api/tags")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert len(data["models"]) >= 1
    assert data["models"][0]["name"].endswith(":latest")


def test_ollama_generate_endpoint_non_stream(test_client: TestClient):
    payload = {"model": "waft-echo:latest", "prompt": "hello waft", "stream": False}
    response = test_client.post("/api/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["model"] == "waft-echo:latest"
    assert data["done"] is True
    assert "response" in data
    assert len(data["response"]) > 0


def test_ollama_generate_endpoint_stream(test_client: TestClient):
    payload = {"model": "waft-echo:latest", "prompt": "hello stream", "stream": True}
    response = test_client.post("/api/generate", json=payload)
    assert response.status_code == 200
    assert "application/x-ndjson" in response.headers.get("content-type", "")

    lines = [line for line in response.text.splitlines() if line.strip()]
    assert len(lines) >= 2

    first = json.loads(lines[0])
    last = json.loads(lines[-1])
    assert first["done"] is False
    assert last["done"] is True
