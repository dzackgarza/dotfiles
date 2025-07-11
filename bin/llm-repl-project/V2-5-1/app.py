"""
LLM REPL V3 - Main Textual Application

Terminal-native TUI application designed for Arch + Sway integration.
Preserves all functionality from V2-5-tkinter-rewrite while achieving 
authentic terminal aesthetics.
"""

from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, Static, Input, Button

from config.settings import get_config
from core.timeline import TimelineManager
from core.cognition import CognitionProcessor
from core.blocks import create_user_input_block, create_assistant_response_block, create_error_block
from messages import UserMessage, ClearTimeline, ProcessingComplete, ProcessingError


class LLMReplApp(App):
    """LLM REPL V3 - Terminal-native TUI application"""
    
    TITLE = "LLM REPL V3 - Terminal Interface"
    CSS_PATH = "theme/theme.tcss"
    
    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+l", "clear_timeline", "Clear"),
        ("ctrl+s", "save_timeline", "Save"),
        ("escape", "cancel_processing", "Cancel"),
    ]
    
    def __init__(self, config_name: str = "debug"):
        super().__init__()
        self.config = get_config(config_name)
        self.timeline_manager = TimelineManager()
        self.cognition_processor = CognitionProcessor()
        self.cognition_processor.configure_processing_delay(self.config.cognition_delay)
        self.is_processing = False
    
    def compose(self) -> ComposeResult:
        """Compose the application layout"""
        yield Header()
        
        with Vertical():
            # Timeline placeholder - will be replaced with TimelineWidget
            yield Static("Welcome to LLM REPL V3!\\nStart by entering a message below.", id="timeline-placeholder")
            
            # Input area
            with Horizontal():
                yield Input(placeholder="Enter your message...", id="user-input")
                yield Button("Send", id="send-btn", variant="primary")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize app on startup"""
        # Add startup blocks like V2-5-tkinter-rewrite
        self.timeline_manager.initialize_with_startup_blocks(self.config.name)
        
        # Update timeline display
        self._update_timeline_display()
        
        # Focus input
        input_field = self.query_one("#user-input", Input)
        input_field.focus()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key in input"""
        if event.input.id == "user-input":
            text = event.value.strip()
            if text:
                self.post_message(UserMessage(text))
                event.input.value = ""
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle Send button"""
        if event.button.id == "send-btn":
            input_field = self.query_one("#user-input", Input)
            text = input_field.value.strip()
            if text:
                self.post_message(UserMessage(text))
                input_field.value = ""
    
    async def on_user_message(self, message: UserMessage) -> None:
        """Handle user input message"""
        if self.is_processing:
            self.notify("Processing in progress, please wait...")
            return
        
        # Add user block to timeline
        user_block = create_user_input_block(message.text)
        self.timeline_manager.add_block(user_block)
        self._update_timeline_display()
        
        try:
            self.is_processing = True
            self.notify("Processing...")
            
            # Process with cognition processor
            result = await self.cognition_processor.process(message.text)
            
            # Add assistant response
            response_block = create_assistant_response_block(
                result["final_output"], 
                result["total_tokens"],
                result
            )
            self.timeline_manager.add_block(response_block)
            self._update_timeline_display()
            
            self.notify("Ready")
            
        except Exception as e:
            error_block = create_error_block(f"Processing error: {str(e)}")
            self.timeline_manager.add_block(error_block)
            self._update_timeline_display()
            self.notify(f"Error: {str(e)}")
        
        finally:
            self.is_processing = False
    
    def on_clear_timeline(self, message: ClearTimeline) -> None:
        """Handle clear timeline message"""
        self.timeline_manager = TimelineManager()
        self._update_timeline_display()
        self.notify("Timeline cleared")
    
    def _update_timeline_display(self) -> None:
        """Update timeline display (simple version for Phase 1)"""
        blocks = self.timeline_manager.get_blocks()
        if not blocks:
            content = "Welcome to LLM REPL V3!\\nStart by entering a message below."
        else:
            content_lines = []
            for block in blocks:
                content_lines.append(f"[bold]{block.title}[/bold]")
                content_lines.append(f"  {block.content}")
                content_lines.append("")
            content = "\\n".join(content_lines)
        
        timeline = self.query_one("#timeline-placeholder", Static)
        timeline.update(content)
    
    def action_clear_timeline(self) -> None:
        """Clear timeline action"""
        self.post_message(ClearTimeline())
    
    def action_cancel_processing(self) -> None:
        """Cancel current processing"""
        if self.is_processing:
            self.is_processing = False
            self.notify("Processing cancelled")
        else:
            self.notify("No processing to cancel")
    
    def action_save_timeline(self) -> None:
        """Save timeline action (placeholder)"""
        self.notify("Save timeline (not implemented yet)")