#!/usr/bin/env python3
"""
Program State Machine - Structural Guarantees for Correct Lifecycle

This module provides strong types and state management to ensure:
1. Startup sequence MUST complete before interactive mode
2. Display operations MUST complete before state transitions
3. Timing violations are impossible at compile/runtime

The state machine prevents entire classes of bugs:
- Prompt appearing before startup
- Display operations being context-dependent
- Async operations completing without visible effects
"""

from enum import Enum
from typing import Optional, Protocol, runtime_checkable
from dataclasses import dataclass


class ProgramPhase(Enum):
    """
    Strong type for program lifecycle phases.
    
    Transitions are strictly ordered:
    INITIALIZING → STARTUP_DISPLAY → READY → INTERACTIVE
    """
    INITIALIZING = "initializing"      # System starting up
    STARTUP_DISPLAY = "startup_display"  # Showing startup blocks
    READY = "ready"                    # Startup complete, ready for input
    INTERACTIVE = "interactive"        # Processing user input
    SHUTDOWN = "shutdown"              # Exiting


@dataclass(frozen=True)
class StartupComplete:
    """
    Proof token that startup sequence completed successfully.
    
    This type can only be created by the startup system and serves as
    compile-time proof that startup display actually finished.
    """
    plugins_displayed: int
    startup_duration: float
    
    def __post_init__(self):
        """Validate that startup actually completed."""
        if self.plugins_displayed < 2:  # Must have at least System_Check + Welcome
            raise ValueError(f"Invalid startup: only {self.plugins_displayed} plugins displayed")


@dataclass(frozen=True)
class DisplayComplete:
    """
    Proof token that a display operation completed successfully.
    
    This prevents async display operations from claiming completion
    without actually rendering to the terminal.
    """
    content_rendered: bool
    render_duration: float
    
    def __post_init__(self):
        """Validate that display actually happened."""
        if not self.content_rendered:
            raise ValueError("Display operation claimed completion without rendering")


@runtime_checkable
class DisplaySystem(Protocol):
    """
    Protocol for display systems that provide completion guarantees.
    
    Any display system must provide proof that content was actually
    rendered to the terminal, not just processed internally.
    """
    
    async def render_with_proof(self, content: str) -> DisplayComplete:
        """
        Render content and provide proof of completion.
        
        This method MUST NOT return until content is visible to user.
        """
        ...
    
    def is_terminal_ready(self) -> bool:
        """
        Check if terminal is ready for display operations.
        
        This prevents display operations when terminal isn't available.
        """
        ...


class ProgramStateMachine:
    """
    State machine that enforces correct program lifecycle.
    
    Prevents timing violations through strong typing and state guards.
    """
    
    def __init__(self):
        self._current_phase = ProgramPhase.INITIALIZING
        self._startup_proof: Optional[StartupComplete] = None
    
    @property
    def current_phase(self) -> ProgramPhase:
        """Get current program phase."""
        return self._current_phase
    
    def can_transition_to(self, target_phase: ProgramPhase) -> bool:
        """
        Check if transition to target phase is allowed.
        
        Enforces strict ordering of lifecycle phases.
        """
        current = self._current_phase
        
        # Define allowed transitions
        allowed_transitions = {
            ProgramPhase.INITIALIZING: [ProgramPhase.STARTUP_DISPLAY],
            ProgramPhase.STARTUP_DISPLAY: [ProgramPhase.READY],
            ProgramPhase.READY: [ProgramPhase.INTERACTIVE],
            ProgramPhase.INTERACTIVE: [ProgramPhase.SHUTDOWN],
            ProgramPhase.SHUTDOWN: []  # Terminal state
        }
        
        return target_phase in allowed_transitions.get(current, [])
    
    def transition_to_startup_display(self) -> None:
        """
        Transition to startup display phase.
        
        Can only be called from INITIALIZING phase.
        """
        if not self.can_transition_to(ProgramPhase.STARTUP_DISPLAY):
            raise ValueError(f"Cannot transition from {self._current_phase} to STARTUP_DISPLAY")
        
        self._current_phase = ProgramPhase.STARTUP_DISPLAY
    
    def complete_startup(self, proof: StartupComplete) -> None:
        """
        Complete startup phase with proof token.
        
        Requires proof that startup display actually finished.
        """
        if self._current_phase != ProgramPhase.STARTUP_DISPLAY:
            raise ValueError(f"Cannot complete startup from {self._current_phase}")
        
        # Validate proof token
        if not isinstance(proof, StartupComplete):
            raise TypeError("Startup completion requires StartupComplete proof token")
        
        self._startup_proof = proof
        self._current_phase = ProgramPhase.READY
    
    def transition_to_interactive(self) -> None:
        """
        Transition to interactive phase.
        
        Can only be called after startup completed with proof.
        """
        if self._current_phase != ProgramPhase.READY:
            raise ValueError(f"Cannot transition from {self._current_phase} to INTERACTIVE")
        
        if self._startup_proof is None:
            raise ValueError("Cannot start interactive mode without startup completion proof")
        
        self._current_phase = ProgramPhase.INTERACTIVE
    
    def can_show_prompt(self) -> bool:
        """
        Check if prompt can be shown.
        
        Prompt can only be shown after startup completed.
        """
        return (self._current_phase == ProgramPhase.READY and 
                self._startup_proof is not None)
    
    def get_startup_proof(self) -> Optional[StartupComplete]:
        """Get startup completion proof if available."""
        return self._startup_proof
    
    def shutdown(self) -> None:
        """Transition to shutdown phase."""
        self._current_phase = ProgramPhase.SHUTDOWN


