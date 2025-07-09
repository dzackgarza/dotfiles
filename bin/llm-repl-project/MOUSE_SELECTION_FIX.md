# Mouse Selection Fix

## Problem
When the LLM REPL application was running, users couldn't drag and select text for copy-paste operations in the terminal. This is a common issue with interactive terminal applications.

## Root Cause
The issue was caused by `mouse_support=True` in the prompt_toolkit PromptSession and Application configurations. When mouse support is enabled, the application captures mouse events, preventing normal terminal text selection behavior.

## Solution
Disabled mouse support in both input system components to restore normal text selection functionality.

### Changes Made

#### 1. **SimpleMultilineInput** (`src/ui/input_system.py`)
```python
# Before
session = PromptSession(
    mouse_support=True,  # This captured mouse events
    ...
)

# After  
session = PromptSession(
    mouse_support=False,  # Allows normal text selection
    ...
)
```

#### 2. **MultilineInputBox Application** (`src/ui/input_system.py`)
```python
# Before
app = Application(
    mouse_support=True,  # This captured mouse events
    ...
)

# After
app = Application(
    mouse_support=False,  # Allows normal text selection
    ...
)
```

## Benefits

### ✅ **Restored Text Selection**
- Users can now drag to select text from any part of the terminal output
- Copy-paste functionality works normally
- Standard terminal selection behavior restored

### ✅ **No Functionality Loss**
- All keyboard shortcuts still work (Enter, Ctrl+J, Ctrl+C, Ctrl+D)
- Multiline input still fully functional
- All application features preserved

### ✅ **Better Terminal UX**
- Follows standard terminal application practices
- Users can copy system check results, LLM responses, etc.
- Better integration with terminal workflows

## Technical Details

### What Mouse Support Does
When `mouse_support=True`:
- prompt_toolkit captures mouse events
- Prevents terminal from handling text selection
- Can enable mouse-based interactions within the app
- Generally used for complex TUI applications

### Why We Disabled It
For the LLM REPL:
- We don't need mouse interactions within the input system
- Keyboard-based workflow is sufficient
- Text selection for copy-paste is more valuable
- Simpler and more predictable behavior

### Alternative Solutions Considered
1. **Conditional mouse support**: Enable only when needed
2. **Mouse region limiting**: Only capture in input areas
3. **Toggle functionality**: Allow users to toggle mouse capture

**Decision**: Complete disable was chosen for simplicity and better UX.

## Usage
Now users can:
- Select any text in the system check results
- Copy LLM responses for further use
- Select and copy conversation history
- Use normal terminal selection shortcuts

## Testing
- Application still functions normally
- All input methods work as expected
- Text selection works throughout the terminal
- No regression in functionality

This fix restores normal terminal behavior while maintaining all the enhanced input system features.