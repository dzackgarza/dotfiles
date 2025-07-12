# Wrinkl Framework - Ledger System Usage

> **Human-in-the-Loop Development**: All visual and UX changes require human verification. Agents cannot self-approve their work.

## Ledger System Overview

The Wrinkl framework implements strict, transparent development with human oversight for all user-facing changes.

### Core Principles

- **Backend Logic ≠ User Experience**: Passing tests does not mean a feature is complete
- **Observable Means User-Visible**: Users must see and interact with changes in the running application
- **No Agent Self-Approval**: Agents cannot approve their own work
- **Context-Driven Development**: All work is grounded in `.ai/docs/` and feature ledgers
- **Transparent Progress**: All decisions and tests are logged in real-time

## Ledger Workflow (Required Process)

### Step 1: Starting a Ledger

```bash
# Check current status and suggested next work
just ledger-status

# Read the ENTIRE ledger file before starting
# Example: .ai/ledgers/v3.1/mock-cognition-pipeline.md
```

**Agent Requirements**:
1. **Read Complete Ledger**: Must read entire ledger file, not just summary
2. **Identify User Behaviors**: Find 3-5 specific, user-visible behaviors
3. **Ask for Clarification**: If behaviors unclear, ask before proceeding
4. **Start Tracking**: Run `just start-ledger <ledger-name>`

### Step 2: Implementation & Static Testing

**Build from Working Code**:
- Study V3, Claude Code, or Gemini CLI patterns first
- Copy proven implementations, adapt for Sacred GUI
- Follow Sacred Architecture constraints

**Implementation Requirements**:
- Implement using V3's proven patterns
- Write comprehensive tests for backend logic
- Test statically using `just test` or `just test-ledger <ledger-name>`
- **CRITICAL**: Never run GUI applications (breaks Claude Code interface)

### Step 3: Requesting Human Review

**When Backend Complete**:
1. **Do NOT mark ledger as complete** (agents cannot self-approve)
2. **Request review**: `just ledger-request-review <ledger-name>`
3. **Notify user clearly**: List specific behaviors to test
4. **Provide run command**: Exact command to run application (e.g., `just run-fast`)

**Review Request Format**:
```
Feature ready for visual confirmation:

User-Visible Behaviors to Test:
1. User sees streaming text appear character by character in cognition blocks
2. User sees token counts increment in real-time during AI processing  
3. User sees workspace transition smoothly from 2-way to 3-way split
4. User sees completed blocks move from workspace to Sacred Timeline
5. User sees error messages display gracefully without app crashes

Run Command: just run-fast

Test Scenario: Type "Tell me about quantum computing" and verify behaviors above.
```

### Step 4: Human Verification

**Human Responsibilities**:
1. Run application to test promised behaviors
2. Verify visual and interaction aspects work as described
3. Approve or reject using commands:
   - `just ledger-approve-review <ledger-name>`
   - `just ledger-reject-review <ledger-name> "feedback on what is broken"`

### Step 5: Completion

**Only humans can complete ledgers**:
- Completion happens through review approval
- `just complete-ledger` is deprecated for agents (protected by `sudo`)
- Agents must not attempt to use completion commands

## User-Visible Behavior Standards

### ✅ Good Behavior Descriptions

```
✅ "User sees streaming text appear character by character in cognition blocks"
✅ "User sees token counts increment in real-time during AI processing"
✅ "User sees workspace transition smoothly from 2-way to 3-way split"
✅ "User sees error messages display gracefully without app crashes"
✅ "User can scroll through unlimited conversation history"
```

### ❌ Bad Behavior Descriptions

```
❌ "Cognition pipeline works" (not user-visible)
❌ "Timeline displays properly" (too vague)
❌ "Code compiles successfully" (not user behavior)
❌ "Tests pass" (backend only)
❌ "Architecture is correct" (not observable)
```

## Ledger Structure

### Current Active Ledgers

