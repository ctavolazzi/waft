import json
from pathlib import Path

from waft.pantheon.pondering_one import ThePonderingOne


def test_ensure_brain_realm_writes_project_mcp_config(tmp_path):
    pondering = ThePonderingOne(project_path=tmp_path)
    pondering._preferred_mcp_command = lambda: "/bin/echo"  # type: ignore[method-assign]

    status = pondering.ensure_brain_realm()
    mcp_file = tmp_path / ".cursor" / "mcp.json"

    assert mcp_file.exists()
    assert status["mcp_server_configured"] is True
    data = json.loads(mcp_file.read_text())
    server = data["mcpServers"]["empirica-epistemic"]
    assert server["command"] == "/bin/echo"
    assert "--workspace" in server["args"]


def test_get_brain_realm_status_reports_cli_fallback_when_mcp_missing(tmp_path):
    pondering = ThePonderingOne(project_path=tmp_path)
    pondering._preferred_mcp_command = lambda: None  # type: ignore[method-assign]

    # no mcp config file -> should settle on cli or degraded depending on local env
    status = pondering.get_brain_realm_status()
    assert status["transport"] in {"cli", "degraded"}
    if status["transport"] == "cli":
        assert status["fallback_reason"] == "mcp unavailable; using cli backend"

