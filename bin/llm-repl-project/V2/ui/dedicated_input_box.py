#!/usr/bin/env python3
"""
Dedicated Input Box - Claude Code Style Interface

This creates a persistent input box at the bottom of the screen, similar to 
Claude Code's architecture. The input box:
- Occupies bottom 10-15% of screen
- Always enclosed in a box (plugin-like visual)
- No title, but always shows ">" prompt inside
- Auto-expands as text wraps to multiple lines
- Shift+Enter adds newlines, Enter sends query
- Architecturally separate from timeline content
"""

import asyncio
from typing import Optional, Callable
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import ROUNDED
from rich.layout import Layout
from rich.live import Live
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.formatted_text import HTML


class DedicatedInputBox:
    """
    Dedicated input box that mimics Claude Code's interface architecture.
    
    This creates a persistent input area at the bottom of the screen that:
    - Is visually distinct from timeline content
    - Always shows a ">" prompt
    - Expands automatically as text wraps
    - Handles multiline input with Shift+Enter
    - Sends queries with Enter
    """
    
    def __init__(self, console: Console):
        self.console = console
        self.current_input = ""
        self.input_lines = [""]
        self.cursor_position = 0
        self.is_active = False
        self.on_submit: Optional[Callable[[str], None]] = None
        
        # Create key bindings
        self.kb = KeyBindings()
        self._setup_key_bindings()
        
        # Create buffer for input
        self.buffer = Buffer()
        
    def _setup_key_bindings(self):
        """Setup key bindings for input box behavior."""
        
        @self.kb.add('enter')
        def send_query(event):
            """Enter sends the query."""
            text = self.buffer.text.strip()
            if text and self.on_submit:
                self.on_submit(text)
                self.buffer.text = ""  # Clear after sending
            event.app.exit()
        
        @self.kb.add('s-enter')  # Shift+Enter
        def add_newline(event):
            """Shift+Enter adds a newline."""
            self.buffer.insert_text('\n')
        
        @self.kb.add('c-c')  # Ctrl+C
        def cancel_input(event):
            """Ctrl+C cancels input."""
            event.app.exit()
        
        @self.kb.add('c-d')  # Ctrl+D
        def exit_program(event):
            """Ctrl+D exits program."""
            if not self.buffer.text.strip():
                event.app.exit()
    
    def create_input_panel(self) -> Panel:
        """
        Create the visual input panel that looks like a plugin box.
        
        Returns Rich Panel with current input text and prompt.
        """
        # Get current input text
        text_content = self.buffer.text if hasattr(self, 'buffer') else ""
        
        # Create content with prompt
        if text_content:
            # Multi-line or single line with content
            lines = text_content.split('\n')
            content_lines = [f"> {lines[0]}"]
            for line in lines[1:]:
                content_lines.append(f"  {line}")  # Indent continuation lines
            content = "\n".join(content_lines)
        else:
            # Empty input - just show prompt
            content = "> "
        
        # Calculate height based on content
        line_count = max(1, content.count('\n') + 1)
        
        # Create panel without title (no title like timeline plugins)
        panel = Panel(
            content,
            box=ROUNDED,
            border_style="white",
            padding=(0, 1),  # Small padding inside
            height=line_count + 2,  # +2 for borders
            expand=False
        )
        
        return panel
    
    async def get_input_async(self, on_submit_callback: Callable[[str], None]) -> None:
        """
        Get input asynchronously with dedicated input box interface.
        
        This creates a persistent input box at the bottom of the screen
        and handles all input until a query is submitted.
        """
        self.on_submit = on_submit_callback
        self.is_active = True
        
        # Create application layout with input area
        input_control = BufferControl(
            buffer=self.buffer,
            input_processors=[],
        )
        
        input_window = Window(
            content=input_control,
            height=lambda: max(1, self.buffer.text.count('\n') + 1),
            wrap_lines=True
        )
        
        # Create layout
        layout = Layout()
        layout.split(
            input_window
        )
        
        # Create application
        app = Application(
            layout=layout,
            key_bindings=self.kb,
            mouse_support=False,
            full_screen=False,
        )
        
        # Run the application
        try:
            await app.run_async()
        finally:
            self.is_active = False
    
    def display_input_box(self) -> None:
        """
        Display the current input box state.
        
        This shows the input box visually but doesn't handle interaction.
        Used for showing the box state during timeline updates.
        """
        panel = self.create_input_panel()
        self.console.print()  # Add spacing
        self.console.print(panel)


class FullscreenInterface:
    """
    Fullscreen interface manager that coordinates timeline and input box.
    
    This creates the Claude Code-style interface where:
    - Top 85-90% is timeline content (scrolling)
    - Bottom 10-15% is dedicated input box (persistent)
    - Input box is visually separate but architecturally integrated
    """
    
    def __init__(self, console: Console, timeline_app):
        self.console = console
        self.timeline_app = timeline_app
        self.input_box = DedicatedInputBox(console)
        self.layout = Layout()
        self.live_display = None
        
    def setup_fullscreen_layout(self):
        """Setup the fullscreen layout with timeline and input areas."""
        # Create layout with timeline (top) and input (bottom)
        self.layout.split_column(
            Layout(name="timeline", ratio=85),    # Timeline gets 85% of screen
            Layout(name="input", ratio=15, minimum_size=3)  # Input gets 15%, min 3 lines
        )
    
    async def start_fullscreen_mode(self, on_input_callback: Callable[[str], None]):
        """
        Start fullscreen mode with persistent input box.
        
        This creates the main interface where timeline content appears
        in the top area and input handling happens in the bottom area.
        """
        self.setup_fullscreen_layout()
        
        # Update input area with current input box
        input_panel = self.input_box.create_input_panel()
        self.layout["input"].update(input_panel)
        
        # Start live display
        with Live(self.layout, console=self.console, refresh_per_second=10) as live:
            self.live_display = live
            
            # Handle input in dedicated box
            await self.input_box.get_input_async(on_input_callback)
    
    def update_timeline_content(self, content):
        """Update the timeline area with new content."""
        if self.live_display and hasattr(self.layout, "timeline"):
            self.layout["timeline"].update(content)
    
    def update_input_box(self):
        """Update the input box display."""
        if self.live_display and hasattr(self.layout, "input"):
            input_panel = self.input_box.create_input_panel()
            self.layout["input"].update(input_panel)


