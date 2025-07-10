# Feature: Research Assistant Routing System

**Created:** 2025-07-10
**Status:** 🟢 In Progress
**Priority:** High

## Overview

Implement a hybrid routing system to classify user queries and route them to appropriate specialized agents. The system uses a 3-layer detection approach for optimal performance and accuracy.

## Goals

- Create a fast, accurate intent detection system
- Route queries to specialized agents based on detected intent
- Provide transparent routing information to users
- Support future expansion with new agent types

## Technical Approach

### Intent Detection (3-Layer System)

1. **Layer 1: Rule-Based Detection (⚡ RULES)**
   - Fast keyword/pattern matching for obvious cases
   - Math queries → COMPUTE intent
   - Literature queries → SEARCH intent
   - Code queries → CODE intent
   - Analysis queries → SYNTHESIZE intent

2. **Layer 2: LLM Classification (🧠 LLM)**
   - Uses TinyLlama for complex queries
   - Constrained prompting with examples
   - Low temperature (0.1) for consistency
   - Validates output against known categories

3. **Layer 3: Default Routing (🔄 DEFAULT)**
   - Fallback to CHAT intent
   - Routes to general conversation handling

### Agent Routing

Based on detected intent:
- **SEARCH** → Literature Agent
- **COMPUTE** → Math Agent
- **CODE** → Code Agent
- **SYNTHESIZE** → Synthesis Agent
- **CHAT** → TinyLlama (Chat Mode)

### Enhanced Display Format

```
[timestamp] Assistant [Methodology: X, Intent: Y] → Destination (Mode):
```

Examples:
- `Assistant [Methodology: Rules, Intent: COMPUTE] → Math Agent (Stub Mode)`
- `Assistant [Methodology: AI-classified, Intent: SEARCH] → Literature Agent (Stub Mode)`
- `Assistant [Methodology: Default, Intent: CHAT] → TinyLlama (Chat Mode)`

## Implementation Details

### Rule-Based Patterns

**Math Queries:**
- Keywords: `solve`, `calculate`, `compute`, `equation`, `integral`
- Patterns: `=`, `+`, `-`, `x^`, `sin(`, `cos(`

**Literature Queries:**
- Keywords: `paper`, `citation`, `reference`, `literature`, `research`

**Code Queries:**
- Keywords: `function`, `class`, `algorithm`, `code`, `program`

**Analysis Queries:**
- Keywords: `explain`, `analyze`, `synthesize`, `summary`

### Testing Commands

- `\search <query>` - Force literature agent
- `\compute <expr>` - Force math agent
- `test_fallback_only` - Hidden rule-based test

## Current Status

- ✅ Rule-based detection implemented
- ✅ TinyLlama classification integrated
- ✅ Default routing working
- ✅ Enhanced display format active
- ⚠️ Research agents are currently stubs

## Next Steps

1. Implement actual research agents (replace stubs)
2. Add confidence scoring for intent detection
3. Consider better models for intent classification
4. Add more sophisticated routing patterns

## Future Improvements

- Replace TinyLlama with better models for accuracy
- Implement actual research agents
- Add confidence scoring
- Support multi-intent queries
- Add user preference learning

## Success Criteria

- [ ] Intent detection accuracy > 90%
- [ ] Routing latency < 100ms for rule-based
- [ ] Clear routing transparency for users
- [ ] Easy to add new agent types
- [ ] Graceful fallback handling

## Notes

- The "Default" methodology means no specific research intent was detected
- All methodologies are internal to the Assistant system
- Everything after `→` represents external agents/systems
- Current implementation uses stub agents for non-chat intents