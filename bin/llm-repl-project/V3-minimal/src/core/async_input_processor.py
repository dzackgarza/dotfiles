"""Async input processing with real live block updates"""

import asyncio
from typing import TYPE_CHECKING, TypedDict, Optional
import random

from ..sacred_timeline import SubBlock
from .live_blocks import LiveBlockManager, LiveBlock

if TYPE_CHECKING:
    from ..sacred_timeline import SacredTimeline
    from .response_generator import ResponseGenerator
    from textual.app import App


class SubModuleData(TypedDict):
    name: str
    icon: str
    model: str
    time: float
    tokens_in: int
    tokens_out: int


class AsyncInputProcessor:
    """Async version that shows real live updates"""

    def __init__(
        self,
        timeline: "SacredTimeline",
        response_generator: "ResponseGenerator",
        app: Optional["App"] = None,
    ):
        self.timeline = timeline
        self.response_generator = response_generator
        self.live_block_manager = LiveBlockManager()
        self.app = app

    async def process_user_input_async(self, user_input: str) -> None:
        """Process user input with real async updates"""
        user_input = user_input.strip()
        if not user_input:
            return

        # Add user message immediately
        self.timeline.add_block(role="user", content=user_input)

        # Start cognition processing with live updates
        await self._add_cognition_block_async(user_input)

        # Generate assistant response after cognition completes
        response = self.response_generator.generate_response(user_input)
        self.timeline.add_block(role="assistant", content=response)

    async def _add_cognition_block_async(self, user_input: str) -> None:
        """Add cognition block with real async updates and sequential sub-module execution"""

        # Create live block with initial content
        live_block = self.live_block_manager.create_live_block(
            role="cognition",
            initial_content="🧠 **Cognition Pipeline**\nInitializing multi-step reasoning process...",
        )

        # Notify observers about the new live block
        for observer in self.timeline._observers:
            if hasattr(observer, "on_live_block_update"):
                observer.on_live_block_update(live_block)

        # Register update callback
        def notify_update(block):
            for observer in self.timeline._observers:
                if hasattr(observer, "on_live_block_update"):
                    observer.on_live_block_update(block)

        live_block.add_update_callback(notify_update)

        # Import sub-modules
        from .sub_modules import RouteQueryModule, CallToolModule, FormatOutputModule
        from .live_blocks import CognitionProgress
        
        # Set up cognition progress tracking
        live_block.set_cognition_steps(3)  # We have 3 sub-modules
        
        # Record start time for accurate timing
        import time
        cognition_start_time = time.time()

        # Sequential sub-module execution
        # Step 1: Route Query
        await self._execute_sub_module(
            live_block, 
            RouteQueryModule,
            "route_query",
            "Route Query"
        )
        
        # Step 2: Call Tool
        await self._execute_sub_module(
            live_block,
            CallToolModule, 
            "call_tool",
            "Call Tool"
        )
        
        # Step 3: Format Output
        await self._execute_sub_module(
            live_block,
            FormatOutputModule,
            "format_output", 
            "Format Output"
        )

        # Set final timing data using actual wall clock time
        actual_wall_time = time.time() - cognition_start_time
        live_block.data.wall_time_seconds = actual_wall_time

        # Small delay before inscribing
        await asyncio.sleep(0.2)

        # Inscribe the block
        inscribed_block = await self.live_block_manager.inscribe_block(live_block.id)

        if inscribed_block:
            # Inscribe sub-blocks first
            for sub_block in live_block.data.sub_blocks:
                await self.live_block_manager.inscribe_block(sub_block.id)

            # Add to timeline but mark it as already having a widget
            # This prevents duplicate widgets while maintaining data persistence
            self.timeline.add_block(
                role=inscribed_block.role,
                content=inscribed_block.content,
                metadata={
                    **inscribed_block.metadata,
                    "_has_live_widget": True,  # Flag to prevent duplicate widget
                },
                time_taken=inscribed_block.metadata.get(
                    "wall_time_seconds", actual_wall_time
                ),
                tokens_input=inscribed_block.metadata.get("tokens_input", 0),
                tokens_output=inscribed_block.metadata.get("tokens_output", 0),
                sub_blocks=[
                    SubBlock(
                        type=sb.get("role", "unknown"),
                        content=sb.get("data", {}).get("content", ""),
                    )
                    for sb in inscribed_block.metadata.get("sub_blocks", [])
                ],
            )

    async def _execute_sub_module(
        self, 
        parent_block: "LiveBlock", 
        module_class: type,
        role: str,
        title: str
    ) -> None:
        """Execute a sub-module sequentially."""
        # Create sub-block for this module
        sub_block = self.live_block_manager.create_live_block(
            role=role,
            initial_content=""  # Module will provide initial content
        )
        
        # Add to parent's sub-blocks
        parent_block.add_sub_block(sub_block)
        
        # Create and configure the module
        module = module_class(sub_block)
        
        # Set initial content from module
        sub_block.update_content(module.get_initial_content())
        
        # Create completion event
        completion_event = asyncio.Event()
        
        async def on_completion():
            completion_event.set()
            
        module.set_completion_callback(on_completion)
        
        # Notify observers about new sub-block
        for observer in self.timeline._observers:
            if hasattr(observer, "on_live_block_update"):
                observer.on_live_block_update(sub_block)
        
        # Execute the module and wait for completion
        await module.execute()
        await completion_event.wait()
