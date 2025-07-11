# V3.1 Ledgers: Critical Architectural Foundations First (Addressing Context Length & Reliability)

This document outlines the prioritized development ledgers for V3.1, with an aggressive focus on proving the viability and robustness of the block-based UI and its core interactions, particularly the management of 'live' vs. 'inscribed' blocks, *and explicitly addressing the LLM context window limitations and interaction reliability* using mocked data before proceeding with full feature implementation.

## Critical Architectural Foundations (Phase 1: UI & Core Logic Proof of Concept - *with Context Management Focus*)

These ledgers are paramount for proving the viability of the Sacred Timeline's block structure, proper formatting, full data transparency (live updates), and the extensibility of plugins, *while explicitly managing LLM context limits*.

1.  **`timeline.md` (Redesigned - Deep Dive into Live vs. Inscribed & Context Awareness):**
    *   **Focus:** This is the absolute top priority. It must explicitly define the "live" vs. "inscribed" block states, the mechanism for transitioning between them, and the concept of a "staging area" (e.g., a `LiveBlockManager` or `TransientBlockStore`) if deemed necessary for transient blocks. It should detail how wall times, token usage, and intermediate responses are handled for live blocks before inscription. **Crucially, it will now also integrate with context management to provide a view of the conversation that is both complete (for the user) and manageable (for the LLM).**

2.  **`memory-and-context-management.md` (Elevated to High Priority & Redesigned):**
    *   **Focus:** This ledger becomes central to solving the "conversation too long" problem. It will detail strategies for managing the LLM's context window, including:
        *   **Dynamic Context Pruning:** Automated methods (e.g., recency, relevance-based filtering, summarization of older turns) to select the most pertinent parts of the Sacred Timeline for the LLM's current context.
        *   **Accurate Token Counting:** Mechanisms for real-time token counting of both input and output to inform pruning decisions.
        *   **Contextualization for LLM:** How the selected context is formatted and presented to the LLM.

3.  **`streaming-live-output-system.md` (Elevated from V3.2):**
    *   **Focus:** Detail how data (including wall times, token usage, intermediate responses from LLMs and tools) is streamed and displayed for "live" blocks. This is crucial for the "transparency of ALL data" requirement and will work in conjunction with `timeline.md` to show blocks animating and updating in real-time.

4.  **`event-driven-communication.md` (Elevated from V3.2):**
    *   **Focus:** This is fundamental for how live updates from plugins and sub-modules are communicated to the UI and the `TimelineManager` without direct coupling. It's essential for managing the "live" state of blocks and ensuring smooth, responsive UI updates.

5.  **`plugin-system.md` (Redesigned - Emphasis on Nesting & Data Aggregation):**
    *   **Focus:** This ledger needs to detail how plugins can be nested (especially for the `CognitionPlugin` and its submodules). It must also cover how data (wall times, tokens, intermediate responses) from nested plugins/submodules is aggregated and presented at the parent (Cognition) block level. It should explicitly cover "external validation of plugins" to ensure only trusted components can interact with the system.

6.  **`intelligent-router-system.md` (Elevated from V3.2):**
    *   **Focus:** This is a core component of the "Cognition Block" and needs to be proven early. It will detail how user intent is routed to appropriate plugins/models, demonstrating the "extensibility and composability of plugins" and the "nesting of blocks and plugins."

7.  **`rich-content-display-engine.md`:**
    *   **Focus:** Remains high priority for proper formatting and animation of both inscribed and live blocks. This will be the visual proof of concept for the UI.

8.  **`testing-framework.md`:**
    *   **Focus:** Remains high priority, now with an explicit focus on testing the live vs. inscribed block transitions, data transparency, and the correct rendering of dynamic elements. **Crucially, it will also include tests for context pruning and token management.** Mocked data will be central to these tests.

9.  **`llm-routing-and-cognitive-plugins.md`:**
    *   **Focus:** Details the implementation of LLM-based routing and cognitive plugins, which are essential for the core functionality of the system.

10. **`intelligent-context-pruning.md`:**
    *   **Focus:** Specific strategies and mechanisms for intelligently pruning context to manage LLM token limits.

11. **`summarize-last-turns.md`:**
    *   **Focus:** Implementation of summarization techniques for older turns to reduce context length.

## Medium Priority (Phase 2: Core System Integration & Refinement - *with Context Management Solutions & Reliability*)

Once the UI foundation and core context management are solid, these ledgers focus on integrating core system components and refining the overall architecture, with an emphasis on reliability for LLM interactions.

12. **`sacred-timeline-persistence.md`:**
    *   **Focus:** This is crucial for ensuring the *entire* Sacred Timeline is preserved, even if only a subset is used for the LLM's active context. It enables long-term conversation history and future context retrieval.

13. **`graceful-rate-limit-handling.md` (Elevated from V3.3):**
    *   **Focus:** Essential for robust LLM integration. This will ensure that the system can reliably interact with LLM providers without being crippled by rate limits, which is critical for demonstrating the Cognition Block's functionality.

14. **`long-running-work-ledger-system.md` and `long-running-work-ledger-file-structure.md` (Elevated from V3.3 - Grouped):**
    *   **Focus:** If the "live" block concept needs to extend to very long-running operations that persist across sessions, these become relevant. They will define how such operations are tracked and stored, potentially impacting `sacred-timeline-persistence.md`.

15. **`manual-context-re-injection.md`:**
    *   **Focus:** Provides the user with explicit control over the context. This is a direct countermeasure to the "conversation too long" problem from the user's perspective, allowing them to manually select specific turns or summarized sections to re-introduce into the LLM's context.

16. **`core-ui-ux.md`:** Overall UI/UX principles.
17. **`input-system.md`:** Stable input.
18. **`llm-integration-foundation.md`:** Basic LLM integration (mocked).
19. **`command-system.md`:** Command processing.
20. **`input-history-and-completion.md`:** Input enhancements.
21. **`ui-navigation-principles.md`:** More advanced UI navigation.
22. **`notification-strategy.md`:** How the user is notified of events.

## Lower Priority (Phase 3: Advanced Features & Robustness)

These can come later, once the core system is stable and proven.

23. **`safety-and-robustness.md` (Redesigned):** Error handling and checkpointing.
24. **`live-block-query-handling.md`:** Handling live queries within blocks.
25. **`double-ctrl-c-exit.md`:** Exit UX.
26. **`elia-integration.md`:** Integration with external systems.
27. **`debug-console-logging.md`:** Debugging tools.
28. **`automated-tool-error-recovery.md`:**
    *   **Focus:** Strategies for automatically recovering from tool execution errors.

29. **`research-and-search-tools.md`:**
    *   **Focus:** Integration of research and search capabilities as plugins.

30. **`user-provided-knowledge-base.md`:**
    *   **Focus:** Allowing users to provide their own knowledge bases for the AI.

31. **`code-quality-plugin.md` (from V3.3):** Feature for code quality.
32. **`debugging-plugin.md` (from V3.3):** Feature for debugging.
33. **`dependency-management-plugin.md` (from V3.3):** Feature for dependency management.
34. **`multimodal-support.md` (from V3.3):** Feature for multimodal LLM interactions.
35. **`sacred-timeline-git-integration.md` (from V3.3):** Advanced persistence feature.
36. **`testing-plugin.md` (from V3.3):** Feature for running tests.