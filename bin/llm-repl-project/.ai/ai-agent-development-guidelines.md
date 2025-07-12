# Guidelines for AI Coding Agents: Architecturally Sound, Regression-Free Development

These principles are addressed directly to AI coding agents (such as Claude Code, Gemini CLI, Cursor, and similar), outlining how to generate code and implement features that are architecturally robust and minimize regressions. These guidelines are specifically tailored to our Sacred GUI Architecture and LLM REPL project requirements.

## 1. Understand Context and Intent

### Core Principles
- **Clarify the Goal:** Before generating code, ensure you understand not only the requested feature but also its architectural motivation and intended impact within the Sacred Architecture.
- **Reference Existing Patterns:** Analyze relevant files, modules, and documentation to align your output with established V3 patterns and Sacred Timeline conventions.
- **Ask for Clarification:** If the user's intent or requirements are ambiguous, request further details before proceeding.

### Sacred Architecture Context Requirements
- **Read CLAUDE.md First:** Always understand project rules, Sacred GUI Architecture constraints, and V3 pattern requirements
- **Analyze Sacred Timeline Structure:** Understand the 2-way ↔ 3-way split design and V3's proven chat_container patterns
- **Review Existing Widgets:** Study `SimpleBlockWidget`, `SacredTimelineWidget`, and `LiveWorkspaceWidget` patterns before modifications
- **Understand Testing Requirements:** Reference `.ai/textual-testing-guide.md` for UX testing expectations

**Example Context Analysis:**
```markdown
Before implementing a new feature:
1. Read CLAUDE.md Sacred Architecture section
2. Review related widget implementations 
3. Check existing test patterns in tests/
4. Understand V3's proven patterns (no nested containers)
5. Clarify how feature integrates with Sacred Timeline/Live Workspace
```

## 2. Plan Before Coding

### Planning Requirements
- **Analyze Before Acting:** Read and summarize relevant code and design documents prior to making changes.
- **Develop a Stepwise Plan:** Outline a detailed, incremental plan for the implementation, including alternatives and reasoning for your chosen approach.
- **Validate Your Plan:** Review your plan for Sacred Architecture consistency and share it for feedback before proceeding to code.

### Sacred Architecture Planning Checklist
- [ ] **Widget Pattern Compliance:** Does the plan follow V3's simple widget + render() pattern?
- [ ] **Layout Conflict Prevention:** Will changes avoid nested containers in VerticalScroll widgets?
- [ ] **CSS Property Validation:** Are only valid Textual CSS properties used?
- [ ] **Testing Strategy:** How will Sacred Architecture compliance be tested?
- [ ] **Workspace Integration:** How does the feature integrate with 2-way ↔ 3-way splits?

**Example Planning Template:**
```markdown
## Implementation Plan: [Feature Name]

### Context Analysis
- Current Sacred Architecture state: [analysis]
- Relevant existing patterns: [V3 patterns to follow]
- Testing requirements: [UX testing needs]

### Proposed Changes
1. **Widget Modifications:** [specific changes with V3 pattern compliance]
2. **CSS Updates:** [valid Textual properties only]
3. **Testing Additions:** [UX testing for Sacred Architecture]

### Validation Checkpoints
- [ ] No nested container conflicts
- [ ] V3 pattern compliance
- [ ] Sacred Architecture integrity maintained
```

## 3. Implement Incrementally and Transparently

### Implementation Standards
- **Small, Testable Steps:** Break down feature development into small, verifiable increments that maintain Sacred Architecture integrity.
- **Self-Review:** After generating code, review your own output for architectural fit, V3 pattern compliance, and adherence to project rules.
- **Document Changes:** Update documentation, test files, and CSS as part of each change.

### Sacred Architecture Implementation Rules
- **V3 Pattern Compliance:** Always use `VerticalScroll` + simple `Widget` children with `render()` methods
- **CSS Validation:** Only use valid Textual CSS properties (`border: solid blue` not `border-color: blue`)
- **Timeline Integration:** Ensure changes work with both Sacred Timeline and Live Workspace
- **Testing Integration:** Add UX tests that validate Sacred Architecture behavior

