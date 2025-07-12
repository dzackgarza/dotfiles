# Design & Aesthetics

This directory contains styling guidelines, theming resources, and visual design specifications for the Sacred GUI Architecture.

## Files Overview

```
design/
├── README.md                    # This overview
├── textual-styling-theming.md   # Textual CSS styling and theming guide
├── sacred-color-palette.md      # Sacred Architecture color schemes
├── typography-guide.md          # Font and text styling guidelines
├── icon-system.md              # Icons and visual elements
└── responsive-design.md         # Responsive layout patterns
```

## Design Philosophy

```
┌─ Sacred Architecture Design Principles ──────────────────┐
│                                                           │
│  🎨 Minimalist Aesthetics: Clean, focused interface      │
│  🌓 Terminal-Native Feel: Respects terminal environment  │
│  📐 Content-First Design: Function over decoration       │
│  🎯 Visual Hierarchy: Clear information organization     │
│  ⚡ Performance-Minded: Lightweight CSS properties       │
│  🔧 Textual-Compliant: Valid CSS properties only        │
│  📱 Responsive by Default: Adapts to terminal size       │
│  🎪 Accessibility-Aware: High contrast, readable text    │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

## Sacred Architecture Visual Identity

### 🎨 **Color Palette**

```
┌─ SACRED COLOR SYSTEM ─────────────────────────────────────┐
│                                                            │
│  🟦 Primary Blue    #0066CC  │  Timeline borders, focus   │
│  🟩 Success Green   #00AA44  │  Completed states, success │
│  🟨 Warning Yellow  #FFAA00  │  In-progress, warnings     │
│  🟥 Error Red       #CC2222  │  Errors, critical states   │
│  ⚫ Dark Gray       #2A2A2A  │  Background, containers     │
│  ⚪ Light Gray      #CCCCCC  │  Text, borders, separators │
│  🟣 Cognition Purple #7744CC │  Cognition pipeline steps  │
│  🟠 Assistant Orange #FF6600 │  Assistant responses       │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 📝 **Typography Hierarchy**

```
┌─ TEXT STYLING SYSTEM ─────────────────────────────────────┐
│                                                            │
│  📢 h1: Panel Titles        │ Bold, primary color        │
│  📄 h2: Section Headers     │ Bold, secondary color      │
│  📝 body: Main Content      │ Regular, readable size     │
│  🔤 code: Code Blocks       │ Monospace, syntax colors  │
│  📎 meta: Timestamps/Stats  │ Small, muted color         │
│  ⚠️  error: Error Messages   │ Bold, error color          │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 🎯 **Visual Elements**

```
┌─ SACRED ARCHITECTURE ICONOGRAPHY ────────────────────────┐
│                                                            │
│  👤 User Input       │  🤖 Assistant Response            │
│  🧠 Cognition Step   │  ⚡ Active Processing              │
│  ✅ Completed        │  ⏳ Pending/Queued                │
│  ❌ Error/Failed     │  ⚠️  Warning State                 │
│  📊 Token Count      │  ⏱️  Duration Timer                │
│  🎯 Route Decision   │  🔄 Processing Loop               │
│  📚 Research Step    │  💻 Code Generation               │
│  ✨ Synthesis        │  🔗 Tool Execution                │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Widget Styling Patterns

### 🏗️ **Sacred Timeline Styling**

```css
/* Sacred Timeline Container */
.sacred-timeline {
    background: $dark-background;
    border: solid $primary-blue;
    padding: 1;
    height: auto;
}

/* Individual Blocks */
.simple-block-user {
    border: solid $success-green;
    background: $dark-surface;
    margin: 1 0;
}

.simple-block-assistant {
    border: solid $assistant-orange;  
    background: $dark-surface;
    margin: 1 0;
}

.simple-block-cognition {
    border: solid $cognition-purple;
    background: $dark-surface;
    margin: 1 0;
}

/* Turn Separators */
.turn-separator {
    height: 1;
    width: 100%;
    color: $muted-gray;
    opacity: 0.5;
    margin: 1 0;
}
```

### ⚡ **Live Workspace Styling**

```css
/* Live Workspace Container */
.live-workspace {
    background: $dark-background;
    border: solid $warning-yellow;
    padding: 1;
    height: auto;
    max-height: 50vh;
}

/* Hidden State (2-way split) */
.live-workspace.hidden {
    display: none;
}

/* Sub-Module Widgets */
.sub-module {
    height: auto;
    min-width: 12;
    margin: 0 0 1 0;
    padding: 1;
}

/* Sub-Module States */
.sub-module.active {
    border: solid $warning-yellow;
    opacity: 1.0;
}

.sub-module.completed {
    border: solid $success-green;
    opacity: 0.8;
}

.sub-module.pending {
    border: solid $muted-gray;
    opacity: 0.6;
}

.sub-module.error {
    border: solid $error-red;
    opacity: 1.0;
}
```

### 💬 **Input Area Styling**

