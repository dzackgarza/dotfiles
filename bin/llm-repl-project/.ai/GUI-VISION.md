# SACRED GUI ARCHITECTURE: VISUAL SPECIFICATION

**STATUS**: CANONICAL REFERENCE - ALL GUI DEVELOPMENT MUST FOLLOW THIS DESIGN

This document provides the complete visual specification for the Sacred GUI Architecture, including detailed ASCII diagrams, interaction flows, and implementation patterns.

## EXECUTIVE SUMMARY

The Sacred GUI Architecture implements a three-area layout optimized for AI-assisted conversations with transparent cognition processing. It combines proven V3 patterns with industry-standard Textual chat application practices to deliver a robust, scalable interface.

```
╭─────────────────────────────────────────────────────╮
│               SACRED GUI OVERVIEW                   │
├─────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐   │
│  │        SACRED TIMELINE (History)            │   │
│  │  ┌───┐ ┌─────────┐ ┌─────────────────────┐  │   │
│  │  │ S │ │ User: Q │ │ Cognition Pipeline  │  │   │ 
│  │  │ Y │ │ 1       │ │ Sub1→Sub2→Sub3→Asst │  │   │
│  │  │ S │ └─────────┘ └─────────────────────┘  │   │
│  │  │ T │ ┌─────────┐ ┌─────────────────────┐  │   │
│  │  │ E │ │ User: Q │ │ Cognition Pipeline  │  │   │
│  │  │ M │ │ 2       │ │ Sub1→Sub2→Sub3→Asst │  │   │
│  │  └───┘ └─────────┘ └─────────────────────┘  │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │      LIVE WORKSPACE (Active Cognition)     │   │ 
│  │  ┌─────────┐ ┌─────────┐ ┌─────────────┐   │   │
│  │  │Route    │ │Call     │ │Format       │   │   │
│  │  │Query ███│ │Tool     │ │Output       │   │   │
│  │  │(active) │ │(pending)│ │(pending)    │   │   │
│  │  └─────────┘ └─────────┘ └─────────────┘   │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │           PROMPT INPUT                      │   │
│  │  > Tell me about quantum computing...      │   │
│  └─────────────────────────────────────────────┘   │
╰─────────────────────────────────────────────────────╯
```

## SACRED ARCHITECTURE STATES

### STATE 1: IDLE (2-Way Split)

When no active processing is occurring, the interface shows only Sacred Timeline and Prompt Input:

```
┌─────────────────────────────────────────────────────────────┐
│                    SACRED TIMELINE                         │
│  ┌─ Turn 1 ────────────────────────────────────────────┐   │
│  │ 👤 User: "Explain machine learning basics"          │   │
│  │ ╭─ 🧠 Cognition Pipeline ─────────────────────────╮ │   │
│  │ │ Route→Research→Synthesize→Present              │ │   │
│  │ ╰─────────────────────────────────────────────────╯ │   │
│  │ 🤖 Assistant: "Machine learning is a subset..."    │   │
│  └─────────────────────────────────────────────────────┘   │
│  ═══════════════════════════════════════════════════════   │ <- hrule separator
│  ┌─ Turn 2 ────────────────────────────────────────────┐   │
│  │ 👤 User: "Give me a practical example"              │   │
│  │ ╭─ 🧠 Cognition Pipeline ─────────────────────────╮ │   │
│  │ │ Route→Example→Code→Explain                     │ │   │
│  │ ╰─────────────────────────────────────────────────╯ │   │
│  │ 🤖 Assistant: "Here's a simple classification..."  │   │
│  └─────────────────────────────────────────────────────┘   │
│  ═══════════════════════════════════════════════════════   │
│                    [scroll for more...]                    │
├─────────────────────────────────────────────────────────────┤
│                     PROMPT INPUT                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ > How does neural network training work?_          │   │
│  │   [Shift+Enter for newline, Enter to submit]       │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### STATE 2: ACTIVE PROCESSING (3-Way Split)

When user submits input, Live Workspace appears showing real-time cognition:

```
┌─────────────────────────────────────────────────────────────┐
│                    SACRED TIMELINE                         │
│  [Previous conversation history continues...]               │
│  ═══════════════════════════════════════════════════════   │
│  ┌─ Turn 3 (Current) ──────────────────────────────────┐   │
│  │ 👤 User: "How does neural network training work?"   │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                    LIVE WORKSPACE                          │
│  ╭─ 🧠 Cognition Pipeline: Neural Network Training ─────╮  │
│  │                                                     │  │
│  │ ✅ 1. Route Query        [tinyllama] ⏱ 0.3s 🎯 ML   │  │
│  │    "Educational query about neural networks"        │  │
│  │                                                     │  │
│  │ ⚡ 2. Research Domain    [phi-3.5] ⏱ 1.2s... 📚     │  │ <- active
│  │    ████████░░░░ "Gathering key concepts..."         │  │
│  │                                                     │  │
│  │ ⏳ 3. Code Examples      [deepseek] ⏱ pending 💻    │  │
│  │                                                     │  │
│  │ ⏳ 4. Synthesize         [claude] ⏱ pending ✨      │  │
│  │                                                     │  │
│  │ ⏳ 5. Final Response     [STREAM] ⏱ pending 🤖      │  │
│  ╰─────────────────────────────────────────────────────╯  │
├─────────────────────────────────────────────────────────────┤
│                     PROMPT INPUT                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ > [Processing... Next input queued]                │   │ <- disabled during processing
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### STATE 3: STREAMING RESPONSE

