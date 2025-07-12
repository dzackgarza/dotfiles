# Testing Guide

> **Test Against Working Patterns**: Validate that our implementations work like V3's proven patterns. Test behavior, not just compilation.

## Testing Philosophy

### Sacred Architecture Testing Principles

```
┌─ Sacred Architecture Testing Rules ──────────────────────┐
│                                                           │
│  🏆 V3 Pattern Validation: Does it work like V3?         │
│  🔍 Reference Behavior Testing: Match working examples   │
│  📐 Layout Conflict Prevention: No nested containers     │
│  ⚡ Streaming Simulation: Test dynamic content updates   │
│  🛡️ Error Boundary Testing: Graceful failure handling    │
│  📏 Responsive Behavior: Dynamic resizing validation     │
│  🔄 State Transition Testing: 2-way ↔ 3-way splits      │
│  🧵 Thread Safety: Concurrent update validation         │
│  📊 Performance Testing: High content volume handling    │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### Testing Categories

1. **V3 Pattern Compliance** - Ensure our widgets work like V3's
2. **Sacred Architecture Validation** - Test layout rules and state transitions  
3. **Streaming Simulation** - Test real-time content updates
4. **Error Boundary Testing** - Validate graceful failure handling
5. **Integration Testing** - Full user interaction flows

## V3 Pattern Compliance Tests

### Test Widget Patterns Match V3

```python
@pytest.mark.asyncio
async def test_sacred_timeline_follows_v3_pattern():
    """Verify Sacred Timeline uses V3's chat_container pattern"""
    
    # Test V3's VerticalScroll pattern
    timeline = SacredTimelineWidget()
    assert isinstance(timeline, VerticalScroll)
    
    # Test V3's simple widget children (no nesting)
    test_block = InscribedBlock("user", "Test content")
    await timeline.add_block(test_block)
    
    # Verify no nested containers (V3's golden rule)
    for child in timeline.children:
        assert not isinstance(child, (Vertical, VerticalScroll))
        assert hasattr(child, 'render')  # V3 render pattern
    
    # Test V3's auto-scroll behavior
    initial_scroll = timeline.scroll_y
    await timeline.add_block(InscribedBlock("assistant", "Response"))
    assert timeline.scroll_y >= initial_scroll  # Scrolled to new content

@pytest.mark.asyncio  
async def test_simple_block_follows_v3_chatbox_pattern():
    """Verify SimpleBlockWidget uses V3's Chatbox pattern"""
    
    block_data = InscribedBlock("user", "Test message")
    widget = SimpleBlockWidget(block_data)
    
    # Test V3's render() pattern (no child widgets)
    assert hasattr(widget, 'render')
    assert not hasattr(widget, 'compose')  # No child widgets
    
    # Test V3's fail-fast validation
    with pytest.raises(ValueError, match="Invalid block data"):
        SimpleBlockWidget(None)
    
    # Test V3's Panel-based rendering
    rendered = widget.render()
    assert isinstance(rendered, Panel)
    assert "Test message" in str(rendered)
```

### Test Thread-Safe Patterns (V3's call_from_thread)

```python
@pytest.mark.asyncio
async def test_v3_thread_safe_updates():
    """Test V3's call_from_thread pattern works"""
    
    app = LLMReplApp()
    async with app.run_test() as pilot:
        workspace = app.query_one("#live-workspace")
        
        # Simulate V3's background thread update
        import asyncio
        import threading
        
        def background_update():
            """Simulate worker thread adding content"""
            sub_module = SubModuleWidget("route_query", "tinyllama")
            
            # V3's thread-safe update pattern
            app.call_from_thread(workspace.mount, sub_module)
        
        # Run in background thread (like V3's workers)
        thread = threading.Thread(target=background_update)
        thread.start()
        thread.join()
        
        # Verify update worked
        await pilot.pause(0.1)  # Allow UI update
        assert len(workspace.children) > 0
