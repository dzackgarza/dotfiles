"""
Advanced input system with persistent bottom input box and multiline support.
"""

import asyncio
from typing import Optional, Callable, List
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import ROUNDED
from prompt_toolkit import Application
from prompt_toolkit.application import get_app
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.formatted_text import HTML


class MultilineInputBox:
    """
    A persistent input box that supports multiline input with Shift+Enter.
    """
    
    def __init__(self, console: Console, on_submit: Callable[[str], None] = None):
        self.console = console
        self.on_submit = on_submit or (lambda x: None)
        self.current_input = ""
        self.input_lines: List[str] = [""]
        self.cursor_line = 0
        self.cursor_col = 0
        self.is_active = True
        
        # Create key bindings
        self.kb = KeyBindings()
        self._setup_key_bindings()
        
        # Create text area
        self.text_area = TextArea(
            text="",
            multiline=True,
            wrap_lines=True,
            prompt=HTML('<ansigreen>></ansigreen> '),
            complete_style="column",
            scrollbar=True,
            height=1,  # Start with single line, will expand
        )
        
        # Bind submit handler
        @self.kb.add('enter')
        def submit_input(event):
            """Submit input on Enter (unless Shift+Enter for new line)."""
            if event.key_sequence[0].key == 'enter' and not event.key_sequence[0].shift:
                self._submit_current_input()
            else:
                # Let the text area handle it (new line)
                event.app.current_buffer.insert_text('\n')
        
        @self.kb.add('s-enter')  # Shift+Enter
        def new_line(event):
            """Add new line on Shift+Enter."""
            event.app.current_buffer.insert_text('\n')
            self._update_height()
        
        # Update text area key bindings
        self.text_area.control.key_bindings = self.kb
    
    def _setup_key_bindings(self):
        """Setup key bindings for the input system."""
        
        @self.kb.add('c-c')  # Ctrl+C
        def quit_app(event):
            """Quit the application."""
            event.app.exit()
        
        @self.kb.add('c-d')  # Ctrl+D
        def eof(event):
            """Handle EOF."""
            event.app.exit()
    
    def _submit_current_input(self):
        """Submit the current input."""
        content = self.text_area.text.strip()
        if content:
            self.on_submit(content)
            self.text_area.text = ""
            self._update_height()
    
    def _update_height(self):
        """Update the height of the text area based on content."""
        lines = self.text_area.text.count('\n') + 1
        # Cap at reasonable height
        height = min(max(1, lines), 10)
        self.text_area.height = height
    
    def get_input_panel(self) -> Panel:
        """Get the Rich panel representation of the input box."""
        if not self.text_area.text:
            content = Text("> ", style="green")
        else:
            lines = self.text_area.text.split('\n')
            content = Text()
            for i, line in enumerate(lines):
                if i == 0:
                    content.append("> ", style="green")
                else:
                    content.append("  ", style="green")  # Continuation indent
                content.append(line + "\n")
        
        return Panel(
            content,
            title="Input",
            box=ROUNDED,
            border_style="green",
            height=min(len(self.text_area.text.split('\n')) + 2, 12)  # +2 for borders
        )
    
    async def run_async(self) -> Optional[str]:
        """Run the input system asynchronously and return the submitted text."""
        submitted_text = None
        
        def on_submit(text: str):
            nonlocal submitted_text
            submitted_text = text
            app.exit()
        
        self.on_submit = on_submit
        
        # Create the application layout
        layout = Layout(
            HSplit([
                Window(height=1),  # Spacer
                Window(
                    content=BufferControl(buffer=self.text_area.buffer),
                    height=lambda: max(1, self.text_area.text.count('\n') + 1),
                ),
            ])
        )
        
        # Create application
        app = Application(
            layout=layout,
            key_bindings=self.kb,
            mouse_support=False,  # Disable to allow normal text selection
            full_screen=False,
        )
        
        # Run the application
        await app.run_async()
        
        return submitted_text


