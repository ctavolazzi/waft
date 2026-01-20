"""
Thread-local context management for distributed tracing.
"""

import contextvars
from typing import Optional
from dataclasses import dataclass


@dataclass
class TraceContext:
    """Context information for a trace."""

    trace_id: str
    parent_span_id: Optional[str] = None
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


# Context variable for storing current trace context
_trace_context: contextvars.ContextVar[Optional[TraceContext]] = contextvars.ContextVar(
    "trace_context", default=None
)


def get_current_context() -> Optional[TraceContext]:
    """Get the current trace context."""
    return _trace_context.get()


def set_current_context(context: Optional[TraceContext]) -> None:
    """Set the current trace context."""
    _trace_context.set(context)


def clear_current_context() -> None:
    """Clear the current trace context."""
    _trace_context.set(None)
