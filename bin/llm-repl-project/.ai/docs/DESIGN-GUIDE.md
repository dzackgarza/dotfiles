# Design Guide

> **Study Working Styles First**: Always examine V3's CSS patterns and Claude Code's styling before creating new designs. Copy proven visual approaches.

## Sacred Architecture Visual Identity

### Three-Area Layout States

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

## V3-Based CSS Patterns (COPY THESE)

### Sacred Timeline Styles (V3's chat_container)

```css
/* COPIED FROM: V3/elia_chat/widgets/chat.tcss */
.sacred-timeline {
    height: 100%;           /* V3's full height pattern */
    border: solid $primary;  /* V3's border syntax */
    background: $surface;    /* V3's color variables */
    padding: 1;             /* V3's spacing */
}

/* V3's scrollable content pattern */
.sacred-timeline VerticalScroll {
    height: 100%;
    overflow-y: auto;
}
```

### Simple Block Styles (V3's Chatbox)

```css
/* COPIED FROM: V3/elia_chat/widgets/chatbox.tcss */
.simple-block {
    height: auto;          /* V3's content-driven sizing */
    min-width: 12;         /* V3's minimum width */
    max-width: 1fr;        /* V3's responsive width */
    margin: 1 0;           /* V3's vertical spacing */
    padding: 1;            /* V3's internal padding */
}

/* Role-based styling (V3's color coding) */
.simple-block-user {
    border: solid green;   /* User messages */
    background: $surface-green;
}

.simple-block-assistant {
    border: solid blue;    /* Assistant responses */
    background: $surface-blue;
}

.simple-block-cognition {
    border: solid yellow;  /* Cognition processing */
    background: $surface-yellow;
}

.simple-block-system {
    border: solid red;     /* System messages */
    background: $surface-red;
}
```

### Live Workspace Styles (V3's Dynamic Container)

```css
/* ADAPTED FROM: V3's dynamic container patterns */
.live-workspace {
    height: auto;          /* Dynamic sizing */
    max-height: 50vh;      /* Limit to half screen */
    border: solid yellow;  /* Processing indicator */
    background: $surface;
    padding: 1;
}

/* State transitions */
.live-workspace.hidden {
    display: none;         /* Clean 2-way split */
}

.live-workspace.visible {
    display: block;        /* 3-way split active */
}

/* Sub-module styling */
.sub-module {
    height: auto;
    margin: 0 0 1 0;
    padding: 1;
    border: solid gray;
    background: $surface-muted;
}

/* Sub-module states */
.sub-module.pending {
    border: solid gray;
    opacity: 0.6;
}

.sub-module.active {
    border: solid yellow;  /* Currently processing */
    opacity: 1.0;
    animation: pulse 1.5s ease-in-out infinite;
}

.sub-module.completed {
    border: solid green;   /* Finished */
    opacity: 0.8;
}

.sub-module.error {
    border: solid red;     /* Failed */
    opacity: 1.0;
}
```

### Input Area Styles (V3's Input Pattern)

```css
/* COPIED FROM: V3's input styling */
.prompt-input {
    height: auto;
    min-height: 3;         /* Readable minimum */
    max-height: 10;        /* Prevent takeover */
    border: solid $primary;
    background: $surface;
    padding: 1;
}

/* Input states */
.prompt-input.focused {
    border: solid $accent; /* Active indicator */
}

.prompt-input.disabled {
    border: solid gray;    /* Processing state */
    opacity: 0.7;
}
```

## Sacred Architecture Color System

### Role-Based Color Coding

