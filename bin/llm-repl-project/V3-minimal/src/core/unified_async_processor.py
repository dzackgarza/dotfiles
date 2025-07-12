"""
Unified Async Input Processor - V3.15

Replaces AsyncInputProcessor to use UnifiedTimeline instead of dual systems.
Eliminates ownership conflicts by using single timeline.
"""

import asyncio
from typing import TYPE_CHECKING, TypedDict, Optional, cast

from .unified_timeline import UnifiedTimelineManager
from .live_blocks import LiveBlock
from ..cognition import CognitionManager, CognitionEvent, CognitionResult

if TYPE_CHECKING:
    from .response_generator import ResponseGenerator
    from textual.app import App
    from ..main import LLMReplApp


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

        # Initialize cognition manager
        self.cognition_manager = CognitionManager()

        # Wire callbacks for staging area and timeline
        self.cognition_manager.set_staging_callback(self._handle_cognition_event)
        self.cognition_manager.set_timeline_callback(self._handle_cognition_result)

    def get_timeline(self):
        """Get the unified timeline for UI integration"""
        return self.timeline_manager.timeline

    async def process_user_input_async(self, user_input: str) -> None:
        """Process user input with atomic turn inscription

        Entire turn (user + cognition + assistant) is inscribed at once.
        """
        user_input = user_input.strip()
        if not user_input:
            return

        # Get turn number
        turn_number = self.app.turn_count if self.app else 1

        # Show live workspace for cognition
        if self.app:
            workspace = self.app.query_one("#staging-container")
            if hasattr(workspace, "show_workspace"):
                workspace.show_workspace()

        # Store components for atomic inscription
        self.current_turn_data = {
            "turn_number": turn_number,
            "user_input": user_input,
            "cognition_result": None,
            "assistant_response": None,
        }

        # Process through cognition module (it will emit events)
        cognition_result = await self.cognition_manager.process_query(user_input)
        self.current_turn_data["cognition_result"] = cognition_result

        # Generate assistant response
        response = self.response_generator.generate_response(user_input)
        self.current_turn_data["assistant_response"] = response

        # Hide live workspace after cognition
        if self.app:
            workspace = self.app.query_one("#staging-container")

            # Clear cognition content
            for widget in list(workspace.children):
                widget.remove()

            # Restore idle animation
            from ..widgets.idle_animation import IdleAnimation

            idle_animation = IdleAnimation()
            await workspace.mount(idle_animation)

            if hasattr(workspace, "hide_workspace"):
                workspace.hide_workspace()

        # NOW inscribe the complete turn atomically
        await self._inscribe_complete_turn()

    async def _inscribe_complete_turn(self) -> None:
        """Inscribe complete turn (user + cognition + assistant) to timeline"""
        if not self.app or not hasattr(self, "current_turn_data"):
            return

        data = self.current_turn_data
        from ..widgets.chatbox import Chatbox

        # Get app state for smart follow
        was_at_bottom = self.app._is_at_bottom()
        chat_container = self.app.query_one("#chat-container")

        # Add user message
        user_chatbox = Chatbox(data["user_input"], role="user")
        await chat_container.mount(user_chatbox)

        # Add cognition result
        if data["cognition_result"]:
            result = data["cognition_result"]
            content = f"**{result.content}**\n"
            if result.sub_blocks:
                content += "\n**Sub-modules:**\n"
                for sub in result.sub_blocks:
                    content += f"• {sub['module_name']}: {sub['content']}\n"

            if result.metadata:
                content += f"\n_Processing time: {result.metadata.get('processing_time', 0):.2f}s_"

            cognition_chatbox = Chatbox(content, role="cognition")
            await chat_container.mount(cognition_chatbox)

        # Add assistant response
        if data["assistant_response"]:
            assistant_chatbox = Chatbox(data["assistant_response"], role="assistant")
            await chat_container.mount(assistant_chatbox)

        # Smart follow: only scroll if user was at bottom
        if was_at_bottom:
            chat_container.scroll_end(animate=False)

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

    async def _handle_cognition_event(self, event: CognitionEvent) -> None:
        """Handle cognition events for staging area updates"""
        if not self.app:
            return

        # Get the staging container
        workspace = self.app.query_one("#staging-container")

        if event.type == "start":
            # Clear staging area (remove idle animation or previous content)
            for widget in list(workspace.children):
                widget.remove()

            # Add turn header with user query
            if hasattr(self, "current_turn_data"):
                from textual.widgets import Static

                turn_data = self.current_turn_data
                header_content = f"**Turn {turn_data['turn_number']}**\n\n**User:** {turn_data['user_input']}\n\n**Cognition:**"
                header_widget = Static(header_content, classes="turn-header")
                await workspace.mount(header_widget)

            # Add initial cognition content
            if event.content:
                from textual.widgets import Static

                widget = Static(event.content, classes="cognition-event")
                await workspace.mount(widget)

        elif event.type == "update":
            # Update staging area content while preserving header
            from textual.widgets import Static

            # Remove old cognition content but keep header
            for widget in list(workspace.children):
                if not widget.has_class("turn-header"):
                    widget.remove()

            # Add updated cognition content
            widget = Static(event.content, classes="cognition-event")
            await workspace.mount(widget)

            # Auto-scroll to bottom to follow updates
            workspace.scroll_end(animate=False)

        elif event.type == "complete":
            # Final update while preserving header
            from textual.widgets import Static

            # Remove old cognition content but keep header
            for widget in list(workspace.children):
                if not widget.has_class("turn-header"):
                    widget.remove()

            widget = Static(event.content, classes="cognition-event complete")
            await workspace.mount(widget)

            # Final auto-scroll
            workspace.scroll_end(animate=False)

    async def _handle_cognition_result(self, result: CognitionResult) -> None:
        """Handle cognition result - just store for atomic inscription"""
        # No longer add to timeline immediately - part of atomic turn
        pass
