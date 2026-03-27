#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import webbrowser
from datetime import datetime
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True)


def init_repo(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    run(["git", "init"], cwd=path)


def build_pass_candidate(path: Path) -> None:
    (path / "src" / "waft").mkdir(parents=True, exist_ok=True)
    (path / "tests").mkdir(parents=True, exist_ok=True)
    (path / "docs").mkdir(parents=True, exist_ok=True)
    (path / "src" / "waft" / "core.py").write_text("VALUE = 42\n", encoding="utf-8")
    (path / "tests" / "test_core.py").write_text(
        "def test_value():\n    assert 42 == 42\n", encoding="utf-8"
    )
    (path / "docs" / "candidate.md").write_text("# Candidate\n", encoding="utf-8")


def build_fail_candidate(path: Path) -> None:
    (path / "_pyrite").mkdir(parents=True, exist_ok=True)
    (path / "src" / "waft").mkdir(parents=True, exist_ok=True)
    (path / "_pyrite" / "journal.md").write_text("private notes\n", encoding="utf-8")
    (path / "src" / "waft" / "core.py").write_text("VALUE = -1\n", encoding="utf-8")


def build_borderline_candidate(path: Path) -> None:
    (path / "src" / "waft").mkdir(parents=True, exist_ok=True)
    (path / "tests").mkdir(parents=True, exist_ok=True)
    (path / "src" / "waft" / "core.py").write_text("VALUE = 7\n", encoding="utf-8")
    (path / "tests" / "test_core.py").write_text(
        "def test_value():\n    assert 7 == 7\n", encoding="utf-8"
    )


def run_review(repo_path: Path, report_path: Path) -> subprocess.CompletedProcess[str]:
    cmd = [
        sys.executable,
        "-m",
        "waft.main",
        "promote",
        "review",
        "--path",
        str(repo_path),
        "--target-repo",
        "FogSift/waft",
        "--min-score",
        "8",
        "--max-files",
        "30",
        "--output",
        str(report_path),
        "--json",
    ]
    return run(cmd)


def parse_json_line(stdout: str) -> dict:
    for line in stdout.splitlines()[::-1]:
        text = line.strip()
        if text.startswith("{") and text.endswith("}"):
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                continue
    return {}


def render_gate_badges(result_json: dict) -> str:
    failed = result_json.get("failed_gates", [])
    if not failed:
        return "<span class='badge ok'>all gates pass</span>"
    return "".join(f"<span class='badge fail'>{gate}</span>" for gate in failed)


def write_demo_html(
    output_dir: Path,
    pass_result: subprocess.CompletedProcess[str],
    borderline_result: subprocess.CompletedProcess[str],
    fail_result: subprocess.CompletedProcess[str],
    pass_report: Path,
    borderline_report: Path,
    fail_report: Path,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    pass_json = parse_json_line(pass_result.stdout)
    borderline_json = parse_json_line(borderline_result.stdout)
    fail_json = parse_json_line(fail_result.stdout)
    html_path = output_dir / "promotion_review_demo.html"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>WAFT Promotion Review Demo</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; background: #f7f7f7; color: #1f1f1f; }}
    h1 {{ margin-bottom: 4px; }}
    .meta {{ color: #555; margin-bottom: 20px; }}
    .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }}
    @media (max-width: 1180px) {{ .grid {{ grid-template-columns: 1fr; }} }}
    .card {{ background: white; border: 1px solid #ddd; border-radius: 10px; padding: 16px; }}
    .pass {{ border-left: 6px solid #2e7d32; }}
    .warn {{ border-left: 6px solid #ef6c00; }}
    .fail {{ border-left: 6px solid #c62828; }}
    .badges {{ margin-top: 8px; }}
    .badge {{ display: inline-block; padding: 4px 8px; margin: 2px 6px 2px 0; border-radius: 999px; font-size: 12px; }}
    .badge.ok {{ background: #e8f5e9; color: #1b5e20; border: 1px solid #a5d6a7; }}
    .badge.fail {{ background: #ffebee; color: #b71c1c; border: 1px solid #ef9a9a; }}
    code {{ background: #efefef; padding: 2px 5px; border-radius: 4px; }}
    .small {{ color: #666; font-size: 12px; }}
    a {{ color: #0b57d0; }}
  </style>
</head>
<body>
  <h1>WAFT Promotion Review Demo</h1>
  <div class="meta">Generated: {datetime.now().isoformat()}</div>
  <div class="grid">
    <div class="card pass">
      <h2>Promotion-Ready Candidate</h2>
      <p><strong>Exit Code:</strong> {pass_result.returncode}</p>
      <p><strong>Ready:</strong> {pass_json.get("promotion_ready", "unknown")}</p>
      <p><strong>Score:</strong> {pass_json.get("score", "n/a")}/10</p>
      <p><strong>Report:</strong> <a href="{pass_report.as_uri()}">{pass_report.name}</a></p>
      <p class="small">Changed files: {len(pass_json.get("changed_files", []))}</p>
      <div class="badges">{render_gate_badges(pass_json)}</div>
    </div>
    <div class="card warn">
      <h2>Borderline Candidate (Docs Missing)</h2>
      <p><strong>Exit Code:</strong> {borderline_result.returncode}</p>
      <p><strong>Ready:</strong> {borderline_json.get("promotion_ready", "unknown")}</p>
      <p><strong>Score:</strong> {borderline_json.get("score", "n/a")}/10</p>
      <p><strong>Report:</strong> <a href="{borderline_report.as_uri()}">{borderline_report.name}</a></p>
      <p class="small">Changed files: {len(borderline_json.get("changed_files", []))}</p>
      <div class="badges">{render_gate_badges(borderline_json)}</div>
    </div>
    <div class="card fail">
      <h2>Blocked Candidate (Internal Artifacts)</h2>
      <p><strong>Exit Code:</strong> {fail_result.returncode}</p>
      <p><strong>Ready:</strong> {fail_json.get("promotion_ready", "unknown")}</p>
      <p><strong>Score:</strong> {fail_json.get("score", "n/a")}/10</p>
      <p><strong>Report:</strong> <a href="{fail_report.as_uri()}">{fail_report.name}</a></p>
      <p class="small">Blocked files: {len(fail_json.get("blocked_files", []))}</p>
      <div class="badges">{render_gate_badges(fail_json)}</div>
    </div>
  </div>
  <h3>CLI command used</h3>
  <p><code>{sys.executable} -m waft.main promote review ...</code></p>
</body>
</html>
"""
    html_path.write_text(html, encoding="utf-8")
    return html_path


def open_in_chrome(path: Path) -> None:
    if sys.platform == "darwin":
        result = subprocess.run(["open", "-a", "Google Chrome", str(path)], capture_output=True, text=True)
        if result.returncode == 0:
            return
    webbrowser.open(path.as_uri())


def main() -> int:
    parser = argparse.ArgumentParser(description="Run an automatic promotion review demo and open in browser.")
    parser.add_argument(
        "--output-dir",
        default="demo_output",
        help="Where demo HTML and reports are stored (default: demo_output).",
    )
    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="Keep temporary candidate repos for inspection.",
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Do not open Chrome/browser automatically.",
    )
    args = parser.parse_args()

    root = Path.cwd()
    output_dir = (root / args.output_dir).resolve()

    temp_ctx = tempfile.TemporaryDirectory(prefix="waft_promotion_demo_")
    temp_root = Path(temp_ctx.name)
    pass_repo = temp_root / "candidate_pass"
    borderline_repo = temp_root / "candidate_borderline"
    fail_repo = temp_root / "candidate_fail"
    init_repo(pass_repo)
    init_repo(borderline_repo)
    init_repo(fail_repo)
    build_pass_candidate(pass_repo)
    build_borderline_candidate(borderline_repo)
    build_fail_candidate(fail_repo)

    pass_report = output_dir / "promotion_review_pass.md"
    borderline_report = output_dir / "promotion_review_borderline.md"
    fail_report = output_dir / "promotion_review_fail.md"
    pass_result = run_review(pass_repo, pass_report)
    borderline_result = run_review(borderline_repo, borderline_report)
    fail_result = run_review(fail_repo, fail_report)

    html_path = write_demo_html(
        output_dir,
        pass_result,
        borderline_result,
        fail_result,
        pass_report,
        borderline_report,
        fail_report,
    )

    print("=== Promotion Demo Complete ===")
    print(f"Output directory: {output_dir}")
    print(f"Demo page: {html_path}")
    print(f"Pass review exit code: {pass_result.returncode}")
    print(f"Borderline review exit code: {borderline_result.returncode}")
    print(f"Fail review exit code: {fail_result.returncode}")
    if pass_result.returncode != 0:
        print("\n[WARN] Pass candidate did not pass as expected. stderr:")
        print(pass_result.stderr)
    if fail_result.returncode == 0:
        print("\n[WARN] Fail candidate unexpectedly passed. stderr:")
        print(fail_result.stderr)

    if not args.no_open:
        open_in_chrome(html_path)
        open_in_chrome(pass_report)
        open_in_chrome(borderline_report)
        open_in_chrome(fail_report)

    if args.keep_temp:
        keep_path = output_dir / "temp_repos_path.txt"
        keep_path.write_text(str(temp_root), encoding="utf-8")
        print(f"Temporary repos kept at: {temp_root}")
        temp_ctx = None
    if temp_ctx is not None:
        temp_ctx.cleanup()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
