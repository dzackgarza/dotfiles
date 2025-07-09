### **Gemini-CLI Research Assistant: Feature Roadmap**

#### **Core Experience & Foundation**
- [x] Rich Terminal Rendering: Implement support for rendering Markdown, tables, syntax-highlighted code, and LaTeX directly in the terminal.
- [x] Advanced Input: Add a multi-line input mode for long prompts and context-aware autocompletion for commands and arguments.
- [x] Streaming Responses: Display LLM responses token-by-token for improved responsiveness.
- [x] Persistent SQLite History: Save command history to a local database for persistence and full-text search across sessions.
- [x] Full Session Management: Implement commands to save, load, list, and fork chat sessions, preserving history, settings, and context.
    - [x] CLI command for history search (e.g., \history_search <query>) to retrieve messages from persistent history.
    - [x] CLI commands \save, \load, \list_sessions, \fork implemented and tested. All tests pass as of this milestone.
- [ ] **Provider/Model Interchangeability & Local Model Testing:**
    - [ ] Refactor the REPL to allow switching between Gemini and local models (e.g., Ollama tinyllama) at runtime.
    - [ ] Switch test suite to use local Ollama tinyllama model for all tests, ensuring no dependency on external APIs for CI and development.
- [ ] **Ollama Integration as Default:**
    - [ ] Integrate Ollama (tinyllama or similar) as the default provider for the REPL, with Gemini and others as optional backends.
    - [ ] Ensure all features and tests work out-of-the-box with Ollama, requiring no external API keys or network access for local use.

#### **Integration Layer**
- [ ] Deep Jupyter Integration:
    - [ ] Connect to a running Jupyter kernel for sandboxed code execution.
    - [ ] Send code blocks from the LLM or user to the kernel for evaluation.
    - [ ] Maintain a persistent variable state within the kernel for the session's duration.
    - [ ] Capture and display rich outputs like Matplotlib plots directly in the terminal or as saved files.
- [ ] Mathematical Computation Protocol (MCP) Server Compatibility:
    - [ ] Integrate a local SymPy engine for fast, accurate symbolic mathematics (\sympy).
    - [ ] Add support for connecting to a SageMath server for advanced mathematical domains (\sage).
    - [ ] Integrate with the Wolfram|Alpha API for natural language computation and curated data (\wa).
    - [ ] Integrate with OpenMemory

#### **Intelligence and Research Workflow**
- [ ] Natural Language Command Layer:
    - [ ] Use a preliminary LLM call to screen user input for "intent" to run a built-in command.
    - [ ] Automatically dispatch to the correct function (e.g., changing models, exporting chat) based on the user's natural language request, instead of requiring explicit \ commands.
- [ ] Automated Prompt Optimization:
    - [ ] Implement an optional pre-processing step that uses an LLM to refine and enhance the user's prompt.
    - [ ] This "meta-prompt" will be tailored to the specific model in use to improve the quality and rigor of mathematical responses.
- [ ] PDF Corpus Management (RAG):
    - [ ] Add commands to ingest a corpus of PDF research papers into a local vector database.
    - [ ] Automatically retrieve and inject relevant text chunks from the corpus into the context for every prompt.
    - [ ] Allow explicit searching and querying of the loaded research papers.

#### **Advanced Extensibility & Self-Modification**
- [ ] LLM-Driven Self-Extensibility:
    - [ ] Create a \def_cmd command that takes a natural language description and uses an LLM to generate the Python code for a new command.
- [ ] Sandboxed Execution & Iteration:
    - [ ] Execute newly generated command code in a secure, sandboxed environment to prevent system instability.
    - [ ] If the code fails, automatically feed the error message back to the LLM to get a corrected version, iterating until the command runs successfully.
- [ ] Hot-Reloading and Plugin Management:
    - [ ] Dynamically load custom commands from a user-managed plugin directory without restarting the REPL.
    - [ ] Implement a command lifecycle to promote stable, user-verified commands for more trusted execution (\promote_cmd).

## Milestone: Add TinyLlama (Ollama) Backend Integration

