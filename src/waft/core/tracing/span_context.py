"""
Context manager for span execution with proper parent-child relationships.
"""

from typing import Optional
from contextlib import contextmanager

from .context import get_current_context, set_current_context, TraceContext


@contextmanager
def span_context(span):
    """
    Context manager that sets a span as the parent for child spans.

    Usage:
        span = tracer.start_span("operation", "layer")
        with span_context(span):
            # Any spans started here will be children of 'span'
            child_span = tracer.start_span("child_operation", "layer")
        tracer.end_span(span)

    Args:
        span: The span to use as parent
    """
    context = get_current_context()
    if context is None:
        yield
        return

    # Save current parent
    old_parent = context.parent_span_id

    # Set this span as parent for children
    context.parent_span_id = span.span_id

    try:
        yield
    finally:
        # Restore original parent
        context.parent_span_id = old_parent
