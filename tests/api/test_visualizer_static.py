from fastapi.testclient import TestClient

from src.waft.api.main import create_app


def test_static_spa_routes_use_fallback(temp_project_path):
    static_dir = temp_project_path / "visualizer_build"
    static_dir.mkdir()
    (static_dir / "index.html").write_text("<html><body>home</body></html>", encoding="utf-8")
    (static_dir / "200.html").write_text("<html><body>spa fallback</body></html>", encoding="utf-8")

    client = TestClient(create_app(temp_project_path, static_dir=static_dir))

    response = client.get("/projects")

    assert response.status_code == 200
    assert "spa fallback" in response.text


def test_static_spa_keeps_api_routes_available(temp_project_path):
    static_dir = temp_project_path / "visualizer_build"
    static_dir.mkdir()
    (static_dir / "index.html").write_text("<html><body>home</body></html>", encoding="utf-8")
    (static_dir / "200.html").write_text("<html><body>spa fallback</body></html>", encoding="utf-8")

    client = TestClient(create_app(temp_project_path, static_dir=static_dir))

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_static_missing_asset_stays_404(temp_project_path):
    static_dir = temp_project_path / "visualizer_build"
    static_dir.mkdir()
    (static_dir / "index.html").write_text("<html><body>home</body></html>", encoding="utf-8")
    (static_dir / "200.html").write_text("<html><body>spa fallback</body></html>", encoding="utf-8")

    client = TestClient(create_app(temp_project_path, static_dir=static_dir))

    response = client.get("/missing.js")

    assert response.status_code == 404
