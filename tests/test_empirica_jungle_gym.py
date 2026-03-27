from pathlib import Path

from scripts.empirica_jungle_gym import run_simulated_scenario


def test_simulated_mcp_scenario_passes():
    result = run_simulated_scenario(Path("."), "mcp")
    assert result["ok"] is True
    assert result["transport"] == "mcp"
    assert result["check_decision"] == "proceed"


def test_simulated_cli_fallback_scenario_passes():
    result = run_simulated_scenario(Path("."), "cli")
    assert result["ok"] is True
    assert result["transport"] == "cli"
    assert result["check_decision"] == "proceed"


def test_simulated_degraded_scenario_reports_expected_failure():
    result = run_simulated_scenario(Path("."), "degraded")
    assert result["ok"] is True
    assert result["transport"] == "degraded"
    assert result["boot_ok"] is False

