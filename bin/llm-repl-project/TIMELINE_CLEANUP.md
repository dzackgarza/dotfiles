# Timeline Cleanup: Remove Raw Prompt Display

## Problem
The timeline was showing redundant information:
```
> Hello                                    <- Raw prompt line (unwanted)
╭────────── 🔧 User_Input ✅ (0.0s) ──────╮
│ > Hello                                 │  <- Plugin box (wanted)
╰─────────────────────────────────────────╯
```

## Solution
Implemented automatic clearing of the raw prompt line while preserving the User_Input plugin in the timeline for conversation history.

## Key Changes

### 1. **Input System Enhancement** (`src/ui/input_system.py`)
- Added `erase_when_done=True` to PromptSession
- Implemented automatic line clearing after input completion
- Uses ANSI escape sequences to clear the displayed prompt

### 2. **Maintained Timeline History** 
- User_Input plugin stays in timeline for conversation history
- Contains the proper formatted input with "> " prefix
- Shows timing, token counts, and metadata

### 3. **Clean Visual Flow**
```
╭───────── 🔧 System_Check ✅ (0.2s) ──────╮
│ ✅ Intent Detection LLM: Online         │
│ ✅ Main Query LLM: Online               │
╰──────────────────────────────────────────╯
╭────────── 🔧 User_Input ✅ (0.0s) ───────╮
│ > Hello                                 │  <- Only this line shows
╰─────────────────────────────────────────╯
╭───── 🔧 Assistant_Response ✅ (0.0s) ────╮
│ Response content...                     │
╰─────────────────────────────────────────╯
```

## Technical Implementation

### Input Flow
1. **Prompt Display**: PromptSession shows "> " prompt
2. **User Types**: Input is captured with multiline support  
3. **Submit**: User presses Enter to submit
4. **Clear Raw**: ANSI sequences clear the raw prompt lines
5. **Process**: Input is processed and User_Input plugin created
6. **Timeline**: Only the plugin box appears in timeline

### Line Clearing Logic
```python
# Clear the input lines after getting the result
if result and result.strip():
    lines_to_clear = result.count('\n') + 1
    for _ in range(lines_to_clear):
        sys.stdout.write('\033[1A\033[2K')  # Move up and clear line
    sys.stdout.flush()
```

### Multiline Support
- Correctly calculates number of lines to clear
- Handles both single-line and multiline input
- Preserves multiline formatting in the plugin

## Benefits

### 1. **Clean Timeline**
- No duplicate input display
- Professional appearance
- Better visual hierarchy

### 2. **Preserved History**
- User_Input plugins maintain conversation log
- Timeline shows complete interaction history
- Proper metadata tracking (timing, tokens, etc.)

### 3. **Better UX**
- No visual pollution
- Clear separation between input capture and display
- Consistent with terminal best practices

### 4. **Multiline Support**
- Proper handling of multiline input
- Clean clearing regardless of input length
- Preserved formatting in timeline

## Configuration Compatibility
Works with all existing configurations:
- `debug`: ollama/tinyllama for both providers
- `mixed`: ollama for intent, groq for main query  
- `fast`: groq for both providers

## Testing
The cleanup maintains all existing functionality while improving the visual presentation:
- User_Input plugin tests still pass
- Timeline shows proper conversation history
- No loss of functionality
- Better user experience

This resolves the raw prompt pollution issue while maintaining the important conversation history in the timeline through the User_Input plugin system.