```

## Sacred Architecture Validation Tests

### Layout Conflict Prevention

```python
def test_no_nested_containers():
    """Ensure Sacred Architecture prevents layout conflicts"""
    
    app = LLMReplApp()
    
    # Check Sacred Timeline compliance
    sacred_timeline = app.query_one("#sacred-timeline")
    assert isinstance(sacred_timeline, VerticalScroll)
    
    # Validate no nested containers anywhere
    def check_no_nesting(widget):
        for child in widget.children:
            if isinstance(widget, VerticalScroll):
                # VerticalScroll should only contain simple widgets
                assert not isinstance(child, (Vertical, VerticalScroll))
                assert hasattr(child, 'render')
            check_no_nesting(child)
    
    check_no_nesting(app)

def test_css_property_validation():
    """Ensure only valid Textual CSS properties are used"""
    
    # Read all CSS files
    css_files = glob.glob("src/**/*.tcss", recursive=True)
    
    forbidden_properties = [
        "border-color",      # Use: border: solid color
        "background-color",  # Use: background: color
        "font-family",       # Not supported in Textual
        "box-shadow",        # Not supported in Textual
    ]
    
    for css_file in css_files:
        with open(css_file) as f:
            content = f.read()
            
        for forbidden in forbidden_properties:
            assert forbidden not in content, f"Invalid CSS property '{forbidden}' in {css_file}"
```

### State Transition Testing

```python
@pytest.mark.asyncio
async def test_workspace_state_transitions():
    """Test 2-way ↔ 3-way split behavior"""
    
    app = LLMReplApp()
    async with app.run_test() as pilot:
        workspace = app.query_one("#live-workspace")
        timeline = app.query_one("#sacred-timeline")
        
        # Initial state: 2-way split (workspace hidden)
        assert workspace.has_class("hidden")
        assert not workspace.is_visible
        
        # Simulate user input → 3-way split
        await app.workspace_controller.start_turn("Test question")
        
        # Verify 3-way split (workspace visible)
        assert not workspace.has_class("hidden")
        assert workspace.is_visible
        
        # Simulate completion → 2-way split
        await app.workspace_controller.complete_turn("Test response")
        
        # Verify back to 2-way split
        assert workspace.has_class("hidden")
        assert not workspace.is_visible
        
        # Verify content moved to Sacred Timeline
        blocks = timeline.query(".simple-block")
        assert len(blocks) >= 2  # User + Assistant blocks

@pytest.mark.asyncio
async def test_sacred_timeline_immutability():
    """Test Sacred Timeline append-only behavior"""
    
    timeline = SacredTimelineWidget()
    
    # Add initial blocks
    block1 = InscribedBlock("user", "First message")
    block2 = InscribedBlock("assistant", "First response")
    
    await timeline.add_block(block1)
    await timeline.add_block(block2)
    
    initial_count = len(timeline.children)
    
    # Verify blocks cannot be modified
    with pytest.raises(AttributeError):
        block1.content = "Modified content"  # Should be immutable
    
    # Verify blocks cannot be removed
    timeline_blocks = timeline.inscribed_blocks.copy()
    assert len(timeline_blocks) == initial_count
    
    # New blocks only append
    block3 = InscribedBlock("user", "Second message")
    await timeline.add_block(block3)
    
    assert len(timeline.children) == initial_count + 1