**Implementation Example:**
```python
# ✅ CORRECT: V3 Pattern with render() method
class NewFeatureWidget(Widget):
    def __init__(self, data):
        super().__init__()
        self.data = self._validate_data(data)  # Fail-fast validation
    
    def render(self) -> RenderableType:
        # Direct render like V3's Chatbox - no child widgets
        return Panel(self._build_content(), border_style="solid")
    
    def _validate_data(self, data):
        if not hasattr(data, 'required_field'):
            raise ValueError("Invalid data: missing required_field")
        return data

# ❌ WRONG: Nested containers
class BadWidget(Vertical):  # Never nest containers in VerticalScroll
    def compose(self):
        yield Vertical(...)  # This breaks Sacred Architecture
```

## 4. Enforce Project Rules and Constraints

### Project Rule Compliance
- **Respect CLAUDE.md Rules:** Always adhere to project-specific rules regarding Sacred Architecture, V3 patterns, dependencies, and modularity.
- **Limit Scope:** Restrict changes to relevant files and modules. Avoid making broad or unrelated modifications.
- **Maintain Consistency:** Ensure new code integrates seamlessly with existing Sacred Architecture patterns and coding standards.

### Sacred Architecture Constraints
- **No Nested Containers:** Never put `Vertical` inside `VerticalScroll` - causes layout conflicts
- **V3 Pattern Enforcement:** Use simple widgets with `render()` methods, not complex child widget hierarchies
- **CSS Property Validation:** Use only valid Textual CSS syntax
- **Timeline Integrity:** Maintain UnifiedTimeline as single source of truth
- **Workspace Behavior:** Respect 2-way ↔ 3-way split transitions

**Rule Enforcement Checklist:**
```python
# Before any widget modification, verify:
def validate_sacred_architecture_compliance(widget_class):
    """Ensure widget follows Sacred Architecture rules"""
    # 1. Check inheritance pattern
    if issubclass(widget_class, VerticalScroll):
        # Must contain only simple widgets, not containers
        pass
    
    # 2. Verify render() method exists for simple widgets
    if hasattr(widget_class, 'render'):
        # Should return RenderableType, not yield child widgets
        pass
    
    # 3. Check CSS properties are valid
    css_file = widget_class._css_file
    if css_file and css_file.exists():
        validate_textual_css_properties(css_file)
```

## 5. Prioritize Testing and Validation

### Testing Requirements
- **Test-Driven Development:** Scaffold and update tests before or alongside implementation, especially for Sacred Architecture compliance.
- **Continuous Verification:** After each change, ensure all tests pass and run linting tools to catch errors or regressions.
- **UX Testing:** Use Textual's `run_test()` and `Pilot` for user experience validation.

### Sacred Architecture Testing Standards
- **Layout Conflict Testing:** Verify no nested containers exist in VerticalScroll widgets
- **V3 Pattern Testing:** Ensure widgets follow proven chat_container patterns
- **Workspace Transition Testing:** Validate 2-way ↔ 3-way split behavior
- **Visual Regression Testing:** Use snapshot testing for layout consistency
- **Performance Testing:** Verify no memory leaks or excessive resource usage

**Sacred Architecture Test Template:**
```python
@pytest.mark.asyncio
async def test_sacred_architecture_compliance():
    """Test that changes maintain Sacred Architecture integrity"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        sacred_timeline = app.query_one("#sacred-timeline")
        live_workspace = app.query_one("#live-workspace")
        
        # Verify V3 pattern compliance
        assert isinstance(sacred_timeline, VerticalScroll)
        assert isinstance(live_workspace, VerticalScroll)
        
        # Test no nested containers
        for child in sacred_timeline.children:
            assert not isinstance(child, (Vertical, Horizontal, VerticalScroll))
            assert hasattr(child, 'render')  # V3 render pattern
        
        # Test workspace transitions
        assert not live_workspace.is_visible  # Start 2-way
        live_workspace.show_workspace()
        assert live_workspace.is_visible     # 3-way split
        live_workspace.hide_workspace()
        assert not live_workspace.is_visible # Back to 2-way
```

