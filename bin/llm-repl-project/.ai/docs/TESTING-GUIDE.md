# Testing Guide

> **SACRED RULE**: Test-first development is MANDATORY. Write failing acceptance tests before any implementation. Only test end-to-end user interactions. No unit tests, no mocks, no internal implementation details. Test the user experience.

## Testing Philosophy: Death to Test Theater

**THE PARABLE OF THE 195 FAKE TESTS**

Once upon a time, there was a project with 195 "passing" tests. Developers felt confident. CI was green. But when a user tried the basic workflow - typing "hello" and pressing Enter - the app crashed.

The tests were testing:
- Mock scenarios with fake data  
- Internal class methods
- CSS loading utilities
- Debug screenshot tools
- Animation timing calculations

But they weren't testing:
- Can a user actually send a message?
- Does the conversation history work?
- Do responses appear?

**195 tests, 0 user value.**

## The Sacred Testing Commandments

### 0. ALWAYS Write Tests First (NEW MANDATORY RULE)
- 🚫 **BLOCKED**: No code without failing test
- ✅ **REQUIRED**: Test defines specification
- 📋 **WORKFLOW**: Write test → Run (fails) → Implement → Run (passes)
- 🤖 **ENFORCEMENT**: Automated hooks prevent code-first development

### 1. ONLY Test User Interactions
- ✅ User types message → response appears
- ✅ Conversation history is preserved
- ✅ App doesn't crash on basic usage
- ❌ Internal method returns correct value
- ❌ CSS class is applied correctly
- ❌ Mock data generation works

### 2. ONLY Test End-to-End Flows
- ✅ Full conversation workflow 
- ✅ Multi-turn conversations
- ✅ Error handling user can see
- ❌ Unit tests for individual functions
- ❌ Component isolation tests
- ❌ Mocked dependencies

### 3. ONLY Test Observable Behavior
- ✅ Timeline shows user messages
- ✅ Workspace appears during processing
- ✅ Responses are displayed
- ❌ Internal state is correct
- ❌ Method was called with right params
- ❌ Data structure is valid

## Sacred Testing Examples

### The ONLY Tests You Need

```python
@pytest.mark.asyncio
async def test_user_can_have_conversation():
    """Test: User sends message, gets response"""
    async with LLMReplApp().run_test() as pilot:
        # Type message
        await pilot.press("h", "e", "l", "l", "o")
        await pilot.press("enter")
        
        # Should see response (however it appears)
        # Don't test HOW it works, test THAT it works
        
@pytest.mark.asyncio  
async def test_conversation_history_persists():
    """Test: Multiple messages stay visible"""
    async with LLMReplApp().run_test() as pilot:
        # Send two messages
        await pilot.press("h", "i")
        await pilot.press("enter")
        await pilot.pause(2.0)
        
        await pilot.press("b", "y", "e")
        await pilot.press("enter")
        
        # Both should be visible somehow
        # Don't care about implementation
        
@pytest.mark.asyncio
async def test_app_handles_errors_gracefully():
    """Test: App doesn't crash on weird input"""
    async with LLMReplApp().run_test() as pilot:
        # Try to break it
        await pilot.press("ctrl+c")
        await pilot.press("escape")
        
        # Should still work
        await pilot.press("h", "i")
        await pilot.press("enter")
```

### What We DON'T Test

❌ **Internal methods**
```python
# FORBIDDEN
def test_sacred_timeline_add_block():
    timeline = SacredTimeline()
    result = timeline.add_block("user", "test")
    assert result.role == "user"  # WHO CARES?
```

❌ **CSS classes and styling**
```python  
# FORBIDDEN
def test_block_has_correct_css_class():
    widget = SimpleBlockWidget(data)
    assert "user-block" in widget.classes  # MEANINGLESS
```

❌ **Mock objects and fake data**
```python
# FORBIDDEN  
@patch('src.core.llm_client')
def test_response_generation(mock_client):
    mock_client.return_value = "fake response"
    # TESTING NOTHING REAL
```

❌ **Component isolation**
```python
# FORBIDDEN
def test_prompt_input_widget_alone():
    widget = PromptInput()
    widget.value = "test"
    # DOESN'T MATTER IF REST OF APP IS BROKEN
```

### The Testing Hierarchy

1. **Level 1: Can user complete basic task?**
   - Send message → get response
   - Have multi-turn conversation
   - App doesn't crash

2. **Level 2: Does the user experience work?**
   - Messages appear in timeline
   - Responses are readable  
   - Interface is responsive

3. **Level 3: Edge cases user might encounter**
   - Very long messages
   - Rapid typing
   - Network errors

**NEVER Level 4**: Internal implementation details

## Implementation Guidelines

### Current Working Tests

Our tests in `tests/` follow these principles:

