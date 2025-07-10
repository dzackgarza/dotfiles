"""#!/usr/bin/env python3
"""
Timeline Widget - A rich, interactive timeline for the LLM REPL

This module contains the implementation of the timeline widget, which is a
central component of the application. The timeline provides a chronological
view of the conversation and the AI's cognitive processes, and is designed
to be a rich and interactive component.
"""

from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Static
from rich.panel import Panel

from enum import Enum
from dataclasses import dataclass, field
import time
from typing import Dict, Any, List

class MessageType(Enum):
    """Types of messages in the conversation."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    COGNITION = "cognition"
    ERROR = "error"

@dataclass
class ConversationMessage:
    """A message in the conversation timeline."""
    id: str
    type: MessageType
    content: Any
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    tokens: Dict[str, int] = field(default_factory=lambda: {"input": 0, "output": 0})
    state: str = "inscribed"  # inscribed, live

class MessageWidget(Static):
    """Widget for displaying a single message in the timeline."""

    def __init__(self, message: ConversationMessage, **kwargs):
        super().__init__(**kwargs)
        self.message = message

    def compose(self) -> ComposeResult:
        """Compose the message widget."""
        border_style = "green"
        title = "Message"
        if self.message.type == MessageType.USER:
            title = "👤 You"
            border_style = "green"
        elif self.message.type == MessageType.ASSISTANT:
            title = f"🤖 Assistant"
            border_style = "blue"
        elif self.message.type == MessageType.COGNITION:
            title = "🧠 Cognition"
            border_style = "purple"
        elif self.message.type == MessageType.SYSTEM:
            title = "⚙️ System"
            border_style = "yellow"
        elif self.message.type == MessageType.ERROR:
            title = "❌ Error"
            border_style = "red"

        if self.message.state == "live":
            border_style = "blink"

        content = self.message.content
        if isinstance(content, str):
            content = Panel(content, title=title, border_style=border_style, padding=(1, 2))

        yield Static(content)

class TimelineWidget(ScrollableContainer):
    """Widget for displaying the conversation timeline."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messages: List[ConversationMessage] = []
        self._message_ids: set = set()

    def add_message(self, message: ConversationMessage) -> bool:
        """Add a message to the timeline, preventing duplicates."""
        if message.id in self._message_ids:
            return False  # Duplicate, don't add

        self.messages.append(message)
        self._message_ids.add(message.id)
        widget = MessageWidget(message, id=f"msg_{message.id}")
        self.mount(widget)
        self.scroll_end(animate=True)
        return True

    def update_message_state(self, message_id: str, new_state: str):
        """Update the state of a message in the timeline."""
        for message in self.messages:
            if message.id == message_id:
                message.state = new_state
                # Re-render the widget
                widget = self.query_one(f"#msg_{message_id}", MessageWidget)
                widget.remove()
                new_widget = MessageWidget(message, id=f"msg_{message.id}")
                self.mount(new_widget)
                break
""