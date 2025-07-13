"""Debug Cognition Module

Enhanced module for debug mode that creates proper sub-module widgets
with timers, progress bars, and token counters.
"""

import time
import random
from typing import Optional, Dict, Any
from .base import CognitionModule, CognitionResult, CognitionEvent
from ..core.config import Config


class DebugCognitionModule(CognitionModule):
    """Debug cognition module with proper sub-module events"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processing_duration = Config.COGNITION_PROCESSING_DURATION

    async def process(
        self, query: str, context: Optional[Dict[str, Any]] = None
    ) -> CognitionResult:
        """Process with enhanced CognitionWidget approach"""
        print(f"DEBUG: DebugCognitionModule.process called with query: {query}")
        start_time = time.time()

        # Clear staging area and start
        await self.emit_staging_event(
            CognitionEvent(
                type="start",
                content="🧠 Debug Cognition Module Starting...",
                metadata={"clear": True},
            )
        )

        # Define sub-modules
        sub_modules = [
            {
                "module": "route_query",
                "name": "Route Query",
                "icon": "🎯",
                "duration": Config.SUBMODULE_PROCESSING_DURATION,
            },
            {
                "module": "call_tool",
                "name": "Call Tool",
                "icon": "🛠️",
                "duration": Config.SUBMODULE_PROCESSING_DURATION,
            },
            {
                "module": "format_output",
                "name": "Format Output",
                "icon": "📝",
                "duration": Config.SUBMODULE_PROCESSING_DURATION,
            }
        ]

        # Emit sub-modules to be displayed in enhanced CognitionWidget
        for i, sub_module in enumerate(sub_modules):
            print(f"DEBUG: Adding sub-module {i}: {sub_module['name']}")

            # Generate mock tokens
            tokens_in = random.randint(50, 200)
            tokens_out = random.randint(100, 400)

            # Emit sub-module data for enhanced CognitionWidget
            await self.emit_staging_event(
                CognitionEvent(
                    type="add_submodule",
                    content=f"{sub_module['name']}",
                    metadata={
                        "name": sub_module["name"],
                        "icon": sub_module["icon"],
                        "tokens_in": tokens_in,
                        "tokens_out": tokens_out,
                        "state": "PROCESSING",
                        "progress": 0.0,
                        "timer": 0.0
                    }
                )
            )

        # Simple completion without complex async loops
        processing_time = time.time() - start_time

        # Emit completion
        await self.emit_staging_event(
            CognitionEvent(
                type="complete",
                content=f"✅ Debug Cognition Complete in {processing_time:.2f}s",
                metadata={"processing_time": processing_time},
            )
        )

        # Create cognition result for timeline inscription
        result = CognitionResult(
            role="cognition",
            content="Debug Cognition Processing Complete",
            sub_blocks=[
                {
                    "role": "route_query",
                    "module_name": "Route Query",
                    "content": f"Routed query: '{query}'",
                    "tokens_input": random.randint(50, 200),
                    "tokens_output": random.randint(100, 400),
                },
                {
                    "role": "call_tool",
                    "module_name": "Call Tool",
                    "content": "Executed tool call (mock)",
                    "tokens_input": random.randint(50, 200),
                    "tokens_output": random.randint(100, 400),
                },
                {
                    "role": "format_output",
                    "module_name": "Format Output",
                    "content": f"Formatted response in {processing_time:.2f}s",
                    "tokens_input": random.randint(50, 200),
                    "tokens_output": random.randint(100, 400),
                },
            ],
            metadata={
                "module": self.get_name(),
                "processing_time": processing_time,
                "query_length": len(query),
                "sub_modules_completed": len(sub_modules),
            },
        )

        return result

    def get_name(self) -> str:
        return "Debug Cognition Module"

    def get_description(self) -> str:
        return "Enhanced module for debug mode with proper sub-module widgets"
