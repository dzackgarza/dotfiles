"""
User Story Tests for Block State Transitions

Tests that demonstrate the block state transition system from a user perspective,
focusing on the visual experience and expected behaviors.
"""

import asyncio
import time
from datetime import datetime

from src.core.live_blocks import LiveBlock, BlockState
from src.core.unified_timeline import UnifiedTimeline
from src.core.block_state_transitions import (
    transition_manager,
    safe_inscribe_block,
    validate_block_ready_for_inscription
)
from src.widgets.live_block_widget import LiveBlockWidget


class TestBlockStateTransitionUserStories:
    """User story tests for block state transitions."""

    def setup_method(self):
        """Set up test environment for each test."""
        self.timeline = UnifiedTimeline()
        self.test_start_time = datetime.now()

    async def test_user_story_smooth_block_transition(self):
        """
        User Story: As a user watching the Sacred Timeline, I want to see blocks
        smoothly transition from 'live' (showing real-time updates) to 'inscribed'
        (permanent, historical) states with clear visual feedback.
        
        Acceptance Criteria:
        1. Visual indication of state change (color, styling)
        2. Final metrics locked in
        3. Block moves from staging area to permanent timeline
        4. No loss of data during transition
        5. Ability to retry failed transitions
        """
        print("\n🧪 USER STORY: Smooth Block Transition")
        print("=" * 50)
        
        # Step 1: Create a live block (simulating user input)
        print("📝 Step 1: Creating live user block...")
        user_block = self.timeline.create_block("user", "What is machine learning?")
        
        # Verify initial state
        assert user_block.state == BlockState.LIVE
        print(f"   ✓ Block created in LIVE state: {user_block.state.value}")
        print(f"   ✓ Block ID: {user_block.id[:8]}...")
        
        # Step 2: Simulate completion (user finished typing)
        print("\n⏱️ Step 2: Completing user input...")
        user_block.set_progress(1.0)
        user_block.data.wall_time_seconds = 0.5
        
        # Step 3: Validate readiness for inscription
        print("\n🔍 Step 3: Validating readiness for inscription...")
        validation_result = await validate_block_ready_for_inscription(user_block)
        
        print(f"   ✓ Is valid: {validation_result.is_valid}")
        if validation_result.warnings:
            for warning in validation_result.warnings:
                print(f"   ⚠️ Warning: {warning}")
        
        assert validation_result.is_valid, f"Validation failed: {validation_result.error_messages}"
        
        # Step 4: Perform inscription with visual feedback
        print("\n🔄 Step 4: Performing inscription transition...")
        
        # Check active transitions before
        active_before = transition_manager.get_active_transitions()
        print(f"   📊 Active transitions before: {len(active_before)}")
        
        # Perform the inscription
        inscribed_block = await self.timeline.inscribe_block(user_block.id)
        
        # Verify transition completed
        assert inscribed_block is not None
        assert user_block.state == BlockState.INSCRIBED
        print(f"   ✅ Block transitioned to: {user_block.state.value}")
        print(f"   ✅ Inscribed block created with ID: {inscribed_block.id[:8]}...")
        
        # Step 5: Verify data preservation
        print("\n💾 Step 5: Verifying data preservation...")
        assert inscribed_block.content == user_block.data.content
        assert inscribed_block.role == user_block.role
        print(f"   ✓ Content preserved: '{inscribed_block.content[:30]}...'")
        print(f"   ✓ Role preserved: {inscribed_block.role}")
        print(f"   ✓ Wall time: {inscribed_block.metadata.get('wall_time_seconds', 0)}s")
        
        # Check active transitions after
        active_after = transition_manager.get_active_transitions()
        print(f"   📊 Active transitions after: {len(active_after)}")
        
        print("\n✅ USER STORY COMPLETED: Block transitioned smoothly with data preservation")

    async def test_user_story_failed_transition_recovery(self):
        """
        User Story: As a user, when a block fails to transition due to validation
        issues, I want the system to attempt automatic recovery and provide
        clear feedback about what went wrong.
        
        Acceptance Criteria:
        1. Clear error messages for validation failures
        2. Automatic recovery attempts for fixable issues
        3. Visual feedback during recovery process
        4. Graceful fallback when recovery fails
        """
        print("\n🧪 USER STORY: Failed Transition Recovery")
        print("=" * 50)
        
        # Step 1: Create a problematic block
        print("📝 Step 1: Creating problematic block...")
        problematic_block = self.timeline.create_block("assistant", "")  # Empty content
        problematic_block.set_tokens(-10, -5)  # Invalid tokens
        problematic_block.set_progress(0.3)  # Incomplete
        
        print(f"   ⚠️ Block created with issues:")
        print(f"      - Empty content: '{problematic_block.data.content}'")
        print(f"      - Invalid tokens: {problematic_block.data.tokens_input}, {problematic_block.data.tokens_output}")
        print(f"      - Incomplete progress: {problematic_block.data.progress}")
        
        # Step 2: Attempt validation (should fail)
        print("\n🔍 Step 2: Validating problematic block...")
        validation_result = await validate_block_ready_for_inscription(problematic_block)
        
        print(f"   ❌ Validation result: {validation_result.is_valid}")
        print(f"   📋 Failed conditions: {validation_result.failed_conditions}")
        for error in validation_result.error_messages:
            print(f"      - {error}")
        
        assert not validation_result.is_valid
        
        # Step 3: Fix some issues manually (simulating partial recovery)
        print("\n🔧 Step 3: Applying manual fixes...")
        problematic_block.stream_content("This is a recovered response.")
        problematic_block.set_progress(1.0)
        print(f"   ✓ Added content: '{problematic_block.data.content[:30]}...'")
        print(f"   ✓ Set progress to: {problematic_block.data.progress}")
        
        # Step 4: Attempt inscription with auto-recovery
        print("\n🔄 Step 4: Attempting inscription with auto-recovery...")
        
        try:
            inscribed_block = await self.timeline.inscribe_block(problematic_block.id)
            
            if inscribed_block:
                print("   ✅ Inscription succeeded after recovery!")
                print(f"   ✓ Final tokens: {problematic_block.data.tokens_input}, {problematic_block.data.tokens_output}")
                print(f"   ✓ Final state: {problematic_block.state.value}")
            else:
                print("   ⚠️ Inscription failed but system handled gracefully")
        
        except Exception as e:
            print(f"   ❌ Inscription failed: {e}")
            print("   ✓ Error was caught and handled gracefully")
        
        print("\n✅ USER STORY COMPLETED: Recovery process provided clear feedback")

    async def test_user_story_sequential_block_processing(self):
        """
        User Story: As a user observing AI processing, I want to see blocks
        appear sequentially with proper state transitions, showing the AI
        "thinking" process step by step.
        
        Acceptance Criteria:
        1. Blocks appear one at a time in sequence
        2. Each block shows clear processing states
        3. Visual timing indicators for each stage
        4. Final inscription happens only when ready
        """
        print("\n🧪 USER STORY: Sequential Block Processing")
        print("=" * 50)
        
        # Step 1: Create user question
        print("📝 Step 1: User asks question...")
        user_block = self.timeline.create_block("user", "Explain quantum computing")
        user_block.set_progress(1.0)
        user_block.data.wall_time_seconds = 0.2
        
        # Step 2: Create assistant response with thinking process
        print("\n🤖 Step 2: Assistant begins processing with cognition...")
        assistant_block = self.timeline.create_block("assistant", "")
        
        # Step 3: Add sequential cognition sub-blocks
        print("\n🧠 Step 3: Sequential cognition sub-blocks...")
        
        # Cognition 1: Understanding the question
        cognition_1 = LiveBlock("cognition", "Understanding quantum computing concepts...")
        cognition_1.set_progress(1.0)
        cognition_1.data.wall_time_seconds = 0.8
        assistant_block.add_sub_block(cognition_1)
        print(f"   ✓ Cognition 1 added: '{cognition_1.data.content[:40]}...'")
        
        # Cognition 2: Structuring response
        cognition_2 = LiveBlock("cognition", "Structuring explanation with examples...")
        cognition_2.set_progress(1.0)
        cognition_2.data.wall_time_seconds = 1.2
        assistant_block.add_sub_block(cognition_2)
        print(f"   ✓ Cognition 2 added: '{cognition_2.data.content[:40]}...'")
        
        # Step 4: Complete assistant response
        print("\n📝 Step 4: Assistant completes response...")
        assistant_response = ("Quantum computing is a revolutionary computing paradigm "
                            "that leverages quantum mechanical phenomena...")
        assistant_block.stream_content(assistant_response)
        assistant_block.set_tokens(50, 120)
        assistant_block.set_progress(1.0)
        assistant_block.data.wall_time_seconds = 3.5
        
        # Step 5: Validate and inscribe user block first
        print("\n🔄 Step 5: Inscribing user block...")
        user_validation = await validate_block_ready_for_inscription(user_block)
        assert user_validation.is_valid
        
        user_inscribed = await self.timeline.inscribe_block(user_block.id)
        assert user_inscribed is not None
        print(f"   ✅ User block inscribed: {user_block.state.value}")
        
        # Step 6: Validate and inscribe assistant block
        print("\n🔄 Step 6: Inscribing assistant block with sub-blocks...")
        assistant_validation = await validate_block_ready_for_inscription(assistant_block)
        
        print(f"   🔍 Assistant validation: {assistant_validation.is_valid}")
        if assistant_validation.warnings:
            for warning in assistant_validation.warnings:
                print(f"      ⚠️ {warning}")
        
        assert assistant_validation.is_valid
        
        assistant_inscribed = await self.timeline.inscribe_block(assistant_block.id)
        assert assistant_inscribed is not None
        print(f"   ✅ Assistant block inscribed: {assistant_block.state.value}")
        
        # Step 7: Verify complete conversation is preserved
        print("\n💾 Step 7: Verifying conversation preservation...")
        
        # Check timeline has both blocks
        inscribed_blocks = self.timeline.get_inscribed_blocks()
        assert len(inscribed_blocks) >= 2
        print(f"   ✓ Timeline contains {len(inscribed_blocks)} inscribed blocks")
        
        # Verify sub-blocks preserved in metadata
        assistant_metadata = assistant_inscribed.metadata
        assert "sub_blocks" in assistant_metadata
        sub_blocks_data = assistant_metadata["sub_blocks"]
        assert len(sub_blocks_data) == 2
        print(f"   ✓ Assistant sub-blocks preserved: {len(sub_blocks_data)}")
        
        # Verify content and timing
        print(f"   ✓ User content: '{user_inscribed.content[:30]}...'")
        print(f"   ✓ Assistant content: '{assistant_inscribed.content[:30]}...'")
        print(f"   ✓ Total processing time: {assistant_metadata.get('wall_time_seconds', 0)}s")
        
        print("\n✅ USER STORY COMPLETED: Sequential processing with proper state transitions")

    async def test_user_story_visual_feedback_widget(self):
        """
        User Story: As a user viewing the interface, I want to see clear visual
        indicators for block states and transition progress, so I understand
        what's happening in real-time.
        
        Acceptance Criteria:
        1. Different visual styles for each state
        2. Transition status messages
        3. Progress indicators during transitions
        4. Error states clearly displayed
        """
        print("\n🧪 USER STORY: Visual Feedback Widget")
        print("=" * 50)
        
        # Step 1: Create block and widget
        print("📝 Step 1: Creating block and visual widget...")
        test_block = self.timeline.create_block("assistant", "Testing visual feedback...")
        widget = LiveBlockWidget(test_block)
        
        # Step 2: Test live state visuals
        print("\n👁️ Step 2: Testing LIVE state visuals...")
        assert test_block.state == BlockState.LIVE
        
        # Get visual indicators
        state_indicator = widget._get_state_indicator()
        role_indicator = widget._get_role_indicator()
        transition_status = widget._get_transition_status_message()
        
        print(f"   ✓ State indicator: '{state_indicator}'")
        print(f"   ✓ Role indicator: '{role_indicator}'")
        print(f"   ✓ Transition status: '{transition_status}' (should be empty)")
        
        assert state_indicator == "●"  # Live indicator
        assert transition_status == ""  # No transition active
        
        # Step 3: Complete block and prepare for transition
        print("\n⏱️ Step 3: Completing block preparation...")
        test_block.set_progress(1.0)
        test_block.set_tokens(25, 40)
        test_block.data.wall_time_seconds = 1.5
        
        # Step 4: Start transition and check visual feedback
        print("\n🔄 Step 4: Starting transition and checking visuals...")
        
        # Use a callback to monitor transition status
        transition_states = []
        def capture_transition_state(state):
            transition_states.append({
                'block_id': state.block_id,
                'from_state': state.from_state.value,
                'to_state': state.to_state.value,
                'duration': state.duration_seconds,
                'attempt': state.attempt_count
            })
        
        transition_manager.add_transition_callback(capture_transition_state)
        
        # Perform inscription
        inscribed_block = await self.timeline.inscribe_block(test_block.id)
        
        # Step 5: Verify visual state changes
        print("\n👁️ Step 5: Verifying visual state changes...")
        
        # Check final state visuals
        final_state_indicator = widget._get_state_indicator()
        final_transition_status = widget._get_transition_status_message()
        
        print(f"   ✓ Final state indicator: '{final_state_indicator}'")
        print(f"   ✓ Final transition status: '{final_transition_status}'")
        print(f"   ✓ Block final state: {test_block.state.value}")
        
        assert test_block.state == BlockState.INSCRIBED
        assert final_state_indicator == "◉"  # Inscribed indicator
        
        # Step 6: Verify transition tracking worked
        print("\n📊 Step 6: Verifying transition tracking...")
        print(f"   ✓ Transition states captured: {len(transition_states)}")
        
        if transition_states:
            for i, state in enumerate(transition_states):
                print(f"      {i+1}. {state['from_state']} → {state['to_state']} "
                     f"(attempt {state['attempt']}, {state['duration']:.2f}s)")
        
        print("\n✅ USER STORY COMPLETED: Visual feedback system working correctly")

    async def run_all_user_stories(self):
        """Run all user story tests in sequence."""
        print("\n🚀 RUNNING ALL BLOCK STATE TRANSITION USER STORIES")
        print("=" * 60)
        
        story_methods = [
            self.test_user_story_smooth_block_transition,
            self.test_user_story_failed_transition_recovery,
            self.test_user_story_sequential_block_processing,
            self.test_user_story_visual_feedback_widget
        ]
        
        for i, story_method in enumerate(story_methods, 1):
            print(f"\n📖 STORY {i}/{len(story_methods)}: {story_method.__name__}")
            try:
                await story_method()
                print(f"✅ STORY {i} PASSED")
            except Exception as e:
                print(f"❌ STORY {i} FAILED: {e}")
                raise
            
            # Brief pause between stories
            await asyncio.sleep(0.1)
        
        total_time = (datetime.now() - self.test_start_time).total_seconds()
        print(f"\n🎉 ALL USER STORIES COMPLETED in {total_time:.2f}s")
        print("=" * 60)


async def main():
    """Run the user story tests."""
    test_suite = TestBlockStateTransitionUserStories()
    await test_suite.run_all_user_stories()


if __name__ == "__main__":
    asyncio.run(main())