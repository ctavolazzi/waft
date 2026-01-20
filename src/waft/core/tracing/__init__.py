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
]

# Global tracer instance
_global_tracer = None


def get_tracer() -> Tracer:
    """Get or create the global tracer instance."""
    global _global_tracer
    if _global_tracer is None:
        _global_tracer = Tracer()
    return _global_tracer
