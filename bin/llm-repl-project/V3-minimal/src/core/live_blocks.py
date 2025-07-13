"""
Live vs Inscribed Block System

Core implementation of the Sacred Timeline's live block concept.
Live blocks are mutable and show real-time updates, then transition to inscribed state.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional, List, Callable
from enum import Enum
import uuid
import asyncio
import time
import threading

from .animation_clock import (
    AnimationClock,
    animate_text_typewriter,
    animate_value_smooth,
)
from .wall_time_tracker import (
    get_wall_time_tracker,
    track_block_creation,
    time_block_stage,
    record_block_tokens,
    complete_block_tracking,
)


@dataclass
class CognitionProgress:
    """Real-time progress tracking for cognition blocks"""

    start_time: float = field(default_factory=time.time)
    total_steps: int = 0
    completed_steps: int = 0
    tokens_input: int = 0
    tokens_output: int = 0

    def __post_init__(self):
        self._timer_running = True
        self._update_callbacks: List[Callable] = []
        self._start_timer_updates()

    @property
    def elapsed_time(self) -> float:
        """Current elapsed time in seconds"""
        return time.time() - self.start_time

    @property
    def progress_percentage(self) -> float:
        """Current progress as 0.0 to 1.0"""
        if self.total_steps == 0:
            return 0.0
        return min(1.0, self.completed_steps / self.total_steps)

    def set_total_steps(self, total: int) -> None:
        """Set total number of steps for progress calculation"""
        self.total_steps = total
        self._notify_update()

    def step_started(self) -> None:
        """Called when a step starts"""
        self._notify_update()

    def step_completed(self, tokens_in: int = 0, tokens_out: int = 0) -> None:
        """Called when a step completes"""
        self.completed_steps += 1
        self.tokens_input += tokens_in
        self.tokens_output += tokens_out
        self._notify_update()

    def add_tokens(self, tokens_in: int = 0, tokens_out: int = 0) -> None:
        """Add tokens without completing a step"""
        self.tokens_input += tokens_in
        self.tokens_output += tokens_out
        self._notify_update()

    def add_update_callback(self, callback: Callable) -> None:
        """Add callback for when progress updates"""
        self._update_callbacks.append(callback)

    def _notify_update(self) -> None:
        """Notify all callbacks of progress update"""
        for callback in self._update_callbacks:
            try:
                callback(self)
            except Exception:
                pass  # Don't let callback errors break progress tracking

    def get_status_line(self, model_name: Optional[str] = None) -> str:
        """Generate single status line for display"""
        progress_bar = "█" * int(self.progress_percentage * 20) + "░" * (
            20 - int(self.progress_percentage * 20)
        )
        percentage = int(self.progress_percentage * 100)

        if model_name:
            # For sub-blocks: show model and progress
            status = "✅ Complete" if percentage == 100 else "⏳ Processing..."
            return (
                f"Model: `{model_name}`\n"
                f"Status: {status}\n"
                f"⏱️ {self.elapsed_time:.1f}s | [{progress_bar}] {percentage}% | "
                f"🔢 {self.tokens_input}↑/{self.tokens_output}↓"
            )
        else:
            # For main cognition blocks: just progress info
            return (
                f"⏱️ {self.elapsed_time:.1f}s | [{progress_bar}] {percentage}% | "
                f"🔢 {self.tokens_input}↑/{self.tokens_output}↓"
            )

    def _start_timer_updates(self) -> None:
        """Start background timer updates at 10Hz for smooth progress"""
        # Skip timer in test environments to avoid callback errors
        import os

        if os.getenv("PYTEST_CURRENT_TEST"):
            return

        def timer_loop():
            while self._timer_running:
                self._notify_update()
                time.sleep(0.1)  # 10Hz updates

        # Start timer in background thread
        timer_thread = threading.Thread(target=timer_loop, daemon=True)
        timer_thread.start()

    def stop_timer(self) -> None:
        """Stop the background timer updates"""
        self._timer_running = False


# Compatibility wrapper for old AnimationRates - will be removed after refactor
class AnimationRates:
    """DEPRECATED: Use AnimationClock instead. This is for backward compatibility only."""

    @classmethod
    def set_test_mode(cls):
        """DEPRECATED: Set animation clock to testing mode instead."""
        AnimationClock.set_testing_mode()

    @classmethod
    def set_production_mode(cls):
        """DEPRECATED: Set animation clock to production mode instead."""
        AnimationClock.set_production_mode()

    @classmethod
    async def sleep(cls, duration: float):
        """DEPRECATED: Use AnimationClock.wait_frame() instead."""
        # Convert duration to approximate frame count
        frames = max(1, int(duration * AnimationClock.get_fps()))
        await AnimationClock.wait_frames(frames)


class BlockState(Enum):
    """States for block lifecycle."""

    LIVE = "live"  # Currently updating, mutable
    TRANSITIONING = "transitioning"  # Moving to inscribed state
    INSCRIBED = "inscribed"  # Permanently added to timeline


@dataclass
class LiveBlockData:
    """Mutable data for live blocks."""

    content: str = ""
    tokens_input: int = 0
    tokens_output: int = 0
    wall_time_seconds: float = 0.0
    progress: float = 0.0  # 0.0 to 1.0
    sub_blocks: List["LiveBlock"] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "tokens_input": self.tokens_input,
            "tokens_output": self.tokens_output,
            "wall_time_seconds": self.wall_time_seconds,
            "progress": self.progress,
            "sub_blocks": [block.to_dict() for block in self.sub_blocks],
            "metadata": self.metadata,
        }


class LiveBlock:
    """A block in live state that can be updated in real-time."""

    def __init__(self, role: str, initial_content: str = ""):
        self.id = str(uuid.uuid4())
        self.role = role
        self.state = BlockState.LIVE
        self.created_at = datetime.now()
        self.data = LiveBlockData(content=initial_content)
        
        # Start wall time tracking for this block
        self._wall_time_metrics = track_block_creation(self.id)

        # Event handlers for UI updates - separate progress from content
        self.content_update_callbacks: List[Callable] = []  # Meaningful content changes
        self.progress_update_callbacks: List[Callable] = (
            []
        )  # Timer/progress updates only

        # Cognition progress tracking (for cognition blocks and sub-blocks)
        self.cognition_progress: Optional[CognitionProgress] = None
        if role == "cognition":
            self.cognition_progress = CognitionProgress()
            self.cognition_progress.add_update_callback(self._on_progress_update)

        # Mock data simulation
        self._simulation_task: Optional[asyncio.Task] = None
        self._is_simulating = False

        # Optional model name for sub-blocks
        self._model_name: Optional[str] = None

    def add_update_callback(self, callback: Callable) -> None:
        """Add callback for when block data updates."""
        self.content_update_callbacks.append(callback)

    def add_progress_callback(self, callback: Callable) -> None:
        """Add callback for progress-only updates (no scroll triggering)."""
        self.progress_update_callbacks.append(callback)

    def _notify_update(self) -> None:
        """Notify all callbacks of data update."""
        for callback in self.content_update_callbacks:
            try:
                callback(self)
            except Exception as e:
                print(f"Error in content update callback: {e}")

    def _notify_progress_update(self) -> None:
        """Notify progress callbacks only (no scroll triggering)."""
        for callback in self.progress_update_callbacks:
            try:
                callback(self)
            except Exception as e:
                print(f"Error in progress update callback: {e}")

    def _on_progress_update(self, progress: CognitionProgress) -> None:
        """Called when cognition progress updates - update content with new status line"""
        if self.cognition_progress:
            status_line = self.cognition_progress.get_status_line()
            # Update the main content to show current progress
            self.data.content = status_line
            # Use progress-only update to avoid triggering scrolls
            self._notify_progress_update()

    def update_content(self, new_content: str) -> None:
        """Update block content (only in live state)."""
        if self.state != BlockState.LIVE:
            raise ValueError("Cannot update inscribed block")

        self.data.content = new_content
        self._notify_update()

    def append_content(self, additional_content: str) -> None:
        """Append to existing content (streaming simulation)."""
        if self.state != BlockState.LIVE:
            raise ValueError("Cannot update inscribed block")

        self.data.content += additional_content
        self._notify_update()

    def stream_content(self, target_content: str) -> None:
        """Update content immediately - UI can animate if desired."""
        if self.state == BlockState.INSCRIBED:
            return

        self.data.content += target_content
        self._notify_update()

    async def stream_content_animated(
        self, target_content: str, chars_per_second: float = 50.0, replace: bool = False
    ) -> None:
        """Stream content with typewriter animation at specified speed.

        Args:
            target_content: Text to stream
            chars_per_second: Animation speed (default 50 chars/sec)
            replace: If True, replace existing content; if False, append

        This provides the real character-by-character streaming experience
        that users should see, while respecting the global animation FPS.
        """
        if self.state == BlockState.INSCRIBED:
            return

        if replace:
            self.data.content = ""
            self._notify_update()

        initial_content = self.data.content

        def update_content(partial_text: str) -> None:
            if self.state == BlockState.INSCRIBED:
                return
            self.data.content = initial_content + partial_text
            self._notify_update()

        await animate_text_typewriter(target_content, update_content, chars_per_second)

    def set_tokens(self, target_input: int, target_output: int) -> None:
        """Set token counts immediately - UI can animate if desired."""
        if self.state != BlockState.LIVE:
            return

        # Calculate the delta to record in wall time tracker
        input_delta = target_input - self.data.tokens_input
        output_delta = target_output - self.data.tokens_output
        
        self.data.tokens_input = target_input
        self.data.tokens_output = target_output
        
        # Record token usage in wall time tracker if there's a change
        if input_delta != 0 or output_delta != 0:
            record_block_tokens(self.id, input_delta, output_delta)
        
        self._notify_update()

    async def animate_tokens(
        self, target_input: int, target_output: int, duration_seconds: float = 0.5
    ) -> None:
        """Animate token counters smoothly to target values.

        Args:
            target_input: Target input token count
            target_output: Target output token count
            duration_seconds: Animation duration

        This creates the visual effect of tokens incrementing that users expect.
        """
        if self.state != BlockState.LIVE:
            return

        start_input = self.data.tokens_input
        start_output = self.data.tokens_output

        def update_tokens(progress: float) -> None:
            if self.state != BlockState.LIVE:
                return

            # Interpolate between start and target values
            current_input = int(start_input + (target_input - start_input) * progress)
            current_output = int(
                start_output + (target_output - start_output) * progress
            )

            self.data.tokens_input = current_input
            self.data.tokens_output = current_output
            self._notify_update()

        await animate_value_smooth(0.0, 1.0, duration_seconds, update_tokens)

    def set_progress(self, target_progress: float) -> None:
        """Set progress immediately - UI can animate if desired."""
        if self.state != BlockState.LIVE:
            return

        self.data.progress = max(0.0, min(1.0, target_progress))
        self._notify_update()

    async def animate_progress(
        self, target_progress: float, duration_seconds: float = 0.3
    ) -> None:
        """Animate progress bar smoothly to target value.

        Args:
            target_progress: Target progress (0.0 to 1.0)
            duration_seconds: Animation duration

        This creates smooth progress bar animations that feel responsive.
        """
        if self.state != BlockState.LIVE:
            return

        target_progress = max(0.0, min(1.0, target_progress))
        start_progress = self.data.progress

        def update_progress(progress: float) -> None:
            if self.state != BlockState.LIVE:
                return

            current_progress = (
                start_progress + (target_progress - start_progress) * progress
            )
            self.data.progress = max(0.0, min(1.0, current_progress))
            self._notify_update()

        await animate_value_smooth(0.0, 1.0, duration_seconds, update_progress)

    def update_tokens(self, input_tokens: int = 0, output_tokens: int = 0) -> None:
        """Update token counts."""
        if self.state != BlockState.LIVE:
            return

        self.data.tokens_input += input_tokens
        self.data.tokens_output += output_tokens
        
        # Record token usage in wall time tracker
        record_block_tokens(self.id, input_tokens, output_tokens)
        
        self._notify_update()

    def update_progress(self, progress: float) -> None:
        """Update progress (0.0 to 1.0)."""
        if self.state != BlockState.LIVE:
            return

        self.data.progress = max(0.0, min(1.0, progress))
        self._notify_update()

    def add_sub_block(self, sub_block: "LiveBlock") -> None:
        """Add sub-block for nested plugin simulation."""
        if self.state != BlockState.LIVE:
            return

        self.data.sub_blocks.append(sub_block)
        # Connect sub-block updates to parent updates
        sub_block.add_update_callback(lambda _: self._notify_update())
        self._notify_update()

    async def start_mock_simulation(self, scenario: str = "default") -> None:
        """Start mock data simulation for this block."""
        if self._is_simulating:
            return

        self._is_simulating = True
        
        # Time the simulation process
        with time_block_stage(self.id, "processing"):
            # Run simulation directly instead of creating a task for better test control
            await self._run_mock_simulation(scenario)

    async def _run_mock_simulation(self, scenario: str) -> None:
        """Run mock simulation based on scenario."""
        try:
            if scenario == "cognition":
                await self._simulate_cognition_block()
            elif scenario == "assistant_response":
                await self._simulate_assistant_response()
            elif scenario == "tool_execution":
                await self._simulate_tool_execution()
            elif scenario == "route_analysis":
                await self._simulate_route_analysis()
            elif scenario == "tool_selection":
                await self._simulate_tool_selection()
            elif scenario == "response_gen":
                await self._simulate_response_generation()
            else:
                await self._simulate_basic_block()
        except asyncio.CancelledError:
            pass
        finally:
            self._is_simulating = False

    async def _simulate_cognition_block(self) -> None:
        """Simulate cognition block with sub-modules."""
        # Start with streaming progress
        self.stream_content("🧠 Starting cognition pipeline...")
        self.set_progress(0.1)

        # Set initial token count
        self.set_tokens(5, 0)

        # Sub-module 1: Route Query
        route_block = LiveBlock("sub_module")
        route_block.stream_content("🎯 Analyzing query intent...")
        self.add_sub_block(route_block)
        await route_block.start_mock_simulation("route_analysis")
        self.set_progress(0.3)

        # Sub-module 2: Tool Selection
        tool_block = LiveBlock("sub_module")
        tool_block.stream_content("🛠️ Selecting appropriate tools...")
        self.add_sub_block(tool_block)
        await tool_block.start_mock_simulation("tool_selection")
        self.set_progress(0.6)

        # Sub-module 3: Response Generation
        response_block = LiveBlock("sub_module")
        response_block.stream_content("📝 Generating response...")
        self.add_sub_block(response_block)
        await response_block.start_mock_simulation("response_gen")
        self.set_progress(0.9)

        # Final update
        self.stream_content("\n\n🧠 Cognition pipeline completed")
        self.set_progress(1.0)
        self.set_tokens(15, 3)

    async def _simulate_assistant_response(self) -> None:
        """Simulate streaming assistant response with character-by-character streaming."""
        full_response = (
            "I'll help you with that. Let me break this down step by step:\n\n"
            "1. First, we need to understand the core requirements\n"
            "2. Then we can design the appropriate solution\n"
            "3. Finally, we'll implement and test the result\n\n"
            "Based on your request, here's what I recommend:\n\n"
            "```python\n# Example implementation\ndef solve_problem():\n    return 'solution'\n```\n\n"
            "This approach ensures we maintain clarity while achieving the desired outcome."
        )

        # Stream the entire response immediately
        self.stream_content(full_response)

        # Update final progress and tokens
        self.set_progress(1.0)
        self.set_tokens(0, len(full_response) // 5)  # Rough token estimation

    async def _simulate_basic_block(self) -> None:
        """Simulate basic block progression."""
        stages = ["Initializing...", "Processing...", "Finalizing...", "Complete"]

        for i, stage in enumerate(stages):
            self.stream_content(f"⏳ {stage}")
            target_progress = (i + 1) / len(stages)
            self.set_progress(target_progress)
            self.set_tokens(0, 2 * (i + 1))
            # Only real async operation - simulating actual work
            await asyncio.sleep(0.1)

    async def _simulate_tool_execution(self) -> None:
        """Simulate tool execution with output."""
        self.update_content("🛠️ Executing tool...")
        self.update_progress(0.2)
        await AnimationRates.sleep(0.8)

        self.update_content("🛠️ Tool execution: Processing input...")
        self.update_progress(0.6)
        await AnimationRates.sleep(1.2)

        self.update_content(
            "🛠️ Tool execution: Complete\n\nOutput: Task completed successfully"
        )
        self.update_progress(1.0)
        self.update_tokens(output_tokens=12)

    async def _simulate_route_analysis(self) -> None:
        """Simulate route analysis sub-module with specific token usage."""
        self.stream_content(" → Analyzing query semantics...")
        self.set_progress(0.3)
        self.set_tokens(3, 0)

        self.stream_content("\n → Detecting intent patterns...")
        self.set_progress(0.7)
        self.set_tokens(2, 1)

        self.stream_content("\n → Route determined: CODING")
        self.set_progress(1.0)
        self.set_tokens(1, 2)

    async def _simulate_tool_selection(self) -> None:
        """Simulate tool selection sub-module with specific token usage."""
        self.stream_content(" → Scanning available tools...")
        self.set_progress(0.2)
        self.set_tokens(2, 0)

        self.stream_content("\n → Evaluating tool compatibility...")
        self.set_progress(0.6)
        self.set_tokens(4, 1)

        self.stream_content("\n → Selected: FileEditor, CodeAnalyzer")
        self.set_progress(1.0)
        self.set_tokens(2, 3)

    async def _simulate_response_generation(self) -> None:
        """Simulate response generation sub-module with specific token usage."""
        self.stream_content(" → Structuring response outline...")
        self.set_progress(0.25)
        self.set_tokens(5, 0)

        self.stream_content("\n → Generating content sections...")
        self.set_progress(0.65)
        self.set_tokens(12, 45)

        self.stream_content("\n → Applying formatting and polish...")
        self.set_progress(0.9)
        self.set_tokens(3, 15)

        self.stream_content("\n → Response ready for delivery")
        self.set_progress(1.0)
        self.set_tokens(1, 5)

    def stop_simulation(self) -> None:
        """Stop any running mock simulation."""
        if self._simulation_task and not self._simulation_task.done():
            self._simulation_task.cancel()
        self._is_simulating = False

    async def to_inscribed_block(self) -> "InscribedBlock":
        """Convert to inscribed block with animated transition."""
        if self.state == BlockState.INSCRIBED:
            raise ValueError("Block already inscribed")

        # Time the inscription process
        with time_block_stage(self.id, "inscription"):
            # Start transition animation
            self.state = BlockState.TRANSITIONING
            self._notify_update()

            # Visual transition effect - pulse the progress to show finalization
            self.set_progress(1.0)
            await AnimationRates.sleep(0.2)

            # Add transition visual cue
            transition_message = "\n🔒 Inscribing to Sacred Timeline..."
            self.stream_content(transition_message)
            await AnimationRates.sleep(0.3)

            # Stop any simulation
            self.stop_simulation()

            # Stop cognition progress timer
            if self.cognition_progress:
                self.cognition_progress.stop_timer()

            # Complete wall time tracking and get final metrics
            final_metrics = complete_block_tracking(self.id)

            # Create inscribed block with enhanced metadata including performance metrics
            inscribed = InscribedBlock(
                id=self.id,
                role=self.role,
                content=self.data.content,
                timestamp=self.created_at,
                metadata={
                    **self.data.metadata,
                    "wall_time_seconds": self.data.wall_time_seconds,
                    "tokens_input": self.data.tokens_input,
                    "tokens_output": self.data.tokens_output,
                    "sub_blocks": [block.to_dict() for block in self.data.sub_blocks],
                    "performance_metrics": final_metrics,  # Add detailed performance data
                },
            )

            # Complete transition
            self.state = BlockState.INSCRIBED
            self._notify_update()

            # Final transition effect
            await AnimationRates.sleep(0.2)

            return inscribed

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "role": self.role,
            "state": self.state.value,
            "created_at": self.created_at.isoformat(),
            "data": self.data.to_dict(),
        }

    # Cognition Progress Methods
    def set_cognition_steps(self, total_steps: int) -> None:
        """Set total number of steps for cognition progress"""
        if self.cognition_progress:
            self.cognition_progress.set_total_steps(total_steps)

    def notify_step_started(self) -> None:
        """Notify that a cognition step has started"""
        if self.cognition_progress:
            self.cognition_progress.step_started()

    def notify_step_completed(self, tokens_in: int = 0, tokens_out: int = 0) -> None:
        """Notify that a cognition step has completed"""
        if self.cognition_progress:
            self.cognition_progress.step_completed(tokens_in, tokens_out)

    def add_cognition_tokens(self, tokens_in: int = 0, tokens_out: int = 0) -> None:
        """Add tokens to cognition progress without completing a step"""
        if self.cognition_progress:
            self.cognition_progress.add_tokens(tokens_in, tokens_out)


@dataclass
class InscribedBlock:
    """Immutable block permanently added to Sacred Timeline."""

    id: str
    role: str
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


class LiveBlockManager:
    """Manages live blocks before timeline inscription."""

    def __init__(self):
        self.live_blocks: Dict[str, LiveBlock] = {}
        self.block_update_callbacks: List[Callable] = []

    def create_live_block(self, role: str, initial_content: str = "") -> LiveBlock:
        """Create a new live block."""
        block = LiveBlock(role, initial_content)
        self.live_blocks[block.id] = block

        # Add callback to notify when block updates
        block.add_update_callback(self._on_block_update)

        return block

    def _on_block_update(self, block: LiveBlock) -> None:
        """Handle live block updates."""
        for callback in self.block_update_callbacks:
            callback(block)

    def add_block_update_callback(self, callback: Callable) -> None:
        """Add callback for live block updates."""
        self.block_update_callbacks.append(callback)

    async def inscribe_block(self, block_id: str) -> Optional[InscribedBlock]:
        """Convert live block to inscribed block."""
        if block_id not in self.live_blocks:
            return None

        live_block = self.live_blocks[block_id]
        inscribed_block = await live_block.to_inscribed_block()

        # Remove from live blocks
        del self.live_blocks[block_id]

        return inscribed_block

    def get_live_blocks(self) -> List[LiveBlock]:
        """Get all current live blocks."""
        return list(self.live_blocks.values())

    def stop_all_simulations(self) -> None:
        """Stop all mock simulations."""
        for block in self.live_blocks.values():
            block.stop_simulation()