```

## Streaming Simulation Tests

### Real-Time Content Updates

```python
class StreamingTestHarness:
    """Simulate streaming content for widget testing"""
    
    async def simulate_cognition_pipeline(self, workspace, steps):
        """Test full cognition pipeline streaming"""
        
        for i, step in enumerate(steps):
            # Add sub-module
            sub_module = SubModuleWidget(step["name"], step["model"])
            workspace.mount(sub_module)
            
            # Simulate streaming content
            for chunk in step["content_chunks"]:
                sub_module.update_content(chunk)
                await asyncio.sleep(0.05)  # Simulate network delay
            
            # Mark complete
            sub_module.mark_complete()
            
            # Verify state
            assert sub_module.status == "completed"
            assert step["expected_content"] in sub_module.content_buffer
    
    async def simulate_error_during_stream(self, widget, error_at_chunk):
        """Test error handling mid-stream"""
        
        content_chunks = ["Hello", " ", "World", "!"]
        
        for i, chunk in enumerate(content_chunks):
            if i == error_at_chunk:
                widget.handle_error(StreamingError("Network timeout"))
                break
            widget.update_content(chunk)
        
        # Verify error state
        assert widget.current_state == "error"
        assert "Network timeout" in widget.error_message
    
    async def simulate_high_volume_streaming(self, widget, chunk_count=1000):
        """Test performance with high volume content"""
        
        start_time = time.time()
        
        for i in range(chunk_count):
            widget.update_content(f"Chunk {i}\n")
            
            # Occasional pause to simulate real streaming
            if i % 50 == 0:
                await asyncio.sleep(0.01)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Verify performance acceptable
        assert duration < 5.0  # Should handle 1000 chunks in < 5 seconds
        assert len(widget.content_buffer.split('\n')) >= chunk_count

@pytest.mark.asyncio
async def test_streaming_content_simulation():
    """Test streaming content using harness"""
    
    harness = StreamingTestHarness()
    workspace = LiveWorkspaceWidget()
    
    cognition_steps = [
        {
            "name": "route_query",
            "model": "tinyllama", 
            "content_chunks": ["Routing", " query", " to math"],
            "expected_content": "Routing query to math"
        },
        {
            "name": "solve_math",
            "model": "deepseek",
            "content_chunks": ["Calculating", " 2+2", " = 4"],
            "expected_content": "Calculating 2+2 = 4"
        }
    ]
    
    await harness.simulate_cognition_pipeline(workspace, cognition_steps)
    
    # Verify all sub-modules completed
    assert len(workspace.children) == 2
    for child in workspace.children:
        assert child.status == "completed"
