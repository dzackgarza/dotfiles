#!/usr/bin/env python3
"""
Task Schema Validation for Extended Task Structure

This module provides comprehensive validation for Task Master tasks
that include user story metadata extensions.
"""

import json
from typing import Dict, Any, List
from pathlib import Path


class TaskSchemaValidator:
    """Validates Task Master task structure with user story extensions"""

    # Valid status values for tasks
    VALID_TASK_STATUSES = {"pending", "in-progress", "done", "review", "deferred", "cancelled"}

    # Valid priority values
    VALID_PRIORITIES = {"high", "medium", "low"}

    # Valid user story status values
    VALID_STORY_STATUSES = {"none", "generated", "failing", "passing"}

    # Required fields for tasks
    REQUIRED_TASK_FIELDS = {"id", "title", "description", "status"}

    # Optional fields for tasks
    OPTIONAL_TASK_FIELDS = {
        "dependencies", "priority", "details", "testStrategy", "subtasks", "userStory"
    }

    # Required fields for user story metadata
    REQUIRED_STORY_FIELDS = {
        "storyId", "title", "description", "acceptanceCriteria",
        "status", "lastRun", "temporalGridPath", "testExecutionTime", "errorMessage"
    }

    @classmethod
    def validate_task(cls, task: Dict[str, Any], task_context: str = "") -> Dict[str, Any]:
        """
        Validate a single task including user story metadata.
        
        Args:
            task: Task dictionary to validate
            task_context: Context string for error reporting (e.g., "Task 46")
            
        Returns:
            Validation result with success status, errors, and warnings
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "context": task_context or f"Task {task.get('id', 'unknown')}"
        }

        # Validate core task structure
        cls._validate_core_task_fields(task, result)
        cls._validate_task_data_types(task, result)
        cls._validate_task_values(task, result)

        # Validate user story if present
        if "userStory" in task and task["userStory"]:
            cls._validate_user_story_structure(task["userStory"], result)

        # Validate subtasks recursively
        if "subtasks" in task and task["subtasks"]:
            cls._validate_subtasks(task["subtasks"], result)

        return result

    @classmethod
    def _validate_core_task_fields(cls, task: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Validate required and optional task fields are present"""

        # Check required fields
        for field in cls.REQUIRED_TASK_FIELDS:
            if field not in task:
                result["valid"] = False
                result["errors"].append(f"Missing required field: {field}")

        # Check for unknown fields
        known_fields = cls.REQUIRED_TASK_FIELDS | cls.OPTIONAL_TASK_FIELDS
        for field in task.keys():
            if field not in known_fields:
                result["warnings"].append(f"Unknown field: {field}")

    @classmethod
    def _validate_task_data_types(cls, task: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Validate data types of task fields"""

        # ID should be numeric
        if "id" in task and not isinstance(task["id"], (int, float)):
            result["valid"] = False
            result["errors"].append(f"Task ID must be numeric, got: {type(task['id']).__name__}")

        # String fields
        string_fields = {"title", "description", "priority", "details", "testStrategy"}
        for field in string_fields:
            if field in task and task[field] is not None and not isinstance(task[field], str):
                result["valid"] = False
                result["errors"].append(f"Field '{field}' must be string, got: {type(task[field]).__name__}")

        # Dependencies should be a list
        if "dependencies" in task and not isinstance(task["dependencies"], list):
            result["valid"] = False
            result["errors"].append(f"Dependencies must be a list, got: {type(task['dependencies']).__name__}")

        # Subtasks should be a list
        if "subtasks" in task and not isinstance(task["subtasks"], list):
            result["valid"] = False
            result["errors"].append(f"Subtasks must be a list, got: {type(task['subtasks']).__name__}")

    @classmethod
    def _validate_task_values(cls, task: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Validate task field values are within allowed ranges"""

        # Validate status
        if "status" in task and task["status"] not in cls.VALID_TASK_STATUSES:
            result["valid"] = False
            result["errors"].append(f"Invalid status '{task['status']}'. Must be one of: {cls.VALID_TASK_STATUSES}")

        # Validate priority
        if "priority" in task and task["priority"] not in cls.VALID_PRIORITIES:
            result["valid"] = False
            result["errors"].append(f"Invalid priority '{task['priority']}'. Must be one of: {cls.VALID_PRIORITIES}")

        # Validate dependencies are numeric
        if "dependencies" in task:
            for i, dep in enumerate(task["dependencies"]):
                if not isinstance(dep, (int, float)):
                    result["valid"] = False
                    result["errors"].append(f"Dependency {i} must be numeric, got: {type(dep).__name__}")

    @classmethod
    def _validate_user_story_structure(cls, user_story: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Validate user story metadata structure"""

        # Check required user story fields
        for field in cls.REQUIRED_STORY_FIELDS:
            if field not in user_story:
                result["warnings"].append(f"Missing user story field: {field}")

        # Validate story status
        if "status" in user_story and user_story["status"] not in cls.VALID_STORY_STATUSES:
            result["valid"] = False
            result["errors"].append(f"Invalid user story status '{user_story['status']}'. Must be one of: {cls.VALID_STORY_STATUSES}")

        # Validate acceptance criteria is a list
        if "acceptanceCriteria" in user_story:
            if not isinstance(user_story["acceptanceCriteria"], list):
                result["valid"] = False
                result["errors"].append("acceptanceCriteria must be a list")
            else:
                # Validate each criterion is a string
                for i, criterion in enumerate(user_story["acceptanceCriteria"]):
                    if not isinstance(criterion, str):
                        result["valid"] = False
                        result["errors"].append(f"Acceptance criterion {i} must be a string")

        # Validate temporal grid path if present
        if "temporalGridPath" in user_story and user_story["temporalGridPath"]:
            if not isinstance(user_story["temporalGridPath"], str):
                result["valid"] = False
                result["errors"].append("temporalGridPath must be a string")

        # Validate execution time if present
        if "testExecutionTime" in user_story and user_story["testExecutionTime"]:
            if not isinstance(user_story["testExecutionTime"], (int, float)):
                result["valid"] = False
                result["errors"].append("testExecutionTime must be numeric")

    @classmethod
    def _validate_subtasks(cls, subtasks: List[Dict[str, Any]], result: Dict[str, Any]) -> None:
        """Validate subtasks recursively"""

        for i, subtask in enumerate(subtasks):
            subtask_context = f"{result['context']}.{subtask.get('id', i+1)}"
            subtask_result = cls.validate_task(subtask, subtask_context)

            # Merge subtask validation results
            if not subtask_result["valid"]:
                result["valid"] = False

            result["errors"].extend(subtask_result["errors"])
            result["warnings"].extend(subtask_result["warnings"])

    @classmethod
    def validate_tasks_file(cls, tasks_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate entire tasks.json file structure.
        
        Args:
            tasks_data: Complete tasks.json data structure
            
        Returns:
            Comprehensive validation result
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "task_count": 0,
            "story_count": 0,
            "format": "unknown"
        }

        # Detect format
        if "tasks" in tasks_data:
            result["format"] = "legacy"
            tasks_list = tasks_data["tasks"]
            result["task_count"] = len(tasks_list)

            # Validate each task
            for task in tasks_list:
                task_result = cls.validate_task(task)
                cls._merge_validation_results(result, task_result)

                # Count stories
                if "userStory" in task and task["userStory"] and task["userStory"].get("storyId"):
                    result["story_count"] += 1

        else:
            result["format"] = "tagged"
            total_tasks = 0

            # Validate each tag
            for tag_name, tag_data in tasks_data.items():
                if not isinstance(tag_data, dict) or "tasks" not in tag_data:
                    result["warnings"].append(f"Tag '{tag_name}' does not contain tasks list")
                    continue

                tasks_list = tag_data["tasks"]
                total_tasks += len(tasks_list)

                # Validate each task in this tag
                for task in tasks_list:
                    task_context = f"Tag '{tag_name}', Task {task.get('id', 'unknown')}"
                    task_result = cls.validate_task(task, task_context)
                    cls._merge_validation_results(result, task_result)

                    # Count stories
                    if "userStory" in task and task["userStory"] and task["userStory"].get("storyId"):
                        result["story_count"] += 1

            result["task_count"] = total_tasks

        return result

    @classmethod
    def _merge_validation_results(cls, main_result: Dict[str, Any], task_result: Dict[str, Any]) -> None:
        """Merge task validation result into main result"""
        if not task_result["valid"]:
            main_result["valid"] = False

        main_result["errors"].extend(task_result["errors"])
        main_result["warnings"].extend(task_result["warnings"])

    @classmethod
    def validate_tasks_file_from_path(cls, file_path: Path) -> Dict[str, Any]:
        """
        Validate tasks.json file from filesystem path.
        
        Args:
            file_path: Path to tasks.json file
            
        Returns:
            Validation result including file loading status
        """
        result = {
            "valid": False,
            "errors": [],
            "warnings": [],
            "file_loaded": False,
            "file_path": str(file_path)
        }

        try:
            if not file_path.exists():
                result["errors"].append(f"File does not exist: {file_path}")
                return result

            with open(file_path, 'r') as f:
                tasks_data = json.load(f)

            result["file_loaded"] = True

            # Validate the loaded data
            validation_result = cls.validate_tasks_file(tasks_data)
            result.update(validation_result)

        except json.JSONDecodeError as e:
            result["errors"].append(f"Invalid JSON: {e}")
        except Exception as e:
            result["errors"].append(f"Error reading file: {e}")

        return result


def main():
    """Example usage and testing"""

    # Test with extended task example
    from task_structure_extension import example_extended_task

    print("=== Task Schema Validation Demo ===\n")

    # Validate single task
    example_task = example_extended_task()
    result = TaskSchemaValidator.validate_task(example_task)

    print("Single Task Validation:")
    print(f"Valid: {result['valid']}")
    print(f"Errors: {len(result['errors'])}")
    print(f"Warnings: {len(result['warnings'])}")

    if result['errors']:
        print("Errors:")
        for error in result['errors']:
            print(f"  - {error}")

    if result['warnings']:
        print("Warnings:")
        for warning in result['warnings']:
            print(f"  - {warning}")

    print("\n" + "="*50 + "\n")

    # Test with tasks file if it exists
    tasks_file = Path("/home/dzack/dotfiles/bin/llm-repl-project/.taskmaster/tasks/tasks.json")
    if tasks_file.exists():
        print("Tasks File Validation:")
        file_result = TaskSchemaValidator.validate_tasks_file_from_path(tasks_file)

        print(f"File loaded: {file_result['file_loaded']}")
        print(f"Format: {file_result.get('format', 'unknown')}")
        print(f"Total tasks: {file_result.get('task_count', 0)}")
        print(f"Tasks with stories: {file_result.get('story_count', 0)}")
        print(f"Valid: {file_result['valid']}")

        if file_result['errors']:
            print("Errors:")
            for error in file_result['errors'][:5]:  # Show first 5 errors
                print(f"  - {error}")
            if len(file_result['errors']) > 5:
                print(f"  ... and {len(file_result['errors']) - 5} more errors")

        if file_result['warnings']:
            print("Warnings:")
            for warning in file_result['warnings'][:5]:  # Show first 5 warnings
                print(f"  - {warning}")
            if len(file_result['warnings']) > 5:
                print(f"  ... and {len(file_result['warnings']) - 5} more warnings")
    else:
        print("Tasks file not found for validation test")


if __name__ == "__main__":
    main()
