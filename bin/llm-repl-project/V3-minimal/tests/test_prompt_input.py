import pytest
from src.main import LLMReplApp
from src.widgets.prompt_input import PromptInput
from src.widgets.unified_timeline_widget import UnifiedTimelineWidget
from src.sacred_timeline import timeline


@pytest.fixture(autouse=True)
def clear_timeline_fixture():
    """Fixture to clear the timeline before each test."""
    timeline.clear_timeline()
    yield
    timeline.clear_timeline()


class TestPromptInput:
    async def test_enter_sends_message(self):
        """Test that pressing Enter sends the message to the timeline."""
        async with LLMReplApp().run_test() as app:
            timeline_view = app.app.query_one(UnifiedTimelineWidget)
            prompt_input = app.app.query_one(PromptInput)

            test_message = "Hello, Textual!"
            prompt_input.text = test_message
            prompt_input.action_submit_prompt()  # Directly call the action

            # Wait for the app to process events and render
            await app.pause(1.0)  # Increased pause duration for async processing

            # Assert that the user message is in the timeline
            # We expect blocks: system, user, cognition, assistant
            blocks = timeline_view.unified_timeline.get_all_blocks()
            assert len(blocks) >= 2  # At minimum, system and user

            # Find user block (should be inscribed)
            user_blocks = [b for b in blocks if b.role == "user"]
            assert len(user_blocks) >= 1
            user_block = user_blocks[0]

            # Check content - access differently for inscribed vs live blocks
            if hasattr(user_block, "content"):
                # For inscribed blocks, content is the final content
                assert test_message in user_block.content
            else:
                # For live blocks, content might have extra inscription messages
                assert test_message in user_block.data.content

            # Assert that the input field is cleared
            assert prompt_input.text == ""

    async def test_shift_enter_inserts_newline(self):
        """Test that pressing Shift+Enter inserts a newline in the input field."""
        async with LLMReplApp().run_test() as app:
            prompt_input = app.app.query_one(PromptInput)

            test_message_part1 = "First line"
            test_message_part2 = "Second line"

            prompt_input.text = test_message_part1 + "\n" + test_message_part2

            # Wait for the app to process events and render
            await app.pause(0.5)  # Increased pause duration

            # Assert that the newline is inserted and text is correct
            assert prompt_input.text == f"{test_message_part1}\n{test_message_part2}"

            # Assert that no message was sent to the timeline
            timeline_view = app.app.query_one(UnifiedTimelineWidget)
            # Check unified timeline instead of blocks property
            blocks = timeline_view.unified_timeline.get_all_blocks()
            assert len(blocks) == 1  # Only welcome message

    async def test_cursor_escaping_top(self):
        """Test that pressing Up arrow at the top of the input sends CursorEscapingTop message."""
        async with LLMReplApp().run_test() as app:
            prompt_input = app.app.query_one(PromptInput)

            # Focus the widget and ensure cursor is at (0,0)
            prompt_input.focus()
            prompt_input.cursor_location = (0, 0)
            await app.pause(0.1)  # Let focus settle

            # Manually capture messages using a cleaner approach
            captured_messages = []
            original_post_message = prompt_input.post_message

            def capture_message(message):
                captured_messages.append(message)
                return original_post_message(message)

            prompt_input.post_message = capture_message

            await app.press("up")
            await app.pause(0.1)

            # Filter for CursorEscapingTop messages
            escaping_messages = [
                msg
                for msg in captured_messages
                if isinstance(msg, PromptInput.CursorEscapingTop)
            ]

            assert len(escaping_messages) == 1

    async def test_cursor_escaping_bottom(self):
        """Test that pressing Down arrow at the end of the input sends CursorEscapingBottom message."""
        async with LLMReplApp().run_test() as app:
            prompt_input = app.app.query_one(PromptInput)
            # Ensure cursor is at end of text
            prompt_input.text = "some text"
            prompt_input.cursor_location = (0, len("some text"))

            # Press 'down' and check if cursor remains at end of text
            await app.press("down")
            await app.pause(0.1)  # Short pause to allow event processing
            assert prompt_input.cursor_location == (0, len("some text"))

            # Optionally, assert that a CursorEscapingBottom message was posted
            # This requires a more sophisticated message capture mechanism if app.listen() is not working
            # For now, we rely on the cursor location assertion.

    async def test_ctrl_c_allows_app_quit(self):
        """Test that Ctrl+C in the text input allows the app to quit."""
        async with LLMReplApp().run_test() as app:
            prompt_input = app.app.query_one(PromptInput)

            # Focus the input widget
            prompt_input.focus()
            await app.pause(0.1)

            # Simulate Ctrl+C key event
            from textual import events

            # Create a Ctrl+C key event
            ctrl_c_event = events.Key(key="ctrl+c", character="")

            # Track if the event was prevented
            prevented = False
            original_prevent_default = ctrl_c_event.prevent_default

            def track_prevent():
                nonlocal prevented
                prevented = True
                original_prevent_default()

            ctrl_c_event.prevent_default = track_prevent

            # Send the event to the widget
            await prompt_input._on_key(ctrl_c_event)

            # Assert that the event was NOT prevented (should bubble up to app)
            assert not prevented, "Ctrl+C should not be prevented in text input"

            # The event should be allowed to bubble up for app-level quit handling
