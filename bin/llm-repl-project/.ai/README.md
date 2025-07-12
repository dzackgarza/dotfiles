# Sacred Architecture Documentation

This directory contains comprehensive documentation for the LLM REPL project's Sacred GUI Architecture. All documentation follows industry best practices for Textual chat applications with extensive ASCII diagrams for visual clarity.

## Directory Structure Overview

```
.ai/
├── README.md                    # This overview
├── project.md                   # Project vision and goals
├── context-rules.md            # AI agent guidelines  
├── wrinkl-rules.md             # Documentation system rules
├── architecture/               # 🏛️ Core architectural specifications
│   ├── GUI-VISION.md           # 🎨 Complete visual GUI specification  
│   ├── SACRED-GUI-ARCHITECTURE.md # 📐 Canonical layout rules
│   ├── core-principles.md      # 🏗️ Foundational philosophies
│   └── sacred-timeline-diagram.md # 📊 Timeline visualizations
├── implementation/             # 🛠️ Development guides and patterns
│   ├── textual-implementation-phases.md
│   ├── textual-migration-architecture.md
│   ├── patterns.md             # Code patterns and philosophy
│   └── ollama-setup.md         # Local LLM configuration
├── testing/                    # 🧪 Testing strategies and validation
│   ├── textual-testing-guide.md
│   ├── sacred-architecture-tests.md  
│   └── widget-test-harnesses.md
├── design/                     # 🎨 Styling and visual design
│   ├── textual-styling-theming.md
│   ├── sacred-color-palette.md
│   └── responsive-design.md
├── reference/                  # 📚 External documentation and examples
│   ├── textual-docs/           # Complete Textual framework docs
│   └── inspiration/            # Reference implementations
└── ledgers/                    # 📋 Feature tracking (unchanged structure)
    ├── v3.1/                   # Current development phase
    ├── v3.2/                   # Future features
    └── ...
```

## Quick Navigation

### 🚀 **Getting Started**
```
Start Here → architecture/GUI-VISION.md
          ↓
     Understand Sacred Architecture principles
          ↓  
     Follow implementation/patterns.md
          ↓
     Test with testing/textual-testing-guide.md
```

### 🎯 **By Use Case**

| I want to... | Start with... | Then see... |
|--------------|---------------|-------------|
| **Understand the vision** | `architecture/GUI-VISION.md` | `project.md` |
| **Implement widgets** | `implementation/patterns.md` | `architecture/SACRED-GUI-ARCHITECTURE.md` |
| **Style the interface** | `design/textual-styling-theming.md` | `design/sacred-color-palette.md` |
| **Test my code** | `testing/textual-testing-guide.md` | `testing/widget-test-harnesses.md` |
| **Find examples** | `reference/textual-docs/` | `reference/inspiration/` |
| **Track features** | `ledgers/v3.1/README.md` | Specific ledger files |

## Sacred Architecture at a Glance

### 🏆 **GOLDEN RULE: BUILD FROM KNOWN WORKING CODE**

> **Critical Development Principle**: It is MUCH better to work from a KNOWN working implementation, like V3 or the inspiration repositories, and build off of that, than to reinvent something. If we get stuck, we should always take a step back and see how it is done elsewhere successfully first.

```
┌─ FUNDAMENTAL DEVELOPMENT PRINCIPLE ──────────────────────┐
│                                                           │
│  🏆 COPY V3 PATTERNS: V3 works perfectly - use its code  │
│       → reference/inspiration/V3/elia_chat/widgets/      │
│                                                           │
│  📚 STUDY INSPIRATION: Reference known working examples  │
│       → reference/inspiration/gemini-cli/               │
│       → reference/inspiration/anthropic-ai-claude-code/ │
│                                                           │
│  🔍 RESEARCH FIRST: When stuck, see how others solved it │
│       → Extract patterns from working implementations    │
│       → Adapt proven solutions to our architecture       │
│                                                           │
│  🚫 NEVER REINVENT: Build from working implementations   │
│       → Avoid creating novel solutions from scratch      │
│       → Prefer tested patterns over experimental code    │
│                                                           │
│  🧬 ADAPT, DON'T CREATE: Modify working code vs rebuild  │
│       → Take working widget → modify for Sacred GUI      │
│       → Copy proven patterns → adjust for our needs      │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### 🏛️ **Sacred Architecture Core Principles**
```
┌─ SACRED ARCHITECTURE FUNDAMENTALS ───────────────────────┐
│                                                           │
│  📜 Sacred Timeline: Append-only conversation history    │
│  🔄 Sacred Turn Structure: User → Cognition → Assistant  │
│  👁️ Radical Transparency: Multi-step cognition visible   │
│  📐 Three-Area Layout: Timeline + Workspace + Input      │
│  🔧 V3 Proven Patterns: VerticalScroll + simple widgets  │
│  ⚡ Fail-Fast Validation: Immediate error surfacing      │
│  🧵 Thread-Safe Updates: call_from_thread() streaming    │
│  📏 Content-Driven Design: No hardcoded dimensions       │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### 🎨 **Visual Layout States**

**IDLE STATE (2-way split):**
```
┌─────────────────────────────────┐
│        Sacred Timeline         │
│  ┌─ Turn 1 ─────────────────┐   │
│  │ 👤 User: "Question..."   │   │
│  │ 🧠 Cognition → Response  │   │  
│  │ 🤖 Assistant: "Answer..." │   │
│  └─────────────────────────────┘   │
│  ═══════════════════════════════   │
│  ┌─ Turn 2 ─────────────────┐   │
│  │ 👤 User: "Follow-up..."  │   │
│  │ 🧠 Cognition → Response  │   │
│  │ 🤖 Assistant: "More..."  │   │
│  └─────────────────────────────┘   │
├─────────────────────────────────┤
│           Input Area            │
│  > Next question here...        │
└─────────────────────────────────┘
```

