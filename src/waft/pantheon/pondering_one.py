"""
The Pondering One: Pantheon Entity of Brain Realm Governance.

Owns the Empirica brain realm contract:
- MCP-first policy
- automatic realm setup
- fallback visibility
"""

from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


class ThePonderingOne:
    """Pantheon steward for Empirica brain realm health and setup."""

    def __init__(self, project_path: Path | None = None):
        if project_path is None:
            project_path = Path.cwd()
        self.project_path = Path(project_path)
        self.pantheon_path = self.project_path / "_pantheon" / "the_pondering_one"
        self.status_path = self.pantheon_path / "status"
        self.pantheon_path.mkdir(parents=True, exist_ok=True)
        self.status_path.mkdir(parents=True, exist_ok=True)

    def _preferred_mcp_command(self) -> str | None:
        local_bin = Path.home() / ".local" / "bin" / "empirica-mcp"
        if local_bin.exists():
            return str(local_bin)
        discovered = shutil.which("empirica-mcp")
        if discovered:
            return discovered
        return None

    def ensure_brain_realm(self) -> dict[str, Any]:
        """Ensure project MCP config exists and points to empirica-mcp."""
        command = self._preferred_mcp_command()
        cursor_dir = self.project_path / ".cursor"
        cursor_dir.mkdir(parents=True, exist_ok=True)
        mcp_file = cursor_dir / "mcp.json"

        if command is None:
            status = {
                "ok": False,
                "message": "empirica-mcp command not found",
                "mcp_config_path": str(mcp_file),
                "timestamp": datetime.now().isoformat(),
            }
            self._write_status(status)
            return status

        config = {
            "mcpServers": {
                "empirica-epistemic": {
                    "command": command,
                    "args": ["--workspace", str(self.project_path)],
                    "env": {
                        "EMPIRICA_EPISTEMIC_MODE": "true",
                        "EMPIRICA_PERSONALITY": "balanced_architect",
                        "EMPIRICA_INSTANCE_ID": "waft-bot",
                    },
                }
            }
        }
        mcp_file.write_text(json.dumps(config, indent=2) + "\n")

        status = self.get_brain_realm_status()
        status["configured"] = True
        status["mcp_config_path"] = str(mcp_file)
        self._write_status(status)
        return status

    def get_brain_realm_status(self) -> dict[str, Any]:
        """Read current brain realm readiness and fallback posture."""
        mcp_file = self.project_path / ".cursor" / "mcp.json"
        mcp_server_ok = False
        mcp_command = ""
        mcp_executable = False
        error = None

        if mcp_file.exists():
            try:
                data = json.loads(mcp_file.read_text())
                server = data.get("mcpServers", {}).get("empirica-epistemic", {})
                mcp_command = server.get("command", "")
                mcp_server_ok = bool(mcp_command)
                mcp_executable = bool(mcp_command) and Path(mcp_command).exists()
                if mcp_server_ok and mcp_executable:
                    probe = subprocess.run(
                        [mcp_command, "--help"],
                        capture_output=True,
                        text=True,
                        timeout=5,
                    )
                    mcp_executable = probe.returncode == 0
            except Exception as exc:
                error = str(exc)

        empirica_cli = shutil.which("empirica")

        transport = "degraded"
        fallback_reason = "mcp unavailable and empirica cli missing"
        if mcp_server_ok and mcp_executable:
            transport = "mcp"
            fallback_reason = None
        elif empirica_cli:
            transport = "cli"
            fallback_reason = "mcp unavailable; using cli backend"

        status = {
            "transport": transport,
            "fallback_reason": fallback_reason,
            "mcp_server_configured": mcp_server_ok,
            "mcp_command": mcp_command,
            "mcp_executable": mcp_executable,
            "empirica_cli": empirica_cli,
            "error": error,
            "timestamp": datetime.now().isoformat(),
        }
        self._write_status(status)
        return status

    def run_jungle_gym(self, mode: str = "simulated") -> dict[str, Any]:
        """Run jungle gym harness and return parsed report."""
        result = subprocess.run(
            ["python3", "scripts/empirica_jungle_gym.py", "--mode", mode, "--json"],
            cwd=self.project_path,
            capture_output=True,
            text=True,
            timeout=120,
        )
        parsed = {}
        try:
            parsed = json.loads(result.stdout)
        except json.JSONDecodeError:
            parsed = {"all_passed": False, "raw_stdout": result.stdout, "raw_stderr": result.stderr}

        report = {
            "mode": mode,
            "returncode": result.returncode,
            "report": parsed,
            "timestamp": datetime.now().isoformat(),
        }
        report_file = self.status_path / f"jungle_gym_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.write_text(json.dumps(report, indent=2) + "\n")
        return report

    def _write_status(self, status: dict[str, Any]) -> None:
        latest = self.status_path / "latest.json"
        latest.write_text(json.dumps(status, indent=2) + "\n")

