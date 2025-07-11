
# Ledger: Interactive Clarification and Ambiguity Resolution

**Goal:** To enable the AI to identify ambiguous user requests or missing information and proactively ask clarifying questions, ensuring it accurately understands the user's intent before proceeding.

## 1. Core Philosophy

- **Proactive Engagement:** The AI should take initiative to resolve ambiguities rather than making assumptions or failing silently.
- **Efficient Interaction:** Minimize back-and-forth by asking precise and helpful clarifying questions.
- **User Guidance:** Guide the user towards providing clear and complete requests.

## 2. Core Functionality

### 2.1. Ambiguity Detection

#### Feature

- The AI will detect ambiguity or missing information in user prompts that prevent it from confidently executing a task or generating a response.

#### Implementation Details

-   **LLM-Powered Detection:** A dedicated LLM (from `llm-routing-and-cognitive-plugins.md`, potentially a smaller, fast model) will analyze the user's prompt and compare it against known tool schemas, common task patterns, and past interactions.
-   **Confidence Scoring:** The LLM will output a confidence score for its understanding of the user's intent. If the score is below a threshold, clarification is triggered.
-   **Missing Parameter Identification:** For tool calls, identify missing required parameters or ambiguous values.

### 2.2. Clarifying Question Generation

#### Feature

- When ambiguity is detected, the AI will generate precise and actionable clarifying questions for the user.

#### Implementation Details

-   **Question Formulation:** The LLM will generate questions based on the identified ambiguity. Examples:
    -   "Could you please specify which file you'd like me to edit?"
    -   "Are you asking for a summary of the entire document or a specific section?"
    -   "By 'fix the code', do you mean refactor for readability, debug a specific error, or optimize performance?"
-   **Contextual Questions:** Questions will be tailored to the specific context of the ambiguity.

### 2.3. Interactive Clarification Loop

#### Feature

- The system will enter an interactive loop where the user provides clarification, and the AI processes it until the intent is clear.

#### Implementation Details

-   **UI Prompt:** Display the clarifying question prominently in the UI.
-   **User Response Handling:** The user's response to the clarifying question will be treated as a continuation of the original prompt.
-   **Re-evaluation:** The AI will re-evaluate the combined context (original prompt + clarification) to confirm its understanding.
-   **Loop Termination:** The loop terminates when the AI's confidence score for understanding the intent reaches an acceptable level, or the user explicitly cancels.

## 3. Integration Points

-   **`llm-routing-and-cognitive-plugins.md`:** For LLM-powered ambiguity detection and question generation.
-   **`input-system.md`:** For handling user responses within the clarification loop.
-   **`project-and-task-management.md`:** Ambiguity in task descriptions can trigger clarification.

## 4. Advanced Features

-   **Multi-turn Clarification:** Support for a series of clarifying questions if the initial one is insufficient.
-   **Visual Aids for Clarification:** For complex ambiguities (e.g., code snippets), use visual aids in the UI to highlight the problematic areas.
-   **Learning from Clarification:** The AI could learn from successful clarification interactions to reduce future ambiguities.
