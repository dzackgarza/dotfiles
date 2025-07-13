#!/usr/bin/env python3
"""
User Story Test: Block Data Structure Validation

This test validates the enhanced data structures for live vs inscribed blocks
through a complete user story demonstrating proper structure and validation.

USER STORY: User creates blocks and sees proper data structure validation
12-Step Flow:
1. Launch - Initialize clean timeline environment
2. Focus - Create live block with proper structure
3. Input - Add content and metadata to block
4. Submit - Validate live block data integrity
5. Process Start - Begin block processing simulation
6. Active - Show live block with real-time updates
7. Working - Demonstrate metadata tracking during updates
8. Streaming - Stream content while maintaining structure
9. Complete - Finalize block processing
10. Collapse - Transition from live to inscribed state
11. Updated - Verify inscribed block structure
12. Ready - Confirm data integrity maintained throughout
"""

import pytest
import asyncio
import time

from src.core.block_metadata import (
    BlockMetadata,
    ProcessingStage,
    CognitionStep,
    EnhancedCognitionProgress,
    BlockDataValidator
)
from src.core.live_blocks import BlockState, InscribedBlock
from src.core.unified_timeline import UnifiedTimeline


class TestBlockDataStructuresUserStory:
    """Test enhanced block data structures through complete user story"""

    def setup_method(self):
        """Setup for each test - Step 1: Launch"""
        self.timeline = UnifiedTimeline()
        self.validator = BlockDataValidator()

        # Track story progression
        self.story_steps = []
        self.step_screenshots = {}

        print("📱 Step 1: Launch - Timeline initialized with clean state")
        self.story_steps.append("launch_complete")

    def test_step_02_create_live_block_structure(self):
        """Step 2: Focus - Create live block with proper structure"""
        print("👤 Step 2: Focus - Creating live block with enhanced structure")

        # Create live block with enhanced metadata
        live_block = self.timeline.add_live_block("user", "What are Python decorators?")

        # Verify basic structure exists
        assert live_block.id is not None
        assert live_block.role == "user"
        assert live_block.state == BlockState.LIVE
        assert live_block.data.content == "What are Python decorators?"

        # Verify enhanced metadata structure can be attached
        enhanced_metadata = BlockMetadata(
            model_name="claude-3-sonnet",
            conversation_turn=1,
            importance_level="normal",
            tags=["question", "python"],
            original_prompt="What are Python decorators?"
        )

        live_block.data.metadata["enhanced"] = enhanced_metadata.to_dict()

        # Verify structure integrity
        validation_result = self.validator.validate_live_block_data(live_block.data.to_dict())
        assert validation_result.is_valid, f"Validation errors: {validation_result.errors}"

        self.story_steps.append("live_block_created")
        self.live_block = live_block

        print(f"✅ Live block created with ID: {live_block.id}")
        print(f"📋 Enhanced metadata attached: {enhanced_metadata.tags}")

    def test_step_03_add_content_and_metadata(self):
        """Step 3: Input - Add content and metadata to block"""
        print("📝 Step 3: Input - Adding content and metadata to block")

        # Ensure we have a live block from previous step
        if not hasattr(self, 'live_block'):
            self.test_step_02_create_live_block_structure()

        block = self.live_block

        # Add processing steps to metadata
        processing_steps = [
            "Query received and parsed",
            "Intent analysis: educational question",
            "Knowledge retrieval: Python decorators",
            "Response structuring",
            "Content generation"
        ]

        block.data.metadata["processing_steps"] = processing_steps
        block.data.metadata["query_type"] = "educational"
        block.data.metadata["complexity_level"] = "intermediate"

        # Update content with user context
        block.update_content("What are Python decorators? I'm learning about advanced Python features.")

        # Verify content and metadata integrity
        assert "learning about advanced Python" in block.data.content
        assert block.data.metadata["processing_steps"] == processing_steps
        assert block.data.metadata["complexity_level"] == "intermediate"

        self.story_steps.append("content_metadata_added")

        print(f"📄 Content updated: {len(block.data.content)} characters")
        print(f"🔧 Processing steps added: {len(processing_steps)} steps")

    def test_step_04_validate_live_block_integrity(self):
        """Step 4: Submit - Validate live block data integrity"""
        print("✅ Step 4: Submit - Validating live block data integrity")

        if not hasattr(self, 'live_block'):
            self.test_step_02_create_live_block_structure()
            self.test_step_03_add_content_and_metadata()

        block = self.live_block

        # Comprehensive validation
        validation_result = self.validator.validate_live_block_data(block.data.to_dict())

        # Should be valid
        assert validation_result.is_valid, f"Block validation failed: {validation_result.errors}"

        # Verify required fields present
        block_dict = block.to_dict()
        required_fields = ["id", "role", "state", "created_at", "data"]
        for field in required_fields:
            assert field in block_dict, f"Missing required field: {field}"

        # Verify data structure
        data_dict = block.data.to_dict()
        assert "content" in data_dict
        assert "tokens_input" in data_dict
        assert "tokens_output" in data_dict
        assert "metadata" in data_dict
        assert "sub_blocks" in data_dict

        # Verify metadata validation
        metadata_result = self.validator.validate_metadata(block.data.metadata)
        # Should have no errors (warnings OK for custom fields)
        assert not metadata_result.errors, f"Metadata validation errors: {metadata_result.errors}"

        self.story_steps.append("validation_passed")

        print(f"🔍 Validation passed: {len(validation_result.warnings)} warnings")
        print(f"📊 Block structure verified: {len(block_dict)} top-level fields")

    @pytest.mark.asyncio
    async def test_step_05_begin_processing_simulation(self):
        """Step 5: Process Start - Begin block processing simulation"""
        print("⚡ Step 5: Process Start - Beginning processing simulation")

        if not hasattr(self, 'live_block'):
            self.test_step_02_create_live_block_structure()
            self.test_step_03_add_content_and_metadata()
            self.test_step_04_validate_live_block_integrity()

        # Create cognition block for processing
        cognition_block = self.timeline.add_live_block("cognition", "🧠 Analyzing query about Python decorators...")

        # Initialize enhanced cognition progress
        cognition_progress = EnhancedCognitionProgress()

        # Add detailed processing steps
        steps = [
            CognitionStep(
                name="Query Analysis",
                description="Parse and understand user question",
                icon="🔍",
                estimated_duration=1.0
            ),
            CognitionStep(
                name="Knowledge Retrieval",
                description="Retrieve relevant information about decorators",
                icon="📚",
                estimated_duration=2.0
            ),
            CognitionStep(
                name="Response Generation",
                description="Generate comprehensive explanation",
                icon="✍️",
                estimated_duration=3.0
            )
        ]

        for step in steps:
            cognition_progress.add_step(step)

        # Store progress in block metadata
        cognition_block.data.metadata["enhanced_progress"] = cognition_progress.to_dict()

        # Verify processing setup
        assert len(cognition_progress.steps) == 3
        assert cognition_progress.total_steps == 3
        assert cognition_progress.progress_percentage == 0.0

        self.story_steps.append("processing_started")
        self.cognition_block = cognition_block
        self.cognition_progress = cognition_progress

        print(f"🧠 Cognition block created: {cognition_block.id}")
        print(f"📋 Processing steps configured: {len(steps)} steps")

    @pytest.mark.asyncio
    async def test_step_06_show_live_block_updates(self):
        """Step 6: Active - Show live block with real-time updates"""
        print("🔄 Step 6: Active - Demonstrating live block real-time updates")

        if not hasattr(self, 'cognition_progress'):
            await self.test_step_05_begin_processing_simulation()

        block = self.cognition_block
        progress = self.cognition_progress

        # Start first step
        current_step = progress.start_next_step()
        assert current_step is not None
        assert current_step.name == "Query Analysis"
        assert current_step.status == ProcessingStage.PROCESSING

        # Update block content with current step
        block.update_content(progress.get_status_summary())

        # Simulate some processing time and updates
        await asyncio.sleep(0.1)
        current_step.progress_percentage = 0.5
        block.update_content(progress.get_status_summary())

        # Complete first step
        progress.complete_current_step("Query analysis complete", tokens_in=5, tokens_out=2)
        block.update_content(progress.get_status_summary())

        # Verify step completion
        assert current_step.is_completed
        assert current_step.tokens_in == 5
        assert current_step.tokens_out == 2
        assert progress.completed_steps == 1
        assert progress.progress_percentage > 0.0

        # Verify block data integrity during updates
        validation_result = self.validator.validate_live_block_data(block.data.to_dict())
        assert validation_result.is_valid

        self.story_steps.append("live_updates_working")

        print(f"🎯 Step completed: {current_step.name}")
        print(f"📊 Progress: {int(progress.progress_percentage * 100)}%")
        print(f"🔢 Tokens: {current_step.tokens_in}↑/{current_step.tokens_out}↓")

    @pytest.mark.asyncio
    async def test_step_07_demonstrate_metadata_tracking(self):
        """Step 7: Working - Demonstrate metadata tracking during updates"""
        print("📈 Step 7: Working - Tracking metadata during processing")

        if not hasattr(self, 'cognition_progress'):
            await self.test_step_05_begin_processing_simulation()
            await self.test_step_06_show_live_block_updates()

        block = self.cognition_block
        progress = self.cognition_progress

        # Start second step
        current_step = progress.start_next_step()
        assert current_step.name == "Knowledge Retrieval"

        # Track metadata changes through processing
        initial_metadata_size = len(block.data.metadata)

        # Add processing metadata
        block.data.metadata["current_model"] = "claude-3-sonnet"
        block.data.metadata["retrieval_sources"] = ["python_docs", "pep_318", "tutorials"]
        block.data.metadata["processing_stage"] = "knowledge_retrieval"

        # Update tokens and timing
        start_time = time.time()
        block.update_tokens(input_tokens=15, output_tokens=0)

        # Simulate retrieval work
        await asyncio.sleep(0.1)

        # Complete step with results
        retrieval_result = "Found comprehensive decorator information"
        progress.complete_current_step(retrieval_result, tokens_in=10, tokens_out=25)

        # Update metadata with results
        block.data.metadata["retrieval_result"] = retrieval_result
        block.data.metadata["retrieval_time"] = time.time() - start_time

        # Verify metadata integrity
        assert len(block.data.metadata) > initial_metadata_size
        assert "retrieval_sources" in block.data.metadata
        assert "retrieval_result" in block.data.metadata

        # Verify enhanced metadata structure
        metadata_validation = self.validator.validate_metadata(block.data.metadata)
        assert not metadata_validation.errors

        self.story_steps.append("metadata_tracking_verified")

        print(f"📊 Metadata fields: {len(block.data.metadata)}")
        print(f"⏱️ Retrieval time: {block.data.metadata['retrieval_time']:.3f}s")
        print(f"📚 Sources: {len(block.data.metadata['retrieval_sources'])}")

    @pytest.mark.asyncio
    async def test_step_08_stream_content_maintain_structure(self):
        """Step 8: Streaming - Stream content while maintaining structure"""
        print("📡 Step 8: Streaming - Content streaming with structure integrity")

        if not hasattr(self, 'cognition_progress'):
            await self.test_step_05_begin_processing_simulation()
            await self.test_step_06_show_live_block_updates()
            await self.test_step_07_demonstrate_metadata_tracking()

        block = self.cognition_block
        progress = self.cognition_progress

        # Start final step - response generation
        current_step = progress.start_next_step()
        assert current_step.name == "Response Generation"

        # Create assistant response block for streaming
        response_block = self.timeline.add_live_block("assistant", "")

        # Stream content while maintaining data structure
        streaming_content = [
            "Python decorators are a powerful feature that allows you to modify or extend functions.",
            "\n\nHere's a simple example:\n\n```python\ndef my_decorator(func):\n    def wrapper(*args, **kwargs):\n        print('Before function call')\n        result = func(*args, **kwargs)\n        print('After function call')\n        return result\n    return wrapper\n```",
            "\n\n@my_decorator\ndef say_hello(name):\n    print(f'Hello, {name}!')",
            "\n\nDecorators use the `@` syntax and are applied to functions or classes to enhance their behavior."
        ]

        # Stream content in chunks
        total_chars = 0
        for i, chunk in enumerate(streaming_content):
            # Stream this chunk
            response_block.append_content(chunk)
            total_chars += len(chunk)

            # Update streaming metadata
            response_block.data.metadata["streaming_progress"] = (i + 1) / len(streaming_content)
            response_block.data.metadata["chars_streamed"] = total_chars
            response_block.data.metadata["chunks_received"] = i + 1

            # Validate structure during streaming
            validation_result = self.validator.validate_live_block_data(response_block.data.to_dict())
            assert validation_result.is_valid, f"Structure corrupted during streaming: {validation_result.errors}"

            # Brief pause to simulate streaming
            await asyncio.sleep(0.05)

        # Complete response generation
        progress.complete_current_step("Response generated successfully", tokens_in=20, tokens_out=150)

        # Verify final content and structure
        assert len(response_block.data.content) == total_chars
        assert "Python decorators are a powerful feature" in response_block.data.content
        assert "@my_decorator" in response_block.data.content
        assert response_block.data.metadata["chunks_received"] == len(streaming_content)

        self.story_steps.append("streaming_completed")
        self.response_block = response_block

        print(f"📝 Content streamed: {total_chars} characters")
        print(f"📦 Chunks: {len(streaming_content)} parts")
        print("🔍 Structure maintained throughout streaming")

    @pytest.mark.asyncio
    async def test_step_09_finalize_processing(self):
        """Step 9: Complete - Finalize block processing"""
        print("🏁 Step 9: Complete - Finalizing block processing")

        if not hasattr(self, 'response_block'):
            await self.test_step_05_begin_processing_simulation()
            await self.test_step_06_show_live_block_updates()
            await self.test_step_07_demonstrate_metadata_tracking()
            await self.test_step_08_stream_content_maintain_structure()

        cognition_block = self.cognition_block
        response_block = self.response_block
        progress = self.cognition_progress

        # Finalize cognition processing
        cognition_block.data.progress = 1.0
        cognition_block.data.metadata["final_status"] = "completed"
        cognition_block.data.metadata["total_processing_time"] = progress.elapsed_time

        # Add completion metadata
        completion_metadata = BlockMetadata(
            completion_status="completed",
            wall_time_seconds=progress.elapsed_time,
            tokens_input=progress.total_tokens_input,
            tokens_output=progress.total_tokens_output,
            processing_steps=[step.name for step in progress.steps]
        )

        cognition_block.data.metadata["completion_summary"] = completion_metadata.to_dict()

        # Finalize response block
        response_block.data.progress = 1.0
        final_tokens = len(response_block.data.content) // 4  # Rough token estimate
        response_block.update_tokens(output_tokens=final_tokens)

        # Verify both blocks are ready for inscription
        cognition_validation = self.validator.validate_live_block_data(cognition_block.data.to_dict())
        response_validation = self.validator.validate_live_block_data(response_block.data.to_dict())

        assert cognition_validation.is_valid
        assert response_validation.is_valid
        assert cognition_block.data.progress == 1.0
        assert response_block.data.progress == 1.0

        self.story_steps.append("processing_finalized")

        print(f"⏱️ Total processing time: {progress.elapsed_time:.2f}s")
        print(f"🔢 Total tokens: {progress.total_tokens_input}↑/{progress.total_tokens_output}↓")
        print("✅ Both blocks ready for inscription")

    @pytest.mark.asyncio
    async def test_step_10_transition_to_inscribed(self):
        """Step 10: Collapse - Transition from live to inscribed state"""
        print("🔄 Step 10: Collapse - Transitioning to inscribed state")

        if not hasattr(self, 'response_block'):
            await self.test_step_05_begin_processing_simulation()
            await self.test_step_06_show_live_block_updates()
            await self.test_step_07_demonstrate_metadata_tracking()
            await self.test_step_08_stream_content_maintain_structure()
            await self.test_step_09_finalize_processing()

        cognition_block = self.cognition_block
        response_block = self.response_block

        # Capture live state data before inscription
        live_cognition_data = cognition_block.data.to_dict()
        live_response_data = response_block.data.to_dict()

        # Inscribe blocks
        inscribed_cognition = await self.timeline.inscribe_block(cognition_block.id)
        inscribed_response = await self.timeline.inscribe_block(response_block.id)

        # Verify inscription successful
        assert inscribed_cognition is not None
        assert inscribed_response is not None
        assert isinstance(inscribed_cognition, InscribedBlock)
        assert isinstance(inscribed_response, InscribedBlock)

        # Verify data preservation during transition
        assert inscribed_cognition.content == live_cognition_data["content"]
        assert inscribed_response.content == live_response_data["content"]

        # Verify metadata preservation
        assert "completion_summary" in inscribed_cognition.metadata
        assert "streaming_progress" in inscribed_response.metadata

        # Verify token data preserved
        assert inscribed_cognition.metadata["tokens_input"] == live_cognition_data["tokens_input"]
        assert inscribed_response.metadata["tokens_output"] == live_response_data["tokens_output"]

        self.story_steps.append("inscription_completed")
        self.inscribed_cognition = inscribed_cognition
        self.inscribed_response = inscribed_response

        print(f"🔒 Cognition block inscribed: {inscribed_cognition.id}")
        print(f"🔒 Response block inscribed: {inscribed_response.id}")
        print(f"📊 Metadata preserved: {len(inscribed_cognition.metadata)} fields")

    def test_step_11_verify_inscribed_structure(self):
        """Step 11: Updated - Verify inscribed block structure"""
        print("🔍 Step 11: Updated - Verifying inscribed block structure")

        if not hasattr(self, 'inscribed_response'):
            # Run all previous steps
            asyncio.run(self._run_all_previous_steps())

        cognition_block = self.inscribed_cognition
        response_block = self.inscribed_response

        # Validate inscribed block structures
        cognition_validation = self.validator.validate_inscribed_block_data(cognition_block.to_dict())
        response_validation = self.validator.validate_inscribed_block_data(response_block.to_dict())

        assert cognition_validation.is_valid, f"Inscribed cognition validation failed: {cognition_validation.errors}"
        assert response_validation.is_valid, f"Inscribed response validation failed: {response_validation.errors}"

        # Verify required inscribed fields
        cognition_dict = cognition_block.to_dict()
        response_dict = response_block.to_dict()

        required_inscribed_fields = ["id", "role", "content", "timestamp", "metadata"]
        for field in required_inscribed_fields:
            assert field in cognition_dict, f"Missing field in cognition: {field}"
            assert field in response_dict, f"Missing field in response: {field}"

        # Verify timeline contains inscribed blocks
        timeline_blocks = self.timeline.get_inscribed_blocks()
        inscribed_ids = {block.id for block in timeline_blocks}

        assert cognition_block.id in inscribed_ids
        assert response_block.id in inscribed_ids

        # Verify no live blocks remain for our conversation
        live_blocks = self.timeline.get_live_blocks()
        our_block_ids = {cognition_block.id, response_block.id}
        live_ids = {block.id for block in live_blocks}

        assert not (our_block_ids & live_ids), "Blocks still in live state after inscription"

        self.story_steps.append("structure_verified")

        print(f"📋 Inscribed blocks validated: {len(timeline_blocks)} total")
        print(f"🎯 Our blocks in timeline: {len(our_block_ids)} blocks")
        print("✅ All structure validation passed")

    def test_step_12_confirm_data_integrity(self):
        """Step 12: Ready - Confirm data integrity maintained throughout"""
        print("🛡️ Step 12: Ready - Confirming complete data integrity")

        if not hasattr(self, 'inscribed_response'):
            asyncio.run(self._run_all_previous_steps())

        # Verify complete story progression
        expected_steps = [
            "launch_complete",
            "live_block_created",
            "content_metadata_added",
            "validation_passed",
            "processing_started",
            "live_updates_working",
            "metadata_tracking_verified",
            "streaming_completed",
            "processing_finalized",
            "inscription_completed",
            "structure_verified"
        ]

        for step in expected_steps:
            assert step in self.story_steps, f"Missing story step: {step}"

        # Final comprehensive validation
        all_blocks = self.timeline.get_all_blocks()
        validation_errors = []

        for block in all_blocks:
            if isinstance(block, InscribedBlock):
                result = self.validator.validate_inscribed_block_data(block.to_dict())
                if not result.is_valid:
                    validation_errors.extend(result.errors)

        assert not validation_errors, f"Final validation errors: {validation_errors}"

        # Verify data integrity preserved through complete lifecycle
        cognition_block = self.inscribed_cognition
        response_block = self.inscribed_response

        # Check essential data preserved
        assert cognition_block.role == "cognition"
        assert response_block.role == "assistant"
        assert "Python decorators" in response_block.content
        assert cognition_block.metadata.get("final_status") == "completed"

        # Verify enhanced metadata structures work end-to-end
        assert "completion_summary" in cognition_block.metadata
        completion_data = cognition_block.metadata["completion_summary"]
        assert completion_data["completion_status"] == "completed"
        assert len(completion_data["processing_steps"]) == 3

        self.story_steps.append("integrity_confirmed")

        print("🎉 User Story Complete: All 12 steps successful")
        print(f"📊 Final validation: {len(all_blocks)} blocks, 0 errors")
        print("🔒 Data integrity: Maintained through complete lifecycle")
        print("✅ Enhanced data structures: Working correctly")

    async def _run_all_previous_steps(self):
        """Helper to run all previous async steps"""
        await self.test_step_05_begin_processing_simulation()
        await self.test_step_06_show_live_block_updates()
        await self.test_step_07_demonstrate_metadata_tracking()
        await self.test_step_08_stream_content_maintain_structure()
        await self.test_step_09_finalize_processing()
        await self.test_step_10_transition_to_inscribed()
        self.test_step_11_verify_inscribed_structure()


