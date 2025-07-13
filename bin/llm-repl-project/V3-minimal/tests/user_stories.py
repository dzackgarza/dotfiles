#!/usr/bin/env python3
"""
USER STORY FRAMEWORK

Defines atomic user stories for LLM REPL testing. Each story captures
a complete user interaction flow in exactly 12 screenshots, providing
visual proof of Sacred GUI state transitions.

PARADIGM: Test user stories, not random actions.
GOAL: Each story proves a specific user capability works end-to-end.
"""

from typing import List, Callable
from dataclasses import dataclass


@dataclass
class UserStoryStep:
    """Single step in a user story with screenshot moment"""
    name: str
    description: str
    action: Callable  # Function that performs the action
    screenshot_name: str


@dataclass
class UserStory:
    """Complete atomic user story with 12 steps"""
    story_id: str
    title: str
    description: str
    steps: List[UserStoryStep]

    def validate(self):
        """Ensure story has exactly 12 steps"""
        if len(self.steps) != 12:
            raise ValueError(f"Story {self.story_id} must have exactly 12 steps, got {len(self.steps)}")


# =============================================================================
# CORE USER STORIES
# =============================================================================

async def story_first_conversation_steps(pilot) -> List[UserStoryStep]:
    """First-time user asks a question and gets response"""

    async def step_01_launch():
        await pilot.pause(0.5)
        return "01_clean_launch"

    async def step_02_focus_input():
        await pilot.click("#prompt-input")
        await pilot.pause(0.2)
        return "02_input_focused"

    async def step_03_type_question():
        message = "What are Python decorators?"
        for char in message:
            await pilot.press(char)
            await pilot.pause(0.02)
        return "03_question_typed"

    async def step_04_submit():
        await pilot.press("enter")
        await pilot.pause(0.1)
        return "04_submitted"

    async def step_05_processing_start():
        await pilot.pause(0.5)
        return "05_processing_start"

    async def step_06_cognition_active():
        await pilot.pause(1.0)
        return "06_cognition_active"

    async def step_07_workspace_visible():
        await pilot.pause(1.0)
        return "07_workspace_visible"

    async def step_08_response_streaming():
        await pilot.pause(2.0)
        return "08_response_streaming"

    async def step_09_response_complete():
        await pilot.pause(1.0)
        return "09_response_complete"

    async def step_10_workspace_collapse():
        await pilot.pause(0.5)
        return "10_workspace_collapsed"

    async def step_11_timeline_updated():
        await pilot.pause(0.5)
        return "11_timeline_updated"

    async def step_12_ready_for_next():
        await pilot.click("#prompt-input")
        await pilot.pause(0.2)
        return "12_ready_next"

    return [
        UserStoryStep("launch", "App launches cleanly", step_01_launch, "01_clean_launch"),
        UserStoryStep("focus", "User clicks input area", step_02_focus_input, "02_input_focused"),
        UserStoryStep("type", "User types their question", step_03_type_question, "03_question_typed"),
        UserStoryStep("submit", "User presses Enter", step_04_submit, "04_submitted"),
        UserStoryStep("process_start", "Processing begins", step_05_processing_start, "05_processing_start"),
        UserStoryStep("cognition", "Cognition pipeline active", step_06_cognition_active, "06_cognition_active"),
        UserStoryStep("workspace", "Live Workspace appears", step_07_workspace_visible, "07_workspace_visible"),
        UserStoryStep("streaming", "Response streams in", step_08_response_streaming, "08_response_streaming"),
        UserStoryStep("complete", "Response generation complete", step_09_response_complete, "09_response_complete"),
        UserStoryStep("collapse", "Workspace collapses", step_10_workspace_collapse, "10_workspace_collapsed"),
        UserStoryStep("timeline", "Timeline shows conversation", step_11_timeline_updated, "11_timeline_updated"),
        UserStoryStep("ready", "Ready for next interaction", step_12_ready_for_next, "12_ready_next")
    ]


async def story_multi_turn_conversation_steps(pilot) -> List[UserStoryStep]:
    """User has a back-and-forth conversation"""

    async def step_01_existing_state():
        # Assume we already have one conversation
        await pilot.pause(0.2)
        return "01_existing_conversation"

    async def step_02_followup_question():
        await pilot.click("#prompt-input")
        followup = "Can you show me an example?"
        for char in followup:
            await pilot.press(char)
            await pilot.pause(0.02)
        return "02_followup_typed"

    async def step_03_submit_followup():
        await pilot.press("enter")
        await pilot.pause(0.1)
        return "03_followup_submitted"

    async def step_04_second_processing():
        await pilot.pause(0.5)
        return "04_second_processing"

    async def step_05_context_aware():
        await pilot.pause(1.0)
        return "05_context_processing"

    async def step_06_second_response():
        await pilot.pause(2.0)
        return "06_second_response"

    async def step_07_conversation_grows():
        await pilot.pause(1.0)
        return "07_conversation_grows"

    async def step_08_third_question():
        await pilot.click("#prompt-input")
        await pilot.pause(0.1)
        third = "What about async decorators?"
        for char in third:
            await pilot.press(char)
            await pilot.pause(0.02)
        return "08_third_typed"

    async def step_09_third_submit():
        await pilot.press("enter")
        await pilot.pause(0.5)
        return "09_third_submitted"

    async def step_10_deep_context():
        await pilot.pause(1.5)
        return "10_deep_context"

    async def step_11_rich_conversation():
        await pilot.pause(2.0)
        return "11_rich_conversation"

    async def step_12_full_timeline():
        await pilot.pause(1.0)
        return "12_full_timeline"

    return [
        UserStoryStep("existing", "Previous conversation exists", step_01_existing_state, "01_existing_conversation"),
        UserStoryStep("followup", "User types follow-up question", step_02_followup_question, "02_followup_typed"),
        UserStoryStep("submit2", "Submit second question", step_03_submit_followup, "03_followup_submitted"),
        UserStoryStep("process2", "Second processing cycle", step_04_second_processing, "04_second_processing"),
        UserStoryStep("context", "Context-aware processing", step_05_context_aware, "05_context_processing"),
        UserStoryStep("response2", "Second response generates", step_06_second_response, "06_second_response"),
        UserStoryStep("grows", "Conversation grows", step_07_conversation_grows, "07_conversation_grows"),
        UserStoryStep("third", "User types third question", step_08_third_question, "08_third_typed"),
        UserStoryStep("submit3", "Submit third question", step_09_third_submit, "09_third_submitted"),
        UserStoryStep("deep", "Deep context processing", step_10_deep_context, "10_deep_context"),
        UserStoryStep("rich", "Rich multi-turn response", step_11_rich_conversation, "11_rich_conversation"),
        UserStoryStep("timeline", "Complete conversation timeline", step_12_full_timeline, "12_full_timeline")
    ]


