from __future__ import annotations

import json
import shlex
import subprocess
from datetime import datetime
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Promotion review commands for professional escalation")
console = Console()


@app.command("review")
def review(
    path: str = typer.Option(".", "--path", "-p", help="Project path to review"),
    target_repo: str = typer.Option(
        "FogSift/waft", "--target-repo", help="Professional destination repository"
    ),
    max_files: int = typer.Option(
        30, "--max-files", help="Maximum changed files allowed for clean promotion batch"
    ),
    min_score: int = typer.Option(
        8, "--min-score", help="Minimum readiness score (0-10) for promotion"
    ),
    docs_exempt: bool = typer.Option(
        False, "--docs-exempt", help="Allow review pass without docs updates"
    ),
    run_tests: bool = typer.Option(
        False, "--run-tests", help="Run test command as part of quality gate"
    ),
    test_command: str = typer.Option(
        "python -m pytest -q", "--test-command", help="Test command when --run-tests is enabled"
    ),
    output: str = typer.Option(
        "",
        "--output",
        help="Output markdown report path (default: _work_efforts/reports/promotion_review_*.md)",
    ),
    json_out: bool = typer.Option(False, "--json", help="Print machine-readable JSON summary"),
):
    """
    Review local changes and score promotion readiness for FogSift/waft.
    """
    project_path = Path(path).expanduser().resolve()

    git_root_result = subprocess.run(
        ["git", "-C", str(project_path), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
    )
    if git_root_result.returncode != 0:
        console.print("[red]❌ Not inside a git repository.[/red]")
        raise typer.Exit(1)

    git_root = Path(git_root_result.stdout.strip())

    status_result = subprocess.run(
        ["git", "-C", str(git_root), "status", "--porcelain", "--untracked-files=all"],
        capture_output=True,
        text=True,
    )
    lines = [line for line in status_result.stdout.splitlines() if line.strip()]
    changed_files: list[str] = []
    for line in lines:
        path_part = line[3:].strip()
        if " -> " in path_part:
            path_part = path_part.split(" -> ", 1)[1].strip()
        changed_files.append(path_part)

    blocked_prefixes = (
        "_work_efforts/",
        "_pyrite/",
        ".empirica/",
        ".waft/",
        "agent-transcripts/",
    )
    blocked_files = [f for f in changed_files if any(f.startswith(prefix) for prefix in blocked_prefixes)]

    risky_names = {"credentials.json", "secrets.json", ".env", "id_rsa", "id_dsa"}
    risky_suffixes = {".pem", ".p12", ".key"}
    risky_files = [
        f
        for f in changed_files
        if Path(f).name in risky_names or Path(f).suffix.lower() in risky_suffixes
    ]

    has_src_changes = any(f.startswith("src/") for f in changed_files)
    has_test_changes = any(f.startswith("tests/") for f in changed_files)
    has_docs_changes = any(f.startswith("docs/") or f == "README.md" for f in changed_files)

    scope_ok = 0 < len(changed_files) <= max_files
    docs_ok = has_docs_changes or docs_exempt
    professional_ok = len(blocked_files) == 0
    security_ok = len(risky_files) == 0 and len(blocked_files) == 0

    test_rc = None
    if run_tests:
        test_rc = subprocess.run(
            shlex.split(test_command),
            cwd=str(git_root),
        ).returncode
        quality_ok = test_rc == 0
    else:
        quality_ok = (not has_src_changes) or has_test_changes

    gates = [
        ("scope", scope_ok, f"{len(changed_files)} changed files (max {max_files})"),
        ("quality", quality_ok, "tests pass or src unchanged/tests updated"),
        ("docs", docs_ok, "docs/README updated or docs-exempt set"),
        (
            "professional_surface",
            professional_ok,
            "no internal-only artifact paths in change set",
        ),
        ("security", security_ok, "no risky secret-like files"),
    ]
    gate_results = [{"name": name, "passed": passed, "detail": detail} for name, passed, detail in gates]
    failed_gates = [name for name, passed, _ in gates if not passed]

    score = sum(2 for _, passed, _ in gates if passed)
    all_gates_pass = all(passed for _, passed, _ in gates)
    promotion_ready = all_gates_pass and score >= min_score

    report_path = (
        Path(output).expanduser().resolve()
        if output.strip()
        else (
            git_root
            / "_work_efforts"
            / "reports"
            / f"promotion_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)

    report = [
        "# Promotion Review Report",
        "",
        f"- **Timestamp:** {datetime.now().isoformat()}",
        f"- **Project:** `{git_root}`",
        f"- **Target Repo:** `{target_repo}`",
        f"- **Score:** `{score}/10` (min `{min_score}`)",
        f"- **Promotion Ready:** `{'yes' if promotion_ready else 'no'}`",
        "",
        "## Gates",
        "",
        "| Gate | Status | Detail |",
        "|---|---|---|",
    ]
    for name, passed, detail in gates:
        report.append(f"| `{name}` | {'PASS' if passed else 'FAIL'} | {detail} |")

    report.extend(["", "## Changed Files", ""])
    report.extend([f"- `{f}`" for f in changed_files] if changed_files else ["- _none_"])
    report.extend(["", "## Blocked/Internal Files", ""])
    report.extend([f"- `{f}`" for f in blocked_files] if blocked_files else ["- _none_"])
    report.extend(["", "## Risky Files", ""])
    report.extend([f"- `{f}`" for f in risky_files] if risky_files else ["- _none_"])
    if run_tests:
        report.extend(["", "## Test Command", "", f"- `{test_command}`", f"- return code: `{test_rc}`"])

    report_path.write_text("\n".join(report) + "\n", encoding="utf-8")

    table = Table(title="Promotion Review")
    table.add_column("Gate")
    table.add_column("Status")
    table.add_column("Detail")
    for name, passed, detail in gates:
        table.add_row(name, "[green]PASS[/green]" if passed else "[red]FAIL[/red]", detail)
    console.print(table)
    console.print(f"\nScore: [bold]{score}/10[/bold] (min {min_score})")
    console.print(f"Report: {report_path}")
    console.print(
        "[bold green]✅ Ready for professional escalation[/bold green]"
        if promotion_ready
        else "[bold yellow]⚠️ Not ready for escalation yet[/bold yellow]"
    )

    if json_out:
        print(
            json.dumps(
                {
                    "target_repo": target_repo,
                    "score": score,
                    "min_score": min_score,
                    "promotion_ready": promotion_ready,
                    "changed_files": changed_files,
                    "blocked_files": blocked_files,
                    "risky_files": risky_files,
                    "gate_results": gate_results,
                    "failed_gates": failed_gates,
                    "report_path": str(report_path),
                },
                separators=(",", ":"),
            )
        )

    raise typer.Exit(0 if promotion_ready else 1)