```
.ai/ledgers/v3.1/
├── README.md                       # Current status and priorities
├── core-ui-ux.md                  # Three-area layout implementation
├── mock-cognition-pipeline.md     # Streaming cognition simulation
├── live-inscribed-block-system.md # Block state management
├── enhanced-config-system.md      # Configuration improvements
└── improved-test-infrastructure.md # Testing enhancements
```

### Ledger Priority System

**High Priority** (Work on These First):
- Features that enable Sacred Architecture core functionality
- User-visible behaviors that demonstrate three-area layout
- Streaming cognition pipeline implementation

**Medium Priority** (Work After High Priority):
- Configuration and setup improvements
- Testing infrastructure enhancements
- Performance optimizations

**Low Priority** (Work When Others Complete):
- Documentation updates
- Code quality improvements
- Nice-to-have features

## Sacred Architecture Integration

### Ledger Requirements for Sacred GUI

**All ledgers must specify**:
1. **Sacred Architecture Compliance**: How feature fits three-area layout
2. **V3 Pattern Usage**: Which V3 patterns are being adapted
3. **State Transition Behavior**: How 2-way ↔ 3-way split is affected
4. **Error Boundary Handling**: How errors are gracefully managed
5. **Performance Impact**: Effect on scrolling and streaming performance

### Validation Requirements

**Before requesting review**:
```
☐ Uses V3's proven patterns (VerticalScroll + render())
☐ Maintains Sacred Architecture layout rules
☐ Includes fail-fast validation
☐ Implements error boundary support  
☐ Uses only valid Textual CSS properties
☐ Provides thread-safe streaming updates
☐ Tests pass with static validation
☐ User-visible behaviors clearly defined
☐ Run command tested and confirmed working
```

## Common Pitfalls

### Agent Mistakes to Avoid

```
❌ Marking ledgers as complete without human approval
❌ Running GUI applications during development
❌ Describing backend functionality as user behaviors
❌ Skipping reference implementation research
❌ Creating nested container layouts (breaks Sacred Architecture)
❌ Using invalid CSS properties (border-color, background-color)
❌ Self-approving work or trying to use completion commands
```

### Quality Issues to Prevent

```
❌ "Feature complete" but user can't see it working
❌ Tests pass but visual behavior is broken
❌ Code compiles but doesn't integrate with Sacred Architecture
❌ Functionality works but breaks on error conditions
❌ Implementation works but doesn't follow V3 patterns
```

## Integration with Development Workflow

### Before Starting Any Work

1. Read `CLAUDE.md` for project overview
2. Check `.ai/ledgers/v3.1/README.md` for current status
3. Read specific ledger file completely
4. Study relevant `.ai/docs/` guides
5. Research working reference implementations

### During Implementation

1. Follow V3 patterns from reference implementations
2. Maintain Sacred Architecture compliance
3. Test frequently with static validation
4. Document progress and decisions in real-time
5. Prepare clear user-visible behavior descriptions

### Before Requesting Review

1. Verify all backend tests pass
2. Confirm Sacred Architecture compliance
3. Test run command works correctly
4. Document specific behaviors for human to test
5. Ensure no GUI applications were run during development

### After Human Feedback

1. Address specific issues identified
2. Re-test with static validation
3. Update behavior descriptions if needed
4. Request re-review if significant changes made
5. Document lessons learned for future work

## Success Metrics

### Ledger Success Indicators

- **Clear User Behaviors**: Specific, testable, user-visible outcomes
- **Sacred Architecture Compliance**: Maintains three-area layout integrity
- **V3 Pattern Usage**: Builds on proven, working implementations
- **Error Resilience**: Graceful handling without application crashes
- **Performance Maintenance**: No regressions from reference implementations

### Process Success Indicators

- **Human Review Efficiency**: Clear behaviors make testing straightforward
- **First-Pass Approval Rate**: Well-prepared features approved on first review
- **Architecture Consistency**: All features maintain Sacred GUI principles
- **Reference Pattern Adoption**: Consistent use of V3 and other working patterns

---

**Remember**: The Wrinkl framework ensures quality by requiring human verification of all user-facing changes. Your job is to prepare features so thoroughly that human review can focus on validating the user experience rather than debugging technical issues.