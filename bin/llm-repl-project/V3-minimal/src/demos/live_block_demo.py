"""
Live Block Demo Application

Demonstrates the live block system with visual widgets.
Shows real-time updates, state transitions, and nested sub-blocks.
"""

import asyncio
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Footer, Static
from textual.screen import Screen

from ..widgets.live_block_widget import (
    LiveBlockManagerWidget,
    BlockTransitionWidget,
)
from ..core.live_blocks import LiveBlockManager


class LiveBlockDemoScreen(Screen):
    """Main demo screen for live blocks."""

    BINDINGS = [
        ("c", "demo_cognition", "Cognition Demo"),
        ("a", "demo_assistant", "Assistant Demo"),
        ("t", "demo_tool", "Tool Demo"),
        ("r", "reset_demo", "Reset"),
        ("q", "quit", "Quit"),
    ]

    CSS = """
    LiveBlockDemoScreen {
        background: $surface;
    }

    .demo-container {
        height: 100%;
        width: 100%;
        padding: 1;
    }

    .control-panel {
        height: 8;
        border: round $primary;
        padding: 1;
        margin-bottom: 1;
    }

    .demo-area {
        height: auto;
        border: round $accent;
        padding: 1;
    }

    .instructions {
        text-align: center;
        color: $text-muted;
        margin-bottom: 1;
    }

    .status-bar {
        height: 3;
        border-top: solid $accent;
        padding: 1;
        text-align: center;
    }
    """

    def __init__(self):
        super().__init__()
        self.demo_manager = LiveBlockManager()
        self.active_demos = []

    def compose(self) -> ComposeResult:
        """Compose the demo screen."""
        yield Header(show_clock=True)

        with Vertical(classes="demo-container"):
            # Control panel
            with Vertical(classes="control-panel"):
                yield Static(
                    "🧠 Live Block System Demo - Sacred Timeline Proof of Concept",
                    classes="instructions",
                )
                yield Static(
                    "Press: [bold cyan]C[/] Cognition | [bold green]A[/] Assistant | [bold yellow]T[/] Tool | [bold red]R[/] Reset | [bold white]Q[/] Quit",
                    classes="instructions",
                )

            # Demo area
            with Vertical(classes="demo-area"):
                yield LiveBlockManagerWidget(self.demo_manager, id="manager_widget")
                yield BlockTransitionWidget(id="transition_widget")

            # Status bar
            yield Static(
                "Ready - Start a demo to see live blocks in action!",
                classes="status-bar",
                id="status_bar",
            )

        yield Footer()

    def action_demo_cognition(self) -> None:
        """Start cognition pipeline demo."""
        asyncio.create_task(self._run_cognition_demo())

    def action_demo_assistant(self) -> None:
        """Start assistant response demo."""
        asyncio.create_task(self._run_assistant_demo())

    def action_demo_tool(self) -> None:
        """Start tool execution demo."""
        asyncio.create_task(self._run_tool_demo())

    def action_reset_demo(self) -> None:
        """Reset all demos."""
        self._reset_all_demos()

    def action_quit(self) -> None:
        """Quit the demo."""
        self.app.exit()

    async def _run_cognition_demo(self) -> None:
        """Run a cognition pipeline demo."""
        status_bar = self.query_one("#status_bar", Static)
        transition_widget = self.query_one("#transition_widget", BlockTransitionWidget)

        status_bar.update("🧠 Starting cognition pipeline demo...")

        # Create cognition block
        block = self.demo_manager.create_live_block(
            "cognition", "🧠 Initializing cognition pipeline..."
        )

        self.active_demos.append(block)

        # Show transition
        from ..core.live_blocks import BlockState

        transition_widget.show_transition(BlockState.LIVE, BlockState.LIVE)

        # Run simulation
        await block.start_mock_simulation("cognition")

        status_bar.update("🧠 Cognition pipeline completed! Inscribing to timeline...")

        # Wait a moment, then inscribe
        await asyncio.sleep(2.0)
        transition_widget.show_transition(BlockState.LIVE, BlockState.INSCRIBED)

        inscribed = self.demo_manager.inscribe_block(block.id)
        if inscribed:
            status_bar.update(
                f"✅ Cognition block inscribed! ({len(inscribed.metadata.get('sub_blocks', []))} sub-modules)"
            )

        self.active_demos.remove(block)

    async def _run_assistant_demo(self) -> None:
        """Run an assistant response demo."""
        status_bar = self.query_one("#status_bar", Static)
        transition_widget = self.query_one("#transition_widget", BlockTransitionWidget)

        status_bar.update("🤖 Starting assistant response demo...")

        # Create assistant block
        block = self.demo_manager.create_live_block(
            "assistant", "🤖 Preparing response..."
        )

        self.active_demos.append(block)

        # Show transition
        from ..core.live_blocks import BlockState

        transition_widget.show_transition(BlockState.LIVE, BlockState.LIVE)

        # Run simulation
        await block.start_mock_simulation("assistant_response")

        status_bar.update("🤖 Assistant response completed! Inscribing to timeline...")

        await asyncio.sleep(1.0)
        transition_widget.show_transition(BlockState.LIVE, BlockState.INSCRIBED)

        inscribed = self.demo_manager.inscribe_block(block.id)
        if inscribed:
            status_bar.update(
                f"✅ Assistant block inscribed! ({inscribed.metadata.get('tokens_output', 0)} tokens)"
            )

        self.active_demos.remove(block)

    async def _run_tool_demo(self) -> None:
        """Run a tool execution demo."""
        status_bar = self.query_one("#status_bar", Static)
        transition_widget = self.query_one("#transition_widget", BlockTransitionWidget)

        status_bar.update("🛠️ Starting tool execution demo...")

        # Create tool block
        block = self.demo_manager.create_live_block("tool", "🛠️ Initializing tool...")

        self.active_demos.append(block)

        # Show transition
        from ..core.live_blocks import BlockState

        transition_widget.show_transition(BlockState.LIVE, BlockState.LIVE)

        # Run simulation
        await block.start_mock_simulation("tool_execution")

        status_bar.update("🛠️ Tool execution completed! Inscribing to timeline...")

        await asyncio.sleep(1.0)
        transition_widget.show_transition(BlockState.LIVE, BlockState.INSCRIBED)

        inscribed = self.demo_manager.inscribe_block(block.id)
        if inscribed:
            status_bar.update("✅ Tool block inscribed! Execution successful")

        self.active_demos.remove(block)

    def _reset_all_demos(self) -> None:
        """Reset all active demos."""
        status_bar = self.query_one("#status_bar", Static)

        # Stop all simulations
        self.demo_manager.stop_all_simulations()

        # Clear active demos
        for block in self.active_demos[:]:
            if block.id in self.demo_manager.live_blocks:
                self.demo_manager.inscribe_block(block.id)

        self.active_demos.clear()

        status_bar.update("🔄 All demos reset! Ready for new demonstrations.")


class LiveBlockDemoApp(App):
    """Main demo application for live blocks."""

    TITLE = "Live Block System Demo"
    SUB_TITLE = "Sacred Timeline Proof of Concept"

    CSS = """
    /* Global app styling */
    App {
        background: $surface;
    }
    """

    def on_mount(self) -> None:
        """Initialize the demo app."""
        self.push_screen(LiveBlockDemoScreen())


def main():
    """Run the live block demo."""
    app = LiveBlockDemoApp()
    app.run()


if __name__ == "__main__":
    main()
