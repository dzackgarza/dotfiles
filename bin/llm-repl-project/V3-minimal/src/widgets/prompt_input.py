from dataclasses import dataclass
from datetime import datetime
from textual import events, on
from textual.reactive import reactive
from textual.widgets import TextArea
from textual.message import Message

from ..config import TimelineConfig, UIConfig


class PromptInput(TextArea):
    """Enhanced input widget: Enter=send, Shift+Enter=newline (requires Kitty terminal)"""

    # Override TextArea's key bindings
    BINDINGS = [
        # Clear TextArea's default Enter binding
    ]

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

    # Note: Enter/Shift+Enter handled explicitly in on_key for precise control

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

    async def _on_key(self, event: events.Key) -> None:
        """Override TextArea's key handling to intercept Enter/Shift+Enter"""
        # Handle Ctrl+C - copy if selection, otherwise quit app
        if event.key == "ctrl+c":
            # Check if there's a selection to copy
            if self.selected_text:
                # Let default copy behavior happen
                await super()._on_key(event)
                return
            else:
                # No selection, quit the app directly
                self.app.exit()
                return

        # Handle Enter - submit message
        if event.key == "enter":
            event.prevent_default()
            event.stop()
            self.action_submit_prompt()
            return

        # Handle Shift+Enter - insert newline (works in Kitty terminal)
        if event.key == "shift+enter":
            event.prevent_default()
            event.stop()
            self.action_insert_newline()
            return

        # Handle cursor escaping
        if self.cursor_location == UIConfig.CURSOR_TOP_POSITION and event.key == "up":
            # print("DEBUG: Cursor at (0,0), sending CursorEscapingTop")
            event.prevent_default()
            self.post_message(self.CursorEscapingTop())
            event.stop()
            return
        elif self.cursor_at_end_of_text and event.key == "down":
            # print(f"DEBUG: Cursor at end, sending CursorEscapingBottom")
            event.prevent_default()
            self.post_message(self.CursorEscapingBottom())
            event.stop()
            return

        # For all other keys, use TextArea's default handling
        await super()._on_key(event)

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
        # Get current cursor position
        row, col = self.cursor_location
        lines = self.text.split("\n") if self.text else [""]

        # Insert newline at cursor position
        if row < len(lines):
            line = lines[row]
            # Split the line at cursor position
            before = line[:col]
            after = line[col:]
            # Replace current line with before part and add after part as new line
            lines[row] = before
            lines.insert(row + 1, after)
            # Update text
            self.text = "\n".join(lines)
            # Move cursor to beginning of next line
            self.cursor_location = (row + 1, 0)
        else:
            # Cursor beyond text, just append newline
            self.text = self.text + "\n"
            self.cursor_location = (row + 1, 0)
