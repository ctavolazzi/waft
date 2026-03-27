from pathlib import Path
import json

import pytest
import typer

from waft.cli import meme_cli


def test_meme_cli_registers_expected_commands():
    names = {command.name for command in meme_cli.meme_app.registered_commands}
    assert {"generate", "styles", "templates", "cooking", "security-check"}.issubset(names)


def test_meme_styles_command_output(monkeypatch, capsys):
    class FakeGenerator:
        def __init__(self, project_path):
            self.project_path = project_path

        def list_styles(self):
            return [type("Style", (), {"name": "top_bottom", "description": "classic"})()]

    monkeypatch.setattr(meme_cli, "MemeGenerator", FakeGenerator)
    meme_cli.meme_styles(path=".")
    output = capsys.readouterr().out
    assert "top_bottom: classic" in output


def test_meme_templates_command_output(monkeypatch, capsys):
    class FakeGenerator:
        def __init__(self, project_path):
            self.project_path = project_path

        def list_templates(self):
            return [
                type(
                    "Template",
                    (),
                    {
                        "name": "drake",
                        "style": "top_bottom",
                        "description": "desc",
                        "category": "mainstream",
                        "featured": True,
                    },
                )()
            ]

    monkeypatch.setattr(meme_cli, "MemeGenerator", FakeGenerator)
    meme_cli.meme_templates(path=".")
    output = capsys.readouterr().out
    assert "drake (top_bottom, mainstream featured): desc" in output


def test_meme_generate_command_calls_generator(monkeypatch, capsys, tmp_path):
    called = {"request": None}

    class FakeGenerator:
        def __init__(self, project_path):
            self.project_path = project_path

        def generate(self, request):
            called["request"] = request
            return Path(tmp_path / "output.jpg")

    monkeypatch.setattr(meme_cli, "MemeGenerator", FakeGenerator)
    meme_cli.meme_generate(
        prompt="hello",
        mode="mixed",
        output=str(tmp_path / "output.jpg"),
        path=".",
    )

    output = capsys.readouterr().out
    assert "Generated meme:" in output
    assert called["request"] is not None
    assert called["request"].prompt == "hello"


def test_meme_cooking_command_output(monkeypatch, capsys):
    class FakeGenerator:
        def __init__(self, project_path):
            self.project_path = project_path

        def list_recipes(self):
            return [
                type(
                    "Recipe",
                    (),
                    {"name": "burnt_ember", "style": "top_bottom", "description": "spicy"},
                )()
            ]

    monkeypatch.setattr(meme_cli, "MemeGenerator", FakeGenerator)
    meme_cli.meme_cooking(path=".")
    output = capsys.readouterr().out
    assert "burnt_ember (top_bottom): spicy" in output


def test_meme_security_check_success(monkeypatch, capsys):
    class FakeGenerator:
        def __init__(self, project_path):
            self.project_path = project_path
            self.max_download_bytes = 15 * 1024 * 1024

    monkeypatch.setattr(meme_cli, "MemeGenerator", FakeGenerator)
    monkeypatch.setattr(meme_cli.meme_lab_route, "MAX_HISTORY_ENTRIES", 2000)
    monkeypatch.setattr(
        meme_cli.inspect,
        "getsource",
        lambda _fn: "relative_to(reports_root) _work_efforts reports file path not permitted",
    )

    meme_cli.meme_security_check(path=".")
    output = capsys.readouterr().out
    assert "PASS download_size_cap" in output
    assert "PASS history_retention_limit" in output
    assert "PASS reports_subtree_file_policy" in output
    assert "Security check passed." in output


def test_meme_security_check_failure(monkeypatch, capsys):
    class FakeGenerator:
        def __init__(self, project_path):
            self.project_path = project_path
            self.max_download_bytes = 99 * 1024 * 1024

    monkeypatch.setattr(meme_cli, "MemeGenerator", FakeGenerator)
    monkeypatch.setattr(meme_cli.meme_lab_route, "MAX_HISTORY_ENTRIES", 2000)
    monkeypatch.setattr(
        meme_cli.inspect,
        "getsource",
        lambda _fn: "relative_to(reports_root) _work_efforts reports file path not permitted",
    )

    with pytest.raises(typer.Exit) as exc:
        meme_cli.meme_security_check(path=".")
    output = capsys.readouterr().out
    assert exc.value.exit_code == 1
    assert "FAIL download_size_cap" in output
    assert "Security check failed" in output


