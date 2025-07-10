# Feature: Ollama-Optimized Cognitive Plugins

## Overview

This ledger outlines the implementation of specialized sub-cognitive plugins, each optimized for a specific task using the most viable local Ollama model as identified in `provider-benchmarks.md`. These plugins will form the building blocks of the `Cognition` pipeline, ensuring efficient and accurate processing of diverse user queries.

## Sub-Cognitive Plugins and User Tests

Each plugin will abstract away the specific Ollama model, allowing the `Intelligent Router` to dynamically select the appropriate plugin based on the task.

### 1. Instruction Processing Plugins

#### 1.1. Instruction Routing Plugin

**Description:** Routes user requests to internal actions/functions.
**Recommended Ollama Model:** Nous Hermes 2 Mistral 7B Q

**User Story:** As a user, when I provide a query, the system accurately identifies the primary intent and routes it to the correct internal function or agent.

**End-to-End User Test:**
- **Action:** User inputs: "Find me documentation on Python's `requests` library."
- **Expected Outcome:** The Instruction Routing Plugin identifies the 'documentation search' intent and passes control to the relevant search agent/tool. The system displays `[Cognition] -> [Instruction Routing (Nous Hermes 2 Mistral 7B Q)] -> [Search Agent]`.

#### 1.2. Instruction Rewriting Plugin

**Description:** Converts vague or ambiguous instructions into clear, actionable steps.
**Recommended Ollama Model:** OpenHermes 2.5 Mistral 7B Q

**User Story:** As a user, if my instruction is unclear, the system should rephrase it into a precise, executable command.

**End-to-End User Test:**
- **Action:** User inputs: "Make that code better."
- **Expected Outcome:** The Instruction Rewriting Plugin rephrases the instruction to something like "Refactor the last code block for readability and efficiency." The system displays `[Cognition] -> [Instruction Rewriting (OpenHermes 2.5 Mistral 7B Q)]` followed by the rephrased instruction.

#### 1.3. Capability-Based Routing Plugin

**Description:** Assigns tasks to the optimal model/tool based on their declared capabilities.
**Recommended Ollama Model:** MythoMax L2 13B Q

**User Story:** As a user, the system should intelligently choose the best tool or model for a given task, even if I don't specify it.

**End-to-End User Test:**
- **Action:** User inputs: "Generate an image of a cat in space."
- **Expected Outcome:** The Capability-Based Routing Plugin identifies the 'image generation' capability and routes the request to an available image generation tool/model. The system displays `[Cognition] -> [Capability-Based Routing (MythoMax L2 13B Q)] -> [Image Generation Tool]`.

#### 1.4. Prompt Amplification Plugin

**Description:** Adds relevant, context-aware instructions to a prompt to improve LLM performance.
**Recommended Ollama Model:** LM Studio 7B (Quantized)

**User Story:** As a user, the system should automatically enhance my prompts with necessary context without me having to explicitly provide it.

**End-to-End User Test:**
- **Action:** User inputs: "Summarize the document."
- **Expected Outcome:** The Prompt Amplification Plugin adds context (e.g., "Focus on key arguments and conclusions, limit to 200 words.") before sending to a summarization model. The system displays `[Cognition] -> [Prompt Amplification (LM Studio 7B (Quantized))]` followed by the amplified prompt.

#### 1.5. Query Expansion Plugin

**Description:** Expands queries with relevant synonyms, clarifications, or related concepts.
**Recommended Ollama Model:** Neural Chat 7B Q

**User Story:** As a user, the system should broaden my search queries to ensure comprehensive results.

**End-to-End User Test:**
- **Action:** User inputs: "Search for 'AI ethics'."
- **Expected Outcome:** The Query Expansion Plugin expands the query to include terms like "artificial intelligence ethics, moral implications of AI, responsible AI development." The system displays `[Cognition] -> [Query Expansion (Neural Chat 7B Q)]` followed by the expanded query.

#### 1.6. Instruction Decomposition Plugin

**Description:** Breaks complex tasks into smaller, actionable steps.
**Recommended Ollama Model:** Phi-4 Mini (Quantized)

**User Story:** As a user, when I give a complex multi-step instruction, the system should break it down into a clear sequence of sub-tasks.

**End-to-End User Test:**
- **Action:** User inputs: "Write a Python script to fetch data from an API, parse the JSON, and save it to a CSV file."
- **Expected Outcome:** The Instruction Decomposition Plugin breaks this into steps: "1. Define API endpoint and parameters. 2. Make HTTP request. 3. Parse JSON response. 4. Convert to CSV format. 5. Write to file." The system displays `[Cognition] -> [Instruction Decomposition (Phi-4 Mini (Quantized))]` followed by the decomposed steps.

