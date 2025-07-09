#!/usr/bin/env python3
"""
Scrivener - Event Ordering System

The scrivener ensures that all display events are inscribed in the correct
cognitive order, regardless of when async operations complete.

Key principles:
1. All display events go through the scrivener
2. Events are inscribed in cognitive order, not completion order
3. The scrivener maintains canonical block state
4. Async operations can run in parallel but display is serialized
"""

import asyncio
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod

class EventType(Enum):
    """Types of events that can be inscribed."""
    USER_INPUT = auto()
    INTERNAL_PROCESSING_START = auto()
    INTERNAL_PROCESSING_COMPLETE = auto()
    PROCESSING_START = auto()
    PROCESSING_COMPLETE = auto()
    COGNITION_BLOCK = auto()
    COGNITION_SUB_BLOCK = auto()
    ASSISTANT_RESPONSE = auto()
    SYSTEM_MESSAGE = auto()
    GOODBYE = auto()

@dataclass
class InscriptionEvent:
    """An event to be inscribed by the scrivener."""
    event_type: EventType
    content: str
    timestamp: float = field(default_factory=time.time)
    sequence_number: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Ensure timestamp is set."""
        if self.timestamp == 0:
            self.timestamp = time.time()

class DisplayInterface(ABC):
    """Interface for displaying inscribed events."""
    
    @abstractmethod
    def display_user_input(self, content: str, metadata: Dict[str, Any]) -> None:
        """Display user input."""
        pass
    
    @abstractmethod
    def display_internal_processing_start(self, content: str, metadata: Dict[str, Any]) -> None:
        """Display internal processing container start."""
        pass
    
    @abstractmethod
    def display_internal_processing_complete(self, content: str, metadata: Dict[str, Any]) -> None:
        """Display internal processing container complete."""
        pass
    
    @abstractmethod
    def display_processing_start(self, content: str, metadata: Dict[str, Any]) -> None:
        """Display processing start."""
        pass
    
    @abstractmethod
    def display_processing_complete(self, content: str, metadata: Dict[str, Any]) -> None:
        """Display processing complete."""
        pass
    
    @abstractmethod
    def display_cognition_block(self, content: str, metadata: Dict[str, Any]) -> None:
        """Display cognition block."""
        pass
    
    @abstractmethod
    def display_cognition_sub_block(self, content: str, metadata: Dict[str, Any]) -> None:
        """Display cognition sub-block."""
        pass
    
    @abstractmethod
    def display_assistant_response(self, content: str, metadata: Dict[str, Any]) -> None:
        """Display assistant response."""
        pass
    
    @abstractmethod
    def display_system_message(self, content: str, metadata: Dict[str, Any]) -> None:
        """Display system message."""
        pass
    
    @abstractmethod
    def display_goodbye(self, content: str, metadata: Dict[str, Any]) -> None:
        """Display goodbye message."""
        pass

class Scrivener:
    """
    The scrivener ensures all events are inscribed in correct cognitive order.
    
    This is the single source of truth for the order of events. All display
    operations go through the scrivener to prevent race conditions.
    """
    
    def __init__(self, display_interface: DisplayInterface):
        self.display_interface = display_interface
        self.event_queue: asyncio.Queue[InscriptionEvent] = asyncio.Queue()
        self.sequence_counter = 0
        self.running = False
        self.inscription_task: Optional[asyncio.Task] = None
        
        # Historical record of all inscribed events
        self.chronicle: List[InscriptionEvent] = []
        
        # Current state tracking
        self.current_processing_id: Optional[str] = None
        self.pending_events: Dict[str, List[InscriptionEvent]] = {}
        
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
        await self.event_queue.put(InscriptionEvent(
            event_type=EventType.GOODBYE,
            content="Scrivener stopping",
            metadata={"internal": True}
        ))
        
        if self.inscription_task:
            await self.inscription_task
            
    async def inscribe(self, event: InscriptionEvent) -> None:
        """Queue an event for inscription."""
        if not self.running:
            return
            
        # Assign sequence number
        event.sequence_number = self.sequence_counter
        self.sequence_counter += 1
        
        # Queue for inscription
        await self.event_queue.put(event)
        
    async def _inscription_loop(self) -> None:
        """Main inscription loop - processes events in order."""
        while self.running:
            try:
                # Get next event (blocks until available)
                event = await asyncio.wait_for(self.event_queue.get(), timeout=1.0)
                
                # Skip internal events
                if event.metadata.get("internal", False):
                    continue
                
                # Inscribe the event
                await self._inscribe_event(event)
                
                # Add to chronicle
                self.chronicle.append(event)
                
            except asyncio.TimeoutError:
                # No events for 1 second - continue loop
                continue
            except Exception as e:
                # Log error but continue
                print(f"Scrivener error: {e}")
                continue
                
    async def _inscribe_event(self, event: InscriptionEvent) -> None:
        """Inscribe a single event using the display interface."""
        try:
            if event.event_type == EventType.USER_INPUT:
                self.display_interface.display_user_input(event.content, event.metadata)
                
            elif event.event_type == EventType.INTERNAL_PROCESSING_START:
                self.display_interface.display_internal_processing_start(event.content, event.metadata)
                
            elif event.event_type == EventType.INTERNAL_PROCESSING_COMPLETE:
                self.display_interface.display_internal_processing_complete(event.content, event.metadata)
                
            elif event.event_type == EventType.PROCESSING_START:
                self.display_interface.display_processing_start(event.content, event.metadata)
                
            elif event.event_type == EventType.PROCESSING_COMPLETE:
                self.display_interface.display_processing_complete(event.content, event.metadata)
                
            elif event.event_type == EventType.COGNITION_BLOCK:
                self.display_interface.display_cognition_block(event.content, event.metadata)
                
            elif event.event_type == EventType.COGNITION_SUB_BLOCK:
                self.display_interface.display_cognition_sub_block(event.content, event.metadata)
                
            elif event.event_type == EventType.ASSISTANT_RESPONSE:
                self.display_interface.display_assistant_response(event.content, event.metadata)
                
            elif event.event_type == EventType.SYSTEM_MESSAGE:
                self.display_interface.display_system_message(event.content, event.metadata)
                
            elif event.event_type == EventType.GOODBYE:
                self.display_interface.display_goodbye(event.content, event.metadata)
                
        except Exception as e:
            print(f"Error inscribing event {event.event_type}: {e}")
            
    def get_chronicle(self) -> List[InscriptionEvent]:
        """Get the complete chronicle of inscribed events."""
        return self.chronicle.copy()
        
    def get_current_state(self) -> Dict[str, Any]:
        """Get current state summary."""
        return {
            "running": self.running,
            "events_inscribed": len(self.chronicle),
            "sequence_counter": self.sequence_counter,
            "current_processing": self.current_processing_id
        }

# Example Rich UI Display Interface
class RichDisplayInterface(DisplayInterface):
    """Rich UI implementation of display interface."""
    
    def __init__(self, rich_ui=None, console=None):
        self.rich_ui = rich_ui
        self.console = console
        
        # V1-style Internal Processing container state
        self.internal_processing_active = False
        self.internal_processing_content = []
        self.internal_processing_start_time = None
        self.internal_processing_metadata = {}
        
    def display_user_input(self, content: str, metadata: Dict[str, Any]) -> None:
        """Display user input with Rich UI."""
        if self.rich_ui:
            try:
                self.rich_ui.print_user_message(content)
            except Exception:
                print(f"You: {content}")
        else:
            print(f"You: {content}")
            
    def display_internal_processing_start(self, content: str, metadata: Dict[str, Any]) -> None:
        """Start the Internal Processing container - V1 style."""
        import time
        self.internal_processing_active = True
        self.internal_processing_content = []
        self.internal_processing_start_time = time.time()
        self.internal_processing_metadata = metadata
        
        # Display the initial Internal Processing container immediately
        if self.rich_ui:
            try:
                from rich.text import Text
                from rich.panel import Panel
                from rich.box import ROUNDED
                
                # Create initial empty container
                initial_content = Text()
                initial_content.append("\\n")
                initial_content.append("   Processing...", style="dim white")
                initial_content.append("\\n")
                
                # Create the main Internal Processing panel
                internal_panel = Panel(
                    initial_content,
                    title=f"[dim yellow]⚙️ Internal Processing (running...)[/dim yellow]",
                    box=ROUNDED,
                    border_style="dim yellow",
                    padding=(0, 1),
                    expand=True  # Use full width
                )
                self.console.print(internal_panel)
                
            except Exception as e:
                print(f"Internal Processing: {content} (starting...)")
        else:
            print(f"Internal Processing: {content} (starting...)")
        
    def display_internal_processing_complete(self, content: str, metadata: Dict[str, Any]) -> None:
        """Complete and display the Internal Processing container - V1 style."""
        if not self.internal_processing_active:
            return
            
        if self.rich_ui:
            try:
                import time
                total_duration = time.time() - self.internal_processing_start_time
                
                # Create V1-style Internal Processing container
                from rich.text import Text
                from rich.panel import Panel
                from rich.box import ROUNDED
                
                # Create nested content using a Group to combine panels
                from rich.console import Group
                from rich.text import Text
                
                # Build content as a Group of panels and flow indicators
                nested_elements = []
                
                for i, sub_block_panel in enumerate(self.internal_processing_content):
                    # Add the sub-block panel
                    nested_elements.append(sub_block_panel)
                    
                    # Add flow indicator between blocks (except after the last one)
                    if i < len(self.internal_processing_content) - 1:
                        flow_indicator = Text("                                    ▼", style="dim white")
                        nested_elements.append(flow_indicator)
                
                # Create group of all elements
                nested_content = Group(*nested_elements)
                
                # Create the main Internal Processing panel with full width
                internal_panel = Panel(
                    nested_content,
                    title=f"[dim yellow]⚙️ Internal Processing ({total_duration:.1f}s total)[/dim yellow]",
                    box=ROUNDED,
                    border_style="dim yellow",
                    padding=(0, 1),
                    expand=True  # Use full width
                )
                self.console.print(internal_panel)
                
            except Exception as e:
                print(f"Internal Processing: {content} ({e})")
        else:
            print(f"Internal Processing: {content}")
            
        # Reset state
        self.internal_processing_active = False
        self.internal_processing_content = []
            
    def display_processing_start(self, content: str, metadata: Dict[str, Any]) -> None:
        """Display processing start - accumulate for Internal Processing container."""
        # Don't display immediately if we're in Internal Processing mode
        if self.internal_processing_active:
            # Just store the stage info for later use
            stage = metadata.get("stage", "processing")
            self.current_stage = content
            self.current_stage_metadata = metadata
            return
            
        # If not in Internal Processing mode, display immediately (fallback)
        if self.rich_ui:
            try:
                stage = metadata.get("stage", "processing")
                message = metadata.get("message", "Processing...")
                provider_model = metadata.get("provider_model", "")
                
                # Create V1-style processing panel
                from rich.text import Text
                from rich.panel import Panel
                from rich.box import ROUNDED
                from rich.columns import Columns
                from rich.align import Align
                
                # Main content with message
                main_content = Text(message, style="dim white")
                
                # Token counter placeholder (will be updated in real implementation)
                token_text = "⏱️ Processing..."
                if provider_model:
                    token_text += f" {provider_model}"
                token_counter = Align(Text(token_text, style="dim cyan"), align="right")
                
                # Create layout with main content and token counter
                content_layout = Columns([main_content, token_counter], expand=True)
                
                processing_panel = Panel(
                    content_layout,
                    title=f"[dim yellow]{content}[/dim yellow]",
                    box=ROUNDED,
                    border_style="dim yellow",
                    padding=(0, 1)
                )
                self.console.print(processing_panel)
                
            except Exception:
                print(f"Processing: {content}")
        else:
            print(f"Processing: {content}")
            
    def display_processing_complete(self, content: str, metadata: Dict[str, Any]) -> None:
        """Display processing complete - accumulate for Internal Processing container."""
        if self.internal_processing_active:
            # Create simple nested sub-block text representation
            try:
                stage = metadata.get("stage", "processing")
                routing_conclusion = metadata.get("routing_conclusion", "")
                tokens_sent = metadata.get("tokens_sent", 0)
                tokens_received = metadata.get("tokens_received", 0)
                duration = metadata.get("duration", 0.0)
                
                # Create the nested sub-block as a Rich Panel instead of raw text
                from rich.text import Text
                from rich.panel import Panel
                from rich.box import ROUNDED
                from rich.columns import Columns
                from rich.align import Align
                
                # Get the current message
                message = getattr(self, 'current_stage_metadata', {}).get("message", "Processing...")
                
                # Create content for the sub-block panel
                panel_content = Text()
                panel_content.append(f"{message} ({duration:.1f}s)\n", style="dim white")
                panel_content.append(routing_conclusion, style="dim white")
                
                # Create token info
                token_text = f"⏱️ ↑{tokens_sent} ↓{tokens_received}"
                token_counter = Align(Text(token_text, style="dim cyan"), align="right")
                
                # Create layout with main content and token counter
                content_layout = Columns([panel_content, token_counter], expand=True)
                
                # Create the sub-block as a proper Rich panel
                sub_block_panel = Panel(
                    content_layout,
                    title=f"[dim cyan]{content}[/dim cyan]",
                    box=ROUNDED,
                    border_style="dim cyan",
                    padding=(0, 1),
                    expand=False,  # Don't force full width for sub-blocks
                    width=None     # Let Rich determine optimal width
                )
                
                # Add the sub-block panel to our accumulated content
                self.internal_processing_content.append(sub_block_panel)
                
            except Exception as e:
                print(f"Error creating sub-block: {e}")
            return
            
        # If not in Internal Processing mode, display immediately (fallback)
        if self.rich_ui:
            try:
                stage = metadata.get("stage", "processing")
                routing_conclusion = metadata.get("routing_conclusion", "")
                tokens_sent = metadata.get("tokens_sent", 0)
                tokens_received = metadata.get("tokens_received", 0)
                duration = metadata.get("duration", 0.0)
                
                # Create V1-style completion panel
                from rich.text import Text
                from rich.panel import Panel
                from rich.box import ROUNDED
                from rich.columns import Columns
                from rich.align import Align
                
                # Main content with routing conclusion
                main_content = Text(routing_conclusion, style="dim white")
                
                # Token counter with actual values
                token_text = f"⏱️ ↑{tokens_sent} ↓{tokens_received} ({duration:.1f}s)"
                token_counter = Align(Text(token_text, style="dim cyan"), align="right")
                
                # Create layout with main content and token counter
                content_layout = Columns([main_content, token_counter], expand=True)
                
                completion_panel = Panel(
                    content_layout,
                    title=f"[dim green]{content}[/dim green]",
                    box=ROUNDED,
                    border_style="dim green",
                    padding=(0, 1)
                )
                self.console.print(completion_panel)
                
            except Exception:
                print(f"Complete: {content}")
        else:
            print(f"Complete: {content}")
            
    def display_cognition_block(self, content: str, metadata: Dict[str, Any]) -> None:
        """Display cognition block."""
        if self.rich_ui:
            try:
                state = metadata.get("state", "running")
                sub_blocks = metadata.get("sub_blocks", [])
                
                # Only display cognition block when it's running (first time)
                # When it's inscribed, it's just marking completion but doesn't need display
                if state == "inscribed":
                    return
                
                # Create cognition block panel
                from rich.text import Text
                from rich.panel import Panel
                from rich.box import ROUNDED
                
                cognition_content = Text()
                cognition_content.append(f"🧠 ", style="bold blue")
                cognition_content.append(content, style="bright_white")
                
                if state == "running":
                    cognition_content.append(" ⚡", style="yellow")
                
                # Add sub-blocks if any
                if sub_blocks:
                    cognition_content.append("\n")
                    for i, sub_block in enumerate(sub_blocks):
                        cognition_content.append(f"  • {sub_block}", style="dim white")
                        if i < len(sub_blocks) - 1:
                            cognition_content.append("\n")
                
                cognition_panel = Panel(
                    cognition_content,
                    title="[bold blue]Cognition[/bold blue]",
                    box=ROUNDED,
                    border_style="blue",
                    padding=(0, 1)
                )
                self.console.print(cognition_panel)
                
            except Exception:
                print(f"Cognition: {content}")
        else:
            print(f"Cognition: {content}")
        
    def display_cognition_sub_block(self, content: str, metadata: Dict[str, Any]) -> None:
        """Display cognition sub-block."""
        if self.rich_ui:
            try:
                state = metadata.get("state", "running")
                step = metadata.get("step", 1)
                total = metadata.get("total", 1)
                
                # Create sub-block content
                from rich.text import Text
                from rich.panel import Panel
                from rich.box import ROUNDED
                
                sub_content = Text()
                sub_content.append(f"  [{step}/{total}] ", style="bold cyan")
                sub_content.append(content, style="bright_white")
                
                if state == "running":
                    sub_content.append(" ⚡", style="yellow")
                elif state == "inscribed":
                    sub_content.append(" ✓", style="green")
                
                # Display as indented block
                sub_panel = Panel(
                    sub_content,
                    title=f"[bold cyan]Step {step}[/bold cyan]",
                    box=ROUNDED,
                    border_style="cyan",
                    padding=(0, 1)
                )
                self.console.print(sub_panel)
                
            except Exception:
                print(f"  • {content}")
        else:
            print(f"  • {content}")
            
    def display_assistant_response(self, content: str, metadata: Dict[str, Any]) -> None:
        """Display assistant response."""
        if self.rich_ui:
            try:
                routing_info = metadata.get("routing_info", "")
                self.rich_ui.print_assistant_message(content, routing_info)
            except Exception:
                print(f"Assistant: {content}")
        else:
            print(f"Assistant: {content}")
            
    def display_system_message(self, content: str, metadata: Dict[str, Any]) -> None:
        """Display system message."""
        if self.rich_ui:
            try:
                self.rich_ui.print_system_message(content)
            except Exception:
                print(f"System: {content}")
        else:
            print(f"System: {content}")
            
    def display_goodbye(self, content: str, metadata: Dict[str, Any]) -> None:
        """Display goodbye message."""
        if self.rich_ui:
            try:
                self.rich_ui.print_system_message(content)
            except Exception:
                print(content)
        else:
            print(content)

# Example usage
async def demo_scrivener():
    """Demonstrate the scrivener pattern."""
    print("📜 Scrivener Pattern Demo")
    print("=" * 40)
    
    # Create display interface
    display = RichDisplayInterface()
    
    # Create scrivener
    scrivener = Scrivener(display)
    
    # Start scrivener
    await scrivener.start()
    
    # Simulate events in cognitive order
    await scrivener.inscribe(InscriptionEvent(
        event_type=EventType.USER_INPUT,
        content="Hello there"
    ))
    
    await scrivener.inscribe(InscriptionEvent(
        event_type=EventType.PROCESSING_START,
        content="Processing query..."
    ))
    
    # Simulate async processing delay
    await asyncio.sleep(0.1)
    
    await scrivener.inscribe(InscriptionEvent(
        event_type=EventType.ASSISTANT_RESPONSE,
        content="Hello! How can I help you today?",
        metadata={"routing_info": "1.2s"}
    ))
    
    await scrivener.inscribe(InscriptionEvent(
        event_type=EventType.PROCESSING_COMPLETE,
        content="Query processed successfully",
        metadata={"tokens_sent": 10, "tokens_received": 20, "duration": 1.2}
    ))
    
    await scrivener.inscribe(InscriptionEvent(
        event_type=EventType.GOODBYE,
        content="👋 Goodbye!"
    ))
    
    # Wait for all events to be inscribed
    await asyncio.sleep(0.5)
    
    # Stop scrivener
    await scrivener.stop()
    
    # Show chronicle
    print("\n📚 Chronicle of inscribed events:")
    for i, event in enumerate(scrivener.get_chronicle()):
        print(f"{i+1}. {event.event_type.name}: {event.content[:50]}...")
    
    print("\n✨ Scrivener demo complete!")

if __name__ == "__main__":
    asyncio.run(demo_scrivener())