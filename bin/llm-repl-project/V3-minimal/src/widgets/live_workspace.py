"""
Live Workspace Widget - V3's chat_container Pattern for Cognition

Uses V3's proven VerticalScroll + simple widget children pattern.
Handles live cognition with show/hide for 2-way ↔ 3-way splits.
"""

from textual.containers import VerticalScroll
from typing import List, Dict
from pathlib import Path

from ..core.live_blocks import LiveBlock
from .sub_module import SubModuleWidget


class LiveWorkspaceWidget(VerticalScroll):
    """Live cognition workspace using V3's chat_container pattern

    Displays live sub-modules during cognition process.
    Uses V3's proven pattern: VerticalScroll with simple widget children.
    Currently shows mockup content and is always visible for 3-way split.
    """

    # Load CSS from external file
    _css_file = Path(__file__).parent / "live_workspace.tcss"
    DEFAULT_CSS = _css_file.read_text() if _css_file.exists() else ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_class("live-workspace")

    def on_mount(self) -> None:
        """Setup after widget is mounted"""
        # Track mounted sub-module widgets
        self.sub_module_widgets: Dict[str, SubModuleWidget] = {}

        # CSS classes
        self.add_class("live-workspace")

        # Start hidden (2-way split)
        self.add_class("hidden")
        self.is_visible = False

        # Smart auto-scroll state (like V3)
        self.user_is_following = True
        self.auto_scroll_threshold = 100
        import time

        self.last_user_scroll_time = time.time()

    async def add_sub_module(self, sub_module: LiveBlock) -> None:
        """Mount sub-module like V3: await self.mount(SubModuleWidget(data))"""
        if sub_module.id in self.sub_module_widgets:
            return  # Already exists

        widget = SubModuleWidget(sub_module)
        self.sub_module_widgets[sub_module.id] = widget

        # Mount widget directly (like V3's chat_container.mount)
        await self.mount(widget)

        # Smart auto-scroll (like V3's scroll_to_latest_message)
        if self._should_auto_scroll():
            self.call_after_refresh(self._scroll_to_latest)

    def remove_sub_module(self, sub_module_id: str) -> None:
        """Remove sub-module widget"""
        if sub_module_id in self.sub_module_widgets:
            widget = self.sub_module_widgets[sub_module_id]
            try:
                widget.remove()
            except Exception:
                pass
            del self.sub_module_widgets[sub_module_id]

    def clear_workspace(self) -> None:
        """Clear all sub-modules and hide workspace"""
        for widget in self.sub_module_widgets.values():
            try:
                widget.remove()
            except Exception:
                pass
        self.sub_module_widgets.clear()

        # Hide workspace (return to 2-way split)
        self.hide_workspace()

    def show_workspace(self) -> None:
        """Show workspace (2-way → 3-way split)"""
        if not self.is_visible:
            self.remove_class("hidden")
            self.is_visible = True
            self.refresh()

    def hide_workspace(self) -> None:
        """Hide workspace (3-way → 2-way split)"""
        if self.is_visible:
            self.add_class("hidden")
            self.is_visible = False
            self.refresh()

    def update_sub_module(self, sub_module: LiveBlock) -> None:
        """Update existing sub-module widget"""
        if sub_module.id in self.sub_module_widgets:
            widget = self.sub_module_widgets[sub_module.id]
            widget.sub_module = sub_module
            widget.refresh()

    def on_scroll(self, event) -> None:
        """Handle scroll events for smart auto-scroll (like V3)"""
        import time

        # Calculate distance from bottom
        max_scroll = self.max_scroll_y
        current_scroll = self.scroll_y
        distance_from_bottom = max_scroll - current_scroll

        # Update following state
        if distance_from_bottom <= self.auto_scroll_threshold:
            self.user_is_following = True
        else:
            self.user_is_following = False
            self.last_user_scroll_time = time.time()

    def _scroll_to_latest(self) -> None:
        """Scroll to latest sub-module (like V3's scroll_to_latest_message)"""
        self.refresh()
        self.scroll_end(animate=False, force=True)

    def _should_auto_scroll(self) -> bool:
        """Smart auto-scroll logic (like V3)"""
        import time

        if not self.user_is_following:
            return False

        current_time = time.time()
        if current_time - self.last_user_scroll_time < 1.0:
            return False

        return True

    def get_sub_module_count(self) -> int:
        """Get number of sub-modules in workspace"""
        return len(self.sub_module_widgets)

    def get_sub_modules(self) -> List[SubModuleWidget]:
        """Get all sub-module widgets"""
        return list(self.sub_module_widgets.values())

    def is_empty(self) -> bool:
        """Check if workspace has any sub-modules"""
        return len(self.sub_module_widgets) == 0

    def start_cognition_turn(self) -> None:
        """Start cognition turn - show workspace if hidden"""
        self.show_workspace()

    def complete_cognition_turn(self) -> None:
        """Complete cognition turn - clear and hide workspace"""
        self.clear_workspace()
