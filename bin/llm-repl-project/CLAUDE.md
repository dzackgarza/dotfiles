# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an LLM REPL (Read-Eval-Print Loop) project - an interactive terminal-based research assistant that provides an AI-powered interface for various research tasks. The project supports multiple LLM providers (Ollama, Groq, Google Gemini) with intent-based routing to specialized agents.

## Key Commands

### Running the Application
```bash
# Run with Ollama (debug mode)
just run

# Run with mixed mode (Ollama for intent, Groq for queries)
just run-mixed

# Run with Groq for everything (fastest)
just run-fast

# Run directly with specific config
python src/main.py --config debug

# Show available configurations
python src/main.py --show-configs

# Install dependencies
just install
```

### Testing
```bash
# Run full test suite
just test

# Run block ordering tests (critical for regression detection)
pytest tests/test_block_ordering.py -v

# Run specific test files
pytest tests/test_integration.py
pytest tests/test_timing_and_race_conditions.py
pytest tests/quick_regression_tests.py

# Tests automatically clean history.db and __pycache__ before running
```

## Architecture

### Plugin-Based Block System (V3)

The project is built around a **plugin-based block system** where every piece of content displayed to the user is represented as an independent, self-contained plugin. This ensures:

1. **Independent plugins**: Each block is a completely autonomous plugin
2. **Plugin registry**: Dynamic discovery and instantiation of plugins
3. **Workflow composition**: Plugins can be composed into complex processing pipelines
4. **Extensibility**: New block types can be added without modifying core code
5. **Testable in isolation**: Each plugin can be developed and tested independently

#### Core Plugin Types
- **UserInputPlugin**: Handles user input capture and validation
- **SystemCheckPlugin**: Performs system validation checks
- **WelcomePlugin**: Displays welcome messages and system info
- **ProcessingPlugin**: Manages query processing pipeline
- **AssistantResponsePlugin**: Generates and formats assistant responses

#### Expected Block Order
For a basic query "Hello", the system MUST produce this exact sequence:
```
[SystemCheck] [Welcome] [User: Hello] [Internal Processing: [Intent Detection]->[Main Query]] [Assistant]
```

### Plugin-Based Architecture Structure

```
src/
├── main.py             # Main application entry point
├── plugins/            # Plugin system
│   ├── base.py         # Plugin interfaces and contracts
│   ├── registry.py     # Plugin manager and workflow system
│   └── blocks/         # Core block plugins
│       ├── user_input.py          # User input plugin
│       ├── system_check.py        # System check plugin
│       ├── welcome.py             # Welcome message plugin
│       ├── processing.py          # Query processing plugin
│       └── assistant_response.py  # Assistant response plugin
├── providers/          # LLM provider integrations
│   ├── base.py         # Provider interface
│   ├── ollama.py       # Ollama provider
│   ├── groq.py         # Groq provider
│   └── manager.py      # LLM manager
├── processing/         # Query processing utilities
│   ├── intent.py       # Intent detection
│   └── router.py       # Query routing
├── config/             # Configuration
│   └── llm_config.py   # LLM configurations
└── scrivener_v2.py     # Plugin-aware block record keeper

archive/
├── v1/                 # Original implementations
└── legacy/             # Migration utilities and old code
```

### Critical Architecture Rules

1. **Plugins are independent**: Each plugin is completely self-contained and autonomous.
2. **Plugin registry manages discovery**: All plugins are registered and discoverable via the registry.
3. **Workflow composition**: Complex processing is achieved by composing plugins into workflows.
4. **Plugin manager orchestrates**: The plugin manager handles lifecycles and inter-plugin communication.
5. **Extensibility without core changes**: New plugins can be added without modifying existing code.

### Plugin Lifecycle

```
INACTIVE → ACTIVE → PROCESSING → COMPLETED
```

- **INACTIVE**: Plugin is registered but not active
- **ACTIVE**: Plugin is active and ready to process
- **PROCESSING**: Plugin is currently executing
- **COMPLETED**: Plugin has finished processing

## Development Notes

### Plugin Development
- **Each plugin is independent**: Can be developed, tested, and deployed separately
- **Plugin interface compliance**: All plugins must implement the `PluginInterface`
- **Self-contained**: Plugins manage their own state, rendering, and lifecycle
- **Event-driven communication**: Plugins communicate via events through the plugin manager

### Creating New Plugins
1. Extend `BlockPlugin` base class
2. Implement required abstract methods (`metadata`, `_on_initialize`, `_on_activate`, etc.)
3. Register plugin with the plugin manager
4. Test plugin in isolation before integration

### Plugin Testing
- **Test plugins independently**: Each plugin can be tested without other components
- **Use mock dependencies**: Plugins should work with mocked external services
- **Test all lifecycle states**: Ensure proper state transitions
- **Verify rendering**: Test both live and inscribed render modes

### Common Pitfalls
- **Don't tightly couple plugins**: Each plugin should be autonomous
- **Always handle errors gracefully**: Plugin failures shouldn't crash the system
- **Register plugin classes, not instances**: The registry manages instances
- **Use plugin manager for lifecycle**: Don't manually manage plugin states

### Configuration System
- **debug**: Uses Ollama/tinyllama (local testing)
- **mixed**: Ollama for intent, Groq for main queries
- **fast**: Groq for everything (cloud-based)
- **test**: Groq-based for CI/testing

Configurations are in `src/config/llm_config.py`