```

### Smart Auto-Scroll Testing

```python
@pytest.mark.asyncio
async def test_smart_auto_scroll_behavior():
    """Test V3's smart auto-scroll pattern"""
    
    timeline = SacredTimelineWidget()
    
    # Fill with content to enable scrolling
    for i in range(20):
        block = InscribedBlock("user", f"Message {i}")
        await timeline.add_block(block)
    
    # User at bottom → should auto-scroll
    timeline.scroll_end()
    assert timeline.scroll_y >= timeline.max_scroll_y - 1
    
    new_block = InscribedBlock("assistant", "New response")
    await timeline.add_block(new_block)
    
    # Should still be at bottom (auto-scrolled)
    assert timeline.scroll_y >= timeline.max_scroll_y - 1
    
    # User scrolls up → should NOT auto-scroll
    timeline.scroll_to_y(timeline.max_scroll_y // 2)
    middle_position = timeline.scroll_y
    
    another_block = InscribedBlock("user", "Another message")
    await timeline.add_block(another_block)
    
    # Should maintain scroll position (didn't auto-scroll)
    assert abs(timeline.scroll_y - middle_position) < 2
```

## Error Boundary Testing

### Graceful Failure Handling

```python
@pytest.mark.asyncio
async def test_error_boundary_widget():
    """Test ErrorBoundaryWidget handles failures gracefully"""
    
    class FailingWidget(Widget):
        def render(self):
            raise ValueError("Intentional test failure")
    
    # Create error boundary wrapper
    safe_widget = ErrorBoundaryWidget(FailingWidget)
    
    # Should not crash app
    rendered = safe_widget.render()
    assert isinstance(rendered, Panel)
    assert "Error: Intentional test failure" in str(rendered)
    assert "red" in str(rendered)  # Error styling

@pytest.mark.asyncio
async def test_app_resilience_to_widget_errors():
    """Test app continues working despite widget errors"""
    
    app = LLMReplApp()
    async with app.run_test() as pilot:
        timeline = app.query_one("#sacred-timeline")
        
        # Add normal block
        good_block = InscribedBlock("user", "Normal message")
        await timeline.add_block(good_block)
        
        # Add failing block with error boundary
        class FailingBlockWidget(SimpleBlockWidget):
            def render(self):
                raise RuntimeError("Widget render failed")
        
        failing_block = ErrorBoundaryWidget(
            FailingBlockWidget, 
            InscribedBlock("assistant", "Broken response")
        )
        timeline.mount(failing_block)
        
        # App should still be responsive
        await pilot.pause(0.1)
        assert app.is_running
        
        # Should be able to add more blocks
        another_block = InscribedBlock("user", "After error")
        await timeline.add_block(another_block)
        
        assert len(timeline.children) >= 3

def test_validation_error_handling():
    """Test widget validation catches errors early"""
    
    # Test SimpleBlockWidget validation
    with pytest.raises(ValueError, match="Invalid block data"):
        SimpleBlockWidget(None)
    
    with pytest.raises(ValueError, match="Missing required field"):
        SimpleBlockWidget({"invalid": "data"})
    
    # Valid data should work
    valid_block = InscribedBlock("user", "Valid content")
    widget = SimpleBlockWidget(valid_block)
    assert widget.data == valid_block
```

## Integration Testing

### Full User Interaction Flows

```python
@pytest.mark.asyncio
async def test_complete_user_interaction_flow():
    """Test full user input → response cycle"""
    
    app = LLMReplApp()
    
    async with app.run_test() as pilot:
        # Validate initial state (2-way split)
        sacred_timeline = app.query_one("#sacred-timeline")
        live_workspace = app.query_one("#live-workspace") 
        prompt_input = app.query_one("#prompt-input")
        
        assert sacred_timeline.is_visible
        assert not live_workspace.is_visible  # Hidden initially
        assert prompt_input.is_visible
        
        # Simulate user input
        await pilot.click("#prompt-input")
        await pilot.type("Tell me about quantum computing")
        await pilot.press("enter")
        
        # Validate workspace activation (3-way split)
        await pilot.pause(0.1)  # Allow state transition
        assert live_workspace.is_visible  # Now visible
        
        # Validate processing flow
        submodules = live_workspace.query(".sub-module")
        assert len(submodules) > 0
        
        # Wait for completion
        await pilot.wait_until(
            lambda: not live_workspace.is_visible,  # Back to 2-way
            timeout=30.0
        )
        
        # Validate final state
        blocks = sacred_timeline.query(".simple-block")
        assert len(blocks) >= 2  # User + Assistant blocks

@pytest.mark.asyncio
async def test_multiple_turn_conversation():
    """Test multi-turn conversation flow"""
    
    app = LLMReplApp()
    async with app.run_test() as pilot:
        timeline = app.query_one("#sacred-timeline")
        
        # Turn 1
        await pilot.click("#prompt-input")
        await pilot.type("What is 2+2?")
        await pilot.press("enter")
        
        await pilot.wait_until(
            lambda: len(timeline.query(".simple-block")) >= 2,
            timeout=10.0
        )
        
        # Turn 2
        await pilot.type("What about 3+3?")
        await pilot.press("enter")
        
        await pilot.wait_until(
            lambda: len(timeline.query(".simple-block")) >= 4,
            timeout=10.0
        )
        
        # Verify turn structure
        blocks = timeline.query(".simple-block")
        assert len(blocks) >= 4
        
        # Verify hrule separators exist
        hrules = timeline.query(".hrule")
        assert len(hrules) >= 1  # At least one turn separator
```

## Performance Testing

### High Volume Content Handling

```python
@pytest.mark.asyncio
async def test_high_volume_timeline_performance():
    """Test Sacred Timeline with large conversation history"""
    
    timeline = SacredTimelineWidget()
    
    start_time = time.time()
    
    # Add 1000 blocks
    for i in range(1000):
        role = "user" if i % 2 == 0 else "assistant"
        content = f"Message {i}: " + "x" * 100  # 100 char messages
        block = InscribedBlock(role, content)
        await timeline.add_block(block)
        
        # Occasional yield to event loop
        if i % 100 == 0:
            await asyncio.sleep(0.01)
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Performance requirements
    assert duration < 10.0  # Should handle 1000 blocks in < 10 seconds
    assert len(timeline.children) == 1000
    
    # Memory usage should be reasonable
    import psutil
    process = psutil.Process()
    memory_mb = process.memory_info().rss / 1024 / 1024
    assert memory_mb < 500  # Should use < 500MB for 1000 blocks

def test_memory_cleanup_on_workspace_clear():
    """Test memory is cleaned when workspace is cleared"""
    
    workspace = LiveWorkspaceWidget()
    
    # Add many sub-modules
    for i in range(100):
        sub_module = SubModuleWidget(f"step_{i}", "test_model")
        workspace.mount(sub_module)
    
    initial_children = len(workspace.children)
    assert initial_children == 100
    
    # Clear workspace
    workspace.clear_workspace()
    
    # Verify cleanup
    assert len(workspace.children) == 0
    assert len(workspace.sub_modules) == 0
```

## Test Organization

### Test File Structure

```
tests/
├── test_v3_pattern_compliance/
│   ├── test_sacred_timeline_v3.py    # Timeline follows V3 chat_container
│   ├── test_simple_block_v3.py       # Blocks follow V3 Chatbox  
│   └── test_thread_safety_v3.py      # Thread-safe patterns
├── test_sacred_architecture/
│   ├── test_layout_validation.py     # No nested containers
│   ├── test_state_transitions.py     # 2-way ↔ 3-way splits
│   └── test_timeline_immutability.py # Append-only timeline
├── test_streaming/
│   ├── test_streaming_harness.py     # Streaming simulation
│   ├── test_auto_scroll.py           # Smart scroll behavior
│   └── test_high_volume.py           # Performance testing
├── test_error_handling/
│   ├── test_error_boundaries.py      # Graceful failure
│   ├── test_validation.py            # Input validation
│   └── test_app_resilience.py        # Error recovery
├── test_integration/
│   ├── test_user_flows.py            # End-to-end interactions
│   ├── test_multi_turn.py            # Conversation flows
│   └── test_performance.py           # High-load scenarios
└── harnesses/
    ├── streaming_harness.py          # Streaming simulation tools
    ├── error_injection.py            # Error scenario tools
    └── performance_harness.py        # Load testing tools
```

### Running Tests

```bash
# Run all Sacred Architecture tests
just test

# Run specific test categories
pytest tests/test_v3_pattern_compliance/ -v
pytest tests/test_sacred_architecture/ -v  
pytest tests/test_streaming/ -v
pytest tests/test_error_handling/ -v
pytest tests/test_integration/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run performance tests only
pytest tests/test_integration/test_performance.py -v

# Run streaming simulation tests
pytest tests/test_streaming/ -k "simulation" -v
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Sacred Architecture Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install pdm
          pdm install --dev
          
      - name: Run V3 pattern compliance tests
        run: |
          pdm run pytest tests/test_v3_pattern_compliance/ -v
          
      - name: Run Sacred Architecture validation
        run: |
          pdm run pytest tests/test_sacred_architecture/ -v
          
      - name: Run streaming tests
        run: |
          pdm run pytest tests/test_streaming/ -v
          
      - name: Run integration tests with timeout
        run: |
          pdm run pytest tests/test_integration/ -v --timeout=60
          
      - name: Validate CSS properties
        run: |
          pdm run python scripts/validate_css.py src/
```

---

**Next Steps**: After setting up testing, see:
- Design Guide → `.ai/docs/DESIGN-GUIDE.md`
- Reference Guide → `.ai/docs/REFERENCE-GUIDE.md`