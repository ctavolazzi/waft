"""
Session Analytics - Track, analyze, and learn from session data over time.

Provides data collection, storage, analysis, and eventually automated
prompt optimization through iterative testing and meta-learning.
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from collections import defaultdict
from dataclasses import dataclass, asdict
import hashlib


@dataclass
class SessionRecord:
    """Structured session data record."""
    session_id: str
    timestamp: str
    duration_seconds: Optional[float] = None
    
    # File metrics
    files_created: int = 0
    files_modified: int = 0
    files_deleted: int = 0
    
    # Code metrics
    lines_written: int = 0
    lines_modified: int = 0
    lines_deleted: int = 0
    net_lines: int = 0
    
    # Activity metrics
    commands_executed: List[str] = None
    work_efforts_created: int = 0
    work_efforts_updated: int = 0
    
    # Context
    project_name: str = ""
    branch: str = ""
    git_commits_ahead: int = 0
    
    # Prompt/approach tracking
    prompt_signature: Optional[str] = None  # Hash of key prompt characteristics
    approach_category: Optional[str] = None  # e.g., "feature_creation", "debugging", "refactoring"
    iteration_chain: Optional[str] = None  # Links to previous session if part of chain
    
    # Outcomes
    success_indicators: List[str] = None  # e.g., "tests_passed", "feature_complete"
    issues_encountered: List[str] = None
    
    # Metadata
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.commands_executed is None:
            self.commands_executed = []
        if self.success_indicators is None:
            self.success_indicators = []
        if self.issues_encountered is None:
            self.issues_encountered = []
        if self.metadata is None:
            self.metadata = {}


class SessionAnalytics:
    """Manages session data collection, storage, and analysis."""
    
    def __init__(self, project_path: Path):
        """
        Initialize session analytics.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.data_dir = project_path / "_pyrite" / "analytics"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # SQLite database for structured queries
        self.db_path = self.data_dir / "sessions.db"
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                duration_seconds REAL,
                files_created INTEGER DEFAULT 0,
                files_modified INTEGER DEFAULT 0,
                files_deleted INTEGER DEFAULT 0,
                lines_written INTEGER DEFAULT 0,
                lines_modified INTEGER DEFAULT 0,
                lines_deleted INTEGER DEFAULT 0,
                net_lines INTEGER DEFAULT 0,
                commands_executed TEXT,  -- JSON array
                work_efforts_created INTEGER DEFAULT 0,
                work_efforts_updated INTEGER DEFAULT 0,
                project_name TEXT,
                branch TEXT,
                git_commits_ahead INTEGER DEFAULT 0,
                prompt_signature TEXT,
                approach_category TEXT,
                iteration_chain TEXT,
                success_indicators TEXT,  -- JSON array
                issues_encountered TEXT,  -- JSON array
                metadata TEXT,  -- JSON object
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Indexes for common queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp ON sessions(timestamp)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_category ON sessions(approach_category)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_chain ON sessions(iteration_chain)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_prompt ON sessions(prompt_signature)
        """)
        
        conn.commit()
        conn.close()
    
    def save_session(self, session: SessionRecord) -> bool:
        """
        Save session record to database and JSON.
        
        Args:
            session: Session record to save
            
        Returns:
            True if successful
        """
        try:
            # Save to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO sessions (
                    session_id, timestamp, duration_seconds,
                    files_created, files_modified, files_deleted,
                    lines_written, lines_modified, lines_deleted, net_lines,
                    commands_executed, work_efforts_created, work_efforts_updated,
                    project_name, branch, git_commits_ahead,
                    prompt_signature, approach_category, iteration_chain,
                    success_indicators, issues_encountered, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.session_id,
                session.timestamp,
                session.duration_seconds,
                session.files_created,
                session.files_modified,
                session.files_deleted,
                session.lines_written,
                session.lines_modified,
                session.lines_deleted,
                session.net_lines,
                json.dumps(session.commands_executed),
                session.work_efforts_created,
                session.work_efforts_updated,
                session.project_name,
                session.branch,
                session.git_commits_ahead,
                session.prompt_signature,
                session.approach_category,
                session.iteration_chain,
                json.dumps(session.success_indicators),
                json.dumps(session.issues_encountered),
                json.dumps(session.metadata),
            ))
            
            conn.commit()
            conn.close()
            
            # Also save as JSON for easy inspection
            json_file = self.data_dir / "sessions" / f"{session.session_id}.json"
            json_file.parent.mkdir(parents=True, exist_ok=True)
            json_file.write_text(json.dumps(asdict(session), indent=2), encoding="utf-8")
            
            return True
        except Exception as e:
            print(f"Error saving session: {e}")
            return False
    
    def get_session(self, session_id: str) -> Optional[SessionRecord]:
        """Retrieve a session by ID."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return self._row_to_session(row)
    
    def get_sessions(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        category: Optional[str] = None,
        limit: int = 100
    ) -> List[SessionRecord]:
        """
        Query sessions with filters.
        
        Args:
            start_date: Filter sessions after this date
            end_date: Filter sessions before this date
            category: Filter by approach category
            limit: Maximum number of results
            
        Returns:
            List of session records
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM sessions WHERE 1=1"
        params = []
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date.isoformat())
        
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date.isoformat())
        
        if category:
            query += " AND approach_category = ?"
            params.append(category)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_session(row) for row in rows]
    
    def _row_to_session(self, row: sqlite3.Row) -> SessionRecord:
        """Convert database row to SessionRecord."""
        return SessionRecord(
            session_id=row["session_id"],
            timestamp=row["timestamp"],
            duration_seconds=row["duration_seconds"],
            files_created=row["files_created"],
            files_modified=row["files_modified"],
            files_deleted=row["files_deleted"],
            lines_written=row["lines_written"],
            lines_modified=row["lines_modified"],
            lines_deleted=row["lines_deleted"],
            net_lines=row["net_lines"],
            commands_executed=json.loads(row["commands_executed"] or "[]"),
            work_efforts_created=row["work_efforts_created"],
            work_efforts_updated=row["work_efforts_updated"],
            project_name=row["project_name"] or "",
            branch=row["branch"] or "",
            git_commits_ahead=row["git_commits_ahead"],
            prompt_signature=row["prompt_signature"],
            approach_category=row["approach_category"],
            iteration_chain=row["iteration_chain"],
            success_indicators=json.loads(row["success_indicators"] or "[]"),
            issues_encountered=json.loads(row["issues_encountered"] or "[]"),
            metadata=json.loads(row["metadata"] or "{}"),
        )
    
    def analyze_productivity_trends(
        self,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Analyze productivity trends over time.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary with trend analysis
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        sessions = self.get_sessions(start_date=start_date, end_date=end_date, limit=1000)
        
        if not sessions:
            return {"error": "No sessions found"}
        
        # Calculate metrics
        total_sessions = len(sessions)
        total_files = sum(s.files_created + s.files_modified for s in sessions)
        total_lines = sum(s.net_lines for s in sessions)
        avg_files_per_session = total_files / total_sessions if total_sessions > 0 else 0
        avg_lines_per_session = total_lines / total_sessions if total_sessions > 0 else 0
        
        # Group by category
        by_category = defaultdict(lambda: {"count": 0, "files": 0, "lines": 0})
        for session in sessions:
            category = session.approach_category or "uncategorized"
            by_category[category]["count"] += 1
            by_category[category]["files"] += session.files_created + session.files_modified
            by_category[category]["lines"] += session.net_lines
        
        # Group by day
        by_day = defaultdict(lambda: {"sessions": 0, "files": 0, "lines": 0})
        for session in sessions:
            day = session.timestamp[:10]  # YYYY-MM-DD
            by_day[day]["sessions"] += 1
            by_day[day]["files"] += session.files_created + session.files_modified
            by_day[day]["lines"] += session.net_lines
        
        return {
            "period_days": days,
            "total_sessions": total_sessions,
            "total_files": total_files,
            "total_lines": total_lines,
            "avg_files_per_session": avg_files_per_session,
            "avg_lines_per_session": avg_lines_per_session,
            "by_category": dict(by_category),
            "by_day": dict(by_day),
        }
    
    def analyze_prompt_drift(
        self,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Analyze prompt signature changes over time (prompt drift).
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary with drift analysis
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        sessions = self.get_sessions(start_date=start_date, end_date=end_date, limit=1000)
        
        if not sessions:
            return {"error": "No sessions found"}
        
        # Group by prompt signature
        by_prompt = defaultdict(lambda: {
            "count": 0,
            "avg_files": 0,
            "avg_lines": 0,
            "success_rate": 0,
            "sessions": []
        })
        
        for session in sessions:
            prompt = session.prompt_signature or "unknown"
            by_prompt[prompt]["count"] += 1
            by_prompt[prompt]["sessions"].append(session.session_id)
        
        # Calculate averages
        for prompt, data in by_prompt.items():
            prompt_sessions = [s for s in sessions if s.prompt_signature == prompt]
            if prompt_sessions:
                data["avg_files"] = sum(s.files_created + s.files_modified for s in prompt_sessions) / len(prompt_sessions)
                data["avg_lines"] = sum(s.net_lines for s in prompt_sessions) / len(prompt_sessions)
                data["success_rate"] = sum(1 for s in prompt_sessions if s.success_indicators) / len(prompt_sessions)
        
        return {
            "period_days": days,
            "unique_prompts": len(by_prompt),
            "by_prompt": dict(by_prompt),
        }
    
    def get_iteration_chains(self) -> Dict[str, List[str]]:
        """
        Get all iteration chains (sessions linked together).
        
        Returns:
            Dictionary mapping chain IDs to session IDs
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT iteration_chain, session_id FROM sessions WHERE iteration_chain IS NOT NULL")
        rows = cursor.fetchall()
        conn.close()
        
        chains = defaultdict(list)
        for chain_id, session_id in rows:
            chains[chain_id].append(session_id)
        
        return dict(chains)
    
    def compare_approaches(
        self,
        category1: str,
        category2: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Compare two approach categories.
        
        Args:
            category1: First category to compare
            category2: Second category to compare
            days: Number of days to analyze
            
        Returns:
            Comparison analysis
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        sessions1 = self.get_sessions(start_date=start_date, end_date=end_date, category=category1, limit=1000)
        sessions2 = self.get_sessions(start_date=start_date, end_date=end_date, category=category2, limit=1000)
        
        def calc_metrics(sessions):
            if not sessions:
                return {}
            return {
                "count": len(sessions),
                "avg_files": sum(s.files_created + s.files_modified for s in sessions) / len(sessions),
                "avg_lines": sum(s.net_lines for s in sessions) / len(sessions),
                "success_rate": sum(1 for s in sessions if s.success_indicators) / len(sessions),
            }
        
        return {
            category1: calc_metrics(sessions1),
            category2: calc_metrics(sessions2),
        }
    
    def generate_prompt_signature(
        self,
        commands: List[str],
        category: Optional[str] = None
    ) -> str:
        """
        Generate a signature hash for prompt characteristics.
        
        Args:
            commands: List of commands executed
            category: Approach category
            
        Returns:
            Hash signature
        """
        # Create signature from key characteristics
        signature_data = {
            "commands": sorted(set(commands)),
            "category": category or "unknown",
        }
        signature_str = json.dumps(signature_data, sort_keys=True)
        return hashlib.sha256(signature_str.encode()).hexdigest()[:16]
