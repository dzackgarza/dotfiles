# Ledger: Safety and Robustness Improvements

**Inspired by:** `gemini-cli`'s checkpointing and retry logic.

## 1. Filesystem Checkpointing and Restore

### Feature

- Implement a checkpointing system that saves the state of files before a tool modifies them.
- Provide a `/restore` command to revert file changes.

### Implementation Details

- **Checkpointing:**
    - Before any tool that modifies the filesystem (e.g., `write_file`, `edit`) is executed, create a checkpoint.
    - A checkpoint will consist of a copy of the original file(s) stored in a temporary location (e.g., `.ai/checkpoints`).
- **`/restore [id]`:**
    - If an `id` is provided, restore the files from that specific checkpoint.
    - If no `id` is provided, list all available checkpoints.
    - Checkpoints should be automatically cleaned up after a certain period of time.

## 2. Retry with Backoff and Model Fallback

### Feature

- Make our `CognitionProcessor` more robust by implementing a retry-with-backoff mechanism for API calls.
- Add a model fallback strategy to handle persistent errors.

### Implementation Details

- **Retry Logic:**
    - When an API call to an LLM fails with a transient error (e.g., 429, 5xx), retry the request with an exponential backoff.
- **Model Fallback:**
    - If an API call fails repeatedly, or if a specific type of error occurs (e.g., quota exceeded), automatically switch to a fallback model for the remainder of the session.
    - The fallback model should be configurable in `settings.json`.
    - Inform the user when a fallback occurs.

## 3. Explicit Error Handling and Timeline Recording

### Feature

- Implement a dedicated mechanism for handling errors that occur during any stage of the application's operation, particularly within the `TurnOrchestrator` and plugin execution.
- Ensure that all significant errors are explicitly recorded on the Sacred Timeline as `error` role `TimelineBlock`s, providing transparency and a historical record of system failures.

### Implementation Details

- **`ErrorReporterPlugin`:**
    - A specialized plugin (`src/plugins/error_reporter.py`) will be responsible for processing error information.
    - This plugin will capture details such as error type, message, traceback, and relevant context (e.g., the user input that led to the error).
    - It will format this information into a `TimelineBlock` with the `role="error"`.
- **Integration with `TurnOrchestrator`:**
    - The `TurnOrchestrator` will include a `try...except` block around its core `process_turn` logic.
    - Upon catching an exception, it will invoke the `ErrorReporterPlugin` to process the error.
    - The resulting `error` `TimelineBlock` will be added to the Sacred Timeline, ensuring that even system failures are part of the immutable record.
- **User Notification:**
    - The `ErrorReporterPlugin` or a related mechanism will also be responsible for presenting a user-friendly error message to the user, potentially suggesting next steps or indicating that an error has been logged.
- **Configurable Error Levels:**
    - Consider different levels of errors (e.g., warnings, critical errors) and how they are displayed and recorded.
    - Allow configuration for whether certain types of errors should halt execution or allow the system to continue.

```python
# src/plugins/error_reporter.py
import traceback
from src.plugins.base import BasePlugin
from typing import Any, Dict

class ErrorReporterPlugin(BasePlugin):
    name = "error_reporter"

    async def process(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "error_type": type(error).__name__,
            "message": str(error),
            "traceback": traceback.format_exc(),
            "context": context
        }

# Register the plugin (this would be done in a central plugin registration area)
# from src.plugins.manager import plugin_manager
# plugin_manager.register_plugin(ErrorReporterPlugin)
```
### Implementation Plan
1. **Phase 1: Planning** - Review and plan implementation
2. **Phase 2: Implementation** - Core development work
3. **Phase 3: Testing** - Testing and validation
4. **Phase 4: UX Polish** - Final polish and user experience improvements
5. **Phase 5: Integration** - Integrate ledger into the main system
