"""
Storage backend for trace data using JSON-lines format.
"""

import json
import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime


class TraceStorage:
    """Stores trace spans in JSON-lines format."""

    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize the storage backend.

        Args:
            base_path: Base directory for trace files.
                      Defaults to _pyrite/analytics/traces/
        """
        if base_path is None:
            # Default to _pyrite/analytics/traces in current working directory
            base_path = Path.cwd() / "_pyrite" / "analytics" / "traces"

        self.base_path = Path(base_path)
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        """Ensure the traces directory exists."""
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _get_trace_file(self, date: Optional[datetime] = None) -> Path:
        """
        Get the trace file path for a given date.

        Args:
            date: Date for the trace file. Defaults to today.

        Returns:
            Path to the trace file
        """
        if date is None:
            date = datetime.utcnow()

        filename = f"{date.strftime('%Y-%m-%d')}.jsonl"
        return self.base_path / filename

    def write_span(self, span) -> None:
        """
        Write a span to the trace file.

        Args:
            span: The span to write
        """
        trace_file = self._get_trace_file()

        # Convert span to dict
        span_dict = span.to_dict()

        # Append to file as JSON line
        with open(trace_file, 'a') as f:
            json.dump(span_dict, f)
            f.write('\n')

    def read_traces(self, date: Optional[datetime] = None, trace_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Read traces from storage.

        Args:
            date: Date to read traces from. Defaults to today.
            trace_id: Optional trace ID to filter by

        Returns:
            List of span dictionaries
        """
        trace_file = self._get_trace_file(date)

        if not trace_file.exists():
            return []

        spans = []
        with open(trace_file, 'r') as f:
            for line in f:
                if line.strip():
                    span = json.loads(line)
                    if trace_id is None or span.get("trace_id") == trace_id:
                        spans.append(span)

        return spans

    def list_trace_files(self) -> List[Path]:
        """
        List all trace files.

        Returns:
            List of trace file paths
        """
        if not self.base_path.exists():
            return []

        return sorted(self.base_path.glob("*.jsonl"))

    def get_trace_by_id(self, trace_id: str) -> List[Dict[str, Any]]:
        """
        Get all spans for a specific trace ID across all files.

        Args:
            trace_id: The trace ID to search for

        Returns:
            List of span dictionaries
        """
        all_spans = []

        for trace_file in self.list_trace_files():
            with open(trace_file, 'r') as f:
                for line in f:
                    if line.strip():
                        span = json.loads(line)
                        if span.get("trace_id") == trace_id:
                            all_spans.append(span)

        return all_spans
