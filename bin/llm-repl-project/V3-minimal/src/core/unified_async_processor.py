"""
Unified Async Input Processor - V3.15

Replaces AsyncInputProcessor to use UnifiedTimeline instead of dual systems.
Eliminates ownership conflicts by using single timeline.
"""

import asyncio
from typing import TYPE_CHECKING, TypedDict, Optional

from .unified_timeline import UnifiedTimelineManager
from .live_blocks import LiveBlock

if TYPE_CHECKING:
    from .response_generator import ResponseGenerator
    from textual.app import App


class SubModuleData(TypedDict):
    name: str
    icon: str
    model: str
    time: float
    tokens_in: int
    tokens_out: int


class UnifiedAsyncInputProcessor:
    """Unified async processor using single timeline ownership

    This replaces AsyncInputProcessor and eliminates the dual-system
    architecture that caused ownership conflicts.
    """

    def __init__(
        self,
        response_generator: "ResponseGenerator",
        app: Optional["App"] = None,
    ):
        self.response_generator = response_generator
        self.timeline_manager = UnifiedTimelineManager()
        self.app = app

    def get_timeline(self):
        """Get the unified timeline for UI integration"""
        return self.timeline_manager.timeline

    async def process_user_input_async(self, user_input: str) -> None:
        """Process user input with unified timeline

        This method replaces the old dual-system approach with
        single timeline ownership.
        """
        user_input = user_input.strip()
        if not user_input:
            return

        # Add user message as inscribed block immediately
        user_block = self.timeline_manager.timeline.add_live_block("user", user_input)
        await self.timeline_manager.timeline.inscribe_block(user_block.id)

        # Start cognition processing with live updates
        await self._add_cognition_block_async(user_input)

        # Generate assistant response
        response = self.response_generator.generate_response(user_input)
        assistant_block = self.timeline_manager.timeline.add_live_block(
            "assistant", response
        )
        await self.timeline_manager.timeline.inscribe_block(assistant_block.id)

    async def _add_cognition_block_async(self, user_input: str) -> None:
        """Add cognition block with unified timeline ownership

        This eliminates the complex ownership transfer logic by
        using timeline as single source of truth.
        """
        # Create live cognition block (timeline owns it immediately)
        live_block = self.timeline_manager.timeline.add_live_block(
            role="cognition",
            content="🧠 **Cognition Pipeline**\nInitializing multi-step reasoning process...",
        )

        # Import sub-modules
        from .sub_modules import RouteQueryModule, CallToolModule, FormatOutputModule

        # Set up cognition progress tracking
        live_block.set_cognition_steps(3)  # 3 sub-modules

        # Record timing
        import time

        cognition_start_time = time.time()

        # Sequential sub-module execution with unified ownership
        await self._execute_sub_module_unified(
            live_block, RouteQueryModule, "route_query", "Route Query"
        )

        await self._execute_sub_module_unified(
            live_block, CallToolModule, "call_tool", "Call Tool"
        )

        await self._execute_sub_module_unified(
            live_block, FormatOutputModule, "format_output", "Format Output"
        )

        # Set final timing
        actual_wall_time = time.time() - cognition_start_time
        live_block.data.wall_time_seconds = actual_wall_time

        # Brief pause before inscription
        await asyncio.sleep(0.2)

        # Atomic inscription preserving complete structure
        await self.timeline_manager.timeline.inscribe_block(live_block.id)

    async def _execute_sub_module_unified(
        self, parent_block: LiveBlock, module_class: type, role: str, title: str
    ) -> None:
        """Execute sub-module with unified timeline ownership

        Sub-blocks are owned by parent, not timeline directly.
        This prevents orphaned sub-blocks and ownership conflicts.
        """
        # Create sub-block owned by parent (not timeline)
        sub_block = self.timeline_manager.timeline.add_sub_block(
            parent_block.id, role, ""
        )

        if not sub_block:
            return  # Parent not found

        # Create and configure module with parent reference
        module = module_class(sub_block, parent_block=parent_block)

        # Set initial content
        sub_block.update_content(module.get_initial_content())

        # Create completion event
        completion_event = asyncio.Event()

        async def on_completion():
            completion_event.set()

        module.set_completion_callback(on_completion)

        # Execute module and wait for completion
        await module.run()
        await completion_event.wait()