```css
/* Prompt Input */
.prompt-input {
    height: auto;
    min-height: 3;
    max-height: 10;
    border: solid $primary-blue;
    background: $dark-surface;
    padding: 1;
}

/* Input States */
.prompt-input.focused {
    border: solid $warning-yellow;
}

.prompt-input.disabled {
    border: solid $muted-gray;
    opacity: 0.7;
}

/* Input Helpers */
.input-helper {
    color: $muted-gray;
    font-size: small;
}
```

## Responsive Design Patterns

### 📱 **Terminal Size Adaptation**

```
┌─ RESPONSIVE BREAKPOINTS ─────────────────────────────────┐
│                                                           │
│  📱 Small (< 80 cols)   │  Single column, minimal UI     │
│  💻 Medium (80-120 cols) │  Standard 3-area layout       │
│  🖥️  Large (> 120 cols)  │  Enhanced info, wider panels  │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### 📐 **Dynamic Content Adaptation**

```css
/* Content-Driven Sizing */
.adaptive-content {
    height: auto;              /* Never fixed heights */
    min-height: 3;             /* Maintain readability */
    max-height: 80vh;          /* Prevent screen takeover */
    overflow-y: auto;          /* Scroll when needed */
}

/* Responsive Text */
.responsive-text {
    word-wrap: break-word;     /* Handle long lines */
    overflow-wrap: break-word; /* Ensure text fits */
    white-space: pre-wrap;     /* Preserve formatting */
}
```

## Animation & Transitions

### ⚡ **State Transitions**

```css
/* Workspace Show/Hide */
.live-workspace {
    transition: opacity 0.3s ease-in-out;
}

.live-workspace.hidden {
    opacity: 0;
    transition: opacity 0.2s ease-in-out;
}

/* Sub-Module State Changes */
.sub-module {
    transition: border-color 0.2s ease-in-out,
                opacity 0.2s ease-in-out;
}

/* Progress Indicators */
.progress-bar {
    animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
    0% { opacity: 0.6; }
    50% { opacity: 1.0; }
    100% { opacity: 0.6; }
}
```

## Theme System

### 🌓 **Theme Architecture**

```python
# Sacred Architecture Theme Structure
SACRED_THEMES = {
    "dark": {
        "primary": "#0066CC",
        "secondary": "#7744CC", 
        "accent": "#00AA44",
        "warning": "#FFAA00",
        "error": "#CC2222",
        "success": "#00AA44",
        "background": "#1A1A1A",
        "surface": "#2A2A2A",
        "text": "#CCCCCC",
        "text_muted": "#888888",
        "dark": True
    },
    "light": {
        "primary": "#0066CC",
        "secondary": "#7744CC",
        "accent": "#00AA44", 
        "warning": "#FF8800",
        "error": "#CC2222",
        "success": "#00AA44",
        "background": "#FFFFFF",
        "surface": "#F5F5F5",
        "text": "#333333",
        "text_muted": "#666666", 
        "dark": False
    }
}
```

## Design Guidelines

### 🏆 **FIRST: Study Working Patterns**

```
┌─ COPY FROM PROVEN IMPLEMENTATIONS ───────────────────────┐
│                                                           │
│  📚 Study V3's chat.py CSS → Copy working patterns       │
│  📚 Extract Claude Code styles → Adapt for Sacred GUI   │
│  📚 Review Textual examples → Use proven CSS properties │
│  🚫 NEVER invent CSS from scratch without references    │
│  🔍 When stuck, find how others styled similar widgets  │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### ✅ **Best Practices (After Studying References)**

```
┌─ SACRED DESIGN BEST PRACTICES ───────────────────────────┐
│                                                           │
│  ✅ Use only valid Textual CSS properties                │
│  ✅ Prefer `border: solid color` over `border-color`     │
│  ✅ Use `height: auto` for dynamic content               │ 
│  ✅ Implement responsive text wrapping                   │
│  ✅ Maintain high contrast for accessibility             │
│  ✅ Use semantic color coding (green=success, red=error) │
│  ✅ Keep animations subtle and functional                │
│  ✅ Test in various terminal sizes                       │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### ❌ **Anti-Patterns**

```
┌─ DESIGN ANTI-PATTERNS TO AVOID ──────────────────────────┐
│                                                           │
│  ❌ Invalid CSS properties (border-color, background-color) │
│  ❌ Fixed heights that break with dynamic content        │
│  ❌ Poor contrast ratios                                 │
│  ❌ Excessive animations that distract                   │
│  ❌ Layout that breaks in small terminals                │
│  ❌ Hardcoded color values in widget code                │
│  ❌ Nested container styling conflicts                   │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

## File Descriptions

- **`textual-styling-theming.md`**: Complete guide to Textual CSS and theming
- **`sacred-color-palette.md`**: Detailed color system and usage guidelines  
- **`typography-guide.md`**: Text styling hierarchy and font guidelines
- **`icon-system.md`**: Visual elements and iconography standards
- **`responsive-design.md`**: Terminal adaptation and responsive patterns

## Cross-References

- **Architecture**: See `../architecture/GUI-VISION.md` for visual specifications
- **Implementation**: See `../implementation/` for CSS integration patterns
- **Testing**: See `../testing/` for visual validation approaches
- **Reference**: See `../reference/` for Textual CSS documentation