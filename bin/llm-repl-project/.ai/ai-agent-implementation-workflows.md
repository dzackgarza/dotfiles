# Specific Guidelines for AI Coding Agents: Architectural Review, Refactoring, and Robust Implementation

This guide provides concrete, actionable instructions for AI coding agents (e.g., Claude Code, Gemini CLI, Cursor) to produce architecturally robust, maintainable, and regression-resistant code. The focus is on explicit behaviors and workflows for reviewing, refactoring, scaffolding, and collaborating effectively within our Sacred GUI Architecture.

## 1. Architectural Review and Analysis

### a. Reading and Summarizing (Required Before Any Implementation)

**Before any implementation, read all relevant files, modules, and architectural documents:**

1. **Sacred Architecture Core Files (Always Read First):**
   - `CLAUDE.md` - Project rules and Sacred Architecture constraints
   - `src/main.py` - Sacred Architecture layout implementation
   - `src/widgets/sacred_timeline.py` - V3's chat_container pattern
   - `src/widgets/live_workspace.py` - Cognition workspace implementation
   - `src/widgets/simple_block.py` - V3's Chatbox pattern
   - `.ai/textual-testing-guide.md` - UX testing requirements

2. **Summarization Requirements:**
   - **Overall Structure:** Identify Sacred Timeline vs Live Workspace separation
   - **Key Interfaces:** UnifiedTimeline, V3 widget patterns, event flow
   - **Dependencies:** Sacred Architecture dependencies and constraints
   - **V3 Patterns:** Document chat_container and Chatbox pattern usage

**Example Architectural Summary Template:**
```markdown
## Sacred Architecture Analysis

### Current Structure
- **Sacred Timeline:** VerticalScroll + SimpleBlockWidget children (V3 chat_container pattern)
- **Live Workspace:** VerticalScroll + SubModuleWidget children (V3 chat_container pattern)
- **Layout Pattern:** 2-way ↔ 3-way split with workspace show/hide transitions

### Key Interfaces
- **UnifiedTimeline:** Single source of truth for all blocks
- **Widget Pattern:** Simple widgets with render() methods (V3 Chatbox pattern)
- **Event Flow:** User input → Sacred Timeline → Live Workspace → processing

### V3 Pattern Compliance
- ✅ VerticalScroll containers with simple widget children
- ✅ No nested Vertical containers causing layout conflicts
- ✅ Widgets use render() method pattern
- ✅ Content-based height with `height: auto` CSS

### Constraints Identified
- No nested containers allowed in VerticalScroll widgets
- Only valid Textual CSS properties permitted
- Must maintain 2-way ↔ 3-way split behavior
- UnifiedTimeline single source of truth must be preserved
```

### b. Flagging Inconsistencies (Sacred Architecture Focus)

**Scan for Sacred Architecture violations:**

- **Layout Conflicts:** Nested `Vertical` containers inside `VerticalScroll` widgets
- **V3 Pattern Violations:** Widgets not using render() method pattern
- **CSS Property Issues:** Invalid Textual CSS properties (e.g., `border-color` instead of `border: solid color`)
- **Timeline Integrity:** Multiple sources of truth or UnifiedTimeline bypassing
- **Workspace Behavior:** Broken 2-way ↔ 3-way split transitions
- **Testing Gaps:** Missing UX tests for Sacred Architecture compliance

**Inconsistency Detection Template:**
```python
def detect_sacred_architecture_violations():
    """Detect common Sacred Architecture violations"""
    violations = []
    
    # Check for nested containers
    for widget_file in glob("src/widgets/*.py"):
        if contains_nested_containers(widget_file):
            violations.append(f"Nested containers in {widget_file}")
    
    # Check CSS properties
    for css_file in glob("src/widgets/*.tcss"):
        invalid_props = validate_textual_css(css_file)
        if invalid_props:
            violations.append(f"Invalid CSS in {css_file}: {invalid_props}")
    
    # Check timeline integrity
    if multiple_timeline_sources():
        violations.append("Multiple timeline sources detected")
    
    return violations
```

