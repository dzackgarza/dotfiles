"""V3-minimal: LLM REPL with Sacred Timeline and unix-rice aesthetics"""

from pathlib import Path
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical

from .config import AppConfig
from .core import InputProcessor, ResponseGenerator
from .ui import TimelineViewController
from .widgets.prompt_input import PromptInput
from .widgets.timeline import TimelineView
from .sacred_timeline import timeline


class LLMReplApp(App[None]):
    """Main application with Sacred Timeline architecture"""

    CSS_PATH = Path(__file__).parent / "theme.tcss"
    TITLE = AppConfig.TITLE
    SUB_TITLE = AppConfig.SUB_TITLE

    BINDINGS = [
        Binding("enter", "submit_prompt", "Send message", key_display="⏎"),
        Binding("shift+enter", "insert_newline", "New line", key_display="⇧⏎"),
        Binding("ctrl+c", "quit", "Quit", key_display="^C"),
    ]

    def __init__(self):
        super().__init__()

        # Core components following architectural patterns
        self.response_generator = ResponseGenerator()
        self.input_processor = InputProcessor(timeline, self.response_generator)

        # UI components
        self.timeline_view: TimelineView | None = None
        self.prompt_input: PromptInput | None = None
        self.timeline_controller: TimelineViewController | None = None

    def compose(self) -> ComposeResult:
        """Create the application layout - terminal-like, no header/footer"""
        with Vertical(id="main-container"):
            # Timeline view (scrolls bottom-up)
            yield TimelineView(id="timeline-container")

            # Input area
            with Horizontal(id="input-container"):
                yield PromptInput(id="prompt-input")

    def on_mount(self) -> None:
        """Initialize the application and wire components"""
        # Initialize UI components
        self.timeline_view = self.query_one("#timeline-container", TimelineView)
        self.prompt_input = self.query_one("#prompt-input", PromptInput)

        # Create and wire timeline controller
        self.timeline_controller = TimelineViewController(self.timeline_view)
        timeline.add_observer(self.timeline_controller)

        # Add welcome message to timeline
        timeline.add_block(
            role="system",
            content=AppConfig.WELCOME_MESSAGE,
        )

        # Set focus to input area
        self.prompt_input.focus()

    def on_prompt_input_prompt_submitted(
        self, event: PromptInput.PromptSubmitted
    ) -> None:
        """Handle user input submission - delegate to input processor"""
        self.input_processor.process_user_input(event.text)

    def action_submit_prompt(self) -> None:
        """Delegate prompt submission to the prompt input widget"""
        if self.prompt_input and self.prompt_input.has_focus:
            self.prompt_input.action_submit_prompt()

    def action_insert_newline(self) -> None:
        """Delegate newline insertion to the prompt input widget"""
        if self.prompt_input and self.prompt_input.has_focus:
            self.prompt_input.action_insert_newline()


def main():
    """Entry point for the application"""
    app = LLMReplApp()
    app.run()


if __name__ == "__main__":
    main()
