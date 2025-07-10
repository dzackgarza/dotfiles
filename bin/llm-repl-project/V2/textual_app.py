#!/usr/bin/env python3
"""
Textual-Based LLM REPL - Massive Differential Overhaul

COMPLETE REWRITE using Textual to solve all UI problems:
- No more timeline duplicates
- Proper layout management
- Professional GUI-like interface
- Offloads hard problems to Textual library
- Emulates Claude Code interface

PRESERVED from original architecture:
- Cognition blocks concept
- Plugin-based processing
- LLM interface abstraction
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Header, Footer, Input, Static, Button, 
    RichLog, ProgressBar, Label, Markdown
)
from textual.reactive import reactive, var
from textual.message import Message
from textual.binding import Binding
from textual.screen import Screen
from textual.css.query import NoMatches

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown as RichMarkdown
from rich.syntax import Syntax
from rich.table import Table

import asyncio
import time
from typing import Optional, List, Dict, Any, AsyncGenerator
from dataclasses import dataclass
from enum import Enum
import uuid


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
    content: str
    timestamp: float
    metadata: Dict[str, Any]
    tokens: Dict[str, int] = None
    
    def __post_init__(self):
        if self.tokens is None:
            self.tokens = {"input": 0, "output": 0}


class ConversationTimeline:
    """Manages the conversation timeline with proper deduplication."""
    
    def __init__(self):
        self.messages: List[ConversationMessage] = []
        self._message_ids: set = set()
    
    def add_message(self, message: ConversationMessage) -> bool:
        """Add message to timeline, preventing duplicates."""
        if message.id in self._message_ids:
            return False  # Duplicate, don't add
        
        self.messages.append(message)
        self._message_ids.add(message.id)
        return True
    
    def get_recent_messages(self, count: int = 10) -> List[ConversationMessage]:
        """Get recent messages for display."""
        return self.messages[-count:] if self.messages else []
    
    def get_total_tokens(self) -> Dict[str, int]:
        """Get total token usage."""
        total = {"input": 0, "output": 0}
        for msg in self.messages:
            if msg.tokens:
                total["input"] += msg.tokens.get("input", 0)
                total["output"] += msg.tokens.get("output", 0)
        return total


class CognitionBlock:
    """
    Simplified cognition block that preserves your multi-step LLM concept.
    
    PRESERVED: Multi-step LLM processing
    SIMPLIFIED: Clean interface, better error handling
    """
    
    def __init__(self, name: str):
        self.name = name
        self.steps: List[str] = []
        self.current_step = 0
        self.total_tokens = {"input": 0, "output": 0}
    
    async def process(self, input_text: str, llm_interface) -> AsyncGenerator[str, None]:
        """Process input through cognition steps with streaming."""
        self.steps = ["Analyzing query", "Enhancing prompt", "Generating response"]
        
        for i, step in enumerate(self.steps):
            self.current_step = i
            yield f"🧠 {step}..."
            
            # Simulate processing time
            await asyncio.sleep(0.5)
            
            # Mock LLM call
            if i == len(self.steps) - 1:
                # Final step - generate actual response
                response = f"This is a response to: {input_text}"
                self.total_tokens["input"] += len(input_text.split())
                self.total_tokens["output"] += len(response.split())
                yield response
            else:
                yield f"✅ {step} complete"
    
    def get_progress(self) -> float:
        """Get processing progress (0.0 to 1.0)."""
        if not self.steps:
            return 0.0
        return (self.current_step + 1) / len(self.steps)


class MessageWidget(Static):
    """Widget for displaying a single message in the timeline."""
    
    def __init__(self, message: ConversationMessage, **kwargs):
        super().__init__(**kwargs)
        self.message = message
    
    def compose(self) -> ComposeResult:
        """Compose the message widget."""
        # Create content based on message type
        if self.message.type == MessageType.USER:
            content = Panel(
                self.message.content,
                title="👤 You",
                border_style="green",
                padding=(1, 2)
            )
        elif self.message.type == MessageType.ASSISTANT:
            tokens = self.message.tokens
            token_info = f"↑{tokens['input']} ↓{tokens['output']}" if tokens else ""
            content = Panel(
                self.message.content,
                title=f"🤖 Assistant {token_info}",
                border_style="blue",
                padding=(1, 2)
            )
        elif self.message.type == MessageType.COGNITION:
            content = Panel(
                self.message.content,
                title="🧠 Cognition",
                border_style="purple",
                padding=(1, 2)
            )
        elif self.message.type == MessageType.SYSTEM:
            content = Panel(
                self.message.content,
                title="⚙️ System",
                border_style="yellow",
                padding=(1, 2)
            )
        else:  # ERROR
            content = Panel(
                self.message.content,
                title="❌ Error",
                border_style="red",
                padding=(1, 2)
            )
        
        yield Static(content)


class TimelineWidget(ScrollableContainer):
    """Widget for displaying the conversation timeline."""
    
    def __init__(self, timeline: ConversationTimeline, **kwargs):
        super().__init__(**kwargs)
        self.timeline = timeline
        self.message_widgets: Dict[str, MessageWidget] = {}
    
    def add_message(self, message: ConversationMessage):
        """Add a message to the timeline display."""
        if self.timeline.add_message(message):
            # Only add if it's not a duplicate
            widget = MessageWidget(message, id=f"msg_{message.id}")
            self.mount(widget)
            self.message_widgets[message.id] = widget
            
            # Auto-scroll to bottom
            self.scroll_end(animate=True)
    
    def clear_timeline(self):
        """Clear the timeline display."""
        for widget in self.message_widgets.values():
            widget.remove()
        self.message_widgets.clear()
        self.timeline.messages.clear()
        self.timeline._message_ids.clear()


class InputWidget(Container):
    """Enhanced input widget with expanding text area."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_field: Optional[Input] = None
    
    def compose(self) -> ComposeResult:
        """Compose the input widget."""
        with Vertical():
            yield Label("💬 Type your message (Enter to send, Ctrl+C to exit)")
            self.input_field = Input(
                placeholder="Ask me anything...",
                id="user_input"
            )
            yield self.input_field
    
    def focus_input(self):
        """Focus the input field."""
        if self.input_field:
            self.input_field.focus()
    
    def clear_input(self):
        """Clear the input field."""
        if self.input_field:
            self.input_field.value = ""
    
    def get_input_value(self) -> str:
        """Get the current input value."""
        return self.input_field.value if self.input_field else ""


