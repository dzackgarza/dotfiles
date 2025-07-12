from dataclasses import dataclass, field
from datetime import datetime
from textual.widgets import Static
from textual.containers import VerticalScroll, Vertical
from textual.reactive import reactive
from textual.message import Message
from rich.text import Text
from rich.console import Console
from rich.syntax import Syntax
from typing import Optional
from pathlib import Path

from ..config import RoleConfig, UIConfig, ThemeConfig


@dataclass
class SubBlock:
    """A sub-block within a main timeline block"""

    id: str
    type: str  # "step", "detail", "info", "progress", "result", "note"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class TimelineBlock:
    """A single block in the Sacred Timeline"""

    id: str
    timestamp: datetime
    role: str  # "user", "system", "assistant", "cognition", "turn", "tool", "error", "processing"
    content: str
    metadata: dict = field(default_factory=dict)
    time_taken: Optional[float] = None  # Time taken for this block in seconds
    tokens_input: Optional[int] = None  # Number of input tokens
    tokens_output: Optional[int] = None  # Number of output tokens
    sub_blocks: list[SubBlock] = field(
        default_factory=list
    )  # Sub-blocks for cognition pipelines


class TurnBlockWidget(Vertical):
    """A widget representing a single turn in the Sacred Timeline."""

    # Load CSS from external file
    _css_file = Path(__file__).parent / "timeline.tcss"
    DEFAULT_CSS = _css_file.read_text() if _css_file.exists() else ""

    def __init__(
        self,
        turn_id: str,
        timestamp: datetime,
        blocks_in_turn: list[TimelineBlock],
        *args,
        **kwargs,
    ):
        self.turn_id = turn_id
        self.timestamp = timestamp
        self.blocks_in_turn = blocks_in_turn
        super().__init__(*args, **kwargs)
        self.add_class("turn-block")

    def compose(self):
        header_text = self._get_header_text()
        yield Static(header_text, classes="turn-header")
        for block in self.blocks_in_turn:
            yield TimelineBlockWidget(block)

    def _get_header_text(self) -> Text:
        """Constructs dim hrule between conversation turns"""
        header = Text()

        # Create a dim hrule: -----------------Turn N--------------
        left_line = "-" * 17
        right_line = "-" * 14
        turn_text = f"Turn {self.turn_id}"

        header.append(f"{left_line}{turn_text}{right_line}", style="dim")

        return header


class TimelineView(VerticalScroll):
    """Bottom-up scrolling timeline - new messages push everything upward"""

    @dataclass
    class BlockAdded(Message):
        block: TimelineBlock

    blocks: reactive[list[TimelineBlock]] = reactive(list)
    _current_turn_widget: Optional[TurnBlockWidget] = None
    _turn_counter: int = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auto_scroll = True  # Always scroll to bottom

        # Smart auto-scroll state tracking
        self.user_is_following = True  # Track if user is following latest content
        self.auto_scroll_threshold = 100  # Pixels from bottom to consider "following"
        import time

        self.last_user_scroll_time = time.time()

    def on_scroll(self, event) -> None:
        """Handle scroll events to detect user intent for smart auto-scroll"""
        import time

        # Calculate distance from bottom
        max_scroll = self.max_scroll_y
        current_scroll = self.scroll_y
        distance_from_bottom = max_scroll - current_scroll

        # Update following state based on scroll position
        if distance_from_bottom <= self.auto_scroll_threshold:
            # User is near bottom - they're following along
            self.user_is_following = True
        else:
            # User scrolled up to review - they're not following
            self.user_is_following = False
            self.last_user_scroll_time = time.time()

    def watch_blocks(self, blocks: list[TimelineBlock]) -> None:
        """Update display when blocks change - using progressive mounting like Elia"""
        # Check how many blocks we currently have rendered
        current_widgets = self.query("TimelineBlockWidget, TurnBlockWidget")
        current_count = len(current_widgets)

        # Only process new blocks that haven't been rendered yet
        if len(blocks) <= current_count:
            return  # No new blocks to add

        # Progressive mounting: only add new blocks
        new_blocks = blocks[current_count:]

        for block in new_blocks:
            # Mount each new block individually (Elia pattern)
            block_widget = TimelineBlockWidget(block)
            self.mount(block_widget)

        # Smart auto-scroll to bottom
        if self._should_auto_scroll():
            self.call_after_refresh(self.scroll_end, animate=False, force=False)

    def _should_auto_scroll(self) -> bool:
        """Smart auto-scroll: only if user is following latest content"""
        import time

        # Don't auto-scroll if user is not following
        if not self.user_is_following:
            return False

        # Don't auto-scroll if user recently manually scrolled (grace period)
        current_time = time.time()
        if current_time - self.last_user_scroll_time < 1.0:  # 1 second grace period
            return False

        return True

    def _mount_turn(self, blocks_in_turn: list[TimelineBlock]):
        self._turn_counter += 1
        turn_id = str(self._turn_counter)
        turn_timestamp = (
            blocks_in_turn[0].timestamp if blocks_in_turn else datetime.now()
        )
        turn_widget = TurnBlockWidget(
            turn_id=turn_id, timestamp=turn_timestamp, blocks_in_turn=blocks_in_turn
        )
        self.mount(turn_widget)

    def add_block(self, block: TimelineBlock) -> None:
        """Add a new block to the timeline using progressive mounting"""
        # Progressive mounting: mount the new block directly (Elia pattern)
        block_widget = TimelineBlockWidget(block)
        self.mount(block_widget)

        # Update blocks list for compatibility
        new_blocks = self.blocks.copy()
        new_blocks.append(block)
        self.blocks = new_blocks

        # Smart auto-scroll to bottom
        if self._should_auto_scroll():
            self.call_after_refresh(self.scroll_end, animate=False, force=False)

        self.post_message(self.BlockAdded(block))

    def add_live_block_widget(self, live_widget) -> None:
        """Add a live block widget to the timeline

        Args:
            live_widget: LiveBlockWidget instance to add
        """
        # Mount the live widget directly
        self.mount(live_widget)

        # Smart auto-scroll to bottom
        if self._should_auto_scroll():
            self.call_after_refresh(self.scroll_end, animate=False, force=False)

    def clear_timeline(self) -> None:
        """Clear all blocks"""
        self.blocks = []
        self.query("TurnBlockWidget").remove()
        self._current_turn_widget = None
        self._turn_counter = 0


