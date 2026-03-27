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


def test_ollama_runtime_ui_endpoint(test_client: TestClient):
    response = test_client.get("/api/runtime-ui")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "WAFT Ollama Runtime UI" in response.text
    assert "/api/generate" in response.text
    assert "/api/chat" in response.text
    assert "/api/history" in response.text
    assert "Run Demo Flow" in response.text
    assert "Visual Diff" in response.text
    assert "Added Events" in response.text


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


def test_ollama_chat_endpoint_non_stream(test_client: TestClient):
    payload = {
        "model": "waft-echo:latest",
        "messages": [{"role": "user", "content": "hello chat"}],
        "stream": False,
    }
    response = test_client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["model"] == "waft-echo:latest"
    assert data["done"] is True
    assert data["message"]["role"] == "assistant"
    assert len(data["message"]["content"]) > 0


def test_ollama_chat_endpoint_stream(test_client: TestClient):
    payload = {
        "model": "waft-echo:latest",
        "messages": [{"role": "user", "content": "hello chat stream"}],
        "stream": True,
    }
    response = test_client.post("/api/chat", json=payload)
    assert response.status_code == 200
    assert "application/x-ndjson" in response.headers.get("content-type", "")

    lines = [line for line in response.text.splitlines() if line.strip()]
    assert len(lines) >= 2
    first = json.loads(lines[0])
    last = json.loads(lines[-1])
    assert first["done"] is False
    assert last["done"] is True


def test_ollama_runtime_history_persists_events(test_client: TestClient, temp_project_path):
    generate_payload = {"model": "waft-echo:latest", "prompt": "persist generate", "stream": False}
    chat_payload = {
        "model": "waft-echo:latest",
        "messages": [{"role": "user", "content": "persist chat"}],
        "stream": False,
    }

    generate_response = test_client.post("/api/generate", json=generate_payload)
    chat_response = test_client.post("/api/chat", json=chat_payload)
    assert generate_response.status_code == 200
    assert chat_response.status_code == 200

    history_response = test_client.get("/api/history?limit=10")
    assert history_response.status_code == 200
    history_data = history_response.json()
    assert "events" in history_data
    assert len(history_data["events"]) >= 2

    endpoints = [event["endpoint"] for event in history_data["events"]]
    assert "/api/generate" in endpoints
    assert "/api/chat" in endpoints

    history_file = temp_project_path / ".waft" / "ollama_runtime.jsonl"
    assert history_file.exists()
    saved_lines = [line for line in history_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(saved_lines) >= 2
