#!/usr/bin/env python3
"""
Test Suite for Task Structure Extension with User Story Metadata

Comprehensive tests for validating the task structure extension functionality.
"""

import json
import tempfile
from pathlib import Path
from datetime import datetime

from task_structure_extension import TaskStructureExtension, UserStoryMetadata
from task_schema_validator import TaskSchemaValidator


def test_user_story_metadata_creation():
    """Test creating UserStoryMetadata objects"""
    print("Testing UserStoryMetadata creation...")

    # Test basic creation
    story = UserStoryMetadata(
        story_id="test_story",
        title="Test Story",
        description="A test user story",
        acceptance_criteria=["Criterion 1", "Criterion 2"],
        status="generated"
    )

    assert story.story_id == "test_story"
    assert story.status == "generated"
    assert len(story.acceptance_criteria) == 2
    print("✅ Basic UserStoryMetadata creation")

    # Test serialization
    story_dict = story.to_dict()
    assert "story_id" in story_dict
    assert "acceptance_criteria" in story_dict
    print("✅ UserStoryMetadata serialization")

    # Test deserialization
    story_copy = UserStoryMetadata.from_dict(story_dict)
    assert story_copy.story_id == story.story_id
    assert story_copy.status == story.status
    print("✅ UserStoryMetadata deserialization")


def test_task_extension():
    """Test extending tasks with user story metadata"""
    print("\nTesting task extension...")

    # Sample base task
    base_task = {
        "id": 1,
        "title": "Test Task",
        "description": "A test task",
        "status": "pending",
        "priority": "high",
        "dependencies": [],
        "subtasks": []
    }

    # Test extending with empty user story
    extended_task = TaskStructureExtension.extend_task_with_user_story(base_task)
    assert "userStory" in extended_task
    assert extended_task["userStory"]["storyId"] is None
    assert extended_task["userStory"]["status"] == "none"
    print("✅ Task extension with empty user story")

    # Test extending with actual user story
    user_story = UserStoryMetadata(
        story_id="task_1",
        title="User validates test task",
        status="passing"
    )

    extended_task = TaskStructureExtension.extend_task_with_user_story(base_task, user_story)
    assert extended_task["userStory"]["storyId"] == "task_1"
    assert extended_task["userStory"]["status"] == "passing"
    print("✅ Task extension with actual user story")

    # Test extracting user story from task
    extracted_story = TaskStructureExtension.extract_user_story_from_task(extended_task)
    assert extracted_story is not None
    assert extracted_story.story_id == "task_1"
    assert extracted_story.status == "passing"
    print("✅ User story extraction from task")


def test_task_validation():
    """Test task validation with user story metadata"""
    print("\nTesting task validation...")

    # Valid task with user story
    valid_task = {
        "id": 1,
        "title": "Valid Task",
        "description": "A valid test task",
        "status": "pending",
        "userStory": {
            "storyId": "task_1",
            "title": "Valid Story",
            "description": "A valid story",
            "acceptanceCriteria": ["Criterion 1"],
            "status": "generated",
            "lastRun": None,
            "temporalGridPath": None,
            "testExecutionTime": None,
            "errorMessage": None
        }
    }

    result = TaskSchemaValidator.validate_task(valid_task)
    assert result["valid"] == True
    assert len(result["errors"]) == 0
    print("✅ Valid task validation passes")

    # Invalid task with bad user story status
    invalid_task = valid_task.copy()
    invalid_task["userStory"]["status"] = "invalid_status"

    result = TaskSchemaValidator.validate_task(invalid_task)
    assert result["valid"] == False
    assert any("Invalid user story status" in error for error in result["errors"])
    print("✅ Invalid user story status detected")

    # Task with non-list acceptance criteria
    invalid_task2 = valid_task.copy()
    invalid_task2["userStory"]["acceptanceCriteria"] = "not a list"

    result = TaskSchemaValidator.validate_task(invalid_task2)
    assert result["valid"] == False
    assert any("acceptanceCriteria must be a list" in error for error in result["errors"])
    print("✅ Invalid acceptance criteria type detected")


