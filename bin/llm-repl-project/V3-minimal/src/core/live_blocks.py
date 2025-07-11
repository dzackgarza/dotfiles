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

        # Event handlers for UI updates
        self.update_callbacks: List[Callable] = []

        # Mock data simulation
        self._simulation_task: Optional[asyncio.Task] = None
        self._is_simulating = False

    def add_update_callback(self, callback: Callable) -> None:
        """Add callback for when block data updates."""
        self.update_callbacks.append(callback)

    def _notify_update(self) -> None:
        """Notify all callbacks of data update."""
        for callback in self.update_callbacks:
            try:
                callback(self)
            except Exception as e:
                print(f"Error in update callback: {e}")

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

    def update_tokens(self, input_tokens: int = 0, output_tokens: int = 0) -> None:
        """Update token counts."""
        if self.state != BlockState.LIVE:
            return

        self.data.tokens_input += input_tokens
        self.data.tokens_output += output_tokens
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
            else:
                await self._simulate_basic_block()
        except asyncio.CancelledError:
            pass
        finally:
            self._is_simulating = False

    async def _simulate_cognition_block(self) -> None:
        """Simulate cognition block with sub-modules."""
        # Start with progress
        self.update_content("🧠 Starting cognition pipeline...")
        self.update_progress(0.1)
        await asyncio.sleep(0.5)

        # Sub-module 1: Route Query
        route_block = LiveBlock("sub_module", "🎯 Analyzing query intent...")
        self.add_sub_block(route_block)
        await route_block.start_mock_simulation("default")
        await asyncio.sleep(0.2)

        # Sub-module 2: Tool Selection
        tool_block = LiveBlock("sub_module", "🛠️ Selecting appropriate tools...")
        self.add_sub_block(tool_block)
        await tool_block.start_mock_simulation("default")
        await asyncio.sleep(0.2)

        # Sub-module 3: Response Generation
        response_block = LiveBlock("sub_module", "📝 Generating response...")
        self.add_sub_block(response_block)
        await response_block.start_mock_simulation("default")
        await asyncio.sleep(0.2)

        # Final update
        self.update_content("🧠 Cognition pipeline completed")
        self.update_progress(1.0)
        self.update_tokens(input_tokens=15, output_tokens=3)

    async def _simulate_assistant_response(self) -> None:
        """Simulate streaming assistant response."""
        base_responses = [
            "I'll help you with that. Let me break this down step by step:\n\n",
            "1. First, we need to understand the core requirements\n",
            "2. Then we can design the appropriate solution\n",
            "3. Finally, we'll implement and test the result\n\n",
            "Based on your request, here's what I recommend:\n\n",
            "```python\n# Example implementation\ndef solve_problem():\n    return 'solution'\n```\n\n",
            "This approach ensures we maintain clarity while achieving the desired outcome.",
        ]

        for i, response_chunk in enumerate(base_responses):
            self.append_content(response_chunk)
            self.update_progress((i + 1) / len(base_responses))
            self.update_tokens(output_tokens=len(response_chunk.split()))
            await asyncio.sleep(0.3 + (i * 0.1))  # Variable timing

    async def _simulate_basic_block(self) -> None:
        """Simulate basic block progression."""
        stages = ["Initializing...", "Processing...", "Finalizing...", "Complete"]

        for i, stage in enumerate(stages):
            self.update_content(f"⏳ {stage}")
            self.update_progress((i + 1) / len(stages))
            await asyncio.sleep(0.1)  # Shorter delay for tests

    async def _simulate_tool_execution(self) -> None:
        """Simulate tool execution with output."""
        self.update_content("🛠️ Executing tool...")
        self.update_progress(0.2)
        await asyncio.sleep(0.8)

        self.update_content("🛠️ Tool execution: Processing input...")
        self.update_progress(0.6)
        await asyncio.sleep(1.2)

        self.update_content(
            "🛠️ Tool execution: Complete\n\nOutput: Task completed successfully"
        )
        self.update_progress(1.0)
        self.update_tokens(output_tokens=12)

    def stop_simulation(self) -> None:
        """Stop any running mock simulation."""
        if self._simulation_task and not self._simulation_task.done():
            self._simulation_task.cancel()
        self._is_simulating = False

    def to_inscribed_block(self) -> "InscribedBlock":
        """Convert to inscribed block (immutable)."""
        if self.state == BlockState.INSCRIBED:
            raise ValueError("Block already inscribed")

        self.state = BlockState.TRANSITIONING
        self._notify_update()

        # Stop any simulation
        self.stop_simulation()

        # Create inscribed block
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
            },
        )

        self.state = BlockState.INSCRIBED
        self._notify_update()

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

    def inscribe_block(self, block_id: str) -> Optional[InscribedBlock]:
        """Convert live block to inscribed block."""
        if block_id not in self.live_blocks:
            return None

        live_block = self.live_blocks[block_id]
        inscribed_block = live_block.to_inscribed_block()

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