class TimelineBlockWidget(Vertical):
    """Individual block widget with Sacred Timeline block aesthetic"""

    # Load CSS from external file
    _css_file = Path(__file__).parent / "timeline.tcss"
    DEFAULT_CSS = _css_file.read_text() if _css_file.exists() else ""

    def __init__(self, block: TimelineBlock, *args, **kwargs):
        self.block = block
        super().__init__(*args, **kwargs)
        self.add_class("timeline-block")
        self.add_class(f"timeline-block-{block.role}")

    def compose(self):
        """Create the Sacred Timeline block structure with sub-blocks"""
        # Header for the main block
        header_text = self._get_header_text()
        yield Static(header_text, classes="block-header")

        # Main content if any
        if self.block.content:
            content = self._render_content_with_syntax()
            yield Static(content, classes="block-content")

        # Sub-blocks as separate child widgets
        if self.block.sub_blocks:
            for sub_block in self.block.sub_blocks:
                yield SubBlockWidget(sub_block)

    def _get_header_text(self) -> Text:
        """Constructs elegant header text without capitals"""
        header = Text()
        role_title = self._get_role_title()
        role_color = self._get_role_color()
        role_indicator = self._get_role_indicator()

        # Build metrics for elegant display
        metrics = []
        if self.block.time_taken is not None:
            metrics.append(f"{self.block.time_taken:.1f}s")
        if self.block.tokens_input is not None:
            metrics.append(f"{self.block.tokens_input}↑")
        if self.block.tokens_output is not None:
            metrics.append(f"{self.block.tokens_output}↓")

        # Elegant format: icon role title (metrics)
        header.append(f"{role_indicator} ", style=f"bold {role_color}")
        header.append(role_title, style=f"{role_color}")

        if metrics:
            header.append(f" • {' | '.join(metrics)}", style="dim")

        return header

    def _get_role_indicator(self) -> str:
        """Returns the elegant indicator for the block's role."""
        return RoleConfig.ROLE_INDICATORS.get(self.block.role, "•")

    def _get_role_title(self) -> str:
        """Returns the elegant title for the block's role (no capitals)."""
        return RoleConfig.ROLE_TITLES.get(self.block.role, self.block.role)

    def _render_content_with_syntax(self) -> Text:
        """Render content with syntax highlighting and sub-blocks."""
        result = Text()

        # Render main content
        content = self.block.content
        if "```" not in content:
            result.append(content)
        else:
            # Simple code block parsing
            parts = content.split("```")
            for i, part in enumerate(parts):
                if i % 2 == 0:  # Regular text
                    result.append(part)
                else:  # Code block
                    lines = part.split("\n")
                    language = lines[0].strip() if lines else ""
                    code = "\n".join(lines[1:]) if len(lines) > 1 else ""

                    if language and code:
                        try:
                            syntax = Syntax(
                                code,
                                language,
                                theme=UIConfig.DEFAULT_SYNTAX_THEME,
                                background_color=UIConfig.DEFAULT_BACKGROUND_COLOR,
                            )
                            console = Console()
                            with console.capture() as capture:
                                console.print(syntax)
                            result.append(capture.get())
                        except Exception:
                            result.append(f"```{language}\n{code}\n```", style="dim")
                    else:
                        result.append(f"```{part}```", style="dim")

        # Sub-blocks are rendered as separate widgets in compose()
        return result

    def _get_sub_block_icon(self, sub_type: str) -> str:
        """Get icon for sub-block type."""
        icons = {
            "step": "→",
            "detail": "◦",
            "info": "i",
            "progress": "⋯",
            "result": "✓",
            "note": "※",
        }
        return icons.get(sub_type, "◦")

    def _get_role_color(self) -> str:
        """Sacred Timeline role colors - theme-aware"""
        # Get current theme from app
        current_theme_name = getattr(
            self.app, "_current_theme", ThemeConfig.DEFAULT_THEME
        )
        theme_config = ThemeConfig.AVAILABLE_THEMES.get(current_theme_name, {})

        # Map roles to theme color properties
        role_to_theme_property = {
            "user": "success",  # User input = positive/success
            "system": "warning",  # System = warning/attention
            "assistant": "primary",  # Assistant = primary theme color
            "cognition": "secondary",  # Cognition = secondary color
            "turn": "primary",  # Turn markers = primary color
            "tool": "accent",  # Tools = accent color
            "error": "error",  # Errors = error color
            "processing": "warning",  # Processing = warning color
        }

        theme_property = role_to_theme_property.get(self.block.role, "primary")
        return str(theme_config.get(theme_property, "#ffffff"))

    def _get_border_color(self) -> str:
        """Sacred Timeline border colors - theme-aware"""
        # Get current theme from app
        current_theme_name = getattr(
            self.app, "_current_theme", ThemeConfig.DEFAULT_THEME
        )
        theme_config = ThemeConfig.AVAILABLE_THEMES.get(current_theme_name, {})

        # Map roles to theme color properties for borders
        role_to_theme_property = {
            "user": "success",
            "system": "warning",
            "assistant": "primary",
            "cognition": "secondary",
            "turn": "secondary",  # Use secondary for subtle turn borders
            "tool": "accent",
            "error": "error",
            "processing": "warning",
        }

        theme_property = role_to_theme_property.get(self.block.role, "primary")
        return str(theme_config.get(theme_property, "#888888"))


