"""
Localhost:5050 dashboard orchestration endpoints.
"""

from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel

from ...api.dependencies import get_project_path, require_auth
from ...core.visualizer import Visualizer

router = APIRouter()


class ReportRequest(BaseModel):
    title: str = "Localhost 5050 Session Report"
    notes: str = ""
    report_type: str = "session_recap"
    include_plan: bool = True
    include_timeline: bool = True


class ContinueCommandRequest(BaseModel):
    objective: str = "Continue dashboard-driven implementation"
    template: str = "analysis"


def _to_iso(ts: float) -> str:
    return datetime.fromtimestamp(ts).isoformat()


def _recent_artifacts(project_path: Path, limit: int = 30) -> list[dict]:
    patterns = [
        "_work_efforts/MINDSPACE_REVIEW_*.md",
        "_work_efforts/MEME_BORG_SESSION_REPORT_*.md",
        "_work_efforts/WE-*/WE-*_index.md",
        "_work_efforts/[0-9][0-9]-*/[0-9][0-9]_*/[0-9][0-9].[0-9][0-9]_*.md",
        "_work_efforts/reports/report_5050_*.md",
        "_work_efforts/reports/report_5050_*.pdf",
        "_pyrite/analyze/analyze-*.md",
        "_pyrite/phase1/phase1-*.json",
        "_pyrite/phase1/phase1-*.html",
    ]

    files: list[Path] = []
    for pattern in patterns:
        files.extend(project_path.glob(pattern))

    unique_files = list({str(f.resolve()): f for f in files}.values())
    unique_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    items = []
    for file_path in unique_files[:limit]:
        rel = file_path.relative_to(project_path).as_posix()
        event_type = "artifact"
        if "/analyze/" in rel:
            event_type = "analyze"
        elif "MINDSPACE_REVIEW" in rel:
            event_type = "mindspace"
        elif "/phase1/" in rel:
            event_type = "phase1"
        elif rel.startswith("_work_efforts/WE-") or rel.startswith("_work_efforts/10-"):
            event_type = "work_effort"
        elif "MEME_BORG_SESSION_REPORT" in rel:
            event_type = "session_report"

        items.append(
            {
                "type": event_type,
                "path": rel,
                "name": file_path.name,
                "timestamp": _to_iso(file_path.stat().st_mtime),
                "size_bytes": file_path.stat().st_size,
            }
        )
    return items


def _latest_work_effort_5050(project_path: Path) -> str | None:
    candidates = list(project_path.glob("_work_efforts/WE-*5050*/WE-*_index.md"))
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0].relative_to(project_path).as_posix()


def _canonical_ui_work_effort(project_path: Path) -> str | None:
    candidate = (
        project_path
        / "_work_efforts"
        / "10-19_user_interface"
        / "10_unified_waft_interface"
        / "10.01_waft_control_center_unification.md"
    )
    if candidate.exists():
        return candidate.relative_to(project_path).as_posix()
    return None


