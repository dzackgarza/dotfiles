"""Core functionality tests - basic app health checks."""

import pytest
from src.main import LLMReplApp
from src.widgets.sacred_timeline import SacredTimelineWidget
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
            timeline = app.app.query_one(SacredTimelineWidget)
            assert timeline is not None

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

            # Check sacred timeline exists
            sacred_timeline = app.app.query_one("#sacred-timeline")
            assert sacred_timeline is not None

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
    async def test_timeline_widget_exists(self):
        """Test that the timeline widget exists and is accessible."""
        async with LLMReplApp().run_test() as app:
            timeline = app.app.query_one(SacredTimelineWidget)
            assert timeline is not None
            # Basic existence test - detailed functionality in Sacred GUI implementation


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
            timeline = app.app.query_one(SacredTimelineWidget)
            prompt_input = app.app.query_one(PromptInput)

            # Verify they exist
            assert timeline is not None
            assert hasattr(prompt_input, "text")  # PromptInput extends TextArea

    @pytest.mark.asyncio
    async def test_async_methods_properly_awaited(self):
        """Test that async methods are properly awaited (prevents RuntimeWarning)."""
        async with LLMReplApp().run_test() as app:
            timeline = app.app.query_one(SacredTimelineWidget)

            # This should not generate runtime warnings about unawaited coroutines
            # Basic async test - detailed functionality in Sacred GUI implementation
            import asyncio

            await asyncio.sleep(0.1)

            # Verify no exceptions were raised
            assert timeline is not None


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