```css
/* Sacred Architecture color variables */
:root {
    /* Primary colors */
    --sacred-blue: #0066CC;       /* Timeline borders, focus */
    --sacred-green: #00AA44;      /* User messages, success */
    --sacred-yellow: #FFAA00;     /* Cognition, processing */
    --sacred-orange: #FF6600;     /* Assistant responses */
    --sacred-red: #CC2222;        /* Errors, system messages */
    --sacred-purple: #7744CC;     /* Cognition sub-modules */
    
    /* Surface colors */
    --surface: #2A2A2A;           /* Default background */
    --surface-green: #1A2A1A;     /* User message background */
    --surface-blue: #1A1A2A;      /* Assistant background */
    --surface-yellow: #2A2A1A;    /* Cognition background */
    --surface-red: #2A1A1A;       /* Error background */
    --surface-muted: #1A1A1A;     /* Inactive elements */
    
    /* Text colors */
    --text: #CCCCCC;              /* Primary text */
    --text-muted: #888888;        /* Secondary text */
    --text-accent: #FFFFFF;       /* Highlighted text */
}
```

### Semantic Color Usage

```css
/* User interactions */
.user-content {
    color: var(--sacred-green);
    border-color: var(--sacred-green);
}

/* Assistant responses */
.assistant-content {
    color: var(--sacred-orange);
    border-color: var(--sacred-orange);
}

/* Processing states */
.processing {
    color: var(--sacred-yellow);
    border-color: var(--sacred-yellow);
}

/* Error states */
.error {
    color: var(--sacred-red);
    border-color: var(--sacred-red);
}

/* Success states */
.success {
    color: var(--sacred-green);
    border-color: var(--sacred-green);
}
```

## Animation Patterns (V3-Based)

### Smooth State Transitions

```css
/* V3's transition patterns */
.live-workspace {
    transition: opacity 0.3s ease-in-out,
                height 0.2s ease-in-out;
}

.live-workspace.hidden {
    opacity: 0;
    transition: opacity 0.2s ease-in-out,
                height 0.1s ease-in-out;
}

/* Sub-module state changes */
.sub-module {
    transition: border-color 0.2s ease-in-out,
                opacity 0.2s ease-in-out;
}
```

### Processing Indicators

```css
/* Pulsing animation for active processing */
@keyframes pulse {
    0% { 
        opacity: 0.6; 
        border-width: 1px;
    }
    50% { 
        opacity: 1.0; 
        border-width: 2px;
    }
    100% { 
        opacity: 0.6; 
        border-width: 1px;
    }
}

.sub-module.active {
    animation: pulse 1.5s ease-in-out infinite;
}

/* Streaming content indicator */
@keyframes streaming {
    0% { content: ""; }
    25% { content: "."; }
    50% { content: ".."; }
    75% { content: "..."; }
    100% { content: ""; }
}

.streaming-indicator::after {
    animation: streaming 1s infinite;
}
```

### Focus Indicators

```css
/* V3's focus patterns */
.prompt-input.focused {
    border: solid var(--sacred-yellow);
    box-shadow: 0 0 0 1px var(--sacred-yellow);
}

.simple-block.focused {
    border-width: 2px;
    margin: 0 -1px;  /* Compensate for thicker border */
}
```

## Responsive Design Patterns

### Terminal Size Adaptation

```css
/* Small terminals (< 80 cols) */
@media (max-width: 80) {
    .simple-block {
        min-width: 8;       /* Reduced minimum */
        padding: 0 1;       /* Compact padding */
    }
    
    .live-workspace {
        max-height: 40vh;   /* More space for timeline */
    }
}

/* Large terminals (> 120 cols) */
@media (min-width: 120) {
    .simple-block {
        max-width: 100;     /* Wider content area */
    }
    
    .live-workspace {
        max-height: 60vh;   /* More workspace room */
    }
}
```

### Content-Driven Sizing

```css
/* Dynamic height based on content */
.adaptive-content {
    height: auto;              /* Never fixed heights */
    min-height: 3;             /* Readable minimum */
    max-height: 80vh;          /* Prevent screen takeover */
    overflow-y: auto;          /* Scroll when needed */
}

/* Responsive text handling */
.responsive-text {
    word-wrap: break-word;     /* Handle long lines */
    overflow-wrap: break-word; /* Ensure text fits */
    white-space: pre-wrap;     /* Preserve formatting */
}
```

## Typography Hierarchy

### Text Styling System

