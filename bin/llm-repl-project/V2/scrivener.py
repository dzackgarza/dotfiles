#!/usr/bin/env python3
"""
Scrivener - Event Ordering and Timeline Management for LLM REPL v3

The scrivener ensures that all display events are inscribed in the correct
cognitive order, regardless of when async operations complete.

Key principles:
1. All timeline events go through the scrivener
2. Events are inscribed in cognitive order, not completion order
3. The scrivener maintains canonical timeline state
4. Only completed plugins are accepted into the timeline
5. Async operations can run in parallel but timeline is serialized
"""

import asyncio
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod

from plugins.base import BlockPlugin, PluginState, RenderContext
from plugins.display import PluginDisplayFormatter

class TimelineEventType(Enum):
    """Types of events that can be inscribed in the timeline."""
    SYSTEM_START = auto()
    USER_INPUT = auto()
    PLUGIN_COMPLETED = auto()
    SYSTEM_END = auto()

@dataclass
class TimelineEvent:
    """An event to be inscribed in the timeline by the scrivener."""
    event_type: TimelineEventType
    plugin_id: str
    plugin: BlockPlugin
    timestamp: float = field(default_factory=time.time)
    sequence_number: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Ensure timestamp is set."""
        if self.timestamp == 0:
            self.timestamp = time.time()

class TimelineDisplayInterface(ABC):
    """Interface for displaying timeline events."""
    
    @abstractmethod
    async def display_plugin_completed(self, plugin: BlockPlugin, metadata: Dict[str, Any]) -> None:
        """Display a completed plugin in the timeline."""
        pass

class RichTimelineDisplay(TimelineDisplayInterface):
    """Rich UI implementation of timeline display."""
    
    def __init__(self, console):
        self.console = console
    
    async def display_plugin_completed(self, plugin: BlockPlugin, metadata: Dict[str, Any]) -> None:
        """Display a completed plugin using Rich UI."""
        # Use the existing rendering system
        context = RenderContext(display_mode="inscribed")
        render_data = await plugin.render(context)
        
        # Extract display info
        title = render_data.get("title", "Plugin")
        content = render_data.get("content", "")
        
        # Handle different plugin types with custom formatting
        if plugin.metadata.name == "system_check":
            if "detailed_results" in render_data:
                content_lines = []
                
                # Format non-LLM results with tab alignment
                for result in render_data["detailed_results"]:
                    status = result['status']
                    name = result['name']
                    message = result['message']
                    
                    # Tab-align the status and message
                    if "Configuration" in name:
                        content_lines.append(f"{status} Configuration:\t{message}")
                    elif "Dependencies" in name:
                        content_lines.append(f"{status} Dependencies:\t{message}")
                    else:
                        content_lines.append(f"{status} {name}:\t{message}")
                
                # Format LLM results as a table
                if "llm_results" in render_data and render_data["llm_results"]:
                    content_lines.append("")  # Empty line before LLM section
                    content_lines.append("LLM Providers:")
                    
                    for llm_result in render_data["llm_results"]:
                        status = llm_result['status']
                        details = llm_result.get('details', {})
                        provider = details.get('provider', 'unknown')
                        model = details.get('model', 'unknown')
                        response_time = details.get('response_time', 0)
                        input_tokens = details.get('input_tokens', 0)
                        output_tokens = details.get('output_tokens', 0)
                        
                        # Format as table row with tab alignment
                        content_lines.append(f"\t{status} {provider:12} {model:20} {response_time:6.1f}s  ↑{input_tokens:3} ↓{output_tokens:3}")
                
                content = "\n".join(content_lines) if content_lines else "System checks completed"
        
        # Handle user input special formatting
        elif plugin.metadata.name == "user_input":
            user_content = render_data.get("content", "")
            # Format multiline input nicely
            if "\n" in user_content:
                lines = user_content.split("\n")
                formatted_lines = []
                for i, line in enumerate(lines):
                    if i == 0:
                        formatted_lines.append(f"> {line}")
                    else:
                        formatted_lines.append(f"  {line}")  # Continuation indent
                content = "\n".join(formatted_lines)
            else:
                content = f"> {user_content}"
        
        # Apply styling based on plugin type
        if plugin.metadata.name == "system_check":
            border_color = "yellow"
        elif plugin.metadata.name == "welcome":
            border_color = "cyan"
        elif plugin.metadata.name == "user_input":
            border_color = "green"
        elif plugin.metadata.name == "cognition":
            border_color = "magenta"
        elif plugin.metadata.name == "assistant_response":
            border_color = "blue"
        else:
            border_color = "white"
        
        # Create and display panel
        from rich.panel import Panel
        from rich.box import ROUNDED
        
        panel = Panel(
            content,
            title=title,
            box=ROUNDED,
            border_style=border_color
        )
        
        self.console.print(panel)
        
        # Handle spacing based on plugin type
        if plugin.metadata.name == "system_check":
            # No gap after system check
            pass
        elif plugin.metadata.name == "welcome":
            # Two gaps after welcome to separate startup from chat
            self.console.print()
            self.console.print()
        elif plugin.metadata.name == "assistant_response":
            # Configurable gap after assistant response (between conversations)
            conversation_spacing = metadata.get('conversation_spacing', 2)
            for _ in range(conversation_spacing):
                self.console.print()
        else:
            # No gaps for other plugins
            pass

class Scrivener:
    """
    The scrivener ensures all timeline events are inscribed in correct cognitive order.
    
    This is the single source of truth for the timeline order. All completed plugins
    go through the scrivener to prevent race conditions and ensure proper ordering.
    """
    
    def __init__(self, display_interface: TimelineDisplayInterface):
        self.display_interface = display_interface
        self.event_queue: asyncio.Queue[TimelineEvent] = asyncio.Queue()
        self.sequence_counter = 0
        self.running = False
        self.inscription_task: Optional[asyncio.Task] = None
        
        # Timeline - the canonical record of all inscribed events
        self.timeline: List[TimelineEvent] = []
        
        # Plugin validation
        self.accepted_plugins: List[str] = []
        
    async def start(self) -> None:
        """Start the scrivener's inscription process."""
        if self.running:
            return
            
        self.running = True
        self.inscription_task = asyncio.create_task(self._inscription_loop())
        
    async def stop(self) -> None:
        """Stop the scrivener gracefully."""
        if not self.running:
            return
            
        self.running = False
        
        # Add a final event to wake up the loop
        await self.event_queue.put(TimelineEvent(
            event_type=TimelineEventType.SYSTEM_END,
            plugin_id="system_end",
            plugin=None,
            metadata={"internal": True}
        ))
        
        if self.inscription_task:
            await self.inscription_task
            
    async def inscribe_plugin(self, plugin: BlockPlugin, metadata: Dict[str, Any] = None) -> bool:
        """
        Request to inscribe a plugin into the timeline.
        
        Scrivener validates:
        1. Plugin is in COMPLETED state
        2. Plugin hasn't been inscribed before
        3. Plugin is inscribed in cognitive order
        """
        if not self.running:
            return False
        
        # Scrivener validation: only completed plugins allowed
        if plugin.state != PluginState.COMPLETED:
            return False
        
        # Prevent duplicate inscriptions
        if plugin.plugin_id in self.accepted_plugins:
            return False
        
        # Create timeline event
        event = TimelineEvent(
            event_type=TimelineEventType.PLUGIN_COMPLETED,
            plugin_id=plugin.plugin_id,
            plugin=plugin,
            metadata=metadata or {}
        )
        
        # Assign sequence number
        event.sequence_number = self.sequence_counter
        self.sequence_counter += 1
        
        # Queue for inscription
        await self.event_queue.put(event)
        
        # Mark as accepted
        self.accepted_plugins.append(plugin.plugin_id)
        
        return True
        
    async def _inscription_loop(self) -> None:
        """Main inscription loop - processes events in chronological order."""
        while self.running:
            try:
                # Get next event (blocks until available)
                event = await asyncio.wait_for(self.event_queue.get(), timeout=1.0)
                
                # Skip internal events
                if event.metadata.get("internal", False):
                    continue
                
                # Inscribe the event
                await self._inscribe_event(event)
                
                # Add to timeline
                self.timeline.append(event)
                
            except asyncio.TimeoutError:
                # No events for 1 second - continue loop
                continue
            except Exception as e:
                # Log error but continue
                print(f"Scrivener error: {e}")
                continue
                
    async def _inscribe_event(self, event: TimelineEvent) -> None:
        """Inscribe a single event using the display interface."""
        try:
            if event.event_type == TimelineEventType.PLUGIN_COMPLETED:
                await self.display_interface.display_plugin_completed(event.plugin, event.metadata)
                
        except Exception as e:
            print(f"Error inscribing event {event.event_type}: {e}")
            
    def get_timeline(self) -> List[TimelineEvent]:
        """Get the complete timeline of inscribed events."""
        return self.timeline.copy()
        
    def get_timeline_plugin_ids(self) -> List[str]:
        """Get list of plugin IDs in timeline order."""
        return [event.plugin_id for event in self.timeline if event.event_type == TimelineEventType.PLUGIN_COMPLETED]
        
    def get_current_state(self) -> Dict[str, Any]:
        """Get current state summary."""
        return {
            "running": self.running,
            "events_inscribed": len(self.timeline),
            "sequence_counter": self.sequence_counter,
            "accepted_plugins": len(self.accepted_plugins)
        }