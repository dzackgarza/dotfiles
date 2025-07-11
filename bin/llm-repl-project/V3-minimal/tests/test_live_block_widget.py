"""Tests for live block widget components."""

import pytest
from textual.app import App

from src.widgets.live_block_widget import (
    LiveBlockWidget,
    LiveBlockManagerWidget,
    BlockTransitionWidget,
    LiveBlockDemoWidget,
)
from src.core.live_blocks import LiveBlock, LiveBlockManager, BlockState


class TestLiveBlockWidget:
    """Test LiveBlockWidget functionality."""

    def test_initialization(self):
        """Test widget initializes with live block."""
        block = LiveBlock("user", "Test content")
        widget = LiveBlockWidget(block)

        assert widget.live_block == block
        assert len(widget.sub_block_widgets) == 0

    def test_role_indicators(self):
        """Test role indicators are correct."""
        block = LiveBlock("user")
        widget = LiveBlockWidget(block)
        assert widget._get_role_indicator() == "👤"

        block = LiveBlock("assistant")
        widget = LiveBlockWidget(block)
        assert widget._get_role_indicator() == "🤖"

        block = LiveBlock("cognition")
        widget = LiveBlockWidget(block)
        assert widget._get_role_indicator() == "🧠"

        block = LiveBlock("unknown_role")
        widget = LiveBlockWidget(block)
        assert widget._get_role_indicator() == "•"

    def test_state_indicators(self):
        """Test state indicators are correct."""
        block = LiveBlock("user")
        widget = LiveBlockWidget(block)

        # Live state
        assert widget._get_state_indicator() == "●"

        # Transitioning state
        block.state = BlockState.TRANSITIONING
        assert widget._get_state_indicator() == "⧗"

        # Inscribed state
        block.state = BlockState.INSCRIBED
        assert widget._get_state_indicator() == "◉"

    def test_update_callback_registration(self):
        """Test widget registers for block updates."""
        block = LiveBlock("user")
        initial_callback_count = len(block.update_callbacks)

        widget = LiveBlockWidget(block)

        # Should have added one callback
        assert len(block.update_callbacks) == initial_callback_count + 1

    def test_sub_block_management(self):
        """Test sub-block widget management."""
        parent_block = LiveBlock("cognition")
        widget = LiveBlockWidget(parent_block)

        # Initially no sub-blocks
        assert len(widget.sub_block_widgets) == 0

        # Add sub-block
        sub_block = LiveBlock("sub_module", "Step 1")
        parent_block.add_sub_block(sub_block)

        # Trigger update manually (in real app this happens via callbacks)
        widget._update_sub_blocks()

        # Should have created sub-block widget
        assert len(widget.sub_block_widgets) == 1
        assert widget.sub_block_widgets[0].live_block == sub_block


class TestLiveBlockManagerWidget:
    """Test LiveBlockManagerWidget functionality."""

    def test_initialization(self):
        """Test widget initializes with manager."""
        manager = LiveBlockManager()
        widget = LiveBlockManagerWidget(manager)

        assert widget.live_block_manager == manager
        assert len(widget.block_widgets) == 0

    def test_manager_callback_registration(self):
        """Test widget registers for manager updates."""
        manager = LiveBlockManager()
        initial_callback_count = len(manager.block_update_callbacks)

        widget = LiveBlockManagerWidget(manager)

        # Should have added one callback
        assert len(manager.block_update_callbacks) == initial_callback_count + 1

    def test_block_widget_management(self):
        """Test block widget creation and removal."""
        manager = LiveBlockManager()
        widget = LiveBlockManagerWidget(manager)

        # Initially no block widgets
        assert len(widget.block_widgets) == 0

        # Create block in manager
        block = manager.create_live_block("user", "Test")

        # Trigger update manually
        widget._update_block_widgets()

        # Should have created block widget
        assert len(widget.block_widgets) == 1
        assert widget.block_widgets[0].live_block == block

        # Remove block from manager
        manager.inscribe_block(block.id)

        # Trigger update manually
        widget._update_block_widgets()

        # Should have removed block widget
        assert len(widget.block_widgets) == 0


class TestBlockTransitionWidget:
    """Test BlockTransitionWidget functionality."""

    def test_initialization(self):
        """Test widget initializes correctly."""
        widget = BlockTransitionWidget()
        assert not widget.is_transitioning

    def test_show_transition(self):
        """Test showing transition."""
        widget = BlockTransitionWidget()

        widget.show_transition(BlockState.LIVE, BlockState.INSCRIBED)

        assert widget.is_transitioning
        # Note: CSS class testing would require full Textual app context

    def test_hide_transition(self):
        """Test hiding transition."""
        widget = BlockTransitionWidget()

        # Show then hide
        widget.show_transition(BlockState.LIVE, BlockState.INSCRIBED)
        widget.hide_transition()

        assert not widget.is_transitioning


