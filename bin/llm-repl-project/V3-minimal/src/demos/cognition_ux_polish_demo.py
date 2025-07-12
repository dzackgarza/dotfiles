"""
Cognition UX Polish Demo

Demonstrates polished user experience features for the mock cognition pipeline
including smooth animations, progress indicators, and responsive feedback.
"""

import asyncio
from datetime import datetime
from typing import Dict, Any
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.live import Live

from src.core.mock_scenarios import (
    CognitionScenarioGenerator,
    EnhancedMockCognitionPlugin,
)
from src.core.live_blocks import AnimationRates


class CognitionUXPolishDemo:
    """Polished UX demonstration for cognition pipeline."""

    def __init__(self):
        self.console = Console()
        self.scenario_generator = CognitionScenarioGenerator()

    async def run_polished_showcase(self) -> None:
        """Run a polished showcase with enhanced UX features."""

        self.console.print(
            Panel.fit(
                "[bold cyan]🧠 Enhanced Cognition Pipeline Showcase[/bold cyan]\n"
                "[dim]Demonstrating polished UX with realistic AI cognition simulation[/dim]",
                border_style="cyan",
            )
        )

        # Demo 1: Progressive Enhancement
        await self._demo_progressive_enhancement()

        # Demo 2: Real-time Metrics Dashboard
        await self._demo_realtime_dashboard()

        # Demo 3: Parallel Pipeline Visualization
        await self._demo_parallel_visualization()

        # Demo 4: Interactive Pipeline Control
        await self._demo_interactive_control()

    async def _demo_progressive_enhancement(self) -> None:
        """Demonstrate progressive enhancement of cognition display."""

        self.console.print(
            "\n[bold yellow]📈 Progressive Enhancement Demo[/bold yellow]"
        )

        query = "Implement a machine learning model for real-time fraud detection"
        plugin = self.scenario_generator.create_coding_scenario()

        # Create progress display
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=self.console,
            transient=True,
        ) as progress:

            main_task = progress.add_task("🧠 Cognition Pipeline", total=100)
            sub_tasks = {}

            # Add callback to track progress
            def update_progress(plugin_instance):
                status = plugin_instance.get_current_status()
                progress.update(main_task, completed=status["progress"] * 100)

                # Update sub-task progress
                for sub_module in plugin_instance.sub_modules:
                    if sub_module.step.name not in sub_tasks:
                        sub_tasks[sub_module.step.name] = progress.add_task(
                            f"{sub_module.step.icon} {sub_module.step.name}", total=100
                        )

                    if sub_module.state == "running":
                        progress.update(
                            sub_tasks[sub_module.step.name],
                            completed=sub_module.progress * 100,
                        )
                    elif sub_module.state == "completed":
                        progress.update(sub_tasks[sub_module.step.name], completed=100)

            plugin.add_update_callback(update_progress)

            # Execute pipeline
            result = await plugin.execute_cognition_pipeline(query)

        # Show final results with enhanced formatting
        self._display_enhanced_results(result, "Progressive Enhancement")

    async def _demo_realtime_dashboard(self) -> None:
        """Demonstrate real-time metrics dashboard."""

        self.console.print("\n[bold green]📊 Real-time Metrics Dashboard[/bold green]")

        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3),
        )

        layout["main"].split_row(Layout(name="left"), Layout(name="right"))

        # Initialize dashboard
        metrics_table = Table.grid(padding=1)
        metrics_table.add_column("Metric", style="cyan")
        metrics_table.add_column("Value", style="green")

        pipeline_status = Table.grid(padding=1)
        pipeline_status.add_column("Step", style="yellow")
        pipeline_status.add_column("Status", style="white")

        with Live(layout, console=self.console, screen=False, refresh_per_second=10):

            # Create plugin and start execution
            plugin = self.scenario_generator.create_debugging_scenario()
            query = "Debug distributed system race condition causing data corruption"

            # Update dashboard in real-time
            start_time = datetime.now()

            def update_dashboard(plugin_instance):
                status = plugin_instance.get_current_status()
                elapsed = (datetime.now() - start_time).total_seconds()

                # Update metrics
                metrics_table.rows.clear()
                metrics_table.add_row("🕐 Elapsed Time", f"{elapsed:.1f}s")
                metrics_table.add_row("🎯 Progress", f"{status['progress']:.0%}")
                metrics_table.add_row("🔢 Total Tokens", str(status["total_tokens"]))
                metrics_table.add_row(
                    "⚡ Steps Completed", str(len(status["completed_steps"]))
                )

                # Update pipeline status
                pipeline_status.rows.clear()
                for sub_module in plugin_instance.sub_modules:
                    state_icon = {
                        "pending": "⏳",
                        "running": "🔄",
                        "completed": "✅",
                        "failed": "❌",
                    }.get(sub_module.state, "❓")

                    pipeline_status.add_row(
                        f"{sub_module.step.icon} {sub_module.step.name}",
                        f"{state_icon} {sub_module.state.title()}",
                    )

                # Update layout
                layout["header"].update(
                    Panel(
                        "[bold cyan]🧠 Real-time Cognition Dashboard[/bold cyan]",
                        border_style="cyan",
                    )
                )
                layout["left"].update(Panel(metrics_table, title="📊 Metrics"))
                layout["right"].update(
                    Panel(pipeline_status, title="🔄 Pipeline Status")
                )
                layout["footer"].update(
                    Panel(f"[dim]Query: {query[:60]}...[/dim]", border_style="dim")
                )

            plugin.add_update_callback(update_dashboard)

            # Execute pipeline
            result = await plugin.execute_cognition_pipeline(query)

            # Final update
            update_dashboard(plugin)
            await AnimationRates.sleep(2)  # Show final state

        self._display_enhanced_results(result, "Real-time Dashboard")

    async def _demo_parallel_visualization(self) -> None:
        """Demonstrate parallel pipeline visualization."""

        self.console.print(
            "\n[bold magenta]🚀 Parallel Pipeline Visualization[/bold magenta]"
        )

        # Create multiple plugins for parallel execution
        scenarios = [
            (
                "🏗️ Architecture",
                "architectural_design",
                "Design microservices for autonomous vehicles",
            ),
            (
                "🔍 Research",
                "research_deep_dive",
                "Compare quantum vs classical cryptography",
            ),
            ("💻 Coding", "simple_coding", "Implement blockchain consensus algorithm"),
            ("🐛 Debug", "complex_debugging", "Fix memory leak in distributed cache"),
        ]

        # Create progress display for parallel execution
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console,
            transient=False,
        ) as progress:

            # Create tasks and plugins
            tasks = []
            plugins = []
            progress_tasks = {}

            for name, scenario_type, query in scenarios:
                plugin = EnhancedMockCognitionPlugin(scenario_type)
                task_id = progress.add_task(f"{name} Pipeline", total=100)

                def create_updater(task_id):
                    def update_progress(plugin_instance):
                        status = plugin_instance.get_current_status()
                        progress.update(task_id, completed=status["progress"] * 100)

                    return update_progress

                plugin.add_update_callback(create_updater(task_id))

                # Start execution
                task = asyncio.create_task(plugin.execute_cognition_pipeline(query))

                tasks.append(task)
                plugins.append(plugin)
                progress_tasks[name] = task_id

            # Wait for all to complete
            results = await asyncio.gather(*tasks)

        # Display parallel execution summary
        summary_table = Table(title="🚀 Parallel Execution Summary")
        summary_table.add_column("Pipeline", style="cyan")
        summary_table.add_column("Steps", style="yellow")
        summary_table.add_column("Tokens", style="green")
        summary_table.add_column("Duration", style="blue")
        summary_table.add_column("Confidence", style="magenta")

        for i, (name, _, _) in enumerate(scenarios):
            result = results[i]
            summary_table.add_row(
                name,
                str(result["total_steps"]),
                str(result["total_tokens"]),
                f"{result['total_duration']:.1f}s",
                f"{result['confidence']:.2f}",
            )

        self.console.print(summary_table)

    async def _demo_interactive_control(self) -> None:
        """Demonstrate interactive pipeline control features."""

        self.console.print("\n[bold red]🎮 Interactive Control Demo[/bold red]")

        # Create a sophisticated scenario
        plugin = EnhancedMockCognitionPlugin("architectural_design")
        query = "Design fault-tolerant distributed system for financial trading"

        # Show step-by-step execution with user control simulation
        self.console.print(
            "[dim]Simulating interactive control (automated for demo)[/dim]\n"
        )

        step_details = []

        def capture_step_details(plugin_instance):
            for sub_module in plugin_instance.sub_modules:
                if sub_module.state == "completed" and sub_module.result:
                    step_info = {
                        "name": sub_module.step.name,
                        "icon": sub_module.step.icon,
                        "content": sub_module.result.content,
                        "tokens": sub_module.result.tokens_used,
                        "duration": sub_module.result.duration_seconds,
                        "confidence": sub_module.result.confidence_score,
                    }
                    if step_info not in step_details:
                        step_details.append(step_info)

        plugin.add_update_callback(capture_step_details)

        # Execute with simulated pauses
        result = await plugin.execute_cognition_pipeline(query)

        # Display interactive-style results
        for i, step in enumerate(step_details):
            self.console.print(
                f"\n[bold cyan]Step {i+1}: {step['icon']} {step['name']}[/bold cyan]"
            )

            detail_panel = Panel(
                f"[white]{step['content'][:200]}...[/white]\n\n"
                f"[dim]Tokens: {step['tokens']} | "
                f"Duration: {step['duration']:.1f}s | "
                f"Confidence: {step['confidence']:.2f}[/dim]",
                border_style="blue",
            )
            self.console.print(detail_panel)

            # Simulate user review time
            await AnimationRates.sleep(0.5)

        # Final comprehensive summary
        self._display_enhanced_results(result, "Interactive Control")

    def _display_enhanced_results(self, result: Dict[str, Any], demo_name: str) -> None:
        """Display results with enhanced formatting."""

        # Create summary panel
        summary_text = Text()
        summary_text.append("🎯 ", style="bold yellow")
        summary_text.append(
            f"Scenario: {result['scenario_type']}\n", style="bold white"
        )
        summary_text.append("📊 ", style="bold green")
        summary_text.append(f"Total Steps: {result['total_steps']} | ", style="white")
        summary_text.append(f"Tokens: {result['total_tokens']} | ", style="white")
        summary_text.append(
            f"Duration: {result['total_duration']:.1f}s\n", style="white"
        )
        summary_text.append("⭐ ", style="bold magenta")
        summary_text.append(f"Confidence: {result['confidence']:.2f}", style="white")

        self.console.print(
            Panel(summary_text, title=f"✨ {demo_name} Results", border_style="green")
        )

    async def run_comprehensive_showcase(self) -> None:
        """Run comprehensive UX showcase combining all features."""

        self.console.clear()
        self.console.print(
            Panel.fit(
                "[bold rainbow]🌟 Comprehensive Cognition UX Showcase 🌟[/bold rainbow]\n"
                "[dim]The complete polished experience[/dim]",
                border_style="rainbow",
            )
        )

        await self.run_polished_showcase()

        # Final summary
        self.console.print("\n" + "=" * 60)
        self.console.print(
            Panel(
                "[bold green]🎉 UX Polish Demo Complete![/bold green]\n\n"
                "[white]Key UX Features Demonstrated:[/white]\n"
                "• Progressive enhancement with real-time updates\n"
                "• Live metrics dashboard with responsive layout\n"
                "• Parallel pipeline visualization\n"
                "• Interactive control simulation\n"
                "• Enhanced result formatting and presentation\n\n"
                "[dim]The mock cognition pipeline now provides a polished,\n"
                "transparent, and engaging user experience.[/dim]",
                border_style="green",
            )
        )


async def main():
    """Run the UX polish demonstration."""
    demo = CognitionUXPolishDemo()
    await demo.run_comprehensive_showcase()


if __name__ == "__main__":
    asyncio.run(main())
