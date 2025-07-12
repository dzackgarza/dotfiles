# Architecture Documentation

This directory contains the core architectural specifications and design principles for the LLM REPL project.

## Files Overview

```
architecture/
├── README.md                    # This file - architecture overview
├── GUI-VISION.md               # Complete visual GUI specification with ASCII diagrams  
├── SACRED-GUI-ARCHITECTURE.md  # Canonical Sacred GUI layout specification
├── core-principles.md          # Foundational architectural principles
└── sacred-timeline-diagram.md  # Sacred Timeline visual documentation
```

## Architecture Hierarchy

### 🏆 **Foundation: Build From Working Code**
- **File**: `core-principles.md`
- **Purpose**: Fundamental architectural philosophies based on PROVEN patterns
- **Key Concepts**: V3 VerticalScroll patterns, Sacred Timeline, Sacred Turn Structure
- **Critical**: ALWAYS reference working implementations before designing new components

### 🎨 **Visual Design: GUI Vision**
- **File**: `GUI-VISION.md` 
- **Purpose**: Complete visual specification with detailed ASCII diagrams
- **Key Features**: 
  - State transition diagrams (Idle → Active → Streaming → Complete)
  - Widget architecture blueprints
  - Data flow visualizations
  - Error handling patterns
  - Responsive design specifications

### 📐 **Implementation: Sacred GUI Architecture**
- **File**: `SACRED-GUI-ARCHITECTURE.md`
- **Purpose**: Immutable layout rules and implementation requirements
- **Focus**: Three-area layout enforcement, V3 pattern compliance, forbidden patterns

### 📊 **Documentation: Sacred Timeline Diagrams**
- **File**: `sacred-timeline-diagram.md`
- **Purpose**: Visual documentation for Sacred Timeline concepts

## Quick Navigation

| Need | File | Section |
|------|------|---------|
| **Understanding the vision** | `GUI-VISION.md` | Executive Summary |
| **Implementation guidance** | `SACRED-GUI-ARCHITECTURE.md` | Implementation Requirements |
| **Philosophical foundation** | `core-principles.md` | Guiding Philosophies |
| **State transitions** | `GUI-VISION.md` | Sacred Architecture States |
| **Widget patterns** | `GUI-VISION.md` | Detailed Widget Architecture |
| **Data flow** | `GUI-VISION.md` | Data Flow Architecture |
| **Error handling** | `GUI-VISION.md` | Error Handling & Validation |

## Architecture Principles Summary

```
┌─ SACRED ARCHITECTURE CORE PRINCIPLES ─────────────────────┐
│                                                            │
│  🏛️ Sacred Timeline: Append-only, immutable conversation  │
│  🔄 Sacred Turn Structure: User → Cognition → Assistant   │
│  👁️ Radical Transparency: Multi-step cognition visible    │
│  📐 Three-Area Layout: Timeline + Workspace + Input       │
│  🔧 V3 Proven Patterns: VerticalScroll + simple widgets   │
│  ⚡ Fail-Fast Validation: Immediate error surfacing       │
│  🧵 Thread-Safe Updates: call_from_thread() for streaming │
│  📏 Content-Driven Heights: No hardcoded dimensions       │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Development Guidelines

1. **Always start with**: `GUI-VISION.md` for visual understanding
2. **Implementation rules**: `SACRED-GUI-ARCHITECTURE.md` for constraints  
3. **Philosophical context**: `core-principles.md` for deeper understanding
4. **All changes**: Must maintain architectural consistency across files

## Cross-References

- **Implementation guides**: See `../implementation/` for step-by-step development
- **Testing strategies**: See `../testing/` for validation approaches
- **Design resources**: See `../design/` for styling and theming
- **Reference materials**: See `../reference/` for external documentation