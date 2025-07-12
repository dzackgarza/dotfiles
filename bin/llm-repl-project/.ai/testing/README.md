# Testing Documentation

> **Test Against Working Patterns**: Validate our implementations against V3's proven patterns. Test that our widgets work like the reference implementations, not just that they compile.

This directory contains comprehensive testing strategies, test harnesses, and validation approaches specifically designed for Sacred Architecture and Textual applications.

## Files Overview

```
testing/
├── README.md                    # This overview
├── textual-testing-guide.md    # Comprehensive Textual testing strategies
├── sacred-architecture-tests.md # Sacred GUI specific test patterns
├── widget-test-harnesses.md    # Simulation scripts for widget testing
├── integration-test-guide.md   # End-to-end testing approaches
└── ci-validation-guide.md      # Continuous integration patterns
```

## Testing Philosophy

```
┌─ Sacred Architecture Testing Principles ─────────────────┐
│                                                           │
│  🏆 V3 Pattern Validation: Test against working examples │
│  🔍 Reference Behavior Testing: Does it work like V3?   │
│  📚 Working Pattern Compliance: VerticalScroll + render() │
│  🚫 Layout Conflict Prevention: No nested containers     │
│  ⚡ Streaming Simulation: Test dynamic content updates   │
│  🛡️ Error Boundary Testing: Graceful failure handling    │
│  📏 Responsive Behavior: Dynamic resizing validation     │
│  🔄 State Transition Testing: 2-way ↔ 3-way splits      │
│  🧵 Thread Safety: Concurrent update validation         │
│  📊 Performance Testing: High content volume handling    │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

## Testing Categories

### 🧪 **Unit Tests (Isolated Components)**

```python
# Example: SimpleBlockWidget validation
@pytest.mark.asyncio
async def test_simple_block_widget_validation():
    """Test fail-fast input validation"""
    
    # Valid input should work
    valid_data = BlockData(role="user", content="Test", timestamp=now())
    widget = SimpleBlockWidget(valid_data)
    assert widget.data == valid_data
    
    # Invalid input should raise immediately
    with pytest.raises(ValueError, match="Invalid block data"):
        SimpleBlockWidget(None)
    
    with pytest.raises(ValueError, match="Missing required field"):
        SimpleBlockWidget({"invalid": "data"})
```

### 🏗️ **Widget Test Harnesses (Simulation)**

```python
# Example: Streaming content simulation
class StreamingTestHarness:
    """Simulate streaming content for widget testing"""
    
    async def simulate_streaming_content(self, widget, content_chunks):
        """Test widget behavior during streaming"""
        for i, chunk in enumerate(content_chunks):
            # Simulate network delay
            await asyncio.sleep(0.1)
            
            # Update widget content
            widget.update_content(chunk)
            
            # Validate widget state
            assert widget.current_content == "".join(content_chunks[:i+1])
            assert widget.streaming_active == (i < len(content_chunks) - 1)
    
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
```

### 🔗 **Integration Tests (End-to-End Flows)**

```python
# Example: Complete user interaction flow
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
```

### 🛡️ **Error Boundary Testing**

```python
# Example: Widget error handling validation
@pytest.mark.asyncio  
async def test_error_boundary_handling():
    """Test that widget errors don't crash the app"""
    
    class FailingWidget(Widget):
        def render(self):
            raise ValueError("Intentional test failure")
    
    app = LLMReplApp()
    async with app.run_test() as pilot:
        # Add failing widget with error boundary
        failing_widget = ErrorBoundaryWidget(FailingWidget())
        await app.mount(failing_widget)
        
        # App should still be responsive
        await pilot.pause(0.1)
        assert app.is_running
        
        # Error should be displayed
        error_display = app.query_one(".error-display")
        assert "Intentional test failure" in error_display.content