### Scaffold Strategy
- Implement a pluggable LLM backend system in the REPL, supporting both Gemini and TinyLlama (via Ollama API).
- Add a `--backend` CLI flag and/or `\model` command to select between Gemini and TinyLlama.
- Implement a minimal TinyLlama backend using Ollama's local API (http://localhost:11434).
- Ensure all user prompts can be routed to either backend, with identical session and message handling.
- No changes to session management or history format.

### Success Criteria
- User can select TinyLlama as the backend at startup or via command.
- Prompts sent to TinyLlama return real, plausible LLM completions (not stubs or no-ops).
- At least one test sends a prompt to TinyLlama and verifies a non-empty, non-error response.
- Adversarial test: If Ollama is not running, error is handled gracefully and reported to the user.
- Gemini backend remains fully functional and selectable.

### Validation Steps
- Run REPL with Gemini: verify Gemini completions as before.
- Run REPL with TinyLlama: verify completions are from TinyLlama (Ollama logs or unique output).
- Run test suite with Ollama running: all LLM tests pass for both backends.
- Run test suite with Ollama stopped: TinyLlama backend reports error, does not hang or crash.
- Inspect code: ensure no stubs, no-ops, or fake completions for TinyLlama path.

### Adversarial Review
- Attempt to fake TinyLlama completions (e.g., by returning hardcoded strings): test must fail.
- Attempt to select a non-existent backend: error is reported, REPL does not crash.
- Attempt to switch backends mid-session: session and message history remain consistent.

### Capabilities Unlocked
- True multi-backend LLM support (Gemini + TinyLlama/Ollama).
- Foundation for adding more LLMs in the future.
- Adversarially robust, testable backend selection and LLM routing.

### Knowledge Gaps Filled
- How to integrate and test local LLMs (Ollama) in the REPL.
- How to design backend-agnostic LLM interfaces for future extensibility.

**Status:** Not started. No code for TinyLlama/Ollama exists as of this milestone definition.

## Milestone Tests: Research Assistant Efficacy (Baseline Suite)

### 1. Math Reasoning Prompt Engineering
- **Example:** Given "Solve for x: 2x^2 - 3x + 1 = 0", the assistant must:
  - Generate a step-by-step solution using a structured prompt.
  - Output the answer in LaTeX with a boxed value.
  - Optionally verify the answer using SymPy or Sage.
- **Success:** Output is stepwise, labeled, boxed in LaTeX, and verified correct.

### 2. Compute Aut(G) in SageMath
- **Example:** For G = SymmetricGroup(4), the assistant must:
  - Write SageMath code to compute Aut(G).
  - Run the code and output the result.
- **Success:** Output matches Sage's built-in Aut(G) for the example group.

### 3. Compute v^perp/v for Isotropic Vector in Lattice
- **Example:** For L = QuadraticForm(ZZ, 2, [0,1,1,0]), v = (1,0), the assistant must:
  - Use personal Sage code to compute v^perp/v.
- **Success:** Output matches expected quotient lattice structure.

### 4. PDF Collection Theorem Retrieval
- **Example:** Given a query like "modular forms and Hecke operators", the assistant must:
  - Index the PDF collection.
  - Return 3-5 relevant theorems (with citation and page number).
- **Success:** Output contains 3-5 correct, relevant theorems with citations.

### 5. Open Paper by Natural Language
- **Example:** Given "the original Nikulin paper on discriminant forms", the assistant must:
  - Use the corpus and Zotero BibTeX file to open the correct PDF.
- **Success:** The correct paper is opened and its citation is displayed.

### 6. Scaffold Sub-Project Directory
- **Example:** For project "my-new-project", the assistant must:
  - Scaffold a directory with {docs, src, logs, README.md, CHANGELOG.md, ROADMAP.md, justfile, pdm/nvm config}.
- **Success:** Directory structure and files are created as specified.

### 7. SageMath-Jupyter MCP Programming
- **Example:** "Compute the first 10 primes" via SageMath-Jupyter MCP.
  - The assistant must write, run, and debug the program until correct.
- **Success:** Program runs and outputs the correct result after debugging.