async def story_error_recovery_steps(pilot) -> List[UserStoryStep]:
    """User encounters error and recovers gracefully"""

    async def step_01_normal_state():
        await pilot.pause(0.2)
        return "01_normal_state"

    async def step_02_problematic_input():
        await pilot.click("#prompt-input")
        # Intentionally problematic input
        bad_input = "Generate 10000 words about nothing" * 10
        for char in bad_input[:100]:  # Truncate for demo
            await pilot.press(char)
            await pilot.pause(0.01)
        return "02_problematic_input"

    async def step_03_submit_bad():
        await pilot.press("enter")
        await pilot.pause(0.1)
        return "03_bad_submitted"

    async def step_04_error_processing():
        await pilot.pause(1.0)
        return "04_error_processing"

    async def step_05_error_displayed():
        await pilot.pause(1.0)
        return "05_error_shown"

    async def step_06_user_sees_error():
        await pilot.pause(0.5)
        return "06_error_visible"

    async def step_07_user_recovery():
        await pilot.click("#prompt-input")
        await pilot.press("ctrl+a")
        await pilot.press("delete")
        return "07_input_cleared"

    async def step_08_good_question():
        good_input = "What is 2+2?"
        for char in good_input:
            await pilot.press(char)
            await pilot.pause(0.02)
        return "08_good_typed"

    async def step_09_recovery_submit():
        await pilot.press("enter")
        await pilot.pause(0.1)
        return "09_recovery_submitted"

    async def step_10_normal_processing():
        await pilot.pause(1.0)
        return "10_normal_processing"

    async def step_11_successful_response():
        await pilot.pause(2.0)
        return "11_successful_response"

    async def step_12_recovered_state():
        await pilot.pause(0.5)
        return "12_recovered"

    return [
        UserStoryStep("normal", "App in normal state", step_01_normal_state, "01_normal_state"),
        UserStoryStep("bad_input", "User types problematic input", step_02_problematic_input, "02_problematic_input"),
        UserStoryStep("bad_submit", "Submit bad input", step_03_submit_bad, "03_bad_submitted"),
        UserStoryStep("error_proc", "Error processing occurs", step_04_error_processing, "04_error_processing"),
        UserStoryStep("error_shown", "Error message displayed", step_05_error_displayed, "05_error_shown"),
        UserStoryStep("user_sees", "User sees error feedback", step_06_user_sees_error, "06_error_visible"),
        UserStoryStep("recovery", "User clears input to recover", step_07_user_recovery, "07_input_cleared"),
        UserStoryStep("good_input", "User types good question", step_08_good_question, "08_good_typed"),
        UserStoryStep("recover_submit", "Submit recovery question", step_09_recovery_submit, "09_recovery_submitted"),
        UserStoryStep("normal_proc", "Normal processing resumes", step_10_normal_processing, "10_normal_processing"),
        UserStoryStep("success", "Successful response received", step_11_successful_response, "11_successful_response"),
        UserStoryStep("recovered", "App fully recovered", step_12_recovered_state, "12_recovered")
    ]


# =============================================================================
# STORY REGISTRY
# =============================================================================

AVAILABLE_STORIES = {
    "first_conversation": UserStory(
        story_id="first_conversation",
        title="First-Time User Conversation",
        description="New user asks their first question and receives response",
        steps=[]  # Populated dynamically
    ),
    "multi_turn": UserStory(
        story_id="multi_turn",
        title="Multi-Turn Conversation",
        description="User has back-and-forth conversation with context",
        steps=[]  # Populated dynamically
    ),
    "error_recovery": UserStory(
        story_id="error_recovery",
        title="Error Handling and Recovery",
        description="User encounters error and recovers gracefully",
        steps=[]  # Populated dynamically
    )
}


async def get_user_story(story_id: str, pilot) -> UserStory:
    """Get a fully populated user story with pilot-specific steps"""
    if story_id not in AVAILABLE_STORIES:
        raise ValueError(f"Unknown story: {story_id}")

    story = AVAILABLE_STORIES[story_id]

    # Populate steps based on story type
    if story_id == "first_conversation":
        story.steps = await story_first_conversation_steps(pilot)
    elif story_id == "multi_turn":
        story.steps = await story_multi_turn_conversation_steps(pilot)
    elif story_id == "error_recovery":
        story.steps = await story_error_recovery_steps(pilot)

    story.validate()
    return story


def list_available_stories() -> List[str]:
    """List all available user story IDs"""
    return list(AVAILABLE_STORIES.keys())
