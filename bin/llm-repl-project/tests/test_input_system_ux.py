"""Test the new input system UX improvements."""

import pytest
import asyncio
import sys
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from plugins.blocks.user_input import UserInputPlugin
from plugins.base import RenderContext, PluginState
from ui.input_system import SimpleMultilineInput


class TestInputSystemUX:
    """Test the improved input system UX."""
    
    @pytest.mark.asyncio
    async def test_user_input_plugin_inscribed_only(self):
        """Test that UserInputPlugin only handles inscribed state properly."""
        plugin = UserInputPlugin()
        await plugin.initialize({"max_length": 1000, "allow_empty": False})
        await plugin.activate()
        
        # Process a simple input
        simple_input = "Hello world"
        result = await plugin.process(simple_input, {})
        
        # Verify the plugin completed successfully
        assert plugin.state == PluginState.COMPLETED
        assert result["input"] == simple_input
        
        # Render the plugin
        context = RenderContext(display_mode="inscribed")
        render_data = await plugin.render(context)
        
        # Verify render data
        assert render_data["render_type"] == "user_input"
        assert render_data["content"] == simple_input
        assert render_data["style"]["border_color"] == "green"
        
        # Verify metadata includes useful information
        metadata = render_data["metadata"]
        assert metadata["character_count"] == len(simple_input)
        assert metadata["word_count"] == 2
        assert metadata["multiline"] is False
        assert "processed_at" in metadata
    
    @pytest.mark.asyncio
    async def test_user_input_plugin_multiline_support(self):
        """Test that UserInputPlugin handles multiline input properly."""
        plugin = UserInputPlugin()
        await plugin.initialize({"max_length": 1000, "allow_empty": False})
        await plugin.activate()
        
        # Process multiline input
        multiline_input = "Line 1\nLine 2\nLine 3"
        result = await plugin.process(multiline_input, {})
        
        # Verify the plugin completed successfully
        assert plugin.state == PluginState.COMPLETED
        assert result["input"] == multiline_input
        
        # Render the plugin
        context = RenderContext(display_mode="inscribed")
        render_data = await plugin.render(context)
        
        # Verify multiline handling
        assert render_data["content"] == multiline_input
        metadata = render_data["metadata"]
        assert metadata["multiline"] is True
        assert metadata["character_count"] == len(multiline_input)
        assert metadata["word_count"] == 6  # "Line", "1", "Line", "2", "Line", "3"
    
    @pytest.mark.asyncio
    async def test_input_system_key_bindings(self):
        """Test that input system has proper key bindings setup."""
        input_system = SimpleMultilineInput()
        
        # Verify key bindings exist
        assert input_system.kb is not None
        
        # Check that we have some key bindings (the exact format may vary)
        assert len(input_system.kb.bindings) > 0
        
        # Verify we can create the input system without errors
        # The actual key binding verification is complex due to prompt_toolkit internals
        assert hasattr(input_system, '_setup_bindings')
        assert hasattr(input_system, 'get_input')
    
    @pytest.mark.asyncio
    async def test_no_you_prompt_pollution(self):
        """Test that we don't have 'You:' pollution in the timeline."""
        # This test verifies that user input doesn't create "You:" lines
        # by checking that UserInputPlugin only shows the content without prefix
        
        plugin = UserInputPlugin()
        await plugin.initialize({})
        await plugin.activate()
        
        user_input = "Test query"
        await plugin.process(user_input, {})
        
        # Render the plugin
        context = RenderContext(display_mode="inscribed")
        render_data = await plugin.render(context)
        
        # Verify no "You:" prefix in the content
        content = render_data["content"]
        assert not content.startswith("You:")
        assert content == user_input
        
        # The display formatting will add ">" in the main.py render logic,
        # but the plugin itself just stores the clean content
    
    @pytest.mark.asyncio
    async def test_input_validation_still_works(self):
        """Test that input validation still works in the new system."""
        plugin = UserInputPlugin()
        await plugin.initialize({"max_length": 10, "allow_empty": False})
        await plugin.activate()
        
        # Test empty input rejection
        with pytest.raises(ValueError, match="Input validation failed"):
            await plugin.process("", {})
        
        assert plugin.state == PluginState.ERROR
        
        # Test too long input rejection
        plugin_2 = UserInputPlugin()
        await plugin_2.initialize({"max_length": 5, "allow_empty": False})
        await plugin_2.activate()
        
        with pytest.raises(ValueError, match="exceeds maximum length"):
            await plugin_2.process("This is too long", {})
        
        assert plugin_2.state == PluginState.ERROR
    
    @pytest.mark.asyncio
    async def test_input_metadata_tracking(self):
        """Test that input metadata is properly tracked."""
        plugin = UserInputPlugin()
        await plugin.initialize({})
        await plugin.activate()
        
        test_input = "Hello\nWorld\nTest"
        await plugin.process(test_input, {})
        
        # Get input metadata
        metadata = plugin.get_input_metadata()
        
        assert metadata["input_length"] == len(test_input)
        assert metadata["processed"] is True
        assert metadata["validation_errors"] == []
        assert "input_timestamp" in metadata
        
        # Verify get_user_input method
        assert plugin.get_user_input() == test_input
    
    def test_simple_multiline_input_documentation(self):
        """Test that SimpleMultilineInput has proper documentation."""
        input_system = SimpleMultilineInput()
        
        # Verify class docstring mentions key bindings
        docstring = input_system.__class__.__doc__
        assert "Enter" in docstring
        assert "Ctrl+J" in docstring
        assert "Ctrl+C" in docstring
        assert "Ctrl+D" in docstring
    
    @pytest.mark.asyncio 
    async def test_timeline_cleanliness(self):
        """Test that the timeline shows clean input without pollution."""
        # Simulate what the main.py render logic does
        plugin = UserInputPlugin()
        await plugin.initialize({})
        await plugin.activate()
        
        # Test single line input
        await plugin.process("Hello", {})
        context = RenderContext(display_mode="inscribed")
        render_data = await plugin.render(context)
        
        # The main.py formatting should add ">" but the plugin content is clean
        assert render_data["content"] == "Hello"
        
        # Test multiline input
        plugin_2 = UserInputPlugin()
        await plugin_2.initialize({})
        await plugin_2.activate()
        
        multiline = "Line 1\nLine 2\nLine 3"
        await plugin_2.process(multiline, {})
        render_data_2 = await plugin_2.render(context)
        
        # Content should be preserved as-is
        assert render_data_2["content"] == multiline
        assert render_data_2["metadata"]["multiline"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])