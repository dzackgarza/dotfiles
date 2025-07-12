#!/usr/bin/env python3
"""Demo showing real live block updates"""

from textual.app import App, ComposeResult
from textual.widgets import Button
from textual.containers import Vertical, Horizontal

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.sacred_timeline import timeline
from src.core.response_generator import ResponseGenerator
from src.core.async_input_processor import AsyncInputProcessor
from src.ui.timeline_controller import TimelineViewController
from src.widgets.timeline import TimelineView


class LiveUpdatesDemoApp(App):
    """Demo app showing live block updates in action"""

    CSS = """
    #demo-controls {
        height: 3;
        margin-bottom: 1;
    }

    Button {
        margin: 0 1;
    }
    """

    def __init__(self):
        super().__init__()

        # Initialize components
        self.response_gen = ResponseGenerator(app=self)
        self.async_processor = AsyncInputProcessor(
            timeline, self.response_gen, app=self
        )

        self.timeline_view = None
        self.timeline_controller = None

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal(id="demo-controls"):
                yield Button("Quick Query", id="quick", variant="primary")
                yield Button("Complex Query", id="complex", variant="success")
                yield Button("Clear Timeline", id="clear", variant="warning")

            yield TimelineView(id="timeline")

    def on_mount(self):
        # Set up timeline
        self.timeline_view = self.query_one("#timeline", TimelineView)
        self.timeline_controller = TimelineViewController(self.timeline_view)
        timeline.add_observer(self.timeline_controller)

        # Add welcome
        timeline.add_block(
            role="system",
            content="**Live Updates Demo**\n\nClick the buttons to see real-time cognition processing!",
        )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quick":
            await self._process_query("What is 2+2?")
        elif event.button.id == "complex":
            await self._process_query("Explain quantum computing in simple terms")
        elif event.button.id == "clear":
            timeline.clear_timeline()
            self.timeline_view.clear_timeline()
            timeline.add_block(
                role="system", content="Timeline cleared. Try another query!"
            )

    async def _process_query(self, query: str) -> None:
        """Process a query with live updates"""
        # Disable buttons during processing
        for button in self.query(Button):
            button.disabled = True

        try:
            await self.async_processor.process_user_input_async(query)
        finally:
            # Re-enable buttons
            for button in self.query(Button):
                button.disabled = False


def main():
    app = LiveUpdatesDemoApp()
    app.run()


if __name__ == "__main__":
    main()
