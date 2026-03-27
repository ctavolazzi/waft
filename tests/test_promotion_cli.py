"""Tests for promotion review CLI."""

import subprocess
from pathlib import Path

from typer.testing import CliRunner

from waft.cli.promotion_cli import app


runner = CliRunner()


def test_promote_review_help():
    """Promotion review command exposes help."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "promotion" in result.stdout.lower()


def test_promote_review_passes_with_clean_candidate(tmp_path: Path):
    """Review passes with scoped src+tests+docs candidate."""
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True, text=True)

    (tmp_path / "src" / "waft").mkdir(parents=True, exist_ok=True)
    (tmp_path / "tests").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs").mkdir(parents=True, exist_ok=True)

    (tmp_path / "src" / "waft" / "core.py").write_text("VALUE = 1\n", encoding="utf-8")
    (tmp_path / "tests" / "test_core.py").write_text("def test_x():\n    assert 1 == 1\n", encoding="utf-8")
    (tmp_path / "docs" / "note.md").write_text("# Note\n", encoding="utf-8")

    report = tmp_path / "promotion_report.md"
    result = runner.invoke(
        app,
        [
            "--path",
            str(tmp_path),
            "--max-files",
            "20",
            "--min-score",
            "8",
            "--output",
            str(report),
        ],
    )
    assert result.exit_code == 0
    assert report.exists()
    content = report.read_text(encoding="utf-8")
    assert "Promotion Review Report" in content
    assert "Promotion Ready" in content


def test_promote_review_fails_with_internal_artifacts(tmp_path: Path):
    """Review fails when internal-only artifacts are included."""
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True, text=True)
    (tmp_path / "_pyrite").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs").mkdir(parents=True, exist_ok=True)
    (tmp_path / "_pyrite" / "journal.md").write_text("private\n", encoding="utf-8")
    (tmp_path / "docs" / "public.md").write_text("public\n", encoding="utf-8")

    result = runner.invoke(app, ["--path", str(tmp_path), "--output", str(tmp_path / "r.md")])
    assert result.exit_code == 1
    assert "Not ready for escalation yet" in result.stdout
