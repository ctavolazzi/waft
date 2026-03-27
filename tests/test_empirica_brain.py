from pathlib import Path
from unittest.mock import MagicMock

from waft.core.empirica_brain import EmpiricaBrain


def test_build_narrative_prompt_contains_contract():
    brain = EmpiricaBrain(project_path=Path("."), empirica_manager=MagicMock())
    prompt = brain.build_narrative_prompt("Refactor the compiler cache layer")

    assert "EMPIRICA BRAIN" in prompt
    assert "PREFLIGHT" in prompt
    assert "CHECK gate" in prompt
    assert "POSTFLIGHT" in prompt
    assert "Refactor the compiler cache layer" in prompt


def test_run_cascade_cycle_proceed_path():
    manager = MagicMock()
    manager.ensure_ready.return_value = {"ready": True, "message": "ok"}
    manager.create_session.return_value = "session-123"
    manager.submit_preflight.return_value = True
    manager.check_submit.return_value = "PROCEED"
    manager.submit_postflight.return_value = True

    brain = EmpiricaBrain(project_path=Path("."), empirica_manager=manager)
    result = brain.run_cascade_cycle("Add runtime diagnostics")

    assert result.proceed is True
    assert result.session_id == "session-123"
    assert result.gate_result == "PROCEED"
    assert result.preflight_submitted is True
    assert result.postflight_submitted is True
    manager.submit_postflight.assert_called_once()


def test_run_cascade_cycle_halt_gate_stops_postflight():
    manager = MagicMock()
    manager.ensure_ready.return_value = {"ready": True, "message": "ok"}
    manager.create_session.return_value = "session-xyz"
    manager.submit_preflight.return_value = True
    manager.check_submit.return_value = "HALT"

    brain = EmpiricaBrain(project_path=Path("."), empirica_manager=manager)
    result = brain.run_cascade_cycle("Change auth flow")

    assert result.proceed is False
    assert result.gate_result == "HALT"
    assert result.postflight_submitted is False
    manager.submit_postflight.assert_not_called()
