"""
Teleport Massive Storage Layer

Content-addressed storage with O(1) lookup, efficient compression,
and full history traversal. Inspired by git's object model.
"""

from __future__ import annotations
import hashlib
import json
import zlib
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, List, Any, Iterator, TypeVar, Generic
from datetime import datetime

from .models import StoryState, TMEntity


T = TypeVar('T', bound=TMEntity)


# =============================================================================
# CONTENT HASH
# =============================================================================

@dataclass
class ContentHash:
    """Content-addressed identifier for any object."""

    hash: str
    content_type: str  # e.g., "story_state", "character", "scene"

    @classmethod
    def compute(cls, content: Any, content_type: str) -> "ContentHash":
        """Compute hash from content."""
        if isinstance(content, str):
            data = content
        elif isinstance(content, dict):
            data = json.dumps(content, sort_keys=True)
        elif hasattr(content, 'to_json'):
            data = content.to_json()
        else:
            data = json.dumps(content, sort_keys=True, default=str)

        hash_val = hashlib.sha256(data.encode()).hexdigest()[:16]
        return cls(hash=hash_val, content_type=content_type)

    def __str__(self) -> str:
        return f"{self.content_type}:{self.hash}"


# =============================================================================
# OBJECT STORE (Low-level content-addressed storage)
# =============================================================================

class ObjectStore:
    """
    Low-level content-addressed object store.

    Objects are stored by their content hash. Duplicate content
    is automatically deduplicated. Supports compression.
    """

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS objects (
                    hash TEXT PRIMARY KEY,
                    content_type TEXT NOT NULL,
                    data BLOB NOT NULL,
                    compressed INTEGER DEFAULT 1,
                    created_at TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_content_type
                ON objects(content_type)
            """)
            conn.commit()

    def put(self, content: Any, content_type: str, compress: bool = True) -> ContentHash:
        """
        Store content and return its hash.

        If content already exists (same hash), returns existing hash
        without storing duplicate.
        """
        # Serialize
        if isinstance(content, str):
            data = content.encode()
        elif isinstance(content, bytes):
            data = content
        elif isinstance(content, dict):
            data = json.dumps(content, sort_keys=True).encode()
        elif hasattr(content, 'to_json'):
            data = content.to_json().encode()
        else:
            data = json.dumps(content, sort_keys=True, default=str).encode()

        # Compute hash from uncompressed data
        hash_val = hashlib.sha256(data).hexdigest()[:16]
        content_hash = ContentHash(hash=hash_val, content_type=content_type)

        # Compress if requested
        store_data = zlib.compress(data, level=6) if compress else data

        # Store (ignore if exists - content-addressed means same hash = same content)
        with sqlite3.connect(self.db_path) as conn:
            try:
                conn.execute(
                    "INSERT INTO objects (hash, content_type, data, compressed, created_at) VALUES (?, ?, ?, ?, ?)",
                    (hash_val, content_type, store_data, int(compress), datetime.utcnow().isoformat())
                )
                conn.commit()
            except sqlite3.IntegrityError:
                pass  # Already exists, which is fine

        return content_hash

    def get(self, hash_val: str) -> Optional[bytes]:
        """Retrieve content by hash. Returns None if not found."""
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT data, compressed FROM objects WHERE hash = ?",
                (hash_val,)
            ).fetchone()

            if row is None:
                return None

            data, compressed = row
            return zlib.decompress(data) if compressed else data

    def get_json(self, hash_val: str) -> Optional[Dict]:
        """Retrieve and parse JSON content."""
        data = self.get(hash_val)
        if data is None:
            return None
        return json.loads(data.decode())

    def exists(self, hash_val: str) -> bool:
        """Check if content exists."""
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT 1 FROM objects WHERE hash = ?",
                (hash_val,)
            ).fetchone()
            return row is not None

    def list_by_type(self, content_type: str) -> List[str]:
        """List all hashes of a given content type."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT hash FROM objects WHERE content_type = ? ORDER BY created_at",
                (content_type,)
            ).fetchall()
            return [row[0] for row in rows]

    def stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        with sqlite3.connect(self.db_path) as conn:
            total = conn.execute("SELECT COUNT(*) FROM objects").fetchone()[0]
            by_type = dict(conn.execute(
                "SELECT content_type, COUNT(*) FROM objects GROUP BY content_type"
            ).fetchall())
            size = conn.execute(
                "SELECT SUM(LENGTH(data)) FROM objects"
            ).fetchone()[0] or 0

        return {
            "total_objects": total,
            "by_type": by_type,
            "storage_bytes": size,
            "storage_mb": round(size / (1024 * 1024), 2)
        }


