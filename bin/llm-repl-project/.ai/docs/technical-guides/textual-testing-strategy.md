# Textual Testing Strategy Ledger

**Scope:** Comprehensive testing approach for V3 Textual implementation  
**Goal:** Ensure functionality preservation, terminal integration, and Sway compatibility

## Testing Architecture

### Test Categories
1. **Unit Tests** - Core business logic (preserved from V2-tkinter-rewrite)
2. **Widget Tests** - Textual component functionality  
3. **Integration Tests** - Full application workflow
4. **Terminal Tests** - Terminal-native behavior validation
5. **Sway Tests** - Window manager integration
6. **Performance Tests** - Responsiveness and resource usage

---

## Unit Testing (Core Logic Preservation)

### Test Suite Migration Strategy
```python
# V3/tests/test_core.py - Port existing tests
"""
Port the complete test suite from V2-tkinter-rewrite/tests/test_core.py
These tests validate core business logic remains unchanged.
"""

import pytest
import sys
from pathlib import Path

# Ensure V3 core modules are importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.blocks import (
    BlockType, TimelineBlock,
    create_system_check_block, create_welcome_block,
    create_user_input_block, create_cognition_block,
    create_assistant_response_block, create_error_block
)
from core.cognition import CognitionProcessor
from core.timeline import TimelineManager

# Copy all test classes from V2-tkinter-rewrite exactly
class TestTimelineBlocks:
    """Preserve all existing block tests"""
    # Copy from V2-tkinter-rewrite/tests/test_core.py
    pass

class TestCognitionProcessor:
    """Preserve all existing cognition tests"""
    # Copy from V2-tkinter-rewrite/tests/test_core.py
    pass

class TestTimelineManager:
    """Preserve all existing timeline tests"""
    # Copy from V2-tkinter-rewrite/tests/test_core.py
    pass
```

### Core Logic Validation
```bash
# Test runner to validate core logic migration
cd V3
python -m pytest tests/test_core.py -v

# Expected output:
# test_core.py::TestTimelineBlocks::test_block_creation PASSED
# test_core.py::TestTimelineBlocks::test_block_helper_methods PASSED
# test_core.py::TestCognitionProcessor::test_processing PASSED
# test_core.py::TestTimelineManager::test_block_management PASSED
# ... (all existing tests should pass)
```

---

## Widget Testing (Textual Components)

### Timeline Widget Tests
```python
# V3/tests/test_timeline_widget.py
import pytest
from textual.app import App
from widgets.timeline_widget import TimelineWidget
from core.blocks import create_user_input_block, create_assistant_response_block

class TestTimelineWidget:
    """Test TimelineWidget functionality"""
    
    def test_widget_initialization(self):
        """Test widget starts correctly"""
        widget = TimelineWidget()
        assert widget.timeline_manager.get_block_count() == 0
        assert "Welcome" in widget.timeline_content
    
    def test_add_single_block(self):
        """Test adding a single block"""
        widget = TimelineWidget()
        block = create_user_input_block("Test message")
        
        widget.add_block(block)
        
        assert widget.timeline_manager.get_block_count() == 1
        assert "Test message" in widget.timeline_content
    
    def test_add_multiple_blocks(self):
        """Test adding multiple blocks maintains order"""
        widget = TimelineWidget()
        
        user_block = create_user_input_block("User message")
        assistant_block = create_assistant_response_block("Assistant response")
        
        widget.add_block(user_block)
        widget.add_block(assistant_block)
        
        assert widget.timeline_manager.get_block_count() == 2
        
        # Check order is preserved in content
        content = widget.timeline_content
        user_pos = content.find("User message")
        assistant_pos = content.find("Assistant response")
        assert user_pos < assistant_pos
    
    def test_clear_timeline(self):
        """Test clearing timeline"""
        widget = TimelineWidget()
        widget.add_block(create_user_input_block("Test"))
        
        widget.clear()
        
        assert widget.timeline_manager.get_block_count() == 0
        assert "Welcome" in widget.timeline_content
    
    def test_block_rendering_styles(self):
        """Test blocks render with correct styling"""
        widget = TimelineWidget()
        
        # Test different block types render differently
        user_block = create_user_input_block("User message")
        assistant_block = create_assistant_response_block("Assistant message")
        
        widget.add_block(user_block)
        widget.add_block(assistant_block)
        
        # Verify visual distinction (colors, icons, etc.)
        rendered = widget._render_block(user_block)
        assert "❯" in str(rendered)  # User icon
        
        rendered = widget._render_block(assistant_block)
        assert "🤖" in str(rendered)  # Assistant icon
```

