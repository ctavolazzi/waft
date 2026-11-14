"""Lab tests never touch the network: any connection that is not to this machine fails the test."""

import ipaddress
import json
import socket

import pytest

from waft.gym import DUNGEONS

_real_connect = socket.socket.connect


def _guarded_connect(self, address):
    host = address[0] if isinstance(address, tuple) else address
    try:
        local = ipaddress.ip_address(host).is_loopback
    except ValueError:
        local = host == "localhost" or isinstance(address, (str, bytes))  # a unix socket path is local
    if not local:
        raise AssertionError(f"unexpected network call in a lab test: {address!r}")
    return _real_connect(self, address)


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    monkeypatch.setattr(socket.socket, "connect", _guarded_connect)
    for name in ("WAFT_LLM_BASE_URL", "WAFT_LLM_API_KEY", "WAFT_LLM_MODEL"):
        monkeypatch.delenv(name, raising=False)


@pytest.fixture(scope="session")
def answers():
    return json.loads((DUNGEONS / "waft_temple.answers.json").read_text())["answers"]
