"""
Datastore — Shared utilities for loading, querying, and storing WAFT data.

Eliminates duplication across dungeon, awakening, personnel, and message
systems. All JSON-based storage goes through here.
"""

import json
from datetime import datetime
from pathlib import Path

# --- Constants ---

DUNGEON_RUNS_DIR = Path("_pyrite") / "dungeon" / "runs"
AWAKENING_RUNS_DIR = Path("_pyrite") / "awakening" / "runs"
MESSAGES_DIR = Path("_pyrite") / "messages"


# --- Generic JSON loading ---


def load_all_json(directory: Path, prefix: str = "") -> list[dict]:
    """Load all JSON files from a directory, optionally filtered by prefix."""
    if not directory.exists():
        return []
    pattern = f"{prefix}*.json" if prefix else "*.json"
    results = []
    for f in sorted(directory.glob(pattern), reverse=True):
        try:
            results.append(json.loads(f.read_text()))
        except (json.JSONDecodeError, KeyError):
            continue
    return results


def load_all_dungeon_runs(project_path: Path) -> list[dict]:
    """Load all dungeon run data."""
    return load_all_json(project_path / DUNGEON_RUNS_DIR, prefix="DNG-")


def load_all_awakening_runs(project_path: Path) -> list[dict]:
    """Load all awakening run data."""
    return load_all_json(project_path / AWAKENING_RUNS_DIR, prefix="AWK-")


# --- Message Store ---


class MessageStore:
    """
    Generic tagged message storage.

    Used by inter-agent messages, archaeology insights, and any
    system that needs to persist and query text with metadata.

    Storage: one JSON file per message in the configured directory.
    """

    def __init__(self, project_path: Path, subdirectory: str = "messages"):
        self.directory = project_path / "_pyrite" / subdirectory
        self.directory.mkdir(parents=True, exist_ok=True)

    def post(
        self,
        author: str,
        text: str,
        tags: list[str] | None = None,
        context: dict | None = None,
    ) -> dict:
        """Post a new message. Returns the message dict."""
        now = datetime.utcnow()
        msg_id = f"MSG-{now.strftime('%Y%m%d-%H%M%S')}-{id(text) & 0xFFFF:04x}"
        msg = {
            "id": msg_id,
            "author": author,
            "text": text,
            "tags": tags or [],
            "context": context or {},
            "timestamp": now.isoformat(),
        }
        out = self.directory / f"{msg_id}.json"
        out.write_text(json.dumps(msg, indent=2))
        return msg

    def query(
        self,
        tag: str | None = None,
        author: str | None = None,
        limit: int = 50,
    ) -> list[dict]:
        """Query messages, optionally filtered by tag or author."""
        messages = load_all_json(self.directory, prefix="MSG-")
        if tag:
            messages = [m for m in messages if tag in m.get("tags", [])]
        if author:
            messages = [m for m in messages if m.get("author") == author]
        return messages[:limit]

    def query_by_seed(self, seed: int) -> list[dict]:
        """Find all messages tagged with a specific dungeon seed."""
        return self.query(tag=f"seed:{seed}")

    def count(self) -> int:
        """Count total messages."""
        return len(list(self.directory.glob("MSG-*.json")))
