"""Standardized display system for all plugins."""

import time
from typing import Dict, Any, Optional
from datetime import datetime
from .base import PluginState, RenderContext


class PluginDisplayFormatter:
    """Unified display formatter for all plugins."""
    
    @staticmethod
    def format_plugin_title(plugin_name: str, 
                          state: PluginState, 
                          duration: Optional[float] = None,
                          tokens: Optional[Dict[str, int]] = None,
                          animated: bool = False) -> str:
        """
        Format a standardized plugin title with name, timer, and tokens.
        
        Args:
            plugin_name: The name of the plugin
            state: Current plugin state
            duration: Duration in seconds (None for live state)
            tokens: Token counts {"input": int, "output": int}
            animated: Whether to show animated indicators
        
        Returns:
            Formatted title string
        """
        # Base title with plugin name
        title = f"🔧 {plugin_name.title()}"
        
        # Add state-specific indicators
        if state == PluginState.PROCESSING:
            if animated:
                # Animated spinner for live state
                spinner = PluginDisplayFormatter._get_spinner()
                title += f" {spinner}"
            else:
                title += " (processing...)"
        elif state == PluginState.COMPLETED:
            title += " ✅"
        elif state == PluginState.ERROR:
            title += " ❌"
        
        # Add timing information
        if duration is not None:
            title += f" ({duration:.1f}s)"
        elif state == PluginState.PROCESSING and animated:
            # Show live timer
            title += f" ({PluginDisplayFormatter._get_live_timer()}s)"
        
        # Add token information with separate upload/download tracking
        if tokens:
            input_tokens = tokens.get("input", 0)
            output_tokens = tokens.get("output", 0)
            total_tokens = input_tokens + output_tokens
            
            if total_tokens > 0:
                if animated and state == PluginState.PROCESSING:
                    # Animated token counter
                    title += f" [{PluginDisplayFormatter._get_animated_tokens(total_tokens)}]"
                else:
                    # Show separate upload/download tokens
                    if input_tokens > 0 and output_tokens > 0:
                        title += f" [↑{input_tokens} ↓{output_tokens}]"
                    elif input_tokens > 0:
                        title += f" [↑{input_tokens}]"
                    elif output_tokens > 0:
                        title += f" [↓{output_tokens}]"
        
        return title
    
    @staticmethod
    def _get_spinner() -> str:
        """Get animated spinner character."""
        spinners = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        return spinners[int(time.time() * 4) % len(spinners)]
    
    @staticmethod
    def _get_live_timer() -> str:
        """Get animated live timer."""
        # This would typically be calculated from start time
        return f"{time.time() % 60:.1f}"
    
    @staticmethod
    def _get_animated_tokens(count: int) -> str:
        """Get animated token counter."""
        if count == 0:
            return "0"
        
        # Add pulsing effect for live token counting
        pulse = "●" if int(time.time() * 2) % 2 else "○"
        return f"{count} {pulse}"
    
    @staticmethod
    def standardize_render_data(render_data: Dict[str, Any], 
                               plugin_name: str,
                               state: PluginState,
                               duration: Optional[float] = None,
                               tokens: Optional[Dict[str, int]] = None,
                               animated: bool = False) -> Dict[str, Any]:
        """
        Standardize render data with uniform title formatting.
        
        Args:
            render_data: Original render data from plugin
            plugin_name: Name of the plugin
            state: Current plugin state
            duration: Duration in seconds
            tokens: Token counts
            animated: Whether to show animated indicators
        
        Returns:
            Standardized render data with uniform title
        """
        # Create standardized title
        title = PluginDisplayFormatter.format_plugin_title(
            plugin_name, state, duration, tokens, animated
        )
        
        # Update render data with standardized title
        render_data["title"] = title
        
        # Add standard timing metadata
        render_data["timing"] = {
            "duration": duration,
            "state": state.value,
            "animated": animated
        }
        
        # Add standard token metadata
        if tokens:
            render_data["tokens"] = tokens
        
        # Ensure consistent style structure
        if "style" not in render_data:
            render_data["style"] = {}
        
        # Add state-specific styling
        if state == PluginState.PROCESSING:
            render_data["style"]["border_color"] = "yellow"
            render_data["style"]["show_spinner"] = animated
        elif state == PluginState.COMPLETED:
            render_data["style"]["border_color"] = "green"
        elif state == PluginState.ERROR:
            render_data["style"]["border_color"] = "red"
        else:
            render_data["style"]["border_color"] = "blue"
        
        return render_data


class PluginTimer:
    """Timer utility for plugins."""
    
    def __init__(self):
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
    
    def start(self) -> None:
        """Start the timer."""
        self.start_time = datetime.now()
    
    def stop(self) -> None:
        """Stop the timer."""
        self.end_time = datetime.now()
    
    def get_duration(self) -> Optional[float]:
        """Get duration in seconds."""
        if not self.start_time:
            return None
        
        end_time = self.end_time or datetime.now()
        return (end_time - self.start_time).total_seconds()
    
    def get_live_duration(self) -> float:
        """Get live duration (current time - start time)."""
        if not self.start_time:
            return 0.0
        
        return (datetime.now() - self.start_time).total_seconds()


class PluginTokenCounter:
    """Token counter utility for plugins."""
    
    def __init__(self):
        self.input_tokens = 0
        self.output_tokens = 0
    
    def add_input_tokens(self, count: int) -> None:
        """Add input tokens."""
        self.input_tokens += count
    
    def add_output_tokens(self, count: int) -> None:
        """Add output tokens."""
        self.output_tokens += count
    
    def get_counts(self) -> Dict[str, int]:
        """Get token counts."""
        return {
            "input": self.input_tokens,
            "output": self.output_tokens
        }
    
    def get_total(self) -> int:
        """Get total token count."""
        return self.input_tokens + self.output_tokens
    
    def reset(self) -> None:
        """Reset token counts."""
        self.input_tokens = 0
        self.output_tokens = 0