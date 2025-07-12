# AI Agent Development Guidelines

> **Core Principle**: Build from KNOWN working implementations. Study V3, Gemini CLI, and Claude Code patterns before writing any new code.

## Agent Operating Principles

### 1. Research-First Development

```
🔍 MANDATORY RESEARCH PHASE:
   ↓
📚 Study CLAUDE.md entry point
   ↓
📚 Read relevant .ai/docs/ guide
   ↓
📚 Examine working reference code (V3, Claude Code, Gemini CLI)
   ↓
📚 Understand Sacred Architecture constraints
   ↓
🛠️ Only then begin implementation
```

### 2. Build From Working Code

**Never Start From Scratch**:
- Always find a working example first
- Copy proven patterns, adapt for Sacred GUI
- When stuck, research how others solved it
- Prefer tested patterns over novel solutions

**Primary References (In Order)**:
1. **V3 Chat Implementation** - `V3/elia_chat/widgets/chat.py`
2. **Claude Code Package** - `reference/inspiration/anthropic-ai-claude-code/`
3. **Gemini CLI** - `reference/inspiration/gemini-cli/`
4. **Textual Examples** - `reference/textual-docs/textual/examples/`

### 3. Sacred Architecture Compliance

**Immutable Rules**:
- Use V3's VerticalScroll + render() pattern (no nested containers)
- Maintain three-area layout (Sacred Timeline + Live Workspace + Input)
- Follow 2-way ↔ 3-way split behavior
- Preserve Sacred Timeline immutability
- Implement thread-safe streaming updates

**Validation Requirements**:
- Test against V3 patterns
- Verify no layout conflicts
- Ensure error boundaries work
- Validate CSS uses only valid Textual properties

## Agent Behavior Workflows

### Feature Implementation Workflow

1. **Planning Phase**:
   - Read feature requirements from `.ai/ledgers/v3.1/`
   - Study relevant `.ai/docs/` guides
   - Identify working reference patterns
   - Document implementation approach

2. **Research Phase**:
   - Examine V3 equivalent functionality
   - Find similar patterns in Claude Code/Gemini CLI
   - Review Textual framework examples
   - Note specific code to copy/adapt

3. **Implementation Phase**:
   - Copy working pattern as starting point
   - Adapt for Sacred Architecture needs
   - Add fail-fast validation
   - Include error boundary support

4. **Validation Phase**:
   - Test that pattern works like reference
   - Verify Sacred Architecture compliance
   - Run comprehensive test suite
   - Document changes and rationale

5. **Review Phase**:
   - Request human review of visual changes
   - Provide specific behaviors to test
   - Wait for approval before marking complete
   - Address feedback and iterate

### Code Review Workflow

**When Reviewing Code**:
- Check for V3 pattern compliance
- Verify no nested container anti-patterns
- Ensure error handling doesn't break app
- Validate CSS uses only valid Textual properties
- Test streaming behavior works correctly
- Confirm Sacred Architecture layout preserved

**When Providing Feedback**:
- Reference specific V3 patterns when suggesting changes
- Provide working code examples
- Explain architectural reasoning
- Suggest specific reference implementations to study

### Debugging Workflow

**When Code Doesn't Work**:
1. Compare against working V3 pattern
2. Check for common anti-patterns (nested containers, invalid CSS)
3. Verify thread-safe update patterns
4. Test with error boundary simulation
5. Validate against Sacred Architecture rules

**When Performance Issues**:
1. Profile against V3 baseline performance
2. Check for memory leaks in widget cleanup
3. Verify smart auto-scroll behavior
4. Test with high-volume content simulation

## Communication Guidelines

### With Humans

**When Requesting Review**:
- Clearly state what visual behaviors to test
- Provide exact command to run application
- List specific Sacred Architecture features to verify
- Explain what working reference pattern was used

**When Providing Updates**:
- Reference specific V3 patterns implemented
- Note any adaptations made and why
- Document test results and validation performed
- Highlight any architectural decisions made

### With Other Agents

**When Collaborating**:
- Share reference patterns being used
- Document Sacred Architecture compliance approach
- Provide clear interface specifications
- Note any working code patterns discovered

**When Documenting**:
- Reference specific working implementations
- Explain why patterns were chosen
- Document architectural decision rationale
- Provide validation steps for future agents

## Quality Standards

### Code Quality Requirements