def _read_text_or_empty(file_path: Path) -> str:
    try:
        return file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def _build_report_markdown(
    title: str,
    report_type: str,
    notes: str,
    state: dict,
    timeline: list[dict],
    plan_text: str,
) -> str:
    git = state.get("git", {})
    gam = state.get("gamification", {})
    pyrite = state.get("pyrite", {})
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        f"# {title}",
        "",
        f"**Generated**: {now}",
        f"**Report Type**: {report_type}",
        f"**Project**: {state.get('project', {}).get('name', 'waft')}",
        "",
        "## Dashboard Snapshot",
        "",
        f"- Branch: `{git.get('branch', 'unknown')}`",
        f"- Uncommitted files: `{len(git.get('uncommitted_files', []))}`",
        f"- Integrity: `{gam.get('integrity', 0):.1f}%`",
        f"- Level: `{gam.get('level', 0)}`",
        f"- _pyrite valid: `{pyrite.get('valid', False)}`",
        "",
    ]

    if notes.strip():
        lines.extend(["## Notes", "", notes.strip(), ""])

    if report_type == "implementation_readiness":
        lines.extend(
            [
                "## Implementation Readiness",
                "",
                f"- _pyrite structure valid: `{pyrite.get('valid', False)}`",
                f"- Integrity threshold met (>= 70): `{gam.get('integrity', 0) >= 70}`",
                f"- Uncommitted files under 50: `{len(git.get('uncommitted_files', [])) < 50}`",
                "",
            ]
        )
    elif report_type == "decision_trace":
        lines.extend(
            [
                "## Decision Trace",
                "",
                (
                    "- Source commands should include: `waft check-assumptions`, "
                    "`waft analyze`, `waft proceed`, `waft decide`"
                ),
                "- Use timeline below as decision evidence chain",
                "",
            ]
        )

    lines.extend(["## Recommended Next Steps", ""])
    lines.extend(
        [
            "1. Launch or refresh `http://localhost:5050`",
            "2. Review timeline and context stack",
            "3. Generate report + PDF and print if needed",
            "4. Use `Continue in Cursor` command copy flow",
            "5. Paste copied command into Cursor to continue loop",
            "",
        ]
    )

    lines.extend(["## Timeline (Most Recent)", ""])
    for event in timeline[:20]:
        lines.append(
            f"- `{event.get('timestamp', '')}` "
            f"[{event.get('type', 'artifact')}] `{event.get('path', '')}`"
        )
    lines.append("")

    if plan_text.strip():
        lines.extend(["## Plan Reference", "", plan_text.strip(), ""])

    return "\n".join(lines)


