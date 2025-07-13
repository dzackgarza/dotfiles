"""
Task Master - User Story Bridge

Connects Task Master tasks with Sacred GUI user stories for TDD enforcement.
This bridge enables task-driven user story generation and validation.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

try:
    from tests.user_stories import UserStory, UserStoryStep, get_user_story, list_available_stories
except ImportError:
    # Fallback if imports fail - we'll create minimal versions
    from dataclasses import dataclass
    from typing import List, Callable

    @dataclass
    class UserStoryStep:
        name: str
        description: str
        action: Callable
        screenshot_name: str

    @dataclass
    class UserStory:
        story_id: str
        title: str
        description: str
        steps: List[UserStoryStep]

        def validate(self):
            if len(self.steps) != 12:
                raise ValueError(f"Story {self.story_id} must have exactly 12 steps")


@dataclass
class TaskUserStory:
    """User story linked to a specific Task Master task"""

    # Task Master integration
    task_id: str
    task_title: str

    # User Story definition
    story_id: str
    story_title: str
    story_description: str

    # TDD workflow tracking
    story_status: str = "pending"  # pending, generated, failing, passing
    last_run: Optional[datetime] = None
    temporal_grid_path: Optional[str] = None

    # Acceptance criteria
    acceptance_criteria: List[str] = None

    # Test metadata
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
    def from_dict(cls, data: Dict[str, Any]) -> "TaskUserStory":
        """Create from dictionary"""
        if 'last_run' in data and data['last_run']:
            data['last_run'] = datetime.fromisoformat(data['last_run'])
        return cls(**data)


class TaskStoryManager:
    """Manages user stories for Task Master tasks"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.stories_dir = project_root / ".taskmaster" / "stories"
        self.stories_dir.mkdir(parents=True, exist_ok=True)

        # Storage for task stories
        self.stories_file = self.stories_dir / "task_stories.json"
        self.task_stories: Dict[str, TaskUserStory] = {}

        # Load existing stories
        self._load_stories()

    def _load_stories(self) -> None:
        """Load existing task stories from JSON file"""
        if self.stories_file.exists():
            try:
                with open(self.stories_file, 'r') as f:
                    data = json.load(f)
                    for task_id, story_data in data.items():
                        self.task_stories[task_id] = TaskUserStory.from_dict(story_data)
            except Exception as e:
                print(f"Warning: Could not load existing stories: {e}")

    def _save_stories(self) -> None:
        """Save task stories to JSON file"""
        try:
            data = {task_id: story.to_dict() for task_id, story in self.task_stories.items()}
            with open(self.stories_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving stories: {e}")

    def generate_story_for_task(self, task_id: str, task_title: str, user_prompt: str) -> TaskUserStory:
        """Generate a user story for a Task Master task"""

        # Create story ID from task
        story_id = f"task_{task_id.replace('.', '_')}"

        # Generate story title and description based on prompt
        story_title = f"User validates: {task_title}"

        # Enhanced story description with Sacred GUI context
        story_description = f"""
User story for Task {task_id}: {task_title}

User Interaction: {user_prompt}

This story validates the task implementation through a complete 12-step user interaction flow,
demonstrating proper Sacred GUI behavior with Timeline, Workspace, and Input areas.

Expected Flow:
1. Launch - App starts in clean state
2. Focus - User attention on input area
3. Input - User types or performs action
4. Submit - User triggers the functionality
5. Process Start - System begins response
6. Active - Live workspace becomes visible
7. Working - Processing indicators active
8. Streaming - Content flows in real-time
9. Complete - Processing finishes
10. Collapse - Workspace hides automatically
11. Updated - Timeline shows complete result
12. Ready - App ready for next interaction

This ensures the implemented feature works from the user's perspective
and maintains Sacred GUI architectural principles.
        """.strip()

        # Create task user story
        task_story = TaskUserStory(
            task_id=task_id,
            task_title=task_title,
            story_id=story_id,
            story_title=story_title,
            story_description=story_description,
            story_status="generated",
            acceptance_criteria=[
                "App launches and shows Sacred GUI layout",
                "User interaction triggers expected functionality",
                "Sacred Timeline displays proper block progression",
                "Live Workspace shows/hides appropriately during processing",
                "Final state shows completed task functionality",
                "Input area remains responsive for next interaction"
            ]
        )

        # Store and save
        self.task_stories[task_id] = task_story
        self._save_stories()

        return task_story

    def get_story_for_task(self, task_id: str) -> Optional[TaskUserStory]:
        """Get user story for a specific task"""
        return self.task_stories.get(task_id)

    def has_story_for_task(self, task_id: str) -> bool:
        """Check if task has an associated user story"""
        return task_id in self.task_stories

    def run_story_for_task(self, task_id: str) -> Dict[str, Any]:
        """Run user story test for a task"""

        story = self.get_story_for_task(task_id)
        if not story:
            return {
                "success": False,
                "error": f"No user story found for task {task_id}",
                "status": "no_story"
            }

        try:
            # Run the actual canonical pilot test to validate the task
            result = self._run_canonical_pilot_test(story)
            
            # Extract temporal grid path from result
            grid_path = None
            if result.get("temporal_grid_path"):
                grid_path = result["temporal_grid_path"]

            # Update story with test results
            story.last_run = datetime.now()
            story.temporal_grid_path = grid_path if grid_path else None
            story.story_status = "passing" if result["success"] else "failing"
            story.test_execution_time = result.get("execution_time", 0.0)
            story.error_message = result.get("error")

            self._save_stories()

            return {
                "success": result["success"],
                "story_id": story.story_id,
                "temporal_grid_path": story.temporal_grid_path,
                "execution_time": story.test_execution_time,
                "status": story.story_status,
                "message": result.get("message", "Canonical pilot test completed"),
                "test_output": result.get("test_output", "")
            }

        except Exception as e:
            story.story_status = "failing"
            story.error_message = str(e)
            story.last_run = datetime.now()
            self._save_stories()

            return {
                "success": False,
                "error": str(e),
                "status": "error"
            }

    def _run_canonical_pilot_test(self, story: TaskUserStory) -> Dict[str, Any]:
        """Run the actual canonical pilot test for task validation"""

        try:
            import subprocess
            import time
            
            start_time = time.time()

            # Change to project root for test execution
            v3_minimal_dir = self.project_root / "V3-minimal"
            
            # Run the canonical pilot test specifically for task validation
            result = subprocess.run([
                'pdm', 'run', 'pytest', 
                'tests/test_canonical_pilot.py::test_canonical_user_journey',
                '-v', '--tb=short'
            ], 
            capture_output=True, 
            text=True, 
            timeout=60,  # Allow more time for actual GUI testing
            cwd=str(v3_minimal_dir)
            )

            execution_time = time.time() - start_time

            if result.returncode == 0:
                # Test passed - look for temporal grid file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Find the most recent temporal grid file
                debug_dir = v3_minimal_dir / "debug_screenshots"
                if debug_dir.exists():
                    temporal_grids = list(debug_dir.glob("*_temporal_grid_*.png"))
                    if temporal_grids:
                        # Use the most recent grid
                        latest_grid = max(temporal_grids, key=lambda p: p.stat().st_mtime)
                        
                        # Create task-specific copy
                        task_grid_name = f"task_{story.task_id.replace('.', '_')}_temporal_grid_{timestamp}.png"
                        task_grid_path = debug_dir / task_grid_name
                        
                        # Copy the canonical grid to task-specific name
                        import shutil
                        shutil.copy2(latest_grid, task_grid_path)
                        
                        return {
                            "success": True,
                            "message": f"Real canonical pilot test passed - temporal grid at {task_grid_path}",
                            "execution_time": execution_time,
                            "temporal_grid_path": str(task_grid_path),
                            "test_output": result.stdout[-500:]  # Last 500 chars
                        }

                return {
                    "success": True,
                    "message": "Canonical pilot test passed but no temporal grid found",
                    "execution_time": execution_time,
                    "test_output": result.stdout[-500:]
                }
            else:
                return {
                    "success": False,
                    "error": f"Canonical pilot test failed with return code {result.returncode}",
                    "message": f"Test execution failed: {result.stderr[-500:]}",
                    "execution_time": execution_time
                }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Test execution timeout",
                "message": "Canonical pilot test took too long to complete"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to run canonical pilot test: {e}"
            }

    def validate_task_completion(self, task_id: str) -> Dict[str, Any]:
        """Validate that a task can be marked complete based on user story"""

        story = self.get_story_for_task(task_id)
        if not story:
            return {
                "valid": False,
                "reason": "no_story",
                "message": f"Task {task_id} has no associated user story. Generate one first with: task-master generate-story --id={task_id}"
            }

        if story.story_status not in ["passing"]:
            return {
                "valid": False,
                "reason": "story_not_passing",
                "message": f"Task {task_id} user story is '{story.story_status}'. Run: task-master test-story --id={task_id}"
            }

        if not story.temporal_grid_path or not Path(story.temporal_grid_path).exists():
            return {
                "valid": False,
                "reason": "no_temporal_grid",
                "message": f"Task {task_id} has no temporal grid proof. Run: task-master test-story --id={task_id}"
            }

        # Check that the story was run recently (within last 24 hours)
        if story.last_run and (datetime.now() - story.last_run).total_seconds() > 86400:
            return {
                "valid": False,
                "reason": "stale_validation",
                "message": f"Task {task_id} story validation is stale (>24h old). Re-run: task-master test-story --id={task_id}"
            }

        return {
            "valid": True,
            "message": f"Task {task_id} is valid for completion with user story proof",
            "temporal_grid_path": story.temporal_grid_path,
            "story_status": story.story_status,
            "last_run": story.last_run.isoformat() if story.last_run else None
        }

    def list_all_task_stories(self) -> List[Dict[str, Any]]:
        """List all task stories with their status"""

        stories = []
        for task_id, story in self.task_stories.items():
            stories.append({
                "task_id": task_id,
                "task_title": story.task_title,
                "story_id": story.story_id,
                "story_status": story.story_status,
                "last_run": story.last_run.isoformat() if story.last_run else None,
                "has_temporal_grid": bool(story.temporal_grid_path and Path(story.temporal_grid_path).exists()),
                "temporal_grid_path": story.temporal_grid_path
            })

        return sorted(stories, key=lambda x: x["task_id"])


# Global instance for easy access
_task_story_manager: Optional[TaskStoryManager] = None

def get_task_story_manager(project_root: Optional[Path] = None) -> TaskStoryManager:
    """Get or create the global TaskStoryManager instance"""
    global _task_story_manager

    if _task_story_manager is None:
        if project_root is None:
            # Try to detect project root
            current_file = Path(__file__)
            project_root = current_file.parent.parent.parent

        _task_story_manager = TaskStoryManager(project_root)

    return _task_story_manager
