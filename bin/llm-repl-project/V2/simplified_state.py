#!/usr/bin/env python3
"""
Simplified State Management - Event-Driven Architecture

DIFFERENTIAL CHANGE: Replace complex state machines with simple event-driven system
while preserving architectural guarantees.

PRESERVED:
- Startup-before-prompt guarantee
- Timeline integrity
- Type safety

SIMPLIFIED:
- No complex proof tokens
- No multi-phase state machines
- Event-driven lifecycle
"""

from dataclasses import dataclass
from typing import Dict, Any, Callable, List, Optional
from enum import Enum
import asyncio
import time


class AppEvent(Enum):
    """Simple application events."""
    SYSTEM_INITIALIZED = "system_initialized"
    STARTUP_COMPLETE = "startup_complete"
    USER_INPUT_RECEIVED = "user_input_received"
    PROCESSING_COMPLETE = "processing_complete"
    ERROR_OCCURRED = "error_occurred"


@dataclass
class EventData:
    """Event data container."""
    event_type: AppEvent
    data: Dict[str, Any]
    timestamp: float
    source: str


class EventBus:
    """Simple event bus for application coordination."""
    
    def __init__(self):
        self._handlers: Dict[AppEvent, List[Callable]] = {}
        self._event_history: List[EventData] = []
    
    def subscribe(self, event_type: AppEvent, handler: Callable):
        """Subscribe to an event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
    
    async def emit(self, event_type: AppEvent, data: Dict[str, Any], source: str = "unknown"):
        """Emit an event to all subscribers."""
        event_data = EventData(event_type, data, time.time(), source)
        self._event_history.append(event_data)
        
        handlers = self._handlers.get(event_type, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event_data)
                else:
                    handler(event_data)
            except Exception as e:
                # Log error but don't break other handlers
                print(f"Error in event handler: {e}")
    
    def has_occurred(self, event_type: AppEvent) -> bool:
        """Check if an event has occurred."""
        return any(event.event_type == event_type for event in self._event_history)
    
    def get_event_data(self, event_type: AppEvent) -> Optional[EventData]:
        """Get the most recent event data for a type."""
        for event in reversed(self._event_history):
            if event.event_type == event_type:
                return event
        return None


class SimplifiedAppState:
    """
    Simplified application state with event-driven guarantees.
    
    DIFFERENTIAL IMPROVEMENT:
    - Replaces complex state machine with simple event checking
    - Preserves startup-before-prompt guarantee
    - Much easier to test and debug
    """
    
    def __init__(self):
        self.event_bus = EventBus()
        self._startup_plugins_count = 0
        
        # Subscribe to our own events for state tracking
        self.event_bus.subscribe(AppEvent.STARTUP_COMPLETE, self._on_startup_complete)
    
    def can_show_prompt(self) -> bool:
        """
        Simple check: can only show prompt after startup complete.
        
        PRESERVED GUARANTEE: Startup-before-prompt
        SIMPLIFIED: No complex proof tokens needed
        """
        return self.event_bus.has_occurred(AppEvent.STARTUP_COMPLETE)
    
    async def mark_system_initialized(self):
        """Mark system as initialized."""
        await self.event_bus.emit(AppEvent.SYSTEM_INITIALIZED, {}, "app_state")
    
    async def mark_startup_complete(self, plugins_count: int):
        """Mark startup as complete."""
        await self.event_bus.emit(
            AppEvent.STARTUP_COMPLETE, 
            {"plugins_count": plugins_count}, 
            "app_state"
        )
    
    async def mark_user_input(self, input_text: str):
        """Mark user input received."""
        await self.event_bus.emit(
            AppEvent.USER_INPUT_RECEIVED, 
            {"input": input_text}, 
            "user"
        )
    
    async def mark_processing_complete(self, result: Any):
        """Mark processing complete."""
        await self.event_bus.emit(
            AppEvent.PROCESSING_COMPLETE, 
            {"result": result}, 
            "processor"
        )
    
    def _on_startup_complete(self, event_data: EventData):
        """Handle startup complete event."""
        self._startup_plugins_count = event_data.data.get("plugins_count", 0)
    
    def get_startup_info(self) -> Dict[str, Any]:
        """Get startup information."""
        startup_event = self.event_bus.get_event_data(AppEvent.STARTUP_COMPLETE)
        if startup_event:
            return {
                "completed": True,
                "plugins_count": startup_event.data.get("plugins_count", 0),
                "timestamp": startup_event.timestamp
            }
        return {"completed": False}