Final sub-module streams assistant response in real-time:

```
┌─────────────────────────────────────────────────────────────┐
│                    SACRED TIMELINE                         │
│  [Previous conversation history...]                         │
│  ┌─ Turn 3 (Current) ──────────────────────────────────┐   │
│  │ 👤 User: "How does neural network training work?"   │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                    LIVE WORKSPACE                          │
│  ╭─ 🧠 Cognition Pipeline: Neural Network Training ─────╮  │
│  │ ✅ 1. Route Query    [tinyllama] ⏱ 0.3s 🎯 Complete │  │
│  │ ✅ 2. Research       [phi-3.5]   ⏱ 1.2s 📚 Complete │  │
│  │ ✅ 3. Code Examples  [deepseek]  ⏱ 2.1s 💻 Complete │  │
│  │ ✅ 4. Synthesize     [claude]    ⏱ 0.8s ✨ Complete │  │
│  ╰─────────────────────────────────────────────────────╯  │
│  ╭─ 🤖 Assistant Response [STREAMING] ─ 📊 1.2k tokens ╮  │
│  │                                                     │  │
│  │ Neural network training is a iterative process     │  │
│  │ that adjusts weights and biases to minimize loss.  │  │ <- streaming text
│  │ Here's how it works:                               │  │
│  │                                                     │  │
│  │ ## 1. Forward Propagation                          │  │
│  │ Data flows through layers: input → hidden → out█   │  │ <- cursor shows live typing
│  ╰─────────────────────────────────────────────────────╯  │
├─────────────────────────────────────────────────────────────┤
│                     PROMPT INPUT                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ > [Response streaming... Please wait]              │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### STATE 4: TURN COMPLETION

When response completes, Live Workspace content transfers to Sacred Timeline:

```
┌─────────────────────────────────────────────────────────────┐
│                    SACRED TIMELINE                         │
│  [Previous conversation history...]                         │
│  ═══════════════════════════════════════════════════════   │
│  ┌─ Turn 3 ────────────────────────────────────────────┐   │
│  │ 👤 User: "How does neural network training work?"   │   │
│  │ ╭─ 🧠 Cognition Pipeline ─────────────────────────╮ │   │
│  │ │ Route→Research→Code→Synthesize (4.4s, 1.2k)    │ │   │ <- summarized
│  │ ╰─────────────────────────────────────────────────╯ │   │
│  │ 🤖 Assistant: "Neural network training is an      │   │
│  │     iterative process that adjusts weights and    │   │
│  │     biases to minimize loss. Here's how it works: │   │
│  │     ## 1. Forward Propagation                     │   │
│  │     Data flows through layers..."                 │   │
│  │     [Complete response preserved in timeline]     │   │
│  └─────────────────────────────────────────────────────┘   │
│  ═══════════════════════════════════════════════════════   │ <- new turn separator
├─────────────────────────────────────────────────────────────┤
│                     PROMPT INPUT                           │ <- Live Workspace hidden
│  ┌─────────────────────────────────────────────────────┐   │
│  │ > What about backpropagation?_                     │   │ <- ready for next input
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## DETAILED WIDGET ARCHITECTURE

