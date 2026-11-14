"""`waft lab` from the command line, in a scratch folder: run, verify, show, share, doctor."""

import re
import subprocess
import sys

import pytest
from typer.testing import CliRunner

from waft.main import app

runner = CliRunner()
SMALL = ["--generations", "3", "--population", "6", "--trials", "2"]


def plain(output: str) -> str:
    return re.sub(r"\s+", " ", output)


@pytest.fixture
def workdir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("COLUMNS", "200")
    return tmp_path


@pytest.fixture
def made(workdir):
    result = runner.invoke(app, ["lab", "run", *SMALL, "--no-video"])
    assert result.exit_code == 0, result.output[-800:]
    run_dir = next((workdir / "lab-runs").iterdir())
    head = re.search(r"head\s+([0-9a-f]{64})", plain(result.output)).group(1)
    return result, run_dir, head


def test_run_records_a_verifiable_run_and_writes_only_there(workdir, made):
    result, run_dir, head = made
    out = plain(result.output)

    assert "scoring controls: pass" in out and "evolution: pass" in out
    assert "simulated agents (scripted fake model)" in out
    assert [p.name for p in workdir.iterdir()] == ["lab-runs"]
    assert (run_dir / "chain.jsonl").exists()
    assert (run_dir / "share" / "card.png").exists() and (run_dir / "share" / "replay.html").exists()


def test_verify_passes_with_the_head_and_fails_with_another(made):
    _result, run_dir, head = made

    good = runner.invoke(app, ["lab", "verify", str(run_dir), "--expect-head", head])
    bad = runner.invoke(app, ["lab", "verify", str(run_dir), "--expect-head", "0" * 64, "--no-node"])

    assert good.exit_code == 0 and "python verifier: intact" in plain(good.output)
    assert bad.exit_code == 1 and "E_HEAD" in bad.output


def test_verify_without_a_head_says_what_that_does_not_prove(made):
    result = runner.invoke(app, ["lab", "verify", "--no-node"])  # no run named: the newest one
    assert result.exit_code == 0
    assert "not that it is the one that was published" in plain(result.output)


def test_verify_catches_an_edit(made):
    _result, run_dir, head = made
    chain = run_dir / "chain.jsonl"
    chain.write_text(chain.read_text().replace("scripted fake model", "a real model", 1))

    result = runner.invoke(app, ["lab", "verify", str(run_dir), "--expect-head", head, "--no-node"])

    assert result.exit_code == 1 and "NOT INTACT" in result.output


def test_show_prints_the_generations_the_champion_and_the_checks(made):
    result = runner.invoke(app, ["lab", "show"])
    out = plain(result.output)

    assert result.exit_code == 0
    assert "first-try wins" in out and "champion g_" in out
    assert "an agent that says nothing scores zero" in out
    assert "every variant in a generation has its own id" in out


def test_share_refuses_a_run_that_does_not_verify(made):
    _result, run_dir, _head = made
    chain = run_dir / "chain.jsonl"
    chain.write_text(chain.read_text().replace('"ok":true', '"ok":false', 1))

    result = runner.invoke(app, ["lab", "share", str(run_dir), "--no-video"])

    assert result.exit_code == 1 and "does not verify" in result.output


def test_share_writes_where_it_is_told(made, workdir):
    _result, run_dir, _head = made
    result = runner.invoke(app, ["lab", "share", str(run_dir), "--out", "out", "--no-video"])
    assert result.exit_code == 0
    assert sorted(p.name for p in (workdir / "out").iterdir()) == ["card.png", "replay.html"]


def test_the_same_seed_twice_prints_the_same_digest_and_different_heads(workdir):
    a = plain(runner.invoke(app, ["lab", "run", *SMALL, "--no-share"]).output)
    b = plain(runner.invoke(app, ["lab", "run", *SMALL, "--no-share"]).output)
    digest = lambda out: re.search(r"result digest\s+([0-9a-f]{64})", out).group(1)  # noqa: E731
    head = lambda out: re.search(r"head\s+([0-9a-f]{64})", out).group(1)  # noqa: E731

    assert digest(a) == digest(b)
    assert head(a) != head(b)


def test_a_model_run_without_providers_explains_what_to_set(workdir):
    result = runner.invoke(app, ["lab", "run", "--agent", "model", *SMALL])
    assert result.exit_code == 2
    assert "WAFT_LLM_BASE_URL" in result.output
    assert not (workdir / "lab-runs").exists()


def test_bad_settings_and_missing_runs_are_refused_clearly(workdir):
    assert runner.invoke(app, ["lab", "run", "--agent", "wizard"]).exit_code == 2
    assert runner.invoke(app, ["lab", "run", "--population", "1"]).exit_code == 2
    missing = runner.invoke(app, ["lab", "show"])
    assert missing.exit_code == 2 and "waft lab run" in missing.output


def test_the_doctor_passes_here(workdir):
    result = runner.invoke(app, ["lab", "doctor"])
    assert result.exit_code == 0, result.output[-800:]
    assert "FAIL" not in result.output and "All good." in result.output
    assert list(workdir.iterdir()) == []  # the doctor leaves nothing behind


def test_the_installed_command_works_in_a_fresh_process(workdir):
    done = subprocess.run(
        [sys.executable, "-m", "waft.main", "lab", "run", *SMALL, "--no-share", "--no-replay"],
        capture_output=True, text=True, timeout=180,
    )
    assert done.returncode == 0, done.stderr[-600:]
    assert "evolution:" in done.stdout
