#!/usr/bin/env python3
"""Test if SubModuleWidget can be created without errors"""

import asyncio
from src.main import LLMReplApp
from src.core.config import Config

async def test_submodule_creation():
    Config.enable_debug_mode()

    async with LLMReplApp().run_test(size=(72, 24)) as pilot:
        # Test creating SubModuleWidget directly
        from src.widgets.sub_module import SubModuleWidget
        from src.core.live_blocks import LiveBlock

        print("Creating LiveBlock...")
        block = LiveBlock('test', 'test content')

        print("Creating SubModuleWidget...")
        widget = SubModuleWidget(block)

        print("SubModuleWidget created successfully!")

        # Test mounting it
        workspace = pilot.app.query_one("#staging-container")
        print("Mounting SubModuleWidget...")
        await workspace.mount(widget)

        print("SubModuleWidget mounted successfully!")
        print(f"Workspace now has {len(list(workspace.children))} children")

if __name__ == "__main__":
    asyncio.run(test_submodule_creation())
