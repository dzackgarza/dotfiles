from dataclasses import dataclass, field
from datetime import datetime
from textual.widgets import Static
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.message import Message
from rich.text import Text
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.align import Align
from typing import Optional

from ..config import RoleConfig, TimelineConfig, UIConfig


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


class TurnBlockWidget(VerticalScroll):
    """A widget representing a single turn in the Sacred Timeline."""

    DEFAULT_CSS = """
    TurnBlockWidget {
        border: round $accent;
        margin-bottom: 1;
        padding: 0 1;
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
        header = Text()
        timestamp_str = self.timestamp.strftime(TimelineConfig.TIMESTAMP_FORMAT)
        header.append(f"[{timestamp_str}] ", style="dim")
        header.append(
            f"{RoleConfig.ROLE_INDICATORS['turn']} ", style="bright_white bold"
        )
        header.append("TURN ", style="bright_white bold")
        header.append(f"#{self.turn_id}", style="bright_white bold")
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
        """Update display when blocks change"""
        # This method will be refactored to manage TurnBlockWidgets
        # For now, it will clear and re-mount all blocks as before
        self.query("TimelineBlockWidget").remove()
        self.query("TurnBlockWidget").remove()

        # Re-render all blocks, grouping them into turns
        current_turn_blocks: list[TimelineBlock] = []
        for block in blocks:
            if block.role == "user":
                if current_turn_blocks:
                    self._mount_turn(current_turn_blocks)
                current_turn_blocks = [block]
            else:
                current_turn_blocks.append(block)
        if current_turn_blocks:
            self._mount_turn(current_turn_blocks)

        # Always scroll to bottom (newest content)
        if self.auto_scroll:
            self.scroll_end(animate=False)

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
        """Add a new block to the timeline"""
        new_blocks = self.blocks.copy()
        new_blocks.append(block)
        self.blocks = new_blocks
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
        """Constructs the uniform header text for the block."""
        header = Text()
        indicator = self._get_role_indicator()
        role_name = self.block.role.upper()
        role_color = self._get_role_color()
        timestamp_str = self.block.timestamp.strftime(TimelineConfig.TIMESTAMP_FORMAT)

        # Base header: [TIMESTAMP] ICON ROLE_NAME
        header.append(f"[{timestamp_str}] ", style="dim")
        header.append(f"{indicator} ", style=role_color)
        header.append(role_name, style=f"bold {role_color}")

        # Add time and token info if available
        metrics = []
        if self.block.time_taken is not None:
            metrics.append(f"{self.block.time_taken:.1f}s")
        if self.block.tokens_input is not None:
            metrics.append(f"{self.block.tokens_input}↑")
        if self.block.tokens_output is not None:
            metrics.append(f"{self.block.tokens_output}↓")

        if metrics:
            header.append(f" ({' | '.join(metrics)})", style="dim")

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