class StatusWidget(Container):
    """Status widget showing token counts and processing state."""
    
    def __init__(self, timeline: ConversationTimeline, **kwargs):
        super().__init__(**kwargs)
        self.timeline = timeline
        self.is_processing = reactive(False)
        self.current_operation = reactive("")
        self.progress = reactive(0.0)
    
    def compose(self) -> ComposeResult:
        """Compose the status widget."""
        with Horizontal():
            yield Label("📊", id="status_icon")
            yield Label("Ready", id="status_text")
            yield Label("Tokens: ↑0 ↓0", id="token_count")
            yield ProgressBar(total=100, show_eta=False, id="progress_bar")
    
    def update_status(self, operation: str = "", progress: float = 0.0, processing: bool = False):
        """Update the status display."""
        self.is_processing = processing
        self.current_operation = operation
        self.progress = progress
        
        # Update status text
        try:
            status_text = self.query_one("#status_text", Label)
            if processing:
                status_text.update(f"🔄 {operation}")
            else:
                status_text.update("✅ Ready")
        except NoMatches:
            pass
        
        # Update progress bar
        try:
            progress_bar = self.query_one("#progress_bar", ProgressBar)
            progress_bar.progress = int(progress * 100)
            progress_bar.display = processing
        except NoMatches:
            pass
        
        # Update token count
        try:
            token_label = self.query_one("#token_count", Label)
            tokens = self.timeline.get_total_tokens()
            token_label.update(f"Tokens: ↑{tokens['input']} ↓{tokens['output']}")
        except NoMatches:
            pass