### c. Suggesting Refactorings (V3 Pattern Alignment)

**Propose refactorings with Sacred Architecture rationale:**

1. **V3 Pattern Compliance Refactoring:**
   ```python
   # ❌ Current (if problematic)
   class ProblematicWidget(Vertical):
       def compose(self):
           yield Static("Header")
           yield Vertical(...)  # Nested container!
   
   # ✅ Refactored (V3 compliant)
   class RefactoredWidget(Widget):
       def render(self) -> RenderableType:
           # Direct render like V3's Chatbox
           return Panel(self._build_content(), border_style="solid")
   ```

2. **CSS Property Refactoring:**
   ```css
   /* ❌ Invalid Textual CSS */
   .widget {
       border-color: blue;
       border-style: solid;
   }
   
   /* ✅ Valid Textual CSS */
   .widget {
       border: solid blue;
   }
   ```

3. **Timeline Integration Refactoring:**
   ```python
   # ❌ Bypassing UnifiedTimeline
   def add_message_directly(content):
       widget.add_child(MessageWidget(content))
   
   # ✅ Using UnifiedTimeline
   def add_message_properly(content):
       block = unified_timeline.add_live_block("user", content)
       inscribed = await unified_timeline.inscribe_block(block.id)
       await sacred_timeline.add_block(inscribed)
   ```

**Refactoring Proposal Template:**
```markdown
## Sacred Architecture Refactoring Proposal

### Current Issue
[Specific violation of V3 patterns or Sacred Architecture]

### Proposed Solution
[V3-compliant approach with code examples]

### Benefits
- Maintains Sacred Architecture integrity
- Follows proven V3 patterns
- Prevents layout conflicts
- Improves testability

### Risks
- [Any potential impact on existing functionality]
- [Migration considerations]

### Implementation Steps
1. [Step-by-step refactoring plan]
2. [Testing validation requirements]
3. [Rollback strategy if needed]
```

## 2. Implementation Planning and Scaffolding

### a. Scaffolding Requirements (Sacred Architecture)

**Before coding, outline necessary scaffolding with Sacred Architecture compliance:**

1. **Widget Scaffolding Checklist:**
   ```python
   # Widget file structure
   src/widgets/new_feature_widget.py:
   - Class inheriting from Widget (not Vertical/Horizontal)
   - render() method returning RenderableType
   - Input validation in __init__
   - CSS class management
   - Sacred Architecture integration methods
   
   # CSS file structure  
   src/widgets/new_feature_widget.tcss:
   - Valid Textual CSS properties only
   - Sacred Architecture styling patterns
   - Responsive design considerations
   
   # Test file structure
   tests/test_widgets/test_new_feature_widget.py:
   - Sacred Architecture compliance tests
   - V3 pattern validation tests
   - UX interaction tests using Pilot
   - Regression prevention tests
   ```

2. **Sacred Architecture Integration Scaffolding:**
   ```python
   # Integration points to scaffold
   - UnifiedTimeline integration methods
   - Sacred Timeline or Live Workspace integration
   - Event handling for workspace transitions
   - CSS loading and validation
   - Error boundary integration
   ```

### b. Incremental Implementation (V3 Pattern Compliance)

**Break down implementation into Sacred Architecture-compliant steps:**

1. **Step 1: Widget Structure (V3 Compliance)**
   ```python
   class NewFeatureWidget(Widget):
       def __init__(self, data):
           super().__init__()
           self.data = self._validate_data(data)  # Fail-fast
           self.add_class("new-feature")
       
       def render(self) -> RenderableType:
           # V3 pattern: direct render, no child widgets
           return Panel("Placeholder", border_style="solid")
       
       def _validate_data(self, data):
           # Sacred Architecture: fail-fast validation
           if not data:
               raise ValueError("Data cannot be empty")
           return data
   ```

2. **Step 2: CSS Integration (Valid Properties)**
   ```css
   .new-feature {
       height: auto;  /* V3 pattern: content-based height */
       width: auto;
       border: solid $primary;  /* Valid Textual CSS */
       padding: 1;
   }
   ```

