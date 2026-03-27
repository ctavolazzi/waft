from fastapi.testclient import TestClient

from src.waft.api.routes import oracle as oracle_routes
from src.waft.api.routes import pantheon_oracle_cycle


class _FakeOracle:
    def __init__(self, project_path):
        self.project_path = project_path

    def provide_guidance(self, question: str, show_thinking: bool = False):
        if "Which risk should be controlled first" in question:
            return {
                "recommendation": "[INVESTIGATE] Prioritize schema mismatch first.",
                "reflection": {"summary": "Risk-oriented review."},
                "check": {"decision": "investigate", "confidence": 0.3},
                "timestamp": "2026-03-04T12:00:00Z",
            }
        return {
            "recommendation": "[PROCEED] Implement state machine first.",
            "reflection": {"summary": "Order-oriented review."},
            "check": {"decision": "proceed", "confidence": 0.8},
            "timestamp": "2026-03-04T12:00:00Z",
        }


class _FakeProfileOracle:
    def __init__(self, project_path):
        self.project_path = project_path

    def get_personality_info(self):
        return {
            "name": "The Oracle",
            "type": "balanced",
            "title": "Epistemic Intelligence System",
            "traits": {"wisdom": 0.9},
            "communication_style": {"tone": "calm"},
        }

    def get_epistemic_state(self):
        return {
            "ready": True,
            "has_context": True,
            "message": "Empirica ready with epistemic context",
            "findings": [{"insight": "x"}],
            "unknowns": [{"unknown": "y"}],
            "goals": [{"goal": "z"}],
            "timestamp": "2026-03-04T12:00:00Z",
        }


class _FakeKarmaMerchant:
    def __init__(self, project_path):
        self.project_path = project_path

    def access_akasha(self, soul_id: str):
        return {
            "soul_id": soul_id,
            "total_karma": 7.5,
            "lifetimes": [{"id": "1"}, {"id": "2"}],
            "last_incarnation": {"life_path": "sage"},
            "memory_fragments": [{"x": 1}, {"x": 2}, {"x": 3}],
        }


def test_oracle_cycle_run_list_get(test_client: TestClient, monkeypatch):
    monkeypatch.setattr(pantheon_oracle_cycle, "TheOracle", _FakeOracle)
    run_res = test_client.post(
        "/api/pantheon/oracle-cycle/run",
        json={"objective": "Pantheon cycle test"},
    )
    assert run_res.status_code == 200
    body = run_res.json()
    assert body["objective"] == "Pantheon cycle test"
    assert body["order_decision"] == "PROCEED"
    assert body["risk_decision"] == "INVESTIGATE"
    assert len(body["timeline"]) == 2

    list_res = test_client.get("/api/pantheon/oracle-cycle/runs")
    assert list_res.status_code == 200
    assert any(item["run_id"] == body["run_id"] for item in list_res.json())

    get_res = test_client.get(f"/api/pantheon/oracle-cycle/runs/{body['run_id']}")
    assert get_res.status_code == 200
    assert get_res.json()["objective"] == "Pantheon cycle test"


def test_oracle_cycle_run_with_output_dir(test_client: TestClient, monkeypatch, temp_project_path):
    monkeypatch.setattr(pantheon_oracle_cycle, "TheOracle", _FakeOracle)
    output_dir = temp_project_path / "custom_oracle_runs"
    run_res = test_client.post(
        "/api/pantheon/oracle-cycle/run",
        json={"objective": "Pantheon explicit output test", "output_dir": str(output_dir)},
    )
    assert run_res.status_code == 200
    body = run_res.json()
    run_file = output_dir / f"{body['run_id']}.json"
    assert run_file.exists()
    assert (output_dir / "index.jsonl").exists()

    default_file = temp_project_path / "_pantheon" / "oracle_cycle" / "runs" / f"{body['run_id']}.json"
    assert not default_file.exists()

    list_default_res = test_client.get("/api/pantheon/oracle-cycle/runs")
    assert list_default_res.status_code == 200
    assert not any(item["run_id"] == body["run_id"] for item in list_default_res.json())

    list_explicit_res = test_client.get(f"/api/pantheon/oracle-cycle/runs?output_dir={output_dir}")
    assert list_explicit_res.status_code == 200
    assert any(item["run_id"] == body["run_id"] for item in list_explicit_res.json())

    get_explicit_res = test_client.get(
        f"/api/pantheon/oracle-cycle/runs/{body['run_id']}?output_dir={output_dir}"
    )
    assert get_explicit_res.status_code == 200
    assert get_explicit_res.json()["run_id"] == body["run_id"]


def test_oracle_profile_endpoint_shape(test_client: TestClient, monkeypatch):
    monkeypatch.setattr(oracle_routes, "TheOracle", _FakeProfileOracle)
    monkeypatch.setattr(oracle_routes, "KarmaMerchant", _FakeKarmaMerchant)

    no_soul_res = test_client.get("/api/oracle/profile")
    assert no_soul_res.status_code == 200
    no_soul_body = no_soul_res.json()
    assert no_soul_body["oracle"]["name"] == "The Oracle"
    assert no_soul_body["epistemic"]["ready"] is True
    assert no_soul_body["reincarnation"]["soul_id"] is None
    assert no_soul_body["reincarnation"]["lifetimes_count"] == 0

    soul_res = test_client.get("/api/oracle/profile?soul_id=tam_001")
    assert soul_res.status_code == 200
    soul_body = soul_res.json()
    assert soul_body["reincarnation"]["soul_id"] == "tam_001"
    assert soul_body["reincarnation"]["total_karma"] == 7.5
    assert soul_body["reincarnation"]["lifetimes_count"] == 2
    assert soul_body["reincarnation"]["memory_fragments_count"] == 3


def test_oracle_cycle_ui_routes(test_client: TestClient):
    html_res = test_client.get("/api/pantheon/oracle-cycle/ui")
    assert html_res.status_code == 200
    assert "Pantheon Oracle Cycle" in html_res.text

    js_res = test_client.get("/api/pantheon/oracle-cycle/ui/app.mjs")
    assert js_res.status_code == 200
    assert "Run Oracle Cycle" in js_res.text

    profile_html_res = test_client.get("/api/pantheon/oracle-cycle/ui/profile")
    assert profile_html_res.status_code == 200
    assert "Oracle Profile" in profile_html_res.text

    profile_js_res = test_client.get("/api/pantheon/oracle-cycle/ui/profile/app.mjs")
    assert profile_js_res.status_code == 200
    assert "Dedicated profile surface" in profile_js_res.text