### Sacred Timeline Widget (VerticalScroll Pattern)

```
╭─ SacredTimelineWidget extends Widget ──────────────────╮
│                                                        │
│  ┌─ VerticalScroll Container ─────────────────────┐    │
│  │                                                │    │
│  │  ┌─ SimpleBlockWidget (User) ────────────┐     │    │
│  │  │ role: "user"                         │     │    │
│  │  │ content: "How does ML work?"         │     │    │
│  │  │ timestamp: 2025-07-12T14:30:00Z     │     │    │
│  │  │ render() → Panel with user styling  │     │    │
│  │  └─────────────────────────────────────┘     │    │
│  │                                                │    │
│  │  ┌─ HRuleWidget (Turn Separator) ───────┐     │    │
│  │  │ render() → Rule with muted color     │     │    │
│  │  └─────────────────────────────────────┘     │    │
│  │                                                │    │
│  │  ┌─ SimpleBlockWidget (Cognition) ──────┐     │    │
│  │  │ role: "cognition"                    │     │    │
│  │  │ content: "Route→Research→Synthesize" │     │    │
│  │  │ metadata: {duration: 3.2, tokens: 847} │  │    │
│  │  │ render() → Panel with pipeline view  │     │    │
│  │  └─────────────────────────────────────┘     │    │
│  │                                                │    │
│  │  ┌─ SimpleBlockWidget (Assistant) ──────┐     │    │
│  │  │ role: "assistant"                    │     │    │ 
│  │  │ content: "Machine learning is..."    │     │    │
│  │  │ render() → Panel with assistant style│     │    │
│  │  └─────────────────────────────────────┘     │    │
│  │                                                │    │
│  │  [... more blocks ...]                        │    │
│  │  [ScrollView handles overflow automatically] │    │
│  └────────────────────────────────────────────┘    │
│                                                        │
│  Methods:                                              │
│  • add_block(block) → mount new SimpleBlockWidget     │
│  • add_turn_separator() → mount HRuleWidget           │ 
│  • scroll_to_bottom() → auto-scroll when appropriate  │
╰────────────────────────────────────────────────────────╯
```

### Live Workspace Widget (VerticalScroll Pattern)

