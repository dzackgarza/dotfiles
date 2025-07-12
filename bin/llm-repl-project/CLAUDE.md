# CLAUDE.md - Agent Entry Point

This file provides guidance to Claude Code agents when working with this LLM REPL project.

## 🚨 CRITICAL OPERATING RULES

1. **Never run GUI apps** - This breaks Claude Code's interface. Test backend logic statically only.
2. **Use `pdm` for Python** - Always prefix python/pytest commands with `pdm` to use project's virtual environment.
3. **Build from working code** - Copy patterns from V3, Gemini CLI, or Claude Code. NEVER reinvent solutions.

## 🎯 PROJECT MISSION

**LLM REPL** - Interactive terminal research assistant with transparent AI cognition pipeline.

**Sacred GUI Architecture** - Three-area layout: Sacred Timeline + Live Workspace + Input

**Core Philosophy** - Every operation is a block in an immutable, append-only timeline.

## 🏆 GOLDEN RULE: BUILD FROM WORKING CODE

> **CRITICAL**: Always study existing working implementations BEFORE writing new code. Copy proven patterns, adapt for our needs.

**Primary References:**
- **V3 Chat Implementation** - `V3/elia_chat/widgets/chat.py` (proven VerticalScroll + render() pattern)
- **Claude Code Package** - `reference/inspiration/anthropic-ai-claude-code/` (production TUI patterns)
- **Gemini CLI** - `reference/inspiration/gemini-cli/` (LLM interface patterns)

**When to use .ai documentation:**
- **Architecture decisions** → `.ai/docs/ARCHITECTURE-GUIDE.md`
- **Implementation help** → `.ai/docs/IMPLEMENTATION-GUIDE.md`
- **Testing strategies** → `.ai/docs/TESTING-GUIDE.md`
- **UI/UX design** → `.ai/docs/DESIGN-GUIDE.md`
- **Feature tracking** → `.ai/ledgers/v3.1/`

## 🏛️ SACRED GUI ARCHITECTURE (IMMUTABLE)

**Three-Area Layout (2-way ↔ 3-way split):**

```
┌─────────────────────────┐
│ Sacred Timeline (Top)   │ ← VerticalScroll: conversation history
│ ├── User Block         │   (V3's chat_container pattern)
│ ├── Cognition Block    │
│ ├── Assistant Block    │
│ ├─────────────────────  │ ← hrule separators
│ └── [scrolling...]     │
├─────────────────────────┤
│ Live Workspace (Mid)   │ ← VerticalScroll: streaming cognition
│ ├── Route Query        │   (shows during processing, hides when idle)
│ ├── Research Step      │
│ ├── Generate Response  │
│ └── [streaming...]     │
├─────────────────────────┤
│ Input (Bottom)         │ ← PromptInput
└─────────────────────────┘
```

**WHY THIS WORKS:**
- ✅ Uses V3's proven VerticalScroll pattern (no nested containers)
- ✅ Clean separation: history vs live processing vs input
- ✅ Scales to unlimited content via scrolling
- ✅ Simple state: 2-way (idle) ↔ 3-way (processing)

## 📁 .AI DOCUMENTATION STRUCTURE

```
.ai/
├── docs/                          # Core guidance documents
│   ├── ARCHITECTURE-GUIDE.md      # Design decisions & Sacred GUI rules
│   ├── IMPLEMENTATION-GUIDE.md    # Development patterns & V3 usage
│   ├── TESTING-GUIDE.md          # Testing strategies & validation
│   ├── DESIGN-GUIDE.md           # UI/UX patterns & CSS guidelines
│   └── REFERENCE-GUIDE.md        # Working examples & inspiration
├── ledgers/                       # Feature tracking
│   └── v3.1/                     # Current development phase
└── context/                       # Agent behavior guides
    ├── ai-agent-guidelines.md     # How agents should work
    └── wrinkl-framework.md        # Ledger system usage
```

## ⚡ QUICK START FOR AGENTS

### 1. Understanding the Project
```bash
# Read the architecture first
→ .ai/docs/ARCHITECTURE-GUIDE.md

# Study V3's working patterns
→ V3/elia_chat/widgets/chat.py
```

### 2. Implementing Features
```bash
# Copy V3 patterns
→ .ai/docs/IMPLEMENTATION-GUIDE.md

# Check current features
→ .ai/ledgers/v3.1/
```

### 3. Testing & Validation
```bash
# Test statically only
→ .ai/docs/TESTING-GUIDE.md

# Run tests
just test
```

### 4. UI/Design Work
```bash
# Follow V3 CSS patterns
→ .ai/docs/DESIGN-GUIDE.md

# Reference working examples
→ .ai/docs/REFERENCE-GUIDE.md
```

## 🛠️ ESSENTIAL COMMANDS

```bash
# Development
just run-fast        # Start app (Groq models)
just test           # Run test suite
just lint           # Type checking

# Ledger workflow
just ledger-status  # Check current work
just start-ledger <name>
just ledger-request-review <name>
```

## 🎯 CURRENT FOCUS: V3.1

**Priority**: Implement Sacred GUI Architecture using V3's proven patterns

**Active Work**: Check `.ai/ledgers/v3.1/` for specific features

**Key Principle**: Build from working V3 code, adapt for Sacred Architecture

## 🚫 COMMON MISTAKES TO AVOID

- ❌ Running GUI apps (breaks Claude Code)
- ❌ Writing widgets from scratch (copy V3 patterns)
- ❌ Nested containers in VerticalScroll (causes layout conflicts)
- ❌ Skipping .ai documentation (leads to architectural mistakes)
- ❌ Self-approving work (human review required)

## 🔗 WHEN YOU NEED MORE DETAIL

**For deep architecture understanding:**
→ `.ai/docs/ARCHITECTURE-GUIDE.md` - Sacred GUI principles, V3 patterns, layout rules

**For implementation help:**
→ `.ai/docs/IMPLEMENTATION-GUIDE.md` - Code patterns, V3 examples, development workflow

**For testing guidance:**
→ `.ai/docs/TESTING-GUIDE.md` - Test strategies, harnesses, validation approaches

**For UI/design questions:**
→ `.ai/docs/DESIGN-GUIDE.md` - CSS patterns, styling guidelines, responsive design

**For working examples:**
→ `.ai/docs/REFERENCE-GUIDE.md` - V3 code, Claude Code patterns, proven solutions

**For feature work:**
→ `.ai/ledgers/v3.1/` - Current development tasks, user stories, validation criteria

---

**Remember**: This file is your starting point. Use it to navigate to the right detailed documentation for your specific task. Always study working implementations before coding.