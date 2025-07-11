
# Ledger: LLM Routing and Cognitive Plugins

**Goal:** To implement a sophisticated system for intelligently routing user prompts to the most appropriate LLM and executing specialized cognitive tasks using optimized models, ensuring efficiency, accuracy, and transparency.

## 1. Core Philosophy

- **The Central Nervous System:** This system acts as the brain of the "Cognition" block, making the initial decision on how to process a user request.
- **Intent-Based Routing:** Routing decisions should be based on the user's underlying intent, not just keywords.
- **Dynamic and Extensible:** The router must be able to learn about new tools and models as they are added to the system.
- **Task-Specific Optimization:** Route specific cognitive tasks to optimal models across local, free-tier, and paid endpoints to maximize performance while managing costs.

## 2. Core Functionality

### 2.1. Intelligent Tool Router Plugin

#### Feature

- A core cognitive plugin that analyzes the user's prompt and intelligently routes it to the most appropriate tool or a chain of tools.

#### Implementation Details

1.  **Tool Registration Awareness:** The router will have access to the `ToolRegistry` (from the `plugin-system.md` ledger) and use tool names, descriptions, and parameter schemas.
2.  **LLM-Powered Routing Logic:** Use a fast and efficient LLM to perform the routing, prompting it with the user's prompt, available tools, and instructions to choose the best tool or respond directly.
3.  **Output Format:** Output a structured format (e.g., JSON) specifying the plan (tool name, parameters).
4.  **No-Tool Fallback:** If no tool is appropriate, indicate that a direct chat response is best.

### 2.2. Model Task Optimization and Routing

#### Feature

- Implement differential model routing based on comprehensive task performance analysis, routing specific cognitive tasks to optimal models across local, free-tier, and paid endpoints.

#### Implementation Details

1.  **Task Categories and Optimal Models:** Define task categories (e.g., Instruction Processing, Validation, Cognitive Operations) and map them to optimal local, free-tier, and paid models based on performance benchmarks.
2.  **Routing Logic:** Implement a `TaskRouter` that selects the best model based on task type, complexity, and budget (local-only, free-tier, paid).
3.  **Provider Integration:** Integrate with various LLM providers (Google Gemini, Groq, Hugging Face, Mistral AI, OpenRouter, Claude, GPT) and manage their API keys and rate limits.

### 2.3. Ollama-Optimized Cognitive Plugins

#### Feature

- Implement specialized sub-cognitive plugins, each optimized for a specific task using the most viable local Ollama model.

#### Implementation Details

-   **Instruction Processing Plugins:**
    -   Instruction Routing (Nous Hermes 2 Mistral 7B Q)
    -   Instruction Rewriting (OpenHermes 2.5 Mistral 7B Q)
    -   Capability-Based Routing (MythoMax L2 13B Q)
    -   Prompt Amplification (LM Studio 7B (Quantized))
    -   Query Expansion (Neural Chat 7B Q)
    -   Instruction Decomposition (Phi-4 Mini (Quantized))
-   **Validation and Quality Control Plugins:**
    -   Tool Use Formatting Validation (Llama 3 8B (Quantized))
    -   Response Structure Assessment (Mistral 7B (Quantized))
    -   Format Correction (Faraday 7B (Quantized))
    -   Query-Result Alignment (Falcon 7B (Quantized))
    -   Intent-Result Consistency (OpenChat 3.5 Q)
    -   Redundancy/Contradiction Detection (OobaGPT 7B (Quantized))
-   **Cognitive Operations Plugins:**
    -   Rationale Generation (Grok 1.5 (Quantized))
    -   Task Triage (Command R+ (Quantized))
    -   Simple Classification (Starling-LM 7B Alpha Q)
    -   Summarization (Falcon 7B (Quantized))
    -   Error/Quality Scoring (Command R+ (Quantized))
    -   Parameter Extraction (Mistral 7B (Quantized))
    -   User Feedback Integration (LM Studio 7B (Quantized))
    -   Todo Planning (Phi-3.5 Mini (Quantized))

## 3. Advanced Features

-   **Multi-Tool Chaining:** The router should be able to create plans that involve multiple tool calls in sequence.
-   **Self-Correction:** If a tool call fails, the router could be invoked again to choose an alternative tool or to modify the parameters.
-   **Learning:** The router could learn from user feedback to adjust its future decisions.
-   **Confidence Scoring:** Add confidence scoring for intent detection.
-   **Multi-Intent Queries:** Support queries that involve multiple intents.