## 6. Prevent Regressions

### Regression Prevention Strategies
- **Run Full Test Suites:** Execute all relevant tests after each change, not just those related to the feature.
- **Use Snapshot and Regression Testing:** Employ snapshot tests for UI outputs to detect unintended Sacred Architecture changes.
- **Analyze Impact:** Consider possible side effects on Sacred Timeline, Live Workspace, and widget interactions.

### Sacred Architecture Regression Guards
- **Layout Regression Testing:** Ensure Sacred Architecture layout remains intact
- **CSS Regression Testing:** Verify no invalid CSS properties are introduced
- **Performance Regression Testing:** Monitor memory usage and rendering performance
- **Workflow Regression Testing:** Validate complete user journeys still function

**Regression Testing Example:**
```python
@pytest.mark.asyncio
async def test_layout_regression_protection():
    """Prevent layout regressions in Sacred Architecture"""
    app = LLMReplApp()
    async with app.run_test() as pilot:
        # Add substantial content to test layout stability
        sacred_timeline = app.query_one("#sacred-timeline")
        
        for i in range(50):
            block = InscribedBlock(
                id=f"regression-test-{i}",
                role="user" if i % 2 == 0 else "assistant",
                content=f"Regression test content {i}",
                metadata={}
            )
            await sacred_timeline.add_block(block)
        
        # Verify layout integrity
        assert sacred_timeline.max_scroll_y > 0  # Scrollable
        assert sacred_timeline.get_block_count() == 50
        
        # Verify no layout corruption
        for child in sacred_timeline.children:
            assert child.styles.height != "100%"  # No equal distribution
            assert not isinstance(child, (Vertical, VerticalScroll))
```

## 7. Conduct Architectural Reviews

### Architectural Analysis Requirements
- **Proactive Analysis:** Regularly review the codebase for Sacred Architecture bottlenecks, inconsistencies, and opportunities for improvement.
- **Explain Reasoning:** When making architectural suggestions or changes, provide clear explanations aligned with V3 patterns and Sacred Architecture principles.
- **Suggest Alternatives:** Where multiple solutions exist, present alternatives and recommend the best fit for Sacred Architecture.

### Sacred Architecture Review Checklist
- **Widget Pattern Review:** Are all widgets following V3's proven patterns?
- **Layout Conflict Analysis:** Any nested containers causing issues?
- **CSS Property Audit:** All properties valid for Textual?
- **Performance Analysis:** Any memory leaks or rendering bottlenecks?
- **Testing Coverage:** Adequate UX testing for Sacred Architecture features?

**Architectural Review Template:**
```markdown
## Sacred Architecture Review: [Component/Feature]

### Current State Analysis
- **V3 Pattern Compliance:** [assessment]
- **Layout Integrity:** [no nested containers check]
- **CSS Validation:** [valid properties check]
- **Performance Profile:** [memory/rendering analysis]

### Identified Issues
1. **Issue:** [specific problem]
   **Impact:** [on Sacred Architecture]
   **Recommendation:** [V3-aligned solution]

### Improvement Opportunities
- **Pattern Enhancement:** [suggestions for better V3 compliance]
- **Performance Optimization:** [rendering/memory improvements]
- **Testing Enhancement:** [UX testing gaps]
```

## 8. Collaborate with Human Developers

### Collaboration Standards
- **Invite Review:** Encourage human review of plans and code before merging, especially for Sacred Architecture changes.
- **Respond to Feedback:** Be open to critique and ready to revise your approach based on feedback about V3 patterns or Sacred Architecture integrity.
- **Document Decisions:** Clearly record architectural decisions and the rationale behind them for future reference.

