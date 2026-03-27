"""
EmpericaHandler — high-level lifecycle owner for Empirica integration.

Sits above EmpiricaManager as the "brain" of a Bot. Owns a single session,
manages CASCADE phase transitions, and gates operations through sentinel checks.

Usage:
    handler = EmpericaHandler(project_path="/path/to/project")
    handler.boot()
    handler.preflight(reasoning="starting work on X")
    result = handler.check(reasoning="about to modify Y")
    if result.proceed:
        # do work
        handler.log_finding("discovered Z", impact=0.8)
    handler.postflight(reasoning="completed X with evidence")
"""

from __future__ import annotations

import json
import os
import subprocess
import shutil
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class Phase(Enum):
    UNBOOTED = "unbooted"
    BOOTED = "booted"
    PREFLIGHT = "preflight"
    ACTIVE = "active"
    POSTFLIGHT = "postflight"
    CLOSED = "closed"


class Transport(Enum):
    MCP = "mcp"
    API = "api"
    CLI = "cli"
    DEGRADED = "degraded"


class GateDecision(Enum):
    PROCEED = "proceed"
    INVESTIGATE = "investigate"
    HALT = "halt"
    BRANCH = "branch"
    REVISE = "revise"
    UNKNOWN = "unknown"

    @classmethod
    def from_str(cls, s: str | None) -> GateDecision:
        if not s:
            return cls.UNKNOWN
        try:
            return cls(s.lower().strip())
        except ValueError:
            return cls.UNKNOWN


@dataclass
class CheckResult:
    decision: GateDecision
    session_id: str | None
    checkpoint_id: str | None
    raw: dict[str, Any]

    @property
    def proceed(self) -> bool:
        return self.decision == GateDecision.PROCEED

    @property
    def halted(self) -> bool:
        return self.decision == GateDecision.HALT


@dataclass
class BootResult:
    ok: bool
    session_id: str | None
    project_id: str | None
    message: str
    transport: str = "cli"


@dataclass
class HandlerState:
    phase: Phase = Phase.UNBOOTED
    session_id: str | None = None
    transaction_id: str | None = None
    project_id: str | None = None
    last_gate: GateDecision | None = None
    vectors: dict[str, float] = field(default_factory=dict)
    findings: list[str] = field(default_factory=list)
    unknowns: list[str] = field(default_factory=list)
    transport: str = "cli"
    fallback_reason: str | None = None


class EmpericaHandlerError(Exception):
    pass


