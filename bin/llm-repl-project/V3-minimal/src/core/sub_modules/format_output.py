"""Format Output sub-module - formats final response."""

import asyncio
import random

from .base import SubModule


class FormatOutputModule(SubModule):
    """Formats and polishes the final response."""

    def get_initial_content(self) -> str:
        """Get initial content for the live block."""
        return (
            "📝 **Format Output**\n"
            "└─ Structuring response with clear formatting and citations\n\n"
            "**Provider**: Local\n"
            "**Model**: `mistral-7b-instruct`\n"
            "**Status**: 🔄 Initializing...\n\n"
            "⏱️ 0.0s | [░░░░░░░░░░░░░░░░░░░░] 0% | 🔢 0↑/0↓"
        )

    async def execute(self) -> None:
        """Execute output formatting."""
        # Simulate processing time
        processing_time = random.uniform(0.8, 1.5)
        tokens_in = random.randint(400, 600)
        tokens_out = random.randint(200, 300)

        # Start progress tracking on parent block
        if self.parent_block and self.parent_block.cognition_progress:
            self.parent_block.notify_step_started()

        # Simulate work with internal sleep
        steps = [
            ("Structuring response outline...", 0.25),
            ("Generating content sections...", 0.5),
            ("Adding citations and references...", 0.75),
            ("Applying formatting and polish...", 0.9),
            ("Response ready for delivery", 1.0),
        ]

        for step_text, progress in steps:
            # Update progress visual in sub-block content
            # (Sub-blocks don't have cognition_progress, only parent does)
            self.live_block.data.progress = progress

            # Update display with new step and progress
            self.update_progress_display(f" → {step_text}")

            # Simulate processing
            await asyncio.sleep(processing_time / len(steps))

        # Set token counts on sub-block
        self.live_block.data.tokens_input = tokens_in
        self.live_block.data.tokens_output = tokens_out

        # Final progress update
        self.update_progress_display()

        # Complete with token counts on parent block
        if self.parent_block and self.parent_block.cognition_progress:
            self.parent_block.notify_step_completed(
                tokens_in=tokens_in, tokens_out=tokens_out
            )

        # Notify parent we're done
        await self._notify_completion()
