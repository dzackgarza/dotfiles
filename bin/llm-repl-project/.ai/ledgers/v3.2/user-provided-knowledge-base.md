
# Ledger: User-Provided Knowledge Base and Fact Injection

**Goal:** To enable users to provide a persistent, structured knowledge base or specific facts that the AI can always refer to for grounding its responses, ensuring accuracy and consistency with user-specific information.

## 1. Core Philosophy

- **Grounding:** Ensure AI responses are grounded in user-provided truths, preventing hallucinations or inconsistencies with personal data.
- **Personalization:** Allow the AI to be aware of and utilize user-specific information, preferences, and domain knowledge.
- **Control:** Give users direct control over the facts and knowledge the AI operates with.

## 2. Core Functionality

### 2.1. Knowledge Base Storage

#### Feature

- A persistent storage mechanism for user-provided facts and knowledge, separate from the conversational timeline.

#### Implementation Details

-   **Format:** Store knowledge in a structured, human-readable format (e.g., YAML, Markdown with specific tags, or a simple SQLite table).
-   **Location:** A dedicated file or directory (e.g., `~/.llm_repl/knowledge_base.yaml` or `~/.llm_repl/facts/`).
-   **Categorization:** Allow users to categorize facts (e.g., `personal_info`, `project_details`, `domain_knowledge`).

### 2.2. Fact Injection Commands

#### Feature

- Commands to allow users to add, remove, or update facts in their knowledge base.

#### Implementation Details

-   **`/fact add <category> <key> <value>`:** Adds a new fact (e.g., `/fact add personal_info my_name "John Doe"`).
-   **`/fact remove <category> <key>`:** Removes a fact.
-   **`/fact show [category]`:** Displays facts from a specific category or all facts.
-   **`/fact load <file_path>`:** Load facts from a local file.

### 2.3. AI Access and Retrieval

#### Feature

- The AI will have access to the user-provided knowledge base and will retrieve relevant facts to augment its prompts.

#### Implementation Details

-   **Integration with RAG:** The knowledge base will be integrated with the RAG system (from `memory-and-context-management.md`). Facts will be indexed and retrieved based on semantic similarity to the current query.
-   **Prioritization:** Facts from the user-provided knowledge base will be given high priority in context injection.
-   **LLM Instruction:** The LLM will be explicitly instructed to refer to the provided facts and to prioritize them over its general training data when conflicts arise.

## 3. Advanced Features

-   **Fact Validation:** The AI could ask clarifying questions if a new fact contradicts existing knowledge.
-   **Natural Language Fact Addition:** Allow users to add facts in natural language, with the AI extracting structured data.
-   **Knowledge Graph:** Represent facts as a knowledge graph for more sophisticated reasoning.
-   **Privacy Controls:** Allow users to mark certain facts as private or sensitive.
