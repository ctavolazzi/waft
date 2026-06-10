#!/usr/bin/env python3
"""
Append markdown to today's Obsidian daily note. Start only while using cockpit (not a 24/7 daemon).

  python3 src/waft/scripts/obsidian_daily_bridge.py

Stdlib only — no FastAPI/uvicorn required.

Env:
  OBSIDIAN_DAILY_DIR    — folder containing YYYY-MM-DD.md
                        (default: ~/Documents/Personal-Remote-Vault/Daily Notes)
  OBSIDIAN_BRIDGE_HOST  — default 127.0.0.1
  OBSIDIAN_BRIDGE_PORT  — default 5055
  OBSIDIAN_BRIDGE_TOKEN — if set, require header X-Bridge-Token

POST /append-daily  JSON {"markdown": "..."}  optional {"date": "YYYY-MM-DD"}
GET  /health
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date, datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_DAILY = (
    Path.home() / "Documents" / "Personal-Remote-Vault" / "Daily Notes"
)


def daily_path(d: date, root: Path) -> Path:
    return root / f"{d.isoformat()}.md"


def append_to_daily(markdown: str, day: date | None) -> tuple[Path, int]:
    root = Path(os.environ.get("OBSIDIAN_DAILY_DIR", str(DEFAULT_DAILY))).expanduser()
    if not root.is_dir():
        raise ValueError(f"OBSIDIAN_DAILY_DIR is not a directory: {root}")
    d = day or date.today()
    path = daily_path(d, root)
    path.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    block = f"\n\n<!-- waft-cockpit-bridge {stamp} -->\n{markdown.rstrip()}\n"
    with path.open("a", encoding="utf-8") as f:
        f.write(block)
    return path, len(block.encode("utf-8"))


def make_handler():
    token = os.environ.get("OBSIDIAN_BRIDGE_TOKEN")

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt: str, *args: object) -> None:
            print(f"[bridge] {self.address_string()} — {fmt % args}", file=sys.stderr)

        def _send(self, code: int, body: bytes, content_type: str = "application/json") -> None:
            self.send_response(code)
            self.send_header("Content-Type", f"{content_type}; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Bridge-Token")
            self.end_headers()
            self.wfile.write(body)

        def do_OPTIONS(self) -> None:  # noqa: N802
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Bridge-Token")
            self.end_headers()

        def do_GET(self) -> None:  # noqa: N802
            if urlparse(self.path).path != "/health":
                self._send(404, b'{"detail":"not found"}')
                return
            root = Path(os.environ.get("OBSIDIAN_DAILY_DIR", str(DEFAULT_DAILY))).expanduser()
            out = {
                "ok": True,
                "daily_dir": str(root.resolve()),
                "exists": root.is_dir(),
            }
            self._send(200, json.dumps(out).encode("utf-8"))

        def do_POST(self) -> None:  # noqa: N802
            if urlparse(self.path).path != "/append-daily":
                self._send(404, b'{"detail":"not found"}')
                return
            if token and self.headers.get("X-Bridge-Token") != token:
                self._send(401, b'{"detail":"bad or missing X-Bridge-Token"}')
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length else b"{}"
            try:
                data = json.loads(raw.decode("utf-8"))
            except json.JSONDecodeError as e:
                self._send(400, json.dumps({"detail": str(e)}).encode("utf-8"))
                return
            md = data.get("markdown")
            if not md or not isinstance(md, str):
                self._send(400, b'{"detail":"markdown required"}')
                return
            ds = data.get("date")
            day: date | None = None
            if ds:
                try:
                    day = date.fromisoformat(str(ds))
                except ValueError as e:
                    self._send(400, json.dumps({"detail": f"bad date: {e}"}).encode("utf-8"))
                    return
            try:
                path, nbytes = append_to_daily(md, day)
            except ValueError as e:
                self._send(400, json.dumps({"detail": str(e)}).encode("utf-8"))
                return
            out = {"ok": True, "path": str(path.resolve()), "bytes_appended": nbytes}
            self._send(200, json.dumps(out).encode("utf-8"))

    return Handler


def main() -> None:
    host = os.environ.get("OBSIDIAN_BRIDGE_HOST", "127.0.0.1")
    port = int(os.environ.get("OBSIDIAN_BRIDGE_PORT", "5055"))
    server = HTTPServer((host, port), make_handler())
    print(f"Obsidian daily bridge http://{host}:{port}/health", file=sys.stderr)
    print(
        f"Daily dir: {Path(os.environ.get('OBSIDIAN_DAILY_DIR', str(DEFAULT_DAILY))).expanduser()}",
        file=sys.stderr,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping.", file=sys.stderr)


if __name__ == "__main__":
    main()
