"""Mock Cognition Module

Simulates computation with typewriter effect for 2 seconds.
Demonstrates full cognition pipeline with staging area updates.
"""

import asyncio
import time
from typing import Optional, Dict, Any
from .base import CognitionModule, CognitionResult, CognitionEvent


class MockCognitionModule(CognitionModule):
    """Mock cognition module with simulated 2s computation"""

    async def process(
        self, query: str, context: Optional[Dict[str, Any]] = None
    ) -> CognitionResult:
        """Simulate 2s computation with typewriter effect"""
        start_time = time.time()

        # Clear staging area and start
        await self.emit_staging_event(
            CognitionEvent(
                type="start",
                content="🧠 Initializing Mock Cognition Module...",
                metadata={"clear": True},
            )
        )

        # Simulate typewriter effect with multiple stages
        stages = [
            "🤔 Analyzing query...",
            f"📝 Processing: '{query[:30]}{'...' if len(query) > 30 else ''}'",
            "🔍 Searching knowledge base...",
            "💭 Formulating response...",
            "✨ Finalizing output...",
        ]

        # Typewriter effect - update staging area progressively
        full_content = ""
        for stage in stages:
            # Add stage with newline
            full_content += stage + "\n"

            # Emit update event
            await self.emit_staging_event(
                CognitionEvent(
                    type="update", content=full_content, metadata={"stage": stage}
                )
            )

            # Wait 400ms between stages (2s / 5 stages)
            await asyncio.sleep(0.4)

        # Calculate actual processing time
        processing_time = time.time() - start_time

        # Emit completion
        await self.emit_staging_event(
            CognitionEvent(
                type="complete",
                content=full_content + f"\n✅ Complete in {processing_time:.2f}s",
                metadata={"processing_time": processing_time},
            )
        )

        # Create cognition result for timeline inscription
        # Note: This is a DIFFERENT data structure than staging area!
        result = CognitionResult(
            role="cognition",
            content="Mock Processing Complete",
            sub_blocks=[
                {
                    "role": "sub_module",
                    "module_name": "query_analysis",
                    "content": f"Analyzed query: '{query}'",
                },
                {
                    "role": "sub_module",
                    "module_name": "knowledge_search",
                    "content": "Searched knowledge base (mock)",
                },
                {
                    "role": "sub_module",
                    "module_name": "response_generation",
                    "content": f"Generated response in {processing_time:.2f}s",
                },
            ],
            metadata={
                "module": self.get_name(),
                "processing_time": processing_time,
                "query_length": len(query),
                "stages_completed": len(stages),
            },
        )

        return result

    def get_name(self) -> str:
        return "Mock Cognition Module"

    def get_description(self) -> str:
        return "Simulates 2s computation with typewriter effect"