### 2. Validation and Quality Control Plugins

#### 2.1. Tool Use Formatting Validation Plugin

**Description:** Detects and flags format errors in tool use instructions or outputs.
**Recommended Ollama Model:** Llama 3 8B (Quantized)

**User Story:** As a user, if the system tries to use a tool with incorrect formatting, it should detect and correct the error or inform me.

**End-to-End User Test:**
- **Action:** The system attempts to call a tool with a malformed JSON argument (e.g., missing a closing brace).
- **Expected Outcome:** The Tool Use Formatting Validation Plugin identifies the error and either corrects it or provides a clear error message. The system displays `[Cognition] -> [Tool Use Formatting Validation (Llama 3 8B (Quantized))]` and the validation result.

#### 2.2. Response Structure Assessment Plugin

**Description:** Checks for the presence and correct order of required sections in LLM responses.
**Recommended Ollama Model:** Mistral 7B (Quantized)

**User Story:** As a user, I expect structured responses to adhere to a predefined format.

**End-to-End User Test:**
- **Action:** The system receives an LLM response that is supposed to have sections like `Summary`, `Analysis`, and `Conclusion`, but `Analysis` is missing.
- **Expected Outcome:** The Response Structure Assessment Plugin flags the missing section. The system displays `[Cognition] -> [Response Structure Assessment (Mistral 7B (Quantized))]` and the assessment result.

#### 2.3. Format Correction Plugin

**Description:** Corrects formatting issues in LLM responses or tool outputs.
**Recommended Ollama Model:** Faraday 7B (Quantized)

**User Story:** As a user, I expect the system's output to be well-formatted and readable.

**End-to-End User Test:**
- **Action:** The system receives an LLM response with inconsistent markdown formatting (e.g., mixed heading styles, incorrect list indentation).
- **Expected Outcome:** The Format Correction Plugin re-formats the response to adhere to consistent markdown standards. The system displays `[Cognition] -> [Format Correction (Faraday 7B (Quantized))]` and the corrected output.

#### 2.4. Query-Result Alignment Plugin

**Description:** Checks if the output addresses the original query.
**Recommended Ollama Model:** Falcon 7B (Quantized)

**User Story:** As a user, I expect the system's response to be directly relevant to my original question.

**End-to-End User Test:**
- **Action:** User asks: "What is the capital of France?" and the LLM (due to some error) responds with information about the Eiffel Tower but not the capital.
- **Expected Outcome:** The Query-Result Alignment Plugin detects that the response does not directly answer the query. The system displays `[Cognition] -> [Query-Result Alignment (Falcon 7B (Quantized))]` and flags the misalignment.

#### 2.5. Intent-Result Consistency Plugin

**Description:** Detects intent drift, ensuring the response aligns with the detected user intent.
**Recommended Ollama Model:** OpenChat 3.5 Q

**User Story:** As a user, I expect the system to stay on topic and not deviate from my original intent.

**End-to-End User Test:**
- **Action:** User asks a question with a 'summarization' intent, but the LLM provides a detailed analysis instead of a summary.
- **Expected Outcome:** The Intent-Result Consistency Plugin detects the drift from 'summarization' to 'analysis' intent. The system displays `[Cognition] -> [Intent-Result Consistency (OpenChat 3.5 Q)]` and flags the inconsistency.

#### 2.6. Redundancy/Contradiction Detection Plugin

**Description:** Flags redundancy or contradictions within LLM responses or across multiple turns.
**Recommended Ollama Model:** OobaGPT 7B (Quantized)

**User Story:** As a user, I expect the system's responses to be coherent and free of repetitive or contradictory information.

**End-to-End User Test:**
- **Action:** The LLM provides a response that repeats a significant portion of previous information or contradicts a statement made earlier in the conversation.
- **Expected Outcome:** The Redundancy/Contradiction Detection Plugin identifies the redundant or contradictory content. The system displays `[Cognition] -> [Redundancy/Contradiction Detection (OobaGPT 7B (Quantized))]` and highlights the problematic sections.

### 3. Cognitive Operations Plugins

#### 3.1. Rationale Generation Plugin

**Description:** Provides clear, logical explanations for LLM decisions or actions.
**Recommended Ollama Model:** Grok 1.5 (Quantized)

**User Story:** As a user, I want to understand why the system made a particular decision or took a specific action.

