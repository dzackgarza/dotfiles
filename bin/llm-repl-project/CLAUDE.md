# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this LLM REPL project.

## Project Overview

LLM REPL - An interactive terminal-based research assistant with plugin-based architecture. Provides transparent AI-powered interface for research tasks with multi-LLM support (Ollama, Groq, Google Gemini).

## Core Philosophy

**The Sacred Timeline**: Append-only, immutable log of all operations. Every action is a block in the timeline.

**Sacred Turn Structure**: `[User] → [Cognition] → [Assistant]` - This rhythm is non-negotiable.

**Radical Transparency**: Users see the multi-step cognition pipeline in real-time with animations, timers, and token counts.

## Development Rules

### Coding Conventions
- **Always use virtual environments** (venv, pdm, poetry)
- **Fail fast and hard** - Use assertions liberally, no try-catch hiding
- **Echo tests only** - Test real user experience, no test modes
- **Functional style** - map/reduce/filter, no nested if-chains
- **Strong typing** - Pydantic types everywhere
- **Module limit** - Refactor at 500 lines
- **Run `just lint` before commits** - MyPy + Flake8 must pass

### Architecture Principles
- **Plugins are autonomous** - Each is self-contained
- **No bug fixing** - Redesign to make bugs impossible
- **Test canonical path** - Same code path as production
- **Crash on errors** - This is development, not production
- **Git discipline** - Atomic commits, revert if stuck

## Commands

### Run Application
```bash
just run          # Ollama/debug mode
just run-mixed    # Ollama intent + Groq queries  
just run-fast     # Groq everything
just install      # Install dependencies
```

### Testing
```bash
just test         # Full test suite
just lint         # Type checking
pytest tests/test_block_ordering.py -v  # Critical regression test
```

## Project Structure

```
src/
├── main.py               # Entry point
├── plugins/              # Plugin system
│   ├── base.py          # Interfaces
│   ├── registry.py      # Plugin manager
│   └── blocks/          # Core plugins
├── config/              # LLM configurations
└── timeline_integrity.py # Timeline guarantees

.ai/                     # Wrinkl documentation
├── project.md          # Vision & goals
├── architecture.md     # Technical design
├── patterns.md         # Code patterns & philosophy
├── context-rules.md    # AI agent guidelines
└── ledgers/           # Feature tracking
```

## Plugin System

### Core Plugins
- `SystemCheckPlugin` - LLM heartbeat validation
- `UserInputPlugin` - Input capture
- `CognitionPlugin` - Transparent processing pipeline
- `AssistantResponsePlugin` - Response formatting

### Plugin Rules
1. Extend `BlockPlugin` base class
2. Implement all abstract methods
3. Self-contained state management
4. Event-driven communication only
5. Test in isolation first

### Expected Block Sequence
```
[SystemCheck] → [Welcome] → [User: query] → [Cognition: pipeline] → [Assistant]
```

## Active Features

### Research Assistant Routing (In Progress)
- 3-layer intent detection: Rules → LLM → Default
- Routes: COMPUTE → Math, SEARCH → Literature, CODE → Code, CHAT → TinyLlama
- Display: `Assistant [Methodology: X, Intent: Y] → Agent (Mode)`

### Next Priority Features
- File context inclusion (@-commands)
- Slash commands system (/help, /quit, etc.)
- Shell integration with security
- Memory persistence across sessions

## Configuration Modes

- **debug**: Ollama/tinyllama (local)
- **mixed**: Ollama intent + Groq queries
- **fast**: Groq only (cloud)
- **test**: CI testing config

## Testing Philosophy

- **Echo tests** simulate full user interaction
- **No mocks** for core functionality
- **Proof-based** - Assert existence or crash
- **Regression guards** - Test before declaring done

## Git Workflow

- Feature branches from master
- Atomic commits with extensive messages
- Run tests and linting before commits
- Revert to last working if stuck

## Future Roadmap

1. **v3.1**: Tool execution foundation (Q1 2025)
2. **v3.2**: Continuation Passing Style - LLM ↔ Tool loops (Q2 2025)
3. **v3.3**: Multi-agent collaboration (Q3 2025)
4. **v4.0**: Production ready with enterprise features (Q4 2025)

## Model Performance Guidelines

We have API keys for 8 major providers. Use task-specific routing:

**Available APIs:**
- Gemini (60 RPM): `gemini-2.5-pro`, `gemini-2.5-flash`
- Groq (30-60 RPM): `llama-3.3-70b-versatile`, `deepseek-r1-distill`
- OpenRouter (10-30 RPM): `claude-4-opus`, `gpt-4.5-preview`
- DeepSeek (10-20 RPM): `deepseek-reasoner`, `deepseek-chat`

**Local Ollama Models:**
- Speed: `mistral:7b-instruct-q4_K_M`
- Tool Use: `llama3.1:8b-instruct-q4_K_M`
- Reasoning: `grok:1.5-7b-q4_K_M`

See `.ai/available-api-models.md` and `.ai/ollama-setup.md` for complete setup.

## Quick Reference

- Timeline is append-only and sacred
- Plugins must be autonomous
- Test the real user path only
- Fail fast, crash on errors
- Keep modules under 500 lines
- Route tasks to optimal models
- Document everything in git