class SimpleInputBox:
    """
    Simplified input box for non-fullscreen mode.
    
    This provides the input box functionality without the complex
    fullscreen layout, for testing and simpler interfaces.
    """
    
    def __init__(self, console: Console):
        self.console = console
    
    def display_input_prompt(self):
        """Display input prompt as a simple box (full screen width)."""
        panel = Panel(
            "> ",
            box=ROUNDED,
            border_style="white",
            padding=(0, 1),
            expand=True  # Full screen width
        )
        self.console.print()
        self.console.print(panel)
    
    async def get_simple_input(self) -> Optional[str]:
        """Get input using simple method with dedicated input box display."""
        import sys
        
        try:
            # Always show the input box (even in non-interactive mode for visual consistency)
            self.display_input_prompt()
            
            if sys.stdin.isatty():
                # Interactive mode: get input without echo to prevent timeline pollution
                try:
                    # Use termios to get input without echo
                    import termios
                    import tty
                    fd = sys.stdin.fileno()
                    old_settings = termios.tcgetattr(fd)
                    try:
                        tty.setcbreak(fd)  # No echo mode
                        line = ""
                        last_update = ""
                        
                        while True:
                            char = sys.stdin.read(1)
                            if char == '\n' or char == '\r':
                                break
                            elif char == '\x03':  # Ctrl+C
                                raise KeyboardInterrupt
                            elif char == '\x04':  # Ctrl+D
                                raise EOFError
                            elif char == '\x7f':  # Backspace
                                if line:
                                    line = line[:-1]
                                    # Only update display if significant change
                                    if len(line) != len(last_update) or line != last_update:
                                        self._update_input_display_live(line)
                                        last_update = line
                            else:
                                line += char
                                # Only update display every few characters to reduce flashing
                                if len(line) % 3 == 0 or len(line) < 5:
                                    self._update_input_display_live(line)
                                    last_update = line
                        
                        # Final update to show complete input
                        if line != last_update:
                            self._update_input_display_live(line)
                        
                        return line.strip() if line else None
                    finally:
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                except (ImportError, OSError):
                    # Fallback for systems without termios - use standard input
                    # This will still echo but it's better than no functionality
                    result = input()
                    if result.strip():
                        self._update_input_display(result.strip())
                    return result.strip() if result else None
            else:
                # Non-interactive mode (like pexpect tests)
                result = sys.stdin.readline()
                if result and result.strip():
                    self._update_input_display(result.strip())
                return result.strip() if result else None
                
        except (KeyboardInterrupt, EOFError):
            return None
    
    def _update_input_display_live(self, current_input: str):
        """Update the input box in real-time as user types."""
        # Only update on significant changes (not every character)
        # This reduces flashing and improves performance
        
        # Move cursor up to overwrite the current input box (properly hidden)
        print(f"\033[3A\033[K", end="", flush=True)  # Move up 3 lines and clear
        
        # Display updated input box with current input (full screen width)
        content = f"> {current_input}" if current_input else "> "
        
        # Handle multiline text - wrap long lines
        terminal_width = self.console.size.width - 4  # Account for padding and borders
        if len(content) > terminal_width:
            # Text is too long - needs to wrap
            lines = []
            remaining = content
            first_line = True
            
            while remaining:
                if first_line:
                    # First line has "> " prefix
                    if len(remaining) <= terminal_width:
                        lines.append(remaining)
                        break
                    else:
                        lines.append(remaining[:terminal_width])
                        remaining = remaining[terminal_width:]
                        first_line = False
                else:
                    # Continuation lines get indented
                    line_content = "  " + remaining  # 2-space indent
                    if len(line_content) <= terminal_width:
                        lines.append(line_content)
                        break
                    else:
                        lines.append(line_content[:terminal_width])
                        remaining = remaining[terminal_width-2:]  # Account for indent
            
            content = "\n".join(lines)
        
        panel = Panel(
            content,
            box=ROUNDED,
            border_style="white", 
            padding=(0, 1),
            expand=True  # Full screen width
        )
        
        # Print without console.print to avoid Rich formatting issues
        import io
        import sys
        buffer = io.StringIO()
        temp_console = self.console.__class__(file=buffer, width=self.console.size.width)
        temp_console.print(panel)
        output = buffer.getvalue()
        
        # Print directly to stdout to avoid escape sequence issues
        sys.stdout.write(output)
        sys.stdout.flush()
    
    def _update_input_display(self, user_input: str):
        """Update the input box to show the final user input."""
        # Move cursor up to overwrite the current input box
        self.console.print(f"\033[3A", end="")  # Move up 3 lines (box + spacing)
        
        # Display final input box with user's input (full screen width)
        panel = Panel(
            f"> {user_input}",
            box=ROUNDED,
            border_style="white", 
            padding=(0, 1),
            expand=True  # Full screen width
        )
        self.console.print(panel)