**End-to-End User Test:**
- **Action:** The system performs a complex multi-step task.
- **Expected Outcome:** The Rationale Generation Plugin provides a concise explanation of the reasoning behind each major step. The system displays `[Cognition] -> [Rationale Generation (Grok 1.5 (Quantized))]` followed by the rationale.

#### 3.2. Task Triage Plugin

**Description:** Filters out-of-scope or inappropriate tasks.
**Recommended Ollama Model:** Command R+ (Quantized)

**User Story:** As a user, if I ask something outside the system's capabilities, it should inform me gracefully.

**End-to-End User Test:**
- **Action:** User inputs: "Order me a pizza."
- **Expected Outcome:** The Task Triage Plugin identifies this as an out-of-scope task and responds with a message like "I cannot fulfill that request as I am an AI assistant and cannot interact with external services in that manner." The system displays `[Cognition] -> [Task Triage (Command R+ (Quantized))]` and the triage result.

#### 3.3. Simple Classification Plugin

**Description:** Performs sentiment, intent, or spam classification.
**Recommended Ollama Model:** Starling-LM 7B Alpha Q

**User Story:** As a user, the system should be able to quickly categorize simple inputs.

**End-to-End User Test:**
- **Action:** User inputs: "This is a terrible idea."
- **Expected Outcome:** The Simple Classification Plugin classifies the sentiment as 'negative'. The system displays `[Cognition] -> [Simple Classification (Starling-LM 7B Alpha Q)]` and the classification result.

#### 3.4. Summarization Plugin

**Description:** Creates concise, accurate summaries of provided text.
**Recommended Ollama Model:** Falcon 7B (Quantized)

**User Story:** As a user, I want to get a quick overview of long texts.

**End-to-End User Test:**
- **Action:** User provides a long article and asks for a summary.
- **Expected Outcome:** The Summarization Plugin generates a concise and accurate summary of the article. The system displays `[Cognition] -> [Summarization (Falcon 7B (Quantized))]` followed by the summary.

#### 3.5. Error/Quality Scoring Plugin

**Description:** Assigns meaningful confidence or quality scores to LLM responses or tool outputs.
**Recommended Ollama Model:** Command R+ (Quantized)

**User Story:** As a user, I want to know how confident the system is in its responses or if there are any quality concerns.

**End-to-End User Test:**
- **Action:** The system generates a response based on potentially ambiguous information.
- **Expected Outcome:** The Error/Quality Scoring Plugin assigns a confidence score (e.g., 0.75) to the response. The system displays `[Cognition] -> [Error/Quality Scoring (Command R+ (Quantized))]` and the score.

#### 3.6. Parameter Extraction Plugin

**Description:** Extracts structured data (parameters) from natural language text.
**Recommended Ollama Model:** Mistral 7B (Quantized)

**User Story:** As a user, I want the system to pull out specific pieces of information from my text.

**End-to-End User Test:**
- **Action:** User inputs: "Schedule a meeting with John Doe for tomorrow at 3 PM about project X."
- **Expected Outcome:** The Parameter Extraction Plugin extracts: `name: John Doe, date: tomorrow, time: 3 PM, topic: project X`. The system displays `[Cognition] -> [Parameter Extraction (Mistral 7B (Quantized))]` and the extracted parameters.

#### 3.7. User Feedback Integration Plugin

**Description:** Incorporates user corrections or feedback effectively to improve future interactions.
**Recommended Ollama Model:** LM Studio 7B (Quantized)

**User Story:** As a user, when I correct the system, it should learn from my feedback and apply it in subsequent interactions.

**End-to-End User Test:**
- **Action:** User corrects a previous factual error made by the system (e.g., "No, the capital of Canada is Ottawa, not Toronto."). Later, the same factual question is asked.
- **Expected Outcome:** The User Feedback Integration Plugin processes the correction, and the system provides the correct answer in the subsequent interaction. The system displays `[Cognition] -> [User Feedback Integration (LM Studio 7B (Quantized))]` and acknowledges the feedback.

#### 3.8. Todo Planning Plugin

**Description:** Generates and manages todo lists or action plans based on user input.
**Recommended Ollama Model:** Phi-3.5 Mini (Quantized)

**User Story:** As a user, I want the system to help me organize my tasks and create actionable plans.

**End-to-End User Test:**
- **Action:** User inputs: "I need to prepare for my presentation next week. What should I do?"
- **Expected Outcome:** The Todo Planning Plugin generates a list of actionable items: "1. Outline presentation content. 2. Create slides. 3. Practice delivery. 4. Gather necessary materials." The system displays `[Cognition] -> [Todo Planning (Phi-3.5 Mini (Quantized))]` followed by the todo list.
