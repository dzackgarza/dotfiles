"""
Test Sacred Turn Inscription Flow

Sacred Principle: The staging area (Live Workspace) represents the ENTIRE turn's cognition.
Nothing should be inscribed to the Sacred Timeline until the turn is complete.

This test catches entire classes of visual flow errors:
- Premature turn separators
- Improper block rendering
- Spacing and layout issues
- Chronological violations
"""

import pytest
from textual.pilot import Pilot
from unittest.mock import AsyncMock, MagicMock, patch
from src.main import LLMReplApp
from src.cognition import CognitionEvent, CognitionResult
import asyncio


@pytest.mark.asyncio
async def test_sacred_turn_inscription_flow():
    """
    Test that turn inscription follows the sacred chronological flow:
    1. User sends message
    2. Staging area opens showing ALL cognition for the turn
    3. Only after cognition completes, the turn is inscribed to timeline
    4. Turn separator appears AFTER inscription, not before
    """
    app = LLMReplApp()
    
    # Track what gets mounted to timeline vs staging area
    timeline_mounts = []
    staging_mounts = []
    
    # Mock the response generator to control output
    mock_response = "Hello! How can I help you today?"
    app.response_generator.generate_response = MagicMock(return_value=mock_response)
    
    # Track cognition events
    cognition_events = []
    
    # Patch cognition manager to emit test events
    async def mock_process_query(query):
        # Emit staging events
        if hasattr(app.unified_async_processor, '_handle_cognition_event'):
            await app.unified_async_processor._handle_cognition_event(
                CognitionEvent(type="start", module="route_query", content="Routing query...")
            )
            cognition_events.append("route_query")
            
            await app.unified_async_processor._handle_cognition_event(
                CognitionEvent(type="update", module="search", content="Searching knowledge base...")
            )
            cognition_events.append("search")
            
            await app.unified_async_processor._handle_cognition_event(
                CognitionEvent(type="complete", module="generate", content="Generating response...")
            )
            cognition_events.append("generate")
        
        # Return cognition result
        return CognitionResult(
            content="Processed through cognition pipeline",
            metadata={"steps": 3, "duration": "1.2s"}
        )
    
    app.unified_async_processor.cognition_manager.process_query = mock_process_query
    
    async with app.run_test() as pilot:
        # Get containers
        timeline = app.query_one("#chat-container")
        staging_area = app.query_one("#staging-container")
        
        # Track mounts to timeline
        original_timeline_mount = timeline.mount
        async def track_timeline_mount(widget, *args, **kwargs):
            timeline_mounts.append({
                'widget': widget,
                'type': widget.__class__.__name__,
                'classes': list(widget.classes) if hasattr(widget, 'classes') else []
            })
            return await original_timeline_mount(widget, *args, **kwargs)
        timeline.mount = track_timeline_mount
        
        # Track mounts to staging area
        original_staging_mount = staging_area.mount
        async def track_staging_mount(widget, *args, **kwargs):
            staging_mounts.append({
                'widget': widget,
                'type': widget.__class__.__name__,
                'classes': list(widget.classes) if hasattr(widget, 'classes') else []
            })
            return await original_staging_mount(widget, *args, **kwargs)
        staging_area.mount = track_staging_mount
        
        # Initial state check
        assert "hidden" in staging_area.classes, "Staging area should be hidden initially"
        
        # Send first user message
        prompt_input = app.query_one("#prompt-input")
        prompt_input.value = "Hello, assistant"
        
        # Count initial timeline widgets (should have welcome message)
        initial_timeline_count = len(list(timeline.children))
        
        # Submit the message
        await pilot.press("enter")
        
        # Wait for processing to start - need longer for async worker
        await pilot.pause(1.0)
        
        # Debug: check staging area state
        print(f"Staging area classes: {staging_area.classes}")
        print(f"Staging area visible: {staging_area.is_visible if hasattr(staging_area, 'is_visible') else 'N/A'}")
        
        # SACRED CHECK 1: Staging area should be visible during cognition
        assert "hidden" not in staging_area.classes, "Staging area must be visible during cognition"
        
        # SACRED CHECK 2: No turn separator should appear in timeline yet
        turn_separators = [m for m in timeline_mounts if m['type'] == 'TurnSeparator']
        assert len(turn_separators) == 0, "Turn separator appeared before cognition completed!"
        
        # SACRED CHECK 3: Cognition events should be in staging area
        assert len(cognition_events) >= 2, "Cognition events should have been processed"
        
        # Wait for processing to complete
        await pilot.pause(0.5)
        
        # SACRED CHECK 4: After turn completion, staging area should hide
        assert "hidden" in staging_area.classes, "Staging area should hide after turn completion"
        
        # SACRED CHECK 5: Timeline should now have complete turn
        # Should have: turn separator (if not first turn), user message, cognition block, assistant response
        timeline_children = list(timeline.children)
        new_widgets_count = len(timeline_children) - initial_timeline_count
        
        # For turn 2+, we expect: separator + user + cognition + assistant = 4 widgets
        # For turn 1, we expect: user + cognition + assistant = 3 widgets
        expected_widgets = 4 if app.turn_count > 1 else 3
        assert new_widgets_count >= expected_widgets - 1, \
            f"Expected at least {expected_widgets-1} new widgets, got {new_widgets_count}"
        
        # Check for proper cognition block in timeline
        cognition_blocks = [m for m in timeline_mounts if 'CognitionWidget' in m['type'] or 'cognition' in str(m['classes'])]
        assert len(cognition_blocks) > 0, "Cognition block must be inscribed to timeline"


