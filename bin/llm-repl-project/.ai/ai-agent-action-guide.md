# AI Agent Action Guide for Working Within the Sacred Architecture & Ledger Framework

This guide provides explicit, actionable steps for AI agents to ensure their work is fully aligned with our Sacred GUI Architecture philosophy and ledger-driven development process. The focus is on keeping `.ai` documentation current, rigorously using the ledger system, and transparently documenting and testing progress throughout Sacred Architecture development.

## 1. Always Begin with Sacred Architecture Context Review

### Required Reading (In Order)

**Before any new task, read:**

1. **Core Project Context:**
   - `CLAUDE.md` - Sacred Architecture rules, V3 patterns, project constraints
   - `.ai/project.md` - Goals, requirements, and workflow (if exists)
   - `.ai/patterns.md` - Coding conventions and anti-patterns (if exists)  
   - `.ai/architecture.md` - System design and decisions (if exists)

2. **Sacred Architecture Context:**
   - `src/main.py` - Sacred Architecture layout implementation
   - `src/widgets/sacred_timeline.py` - V3's chat_container pattern
   - `src/widgets/live_workspace.py` - Cognition workspace implementation
   - `src/widgets/simple_block.py` - V3's Chatbox pattern

3. **Development Context:**
   - `.ai/textual-testing-guide.md` - UX testing requirements
   - `.ai/ai-agent-development-guidelines.md` - Development principles
   - `.ai/ai-agent-implementation-workflows.md` - Specific behaviors

4. **Feature-Specific Context:**
   - `.ai/ledgers/v3.1/[feature-name].md` - Current feature requirements, status, and blockers
   - Run `just ledger-status` to see current state and suggested next ledger

### Context Summary Template

After reading, create a context summary:

```markdown
## Sacred Architecture Context Summary

### Current Sacred Architecture State
- **Sacred Timeline:** [V3 pattern compliance status]
- **Live Workspace:** [2-way ↔ 3-way split status]
- **CSS Properties:** [valid Textual property usage]
- **Testing Coverage:** [UX testing completeness]

### Feature Context: [Feature Name]
- **Requirements:** [from ledger]
- **Status:** [current progress]
- **Blockers:** [any identified issues]
- **Sacred Architecture Impact:** [timeline/workspace integration needs]

### Constraints Identified
- V3 Pattern Requirements: [specific constraints]
- Sacred Architecture Rules: [layout/integration constraints]
- Testing Requirements: [UX validation needs]
```

## 2. Plan and Log Every Step in the Ledger

### Ledger Planning Requirements

**For every feature task:**

1. **Summarize Understanding**
   - Write concise summary of feature understanding
   - Reference Sacred Architecture context and constraints
   - Document V3 pattern compliance requirements

2. **Draft Sacred Architecture-Compliant Plan**
   - List concrete steps that maintain V3 patterns
   - Reference Sacred Architecture decisions and constraints
   - Include CSS property validation steps
   - Plan UX testing approach

3. **Log in Feature Ledger**
   - Record plan under new dated entry
   - Include alternatives considered with Sacred Architecture rationale
   - Document Sacred Timeline/Live Workspace integration approach

### Ledger Entry Template

```markdown
## [Date] - Sacred Architecture Implementation Plan

### Context Understanding
- **Feature Goal:** [description]
- **Sacred Architecture Requirements:** [V3 compliance needs]
- **Integration Points:** [Sacred Timeline/Live Workspace]

### Implementation Plan
1. **Widget Development:** [V3 pattern approach]
   - Use simple widgets with render() methods
   - Avoid nested containers in VerticalScroll
   - Validate CSS properties for Textual compatibility

2. **Sacred Architecture Integration:**
   - [Sacred Timeline integration approach]
   - [Live Workspace integration approach]  
   - [Workspace transition preservation]

3. **Testing Strategy:**
   - [UX tests for Sacred Architecture compliance]
   - [Layout conflict prevention tests]
   - [Workspace transition validation]

### Alternatives Considered
- **Alternative 1:** [approach with Sacred Architecture pros/cons]
- **Alternative 2:** [approach with Sacred Architecture pros/cons]
- **Chosen Approach:** [rationale for Sacred Architecture compliance]

### Sacred Architecture Risks
- [Potential V3 pattern violations]
- [Layout conflict possibilities]
- [Workspace behavior impacts]
```

## 3. Implement Incrementally and Transparently

### Sacred Architecture Incremental Implementation

**Small, Sacred Architecture-Compliant Steps:**

1. **Widget Structure (V3 Compliance)**
   ```python
   # Step 1: Create V3-compliant widget structure
   class FeatureWidget(Widget):
       def render(self) -> RenderableType:
           return Panel("Implementation step 1", border_style="solid")
   ```

