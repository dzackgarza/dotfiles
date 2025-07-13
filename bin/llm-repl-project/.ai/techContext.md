# Tech Context: LLM REPL - Technologies and Development Setup

## Technologies Used

This project leverages the following key technologies and frameworks:

*   **Python**: The primary programming language for the application logic and backend.
*   **Textual**: A powerful Python framework for building Text User Interfaces (TUIs), used for the Sacred GUI Architecture.
*   **PDM**: Python Development Master, used for dependency management and project environment setup.
*   **LLM Providers**: Integration with various Large Language Models (LLMs) for AI cognition and response generation (e.g., tinyllama, phi-3.5, deepseek, claude, as referenced in the cognition pipeline).
*   **Git**: For version control and repository management.

## Development Setup

### Python Environment Management with PDM

All Python-related commands (running the application, tests, linting) **MUST** be prefixed with `pdm` to ensure the project's virtual environment is used. This is a critical operating rule.

*   **Installation**: Ensure PDM is installed (`pip install pdm`).
*   **Dependency Installation**: `pdm install` to set up the project dependencies from `pyproject.toml` and `pdm.lock`.
*   **Running Commands**: `pdm run python <script.py>`, `pdm run pytest`, `pdm run lint`.

### Project Structure

The project follows a structured directory layout:

*   `src/`: Contains the main application source code, including widgets and services.
*   `.ai/`: The new Memory Bank directory, containing core documentation and agent guidelines.
*   `tests/`: Houses all testing-related files.
*   `scripts/`: Utility scripts, including `block-gui-commands.sh`.
*   `V3/`: Reference implementation for proven Textual patterns.

## Technical Constraints

*   **No GUI Applications**: The agent is strictly forbidden from running GUI applications, as this breaks the Claude Code interface. All testing and execution must be static or TUI-based.
*   **Immutable GUI Architecture**: The Sacred GUI Architecture (three-area layout) is immutable and must be adhered to without deviation.
*   **Test-First Development**: All code changes require a corresponding failing test first.
*   **Build from Working Code**: New implementations must copy patterns from existing, proven working code (e.g., V3, Gemini CLI, Claude Code) rather than reinventing solutions.

## Dependencies

Dependencies are managed via PDM. The `requirements.txt` file (or `pyproject.toml` in a PDM project) lists the necessary packages. Key dependencies include:

*   `textual` (for TUI development)
*   `pytest` (for testing)
*   `rich` (for rich text in terminal)
*   `pydantic` (for data validation, if used)
*   `httpx` (for async HTTP requests, if used for LLM APIs)

## Tool Usage Patterns

*   **Shell Commands**: Use `run_shell_command` for executing shell commands, with a clear description of purpose and potential impact.
*   **File Operations**: Prefer specialized tools like `read_file`, `write_file`, `list_directory`, `search_file_content`, `glob`, and `replace` over generic shell commands (`cat`, `grep`, `ls`).
*   **Web Interaction**: Utilize `google_web_search`, `brave_web_search`, `tavily-search`, and `firecrawl_scrape` for web-based information retrieval.
*   **Memory Management**: Use `save_memory` for persistent user-specific facts.
*   **Sequential Thinking**: Employ `sequentialthinking` for complex problem-solving and planning.
