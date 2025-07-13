# Debug Mode for LLM REPL

## Overview

Debug Mode is a developer/tester feature that pauses LLM responses in the staging area for inspection before committing them to the timeline. This allows developers to:

- Inspect raw LLM output before it's finalized
- Take screenshots of intermediate states
- Debug the cognition pipeline
- Test edge cases without polluting the timeline

## How It Works

### Normal Mode (Default)
```
Input → Staging (Processing) → Timeline (Auto-inscribed)
```

### Debug Mode
```
Input → Staging (Processing) → Pause for Inspection → Manual Inscription → Timeline
```

## Enabling Debug Mode

### In Code
```python
from src.core.config import Config

# Enable debug mode
Config.enable_debug_mode()

# Disable debug mode  
Config.disable_debug_mode()
```

### In Configuration
```python
# src/core/config.py
DEBUG_MODE = True  # Enable debug mode by default
```

## Using Debug Mode

1. **Send a message** - Type your message and press Enter as normal
2. **Response pauses in staging** - The LLM response appears but stays in the staging area
3. **Visual indicators show debug state**:
   - Yellow separator: "📝 Debug Mode - Response Ready | Type /inscribe to commit"
   - Warning notification: "🔍 Debug Mode: Response ready for inspection"
4. **Inspect the response** - Review the staging area content, take screenshots, etc.
5. **Commit to timeline** - Type `/inscribe` or press `Ctrl+I` to save the response

## Visual Indicators

### Staging Separator
- **Normal Processing**: Blue separator showing "Turn N"
- **Debug Mode Ready**: Yellow separator showing debug instructions

### Notifications
- Warning-level notification when response is ready for inspection
- Success notification when inscription completes

## Commands

- `/inscribe` - Commit the staged response to the timeline
- `Ctrl+I` - Keyboard shortcut for inscription

## Architecture

The debug mode leverages the existing Sacred GUI two-state architecture:

### IDLE State (2-way layout)
```
┌─────────────────────────┐
│ Sacred Timeline (Top)   │
│ └── [conversation...]   │
├─────────────────────────┤
│ Input (Bottom)          │
└─────────────────────────┘
```

### PROCESSING State (3-way layout)
```
┌─────────────────────────┐
│ Sacred Timeline (Top)   │
├─────────────────────────┤
│ Live Workspace (Mid)    │ ← Debug mode keeps this visible
├─────────────────────────┤
│ Input (Bottom)          │
└─────────────────────────┘
```

## Implementation Details

- `Config.DEBUG_MODE` - Global toggle for debug behavior
- `UnifiedAsyncInputProcessor._pending_inscription` - Stores response data awaiting inscription
- `StagingSeparator.set_pending_inscription()` - Updates UI to show debug state
- `/inscribe` command parsing in `PromptInput` and `LLMReplApp`

## Use Cases

1. **LLM Output Inspection** - Review exact model responses before committing
2. **Screenshot Documentation** - Capture intermediate states for documentation
3. **Edge Case Testing** - Test problematic inputs without breaking the timeline
4. **Performance Analysis** - Measure processing times in staging area
5. **UI Development** - Test staging area widgets and animations

## Best Practices

- Remember to disable debug mode for normal usage
- Use `/inscribe` to commit valuable responses
- Clear staging area allows fresh inspection for each response
- Debug mode preserves the Sacred GUI's clean state transitions