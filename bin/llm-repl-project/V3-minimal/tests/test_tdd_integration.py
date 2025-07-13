#!/usr/bin/env python3
"""
Test suite for TDD integration system

Tests the complete TDD workflow:
1. Task story generation
2. Story testing with temporal grids
3. Task validation
4. Task completion with proof
"""

import pytest
import tempfile
import json
import shutil
from pathlib import Path
from unittest.mock import patch
import sys

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.tdd_integration.task_story_bridge import TaskStoryManager, TaskUserStory
from src.tdd_integration.tdd_commands import (
    generate_story_command,
    test_story_command,
    validate_task_command,
    complete_with_story_command
)
from src.tdd_integration.task_structure_extension import (
    TaskStructureExtension,
    UserStoryMetadata
)
from src.tdd_integration.task_schema_validator import TaskSchemaValidator


class TestTaskStoryManager:
    """Test the TaskStoryManager core functionality"""
    
    @pytest.fixture
    def temp_project_root(self):
        """Create a temporary project root for testing"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def story_manager(self, temp_project_root):
        """Create a TaskStoryManager instance for testing"""
        return TaskStoryManager(temp_project_root)
    
    def test_story_manager_initialization(self, story_manager, temp_project_root):
        """Test TaskStoryManager initializes correctly"""
        assert story_manager.project_root == temp_project_root
        assert story_manager.stories_dir.exists()
        assert story_manager.stories_file.name == "task_stories.json"
    
    def test_generate_story_for_task(self, story_manager):
        """Test generating a user story for a task"""
        task_id = "test_47"
        task_title = "Test Task"
        user_prompt = "User tests the functionality"
        
        story = story_manager.generate_story_for_task(task_id, task_title, user_prompt)
        
        assert story.task_id == task_id
        assert story.task_title == task_title
        assert story.story_id == "task_test_47"
        assert story.story_status == "generated"
        assert len(story.acceptance_criteria) == 6
        assert user_prompt in story.story_description
    
    def test_story_persistence(self, story_manager):
        """Test that stories are properly saved and loaded"""
        task_id = "test_persist"
        task_title = "Persistence Test"
        user_prompt = "Testing persistence"
        
        # Generate a story
        story = story_manager.generate_story_for_task(task_id, task_title, user_prompt)
        
        # Create a new manager instance (simulates restart)
        new_manager = TaskStoryManager(story_manager.project_root)
        
        # Check the story was loaded
        loaded_story = new_manager.get_story_for_task(task_id)
        assert loaded_story is not None
        assert loaded_story.task_id == task_id
        assert loaded_story.story_status == "generated"
    
    def test_story_validation_requirements(self, story_manager):
        """Test story validation logic"""
        task_id = "test_validation"
        
        # No story should be invalid
        result = story_manager.validate_task_completion(task_id)
        assert not result["valid"]
        assert result["reason"] == "no_story"
        
        # Generated story without test should be invalid
        story_manager.generate_story_for_task(task_id, "Test", "Test prompt")
        result = story_manager.validate_task_completion(task_id)
        assert not result["valid"]
        assert result["reason"] == "story_not_passing"


class TestTDDCommands:
    """Test the TDD command implementations"""
    
    @pytest.fixture
    def temp_project_root(self):
        """Create a temporary project root for testing"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    @patch('src.tdd_integration.tdd_commands.get_task_story_manager')
    def test_generate_story_command(self, mock_get_manager, temp_project_root):
        """Test the generate-story command"""
        mock_manager = TaskStoryManager(temp_project_root)
        mock_get_manager.return_value = mock_manager
        
        result = generate_story_command("47", "Test prompt", "Test Task")
        
        assert result["success"] is True
        assert result["task_id"] == "47"
        assert result["story_id"] == "task_47"
        assert result["story_status"] == "generated"
    
    @patch('src.tdd_integration.tdd_commands.get_task_story_manager')
    def test_test_story_command_no_story(self, mock_get_manager, temp_project_root):
        """Test test-story command when no story exists"""
        mock_manager = TaskStoryManager(temp_project_root)
        mock_get_manager.return_value = mock_manager
        
        result = test_story_command("nonexistent")
        
        assert result["success"] is False
        assert "No user story found" in result["error"]
    
    @patch('src.tdd_integration.tdd_commands.get_task_story_manager')
    def test_validate_task_command(self, mock_get_manager, temp_project_root):
        """Test validate-task command"""
        mock_manager = TaskStoryManager(temp_project_root)
        mock_get_manager.return_value = mock_manager
        
        # Test validation with no story
        result = validate_task_command("47", require_story=True)
        assert result["valid"] is False
        
        # Test validation without requiring story
        result = validate_task_command("47", require_story=False)
        assert result["valid"] is True


