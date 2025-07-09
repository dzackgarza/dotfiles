# Research Assistant Routing System - Developer Documentation

## Overview

The Research Assistant uses a hybrid routing system to classify user queries and route them to appropriate handlers. This document explains the routing logic and decision flow.

## Routing Flow

```
User Query → Intent Detection → Agent Routing → Response Generation
```

## Intent Detection (3-Layer System)

### Layer 1: Rule-Based Detection (⚡ RULES)
Fast keyword/pattern matching for obvious cases:

**Math Queries** → COMPUTE intent
- Keywords: `solve`, `calculate`, `compute`, `equation`, `integral`, etc.
- Patterns: `=`, `+`, `-`, `x^`, `sin(`, `cos(`, etc.
- Example: `"solve x^2 = 4"` → COMPUTE

**Literature Queries** → SEARCH intent  
- Keywords: `paper`, `citation`, `reference`, `literature`, `research`, etc.
- Example: `"find papers about AI"` → SEARCH

**Code Queries** → CODE intent
- Keywords: `function`, `class`, `algorithm`, `code`, `program`, etc.
- Example: `"write a python function"` → CODE

**Analysis Queries** → SYNTHESIZE intent
- Keywords: `explain`, `analyze`, `synthesize`, `summary`, etc.
- Example: `"explain machine learning"` → SYNTHESIZE

### Layer 2: TinyLlama Classification (🧠 LLM)
When rule-based detection finds no clear match, TinyLlama attempts classification:
- Uses constrained prompting with examples
- Low temperature (0.1) for consistency
- Validates output against known intent categories
- Example: Complex queries that don't match clear patterns

### Layer 3: Default Routing (🔄 DEFAULT)
When both rule-based and LLM classification fail or return CHAT:
- Defaults to CHAT intent
- Routes to general conversation handling
- **This is why "Hello" shows DEFAULT** - it doesn't match any research patterns

## Agent Routing

Based on detected intent, queries are routed to:

### Research Agent Stubs
- **SEARCH** → `Assistant → [METHOD] → Literature Agent`
- **COMPUTE** → `Assistant → [METHOD] → Math Agent`  
- **CODE** → `Assistant → [METHOD] → Code Agent`
- **SYNTHESIZE** → `Assistant → [METHOD] → Synthesis Agent`

### Chat Handling
- **CHAT** → `Assistant → [METHOD] → TinyLlama`

## Enhanced Routing Display Format

```
[timestamp] Assistant [Methodology: X, Intent: Y] → Destination (Mode):
```

**Examples:**
- `Assistant [Methodology: Rules, Intent: COMPUTE] → Math Agent (Stub Mode)`
- `Assistant [Methodology: AI-classified, Intent: SEARCH] → Literature Agent (Stub Mode)`  
- `Assistant [Methodology: Default, Intent: CHAT] → TinyLlama (Chat Mode)`

**What This Shows:**
1. **Assistant**: The unified routing system (all methodologies are internal to it)
2. **Methodology**: How the routing decision was made (Rules/AI-classified/Default)
3. **Intent**: What type of task was detected (COMPUTE/SEARCH/CODE/SYNTHESIZE/CHAT)
4. **→**: Actual handoff to a different agent/system
5. **Destination (Mode)**: Where the query was routed and what configuration it uses

**Key Distinction:**
- Everything before `→` is internal to the Assistant system
- Everything after `→` represents external agents/systems the Assistant routes to

## TinyLlama Chat Handling

When routed to TinyLlama for chat:

### Emergency Rules (Minimal)
- Only for critical system failures
- Almost no hard-coded responses to preserve AI experience

### TinyLlama Direct Processing  
- Minimal prompt constraints to preserve authentic AI behavior
- Simple system prompt: "You are a helpful research assistant"
- Shows real model capabilities and limitations
- Temperature 0.4, allowing some creativity

### Response Attribution
Original prefixes are removed from display content but routing is tracked in metadata.

## Why "Hello" → Assistant [Methodology: Default, Intent: CHAT] → TinyLlama (Chat Mode)

1. **"Hello" doesn't match any research patterns** (no keywords like "solve", "find papers", etc.)
2. **Rule-based detection returns None**
3. **TinyLlama classification** (if used) also returns CHAT
4. **Assistant defaults to general conversation**
5. **Final routing**: `Assistant [Methodology: Default, Intent: CHAT] → TinyLlama (Chat Mode)`

The "Default" methodology means **"no specific research intent detected, using default chat routing"**.

## Terminology Clarification

### Intent Detection Methods:
- **RULES** (⚡): Keyword/pattern matching detected the intent immediately  
- **LLM** (🧠): TinyLlama was used to classify the intent when rules didn't match
- **DEFAULT** (🔄): No specific research intent detected, defaulting to general chat

### What "Default" Means:
When you see `🎯 Intent: CHAT (🔄 DEFAULT)`, it means:
1. The query didn't match any research patterns (no "solve", "find papers", etc.)
2. If TinyLlama was consulted, it also said "general chat"  
3. System uses default routing: general conversation → TinyLlama

"Default" = "no special handling needed, treat as normal chat"

## Mode Tracking

**Routing Modes:**
- `TinyLlama (Routing Mode)` - TinyLlama configured for intent classification with constrained prompts
- No routing mode needed for Rules or Default (they're deterministic)

**Destination Modes:**
- `TinyLlama (Chat Mode)` - TinyLlama configured for natural conversation
- `Math Agent (Stub Mode)` - Placeholder math agent (not yet implemented)
- `Literature Agent (Stub Mode)` - Placeholder literature search (not yet implemented)
- `Code Agent (Stub Mode)` - Placeholder code generation (not yet implemented)
- `Synthesis Agent (Stub Mode)` - Placeholder research synthesis (not yet implemented)

## Testing Commands

- `\search <query>` - Force literature agent
- `\compute <expr>` - Force math agent
- `test_fallback_only` - Hidden rule-based test

## Future Improvements

- Replace TinyLlama with better models for more accurate intent detection
- Implement actual research agents (currently stubs)
- Add confidence scoring for intent detection
- Consider renaming FALLBACK terminology for clarity