```css
/* Sacred Architecture typography */
.sacred-title {
    font-weight: bold;
    color: var(--text-accent);
    text-decoration: underline;
}

.sacred-header {
    font-weight: bold;
    color: var(--text);
}

.sacred-body {
    font-weight: normal;
    color: var(--text);
    line-height: 1.4;
}

.sacred-meta {
    font-size: small;
    color: var(--text-muted);
    font-style: italic;
}

.sacred-code {
    font-family: monospace;
    background: var(--surface-muted);
    padding: 0 1;
    border: solid gray;
}

.sacred-error {
    font-weight: bold;
    color: var(--sacred-red);
}
```

### Message Formatting

```css
/* Block content styling */
.block-header {
    font-weight: bold;
    color: var(--text-accent);
    margin-bottom: 1;
}

.block-content {
    color: var(--text);
    white-space: pre-wrap;
}

.block-metadata {
    font-size: small;
    color: var(--text-muted);
    margin-top: 1;
    padding-top: 1;
    border-top: solid gray;
}

/* Cognition sub-module styling */
.sub-module-title {
    font-weight: bold;
    color: var(--sacred-purple);
}

.sub-module-model {
    font-size: small;
    color: var(--text-muted);
}

.sub-module-content {
    margin-top: 1;
    padding-top: 1;
}
```

## Icon System

### Sacred Architecture Iconography

```css
/* Role icons using text symbols */
.icon-user::before { content: "👤 "; }
.icon-assistant::before { content: "🤖 "; }
.icon-cognition::before { content: "🧠 "; }
.icon-system::before { content: "⚙️ "; }

/* State icons */
.icon-active::before { content: "⚡ "; }
.icon-completed::before { content: "✅ "; }
.icon-pending::before { content: "⏳ "; }
.icon-error::before { content: "❌ "; }
.icon-warning::before { content: "⚠️ "; }

/* Processing icons */
.icon-processing::before { content: "🔄 "; }
.icon-streaming::before { content: "📡 "; }
.icon-thinking::before { content: "💭 "; }

/* Meta icons */
.icon-time::before { content: "⏱️ "; }
.icon-tokens::before { content: "📊 "; }
.icon-model::before { content: "🧪 "; }
```

## Valid Textual CSS Properties

### ✅ Supported Properties (Use These)

```css
/* Layout */
width: auto | 1fr | 50% | 20;
height: auto | 1fr | 50% | 10;
min-width: 10;
max-width: 100;
min-height: 3;
max-height: 50vh;

/* Spacing */
margin: 1 0;
margin-top: 1;
margin-right: 0; 
margin-bottom: 1;
margin-left: 0;
padding: 1;
padding-top: 1;
padding-right: 1;
padding-bottom: 1;
padding-left: 1;

/* Borders */
border: solid blue;
border: dashed red;
border: double green;
border-top: solid gray;
border-right: solid gray;
border-bottom: solid gray;
border-left: solid gray;

/* Colors */
color: blue;
background: #1a1a1a;
opacity: 0.8;

/* Display */
display: block;
display: none;
visibility: visible;
visibility: hidden;

/* Text */
text-align: left;
text-align: center;
text-align: right;
```

### ❌ Invalid Properties (Will Break)

```css
/* These don't exist in Textual */
border-color: blue;        /* Use: border: solid blue */
background-color: red;     /* Use: background: red */
font-family: Arial;        /* Not supported */
font-size: 14px;          /* Not supported */
box-shadow: 0 0 5px;      /* Not supported */
border-radius: 5px;       /* Not supported */
position: absolute;       /* Not supported */
z-index: 100;             /* Not supported */
```

## Design Guidelines

### V3-Based Best Practices