# =============================================================================
# STORY STORE (High-level story state management)
# =============================================================================

class StoryStore:
    """
    High-level story state management with history traversal.

    Provides:
    - Immutable state snapshots
    - Full history (git-like parent chain)
    - Branch/merge for Scinted realities
    - O(1) state lookup by hash
    - Efficient queries across all history
    """

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.objects = ObjectStore(base_path / "objects.db")
        self._init_refs()

    def _init_refs(self):
        """Initialize reference storage (like git refs)."""
        refs_path = self.base_path / "refs.json"
        if not refs_path.exists():
            self._save_refs({
                "HEAD": None,
                "timelines": {"prime": None},
                "tags": {}
            })

    def _load_refs(self) -> Dict:
        """Load refs."""
        refs_path = self.base_path / "refs.json"
        if refs_path.exists():
            return json.loads(refs_path.read_text())
        return {"HEAD": None, "timelines": {"prime": None}, "tags": {}}

    def _save_refs(self, refs: Dict):
        """Save refs."""
        refs_path = self.base_path / "refs.json"
        refs_path.parent.mkdir(parents=True, exist_ok=True)
        refs_path.write_text(json.dumps(refs, indent=2))

    # -------------------------------------------------------------------------
    # State Management
    # -------------------------------------------------------------------------

    def save_state(self, state: StoryState, timeline: str = "prime") -> str:
        """
        Save a story state and return its hash.

        Automatically sets parent to current HEAD of timeline.
        """
        # Get current head as parent
        refs = self._load_refs()
        parent = refs["timelines"].get(timeline)
        state.parent_hash = parent or ""

        # Finalize (compute hash)
        state.finalize()

        # Store
        self.objects.put(state.to_dict(), "story_state")

        # Update refs
        refs["timelines"][timeline] = state.state_hash
        refs["HEAD"] = state.state_hash
        self._save_refs(refs)

        return state.state_hash

    def get_state(self, hash_val: str) -> Optional[StoryState]:
        """Retrieve a story state by hash."""
        data = self.objects.get_json(hash_val)
        if data is None:
            return None

        # Reconstruct StoryState
        state = StoryState(
            state_hash=data.get('state_hash', ''),
            parent_hash=data.get('parent_hash', ''),
            timeline_id=data.get('timeline_id', 'prime'),
            current_chapter=data.get('current_chapter', 0),
            current_scene=data.get('current_scene', 0),
            characters=data.get('characters', {}),
            factions=data.get('factions', {}),
            locations=data.get('locations', {}),
            artifacts=data.get('artifacts', {}),
            knowledge_states=data.get('knowledge_states', {}),
            open_threads=data.get('open_threads', []),
            resolved_threads=data.get('resolved_threads', []),
            active_timelines=data.get('active_timelines', []),
            scint_points=data.get('scint_points', []),
            last_event=data.get('last_event', ''),
            pov_character=data.get('pov_character', ''),
        )
        return state

    def get_head(self, timeline: str = "prime") -> Optional[StoryState]:
        """Get the current HEAD state for a timeline."""
        refs = self._load_refs()
        head_hash = refs["timelines"].get(timeline)
        if head_hash:
            return self.get_state(head_hash)
        return None

    # -------------------------------------------------------------------------
    # History Traversal
    # -------------------------------------------------------------------------

    def history(self, start_hash: Optional[str] = None, timeline: str = "prime") -> Iterator[StoryState]:
        """
        Iterate through history from a state back to the beginning.

        Yields states from newest to oldest.
        """
        if start_hash is None:
            refs = self._load_refs()
            start_hash = refs["timelines"].get(timeline)

        current = start_hash
        while current:
            state = self.get_state(current)
            if state is None:
                break
            yield state
            current = state.parent_hash if state.parent_hash else None

    def get_history_length(self, timeline: str = "prime") -> int:
        """Get number of states in history."""
        return sum(1 for _ in self.history(timeline=timeline))

    # -------------------------------------------------------------------------
    # Entity Storage
    # -------------------------------------------------------------------------

    def save_entity(self, entity: TMEntity, entity_type: str) -> ContentHash:
        """Save an entity and return its content hash."""
        return self.objects.put(entity.to_dict(), entity_type)

    def get_entity(self, hash_val: str) -> Optional[Dict]:
        """Retrieve an entity by hash."""
        return self.objects.get_json(hash_val)

    # -------------------------------------------------------------------------
    # Branching (for Scinted realities)
    # -------------------------------------------------------------------------

    def create_branch(self, branch_name: str, from_timeline: str = "prime") -> str:
        """Create a new timeline branch from the current HEAD of another timeline."""
        refs = self._load_refs()
        source_hash = refs["timelines"].get(from_timeline)

        if source_hash is None:
            raise ValueError(f"Source timeline '{from_timeline}' has no states")

        refs["timelines"][branch_name] = source_hash
        self._save_refs(refs)

        return source_hash

    def list_timelines(self) -> List[str]:
        """List all timelines."""
        refs = self._load_refs()
        return list(refs["timelines"].keys())

    # -------------------------------------------------------------------------
    # Tagging
    # -------------------------------------------------------------------------

    def tag(self, tag_name: str, hash_val: Optional[str] = None, timeline: str = "prime"):
        """Create a named tag pointing to a state."""
        refs = self._load_refs()

        if hash_val is None:
            hash_val = refs["timelines"].get(timeline)

        if hash_val:
            refs["tags"][tag_name] = hash_val
            self._save_refs(refs)

    def get_tag(self, tag_name: str) -> Optional[str]:
        """Get the hash a tag points to."""
        refs = self._load_refs()
        return refs["tags"].get(tag_name)

    # -------------------------------------------------------------------------
    # Queries
    # -------------------------------------------------------------------------

    def find_states_with_character(self, character_id: str, timeline: str = "prime") -> List[StoryState]:
        """Find all states where a character appears."""
        results = []
        for state in self.history(timeline=timeline):
            if character_id in state.characters:
                results.append(state)
        return results

    def find_character_knowledge_at(self, character_id: str, state_hash: str) -> Optional[Dict]:
        """Get what a character knew at a specific state."""
        state = self.get_state(state_hash)
        if state and character_id in state.knowledge_states:
            return state.knowledge_states[character_id]
        return None

    def diff_states(self, hash_a: str, hash_b: str) -> Dict[str, Any]:
        """Compare two states and return differences."""
        state_a = self.get_state(hash_a)
        state_b = self.get_state(hash_b)

        if not state_a or not state_b:
            return {"error": "One or both states not found"}

        diff = {
            "chapter_change": state_b.current_chapter - state_a.current_chapter,
            "scene_change": state_b.current_scene - state_a.current_scene,
            "characters_added": [c for c in state_b.characters if c not in state_a.characters],
            "characters_removed": [c for c in state_a.characters if c not in state_b.characters],
            "threads_opened": [t for t in state_b.open_threads if t not in state_a.open_threads],
            "threads_resolved": [t for t in state_b.resolved_threads if t not in state_a.resolved_threads],
        }
        return diff

    # -------------------------------------------------------------------------
    # Stats
    # -------------------------------------------------------------------------

    def stats(self) -> Dict[str, Any]:
        """Get store statistics."""
        obj_stats = self.objects.stats()
        refs = self._load_refs()

        return {
            **obj_stats,
            "timelines": len(refs["timelines"]),
            "tags": len(refs["tags"]),
            "head": refs["HEAD"]
        }
