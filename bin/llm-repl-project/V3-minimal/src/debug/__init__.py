"""Debug command provider for Ctrl+P menu"""

from textual.command import Command, CommandPalette, Hit, Hits, Provider
from typing import Iterator


class DebugCommandProvider(Provider):
    """Debug commands for development and troubleshooting"""

    async def search(self, query: str) -> Hits:
        """Search for debug commands"""
        
        def make_hit(name: str, description: str, command_name: str) -> Hit:
            """Create a command hit"""
            def run_command() -> None:
                self.app.action_debug_command(command_name)
            
            return Hit(
                score=1.0,
                match_display=name,
                command=run_command,
            )

        commands = [
            ("Screenshot", "Take debug screenshot", "screenshot"),
            ("Clear Timeline", "Clear conversation timeline", "clear_timeline"),
            ("Show Widget Tree", "Display widget hierarchy", "widget_tree"),
            ("Toggle Debug Mode", "Enable/disable debug logging", "toggle_debug"),
            ("Export Logs", "Export debug logs to file", "export_logs"),
            ("Reset Layout", "Reset widget layout", "reset_layout"),
            ("Memory Usage", "Show memory usage stats", "memory_stats"),
            ("Theme Info", "Show current theme details", "theme_info"),
        ]

        matcher = self.matcher(query)
        
        for name, description, command_name in commands:
            if not query or matcher.match(name):
                yield make_hit(name, description, command_name)


def action_debug_command(self, command: str) -> None:
    """Handle debug commands - to be added to LLMReplApp"""
    if command == "screenshot":
        filename = self.create_debug_screenshot("manual")
        self.notify(f"Screenshot saved: {filename}")
        
    elif command == "clear_timeline":
        try:
            container = self.chat_container
            container.clear_timeline()
            self.notify("Timeline cleared")
        except Exception as e:
            self.notify(f"Error clearing timeline: {e}")
            
    elif command == "widget_tree":
        tree = self._get_widget_tree()
        self.log(f"Widget tree:\n{tree}")
        self.notify("Widget tree logged (check console)")
        
    elif command == "toggle_debug":
        # Toggle debug logging
        import logging
        logger = logging.getLogger()
        if logger.level == logging.DEBUG:
            logger.setLevel(logging.INFO)
            self.notify("Debug logging disabled")
        else:
            logger.setLevel(logging.DEBUG)
            self.notify("Debug logging enabled")
            
    elif command == "export_logs":
        self.notify("Log export not implemented yet")
        
    elif command == "reset_layout":
        self.notify("Layout reset not implemented yet")
        
    elif command == "memory_stats":
        try:
            import psutil
            import os
            process = psutil.Process(os.getpid())
            memory_mb = process.memory_info().rss / 1024 / 1024
            self.notify(f"Memory usage: {memory_mb:.1f} MB")
        except ImportError:
            self.notify("psutil not available")
            
    elif command == "theme_info":
        self.notify(f"Current theme: {self._current_theme}")
        
    else:
        self.notify(f"Unknown debug command: {command}")

def _get_widget_tree(self, widget=None, indent=0) -> str:
    """Get widget hierarchy as string - to be added to LLMReplApp"""
    if widget is None:
        widget = self
        
    result = "  " * indent + f"{widget.__class__.__name__} (id={widget.id})\n"
    
    for child in widget.children:
        result += self._get_widget_tree(child, indent + 1)
        
    return result