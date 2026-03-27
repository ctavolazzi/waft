import json

from cognitive_prosthetics_cli import main as cli_main


def _write_manifest(path, repo_path, required_paths):
    data = {
        "repositories": [
            {
                "id": "sample",
                "name": "Sample",
                "path": str(repo_path),
                "required_paths": required_paths,
            }
        ]
    }
    path.write_text(json.dumps(data), encoding="utf-8")


def _mock_which(monkeypatch):
    def fake_which(name):
        if name == "uv":
            return "/mock/bin/uv"
        return None

    monkeypatch.setattr(cli_main.shutil, "which", fake_which)


def test_missing_repo_path(tmp_path, monkeypatch, capsys):
    _mock_which(monkeypatch)
    manifest_path = tmp_path / "repositories.json"
    missing_repo = tmp_path / "missing-repo"
    _write_manifest(manifest_path, missing_repo, ["README.md"])

    code = cli_main.main(["check", "--json", "--manifest", str(manifest_path)])
    out = capsys.readouterr().out
    payload = json.loads(out)

    assert code == 1
    assert payload["ok"] is False
    assert payload["repositories"][0]["exists"] is False


def test_missing_required_script(tmp_path, monkeypatch, capsys):
    _mock_which(monkeypatch)
    manifest_path = tmp_path / "repositories.json"
    repo = tmp_path / "repo"
    repo.mkdir()
    _write_manifest(manifest_path, repo, ["missing.txt"])

    code = cli_main.main(["check", "--json", "--manifest", str(manifest_path)])
    out = capsys.readouterr().out
    payload = json.loads(out)

    assert code == 1
    assert payload["ok"] is False
    assert payload["repositories"][0]["missing_required_paths"] == ["missing.txt"]


def test_happy_path_with_exit_zero(tmp_path, monkeypatch, capsys):
    _mock_which(monkeypatch)
    manifest_path = tmp_path / "repositories.json"
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("ok", encoding="utf-8")
    _write_manifest(manifest_path, repo, ["README.md"])

    code = cli_main.main(["check", "--json", "--manifest", str(manifest_path)])
    out = capsys.readouterr().out
    payload = json.loads(out)

    assert code == 0
    assert payload["ok"] is True
    assert payload["summary"]["repo_count"] == 1


def test_json_shape_contains_expected_keys(tmp_path, monkeypatch, capsys):
    _mock_which(monkeypatch)
    manifest_path = tmp_path / "repositories.json"
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("ok", encoding="utf-8")
    _write_manifest(manifest_path, repo, ["README.md"])

    cli_main.main(["check", "--json", "--manifest", str(manifest_path)])
    out = capsys.readouterr().out
    payload = json.loads(out)

    assert {"ok", "summary", "required_checks", "tooling", "manifest", "repositories", "signals"} <= set(payload.keys())


def test_exit_code_assertion_for_required_failures(tmp_path, monkeypatch):
    _mock_which(monkeypatch)
    manifest_path = tmp_path / "repositories.json"
    repo = tmp_path / "repo"
    repo.mkdir()
    _write_manifest(manifest_path, repo, ["README.md"])

    code = cli_main.main(["check", "--manifest", str(manifest_path)])

    assert code == 1
