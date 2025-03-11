import logging
import uuid
from contextvars import ContextVar
from logging import LogRecord

# Context variable to store trace_id for the current execution context
trace_id_var: ContextVar[str] = ContextVar('trace_id', default='')

def get_trace_id() -> str:
    """Get the current trace ID or generate a new one if none exists."""
    trace_id = trace_id_var.get()
    if not trace_id:
        trace_id = str(uuid.uuid4())
        trace_id_var.set(trace_id)
    return trace_id

def set_trace_id(trace_id: str = None) -> None:
    """Set the trace ID for the current execution context."""
    if trace_id is None:
        trace_id = str(uuid.uuid4())
    trace_id_var.set(trace_id)

class TraceIdFilter(logging.Filter):
    """
    Logging filter that adds a trace_id attribute to LogRecord instances.
    If no trace_id is set in the current context, a new one is generated.
    """
    def filter(self, record: LogRecord) -> bool:
        record.trace_id = get_trace_id()
        return True

class RequestFormatter(logging.Formatter):
    """
    Custom formatter that ensures trace_id is included in log messages.
    Works with the standard format defined in the logging config.
    """
    def format(self, record: LogRecord) -> str:
        if not hasattr(record, 'trace_id'):
            record.trace_id = get_trace_id()
        return super().format(record)