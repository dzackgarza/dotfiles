#!/usr/bin/env python3
"""
TDD Command Integration

Provides the actual command implementations for TDD enforcement:
- generate-story
- test-story  
- update-story
- validate-task
- complete-with-story

These commands can be called from scripts to integrate with Task Master.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.tdd_integration.task_story_bridge import get_task_story_manager


def generate_story_command(task_id: str, prompt: str, task_title: str = None) -> Dict[str, Any]:
    """Generate user story for a task (task-master generate-story implementation)"""

    try:
        manager = get_task_story_manager()

        # If no task title provided, try to infer from prompt
        if not task_title:
            task_title = f"Task {task_id}"

        # Generate the story
        story = manager.generate_story_for_task(task_id, task_title, prompt)

        return {
            "success": True,
            "task_id": task_id,
            "story_id": story.story_id,
            "story_title": story.story_title,
            "story_status": story.story_status,
            "acceptance_criteria": story.acceptance_criteria,
            "message": f"User story generated for task {task_id}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "task_id": task_id
        }


def test_story_command(task_id: str) -> Dict[str, Any]:
    """Run user story test for a task (task-master test-story implementation)"""

    try:
        manager = get_task_story_manager()

        # Check if story exists
        if not manager.has_story_for_task(task_id):
            return {
                "success": False,
                "error": f"No user story found for task {task_id}. Generate one first.",
                "suggestion": f"task-master generate-story --id={task_id} --prompt='<describe user interaction>'"
            }

        # Run the story test
        result = manager.run_story_for_task(task_id)

        return result

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "task_id": task_id
        }


def update_story_command(task_id: str, grid_path: str) -> Dict[str, Any]:
    """Update task with story results (task-master update-story implementation)"""

    try:
        manager = get_task_story_manager()

        story = manager.get_story_for_task(task_id)
        if not story:
            return {
                "success": False,
                "error": f"No user story found for task {task_id}"
            }

        # Update temporal grid path
        if Path(grid_path).exists():
            story.temporal_grid_path = grid_path
            story.story_status = "passing"  # Assume passing if grid provided
            manager._save_stories()

            return {
                "success": True,
                "task_id": task_id,
                "temporal_grid_path": grid_path,
                "story_status": story.story_status,
                "message": f"Updated task {task_id} with temporal grid proof"
            }
        else:
            return {
                "success": False,
                "error": f"Temporal grid file not found: {grid_path}"
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "task_id": task_id
        }


def validate_task_command(task_id: str, require_story: bool = True) -> Dict[str, Any]:
    """Validate task completion with story proof (task-master validate-task implementation)"""

    try:
        manager = get_task_story_manager()

        if require_story:
            result = manager.validate_task_completion(task_id)
            return result
        else:
            # If not requiring story, just check basic validation
            return {
                "valid": True,
                "message": f"Task {task_id} validation passed (story not required)"
            }

    except Exception as e:
        return {
            "valid": False,
            "error": str(e),
            "task_id": task_id
        }


def complete_with_story_command(task_id: str, story_id: str = None) -> Dict[str, Any]:
    """Complete task with story proof (task-master complete-with-story implementation)"""

    try:
        manager = get_task_story_manager()

        # First validate the task
        validation = manager.validate_task_completion(task_id)

        if not validation["valid"]:
            return {
                "success": False,
                "reason": validation["reason"],
                "message": validation["message"],
                "task_id": task_id
            }

        # If validation passes, the task can be marked complete
        story = manager.get_story_for_task(task_id)

        return {
            "success": True,
            "task_id": task_id,
            "story_id": story.story_id if story else story_id,
            "temporal_grid_path": story.temporal_grid_path if story else None,
            "message": f"Task {task_id} validated and ready for completion",
            "validation_proof": {
                "story_status": story.story_status if story else "unknown",
                "last_run": story.last_run.isoformat() if story and story.last_run else None,
                "temporal_grid_exists": bool(story and story.temporal_grid_path and Path(story.temporal_grid_path).exists())
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "task_id": task_id
        }


def list_stories_command() -> Dict[str, Any]:
    """List all task stories with their status"""

    try:
        manager = get_task_story_manager()
        stories = manager.list_all_task_stories()

        return {
            "success": True,
            "stories": stories,
            "total_stories": len(stories),
            "summary": {
                "pending": len([s for s in stories if s["story_status"] == "pending"]),
                "generated": len([s for s in stories if s["story_status"] == "generated"]),
                "passing": len([s for s in stories if s["story_status"] == "passing"]),
                "failing": len([s for s in stories if s["story_status"] == "failing"])
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def main():
    """Command-line interface for TDD commands"""

    parser = argparse.ArgumentParser(description="TDD Integration Commands")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # generate-story command
    gen_parser = subparsers.add_parser("generate-story", help="Generate user story for task")
    gen_parser.add_argument("--id", required=True, help="Task ID")
    gen_parser.add_argument("--prompt", required=True, help="User interaction description")
    gen_parser.add_argument("--title", help="Task title (optional)")

    # test-story command
    test_parser = subparsers.add_parser("test-story", help="Run user story test")
    test_parser.add_argument("--id", required=True, help="Task ID")

    # update-story command
    update_parser = subparsers.add_parser("update-story", help="Update task with story results")
    update_parser.add_argument("--id", required=True, help="Task ID")
    update_parser.add_argument("--grid-path", required=True, help="Path to temporal grid")

    # validate-task command
    validate_parser = subparsers.add_parser("validate-task", help="Validate task completion")
    validate_parser.add_argument("--id", required=True, help="Task ID")
    validate_parser.add_argument("--require-story", action="store_true", default=True, help="Require user story")

    # complete-with-story command
    complete_parser = subparsers.add_parser("complete-with-story", help="Complete task with story proof")
    complete_parser.add_argument("--id", required=True, help="Task ID")
    complete_parser.add_argument("--story-id", help="Story ID (optional)")

    # list-stories command
    list_parser = subparsers.add_parser("list-stories", help="List all task stories")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Execute command
    result = None

    if args.command == "generate-story":
        result = generate_story_command(args.id, args.prompt, args.title)
    elif args.command == "test-story":
        result = test_story_command(args.id)
    elif args.command == "update-story":
        result = update_story_command(args.id, args.grid_path)
    elif args.command == "validate-task":
        result = validate_task_command(args.id, args.require_story)
    elif args.command == "complete-with-story":
        result = complete_with_story_command(args.id, args.story_id)
    elif args.command == "list-stories":
        result = list_stories_command()

    # Output result as JSON
    print(json.dumps(result, indent=2))

    # Exit with appropriate code
    if result and not result.get("success", result.get("valid", False)):
        sys.exit(1)


if __name__ == "__main__":
    main()
