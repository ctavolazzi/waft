import json

from waft.core.door_guy import Bouncer, PortManifest, ShipManifest


def test_allows_normal_https_url():
    decision = Bouncer().inspect_url("https://example.com/data.json")
    assert decision.allowed is True
    assert decision.reason == "allowed"


def test_blocks_non_http_scheme():
    decision = Bouncer().inspect_url("file:///etc/passwd")
    assert decision.allowed is False
    assert decision.reason == "blocked_scheme"


def test_blocks_metadata_ip():
    decision = Bouncer().inspect_url("http://169.254.169.254/latest/meta-data")
    assert decision.allowed is False
    assert decision.reason in {"blocked_host", "link_local_ip"}


def test_blocks_private_ip_by_default():
    decision = Bouncer().inspect_url("http://10.0.0.9/payload")
    assert decision.allowed is False
    assert decision.reason == "private_or_reserved_ip"


def test_allows_private_ip_when_enabled():
    decision = Bouncer(allow_private_network=True).inspect_url("http://10.0.0.9/status")
    assert decision.allowed is True
    assert decision.reason == "allowed"


def test_blocks_downloadable_executable_path():
    decision = Bouncer().inspect_url("https://downloads.example.com/agent.pkg")
    assert decision.allowed is False
    assert decision.reason == "blocked_download_extension"


def test_domain_allowlist_blocks_unknown_host():
    decision = Bouncer(allowed_domains={"trusted.example.com"}).inspect_url("https://evil.example.org")
    assert decision.allowed is False
    assert decision.reason == "domain_not_allowlisted"


def test_domain_allowlist_allows_subdomain():
    decision = Bouncer(allowed_domains={"trusted.example.com"}).inspect_url(
        "https://api.trusted.example.com/model"
    )
    assert decision.allowed is True


def test_blocks_risky_command_head():
    decision = Bouncer().inspect_command(["curl", "https://example.com/file.sh"])
    assert decision.allowed is False
    assert decision.reason == "blocked_command"


def test_blocks_shell_chain_tokens():
    decision = Bouncer().inspect_command(["python", "script.py; rm -rf /"])
    assert decision.allowed is False
    assert decision.reason == "shell_chain_token"


def test_manifest_denies_unknown_ship():
    manifest = PortManifest.from_dict({"allow_ships": ["trusted-ship"]})
    ship = ShipManifest(ship_id="untrusted-ship", source_host="example.com", destination_port=443, cargo_type="json")
    decision = Bouncer(port_manifest=manifest).inspect_manifest(ship)
    assert decision.allowed is False
    assert decision.reason == "ship_not_allowlisted"


def test_manifest_allows_trusted_ship_and_cargo():
    manifest = PortManifest.from_dict(
        {
            "allow_ships": ["trusted-ship"],
            "allow_hosts": ["trusted.example.com"],
            "allow_ports": [443],
            "allow_cargo": ["json"],
        }
    )
    ship = ShipManifest(
        ship_id="trusted-ship",
        source_host="trusted.example.com",
        destination_port=443,
        cargo_type="json",
        endpoint="https://trusted.example.com/v1/infer",
    )
    decision = Bouncer(port_manifest=manifest).inspect_manifest(ship)
    assert decision.allowed is True
    assert decision.reason == "allowed"


def test_manifest_denies_cargo_type():
    manifest = PortManifest.from_dict({"deny_cargo": ["executable"]})
    ship = ShipManifest(ship_id="trusted", source_host="example.com", destination_port=443, cargo_type="executable")
    decision = Bouncer(port_manifest=manifest).inspect_manifest(ship)
    assert decision.allowed is False
    assert decision.reason == "cargo_denylisted"


def test_manifest_denies_unlisted_port():
    manifest = PortManifest.from_dict({"allow_ports": [443]})
    ship = ShipManifest(ship_id="trusted", source_host="example.com", destination_port=8080, cargo_type="json")
    decision = Bouncer(port_manifest=manifest).inspect_manifest(ship)
    assert decision.allowed is False
    assert decision.reason == "port_not_allowlisted"


def test_manifest_file_loader(tmp_path):
    manifest_path = tmp_path / "dock_manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "allow_hosts": ["trusted.example.com"],
                "allow_ports": [443],
                "allow_cargo": ["json"],
            }
        ),
        encoding="utf-8",
    )
    bouncer = Bouncer.from_manifest_file(manifest_path)
    ship = ShipManifest(source_host="trusted.example.com", destination_port=443, cargo_type="json")
    decision = bouncer.inspect_manifest(ship)
    assert decision.allowed is True