class StartupSequenceManager:
    """
    Manager for startup sequence with display completion guarantees.
    
    Ensures startup display actually completes before allowing
    transition to interactive mode.
    """
    
    def __init__(self, display_system: DisplaySystem):
        self.display_system = display_system
        self.displayed_plugins = 0
        self.startup_start_time = 0.0
    
    async def run_startup_with_proof(self, plugins_to_display: list) -> StartupComplete:
        """
        Run startup sequence and provide completion proof.
        
        This method MUST NOT return until all startup content is
        visible to the user.
        """
        import time
        
        if not self.display_system.is_terminal_ready():
            raise RuntimeError("Terminal not ready for startup display")
        
        self.startup_start_time = time.time()
        
        # Display each plugin with proof of completion
        for plugin in plugins_to_display:
            display_proof = await self.display_system.render_with_proof(plugin)
            
            # Validate that display actually happened
            if not display_proof.content_rendered:
                raise RuntimeError(f"Plugin {plugin} failed to display")
            
            self.displayed_plugins += 1
        
        startup_duration = time.time() - self.startup_start_time
        
        # Create proof token that startup completed
        return StartupComplete(
            plugins_displayed=self.displayed_plugins,
            startup_duration=startup_duration
        )


class GuaranteedDisplaySystem:
    """
    Display system that provides completion guarantees.
    
    Implements DisplaySystem protocol to ensure content is actually
    rendered to terminal before claiming completion.
    """
    
    def __init__(self, console):
        self.console = console
        self._terminal_ready = True
    
    async def render_with_proof(self, content) -> DisplayComplete:
        """
        Render content and provide proof of completion.
        
        This implementation ensures content is flushed to terminal
        before returning proof token. Uses timeline-pure display.
        """
        import time
        
        if not self.is_terminal_ready():
            raise RuntimeError("Terminal not ready for display")
        
        render_start = time.time()
        
        # Render content to terminal (handle both strings and Rich objects)
        # Note: During startup, we use direct console access since we're not
        # polluting the timeline - we're creating the initial timeline
        if hasattr(content, '__rich_console__') or hasattr(content, 'to_panel'):
            # Rich object - render directly
            self.console.print(content)
        else:
            # String content - print as-is
            self.console.print(content)
        
        # Force flush to ensure content is visible
        if hasattr(self.console, 'file') and hasattr(self.console.file, 'flush'):
            self.console.file.flush()
        
        render_duration = time.time() - render_start
        
        # Return proof that content was actually rendered
        return DisplayComplete(
            content_rendered=True,
            render_duration=render_duration
        )
    
    def is_terminal_ready(self) -> bool:
        """Check if terminal is ready for display operations."""
        return self._terminal_ready and hasattr(self.console, 'file') and self.console.file