class TestTaskStructureExtension:
    """Test the task structure extension functionality"""
    
    def test_extend_task_with_user_story(self):
        """Test extending a task with user story metadata"""
        base_task = {
            "id": 47,
            "title": "Test Task",
            "description": "A test task",
            "status": "pending"
        }
        
        extended_task = TaskStructureExtension.extend_task_with_user_story(base_task)
        
        assert "userStory" in extended_task
        user_story = extended_task["userStory"]
        assert user_story["storyId"] is None
        assert user_story["status"] == "none"
        assert isinstance(user_story["acceptanceCriteria"], list)
    
    def test_extract_user_story_from_task(self):
        """Test extracting user story metadata from a task"""
        task_with_story = {
            "id": 47,
            "title": "Test Task",
            "userStory": {
                "storyId": "task_47",
                "title": "Test Story",
                "description": "Test description",
                "acceptanceCriteria": ["Criterion 1", "Criterion 2"],
                "status": "generated",
                "lastRun": None,
                "temporalGridPath": None,
                "testExecutionTime": None,
                "errorMessage": None
            }
        }
        
        extracted_story = TaskStructureExtension.extract_user_story_from_task(task_with_story)
        
        assert extracted_story is not None
        assert extracted_story.story_id == "task_47"
        assert extracted_story.status == "generated"
        assert len(extracted_story.acceptance_criteria) == 2
    
    def test_validate_extended_task_structure(self):
        """Test validation of extended task structure"""
        valid_task = {
            "id": 47,
            "title": "Test Task",
            "description": "Test description",
            "status": "pending",
            "userStory": {
                "storyId": "task_47",
                "title": "Test Story",
                "description": "Test description",
                "acceptanceCriteria": ["Criterion 1"],
                "status": "generated",
                "lastRun": None,
                "temporalGridPath": None,
                "testExecutionTime": None,
                "errorMessage": None
            }
        }
        
        result = TaskStructureExtension.validate_extended_task_structure(valid_task)
        assert result["valid"] is True
        assert len(result["errors"]) == 0
    
    def test_migrate_tasks_to_include_user_stories(self):
        """Test migrating existing tasks to include user story fields"""
        legacy_tasks = {
            "tasks": [
                {
                    "id": 1,
                    "title": "Task 1",
                    "description": "Description 1",
                    "status": "pending"
                },
                {
                    "id": 2,
                    "title": "Task 2", 
                    "description": "Description 2",
                    "status": "done"
                }
            ]
        }
        
        migrated_tasks = TaskStructureExtension.migrate_tasks_to_include_user_stories(legacy_tasks)
        
        assert "tasks" in migrated_tasks
        for task in migrated_tasks["tasks"]:
            assert "userStory" in task
            assert task["userStory"]["status"] == "none"


class TestTaskSchemaValidator:
    """Test the task schema validation functionality"""
    
    def test_validate_task_valid(self):
        """Test validation of a valid task"""
        valid_task = {
            "id": 47,
            "title": "Test Task",
            "description": "Test description",
            "status": "pending",
            "userStory": {
                "storyId": "task_47",
                "title": "Test Story",
                "description": "Test description",
                "acceptanceCriteria": ["Criterion 1"],
                "status": "generated",
                "lastRun": None,
                "temporalGridPath": None,
                "testExecutionTime": None,
                "errorMessage": None
            }
        }
        
        result = TaskSchemaValidator.validate_task(valid_task)
        assert result["valid"] is True
        assert len(result["errors"]) == 0
    
    def test_validate_task_missing_fields(self):
        """Test validation of a task with missing required fields"""
        invalid_task = {
            "id": 47,
            "title": "Test Task"
            # Missing description and status
        }
        
        result = TaskSchemaValidator.validate_task(invalid_task)
        assert result["valid"] is False
        assert len(result["errors"]) > 0
    
    def test_validate_task_invalid_status(self):
        """Test validation of a task with invalid status"""
        invalid_task = {
            "id": 47,
            "title": "Test Task",
            "description": "Test description",
            "status": "invalid_status"
        }
        
        result = TaskSchemaValidator.validate_task(invalid_task)
        assert result["valid"] is False
        assert any("Invalid task status" in error for error in result["errors"])


class TestTDDWorkflow:
    """Integration test for the complete TDD workflow"""
    
    @pytest.fixture
    def temp_project_root(self):
        """Create a temporary project root for testing"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    def test_complete_tdd_workflow(self, temp_project_root):
        """Test the complete TDD workflow from story generation to completion"""
        manager = TaskStoryManager(temp_project_root)
        task_id = "workflow_test"
        task_title = "Workflow Test Task"
        user_prompt = "User tests the complete workflow"
        
        # Step 1: Generate story
        story = manager.generate_story_for_task(task_id, task_title, user_prompt)
        assert story.story_status == "generated"
        
        # Step 2: Run story test (mock the canonical pilot test)
        with patch.object(manager, '_run_canonical_pilot_test') as mock_pilot:
            mock_pilot.return_value = {
                "success": True,
                "message": "Mock canonical pilot test passed",
                "execution_time": 0.1,
                "temporal_grid_path": "/mock/path/to/grid.png"
            }
            
            result = manager.run_story_for_task(task_id)
            assert result["success"] is True
            
            # Check story status updated
            updated_story = manager.get_story_for_task(task_id)
            assert updated_story.story_status == "passing"
        
        # Step 3: Validate task completion
        validation = manager.validate_task_completion(task_id)
        assert validation["valid"] is True
        
        # Step 4: The story is ready for task completion
        assert updated_story.story_status == "passing"
        assert updated_story.temporal_grid_path is not None
        assert updated_story.last_run is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])