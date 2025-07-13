"""
Processing Queue Manager for Debug Mode

Manages sequential processing of blocks in the staging area.
Only one block can be actively processing at a time.
"""

from typing import List, Optional
import asyncio
from ..widgets.processing_widget import ProcessingWidget, ProcessingState


class ProcessingQueue:
    """Manages the sequential processing of blocks in debug mode"""

    def __init__(self, app):
        self.app = app
        self.queue: List[ProcessingWidget] = []
        self.current_processing: Optional[ProcessingWidget] = None
        self._processing_lock = asyncio.Lock()

    async def add_block(self, message: str) -> ProcessingWidget:
        """Add a new processing block to the queue"""
        # Create the widget
        widget = ProcessingWidget(message)
        self.queue.append(widget)

        # Mount it to staging area
        staging = self.app.query_one("#staging-container")
        await staging.mount(widget)

        # Start processing if nothing else is active
        if not self.current_processing:
            asyncio.create_task(self._process_next())

        return widget

    async def _process_next(self) -> None:
        """Process the next block in queue"""
        async with self._processing_lock:
            # Find next queued block
            next_block = None
            for block in self.queue:
                if block.state == ProcessingState.QUEUED:
                    next_block = block
                    break

            if not next_block:
                self.current_processing = None
                return

            # Process it
            self.current_processing = next_block
            await next_block.start_processing()

            # Process next one
            asyncio.create_task(self._process_next())

    def get_ready_blocks(self) -> List[ProcessingWidget]:
        """Get all blocks that are done and ready for inscription"""
        return [b for b in self.queue if b.state == ProcessingState.DONE]

    async def inscribe_next(self) -> bool:
        """Inscribe the next ready block to timeline"""
        ready_blocks = self.get_ready_blocks()
        if not ready_blocks:
            return False

        # Take the first ready block
        block = ready_blocks[0]

        # Remove from queue and staging area
        self.queue.remove(block)
        await block.remove()

        # Log the inscription
        self.app.log(f"Inscribed block: {block.message[:50]}...")

        return True

    def clear_all(self) -> None:
        """Clear all blocks from the queue"""
        self.queue.clear()
        self.current_processing = None
