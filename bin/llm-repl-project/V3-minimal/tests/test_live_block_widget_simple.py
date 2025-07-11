"""Simplified tests for live block widget components."""

from src.widgets.live_block_widget import LiveBlockWidget
from src.core.live_blocks import LiveBlock, BlockState


class TestLiveBlockWidgetBasics:
    """Test basic LiveBlockWidget functionality without UI context."""

    def test_widget_creation(self):
        """Test widget can be created with a live block."""
        block = LiveBlock("user", "Test content")
        widget = LiveBlockWidget(block)

        assert widget.live_block == block
        assert widget.live_block.data.content == "Test content"

    def test_role_indicator_mapping(self):
        """Test role indicator mappings work correctly."""
        test_cases = [
            ("user", "👤"),
            ("assistant", "🤖"),
            ("cognition", "🧠"),
            ("tool", "🛠️"),
            ("system", "⚙️"),
            ("sub_module", "└─"),
            ("error", "❌"),
            ("unknown", "•"),
        ]

        for role, expected_indicator in test_cases:
            block = LiveBlock(role)
            widget = LiveBlockWidget(block)
            assert widget._get_role_indicator() == expected_indicator

    def test_state_indicator_mapping(self):
        """Test state indicator mappings work correctly."""
        block = LiveBlock("user")
        widget = LiveBlockWidget(block)

        # Test each state
        block.state = BlockState.LIVE
        assert widget._get_state_indicator() == "●"

        block.state = BlockState.TRANSITIONING
        assert widget._get_state_indicator() == "⧗"

        block.state = BlockState.INSCRIBED
        assert widget._get_state_indicator() == "◉"

    def test_callback_registration(self):
        """Test widget registers update callbacks."""
        block = LiveBlock("user")
        initial_callbacks = len(block.update_callbacks)

        widget = LiveBlockWidget(block)

        # Widget should have registered a callback
        assert len(block.update_callbacks) == initial_callbacks + 1

    def test_sub_block_tracking(self):
        """Test sub-block widget tracking."""
        parent_block = LiveBlock("cognition")
        widget = LiveBlockWidget(parent_block)

        # Initially no sub-blocks
        assert len(widget.sub_block_widgets) == 0

        # Add sub-block to parent
        sub_block = LiveBlock("sub_module", "Step 1")
        parent_block.add_sub_block(sub_block)

        # Call update method manually
        widget._update_sub_blocks()

        # Should track sub-block widget
        assert len(widget.sub_block_widgets) == 1
        assert widget.sub_block_widgets[0].live_block == sub_block


class TestWidgetMethodsWithoutUI:
    """Test widget methods that don't require UI context."""

    def test_css_class_updates(self):
        """Test CSS class update methods don't error."""
        block = LiveBlock("user")
        widget = LiveBlockWidget(block)

        # These should not raise exceptions
        try:
            widget._update_css_classes()
            assert True  # Method completed without error
        except Exception as e:
            # Allow NoActiveAppError or similar, but not other errors
            assert "NoActiveAppError" in str(type(e)) or "app" in str(e).lower()

    def test_display_update_methods(self):
        """Test display update methods work or handle errors gracefully."""
        block = LiveBlock("user", "Test content")
        block.update_progress(0.5)
        block.update_tokens(input_tokens=10, output_tokens=20)

        widget = LiveBlockWidget(block)

        # These methods should handle missing app context gracefully
        try:
            widget._update_all_displays()
        except Exception as e:
            # Should be app context related, not logic errors
            error_str = str(e) + str(type(e))
            assert "app" in error_str.lower() or "context" in error_str.lower()


class TestBlockTransitionWidget:
    """Test BlockTransitionWidget without UI context."""

    def test_transition_widget_creation(self):
        """Test transition widget can be created."""
        from src.widgets.live_block_widget import BlockTransitionWidget

        widget = BlockTransitionWidget()
        assert not widget.is_transitioning

    def test_transition_state_management(self):
        """Test transition state management."""
        from src.widgets.live_block_widget import BlockTransitionWidget

        widget = BlockTransitionWidget()

        # Show transition
        widget.show_transition(BlockState.LIVE, BlockState.INSCRIBED)
        assert widget.is_transitioning

        # Hide transition
        widget.hide_transition()
        assert not widget.is_transitioning


class TestDemoWidget:
    """Test demo widget creation."""

    def test_demo_widget_creation(self):
        """Test demo widget can be created."""
        from src.widgets.live_block_widget import LiveBlockDemoWidget

        widget = LiveBlockDemoWidget()
        assert widget.demo_manager is not None
        assert hasattr(widget, "manager_widget")
        assert hasattr(widget, "transition_widget")