2. **CSS Integration (Valid Properties)**
   ```css
   /* Step 2: Add valid Textual CSS */
   .feature-widget {
       height: auto;  /* V3 pattern */
       border: solid $primary;  /* Valid Textual CSS */
   }
   ```

3. **Sacred Architecture Integration**
   ```python
   # Step 3: Integrate with Sacred Timeline or Live Workspace
   async def integrate_with_sacred_architecture():
       # Implementation maintaining V3 patterns
   ```

### Ledger Progress Documentation

**After each step, update ledger:**

```markdown
### [Date/Time] - Implementation Step [N]

#### What Was Done
- [Specific Sacred Architecture changes made]
- [V3 pattern compliance maintained how]
- [CSS properties validated]

#### Tests
- **Tests Run:** [specific test commands]
- **Results:** [pass/fail with Sacred Architecture focus]
- **New Tests Added:** [UX tests for Sacred Architecture compliance]

#### Sacred Architecture Validation
- ✅/❌ V3 pattern compliance maintained
- ✅/❌ No nested container violations
- ✅/❌ Valid Textual CSS properties only
- ✅/❌ Sacred Timeline/Workspace integration preserved

#### Issues Encountered
- [Any Sacred Architecture challenges]
- [V3 pattern conflicts resolved]
- [CSS property validation issues]

#### Next Steps
- [Remaining Sacred Architecture integration work]
- [Additional testing needed]
```

## 4. Keep All `.ai` Documentation Up to Date

### Sacred Architecture Documentation Updates

**Update documentation immediately when:**

1. **New V3 Pattern Usage:**
   - Update `.ai/ai-agent-development-guidelines.md` with new patterns
   - Document in CLAUDE.md Sacred Architecture section
   - Add to `.ai/ai-agent-implementation-workflows.md` if workflow changes

2. **Sacred Architecture Decisions:**
   - Record architectural decisions in feature ledger
   - Update CLAUDE.md if affecting overall Sacred Architecture
   - Document rationale for V3 pattern choices

3. **CSS Property Discoveries:**
   - Update valid Textual CSS property lists
   - Document new styling patterns for Sacred Architecture
   - Add to CSS validation guidelines

### Documentation Synchronization

**Keep synchronized:**
- Feature ledgers ↔ CLAUDE.md Sacred Architecture section
- Implementation decisions ↔ AI agent guidelines
- Testing patterns ↔ UX testing guide
- V3 pattern usage ↔ Sacred Architecture documentation

## 5. Rigorously Use the Ledger System

### Ledger as Sacred Architecture Source of Truth

**Feature ledger must contain:**

1. **Sacred Architecture Requirements:**
   - V3 pattern compliance needs
   - Sacred Timeline/Live Workspace integration requirements
   - CSS property constraints
   - Workspace transition preservation needs

2. **Implementation Progress:**
   - Each Sacred Architecture-compliant step
   - V3 pattern validation results
   - CSS property validation
   - UX testing outcomes

3. **Decisions and Rationale:**
   - Why specific V3 patterns were chosen
   - Sacred Architecture trade-offs made
   - Alternative approaches considered

### Continuous Sacred Architecture Documentation

**Log immediately:**
- Sacred Architecture compliance checks
- V3 pattern validation results
- CSS property validation outcomes
- Workspace transition testing
- Layout conflict prevention measures

### Sacred Architecture Blockers and Questions

**Document in ledger:**
```markdown
### Sacred Architecture Blocker: [Date]

#### Issue
[Specific Sacred Architecture challenge]

#### V3 Pattern Impact
[How this affects V3 compliance]

#### Workspace Behavior Impact  
[Effect on 2-way ↔ 3-way splits]

#### Human Review Needed
- [ ] Sacred Architecture pattern validation
- [ ] V3 compliance verification
- [ ] CSS property approval
- [ ] Workspace behavior review

#### Questions for Human Review
1. [Specific Sacred Architecture question]
2. [V3 pattern compliance question]
3. [Workspace integration question]
```

## 6. Validate and Invite Review

### Sacred Architecture Self-Check After Each Step

**Validate:**
- ✅ V3 pattern compliance (VerticalScroll + simple widgets)
- ✅ No nested container violations
- ✅ Valid Textual CSS properties only
- ✅ Sacred Timeline integrity preserved
- ✅ Live Workspace transition behavior maintained
- ✅ UX tests pass for Sacred Architecture features

### Human Review Flag Template

```markdown
### [Date] - Human Review Required

#### Sacred Architecture Changes Made
[Summary of V3 pattern and Sacred Architecture modifications]

#### Review Needed For
- [ ] **V3 Pattern Compliance:** [specific validation needed]
- [ ] **Sacred Architecture Integration:** [integration approach approval]
- [ ] **CSS Property Usage:** [Textual compatibility verification]
- [ ] **Workspace Behavior:** [transition behavior validation]
- [ ] **Testing Strategy:** [UX testing approach approval]

#### Sacred Architecture Risks Identified
- [Potential layout conflicts]
- [V3 pattern violations]
- [Workspace behavior impacts]

#### Questions for Human Reviewer
1. Does this maintain Sacred Architecture integrity?
2. Are V3 patterns correctly applied?
3. Should additional Sacred Architecture tests be added?
```

