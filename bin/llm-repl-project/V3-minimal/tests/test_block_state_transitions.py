"""
Test Block State Transition Logic

Tests for the comprehensive state transition system with validation,
error handling, and recovery mechanisms.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from datetime import datetime

from src.core.live_blocks import LiveBlock, BlockState
from src.core.block_metadata import BlockRole
from src.core.block_state_transitions import (
    BlockTransitionManager,
    PreInscriptionValidator,
    StandardRecoveryStrategy,
    TransitionCondition,
    ValidationError,
    InscriptionError,
    transition_manager,
    safe_inscribe_block,
    validate_block_ready_for_inscription
)


class TestPreInscriptionValidator:
    """Test the pre-inscription validation logic."""
    
    @pytest.fixture
    def validator(self):
        return PreInscriptionValidator()
    
    @pytest.fixture
    def valid_block(self):
        """Create a valid block ready for inscription."""
        block = LiveBlock("assistant", "Complete response content")
        block.set_tokens(100, 150)
        block.set_progress(1.0)
        block.data.wall_time_seconds = 2.5
        return block
    
    @pytest.mark.asyncio
    async def test_valid_block_passes_validation(self, validator, valid_block):
        """Test that a properly completed block passes validation."""
        result = await validator.validate(valid_block)
        
        assert result.is_valid
        assert len(result.failed_conditions) == 0
        assert len(result.error_messages) == 0
        # May have warnings but should still be valid
    
    @pytest.mark.asyncio
    async def test_empty_content_fails_validation(self, validator):
        """Test that blocks with empty content fail validation."""
        block = LiveBlock("assistant", "")
        block.set_tokens(100, 150)
        block.set_progress(1.0)
        
        result = await validator.validate(block)
        
        assert not result.is_valid
        assert TransitionCondition.CONTENT_COMPLETE in result.failed_conditions
        assert any("empty" in msg.lower() for msg in result.error_messages)
    
    @pytest.mark.asyncio
    async def test_negative_tokens_fail_validation(self, validator):
        """Test that negative token counts fail validation."""
        block = LiveBlock("assistant", "Valid content")
        block.set_tokens(-10, 150)  # Negative input tokens
        block.set_progress(1.0)
        
        result = await validator.validate(block)
        
        assert not result.is_valid
        assert TransitionCondition.TOKENS_FINALIZED in result.failed_conditions
        assert any("negative" in msg.lower() for msg in result.error_messages)
    
    @pytest.mark.asyncio
    async def test_incomplete_sub_blocks_fail_validation(self, validator, valid_block):
        """Test that incomplete sub-blocks fail validation."""
        # Add incomplete sub-block
        sub_block = LiveBlock("cognition", "Partial thinking...")
        sub_block.set_progress(0.5)  # Not complete
        valid_block.add_sub_block(sub_block)
        
        result = await validator.validate(valid_block)
        
        assert not result.is_valid
        assert TransitionCondition.SUB_BLOCKS_READY in result.failed_conditions
        assert any("sub-block" in msg.lower() for msg in result.error_messages)
    
    @pytest.mark.asyncio
    async def test_active_simulation_fails_validation(self, validator, valid_block):
        """Test that blocks with active simulations fail validation."""
        # Mock active simulation
        valid_block._is_simulating = True
        
        result = await validator.validate(valid_block)
        
        assert not result.is_valid
        assert TransitionCondition.NO_ACTIVE_OPERATIONS in result.failed_conditions
        assert any("simulation" in msg.lower() for msg in result.error_messages)
    
    @pytest.mark.asyncio
    async def test_warnings_for_edge_cases(self, validator, valid_block):
        """Test that edge cases generate warnings but don't fail validation."""
        # Set zero wall time (edge case that should warn but not fail)
        valid_block.data.wall_time_seconds = 0
        
        result = await validator.validate(valid_block)
        
        assert result.is_valid  # Still valid
        assert len(result.warnings) > 0
        assert any("wall time" in msg.lower() for msg in result.warnings)


