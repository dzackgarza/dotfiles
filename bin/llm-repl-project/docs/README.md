# llm-repl-project

This directory is the canonical development scaffold for the `llm-repl` terminal project.

## Running the REPL

To start the REPL:

```bash
python llm-repl_v0.py
```

Or, if you have `just` installed:

```bash
just run
```

## Milestone-Based Development

Development proceeds via explicit, testable milestones. Each version is tracked in this directory, with clear documentation and validation for each step.

- **llm-repl_v0.py**: Initial scaffold, copied from the working REPL.
- **llm-repl_v1.py**: First milestone (to be defined and implemented).

## Testing

The non-interactive test harness (`test_llm_repl.py`) simulates user input and checks for the presence of code or numeric answers in the assistant's response. It does **not** require literal markdown code block delimiters (```...```) in the output, since the REPL displays formatted output and the LLM may or may not use code blocks depending on prompt and context.

**Test Environment Hygiene:**
- Before every test, the suite automatically deletes the persistent `history.db` file and all `__pycache__` directories. This ensures every test starts from a clean environment, preventing stale state or bytecode from affecting results.

## Session Management

The REPL now supports session management commands:

- `\save` — Save the current session (creates or updates the session in the database)
- `\load <session_id>` — Switch to a different session by ID
- `\list_sessions` — List all saved sessions
- `\fork <new_session_id>` — Fork the current session to a new session ID

These commands are available at the REPL prompt and are included in command autocompletion and help.

## How to Contribute

- Make changes incrementally, always keeping the scaffold in a working state.
- Document each milestone and its success criteria in the README.
- Use the justfile to standardize running and testing. 