## 7. Maintain and Evolve Sacred Architecture Context

### Proactive Sacred Architecture Updates

**When to update `.ai` documentation:**

1. **New V3 Pattern Discovery:**
   - Immediately update `.ai/ai-agent-development-guidelines.md`
   - Add to Sacred Architecture examples in CLAUDE.md
   - Document in implementation workflows

2. **Sacred Architecture Enhancement:**
   - Update Sacred Architecture section in CLAUDE.md
   - Enhance UX testing guide with new patterns
   - Document in feature ledgers

3. **CSS Property Validation Updates:**
   - Update valid property lists
   - Document new Textual compatibility findings
   - Add to CSS validation workflows

### Archive and Curate Sacred Architecture Ledgers

**Ledger management:**
- Move completed feature ledgers to `.ai/ledgers/archived/`
- Extract Sacred Architecture patterns for documentation
- Update `.ai/ledgers/_active.md` with ongoing Sacred Architecture work
- Document V3 pattern lessons learned

## 8. Sacred Architecture Workflow Table

| Step | Concrete Agent Action | Sacred Architecture Focus | Wrinkl Artifact Updated |
|------|----------------------|---------------------------|-------------------------|
| **Context Review** | Read CLAUDE.md, Sacred Architecture widgets, feature ledger | V3 pattern understanding, workspace behavior | None |
| **Plan** | Summarize Sacred Architecture context, outline V3-compliant steps | Sacred Timeline/Workspace integration approach | `.ai/ledgers/[feature].md` |
| **Implement** | Code V3-compliant widgets, validate CSS, maintain patterns | Sacred Architecture integrity preservation | `.ai/ledgers/[feature].md` |
| **Test** | Run UX tests, validate Sacred Architecture compliance | Layout conflict prevention, workspace transitions | `.ai/ledgers/[feature].md` |
| **Document** | Update Sacred Architecture docs, record V3 pattern decisions | Pattern evolution, architectural decisions | `CLAUDE.md`, `.ai/` guides |
| **Archive** | Move completed ledger, extract Sacred Architecture patterns | V3 pattern documentation, lessons learned | `.ai/ledgers/archived/`, `_active.md` |

## 9. Key Principles for AI Agents in Sacred Architecture Development

### Core Principles

- **Sacred Architecture-Driven:** Every action preserves V3 patterns and Sacred Timeline/Workspace design
- **Transparent Progress:** All Sacred Architecture decisions, tests, and validation logged in real time
- **V3 Pattern-Aligned:** Code always reflects proven chat_container and Chatbox patterns
- **Incremental Validation:** Each step maintains Sacred Architecture integrity with validation
- **Collaborative Review:** Human review invited for Sacred Architecture decisions with clear rationale

### Sacred Architecture Compliance Checklist

**Before every change:**
- [ ] Read Sacred Architecture context (CLAUDE.md, existing widgets)
- [ ] Plan V3-compliant approach with alternatives
- [ ] Validate CSS properties for Textual compatibility
- [ ] Consider Sacred Timeline/Workspace integration impact

**During implementation:**
- [ ] Use simple widgets with render() methods (V3 pattern)
- [ ] Avoid nested containers in VerticalScroll widgets
- [ ] Validate CSS properties continuously
- [ ] Log all Sacred Architecture decisions in ledger

**After each step:**
- [ ] Run Sacred Architecture compliance tests
- [ ] Validate workspace transition behavior
- [ ] Update ledger with V3 pattern validation results
- [ ] Flag any Sacred Architecture risks for human review

**Before completion:**
- [ ] Full Sacred Architecture regression testing
- [ ] UX testing for Sacred Timeline/Workspace integration
- [ ] Documentation updates for V3 pattern usage
- [ ] Human review request for Sacred Architecture validation

By following these concrete steps specifically tailored to our Sacred GUI Architecture, AI agents will ensure their work maintains V3 patterns, preserves Sacred Timeline and Live Workspace integrity, and follows our ledger-driven, context-aware development philosophy while enabling transparent human collaboration throughout the development process.

---

**References:** This guide integrates with `.ai/ai-agent-development-guidelines.md` for comprehensive principles, `.ai/ai-agent-implementation-workflows.md` for specific behaviors, and `.ai/textual-testing-guide.md` for Sacred Architecture testing requirements. Always consult CLAUDE.md for current Sacred Architecture constraints and V3 pattern specifications.