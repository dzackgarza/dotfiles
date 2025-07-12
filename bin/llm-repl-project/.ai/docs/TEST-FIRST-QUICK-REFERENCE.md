# Test-First Development Quick Reference

## 🚨 THE GOLDEN RULE
**No code without a failing test. The test IS the specification.**

## 🔄 The Sacred Workflow

### 1. Start Feature → Write Test First
```bash
# Create failing test
just create-test chat-widget

# Edit test to define behavior
vi tests/test_chat_widget.py
```

### 2. Verify Test Fails
```bash
# Must fail (feature doesn't exist yet)
just verify-failing test_chat_widget
✅ Good! Test is properly failing.
```

### 3. NOW Implement
```bash
# Hook allows editing only after failing test exists
vi src/widgets/chat_widget.py
```

### 4. Make Test Pass
```bash
# Run tests
just test-acceptance
✅ Tests passing - feature complete!
```

## 🛡️ Automatic Enforcement

### What Gets Blocked
- ❌ Editing `src/*.py` without test → **BLOCKED**
- ❌ Test already passing → **BLOCKED** (not driving development)
- ❌ Test has errors → **BLOCKED** (fix test first)

### Error Messages You'll See
```
🚫 BLOCKED: Test-First Development Required

No test found at: tests/test_feature.py

You must create a failing acceptance test BEFORE implementing code.
```

## 📝 Test Template

```python
import pytest
from textual.testing import AppTest
from src.main import LLMReplApp

@pytest.mark.asyncio
async def test_feature_user_interaction():
    """User interacts with feature."""
    async with LLMReplApp().run_test() as pilot:
        # Define user interaction
        await pilot.press("key")
        
        # Verify user-observable behavior
        assert "expected" in pilot.app.screen
```

## 🎯 Commands Reference

| Command | Purpose |
|---------|---------|
| `just create-test <name>` | Create new failing test |
| `just verify-failing <test>` | Check test fails properly |
| `just test-acceptance` | Run acceptance tests only |
| `just check-coverage` | Find files missing tests |

## 💡 Pro Tips

1. **Test names describe user actions**: `test_user_sends_message`, not `test_send_method`
2. **Test what users see**: Screen content, not internal state
3. **One behavior per test**: Keep tests focused
4. **Let test fail first**: Proves it's testing the right thing
5. **Test guides design**: Hard to test = bad design

## 🚫 Common Mistakes

### ❌ Writing implementation first
```bash
vi src/feature.py  # BLOCKED! No test exists
```

### ❌ Test already passes
```python
async def test_feature():
    assert True  # Useless - not driving development
```

### ❌ Testing internals
```python
def test_internal_method():
    obj._private_method()  # NO! Test user behavior
```

### ✅ Correct approach
```python
async def test_user_sees_result():
    """User performs action and sees result."""
    # Real user interaction test
```

## 🔍 When You're Blocked

1. **No test file?** → `just create-test feature-name`
2. **Test passing?** → Make it expect NEW behavior
3. **Test errors?** → Fix test syntax first
4. **Not sure what to test?** → What would user notice?

## 📚 Full Documentation

- Strategy: `.ai/docs/MANDATORY-ACCEPTANCE-TESTING-STRATEGY.md`
- Testing Guide: `.ai/docs/TESTING-GUIDE.md`
- Examples: `tests/test_user_interactions.py`

---

**Remember**: The test defines what "working" means. Code just makes the test pass.