```
☐ Uses V3's proven patterns (VerticalScroll + render())
☐ Follows Sacred Architecture layout rules
☐ Includes fail-fast validation at boundaries
☐ Implements error boundary support
☐ Uses only valid Textual CSS properties
☐ Provides thread-safe streaming updates
☐ Handles dynamic content sizing correctly
☐ Maintains smart auto-scroll behavior
☐ Includes comprehensive test coverage
☐ Documents reference patterns used
```

### Architectural Compliance

```
☐ No nested containers in VerticalScroll widgets
☐ Maintains Sacred Timeline immutability
☐ Implements 2-way ↔ 3-way split behavior
☐ Preserves three-area layout structure
☐ Follows Sacred Turn structure (User → Cognition → Assistant)
☐ Uses V3's thread-safe update patterns
☐ Implements content-driven dynamic sizing
☐ Provides graceful error handling
☐ Maintains performance comparable to V3
☐ Validates against working reference behavior
```

### Documentation Standards

```
☐ References working implementations used
☐ Documents adaptation rationale
☐ Explains architectural decisions
☐ Provides validation steps
☐ Includes error handling approach
☐ Notes performance considerations
☐ Updates relevant .ai/docs/ guides
☐ Maintains cross-reference consistency
```

## Agent Interaction Patterns

### Repository Navigation

**Always Start Here**:
1. `CLAUDE.md` - Entry point and quick reference
2. `.ai/docs/ARCHITECTURE-GUIDE.md` - Sacred GUI principles
3. `.ai/docs/IMPLEMENTATION-GUIDE.md` - V3 patterns and code
4. Working references - V3, Claude Code, Gemini CLI

**For Specific Tasks**:
- **Widget Development** → `Implementation Guide` + V3 examples
- **CSS Styling** → `Design Guide` + V3 CSS patterns
- **Testing** → `Testing Guide` + test harnesses
- **Feature Planning** → `.ai/ledgers/v3.1/` + Architecture Guide

### Error Recovery Patterns

**When Implementation Fails**:
1. Return to working reference implementation
2. Compare exact differences with broken code
3. Re-read Sacred Architecture constraints
4. Test isolated components before integration
5. Validate against V3 behavior patterns

**When Architectural Issues Arise**:
1. Re-examine Sacred Architecture principles
2. Study V3's exact implementation approach
3. Verify no anti-patterns introduced
4. Test with reference implementation for comparison
5. Document issues for future agent learning

## Prohibited Patterns

### Never Do These

```
❌ Write widgets from scratch without studying V3
❌ Create nested containers in VerticalScroll
❌ Use invalid CSS properties (border-color, background-color)
❌ Run GUI applications (breaks Claude Code interface)
❌ Self-approve work without human review
❌ Skip reference implementation research
❌ Reinvent patterns that already work
❌ Break Sacred Architecture layout rules
❌ Ignore fail-fast validation requirements
❌ Create untested streaming update patterns
```

### Always Do These

```
✅ Study V3 patterns before implementing
✅ Copy working code, adapt for Sacred GUI
✅ Use VerticalScroll + render() pattern
✅ Implement fail-fast validation
✅ Include error boundary support
✅ Test against reference behavior
✅ Document working patterns used
✅ Request human review for visual changes
✅ Maintain Sacred Architecture compliance
✅ Follow proven thread-safe patterns
```

## Success Metrics

### Implementation Success

- **Pattern Compliance**: Uses V3's exact patterns where applicable
- **Architecture Adherence**: Maintains Sacred GUI three-area layout
- **Error Resilience**: Graceful handling without app crashes
- **Performance**: Comparable to V3 reference implementation
- **Testability**: Comprehensive test coverage with harnesses

### Collaboration Success

- **Reference Usage**: Consistently builds from working implementations
- **Documentation Quality**: Clear rationale and validation steps
- **Review Efficiency**: Specific, testable behaviors for human review
- **Knowledge Transfer**: Other agents can build on documented patterns

### Project Success

- **Sacred Architecture Integrity**: Layout rules never violated
- **V3 Pattern Adoption**: Proven patterns used throughout
- **Error Boundary Coverage**: All major UI sections protected
- **Performance Maintenance**: No regressions from reference implementations
- **Test Suite Robustness**: Comprehensive validation of all patterns

---

**Remember**: Your primary job is to build reliable software by copying proven patterns. Innovation comes through intelligent adaptation of working solutions, not reinvention from scratch.