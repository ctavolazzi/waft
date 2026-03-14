from fastapi.testclient import TestClient

CANONICAL_UI_PATH = (
    "_work_efforts/10-19_user_interface/10_unified_waft_interface/"
    "10.01_waft_control_center_unification.md"
)


def _seed_project(temp_project_path):
    (temp_project_path / "_pyrite" / "active").mkdir(parents=True, exist_ok=True)
    (temp_project_path / "_pyrite" / "backlog").mkdir(parents=True, exist_ok=True)
    (temp_project_path / "_pyrite" / "standards").mkdir(parents=True, exist_ok=True)
    (temp_project_path / "pyproject.toml").write_text(
        '[project]\nname = "waft-test"\nversion = "0.1.0"\n',
        encoding="utf-8",
    )
    (
        temp_project_path
        / "_work_efforts"
        / "10-19_user_interface"
        / "10_unified_waft_interface"
        / "10.01_waft_control_center_unification.md"
    ).parent.mkdir(parents=True, exist_ok=True)
    (
        temp_project_path
        / "_work_efforts"
        / "10-19_user_interface"
        / "10_unified_waft_interface"
        / "10.01_waft_control_center_unification.md"
    ).write_text("# Unified UI\n", encoding="utf-8")
    (temp_project_path / "_work_efforts" / "reports").mkdir(parents=True, exist_ok=True)
    (temp_project_path / "_work_efforts" / "reports" / "report_5050_test.md").write_text(
        "# Report\n", encoding="utf-8"
    )


def test_5050_session_exposes_canonical_ui_work_effort(test_client: TestClient, temp_project_path):
    _seed_project(temp_project_path)

    response = test_client.get("/api/5050/session")

    assert response.status_code == 200
    data = response.json()
    assert data["canonical_ui_work_effort"] == CANONICAL_UI_PATH
    assert data["summary"]["work_efforts"] >= 1
    assert any(
        item["path"].endswith("10.01_waft_control_center_unification.md")
        for item in data["artifacts"]
    )


def test_5050_timeline_returns_recent_artifacts(test_client: TestClient, temp_project_path):
    _seed_project(temp_project_path)

    response = test_client.get("/api/5050/timeline")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert any(event["path"].endswith("report_5050_test.md") for event in data["events"])


def test_5050_file_rejects_path_traversal(test_client: TestClient, temp_project_path):
    _seed_project(temp_project_path)

    response = test_client.get("/api/5050/file", params={"path": "../devlog.md"})

    assert response.status_code == 400
    assert response.json()["message"] == "Invalid path"


def test_5050_file_serves_report(test_client: TestClient, temp_project_path):
    _seed_project(temp_project_path)

    response = test_client.get(
        "/api/5050/file", params={"path": "_work_efforts/reports/report_5050_test.md"}
    )

    assert response.status_code == 200
    assert response.text == "# Report\n"