@pytest.mark.asyncio
async def test_cognition_block_proper_rendering():
    """
    Test that cognition blocks render properly in both staging area and timeline:
    - Proper header ("> Cognition")
    - Sub-items on separate lines
    - No raw text dumping
    """
    app = LLMReplApp()
    
    # Mock response generator
    app.response_generator.generate_response = MagicMock(return_value="Test response")
    
    async with app.run_test() as pilot:
        staging_area = app.query_one("#staging-container")
        timeline = app.query_one("#chat-container")
        
        # Send message to trigger cognition
        prompt_input = app.query_one("#prompt-input")
        prompt_input.value = "Test message"
        await pilot.press("enter")
        
        await pilot.pause(0.1)
        
        # Check staging area rendering during cognition
        staging_widgets = list(staging_area.children)
        
        # Look for cognition-related widgets in staging area
        for widget in staging_widgets:
            widget_str = str(widget)
            
            # Skip separator widgets
            if "separator" in widget.__class__.__name__.lower():
                continue
                
            # Check if it's a cognition widget
            if hasattr(widget, 'border_title') or hasattr(widget, 'content'):
                # VISUAL CHECK 1: Should have proper styling/header
                if hasattr(widget, 'border_title') and widget.border_title:
                    assert "Cognition" in widget.border_title or "Processing" in widget.border_title, \
                        "Cognition widgets should have appropriate headers"
        
        # Wait for completion
        await pilot.pause(0.5)
        
        # Check timeline rendering after completion
        timeline_widgets = list(timeline.children)
        
        # Find cognition widgets in timeline
        from src.widgets.cognition_widget import CognitionWidget
        cognition_widgets = [w for w in timeline_widgets if isinstance(w, CognitionWidget)]
        
        if cognition_widgets:
            for widget in cognition_widgets:
                # VISUAL CHECK 2: Should be a proper widget, not raw text
                assert hasattr(widget, 'render'), "Cognition must be a proper widget with render method"
                
                # VISUAL CHECK 3: Should have proper structure
                if hasattr(widget, 'border_title'):
                    assert widget.border_title, "Cognition widget should have a border title"


@pytest.mark.asyncio  
async def test_no_massive_gaps_or_scrolling_issues():
    """
    Test that there are no massive whitespace gaps or scrolling issues:
    - Staging area should not have excessive height
    - No huge gaps between blocks
    - Proper auto-scrolling behavior
    """
    app = LLMReplApp()
    
    # Mock response generator
    app.response_generator.generate_response = MagicMock(return_value="Test response")
    
    # Mock cognition to emit multiple events
    async def mock_multi_step_cognition(query):
        for i in range(5):
            if hasattr(app.unified_async_processor, '_handle_cognition_event'):
                await app.unified_async_processor._handle_cognition_event(
                    CognitionEvent(
                        type="update",
                        module=f"step_{i}",
                        content=f"Processing step {i}..."
                    )
                )
        return CognitionResult(content="Multi-step processing complete")
    
    app.unified_async_processor.cognition_manager.process_query = mock_multi_step_cognition
    
    async with app.run_test() as pilot:
        staging_area = app.query_one("#staging-container")
        timeline = app.query_one("#chat-container")
        
        # Send message
        prompt_input = app.query_one("#prompt-input")
        prompt_input.value = "Test gaps"
        await pilot.press("enter")
        
        await pilot.pause(0.1)
        
        # LAYOUT CHECK 1: Staging area should be visible and reasonable height
        assert "hidden" not in staging_area.classes
        
        # Check staging area isn't taking too much space
        if hasattr(staging_area, 'size'):
            staging_height = staging_area.size.height
            app_height = app.size.height
            
            # Staging area should be reasonably sized (not more than 50% of screen)
            if app_height > 0:  # Avoid division by zero
                height_ratio = staging_height / app_height
                assert height_ratio <= 0.6, \
                    f"Staging area height ratio {height_ratio:.2f} exceeds 60% of app height"
        
        # LAYOUT CHECK 2: Should not be scrolled to bottom initially
        if hasattr(staging_area, 'scroll_offset'):
            assert staging_area.scroll_offset.y == 0, \
                "Staging area should not be scrolled to bottom on open"
        
        # Wait for completion
        await pilot.pause(0.5)
        
        # LAYOUT CHECK 3: Check timeline for excessive gaps
        timeline_widgets = list(timeline.children)
        
        # Look for suspicious gaps between widgets
        from src.widgets.turn_separator import TurnSeparator
        from src.widgets.chatbox import Chatbox
        from src.widgets.cognition_widget import CognitionWidget
        
        valid_widget_types = (TurnSeparator, Chatbox, CognitionWidget)
        
        for i, widget in enumerate(timeline_widgets):
            # Skip initial widgets (like welcome message)
            if i < 2:
                continue
                
            # Check for unexpected widget types that might be spacers
            if not isinstance(widget, valid_widget_types):
                widget_type = widget.__class__.__name__
                # Rule widgets are okay (they're separators)
                if widget_type != "Rule" and not widget_type.endswith("Separator"):
                    # Check if it's an empty/spacer widget
                    if hasattr(widget, 'renderable') and not widget.renderable:
                        pytest.fail(f"Found empty spacer widget at position {i}")
            
            # Check for excessive margins on widgets
            if hasattr(widget, 'styles') and hasattr(widget.styles, 'margin'):
                margin = widget.styles.margin
                if margin:
                    # Check each margin value
                    for side in ['top', 'right', 'bottom', 'left']:
                        margin_value = getattr(margin, side, 0)
                        if margin_value > 5:  # More than 5 units is suspicious
                            pytest.fail(
                                f"Widget {i} ({widget.__class__.__name__}) has excessive "
                                f"{side} margin: {margin_value}"
                            )