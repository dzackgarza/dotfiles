# Advanced Guide: Automated User Experience Testing for Python Textual Apps

This comprehensive guide addresses both fundamental testing strategies and advanced user experience testing for apps built with the [Textual](https://textual.textualize.io/) TUI framework. It covers how to test real user interactions, visual feedback, accessibility, and workflow reliability—going far beyond core logic validation. All examples are tailored specifically to Textual applications and our Sacred GUI Architecture patterns.

## 1. What Does "Testing User Experience" Really Mean?

Testing user experience (UX) in Textual apps goes beyond verifying that functions return correct values. It means:

- **Simulating real user workflows:** Navigating, typing, clicking, scrolling, and seeing what the user sees in the Sacred Architecture interface.
- **Validating visual and interactive feedback:** Ensuring UI elements in Sacred Timeline and Live Workspace update, animate, and respond as intended.
- **Checking accessibility and usability:** Verifying keyboard navigation, error messages, and clarity across our 2-way ↔ 3-way split design.
- **Assessing layout and responsiveness:** Confirming that dynamic content, streaming updates, and scrollable areas behave intuitively.
- **Ensuring error states and edge cases are surfaced and handled gracefully** without breaking the Sacred Architecture.

## 2. Testing Philosophy for Sacred Architecture

- **Simulate Real User Interactions:** Test as a user would—via key presses, focus changes, and observing Sacred Timeline/Live Workspace updates.
- **Isolate Each Test:** Ensure tests are independent and reset app state between runs.
- **Automate Early:** Integrate tests into your workflow and CI for rapid feedback.
- **Sacred Architecture Focus:** Test the proven V3 patterns and validate no layout conflicts occur.
- **Workflow Reliability:** Verify complete user journeys through cognition processing and workspace transitions.

## 3. Core Testing Strategies

### a. Unit Testing

Test pure logic and utility functions separate from UI. Use `pytest` or `unittest`.

**Example:**
```python
def format_username(name):
    return name.strip().capitalize()

def test_format_username():
    assert format_username(" alice ") == "Alice"
```

**Sacred Architecture Unit Tests:**
```python
def test_unified_timeline_block_creation():
    timeline = UnifiedTimeline()
    block = timeline.add_live_block("user", "test content")
    assert block.role == "user"
    assert block.data.content == "test content"
    assert timeline.owns_block(block.id)
```

### b. Integration Testing

Test how widgets and services interact. Simulate user events and check UI state.

**Example:**
```python
import pytest
from textual.app import App

class MyTextualApp(App):
    ...

@pytest.mark.asyncio
async def test_input_triggers_message():
    app = MyTextualApp()
    async with app.run_test() as pilot:
        await pilot.press("h")
        await pilot.press("i")
        await pilot.press("enter")
        messages = app.query("#message_list").first()
        assert "hi" in messages.text
```

**Sacred Architecture Integration Tests:**
```python
@pytest.mark.asyncio
async def test_sacred_timeline_widget_integration():
    app = LLMReplApp()
    async with app.run_test() as pilot:
        sacred_timeline = app.query_one("#sacred-timeline")
        assert sacred_timeline is not None
        assert isinstance(sacred_timeline, SacredTimelineWidget)
        
        # Test block addition
        test_block = InscribedBlock(
            id="test-123",
            role="user", 
            content="Test message",
            metadata={}
        )
        await sacred_timeline.add_block(test_block)
        assert sacred_timeline.get_block_count() == 1
```

### c. End-to-End (E2E) Testing

Simulate full user workflows using Textual's headless test mode and the `Pilot` object.

**Example:**
```python
@pytest.mark.asyncio
async def test_send_message_flow():
    app = MyTextualApp()
    async with app.run_test() as pilot:
        await pilot.focus("#input_box")
        await pilot.type("Hello, world!")
        await pilot.press("enter")
        chat = app.query_one("#message_list")
        assert "Hello, world!" in chat.text
```

**Sacred Architecture E2E Tests:**
```python
@pytest.mark.asyncio
async def test_complete_user_interaction_flow():
    """Test full Sacred Architecture user interaction flow"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        # Focus prompt input
        prompt_input = app.query_one("#prompt-input")
        await pilot.focus(prompt_input)
        
        # Type test message
        test_message = "Hello, Sacred Architecture!"
        await pilot.type(test_message)
        
        # Submit message
        await pilot.press("enter")
        
        # Wait for processing
        await pilot.pause(0.5)
        
        # Verify Sacred Timeline received user block
        sacred_timeline = app.query_one("#sacred-timeline")
        assert sacred_timeline.get_block_count() >= 1
        
        # Verify Live Workspace shows during processing
        live_workspace = app.query_one("#live-workspace")
        assert live_workspace.is_visible
        
        # Verify input cleared
        assert prompt_input.text == ""
```

## 4. Advanced User Experience Testing Strategies

### a. Simulate Real User Interactions

**Keyboard Navigation Testing:**
```python
@pytest.mark.asyncio
async def test_keyboard_navigation_sacred_architecture():
    """Test complete keyboard navigation through Sacred Architecture"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        # Start with focus on prompt input
        prompt_input = app.query_one("#prompt-input")
        assert prompt_input.has_focus
        
        # Tab navigation through interface
        await pilot.press("tab")
        # Should move to next focusable element
        
        # Arrow key navigation in Sacred Timeline
        sacred_timeline = app.query_one("#sacred-timeline")
        await pilot.focus(sacred_timeline)
        await pilot.press("up", "down")
        
        # Verify focus indicators are visible
        focused_widget = app.focused
        assert focused_widget is not None
        assert focused_widget.has_class("focus")
```

**Mouse Actions and Touch Simulation:**
```python
@pytest.mark.asyncio
async def test_mouse_interactions():
    """Test mouse/click interactions in Sacred Architecture"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        # Click on specific widgets
        sacred_timeline = app.query_one("#sacred-timeline")
        await pilot.click(sacred_timeline)
        
        # Verify click changed focus or triggered action
        assert sacred_timeline.has_focus
        
        # Test scroll wheel simulation
        await pilot.scroll(sacred_timeline, lines=5)
        scroll_position = sacred_timeline.scroll_y
        assert scroll_position > 0
```

**Rapid Typing and Input Stress Testing:**
```python
@pytest.mark.asyncio
async def test_rapid_typing_stress():
    """Test rapid input handling without UI corruption"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        prompt_input = app.query_one("#prompt-input")
        await pilot.focus(prompt_input)
        
        # Rapid typing simulation
        rapid_text = "This is a very long message that tests rapid typing and input handling"
        for char in rapid_text:
            await pilot.type(char)
            # No pause - stress test input handling
        
        # Verify text integrity
        assert prompt_input.text == rapid_text
        
        # Test rapid backspacing
        for _ in range(10):
            await pilot.press("backspace")
        
        # Verify partial text remains correct
        expected = rapid_text[:-10]
        assert prompt_input.text == expected
```

### b. Assert on Visual and Interactive Feedback

**UI State and Dynamic Content Testing:**
```python
@pytest.mark.asyncio
async def test_workspace_visual_transitions():
    """Test visual feedback during Sacred Architecture transitions"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        live_workspace = app.query_one("#live-workspace")
        
        # Initially hidden (2-way split)
        assert live_workspace.has_class("hidden")
        assert not live_workspace.is_visible
        
        # Trigger cognition (should show workspace)
        prompt_input = app.query_one("#prompt-input")
        await pilot.focus(prompt_input)
        await pilot.type("test cognition trigger")
        await pilot.press("enter")
        
        # Wait for transition animation
        await pilot.pause(0.2)
        
        # Verify workspace is now visible (3-way split)
        assert not live_workspace.has_class("hidden")
        assert live_workspace.is_visible
        
        # Verify visual indicators (opacity, borders, etc.)
        assert live_workspace.styles.opacity == 1.0
```

**Streaming Content Visual Updates:**
```python
@pytest.mark.asyncio
async def test_streaming_visual_feedback():
    """Test visual feedback during content streaming"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        live_workspace = app.query_one("#live-workspace")
        
        # Create streaming sub-module
        sub_module = LiveBlock(
            id="visual-stream-test",
            role="route_query", 
            data=LiveBlockData(content="", sub_blocks=[], metadata={})
        )
        
        await live_workspace.add_sub_module(sub_module)
        widget = live_workspace.sub_module_widgets[sub_module.id]
        
        # Test incremental visual updates
        content_chunks = ["Processing", "...", " analyzing", "...", " complete!"]
        
        for chunk in content_chunks:
            sub_module.append_content(chunk)
            await pilot.pause(0.1)  # Allow UI update
            
            # Verify content is visually updated
            rendered_content = widget.sub_module.data.content
            assert chunk in rendered_content
            
            # Verify visual indicators (streaming state)
            assert widget.has_class("state-live")
```

### c. Validate Layout, Responsiveness, and Accessibility

**Layout Consistency and Responsiveness:**
```python
@pytest.mark.asyncio
async def test_layout_responsiveness():
    """Test Sacred Architecture layout under various conditions"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        # Test with minimal content
        sacred_timeline = app.query_one("#sacred-timeline")
        initial_height = sacred_timeline.size.height
        
        # Add substantial content
        for i in range(20):
            block = InscribedBlock(
                id=f"layout-test-{i}",
                role="user",
                content=f"This is test message {i} with substantial content to test layout responsiveness and scrolling behavior in the Sacred Timeline widget.",
                metadata={}
            )
            await sacred_timeline.add_block(block)
        
        # Verify layout adapts (scrollable, no overflow)
        assert sacred_timeline.max_scroll_y > 0
        assert sacred_timeline.size.height == initial_height  # Container size stable
        
        # Test Live Workspace layout adaptation
        live_workspace = app.query_one("#live-workspace")
        live_workspace.show_workspace()
        
        # Add multiple sub-modules
        for i in range(10):
            sub_module = LiveBlock(
                id=f"sub-{i}",
                role="call_tool",
                data=LiveBlockData(
                    content=f"Sub-module {i} with dynamic content that tests workspace layout adaptation",
                    sub_blocks=[],
                    metadata={}
                )
            )
            await live_workspace.add_sub_module(sub_module)
        
        # Verify workspace handles multiple sub-modules without layout corruption
        assert live_workspace.get_sub_module_count() == 10
        assert live_workspace.max_scroll_y > 0  # Scrollable when needed
```

**Accessibility Testing:**
```python
@pytest.mark.asyncio
async def test_accessibility_compliance():
    """Test accessibility features in Sacred Architecture"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        # Test keyboard-only navigation
        focusable_widgets = [
            "#prompt-input",
            "#sacred-timeline", 
            "#live-workspace"
        ]
        
        for widget_id in focusable_widgets:
            widget = app.query_one(widget_id)
            await pilot.focus(widget)
            
            # Verify focus indicators
            assert widget.has_focus
            assert widget.has_class("focus") or widget.pseudo_classes.intersection({"focus"})
            
            # Test screen reader accessibility
            assert hasattr(widget, 'aria_label') or hasattr(widget, 'title')
        
        # Test error message accessibility
        # Simulate error condition
        with patch('src.core.unified_async_processor.UnifiedAsyncProcessor.process_user_input_async') as mock_process:
            mock_process.side_effect = Exception("Test error")
            
            prompt_input = app.query_one("#prompt-input")
            await pilot.focus(prompt_input)
            await pilot.type("trigger error")
            await pilot.press("enter")
            
            await pilot.pause(0.5)
            
            # Verify error is accessible
            # Should appear in Sacred Timeline with appropriate role
            blocks = app.unified_async_processor.get_timeline().get_all_blocks()
            error_blocks = [b for b in blocks if "error" in b.content.lower()]
            assert len(error_blocks) > 0
```

### d. Test Error and Edge States

**Error Surfacing and Recovery Testing:**
```python
@pytest.mark.asyncio
async def test_error_state_handling():
    """Test error states are properly surfaced and recoverable"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        # Test API failure handling
        with patch('src.core.ResponseGenerator.generate_response') as mock_gen:
            mock_gen.side_effect = ConnectionError("API unavailable")
            
            prompt_input = app.query_one("#prompt-input")
            await pilot.focus(prompt_input)
            await pilot.type("test api failure")
            await pilot.press("enter")
            
            await pilot.pause(1.0)
            
            # Verify error appears in Sacred Timeline
            sacred_timeline = app.query_one("#sacred-timeline")
            blocks = app.unified_async_processor.get_timeline().get_all_blocks()
            error_blocks = [b for b in blocks if "error" in b.content.lower()]
            assert len(error_blocks) > 0
            
            # Verify Live Workspace is hidden after error
            live_workspace = app.query_one("#live-workspace")
            assert not live_workspace.is_visible
            
            # Verify app remains responsive
            await pilot.type("recovery test")
            await pilot.press("enter")
            # Should not crash

@pytest.mark.asyncio
async def test_empty_and_loading_states():
    """Test empty states and loading behavior"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        # Test initial empty state
        sacred_timeline = app.query_one("#sacred-timeline")
        live_workspace = app.query_one("#live-workspace")
        
        # Should show welcome message only
        blocks = app.unified_async_processor.get_timeline().get_all_blocks()
        assert len(blocks) >= 1  # Welcome message
        
        # Workspace should be hidden
        assert not live_workspace.is_visible
        
        # Test loading state during processing
        with patch('src.core.unified_async_processor.UnifiedAsyncProcessor.process_user_input_async') as mock_process:
            # Simulate slow processing
            async def slow_process(text):
                await asyncio.sleep(2.0)
                return "Slow response"
            
            mock_process.side_effect = slow_process
            
            prompt_input = app.query_one("#prompt-input")
            await pilot.focus(prompt_input)
            await pilot.type("slow processing test")
            await pilot.press("enter")
            
            # Immediately check loading state
            await pilot.pause(0.1)
            
            # Workspace should be visible during processing
            assert live_workspace.is_visible
            
            # Wait for completion
            await pilot.pause(2.5)
            
            # Workspace should hide after completion
            assert not live_workspace.is_visible
```

## 5. Tooling and Frameworks for User Experience Testing

### a. Textual-Specific Testing Tools

| Tool/Framework                  | Purpose & Features                                                                                           |
|---------------------------------|-------------------------------------------------------------------------------------------------------------|
| **Textual's `run_test()` & Pilot** | Headless testing; simulate keypresses, clicks, typing, and scrolls; query widget state after actions   |
| **pytest + pytest-asyncio**     | Write async tests for event-driven, streaming, or incremental UI updates                                   |
| **pytest-textual-snapshot**     | Snapshot testing for Textual apps; generates SVGs of UI for visual regression detection                    |
| **Textual Devtools**            | Interactive inspection, widget tree visualization, and live debugging during test development              |
| **Rich Assertions**              | Use Rich's rendering capabilities for asserting on rich text output and UI state                          |

### b. Sacred Architecture Testing Tools

**Custom Test Fixtures for Sacred Architecture:**
```python
@pytest.fixture
def sacred_app_with_mocks():
    """Provide LLMReplApp with all external services mocked"""
    with patch('src.core.ResponseGenerator') as mock_gen, \
         patch('src.core.unified_async_processor.UnifiedAsyncProcessor') as mock_proc:
        
        mock_gen.return_value.generate_response.return_value = "Mocked response"
        app = LLMReplApp()
        yield app, mock_gen, mock_proc

@pytest.fixture  
def clean_timeline():
    """Provide fresh UnifiedTimeline for each test"""
    timeline = UnifiedTimeline()
    yield timeline
    timeline.clear_timeline()
```

### c. Advanced UX Testing Tools

| Tool/Framework          | Best For                                                 | Sacred Architecture Use Case           |
|------------------------|----------------------------------------------------------|------------------------------------|
| **Visual Regression**   | pytest-textual-snapshot for SVG UI comparison           | Detect layout/styling regressions |
| **Accessibility**      | Custom keyboard navigation and focus testing            | Verify Sacred Architecture accessibility |
| **Performance**        | Memory and CPU profiling during streaming               | Test workspace transitions        |
| **Load Testing**       | Rapid input simulation and stress testing               | Validate input handling           |

## 6. Advanced Testing Techniques for User Experience

### a. Snapshot and Visual Regression Testing

**Sacred Architecture Snapshot Testing:**
```python
@pytest.mark.asyncio
async def test_sacred_timeline_visual_regression():
    """Snapshot test for Sacred Timeline layout"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        # Add known content for consistent snapshots
        sacred_timeline = app.query_one("#sacred-timeline")
        
        # Add test blocks
        test_blocks = [
            InscribedBlock(id="snap-1", role="user", content="Test user message", metadata={}),
            InscribedBlock(id="snap-2", role="assistant", content="Test assistant response", metadata={}),
            InscribedBlock(id="snap-3", role="system", content="Test system message", metadata={})
        ]
        
        for block in test_blocks:
            await sacred_timeline.add_block(block)
        
        # Generate snapshot
        await pilot.pause(0.5)  # Allow rendering to complete
        
        # Compare with saved snapshot
        rendered_svg = app.export_svg()
        assert_snapshot_matches(rendered_svg, "sacred_timeline_baseline.svg")

def assert_snapshot_matches(actual_svg: str, baseline_file: str):
    """Custom snapshot comparison with Sacred Architecture awareness"""
    baseline_path = Path("tests/snapshots") / baseline_file
    
    if not baseline_path.exists():
        # First run - save baseline
        baseline_path.parent.mkdir(parents=True, exist_ok=True)
        baseline_path.write_text(actual_svg)
        pytest.skip("Baseline snapshot created")
    
    baseline_svg = baseline_path.read_text()
    
    # Compare with tolerance for minor rendering differences
    assert normalize_svg(actual_svg) == normalize_svg(baseline_svg)

def normalize_svg(svg_content: str) -> str:
    """Normalize SVG content for consistent comparison"""
    # Remove timestamp-specific elements, normalize spacing, etc.
    import re
    normalized = re.sub(r'timestamp="[^"]*"', '', svg_content)
    normalized = re.sub(r'\s+', ' ', normalized)
    return normalized.strip()
```

### b. Workflow and Journey Testing

**Complete User Journey Testing:**
```python
@pytest.mark.asyncio
async def test_complete_user_journey():
    """Test full user workflow through Sacred Architecture"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        # Journey: Start -> Input -> Cognition -> Response -> Recovery from Error
        
        # 1. Initial state verification
        sacred_timeline = app.query_one("#sacred-timeline")
        live_workspace = app.query_one("#live-workspace")
        prompt_input = app.query_one("#prompt-input")
        
        assert not live_workspace.is_visible  # 2-way split
        assert prompt_input.has_focus
        
        # 2. User inputs query
        test_query = "Explain quantum computing"
        await pilot.type(test_query)
        await pilot.press("enter")
        
        # 3. Verify cognition workflow begins
        await pilot.pause(0.2)
        assert live_workspace.is_visible  # 3-way split
        assert prompt_input.text == ""    # Input cleared
        
        # 4. Simulate cognition sub-modules
        sub_modules = [
            ("route_query", "Routing to science explanation..."),
            ("call_tool", "Accessing quantum computing knowledge..."),
            ("format_output", "Formatting comprehensive response...")
        ]
        
        for role, content in sub_modules:
            sub_module = LiveBlock(
                id=f"journey-{role}",
                role=role,
                data=LiveBlockData(content=content, sub_blocks=[], metadata={})
            )
            await live_workspace.add_sub_module(sub_module)
            await pilot.pause(0.1)
            
            # Verify sub-module appears
            assert live_workspace.get_sub_module_count() > 0
        
        # 5. Complete cognition and add final response
        final_response = "Quantum computing uses quantum mechanical phenomena..."
        response_block = InscribedBlock(
            id="journey-response",
            role="assistant",
            content=final_response,
            metadata={"sub_modules": len(sub_modules)}
        )
        await sacred_timeline.add_block(response_block)
        
        # 6. Verify workflow completion
        live_workspace.clear_workspace()  # Simulate turn completion
        await pilot.pause(0.1)
        
        assert not live_workspace.is_visible  # Back to 2-way split
        assert sacred_timeline.get_block_count() >= 2  # User + Assistant blocks
        
        # 7. Test error recovery
        await pilot.type("trigger error test")
        
        with patch('src.core.unified_async_processor.UnifiedAsyncProcessor.process_user_input_async') as mock_proc:
            mock_proc.side_effect = Exception("Simulated API error")
            await pilot.press("enter")
            await pilot.pause(0.5)
            
            # Verify error handling
            blocks = app.unified_async_processor.get_timeline().get_all_blocks()
            error_blocks = [b for b in blocks if "error" in b.content.lower()]
            assert len(error_blocks) > 0
            
            # Verify app remains responsive
            await pilot.type("recovery successful")
            await pilot.press("enter")
            # Should not crash - successful recovery
```

### c. Performance and Load Testing

**Sacred Architecture Performance Testing:**
```python
@pytest.mark.asyncio
async def test_performance_under_load():
    """Test Sacred Architecture performance with heavy content"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        sacred_timeline = app.query_one("#sacred-timeline")
        live_workspace = app.query_one("#live-workspace")
        
        # Performance baseline
        import time
        import psutil
        
        start_memory = psutil.Process().memory_info().rss
        start_time = time.time()
        
        # Load test: Add many blocks rapidly
        for i in range(100):
            block = InscribedBlock(
                id=f"perf-test-{i}",
                role="user" if i % 2 == 0 else "assistant",
                content=f"Performance test message {i} with substantial content to test memory usage and rendering performance under load conditions.",
                metadata={"test_index": i}
            )
            await sacred_timeline.add_block(block)
            
            # Every 10 blocks, check performance
            if i % 10 == 0:
                await pilot.pause(0.01)  # Allow UI update
                
                current_memory = psutil.Process().memory_info().rss
                memory_increase = current_memory - start_memory
                
                # Memory should not increase excessively
                assert memory_increase < 50 * 1024 * 1024  # 50MB limit
        
        # Test workspace performance with many sub-modules
        live_workspace.show_workspace()
        
        for i in range(50):
            sub_module = LiveBlock(
                id=f"perf-sub-{i}",
                role="call_tool",
                data=LiveBlockData(
                    content=f"Performance sub-module {i} testing memory and rendering efficiency",
                    sub_blocks=[],
                    metadata={"perf_test": True}
                )
            )
            await live_workspace.add_sub_module(sub_module)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Performance assertions
        assert total_time < 5.0  # Should complete within 5 seconds
        assert sacred_timeline.get_block_count() == 100
        assert live_workspace.get_sub_module_count() == 50
        
        # Verify UI remains responsive
        prompt_input = app.query_one("#prompt-input")
        await pilot.focus(prompt_input)
        await pilot.type("responsiveness test")
        assert prompt_input.text == "responsiveness test"

@pytest.mark.asyncio 
async def test_rapid_input_handling():
    """Test rapid user input without UI corruption"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        prompt_input = app.query_one("#prompt-input")
        await pilot.focus(prompt_input)
        
        # Rapid input test
        rapid_inputs = [
            "rapid input test 1",
            "rapid input test 2", 
            "rapid input test 3"
        ]
        
        for text in rapid_inputs:
            await pilot.type(text)
            await pilot.press("enter")
            # No pause - stress test
        
        # Verify all inputs were processed
        await pilot.pause(1.0)  # Allow processing to complete
        
        blocks = app.unified_async_processor.get_timeline().get_all_blocks()
        user_blocks = [b for b in blocks if b.role == "user"]
        
        # Should have at least the rapid inputs (plus welcome message)
        assert len(user_blocks) >= len(rapid_inputs)
```

## 7. Best Practices Table for User Experience Testing

| Practice                        | Implementation in Sacred Architecture Testing                                     |
|----------------------------------|-----------------------------------------------------------------------------|
| **Simulate real user workflows** | Use Pilot to automate keypresses, clicks, and typing through complete journeys |
| **Assert on visible outcomes**   | Query widgets and assert on text, styles, visibility, and Sacred Architecture state |
| **Test dynamic/streaming updates** | Incrementally update widgets and assert on intermediate states and visual feedback |
| **Snapshot visual output**       | Use pytest-textual-snapshot for SVG-based regression testing                    |
| **Validate accessibility**       | Automate keyboard navigation and focus assertions across Sacred Architecture    |
| **Surface and handle errors**    | Simulate failures, assert error banners/overlays are shown in Sacred Timeline  |
| **Test edge cases**              | Rapid input, resizing, empty/loading/error states, workspace transitions       |
| **Performance testing**          | Memory profiling, load testing, responsiveness validation                      |
| **Layout consistency**           | Verify Sacred Architecture prevents nested containers and layout conflicts     |
| **Workflow reliability**         | Test complete user journeys from input through cognition to response           |
| **Visual regression detection**   | Compare rendered output against baselines to catch subtle UI changes           |
| **Integrate into CI**            | Run all tests and collect reports on every commit                              |

## 5. Testing Dynamic Content and Streaming

### Streaming Updates

Simulate streaming by sending content chunks and asserting that the UI updates incrementally.

**Example:**
```python
@pytest.mark.asyncio
async def test_streaming_message_bubble():
    app = MyTextualApp()
    async with app.run_test() as pilot:
        bubble = app.query_one("#streaming_bubble")
        await bubble.append_content("Hello")
        assert bubble.text == "Hello"
        await bubble.append_content(", world!")
        assert bubble.text == "Hello, world!"
```

**Sacred Architecture Streaming Tests:**
```python
@pytest.mark.asyncio
async def test_sub_module_streaming():
    """Test streaming updates in Live Workspace sub-modules"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        live_workspace = app.query_one("#live-workspace")
        
        # Create streaming sub-module
        sub_module = LiveBlock(
            id="stream-test",
            role="route_query",
            data=LiveBlockData(content="", sub_blocks=[], metadata={})
        )
        
        await live_workspace.add_sub_module(sub_module)
        
        # Simulate streaming content
        sub_module.update_content("Processing")
        await pilot.pause(0.1)
        
        sub_module.append_content("... analyzing query")
        await pilot.pause(0.1)
        
        sub_module.append_content("... complete")
        await pilot.pause(0.1)
        
        # Verify final content
        widget = live_workspace.sub_module_widgets[sub_module.id]
        assert "Processing... analyzing query... complete" in widget.sub_module.data.content
```

### Scroll Position Testing

Test that new messages auto-scroll only if the user is at the bottom.

**Example:**
```python
@pytest.mark.asyncio
async def test_scroll_behavior():
    app = MyTextualApp()
    async with app.run_test() as pilot:
        message_list = app.query_one("#message_list")
        # Simulate user scroll up
        await pilot.scroll(message_list, lines=-10)
        # Add new message
        await app.add_message("New message")
        # Assert scroll position unchanged
        assert not message_list.at_bottom
```

**Sacred Architecture Scroll Tests:**
```python
@pytest.mark.asyncio
async def test_sacred_timeline_smart_scroll():
    """Test Sacred Timeline smart auto-scroll behavior"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        sacred_timeline = app.query_one("#sacred-timeline")
        
        # Add multiple blocks to fill timeline
        for i in range(10):
            block = InscribedBlock(
                id=f"test-{i}",
                role="user",
                content=f"Message {i}",
                metadata={}
            )
            await sacred_timeline.add_block(block)
        
        # Scroll up (user reading history)
        await pilot.scroll(sacred_timeline, lines=-5)
        assert not sacred_timeline.user_is_following
        
        # Add new block - should not auto-scroll
        new_block = InscribedBlock(
            id="test-new",
            role="assistant", 
            content="New response",
            metadata={}
        )
        await sacred_timeline.add_block(new_block)
        
        # User should still be scrolled up
        assert not sacred_timeline.user_is_following
        
        # Scroll back to bottom
        sacred_timeline.scroll_end()
        await pilot.pause(0.1)
        assert sacred_timeline.user_is_following
```

## 6. Error Handling and Surfacing

### Fail-Fast Testing

Widgets and services should assert expected states and raise/log errors immediately.

**Example:**
```python
@pytest.mark.asyncio
async def test_error_boundary():
    app = MyTextualApp()
    async with app.run_test() as pilot:
        # Simulate error in widget
        await app.simulate_widget_error()
        error_banner = app.query_one("#notification_banner")
        assert "Error" in error_banner.text
```

**Sacred Architecture Error Tests:**
```python
@pytest.mark.asyncio
async def test_invalid_block_data_handling():
    """Test that invalid block data raises clear errors"""
    timeline = UnifiedTimeline()
    
    # Test invalid role
    with pytest.raises(ValueError, match="Invalid role"):
        timeline.add_live_block("invalid_role", "content")
    
    # Test empty content
    with pytest.raises(ValueError, match="Content must be non-empty"):
        timeline.add_live_block("user", "")
    
    # Test None content
    with pytest.raises(ValueError, match="Content must be non-empty"):
        timeline.add_live_block("user", None)

@pytest.mark.asyncio
async def test_css_validation_errors():
    """Test that CSS property validation catches errors early"""
    app = LLMReplApp()
    
    # This should be caught during app initialization
    with pytest.raises(StylesheetParseError):
        # Simulate invalid CSS property
        test_css = ".test { border-color: blue; }"  # Invalid for Textual
        app._apply_test_css(test_css)

@pytest.mark.asyncio
async def test_nested_container_prevention():
    """Test prevention of nested container layout conflicts"""
    # This should be enforced by widget design
    sacred_timeline = SacredTimelineWidget()
    
    # Attempting to add nested Vertical should be prevented
    with pytest.raises(ValueError, match="Nested containers not allowed"):
        nested_vertical = Vertical()
        sacred_timeline._validate_child_widget(nested_vertical)
```

## 7. Advanced Testing Scenarios

### Layout Conflict Detection

**Sacred Architecture Layout Tests:**
```python
@pytest.mark.asyncio
async def test_no_nested_containers():
    """Verify Sacred Architecture prevents nested container conflicts"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        sacred_timeline = app.query_one("#sacred-timeline")
        live_workspace = app.query_one("#live-workspace")
        
        # Verify both are VerticalScroll widgets
        assert isinstance(sacred_timeline, VerticalScroll)
        assert isinstance(live_workspace, VerticalScroll)
        
        # Add blocks and verify children are simple widgets
        test_block = InscribedBlock(
            id="layout-test",
            role="user",
            content="Layout test",
            metadata={}
        )
        await sacred_timeline.add_block(test_block)
        
        # Verify children are simple widgets, not containers
        for child in sacred_timeline.children:
            assert not isinstance(child, (Vertical, Horizontal, VerticalScroll))
            assert hasattr(child, 'render')  # Should use render() pattern

@pytest.mark.asyncio
async def test_workspace_show_hide_transitions():
    """Test 2-way ↔ 3-way split transitions"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        live_workspace = app.query_one("#live-workspace")
        
        # Should start hidden (2-way split)
        assert not live_workspace.is_visible
        assert live_workspace.has_class("hidden")
        
        # Show workspace (3-way split)
        live_workspace.show_workspace()
        await pilot.pause(0.1)
        
        assert live_workspace.is_visible
        assert not live_workspace.has_class("hidden")
        
        # Hide workspace (back to 2-way split)
        live_workspace.hide_workspace()
        await pilot.pause(0.1)
        
        assert not live_workspace.is_visible
        assert live_workspace.has_class("hidden")
```

### Snapshot Testing

Capture and compare rendered output to detect regressions.

```python
@pytest.mark.asyncio
async def test_welcome_message_snapshot():
    """Snapshot test for welcome message display"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        await pilot.pause(1.0)  # Wait for welcome message
        
        sacred_timeline = app.query_one("#sacred-timeline")
        rendered_output = sacred_timeline._render()
        
        # Compare with saved snapshot
        expected_snapshot = load_snapshot("welcome_message.snapshot")
        assert_snapshot_match(rendered_output, expected_snapshot)
```

### Accessibility Testing

Simulate keyboard navigation and assert focus changes.

```python
@pytest.mark.asyncio
async def test_keyboard_navigation():
    """Test keyboard accessibility in Sacred Architecture"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        # Start with focus on prompt input
        prompt_input = app.query_one("#prompt-input")
        assert prompt_input.has_focus
        
        # Tab navigation should work
        await pilot.press("tab")
        # Focus should move to next focusable widget
        
        # Arrow keys should work in scrollable areas
        sacred_timeline = app.query_one("#sacred-timeline")
        await pilot.focus(sacred_timeline)
        await pilot.press("up", "down")
        # Should scroll timeline content
```

## 8. Example Directory Structure

```
tests/
├── test_widgets/
│   ├── test_sacred_timeline.py      # Sacred Timeline widget tests
│   ├── test_live_workspace.py       # Live Workspace widget tests  
│   ├── test_simple_block.py         # Simple Block widget tests
│   ├── test_sub_module.py           # Sub-module widget tests
│   └── test_prompt_input.py         # Prompt Input widget tests
├── test_services/
│   ├── test_unified_timeline.py     # Timeline service tests
│   ├── test_async_processor.py      # Async processor tests
│   └── test_response_generator.py   # Response generator tests
├── test_integration/
│   ├── test_user_flows.py           # End-to-end user workflows
│   ├── test_workspace_transitions.py # 2-way ↔ 3-way split tests
│   └── test_error_scenarios.py     # Error handling integration
├── harnesses/
│   ├── streaming_harness.py        # Streaming simulation tools
│   ├── error_injection.py          # Error scenario generators
│   └── layout_validator.py         # Layout conflict detection
├── fixtures/
│   ├── test_blocks.py               # Test data fixtures
│   ├── mock_services.py             # Service mocks
│   └── snapshots/                   # Snapshot test data
└── conftest.py                      # Pytest configuration
```

## 9. Continuous Integration

Run all tests in CI pipelines with Sacred Architecture validation:

```yaml
# .github/workflows/test.yml
name: Sacred Architecture Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install pdm
          pdm install
      
      - name: Run unit tests
        run: pdm run pytest tests/test_widgets/ tests/test_services/ -v
      
      - name: Run integration tests
        run: pdm run pytest tests/test_integration/ -v
      
      - name: Run layout validation
        run: pdm run pytest tests/harnesses/test_layout_validator.py -v
      
      - name: Run linting
        run: pdm run just lint
      
      - name: Generate coverage report
        run: pdm run pytest --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## 10. Sacred Architecture Testing Checklist

- [ ] **Layout Conflicts:** No nested containers in VerticalScroll widgets
- [ ] **CSS Validation:** All CSS properties are valid for Textual
- [ ] **Widget Isolation:** Each widget is independently testable
- [ ] **State Management:** UnifiedTimeline singleton behavior validated
- [ ] **Event Flow:** User input → processing → display flow tested
- [ ] **Workspace Transitions:** 2-way ↔ 3-way split behavior verified
- [ ] **Streaming Content:** Live updates and scroll management tested
- [ ] **Error Boundaries:** Graceful error handling without crashes
- [ ] **Type Safety:** All interfaces validated with proper type hints
- [ ] **Performance:** No memory leaks or excessive resource usage

## 11. Key Takeaways for Advanced User Experience Testing

**Core UX Testing Principles:**
- **Simulate Real User Interactions:** Test as users actually behave—typing, clicking, navigating, and observing visual feedback
- **Go Beyond Logic Testing:** Validate visual updates, accessibility, workflow reliability, and error recovery
- **Test Complete Journeys:** Verify entire user workflows from input through cognition processing to final response
- **Assert on Visible Outcomes:** Test what users see and experience, not just internal state changes

**Sacred Architecture UX Validation:**
- **Workspace Transitions:** Test 2-way ↔ 3-way split behavior and visual feedback during cognition
- **Layout Consistency:** Verify Sacred Architecture prevents nested containers and maintains V3 patterns
- **Streaming Content:** Validate real-time updates in Live Workspace and Sacred Timeline
- **Error Recovery:** Ensure graceful error handling without breaking Sacred Architecture integrity

**Advanced Testing Techniques:**
- **Visual Regression:** Use snapshot testing to catch subtle layout and styling changes
- **Performance Testing:** Validate memory usage, rendering speed, and responsiveness under load
- **Accessibility Compliance:** Test keyboard navigation, focus indicators, and screen reader compatibility  
- **Stress Testing:** Verify app stability with rapid input, heavy content, and edge conditions

**Textual-Specific Best Practices:**
- **Use Textual's Test API:** Leverage `run_test()` and `Pilot` for comprehensive user interaction simulation
- **Async Test Support:** Handle streaming and dynamic updates with pytest-asyncio for realistic testing
- **Widget Querying:** Use `app.query_one()` and CSS selectors for precise component validation
- **Event Simulation:** Test keypresses, clicks, scrolling, and focus changes as users would perform them

**Quality Assurance Integration:**
- **CI/CD Integration:** Run comprehensive UX tests on every commit with performance baselines
- **Snapshot Baselines:** Maintain visual regression protection with SVG comparison testing
- **Error Boundary Validation:** Ensure fail-fast behavior surfaces issues without app crashes
- **Cross-Platform Testing:** Validate UX consistency across different terminal environments

By implementing these advanced user experience testing strategies specifically tailored to Textual and our Sacred GUI Architecture, you ensure that your application not only functions correctly but delivers a seamless, reliable, and delightful user experience that maintains the proven V3 patterns throughout its development lifecycle.

---

**References:** This guide synthesizes advanced UX testing practices from the Textual testing framework, GUI testing methodologies, and Sacred Architecture validation requirements. For framework-specific details, consult the [Textual Testing Documentation](https://textual.textualize.io/guide/testing/) and [Textual Devtools](https://textual.textualize.io/guide/devtools/).