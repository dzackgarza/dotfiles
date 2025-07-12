"""
Simple UX Polish Demo

Demonstrates polished user experience features using existing mock scenarios.
"""

import asyncio
from typing import Dict, Any
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from src.core.mock_scenarios import CognitionScenarioGenerator


class SimpleUXPolishDemo:
    """Simple polished UX demonstration for cognition pipeline."""

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

        # Demo 2: Parallel Pipeline Visualization
        await self._demo_parallel_visualization()

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

    async def _demo_parallel_visualization(self) -> None:
        """Demonstrate parallel pipeline visualization."""

        self.console.print(
            "\n[bold magenta]🚀 Parallel Pipeline Visualization[/bold magenta]"
        )

        # Create multiple scenarios for parallel execution
        scenarios = [
            ("🏗️ Architecture", "Design microservices for autonomous vehicles"),
            ("🔍 Research", "Compare quantum vs classical cryptography"),
            ("💻 Coding", "Implement blockchain consensus algorithm"),
            ("🐛 Debug", "Fix memory leak in distributed cache"),
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

            for name, query in scenarios:
                plugin = self.scenario_generator.create_research_scenario()
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

            # Wait for all to complete
            results = await asyncio.gather(*tasks)

        # Display parallel execution summary
        summary_table = Table(title="🚀 Parallel Execution Summary")
        summary_table.add_column("Pipeline", style="cyan")
        summary_table.add_column("Steps", style="yellow")
        summary_table.add_column("Tokens", style="green")
        summary_table.add_column("Duration", style="blue")
        summary_table.add_column("Confidence", style="magenta")

        for i, (name, _) in enumerate(scenarios):
            result = results[i]
            summary_table.add_row(
                name,
                str(result["total_steps"]),
                str(result["total_tokens"]),
                f"{result['total_duration']:.1f}s",
                f"{result['confidence']:.2f}",
            )

        self.console.print(summary_table)

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
                "• Parallel pipeline visualization\n"
                "• Enhanced result formatting and presentation\n"
                "• Smooth progress tracking and animations\n\n"
                "[dim]The mock cognition pipeline now provides a polished,\n"
                "transparent, and engaging user experience.[/dim]",
                border_style="green",
            )
        )


async def main():
    """Run the UX polish demonstration."""
    demo = SimpleUXPolishDemo()
    await demo.run_comprehensive_showcase()


if __name__ == "__main__":
    asyncio.run(main())
