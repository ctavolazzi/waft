"""
Decorators for automatic function tracing.
"""

import functools
from typing import Callable, Any, Optional

from .tracer import SpanStatus


def trace_function(operation: Optional[str] = None, layer: str = "core", capture_args: bool = False, capture_result: bool = True):
    """
    Decorator to automatically trace a function.

    Args:
        operation: Name of the operation. Defaults to function name.
        layer: Application layer (api, core, persistence, etc.)
        capture_args: Whether to capture function arguments
        capture_result: Whether to capture the return value

    Usage:
        @trace_function(layer="core", capture_args=True)
        def my_function(x, y):
            return x + y
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            from . import get_tracer
            tracer = get_tracer()
            op_name = operation or f"{func.__module__}.{func.__name__}"

            # Prepare span data
            span_data = {}
            if capture_args:
                span_data["args"] = tracer._sanitize_data(args)
                span_data["kwargs"] = tracer._sanitize_data(kwargs)

            # Start span
            span = tracer.start_span(op_name, layer, data=span_data)

            try:
                result = func(*args, **kwargs)
                output_data = result if capture_result else None
                tracer.end_span(span, SpanStatus.SUCCESS, output_data)
                return result
            except Exception as e:
                tracer.end_span(span, SpanStatus.ERROR, error=e)
                raise

        return wrapper
    return decorator


def trace_data_transform(operation: Optional[str] = None, layer: str = "core"):
    """
    Decorator specifically for data transformation functions.
    Automatically captures input (first arg) and output.

    Args:
        operation: Name of the operation. Defaults to function name.
        layer: Application layer

    Usage:
        @trace_data_transform(operation="normalize_scores")
        def normalize(data):
            return normalized_data
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            from . import get_tracer
            tracer = get_tracer()
            op_name = operation or f"{func.__module__}.{func.__name__}"

            # Capture first argument as input
            input_data = args[0] if args else None
            span_data = {"input": tracer._sanitize_data(input_data)}

            span = tracer.start_span(op_name, layer, data=span_data)

            try:
                result = func(*args, **kwargs)
                tracer.end_span(span, SpanStatus.SUCCESS, output_data=result)
                return result
            except Exception as e:
                tracer.end_span(span, SpanStatus.ERROR, error=e)
                raise

        return wrapper
    return decorator
