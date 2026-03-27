"""
Door Guy / Bouncer: outbound security gate for Waft.

This class is intentionally standalone in v1 so callers can adopt it gradually.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from ipaddress import ip_address
from pathlib import Path
from urllib.parse import urlparse


@dataclass(frozen=True)
class BouncerDecision:
    allowed: bool
    reason: str


@dataclass(frozen=True)
class ShipManifest:
    """
    One docking request (network/process exchange intent).
    """

    ship_id: str = ""
    source_host: str = ""
    source_ip: str = ""
    destination_port: int = 0
    cargo_type: str = ""
    endpoint: str = ""
    command: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class PortManifest:
    """
    Policy manifest that defines who can dock and what they can exchange.
    """

    allow_ships: set[str] = field(default_factory=set)
    deny_ships: set[str] = field(default_factory=set)
    allow_hosts: set[str] = field(default_factory=set)
    deny_hosts: set[str] = field(default_factory=set)
    allow_ports: set[int] = field(default_factory=set)
    deny_ports: set[int] = field(default_factory=set)
    allow_cargo: set[str] = field(default_factory=set)
    deny_cargo: set[str] = field(default_factory=set)
    allow_private_network: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "PortManifest":
        def lower_set(key: str) -> set[str]:
            return {str(v).strip().lower() for v in data.get(key, []) if str(v).strip()}

        def int_set(key: str) -> set[int]:
            result = set()
            for value in data.get(key, []):
                try:
                    result.add(int(value))
                except (TypeError, ValueError):
                    continue
            return result

        return cls(
            allow_ships=lower_set("allow_ships"),
            deny_ships=lower_set("deny_ships"),
            allow_hosts=lower_set("allow_hosts"),
            deny_hosts=lower_set("deny_hosts"),
            allow_ports=int_set("allow_ports"),
            deny_ports=int_set("deny_ports"),
            allow_cargo=lower_set("allow_cargo"),
            deny_cargo=lower_set("deny_cargo"),
            allow_private_network=bool(data.get("allow_private_network", False)),
        )

    @classmethod
    def from_json_file(cls, path: str | Path) -> "PortManifest":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Port manifest JSON must be an object")
        return cls.from_dict(payload)


class Bouncer:
    """
    Evaluate outbound network/process intent and block risky patterns.
    """

    DEFAULT_ALLOWED_SCHEMES = {"http", "https"}
    BLOCKED_HOSTS = {
        "localhost",
        "127.0.0.1",
        "0.0.0.0",
        "::1",
        "169.254.169.254",  # cloud metadata endpoint
        "metadata.google.internal",
        "169.254.170.2",  # ECS task metadata
    }
    BLOCKED_COMMANDS = {
        "curl",
        "wget",
        "aria2c",
        "powershell",
        "pwsh",
        "Invoke-WebRequest",
        "Invoke-Expression",
    }
    SHELL_CHAIN_TOKENS = {";", "&&", "||", "|", "$(", "`"}
    BLOCKED_DOWNLOAD_EXTENSIONS = {
        ".sh",
        ".bash",
        ".zsh",
        ".command",
        ".exe",
        ".dll",
        ".dmg",
        ".pkg",
        ".msi",
        ".bat",
        ".ps1",
    }

    def __init__(
        self,
        allowed_domains: set[str] | None = None,
        allow_private_network: bool = False,
        port_manifest: PortManifest | None = None,
    ) -> None:
        self.port_manifest = port_manifest or PortManifest()
        policy_domains = set(self.port_manifest.allow_hosts)
        self.allowed_domains = {d.lower() for d in (allowed_domains or set()) if d} | policy_domains
        self.allow_private_network = allow_private_network or self.port_manifest.allow_private_network

    @classmethod
    def from_manifest_file(cls, path: str | Path) -> "Bouncer":
        return cls(port_manifest=PortManifest.from_json_file(path))

    def inspect_url(self, url: str) -> BouncerDecision:
        raw = str(url or "").strip()
        if not raw:
            return BouncerDecision(False, "empty_url")

        parsed = urlparse(raw)
        scheme = (parsed.scheme or "").lower()
        host = (parsed.hostname or "").lower()

        if scheme not in self.DEFAULT_ALLOWED_SCHEMES:
            return BouncerDecision(False, "blocked_scheme")
        if not host:
            return BouncerDecision(False, "missing_host")
        if host in self.BLOCKED_HOSTS:
            return BouncerDecision(False, "blocked_host")

        host_ip = self._safe_parse_ip(host)
        if host_ip and host_ip.is_loopback:
            return BouncerDecision(False, "loopback_ip")
        if host_ip and host_ip.is_link_local:
            return BouncerDecision(False, "link_local_ip")
        if host_ip and (host_ip.is_private or host_ip.is_reserved) and not self.allow_private_network:
            return BouncerDecision(False, "private_or_reserved_ip")

        if self.allowed_domains and not self._domain_allowed(host):
            return BouncerDecision(False, "domain_not_allowlisted")

        path = (parsed.path or "").lower()
        if any(path.endswith(ext) for ext in self.BLOCKED_DOWNLOAD_EXTENSIONS):
            return BouncerDecision(False, "blocked_download_extension")

        return BouncerDecision(True, "allowed")

    def inspect_command(self, argv: list[str]) -> BouncerDecision:
        if not argv:
            return BouncerDecision(False, "empty_command")

        head = str(argv[0]).strip()
        if not head:
            return BouncerDecision(False, "empty_command")

        if head in self.BLOCKED_COMMANDS:
            return BouncerDecision(False, "blocked_command")

        for token in argv:
            value = str(token)
            if any(chain in value for chain in self.SHELL_CHAIN_TOKENS):
                return BouncerDecision(False, "shell_chain_token")

            if value.startswith(("http://", "https://")):
                decision = self.inspect_url(value)
                if not decision.allowed:
                    return decision

        return BouncerDecision(True, "allowed")

    def inspect_manifest(self, ship: ShipManifest) -> BouncerDecision:
        ship_id = ship.ship_id.strip().lower()
        host = ship.source_host.strip().lower()
        ip = ship.source_ip.strip()
        cargo = ship.cargo_type.strip().lower()
        port = int(ship.destination_port or 0)

        # Hard denies first
        if ship_id and ship_id in self.port_manifest.deny_ships:
            return BouncerDecision(False, "ship_denylisted")
        if host and host in self.port_manifest.deny_hosts:
            return BouncerDecision(False, "host_denylisted")
        if port and port in self.port_manifest.deny_ports:
            return BouncerDecision(False, "port_denylisted")
        if cargo and cargo in self.port_manifest.deny_cargo:
            return BouncerDecision(False, "cargo_denylisted")

        # Explicit allowlist gates when configured
        if self.port_manifest.allow_ships and ship_id not in self.port_manifest.allow_ships:
            return BouncerDecision(False, "ship_not_allowlisted")
        if self.port_manifest.allow_hosts and not self._domain_allowed(host):
            return BouncerDecision(False, "host_not_allowlisted")
        if self.port_manifest.allow_ports and port not in self.port_manifest.allow_ports:
            return BouncerDecision(False, "port_not_allowlisted")
        if self.port_manifest.allow_cargo and cargo not in self.port_manifest.allow_cargo:
            return BouncerDecision(False, "cargo_not_allowlisted")

        if ship.endpoint:
            endpoint_decision = self.inspect_url(ship.endpoint)
            if not endpoint_decision.allowed:
                return endpoint_decision
        elif host:
            probe_url = f"https://{host}/"
            host_decision = self.inspect_url(probe_url)
            if not host_decision.allowed:
                return host_decision
        elif ip:
            host_ip = self._safe_parse_ip(ip)
            if host_ip and host_ip.is_loopback:
                return BouncerDecision(False, "loopback_ip")
            if host_ip and host_ip.is_link_local:
                return BouncerDecision(False, "link_local_ip")
            if host_ip and (host_ip.is_private or host_ip.is_reserved) and not self.allow_private_network:
                return BouncerDecision(False, "private_or_reserved_ip")

        if ship.command:
            cmd_decision = self.inspect_command(ship.command)
            if not cmd_decision.allowed:
                return cmd_decision

        return BouncerDecision(True, "allowed")

    def _domain_allowed(self, host: str) -> bool:
        for allowed in self.allowed_domains:
            if host == allowed or host.endswith("." + allowed):
                return True
        return False

    @staticmethod
    def _safe_parse_ip(host: str):
        try:
            return ip_address(host)
        except ValueError:
            return None
