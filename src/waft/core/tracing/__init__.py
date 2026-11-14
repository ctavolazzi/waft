"""
Minimal data tracing system for Waft.

Provides lightweight distributed tracing capabilities to track
data flow and transformations throughout the application.
"""

from .tracer import Tracer, Span, SpanStatus
from .context import TraceContext
from .decorators import trace_function, trace_data_transform
from .storage import TraceStorage
from .viewer import TraceViewer
from .span_context import span_context

__all__ = [
    "Tracer",
    "Span",
    "SpanStatus",
    "TraceContext",
    "trace_function",
    "trace_data_transform",
    "TraceStorage",
    "TraceViewer",
    "span_context",
    "get_tracer",
    "reset_tracer",
]

# Global tracer instance
_global_tracer = None


def get_tracer() -> Tracer:
    """Get or create the global tracer instance."""
    global _global_tracer
    if _global_tracer is None:
        _global_tracer = Tracer()
    return _global_tracer


def reset_tracer() -> None:
    """Drop the global tracer so the next get_tracer() reads WAFT_TRACE_DIR and WAFT_TRACING again."""
    global _global_tracer
    _global_tracer = None
