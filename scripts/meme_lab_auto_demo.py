#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx


SEEDS = [
    ("drake", "https://picsum.photos/seed/waft-demo-drake/1280/720"),
    ("gru_plan", "https://picsum.photos/seed/waft-demo-gru/1280/720"),
    ("change_my_mind", "https://picsum.photos/seed/waft-demo-change/1280/720"),
]


def ensure_demo_history(project_path: Path) -> Path:
    artifacts_dir = project_path / "_work_efforts" / "reports" / "meme_web_artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    history_path = artifacts_dir / "meme_history.jsonl"

    entries: list[dict] = []
    for template, url in SEEDS:
        out_path = artifacts_dir / f"demo_{template}.jpg"
        if not out_path.exists():
            response = httpx.get(url, timeout=20.0, follow_redirects=True)
            response.raise_for_status()
            out_path.write_bytes(response.content)
        rel_path = str(out_path.relative_to(project_path.resolve()))
        entries.append(
            {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "template": template,
                "seed": abs(hash(template)) % 1_000_000,
                "output_path": str(out_path),
                "relative_path": rel_path,
            }
        )

    # prepend entries so they show first in reverse-read history view
    existing_lines = history_path.read_text(encoding="utf-8").splitlines() if history_path.exists() else []
    new_lines = [json.dumps(entry, ensure_ascii=True) for entry in entries]
    history_path.write_text("\n".join(new_lines + existing_lines) + "\n", encoding="utf-8")
    return history_path


def open_chrome(url: str) -> None:
    if sys.platform == "darwin":
        subprocess.run(["open", "-a", "Google Chrome", url], check=False)
    else:
        import webbrowser

        webbrowser.open(url)


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed Meme Lab demo artifacts and open theater in Chrome.")
    parser.add_argument("--project-path", default=".", help="WAFT project path (default: current directory)")
    parser.add_argument("--host", default="127.0.0.1", help="Meme Lab API host")
    parser.add_argument("--port", default=8012, type=int, help="Meme Lab API port")
    parser.add_argument("--no-open", action="store_true", help="Do not open Chrome automatically")
    args = parser.parse_args()

    project_path = Path(args.project_path).expanduser().resolve()
    history_path = ensure_demo_history(project_path)
    target_url = f"http://{args.host}:{args.port}/api/meme-lab"

    print("=== Meme Lab Auto Demo Seeded ===")
    print(f"History file: {history_path}")
    print(f"Theater URL: {target_url}")
    print("Tip: run the API with --reload for live backend edits:")
    print("  PYENV_VERSION=3.14.3 python -m uvicorn src.waft.api.main:app --host 127.0.0.1 --port 8012 --reload")

    if not args.no_open:
        open_chrome(target_url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