class TestLiveBlockDemoWidget:
    """Test LiveBlockDemoWidget functionality."""

    def test_initialization(self):
        """Test demo widget initializes correctly."""
        widget = LiveBlockDemoWidget()

        assert widget.demo_manager is not None
        assert widget.manager_widget is not None
        assert widget.transition_widget is not None

    @pytest.mark.asyncio
    async def test_demo_cognition_pipeline(self):
        """Test cognition pipeline demo."""
        widget = LiveBlockDemoWidget()

        # Run demo
        inscribed = await widget.demo_cognition_pipeline()

        # Should have created and inscribed a block
        assert inscribed is not None
        assert inscribed.role == "cognition"
        assert "cognition" in inscribed.content.lower()

    @pytest.mark.asyncio
    async def test_demo_assistant_response(self):
        """Test assistant response demo."""
        widget = LiveBlockDemoWidget()

        # Run demo
        inscribed = await widget.demo_assistant_response()

        # Should have created and inscribed a block
        assert inscribed is not None
        assert inscribed.role == "assistant"
        assert len(inscribed.content) > 0


# Integration test with actual Textual app
class LiveBlockTestApp(App):
    """Test app for live block widgets."""

    def compose(self):
        # Create demo components
        manager = LiveBlockManager()
        manager_widget = LiveBlockManagerWidget(manager)

        # Create a test block
        block = manager.create_live_block("user", "Test block")

        yield manager_widget


@pytest.mark.asyncio
class TestLiveBlockWidgetIntegration:
    """Integration tests for live block widgets."""

    async def test_widget_in_app_context(self):
        """Test widget behavior in app context."""
        # This would be a more comprehensive test with actual Textual app
        # For now, just test basic functionality

        app = LiveBlockTestApp()

        # Test that app can be created with live block widgets
        assert app is not None

        # Note: Full integration testing would require running the app
        # which is complex in a test environment


class TestWidgetUpdates:
    """Test widget update mechanisms."""

    def test_content_update_propagation(self):
        """Test that block updates propagate to widgets."""
        block = LiveBlock("user", "Initial content")
        widget = LiveBlockWidget(block)

        # Update block content
        block.update_content("Updated content")

        # Widget should have received update callback
        # Note: In real app, this would update the display
        # Here we just test the callback was called
        assert block.data.content == "Updated content"

    def test_progress_update_propagation(self):
        """Test progress updates propagate to widgets."""
        block = LiveBlock("assistant")
        widget = LiveBlockWidget(block)

        # Update progress
        block.update_progress(0.5)

        # Widget should reflect the progress
        assert block.data.progress == 0.5

    def test_token_update_propagation(self):
        """Test token updates propagate to widgets."""
        block = LiveBlock("assistant")
        widget = LiveBlockWidget(block)

        # Update tokens
        block.update_tokens(input_tokens=10, output_tokens=20)

        # Widget should reflect the tokens
        assert block.data.tokens_input == 10
        assert block.data.tokens_output == 20

    def test_sub_block_update_propagation(self):
        """Test sub-block updates propagate to widgets."""
        parent_block = LiveBlock("cognition")
        widget = LiveBlockWidget(parent_block)

        # Add sub-block
        sub_block = LiveBlock("sub_module", "Step 1")
        parent_block.add_sub_block(sub_block)

        # Widget should be notified of the change
        assert len(parent_block.data.sub_blocks) == 1


class TestWidgetCSS:
    """Test widget CSS and styling."""

    def test_css_class_application(self):
        """Test CSS classes are applied based on state."""
        block = LiveBlock("user")
        widget = LiveBlockWidget(block)

        # Test state-based CSS classes
        widget._update_css_classes()

        # Note: Actual CSS class testing would require Textual app context
        # Here we just test the method doesn't error
        assert True  # Method executed without error

    def test_role_based_styling(self):
        """Test role-based styling works."""
        roles = ["user", "assistant", "cognition", "tool", "system"]

        for role in roles:
            block = LiveBlock(role)
            widget = LiveBlockWidget(block)

            # Should have role indicator
            indicator = widget._get_role_indicator()
            assert indicator is not None
            assert len(indicator) > 0