def test_tasks_file_migration():
    """Test migrating entire tasks.json file"""
    print("\nTesting tasks file migration...")

    # Sample tasks data in tagged format
    tasks_data = {
        "master": {
            "tasks": [
                {
                    "id": 1,
                    "title": "Task 1",
                    "description": "First task",
                    "status": "pending",
                    "subtasks": [
                        {
                            "id": 1,
                            "title": "Subtask 1",
                            "description": "First subtask",
                            "status": "pending"
                        }
                    ]
                },
                {
                    "id": 2,
                    "title": "Task 2",
                    "description": "Second task",
                    "status": "done"
                }
            ]
        }
    }

    # Migrate tasks
    migrated_data = TaskStructureExtension.migrate_tasks_to_include_user_stories(tasks_data)

    # Check migration results
    master_tasks = migrated_data["master"]["tasks"]

    # Check first task has user story field
    assert "userStory" in master_tasks[0]
    assert master_tasks[0]["userStory"]["status"] == "none"

    # Check subtask has user story field
    assert "userStory" in master_tasks[0]["subtasks"][0]
    assert master_tasks[0]["subtasks"][0]["userStory"]["status"] == "none"

    # Check second task has user story field
    assert "userStory" in master_tasks[1]

    print("✅ Tasks file migration successful")


def test_legacy_format_migration():
    """Test migrating legacy format tasks.json"""
    print("\nTesting legacy format migration...")

    # Legacy format tasks data
    legacy_data = {
        "tasks": [
            {
                "id": 1,
                "title": "Legacy Task",
                "description": "A legacy format task",
                "status": "pending"
            }
        ]
    }

    # Migrate
    migrated_data = TaskStructureExtension.migrate_tasks_to_include_user_stories(legacy_data)

    # Check results
    assert "tasks" in migrated_data
    assert "userStory" in migrated_data["tasks"][0]
    assert migrated_data["tasks"][0]["userStory"]["status"] == "none"

    print("✅ Legacy format migration successful")


def test_task_story_update():
    """Test updating task with new user story metadata"""
    print("\nTesting task story updates...")

    # Base task with empty user story
    task = {
        "id": 1,
        "title": "Updateable Task",
        "description": "A task to be updated",
        "status": "pending",
        "userStory": {
            "storyId": None,
            "title": None,
            "description": None,
            "acceptanceCriteria": [],
            "status": "none",
            "lastRun": None,
            "temporalGridPath": None,
            "testExecutionTime": None,
            "errorMessage": None
        }
    }

    # New user story metadata
    new_story = UserStoryMetadata(
        story_id="updated_task_1",
        title="Updated User Story",
        description="An updated user story",
        acceptance_criteria=["New criterion"],
        status="passing",
        temporal_grid_path="/path/to/grid.png",
        test_execution_time=1.5
    )

    # Update task
    updated_task = TaskStructureExtension.update_task_user_story(task, new_story)

    # Verify update
    assert updated_task["userStory"]["storyId"] == "updated_task_1"
    assert updated_task["userStory"]["status"] == "passing"
    assert updated_task["userStory"]["temporalGridPath"] == "/path/to/grid.png"
    assert updated_task["userStory"]["testExecutionTime"] == 1.5
    assert len(updated_task["userStory"]["acceptanceCriteria"]) == 1

    print("✅ Task story update successful")


