"""V3-minimal: LLM REPL with Sacred Timeline and unix-rice aesthetics"""

from pathlib import Path
from textual import events
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.theme import Theme

from .config import AppConfig, ThemeConfig
from .core import ResponseGenerator
from .core.unified_async_processor import UnifiedAsyncInputProcessor
from .widgets.prompt_input import PromptInput
from .theme_picker import InteractiveThemeProvider
from .core.animation_clock import AnimationClock


class LLMReplApp(App[None]):
    """Main application with Sacred Timeline architecture"""

    TITLE = AppConfig.TITLE
    SUB_TITLE = AppConfig.SUB_TITLE
    CSS_PATH = Path(__file__).parent / "theme.tcss"

    # Custom command providers for enhanced theme picker
    # This replaces the default theme provider with our live-switching version
    COMMANDS = {
        InteractiveThemeProvider,
    }

    def __init__(self):
        super().__init__()

        # Set current theme using Textual's theme system
        self._current_theme = self._load_saved_theme()

        # Core components with unified architecture
        self.response_generator = ResponseGenerator(app=self)
        # Use unified async processor (eliminates dual-system conflicts)
        self.unified_async_processor = UnifiedAsyncInputProcessor(
            self.response_generator, app=self
        )

        # UI components - V3 pattern
        self.prompt_input: PromptInput | None = None

    BINDINGS = [
        # Disable Ctrl+Q quit binding by overriding with do-nothing action
        Binding("ctrl+q", "do_nothing", show=False, priority=True),
        # Note: Enter and Shift+Enter are handled directly in PromptInput widget
        # Note: Ctrl+C is handled in PromptInput for copy/quit functionality
        # Note: Ctrl+P uses Textual's built-in theme picker with our custom themes
    ]

    def _load_saved_theme(self) -> str:
        """Load saved theme preference or default"""
        try:
            theme_file = Path.home() / ".config" / "llm-repl" / "theme"
            if theme_file.exists():
                saved_theme = theme_file.read_text().strip()
                if saved_theme in ThemeConfig.AVAILABLE_THEMES:
                    return saved_theme
        except Exception:
            pass
        return ThemeConfig.DEFAULT_THEME

    def _save_theme_preference(self, theme_name: str) -> None:
        """Save theme preference to disk"""
        try:
            config_dir = Path.home() / ".config" / "llm-repl"
            config_dir.mkdir(parents=True, exist_ok=True)
            theme_file = config_dir / "theme"
            theme_file.write_text(theme_name)
        except Exception:
            pass

    def _create_theme_from_config(self, theme_name: str, theme_config: dict) -> Theme:
        """Create a Textual Theme object from configuration"""
        return Theme(
            name=theme_name,
            primary=theme_config["primary"],
            secondary=theme_config["secondary"],
            accent=theme_config["accent"],
            warning=theme_config["warning"],
            error=theme_config["error"],
            success=theme_config["success"],
            dark=theme_config["dark"],
        )

    def _register_all_themes(self) -> None:
        """Register all custom themes with Textual"""
        for theme_name, theme_config in ThemeConfig.AVAILABLE_THEMES.items():
            theme = self._create_theme_from_config(theme_name, theme_config)
            self.register_theme(theme)

    def _get_available_themes(self) -> dict:
        """Get available themes for the command palette"""
        return ThemeConfig.AVAILABLE_THEMES

    def switch_theme(self, theme_name: str) -> bool:
        """Switch to a different theme using Textual's theme system"""
        if theme_name not in ThemeConfig.AVAILABLE_THEMES:
            return False

        try:
            self._current_theme = theme_name
            self._save_theme_preference(theme_name)
            self.theme = theme_name  # Use Textual's built-in theme switching
            return True
        except Exception:
            return False

    def compose(self) -> ComposeResult:
        """Sacred Architecture: Copy V3's exact chat pattern + add staging area"""
        with Vertical(id="main-container"):
            # Sacred Timeline - V3's exact chat-container pattern
            with VerticalScroll(id="chat-container") as chat_scroll:
                chat_scroll.can_focus = False

            # Live Workspace - Second VerticalScroll for staging area
            with VerticalScroll(id="staging-container") as staging_scroll:
                staging_scroll.can_focus = False

            # Input area - V3's exact pattern
            yield PromptInput(id="prompt-input")

    # Disable mouse capture to restore terminal text selection
    def on_mouse_down(self, event) -> None:
        """Override to disable mouse capture - allows terminal text selection"""
        pass

    def on_mouse_up(self, event) -> None:
        """Override to disable mouse capture - allows terminal text selection"""
        pass

    def on_mouse_move(self, event) -> None:
        """Override to disable mouse capture - allows terminal text selection"""
        pass

    def on_mount(self) -> None:
        """Initialize the application and wire components"""
        # Set production mode for smooth 60fps animations
        AnimationClock.set_production_mode()

        # Register all custom themes first
        self._register_all_themes()

        # Set the saved theme
        self.theme = self._current_theme

        # Initialize UI components - V3's exact pattern
        self.prompt_input = self.query_one("#prompt-input", PromptInput)

        # Add welcome message using V3's pattern
        from .widgets.chatbox import Chatbox

        welcome_chatbox = Chatbox(AppConfig.WELCOME_MESSAGE, role="system")
        self.chat_container.mount(welcome_chatbox)

        # Add staging area mockup
        staging_items = [
            "🎯 Route Query → Determining intent...",
            "🛠️ Tool Selection → Selecting tools...",
            "📝 Response Generation → Generating...",
        ]
        for item in staging_items:
            staging_chatbox = Chatbox(item, role="system")
            self.staging_container.mount(staging_chatbox)

        # Set focus to input area
        self.prompt_input.focus()

    @property
    def chat_container(self) -> VerticalScroll:
        """V3's exact chat container property"""
        return self.query_one("#chat-container", VerticalScroll)

    @property
    def staging_container(self) -> VerticalScroll:
        """Staging area container for live cognition"""
        return self.query_one("#staging-container", VerticalScroll)

    def on_prompt_input_prompt_submitted(
        self, event: PromptInput.PromptSubmitted
    ) -> None:
        """Handle user input submission - V3's exact pattern"""

        async def safe_process():
            try:
                from .widgets.chatbox import Chatbox

                # Add user message using V3's pattern
                user_chatbox = Chatbox(event.text, role="user")
                await self.chat_container.mount(user_chatbox)

                # V3's scroll to latest message
                self.chat_container.refresh()
                self.chat_container.scroll_end(animate=False, force=True)

                # Generate response
                response = await self.response_generator.generate_response_async(
                    event.text
                )

                # Add assistant response using V3's pattern
                assistant_chatbox = Chatbox(response, role="assistant")
                self.chat_container.mount(assistant_chatbox)

                # V3's smart scrolling - only scroll if already near bottom
                scroll_y = self.chat_container.scroll_y
                max_scroll_y = self.chat_container.max_scroll_y
                if scroll_y in range(max_scroll_y - 3, max_scroll_y + 1):
                    self.chat_container.scroll_end(animate=False)

            except Exception as e:
                # Simple error handling
                error_chatbox = Chatbox(f"❌ Error: {str(e)}", role="system")
                self.chat_container.mount(error_chatbox)

        self.run_worker(safe_process(), name="process_input")

    def action_do_nothing(self) -> None:
        """Action that does nothing - used to disable Ctrl+Q"""
        pass

    def on_key(self, event: events.Key) -> None:
        """Global key handler - redirect all typing to prompt input"""
        # Handle Ctrl+C globally for quit
        if event.key == "ctrl+c":
            self.exit()
            return

        # Let other bindings work normally (Ctrl+Q, Ctrl+P, etc.)
        if event.key.startswith("ctrl+") or event.key.startswith("f"):
            return

        # Let Enter and Shift+Enter be handled by the prompt input widget
        # Stop propagation to prevent interference
        if event.key in ["enter", "shift+enter"]:
            if self.prompt_input and self.prompt_input.has_focus:
                # The prompt input will handle these keys
                event.stop()
            return

        # Get the prompt input widget
        if not self.prompt_input:
            return

        # Check if the prompt input already has focus - if so, let it handle normally
        if self.prompt_input.has_focus:
            return

        # For printable characters, redirect to prompt input
        if event.is_printable and event.character:
            # Stop event from propagating to other widgets
            event.stop()

            # Focus the prompt input and let it handle the key
            self.prompt_input.focus()

            # Insert the character
            current_value = self.prompt_input.text
            cursor_row, cursor_col = self.prompt_input.cursor_location
            lines = current_value.split("\n")

            # Insert character at cursor position
            if cursor_row < len(lines):
                line = lines[cursor_row]
                new_line = line[:cursor_col] + event.character + line[cursor_col:]
                lines[cursor_row] = new_line
                self.prompt_input.text = "\n".join(lines)
                # Move cursor forward
                self.prompt_input.cursor_location = (cursor_row, cursor_col + 1)

        # Handle backspace globally
        elif event.key == "backspace":
            event.stop()
            self.prompt_input.focus()

            current_value = self.prompt_input.text
            if current_value:
                cursor_row, cursor_col = self.prompt_input.cursor_location
                lines = current_value.split("\n")

                if cursor_row < len(lines) and cursor_col > 0:
                    # Remove character before cursor
                    line = lines[cursor_row]
                    new_line = line[: cursor_col - 1] + line[cursor_col:]
                    lines[cursor_row] = new_line
                    self.prompt_input.text = "\n".join(lines)
                    self.prompt_input.cursor_location = (cursor_row, cursor_col - 1)
                elif cursor_row > 0 and cursor_col == 0:
                    # At beginning of line, merge with previous line
                    current_line = lines[cursor_row]
                    prev_line = lines[cursor_row - 1]
                    new_cursor_col = len(prev_line)
                    lines[cursor_row - 1] = prev_line + current_line
                    lines.pop(cursor_row)
                    self.prompt_input.text = "\n".join(lines)
                    self.prompt_input.cursor_location = (cursor_row - 1, new_cursor_col)


def main():
    """Entry point for the application"""
    # SAFETY: Prevent accidental GUI runs in Claude Code environment
    import os

    if os.environ.get("CLAUDE_CODE_SESSION"):
        print("❌ ERROR: Cannot run GUI app in Claude Code environment!")
        print("This would corrupt the Claude Code interface.")
        print("Please run manually: `pdm run python -m src.main`")
        return

    app = LLMReplApp()
    app.run()


if __name__ == "__main__":
    main()
