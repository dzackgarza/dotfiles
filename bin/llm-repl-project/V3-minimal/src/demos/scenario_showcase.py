"""
Scenario Showcase Demo

Demonstrates various mock scenarios for the live block system.
Shows realistic conversation types with different complexities.
"""

import asyncio
from textual.app import App
from textual.containers import Vertical
from textual.widgets import Header, Footer, Static
from textual.screen import Screen

from ..widgets.live_block_widget import LiveBlockManagerWidget, BlockTransitionWidget
from ..core.live_blocks import LiveBlockManager
from ..core.mock_scenarios import MockScenarioGenerator


class ScenarioShowcaseScreen(Screen):
    """Main screen for scenario showcase."""

    BINDINGS = [
        ("1", "quick_demo", "Quick Question"),
        ("2", "coding_demo", "Coding Session"),
        ("3", "debug_demo", "Debugging"),
        ("4", "research_demo", "Research"),
        ("5", "complex_demo", "Complex Analysis"),
        ("r", "reset_demo", "Reset"),
        ("q", "quit", "Quit"),
    ]

    CSS = """
    ScenarioShowcaseScreen {
        background: $surface;
    }

    .showcase-container {
        height: 100%;
        width: 100%;
        padding: 1;
    }

    .control-panel {
        height: 12;
        border: round $primary;
        padding: 1;
        margin-bottom: 1;
    }

    .scenario-info {
        height: 6;
        border: round $accent;
        padding: 1;
        margin-bottom: 1;
    }

    .demo-area {
        height: auto;
        border: round $accent;
        padding: 1;
    }

    .title {
        text-align: center;
        color: $primary;
        text-style: bold;
        margin-bottom: 1;
    }

    .instructions {
        text-align: center;
        color: $text-muted;
        margin-bottom: 1;
    }

    .scenario-description {
        color: $text;
        margin-bottom: 1;
    }

    .status-bar {
        height: 4;
        border-top: solid $accent;
        padding: 1;
        text-align: center;
    }
    """

    def __init__(self):
        super().__init__()
        self.demo_manager = LiveBlockManager()
        self.scenario_generator = MockScenarioGenerator(self.demo_manager)
        self.current_scenario = None
        self.running_demo = False

    def compose(self):
        """Compose the showcase screen."""
        yield Header(show_clock=True)

        with Vertical(classes="showcase-container"):
            # Control panel
            with Vertical(classes="control-panel"):
                yield Static(
                    "🎭 Mock Scenario Showcase - Sacred Timeline Demonstrations",
                    classes="title",
                )
                yield Static(
                    "Press: [bold cyan]1[/] Quick | [bold green]2[/] Coding | [bold yellow]3[/] Debug | [bold blue]4[/] Research | [bold magenta]5[/] Complex",
                    classes="instructions",
                )
                yield Static(
                    "[bold red]R[/] Reset | [bold white]Q[/] Quit",
                    classes="instructions",
                )

            # Scenario info panel
            with Vertical(classes="scenario-info"):
                yield Static(
                    "Select a scenario to see realistic Sacred Timeline interactions",
                    classes="scenario-description",
                    id="scenario_description",
                )

            # Demo area
            with Vertical(classes="demo-area"):
                yield LiveBlockManagerWidget(self.demo_manager, id="manager_widget")
                yield BlockTransitionWidget(id="transition_widget")

            # Status bar
            yield Static(
                "Ready - Choose a scenario to begin demonstration",
                classes="status-bar",
                id="status_bar",
            )

        yield Footer()

    def action_quick_demo(self) -> None:
        """Start quick question demo."""
        if not self.running_demo:
            asyncio.create_task(self._run_scenario_demo("quick_question"))

    def action_coding_demo(self) -> None:
        """Start coding session demo."""
        if not self.running_demo:
            asyncio.create_task(self._run_scenario_demo("coding_session"))

    def action_debug_demo(self) -> None:
        """Start debugging demo."""
        if not self.running_demo:
            asyncio.create_task(self._run_scenario_demo("debugging_session"))

    def action_research_demo(self) -> None:
        """Start research demo."""
        if not self.running_demo:
            asyncio.create_task(self._run_scenario_demo("research_query"))

    def action_complex_demo(self) -> None:
        """Start complex analysis demo."""
        if not self.running_demo:
            asyncio.create_task(self._run_scenario_demo("complex_analysis"))

    def action_reset_demo(self) -> None:
        """Reset current demo."""
        self._reset_demo()

    def action_quit(self) -> None:
        """Quit the showcase."""
        self.app.exit()

    async def _run_scenario_demo(self, scenario_type: str) -> None:
        """Run a specific scenario demonstration."""
        if self.running_demo:
            return

        self.running_demo = True
        self.current_scenario = scenario_type

        # Update UI elements
        status_bar = self.query_one("#status_bar", Static)
        description_widget = self.query_one("#scenario_description", Static)
        transition_widget = self.query_one("#transition_widget", BlockTransitionWidget)

        try:
            # Get scenario info and update description
            scenario_info = self.scenario_generator.get_scenario_info(scenario_type)
            description_text = f"**{scenario_type.replace('_', ' ').title()}**\n"
            description_text += f"Description: {scenario_info['description']}\n"
            description_text += f"Complexity: {scenario_info['complexity']} | Duration: {scenario_info['duration']}"
            description_widget.update(description_text)

            status_bar.update(
                f"🎬 Running {scenario_type.replace('_', ' ')} scenario..."
            )

            # Show initial transition
            from ..core.live_blocks import BlockState

            transition_widget.show_transition(BlockState.LIVE, BlockState.LIVE)

            # Generate and execute scenario
            blocks = await self.scenario_generator.generate_scenario(scenario_type)

            # Show completion
            status_bar.update(
                f"✅ {scenario_type.replace('_', ' ').title()} scenario completed! ({len(blocks)} blocks generated)"
            )

            # Auto-inscribe blocks after a delay
            await asyncio.sleep(3.0)
            await self._inscribe_all_blocks()

            status_bar.update(
                "📜 Scenario inscribed to Sacred Timeline. Ready for next demonstration."
            )

        except Exception as e:
            status_bar.update(f"❌ Error running scenario: {str(e)}")
        finally:
            self.running_demo = False

    async def _inscribe_all_blocks(self) -> None:
        """Inscribe all live blocks to the timeline."""
        transition_widget = self.query_one("#transition_widget", BlockTransitionWidget)

        live_blocks = list(self.demo_manager.live_blocks.keys())

        if live_blocks:
            from ..core.live_blocks import BlockState

            transition_widget.show_transition(BlockState.LIVE, BlockState.INSCRIBED)

            for block_id in live_blocks:
                inscribed = self.demo_manager.inscribe_block(block_id)
                if inscribed:
                    await asyncio.sleep(0.1)  # Small delay between inscriptions

    def _reset_demo(self) -> None:
        """Reset the current demonstration."""
        status_bar = self.query_one("#status_bar", Static)
        description_widget = self.query_one("#scenario_description", Static)

        # Stop all simulations
        self.demo_manager.stop_all_simulations()

        # Inscribe any remaining live blocks
        live_block_ids = list(self.demo_manager.live_blocks.keys())
        for block_id in live_block_ids:
            self.demo_manager.inscribe_block(block_id)

        # Reset UI
        description_widget.update(
            "Select a scenario to see realistic Sacred Timeline interactions"
        )
        status_bar.update("🔄 Demo reset! Ready for new scenario demonstration.")

        self.current_scenario = None
        self.running_demo = False


class ScenarioShowcaseApp(App):
    """Main app for scenario showcase."""

    TITLE = "Mock Scenario Showcase"
    SUB_TITLE = "Sacred Timeline Demonstrations"

    def on_mount(self) -> None:
        """Initialize the showcase app."""
        self.push_screen(ScenarioShowcaseScreen())


def main():
    """Run the scenario showcase."""
    app = ScenarioShowcaseApp()
    app.run()


if __name__ == "__main__":
    main()