3. **Step 3: Sacred Architecture Integration**
   ```python
   # Integration with Sacred Timeline or Live Workspace
   async def integrate_with_sacred_architecture(self):
       if self.workspace_integration:
           await live_workspace.add_sub_module(self.create_sub_module())
       else:
           await sacred_timeline.add_block(self.create_block())
   ```

4. **Step 4: Testing (UX and Compliance)**
   ```python
   @pytest.mark.asyncio
   async def test_sacred_architecture_compliance():
       """Test V3 pattern compliance and Sacred Architecture integration"""
       widget = NewFeatureWidget(test_data)
       
       # V3 pattern compliance
       assert hasattr(widget, 'render')
       assert not isinstance(widget, (Vertical, Horizontal))
       
       # Sacred Architecture integration
       app = LLMReplApp()
       async with app.run_test() as pilot:
           # Test integration without layout conflicts
           pass
   ```

## 3. Delegation and Sub-Agent Utilization

### a. Delegating Subtasks (Sacred Architecture Context)

**For complex Sacred Architecture tasks, delegate appropriately:**

1. **Research Delegation:**
   ```markdown
   Sub-Agent Task: Sacred Architecture Pattern Research
   - Review existing V3 widgets for pattern consistency
   - Analyze Sacred Timeline vs Live Workspace integration points
   - Document current CSS property usage patterns
   - Identify testing patterns for Sacred Architecture compliance
   ```

2. **Code Review Delegation:**
   ```markdown
   Sub-Agent Task: Sacred Architecture Code Review
   - Check for nested container violations
   - Validate CSS property usage
   - Verify V3 pattern compliance
   - Assess Sacred Architecture integration impact
   ```

3. **Testing Delegation:**
   ```markdown
   Sub-Agent Task: Sacred Architecture Test Generation
   - Generate UX tests using Textual's run_test() and Pilot
   - Create layout conflict prevention tests
   - Develop workspace transition validation tests
   - Build performance regression tests
   ```

### b. Coordinating Sub-Agent Output (Sacred Architecture Synthesis)

**Integrate sub-agent results for Sacred Architecture consistency:**

```python
def synthesize_sacred_architecture_findings(sub_agent_outputs):
    """Coordinate sub-agent findings for Sacred Architecture compliance"""
    
    # Consolidate V3 pattern findings
    v3_compliance = merge_v3_pattern_analysis(sub_agent_outputs)
    
    # Resolve conflicting CSS recommendations
    css_recommendations = resolve_css_conflicts(sub_agent_outputs)
    
    # Validate Sacred Architecture integration
    integration_strategy = validate_integration_approach(sub_agent_outputs)
    
    return {
        'v3_compliance': v3_compliance,
        'css_strategy': css_recommendations,
        'integration': integration_strategy,
        'testing_approach': consolidate_testing_strategies(sub_agent_outputs)
    }
```

## 4. Explicit Workflows for Code Generation

### a. Reading and Summarizing (Sacred Architecture Workflow)

**Mandatory workflow before any Sacred Architecture changes:**

```markdown
Step 1: Sacred Architecture Context Analysis
"Read the following Sacred Architecture files:
- CLAUDE.md (Sacred Architecture section)
- src/widgets/sacred_timeline.py
- src/widgets/live_workspace.py  
- src/widgets/simple_block.py

Summarize:
1. Current V3 pattern usage
2. Sacred Architecture constraints
3. Widget integration patterns
4. CSS property conventions

Do not write code yet - analysis only."
```

### b. Planning and Review (V3 Pattern Validation)

**Required planning with Sacred Architecture alternatives:**

