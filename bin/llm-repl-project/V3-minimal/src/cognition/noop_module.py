"""No-Op Cognition Module

Pass-through module for testing the cognition pipeline.
Simply returns the query as-is without any processing.
"""

from typing import Optional, Dict, Any
from .base import CognitionModule, CognitionResult, CognitionEvent


class NoOpCognitionModule(CognitionModule):
    """No-operation cognition module - passes through query unchanged"""

    async def process(
        self, query: str, context: Optional[Dict[str, Any]] = None
    ) -> CognitionResult:
        """Pass through query without processing"""
        # Emit start event
        await self.emit_staging_event(
            CognitionEvent(type="start", content="NoOp Module: Starting pass-through")
        )

        # Emit complete event
        await self.emit_staging_event(
            CognitionEvent(
                type="complete", content="NoOp Module: Pass-through complete"
            )
        )

        # Return result for timeline inscription
        return CognitionResult(
            role="cognition",
            content=f"[NoOp Pass-through]\n{query}",
            metadata={"module": self.get_name(), "processing_time": 0},
        )

    def get_name(self) -> str:
        return "NoOp Module"

    def get_description(self) -> str:
        return "Pass-through module for testing - no processing"
