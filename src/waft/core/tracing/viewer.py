"""
Trace viewer utilities for displaying and analyzing traces.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from .storage import TraceStorage


class TraceViewer:
    """View and analyze collected traces."""

    def __init__(self, storage: Optional[TraceStorage] = None):
        """
        Initialize the trace viewer.

        Args:
            storage: Optional storage backend. If None, uses default.
        """
        self.storage = storage or TraceStorage()

    def get_trace(self, trace_id: str) -> List[Dict[str, Any]]:
        """
        Get all spans for a specific trace.

        Args:
            trace_id: The trace ID to retrieve

        Returns:
            List of span dictionaries
        """
        return self.storage.get_trace_by_id(trace_id)

    def list_recent_traces(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        List recent traces.

        Args:
            limit: Maximum number of traces to return

        Returns:
            List of trace root spans (first span of each trace)
        """
        trace_files = self.storage.list_trace_files()
        if not trace_files:
            return []

        # Read from most recent file
        recent_file = trace_files[-1]
        spans = []

        with open(recent_file, 'r') as f:
            import json
            for line in f:
                if line.strip():
                    span = json.loads(line)
                    # Only include root spans (no parent)
                    if span.get('parent_span_id') is None:
                        spans.append(span)

        # Return most recent
        return sorted(spans, key=lambda s: s['timestamp'], reverse=True)[:limit]

    def format_trace_tree(self, trace_id: str) -> str:
        """
        Format a trace as a tree for display.

        Args:
            trace_id: The trace ID to format

        Returns:
            Formatted string representation of the trace tree
        """
        spans = self.get_trace(trace_id)
        if not spans:
            return f"No trace found with ID: {trace_id}"

        # Build span lookup
        span_lookup = {s['span_id']: s for s in spans}

        # Find root span
        root_spans = [s for s in spans if s.get('parent_span_id') is None]
        if not root_spans:
            return "Invalid trace: no root span found"

        root = root_spans[0]

        # Build tree
        lines = []
        lines.append(f"Trace ID: {trace_id}")
        lines.append(f"Timestamp: {root['timestamp']}")
        lines.append("")

        self._format_span_recursive(root, span_lookup, lines, indent=0)

        return "\n".join(lines)

    def _format_span_recursive(
        self,
        span: Dict[str, Any],
        span_lookup: Dict[str, Dict[str, Any]],
        lines: List[str],
        indent: int
    ) -> None:
        """
        Recursively format a span and its children.

        Args:
            span: The span to format
            span_lookup: Dictionary of all spans by ID
            lines: Output lines list
            indent: Current indentation level
        """
        prefix = "  " * indent
        duration = span.get('duration_ms', 0)
        status = span.get('status', 'unknown')
        status_icon = "✓" if status == "success" else "✗" if status == "error" else "•"

        line = f"{prefix}{status_icon} {span['operation']} ({duration:.2f}ms) [{span['layer']}]"
        lines.append(line)

        # Add error info if present
        if span.get('error'):
            lines.append(f"{prefix}  Error: {span['error']}")

        # Add data summary if present
        data = span.get('data', {})
        if data:
            # Show input/output info
            if 'input' in data:
                lines.append(f"{prefix}  Input: {self._summarize_data(data['input'])}")
            if 'output' in data:
                lines.append(f"{prefix}  Output: {self._summarize_data(data['output'])}")

        # Find and format children
        children = [
            s for s in span_lookup.values()
            if s.get('parent_span_id') == span['span_id']
        ]

        for child in sorted(children, key=lambda s: s['timestamp']):
            self._format_span_recursive(child, span_lookup, lines, indent + 1)

    def _summarize_data(self, data: Any) -> str:
        """
        Create a short summary of data for display.

        Args:
            data: Data to summarize

        Returns:
            Summary string
        """
        if data is None:
            return "None"

        data_str = str(data)
        if len(data_str) > 100:
            return data_str[:100] + "..."
        return data_str

    def format_trace_summary(self, span: Dict[str, Any]) -> str:
        """
        Format a single span as a summary line.

        Args:
            span: The span to format

        Returns:
            Summary string
        """
        trace_id = span['trace_id'][:8]
        timestamp = span['timestamp'].split('T')[1].split('.')[0]
        operation = span['operation']
        status = span.get('status', 'unknown')
        duration = span.get('duration_ms', 0)

        status_icon = "✓" if status == "success" else "✗"

        return f"{status_icon} [{trace_id}] {timestamp} | {operation} ({duration:.2f}ms)"