```markdown
Step 2: Sacred Architecture Implementation Planning
"Outline your implementation plan with Sacred Architecture focus:

1. V3 Pattern Compliance:
   - How will the solution follow VerticalScroll + simple widget patterns?
   - What render() method approach will be used?

2. CSS Property Strategy:
   - Which valid Textual CSS properties will be used?
   - How will styling integrate with existing Sacred Architecture themes?

3. Sacred Architecture Integration:
   - Will this integrate with Sacred Timeline or Live Workspace?
   - How will 2-way ↔ 3-way split behavior be preserved?

4. Alternative Approaches:
   - Present at least 2 V3-compliant approaches
   - Explain pros/cons for Sacred Architecture

5. Testing Strategy:
   - How will Sacred Architecture compliance be tested?
   - What UX tests will validate the integration?

Do not implement yet - planning and validation only."
```

### c. Implementation and Self-Review (Sacred Architecture Validation)

**Post-implementation Sacred Architecture review:**

```markdown
Step 3: Sacred Architecture Self-Review
"Review your implementation for Sacred Architecture compliance:

1. V3 Pattern Compliance Check:
   - ✅/❌ Uses simple widgets with render() methods
   - ✅/❌ No nested containers in VerticalScroll
   - ✅/❌ Follows proven chat_container patterns

2. CSS Property Validation:
   - ✅/❌ All CSS properties valid for Textual
   - ✅/❌ No border-color/border-style issues
   - ✅/❌ Follows Sacred Architecture styling

3. Sacred Architecture Integration:
   - ✅/❌ Properly integrates with UnifiedTimeline
   - ✅/❌ Maintains workspace transition behavior
   - ✅/❌ Preserves Sacred Timeline integrity

4. Testing Coverage:
   - ✅/❌ Sacred Architecture compliance tests added
   - ✅/❌ UX tests for integration behavior
   - ✅/❌ Regression prevention measures

Summarize any risks or Sacred Architecture concerns."
```

## 5. Automated Consistency Checks and Regression Prevention

### a. Automated Sacred Architecture Checks

**Required checks after every Sacred Architecture change:**

```python
def run_sacred_architecture_checks():
    """Automated Sacred Architecture compliance validation"""
    
    checks = {
        'lint_compliance': run_lint_tools(),
        'test_suite': run_full_test_suite(),
        'css_validation': validate_all_css_properties(),
        'layout_conflicts': check_for_nested_containers(),
        'v3_pattern_compliance': validate_v3_patterns(),
        'workspace_behavior': test_workspace_transitions(),
        'timeline_integrity': validate_unified_timeline()
    }
    
    # Fail if any Sacred Architecture violations
    violations = [k for k, v in checks.items() if not v]
    if violations:
        raise SacredArchitectureViolation(f"Violations: {violations}")
    
    return checks
```

### b. Sacred Architecture Regression Safeguards

**Specific regression prevention for Sacred Architecture:**

1. **Layout Regression Tests:**
   ```python
   @pytest.mark.asyncio
   async def test_layout_regression_prevention():
       """Prevent Sacred Architecture layout regressions"""
       app = LLMReplApp()
       async with app.run_test() as pilot:
           # Test no nested containers
           sacred_timeline = app.query_one("#sacred-timeline")
           for child in sacred_timeline.children:
               assert not isinstance(child, (Vertical, VerticalScroll))
   ```

2. **Workspace Transition Regression Tests:**
   ```python
   @pytest.mark.asyncio
   async def test_workspace_transition_regression():
       """Prevent workspace transition regressions"""
       app = LLMReplApp()
       async with app.run_test() as pilot:
           live_workspace = app.query_one("#live-workspace")
           
           # Test 2-way → 3-way → 2-way transitions
           assert not live_workspace.is_visible  # 2-way
           live_workspace.show_workspace()
           assert live_workspace.is_visible     # 3-way
           live_workspace.hide_workspace()
           assert not live_workspace.is_visible # 2-way
   ```

## 6. Documentation and Collaboration

### a. Sacred Architecture Documentation Standards

**Required documentation updates for Sacred Architecture changes:**

1. **CLAUDE.md Updates:**
   ```markdown
   When modifying Sacred Architecture:
   - Update Sacred GUI Architecture section if layout changes
   - Document new V3 pattern usage
   - Add any new testing requirements
   - Update AI agent guidelines if workflow changes
   ```

