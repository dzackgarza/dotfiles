"""Input processing component following Sacred Timeline architecture

Handles user input processing and coordinates the Sacred Turn Structure:
[User] → [Cognition] → [Assistant]
"""

from typing import TYPE_CHECKING, TypedDict

from ..config import TimelineConfig
from ..sacred_timeline import SubBlock
from .live_blocks import LiveBlockManager


class SubModuleData(TypedDict):
    name: str
    icon: str
    model: str
    time: float
    tokens_in: int
    tokens_out: int


if TYPE_CHECKING:
    from ..sacred_timeline import SacredTimeline
    from .response_generator import ResponseGenerator


class InputProcessor:
    """Processes user input following Sacred Timeline patterns

    Responsibilities:
    - Validate and sanitize user input
    - Add user blocks to Sacred Timeline
    - Coordinate cognition processing
    - Trigger assistant response generation
    - Manage live blocks during processing
    """

    def __init__(
        self, timeline: "SacredTimeline", response_generator: "ResponseGenerator"
    ):
        self.timeline = timeline
        self.response_generator = response_generator
        self.live_block_manager = LiveBlockManager()

    def process_user_input(self, user_input: str) -> None:
        """Process user input through the Sacred Turn Structure

        Args:
            user_input: Raw user input text

        Sacred Turn Structure:
        1. Add user block to timeline
        2. Generate and add cognition block
        3. Generate and add assistant response block
        """
        user_input = user_input.strip()

        if not user_input:
            return

        # Step 1: Add user message to Sacred Timeline
        self.timeline.add_block(role="user", content=user_input)

        # Step 2: Generate cognition processing block
        self._add_cognition_block(user_input)

        # Step 3: Generate assistant response
        response = self.response_generator.generate_response(user_input)
        self.timeline.add_block(role="assistant", content=response)

    def _add_cognition_block(self, user_input: str) -> None:
        """Add cognition processing block with 3 sub-blocks to timeline

        Creates the transparent cognition pipeline with 3 sub-modules:
        1. Route query - Intent classification and routing
        2. Call tool - Tool execution or external API calls
        3. Format output - Response formatting and presentation

        Args:
            user_input: User input being processed
        """
        import time
        import random

        # Create a live cognition block
        live_block = self.live_block_manager.create_live_block(
            role="cognition",
            initial_content="**Cognition Pipeline** starting...\n\n⏳ Processing...",
        )

        # Register update callback to notify timeline observers
        def on_block_update(block_id: str):
            # Get the live block and notify timeline observers
            if block_id in self.live_block_manager.live_blocks:
                live_block_data = self.live_block_manager.live_blocks[block_id]
                # Notify timeline observers about the live update
                for observer in self.timeline._observers:
                    if hasattr(observer, "on_live_block_update"):
                        observer.on_live_block_update(live_block_data)

        live_block.add_update_callback(lambda block: on_block_update(block.id))

        # Simulate cognition sub-modules with realistic data
        sub_modules_data: list[SubModuleData] = [
            {
                "name": "Route query",
                "icon": "🧠",
                "model": "tinyllama-v2",
                "time": random.uniform(0.1, 0.3),
                "tokens_in": random.randint(5, 15),
                "tokens_out": random.randint(1, 5),
            },
            {
                "name": "Call tool",
                "icon": "🛠️",
                "model": "brave_web_search",
                "time": random.uniform(1.0, 4.0),
                "tokens_in": random.randint(10, 20),
                "tokens_out": random.randint(1000, 1500),
            },
            {
                "name": "Format output",
                "icon": "🤖",
                "model": "mistral-7b-instruct",
                "time": random.uniform(0.5, 2.0),
                "tokens_in": random.randint(400, 600),
                "tokens_out": random.randint(200, 300),
            },
        ]

        total_time = 0.0
        total_tokens_in = 0
        total_tokens_out = 0

        # Process each sub-module and update live block
        for i, sub_module in enumerate(sub_modules_data):
            time.sleep(0.05)  # Simulate some processing time

            step_time = float(sub_module["time"])
            step_tokens_in = int(sub_module["tokens_in"])
            step_tokens_out = int(sub_module["tokens_out"])

            total_time += step_time
            total_tokens_in += step_tokens_in
            total_tokens_out += step_tokens_out

            # Create sub-block content
            sub_block_content = (
                f"Model: `{sub_module['model']}`\n" f"Status: ✅ Complete"
            )

            # Use the step name as the type (convert to snake_case for consistency)
            step_type = sub_module["name"].lower().replace(" ", "_")

            # Create a live sub-block
            sub_live_block = self.live_block_manager.create_live_block(
                role=step_type, initial_content=sub_block_content
            )

            # Add sub-block to live block
            live_block.add_sub_block(sub_live_block)

            # Update progress
            progress = (i + 1) / len(sub_modules_data)
            live_block.update_progress(progress)

            # Update tokens
            live_block.update_tokens(total_tokens_in, total_tokens_out)

            # Update main content with progress
            main_content = (
                f"**Cognition Pipeline** in progress...\n\n"
                f"⏳ Step {i + 1}/{len(sub_modules_data)}: {sub_module['name']}\n"
                f"🔢 Tokens so far: {total_tokens_in}↑ / {total_tokens_out}↓"
            )
            live_block.update_content(main_content)

        # Final update with complete summary
        main_cognition_content = (
            f"**Cognition Pipeline** completed in {total_time:.1f}s\n\n"
            f"📊 **Summary**: {len(sub_modules_data)} modules executed\n"
            f"🔢 **Total Tokens**: {total_tokens_in}↑ / {total_tokens_out}↓\n"
            f"⚡ **Pipeline**: Route → Tool → Format"
        )
        live_block.update_content(main_cognition_content)

        # Update wall time
        live_block.data.wall_time_seconds = total_time

        # Inscribe the live block to the timeline
        inscribed_block = self.live_block_manager.inscribe_block(live_block.id)

        # Add the inscribed block to the timeline
        if inscribed_block:
            self.timeline.add_block(
                role=inscribed_block.role,
                content=inscribed_block.content,
                metadata=inscribed_block.metadata,
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

    def _create_input_preview(self, user_input: str) -> str:
        """Create a preview of user input for cognition display

        Args:
            user_input: Full user input text

        Returns:
            Truncated preview if input exceeds max length
        """
        max_length = TimelineConfig.MAX_CONTENT_PREVIEW
        if len(user_input) > max_length:
            return user_input[:max_length]
        return user_input
