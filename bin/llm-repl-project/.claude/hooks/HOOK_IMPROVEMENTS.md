# Hook System Improvements

## 1. Claude Communication Documentation

### Hooks That Can Communicate With Claude

#### **PreToolUse Hook** ✅ **CAN BLOCK EXECUTION**
- **Method 1**: Exit Code 2 + stderr → **Blocks tool, shows error to Claude** ✅ **TESTED & WORKING**
- **Method 2**: JSON stdout `{"decision": "block", "reason": "explanation"}` → **⚠️ UNTESTED - NO EVIDENCE THIS WORKS**
- **Method 3**: JSON stdout `{"decision": "approve", "reason": "explanation"}` → **⚠️ UNTESTED - NO EVIDENCE THIS WORKS**
- **Current**: Uses Method 1 for security blocks

⚠️ **HUGE WARNING**: Only Method 1 (Exit Code 2 + stderr) has been verified to work in practice. The JSON methods are documented but UNPROVEN.

#### **PostToolUse Hook** ✅ **CAN PROVIDE FEEDBACK** 
- **Method 1**: Exit Code 2 + stderr → **Shows error to Claude (tool already ran)** ✅ **TESTED & WORKING**
- **Method 2**: JSON stdout `{"decision": "block", "reason": "explanation"}` → **⚠️ UNTESTED - NO EVIDENCE THIS WORKS**
- **Current**: No communication (pure logging) - could be extended

#### **Stop Hook** ✅ **CAN FORCE CONTINUATION**
- **Method 1**: Exit Code 2 + stderr → **Blocks stopping, stderr sent to Claude as instructions** ✅ **TESTED & WORKING**
- **Method 2**: JSON stdout `{"decision": "block", "reason": "explanation"}` → **⚠️ UNTESTED - NO EVIDENCE THIS WORKS**
- **Current**: No communication by default, **Loop Mode** available via `--loop` flag

#### **SubagentStop Hook** ✅ **CAN CONTROL SUBAGENTS**
- **Method 1**: Exit Code 2 + stderr → **Blocks subagent stopping, stderr sent to SUBAGENT** ✅ **TESTED & WORKING**
- **Method 2**: JSON stdout `{"decision": "block", "reason": "explanation"}` → **⚠️ UNTESTED - NO EVIDENCE THIS WORKS**
- **Current**: No communication (pure logging)

#### **Notification Hook** ❌ **CANNOT COMMUNICATE WITH CLAUDE**
- **No Claude Communication**: This hook type only handles user notifications
- **stderr**: Shown to USER only, not Claude
- **Current**: Pure user notification with TTS support

### Universal Control Options
All hooks support:
```json
{
  "continue": false,        // Stops Claude entirely 
  "stopReason": "message"   // Shown to USER (not Claude)
}
```

## 2. Extensible Pre-Tool Security System

### Current Validators
1. **`is_dangerous_rm_command`** - Blocks destructive rm operations
2. **`is_env_file_access`** - Prevents .env file access
3. **`is_sudo_privilege_escalation`** - Blocks dangerous sudo usage
4. **`is_network_exposure`** - Detects unsafe network exposure

### Adding New Validators

```python
def is_your_custom_check(tool_name, tool_input):
    """
    Your custom security validator.
    Returns (is_violation, reason) tuple.
    """
    if tool_name != 'Bash':
        return False, ""
    
    command = tool_input.get('command', '')
    
    # Your validation logic here
    if some_dangerous_pattern_detected(command):
        return True, "Your descriptive reason"
    
    return False, ""

# Register your validator
SECURITY_VALIDATORS.append(is_your_custom_check)
```

### Example Patterns Blocked
```bash
# Dangerous removal commands
rm -rf /
sudo rm -rf *
rm --recursive --force ~/

# Environment file access  
cat .env
echo "SECRET=123" > .env

# Privilege escalation
sudo su
sudo passwd
sudo chmod 777

# Network exposure
python3 -m http.server 8000 --bind 0.0.0.0
nc -l 0.0.0.0 8080
```

## 3. Stop Hook Loop Mode

### Enabling Loop Mode
```json
{
  "command": "uv run .claude/hooks/stop.py --chat --loop"
}
```

### Current Completion Checks
1. **Tests**: Runs `pytest --tb=short` to verify tests pass
2. **Lint**: Runs basic Python syntax validation
3. **Git**: Checks for uncommitted changes

### Adding New Completion Checks

```python
def check_your_completion_criteria():
    """
    Your custom completion check.
    Returns (is_passing, failure_reason) tuple.
    """
    try:
        # Your validation logic
        if not your_criteria_met():
            return False, "Your specific failure reason"
        return True, ""
    except Exception:
        return True, ""  # Don't block on check errors

# Register your check
COMPLETION_CHECKS.append(("your_check", check_your_completion_criteria))
```

### Loop Mode Behavior
- **Criteria Met**: Normal completion with TTS announcement
- **Criteria Failed**: Blocks Claude from stopping, sends specific instructions:
  ```
  "Please address these issues before completing: tests: Tests failing; git: Uncommitted changes"
  ```

### Example Use Cases
- Enforce code quality before task completion
- Ensure all tests pass before moving to next task
- Verify documentation is updated
- Check deployment prerequisites
- Validate security requirements

## Benefits

1. **Precise Documentation**: Clear understanding of which hooks can talk to Claude and how
2. **Easy Security Extension**: Add new security validators in minutes
3. **Quality Enforcement**: Loop mode ensures tasks meet completion criteria
4. **Comprehensive Logging**: All interactions and blocks are logged with context
5. **Fail-Safe Design**: Hooks gracefully handle errors without breaking Claude Code

## Usage Patterns

### Development Workflow
1. **PreToolUse**: Prevents dangerous operations during development
2. **PostToolUse**: Could validate results and provide feedback to Claude
3. **Stop + Loop Mode**: Ensures quality gates before task completion
4. **Notification**: Provides audio feedback to developer

### Security Posture
- **Multi-layer validation**: Extensible security checks
- **Complete audit trail**: All blocked operations logged
- **Fail-secure**: Unknown operations allowed, known dangerous ones blocked
- **Contextual blocking**: Different validators for different tool types