2. **Code Documentation:**
   ```python
   class NewSacredWidget(Widget):
       """New Sacred Architecture widget following V3 patterns.
       
       This widget maintains Sacred Architecture integrity by:
       - Using simple render() method (V3 Chatbox pattern)
       - Avoiding nested containers to prevent layout conflicts
       - Integrating with UnifiedTimeline single source of truth
       - Supporting 2-way ↔ 3-way split workspace behavior
       
       Args:
           data: Validated input data (fails fast on invalid input)
       
       Raises:
           ValueError: If data violates Sacred Architecture constraints
       """
   ```

### b. Human Collaboration (Sacred Architecture Review)

**Required human review for Sacred Architecture changes:**

```markdown
## Sacred Architecture Change Review Request

### Change Summary
[Description of Sacred Architecture modifications]

### V3 Pattern Compliance
- ✅/❌ Follows VerticalScroll + simple widget pattern
- ✅/❌ Uses render() method approach
- ✅/❌ No nested container violations

### Sacred Architecture Impact
- **Sacred Timeline:** [impact assessment]
- **Live Workspace:** [impact assessment]  
- **Workspace Transitions:** [2-way ↔ 3-way split impact]
- **CSS Properties:** [valid Textual CSS only]

### Testing Strategy
- [UX tests for Sacred Architecture compliance]
- [Regression prevention measures]
- [Performance impact assessment]

### Human Review Required For:
- [ ] Sacred Architecture pattern validation
- [ ] V3 compliance verification
- [ ] CSS property approval
- [ ] Testing strategy review
- [ ] Documentation accuracy

### Questions for Human Reviewer:
1. Does this change maintain Sacred Architecture integrity?
2. Are there V3 pattern considerations missed?
3. Should additional Sacred Architecture tests be added?
4. Any concerns about workspace transition behavior?
```

## 7. Sacred Architecture Agent Behavior Table

| Task/Scenario                           | Expected Sacred Architecture Agent Behavior                                              |
|----------------------------------------|------------------------------------------------------------------------------------------|
| **Architectural Review**               | Read Sacred Architecture files; flag V3 violations; suggest refactorings with rationale |
| **Widget Implementation**              | Scaffold V3-compliant widgets; implement render() patterns; validate CSS properties     |
| **Complex Sacred Architecture Task**   | Delegate V3 pattern research; aggregate findings; resolve Sacred Architecture conflicts  |
| **CSS Changes**                        | Validate Textual properties; maintain Sacred Architecture styling; prevent border-color issues |
| **Timeline Integration**               | Maintain UnifiedTimeline integrity; preserve workspace transitions; validate event flow  |
| **Testing Implementation**             | Add UX tests with Pilot; test Sacred Architecture compliance; prevent layout regressions |
| **Regression Prevention**              | Run Sacred Architecture checks; flag workspace behavior risks; validate V3 patterns     |
| **Documentation**                      | Update CLAUDE.md Sacred Architecture section; document V3 pattern rationale             |

## Sacred Architecture Workflow Summary

**For every Sacred Architecture change:**

1. **Read Sacred Architecture context** (CLAUDE.md, existing widgets, testing guide)
2. **Analyze V3 pattern compliance** and flag any violations
3. **Plan with Sacred Architecture alternatives** and V3-compliant approaches
4. **Implement incrementally** with render() patterns and valid CSS
5. **Test Sacred Architecture compliance** with UX tests and regression prevention
6. **Document Sacred Architecture impact** and rationale for V3 pattern decisions
7. **Request human review** for Sacred Architecture validation

By following these specific, actionable guidelines tailored to our Sacred GUI Architecture, AI coding agents can consistently deliver code that maintains V3 patterns, prevents layout conflicts, and preserves the proven Sacred Timeline and Live Workspace design—while minimizing regressions and architectural drift.

---

**References:** These workflows integrate with `.ai/ai-agent-development-guidelines.md` for comprehensive AI agent guidance and `.ai/textual-testing-guide.md` for Sacred Architecture testing requirements. Always consult CLAUDE.md for current Sacred Architecture constraints and V3 pattern specifications.