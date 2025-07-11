"""
Cognition Pipeline Widget

Advanced Textual widget for displaying nested cognition pipelines with
real-time updates, smooth animations, and polished UX.
"""

from textual.widgets import Static, ProgressBar
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive
from textual.timer import Timer
from rich.text import Text
from rich.panel import Panel
from rich.progress import Progress
from typing import Optional, Dict, Any, List, Callable
from datetime import datetime
import asyncio

from src.core.mock_scenarios import MockCognitionPlugin


class CognitionStepWidget(Static):
    """Enhanced widget for displaying individual cognition steps with animations."""
    
    DEFAULT_CSS = """
    CognitionStepWidget {
        border: round $accent;
        width: 90%;
        margin: 0 2;
        padding: 0 1;
        height: auto;
        min-height: 4;
        max-height: 8;
    }
    
    .step-pending {
        border: round $surface;
        opacity: 0.6;
    }
    
    .step-running {
        border: round $warning;
        background: $warning 10%;
    }
    
    .step-completed {
        border: round $success;
        background: $success 10%;
    }
    
    .step-failed {
        border: round $error;
        background: $error 10%;
    }
    """
    
    # Reactive properties for smooth updates
    step_state = reactive("pending")
    step_progress = reactive(0.0)
    step_content = reactive("")
    
    def __init__(self, sub_module, **kwargs):
        super().__init__(**kwargs)
        self.sub_module = sub_module
        self.sub_module.add_update_callback(self._on_step_update)
        self.animation_timer: Optional[Timer] = None
        self._update_display()
    
    def _on_step_update(self, sub_module: CognitionSubModule) -> None:
        """Update display when step state changes with smooth transitions."""
        self.step_state = sub_module.state
        self.step_progress = sub_module.progress
        
        if sub_module.result:
            self.step_content = sub_module.result.content[:100] + "..." if len(sub_module.result.content) > 100 else sub_module.result.content
        
        self._update_display()
        self._animate_state_change()
    
    def _update_display(self) -> None:
        """Update the visual display with enhanced styling."""
        step = self.sub_module.step
        state = self.step_state
        progress = self.step_progress
        
        # Remove all state classes first
        self.remove_class("step-pending", "step-running", "step-completed", "step-failed")
        
        # Create rich display text
        display_text = Text()
        
        # Step header with icon and name
        display_text.append(f"{step.icon} ", style="bold")
        display_text.append(f"{step.name}", style="bold white")
        
        # State-specific styling and content
        if state == "pending":
            display_text.append(" ⏳", style="dim")
            self.add_class("step-pending")
        elif state == "running":
            display_text.append(f" 🔄 ({progress:.0%})", style="yellow bold")
            self.add_class("step-running")
            # Add animated progress indicator
            progress_bar = "█" * int(progress * 10) + "░" * (10 - int(progress * 10))
            display_text.append(f"\n[{progress_bar}]", style="yellow")
        elif state == "completed":
            display_text.append(" ✅", style="green bold")
            self.add_class("step-completed")
            if self.step_content:
                display_text.append(f"\n{self.step_content}", style="dim white")
        elif state == "failed":
            display_text.append(" ❌", style="red bold")
            self.add_class("step-failed")
        
        # Add metadata for completed or running steps
        if state in ["running", "completed"] and self.sub_module.result:
            metadata_text = f"\nModel: {step.model}"
            if self.sub_module.result:
                metadata_text += f" | Tokens: {self.sub_module.result.tokens_used}"
                metadata_text += f" | Confidence: {self.sub_module.result.confidence_score:.2f}"
            display_text.append(metadata_text, style="dim cyan")
        
        self.update(display_text)
    
    def _animate_state_change(self) -> None:
        """Add subtle animation when state changes."""
        if self.animation_timer:
            self.animation_timer.stop()
        
        # Pulse effect for state changes
        original_opacity = 1.0
        pulse_opacity = 0.7
        
        def pulse_animation():
            # Simple opacity pulse (simulated through styling)
            if self.step_state == "running":
                # Keep pulsing while running
                self.animation_timer = self.set_timer(0.5, pulse_animation)
        
        pulse_animation()


