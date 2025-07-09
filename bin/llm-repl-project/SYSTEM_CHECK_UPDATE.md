# System Check LLM Heartbeat Implementation

## Overview
The SystemCheckPlugin now performs actual LLM heartbeat checks to verify that configured LLM providers are online and responsive. This resolves the previous issue where system checks showed empty content.

## What Changed

### Before
- System check displayed empty content 
- No actual validation of LLM providers
- Tests passed but application showed empty system check blocks

### After  
- System check performs real LLM heartbeat checks
- Displays actual provider names, models, response times, and token counts
- Shows configuration-specific providers (ollama, groq, etc.)

## Features

### LLM Heartbeat Checks
The system check now includes:

1. **Provider Identification**: Shows the actual LLM provider (ollama, groq, etc.)
2. **Model Verification**: Displays the specific model being used
3. **Response Time**: Measures and displays actual response time
4. **Token Count**: Shows tokens used in the heartbeat request
5. **Status Indicators**: Clear ✅/❌ status for each provider

### Configuration Support
Different configurations show different providers:

- **debug**: `ollama/tinyllama` for both intent detection and main query
- **mixed**: `ollama/tinyllama` for intent, `groq/llama3-8b-8192` for main query  
- **fast**: `groq/llama3-8b-8192` for both providers

### Example Output
```
╭───────────────────────── 🔧 System_Check ✅ (0.2s) ──────────────────────────╮
│ ✅ Configuration: Configuration is valid                                     │
│ ✅ Dependencies: All dependencies are available                              │
│ ✅ Intent Detection LLM: ✅ ollama/tinyllama: Online (0.1s, 51 tokens)       │
│ ✅ Main Query LLM: ✅ groq/llama3-8b-8192: Online (0.1s, 51 tokens)          │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## Implementation Details

### New Check Type: `llm_heartbeat`
Added a new check type that:
- Creates minimal LLM requests ("Hi" message)
- Times the response
- Tracks token usage
- Handles timeouts gracefully
- Reports errors clearly

### Configuration Integration
The system check now:
- Loads LLM configuration based on `--config` parameter
- Creates separate heartbeat checks for intent detection and main query LLMs
- Passes LLM manager for actual provider communication

### Error Handling
Comprehensive error handling for:
- **Timeouts**: Shows timeout duration
- **Connection errors**: Shows specific error messages  
- **Missing configuration**: Shows clear error for missing LLM manager
- **Provider failures**: Displays provider-specific error details

## Testing
Added comprehensive test suite (`test_system_check_llm_heartbeat.py`) covering:
- Successful heartbeat checks
- Timeout scenarios
- Missing LLM manager
- Exception handling
- Multiple provider checks
- Render verification

## Resolution
This update resolves the original issue: "We didn't catch the fact that 'System Check' is empty" by:

1. **Providing actual content**: System check now shows meaningful information
2. **Real validation**: Performs actual LLM provider checks instead of placeholders
3. **Configuration accuracy**: Shows the exact providers and models configured
4. **Test coverage**: Tests verify both mock and real behavior consistency

The system check is no longer empty and provides valuable startup validation information.