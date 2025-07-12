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
        
        # Start progress tracking
        if self.live_block.cognition_progress:
            self.live_block.notify_step_started()
        
        # Simulate work with internal sleep
        steps = [
            ("Structuring response outline...", 0.25),
            ("Generating content sections...", 0.5),
            ("Adding citations and references...", 0.75),
            ("Applying formatting and polish...", 0.9),
            ("Response ready for delivery", 1.0)
        ]
        
        for step_text, progress in steps:
            # Update content
            self.live_block.stream_content(f"\n → {step_text}")
            
            # Update progress
            if self.live_block.cognition_progress:
                self.live_block.data.progress = progress
                
            # Simulate processing
            await asyncio.sleep(processing_time / len(steps))
        
        # Complete with token counts
        if self.live_block.cognition_progress:
            self.live_block.notify_step_completed(
                tokens_in=tokens_in, 
                tokens_out=tokens_out
            )
            
        # Notify parent we're done
        await self._notify_completion()