class CognitionPipelineWidget(Vertical):
    """Enhanced widget for displaying full cognition pipeline with real-time updates."""
    
    DEFAULT_CSS = """
    CognitionPipelineWidget {
        border: round $primary;
        margin-bottom: 1;
        padding: 1;
        height: auto;
        min-height: 10;
        background: $surface;
    }
    
    .pipeline-header {
        text-style: bold;
        color: $text;
        margin-bottom: 1;
        padding: 1;
        background: $primary 20%;
        border-radius: 1;
    }
    
    .pipeline-metrics {
        margin-bottom: 1;
        padding: 0 1;
    }
    
    .pipeline-steps {
        height: auto;
    }
    """
    
    # Reactive properties
    pipeline_state = reactive("pending")
    pipeline_progress = reactive(0.0)
    total_tokens = reactive(0)
    total_duration = reactive(0.0)
    
    def __init__(self, cognition_plugin: MockCognitionPlugin, **kwargs):
        super().__init__(**kwargs)
        self.cognition_plugin = cognition_plugin
        self.cognition_plugin.add_update_callback(self._on_pipeline_update)
        
        # Create child widgets
        self.header_widget = Static(classes="pipeline-header")
        self.metrics_widget = Static(classes="pipeline-metrics")
        self.steps_container = Vertical(classes="pipeline-steps")
        
        # Create step widgets
        self.step_widgets = []
        for sub_module in cognition_plugin.sub_modules:
            step_widget = CognitionStepWidget(sub_module)
            self.step_widgets.append(step_widget)
            self.steps_container.mount(step_widget)
        
        # Mount widgets
        self.mount(self.header_widget)
        self.mount(self.metrics_widget) 
        self.mount(self.steps_container)
        
        self._update_header()
        self._update_metrics()
    
    def _on_pipeline_update(self, plugin: EnhancedMockCognitionPlugin) -> None:
        """Update display when pipeline state changes."""
        status = plugin.get_current_status()
        
        self.pipeline_state = status["state"]
        self.pipeline_progress = status["progress"]
        self.total_tokens = status["total_tokens"]
        self.total_duration = status["total_duration"]
        
        self._update_header()
        self._update_metrics()
    
    def _update_header(self) -> None:
        """Update the pipeline header display with enhanced styling."""
        status = self.cognition_plugin.get_current_status()
        
        header_text = Text()
        header_text.append("🧠 ", style="bold cyan")
        header_text.append("Cognition Pipeline", style="bold white")
        
        if self.pipeline_state == "pending":
            header_text.append(" ⏳ Ready", style="dim")
        elif self.pipeline_state == "running":
            header_text.append(f" 🔄 Processing ({self.pipeline_progress:.0%})", style="yellow bold")
            if status.get("active_step"):
                header_text.append(f"\n🎯 Current: {status['active_step']}", style="dim yellow")
        elif self.pipeline_state == "completed":
            header_text.append(" ✅ Complete", style="green bold")
            header_text.append(f"\n🎉 All {len(status['completed_steps'])} steps finished", style="dim green")
        elif self.pipeline_state == "failed":
            header_text.append(" ❌ Failed", style="red bold")
        
        self.header_widget.update(header_text)
    
    def _update_metrics(self) -> None:
        """Update the metrics display with real-time data."""
        metrics_text = Text()
        
        # Tokens and duration
        metrics_text.append("📊 ", style="bold blue")
        metrics_text.append(f"Tokens: {self.total_tokens}", style="white")
        metrics_text.append(" | ", style="dim")
        metrics_text.append(f"Duration: {self.total_duration:.1f}s", style="white")
        
        # Progress breakdown
        if self.pipeline_state == "running":
            completed = len([m for m in self.cognition_plugin.sub_modules if m.state == "completed"])
            total = len(self.cognition_plugin.sub_modules)
            metrics_text.append(" | ", style="dim")
            metrics_text.append(f"Steps: {completed}/{total}", style="cyan")
        
        # Average confidence (if available)
        completed_modules = [m for m in self.cognition_plugin.sub_modules if m.state == "completed" and m.result]
        if completed_modules:
            avg_confidence = sum(m.result.confidence_score for m in completed_modules) / len(completed_modules)
            metrics_text.append(" | ", style="dim")
            metrics_text.append(f"Confidence: {avg_confidence:.2f}", style="magenta")
        
        self.metrics_widget.update(metrics_text)