```python
# tests/test_user_interactions.py
class TestUserInteractions:
    async def test_app_starts_and_shows_welcome(self):
        """User opens app and sees welcome"""
        
    async def test_user_sends_message_gets_response(self):
        """User types, presses Enter, gets response"""
        
    async def test_conversation_history_preserved(self):
        """Multiple messages create history"""
        
    async def test_multiline_input_with_shift_enter(self):
        """Shift+Enter creates new line"""
        
    async def test_app_handles_errors_gracefully(self):
        """App doesn't crash on errors"""

# tests/test_sacred_architecture.py  
class TestSacredArchitecture:
    async def test_starts_in_2way_split(self):
        """App starts with timeline + input visible"""
        
    async def test_transitions_to_3way_split_during_processing(self):
        """Workspace appears during processing"""
        
    async def test_returns_to_2way_split_after_completion(self):
        """Workspace disappears after completion"""
        
    async def test_timeline_preserves_conversation_history(self):
        """All messages stay in timeline"""
        
    async def test_workspace_shows_cognition_steps(self):
        """Live processing is visible to user"""
```

### Test File Structure

```
tests/
├── test_user_interactions.py     # Basic user workflows
├── test_sacred_architecture.py   # GUI behavior user sees
└── test_edge_cases.py            # Error scenarios user encounters
```

**That's it. 3 files. 15 tests. All user-focused.**

### Test-First Development Workflow

```bash
# 1. Create failing test for new feature
just create-test chat-widget

# 2. Edit test to define desired behavior
vi tests/test_chat_widget.py

# 3. Verify test fails (feature not implemented)
just verify-failing test_chat_widget

# 4. NOW you can implement (hook allows editing)
vi src/widgets/chat_widget.py

# 5. Run test to verify implementation
just test-acceptance
```

### Running Tests

```bash
# Run all user interaction tests
just test

# Run acceptance tests only (no linting)
just test-acceptance

# Check which files need tests
just check-coverage

# Quick development check
pdm run pytest tests/test_user_interactions.py -v

# Check specific behavior
pdm run pytest tests/test_sacred_architecture.py::TestSacredArchitecture::test_starts_in_2way_split -v
```

## The Anti-Pattern Hall of Shame

### Things We Used to Test (DON'T DO THIS)

❌ **Mock scenario generation** - 50 tests for fake data generators  
❌ **Animation timing** - 25 tests for FPS calculations  
❌ **Debug tool utilities** - 30 tests for screenshot functions  
❌ **CSS loading** - 15 tests for theme validation  
❌ **Performance monitoring** - 40 tests for metric collection  
❌ **Configuration validation** - 20 tests for YAML parsing  
❌ **Internal state management** - 15 tests for data structures  

**Total: 195 tests, 0 user value**

### What Actually Matters

✅ **User can send messages** - 1 test  
✅ **User can see responses** - 1 test  
✅ **User can have conversations** - 1 test  
✅ **App doesn't crash** - 1 test  

**Total: 4 tests, infinite user value**

## Memory Techniques

### The Test Theater Detection Kit

Ask yourself:
1. **Would a user care if this fails?** If no → delete test
2. **Does this test the full workflow?** If no → expand or delete  
3. **Can I run this without mocks?** If no → delete
4. **Does this test implementation details?** If yes → delete

### The Sacred Testing Mantra

*"I test what users do, not how code works"*

*"I test end-to-end flows, not isolated units"*  

*"I test observable behavior, not internal state"*

*"I test real interactions, not mock scenarios"*

## Enforcement

### Test-First Development Hook

The `acceptance-test-hook.sh` runs automatically when you try to edit source code:

```bash
# Triggered on Edit/Write/MultiEdit of src/*.py files
# Blocks if:
# - No corresponding test file exists
# - Test file exists but is passing (not driving new development)
# - Test has syntax errors
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Count test files
test_count=$(find tests/ -name "*.py" | wc -l)

if [ $test_count -gt 5 ]; then
    echo "❌ TOO MANY TEST FILES ($test_count)"
    echo "Only user interaction tests allowed"
    echo "Delete unit tests and mocks"
    exit 1
fi

# Check for forbidden patterns
if grep -r "mock\|patch\|Mock" tests/; then
    echo "❌ MOCKS DETECTED"
    echo "Only real end-to-end tests allowed"
    exit 1
fi

if grep -r "def test_.*_unit\|def test_.*_method\|def test_.*_class" tests/; then
    echo "❌ UNIT TESTS DETECTED"  
    echo "Only user interaction tests allowed"
    exit 1
fi

echo "✅ Tests follow Sacred Rules"
```

### Code Review Checklist

- [ ] Tests simulate actual user interactions
- [ ] No mocks, patches, or fake data
- [ ] Tests run full app end-to-end
- [ ] Tests verify user-observable behavior
- [ ] Test count remains low (< 20 total)

---

**Remember**: Your tests should tell the story of how users interact with your app, not how your code is structured internally.