def _render_pdf_from_markdown(markdown: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(str(output_path), pagesize=letter)
        width, height = letter
        x = 48
        y = height - 48
        line_height = 13

        for raw_line in markdown.splitlines():
            line = raw_line if raw_line else " "
            if y < 48:
                c.showPage()
                y = height - 48
            c.setFont("Helvetica", 10)
            c.drawString(x, y, line[:140])
            y -= line_height
        c.save()
        return
    except ModuleNotFoundError:
        pass

    # Fallback: use system python3 runtime (where reportlab may be available)
    import subprocess
    import tempfile

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as tmp:
        tmp.write(markdown)
        tmp_markdown = tmp.name

    script = (
        "from reportlab.lib.pagesizes import letter\n"
        "from reportlab.pdfgen import canvas\n"
        "from pathlib import Path\n"
        "import sys\n"
        "md_path = Path(sys.argv[1])\n"
        "out_path = Path(sys.argv[2])\n"
        "text = md_path.read_text(encoding='utf-8')\n"
        "c = canvas.Canvas(str(out_path), pagesize=letter)\n"
        "width, height = letter\n"
        "x, y = 48, height - 48\n"
        "line_height = 13\n"
        "for raw_line in text.splitlines():\n"
        "    line = raw_line if raw_line else ' '\n"
        "    if y < 48:\n"
        "        c.showPage()\n"
        "        y = height - 48\n"
        "    c.setFont('Helvetica', 10)\n"
        "    c.drawString(x, y, line[:140])\n"
        "    y -= line_height\n"
        "c.save()\n"
    )
    try:
        subprocess.run(
            ["python3", "-c", script, tmp_markdown, str(output_path)],
            check=True,
            capture_output=True,
            text=True,
        )
    finally:
        try:
            Path(tmp_markdown).unlink(missing_ok=True)
        except OSError:
            pass


@router.get("/5050/session")
async def get_5050_session(request: Request):
    project_path: Path = get_project_path(request)
    visualizer = Visualizer(project_path)
    state = visualizer.gather_state()
    artifacts = _recent_artifacts(project_path, limit=30)
    latest_we = _latest_work_effort_5050(project_path)
    canonical_ui_work_effort = _canonical_ui_work_effort(project_path)

    return {
        "timestamp": datetime.now().isoformat(),
        "state": state,
        "latest_work_effort_5050": latest_we,
        "canonical_ui_work_effort": canonical_ui_work_effort,
        "artifacts": artifacts,
        "summary": {
            "uncommitted_files": len(state.get("git", {}).get("uncommitted_files", [])),
            "integrity": state.get("gamification", {}).get("integrity", 0),
            "work_efforts": len(state.get("work_efforts", [])),
        },
    }


@router.get("/5050/timeline")
async def get_5050_timeline(request: Request):
    project_path: Path = get_project_path(request)
    events = _recent_artifacts(project_path, limit=100)
    return {"total": len(events), "events": events}


@router.post("/5050/report")
async def create_5050_report(
    request: Request,
    body: ReportRequest,
    token: str = Depends(require_auth),
):
    del token
    project_path: Path = get_project_path(request)
    visualizer = Visualizer(project_path)
    state = visualizer.gather_state()
    timeline = _recent_artifacts(project_path, limit=40) if body.include_timeline else []
    plan_text = ""
    if body.include_plan:
        for candidate in [
            project_path
            / "_work_efforts"
            / "WE-260301-5050_localhost_5050_dashboard"
            / "WE-260301-5050_index.md",
            project_path
            / "_work_efforts"
            / "10-19_user_interface"
            / "10_unified_waft_interface"
            / "10.01_waft_control_center_unification.md",
        ]:
            plan_text = _read_text_or_empty(candidate)
            if plan_text:
                break

    markdown = _build_report_markdown(
        body.title, body.report_type, body.notes, state, timeline, plan_text
    )
    output_dir = project_path / "_work_efforts" / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_path = output_dir / f"report_5050_{timestamp}.md"
    md_path.write_text(markdown, encoding="utf-8")

    return {
        "ok": True,
        "report_path": md_path.relative_to(project_path).as_posix(),
        "report_markdown": markdown,
    }


@router.post("/5050/report/pdf")
async def create_5050_report_pdf(
    request: Request,
    body: ReportRequest,
    token: str = Depends(require_auth),
):
    del token
    project_path: Path = get_project_path(request)
    visualizer = Visualizer(project_path)
    state = visualizer.gather_state()
    timeline = _recent_artifacts(project_path, limit=40) if body.include_timeline else []
    plan_text = ""
    if body.include_plan:
        for candidate in [
            project_path
            / "_work_efforts"
            / "WE-260301-5050_localhost_5050_dashboard"
            / "WE-260301-5050_index.md",
            project_path
            / "_work_efforts"
            / "10-19_user_interface"
            / "10_unified_waft_interface"
            / "10.01_waft_control_center_unification.md",
        ]:
            plan_text = _read_text_or_empty(candidate)
            if plan_text:
                break
    markdown = _build_report_markdown(
        body.title, body.report_type, body.notes, state, timeline, plan_text
    )

    output_dir = project_path / "_work_efforts" / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_path = output_dir / f"report_5050_{timestamp}.md"
    pdf_path = output_dir / f"report_5050_{timestamp}.pdf"

    md_path.write_text(markdown, encoding="utf-8")
    _render_pdf_from_markdown(markdown, pdf_path)

    return {
        "ok": True,
        "report_path": md_path.relative_to(project_path).as_posix(),
        "pdf_path": pdf_path.relative_to(project_path).as_posix(),
    }


@router.post("/5050/continue-command")
async def create_continue_command(request: Request, body: ContinueCommandRequest):
    project_path: Path = get_project_path(request)
    events = _recent_artifacts(project_path, limit=5)
    context_lines = [f"{e['type']}::{e['path']}" for e in events]
    context_snippet = " | ".join(context_lines)

    template = body.template.strip().lower()
    if template == "analysis":
        command = (
            "waft check-assumptions --verbose && waft analyze --verbose && waft proceed --strict"
        )
    elif template == "decision":
        command = "waft decide --topic workflow"
    elif template == "report":
        command = "waft recap-and-review"
    else:
        command = "waft proceed --strict"

    command_with_context = (
        f"{command}\n\n# objective: {body.objective}\n# context: {context_snippet}"
    )
    return {
        "ok": True,
        "template": template,
        "command": command_with_context,
        "copy_hint": "Copy this payload, paste in Cursor chat, and run.",
    }


@router.get("/5050/file")
async def download_5050_file(
    request: Request,
    path: str = Query(..., description="Relative path under _work_efforts/reports"),
):
    project_path: Path = get_project_path(request)
    reports_dir = (project_path / "_work_efforts" / "reports").resolve()
    target = (project_path / path).resolve()

    if not str(target).startswith(str(reports_dir)):
        raise HTTPException(status_code=400, detail="Invalid path")
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(str(target), filename=target.name)