class CognitionDashboardWidget(Horizontal):
    """Comprehensive dashboard widget for multiple cognition pipelines."""
    
    DEFAULT_CSS = """
    CognitionDashboardWidget {
        height: 100%;
        border: round $primary;
        background: $surface;
    }
    
    .dashboard-sidebar {
        width: 30%;
        border-right: vkey $primary;
        padding: 1;
        background: $primary 10%;
    }
    
    .dashboard-main {
        width: 70%;
        padding: 1;
    }
    
    .pipeline-list {
        height: auto;
    }
    
    .dashboard-summary {
        margin-bottom: 2;
        padding: 1;
        border: round $accent;
        background: $accent 10%;
    }
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Sidebar for pipeline list and controls
        self.sidebar = Vertical(classes="dashboard-sidebar")
        self.pipeline_list = Vertical(classes="pipeline-list")
        self.summary_widget = Static(classes="dashboard-summary")
        
        # Main area for detailed pipeline view
        self.main_area = Vertical(classes="dashboard-main")
        
        # Setup layout
        self.sidebar.mount(self.summary_widget)
        self.sidebar.mount(self.pipeline_list)
        self.mount(self.sidebar)
        self.mount(self.main_area)
        
        # Pipeline management
        self.pipelines: List[CognitionPipelineWidget] = []
        self.active_pipeline: Optional[CognitionPipelineWidget] = None
        
        self._update_summary()
    
    def add_pipeline(self, plugin: MockCognitionPlugin, name: str) -> CognitionPipelineWidget:
        """Add a new cognition pipeline to the dashboard."""
        pipeline_widget = CognitionPipelineWidget(plugin)
        self.pipelines.append(pipeline_widget)
        
        # Add to sidebar list
        pipeline_item = Static(f"🧠 {name}")
        self.pipeline_list.mount(pipeline_item)
        
        # Set as active if first pipeline
        if not self.active_pipeline:
            self.set_active_pipeline(pipeline_widget)
        
        self._update_summary()
        return pipeline_widget
    
    def set_active_pipeline(self, pipeline: CognitionPipelineWidget) -> None:
        """Set the active pipeline for detailed view."""
        if self.active_pipeline:
            self.main_area.remove_children()
        
        self.active_pipeline = pipeline
        self.main_area.mount(pipeline)
    
    def _update_summary(self) -> None:
        """Update the dashboard summary."""
        summary_text = Text()
        summary_text.append("📊 Dashboard Summary\n\n", style="bold cyan")
        summary_text.append(f"Total Pipelines: {len(self.pipelines)}\n", style="white")
        
        if self.pipelines:
            running = sum(1 for p in self.pipelines if p.pipeline_state == "running")
            completed = sum(1 for p in self.pipelines if p.pipeline_state == "completed")
            
            summary_text.append(f"Running: {running}\n", style="yellow")
            summary_text.append(f"Completed: {completed}\n", style="green")
            
            # Total tokens across all pipelines
            total_tokens = sum(p.total_tokens for p in self.pipelines)
            summary_text.append(f"Total Tokens: {total_tokens}", style="blue")
        
        self.summary_widget.update(summary_text)


# Export main widgets
__all__ = [
    "CognitionStepWidget",
    "CognitionPipelineWidget", 
    "CognitionDashboardWidget"
]