```

### 📐 **Layout Validation Tests**

```python
# Example: Sacred Architecture compliance
def test_sacred_architecture_compliance():
    """Ensure no nested containers in VerticalScroll widgets"""
    app = LLMReplApp()
    
    # Check Sacred Timeline
    sacred_timeline = app.query_one("#sacred-timeline")
    assert isinstance(sacred_timeline, VerticalScroll)
    
    # Validate no nested containers
    for child in sacred_timeline.children:
        assert not isinstance(child, (Vertical, VerticalScroll))
        assert hasattr(child, 'render')  # V3 render pattern
    
    # Check Live Workspace
    live_workspace = app.query_one("#live-workspace")
    assert isinstance(live_workspace, VerticalScroll)
    
    for child in live_workspace.children:
        assert not isinstance(child, (Vertical, VerticalScroll))
        assert hasattr(child, 'render')  # V3 render pattern
```

## Testing Tools & Utilities

### 🎯 **Test Data Generators**

```python
# Generate test data for various scenarios
class TestDataGenerator:
    @staticmethod
    def create_block_data(role="user", content="Test content"):
        return BlockData(
            id=f"test-{uuid4()}",
            role=role,
            content=content,
            timestamp=datetime.now(timezone.utc)
        )
    
    @staticmethod  
    def create_streaming_chunks(text, chunk_size=10):
        """Split text into streaming chunks"""
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    @staticmethod
    def create_cognition_pipeline():
        """Generate test cognition pipeline"""
        return [
            SubModuleData("route_query", "tinyllama", "completed"),
            SubModuleData("research", "phi-3.5", "active"),
            SubModuleData("synthesize", "claude", "pending"),
        ]
```

### 🔧 **Testing Utilities**

```python
# Helper functions for common test operations
class TestingUtils:
    @staticmethod
    async def wait_for_widget_state(widget, expected_state, timeout=5.0):
        """Wait for widget to reach expected state"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if widget.current_state == expected_state:
                return True
            await asyncio.sleep(0.1)
        raise TimeoutError(f"Widget never reached state: {expected_state}")
    
    @staticmethod
    def assert_valid_css_properties(widget):
        """Validate CSS uses only valid Textual properties"""
        css_rules = widget.get_style_rules()
        forbidden_properties = ["border-color", "background-color"]
        
        for rule in css_rules:
            for prop in forbidden_properties:
                assert prop not in rule.properties, f"Invalid CSS property: {prop}"
```

## Test Categories Summary

| Test Type | Purpose | Files | Tools |
|-----------|---------|--------|-------|
| **Unit Tests** | Component validation | `test_widgets/` | pytest, pytest-asyncio |
| **Widget Harnesses** | Simulation testing | `test_harnesses/` | Custom simulators |
| **Integration Tests** | End-to-end flows | `test_integration/` | Textual Pilot, run_test() |
| **Layout Tests** | Architecture compliance | `test_layout/` | DOM inspection |
| **Performance Tests** | Load and stress testing | `test_performance/` | Memory profiling |
| **Error Tests** | Failure scenario testing | `test_errors/` | Error injection |

## CI/CD Integration

```yaml
# Example GitHub Actions workflow
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
          pip install -r requirements-test.txt
          
      - name: Run Sacred Architecture tests
        run: |
          # Layout compliance tests
          pytest tests/test_layout/ -v
          
          # Widget validation tests  
          pytest tests/test_widgets/ -v
          
          # Integration tests with timeout
          pytest tests/test_integration/ -v --timeout=60
          
          # Performance benchmarks
          pytest tests/test_performance/ -v --benchmark-only
      
      - name: Validate CSS properties
        run: |
          python scripts/validate_css.py src/
```

## Quick Commands

```bash
# Run all Sacred Architecture tests
pytest tests/ -k "sacred" -v

# Run streaming simulation tests
pytest tests/test_harnesses/test_streaming.py -v

# Run layout compliance tests
pytest tests/test_layout/ -v

# Run performance benchmarks
pytest tests/test_performance/ --benchmark-only

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Cross-References

- **Architecture**: See `../architecture/` for design specifications being tested
- **Implementation**: See `../implementation/` for code being validated
- **Design**: See `../design/` for UI components being tested
- **Reference**: See `../reference/` for testing framework documentation