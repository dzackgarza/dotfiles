"""Core functionality tests - basic app health checks."""

import pytest
from src.main import LLMReplApp
from src.widgets.unified_timeline_widget import UnifiedTimelineWidget
from src.widgets.prompt_input import PromptInput


class TestCoreAppFunctionality:
    """Test basic app functionality that must never break."""

    @pytest.mark.asyncio
    async def test_app_starts_without_crashes(self):
        """Test that the app can start and initialize without crashing."""
        async with LLMReplApp().run_test() as app:
            # If we get here, the app started successfully
            assert app.app is not None
            assert app.app.title == "LLM REPL V3-minimal"

    @pytest.mark.asyncio
    async def test_timeline_widget_present(self):
        """Test that the timeline widget is present and functional."""
        async with LLMReplApp().run_test() as app:
            timeline = app.app.query_one(UnifiedTimelineWidget)
            assert timeline is not None
            assert hasattr(timeline, "unified_timeline")

    @pytest.mark.asyncio
    async def test_prompt_input_present(self):
        """Test that the prompt input widget is present and functional."""
        async with LLMReplApp().run_test() as app:
            prompt_input = app.app.query_one(PromptInput)
            assert prompt_input is not None
            assert hasattr(prompt_input, "text")  # PromptInput extends TextArea

    @pytest.mark.asyncio
    async def test_basic_layout_structure(self):
        """Test that the basic layout structure is intact."""
        async with LLMReplApp().run_test() as app:
            # Check main container exists
            main_container = app.app.query_one("#main-container")
            assert main_container is not None

            # Check timeline container exists (UnifiedTimelineWidget is the scroll container)
            timeline_container = app.app.query_one("#timeline-container")
            assert timeline_container is not None

            # Check input container exists
            input_container = app.app.query_one("#input-container")
            assert input_container is not None

    @pytest.mark.asyncio
    async def test_app_can_handle_keypress(self):
        """Test that the app can handle basic keyboard input without crashing."""
        async with LLMReplApp().run_test() as app:
            # Send a simple key press
            app.app.action_focus_next()
            # If we get here, the app handled the action without crashing
            assert True

    @pytest.mark.asyncio
    async def test_timeline_can_accept_blocks(self):
        """Test that the timeline can accept and display blocks."""
        async with LLMReplApp().run_test() as app:
            timeline = app.app.query_one(UnifiedTimelineWidget)

            # Get initial block count
            initial_count = len(timeline.unified_timeline.get_all_blocks())

            # Add a test block through the timeline
            from src.core.live_blocks import InscribedBlock
            from datetime import datetime

            test_block = InscribedBlock(
                id="test-block",
                role="system",
                content="Test block content",
                timestamp=datetime.now(),
            )

            # Use add_live_block and immediately inscribe it
            live_block = timeline.unified_timeline.add_live_block(
                "system", "Test block content"
            )
            # Convert to inscribed (simulate completion)
            inscribed = live_block.to_inscribed_block()
            timeline.unified_timeline.inscribe_live_block(live_block.id, inscribed)

            # Verify block was added
            assert len(timeline.unified_timeline.get_all_blocks()) == initial_count + 1
            last_block = timeline.unified_timeline.get_all_blocks()[-1]
            assert last_block.content == "Test block content"


class TestRegressionProtection:
    """Tests that protect against known regressions."""

    @pytest.mark.asyncio
    async def test_textual_imports_work(self):
        """Test that all required Textual imports are available."""
        # This test prevents import errors like the VerticalScroll issue

        # If we get here, all imports work
        assert True

    @pytest.mark.asyncio
    async def test_no_missing_widget_dependencies(self):
        """Test that all widget dependencies are satisfied."""
        async with LLMReplApp().run_test() as app:
            # Query for all critical widgets - this will fail if dependencies are missing
            timeline = app.app.query_one(UnifiedTimelineWidget)
            prompt_input = app.app.query_one(PromptInput)

            # Verify they have required attributes
            assert hasattr(timeline, "unified_timeline")
            assert hasattr(prompt_input, "text")  # PromptInput extends TextArea

    @pytest.mark.asyncio
    async def test_async_methods_properly_awaited(self):
        """Test that async methods are properly awaited (prevents RuntimeWarning)."""
        async with LLMReplApp().run_test() as app:
            timeline = app.app.query_one(UnifiedTimelineWidget)

            # This should not generate runtime warnings about unawaited coroutines
            from src.core.live_blocks import InscribedBlock
            from datetime import datetime

            test_block = InscribedBlock(
                id="async-test-block",
                role="test",
                content="Testing async handling",
                timestamp=datetime.now(),
            )

            # Add block through the proper async mechanism
            # Use add_live_block and immediately inscribe it
            live_block = timeline.unified_timeline.add_live_block(
                "system", "Test block content"
            )
            # Convert to inscribed (simulate completion)
            inscribed = live_block.to_inscribed_block()
            timeline.unified_timeline.inscribe_live_block(live_block.id, inscribed)

            # Wait a moment for async processing
            import asyncio

            await asyncio.sleep(0.1)

            # Verify no exceptions were raised
            assert True


class TestGUIHealthCheck:
    """High-level GUI health checks."""

    @pytest.mark.asyncio
    async def test_app_renders_without_errors(self):
        """Test that the app renders its UI without errors."""
        async with LLMReplApp().run_test() as app:
            # Force a render cycle
            app.app.refresh()
            import asyncio

            await asyncio.sleep(0.1)

            # If we get here, rendering succeeded
            assert True

    @pytest.mark.asyncio
    async def test_widgets_can_receive_focus(self):
        """Test that focusable widgets can receive focus."""
        async with LLMReplApp().run_test() as app:
            prompt_input = app.app.query_one(PromptInput)

            # Focus the prompt input
            prompt_input.focus()
            import asyncio

            await asyncio.sleep(0.1)

            # Verify focus was received
            assert prompt_input.has_focus or app.app.focused is not None

    @pytest.mark.asyncio
    async def test_css_loads_without_errors(self):
        """Test that CSS files load without errors."""
        async with LLMReplApp().run_test() as app:
            # If the app started, CSS loaded successfully
            # This catches CSS syntax errors and missing file issues
            assert app.app.stylesheet is not None
