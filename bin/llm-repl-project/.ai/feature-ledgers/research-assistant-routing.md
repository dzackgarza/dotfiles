# Feature: Research Assistant Routing System

## Overview

Implement a hybrid routing system to classify user queries and route them to appropriate specialized agents. The system uses a 3-layer detection approach for optimal performance and accuracy.

## Sub-Features and User Tests

### 1. Rule-Based Detection (Layer 1)

**Description:** Fast keyword/pattern matching for obvious cases, routing queries to specific agents based on predefined rules.

**User Stories:**
- As a user, when I ask a math-related question (e.g., "solve 2+2"), the system should identify it as a COMPUTE intent and route it to the Math Agent.
- As a user, when I ask a literature-related question (e.g., "find papers on AI"), the system should identify it as a SEARCH intent and route it to the Literature Agent.
- As a user, when I ask a code-related question (e.g., "write a Python function"), the system should identify it as a CODE intent and route it to the Code Agent.
- As a user, when I ask an analysis-related question (e.g., "explain quantum physics"), the system should identify it as a SYNTHESIZE intent and route it to the Synthesis Agent.

**End-to-End User Tests:**
- **Test 1.1 (Math Query):**
    - **Input:** "solve for x in 2x + 5 = 10"
    - **Expected Output:** System routes to Math Agent. Display shows `Assistant [Methodology: Rules, Intent: COMPUTE] → Math Agent (Stub Mode)`
- **Test 1.2 (Literature Query):**
    - **Input:** "find recent research on large language models"
    - **Expected Output:** System routes to Literature Agent. Display shows `Assistant [Methodology: Rules, Intent: SEARCH] → Literature Agent (Stub Mode)`
- **Test 1.3 (Code Query):**
    - **Input:** "how to implement a quicksort algorithm in Java"
    - **Expected Output:** System routes to Code Agent. Display shows `Assistant [Methodology: Rules, Intent: CODE] → Code Agent (Stub Mode)`
- **Test 1.4 (Analysis Query):**
    - **Input:** "synthesize the key arguments from the provided text"
    - **Expected Output:** System routes to Synthesis Agent. Display shows `Assistant [Methodology: Rules, Intent: SYNTHESIZE] → Synthesis Agent (Stub Mode)`
- **Test 1.5 (Forced Literature Agent):**
    - **Input:** `\search "machine learning applications"`
    - **Expected Output:** System routes to Literature Agent, overriding rule-based detection. Display shows `Assistant [Methodology: Rules, Intent: SEARCH] → Literature Agent (Stub Mode)`
- **Test 1.6 (Forced Math Agent):**
    - **Input:** `\compute "sqrt(16)"`
    - **Expected Output:** System routes to Math Agent, overriding rule-based detection. Display shows `Assistant [Methodology: Rules, Intent: COMPUTE] → Math Agent (Stub Mode)`

### 2. LLM Classification (Layer 2)

**Description:** Uses TinyLlama for complex queries, with constrained prompting and low temperature for consistency, validating output against known categories.

**User Stories:**
- As a user, when I ask a complex question that doesn't match simple rules, the system should use the LLM to classify the intent accurately.
- As a user, the LLM classification should be consistent and avoid misclassifying queries.

**End-to-End User Tests:**
- **Test 2.1 (Complex Math Query):**
    - **Input:** "What is the derivative of x^2 + 3x - 5?"
    - **Expected Output:** System routes to Math Agent via LLM classification. Display shows `Assistant [Methodology: AI-classified, Intent: COMPUTE] → Math Agent (Stub Mode)`
- **Test 2.2 (Complex Literature Query):**
    - **Input:** "Can you provide a summary of the historical development of neural networks?"
    - **Expected Output:** System routes to Literature Agent via LLM classification. Display shows `Assistant [Methodology: AI-classified, Intent: SEARCH] → Literature Agent (Stub Mode)`
- **Test 2.3 (Complex Code Query):**
    - **Input:** "Explain the concept of polymorphism in object-oriented programming and provide a C++ example."
    - **Expected Output:** System routes to Code Agent via LLM classification. Display shows `Assistant [Methodology: AI-classified, Intent: CODE] → Code Agent (Stub Mode)`
- **Test 2.4 (Complex Analysis Query):**
    - **Input:** "Analyze the economic implications of global climate change policies."
    - **Expected Output:** System routes to Synthesis Agent via LLM classification. Display shows `Assistant [Methodology: AI-classified, Intent: SYNTHESIZE] → Synthesis Agent (Stub Mode)`

### 3. Default Routing (Layer 3)

**Description:** Fallback to CHAT intent for queries not classified by rule-based or LLM methods, routing to general conversation handling.

**User Stories:**
- As a user, if my query doesn't fit any specific intent, the system should gracefully handle it as a general chat.

**End-to-End User Tests:**
- **Test 3.1 (General Chat Query):**
    - **Input:** "Tell me a joke."
    - **Expected Output:** System routes to TinyLlama (Chat Mode). Display shows `Assistant [Methodology: Default, Intent: CHAT] → TinyLlama (Chat Mode)`
- **Test 3.2 (Unclassifiable Query):**
    - **Input:** "What is the meaning of life, the universe, and everything?"
    - **Expected Output:** System routes to TinyLlama (Chat Mode). Display shows `Assistant [Methodology: Default, Intent: CHAT] → TinyLlama (Chat Mode)`

### 4. Enhanced Display Format

**Description:** Provides transparent routing information to users in a standardized format.

**User Stories:**
- As a user, I should clearly see how my query was classified and which agent it was routed to.

**End-to-End User Tests:**
- **Test 4.1 (Display Format Verification - Rule-Based):**
    - **Input:** "calculate 5 * 7"
    - **Expected Output:** Display includes `Assistant [Methodology: Rules, Intent: COMPUTE] → Math Agent (Stub Mode)`
- **Test 4.2 (Display Format Verification - LLM Classified):**
    - **Input:** "Summarize the main points of the theory of relativity."
    - **Expected Output:** Display includes `Assistant [Methodology: AI-classified, Intent: SEARCH] → Literature Agent (Stub Mode)`
- **Test 4.3 (Display Format Verification - Default):**
    - **Input:** "Hello there!"
    - **Expected Output:** Display includes `Assistant [Methodology: Default, Intent: CHAT] → TinyLlama (Chat Mode)`