### Input Widget Tests
```python
# V3/tests/test_input_widget.py
import pytest
from textual.widgets import Input, Button
from widgets.input_widget import InputWidget, UserMessage

class TestInputWidget:
    """Test InputWidget functionality"""
    
    def test_widget_composition(self):
        """Test widget composes correctly"""
        widget = InputWidget()
        
        # Check required components exist
        input_field = widget.query_one("#user-input", Input)
        send_button = widget.query_one("#send-btn", Button)
        
        assert input_field is not None
        assert send_button is not None
        assert send_button.label.plain == "Send"
    
    def test_input_submission_enter_key(self):
        """Test Enter key submits input"""
        widget = InputWidget()
        messages = []
        
        # Mock message posting
        original_post = widget.post_message
        def mock_post(message):
            messages.append(message)
        widget.post_message = mock_post
        
        # Simulate user input and Enter
        input_field = widget.query_one("#user-input", Input)
        input_field.value = "Test message"
        
        # Simulate Enter key submission
        from textual.events import Input as InputEvent
        event = InputEvent.Submitted(input_field, "Test message")
        widget.on_input_submitted(event)
        
        # Verify message was posted and input cleared
        assert len(messages) == 1
        assert isinstance(messages[0], UserMessage)
        assert messages[0].text == "Test message"
        assert input_field.value == ""
    
    def test_send_button_click(self):
        """Test Send button submits input"""
        widget = InputWidget()
        messages = []
        
        # Mock message posting
        def mock_post(message):
            messages.append(message)
        widget.post_message = mock_post
        
        # Set input value
        input_field = widget.query_one("#user-input", Input)
        input_field.value = "Button test"
        
        # Simulate button click
        send_button = widget.query_one("#send-btn", Button)
        from textual.events import Button as ButtonEvent
        event = ButtonEvent.Pressed(send_button)
        widget.on_button_pressed(event)
        
        # Verify message was posted
        assert len(messages) == 1
        assert messages[0].text == "Button test"
    
    def test_empty_input_ignored(self):
        """Test empty/whitespace input is ignored"""
        widget = InputWidget()
        messages = []
        
        def mock_post(message):
            messages.append(message)
        widget.post_message = mock_post
        
        # Test empty string
        input_field = widget.query_one("#user-input", Input)
        input_field.value = ""
        
        event = InputEvent.Submitted(input_field, "")
        widget.on_input_submitted(event)
        
        assert len(messages) == 0
        
        # Test whitespace only
        input_field.value = "   \\n\\t  "
        event = InputEvent.Submitted(input_field, "   \\n\\t  ")
        widget.on_input_submitted(event)
        
        assert len(messages) == 0
    
    def test_status_updates(self):
        """Test status display updates"""
        widget = InputWidget()
        
        widget.set_status("Processing...", "processing")
        status = widget.query_one("#status")
        assert status.renderable.plain == "Processing..."
        
        widget.set_status("Ready", "ready")
        assert status.renderable.plain == "Ready"
```

---

## Integration Testing (Full Workflow)

