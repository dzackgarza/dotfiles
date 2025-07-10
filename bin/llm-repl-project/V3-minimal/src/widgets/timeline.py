from dataclasses import dataclass, field
from datetime import datetime
from textual.widgets import Static
from textual.containers import VerticalScroll, Vertical
from textual.reactive import reactive
from textual.message import Message
from rich.text import Text
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.align import Align
from typing import Optional

from ..config import RoleConfig, UIConfig


@dataclass
class TimelineBlock:
    """A single block in the Sacred Timeline"""

    id: str
    timestamp: datetime
    role: str  # "user", "system", "assistant", "cognition", "turn"
    content: str
    metadata: dict = field(default_factory=dict)
    time_taken: Optional[float] = None  # Time taken for this block in seconds
    tokens_input: Optional[int] = None  # Number of input tokens
    tokens_output: Optional[int] = None  # Number of output tokens


class TurnBlockWidget(Vertical):
    """A widget representing a single turn in the Sacred Timeline."""

    DEFAULT_CSS = """
    TurnBlockWidget {
        border: round $accent;
        margin-bottom: 1;
        padding: 0 1;
        height: auto;
        min-height: 0;
    }
    """

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
        """Constructs uniform turn header in format: |----TURN #X-------|"""
        header = Text()

        # Create uniform turn header: |----TURN #X-------|
        header.append("|----", style="dim")
        header.append("TURN ", style="bright_white bold")
        header.append(f"#{self.turn_id}", style="bright_white bold")
        header.append("-------|", style="dim")

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

        # Smart auto-scroll - only if user is near bottom (Elia pattern)
        if self._should_auto_scroll():
            self.scroll_end(animate=False, force=True)

    def _should_auto_scroll(self) -> bool:
        """Check if we should auto-scroll (user near bottom) - Elia pattern"""
        try:
            return self.scroll_y >= self.max_scroll_y - 3
        except (AttributeError, ValueError):
            # If scroll properties not available yet, default to auto-scroll
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

        # Smart auto-scroll - only if user is near bottom
        if self._should_auto_scroll():
            self.scroll_end(animate=False, force=True)

        self.post_message(self.BlockAdded(block))

    def clear_timeline(self) -> None:
        """Clear all blocks"""
        self.blocks = []
        self.query("TurnBlockWidget").remove()
        self._current_turn_widget = None
        self._turn_counter = 0


class TimelineBlockWidget(Static):
    """Individual block widget with Sacred Timeline block aesthetic"""

    def __init__(self, block: TimelineBlock, *args, **kwargs):
        self.block = block
        super().__init__(*args, **kwargs)
        self.add_class("timeline-block")
        self.add_class(f"timeline-block-{block.role}")

    def compose(self):
        """Create the Sacred Timeline block structure"""
        header_text = self._get_header_text()
        border_color = self._get_border_color()

        # Content area with proper formatting and syntax highlighting
        content_renderable = self._render_content_with_syntax()

        yield Static(
            Panel(
                Align.left(content_renderable),
                title=header_text,
                border_style=border_color,
                title_align="left",
                expand=True,
                padding=(0, 1),
            )
        )

    def _get_header_text(self) -> Text:
        """Constructs the uniform header text for the block in format: |----TYPE (X s, Y up/Z down)-------|"""
        header = Text()
        role_name = self.block.role.upper()
        role_color = self._get_role_color()

        # Build metrics for the uniform format
        metrics = []
        if self.block.time_taken is not None:
            metrics.append(f"{self.block.time_taken:.1f}s")
        if self.block.tokens_input is not None:
            metrics.append(f"{self.block.tokens_input}↑")
        if self.block.tokens_output is not None:
            metrics.append(f"{self.block.tokens_output}↓")

        # Create uniform header: |----TYPE (metrics)-------|
        header.append("|----", style="dim")
        header.append(role_name, style=f"bold {role_color}")

        if metrics:
            header.append(f" ({', '.join(metrics)})", style="dim")

        header.append("-------|", style="dim")

        return header

    def _get_role_indicator(self) -> str:
        """Returns the ASCII indicator for the block's role."""
        return RoleConfig.ROLE_INDICATORS.get(self.block.role, "•")

    def _render_content_with_syntax(self) -> Text:
        """Render content with syntax highlighting for code blocks."""
        content = self.block.content
        if "```" not in content:
            return Text(content)

        # Simple code block parsing
        parts = content.split("```")
        result = Text()

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

        return result

    def _get_role_color(self) -> str:
        """Sacred Timeline role colors"""
        return RoleConfig.ROLE_COLORS.get(self.block.role, "white")

    def _get_border_color(self) -> str:
        """Sacred Timeline border colors - subtle but distinct per role"""
        return RoleConfig.BORDER_COLORS.get(self.block.role, "white")