# Integration test to run complete user story
@pytest.mark.asyncio
async def test_complete_user_story_block_data_structures():
    """Run complete 12-step user story for block data structures"""
    test_instance = TestBlockDataStructuresUserStory()
    test_instance.setup_method()

    # Run all 12 steps in sequence
    test_instance.test_step_02_create_live_block_structure()
    test_instance.test_step_03_add_content_and_metadata()
    test_instance.test_step_04_validate_live_block_integrity()
    await test_instance.test_step_05_begin_processing_simulation()
    await test_instance.test_step_06_show_live_block_updates()
    await test_instance.test_step_07_demonstrate_metadata_tracking()
    await test_instance.test_step_08_stream_content_maintain_structure()
    await test_instance.test_step_09_finalize_processing()
    await test_instance.test_step_10_transition_to_inscribed()
    test_instance.test_step_11_verify_inscribed_structure()
    test_instance.test_step_12_confirm_data_integrity()

    print("\n🎯 COMPLETE USER STORY SUCCESS")
    print("Enhanced block data structures validated through full lifecycle:")
    print("✅ Live block creation with enhanced metadata")
    print("✅ Real-time updates maintaining structure integrity")
    print("✅ Metadata tracking through processing stages")
    print("✅ Content streaming with validation")
    print("✅ Live to inscribed transition preserving data")
    print("✅ Complete data integrity throughout Sacred Timeline")


if __name__ == "__main__":
    # Run the complete user story
    asyncio.run(test_complete_user_story_block_data_structures())
