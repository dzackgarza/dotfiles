# Project Goals

This project's mission is to create a new class of AI development tool that is radically transparent and extensible. The user experience is paramount and must directly reflect the underlying architecture, providing a clear, intuitive window into the AI's thought process.

## Overarching Vision: The Unix System's Intelligent Hub

This application is designed to be more than just a REPL; it is intended to be the central, intelligent hub of a Unix system. It will be a "home" – a genuinely fun and engaging place to spend time, fostering deep work in areas like mathematics research, coding projects, and general system organization.

Key aspects of this vision include:

-   **Aesthetic and Experience**: The UI will be colorful, mimicking terminal aesthetics, and designed to be genuinely enjoyable and productive. It aims to be as fundamental and constantly accessible as a terminal scratchpad, perhaps integrated via OS features like a Sway key-combo popup.
-   **Universal Entry Point**: It will serve as the primary interface for a vast array of tasks: initiating web searches, starting coding projects, organizing your system, conducting web research, carrying out pure mathematics research (finding theorems, proofs, definitions), indexing into your personal corpus, and providing a natural language interface to your terminal and entire system, abstracting away complex bash/git commands and man pages.
-   **Hyper-Optimized Multi-LLM Orchestration**: Most, if not all, of this functionality will be implemented through the plugin system, driven by a clever routing plugin. The system will seamlessly interface with potentially dozens of LLMs, hyper-optimizing for very specific tasks. This includes integrating with hard-coded augmentations, direct bash access, and external services like MCP servers.

## Core User Experience Pillars

1.  **The Sacred Timeline**: The user interface is a direct visualization of the Sacred Timeline, a persistent, append-only log of all actions. Every operation is rendered as a block, creating an immutable, transparent, and auditable history of the conversation. This is the foundation of the user experience.

2.  **The Sacred Turn Structure**: The conversation is organized into `[User] -> [Cognition] -> [Assistant]` turns. This predictable rhythm is the core interaction model. It is non-negotiable and provides a clear structure for both the user and the underlying system.

3.  **The Transparent Cognition Pipeline**: The `[Cognition]` block is the star of the show. It is not a black box. The user must see the multi-step pipeline of submodules executing in real-time. Each step must be animated, showing its name, the model/tool used, live timers, and streaming token counts, before finalizing and making way for the next. This provides an unprecedented level of transparency.

4.  **Rich Visual Output**: The application will prioritize beautiful and informative rendering of diverse content types. This includes:
    -   **Markdown**: Flawless and colorful rendering of standard Markdown.
    -   **Mathematics**: Seamless display of LaTeX-compatible mathematics (e.g., MathJax/KaTeX).
    -   **Code Blocks**: Syntax-highlighted code blocks for various languages.
    -   **Jupyter Notebook Cells**: Rich visual rendering of Jupyter input/output cells, including plots and other complex data types (leveraging MCP server data).
    -   **Diagrams**: Future support for rendering `tikzcd`, Mermaid, Graphviz, and other diagramming formats.
    -   **Deep Linking**: Interactive links to the filesystem (e.g., `xdg-open` for files, browser for URLs) and special visual representations for different MIME types (e.g., PDF icons).

5.  **Intelligent Input Handling**: The input box is a critical interaction point, designed for power and intuitiveness.
    -   **Multiline Input**: Full support for multiline text input.
    -   **Copy-Pasted Data**: Special provisions for copy-pasted data, intelligently attaching it to the input with unobtrusive visual cues (e.g., `[Pasted Data]` tag, separate illuminated input area). This data will be inscribed onto the Sacred Timeline in a principled way (e.g., fenced code blocks, intelligent recognition of terminal output).
    -   **Rich Clipboard Data (Horizon)**: Future support for rich clipboard data, such as PNG images from screen selections, once LLM APIs and rendering capabilities mature.

6.  **Live Streaming and Transparency**: All model responses will be streamed while in live states, providing real-time feedback. Thoughts and intermediate reasoning from LLMs will be streamed and, when applicable, inscribed onto the timeline, further enhancing transparency.

## Strategic Priorities

1.  **Priority 1: Implement the Core Experience**
    -   **Focus**: Build a stable, beautiful, and modern UI (GUI or TUI, *framework choice is secondary to the core experience*) that perfectly realizes the block-based timeline and the dynamic, transparent `Cognition` block pipeline.
    -   **Initial Plugins**: Develop the essential `User`, `Cognition`, and `Assistant` plugins, along with a `System/Bootup` plugin that performs heartbeat checks on all models required by other installed plugins.

2.  **Priority 2: Radical Extensibility & Safety**
    -   **Focus**: Solidify the plugin ecosystem.
    -   **Core Feature**: A `Plugin Validator` that strictly enforces the transparency and UI contracts, rejecting any plugin that could break the timeline's integrity or visual consistency. Plugins must be trivial to develop, test in isolation, and safely integrate.

3.  **Priority 3: Bootstrapping and Self-Improvement**
    -   **Focus**: Enable the system to write its own plugins.
    -   **Core Feature**: Develop a "coding" route within the `Cognition` pipeline that allows the AI to create, test, and validate new plugins against the `Plugin Validator`, enabling it to autonomously expand its own capabilities.

## Task Master AI Integration

This project now incorporates **Task Master AI** as a foundational project management and development workflow tool. Task Master provides:

### AI-Driven Development Workflow
- **Intelligent Task Generation**: PRD parsing into actionable, prioritized tasks
- **Dynamic Task Management**: Real-time reorganization and implementation drift handling
- **Research-Enhanced Planning**: Integration with AI research for current best practices
- **Natural Language Interface**: Claude Code integration for conversational task management

### Alignment with Sacred Timeline Architecture
Task Master's workflow mirrors our Sacred Timeline concept:
- **User Input**: Natural language task requests and status updates
- **AI Cognition**: Task Master's intelligent analysis, research, and planning
- **Assistant Response**: Concrete implementation guidance and next steps

### Current Project Integration
- ✅ 10 main tasks generated covering full Sacred GUI implementation
- ✅ Dependency-aware task structure matching our architectural priorities
- ✅ MCP integration with Claude Code for seamless AI collaboration
- ✅ Research mode enabled for staying current with development practices

### Meta-Development Capability
Task Master enables the project to be self-managing:
- Tasks evolve based on implementation learnings
- Future tasks automatically update when approaches change
- AI provides contextual guidance and research during development
- Progress tracking becomes part of the Sacred Timeline itself

This integration transforms development from linear task execution to dynamic, AI-enhanced project evolution, perfectly aligned with our vision of transparent, intelligent tooling.