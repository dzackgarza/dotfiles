### 2.6. Persistent Operational Context (Addressing Agent Forgetfulness)

#### Problem Statement

Agents constantly forget the basic, fundamental aspects of what they're working on, e.g., that they are in a PDM-based project with a `venv`, falling back to training data and using `pip install`. This is a general failure in intelligence and context management, not a specific tooling/training failure, that we need to overcome. This leads to inefficient, incorrect, and frustrating interactions.

#### Feature

Ensure the LLM consistently retains and utilizes fundamental project-specific operational context (e.g., package manager, environment setup, common project paths, established conventions) throughout a session and across turns.

#### Implementation Plan
1. **Phase 1: Planning** - Review and plan implementation
2. **Phase 2: Implementation** - Core development work
3. **Phase 3: Testing** - Testing and validation
4. **Phase 4: UX Polish** - Final polish and user experience improvements
5. **Phase 5: Integration** - Integrate ledger into the main system

#### Implementation Details

-   **Explicit Context Injection:** Beyond `GEMINI.md`, ensure that critical, unchanging operational facts (e.g., "This is a PDM project," "Use `pdm run` for commands," "The virtual environment is managed by PDM") are consistently injected into the LLM's context, potentially as part of the system prompt or a high-priority context block.
-   **Contextual Reminders:** Implement mechanisms to automatically re-inject or highlight these core facts if the LLM's responses indicate a deviation from the established operational context (e.g., if it suggests `pip install` in a PDM project).
-   **Dynamic Context Updates:** If the project's operational context changes (e.g., switching from PDM to Poetry), ensure the system can update the LLM's understanding accordingly.
-   **"Grounding" Mechanisms:** Explore techniques to "ground" the LLM's understanding of the project environment, potentially by providing access to project configuration files (`pyproject.toml`, `.env`) or by summarizing their contents.
-   **User-Configurable Operational Facts:** Allow users to define and prioritize specific operational facts that the LLM should always remember for a given project.