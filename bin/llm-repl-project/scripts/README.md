# Claude Code Command Validation

This directory contains scripts for validating commands in Claude Code hooks to ensure safe and proper usage.

## Files

### `validate-command.sh`
Main command validation script used by Claude Code PreToolUse hooks.

**Features:**
- Blocks raw `pytest` commands, forcing use of `just test` for comprehensive testing
- Prevents GUI applications that would crash Claude Code
- Blocks dangerous commands (sudo, rm -rf, etc.)
- Allows help/info commands to pass through
- Extensible pattern matching for new command restrictions

**Usage:**
```bash
# Via Claude Code hooks (automatic)
echo '{"tool_input": {"command": "pdm run pytest"}}' | ./validate-command.sh

# Direct testing
./validate-command.sh "pdm run pytest tests/"
```

### `test-command-validation.sh`
Test suite for command validation logic.

**Usage:**
```bash
./test-command-validation.sh
```

## Integration with Claude Code

The validation is integrated via `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/validate-command.sh"
          }
        ]
      }
    ]
  }
}
```

## Command Policies

### ❌ Blocked Commands

1. **Raw pytest execution**
   - `pdm run pytest`
   - `poetry run pytest` 
   - `python -m pytest`
   - `pytest` (bare command)
   
   **Reason:** Use `just test` for comprehensive testing including linting, formatting, and validation.

2. **GUI applications**
   - `python -m src.main`
   - `just run` variants
   
   **Reason:** Would crash Claude Code interface.

3. **Dangerous operations**
   - `sudo` commands
   - `rm -rf` operations
   - Force reinstalls
   - Permissive permissions (777)

### ✅ Allowed Exceptions

- `pytest --help`, `pytest --version`, `pytest --collect-only`
- `just test` (comprehensive test suite)
- Regular development commands
- Safe package management operations

## Adding New Validations

Edit `validate-command.sh` and add patterns:

```bash
# Add to the case statement or grep patterns
if echo "$COMMAND" | grep -qE 'new_dangerous_pattern'; then
    block "Reason why this is dangerous"
fi
```

## Testing Changes

Always run the test suite after modifications:

```bash
./test-command-validation.sh
./test-code-review-hook.sh
```

Add new test cases for any new validation rules.

## Code Review Hook

### `code-review-hook.sh`
Automated code analysis and review for modified files.

**Features:**
- **Python Analysis**: Uses tool-integration-matrix.py for comprehensive analysis
  - Pylint errors/warnings detection
  - Complexity analysis (radon)
  - Security issues (bandit)
  - Dependencies analysis
- **CSS/TCSS Analysis**: Uses css-analysis-tool.py for Textual CSS validation
  - TCSS-specific property validation
  - Complexity scoring
  - Textual framework compatibility
- **Multi-language Support**: JSON, YAML, JavaScript/TypeScript, Markdown
- **Non-blocking**: Always exits 0 (informational only)

**Usage:**
```bash
# Automatically triggered by PostToolUse hooks
# Manual testing:
export CLAUDE_FILE_PATHS="file1.py file2.tcss"
./code-review-hook.sh
```

**Integration:**
Added to `.claude/settings.json` as PostToolUse hook - runs automatically after Edit/Write/MultiEdit operations.

**Output Format:**
- ✅ Clean files
- ⚠️ Issues detected with counts
- 🔧 Analysis failures
- 📄 Unknown file types
- Enhanced analysis recommendations