### Application Integration Tests
```python
# V3/tests/test_integration.py
import pytest
import asyncio
from textual.app import App
from app import LLMReplApp
from widgets.input_widget import UserMessage

class TestApplicationIntegration:
    """Test complete application workflows"""
    
    @pytest.mark.asyncio
    async def test_startup_sequence(self):
        """Test application starts with correct initial state"""
        app = LLMReplApp("debug")
        
        # Simulate mount without running GUI
        await app._handle_startup()
        
        timeline = app.query_one("#timeline")
        
        # Should have system check and welcome blocks
        assert timeline.timeline_manager.get_block_count() == 2
        
        blocks = timeline.timeline_manager.get_blocks()
        assert blocks[0].type.value == "system_check"
        assert blocks[1].type.value == "welcome"
    
    @pytest.mark.asyncio 
    async def test_user_message_flow(self):
        """Test complete user message processing flow"""
        app = LLMReplApp("debug")
        await app._handle_startup()
        
        timeline = app.query_one("#timeline")
        initial_count = timeline.timeline_manager.get_block_count()
        
        # Send user message
        message = UserMessage("Hello, world!")
        await app.on_user_message(message)
        
        # Should have added user block, cognition block, and assistant response
        final_count = timeline.timeline_manager.get_block_count()
        assert final_count == initial_count + 3
        
        # Verify block types and order
        new_blocks = timeline.timeline_manager.get_blocks()[initial_count:]
        assert new_blocks[0].type.value == "user_input"
        assert new_blocks[1].type.value == "cognition"
        assert new_blocks[2].type.value == "assistant_response"
        
        # Verify content
        assert "Hello, world!" in new_blocks[0].content
        assert new_blocks[2].content  # Assistant should have responded
    
    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error scenarios are handled gracefully"""
        app = LLMReplApp("debug")
        
        # Mock cognition processor to raise error
        original_process = app.cognition_processor.process
        async def failing_process(text):
            raise Exception("Simulated processing error")
        app.cognition_processor.process = failing_process
        
        timeline = app.query_one("#timeline")
        initial_count = timeline.timeline_manager.get_block_count()
        
        # Send message that will cause error
        message = UserMessage("This will fail")
        await app.on_user_message(message)
        
        # Should have user block and error block
        blocks = timeline.timeline_manager.get_blocks()[initial_count:]
        assert len(blocks) >= 2
        assert blocks[0].type.value == "user_input"
        
        # Should have error block somewhere
        error_blocks = [b for b in blocks if b.type.value == "error"]
        assert len(error_blocks) == 1
        assert "error" in error_blocks[0].content.lower()
    
    def test_keyboard_shortcuts(self):
        """Test keyboard shortcuts work correctly"""
        app = LLMReplApp("debug")
        
        # Test clear shortcut
        timeline = app.query_one("#timeline")
        timeline.add_block(create_user_input_block("Test"))
        
        app.action_clear_timeline()
        
        # Timeline should be cleared
        assert timeline.timeline_manager.get_block_count() == 0
    
    def test_configuration_loading(self):
        """Test different configurations load correctly"""
        debug_app = LLMReplApp("debug")
        assert debug_app.config.name == "debug"
        
        fast_app = LLMReplApp("fast") 
        assert fast_app.config.name == "fast"
        
        # Cognition delay should be different
        assert debug_app.cognition_processor.processing_delay != fast_app.cognition_processor.processing_delay
```

### Message System Tests
```python
# V3/tests/test_message_system.py
import pytest
from messages import UserMessage, ClearTimeline, ProcessingComplete
from app import LLMReplApp

class TestMessageSystem:
    """Test Textual message passing system"""
    
    def test_message_creation(self):
        """Test custom messages create correctly"""
        user_msg = UserMessage("Test text")
        assert user_msg.text == "Test text"
        
        clear_msg = ClearTimeline()
        assert isinstance(clear_msg, ClearTimeline)
        
        result_msg = ProcessingComplete({"output": "test"})
        assert result_msg.result["output"] == "test"
    
    @pytest.mark.asyncio
    async def test_message_handling(self):
        """Test messages are handled correctly by app"""
        app = LLMReplApp("debug")
        
        # Test user message handling
        timeline = app.query_one("#timeline")
        initial_count = timeline.timeline_manager.get_block_count()
        
        user_msg = UserMessage("Test message")
        await app.on_user_message(user_msg)
        
        # Timeline should have new blocks
        assert timeline.timeline_manager.get_block_count() > initial_count
```