class LLMREPLApp(App):
    """
    Main Textual application for LLM REPL.
    
    MASSIVE IMPROVEMENT:
    - Professional GUI-like interface
    - No more timeline issues
    - Proper layout management
    - Keyboard shortcuts
    - Status indicators
    """
    
    CSS = """
    Screen {
        layout: vertical;
    }
    
    #main_container {
        layout: vertical;
        height: 1fr;
    }
    
    #timeline_container {
        height: 1fr;
        border: solid $primary;
        margin: 1;
    }
    
    #input_container {
        height: auto;
        min-height: 4;
        border: solid $accent;
        margin: 1;
    }
    
    #status_container {
        height: 3;
        border: solid $secondary;
        margin: 1;
    }
    
    Input {
        width: 1fr;
    }
    
    ProgressBar {
        width: 20;
    }
    
    MessageWidget {
        margin: 1 0;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("ctrl+l", "clear_timeline", "Clear"),
        Binding("f1", "show_help", "Help"),
    ]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timeline = ConversationTimeline()
        self.cognition_block = CognitionBlock("default")
        self.is_processing = False
    
    def compose(self) -> ComposeResult:
        """Compose the main application layout."""
        yield Header()
        
        with Container(id="main_container"):
            # Timeline area
            with Container(id="timeline_container"):
                yield TimelineWidget(self.timeline, id="timeline")
            
            # Input area
            with Container(id="input_container"):
                yield InputWidget(id="input_widget")
            
            # Status area
            with Container(id="status_container"):
                yield StatusWidget(self.timeline, id="status_widget")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self.title = "LLM REPL - Textual Interface"
        self.sub_title = "Powered by Textual"
        
        # Focus the input
        input_widget = self.query_one("#input_widget", InputWidget)
        input_widget.focus_input()
        
        # Add welcome message
        welcome_msg = ConversationMessage(
            id=str(uuid.uuid4()),
            type=MessageType.SYSTEM,
            content="Welcome to LLM REPL! Type your message below and press Enter to start chatting.",
            timestamp=time.time(),
            metadata={"source": "system"}
        )
        
        timeline_widget = self.query_one("#timeline", TimelineWidget)
        timeline_widget.add_message(welcome_msg)
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        if event.input.id == "user_input" and not self.is_processing:
            user_input = event.value.strip()
            if user_input:
                # Clear input immediately
                event.input.value = ""
                
                # Process the input
                self.run_worker(self.process_user_input(user_input))
    
    async def process_user_input(self, user_input: str):
        """Process user input through the cognition block."""
        self.is_processing = True
        
        timeline_widget = self.query_one("#timeline", TimelineWidget)
        status_widget = self.query_one("#status_widget", StatusWidget)
        
        try:
            # Add user message
            user_msg = ConversationMessage(
                id=str(uuid.uuid4()),
                type=MessageType.USER,
                content=user_input,
                timestamp=time.time(),
                metadata={"source": "user"}
            )
            timeline_widget.add_message(user_msg)
            
            # Process through cognition block with streaming
            cognition_content = ""
            assistant_content = ""
            
            async for chunk in self.cognition_block.process(user_input, None):
                if chunk.startswith("🧠"):
                    # Cognition step
                    status_widget.update_status(
                        chunk, 
                        self.cognition_block.get_progress(), 
                        True
                    )
                    cognition_content += chunk + "\n"
                elif chunk.startswith("✅"):
                    # Step completion
                    cognition_content += chunk + "\n"
                else:
                    # Final response
                    assistant_content = chunk
            
            # Add cognition message if there's content
            if cognition_content.strip():
                cognition_msg = ConversationMessage(
                    id=str(uuid.uuid4()),
                    type=MessageType.COGNITION,
                    content=cognition_content.strip(),
                    timestamp=time.time(),
                    metadata={"source": "cognition", "steps": self.cognition_block.steps}
                )
                timeline_widget.add_message(cognition_msg)
            
            # Add assistant response
            assistant_msg = ConversationMessage(
                id=str(uuid.uuid4()),
                type=MessageType.ASSISTANT,
                content=assistant_content,
                timestamp=time.time(),
                metadata={"source": "assistant"},
                tokens=self.cognition_block.total_tokens.copy()
            )
            timeline_widget.add_message(assistant_msg)
            
            # Update status
            status_widget.update_status("Complete", 1.0, False)
            
        except Exception as e:
            # Add error message
            error_msg = ConversationMessage(
                id=str(uuid.uuid4()),
                type=MessageType.ERROR,
                content=f"Error processing request: {str(e)}",
                timestamp=time.time(),
                metadata={"source": "error", "error_type": type(e).__name__}
            )
            timeline_widget.add_message(error_msg)
            status_widget.update_status("Error", 0.0, False)
        
        finally:
            self.is_processing = False
            
            # Refocus input
            input_widget = self.query_one("#input_widget", InputWidget)
            input_widget.focus_input()
    
    def action_clear_timeline(self) -> None:
        """Clear the conversation timeline."""
        timeline_widget = self.query_one("#timeline", TimelineWidget)
        timeline_widget.clear_timeline()
        
        # Add welcome message back
        welcome_msg = ConversationMessage(
            id=str(uuid.uuid4()),
            type=MessageType.SYSTEM,
            content="Timeline cleared. Ready for new conversation!",
            timestamp=time.time(),
            metadata={"source": "system"}
        )
        timeline_widget.add_message(welcome_msg)
    
    def action_show_help(self) -> None:
        """Show help information."""
        help_msg = ConversationMessage(
            id=str(uuid.uuid4()),
            type=MessageType.SYSTEM,
            content="""
**LLM REPL Help**

**Keyboard Shortcuts:**
- Enter: Send message
- Ctrl+C: Quit application
- Ctrl+L: Clear timeline
- F1: Show this help

**Features:**
- Real-time conversation with AI
- Cognition blocks for multi-step processing
- Token usage tracking
- Professional GUI interface

Type your message in the input box and press Enter to start chatting!
            """.strip(),
            timestamp=time.time(),
            metadata={"source": "help"}
        )
        
        timeline_widget = self.query_one("#timeline", TimelineWidget)
        timeline_widget.add_message(help_msg)


async def main():
    """Main entry point for the Textual LLM REPL."""
    app = LLMREPLApp()
    await app.run_async()


if __name__ == "__main__":
    asyncio.run(main())