```
╭─ LiveWorkspaceWidget extends Widget ───────────────────╮
│                                                        │
│  ┌─ VerticalScroll Container ─────────────────────┐    │
│  │                                                │    │
│  │  ┌─ SubModuleWidget (Route) ─────────────┐     │    │
│  │  │ module_type: "route_query"           │     │    │
│  │  │ status: "completed" ✅               │     │    │
│  │  │ model: "tinyllama"                   │     │    │
│  │  │ duration: 0.3s                      │     │    │
│  │  │ render() → Panel with status icon   │     │    │
│  │  └─────────────────────────────────────┘     │    │
│  │                                                │    │
│  │  ┌─ SubModuleWidget (Research) ──────────┐     │    │
│  │  │ module_type: "research_domain"       │     │    │
│  │  │ status: "streaming" ⚡               │     │    │
│  │  │ model: "phi-3.5"                     │     │    │
│  │  │ progress_bar: ████████░░░░          │     │    │
│  │  │ stream_content: "Gathering key..."   │     │    │
│  │  │ render() → Panel with progress       │     │    │
│  │  └─────────────────────────────────────┘     │    │
│  │                                                │    │
│  │  ┌─ SubModuleWidget (Pending) ────────────┐   │    │
│  │  │ module_type: "code_examples"         │   │    │
│  │  │ status: "pending" ⏳                 │   │    │
│  │  │ render() → Dimmed panel placeholder  │   │    │
│  │  └─────────────────────────────────────┘   │    │
│  │                                                │    │
│  │  ┌─ StreamingResponseWidget ──────────────┐   │    │
│  │  │ role: "assistant"                    │   │    │
│  │  │ status: "streaming" 🤖               │   │    │
│  │  │ content: "Neural network training..." │   │    │
│  │  │ cursor_position: visible █           │   │    │
│  │  │ render() → Panel with streaming text │   │    │
│  │  └─────────────────────────────────────┘   │    │
│  └────────────────────────────────────────────┘    │
│                                                        │
│  State Management:                                     │
│  • show_workspace() → display: visible               │
│  • hide_workspace() → display: none (2-way split)     │
│  • add_submodule(module) → mount SubModuleWidget      │
│  • update_streaming(content) → call_from_thread()     │
│  • clear_workspace() → remove all children            │
╰────────────────────────────────────────────────────────╯
```

## DATA FLOW ARCHITECTURE

### User Input Processing Flow

```
┌─ User Types & Submits ─────────────────────────────────────┐
│                                                            │
│  PromptInput.on_submit(text) ──────────────────────────┐   │
│                                                        │   │
│  ┌─ 1. Validation ───────────────────────────────────┐ │   │
│  │ • Assert text is non-empty string                 │ │   │
│  │ • Validate input length limits                    │ │   │
│  │ • Check for dangerous content patterns            │ │   │
│  │ • Raise ValidationError on failure                │ │   │
│  └───────────────────────────────────────────────────┘ │   │
│                          │                              │   │
│  ┌─ 2. Timeline Addition ────────────────────────────┐ │   │
│  │ user_block = timeline.add_live_block(             │ │   │
│  │     role="user",                                  │ │   │
│  │     content=text,                                 │ │   │
│  │     timestamp=now()                               │ │   │
│  │ )                                                 │ │   │
│  │ await sacred_timeline.add_block(user_block)       │ │   │
│  └───────────────────────────────────────────────────┘ │   │
│                          │                              │   │
│  ┌─ 3. Workspace Activation ─────────────────────────┐ │   │
│  │ live_workspace.show_workspace()                   │ │   │
│  │ # Triggers 2-way → 3-way split transition         │ │   │
│  └───────────────────────────────────────────────────┘ │   │
│                          │                              │   │
│  ┌─ 4. Async Processing Start ───────────────────────┐ │   │
│  │ await unified_processor.process_user_input_async( │ │   │
│  │     text,                                         │ │   │
│  │     callback=live_workspace.update_submodule      │ │   │
│  │ )                                                 │ │   │
│  └───────────────────────────────────────────────────┘ │   │
└────────────────────────────────────────────────────────────┘
```

### Cognition Pipeline Processing Flow