class TestStandardRecoveryStrategy:
    """Test the standard recovery strategy."""
    
    @pytest.fixture
    def strategy(self):
        return StandardRecoveryStrategy()
    
    @pytest.fixture
    def transition_state(self):
        from src.core.block_state_transitions import TransitionState
        return TransitionState(
            block_id="test-123",
            from_state=BlockState.LIVE,
            to_state=BlockState.INSCRIBED,
            started_at=datetime.now()
        )
    
    @pytest.mark.asyncio
    async def test_recovery_stops_simulation(self, strategy, transition_state):
        """Test that recovery stops active simulations."""
        block = LiveBlock("assistant", "Content")
        block._is_simulating = True
        
        success = await strategy.recover(transition_state, block)
        
        assert success
        assert not block._is_simulating
    
    @pytest.mark.asyncio
    async def test_recovery_fixes_progress(self, strategy, transition_state):
        """Test that recovery sets progress to complete."""
        block = LiveBlock("assistant", "Content")
        block.set_progress(0.7)
        
        success = await strategy.recover(transition_state, block)
        
        assert success
        assert block.data.progress == 1.0
    
    @pytest.mark.asyncio
    async def test_recovery_fixes_negative_tokens(self, strategy, transition_state):
        """Test that recovery fixes negative token counts."""
        block = LiveBlock("assistant", "Content")
        block.set_tokens(-50, 100)  # Negative input tokens
        
        success = await strategy.recover(transition_state, block)
        
        assert success
        assert block.data.tokens_input >= 0
        assert block.data.tokens_output == 100  # Should preserve valid output tokens


class TestBlockTransitionManager:
    """Test the main transition manager."""
    
    @pytest.fixture
    def manager(self):
        return BlockTransitionManager()
    
    @pytest.fixture
    def valid_block(self):
        """Create a valid block ready for inscription."""
        block = LiveBlock("assistant", "Complete response content")
        block.set_tokens(100, 150)
        block.set_progress(1.0)
        block.data.wall_time_seconds = 2.5
        return block
    
    @pytest.mark.asyncio
    async def test_successful_transition(self, manager, valid_block):
        """Test successful transition from live to inscribed."""
        inscribed_block = await manager.transition_to_inscribed(valid_block)
        
        assert inscribed_block is not None
        assert inscribed_block.role == valid_block.role
        assert inscribed_block.content == valid_block.data.content
        assert valid_block.state == BlockState.INSCRIBED
    
    @pytest.mark.asyncio
    async def test_validation_failure_raises_error(self, manager):
        """Test that validation failure raises appropriate error."""
        invalid_block = LiveBlock("assistant", "")  # Empty content
        
        with pytest.raises(ValidationError) as exc_info:
            await manager.transition_to_inscribed(invalid_block)
        
        assert "validation" in str(exc_info.value).lower()
    
    @pytest.mark.asyncio
    async def test_force_bypasses_validation(self, manager):
        """Test that force=True bypasses validation."""
        invalid_block = LiveBlock("assistant", "")  # Empty content
        
        # Should not raise ValidationError when forced
        try:
            inscribed_block = await manager.transition_to_inscribed(
                invalid_block, 
                force=True
            )
            # May still fail at inscription level, but not validation
        except InscriptionError:
            # This is acceptable - the inscription itself may fail
            pass
    
    @pytest.mark.asyncio
    async def test_transition_context_manager(self, manager, valid_block):
        """Test that transition context properly tracks active transitions."""
        # Before transition
        assert len(manager.get_active_transitions()) == 0
        
        async with manager.transition_context(valid_block, BlockState.INSCRIBED) as transition_state:
            # During transition
            assert valid_block.id in manager.get_active_transitions()
            assert transition_state.block_id == valid_block.id
        
        # After transition
        assert len(manager.get_active_transitions()) == 0
    
    @pytest.mark.asyncio
    async def test_transition_callbacks(self, manager, valid_block):
        """Test that transition callbacks are called."""
        callback_calls = []
        
        def test_callback(transition_state):
            callback_calls.append(transition_state.block_id)
        
        manager.add_transition_callback(test_callback)
        
        await manager.transition_to_inscribed(valid_block)
        
        assert len(callback_calls) > 0
        assert valid_block.id in callback_calls
    
    @pytest.mark.asyncio
    async def test_retry_mechanism_with_recovery(self, manager):
        """Test retry mechanism with recovery attempts."""
        block = LiveBlock("assistant", "Content")
        block.set_tokens(-10, 100)  # Start with invalid state
        block.set_progress(0.5)
        
        # The recovery should fix the issues and allow successful inscription
        inscribed_block = await manager.transition_to_inscribed(block, auto_recover=True)
        
        # Should succeed after recovery
        assert inscribed_block is not None
        assert block.data.tokens_input >= 0
        assert block.data.progress == 1.0


