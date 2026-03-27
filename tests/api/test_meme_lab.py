import json
from pathlib import Path

from fastapi.testclient import TestClient


def test_meme_lab_ui_endpoint(test_client: TestClient):
    response = test_client.get("/api/meme-lab")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "WAFT Meme Kitchen" in response.text
    assert "ReactDOM.createRoot" in response.text
    assert "/api/meme-lab/generate-meme" in response.text
    assert "/api/meme-lab/generate-dossier" in response.text
    assert "/api/meme-lab/cookbook" in response.text


def test_generate_meme_endpoint_returns_file_url(
    test_client: TestClient, temp_project_path: Path, monkeypatch
):
    from src.waft.api.routes import meme_lab

    def fake_generate(self, request):
        output_path = Path(request.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(b"fake-image")
        return output_path

    monkeypatch.setattr(meme_lab.MemeGenerator, "generate", fake_generate)
    response = test_client.post(
        "/api/meme-lab/generate-meme",
        json={"prompt": "test meme prompt", "mode": "mixed"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "file_url" in data
    assert data["file_url"].startswith("/api/meme-lab/file?path=")

    file_response = test_client.get(data["file_url"])
    assert file_response.status_code == 200
    assert file_response.content == b"fake-image"


def test_cookbook_endpoint_returns_recipe_list(test_client: TestClient):
    response = test_client.get("/api/meme-lab/cookbook")
    assert response.status_code == 200
    data = response.json()
    assert "recipes" in data
    assert len(data["recipes"]) >= 1
    assert "name" in data["recipes"][0]
    assert "style" in data["recipes"][0]


def test_templates_endpoint_returns_mainstream_and_more(test_client: TestClient):
    response = test_client.get("/api/meme-lab/templates")
    assert response.status_code == 200
    data = response.json()
    assert "templates" in data
    assert len(data["templates"]) >= 8
    first = data["templates"][0]
    assert "name" in first
    assert "style" in first
    assert "category" in first


def test_soundboard_endpoint_returns_8_buttons(test_client: TestClient, monkeypatch):
    from src.waft.api.routes import meme_lab

    def fake_generate(self, request):
        output_path = Path(request.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(b"btn")
        return output_path

    monkeypatch.setattr(meme_lab.MemeGenerator, "generate", fake_generate)
    response = test_client.get("/api/meme-lab/soundboard")
    assert response.status_code == 200
    data = response.json()
    assert "buttons" in data
    assert len(data["buttons"]) == 8
    assert "template" in data["buttons"][0]
    assert "image_url" in data["buttons"][0]


def test_cook_template_generates_random_template_image(test_client: TestClient, monkeypatch):
    from src.waft.api.routes import meme_lab

    def fake_generate(self, request):
        output_path = Path(request.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(b"template-image")
        return output_path

    monkeypatch.setattr(meme_lab.MemeGenerator, "generate", fake_generate)
    response = test_client.post(
        "/api/meme-lab/cook-template/drake",
        json={"temperature": 1.1, "top_k": 9, "creativity": 0.8, "punchiness": 0.7, "absurdity": 0.6},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["template"] == "drake"
    assert "file_url" in data
    file_response = test_client.get(data["file_url"])
    assert file_response.status_code == 200
    assert file_response.content == b"template-image"


def test_generate_dossier_endpoint_returns_pdf_and_artifacts(
    test_client: TestClient, temp_project_path: Path, monkeypatch
):
    from src.waft.api.routes import meme_lab

    def fake_generate_dossier(project_path, prompt, count, seed, output_pdf, artifacts_dir):
        output_pdf.parent.mkdir(parents=True, exist_ok=True)
        output_pdf.write_bytes(b"fake-pdf")
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        artifact_path = artifacts_dir / "artifact_01.jpg"
        artifact_path.write_bytes(b"fake-artifact")
        records = [
            {
                "index": 1,
                "success": True,
                "output_path": str(artifact_path),
            }
        ]
        return output_pdf, records

    monkeypatch.setattr(meme_lab, "generate_dossier", fake_generate_dossier)
    response = test_client.post(
        "/api/meme-lab/generate-dossier",
        json={"prompt": "test dossier prompt", "count": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["pdf_url"].startswith("/api/meme-lab/file?path=")
    assert data["successes"] == 1
    assert len(data["artifacts"]) == 1

    pdf_response = test_client.get(data["pdf_url"])
    assert pdf_response.status_code == 200
    assert pdf_response.content == b"fake-pdf"


def test_history_endpoint_returns_recent_generated_items(test_client: TestClient, monkeypatch):
    from src.waft.api.routes import meme_lab

    def fake_generate(self, request):
        output_path = Path(request.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(b"hist-image")
        return output_path

    monkeypatch.setattr(meme_lab.MemeGenerator, "generate", fake_generate)
    create_response = test_client.post(
        "/api/meme-lab/generate-meme",
        json={"prompt": "history test meme", "mode": "mixed", "template": "drake"},
    )
    assert create_response.status_code == 200

    history_response = test_client.get("/api/meme-lab/history?limit=5")
    assert history_response.status_code == 200
    data = history_response.json()
    assert "history" in data
    assert len(data["history"]) >= 1
    first = data["history"][0]
    assert "file_url" in first
    assert "relative_path" in first


def test_file_endpoint_blocks_non_reports_path(test_client: TestClient):
    response = test_client.get("/api/meme-lab/file?path=README.md")
    assert response.status_code == 403


def test_generate_meme_validation_rejects_out_of_range_values(test_client: TestClient):
    response = test_client.post(
        "/api/meme-lab/generate-meme",
        json={"prompt": "bad", "temperature": 3.5, "top_k": 999, "creativity": -0.1},
    )
    assert response.status_code == 422


def test_cook_template_unknown_template_returns_404(test_client: TestClient):
    response = test_client.post(
        "/api/meme-lab/cook-template/not_a_template",
        json={"temperature": 1.0, "top_k": 8, "creativity": 0.7, "punchiness": 0.7, "absurdity": 0.4},
    )
    assert response.status_code == 404
    assert "unknown template" in response.text


def test_file_endpoint_rejects_out_of_root_path_with_400(test_client: TestClient):
    response = test_client.get("/api/meme-lab/file?path=../../../../etc/passwd")
    assert response.status_code == 400


def test_file_endpoint_rejects_missing_file_with_404(test_client: TestClient):
    response = test_client.get(
        "/api/meme-lab/file?path=_work_efforts/reports/meme_web_artifacts/does_not_exist.jpg"
    )
    assert response.status_code == 404


def test_history_reader_skips_malformed_and_invalid_entries(
    test_client: TestClient, temp_project_path: Path
):
    history_path = temp_project_path / "_work_efforts" / "reports" / "meme_web_artifacts" / "meme_history.jsonl"
    history_path.parent.mkdir(parents=True, exist_ok=True)
    valid_artifact = temp_project_path / "_work_efforts" / "reports" / "meme_web_artifacts" / "valid.jpg"
    valid_artifact.write_bytes(b"ok")
    history_path.write_text(
        "\n".join(
            [
                "{not-json",
                json.dumps({"created_at": "2026-03-03T00:00:00Z", "relative_path": ""}),
                json.dumps(
                    {
                        "created_at": "2026-03-03T00:00:00Z",
                        "relative_path": "../../outside.jpg",
                    }
                ),
                json.dumps(
                    {
                        "created_at": "2026-03-03T00:00:00Z",
                        "relative_path": "_work_efforts/reports/meme_web_artifacts/missing.jpg",
                    }
                ),
                json.dumps(
                    {
                        "created_at": "2026-03-03T00:00:00Z",
                        "relative_path": "_work_efforts/reports/meme_web_artifacts/valid.jpg",
                        "template": "drake",
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    response = test_client.get("/api/meme-lab/history?limit=20")
    assert response.status_code == 200
    data = response.json()
    assert len(data["history"]) == 1
    assert data["history"][0]["relative_path"].endswith("valid.jpg")


def test_history_append_is_bounded(temp_project_path: Path):
    from src.waft.api.routes import meme_lab

    old_max = meme_lab.MAX_HISTORY_ENTRIES
    meme_lab.MAX_HISTORY_ENTRIES = 5
    try:
        for i in range(9):
            meme_lab._append_history_entry(
                temp_project_path,
                {
                    "created_at": f"2026-01-01T00:00:0{i}Z",
                    "template": "drake",
                    "seed": i,
                    "output_path": f"/tmp/meme_{i}.jpg",
                    "relative_path": f"_work_efforts/reports/meme_web_artifacts/meme_{i}.jpg",
                },
            )
        history_path = temp_project_path / "_work_efforts" / "reports" / "meme_web_artifacts" / "meme_history.jsonl"
        lines = history_path.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 5
    finally:
        meme_lab.MAX_HISTORY_ENTRIES = old_max
