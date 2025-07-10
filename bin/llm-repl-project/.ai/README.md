# AI Agent README

This directory contains the guiding principles and architectural documentation for the project. As an AI agent contributing to this codebase, you are expected to understand and adhere to these documents.

## Core Mission

The primary goal is to build a modular, timeline-centric AI tool that can orchestrate a variety of local and remote language models. The long-term vision is for the system to be able to bootstrap its own development by creating and validating its own plugins.

## How to Use This Directory

Before making any changes, review the following documents to understand the project's philosophy and structure:

-   **`architecture.md`**: Describes the plugin-driven, UI-agnostic architecture. The timeline is the central data structure.
-   **`project.md`**: Outlines the strategic priorities, from building a usable, transparent tool to enabling self-improvement.
-   **`patterns.md`**: Explains the core design patterns, coding conventions, and development philosophy including:
    -   Plugin system patterns and contracts
    -   Proof-based development practices
    -   Testing philosophy (echo tests, no test modes)
    -   Type checking and linting requirements
    -   Functional programming style guidelines
-   **`context-rules.md`**: Defines the rules of engagement for AI agents working on this project.
-   **`ledgers/`**: Contains feature specifications and tracking:
    -   `_active.md`: Dashboard of active features
    -   `_template.md`: Template for new feature ledgers
    -   `roadmap.md`: Future development phases and vision
-   **`provider-benchmarks.md`**: Comprehensive performance data for model selection and task optimization
-   **`available-api-models.md`**: Current models available through our API keys
-   **`ollama-setup.md`**: Local model download and configuration guide
-   **`wrinkl-rules.md`**: Specific guidelines for the wrinkl context management system

Your contributions should always align with the principles laid out in these documents. The focus is on building a robust, extensible, and eventually, self-improving system.
