"""
Enhanced CognitionWidget for displaying cognition with sub-modules in ProcessingWidget style.
"""

from textual.widgets import Static
from textual.reactive import reactive
from textual import work
from rich.text import Text
import time
import asyncio


class CognitionWidget(Static):
    """Enhanced widget for displaying cognition with sub-modules in ProcessingWidget style."""

    DEFAULT_CSS = """
    CognitionWidget {
        border: round $accent;
        margin: 1 0;
        padding: 1;
        height: auto;
        background: $surface;
    }
    """

    # Class-level tracker for sequential processing enforcement
    _active_widgets = set()

    # Reactive properties for live updates
    elapsed_time = reactive(0.0)

    def watch_elapsed_time(self, elapsed_time: float) -> None:
        """Watch elapsed_time changes and update display"""
        if self.is_live:
            self._update_display()

    def __init__(self, content="", is_live=False, **kwargs):
        super().__init__(**kwargs)
        self.content = content
        self.is_live = is_live
        self.sub_modules = []  # List of sub-module data
        self.start_time = time.time()
        self._timer_task = None
        self._widget_id = id(self)  # Unique identifier for this widget

        if is_live:
            self._register_as_active()
            self._start_timer()

        self._update_display()

    def _register_as_active(self):
        """Register this widget as actively processing for sequential enforcement"""
        CognitionWidget._active_widgets.add(self._widget_id)

    def _unregister_as_active(self):
        """Unregister this widget from active processing"""
        CognitionWidget._active_widgets.discard(self._widget_id)

    def is_processing_allowed(self):
        """Check if this widget is allowed to process (sequential enforcement)"""
        # Allow processing if no other widgets are active, or this widget is already active
        return len(CognitionWidget._active_widgets) == 0 or self._widget_id in CognitionWidget._active_widgets

    def _start_timer(self):
        """Start the timer for live cognition"""
        if not self._timer_task or self._timer_task.is_finished:
            self._timer_task = self._update_timer()

    @work(exclusive=True)
    async def _update_timer(self):
        """Update timer every 0.1s for smooth live updates"""
        while self.is_live and self.start_time:
            self.elapsed_time = time.time() - self.start_time
            await asyncio.sleep(0.1)  # Update every 0.1s for smooth UI

    def add_sub_module(self, name, icon, state="PROCESSING", tokens_in=0, tokens_out=0, progress=0.0, timer=0.0):
        """Add a sub-module to display with live tracking"""
        sub_module = {
            "name": name,
            "icon": icon,
            "state": state,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "progress": progress,
            "timer": timer,
            "start_time": time.time(),  # Track when this sub-module started
            "is_live": state == "PROCESSING"
        }
        self.sub_modules.append(sub_module)
        self._update_display()

    def update_sub_module(self, name, **kwargs):
        """Update a specific sub-module"""
        for sub_module in self.sub_modules:
            if sub_module["name"] == name:
                sub_module.update(kwargs)
                break
        self._update_display()

    def increment_tokens(self, name, tokens_in=0, tokens_out=0):
        """Increment token counters for a specific sub-module in real-time"""
        for sub_module in self.sub_modules:
            if sub_module["name"] == name and sub_module["is_live"]:
                sub_module["tokens_in"] += tokens_in
                sub_module["tokens_out"] += tokens_out
                self._update_display()
                break

    def update_progress(self, name, progress):
        """Update progress bar for a specific sub-module"""
        for sub_module in self.sub_modules:
            if sub_module["name"] == name and sub_module["is_live"]:
                sub_module["progress"] = min(progress, 1.0)  # Cap at 100%
                self._update_display()
                break

    def complete_sub_module(self, name):
        """Mark a sub-module as completed - stop all live updates"""
        for sub_module in self.sub_modules:
            if sub_module["name"] == name:
                sub_module["state"] = "COMPLETED"
                sub_module["is_live"] = False
                sub_module["progress"] = 1.0  # Set to 100%
                self._update_display()
                break

    def _update_display(self):
        """Update the widget display with ProcessingWidget style."""
        display_text = Text()

        # Header
        display_text.append("🧠 ", style="bold cyan")
        display_text.append("Cognition", style="bold white")

        if self.is_live:
            if self.is_processing_allowed():
                display_text.append(" 🔄", style="yellow")
                display_text.append(f" {self.elapsed_time:.1f}s", style="bright_cyan")
            else:
                display_text.append(" ⏸️", style="dim")
                display_text.append(" Waiting for prior block to finish", style="dim white")
        else:
            if self.is_ready_for_inscription():
                display_text.append(" ✅", style="green")
                display_text.append(" Ready for /inscribe", style="bright_green")
            else:
                display_text.append(" ✅", style="green")

        display_text.append("\n\n")

        # Sub-modules in ProcessingWidget style
        for i, sub_module in enumerate(self.sub_modules):
            if i > 0:
                display_text.append("\n")

            state = sub_module["state"]
            name = sub_module["name"]
            icon = sub_module["icon"]
            tokens_in = sub_module["tokens_in"]
            tokens_out = sub_module["tokens_out"]
            progress = sub_module["progress"]
            timer = sub_module["timer"]

            # State colors
            state_color = {
                "PROCESSING": "bright_yellow",
                "COMPLETED": "bright_green",
                "QUEUED": "dim white"
            }.get(state, "white")

            # Calculate live timer for this sub-module
            if sub_module["is_live"] and sub_module["start_time"]:
                live_timer = time.time() - sub_module["start_time"]
            else:
                live_timer = timer  # Use static timer if not live

            # First line: [STATE] | Timer | Tokens
            display_text.append(f"[{state}]", style=state_color)
            display_text.append(" | ", style="dim")
            display_text.append(f"⏱️  {live_timer:.1f}s", style="bright_cyan")
            display_text.append(" | ", style="dim")
            display_text.append(f"↑ {tokens_in} tokens  ↓ {tokens_out} tokens", style="bright_magenta")

            # Second line: Icon + Name
            display_text.append(f"\n{icon} {name}", style="white")

            # Third line: Progress bar
            if state == "COMPLETED":
                progress_bar = "█" * 30  # 100% filled when completed
                progress_text = "100%"
                progress_style = "bright_green"
            elif state == "PROCESSING":
                if progress > 0:
                    # Real progress
                    filled = int(progress * 30)
                    empty = 30 - filled
                    progress_bar = "█" * filled + "━" * empty
                    progress_text = f"{int(progress * 100)}%"
                else:
                    # Indeterminate/pulsing animation for processing
                    progress_bar = "━" * 30
                    progress_text = "..."
                progress_style = "bright_blue"
            else:
                # Queued or other states
                progress_bar = "━" * 30
                progress_text = "0%"
                progress_style = "dim white"

            display_text.append(f"\n[{progress_bar}] {progress_text}", style=progress_style)

        self.update(display_text)

    def complete_cognition(self):
        """Complete the entire cognition process - stop all timers and mark ready for inscription"""
        self.is_live = False
        self._unregister_as_active()  # Allow other widgets to process

        # Complete all sub-modules
        for sub_module in self.sub_modules:
            sub_module["state"] = "COMPLETED"
            sub_module["is_live"] = False
            sub_module["progress"] = 1.0

        self._update_display()

    def is_ready_for_inscription(self):
        """Check if this cognition is ready for manual inscription"""
        return not self.is_live and all(not sm["is_live"] for sm in self.sub_modules)

    def update_content(self, content, is_live=None):
        """Update the widget content."""
        self.content = content
        if is_live is not None:
            self.is_live = is_live
            if is_live:
                self.start_time = time.time()
                self._start_timer()
            elif self._timer_task:
                self._timer_task.cancel()
        self._update_display()

    def set_live_content(self, content):
        """Update content while maintaining live state"""
        self.content = content
        self._update_display()
