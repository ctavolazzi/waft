"""The API's trust boundary: this machine is trusted, everyone else needs the token.

Before 2026-11-14 the handshake route returned the token to any caller and most write
routes asked for none, so binding the server to 0.0.0.0 (Docker, a LAN) opened it.
"""

import re

import pytest
from fastapi.testclient import TestClient

from waft.api.auth import TOKEN_FILE, get_or_create_token, is_local_client
from waft.api.main import create_app

REMOTE = ("203.0.113.7", 40000)  # TEST-NET-3: an address that is never this machine
OPEN_TO_REMOTE = {"/api/health", "/api/auth/info", "/api/auth/verify", "/api/decision/health"}


@pytest.fixture
def project(tmp_path):
    (tmp_path / "_work_efforts").mkdir()
    return tmp_path


@pytest.fixture
def app(project):
    return create_app(project_path=project)


@pytest.fixture
def local(app):
    return TestClient(app)


@pytest.fixture
def remote(app):
    return TestClient(app, client=REMOTE)


def _operations(app):
    """Every (method, concrete path) the app declares, with path parameters filled in."""
    for path, methods in app.openapi()["paths"].items():
        concrete = re.sub(r"\{[^}]+\}", "probe", path)
        for method in methods:
            if method in ("get", "post", "put", "patch", "delete"):
                yield method.upper(), path, concrete


@pytest.mark.parametrize(
    "host,expected",
    [
        ("127.0.0.1", True),
        ("127.8.9.10", True),
        ("::1", True),
        ("localhost", True),
        ("testclient", True),
        ("203.0.113.7", False),
        ("10.0.0.5", False),
        ("172.17.0.1", False),  # the Docker bridge: the host machine as a container sees it
        ("::ffff:203.0.113.7", False),
        ("", False),
        (None, False),
        ("not-an-address", False),
    ],
)
def test_what_counts_as_this_machine(host, expected):
    assert is_local_client(host) is expected


def test_trusted_networks_are_opt_in(monkeypatch):
    bridge = "172.18.0.1"
    assert is_local_client(bridge) is False

    monkeypatch.setenv("WAFT_API_TRUSTED_CLIENTS", "172.16.0.0/12, not-a-network")
    assert is_local_client(bridge) is True
    assert is_local_client("203.0.113.7") is False

    monkeypatch.setenv("WAFT_API_TRUSTED_CLIENTS", "not-a-network,,")
    assert is_local_client(bridge) is False


def test_local_handshake_returns_the_token(local, project):
    response = local.post("/api/auth/handshake", json={})
    assert response.status_code == 200
    assert response.json()["token"] == (project / TOKEN_FILE).read_text().strip()


def test_remote_handshake_is_refused_and_leaks_nothing(remote, project):
    token = get_or_create_token(project)

    response = remote.post("/api/auth/handshake", json={})

    # The middleware answers first (401); the route's own guard would answer 403.
    assert response.status_code in (401, 403)
    assert token not in response.text


def test_remote_handshake_is_refused_even_with_the_token(remote, project):
    """Holding the token does not turn the handshake into a remote token dispenser."""
    token = get_or_create_token(project)

    response = remote.post(
        "/api/auth/handshake", json={}, headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
    assert token not in response.text


def test_every_route_refuses_a_remote_client_without_the_token(app, remote, project):
    get_or_create_token(project)
    answered_without_a_token = []
    checked = 0

    for method, path, concrete in _operations(app):
        if path in OPEN_TO_REMOTE:
            continue
        response = remote.request(method, concrete, json={} if method != "GET" else None)
        checked += 1
        if response.status_code != 401:
            answered_without_a_token.append((method, path, response.status_code))

    assert checked > 50, "the schema walk found too few routes to mean anything"
    assert answered_without_a_token == []


def test_a_wrong_token_is_refused(remote, project):
    get_or_create_token(project)

    response = remote.get("/api/work-efforts", headers={"Authorization": "Bearer not-the-token"})

    assert response.status_code == 401


def test_a_remote_client_with_the_token_gets_through(remote, project):
    token = get_or_create_token(project)

    response = remote.get("/api/work-efforts", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200


def test_remote_is_refused_when_no_token_exists_yet(remote, project):
    """No token file must mean nobody remote gets in, not that an empty token matches."""
    assert not (project / TOKEN_FILE).exists()

    for header in ({}, {"Authorization": "Bearer "}, {"Authorization": "Bearer x"}):
        assert remote.get("/api/work-efforts", headers=header).status_code == 401


def test_health_stays_open_so_a_remote_monitor_can_probe(remote):
    assert remote.get("/api/health").status_code == 200


def test_local_clients_work_as_before(local):
    """Control: the boundary must not lock out the dashboards running on the same machine."""
    assert local.get("/api/work-efforts").status_code == 200
    assert local.post("/api/decision/analyze", json={}).status_code != 401


def test_preflight_requests_pass_so_browsers_can_ask(remote):
    response = remote.options(
        "/api/work-efforts",
        headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "POST"},
    )
    assert response.status_code == 200


def test_starting_the_server_creates_the_token(app, project):
    assert not (project / TOKEN_FILE).exists()

    with TestClient(app):  # entering the context runs the app's startup
        pass

    assert len((project / TOKEN_FILE).read_text().strip()) >= 32