class EmpericaHandler:
    DEFAULT_VECTORS = {
        "engagement": 0.7,
        "know": 0.5,
        "uncertainty": 0.4,
    }

    def __init__(
        self,
        project_path: str | Path,
        instance_id: str = "waft-bot",
        ai_id: str = "waft-brain",
        default_vectors: dict[str, float] | None = None,
        cli_timeout: int = 15,
    ) -> None:
        self.project_path = Path(project_path).resolve()
        self.instance_id = instance_id
        self.ai_id = ai_id
        self.cli_timeout = cli_timeout
        self._default_vectors = default_vectors or dict(self.DEFAULT_VECTORS)
        self._state = HandlerState()
        self._transport = Transport.CLI

    @property
    def session_id(self) -> str | None:
        return self._state.session_id

    @property
    def phase(self) -> Phase:
        return self._state.phase

    @property
    def state(self) -> HandlerState:
        return self._state

    @property
    def is_ready(self) -> bool:
        return self._state.phase not in (Phase.UNBOOTED, Phase.CLOSED)

    @property
    def vectors(self) -> dict[str, float]:
        return dict(self._state.vectors)

    @property
    def transport(self) -> str:
        return self._transport.value

    def boot(self) -> BootResult:
        self._select_transport()
        self._ensure_instance_file()
        os.environ["EMPIRICA_INSTANCE_ID"] = self.instance_id

        project_id = self._resolve_project()
        session_id = self._create_session()
        if not session_id:
            return BootResult(
                ok=False,
                session_id=None,
                project_id=project_id,
                message="session-create failed",
                transport=self.transport,
            )

        self._state.session_id = session_id
        self._state.project_id = project_id
        self._state.phase = Phase.BOOTED
        self._state.transport = self.transport
        return BootResult(
            ok=True,
            session_id=session_id,
            project_id=project_id,
            message="ready",
            transport=self.transport,
        )

    def preflight(
        self,
        reasoning: str = "",
        vectors: dict[str, float] | None = None,
    ) -> dict[str, Any]:
        self._require_phase(Phase.BOOTED, Phase.ACTIVE)
        vecs = vectors or dict(self._default_vectors)
        payload = {
            "session_id": self._state.session_id,
            "vectors": vecs,
            "reasoning": reasoning or "preflight assessment",
        }
        result = self._cli_json("preflight-submit", stdin_data=payload)
        if result.get("ok"):
            self._state.phase = Phase.PREFLIGHT
            self._state.vectors = vecs
            self._state.transaction_id = result.get("transaction_id")
        return result

    def check(
        self,
        reasoning: str = "",
        vectors: dict[str, float] | None = None,
    ) -> CheckResult:
        self._require_phase(Phase.PREFLIGHT, Phase.ACTIVE)
        vecs = vectors or dict(self._state.vectors) or dict(self._default_vectors)
        payload = {
            "session_id": self._state.session_id,
            "vectors": vecs,
            "reasoning": reasoning or "check gate",
        }
        result = self._cli_json("check-submit", stdin_data=payload)
        decision = GateDecision.from_str(result.get("decision") or result.get("metacog", {}).get("computed_decision"))
        self._state.last_gate = decision
        if decision == GateDecision.PROCEED:
            self._state.phase = Phase.ACTIVE
        cr = CheckResult(
            decision=decision,
            session_id=self._state.session_id,
            checkpoint_id=result.get("checkpoint_id"),
            raw=result,
        )
        return cr

    def postflight(
        self,
        reasoning: str = "",
        vectors: dict[str, float] | None = None,
    ) -> dict[str, Any]:
        self._require_phase(Phase.ACTIVE, Phase.PREFLIGHT)
        vecs = vectors or dict(self._state.vectors) or dict(self._default_vectors)
        payload = {
            "session_id": self._state.session_id,
            "vectors": vecs,
            "reasoning": reasoning or "postflight assessment",
        }
        result = self._cli_json("postflight-submit", stdin_data=payload)
        if result.get("ok"):
            self._state.phase = Phase.POSTFLIGHT
        return result

    def log_finding(self, finding: str, impact: float = 0.5) -> bool:
        try:
            self._cli_raw(["finding-log", "--finding", finding, "--impact", str(impact)])
            self._state.findings.append(finding)
            return True
        except EmpericaHandlerError:
            return False

    def log_unknown(self, unknown: str) -> bool:
        try:
            self._cli_raw(["unknown-log", "--unknown", unknown])
            self._state.unknowns.append(unknown)
            return True
        except EmpericaHandlerError:
            return False

    def close(self) -> None:
        self._state.phase = Phase.CLOSED

    def backend_status(self) -> dict[str, Any]:
        return {
            "transport": self.transport,
            "fallback_reason": self._state.fallback_reason,
            "session_id": self._state.session_id,
            "project_id": self._state.project_id,
        }

    # --- internal ---

    def _select_transport(self) -> None:
        # MCP-first policy: if configured and executable, prefer MCP mode.
        if self._mcp_available():
            self._transport = Transport.MCP
            self._state.transport = self._transport.value
            self._state.fallback_reason = None
            return

        # API transport can be added later; current implementation keeps CLI deterministic.
        if shutil.which("empirica"):
            self._transport = Transport.CLI
            self._state.transport = self._transport.value
            self._state.fallback_reason = "mcp unavailable; using cli backend"
            return

        self._transport = Transport.DEGRADED
        self._state.transport = self._transport.value
        self._state.fallback_reason = "mcp unavailable and empirica cli missing"

    def _mcp_available(self) -> bool:
        mcp_cmd = self._resolve_mcp_command()
        if not mcp_cmd:
            return False
        try:
            probe = subprocess.run(
                [mcp_cmd, "--help"],
                capture_output=True,
                text=True,
                timeout=5,
                env=self._empirica_env(),
            )
            return probe.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def _resolve_mcp_command(self) -> str | None:
        project_mcp = self.project_path / ".cursor" / "mcp.json"
        if not project_mcp.exists():
            return shutil.which("empirica-mcp")
        try:
            data = json.loads(project_mcp.read_text())
            servers = data.get("mcpServers", {})
            if not isinstance(servers, dict):
                return shutil.which("empirica-mcp")
            empirica_server = servers.get("empirica-epistemic") or servers.get("empirica")
            if isinstance(empirica_server, dict):
                command = empirica_server.get("command")
                if isinstance(command, str) and command.strip():
                    return command.strip()
        except (json.JSONDecodeError, OSError):
            return shutil.which("empirica-mcp")
        return shutil.which("empirica-mcp")

    def _resolve_empirica_home(self) -> Path:
        forced = os.getenv("WAFT_EMPIRICA_HOME")
        if forced:
            home = Path(forced).expanduser().resolve()
            home.mkdir(parents=True, exist_ok=True)
            return home

        real_home = Path.home()
        probe_dir = real_home / ".empirica" / "instance_projects"
        try:
            probe_dir.mkdir(parents=True, exist_ok=True)
            probe = probe_dir / ".waft_write_probe"
            probe.write_text("ok")
            probe.unlink(missing_ok=True)
            return real_home
        except OSError:
            self.project_path.mkdir(parents=True, exist_ok=True)
            return self.project_path

    def _empirica_env(self) -> dict[str, str]:
        env = dict(os.environ)
        env["EMPIRICA_INSTANCE_ID"] = self.instance_id
        env["HOME"] = str(self._resolve_empirica_home())
        return env

    def _ensure_instance_file(self) -> None:
        instance_dir = self._resolve_empirica_home() / ".empirica" / "instance_projects"
        instance_dir.mkdir(parents=True, exist_ok=True)
        data = {
            "project_path": str(self.project_path),
            "project_name": self.project_path.name,
        }
        if self._state.project_id:
            data["project_id"] = self._state.project_id
        (instance_dir / f"{self.instance_id}.json").write_text(json.dumps(data))

    def _resolve_project(self) -> str | None:
        result = self._cli_json("project-list")
        for p in result.get("projects", []):
            if p.get("name") == self.project_path.name or str(self.project_path) in str(p.get("trajectory_path", "")):
                pid = p.get("id")
                self._state.project_id = pid
                self._ensure_instance_file()
                return pid

        create_result = self._cli_json(
            "project-create",
            extra_args=["--name", self.project_path.name, "--type", "infrastructure"],
        )
        pid = create_result.get("project_id")
        if pid:
            self._state.project_id = pid
            self._ensure_instance_file()
        return pid

    def _create_session(self) -> str | None:
        result = self._cli_json("session-create", extra_args=["--ai-id", self.ai_id, "--output", "json"])
        return result.get("session_id") if result.get("ok") else None

    def _require_phase(self, *allowed: Phase) -> None:
        if self._state.phase not in allowed:
            raise EmpericaHandlerError(
                f"operation requires phase {[p.value for p in allowed]}, currently in {self._state.phase.value}"
            )

    def _cli_json(
        self,
        command: str,
        stdin_data: dict | None = None,
        extra_args: list[str] | None = None,
    ) -> dict[str, Any]:
        if self._transport == Transport.DEGRADED:
            return {"ok": False, "error": "empirica backend unavailable", "transport": "degraded"}
        args = ["empirica", command]
        if extra_args:
            args.extend(extra_args)
        if stdin_data:
            args.append("-")

        try:
            proc = subprocess.run(
                args,
                cwd=self.project_path,
                input=json.dumps(stdin_data) if stdin_data else None,
                capture_output=True,
                text=True,
                timeout=self.cli_timeout,
                env=self._empirica_env(),
            )
        except subprocess.TimeoutExpired:
            return {"ok": False, "error": f"{command} timed out after {self.cli_timeout}s", "transport": self.transport}
        except FileNotFoundError:
            return {"ok": False, "error": "empirica CLI not found", "transport": self.transport}

        stdout = proc.stdout.strip()
        for line in stdout.split("\n"):
            line = line.strip()
            if line.startswith("{"):
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    continue
        if stdout:
            try:
                return json.loads(stdout)
            except json.JSONDecodeError:
                pass
        return {
            "ok": False,
            "error": f"unparseable output from {command}",
            "raw_stdout": stdout,
            "raw_stderr": proc.stderr,
            "transport": self.transport,
        }

    def _cli_raw(self, args: list[str]) -> str:
        try:
            proc = subprocess.run(
                ["empirica"] + args,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=self.cli_timeout,
                env=self._empirica_env(),
            )
            if proc.returncode != 0:
                raise EmpericaHandlerError(proc.stderr or proc.stdout or f"exit {proc.returncode}")
            return proc.stdout
        except subprocess.TimeoutExpired:
            raise EmpericaHandlerError(f"command timed out after {self.cli_timeout}s")
        except FileNotFoundError:
            raise EmpericaHandlerError("empirica CLI not found")
