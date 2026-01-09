"""
Core tracer implementation for distributed tracing.
"""

import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

from .context import TraceContext, get_current_context, set_current_context
from .storage import TraceStorage


class SpanStatus(Enum):
    """Status of a span."""
    SUCCESS = "success"
    ERROR = "error"
    PENDING = "pending"


@dataclass
class Span:
    """Represents a single traced operation (span)."""

    trace_id: str
    span_id: str
    operation: str
    layer: str
    parent_span_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    duration_ms: Optional[float] = None
    status: SpanStatus = SpanStatus.PENDING
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    # Internal tracking
    _start_time: Optional[float] = field(default=None, repr=False)

    def to_dict(self) -> Dict[str, Any]:
        """Convert span to dictionary for storage."""
        result = asdict(self)
        result["status"] = self.status.value
        # Remove internal fields
        result.pop("_start_time", None)
        return result


class Tracer:
    """Main tracer class for managing distributed traces."""

    def __init__(self, storage: Optional[TraceStorage] = None):
        """
        Initialize the tracer.

        Args:
            storage: Optional custom storage backend. If None, uses default.
        """
        self.storage = storage or TraceStorage()

    def start_trace(self, operation: str, layer: str, metadata: Optional[Dict[str, Any]] = None) -> Span:
        """
        Start a new trace (root span).

        Args:
            operation: Name of the operation being traced
            layer: Layer of the application (api, core, persistence, etc.)
            metadata: Optional metadata to attach to the trace

        Returns:
            The newly created root span
        """
        trace_id = str(uuid.uuid4())
        span_id = str(uuid.uuid4())

        # Create trace context
        context = TraceContext(
            trace_id=trace_id,
            parent_span_id=None,
            metadata=metadata or {}
        )
        set_current_context(context)

        # Create root span
        span = Span(
            trace_id=trace_id,
            span_id=span_id,
            operation=operation,
            layer=layer,
            metadata=metadata or {},
            _start_time=time.time()
        )

        return span

    def start_span(self, operation: str, layer: str, data: Optional[Dict[str, Any]] = None) -> Span:
        """
        Start a new span within an existing trace.

        Args:
            operation: Name of the operation being traced
            layer: Layer of the application
            data: Optional data to attach to the span

        Returns:
            The newly created span
        """
        context = get_current_context()

        if context is None:
            # No active trace, start a new one
            return self.start_trace(operation, layer)

        span_id = str(uuid.uuid4())

        span = Span(
            trace_id=context.trace_id,
            span_id=span_id,
            operation=operation,
            layer=layer,
            parent_span_id=context.parent_span_id,
            data=data or {},
            metadata=context.metadata,
            _start_time=time.time()
        )

        # Note: We intentionally DO NOT update context.parent_span_id here
        # This allows sibling spans to share the same parent
        # Child spans should be created by updating context before calling start_span

        return span

    def end_span(
        self,
        span: Span,
        status: SpanStatus = SpanStatus.SUCCESS,
        output_data: Optional[Any] = None,
        error: Optional[Exception] = None
    ) -> None:
        """
        End a span and record it.

        Args:
            span: The span to end
            status: Status of the operation
            output_data: Optional output data to record
            error: Optional exception if status is ERROR
        """
        if span._start_time is not None:
            span.duration_ms = (time.time() - span._start_time) * 1000

        span.status = status

        if output_data is not None:
            span.data["output"] = self._sanitize_data(output_data)

        if error is not None:
            span.error = str(error)
            span.status = SpanStatus.ERROR

        # Store the span
        self.storage.write_span(span)

    def trace_data_transform(
        self,
        operation: str,
        layer: str,
        input_data: Any,
        transform_fn: callable,
        capture_output: bool = True
    ) -> Any:
        """
        Trace a data transformation operation.

        Args:
            operation: Name of the transformation
            layer: Application layer
            input_data: Input to the transformation
            transform_fn: Function that performs the transformation
            capture_output: Whether to capture the output data

        Returns:
            The result of the transformation
        """
        span = self.start_span(operation, layer, data={"input": self._sanitize_data(input_data)})

        try:
            result = transform_fn()
            output_data = result if capture_output else None
            self.end_span(span, SpanStatus.SUCCESS, output_data)
            return result
        except Exception as e:
            self.end_span(span, SpanStatus.ERROR, error=e)
            raise

    def _sanitize_data(self, data: Any, max_size: int = 1000) -> Any:
        """
        Sanitize data for storage (truncate large objects).

        Args:
            data: Data to sanitize
            max_size: Maximum string length

        Returns:
            Sanitized data
        """
        if data is None:
            return None

        # Convert to string and check size
        data_str = str(data)
        if len(data_str) > max_size:
            return data_str[:max_size] + f"... (truncated, total length: {len(data_str)})"

        return data
