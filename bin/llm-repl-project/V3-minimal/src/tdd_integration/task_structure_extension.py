#!/usr/bin/env python3
"""
Task Structure Extension for User Story Metadata

This module defines the extended task structure that includes user story metadata
for TDD integration with Task Master.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class UserStoryMetadata:
    """User story metadata that can be embedded in Task Master tasks"""

    # Core story identification
    story_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None

    # Acceptance criteria for validation
    acceptance_criteria: List[str] = None

    # TDD workflow tracking
    status: str = "none"  # none, generated, failing, passing
    last_run: Optional[datetime] = None
    temporal_grid_path: Optional[str] = None

    # Test execution metadata
    test_execution_time: Optional[float] = None
    error_message: Optional[str] = None

    def __post_init__(self):
        if self.acceptance_criteria is None:
            self.acceptance_criteria = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        if self.last_run:
            data['last_run'] = self.last_run.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserStoryMetadata":
        """Create from dictionary"""
        if 'last_run' in data and data['last_run']:
            data['last_run'] = datetime.fromisoformat(data['last_run'])
        return cls(**data)


class TaskStructureExtension:
    """
    Handles extending Task Master task structure with user story metadata.
    
    This class provides methods to:
    1. Add userStory field to existing tasks
    2. Validate task structure with user story metadata
    3. Migrate existing tasks to include user story fields
    4. Maintain backward compatibility
    """

    @staticmethod
    def extend_task_with_user_story(task: Dict[str, Any], user_story_metadata: Optional[UserStoryMetadata] = None) -> Dict[str, Any]:
        """
        Extend a task dictionary with user story metadata.
        
        Args:
            task: Original task dictionary from Task Master
            user_story_metadata: User story metadata to add (optional)
            
        Returns:
            Extended task dictionary with userStory field
        """
        extended_task = task.copy()

        if user_story_metadata is None:
            # Add empty user story metadata structure
            extended_task["userStory"] = {
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
        else:
            # Convert UserStoryMetadata to task format
            story_dict = user_story_metadata.to_dict()
            extended_task["userStory"] = {
                "storyId": story_dict.get("story_id"),
                "title": story_dict.get("title"),
                "description": story_dict.get("description"),
                "acceptanceCriteria": story_dict.get("acceptance_criteria", []),
                "status": story_dict.get("status", "none"),
                "lastRun": story_dict.get("last_run"),
                "temporalGridPath": story_dict.get("temporal_grid_path"),
                "testExecutionTime": story_dict.get("test_execution_time"),
                "errorMessage": story_dict.get("error_message")
            }

        return extended_task

    @staticmethod
    def extract_user_story_from_task(task: Dict[str, Any]) -> Optional[UserStoryMetadata]:
        """
        Extract user story metadata from an extended task.
        
        Args:
            task: Task dictionary that may contain userStory field
            
        Returns:
            UserStoryMetadata object or None if no user story exists
        """
        if "userStory" not in task or not task["userStory"]:
            return None

        story_data = task["userStory"]

        # Handle case where storyId is None (no user story defined)
        if not story_data.get("storyId"):
            return None

        # Convert from task format to UserStoryMetadata format
        metadata_dict = {
            "story_id": story_data.get("storyId"),
            "title": story_data.get("title"),
            "description": story_data.get("description"),
            "acceptance_criteria": story_data.get("acceptanceCriteria", []),
            "status": story_data.get("status", "none"),
            "last_run": story_data.get("lastRun"),
            "temporal_grid_path": story_data.get("temporalGridPath"),
            "test_execution_time": story_data.get("testExecutionTime"),
            "error_message": story_data.get("errorMessage")
        }

        return UserStoryMetadata.from_dict(metadata_dict)

    @staticmethod
    def validate_extended_task_structure(task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that a task has proper structure including user story metadata.
        
        Args:
            task: Task dictionary to validate
            
        Returns:
            Validation result with success status and any errors
        """
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }

        # Check core task fields
        required_fields = ["id", "title", "description", "status"]
        for field in required_fields:
            if field not in task:
                validation_result["valid"] = False
                validation_result["errors"].append(f"Missing required field: {field}")

        # Check user story structure if present
        if "userStory" in task and task["userStory"]:
            user_story = task["userStory"]

            # Check user story fields
            expected_fields = [
                "storyId", "title", "description", "acceptanceCriteria",
                "status", "lastRun", "temporalGridPath", "testExecutionTime", "errorMessage"
            ]

            for field in expected_fields:
                if field not in user_story:
                    validation_result["warnings"].append(f"Missing user story field: {field}")

            # Validate status values
            valid_statuses = ["none", "generated", "failing", "passing"]
            if "status" in user_story and user_story["status"] not in valid_statuses:
                validation_result["valid"] = False
                validation_result["errors"].append(f"Invalid user story status: {user_story['status']}. Must be one of {valid_statuses}")

            # Check acceptance criteria is a list
            if "acceptanceCriteria" in user_story and not isinstance(user_story["acceptanceCriteria"], list):
                validation_result["valid"] = False
                validation_result["errors"].append("acceptanceCriteria must be a list")

        return validation_result

    @staticmethod
    def migrate_tasks_to_include_user_stories(tasks_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Migrate existing Task Master tasks.json to include user story metadata fields.
        
        Args:
            tasks_data: Complete tasks.json data structure
            
        Returns:
            Migrated tasks data with user story fields added
        """
        migrated_data = tasks_data.copy()

        # Handle both legacy and tagged task formats
        if "tasks" in tasks_data:
            # Legacy format: {"tasks": [...]}
            migrated_data["tasks"] = [
                TaskStructureExtension.extend_task_with_user_story(task)
                for task in tasks_data["tasks"]
            ]
        else:
            # Tagged format: {"master": {"tasks": [...]}, ...}
            for tag_name, tag_data in tasks_data.items():
                if "tasks" in tag_data:
                    migrated_data[tag_name]["tasks"] = [
                        TaskStructureExtension.extend_task_with_user_story(task)
                        for task in tag_data["tasks"]
                    ]

                    # Also extend subtasks
                    for task in migrated_data[tag_name]["tasks"]:
                        if "subtasks" in task and task["subtasks"]:
                            task["subtasks"] = [
                                TaskStructureExtension.extend_task_with_user_story(subtask)
                                for subtask in task["subtasks"]
                            ]

        return migrated_data

    @staticmethod
    def update_task_user_story(task: Dict[str, Any], user_story_metadata: UserStoryMetadata) -> Dict[str, Any]:
        """
        Update an existing task with new user story metadata.
        
        Args:
            task: Existing task dictionary
            user_story_metadata: New user story metadata
            
        Returns:
            Updated task dictionary
        """
        updated_task = task.copy()

        # Convert metadata to task format
        story_dict = user_story_metadata.to_dict()
        updated_task["userStory"] = {
            "storyId": story_dict.get("story_id"),
            "title": story_dict.get("title"),
            "description": story_dict.get("description"),
            "acceptanceCriteria": story_dict.get("acceptance_criteria", []),
            "status": story_dict.get("status", "none"),
            "lastRun": story_dict.get("last_run"),
            "temporalGridPath": story_dict.get("temporal_grid_path"),
            "testExecutionTime": story_dict.get("test_execution_time"),
            "errorMessage": story_dict.get("error_message")
        }

        return updated_task


# Example usage and validation
def example_extended_task():
    """Example of a task with user story metadata"""

    # Sample user story metadata
    user_story = UserStoryMetadata(
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

    # Sample base task
    base_task = {
        "id": 46,
        "title": "Extend Task Structure with User Story Metadata",
        "description": "Extend the Task Master task structure to include user story metadata as specified in the PRD.",
        "status": "in-progress",
        "priority": "high",
        "dependencies": [45],
        "details": "1. Modify the Task data structure to include the `userStory` field...",
        "testStrategy": "Create new tasks with user story metadata and verify...",
        "subtasks": []
    }

    # Extend task with user story
    extended_task = TaskStructureExtension.extend_task_with_user_story(base_task, user_story)

    return extended_task


if __name__ == "__main__":
    # Example and validation
    example_task = example_extended_task()

    print("Extended Task Example:")
    print(json.dumps(example_task, indent=2, default=str))

    print("\nValidation Result:")
    validation = TaskStructureExtension.validate_extended_task_structure(example_task)
    print(json.dumps(validation, indent=2))

    print("\nUser Story Extraction:")
    extracted_story = TaskStructureExtension.extract_user_story_from_task(example_task)
    if extracted_story:
        print(f"Story ID: {extracted_story.story_id}")
        print(f"Status: {extracted_story.status}")
        print(f"Acceptance Criteria: {len(extracted_story.acceptance_criteria)} items")
