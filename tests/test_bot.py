"""Tests for Bot and EmpericaHandler."""

from unittest.mock import MagicMock, patch
from pathlib import Path

from waft.core.empirica_handler import (
    EmpericaHandler,
    GateDecision,
    Phase,
    CheckResult,
    HandlerState,
)
from waft.core.bot import Bot, BotConfig, Inventory, Journal, Port


def _mock_cli_json(command, stdin_data=None, extra_args=None):
    responses = {
        "project-list": {"ok": True, "projects": [{"id": "test-pid", "name": "test", "trajectory_path": "/tmp/test"}]},
        "project-create": {"ok": True, "project_id": "test-pid"},
        "session-create": {"ok": True, "session_id": "test-sid"},
        "preflight-submit": {"ok": True, "transaction_id": "test-tid"},
        "check-submit": {"ok": True, "decision": "proceed", "checkpoint_id": "test-cpid"},
        "postflight-submit": {"ok": True},
    }
    return responses.get(command, {"ok": False, "error": f"unknown command {command}"})


class TestGateDecision:
    def test_from_str_proceed(self):
        assert GateDecision.from_str("proceed") == GateDecision.PROCEED

    def test_from_str_halt(self):
        assert GateDecision.from_str("halt") == GateDecision.HALT

    def test_from_str_none(self):
        assert GateDecision.from_str(None) == GateDecision.UNKNOWN

    def test_from_str_garbage(self):
        assert GateDecision.from_str("xyzzy") == GateDecision.UNKNOWN


class TestCheckResult:
    def test_proceed_property(self):
        cr = CheckResult(decision=GateDecision.PROCEED, session_id="s", checkpoint_id="c", raw={})
        assert cr.proceed is True
        assert cr.halted is False

    def test_halt_property(self):
        cr = CheckResult(decision=GateDecision.HALT, session_id="s", checkpoint_id="c", raw={})
        assert cr.proceed is False
        assert cr.halted is True


class TestHandlerState:
    def test_defaults(self):
        s = HandlerState()
        assert s.phase == Phase.UNBOOTED
        assert s.session_id is None
        assert s.vectors == {}
        assert s.findings == []


class TestInventory:
    def test_put_get(self):
        inv = Inventory()
        inv.put("key", "value")
        assert inv.get("key") == "value"
        assert inv.has("key") is True
        assert inv.get("missing", "default") == "default"

    def test_keys(self):
        inv = Inventory()
        inv.put("a", 1)
        inv.put("b", 2)
        assert sorted(inv.keys()) == ["a", "b"]


class TestPort:
    def test_receive_and_drain(self):
        p = Port()
        p.receive("hello")
        p.receive("world")
        messages = p.drain_inbox()
        assert messages == ["hello", "world"]
        assert p.drain_inbox() == []

    def test_emit_and_drain(self):
        p = Port()
        p.emit("response")
        messages = p.drain_outbox()
        assert messages == ["response"]
        assert p.drain_outbox() == []


class TestEmpericaHandler:
    @patch.object(EmpericaHandler, "_cli_json", side_effect=_mock_cli_json)
    @patch.object(EmpericaHandler, "_ensure_instance_file")
    def test_boot_success(self, mock_instance, mock_cli):
        h = EmpericaHandler(project_path="/tmp/test", instance_id="test")
        result = h.boot()
        assert result.ok is True
        assert result.session_id == "test-sid"
        assert h.phase == Phase.BOOTED

    @patch.object(EmpericaHandler, "_cli_json", side_effect=_mock_cli_json)
    @patch.object(EmpericaHandler, "_ensure_instance_file")
    def test_full_lifecycle(self, mock_instance, mock_cli):
        h = EmpericaHandler(project_path="/tmp/test", instance_id="test")
        h.boot()
        assert h.phase == Phase.BOOTED

        h.preflight(reasoning="test preflight")
        assert h.phase == Phase.PREFLIGHT

        cr = h.check(reasoning="test check")
        assert cr.proceed is True
        assert h.phase == Phase.ACTIVE

        h.postflight(reasoning="test postflight")
        assert h.phase == Phase.POSTFLIGHT


class TestBot:
    @patch.object(EmpericaHandler, "_cli_json", side_effect=_mock_cli_json)
    @patch.object(EmpericaHandler, "_ensure_instance_file")
    def test_bot_lifecycle(self, mock_instance, mock_cli):
        bot = Bot(BotConfig(project_path="/tmp/test", instance_id="test-bot"))
        assert bot.boot() is True
        assert bot.is_ready is True

        bot.preflight(reasoning="starting")
        cr = bot.check(reasoning="checking")
        assert cr.proceed is True

        bot.journal.finding("discovered X", impact=0.8)
        bot.inventory.put("artifact", {"data": 123})

        bot.postflight(reasoning="done")
        bot.close()
        assert bot.phase == Phase.CLOSED
        assert len(bot.journal.entries) >= 4
        assert bot.inventory.has("artifact")