```
┌─ UnifiedAsyncProcessor.process_user_input_async() ────────┐
│                                                            │
│  ┌─ Pipeline Definition ─────────────────────────────────┐ │
│  │ submodules = [                                        │ │
│  │     RouteQueryModule(model="tinyllama"),              │ │
│  │     ResearchModule(model="phi-3.5"),                  │ │
│  │     CodeExampleModule(model="deepseek"),              │ │
│  │     SynthesizeModule(model="claude"),                 │ │
│  │     AssistantResponseModule(stream=True)              │ │
│  │ ]                                                     │ │
│  └───────────────────────────────────────────────────────┘ │
│                          │                                 │
│  ┌─ Sequential Execution ────────────────────────────────┐ │
│  │ for module in submodules:                             │ │
│  │     # Create UI widget for this module                │ │
│  │     widget = SubModuleWidget(module)                  │ │
│  │     app.call_from_thread(                             │ │
│  │         live_workspace.add_submodule, widget          │ │
│  │     )                                                 │ │
│  │                                                       │ │
│  │     # Execute module in background thread             │ │
│  │     async def run_module():                           │ │
│  │         widget.set_status("active")                   │ │
│  │         result = await module.execute(context)       │ │
│  │         widget.set_status("completed")                │ │
│  │         return result                                 │ │
│  │                                                       │ │
│  │     result = await run_module()                       │ │
│  │     context.update(result)                           │ │
│  └───────────────────────────────────────────────────────┘ │
│                          │                                 │
│  ┌─ Turn Completion ─────────────────────────────────────┐ │
│  │ # Transfer Live Workspace → Sacred Timeline           │ │
│  │ cognition_block = create_cognition_summary(pipeline)  │ │
│  │ assistant_block = get_final_response()                │ │
│  │                                                       │ │
│  │ await sacred_timeline.add_block(cognition_block)      │ │
│  │ await sacred_timeline.add_block(assistant_block)      │ │
│  │ await sacred_timeline.add_turn_separator()            │ │
│  │                                                       │ │
│  │ live_workspace.clear_workspace()                      │ │
│  │ live_workspace.hide_workspace()  # 3-way → 2-way     │ │
│  └───────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

## ERROR HANDLING & VALIDATION PATTERNS

### Error Boundary Implementation

```
┌─ ErrorBoundaryWidget Pattern ─────────────────────────────┐
│                                                            │
│  ┌─ Widget Wrapper ──────────────────────────────────────┐ │
│  │ class ErrorBoundaryWidget(Widget):                    │ │
│  │     def __init__(self, child_widget):                 │ │
│  │         super().__init__()                            │ │
│  │         self.child = child_widget                     │ │
│  │         self.error_state = None                       │ │
│  │                                                       │ │
│  │     def compose(self):                                │ │
│  │         try:                                          │ │
│  │             yield self.child                          │ │
│  │         except Exception as e:                        │ │
│  │             self.error_state = e                      │ │
│  │             yield ErrorDisplayWidget(e)               │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌─ Error Display ───────────────────────────────────────┐ │
│  │ ╭─ ❌ WIDGET ERROR ─────────────────────────────────╮ │ │
│  │ │                                                   │ │ │
│  │ │ SimpleBlockWidget failed to render                │ │ │
│  │ │                                                   │ │ │
│  │ │ Error: Invalid block data: missing 'role' field   │ │ │
│  │ │ Location: sacred_timeline.py:145                  │ │ │
│  │ │ Timestamp: 2025-07-12T14:30:15Z                   │ │ │
│  │ │                                                   │ │ │
│  │ │ [View Stack Trace] [Retry] [Report Bug]          │ │ │
│  │ ╰───────────────────────────────────────────────────╯ │ │
│  └───────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

### Input Validation Flow

```
┌─ Fail-Fast Validation Pipeline ───────────────────────────┐
│                                                            │
│  User Input: "Tell me about quantum computing"            │
│                          │                                 │
│  ┌─ 1. Type Validation ─────────────────────────────────┐ │
│  │ if not isinstance(input_text, str):                  │ │
│  │     raise TypeError(f"Expected str, got {type(...)}")│ │
│  │ ✅ PASS: Input is string                             │ │
│  └───────────────────────────────────────────────────────┘ │
│                          │                                 │
│  ┌─ 2. Content Validation ──────────────────────────────┐ │
│  │ if not input_text.strip():                           │ │
│  │     raise ValueError("Input cannot be empty")        │ │
│  │ if len(input_text) > MAX_INPUT_LENGTH:               │ │
│  │     raise ValueError(f"Input too long: {len(...)}")  │ │
│  │ ✅ PASS: Content is valid                            │ │
│  └───────────────────────────────────────────────────────┘ │
│                          │                                 │
│  ┌─ 3. Security Validation ─────────────────────────────┐ │
│  │ dangerous_patterns = [                               │ │
│  │     r"<script.*?>",  # XSS attempts                  │ │
│  │     r"DROP TABLE",   # SQL injection                 │ │
│  │     r"rm -rf",       # Shell injection               │ │
│  │ ]                                                    │ │
│  │ for pattern in dangerous_patterns:                   │ │
│  │     if re.search(pattern, input_text, re.IGNORECASE):│ │
│  │         raise SecurityError(f"Dangerous pattern: {pattern}") │
│  │ ✅ PASS: No security threats detected               │ │
│  └───────────────────────────────────────────────────────┘ │
│                          │                                 │
│  ✅ INPUT VALIDATED → Proceed to processing               │
└────────────────────────────────────────────────────────────┘
```

