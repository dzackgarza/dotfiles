"""
Enhanced Demo with Performance Monitoring and UX Polish

Demonstrates the complete live block system with performance
monitoring, user controls, and polished interactions.
"""

import asyncio
from textual.app import App
from textual.containers import Vertical, Horizontal
from textual.widgets import (
    Header,
    Footer,
    Static,
    Button,
    ProgressBar,
    Switch,
)
from textual.screen import Screen
from textual.timer import Timer

from ..widgets.live_block_widget import LiveBlockManagerWidget, BlockTransitionWidget
from ..core.mock_scenarios import MockScenarioGenerator
from ..core.performance_monitor import OptimizedLiveBlockManager


class EnhancedDemoScreen(Screen):
    """Enhanced demo screen with performance monitoring and controls."""

    BINDINGS = [
        ("1", "quick_demo", "Quick"),
        ("2", "coding_demo", "Coding"),
        ("3", "debug_demo", "Debug"),
        ("4", "research_demo", "Research"),
        ("5", "complex_demo", "Complex"),
        ("p", "toggle_performance", "Performance"),
        ("s", "settings", "Settings"),
        ("r", "reset_demo", "Reset"),
        ("q", "quit", "Quit"),
    ]

    CSS = """
    EnhancedDemoScreen {
        background: $surface;
    }

    .main-container {
        height: 100%;
        width: 100%;
        padding: 1;
    }

    .left-panel {
        width: 75%;
        height: 100%;
    }

    .right-panel {
        width: 25%;
        height: 100%;
        margin-left: 1;
    }

    .control-section {
        height: 15;
        border: round $primary;
        padding: 1;
        margin-bottom: 1;
    }

    .demo-area {
        height: auto;
        border: round $accent;
        padding: 1;
    }

    .performance-panel {
        height: 20;
        border: round $warning;
        padding: 1;
        margin-bottom: 1;
    }

    .settings-panel {
        height: 15;
        border: round $secondary;
        padding: 1;
        margin-bottom: 1;
    }

    .status-panel {
        height: 10;
        border: round $success;
        padding: 1;
    }

    .title {
        text-align: center;
        color: $primary;
        text-style: bold;
        margin-bottom: 1;
    }

    .section-title {
        color: $accent;
        text-style: bold;
        margin-bottom: 1;
    }

    .metric {
        color: $text;
        margin-bottom: 1;
    }

    .warning {
        color: $warning;
        text-style: bold;
    }

    .good {
        color: $success;
    }

    .controls-grid {
        layout: grid;
        grid-size: 2 3;
        grid-gutter: 1;
        margin-bottom: 1;
    }

    .setting-item {
        margin-bottom: 1;
    }
    """

    def __init__(self):
        super().__init__()
        self.demo_manager = OptimizedLiveBlockManager()
        self.scenario_generator = MockScenarioGenerator(self.demo_manager)
        self.running_demo = False
        self.performance_visible = True
        self.auto_inscribe = True
        self.animation_speed = "normal"

        # Performance monitoring timer
        self.performance_timer: Timer = None

    def compose(self):
        """Compose the enhanced demo screen."""
        yield Header(show_clock=True, title="Live Block System - Enhanced Demo")

        with Horizontal(classes="main-container"):
            # Left panel - main demo area
            with Vertical(classes="left-panel"):
                # Control section
                with Vertical(classes="control-section"):
                    yield Static("🎭 Enhanced Sacred Timeline Demo", classes="title")

                    with Horizontal(classes="controls-grid"):
                        yield Button(
                            "Quick Question", id="btn_quick", variant="success"
                        )
                        yield Button(
                            "Coding Session", id="btn_coding", variant="primary"
                        )
                        yield Button("Debug Session", id="btn_debug", variant="warning")
                        yield Button(
                            "Research Query", id="btn_research", variant="default"
                        )
                        yield Button(
                            "Complex Analysis", id="btn_complex", variant="error"
                        )
                        yield Button("Reset Demo", id="btn_reset", variant="default")

                # Demo area
                with Vertical(classes="demo-area"):
                    yield LiveBlockManagerWidget(self.demo_manager, id="manager_widget")
                    yield BlockTransitionWidget(id="transition_widget")

            # Right panel - monitoring and controls
            with Vertical(classes="right-panel"):
                # Performance panel
                with Vertical(classes="performance-panel", id="performance_panel"):
                    yield Static("📊 Performance Monitor", classes="section-title")
                    yield Static(
                        "Status: Good", id="perf_status", classes="metric good"
                    )
                    yield Static("Memory: 0.0 MB", id="perf_memory", classes="metric")
                    yield Static("Active Blocks: 0", id="perf_blocks", classes="metric")
                    yield Static(
                        "Update Rate: 0 Hz", id="perf_updates", classes="metric"
                    )
                    yield ProgressBar(total=100, show_eta=False, id="memory_progress")
                    yield Static("No warnings", id="perf_warnings", classes="metric")

                # Settings panel
                with Vertical(classes="settings-panel"):
                    yield Static("⚙️ Settings", classes="section-title")

                    with Horizontal(classes="setting-item"):
                        yield Static("Auto-inscribe: ")
                        yield Switch(value=True, id="auto_inscribe_switch")

                    with Horizontal(classes="setting-item"):
                        yield Static("Performance: ")
                        yield Switch(value=True, id="performance_switch")

                    yield Static(
                        "Animation: Normal", id="animation_setting", classes="metric"
                    )
                    yield Button(
                        "Apply Optimizations", id="btn_optimize", variant="success"
                    )

                # Status panel
                with Vertical(classes="status-panel"):
                    yield Static("🎯 Status", classes="section-title")
                    yield Static(
                        "Ready - Select a scenario to begin",
                        id="status_text",
                        classes="metric",
                    )

        yield Footer()

    def on_mount(self) -> None:
        """Initialize the enhanced demo."""
        # Start performance monitoring
        self.performance_timer = self.set_interval(2.0, self._update_performance)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id

        if not self.running_demo:
            if button_id == "btn_quick":
                asyncio.create_task(self._run_scenario("quick_question"))
            elif button_id == "btn_coding":
                asyncio.create_task(self._run_scenario("coding_session"))
            elif button_id == "btn_debug":
                asyncio.create_task(self._run_scenario("debugging_session"))
            elif button_id == "btn_research":
                asyncio.create_task(self._run_scenario("research_query"))
            elif button_id == "btn_complex":
                asyncio.create_task(self._run_scenario("complex_analysis"))

        if button_id == "btn_reset":
            self._reset_demo()
        elif button_id == "btn_optimize":
            self._apply_optimizations()

    def on_switch_changed(self, event: Switch.Changed) -> None:
        """Handle switch changes."""
        switch_id = event.switch.id

        if switch_id == "auto_inscribe_switch":
            self.auto_inscribe = event.value
            self._update_status(
                f"Auto-inscribe: {'Enabled' if event.value else 'Disabled'}"
            )
        elif switch_id == "performance_switch":
            self.performance_visible = event.value
            panel = self.query_one("#performance_panel")
            panel.display = event.value

    async def _run_scenario(self, scenario_type: str) -> None:
        """Run a scenario with enhanced monitoring."""
        if self.running_demo:
            return

        self.running_demo = True
        self._update_status(f"Running {scenario_type.replace('_', ' ')} scenario...")

        try:
            # Show transition
            transition_widget = self.query_one(
                "#transition_widget", BlockTransitionWidget
            )
            from ..core.live_blocks import BlockState

            transition_widget.show_transition(BlockState.LIVE, BlockState.LIVE)

            # Generate scenario
            blocks = await self.scenario_generator.generate_scenario(scenario_type)

            self._update_status(f"Scenario completed! Generated {len(blocks)} blocks")

            # Auto-inscribe if enabled
            if self.auto_inscribe:
                await asyncio.sleep(3.0)
                await self._auto_inscribe_blocks()

        except Exception as e:
            self._update_status(f"Error: {str(e)}")
        finally:
            self.running_demo = False

    async def _auto_inscribe_blocks(self) -> None:
        """Auto-inscribe all live blocks."""
        transition_widget = self.query_one("#transition_widget", BlockTransitionWidget)

        live_blocks = list(self.demo_manager.live_blocks.keys())
        if live_blocks:
            from ..core.live_blocks import BlockState

            transition_widget.show_transition(BlockState.LIVE, BlockState.INSCRIBED)

            for block_id in live_blocks:
                self.demo_manager.inscribe_block(block_id)
                await asyncio.sleep(0.1)

            self._update_status("All blocks inscribed to Sacred Timeline")

    def _update_performance(self) -> None:
        """Update performance display."""
        if not self.performance_visible:
            return

        try:
            status = self.demo_manager.get_performance_status()

            # Update status
            status_text = status["status"].upper()
            status_widget = self.query_one("#perf_status", Static)
            status_widget.remove_class("good", "warning", "error")

            if status["status"] == "good":
                status_widget.add_class("good")
            elif status["status"] in ["caution", "warning"]:
                status_widget.add_class("warning")
            else:
                status_widget.add_class("error")

            status_widget.update(f"Status: {status_text}")

            # Update metrics
            metrics = status["metrics"]
            self.query_one("#perf_memory", Static).update(
                f"Memory: {metrics['average_memory_mb']} MB"
            )
            self.query_one("#perf_blocks", Static).update(
                f"Active Blocks: {int(metrics['average_active_blocks'])}"
            )
            self.query_one("#perf_updates", Static).update(
                f"Update Rate: {metrics['average_update_frequency']:.1f} Hz"
            )

            # Update memory progress bar
            memory_progress = self.query_one("#memory_progress", ProgressBar)
            memory_percent = min(100, (metrics["average_memory_mb"] / 100) * 100)
            memory_progress.progress = memory_percent

            # Update warnings
            warnings = status["warnings"]
            if warnings["total"] > 0:
                recent_warning = warnings["recent"][-1] if warnings["recent"] else None
                if recent_warning:
                    warning_text = f"⚠️ {recent_warning['message']}"
                    self.query_one("#perf_warnings", Static).update(warning_text)
                    self.query_one("#perf_warnings", Static).add_class("warning")
                else:
                    self.query_one("#perf_warnings", Static).update("No warnings")
                    self.query_one("#perf_warnings", Static).remove_class("warning")
            else:
                self.query_one("#perf_warnings", Static).update("No warnings")
                self.query_one("#perf_warnings", Static).remove_class("warning")

        except Exception:
            # Handle performance monitoring errors gracefully
            pass

    def _apply_optimizations(self) -> None:
        """Apply performance optimizations."""
        try:
            optimizations = ["memory_cleanup", "throttle_updates", "callback_batching"]
            applied = 0

            for opt in optimizations:
                if self.demo_manager.performance_monitor.apply_optimization(opt):
                    applied += 1

            self._update_status(f"Applied {applied} optimizations")

        except Exception as e:
            self._update_status(f"Optimization error: {str(e)}")

    def _reset_demo(self) -> None:
        """Reset the demo."""
        # Stop all simulations
        self.demo_manager.stop_all_simulations()

        # Inscribe remaining blocks
        live_block_ids = list(self.demo_manager.live_blocks.keys())
        for block_id in live_block_ids:
            self.demo_manager.inscribe_block(block_id)

        self.running_demo = False
        self._update_status("Demo reset - Ready for new scenario")

    def _update_status(self, message: str) -> None:
        """Update status message."""
        self.query_one("#status_text", Static).update(message)

    def action_toggle_performance(self) -> None:
        """Toggle performance panel visibility."""
        self.performance_visible = not self.performance_visible
        self.query_one("#performance_panel").display = self.performance_visible
        switch = self.query_one("#performance_switch", Switch)
        switch.value = self.performance_visible

    def action_settings(self) -> None:
        """Show settings (placeholder for future enhancement)."""
        self._update_status("Settings panel - Configure demo behavior")

    def action_quit(self) -> None:
        """Quit the enhanced demo."""
        if self.performance_timer:
            self.performance_timer.stop()
        self.app.exit()


class EnhancedDemoApp(App):
    """Enhanced demo application with full feature set."""

    TITLE = "Live Block System - Enhanced Demo"
    SUB_TITLE = "Sacred Timeline with Performance Monitoring"

    CSS = """
    App {
        background: $surface;
    }
    """

    def on_mount(self) -> None:
        """Initialize the enhanced demo app."""
        self.push_screen(EnhancedDemoScreen())


def main():
    """Run the enhanced demo."""
    app = EnhancedDemoApp()
    app.run()


if __name__ == "__main__":
    main()