---

## Terminal Integration Testing

### Terminal Behavior Tests
```python
# V3/tests/test_terminal_integration.py
import os
import subprocess
import pytest
from theme.terminal_integration import TerminalIntegration

class TestTerminalIntegration:
    """Test terminal-specific behavior"""
    
    def test_terminal_size_detection(self):
        """Test terminal size detection works"""
        lines, cols = TerminalIntegration.get_terminal_size()
        
        assert isinstance(lines, int)
        assert isinstance(cols, int)
        assert lines > 0
        assert cols > 0
        # Reasonable bounds
        assert 10 <= lines <= 200
        assert 40 <= cols <= 500
    
    def test_transparency_support_detection(self):
        """Test transparency support detection"""
        # Mock different TERM values
        original_term = os.environ.get("TERM", "")
        
        try:
            # Test supported terminals
            os.environ["TERM"] = "alacritty"
            assert TerminalIntegration.supports_transparency() == True
            
            os.environ["TERM"] = "xterm-kitty"
            assert TerminalIntegration.supports_transparency() == True
            
            # Test unsupported terminals
            os.environ["TERM"] = "xterm"
            assert TerminalIntegration.supports_transparency() == False
            
        finally:
            os.environ["TERM"] = original_term
    
    def test_sway_environment_detection(self):
        """Test Sway environment detection"""
        # Mock SWAYSOCK environment
        original_swaysock = os.environ.get("SWAYSOCK")
        
        try:
            # Test with Sway
            os.environ["SWAYSOCK"] = "/run/user/1000/sway-ipc.sock"
            assert TerminalIntegration.is_sway_environment() == True
            
            # Test without Sway
            if "SWAYSOCK" in os.environ:
                del os.environ["SWAYSOCK"]
            assert TerminalIntegration.is_sway_environment() == False
            
        finally:
            if original_swaysock:
                os.environ["SWAYSOCK"] = original_swaysock
```

### Theme Integration Tests
```python
# V3/tests/test_theme_integration.py
import pytest
from theme.theme import TerminalTheme, ThemeVariant
from theme.loader import ThemeLoader

class TestThemeIntegration:
    """Test theme system integration"""
    
    def test_theme_loading(self):
        """Test themes load correctly"""
        tokyo_theme = TerminalTheme.get_theme(ThemeVariant.TOKYO_NIGHT)
        assert tokyo_theme["name"] == "Tokyo Night"
        assert "colors" in tokyo_theme
        assert "background" in tokyo_theme["colors"]
        
        nord_theme = TerminalTheme.get_theme(ThemeVariant.NORD)
        assert nord_theme["name"] == "Nord"
        
        # Themes should be different
        assert tokyo_theme["colors"]["background"] != nord_theme["colors"]["background"]
    
    def test_css_variable_generation(self):
        """Test CSS variable generation from themes"""
        theme = TerminalTheme.get_theme(ThemeVariant.TOKYO_NIGHT)
        css_vars = ThemeLoader._generate_css_variables(theme["colors"])
        
        assert "background" in css_vars
        assert "text-primary" in css_vars
        assert "accent-user" in css_vars
        
        # Values should be hex colors
        assert css_vars["background"].startswith("#")
    
    def test_theme_detection(self):
        """Test automatic theme detection"""
        # This is environment-dependent, so test basic functionality
        detected = ThemeLoader.detect_terminal_theme()
        
        # Should either detect a theme or return None
        if detected:
            assert isinstance(detected, ThemeVariant)
```

---

## Sway Integration Testing