class PersistentInputSystem:
    """
    Input system with a persistent bottom input area that doesn't pollute the timeline.
    """
    
    def __init__(self, console: Console):
        self.console = console
        self.input_history: List[str] = []
        self.history_index = -1
    
    async def get_user_input(self, prompt: str = "> ") -> Optional[str]:
        """
        Get user input using the persistent input system.
        Returns None if user wants to quit.
        """
        try:
            # Create and run the input box
            input_box = MultilineInputBox(self.console)
            result = await input_box.run_async()
            
            if result:
                # Add to history
                self.input_history.append(result)
                self.history_index = len(self.input_history)
                
            return result
            
        except (KeyboardInterrupt, EOFError):
            return None
    
    def create_simple_prompt(self) -> str:
        """Create a simple powerline-style prompt."""
        return "> "
    
    def get_input_display_text(self, text: str) -> Text:
        """Format input text for display without the 'You:' prefix."""
        # For multiline input, show it nicely formatted
        lines = text.strip().split('\n')
        if len(lines) == 1:
            return Text(f"> {lines[0]}", style="green")
        else:
            result = Text()
            for i, line in enumerate(lines):
                if i == 0:
                    result.append(f"> {line}\n", style="green")
                else:
                    result.append(f"  {line}\n", style="green")  # Continuation
            return result


# Simpler alternative using prompt_toolkit directly
class SimpleMultilineInput:
    """
    Simplified multiline input using prompt_toolkit with better UX.
    
    Key bindings:
    - Enter: Submit input
    - Ctrl+J: Add new line 
    - Ctrl+C: Cancel/quit
    - Ctrl+D: EOF/quit
    """
    
    def __init__(self):
        self.kb = KeyBindings()
        self._setup_bindings()
    
    def _setup_bindings(self):
        """Setup key bindings for multiline input."""
        
        @self.kb.add('enter')
        def submit_input(event):
            """Submit on Enter."""
            # Regular Enter: submit if buffer is not empty
            buffer = event.app.current_buffer
            if buffer.text.strip():
                buffer.validate_and_handle()
            
        @self.kb.add('c-j')  # Alternative: Ctrl+J for new line
        def explicit_newline(event):
            """Explicit new line on Ctrl+J."""
            event.app.current_buffer.insert_text('\n')
    
    async def get_input(self, message: str = "> ") -> Optional[str]:
        """Get multiline input from user."""
        from prompt_toolkit import PromptSession
        from prompt_toolkit.history import InMemoryHistory
        from prompt_toolkit.styles import Style
        
        style = Style.from_dict({
            'prompt': '#00aa00 bold',
            'input': '#ffffff',
        })
        
        session = PromptSession(
            message=message,
            multiline=True,
            key_bindings=self.kb,
            style=style,
            history=InMemoryHistory(),
            complete_style='column',
            mouse_support=False,  # Disable to allow normal text selection
            erase_when_done=False,  # Don't erase - we'll handle cleanup manually
        )
        
        try:
            # Check if we're in a non-interactive environment
            import sys
            if not sys.stdin.isatty():
                # Read from stdin directly in non-interactive mode
                line = sys.stdin.readline()
                if line:
                    return line.strip()
                else:
                    return None
            
            # Force flush before showing prompt
            sys.stdout.flush()
            
            result = await session.prompt_async()
            
            # Clear the input lines after getting the result
            # This prevents the raw input from appearing above the plugin box
            # NOTE: Disabled for now as it may interfere with prompt display
            # if result and result.strip():
            #     import sys
            #     lines_to_clear = result.count('\n') + 1
            #     for _ in range(lines_to_clear):
            #         sys.stdout.write('\033[1A\033[2K')  # Move up and clear line
            #     sys.stdout.flush()
            
            return result.strip() if result else None
        except (KeyboardInterrupt, EOFError):
            return None