def test_file_validation():
    """Test validating tasks file from filesystem"""
    print("\nTesting file validation...")

    # Create temporary test file
    test_data = {
        "master": {
            "tasks": [
                {
                    "id": 1,
                    "title": "File Test Task",
                    "description": "Task for file validation test",
                    "status": "pending",
                    "userStory": {
                        "storyId": "file_test_1",
                        "title": "File Test Story",
                        "description": "Story for file validation",
                        "acceptanceCriteria": ["File loads correctly"],
                        "status": "generated",
                        "lastRun": None,
                        "temporalGridPath": None,
                        "testExecutionTime": None,
                        "errorMessage": None
                    }
                }
            ]
        }
    }

    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f, indent=2)
        temp_path = Path(f.name)

    try:
        # Validate file
        result = TaskSchemaValidator.validate_tasks_file_from_path(temp_path)

        assert result["file_loaded"] == True
        assert result["valid"] == True
        assert result["format"] == "tagged"
        assert result["task_count"] == 1
        assert result["story_count"] == 1

        print("✅ File validation successful")

    finally:
        # Clean up
        temp_path.unlink()


def run_comprehensive_test():
    """Run all tests"""
    print("=== Task Structure Extension Test Suite ===\n")

    try:
        test_user_story_metadata_creation()
        test_task_extension()
        test_task_validation()
        test_tasks_file_migration()
        test_legacy_format_migration()
        test_task_story_update()
        test_file_validation()

        print("\n" + "="*50)
        print("🎉 ALL TESTS PASSED! Task structure extension is working correctly.")
        print("="*50)

        return True

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def demonstrate_usage():
    """Demonstrate practical usage of the task extension system"""
    print("\n=== Usage Demonstration ===\n")

    # Example: Extending Task 46 with its user story
    print("1. Creating user story for Task 46...")

    task_46_story = UserStoryMetadata(
        story_id="task_46",
        title="User validates: Extend Task Structure with User Story Metadata",
        description="User story for validating task structure extension implementation",
        acceptance_criteria=[
            "App launches and shows Sacred GUI layout",
            "User interaction triggers expected functionality",
            "Sacred Timeline displays proper block progression",
            "Live Workspace shows/hides appropriately during processing",
            "Final state shows completed task functionality",
            "Input area remains responsive for next interaction"
        ],
        status="generated"
    )

    print(f"   Story ID: {task_46_story.story_id}")
    print(f"   Status: {task_46_story.status}")
    print(f"   Criteria: {len(task_46_story.acceptance_criteria)} items")

    print("\n2. Extending base task with story...")

    base_task_46 = {
        "id": 46,
        "title": "Extend Task Structure with User Story Metadata",
        "description": "Extend the Task Master task structure to include user story metadata as specified in the PRD.",
        "status": "in-progress",
        "priority": "high",
        "dependencies": [45],
        "details": "1. Modify the Task data structure...",
        "testStrategy": "Create new tasks with user story metadata...",
        "subtasks": []
    }

    extended_task_46 = TaskStructureExtension.extend_task_with_user_story(base_task_46, task_46_story)

    print("   ✅ Task extended with user story metadata")
    print(f"   User story status: {extended_task_46['userStory']['status']}")

    print("\n3. Validating extended task...")

    validation_result = TaskSchemaValidator.validate_task(extended_task_46)
    print(f"   Valid: {validation_result['valid']}")
    print(f"   Errors: {len(validation_result['errors'])}")
    print(f"   Warnings: {len(validation_result['warnings'])}")

    print("\n4. Simulating story update after test run...")

    # Update story as if a test was run
    task_46_story.status = "passing"
    task_46_story.last_run = datetime.now()
    task_46_story.temporal_grid_path = "/path/to/task_46_temporal_grid.png"
    task_46_story.test_execution_time = 2.3

    updated_task_46 = TaskStructureExtension.update_task_user_story(extended_task_46, task_46_story)

    print(f"   Updated status: {updated_task_46['userStory']['status']}")
    print(f"   Grid path: {updated_task_46['userStory']['temporalGridPath']}")
    print(f"   Execution time: {updated_task_46['userStory']['testExecutionTime']}s")

    print("\n✅ Usage demonstration complete!")


if __name__ == "__main__":
    # Run tests
    success = run_comprehensive_test()

    if success:
        # Show usage demonstration
        demonstrate_usage()

    print(f"\nTest result: {'PASS' if success else 'FAIL'}")
