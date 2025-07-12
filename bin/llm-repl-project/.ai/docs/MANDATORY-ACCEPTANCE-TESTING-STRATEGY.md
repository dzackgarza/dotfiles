# Mandatory Acceptance Testing Strategy

## Executive Summary

This document outlines the strategy and implementation plan for enforcing a **Mandatory Acceptance Testing** paradigm in the LLM REPL project. The core principle: **No application code can be written until a failing test exists that defines what that code must do.**

## Core Philosophy

### The Sacred Rule
> "The test IS the specification. Code follows test. Always."

### Key Principles

1. **Test-First Development**: Tests must exist and fail before implementation
2. **Executable Specifications**: Tests define behavior, not documentation
3. **User-Observable Only**: Tests verify what users see, not internals
4. **No Test, No Code**: Implementation blocked without failing test

## Implementation Strategy

### Phase 1: Hook System Enhancement

#### 1.1 PreToolUse Hook for Edit/Write/MultiEdit
```json
{
  "matcher": "Edit|Write|MultiEdit",
  "hooks": [{
    "type": "command",
    "command": "/home/dzack/dotfiles/bin/llm-repl-project/scripts/acceptance-test-hook.sh"
  }]
}
```

#### 1.2 Hook Logic Flow
```
1. Detect file modification attempt
2. Check if file is application code (src/*.py)
3. Verify corresponding test exists (tests/test_*.py)
4. Run test to ensure it's failing
5. Block edit if:
   - No test exists
   - Test is passing
   - Test has errors
```

### Phase 2: Ledger System Integration

#### 2.1 Modified Ledger Workflow
```
1. Start Ledger → Create test tasks FIRST
2. Test Phase → Write failing acceptance tests
3. Implementation Phase → Make tests pass
4. Review Phase → Verify all tests green
```

#### 2.2 Test-Driven Task Creation
When starting a ledger, automatically create:
- "Write failing test for [feature]" tasks
- "Implement [feature] to pass test" tasks
- "Verify test coverage" tasks

### Phase 3: Workflow Enforcement

#### 3.1 New Just Commands
```bash
# Create failing test for a feature
just create-test <feature-name>

# Verify test is failing properly
just verify-failing-test <test-name>

# Check implementation readiness
just check-test-coverage

# Run acceptance tests only
just test-acceptance
```

#### 3.2 Git Hooks
- Pre-commit: Verify all code has tests
- Pre-push: Ensure tests are passing
- Post-merge: Run full test suite

## Technical Implementation

### Hook Script Enhancement

```bash
#!/bin/bash
# acceptance-test-hook.sh v2

# Enhanced validation with better error messages
validate_test_first_development() {
    local file="$1"
    
    # Skip non-application code
    if [[ ! $file =~ ^src/.*\.py$ ]] || [[ $file =~ ^tests/ ]]; then
        return 0
    fi
    
    # Derive test file path
    local test_file=$(derive_test_path "$file")
    
    # Check test existence
    if [[ ! -f "$test_file" ]]; then
        cat << EOF
🚫 BLOCKED: No test found for $file

You must create a failing acceptance test first:
1. Run: just create-test $(basename $file .py)
2. Write test that defines desired behavior
3. Verify test fails: just verify-failing-test $test_file
4. Then implement the code

Test-Driven Development is mandatory.
EOF
        return 1
    fi
    
    # Verify test is failing
    if run_test "$test_file"; then
        cat << EOF
🚫 BLOCKED: Test is already passing for $file

This violates test-first development:
- Either the test doesn't properly verify the new behavior
- Or the implementation already exists

Fix the test to fail for the missing behavior.
EOF
        return 1
    fi
    
    return 0
}
```

### Ledger Tracker Enhancement

