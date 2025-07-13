"""
Unified Async Input Processor - V3.15

Replaces AsyncInputProcessor to use UnifiedTimeline instead of dual systems.
Eliminates ownership conflicts by using single timeline.
"""

import asyncio
from typing import TYPE_CHECKING, TypedDict, Optional

from .config import Config
from .unified_timeline import UnifiedTimelineManager
from .live_blocks import LiveBlock
from ..cognition import CognitionManager, CognitionEvent, CognitionResult
from .processing_queue import ProcessingQueue

if TYPE_CHECKING:
    from .response_generator import ResponseGenerator
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
        app: Optional["LLMReplApp"] = None,
    ):
        self.response_generator = response_generator
        self.timeline_manager = UnifiedTimelineManager()
        self.app = app
        self._pending_inscription = None  # Store data for manual inscription

        # Initialize cognition manager
        self.cognition_manager = CognitionManager()

        # Wire callbacks for staging area and timeline
        self.cognition_manager.set_staging_callback(self._handle_cognition_event)
        self.cognition_manager.set_timeline_callback(self._handle_cognition_result)

        # Processing control
        self._processing_paused = False

        # Processing queue for debug mode
        self.processing_queue = ProcessingQueue(app) if app else None

        # Reference to active cognition widget for sub-module updates
        self._active_cognition_widget = None

    def pause_processing(self):
        """Pause all processing to prevent interference"""
        self._processing_paused = True

    def resume_processing(self):
        """Resume processing"""
        self._processing_paused = False

    def get_timeline(self):
        """Get the unified timeline for UI integration"""
        return self.timeline_manager.timeline

    async def manual_inscribe(self):
        """Manually inscribe pending turn data to timeline"""
        print("DEBUG: manual_inscribe called")

        # Use new processing queue system if enabled
        if Config.USE_PROCESSING_QUEUE and self.processing_queue:
            success = await self.processing_queue.inscribe_next()

            if success and self._pending_inscription:
                print("DEBUG: Manual inscription triggered - processing queue")
                # Temporarily restore current_turn_data
                self.current_turn_data = self._pending_inscription
                await self._inscribe_complete_turn()
                self._pending_inscription = None

                # Check if more blocks are ready
                ready_count = len(self.processing_queue.get_ready_blocks())
                if ready_count > 0:
                    self.app.notify(f"✅ Inscribed! {ready_count} more blocks ready.", severity="information")
                else:
                    # All done - hide workspace
                    workspace = self.app.query_one("#staging-container")
                    if hasattr(self.app, "staging_separator"):
                        self.app.staging_separator.set_idle()
                    if hasattr(workspace, "hide_workspace"):
                        workspace.hide_workspace()
                    self.app.notify("All blocks inscribed!", severity="success")
            else:
                self.app.notify("No completed blocks ready for inscription.", severity="warning")

        # Legacy mode fallback
        elif self._pending_inscription:
            print("DEBUG: Manual inscription triggered - legacy mode")
            self.current_turn_data = self._pending_inscription
            await self._inscribe_complete_turn()
            self._pending_inscription = None

            if self.app:
                workspace = self.app.query_one("#staging-container")
                for widget in list(workspace.children):
                    if not widget.has_class("staging-separator"):
                        widget.remove()
                if hasattr(self.app, "staging_separator"):
                    self.app.staging_separator.set_idle()
                if hasattr(workspace, "hide_workspace"):
                    workspace.hide_workspace()
                self.app.notify("Turn inscribed to timeline!", severity="information")
        else:
            print("DEBUG: No pending inscription data")
            if self.app:
                self.app.notify("No pending inscription to process.", severity="warning")

    async def process_user_input_async(self, user_input: str) -> None:
        """Process user input with atomic turn inscription

        Entire turn (user + cognition + assistant) is inscribed at once.
        """
        print(f"DEBUG: process_user_input_async called with: {user_input}")

        # Check if processing is paused (e.g., for reality capture)
        if self._processing_paused:
            print("DEBUG: Processing paused, skipping")
            return

        user_input = user_input.strip()
        if not user_input:
            return

        # Get turn number
        turn_number = self.app.turn_count if self.app else 1

        # Show live workspace for cognition
        if self.app:
            workspace = self.app.query_one("#staging-container")
            print(f"DEBUG: Found workspace, has show_workspace: {hasattr(workspace, 'show_workspace')}")
            if hasattr(workspace, "show_workspace"):
                print("DEBUG: Calling show_workspace()")
                workspace.show_workspace()
                print(f"DEBUG: After show_workspace, classes: {workspace.classes}")

                # In debug mode with processing queue, the queue will handle widget creation
                # Otherwise, we'll add the widget manually in simple debug mode later

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
        print("DEBUG: About to generate assistant response")
        response = self.response_generator.generate_response(user_input)
        self.current_turn_data["assistant_response"] = response
        print(f"DEBUG: Generated assistant response: {response[:50]}...")
        print(f"DEBUG: About to check manual inscribe mode: {Config.MANUAL_INSCRIBE_MODE}")

        # Check if debug mode is enabled
        if Config.DEBUG_MODE:
            # Use processing queue only if enabled
            if Config.USE_PROCESSING_QUEUE and self.processing_queue:
                print("DEBUG: Debug mode with processing queue")

                # Add the message to processing queue
                processing_widget = await self.processing_queue.add_block(user_input)

                # Store the pending inscription data with the widget
                self._pending_inscription = self.current_turn_data.copy() if hasattr(self, 'current_turn_data') else None

                # Update the staging separator to show debug mode active
                if self.app and hasattr(self.app, "staging_separator"):
                    self.app.staging_separator.set_pending_inscription()

                # Show a notification to the user
                if self.app:
                    self.app.notify("🔍 Debug Mode: Processing block added. Type /inscribe when ready to commit.", severity="warning")
            else:
                # Simple debug mode (original implementation)
                print("DEBUG: Simple debug mode - response stays in staging")
                self._pending_inscription = self.current_turn_data.copy() if hasattr(self, 'current_turn_data') else None

                # Keep workspace visible AND add response for inspection
                if self.app:
                    workspace = self.app.query_one("#staging-container")

                    # Add the assistant response to staging area for inspection
                    if response:
                        from ..widgets.chatbox import Chatbox
                        assistant_preview = Chatbox(str(response), role="assistant")
                        await workspace.mount(assistant_preview)
                        print("DEBUG: Added assistant response to staging area for inspection")

                        # Add help text for debug mode
                        from textual.widgets import Static
                        help_text = Static(
                            "\n💡 **Debug Mode Instructions:**\n"
                            "• Response is paused in staging area for inspection\n"
                            "• Type `/inscribe` and press Enter to commit to timeline\n"
                            "• Take screenshots or examine the response before committing\n",
                            classes="debug-help"
                        )
                        await workspace.mount(help_text)

                    # Update the staging separator to show manual inscription is pending
                    if hasattr(self.app, "staging_separator"):
                        self.app.staging_separator.set_pending_inscription()

                # Show a notification to the user
                if self.app:
                    self.app.notify("🔍 Debug Mode: Response ready for inspection. Type /inscribe to commit to timeline.", severity="warning")
        else:
            # Normal mode: hide workspace after cognition
            if self.app:
                workspace = self.app.query_one("#staging-container")

                # Clear cognition content (keep staging separator)
                for widget in list(workspace.children):
                    if not widget.has_class("staging-separator"):
                        widget.remove()

                # Set staging separator back to idle state
                if self.app and hasattr(self.app, "staging_separator"):
                    self.app.staging_separator.set_idle()

                if hasattr(workspace, "hide_workspace"):
                    workspace.hide_workspace()

            # NOW inscribe the complete turn atomically
            print("DEBUG: About to inscribe complete turn")
            try:
                await self._inscribe_complete_turn()
                print("DEBUG: Finished inscribing complete turn")
            except Exception as e:
                print(f"DEBUG: Inscription failed with error: {e}")
                import traceback
                traceback.print_exc()

    async def _inscribe_complete_turn(self) -> None:
        """Inscribe complete turn (user + cognition + assistant) to timeline"""
        print("DEBUG: _inscribe_complete_turn called")
        if not self.app or not hasattr(self, "current_turn_data"):
            print("DEBUG: _inscribe_complete_turn early return - no app or current_turn_data")
            return

        data = self.current_turn_data
        from ..widgets.chatbox import Chatbox
        from ..widgets.turn_separator import TurnSeparator

        # Get app state for smart follow
        was_at_bottom = self.app._is_at_bottom()
        chat_container = self.app.query_one("#chat-container")

        # FIRST: Add user message (Turn 2 starts with user input)
        user_chatbox = Chatbox(str(data["user_input"]), role="user")
        await chat_container.mount(user_chatbox)

        # Add cognition result using unified widget
        cognition_result = data["cognition_result"]
        if cognition_result:
            from ..widgets.cognition_widget import CognitionWidget

            # Create unified cognition widget in final state
            if hasattr(cognition_result, "content"):
                content = cognition_result.content or "Cognition Processing Complete"
                sub_blocks = getattr(cognition_result, "sub_blocks", [])
                metadata = getattr(cognition_result, "metadata", {})
            else:
                # Handle case where cognition_result is a simple type
                content = (
                    str(cognition_result)
                    if cognition_result
                    else "Cognition Processing Complete"
                )
                sub_blocks = []
                metadata = {}

            cognition_widget = CognitionWidget(
                content=content,
                is_live=False,
            )

            print("DEBUG: Creating unified cognition widget for timeline")
            print(f"DEBUG: Cognition content: {content[:50]}...")
            print(
                f"DEBUG: Cognition widget border_title: {cognition_widget.border_title}"
            )
            print(
                f"DEBUG: Cognition widget CSS classes: {list(cognition_widget.classes)}"
            )

            await chat_container.mount(cognition_widget)
            print("DEBUG: Mounted unified cognition widget")

        # Add assistant response
        assistant_response = data["assistant_response"]
        print(f"DEBUG: Assistant response in inscription: {assistant_response}")
        if assistant_response:
            assistant_chatbox = Chatbox(str(assistant_response), role="assistant")
            await chat_container.mount(assistant_chatbox)
            print("DEBUG: Mounted assistant chatbox")

        # LAST: Add turn separator AFTER the complete turn
        # This separator marks the END of Turn N, not the beginning of Turn N+1
        turn_number = data.get("turn_number", 1)
        print(f"DEBUG: Turn number for separator: {turn_number}")
        if turn_number > 0:  # Add separator after every turn
            separator = TurnSeparator(turn_number)
            await chat_container.mount(separator)
            print(f"DEBUG: Mounted turn separator for turn {turn_number}")

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
        print(f"DEBUG: _handle_cognition_event called - type: {event.type}, module: {event.metadata.get('module', 'N/A')}")
        if self._processing_paused:
            return
        if not self.app:
            return

        # Get the staging container
        workspace = self.app.query_one("#staging-container")

        if event.type == "start":
            # Set staging separator to processing state
            if self.app and hasattr(self.app, "staging_separator"):
                turn_num = self.current_turn_data["turn_number"]
                if isinstance(turn_num, int):
                    self.app.staging_separator.set_processing(turn_num)

            # Clear staging area (except staging separator)
            for widget in list(workspace.children):
                if not widget.has_class("staging-separator"):
                    widget.remove()

            # Add turn header with user query
            if hasattr(self, "current_turn_data"):
                from textual.widgets import Static

                turn_data = self.current_turn_data
                header_content = (
                    f"**User:** {turn_data['user_input']}\n\n**Cognition:**"
                )
                header_widget = Static(header_content, classes="turn-header")
                await workspace.mount(header_widget)

            # Add initial cognition content using enhanced widget
            if event.content:
                from ..widgets.cognition_widget import CognitionWidget

                # Store reference to the cognition widget for later updates
                self._active_cognition_widget = CognitionWidget(content=event.content, is_live=True)
                await workspace.mount(self._active_cognition_widget)

        elif event.type == "add_submodule":
            print("DEBUG: Handling add_submodule event")
            # Add sub-module to the active CognitionWidget
            if hasattr(self, '_active_cognition_widget') and self._active_cognition_widget:
                metadata = event.metadata
                self._active_cognition_widget.add_sub_module(
                    name=metadata.get("name", "Unknown"),
                    icon=metadata.get("icon", "⚙️"),
                    state=metadata.get("state", "PROCESSING"),
                    tokens_in=metadata.get("tokens_in", 0),
                    tokens_out=metadata.get("tokens_out", 0),
                    progress=metadata.get("progress", 0.0),
                    timer=metadata.get("timer", 0.0)
                )
                print(f"DEBUG: Added sub-module {metadata.get('name')} to CognitionWidget")

        elif event.type == "update":
            print(f"DEBUG: Handling update event for module: {event.metadata.get('module', 'N/A')}")
            # Add each cognition event as a separate sub-module widget
            from ..widgets.sub_module import SubModuleWidget
            from ..core.live_blocks import LiveBlock

            # Create a live block for this sub-module
            sub_module_data = LiveBlock(
                role=event.metadata.get("module", "cognition"),
                initial_content=event.content
            )

            # Add metadata and token counts
            sub_module_data.data.metadata = event.metadata
            sub_module_data.data.tokens_input = event.metadata.get("tokens_input", 0)
            sub_module_data.data.tokens_output = event.metadata.get("tokens_output", 0)
            sub_module_data.data.progress = event.metadata.get("progress", 0.0)

            print(f"DEBUG: Creating SubModuleWidget for {event.metadata.get('module', 'N/A')}")
            # Create and mount sub-module widget
            try:
                sub_widget = SubModuleWidget(sub_module=sub_module_data)
                print("DEBUG: SubModuleWidget created successfully")
                await workspace.mount(sub_widget)
                print(f"DEBUG: Mounted SubModuleWidget, now workspace has {len(list(workspace.children))} children")
            except Exception as e:
                print(f"DEBUG: ERROR creating/mounting SubModuleWidget: {e}")
                import traceback
                traceback.print_exc()

            # Auto-scroll to bottom to follow updates
            workspace.scroll_end(animate=False)

        elif event.type == "progress":
            print(f"DEBUG: Handling progress event for module: {event.metadata.get('module', 'N/A')}")
            # Update existing SubModuleWidget progress
            module_name = event.metadata.get("module", "")
            progress = event.metadata.get("progress", 0.0)

            # Find the SubModuleWidget for this module and update its progress
            for widget in workspace.children:
                if (hasattr(widget, 'sub_module') and
                    widget.sub_module.role == module_name):
                    print(f"DEBUG: Updating progress for {module_name}: {int(progress * 100)}%")
                    widget.sub_module.data.progress = progress
                    widget.sub_module.data.tokens_input = event.metadata.get("tokens_input", 0)
                    widget.sub_module.data.tokens_output = event.metadata.get("tokens_output", 0)
                    widget.refresh()  # Trigger re-render
                    break

        elif event.type == "complete":
            # Final update while preserving header
            from ..widgets.cognition_widget import CognitionWidget

            # Find existing cognition widget and update it, or create new one
            cognition_widget = None
            for widget in workspace.children:
                if isinstance(widget, CognitionWidget):
                    cognition_widget = widget
                    break

            if cognition_widget:
                # Update existing widget to complete state
                cognition_widget.set_live_content(event.content)
            else:
                # Remove old content but keep header and staging separator
                for widget in list(workspace.children):
                    if not widget.has_class("turn-header") and not widget.has_class(
                        "staging-separator"
                    ):
                        widget.remove()

                # Create new cognition widget in live state
                widget = CognitionWidget(content=event.content, is_live=True)
                await workspace.mount(widget)

            # Final auto-scroll
            workspace.scroll_end(animate=False)

    async def _handle_cognition_result(self, result: CognitionResult) -> None:
        """Handle cognition result - just store for atomic inscription"""
        if self._processing_paused:
            return
        # No longer add to timeline immediately - part of atomic turn
        pass