def test_meme_generate_config_file_not_found_raises_bad_parameter(tmp_path):
    with pytest.raises(typer.BadParameter, match="config file not found"):
        meme_cli.meme_generate(
            prompt="hello",
            config=str(tmp_path / "missing.json"),
            output=str(tmp_path / "output.jpg"),
            path=".",
        )


def test_meme_generate_invalid_json_config_raises_decode_error(tmp_path):
    config_path = tmp_path / "bad.json"
    config_path.write_text("{not-valid-json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        meme_cli.meme_generate(
            prompt="hello",
            config=str(config_path),
            output=str(tmp_path / "output.jpg"),
            path=".",
        )


def test_meme_generate_config_overrides_cli_values(monkeypatch, tmp_path):
    called = {"request": None}

    class FakeGenerator:
        def __init__(self, project_path):
            self.project_path = project_path

        def generate(self, request):
            called["request"] = request
            return Path(tmp_path / "output.jpg")

    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps({"top_text": "FROM_CONFIG", "temperature": 0.3, "top_k": 4}),
        encoding="utf-8",
    )
    monkeypatch.setattr(meme_cli, "MemeGenerator", FakeGenerator)
    meme_cli.meme_generate(
        prompt="hello",
        top="FROM_CLI",
        temperature=1.9,
        top_k=19,
        config=str(config_path),
        output=str(tmp_path / "output.jpg"),
        path=".",
    )

    assert called["request"] is not None
    assert called["request"].top_text == "FROM_CONFIG"
    assert called["request"].temperature == 0.3
    assert called["request"].top_k == 4


def test_meme_generate_config_type_coercion_failure_raises_value_error(monkeypatch, tmp_path):
    class FakeGenerator:
        def __init__(self, project_path):
            self.project_path = project_path

        def generate(self, request):
            return Path(tmp_path / "output.jpg")

    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"temperature": "not-a-float"}), encoding="utf-8")
    monkeypatch.setattr(meme_cli, "MemeGenerator", FakeGenerator)

    with pytest.raises(ValueError):
        meme_cli.meme_generate(
            prompt="hello",
            config=str(config_path),
            output=str(tmp_path / "output.jpg"),
            path=".",
        )


def test_meme_security_check_fails_when_history_limit_invalid(monkeypatch, capsys):
    class FakeGenerator:
        def __init__(self, project_path):
            self.project_path = project_path
            self.max_download_bytes = 15 * 1024 * 1024

    monkeypatch.setattr(meme_cli, "MemeGenerator", FakeGenerator)
    monkeypatch.setattr(meme_cli.meme_lab_route, "MAX_HISTORY_ENTRIES", 99_999)
    monkeypatch.setattr(
        meme_cli.inspect,
        "getsource",
        lambda _fn: "relative_to(reports_root) _work_efforts reports file path not permitted",
    )

    with pytest.raises(typer.Exit) as exc:
        meme_cli.meme_security_check(path=".")
    output = capsys.readouterr().out
    assert exc.value.exit_code == 1
    assert "FAIL history_retention_limit" in output


def test_meme_security_check_fails_when_file_policy_missing(monkeypatch, capsys):
    class FakeGenerator:
        def __init__(self, project_path):
            self.project_path = project_path
            self.max_download_bytes = 15 * 1024 * 1024

    monkeypatch.setattr(meme_cli, "MemeGenerator", FakeGenerator)
    monkeypatch.setattr(meme_cli.meme_lab_route, "MAX_HISTORY_ENTRIES", 2000)
    monkeypatch.setattr(meme_cli.inspect, "getsource", lambda _fn: "some unrelated source")

    with pytest.raises(typer.Exit) as exc:
        meme_cli.meme_security_check(path=".")
    output = capsys.readouterr().out
    assert exc.value.exit_code == 1
    assert "FAIL reports_subtree_file_policy" in output
