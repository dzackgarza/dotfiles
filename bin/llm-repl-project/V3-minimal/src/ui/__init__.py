"""UI coordination components for LLM REPL V3-minimal

Following the established architecture with clean separation between
timeline state management and UI widget coordination.
"""

from .timeline_controller import TimelineViewController

__all__ = ["TimelineViewController"]