### Sacred Architecture Collaboration
- **Sacred Architecture Decisions:** Always explain how changes align with V3 patterns and Sacred Timeline design
- **Layout Impact Communication:** Clearly communicate any potential impact on 2-way ↔ 3-way split behavior
- **Testing Strategy Discussion:** Collaborate on UX testing approaches for Sacred Architecture features

**Collaboration Example:**
```markdown
## Change Request: [Feature Name]

### Sacred Architecture Impact Assessment
- **V3 Pattern Compliance:** This change follows V3's VerticalScroll + simple widget pattern
- **Layout Integrity:** No nested containers introduced, maintains Sacred Architecture
- **Workspace Integration:** [explanation of 2-way ↔ 3-way split impact]

### Human Review Needed
- [ ] Sacred Architecture pattern validation
- [ ] CSS property verification  
- [ ] UX testing strategy approval
- [ ] Performance impact assessment

### Questions for Human Review
1. Does this approach align with Sacred Architecture goals?
2. Are there V3 pattern considerations I've missed?
3. Should additional UX tests be added?
```

## 9. Manage and Evolve Guidance

### Guidance Evolution
- **Version Prompts and Rules:** Treat CLAUDE.md and AI guidelines as versioned artifacts—update and refine them as Sacred Architecture evolves.
- **Iterative Improvement:** Learn from feedback and real-world outcomes to continually improve workflow and Sacred Architecture compliance.

### Sacred Architecture Guidance Updates
- **Pattern Refinement:** Update guidelines as V3 patterns are refined or new proven patterns emerge
- **Testing Evolution:** Enhance UX testing guidelines based on Sacred Architecture testing experience
- **Performance Optimization:** Update guidelines based on performance learnings

## 10. Maintain Focus and Minimize Disruption

### Focus Requirements
- **Stay Within Sacred Architecture Context:** Only modify files and modules relevant to the current task within Sacred Architecture constraints.
- **Avoid Breaking Changes:** Do not introduce changes that break Sacred Timeline, Live Workspace, or V3 pattern interfaces.
- **Preserve Stability:** Strive to enhance Sacred Architecture's reliability, maintainability, and coherence with every contribution.

### Sacred Architecture Stability Rules
- **Sacred Timeline Integrity:** Never break the UnifiedTimeline single source of truth
- **V3 Pattern Preservation:** Maintain proven chat_container and Chatbox patterns
- **CSS Compatibility:** Only use validated Textual CSS properties
- **Workspace Behavior:** Preserve 2-way ↔ 3-way split functionality

## Sacred Architecture Compliance Summary

**Before every change, verify:**
- [ ] **V3 Pattern Compliance:** Using VerticalScroll + simple widgets with render() methods
- [ ] **No Nested Containers:** No Vertical inside VerticalScroll causing layout conflicts
- [ ] **Valid CSS Properties:** Only Textual-compatible CSS syntax used
- [ ] **Timeline Integrity:** UnifiedTimeline remains single source of truth
- [ ] **Workspace Behavior:** 2-way ↔ 3-way splits function correctly
- [ ] **Testing Coverage:** UX tests validate Sacred Architecture behavior
- [ ] **Performance Impact:** No memory leaks or rendering degradation
- [ ] **Documentation Updates:** CLAUDE.md and related docs updated as needed

**After every change, validate:**
- [ ] **Full Test Suite:** All tests pass including Sacred Architecture compliance tests
- [ ] **Lint Compliance:** MyPy and linting tools report no errors
- [ ] **Layout Verification:** No visual regression in Sacred Architecture
- [ ] **Performance Check:** Memory usage and rendering performance maintained

By following these guidelines specifically tailored to our Sacred GUI Architecture, AI coding agents can produce code that is not only functionally correct but also architecturally robust, maintains V3 patterns, and ensures the long-term health of our proven Sacred Timeline and Live Workspace design.

---

**References:** These guidelines synthesize best practices for AI agent development with our specific Sacred GUI Architecture requirements, V3 proven patterns, and UX testing standards. Always consult CLAUDE.md and `.ai/textual-testing-guide.md` for current project-specific requirements.