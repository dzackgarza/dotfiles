# Project Brief: LLM REPL - The Unix System's Intelligent Hub

## Overarching Vision

This project aims to create a new class of AI development tool: an interactive terminal research assistant with a transparent AI cognition pipeline. It is envisioned as the central, intelligent hub of a Unix system, fostering deep work in mathematics, coding, and system organization.

## Core User Experience Pillars

1.  **The Sacred Timeline**: A persistent, append-only log of all actions, visualized as blocks, providing immutable and transparent history.
2.  **The Sacred Turn Structure**: A non-negotiable `[User] -> [Cognition] -> [Assistant]` conversation rhythm.
3.  **The Transparent Cognition Pipeline**: The `[Cognition]` block is not a black box; its multi-step submodules (with live timers, token counts, and streaming output) are visible in real-time.
4.  **Rich Visual Output**: Flawless and colorful rendering of Markdown, LaTeX, code blocks, Jupyter cells, and diagrams.
5.  **Intelligent Input Handling**: Multiline input with smart handling of copy-pasted data and future support for rich clipboard data.
6.  **Live Streaming and Transparency**: Real-time streaming of all model responses and intermediate AI reasoning.

## Strategic Priorities

1.  **Implement the Core Experience**: Build a stable, beautiful, and modern UI realizing the block-based timeline and transparent `Cognition` pipeline. Develop essential `User`, `Cognition`, `Assistant`, and `System/Bootup` plugins.
2.  **Radical Extensibility & Safety**: Solidify the plugin ecosystem with a `Plugin Validator` enforcing transparency and UI contracts.
3.  **Bootstrapping and Self-Improvement**: Enable the system to write its own plugins through a "coding" route within the `Cognition` pipeline.
