"""Route Query sub-module - analyzes user intent."""

import asyncio
import random

from .base import SubModule
from ..config import Config


class RouteQueryModule(SubModule):
    """Analyzes user query to determine appropriate response strategy."""

    def get_initial_content(self) -> str:
        """Get initial content for the live block."""
        return (
            "🎯 **Route Query**\n"
            "└─ Analyzing user intent and determining appropriate response strategy\n\n"
            "**Provider**: Local\n"
            "**Model**: `tinyllama-v2`\n"
            "**Status**: 🔄 Initializing...\n\n"
            "⏱️ 0.0s | [░░░░░░░░░░░░░░░░░░░░] 0% | 🔢 0↑/0↓"
        )

    async def execute(self) -> None:
        """Execute route query analysis."""
        # Use configured processing time with slight variation
        base_time = Config.SUBMODULE_PROCESSING_DURATION
        processing_time = random.uniform(base_time * 0.8, base_time * 1.2)
        tokens_in = random.randint(5, 15)
        tokens_out = random.randint(1, 5)

        # Start progress tracking on parent block
        if self.parent_block and self.parent_block.cognition_progress:
            self.parent_block.notify_step_started()

        # Simulate work with internal sleep
        steps = [
            ("Analyzing query semantics...", 0.3),
            ("Detecting intent patterns...", 0.6),
            ("Route determined: CODING", 1.0),
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
