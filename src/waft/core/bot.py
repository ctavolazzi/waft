"""
Bot — composable agent with Empirica-gated lifecycle.

    bot = Bot(BotConfig(project_path="/path/to/project"))
    bot.boot()
    bot.preflight("starting mission X")
    gate = bot.check("about to modify Y")
    if gate.proceed:
        bot.journal.log("did the thing")
    bot.postflight("completed mission X")
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .empirica_handler import (
    CheckResult,
    EmpericaHandler,
    GateDecision,
    Phase,
)


@dataclass
class BotConfig:
    project_path: str | Path
    instance_id: str = "waft-bot"
    ai_id: str = "waft-brain"
    default_vectors: dict[str, float] | None = None
    cli_timeout: int = 15


class Journal:
    """Structured log of findings, unknowns, and free-form entries."""

    def __init__(self, handler: EmpericaHandler) -> None:
        self._handler = handler
        self._entries: list[dict[str, Any]] = []

    def log(self, message: str, kind: str = "note") -> None:
        self._entries.append({"kind": kind, "message": message})

    def finding(self, text: str, impact: float = 0.5) -> bool:
        self._entries.append({"kind": "finding", "message": text, "impact": impact})
        return self._handler.log_finding(text, impact)

    def unknown(self, text: str) -> bool:
        self._entries.append({"kind": "unknown", "message": text})
        return self._handler.log_unknown(text)

    @property
    def entries(self) -> list[dict[str, Any]]:
        return list(self._entries)


class Inventory:
    """Key-value store for artifacts the bot accumulates during a session."""

    def __init__(self) -> None:
        self._items: dict[str, Any] = {}

    def put(self, key: str, value: Any) -> None:
        self._items[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._items.get(key, default)

    def has(self, key: str) -> bool:
        return key in self._items

    def keys(self) -> list[str]:
        return list(self._items.keys())

    @property
    def contents(self) -> dict[str, Any]:
        return dict(self._items)


@dataclass
class Port:
    """Bidirectional message port for command ingestion and response emission."""
    inbox: list[Any] = field(default_factory=list)
    outbox: list[Any] = field(default_factory=list)

    def receive(self, message: Any) -> None:
        self.inbox.append(message)

    def emit(self, message: Any) -> None:
        self.outbox.append(message)

    def drain_inbox(self) -> list[Any]:
        messages = list(self.inbox)
        self.inbox.clear()
        return messages

    def drain_outbox(self) -> list[Any]:
        messages = list(self.outbox)
        self.outbox.clear()
        return messages


class Bot:
    """
    Composable agent whose lifecycle is gated by Empirica CASCADE.

    Components:
        brain      — EmpericaHandler (session, vectors, sentinel gates)
        journal    — structured log (findings, unknowns, notes)
        inventory  — accumulated artifacts and cached state
        port       — bidirectional message ingestion/emission
        state      — proxy to handler state (phase, vectors, gate decision)
    """

    def __init__(self, config: BotConfig) -> None:
        self.config = config
        self.brain = EmpericaHandler(
            project_path=config.project_path,
            instance_id=config.instance_id,
            ai_id=config.ai_id,
            default_vectors=config.default_vectors,
            cli_timeout=config.cli_timeout,
        )
        self.journal = Journal(self.brain)
        self.inventory = Inventory()
        self.port = Port()

    @property
    def session_id(self) -> str | None:
        return self.brain.session_id

    @property
    def phase(self) -> Phase:
        return self.brain.phase

    @property
    def is_ready(self) -> bool:
        return self.brain.is_ready

    @property
    def vectors(self) -> dict[str, float]:
        return self.brain.vectors

    def boot(self) -> bool:
        result = self.brain.boot()
        if result.ok:
            self.journal.log(f"booted session={result.session_id} project={result.project_id}")
        else:
            self.journal.log(f"boot failed: {result.message}", kind="error")
        return result.ok

    def preflight(self, reasoning: str = "", vectors: dict[str, float] | None = None) -> dict[str, Any]:
        result = self.brain.preflight(reasoning=reasoning, vectors=vectors)
        self.journal.log(f"preflight: ok={result.get('ok')}", kind="lifecycle")
        return result

    def check(self, reasoning: str = "", vectors: dict[str, float] | None = None) -> CheckResult:
        result = self.brain.check(reasoning=reasoning, vectors=vectors)
        self.journal.log(f"check: decision={result.decision.value}", kind="gate")
        return result

    def postflight(self, reasoning: str = "", vectors: dict[str, float] | None = None) -> dict[str, Any]:
        result = self.brain.postflight(reasoning=reasoning, vectors=vectors)
        self.journal.log(f"postflight: ok={result.get('ok')}", kind="lifecycle")
        return result

    def close(self) -> None:
        self.brain.close()
        self.journal.log("session closed", kind="lifecycle")
