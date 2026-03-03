#!/usr/bin/env python3
"""Generate recent work report artifacts and a hub page."""

from __future__ import annotations

import argparse
import json
import logging
import math
import os
import re
import subprocess
import sys
import time
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path

import markdown

LOGGER = logging.getLogger("waft.sitrep")


def _configure_logging() -> None:
    level_name = os.getenv("WAFT_SITREP_LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    if LOGGER.handlers:
        LOGGER.setLevel(level)
        return
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    LOGGER.addHandler(handler)
    LOGGER.setLevel(level)
    LOGGER.propagate = False


def _runtime_trace() -> dict:
    expected_major = 3
    expected_minor = 14
    expected_pyenv = "3.14.3"
    actual_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    pyenv_version = os.getenv("PYENV_VERSION", "").strip()
    virtual_env = os.getenv("VIRTUAL_ENV", "").strip()
    is_314 = sys.version_info.major == expected_major and sys.version_info.minor == expected_minor
    if is_314 and pyenv_version.startswith("3.14"):
        reason = "Pinned Python 3.14 runtime confirmed (PYENV_VERSION and interpreter match)."
    elif is_314 and pyenv_version:
        reason = (
            f"Interpreter is Python 3.14, but PYENV_VERSION is '{pyenv_version}' "
            "instead of a 3.14 pin."
        )
    elif is_314:
        reason = "Interpreter is Python 3.14, but PYENV_VERSION is unset (shell default/runtime shim selected it)."
    else:
        reason = (
            f"Interpreter resolved to Python {sys.version_info.major}.{sys.version_info.minor}. "
            "Expected 3.14. /sitrep likely ran without the 3.14 pin or with a different python resolver."
        )
    return {
        "expected": f"{expected_major}.{expected_minor}.x (PYENV_VERSION={expected_pyenv})",
        "actual_version": actual_version,
        "python_executable": sys.executable,
        "pyenv_version": pyenv_version,
        "virtual_env": virtual_env,
        "is_expected": is_314 and (pyenv_version.startswith("3.14") or not pyenv_version),
        "reason": reason,
    }


def _print_runtime_trace(runtime: dict) -> None:
    print("=== Runtime Trace ===")
    print(f"Expected: {runtime['expected']}")
    print(f"Resolved: Python {runtime['actual_version']}")
    print(f"Executable: {runtime['python_executable']}")
    print(f"PYENV_VERSION: {runtime['pyenv_version'] or '(unset)'}")
    print(f"VIRTUAL_ENV: {runtime['virtual_env'] or '(unset)'}")
    print(f"Status: {'OK' if runtime['is_expected'] else 'MISMATCH'}")
    print(f"Reason: {runtime['reason']}")
    print("")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build recent work report artifacts and a report hub page."
    )
    parser.add_argument("--work-efforts-dir", default="_work_efforts")
    parser.add_argument("--devlog", default="_work_efforts/devlog.md")
    parser.add_argument("--output-dir", default="_work_efforts/reports")
    parser.add_argument("--work-effort-count", type=int, default=12)
    parser.add_argument("--devlog-sections", type=int, default=10)
    parser.add_argument("--hub-max-runs", type=int, default=240)
    parser.add_argument("--no-open", action="store_true")
    return parser.parse_args()