**ACTIVE STATE (3-way split):**
```
┌─────────────────────────────────┐
│        Sacred Timeline         │
│  [Previous conversation...]     │
│  👤 User: "Current question"    │
├─────────────────────────────────┤
│        Live Workspace          │
│  ⚡ Route Query    [active]     │
│  ⏳ Research       [pending]    │
│  ⏳ Synthesize     [pending]    │
│  ⏳ Response       [pending]    │
├─────────────────────────────────┤
│           Input Area            │
│  > [Processing... please wait]  │
└─────────────────────────────────┘
```

## Documentation Standards

### 📝 **Document Types**

**Architecture Documents** (`architecture/`)
- Define immutable design principles
- Include detailed ASCII diagrams
- Specify implementation requirements
- Document forbidden patterns

**Implementation Guides** (`implementation/`)  
- Provide step-by-step development instructions
- Include code examples and patterns
- Reference V3 proven approaches
- Detail migration strategies

**Testing Resources** (`testing/`)
- Define comprehensive testing strategies
- Include widget test harnesses
- Specify validation approaches
- Document CI/CD integration

**Design Guidelines** (`design/`)
- Establish visual design system
- Define color palettes and typography
- Specify CSS patterns and constraints
- Document responsive behavior

### 🎨 **ASCII Diagram Standards**

All documentation uses consistent ASCII diagram conventions:

```
┌─ DIAGRAM TYPE CONVENTIONS ───────────────────────────────┐
│                                                           │
│  ┌─────┐  Boxes: Components, widgets, containers         │
│  │     │                                                 │
│  └─────┘                                                 │
│                                                           │
│  ═══════  Double lines: Major separators, hrules        │
│  ───────  Single lines: Minor separators, borders       │
│                                                           │
│  👤 🤖 🧠  Icons: User, Assistant, Cognition             │
│  ⚡ ✅ ⏳  Status: Active, Complete, Pending              │
│  📊 ⏱️ 🎯  Meta: Stats, Time, Focus                      │
│                                                           │
│  [Text]   Labels: Descriptive text and annotations      │
│  ↓ → ←    Arrows: Flow direction and relationships       │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

## Development Workflow

### 🔄 **Standard Development Process**

```
1. 📖 Read Architecture    → architecture/GUI-VISION.md
2. 🎯 Check Requirements   → Relevant ledger in ledgers/
3. 🛠️ Follow Patterns      → implementation/patterns.md  
4. 🎨 Apply Design         → design/ guidelines
5. 🧪 Validate with Tests  → testing/ strategies
6. 📚 Reference Examples   → reference/ materials
7. 📝 Update Documentation → Relevant .ai/ files
```

### ✅ **Quality Gates**

Before completing any development:

```
┌─ DEVELOPMENT QUALITY CHECKLIST ──────────────────────────┐
│                                                           │
│  ☐ Follows Sacred Architecture principles                │
│  ☐ Uses V3 proven patterns (VerticalScroll + render())   │ 
│  ☐ Includes fail-fast validation                         │
│  ☐ Implements error boundaries                           │
│  ☐ Uses valid Textual CSS properties                     │
│  ☐ Passes widget test harnesses                          │
│  ☐ Updates relevant documentation                        │
│  ☐ Includes ASCII diagrams where appropriate             │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

## Key Files Quick Reference

### 🏆 **Most Important Files**

1. **`architecture/GUI-VISION.md`** - THE definitive visual specification
2. **`architecture/SACRED-GUI-ARCHITECTURE.md`** - Implementation constraints  
3. **`implementation/patterns.md`** - Coding standards and patterns
4. **`testing/textual-testing-guide.md`** - Validation strategies
5. **`design/textual-styling-theming.md`** - Visual design system

### 📊 **File Size Summary**

```
Large Files (>10k):
├── architecture/GUI-VISION.md           # 25k+ - Comprehensive visual spec
├── architecture/SACRED-GUI-ARCHITECTURE.md # 15k+ - Layout specification  
└── reference/textual-docs/              # 100MB+ - Complete framework docs

Medium Files (5-10k):  
├── implementation/patterns.md           # 8k - Code patterns
├── testing/textual-testing-guide.md     # 7k - Testing strategies
└── design/textual-styling-theming.md    # 6k - Design system

Quick Reference (<5k):
├── README files in each directory       # 3-4k each
├── Specific implementation guides       # 2-3k each  
└── Individual design specifications     # 1-2k each
```

## Cross-Directory Relationships

```
┌─ DOCUMENTATION RELATIONSHIPS ────────────────────────────┐
│                                                           │
│  architecture/ ←─ defines ──→ implementation/            │
│       ↑                              ↓                   │
│  specifies                     implements                │ 
│       ↓                              ↑                   │
│  design/ ←──── styles ─────→ testing/                    │
│       ↑                              ↓                   │
│  references                   validates                  │
│       ↓                              ↑                   │
│  reference/ ←─ supports ────→ ledgers/                   │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

## Contributing Guidelines

When updating documentation:

1. **Maintain consistency** across all ASCII diagrams
2. **Update cross-references** when moving or changing files
3. **Include visual examples** for complex concepts
4. **Test code examples** before including them
5. **Follow the Sacred Architecture principles** in all changes
6. **Update README files** when directory structure changes

---

**Status**: This documentation represents the complete Sacred Architecture specification as of 2025-07-12. All development must follow these guidelines to ensure architectural consistency and maintainability.