## RESPONSIVE DESIGN PATTERNS

### Auto-Scroll Behavior

```
┌─ Smart Auto-Scroll Logic ─────────────────────────────────┐
│                                                            │
│  ┌─ Scroll Position Detection ──────────────────────────┐ │
│  │ class SmartScrollMixin:                               │ │
│  │     def should_auto_scroll(self) -> bool:             │ │
│  │         scroll_y = self.scroll_y                      │ │
│  │         max_scroll = self.max_scroll_y                │ │
│  │         threshold = 3  # Lines from bottom            │ │
│  │                                                       │ │
│  │         # Only auto-scroll if user is near bottom    │ │
│  │         return scroll_y >= max_scroll - threshold     │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌─ Content Update Handling ────────────────────────────┐ │
│  │ def on_content_added(self, new_widget):              │ │
│  │     # Add content to scroll container                │ │
│  │     await self.mount(new_widget)                     │ │
│  │                                                       │ │
│  │     # Auto-scroll only if appropriate                │ │
│  │     if self.should_auto_scroll():                    │ │
│  │         self.scroll_end(animate=False, force=True)   │ │
│  │     else:                                             │ │
│  │         # Show "new content" indicator               │ │
│  │         self.show_new_content_indicator()            │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌─ User Experience ─────────────────────────────────────┐ │
│  │                                                       │ │
│  │ User scrolled up to read history:                    │ │
│  │ ┌─────────────────────────────────┐                 │ │
│  │ │ Turn 1: [old conversation...]   │ ← User here      │ │
│  │ │ Turn 2: [more history...]       │                 │ │
│  │ │ Turn 3: [latest content...]     │                 │ │
│  │ │ [💬 New response available ↓]   │ ← Indicator      │ │
│  │ └─────────────────────────────────┘                 │ │
│  │                                                       │ │
│  │ User at bottom - auto-scroll:                        │ │
│  │ ┌─────────────────────────────────┐                 │ │
│  │ │ Turn 2: [previous content...]   │                 │ │
│  │ │ Turn 3: [current response...]   │                 │ │
│  │ │ Assistant: "The answer is...█"  │ ← Auto-scroll   │ │
│  │ └─────────────────────────────────┘                 │ │
│  └───────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

### Dynamic Content Resizing

```
┌─ Content-Driven Height Management ────────────────────────┐
│                                                            │
│  ┌─ CSS Height Strategy ────────────────────────────────┐ │
│  │ /* All widgets use content-driven height */           │ │
│  │ .simple-block {                                       │ │
│  │     height: auto;          /* No fixed heights */    │ │
│  │     min-height: 3;         /* Minimum readability */ │ │
│  │     max-height: 80vh;      /* Prevent screen takeover*/ │
│  │     overflow-y: auto;      /* Scroll if needed */    │ │
│  │ }                                                     │ │
│  │                                                       │ │
│  │ .live-workspace {                                     │ │
│  │     height: auto;          /* Dynamic sizing */      │ │
│  │     max-height: 50vh;      /* Don't dominate screen */ │ │
│  │ }                                                     │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌─ Content Size Adaptation ────────────────────────────┐ │
│  │ class SimpleBlockWidget(Widget):                      │ │
│  │     def render(self) -> RenderableType:               │ │
│  │         # Content determines size                     │ │
│  │         content_lines = self.content.split('\n')     │ │
│  │         height = min(len(content_lines) + 2, 20)     │ │
│  │                                                       │ │
│  │         return Panel(                                 │ │
│  │             self.content,                             │ │
│  │             height=height,   # Calculated height     │ │
│  │             title=self.role,                          │ │
│  │             border_style=self.get_border_style()     │ │
│  │         )                                             │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌─ Layout Recalculation ───────────────────────────────┐ │
│  │ # When content changes, trigger layout update        │ │
│  │ def update_content(self, new_content: str):           │ │
│  │     self.content = new_content                        │ │
│  │     self.refresh()  # Triggers render() + layout     │ │
│  │     self.parent.refresh()  # Parent adjusts to fit   │ │
│  └───────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