### Manual Sway Tests
```bash
#!/bin/bash
# V3/tests/test_sway_integration.sh
# Manual tests for Sway window manager integration

echo "🎯 Testing LLM REPL V3 Sway Integration"
echo "========================================"

# Prerequisites check
if [ -z "$SWAYSOCK" ]; then
    echo "❌ Not running under Sway - skipping Sway-specific tests"
    exit 1
fi

echo "✅ Sway environment detected"

# Test 1: Application launches and tiles correctly
echo "📋 Test 1: Launch and tiling behavior"
echo "  Launching app in new terminal..."

alacritty -e python V3/main.py &
APP_PID=$!
sleep 3

echo "  ✅ App launched (PID: $APP_PID)"
echo "  👀 Manual check: Does app tile properly with gaps?"
echo "  Press Enter when verified..."
read

pkill -P $APP_PID 2>/dev/null
kill $APP_PID 2>/dev/null

# Test 2: Transparency support
echo "📋 Test 2: Transparency support"
echo "  Launching with transparent terminal..."

alacritty --config-file /dev/stdin -e python V3/main.py <<EOF &
window:
  opacity: 0.8
EOF

APP_PID=$!
sleep 3

echo "  👀 Manual check: Is app background transparent?"
echo "  Press Enter when verified..."
read

pkill -P $APP_PID 2>/dev/null
kill $APP_PID 2>/dev/null

# Test 3: Keyboard shortcuts don't conflict
echo "📋 Test 3: Keyboard shortcut conflicts"
echo "  Testing common Sway shortcuts..."
echo "  Mod+Enter (new terminal) should work"
echo "  Mod+Q (close window) should work" 
echo "  App's Ctrl+C should quit app, not interfere with Sway"
echo "  👀 Manual verification required"

# Test 4: Font rendering
echo "📋 Test 4: Font rendering"
echo "  👀 Manual check: Does text look crisp and properly spaced?"
echo "  👀 Check: Do icons/emojis render correctly?"

echo "🎯 Sway integration tests complete"
echo "   Most tests require manual verification"
echo "   All checks should pass for Sway compatibility"
```

### Automated Sway Property Tests
```python
# V3/tests/test_sway_properties.py
import os
import subprocess
import pytest

class TestSwayProperties:
    """Test Sway-specific properties and behaviors"""
    
    @pytest.mark.skipif(not os.getenv("SWAYSOCK"), reason="Not running under Sway")
    def test_window_class_detection(self):
        """Test app gets correct window class in Sway"""
        # This would require launching the app and querying Sway
        # for window properties - complex integration test
        pass
    
    @pytest.mark.skipif(not os.getenv("SWAYSOCK"), reason="Not running under Sway")  
    def test_focus_behavior(self):
        """Test focus behavior in Sway"""
        # Test that app receives focus properly
        # Test that keyboard input works correctly
        pass
    
    def test_terminal_emulator_compatibility(self):
        """Test compatibility with common terminal emulators"""
        common_terminals = ["alacritty", "kitty", "foot", "wezterm"]
        
        for terminal in common_terminals:
            # Check if terminal is available
            try:
                result = subprocess.run([terminal, "--version"], 
                                      capture_output=True, 
                                      timeout=5)
                if result.returncode == 0:
                    print(f"✅ {terminal} available")
                    # Could launch app in each terminal for testing
                else:
                    print(f"⚠️  {terminal} not available")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                print(f"❌ {terminal} not found")
```

---

## Performance Testing