class TestConvenienceFunctions:
    """Test the convenience functions."""
    
    @pytest.mark.asyncio
    async def test_safe_inscribe_block(self):
        """Test the safe_inscribe_block convenience function."""
        block = LiveBlock("assistant", "Complete response")
        block.set_tokens(50, 75)
        block.set_progress(1.0)
        
        inscribed_block = await safe_inscribe_block(block)
        
        assert inscribed_block is not None
        assert inscribed_block.content == "Complete response"
    
    @pytest.mark.asyncio
    async def test_validate_block_ready_for_inscription(self):
        """Test the validation convenience function."""
        block = LiveBlock("assistant", "Complete response")
        block.set_tokens(50, 75)
        block.set_progress(1.0)
        
        result = await validate_block_ready_for_inscription(block)
        
        assert result.is_valid
        assert len(result.failed_conditions) == 0


class TestIntegrationScenarios:
    """Integration tests for realistic scenarios."""
    
    @pytest.mark.asyncio
    async def test_complete_user_conversation_flow(self):
        """Test a complete user conversation flow with state transitions."""
        # Create user input block
        user_block = LiveBlock("user", "What is the capital of France?")
        user_block.set_progress(1.0)
        user_block.data.wall_time_seconds = 0.1
        
        # Create assistant response with sub-blocks
        assistant_block = LiveBlock("assistant", "")
        
        # Add cognition sub-blocks
        thinking_block = LiveBlock("cognition", "I need to recall the capital of France...")
        thinking_block.set_progress(1.0)
        assistant_block.add_sub_block(thinking_block)
        
        # Complete assistant response
        assistant_block.stream_content("The capital of France is Paris.")
        assistant_block.set_tokens(25, 8)
        assistant_block.set_progress(1.0)
        assistant_block.data.wall_time_seconds = 1.2
        
        # Validate both blocks are ready
        user_result = await validate_block_ready_for_inscription(user_block)
        assistant_result = await validate_block_ready_for_inscription(assistant_block)
        
        assert user_result.is_valid
        assert assistant_result.is_valid
        
        # Inscribe both blocks
        user_inscribed = await safe_inscribe_block(user_block)
        assistant_inscribed = await safe_inscribe_block(assistant_block)
        
        assert user_inscribed is not None
        assert assistant_inscribed is not None
        assert user_inscribed.content == "What is the capital of France?"
        assert assistant_inscribed.content == "The capital of France is Paris."
        
        # Verify sub-blocks are preserved in metadata
        assert "sub_blocks" in assistant_inscribed.metadata
        sub_blocks_data = assistant_inscribed.metadata["sub_blocks"]
        assert len(sub_blocks_data) == 1
        assert sub_blocks_data[0]["content"] == "I need to recall the capital of France..."
    
    @pytest.mark.asyncio
    async def test_error_recovery_scenario(self):
        """Test error recovery in realistic failure scenarios."""
        # Create block with multiple issues
        problematic_block = LiveBlock("assistant", "")  # Empty content
        problematic_block.set_tokens(-10, -5)  # Negative tokens
        problematic_block.set_progress(0.3)  # Incomplete
        problematic_block._is_simulating = True  # Active simulation
        
        # The transition should fail without recovery
        with pytest.raises(ValidationError):
            await safe_inscribe_block(problematic_block, auto_recover=False)
        
        # But should succeed with recovery enabled
        inscribed_block = await safe_inscribe_block(
            problematic_block, 
            auto_recover=True,
            force=True  # Bypass validation after recovery
        )
        
        # Recovery should have fixed the issues
        assert not problematic_block._is_simulating
        assert problematic_block.data.progress == 1.0
        assert problematic_block.data.tokens_input >= 0
        assert problematic_block.data.tokens_output >= 0


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])