## IMPLEMENTATION CHECKLIST

### Core Widget Requirements

```
┌─ Sacred Timeline Widget ✅ Requirements ─────────────────┐
│ ☐ Extends Widget (not VerticalScroll directly)           │
│ ☐ Contains VerticalScroll as single child                │
│ ☐ Uses SimpleBlockWidget for all content                 │
│ ☐ Implements add_block() method                          │
│ ☐ Implements add_turn_separator() method                 │
│ ☐ Smart auto-scroll behavior                             │
│ ☐ Error boundary wrapper                                 │
│ ☐ Content validation on all inputs                       │
└───────────────────────────────────────────────────────────┘

┌─ Live Workspace Widget ✅ Requirements ──────────────────┐
│ ☐ Identical VerticalScroll pattern to Sacred Timeline   │
│ ☐ Uses SubModuleWidget for pipeline steps               │
│ ☐ Implements show_workspace()/hide_workspace()          │
│ ☐ Thread-safe update methods with call_from_thread()    │
│ ☐ Streaming content support                             │
│ ☐ Clear workspace functionality                         │
│ ☐ Progress indicators and status icons                  │
└───────────────────────────────────────────────────────────┘

┌─ Simple Block Widget ✅ Requirements ────────────────────┐
│ ☐ Uses render() method (no child widgets)               │
│ ☐ Validates block data in __init__                      │
│ ☐ Role-based styling (user/assistant/system/cognition)  │
│ ☐ Content-driven height calculation                     │
│ ☐ Timestamp and metadata display                        │
│ ☐ Copy-to-clipboard functionality                       │
└───────────────────────────────────────────────────────────┘
```

### Testing Requirements

```
┌─ Widget Test Harnesses ✅ Requirements ──────────────────┐
│ ☐ Streaming simulation tests                            │
│ ☐ Dynamic resizing validation                           │
│ ☐ Error injection scenarios                             │
│ ☐ Layout conflict detection                             │
│ ☐ Performance under high content volume                 │
│ ☐ Auto-scroll behavior validation                       │
│ ☐ Show/hide workspace transitions                       │
└───────────────────────────────────────────────────────────┘

┌─ Integration Test Scenarios ✅ Requirements ─────────────┐
│ ☐ Complete user input → response cycle                  │
│ ☐ Multiple concurrent turns                             │
│ ☐ Error recovery and graceful degradation               │
│ ☐ Memory usage with large conversation history          │
│ ☐ CSS validation across all widgets                     │
│ ☐ Thread safety under load                              │
└───────────────────────────────────────────────────────────┘
```

## CONCLUSION

This Sacred GUI Architecture specification provides a complete visual and technical blueprint for implementing a robust, scalable chat interface. The design combines proven V3 patterns with industry-standard best practices to deliver:

- **Visual Clarity**: Three distinct areas with clear purposes
- **Scalable Architecture**: Handles unlimited conversation history and complex cognition pipelines  
- **Error Resilience**: Comprehensive validation and error boundaries
- **Performance**: Smart scrolling, content-driven sizing, thread-safe updates
- **Maintainability**: Modular widgets following consistent patterns

All implementation must strictly follow these specifications to ensure architectural consistency and reliability.

---

**Status**: This document is the canonical reference for all Sacred GUI development. Any deviations must be approved and documented.