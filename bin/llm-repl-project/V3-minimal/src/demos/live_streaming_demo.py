#!/usr/bin/env python3
"""
Live Streaming Demo

Demonstrates the 5 user-visible behaviors implemented in the live-inscribed-block-system:
1. Real-time streaming text (character by character)
2. Live token counters (incrementing visually)
3. Animated progress indicators (smooth 0-100%)
4. Live → Inscribed transitions (visual animation)
5. Nested sub-block streaming (sub-modules with own counters)
"""

import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Button, Static
from textual.containers import Vertical, Horizontal

from ..core.live_blocks import LiveBlockManager
from ..widgets.live_block_widget import LiveBlockWidget


class LiveStreamingDemoApp(App):
    """Demo app showcasing real streaming behaviors."""

    CSS = """
    Screen {
        background: $background;
    }

    #demo-controls {
        height: 4;
        margin-bottom: 1;
        padding: 1;
        background: $primary 20%;
        border: round $primary;
    }

    #demo-area {
        height: auto;
        padding: 1;
    }

    Button {
        margin: 0 1;
    }

    .demo-title {
        text-style: bold;
        color: $accent;
        text-align: center;
        margin-bottom: 1;
    }
    """

    def __init__(self):
        super().__init__()
        self.live_manager = LiveBlockManager()
        self.active_widgets = []

    def compose(self) -> ComposeResult:
        yield Static(
            "🧠 Live Streaming Demo - Real-time AI Processing", classes="demo-title"
        )

        with Horizontal(id="demo-controls"):
            yield Button("1. Streaming Text Demo", id="demo1", variant="success")
            yield Button("2. Cognition Pipeline", id="demo2", variant="primary")
            yield Button("3. Assistant Response", id="demo3", variant="warning")
            yield Button("4. Transition Demo", id="demo4", variant="error")
            yield Button("Clear All", id="clear", variant="default")

        with Vertical(id="demo-area"):
            pass

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle demo button presses."""
        if event.button.id == "demo1":
            await self._demo_streaming_text()
        elif event.button.id == "demo2":
            await self._demo_cognition_pipeline()
        elif event.button.id == "demo3":
            await self._demo_assistant_response()
        elif event.button.id == "demo4":
            await self._demo_transition()
        elif event.button.id == "clear":
            await self._clear_demos()

    async def _demo_streaming_text(self) -> None:
        """Demo 1: Character-by-character streaming text."""
        block = self.live_manager.create_live_block("demo", "")
        widget = LiveBlockWidget(block)

        await self.query_one("#demo-area").mount(widget)
        self.active_widgets.append(widget)

        # Stream content character by character
        demo_text = "🎯 Demonstrating character-by-character streaming...\n\nYou should see this text appear gradually, not all at once!\n\nEach character appears with a small delay to simulate real-time AI generation."
        await block.stream_content(demo_text, char_delay=0.05)

    async def _demo_cognition_pipeline(self) -> None:
        """Demo 2: Full cognition pipeline with nested sub-blocks."""
        block = self.live_manager.create_live_block("cognition", "")
        widget = LiveBlockWidget(block)

        await self.query_one("#demo-area").mount(widget)
        self.active_widgets.append(widget)

        # Run full cognition simulation with nested streaming
        await block.start_mock_simulation("cognition")

    async def _demo_assistant_response(self) -> None:
        """Demo 3: Assistant response with token animation."""
        block = self.live_manager.create_live_block("assistant", "")
        widget = LiveBlockWidget(block)

        await self.query_one("#demo-area").mount(widget)
        self.active_widgets.append(widget)

        # Run assistant response with streaming
        await block.start_mock_simulation("assistant_response")

    async def _demo_transition(self) -> None:
        """Demo 4: Live → Inscribed transition animation."""
        block = self.live_manager.create_live_block("transition", "")
        widget = LiveBlockWidget(block)

        await self.query_one("#demo-area").mount(widget)
        self.active_widgets.append(widget)

        # Quick simulation followed by transition
        await block.stream_content("🔄 Preparing for inscription...", char_delay=0.03)
        await block.animate_progress(1.0, duration=1.0)
        await block.animate_tokens(10, 25)

        # Animate the transition to inscribed
        await block.to_inscribed_block()

        # Show transition completed
        await asyncio.sleep(0.5)

    async def _clear_demos(self) -> None:
        """Clear all demo widgets."""
        demo_area = self.query_one("#demo-area")
        await demo_area.remove_children()
        self.active_widgets.clear()


def main():
    """Run the live streaming demo."""
    app = LiveStreamingDemoApp()
    app.run()


if __name__ == "__main__":
    main()
