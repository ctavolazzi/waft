#!/usr/bin/env python3
"""
Housekeeping Storage Helper
===========================

Scans for old augmented content, builds a manifest, and optionally moves/copies
files into the EasyStore realm.
"""

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.waft.pantheon import ExternalDriveRealm
from src.waft.utils import (
    StorageRegistry,
    classify_content_type,
    detect_external_drive,
    get_external_drive_base,
)

app = typer.Typer(add_completion=False)
console = Console()

EXCLUDE_PREFIXES = [
    ".git/",
    ".cursor/",
    ".empirica/",
    ".venv/",
    ".pytest_cache/",
    ".ruff_cache/",
    "__pycache__/",
    "node_modules/",
    "_pantheon/",
    "_pyrite/",
]

EXCLUDE_FILES = {
    ".env",
    ".waft_api_token",
    "waft_memory.db",
}


@app.command()
def hoover(
    older_days: int = typer.Option(30, "--older-days", "-o", help="Only include files older than N days"),
    realm_name: str = typer.Option("EasyStore_Realm", "--realm", "-r", help="Realm name"),
    apply: bool = typer.Option(False, "--apply", help="Apply move/copy (default: dry-run)"),
    copy: bool = typer.Option(False, "--copy", help="Copy instead of move"),
    include_work_efforts: bool = typer.Option(
        False, "--include-work-efforts", help="Include _work_efforts content"
    ),
    max_files: int | None = typer.Option(None, "--max-files", help="Limit number of files"),
):
    """Hoover old augmented content into EasyStore realm."""
    project_path = project_root
    now_ts = datetime.now().timestamp()

    console.print(Panel("Housekeeping Storage Helper", border_style="cyan"))

    drive_path = detect_external_drive("Easystore")
    if not drive_path:
        console.print("Error: EasyStore drive not detected.")
        raise typer.Exit(1)

    realm = ExternalDriveRealm(project_path)
    registered_realms = {entry.get("realm_name") for entry in realm.list_realms()}
    if realm_name not in registered_realms:
        result = realm.register_realm(
            realm_name=realm_name, drive_name="Easystore", project_name=project_path.name
        )
        if not result.get("success"):
            console.print(f"Error: Failed to register realm: {result.get('error')}")
            raise typer.Exit(1)
        console.print(f"Registered realm: {realm_name}")

    external_base = get_external_drive_base(project_path.name)
    if not external_base:
        console.print("Error: Could not resolve external drive base path.")
        raise typer.Exit(1)

    realm_base = external_base / "Realms" / realm_name

    exclude_prefixes = list(EXCLUDE_PREFIXES)
    if not include_work_efforts:
        exclude_prefixes.append("_work_efforts/")

    registry = StorageRegistry(project_path)

    scanned = 0
    candidates = []
    for path in project_path.rglob("*"):
        if not path.is_file():
            continue
        scanned += 1
        if path.is_symlink():
            continue

        rel = path.relative_to(project_path)
        if ".." in rel.parts:
            continue

        rel_str = rel.as_posix()
        if rel.name in EXCLUDE_FILES:
            continue
        if any(rel_str.startswith(prefix) for prefix in exclude_prefixes):
            continue

        if classify_content_type(rel) != "augmented":
            continue

        try:
            stat = path.stat()
        except OSError:
            continue

        age_days = (now_ts - stat.st_mtime) / 86400
        if older_days > 0 and age_days < older_days:
            continue

        size_kb = stat.st_size / 1024
        candidates.append(
            {
                "path": path,
                "relative": rel,
                "age_days": age_days,
                "size_kb": size_kb,
            }
        )

    candidates.sort(key=lambda item: item["age_days"], reverse=True)
    if max_files:
        candidates = candidates[:max_files]

    manifest_dir = project_path / "_work_efforts" / "housekeeping_manifests"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    manifest_path = manifest_dir / f"housekeeping_storage_manifest_{timestamp}.json"

    actions = []
    moved = 0
    skipped = 0
    errors = 0

    for item in candidates:
        src = item["path"]
        rel = item["relative"]
        rel_str = str(rel)
        dest = realm_base / rel
        dest_str = str(dest)

        action = {
            "source": str(src),
            "relative_path": rel_str,
            "destination": dest_str,
            "age_days": round(item["age_days"], 2),
            "size_kb": round(item["size_kb"], 2),
            "status": "planned" if not apply else "pending",
            "operation": "copy" if copy else "move",
        }

        existing_entry = registry.find_content(rel_str)
        if existing_entry and str(existing_entry.get("storage_location", "")).startswith(
            str(drive_path)
        ):
            action["status"] = "skipped_already_external"
            skipped += 1
            actions.append(action)
            continue

        if dest.exists():
            action["status"] = "skipped_exists"
            skipped += 1
            actions.append(action)
            continue

        if not apply:
            actions.append(action)
            continue

        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            if copy:
                shutil.copy2(src, dest)
                action["operation"] = "copied"
            else:
                shutil.move(src, dest)
                action["operation"] = "moved"

            registry.register(rel_str, dest_str, "augmented")
            realm.route_content_to_realm(
                content_path=rel, realm_name=realm_name, project_name=project_path.name
            )

            action["status"] = "done"
            moved += 1
        except Exception as exc:
            action["status"] = "error"
            action["error"] = str(exc)
            errors += 1

        actions.append(action)

    manifest = {
        "created_at": datetime.now().isoformat(),
        "project_path": str(project_path),
        "realm_name": realm_name,
        "drive_path": str(drive_path),
        "older_days": older_days,
        "apply": apply,
        "copy": copy,
        "include_work_efforts": include_work_efforts,
        "max_files": max_files,
        "scanned_files": scanned,
        "candidate_count": len(candidates),
        "results": {"moved": moved, "skipped": skipped, "errors": errors},
        "actions": actions,
    }

    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    console.print("")
    console.print(f"Scanned files: {scanned}")
    console.print(f"Candidates: {len(candidates)}")
    console.print(f"Moved: {moved}  Skipped: {skipped}  Errors: {errors}")
    console.print(f"Manifest: {manifest_path}")

    if actions:
        table = Table(show_header=True, header_style="bold")
        table.add_column("Age(d)", justify="right")
        table.add_column("Size(KB)", justify="right")
        table.add_column("Status")
        table.add_column("Path")

        for action in actions[:10]:
            table.add_row(
                f"{action['age_days']}",
                f"{action['size_kb']}",
                action["status"],
                action["relative_path"],
            )

        console.print("")
        console.print(table)

    if not apply:
        console.print("\nDry-run complete. Re-run with --apply to move/copy files.")


if __name__ == "__main__":
    app()
