"""Async input processing with real live block updates"""

import asyncio
from typing import TYPE_CHECKING, TypedDict, Optional
import random

from ..sacred_timeline import SubBlock
from .live_blocks import LiveBlockManager

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
        """Add cognition block with real async updates"""

        # Create live block with empty content to animate from start
        live_block = self.live_block_manager.create_live_block(
            role="cognition",
            initial_content="",
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

        # Define sub-modules
        sub_modules_data: list[SubModuleData] = [
            {
                "name": "Route query",
                "icon": "🧠",
                "model": "tinyllama-v2",
                "time": random.uniform(0.3, 0.8),
                "tokens_in": random.randint(5, 15),
                "tokens_out": random.randint(1, 5),
            },
            {
                "name": "Call tool",
                "icon": "🛠️",
                "model": "brave_web_search",
                "time": random.uniform(1.5, 3.0),
                "tokens_in": random.randint(10, 20),
                "tokens_out": random.randint(1000, 1500),
            },
            {
                "name": "Format output",
                "icon": "🤖",
                "model": "mistral-7b-instruct",
                "time": random.uniform(0.8, 1.5),
                "tokens_in": random.randint(400, 600),
                "tokens_out": random.randint(200, 300),
            },
        ]

        total_time = 0.0
        total_tokens_in = 0
        total_tokens_out = 0

        # Set up cognition progress tracking
        live_block.set_cognition_steps(len(sub_modules_data))

        # Record start time for accurate timing
        import time

        cognition_start_time = time.time()

        # Process each sub-module with real delays
        for i, sub_module in enumerate(sub_modules_data):
            # Notify that step is starting
            live_block.notify_step_started()

            # Create sub-block with rich initial content
            task_descriptions = {
                "Route query": "Analyzing user intent and determining appropriate response strategy",
                "Call tool": "Executing web search to gather relevant information",
                "Format output": "Structuring response with clear formatting and citations",
            }

            initial_content = (
                f"{sub_module['icon']} **{sub_module['name']}**\n"
                f"└─ {task_descriptions.get(sub_module['name'], 'Processing...')}\n\n"
                f"**Provider**: {sub_module['model'].split('_')[0].title() if '_' in sub_module['model'] else 'Local'}\n"
                f"**Model**: `{sub_module['model']}`\n"
                f"**Status**: 🔄 Initializing...\n\n"
                f"⏱️ 0.0s | [░░░░░░░░░░░░░░░░░░░░] 0% | 🔢 0↑/0↓"
            )
            sub_live_block = self.live_block_manager.create_live_block(
                role=sub_module["name"].lower().replace(" ", "_"),
                initial_content=initial_content,
            )

            # Give sub-block its own progress tracking
            from .live_blocks import CognitionProgress

            sub_live_block.cognition_progress = CognitionProgress()

            # Store model name for display
            sub_live_block._model_name = sub_module["model"]

            # Create custom progress callback that updates just the progress line
            # Use closure to capture current sub_live_block reference
            def make_sub_progress_callback(block, base_content):
                def sub_progress_callback(progress):
                    if block.cognition_progress:
                        # Keep the rich metadata, just update the progress line
                        lines = block.data.content.split("\n")
                        # Find and replace the progress line (last line with timer)
                        for i in range(len(lines) - 1, -1, -1):
                            if "⏱️" in lines[i]:
                                progress_line = (
                                    block.cognition_progress.get_status_line()
                                )
                                lines[i] = progress_line
                                break
                        block.data.content = "\n".join(lines)
                        block._notify_update()

                return sub_progress_callback

            # Use progress callback for timer updates to avoid scroll triggering
            sub_live_block.cognition_progress.add_update_callback(
                make_sub_progress_callback(sub_live_block, initial_content)
            )
            sub_live_block.cognition_progress.set_total_steps(
                1
            )  # Each sub-block is one step

            # Add sub-block - this is a content change, so it uses content callback
            live_block.add_sub_block(sub_live_block)

            # Start sub-block processing
            sub_live_block.notify_step_started()

            # Simulate processing with real delay
            await asyncio.sleep(sub_module["time"])

            # Complete sub-block with timing and token data
            sub_live_block.notify_step_completed(
                tokens_in=sub_module["tokens_in"], tokens_out=sub_module["tokens_out"]
            )

            # Stop sub-block timer
            if sub_live_block.cognition_progress:
                sub_live_block.cognition_progress.stop_timer()

            # Update totals
            total_time += sub_module["time"]
            total_tokens_in += sub_module["tokens_in"]
            total_tokens_out += sub_module["tokens_out"]

            # Notify step completion with token counts
            live_block.notify_step_completed(
                tokens_in=sub_module["tokens_in"], tokens_out=sub_module["tokens_out"]
            )

            # Small delay between steps
            await asyncio.sleep(0.1)

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
                    "wall_time_seconds", total_time
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