```
┌─ COPY FROM PROVEN IMPLEMENTATIONS ───────────────────────┐
│                                                           │
│  📚 Study V3's chat.tcss → Copy working patterns         │
│  📚 Extract Claude Code styles → Adapt for Sacred GUI    │
│  📚 Review Textual examples → Use proven CSS properties  │
│  🚫 NEVER invent CSS from scratch without references     │
│  🔍 When stuck, find how others styled similar widgets   │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### Quality Checklist

```
☐ Uses only valid Textual CSS properties
☐ Follows V3's color coding patterns
☐ Implements content-driven sizing (height: auto)
☐ Supports responsive terminal sizes
☐ Maintains high contrast for accessibility
☐ Uses semantic color coding (green=success, red=error)
☐ Keeps animations subtle and functional
☐ Tests in various terminal sizes
☐ No hardcoded dimensions that break with content
☐ Follows Sacred Architecture three-area layout
```

### Anti-Patterns to Avoid

```
❌ Invalid CSS properties (border-color, background-color)
❌ Fixed heights that break with dynamic content
❌ Poor contrast ratios
❌ Excessive animations that distract  
❌ Layout that breaks in small terminals
❌ Hardcoded color values in widget code
❌ Nested container styling conflicts
❌ Inconsistent spacing and alignment
❌ Colors that don't follow role-based coding
❌ Styles that conflict with V3 patterns
```

## Theme System Architecture

### Theme Structure (V3-Compatible)

```python
# Sacred Architecture theme definition
SACRED_THEMES = {
    "dark": {
        "primary": "#0066CC",
        "accent": "#FFAA00", 
        "success": "#00AA44",
        "warning": "#FFAA00",
        "error": "#CC2222",
        "cognition": "#7744CC",
        "assistant": "#FF6600",
        "background": "#1A1A1A",
        "surface": "#2A2A2A",
        "surface-muted": "#1A1A1A",
        "text": "#CCCCCC",
        "text-muted": "#888888",
        "text-accent": "#FFFFFF",
        "dark": True
    },
    "light": {
        "primary": "#0066CC",
        "accent": "#FF8800",
        "success": "#00AA44", 
        "warning": "#FF8800",
        "error": "#CC2222",
        "cognition": "#7744CC",
        "assistant": "#FF6600",
        "background": "#FFFFFF",
        "surface": "#F5F5F5",
        "surface-muted": "#E5E5E5",
        "text": "#333333",
        "text-muted": "#666666",
        "text-accent": "#000000",
        "dark": False
    }
}
```

### Dynamic Theme Application

```css
/* Theme variables in CSS */
.theme-dark {
    --primary: #0066CC;
    --surface: #2A2A2A;
    --text: #CCCCCC;
}

.theme-light {
    --primary: #0066CC;
    --surface: #F5F5F5;
    --text: #333333;
}

/* Theme-aware styling */
.sacred-timeline {
    background: var(--surface);
    color: var(--text);
    border: solid var(--primary);
}
```

## File Organization

### CSS File Structure

```
src/widgets/
├── sacred_timeline.tcss     # V3's chat_container styles
├── live_workspace.tcss      # V3's dynamic container styles  
├── simple_block.tcss        # V3's Chatbox styles
├── sub_module.tcss          # Cognition sub-module styles
├── prompt_input.tcss        # V3's input styles
├── error_boundary.tcss      # Error display styles
└── shared/
    ├── colors.tcss          # Sacred Architecture color system
    ├── animations.tcss      # Transition and animation patterns
    ├── typography.tcss      # Text styling hierarchy
    └── responsive.tcss      # Terminal size adaptations
```

### Style Loading Order

```python
# Load styles in dependency order
CSS_FILES = [
    "src/widgets/shared/colors.tcss",      # Base colors first
    "src/widgets/shared/typography.tcss",  # Text styles
    "src/widgets/shared/animations.tcss",  # Animations
    "src/widgets/shared/responsive.tcss",  # Responsive rules
    "src/widgets/sacred_timeline.tcss",    # Widget styles
    "src/widgets/live_workspace.tcss",
    "src/widgets/simple_block.tcss",
    "src/widgets/sub_module.tcss",
    "src/widgets/prompt_input.tcss",
    "src/widgets/error_boundary.tcss",
]
```

---

**Next Steps**: After implementing design patterns, see:
- Reference Guide → `.ai/docs/REFERENCE-GUIDE.md`
- Testing Guide → `.ai/docs/TESTING-GUIDE.md`