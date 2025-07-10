from dataclasses import dataclass
from datetime import datetime
from textual import events, on
from textual.reactive import reactive
from textual.widgets import TextArea
from textual.message import Message

from ..config import TimelineConfig, UIConfig


class PromptInput(TextArea):
    """Enhanced input widget: Enter=send, Shift+Enter=newline"""

    @dataclass
    class PromptSubmitted(Message):
        text: str
        prompt_input: "PromptInput"

    @dataclass
    class CursorEscapingTop(Message):
        pass

    @dataclass
    class CursorEscapingBottom(Message):
        pass

    submit_ready = reactive(True)

    @property
    def cursor_at_end_of_text(self) -> bool:
        """Check if cursor is at the end of the text."""
        row, col = self.cursor_location
        lines = self.text.split("\n")
        if row == len(lines) - 1:  # Last line
            return col >= len(lines[row])
        return False

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            name=name, id=id, classes=classes, disabled=disabled, language="markdown"
        )

    def on_key(self, event: events.Key) -> None:
        # Intercept Enter key to prevent default TextArea newline behavior
        if event.key == "enter":
            event.prevent_default()
            # App-level bindings will handle calling action_submit_prompt or action_insert_newline
            # based on whether Shift is pressed. We just need to prevent the default.

        # Handle cursor escaping
        if self.cursor_location == UIConfig.CURSOR_TOP_POSITION and event.key == "up":
            # print("DEBUG: Cursor at (0,0), sending CursorEscapingTop")
            event.prevent_default()
            self.post_message(self.CursorEscapingTop())
            event.stop()
        elif self.cursor_at_end_of_text and event.key == "down":
            # print(f"DEBUG: Cursor at end, sending CursorEscapingBottom")
            event.prevent_default()
            self.post_message(self.CursorEscapingBottom())
            event.stop()

    def watch_submit_ready(self, submit_ready: bool) -> None:
        self.set_class(not submit_ready, "-submit-blocked")

    def on_mount(self):
        # PowerLine-style prompt with useful info
        now = datetime.now()
        time_str = now.strftime(TimelineConfig.BORDER_TITLE_FORMAT)
        self.border_title = f"❯ Sacred Timeline • {time_str} • V3-minimal"

    @on(TextArea.Changed)
    async def prompt_changed(self, event: TextArea.Changed) -> None:
        text_area = event.text_area
        # Remove subtitle indicators - users know how text boxes work
        text_area.border_subtitle = None

        text_area.set_class(text_area.wrapped_document.height > 1, "multiline")

        # Refresh parent when height changes
        if self.parent:
            self.parent.refresh()

    def action_submit_prompt(self) -> None:
        """Send message on Enter key"""
        if self.text.strip() == "":
            self.notify("Cannot send empty message!")
            return

        if self.submit_ready:
            message = self.PromptSubmitted(self.text, prompt_input=self)
            self.clear()
            self.post_message(message)
        else:
            self.app.bell()
            self.notify("Please wait for response to complete.")

    def action_insert_newline(self) -> None:
        """Insert newline on Shift+Enter"""
        self.insert("\n")