```python
def start_ledger_with_tests(self, ledger_name: str):
    """Enhanced ledger start with test-first tasks."""
    
    # Extract features from ledger
    features = self.extract_features_from_ledger(ledger_path)
    
    # Create test-first tasks
    todos = []
    for feature in features:
        # Test task comes FIRST
        todos.append({
            "content": f"Write failing acceptance test for: {feature['name']}",
            "status": "pending",
            "priority": "high",
            "id": f"{ledger_name}_test_{feature['id']}"
        })
        
        # Implementation task depends on test
        todos.append({
            "content": f"Implement {feature['name']} to pass test",
            "status": "blocked",  # Blocked until test exists
            "priority": "high",
            "id": f"{ledger_name}_impl_{feature['id']}",
            "depends_on": f"{ledger_name}_test_{feature['id']}"
        })
```

## Workflow Examples

### Example 1: Adding New Feature

```bash
# 1. Agent starts work on chat widget
$ just start-ledger chat-widget

# 2. System creates tasks:
- [ ] Write failing test for chat message display
- [ ] Implement chat message display (BLOCKED)
- [ ] Write failing test for message history
- [ ] Implement message history (BLOCKED)

# 3. Agent writes test
$ cat > tests/test_chat_widget.py << EOF
async def test_chat_displays_user_message():
    """User types message and sees it in chat."""
    async with app.run_test() as pilot:
        await pilot.press("h", "i")
        await pilot.press("enter")
        # Verify message appears in chat
        assert "hi" in pilot.app.query_one("ChatWidget").messages
EOF

# 4. Verify test fails
$ just verify-failing-test tests/test_chat_widget.py
✅ Test is properly failing (feature not implemented)

# 5. Now implementation is allowed
$ vi src/widgets/chat_widget.py  # Hook allows edit
```

### Example 2: Modifying Existing Code

```bash
# 1. Agent tries to modify existing widget
$ vi src/widgets/timeline.py

# 2. Hook checks for test
🚫 BLOCKED: No failing test for timeline changes

# 3. Agent must write test first
$ cat > tests/test_timeline_new_feature.py << EOF
async def test_timeline_shows_timestamps():
    """Each message in timeline has visible timestamp."""
    async with app.run_test() as pilot:
        # Send message
        await pilot.press("h", "i")
        await pilot.press("enter")
        
        # Check timestamp appears
        timeline = pilot.app.query_one("Timeline")
        assert "timestamp" in timeline.messages[0]
EOF

# 4. Now modification allowed
$ vi src/widgets/timeline.py  # Hook allows edit
```

## Benefits

1. **Quality Assurance**: Every line of code has test coverage
2. **Clear Specifications**: Tests document exact behavior
3. **Prevent Regression**: Changes require test updates
4. **Design Clarity**: Writing test first clarifies design
5. **User Focus**: Tests enforce user-observable behavior

## Migration Plan

### Week 1: Infrastructure
- [ ] Enhance acceptance-test-hook.sh
- [ ] Update .claude/settings.json
- [ ] Create new just commands
- [ ] Update ledger_tracker.py

### Week 2: Documentation
- [ ] Update CLAUDE.md with new rules
- [ ] Create test-writing guide
- [ ] Update onboarding docs
- [ ] Add workflow examples

### Week 3: Enforcement
- [ ] Enable hooks in production
- [ ] Monitor compliance
- [ ] Refine error messages
- [ ] Gather feedback

### Week 4: Optimization
- [ ] Improve test running speed
- [ ] Better test failure messages
- [ ] Enhanced IDE integration
- [ ] Success metrics

## Success Metrics

1. **Coverage**: 100% of new code has tests
2. **Test-First Rate**: 100% of changes start with test
3. **Test Quality**: 0% mock-based tests
4. **User Focus**: 100% tests verify user behavior
5. **Development Speed**: Maintained or improved

## Conclusion

Mandatory Acceptance Testing transforms our development process from "code-then-test" to "test-then-code". This ensures every feature is specified by executable tests that verify user-observable behavior. The system is enforced through hooks, integrated with our ledger workflow, and supported by enhanced tooling.

The result: Higher quality code that always works for users, because we've defined "works" through tests before writing a single line of implementation.