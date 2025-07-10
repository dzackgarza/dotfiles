# AI Agent Context Rules

This document defines a set of rules and guidelines for AI agents that are working on this project. These rules are designed to ensure that AI agents make safe and effective contributions to the codebase, and to help them to work collaboratively with human developers.

## Core Principles

- **Safety First**: The safety and security of the project are of the utmost importance. AI agents should always prioritize safety and security in their work, and should never take actions that could compromise the integrity of the codebase or the security of the application.
- **Respect Existing Conventions**: AI agents should always respect the existing code patterns, conventions, and architectural decisions of the project. They should not make any changes that are inconsistent with the existing codebase, unless they have been explicitly instructed to do so.
- **Collaborate with Humans**: AI agents should work collaboratively with human developers, and should always be open to feedback and guidance. They should not make any major changes to the codebase without first consulting with a human developer.

## Guidelines for Making Changes

- **Read the Documentation**: Before making any changes to the codebase, AI agents should read the relevant documentation in this directory to ensure that they understand the project's architecture, goals, and code patterns.
- **Analyze the Existing Code**: AI agents should carefully analyze the existing code before making any changes. They should pay close attention to the surrounding code, tests, and configuration to ensure that their changes are consistent with the existing codebase.
- **Write Tests**: AI agents should write tests for all new code that they add to the project. They should also ensure that all existing tests pass before submitting their changes.
- **Run Linting and Type Checking**: AI agents should run the project's linting and type-checking tools to ensure that their changes are consistent with the project's coding standards.
- **Provide Clear and Concise Explanations**: When submitting their changes, AI agents should provide clear and concise explanations of the changes they have made. They should also explain why they have made these changes, and how they will benefit the project.

## Development Philosophy Requirements

AI agents must adhere to the following development philosophy when contributing to this project:

### Environment and Testing
- **Always use virtual environments** (venv, pdm, poetry) for dependency management
- **Run echo tests** that simulate the full user experience using the exact same code path as production
- **No test modes or special flags** - test the canonical user experience
- **Run all tests before declaring any feature complete**
- **Never skip linting or type checking** - these must pass before any code is considered ready

### Code Quality and Architecture
- **Fail fast and hard** - use assertions liberally to catch bugs early
- **Never use try-catch blocks** to hide failures - let errors surface immediately
- **When encountering bugs**, redesign the architecture to make the bug impossible rather than patching it
- **Keep modules under 500 lines** - refactor and redesign when approaching this limit
- **Ensure module independence** - developers shouldn't need to understand 15 other files to work on one module

### Coding Style
- **Use functional programming patterns**:
  - Replace nested if-then chains with principled logic routers
  - Use map/reduce/filter/collect and lambda constructions
  - Leverage list comprehensions and mathematical structures like sets
- **Employ strong typing** with Pydantic types wherever possible
- **Write code that proves its own correctness** through structure and assertions

### Version Control
- **Make atomic commits** with extensive, descriptive messages
- **If stuck, revert to the last working version** and rethink the approach
- **Document all design decisions** in commit messages and code comments
- **Never commit code that doesn't pass all tests and linters**

### Error Handling Philosophy
- **This is a development project, not production software**
- **Assume a frozen environment** where all dependencies are present
- **Crash on any missing dependency or failed assertion**
- **No graceful degradation** - if something is wrong, make it obvious immediately
- **Errors indicate design flaws**, not user mistakes