def _extract_section(lines: list[str], heading: str) -> list[str]:
    start = -1
    for i, line in enumerate(lines):
        if line.strip().lower() == heading.lower():
            start = i + 1
            break
    if start == -1:
        return []
    end = len(lines)
    for i in range(start, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    return lines[start:end]


def _first_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Untitled"


def _frontmatter_value(text: str, key: str) -> str:
    m = re.search(rf"(?m)^{re.escape(key)}:\s*(.+)$", text)
    if not m:
        return ""
    return m.group(1).strip().strip('"')


def _recent_work_efforts(work_efforts_dir: Path, count: int) -> list[Path]:
    candidates = []
    patterns = [
        "WE-*/WE-*_index.md",
        "CHECKPOINT_*.md",
        "SESSION_RECAP_*.md",
        "HANDOFF_BRIEF_*.md",
        "CRITIQUE_*.md",
        "VALIDATION_*.md",
    ]
    for pattern in patterns:
        candidates.extend(work_efforts_dir.glob(pattern))
    unique = list({p.resolve(): p for p in candidates}.values())
    unique.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return unique[: max(1, count)]


def _recent_devlog_sections(devlog_text: str, limit: int) -> list[tuple[str, str]]:
    lines = devlog_text.splitlines()
    indices = [i for i, line in enumerate(lines) if line.startswith("## ")]
    if not indices:
        body = "\n".join(lines[-80:])
        return [("Latest Notes", body)]
    out: list[tuple[str, str]] = []
    for i in indices[-limit:]:
        heading = lines[i][3:].strip()
        end = len(lines)
        for j in range(i + 1, len(lines)):
            if lines[j].startswith("## "):
                end = j
                break
        block = "\n".join(lines[i + 1 : end]).strip()
        out.append((heading, block))
    return out


def _render_markdown(
    generated_at: str,
    work_efforts_dir: Path,
    work_files: list[Path],
    devlog_sections: list[tuple[str, str]],
    runtime: dict,
) -> str:
    lines: list[str] = []
    lines.append("# WAFT Recent Work Report")
    lines.append("")
    lines.append(f"- Generated: `{generated_at}`")
    lines.append(f"- Work effort root: `{work_efforts_dir}`")
    lines.append(f"- Files reviewed: `{len(work_files)}` work-effort artifacts + `{len(devlog_sections)}` devlog sections")
    lines.append("")
    lines.append("## Runtime Trace")
    lines.append("")
    lines.append(f"- Expected: `{runtime['expected']}`")
    lines.append(f"- Resolved: `Python {runtime['actual_version']}`")
    lines.append(f"- Executable: `{runtime['python_executable']}`")
    lines.append(f"- PYENV_VERSION: `{runtime['pyenv_version'] or '(unset)'}`")
    lines.append(f"- VIRTUAL_ENV: `{runtime['virtual_env'] or '(unset)'}`")
    lines.append(f"- Status: `{'OK' if runtime['is_expected'] else 'MISMATCH'}`")
    lines.append(f"- Reason: {runtime['reason']}")
    lines.append("")
    lines.append("## Executive Snapshot")
    lines.append("")
    lines.append(
        "This report consolidates the latest indexed work efforts/checkpoints/session recaps and the newest devlog sections into one readable artifact."
    )
    lines.append("")
    lines.append("## Recent Work Efforts")
    lines.append("")
    for path in work_files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        title = _frontmatter_value(text, "title") or _first_heading(text)
        status = _frontmatter_value(text, "status") or "n/a"
        updated = _frontmatter_value(text, "last_updated")
        rel = path.relative_to(work_efforts_dir.parent)
        stat_time = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        lines.append(f"### {title}")
        lines.append("")
        lines.append(f"- File: `{rel}`")
        lines.append(f"- Status: `{status}`")
        lines.append(f"- Last Updated (frontmatter): `{updated or 'n/a'}`")
        lines.append(f"- Last Modified (filesystem): `{stat_time}`")
        lines.append("")
        progress = _extract_section(text.splitlines(), "## Progress")
        if progress:
            lines.append("Progress highlights:")
            shown = 0
            for line in progress:
                if line.strip().startswith("- "):
                    lines.append(line.rstrip())
                    shown += 1
                if shown >= 5:
                    break
            if shown == 0:
                snippet = "\n".join(progress[:8]).strip()
                if snippet:
                    lines.append("")
                    lines.append("```text")
                    lines.append(snippet)
                    lines.append("```")
        else:
            snippet = "\n".join(text.splitlines()[:18]).strip()
            lines.append("Excerpt:")
            lines.append("")
            lines.append("```text")
            lines.append(snippet)
            lines.append("```")
        lines.append("")
    lines.append("## Recent Devlog Sections")
    lines.append("")
    for heading, block in devlog_sections:
        lines.append(f"### {heading}")
        lines.append("")
        snippet = block.strip() or "(No body text in this section.)"
        lines.append("```text")
        lines.append(snippet[:4500])
        lines.append("```")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def _render_html(markdown_text: str, generated_at: str) -> str:
    body = markdown.markdown(
        markdown_text,
        extensions=["tables", "fenced_code", "sane_lists", "toc"],
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>WAFT Recent Work Report</title>
  <style>
    :root {{
      --bg: #f5f0e6;
      --paper: #faf8f3;
      --ink: #3a312b;
      --muted: #7a6b5d;
      --line: #d4c4a8;
      --accent: #e07b3c;
      --accent-dark: #4a2c2a;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 32px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--ink);
      line-height: 1.6;
    }}
    .wrap {{
      max-width: 980px;
      margin: 0 auto;
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 28px 30px;
      box-shadow: 6px 6px 0 var(--accent-dark);
    }}
    h1, h2, h3 {{
      color: var(--accent-dark);
      line-height: 1.25;
    }}
    h1 {{ margin-top: 0; }}
    h2 {{
      margin-top: 28px;
      border-top: 1px dashed var(--line);
      padding-top: 16px;
    }}
    code {{
      background: #efe8da;
      padding: 2px 6px;
      border-radius: 6px;
      font-size: 0.95em;
    }}
    pre {{
      background: #efe8da;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      overflow-x: auto;
    }}
    .stamp {{
      color: var(--muted);
      font-size: 0.9rem;
      margin-top: -10px;
      margin-bottom: 18px;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="stamp">Generated {generated_at}</div>
    {body}
  </div>
</body>
</html>
"""


def _parse_run_id(name: str) -> str:
    m = re.search(r"recent_work_report_(\d{8}_\d{6})", name)
    if m:
        return m.group(1)
    return ""


def _run_id_to_datetime(run_id: str) -> datetime | None:
    try:
        return datetime.strptime(run_id, "%Y%m%d_%H%M%S")
    except ValueError:
        return None


def _parse_generated_at(value: str) -> datetime | None:
    text = value.strip()
    if not text:
        return None
    fmts = [
        "%Y-%m-%d %H:%M:%S %Z",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
    ]
    for fmt in fmts:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def _load_index(index_path: Path) -> dict:
    if not index_path.exists():
        return {"latest_run_id": "", "reports": []}
    try:
        payload = json.loads(index_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        LOGGER.warning("Index read failed at %s (%s); rebuilding index.", index_path, exc)
        return {"latest_run_id": "", "reports": []}
    if isinstance(payload, dict) and isinstance(payload.get("reports"), list):
        reports = [r for r in payload["reports"] if isinstance(r, dict)]
        return {"latest_run_id": str(payload.get("latest_run_id", "")), "reports": reports}
    return {"latest_run_id": "", "reports": []}


def _write_index(index_path: Path, reports: list[dict], latest_run_id: str) -> None:
    payload = {"latest_run_id": latest_run_id, "reports": reports}
    index_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _discover_report_runs(output_dir: Path) -> list[dict]:
    runs: dict[str, dict] = {}
    for path in output_dir.glob("recent_work_report_*.*"):
        if path.name.startswith("recent_work_report_latest"):
            continue
        if path.suffix not in {".md", ".html", ".pdf"}:
            continue
        run_id = _parse_run_id(path.name)
        if not run_id:
            continue
        row = runs.setdefault(run_id, {"run_id": run_id})
        key = f"{path.suffix[1:]}_path"
        row[key] = path.name
        row["title"] = f"WAFT Recent Work Report {run_id}"
        row.setdefault("generated_at", datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"))
    return list(runs.values())


def _safe_int(value: object, fallback: int = 0) -> int:
    try:
        return int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return fallback


def _freshness_tier(age_hours: float) -> str:
    if age_hours <= 24:
        return "fresh"
    if age_hours <= 72:
        return "aging"
    return "stale"


def _quality_tier(score: int) -> str:
    if score >= 90:
        return "excellent"
    if score >= 75:
        return "good"
    if score >= 55:
        return "fair"
    return "poor"


def _with_row_metrics(row: dict, output_dir: Path, now: datetime) -> dict:
    run_id = str(row.get("run_id", "")).strip()
    title = str(row.get("title", f"WAFT Recent Work Report {run_id}")).strip() or f"WAFT Recent Work Report {run_id}"
    md_name = str(row.get("md_path", "")).strip()
    html_name = str(row.get("html_path", "")).strip()
    pdf_name = str(row.get("pdf_path", "")).strip()
    has_md = bool(md_name and (output_dir / md_name).exists())
    has_html = bool(html_name and (output_dir / html_name).exists())
    has_pdf = bool(pdf_name and (output_dir / pdf_name).exists())
    missing_artifacts = 3 - sum([has_md, has_html, has_pdf])

    run_dt = _run_id_to_datetime(run_id) or _parse_generated_at(str(row.get("generated_at", "")))
    if not run_dt:
        run_dt = now
    age_hours = max(0.0, (now - run_dt).total_seconds() / 3600.0)
    freshness = _freshness_tier(age_hours)

    reasons: list[str] = []
    if missing_artifacts:
        reasons.append(f"missing:{missing_artifacts}")
    if freshness != "fresh":
        reasons.append(f"freshness:{freshness}")
    if not str(row.get("generated_at", "")).strip():
        reasons.append("generated_at:missing")
    if not reasons:
        reasons.append("complete")

    base_score = 100
    base_score -= missing_artifacts * 22
    if freshness == "aging":
        base_score -= 10
    if freshness == "stale":
        base_score -= 22
    if "generated_at:missing" in reasons:
        base_score -= 6
    quality_score = max(0, min(100, base_score))
    quality_tier = _quality_tier(quality_score)

    normalized = {
        "run_id": run_id,
        "title": title,
        "generated_at": run_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "run_ts": int(run_dt.timestamp()),
        "md_path": md_name,
        "html_path": html_name,
        "pdf_path": pdf_name,
        "has_md": has_md,
        "has_html": has_html,
        "has_pdf": has_pdf,
        "missing_artifacts": missing_artifacts,
        "freshness": freshness,
        "freshness_age_hours": round(age_hours, 2),
        "quality_score": quality_score,
        "quality_tier": quality_tier,
        "quality_reasons": reasons,
        "run_duration_ms": _safe_int(row.get("run_duration_ms"), 0),
    }
    return normalized


def _merge_reports(index_rows: list[dict], discovered_rows: list[dict], current_row: dict, output_dir: Path, now: datetime) -> list[dict]:
    merged: dict[str, dict] = {}
    for row in index_rows + discovered_rows + [current_row]:
        run_id = str(row.get("run_id", "")).strip()
        if not run_id:
            continue
        existing = merged.get(run_id, {"run_id": run_id})
        existing.update(row)
        merged[run_id] = existing
    rows = [_with_row_metrics(row, output_dir, now) for row in merged.values()]
    rows.sort(key=lambda r: int(r.get("run_ts", 0)), reverse=True)
    return rows


def _reconcile_rows(index_rows: list[dict], discovered_rows: list[dict]) -> dict:
    index_ids = {str(r.get("run_id", "")).strip() for r in index_rows if str(r.get("run_id", "")).strip()}
    disk_ids = {str(r.get("run_id", "")).strip() for r in discovered_rows if str(r.get("run_id", "")).strip()}
    indexed_only = sorted(index_ids - disk_ids, reverse=True)
    disk_only = sorted(disk_ids - index_ids, reverse=True)
    return {
        "indexed_only": indexed_only,
        "disk_only": disk_only,
        "indexed_only_count": len(indexed_only),
        "disk_only_count": len(disk_only),
    }


def _format_since(hours: float) -> str:
    if hours < 1:
        mins = max(1, round(hours * 60))
        return f"{mins}m ago"
    if hours < 48:
        return f"{round(hours)}h ago"
    days = round(hours / 24, 1)
    return f"{days}d ago"


def _delta_from_prior(current: dict, rows: list[dict]) -> dict:
    prior = rows[1] if len(rows) > 1 else None
    if not prior:
        return {
            "new_runs_since_prior": 1,
            "missing_artifact_delta": 0,
            "quality_delta": 0,
            "quality_trend": "flat",
            "prior_run_id": "",
        }
    missing_delta = int(current.get("missing_artifacts", 0)) - int(prior.get("missing_artifacts", 0))
    quality_delta = int(current.get("quality_score", 0)) - int(prior.get("quality_score", 0))
    trend = "flat"
    if quality_delta > 0:
        trend = "up"
    if quality_delta < 0:
        trend = "down"
    return {
        "new_runs_since_prior": 1,
        "missing_artifact_delta": missing_delta,
        "quality_delta": quality_delta,
        "quality_trend": trend,
        "prior_run_id": str(prior.get("run_id", "")),
    }


def _svg_quality_trend(rows: list[dict], width: int = 360, height: int = 90) -> str:
    series = list(reversed(rows[:12]))
    if not series:
        return "<svg width='100%' height='90' viewBox='0 0 360 90' preserveAspectRatio='xMidYMid meet'><text x='10' y='45'>No data</text></svg>"
    max_x = max(1, len(series) - 1)
    points = []
    for idx, row in enumerate(series):
        score = int(row.get("quality_score", 0))
        x = 10 + ((width - 20) * idx / max_x)
        y = 10 + ((height - 20) * (1 - score / 100))
        points.append(f"{x:.1f},{y:.1f}")
    polyline = " ".join(points)
    return (
        f"<svg width='100%' height='{height}' viewBox='0 0 {width} {height}' preserveAspectRatio='xMidYMid meet' aria-label='Quality trend'>"
        f"<rect x='0' y='0' width='{width}' height='{height}' fill='none' />"
        f"<polyline class='anim-line' points='{polyline}' fill='none' stroke='#4a2c2a' stroke-width='2' />"
        f"</svg>"
    )


def _svg_freshness_timeline(rows: list[dict], width: int = 360, height: int = 90) -> str:
    series = list(reversed(rows[:12]))
    if not series:
        return "<svg width='100%' height='90' viewBox='0 0 360 90' preserveAspectRatio='xMidYMid meet'><text x='10' y='45'>No data</text></svg>"
    bars = []
    bar_w = max(8, math.floor((width - 24) / max(1, len(series))))
    for idx, row in enumerate(series):
        x = 10 + idx * bar_w
        freshness = str(row.get("freshness", "stale"))
        color = "#c2410c"
        if freshness == "fresh":
            color = "#0d9488"
        elif freshness == "aging":
            color = "#d97706"
        bars.append(
            f"<rect class='anim-bar' style='animation-delay:{idx * 0.05:.2f}s' "
            f"x='{x}' y='14' width='{bar_w - 2}' height='{height - 28}' fill='{color}' opacity='0.85' />"
        )
    return f"<svg width='100%' height='{height}' viewBox='0 0 {width} {height}' preserveAspectRatio='xMidYMid meet' aria-label='Freshness timeline'>{''.join(bars)}</svg>"


def _svg_artifact_completeness(rows: list[dict], width: int = 360, height: int = 90) -> str:
    top = rows[:8]
    if not top:
        return "<svg width='100%' height='90' viewBox='0 0 360 90' preserveAspectRatio='xMidYMid meet'><text x='10' y='45'>No data</text></svg>"
    line_h = max(9, math.floor((height - 12) / len(top)))
    bars = []
    for idx, row in enumerate(top):
        complete_pct = round((3 - int(row.get("missing_artifacts", 0))) / 3 * 100)
        y = 6 + idx * line_h
        bar_w = max(0, int((width - 70) * complete_pct / 100))
        bars.append(f"<text x='4' y='{y + line_h - 2}' font-size='8'>{row.get('run_id', '')[-6:]}</text>")
        bars.append(
            f"<rect class='anim-bar' style='animation-delay:{idx * 0.05:.2f}s' "
            f"x='66' y='{y}' width='{bar_w}' height='{line_h - 3}' fill='#e07b3c' />"
        )
    return f"<svg width='100%' height='{height}' viewBox='0 0 {width} {height}' preserveAspectRatio='xMidYMid meet' aria-label='Artifact completeness'>{''.join(bars)}</svg>"


def _hub_row_html(row: dict) -> str:
    run_id = row.get("run_id", "unknown")
    title = row.get("title", f"Report {run_id}")
    generated_at = row.get("generated_at", "n/a")
    html_link = row.get("html_path", "")
    pdf_link = row.get("pdf_path", "")
    md_link = row.get("md_path", "")
    quality_tier = row.get("quality_tier", "n/a")
    quality_score = row.get("quality_score", 0)
    freshness = row.get("freshness", "stale")
    missing = row.get("missing_artifacts", 0)
    run_ts = int(row.get("run_ts", 0))
    completeness = 100 - int(missing) * 33
    reason_text = ", ".join(row.get("quality_reasons", []))
    parts = [
        (
            f"<div class='archive-card' "
            f"data-run-id='{run_id}' data-title='{title}' data-generated='{generated_at}' "
            f"data-run-ts='{run_ts}' data-quality-tier='{quality_tier}' data-quality-score='{quality_score}' "
            f"data-freshness='{freshness}' data-missing='{missing}' data-completeness='{completeness}'>"
        ),
        f"<h3>{title}</h3>",
        f"<div class='meta'>Run ID: {run_id} | Generated: {generated_at}</div>",
        (
            "<div class='chips'>"
            f"<span class='chip'>Freshness: {freshness}</span>"
            f"<span class='chip'>Quality: {quality_score} ({quality_tier})</span>"
            f"<span class='chip'>Missing: {missing}</span>"
            "</div>"
        ),
        f"<div class='meta'>Quality reasons: {reason_text}</div>",
        "<div class='links'>",
    ]
    if html_link:
        parts.append(f"<a href='{html_link}'>Open HTML</a>")
    if pdf_link:
        parts.append(f"<a href='{pdf_link}'>Open PDF</a>")
    if md_link:
        parts.append(f"<a href='{md_link}'>Source MD</a>")
    parts.append("</div></div>")
    return "".join(parts)


def _render_hub_html(
    generated_at: str,
    current: dict,
    archive_rows: list[dict],
    reconciliation: dict,
    latest_run_id: str,
    now: datetime,
    hub_max_runs: int,
) -> str:
    max_runs = max(40, min(1000, int(hub_max_runs)))
    display_rows = archive_rows[:max_runs]
    omitted_runs = max(0, len(archive_rows) - len(display_rows))
    current_links = []
    if current.get("html_path"):
        current_links.append(f"<a href='{current['html_path']}'>Current HTML</a>")
    if current.get("pdf_path"):
        current_links.append(f"<a href='{current['pdf_path']}'>Current PDF</a>")
    if current.get("md_path"):
        current_links.append(f"<a href='{current['md_path']}'>Source MD</a>")

    current_freshness = str(current.get("freshness", "stale"))
    current_quality_score = int(current.get("quality_score", 0))
    current_quality_tier = str(current.get("quality_tier", "poor"))
    current_quality_reasons = ", ".join(current.get("quality_reasons", []))
    delta = _delta_from_prior(current, archive_rows)
    stale_index_entries = reconciliation.get("indexed_only_count", 0)
    orphan_disk_runs = reconciliation.get("disk_only_count", 0)
    recent_rows = archive_rows[:10]
    recent_total = max(1, len(recent_rows))
    recent_complete = sum(1 for row in recent_rows if int(row.get("missing_artifacts", 0)) == 0)
    recent_missing_total = sum(int(row.get("missing_artifacts", 0)) for row in recent_rows)
    trend_icon = "flat"
    if delta["quality_trend"] == "up":
        trend_icon = "up"
    elif delta["quality_trend"] == "down":
        trend_icon = "down"
    status_label = "ready"
    status_reason = "Stable archive and complete artifacts."
    if orphan_disk_runs or stale_index_entries or int(current.get("missing_artifacts", 0)):
        status_label = "attention"
        status_reason = "Archive drift or missing artifacts detected."
    warnings = []
    if stale_index_entries:
        warnings.append(f"{stale_index_entries} indexed-only run(s)")
    if orphan_disk_runs:
        warnings.append(f"{orphan_disk_runs} disk-only run(s)")
    if not warnings:
        warnings.append("No index/filesystem drift detected")

    age_text = _format_since(float(current.get("freshness_age_hours", 0)))
    archive_html = "\n".join(_hub_row_html(row) for row in display_rows)
    quality_svg = _svg_quality_trend(archive_rows)
    freshness_svg = _svg_freshness_timeline(archive_rows)
    completeness_svg = _svg_artifact_completeness(archive_rows)

    throughput_24h = sum(1 for r in archive_rows if now - datetime.fromtimestamp(int(r.get("run_ts", 0))) <= timedelta(hours=24))
    throughput_7d = sum(1 for r in archive_rows if now - datetime.fromtimestamp(int(r.get("run_ts", 0))) <= timedelta(days=7))
    throughput_30d = sum(1 for r in archive_rows if now - datetime.fromtimestamp(int(r.get("run_ts", 0))) <= timedelta(days=30))
    ticker_items = [
        f"Status: {status_label}",
        f"Freshness: {current_freshness} ({age_text})",
        f"Quality: {current_quality_score} ({current_quality_tier})",
        f"Trend: {trend_icon} ({delta['quality_delta']:+d})",
        f"Runs 24h/7d/30d: {throughput_24h}/{throughput_7d}/{throughput_30d}",
        f"Artifact health: {recent_complete}/{recent_total} complete",
        f"Drift indexed-only/disk-only: {stale_index_entries}/{orphan_disk_runs}",
    ]
    ticker_text = "  •  ".join(ticker_items)
    golden_nugget = (
        f"Status is {status_label.upper()}: freshest run is {age_text}, quality is "
        f"{current_quality_score}/100 ({current_quality_tier}), and archive drift is "
        f"{stale_index_entries} indexed-only / {orphan_disk_runs} disk-only."
    )

    grouped_by_day: dict[str, list[dict]] = {}
    for row in display_rows:
        day_key = str(row.get("generated_at", "n/a"))[:10]
        grouped_by_day.setdefault(day_key, []).append(row)
    explorer_blocks = []
    for day, rows in sorted(grouped_by_day.items(), reverse=True):
        links = []
        for row in rows[:8]:
            run_id = row.get("run_id", "")
            html_path = row.get("html_path", "")
            pdf_path = row.get("pdf_path", "")
            md_path = row.get("md_path", "")
            link_parts = [f"<span class='mono'>{run_id}</span>"]
            if html_path:
                link_parts.append(f"<a href='{html_path}'>HTML</a>")
            if pdf_path:
                link_parts.append(f"<a href='{pdf_path}'>PDF</a>")
            if md_path:
                link_parts.append(f"<a href='{md_path}'>MD</a>")
            links.append(f"<div class='explorer-row'>{' | '.join(link_parts)}</div>")
        explorer_blocks.append(f"<div class='explorer-group'><h4>{day}</h4>{''.join(links)}</div>")

    archive_html = "\n".join(_hub_row_html(row) for row in display_rows)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>WAFT Sitrep Hub</title>
  <style>
    :root {{
      --bg: #f5f0e6;
      --paper: #faf8f3;
      --ink: #3a312b;
      --muted: #7a6b5d;
      --line: #d4c4a8;
      --accent: #e07b3c;
      --dark: #4a2c2a;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 28px;
      background: var(--bg);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      line-height: 1.55;
    }}
    .wrap {{
      max-width: 1040px;
      margin: 0 auto;
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 24px;
      box-shadow: 6px 6px 0 var(--dark);
      overflow: hidden;
    }}
    h1, h2, h3 {{ color: var(--dark); margin: 0 0 10px; }}
    .muted {{ color: var(--muted); margin-bottom: 16px; }}
    .ticker {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      padding: 8px 0;
      margin: 8px 0 14px;
      overflow: hidden;
      white-space: nowrap;
    }}
    .ticker-track {{
      display: inline-block;
      padding-left: 100%;
      color: var(--muted);
      font-size: 0.88rem;
      animation: ticker-scroll 28s linear infinite;
      will-change: transform;
    }}
    .hero {{
      border: 1px solid var(--line);
      border-left: 6px solid var(--accent);
      border-radius: 10px;
      padding: 16px;
      margin: 16px 0 26px;
      background: #fff7ec;
    }}
    .links a {{
      display: inline-block;
      margin-right: 10px;
      margin-bottom: 8px;
      padding: 6px 10px;
      border: 1px solid var(--line);
      border-radius: 8px;
      color: var(--dark);
      text-decoration: none;
      background: #fff;
    }}
    .archive {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 12px;
    }}
    .archive-card {{
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 12px;
      background: #fff;
      overflow: hidden;
    }}
    .meta {{
      color: var(--muted);
      font-size: 0.9rem;
      margin-bottom: 10px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 10px;
      margin: 12px 0;
    }}
    .card {{
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 12px;
      background: #fff;
      overflow: hidden;
      min-width: 0;
    }}
    .kpi {{
      font-size: 1.35rem;
      font-weight: 700;
      color: var(--dark);
      margin-top: 4px;
    }}
    .kpi-big {{
      font-size: 1.8rem;
      line-height: 1.1;
      font-weight: 800;
      color: var(--dark);
      margin-top: 4px;
    }}
    .status-dot {{
      display: inline-block;
      width: 10px;
      height: 10px;
      border-radius: 999px;
      background: #0d9488;
      margin-right: 8px;
      animation: pulse 1.8s ease-in-out infinite;
    }}
    .status-attention .status-dot {{
      background: #c2410c;
    }}
    .chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin: 8px 0;
    }}
    .chip {{
      border: 1px solid var(--line);
      border-radius: 999px;
      background: #fff;
      padding: 2px 8px;
      font-size: 0.8rem;
      color: var(--dark);
    }}
    .warning {{
      border: 1px dashed var(--line);
      border-radius: 8px;
      padding: 8px 10px;
      margin: 6px 0;
      background: #fff;
      color: var(--muted);
      font-size: 0.9rem;
    }}
    .resource-alert {{
      border: 2px solid var(--line);
      border-left: 8px solid #d97706;
      border-radius: 10px;
      background: #fff7ec;
      padding: 10px 12px;
      margin: 10px 0 16px;
    }}
    .resource-alert.critical {{
      border-left-color: #c2410c;
      background: #fff2f0;
    }}
    .resource-alert.warning {{
      border-left-color: #d97706;
      background: #fff9eb;
    }}
    .resource-alert.ok {{
      border-left-color: #0d9488;
      background: #f1fbf9;
    }}
    .resource-alert-title {{
      font-size: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--muted);
      margin-bottom: 2px;
    }}
    .resource-alert-body {{
      color: var(--dark);
      font-weight: 700;
      font-size: 1rem;
    }}
    .resource-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 8px;
      margin-top: 8px;
    }}
    .resource-stat {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 8px;
      background: #fff;
    }}
    .resource-label {{
      color: var(--muted);
      font-size: 0.78rem;
    }}
    .resource-value {{
      color: var(--dark);
      font-size: 1.05rem;
      font-weight: 700;
    }}
    .controls {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 8px;
      margin: 8px 0 14px;
    }}
    input, select {{
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 8px 10px;
      background: #fff;
      color: var(--ink);
      font: inherit;
    }}
    .result-meta {{
      color: var(--muted);
      margin: 0 0 10px;
      font-size: 0.9rem;
    }}
    .empty {{
      display: none;
      border: 1px dashed var(--line);
      border-radius: 10px;
      padding: 16px;
      color: var(--muted);
      background: #fff;
    }}
    .charts {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 10px;
      margin: 8px 0 20px;
    }}
    .charts svg {{
      display: block;
      width: 100%;
      max-width: 100%;
      height: auto;
    }}
    .anim-line {{
      stroke-dasharray: 500;
      stroke-dashoffset: 500;
      animation: draw-line 1.2s ease-out forwards;
    }}
    .anim-bar {{
      transform-origin: left center;
      animation: grow-bar 0.5s ease-out both;
    }}
    .chart-title {{
      font-size: 0.9rem;
      color: var(--muted);
      margin-bottom: 6px;
    }}
    .explorer-group {{
      border-top: 1px dashed var(--line);
      margin-top: 8px;
      padding-top: 8px;
    }}
    .explorer-row {{
      font-size: 0.9rem;
      color: var(--ink);
      margin: 4px 0;
      overflow-wrap: anywhere;
    }}
    .mono {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, "Courier New", monospace;
    }}
    .hint {{
      color: var(--muted);
      font-size: 0.85rem;
    }}
    .toast-layer {{
      position: sticky;
      top: 8px;
      z-index: 30;
      display: flex;
      justify-content: flex-end;
      pointer-events: none;
      min-height: 0;
    }}
    .toast {{
      max-width: 340px;
      border: 1px solid var(--line);
      border-left: 4px solid var(--accent);
      background: #fff;
      color: var(--ink);
      border-radius: 8px;
      padding: 8px 10px;
      box-shadow: 4px 4px 0 var(--dark);
      font-size: 0.84rem;
      opacity: 0;
      transform: translateY(-6px);
      transition: opacity 180ms ease, transform 180ms ease;
    }}
    .toast.show {{
      opacity: 1;
      transform: translateY(0);
    }}
    .nugget {{
      border: 1px solid var(--line);
      border-left: 6px solid var(--accent);
      border-radius: 10px;
      background: #fff7ec;
      padding: 12px;
      margin: 0 0 14px;
    }}
    .nugget-title {{
      font-size: 0.78rem;
      letter-spacing: 0.04em;
      color: var(--muted);
      text-transform: uppercase;
    }}
    .nugget-body {{
      margin-top: 4px;
      font-size: 1.05rem;
      font-weight: 600;
      color: var(--dark);
    }}
    .cone {{
      border: 1px solid var(--line);
      border-radius: 10px;
      background: #fff;
      padding: 10px 12px;
      margin: 8px 0 20px;
    }}
    .cone-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 6px 0;
    }}
    .cone-chip {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 5px 10px;
      color: var(--dark);
      text-decoration: none;
      background: #fff;
      font-size: 0.84rem;
    }}
    .cone-level {{
      font-size: 0.76rem;
      color: var(--muted);
      margin-right: 8px;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }}
    .prompt-lab {{
      border: 1px solid var(--line);
      border-radius: 10px;
      background: #fff;
      padding: 12px;
      margin-top: 10px;
    }}
    .prompt-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 8px;
    }}
    textarea {{
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 8px 10px;
      background: #fff;
      color: var(--ink);
      font: inherit;
      min-height: 90px;
      resize: vertical;
    }}
    .btn {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 8px 10px;
      background: #fff;
      color: var(--dark);
      cursor: pointer;
      text-decoration: none;
      display: inline-block;
      font: inherit;
    }}
    .btn:hover {{
      border-color: var(--accent);
    }}
    .hidden {{
      display: none !important;
    }}
    .low-power * {{
      animation: none !important;
      transition: none !important;
      scroll-behavior: auto !important;
    }}
    @keyframes pulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.55; transform: scale(0.92); }}
    }}
    @keyframes draw-line {{
      from {{ stroke-dashoffset: 500; }}
      to {{ stroke-dashoffset: 0; }}
    }}
    @keyframes grow-bar {{
      from {{ transform: scaleX(0); }}
      to {{ transform: scaleX(1); }}
    }}
    @keyframes ticker-scroll {{
      from {{ transform: translateX(0); }}
      to {{ transform: translateX(-100%); }}
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>WAFT Sitrep Hub</h1>
    <div class="muted">Generated {generated_at}. This hub highlights the current report and archives prior runs.</div>
    <div class="nugget">
      <div class="nugget-title">Golden Nugget</div>
      <div class="nugget-body">{golden_nugget}</div>
    </div>
    <div class="cone">
      <div class="cone-row"><span class="cone-level">Top text</span><a class="cone-chip" href="#current-sitrep">State snapshot</a><a class="cone-chip" href="#trends">Trend pulse</a></div>
      <div class="cone-row"><span class="cone-level">Evidence</span><a class="cone-chip" href="#archive">Run archive</a><a class="cone-chip" href="#explorer">Explorer</a><a class="cone-chip" href="#health">Health</a></div>
      <div class="cone-row"><span class="cone-level">Rabbit holes</span><a class="cone-chip" href="#prompt-lab">404 prompt configurator</a></div>
    </div>
    <div class="ticker"><div class="ticker-track">{ticker_text}</div></div>
    <div id="resourceAlert" class="resource-alert ok">
      <div class="resource-alert-title">System Resource Monitor</div>
      <div id="resourceAlertBody" class="resource-alert-body">Initializing adaptive monitor...</div>
      <div id="resourceFlags" class="hint"></div>
      <div class="resource-grid">
        <div class="resource-stat"><div class="resource-label">Status</div><div id="resourceStatus" class="resource-value">OK</div></div>
        <div class="resource-stat"><div class="resource-label">Event Loop Lag</div><div id="resourceLag" class="resource-value">--</div></div>
        <div class="resource-stat"><div class="resource-label">Long Tasks / min</div><div id="resourceLongTasks" class="resource-value">--</div></div>
        <div class="resource-stat"><div class="resource-label">Heap Usage</div><div id="resourceHeap" class="resource-value">n/a</div></div>
        <div class="resource-stat"><div class="resource-label">Queue Depth</div><div id="resourceQueue" class="resource-value">0</div></div>
      </div>
    </div>
    <div class="toast-layer"><div id="toast" class="toast"></div></div>
    <div class="hero" id="current-sitrep">
      <h2>Current Sitrep</h2>
      <div class="meta">Run ID: {current.get("run_id", "n/a")} | Generated: {current.get("generated_at", "n/a")}</div>
      <div class="links">{''.join(current_links)}</div>
      <div class="grid">
        <div class="card {'status-attention' if status_label == 'attention' else ''}">
          <div class="hint">Overall status</div>
          <div class="kpi-big"><span class="status-dot"></span>{status_label}</div>
          <div class="meta">{status_reason}</div>
        </div>
        <div class="card">
          <div class="hint">Recency and cadence</div>
          <div class="kpi">{age_text}</div>
          <div class="meta">Freshness: {current_freshness} | Runs (24h): {throughput_24h}</div>
        </div>
        <div class="card">
          <div class="hint">Quality trend</div>
          <div class="kpi">{current_quality_score} ({current_quality_tier})</div>
          <div class="meta">Trend: {trend_icon} ({delta["quality_delta"]:+d}) vs {delta["prior_run_id"] or "n/a"}</div>
        </div>
        <div class="card">
          <div class="hint">Artifact health (last {recent_total} runs)</div>
          <div class="kpi">{recent_complete}/{recent_total} complete</div>
          <div class="meta">Total missing artifacts: {recent_missing_total}</div>
        </div>
      </div>
      <div class="grid">
        <div class="card">
          <div class="hint">Current quality detail</div>
          <div class="kpi">{current_quality_score} / 100</div>
          <div class="meta">Tier: {current_quality_tier}</div>
          <div class="hint">Reason tags: {current_quality_reasons}</div>
        </div>
        <div class="card">
          <div class="hint">New runs since prior execution</div>
          <div class="kpi">{delta["new_runs_since_prior"]}</div>
          <div class="meta">Compared to run: {delta["prior_run_id"] or "n/a"}</div>
        </div>
        <div class="card">
          <div class="hint">Missing artifact delta</div>
          <div class="kpi">{delta["missing_artifact_delta"]:+d}</div>
        </div>
        <div class="card">
          <div class="hint">Quality trend</div>
          <div class="kpi">{delta["quality_trend"]}</div>
          <div class="meta">Score delta: {delta["quality_delta"]:+d}</div>
        </div>
      </div>
      <div class="warning">Latest-run lock: <span class="mono">{latest_run_id or "none"}</span></div>
      {''.join(f"<div class='warning'>{msg}</div>" for msg in warnings)}
    </div>
    <h2 id="trends">Trends</h2>
    <div class="grid">
      <div class="card"><div class="hint">Runs in 24h</div><div class="kpi">{throughput_24h}</div></div>
      <div class="card"><div class="hint">Runs in 7d</div><div class="kpi">{throughput_7d}</div></div>
      <div class="card"><div class="hint">Runs in 30d</div><div class="kpi">{throughput_30d}</div></div>
    </div>
    <div class="charts">
      <div class="card"><div class="chart-title">Freshness timeline</div>{freshness_svg}</div>
      <div class="card"><div class="chart-title">Quality trend (recent runs)</div>{quality_svg}</div>
      <div class="card"><div class="chart-title">Artifact completeness</div>{completeness_svg}</div>
    </div>
    <h2 id="archive">Archive</h2>
    <div class="hint">Search/filter/sort are local and file-safe; no external dependencies.</div>
    <div class="warning">Rendered runs: {len(display_rows)} / {len(archive_rows)} total{(" (resource cap active)" if omitted_runs else "")}.</div>
    {("<div class='warning'>Archive rendering is capped for responsiveness. Refine with date filters or regenerate with a higher --hub-max-runs if needed.</div>" if omitted_runs else "")}
    <div class="controls">
      <input id="search" type="text" placeholder="Search run id, title, date, path keywords" />
      <select id="qualityFilter">
        <option value="all">Quality: all</option>
        <option value="excellent">excellent</option>
        <option value="good">good</option>
        <option value="fair">fair</option>
        <option value="poor">poor</option>
      </select>
      <select id="dateFilter">
        <option value="all">Date: all</option>
        <option value="24h">Last 24h</option>
        <option value="7d">Last 7d</option>
        <option value="30d">Last 30d</option>
      </select>
      <select id="artifactFilter">
        <option value="all">Artifacts: all</option>
        <option value="complete">Complete (HTML+PDF+MD)</option>
        <option value="incomplete">Incomplete</option>
      </select>
      <select id="sortMode">
        <option value="newest">Sort: newest</option>
        <option value="quality">Sort: quality high→low</option>
        <option value="stale">Sort: stale first</option>
      </select>
    </div>
    <div class="cone-row" style="margin-top:4px; margin-bottom:10px;">
      <button id="loadMoreBtn" class="btn" type="button">Load more</button>
      <button id="showAllBtn" class="btn" type="button">Show all (may be heavy)</button>
      <span id="loadMeta" class="hint"></span>
    </div>
    <div id="resultMeta" class="result-meta"></div>
    <div class="archive">
      {archive_html}
    </div>
    <div id="emptyState" class="empty">No runs match your current filters.</div>
    <h2 id="explorer">Explorer</h2>
    <div class="hint">Grouped by day with quick links. Use this to triage report storage quickly.</div>
    <div class="card">
      {"".join(explorer_blocks)}
    </div>
    <h3 id="health">Health</h3>
    <div class="warning">Orphan files (disk-only runs): {orphan_disk_runs}</div>
    <div class="warning">Stale index entries (indexed-only runs): {stale_index_entries}</div>
    <div class="hint">Remediation: run `/sitrep` to refresh index, then remove stale artifacts if they are no longer needed.</div>
    <h2 id="prompt-lab">404 Prompt Configurator</h2>
    <div class="hint">If a route does not exist, generate a context-rich build prompt instead of dead-ending.</div>
    <div class="prompt-lab">
      <div class="prompt-grid">
        <div>
          <label for="endpointInput" class="hint">Route / endpoint to open</label>
          <input id="endpointInput" type="text" placeholder="/reports/new-slice" />
        </div>
        <div>
          <label for="desiredInput" class="hint">Desired outcome (mad-lib style)</label>
          <input id="desiredInput" type="text" placeholder="I want this route to show ..." />
        </div>
        <div>
          <label for="wireframeInput" class="hint">Wireframe notes (optional)</label>
          <input id="wireframeInput" type="text" placeholder="Hero | filters | cards | CTA" />
        </div>
        <div>
          <label for="screenshotInput" class="hint">Attach screenshot (optional)</label>
          <input id="screenshotInput" type="file" accept="image/*" />
        </div>
      </div>
      <div class="cone-row" style="margin-top:8px;">
        <button id="checkRouteBtn" class="btn">Check Route</button>
        <button id="generatePromptBtn" class="btn">Generate Prompt</button>
        <button id="copyPromptBtn" class="btn">Copy Prompt</button>
      </div>
      <div id="routeStatus" class="warning">No route check yet.</div>
      <textarea id="promptOutput" placeholder="Generated prompt will appear here..."></textarea>
      <div class="hint">Tip: Use a quick wireframe image + route goal, then paste the generated prompt into your next chat.</div>
    </div>
  </div>
  <script>
    (function() {{
      const cards = Array.from(document.querySelectorAll('.archive-card'));
      const hrefs = Array.from(document.querySelectorAll('a[href]')).map((a) => a.getAttribute('href') || '');
      const knownRoutes = new Set(hrefs.filter((h) => h && !h.startsWith('#')));
      const archive = document.querySelector('.archive');
      const resultMeta = document.getElementById('resultMeta');
      const emptyState = document.getElementById('emptyState');
      const search = document.getElementById('search');
      const qualityFilter = document.getElementById('qualityFilter');
      const dateFilter = document.getElementById('dateFilter');
      const artifactFilter = document.getElementById('artifactFilter');
      const sortMode = document.getElementById('sortMode');
      const loadMoreBtn = document.getElementById('loadMoreBtn');
      const showAllBtn = document.getElementById('showAllBtn');
      const loadMeta = document.getElementById('loadMeta');
      const toast = document.getElementById('toast');
      const resourceAlert = document.getElementById('resourceAlert');
      const resourceAlertBody = document.getElementById('resourceAlertBody');
      const resourceFlags = document.getElementById('resourceFlags');
      const resourceStatus = document.getElementById('resourceStatus');
      const resourceLag = document.getElementById('resourceLag');
      const resourceLongTasks = document.getElementById('resourceLongTasks');
      const resourceHeap = document.getElementById('resourceHeap');
      const resourceQueue = document.getElementById('resourceQueue');
      const endpointInput = document.getElementById('endpointInput');
      const desiredInput = document.getElementById('desiredInput');
      const wireframeInput = document.getElementById('wireframeInput');
      const screenshotInput = document.getElementById('screenshotInput');
      const routeStatus = document.getElementById('routeStatus');
      const promptOutput = document.getElementById('promptOutput');
      const checkRouteBtn = document.getElementById('checkRouteBtn');
      const generatePromptBtn = document.getElementById('generatePromptBtn');
      const copyPromptBtn = document.getElementById('copyPromptBtn');
      const nowTs = {int(now.timestamp())};
      let toastTimer = null;
      let activeRenderToken = 0;
      let filterTimer = null;
      const prefersReducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      const hwThreads = Number(navigator.hardwareConcurrency || 4);
      const deviceMem = Number(navigator.deviceMemory || 4);
      const lowPowerMode = prefersReducedMotion || hwThreads <= 4 || deviceMem <= 4;
      const CHUNK_SIZE = lowPowerMode ? 12 : 28;
      const DEBOUNCE_MS = lowPowerMode ? 220 : 120;
      const YIELD_MS = lowPowerMode ? 22 : 8;
      const PAGE_SIZE = lowPowerMode ? 40 : 90;
      let visibleLimit = PAGE_SIZE;
      const softwareLimits = window.WAFT_RESOURCE_LIMITS || {{}};

      const Logger = {{
        debugEnabled: localStorage.getItem('waft.sitrep.debug') === '1',
        info(...args) {{
          if (this.debugEnabled) console.info('[sitrep]', ...args);
        }},
        warn(...args) {{
          console.warn('[sitrep]', ...args);
        }},
        error(...args) {{
          console.error('[sitrep]', ...args);
        }},
      }};

      const ErrorManager = {{
        handle(error, context) {{
          Logger.error('error', context, error);
          showToast(`Error: ${{context}}`);
        }},
      }};

      function safeHandler(fn, context) {{
        return (...args) => {{
          try {{
            return fn(...args);
          }} catch (error) {{
            ErrorManager.handle(error, context);
          }}
        }};
      }}

      const HandlerManager = {{
        bind(element, eventName, handler, context) {{
          if (!element) return;
          element.addEventListener(eventName, safeHandler(handler, context));
        }},
      }};

      const RouteManager = {{
        normalize(endpoint) {{
          return (endpoint || '').trim();
        }},
        exists(endpoint) {{
          const normalized = this.normalize(endpoint);
          return knownRoutes.has(normalized) || knownRoutes.has(normalized.replace(/^\\//, ''));
        }},
      }};

      function createTaskQueueManager() {{
        let pending = [];
        let running = false;
        function runNext() {{
          if (running || !pending.length) return;
          running = true;
          const task = pending.shift();
          const done = () => {{
            running = false;
            runNext();
          }};
          if ('requestIdleCallback' in window) {{
            window.requestIdleCallback(() => {{
              try {{
                task();
              }} finally {{
                done();
              }}
            }}, {{ timeout: 80 }});
          }} else {{
            setTimeout(() => {{
              try {{
                task();
              }} finally {{
                done();
              }}
            }}, YIELD_MS);
          }}
        }}
        return {{
          enqueue(task) {{
            pending.push(task);
            runNext();
          }},
          cancelAll() {{
            pending = [];
            running = false;
          }},
          size() {{
            return pending.length;
          }},
        }};
      }}

      const RenderQueueManager = createTaskQueueManager();
      window.addEventListener('error', (event) => ErrorManager.handle(event.error || event.message, 'window.error'));
      window.addEventListener('unhandledrejection', (event) => ErrorManager.handle(event.reason, 'window.unhandledrejection'));
      if (lowPowerMode) {{
        document.body.classList.add('low-power');
      }}
      cards.forEach((card) => {{
        if (!card.dataset.searchText) {{
          card.dataset.searchText = [
            card.dataset.runId || '',
            card.dataset.title || '',
            card.dataset.generated || '',
            card.textContent || ''
          ].join(' ').toLowerCase();
        }}
      }});

      function schedule(cb) {{
        RenderQueueManager.enqueue(cb);
      }}

      function formatSeverity(sev) {{
        if (sev === 'critical') return 'CRITICAL';
        if (sev === 'warning') return 'WARNING';
        return 'OK';
      }}

      const ResourceMonitorManager = (() => {{
        const adaptiveLimits = {{
          lagWarnMs: softwareLimits.lagWarnMs || (hwThreads <= 4 ? 60 : 90),
          lagCritMs: softwareLimits.lagCritMs || (hwThreads <= 4 ? 120 : 180),
          longTaskWarnPerMin: softwareLimits.longTaskWarnPerMin || (hwThreads <= 4 ? 4 : 8),
          longTaskCritPerMin: softwareLimits.longTaskCritPerMin || (hwThreads <= 4 ? 8 : 14),
          queueWarn: softwareLimits.queueWarn || (lowPowerMode ? 80 : 140),
          queueCrit: softwareLimits.queueCrit || (lowPowerMode ? 160 : 260),
          heapWarnRatio: softwareLimits.heapWarnRatio || (deviceMem <= 4 ? 0.65 : 0.78),
          heapCritRatio: softwareLimits.heapCritRatio || (deviceMem <= 4 ? 0.82 : 0.90),
          sampleMs: softwareLimits.sampleMs || 3500,
          alertCooldownMs: softwareLimits.alertCooldownMs || 12000,
        }};
        let timerId = null;
        let longTasksInWindow = 0;
        let lastTick = performance.now();
        let lastAlertMs = 0;
        let longTaskObserver = null;

        if ('PerformanceObserver' in window) {{
          try {{
            longTaskObserver = new PerformanceObserver((list) => {{
              longTasksInWindow += list.getEntries().length;
            }});
            longTaskObserver.observe({{ entryTypes: ['longtask'] }});
          }} catch (err) {{
            Logger.warn('LongTask observer unavailable', err);
          }}
        }}

        function severityRank(level) {{
          if (level === 'critical') return 2;
          if (level === 'warning') return 1;
          return 0;
        }}

        function evaluate(snapshot) {{
          const flags = [];
          const pushFlag = (level, code, message) => flags.push({{ level, code, message }});

          if (snapshot.lagMs >= adaptiveLimits.lagCritMs) pushFlag('critical', 'lag', `Event loop lag high (${{snapshot.lagMs}}ms)`);
          else if (snapshot.lagMs >= adaptiveLimits.lagWarnMs) pushFlag('warning', 'lag', `Event loop lag elevated (${{snapshot.lagMs}}ms)`);

          if (snapshot.longTasksPerMin >= adaptiveLimits.longTaskCritPerMin) pushFlag('critical', 'longtask', `Long tasks high (${{snapshot.longTasksPerMin}}/min)`);
          else if (snapshot.longTasksPerMin >= adaptiveLimits.longTaskWarnPerMin) pushFlag('warning', 'longtask', `Long tasks elevated (${{snapshot.longTasksPerMin}}/min)`);

          if (snapshot.queueDepth >= adaptiveLimits.queueCrit) pushFlag('critical', 'queue', `Queue depth high (${{snapshot.queueDepth}})`);
          else if (snapshot.queueDepth >= adaptiveLimits.queueWarn) pushFlag('warning', 'queue', `Queue depth elevated (${{snapshot.queueDepth}})`);

          if (snapshot.heapRatio !== null) {{
            if (snapshot.heapRatio >= adaptiveLimits.heapCritRatio) pushFlag('critical', 'heap', `Heap near limit (${{Math.round(snapshot.heapRatio * 100)}}%)`);
            else if (snapshot.heapRatio >= adaptiveLimits.heapWarnRatio) pushFlag('warning', 'heap', `Heap pressure (${{Math.round(snapshot.heapRatio * 100)}}%)`);
          }}

          let overall = 'ok';
          for (const f of flags) {{
            if (severityRank(f.level) > severityRank(overall === 'ok' ? 'ok' : overall)) {{
              overall = f.level;
            }}
          }}
          return {{ overall, flags }};
        }}

        function updateUi(snapshot, evaluation) {{
          if (!resourceAlert) return;
          resourceAlert.classList.remove('ok', 'warning', 'critical');
          resourceAlert.classList.add(evaluation.overall);
          if (resourceStatus) resourceStatus.textContent = formatSeverity(evaluation.overall);
          if (resourceLag) resourceLag.textContent = `${{snapshot.lagMs}}ms`;
          if (resourceLongTasks) resourceLongTasks.textContent = String(snapshot.longTasksPerMin);
          if (resourceQueue) resourceQueue.textContent = String(snapshot.queueDepth);
          if (resourceHeap) {{
            resourceHeap.textContent = snapshot.heapRatio === null ? 'n/a' : `${{Math.round(snapshot.heapRatio * 100)}}%`;
          }}
          if (resourceFlags) {{
            resourceFlags.textContent = evaluation.flags.length
              ? `Flags: ${{evaluation.flags.map((f) => f.message).join(' | ')}}`
              : 'No resource pressure flags.';
          }}
          if (resourceAlertBody) {{
            resourceAlertBody.textContent = evaluation.flags.length
              ? evaluation.flags[0].message
              : 'Resource profile within adaptive limits.';
          }}
        }}

        function maybeAlert(evaluation) {{
          if (!evaluation.flags.length) return;
          const nowMs = Date.now();
          if (nowMs - lastAlertMs < adaptiveLimits.alertCooldownMs) return;
          const primary = evaluation.flags[0];
          showToast(`Resource ${{primary.level.toUpperCase()}}: ${{primary.message}}`);
          lastAlertMs = nowMs;
        }}

        function sample() {{
          const nowPerf = performance.now();
          const expectedMs = adaptiveLimits.sampleMs;
          const lagMs = Math.max(0, Math.round(nowPerf - lastTick - expectedMs));
          lastTick = nowPerf;
          const queueDepth = RenderQueueManager.size();
          const longTasksPerMin = Math.round(longTasksInWindow * (60000 / expectedMs));
          longTasksInWindow = 0;
          let heapRatio = null;
          if (performance.memory && performance.memory.jsHeapSizeLimit > 0) {{
            heapRatio = performance.memory.usedJSHeapSize / performance.memory.jsHeapSizeLimit;
          }}
          const snapshot = {{ lagMs, longTasksPerMin, queueDepth, heapRatio }};
          const evaluation = evaluate(snapshot);
          updateUi(snapshot, evaluation);
          maybeAlert(evaluation);
          Logger.info('resource.sample', {{ snapshot, evaluation, adaptiveLimits }});
        }}

        function start() {{
          if (timerId) return;
          sample();
          timerId = window.setInterval(sample, adaptiveLimits.sampleMs);
        }}

        function stop() {{
          if (timerId) {{
            clearInterval(timerId);
            timerId = null;
          }}
        }}

        function teardown() {{
          stop();
          if (longTaskObserver) {{
            try {{
              longTaskObserver.disconnect();
            }} catch (_err) {{
              // ignore
            }}
          }}
        }}

        return {{ start, stop, teardown }};
      }})();

      function showToast(msg) {{
        if (!toast) return;
        toast.textContent = msg;
        toast.classList.add('show');
        if (toastTimer) clearTimeout(toastTimer);
        toastTimer = setTimeout(() => {{
          toast.classList.remove('show');
        }}, 1700);
      }}

      function withinWindow(runTs, windowKey) {{
        if (windowKey === 'all') return true;
        const ageSeconds = nowTs - runTs;
        if (windowKey === '24h') return ageSeconds <= 24 * 3600;
        if (windowKey === '7d') return ageSeconds <= 7 * 24 * 3600;
        if (windowKey === '30d') return ageSeconds <= 30 * 24 * 3600;
        return true;
      }}

      function freshnessRank(value) {{
        if (value === 'stale') return 0;
        if (value === 'aging') return 1;
        return 2;
      }}

      function applyFilters(resetLimit = false) {{
        const renderToken = ++activeRenderToken;
        RenderQueueManager.cancelAll();
        if (resetLimit) visibleLimit = PAGE_SIZE;
        const q = search.value.trim().toLowerCase();
        const quality = qualityFilter.value;
        const dateWindow = dateFilter.value;
        const artifact = artifactFilter.value;
        const mode = sortMode.value;

        const filtered = cards.filter((card) => {{
          const runId = card.dataset.runId || '';
          const title = card.dataset.title || '';
          const generated = card.dataset.generated || '';
          const qualityTier = card.dataset.qualityTier || '';
          const completeness = Number(card.dataset.completeness || 0);
          const runTs = Number(card.dataset.runTs || 0);
          const haystack = card.dataset.searchText || [runId, title, generated, card.textContent || ''].join(' ').toLowerCase();
          if (q && !haystack.includes(q)) return false;
          if (quality !== 'all' && qualityTier !== quality) return false;
          if (!withinWindow(runTs, dateWindow)) return false;
          if (artifact === 'complete' && completeness < 100) return false;
          if (artifact === 'incomplete' && completeness === 100) return false;
          return true;
        }});

        filtered.sort((a, b) => {{
          const runTsA = Number(a.dataset.runTs || 0);
          const runTsB = Number(b.dataset.runTs || 0);
          const scoreA = Number(a.dataset.qualityScore || 0);
          const scoreB = Number(b.dataset.qualityScore || 0);
          const freshnessA = freshnessRank(a.dataset.freshness || '');
          const freshnessB = freshnessRank(b.dataset.freshness || '');
          if (mode === 'quality') return scoreB - scoreA || runTsB - runTsA;
          if (mode === 'stale') return freshnessA - freshnessB || runTsB - runTsA;
          return runTsB - runTsA;
        }});

        const totalFiltered = filtered.length;
        const toRender = filtered.slice(0, visibleLimit);
        archive.innerHTML = '';
        emptyState.style.display = 'none';
        if (!toRender.length) {{
          resultMeta.textContent = `Showing 0 of ${{cards.length}} runs`;
          emptyState.style.display = 'block';
          if (loadMoreBtn) loadMoreBtn.style.display = 'none';
          if (showAllBtn) showAllBtn.style.display = 'none';
          if (loadMeta) loadMeta.textContent = '';
          showToast('No runs match filters');
          return;
        }}

        let index = 0;
        resultMeta.textContent = `Rendering 0/${{toRender.length}} of ${{totalFiltered}} filtered (queue:${{CHUNK_SIZE}}, mode:${{lowPowerMode ? 'low-power' : 'normal'}})`;
        if (loadMeta) {{
          loadMeta.textContent = `Showing ${{toRender.length}} / ${{totalFiltered}} filtered`;
        }}
        const hasMore = totalFiltered > toRender.length;
        if (loadMoreBtn) loadMoreBtn.style.display = hasMore ? 'inline-block' : 'none';
        if (showAllBtn) showAllBtn.style.display = hasMore ? 'inline-block' : 'none';
        if (loadMoreBtn) {{
          loadMoreBtn.textContent = `Load more (+${{PAGE_SIZE}})`;
        }}

        function renderChunk() {{
          if (renderToken !== activeRenderToken) return;
          const frag = document.createDocumentFragment();
          const end = Math.min(toRender.length, index + CHUNK_SIZE);
          for (; index < end; index++) {{
            frag.appendChild(toRender[index]);
          }}
          archive.appendChild(frag);
          resultMeta.textContent = `Showing ${{index}} of ${{toRender.length}} rendered (${{totalFiltered}} filtered, ${{cards.length}} indexed)`;
          if (index < toRender.length) {{
            schedule(renderChunk);
          }} else {{
            showToast(`Filters applied: ${{totalFiltered}} result(s), rendered ${{toRender.length}}`);
          }}
        }}
        schedule(renderChunk);
      }}

      function collectUiContext() {{
        const components = Array.from(new Set(Array.from(document.querySelectorAll('[class]'))
          .flatMap((el) => (el.className || '').split(' '))
          .map((x) => x.trim())
          .filter((x) => x && !x.includes('show')))).slice(0, 40);
        const styleTokens = ['--bg', '--paper', '--ink', '--accent', '--dark', '--line'];
        return {{
          title: document.title,
          h1: (document.querySelector('h1') || {{ textContent: '' }}).textContent.trim(),
          generatedAt: "{generated_at}",
          components,
          styleTokens,
          cardCount: cards.length,
        }};
      }}

      function buildPrompt(routeExists) {{
        const ctx = collectUiContext();
        const endpoint = (endpointInput.value || '').trim() || '/missing/route';
        const desired = (desiredInput.value || '').trim() || 'Show a useful page with clear top summary and progressively deeper evidence';
        const wireframe = (wireframeInput.value || '').trim() || 'Top: golden nugget; Middle: evidence cards; Bottom: explorer and actions';
        const screenshot = screenshotInput && screenshotInput.files && screenshotInput.files[0] ? screenshotInput.files[0].name : '(none)';
        return [
          `You are continuing WAFT site development.`,
          ``,
          `Route request: ${{endpoint}}`,
          `Route exists now: ${{routeExists ? 'yes' : 'no (treat as 404-to-feature request)'}}`,
          `Desired outcome: ${{desired}}`,
          `Wireframe hint: ${{wireframe}}`,
          `Screenshot file: ${{screenshot}}`,
          ``,
          `Site context:`,
          `- Page title: ${{ctx.title}}`,
          `- Header: ${{ctx.h1}}`,
          `- Generated: ${{ctx.generatedAt}}`,
          `- Archive cards visible: ${{ctx.cardCount}}`,
          `- Known style tokens: ${{ctx.styleTokens.join(', ')}}`,
          `- Key component classes: ${{ctx.components.join(', ')}}`,
          ``,
          `Build requirements:`,
          `1) Add a concise abstract at the top explaining current system status.`,
          `2) Provide a reverse-cone exploration flow: summary -> evidence -> raw detail.`,
          `3) Add/upgrade endpoint UX so missing routes open a prompt-configurator instead of dead-end 404.`,
          `4) Keep styling consistent with this site tokens and card system.`,
          `5) Return implementation steps and updated code snippets.`,
        ].join('\\n');
      }}

      function checkRoute() {{
        const endpoint = (endpointInput.value || '').trim();
        if (!endpoint) {{
          routeStatus.textContent = 'Enter a route first.';
          showToast('Enter a route to check');
          return false;
        }}
        const exists = RouteManager.exists(endpoint);
        if (exists) {{
          routeStatus.textContent = `Route exists: ${{endpoint}}`;
          showToast('Route exists');
        }} else {{
          routeStatus.textContent = `Route missing (404 candidate): ${{endpoint}} - prompt configurator ready.`;
          showToast('404 candidate detected, prompt prefilled');
          promptOutput.value = buildPrompt(false);
        }}
        return exists;
      }}

      function requestApplyFilters() {{
        if (filterTimer) clearTimeout(filterTimer);
        filterTimer = setTimeout(() => applyFilters(true), DEBOUNCE_MS);
      }}

      [search, qualityFilter, dateFilter, artifactFilter, sortMode].forEach((el) => {{
        HandlerManager.bind(el, 'input', requestApplyFilters, 'filters.input');
        HandlerManager.bind(el, 'change', requestApplyFilters, 'filters.change');
      }});
      HandlerManager.bind(checkRouteBtn, 'click', checkRoute, 'route.check');
      HandlerManager.bind(generatePromptBtn, 'click', () => {{
        const exists = checkRoute();
        promptOutput.value = buildPrompt(exists);
        showToast('Prompt generated');
      }}, 'prompt.generate');
      HandlerManager.bind(copyPromptBtn, 'click', async () => {{
        try {{
          await navigator.clipboard.writeText(promptOutput.value || '');
          showToast('Prompt copied');
        }} catch (err) {{
          showToast('Copy failed - manual copy needed');
        }}
      }}, 'prompt.copy');
      HandlerManager.bind(loadMoreBtn, 'click', () => {{
        visibleLimit += PAGE_SIZE;
        applyFilters(false);
      }}, 'archive.loadMore');
      HandlerManager.bind(showAllBtn, 'click', () => {{
        visibleLimit = cards.length;
        applyFilters(false);
      }}, 'archive.showAll');
      document.addEventListener('visibilitychange', safeHandler(() => {{
        if (document.visibilityState === 'hidden') ResourceMonitorManager.stop();
        else ResourceMonitorManager.start();
      }}, 'resource.visibility'));
      window.addEventListener('beforeunload', safeHandler(() => ResourceMonitorManager.teardown(), 'resource.teardown'));
      showToast(`Sitrep ready: ${{cards.length}} run(s) indexed (${{lowPowerMode ? 'low-power' : 'normal'}} mode)`);
      Logger.info('init', {{ indexedRuns: cards.length, lowPowerMode, queue: CHUNK_SIZE }});
      ResourceMonitorManager.start();
      applyFilters(true);
    }})();
  </script>
</body>
</html>
"""


def _write_pdf(html: str, html_path: Path, pdf_path: Path) -> None:
    try:
        from weasyprint import HTML  # type: ignore

        HTML(string=html, base_url=str(html_path.parent)).write_pdf(str(pdf_path))
        LOGGER.info("PDF generated via WeasyPrint: %s", pdf_path)
        return
    except Exception as exc:
        LOGGER.warning("WeasyPrint PDF generation failed (%s); trying Chrome fallback.", exc)
    chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    if chrome.exists():
        result = subprocess.run(
            [
                str(chrome),
                "--headless",
                "--disable-gpu",
                f"--print-to-pdf={pdf_path}",
                html_path.as_uri(),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and pdf_path.exists():
            LOGGER.info("PDF generated via Chrome fallback: %s", pdf_path)
        else:
            LOGGER.warning("Chrome PDF fallback failed (exit=%s): %s", result.returncode, result.stderr.strip())


def _open_in_chrome(path: Path) -> None:
    if sys.platform == "darwin":
        result = subprocess.run(
            ["open", "-a", "Google Chrome", str(path)],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            LOGGER.info("Opened hub in Chrome: %s", path)
            return
        LOGGER.warning("Could not open in Chrome (exit=%s), using default browser.", result.returncode)
    webbrowser.open(path.as_uri())


def main() -> int:
    _configure_logging()
    started = time.perf_counter()
    args = parse_args()
    runtime = _runtime_trace()
    _print_runtime_trace(runtime)
    root = Path.cwd()
    work_efforts_dir = (root / args.work_efforts_dir).resolve()
    devlog_path = (root / args.devlog).resolve()
    output_dir = (root / args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if not work_efforts_dir.exists():
        print(f"[error] Missing work efforts directory: {work_efforts_dir}")
        return 1
    if not devlog_path.exists():
        print(f"[error] Missing devlog file: {devlog_path}")
        return 1

    now = datetime.now()
    generated_at = now.strftime("%Y-%m-%d %H:%M:%S %Z")
    stamp = now.strftime("%Y%m%d_%H%M%S")
    work_files = _recent_work_efforts(work_efforts_dir, args.work_effort_count)
    devlog_text = devlog_path.read_text(encoding="utf-8", errors="ignore")
    dev_sections = _recent_devlog_sections(devlog_text, args.devlog_sections)

    try:
        markdown_text = _render_markdown(generated_at, work_efforts_dir, work_files, dev_sections, runtime)
        md_path = output_dir / f"recent_work_report_{stamp}.md"
        html_path = output_dir / f"recent_work_report_{stamp}.html"
        pdf_path = output_dir / f"recent_work_report_{stamp}.pdf"
        md_path.write_text(markdown_text, encoding="utf-8")

        html_text = _render_html(markdown_text, generated_at)
        html_path.write_text(html_text, encoding="utf-8")
        _write_pdf(html_text, html_path, pdf_path)

        latest_md = output_dir / "recent_work_report_latest.md"
        latest_html = output_dir / "recent_work_report_latest.html"
        latest_pdf = output_dir / "recent_work_report_latest.pdf"
        latest_md.write_text(markdown_text, encoding="utf-8")
        latest_html.write_text(html_text, encoding="utf-8")
        if pdf_path.exists():
            latest_pdf.write_bytes(pdf_path.read_bytes())

        current_entry = {
            "run_id": stamp,
            "title": f"WAFT Recent Work Report {stamp}",
            "generated_at": generated_at,
            "md_path": md_path.name,
            "html_path": html_path.name,
            "pdf_path": pdf_path.name if pdf_path.exists() else "",
            "run_duration_ms": int((time.perf_counter() - started) * 1000),
        }
        index_path = output_dir / "report_index.json"
        index_payload = _load_index(index_path)
        indexed_rows = index_payload["reports"]
        discovered_rows = _discover_report_runs(output_dir)
        merged_rows = _merge_reports(indexed_rows, discovered_rows, current_entry, output_dir, now)
        latest_run_id = merged_rows[0]["run_id"] if merged_rows else index_payload.get("latest_run_id", "")
        _write_index(index_path, merged_rows, latest_run_id)
        reconciliation = _reconcile_rows(merged_rows, discovered_rows)
        current_row = next((row for row in merged_rows if row.get("run_id") == stamp), merged_rows[0] if merged_rows else current_entry)

        hub_html = _render_hub_html(
            generated_at,
            current_row,
            merged_rows,
            reconciliation,
            latest_run_id,
            now,
            args.hub_max_runs,
        )
        hub_path = output_dir / f"report_hub_{stamp}.html"
        latest_hub = output_dir / "report_hub_latest.html"
        hub_path.write_text(hub_html, encoding="utf-8")
        latest_hub.write_text(hub_html, encoding="utf-8")

        print("=== WAFT Recent Work Report ===")
        print(f"Markdown: {md_path}")
        print(f"HTML: {html_path}")
        print(f"PDF: {pdf_path}")
        print(f"Hub: {hub_path}")

        if not args.no_open:
            _open_in_chrome(latest_hub)
        return 0
    except Exception as exc:
        LOGGER.exception("Sitrep generation failed: %s", exc)
        print(f"[error] Sitrep generation failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
