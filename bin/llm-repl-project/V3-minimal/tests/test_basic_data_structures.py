#!/usr/bin/env python3
"""
Simple validation test for enhanced block data structures

This validates the core data structures without requiring full textual dependencies.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.block_metadata import (
    BlockMetadata,
    BlockRole,
    ProcessingStage,
    CognitionStep,
    EnhancedCognitionProgress,
    BlockDataValidator
)


def test_basic_metadata_structure():
    """Test basic metadata structure creation and validation"""
    print("🧪 Testing basic metadata structure...")

    # Create metadata
    metadata = BlockMetadata(
        model_name="claude-3-sonnet",
        conversation_turn=1,
        importance_level="high",
        tags=["question", "python", "decorators"],
        original_prompt="What are Python decorators?"
    )

    # Verify structure
    assert metadata.model_name == "claude-3-sonnet"
    assert metadata.conversation_turn == 1
    assert "python" in metadata.tags
    assert len(metadata.tags) == 3

    # Test serialization
    metadata_dict = metadata.to_dict()
    assert "model_name" in metadata_dict
    assert "tags" in metadata_dict
    assert metadata_dict["conversation_turn"] == 1

    # Test deserialization
    restored_metadata = BlockMetadata.from_dict(metadata_dict)
    assert restored_metadata.model_name == metadata.model_name
    assert restored_metadata.tags == metadata.tags

    print("✅ Basic metadata structure: PASSED")


def test_cognition_step_lifecycle():
    """Test cognition step creation and lifecycle"""
    print("🧪 Testing cognition step lifecycle...")

    # Create step
    step = CognitionStep(
        name="Query Analysis",
        description="Analyze user query for intent",
        icon="🔍",
        estimated_duration=2.0
    )

    # Verify initial state
    assert step.name == "Query Analysis"
    assert step.status == ProcessingStage.CREATED
    assert not step.is_completed
    assert not step.is_error
    assert step.duration is None  # Not completed yet

    # Mark as completed
    step.mark_completed("Analysis complete: educational question about Python")

    # Verify completion
    assert step.is_completed
    assert step.status == ProcessingStage.COMPLETED
    assert step.result == "Analysis complete: educational question about Python"
    assert step.duration is not None
    assert step.duration > 0

    # Test serialization
    step_dict = step.to_dict()
    assert step_dict["name"] == "Query Analysis"
    assert step_dict["status"] == "completed"
    assert step_dict["result"] is not None

    print("✅ Cognition step lifecycle: PASSED")


def test_enhanced_cognition_progress():
    """Test enhanced cognition progress tracking"""
    print("🧪 Testing enhanced cognition progress...")

    # Create progress tracker
    progress = EnhancedCognitionProgress()

    # Add steps
    steps = [
        CognitionStep(name="Parse Query", icon="📝"),
        CognitionStep(name="Retrieve Knowledge", icon="📚"),
        CognitionStep(name="Generate Response", icon="✍️")
    ]

    for step in steps:
        progress.add_step(step)

    # Verify setup
    assert progress.total_steps == 3
    assert len(progress.steps) == 3
    assert progress.progress_percentage == 0.0
    assert progress.current_step is None  # No step started yet

    # Start first step
    current_step = progress.start_next_step()
    assert current_step is not None
    assert current_step.name == "Parse Query"
    assert current_step.status == ProcessingStage.PROCESSING
    assert progress.current_step_index == 0

    # Complete first step
    progress.complete_current_step("Parsed successfully", tokens_in=5, tokens_out=2)
    assert progress.completed_steps == 1
    assert progress.progress_percentage > 0.0
    assert progress.total_tokens_input == 5
    assert progress.total_tokens_output == 2

    # Start and complete remaining steps
    progress.start_next_step()
    progress.complete_current_step("Knowledge retrieved", tokens_in=15, tokens_out=8)

    progress.start_next_step()
    progress.complete_current_step("Response generated", tokens_in=20, tokens_out=50)

    # Verify final state
    assert progress.completed_steps == 3
    assert progress.progress_percentage == 1.0
    assert progress.total_tokens_input == 40  # 5 + 15 + 20
    assert progress.total_tokens_output == 60  # 2 + 8 + 50

    # Test status summary
    status = progress.get_status_summary()
    assert "100%" in status
    assert "40↑/60↓" in status

    # Test serialization
    progress_dict = progress.to_dict()
    assert progress_dict["total_steps"] == 3
    assert progress_dict["completed_steps"] == 3
    assert len(progress_dict["steps"]) == 3

    print("✅ Enhanced cognition progress: PASSED")


def test_block_data_validation():
    """Test block data validation functionality"""
    print("🧪 Testing block data validation...")

    validator = BlockDataValidator()

    # Test valid live block data
    valid_live_data = {
        "content": "Test content",
        "tokens_input": 10,
        "tokens_output": 20,
        "wall_time_seconds": 1.5,
        "progress": 0.75,
        "sub_blocks": [],
        "metadata": {}
    }

    result = validator.validate_live_block_data(valid_live_data)
    assert result.is_valid
    assert len(result.errors) == 0

    # Test invalid live block data
    invalid_live_data = {
        "content": "Test content",
        "tokens_input": -5,  # Invalid: negative
        "tokens_output": "not_a_number",  # Invalid: wrong type
        "progress": 1.5,  # Invalid: > 1.0
        "wall_time_seconds": -1.0  # Invalid: negative
    }

    result = validator.validate_live_block_data(invalid_live_data)
    assert not result.is_valid
    assert len(result.errors) > 0
    assert any("negative" in error.lower() for error in result.errors)

    # Test valid inscribed block data
    valid_inscribed_data = {
        "id": "test-id-123",
        "role": "user",
        "content": "Test content",
        "timestamp": "2024-01-01T12:00:00",
        "metadata": {}
    }

    result = validator.validate_inscribed_block_data(valid_inscribed_data)
    assert result.is_valid
    assert len(result.errors) == 0

    # Test inscribed data with unknown role (should be warning, not error)
    unknown_role_data = valid_inscribed_data.copy()
    unknown_role_data["role"] = "unknown_role"

    result = validator.validate_inscribed_block_data(unknown_role_data)
    assert result.is_valid  # Should still be valid
    assert len(result.warnings) > 0  # But should have warning

    print("✅ Block data validation: PASSED")


def test_block_roles_and_stages():
    """Test block roles and processing stages enums"""
    print("🧪 Testing block roles and stages...")

    # Test block roles
    assert BlockRole.USER.value == "user"
    assert BlockRole.ASSISTANT.value == "assistant"
    assert BlockRole.COGNITION.value == "cognition"
    assert BlockRole.SUB_MODULE.value == "sub_module"

    # Test processing stages
    assert ProcessingStage.CREATED.value == "created"
    assert ProcessingStage.PROCESSING.value == "processing"
    assert ProcessingStage.COMPLETED.value == "completed"
    assert ProcessingStage.INSCRIBED.value == "inscribed"

    # Verify enum coverage
    expected_roles = {"user", "assistant", "cognition", "tool", "system", "sub_module", "error", "debug"}
    actual_roles = {role.value for role in BlockRole}
    assert expected_roles == actual_roles

    expected_stages = {
        "created", "queued", "processing", "streaming", "completing",
        "completed", "transitioning", "inscribed", "error", "cancelled"
    }
    actual_stages = {stage.value for stage in ProcessingStage}
    assert expected_stages == actual_stages

    print("✅ Block roles and stages: PASSED")


def run_all_tests():
    """Run all basic data structure tests"""
    print("🚀 Running Enhanced Block Data Structure Tests")
    print("=" * 50)

    try:
        test_basic_metadata_structure()
        test_cognition_step_lifecycle()
        test_enhanced_cognition_progress()
        test_block_data_validation()
        test_block_roles_and_stages()

        print("=" * 50)
        print("🎉 ALL TESTS PASSED!")
        print("✅ Enhanced block data structures are working correctly")
        print("✅ Validation systems functioning properly")
        print("✅ Metadata tracking operational")
        print("✅ Cognition progress enhanced")
        print("✅ Ready for integration with Sacred Timeline")

        return True

    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