class SubBlockWidget(Vertical):
    """Individual sub-block widget for cognition steps"""

    # Load CSS from external file
    _css_file = Path(__file__).parent / "timeline.tcss"
    DEFAULT_CSS = _css_file.read_text() if _css_file.exists() else ""

    def __init__(self, sub_block: SubBlock, *args, **kwargs):
        self.sub_block = sub_block
        super().__init__(*args, **kwargs)
        self.add_class("sub-block")
        self.add_class(f"sub-block-{sub_block.type}")

    def compose(self):
        """Create the sub-block structure"""
        # Header with step name and timing
        header_text = self._get_sub_block_header()
        yield Static(header_text, classes="sub-block-header")

        # Content with model and status info
        content_text = self._get_sub_block_content()
        yield Static(content_text, classes="sub-block-content")

    def _get_sub_block_header(self) -> Text:
        """Create header for sub-block"""
        header = Text()

        # Get step name
        step_name = self.sub_block.type.replace("_", " ").title()
        header.append(f"{step_name}", style="bold")

        # Add timing info (simulated for now)
        header.append(" (0.2s | 10↑ / 3↓)", style="dim")

        return header

    def _get_sub_block_content(self) -> Text:
        """Create content for sub-block"""
        content = Text()

        # Model info
        content.append("Model: ", style="dim")
        content.append("`tinyllama-v2`", style="bold")
        content.append("\n")

        # Status
        content.append("Status: ", style="dim")
        content.append("✅ Complete", style="green")

        return content
