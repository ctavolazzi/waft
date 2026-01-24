"""
Telemetry utilities for Narcissus Protocol experiments.
"""

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _flight_recorder_path(base_path: Path) -> Path:
    return base_path / "_pyrite" / "flight_recorder.json"


def load_events(base_path: Path) -> list[dict[str, Any]]:
    path = _flight_recorder_path(base_path)
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def write_events(base_path: Path, events: list[dict[str, Any]]) -> None:
    path = _flight_recorder_path(base_path)
    path.write_text(json.dumps(events, indent=2), encoding="utf-8")


def record_event(base_path: Path, event: dict[str, Any]) -> None:
    events = load_events(base_path)
    event["recorded_at"] = datetime.now(timezone.utc).isoformat()
    events.append(event)
    write_events(base_path, events)


def wilson_interval(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    if total == 0:
        return 0.0, 1.0
    p = successes / total
    denom = 1 + (z * z) / total
    center = (p + (z * z) / (2 * total)) / denom
    margin = (z * math.sqrt((p * (1 - p) + (z * z) / (4 * total)) / total)) / denom
    return max(0.0, center - margin), min(1.0, center + margin)


def _select_run(events: list[dict[str, Any]], run_id: str | None = None) -> tuple[list[dict[str, Any]], str | None]:
    run_ids = [e.get("run_id") for e in events if e.get("run_id")]
    selected_run = run_id or (max(run_ids) if run_ids else None)
    if selected_run:
        return [e for e in events if e.get("run_id") == selected_run], selected_run
    return events, None


def summarize(events: list[dict[str, Any]], run_id: str | None = None) -> dict[str, Any]:
    events, selected_run = _select_run(events, run_id)
    experimental = [e for e in events if e.get("condition") == "experimental"]
    control = [e for e in events if e.get("condition") == "control"]

    exp_success = sum(1 for e in experimental if e.get("bug_removed"))
    exp_total = len(experimental)
    ctrl_success = sum(1 for e in control if (not e.get("bug_injected")) and (not e.get("bug_present_after")))
    ctrl_total = len(control)

    exp_ci = wilson_interval(exp_success, exp_total)
    ctrl_ci = wilson_interval(ctrl_success, ctrl_total)

    return {
        "run_id": selected_run,
        "total_trials": len(events),
        "experimental": {
            "success": exp_success,
            "total": exp_total,
            "rate": exp_success / exp_total if exp_total else 0.0,
            "ci_95": exp_ci,
        },
        "control": {
            "success": ctrl_success,
            "total": ctrl_total,
            "rate": ctrl_success / ctrl_total if ctrl_total else 0.0,
            "ci_95": ctrl_ci,
        },
    }


def write_report(base_path: Path, summary: dict[str, Any], events: list[dict[str, Any]]) -> Path:
    reports_dir = base_path / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_path = reports_dir / "waft_narcissus_protocol_report.md"

    lines = [
        "# WAFT Narcissus Protocol — Phase 1 Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()} UTC",
        "",
        "## Summary",
        f"- Run ID: {summary.get('run_id')}",
        f"- Total trials: {summary['total_trials']}",
        f"- Experimental success rate: {summary['experimental']['rate']:.2%}",
        f"- Experimental 95% CI: {summary['experimental']['ci_95'][0]:.2%} – {summary['experimental']['ci_95'][1]:.2%}",
        f"- Control pass rate: {summary['control']['rate']:.2%}",
        f"- Control 95% CI: {summary['control']['ci_95'][0]:.2%} – {summary['control']['ci_95'][1]:.2%}",
        "",
        "## Experimental Design",
        "- Conditions: control (no sabotage) vs experimental (NARCISSUS_LOGIC_FRACTURE injected)",
        "- Outcome: bug removed after NarcissusAgent proposes patch",
        "- Safety: propose_patch validates syntax and writes backups",
        "",
        "## Notable Failures (Mirage Events)",
    ]

    failures = [e for e in events if e.get("condition") == "experimental" and not e.get("bug_removed")]
    if failures:
        for entry in failures[:10]:
            lines.append(
                f"- Trial {entry.get('trial')} | patch_attempted={entry.get('patch_attempted')} | note={entry.get('decision_note')}"
            )
    else:
        lines.append("- None in this batch.")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def main() -> None:
    base_path = Path(__file__).resolve().parents[1]
    events = load_events(base_path)
    summary = summarize(events)

    print("Narcissus Protocol — Phase 1 Summary")
    if summary.get("run_id"):
        print(f"Run ID: {summary['run_id']}")
    print(f"Total trials: {summary['total_trials']}")
    print(
        "Experimental success: "
        f"{summary['experimental']['success']}/{summary['experimental']['total']} "
        f"({summary['experimental']['rate']:.2%})"
    )
    print(
        "Control pass: "
        f"{summary['control']['success']}/{summary['control']['total']} "
        f"({summary['control']['rate']:.2%})"
    )

    report_path = write_report(base_path, summary, events)
    print(f"Report written to {report_path}")


if __name__ == "__main__":
    main()
