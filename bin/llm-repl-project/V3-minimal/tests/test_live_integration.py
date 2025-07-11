"""Test the integration of live blocks into the main application"""

import pytest
from unittest.mock import Mock
from datetime import datetime

from src.core.input_processor import InputProcessor
from src.core.response_generator import ResponseGenerator
from src.sacred_timeline import SacredTimeline
from src.ui.timeline_controller import TimelineViewController


class TestLiveBlockIntegration:
    """Test that live blocks are properly integrated into the application flow"""

    def test_input_processor_creates_live_blocks(self):
        """Test that InputProcessor creates live blocks for cognition"""
        # Create a fresh timeline for testing
        test_timeline = SacredTimeline()

        # Create response generator and input processor
        response_gen = ResponseGenerator()
        input_processor = InputProcessor(test_timeline, response_gen)

        # Mock the timeline controller to capture live block updates
        mock_controller = Mock(spec=TimelineViewController)
        mock_controller.on_live_block_update = Mock()

        # Add the mock controller as an observer
        test_timeline.add_observer(mock_controller)

        # Process user input
        input_processor.process_user_input("test query")

        # Verify blocks were added to timeline
        blocks = test_timeline.get_blocks()
        assert len(blocks) == 3  # user, cognition, assistant

        # Verify cognition block has sub-blocks
        cognition_block = blocks[1]
        assert cognition_block.role == "cognition"
        assert (
            len(cognition_block.sub_blocks) == 3
        )  # route_query, call_tool, format_output

        # Verify live block manager was used
        assert (
            len(input_processor.live_block_manager.live_blocks) == 0
        )  # Should be inscribed

    def test_timeline_controller_handles_live_updates(self):
        """Test that TimelineViewController properly handles live block updates"""
        from src.widgets.timeline import TimelineView
        from src.core.live_blocks import LiveBlock, LiveBlockData

        # Create mock timeline view
        mock_timeline_view = Mock(spec=TimelineView)
        mock_timeline_view.add_live_block_widget = Mock()

        # Create controller
        controller = TimelineViewController(mock_timeline_view)

        # Create a live block
        live_data = LiveBlockData(
            role="cognition", content="Processing...", timestamp=datetime.now()
        )
        live_block = LiveBlock("test-id", live_data)

        # Simulate live block update
        controller.on_live_block_update(live_block)

        # Verify widget was created and added
        assert "test-id" in controller.live_block_widgets
        mock_timeline_view.add_live_block_widget.assert_called_once()

        # Simulate progress update
        live_block.update_progress(0.5)
        controller.on_live_block_update(live_block)

        # Verify widget was updated
        widget = controller.live_block_widgets["test-id"]
        assert widget is not None

        # Simulate completion (inscribing)
        live_block.update_progress(1.0)
        controller.on_live_block_update(live_block)

        # Verify widget was removed when inscribed
        assert "test-id" not in controller.live_block_widgets

    @pytest.mark.asyncio
    async def test_live_block_animation_in_app(self):
        """Test that live blocks animate properly in the app context"""
        from textual.app import App
        from src.widgets.live_block_widget import LiveBlockWidget

        class TestApp(App):
            def compose(self):
                yield LiveBlockWidget(
                    role="cognition", initial_content="Starting...", block_id="test"
                )

        app = TestApp()

        async with app.run_test() as pilot:
            # Get the widget
            widget = app.query_one(LiveBlockWidget)

            # Update content
            widget.update_content("Processing step 1...")
            await pilot.pause()

            # Update progress
            widget.update_progress(0.5)
            await pilot.pause()

            # Add sub-block
            widget.add_sub_block("step1", "Step 1 complete")
            await pilot.pause()

            # Verify updates were applied
            assert widget._progress == 0.5
            assert len(widget._sub_blocks) == 1
            assert "Processing step 1..." in widget._content_display.renderable