### Startup Performance Tests
```python
# V3/tests/test_performance.py
import time
import asyncio
import psutil
import pytest
from app import LLMReplApp

class TestPerformance:
    """Test application performance characteristics"""
    
    def test_startup_time(self):
        """Test application startup time"""
        times = []
        
        for _ in range(5):
            start = time.time()
            
            # Create app (without running GUI)
            app = LLMReplApp("debug")
            
            end = time.time()
            times.append(end - start)
        
        avg_time = sum(times) / len(times)
        print(f"Average startup time: {avg_time:.3f}s")
        
        # Should start quickly for terminal app
        assert avg_time < 1.0, f"Startup too slow: {avg_time:.3f}s"
    
    @pytest.mark.asyncio
    async def test_message_processing_time(self):
        """Test message processing performance"""
        app = LLMReplApp("debug")
        
        # Configure fast processing for testing
        app.cognition_processor.configure_processing_delay(0.01)
        
        start = time.time()
        
        # Process a simple message
        result = await app.cognition_processor.process("Hello")
        
        end = time.time()
        processing_time = end - start
        
        print(f"Message processing time: {processing_time:.3f}s")
        
        # Should be reasonably fast even with mocked processing
        assert processing_time < 5.0, f"Processing too slow: {processing_time:.3f}s"
    
    def test_memory_usage(self):
        """Test memory usage is reasonable"""
        process = psutil.Process()
        
        # Baseline memory
        baseline = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create app
        app = LLMReplApp("debug")
        
        # Add some blocks to timeline
        timeline = app.query_one("#timeline")
        for i in range(100):
            block = create_user_input_block(f"Message {i}")
            timeline.add_block(block)
        
        # Check memory usage
        current = process.memory_info().rss / 1024 / 1024  # MB
        usage = current - baseline
        
        print(f"Memory usage: {usage:.1f}MB")
        
        # Should use reasonable amount of memory
        assert usage < 100, f"Memory usage too high: {usage:.1f}MB"
    
    def test_ui_responsiveness(self):
        """Test UI remains responsive under load"""
        app = LLMReplApp("debug")
        timeline = app.query_one("#timeline")
        
        # Add many blocks quickly
        start = time.time()
        
        for i in range(1000):
            block = create_user_input_block(f"Block {i}")
            timeline.add_block(block)
        
        end = time.time()
        total_time = end - start
        
        print(f"Added 1000 blocks in {total_time:.3f}s")
        
        # Should handle many blocks without significant slowdown
        assert total_time < 5.0, f"UI too slow with many blocks: {total_time:.3f}s"
```

---

## Continuous Integration Setup

### GitHub Actions Workflow
```yaml
# .github/workflows/test_v3.yml
name: V3 Tests

on:
  push:
    paths: 
      - 'V3/**'
  pull_request:
    paths:
      - 'V3/**'

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd V3
        pip install -r requirements.txt
        pip install pytest pytest-asyncio pytest-cov
    
    - name: Run unit tests
      run: |
        cd V3
        python -m pytest tests/test_core.py -v
    
    - name: Run widget tests  
      run: |
        cd V3
        python -m pytest tests/test_*widget*.py -v
    
    - name: Run integration tests
      run: |
        cd V3
        python -m pytest tests/test_integration.py -v
    
    - name: Run performance tests
      run: |
        cd V3
        python -m pytest tests/test_performance.py -v
    
    - name: Generate coverage report
      run: |
        cd V3
        python -m pytest --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: V3/coverage.xml
```

### Test Execution Script
```bash
#!/bin/bash
# V3/run_tests.sh
# Comprehensive test runner

echo "🧪 Running LLM REPL V3 Test Suite"
echo "=================================="

cd V3

# Unit tests
echo "📋 Running unit tests..."
python -m pytest tests/test_core.py -v
if [ $? -ne 0 ]; then
    echo "❌ Unit tests failed"
    exit 1
fi

# Widget tests
echo "📋 Running widget tests..."
python -m pytest tests/test_*widget*.py -v
if [ $? -ne 0 ]; then
    echo "❌ Widget tests failed"
    exit 1
fi

# Integration tests
echo "📋 Running integration tests..."
python -m pytest tests/test_integration.py -v
if [ $? -ne 0 ]; then
    echo "❌ Integration tests failed"
    exit 1
fi

# Performance tests
echo "📋 Running performance tests..."
python -m pytest tests/test_performance.py -v
if [ $? -ne 0 ]; then
    echo "❌ Performance tests failed"
    exit 1
fi

echo "✅ All tests passed!"

# Optional: Run manual Sway tests if in Sway environment
if [ -n "$SWAYSOCK" ]; then
    echo "📋 Sway environment detected - running integration tests..."
    bash tests/test_sway_integration.sh
fi

echo "🎯 Test suite complete!"
```

This comprehensive testing strategy ensures V3 maintains all functionality from V2-tkinter-rewrite while validating the new terminal-native behavior and Sway integration.