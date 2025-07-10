# Textual Styling & Theming Ledger

**Scope:** Terminal-native aesthetic design for Arch + Sway integration  
**Goal:** Seamless visual integration with tiled terminal environments

## Terminal Aesthetic Principles

### Sway Integration Requirements
- **Gap-aware design**: Respects Sway's window gaps
- **Transparency support**: Works with terminal transparency settings
- **Tiling behavior**: Looks natural in terminal grid layouts
- **Keyboard-first**: Optimized for keyboard navigation
- **Minimalist**: Clean, uncluttered terminal aesthetic

### Color Scheme Integration
- **Terminal theme inheritance**: Respect user's terminal color scheme
- **Popular ricing schemes**: Tokyo Night, Nord, Dracula, Rosé Pine, Kanagawa
- **Adaptive theming**: Automatically adapt to terminal background
- **Accessibility**: High contrast, readable in various lighting

## Theme Architecture

### 1. Theme Definition System

```python
# theme/theme.py
from typing import Dict, Any
from enum import Enum

class ThemeVariant(Enum):
    TOKYO_NIGHT = "tokyo_night"
    NORD = "nord" 
    DRACULA = "dracula"
    ROSE_PINE = "rose_pine"
    KANAGAWA = "kanagawa"
    TERMINAL_AUTO = "terminal_auto"  # Inherit from terminal

class TerminalTheme:
    """Terminal-native theme definitions"""
    
    # Tokyo Night (most popular in ricing community)
    TOKYO_NIGHT = {
        "name": "Tokyo Night",
        "description": "Clean dark theme celebrating Tokyo lights",
        "colors": {
            # Background layers
            "background": "#1a1b26",      # Main background
            "surface": "#24283b",         # Elevated surfaces
            "surface_variant": "#3b4261", # Timeline blocks
            
            # Text colors
            "text_primary": "#c0caf5",    # Main text
            "text_secondary": "#9aa5ce",  # Secondary text
            "text_muted": "#565f89",      # Muted text
            
            # Accent colors for block types
            "accent_user": "#9ece6a",     # User input (green)
            "accent_assistant": "#7dcfff", # Assistant (cyan)
            "accent_system": "#bb9af7",   # System (purple)
            "accent_error": "#f7768e",    # Error (red)
            "accent_processing": "#e0af68", # Processing (orange)
            
            # UI elements
            "border": "#414868",          # Borders
            "border_focus": "#7aa2f7",    # Focused borders
            "selection": "#364a82",       # Selection background
        },
        "fonts": {
            "mono": ("JetBrains Mono", "Fira Code", "Consolas", "monospace"),
            "ui": ("Inter", "system-ui", "sans-serif"),
        }
    }
    
    # Nord (minimalist Scandinavian)
    NORD = {
        "name": "Nord",
        "description": "Arctic, north-bluish clean palette",
        "colors": {
            "background": "#2e3440",
            "surface": "#3b4252", 
            "surface_variant": "#434c5e",
            
            "text_primary": "#eceff4",
            "text_secondary": "#e5e9f0",
            "text_muted": "#4c566a",
            
            "accent_user": "#a3be8c",     # Green
            "accent_assistant": "#88c0d0", # Cyan
            "accent_system": "#b48ead",   # Purple
            "accent_error": "#bf616a",    # Red
            "accent_processing": "#ebcb8b", # Yellow
            
            "border": "#4c566a",
            "border_focus": "#81a1c1",
            "selection": "#434c5e",
        }
    }
    
    # Dracula (widely used)
    DRACULA = {
        "name": "Dracula", 
        "description": "Dark theme with vibrant colors",
        "colors": {
            "background": "#282a36",
            "surface": "#44475a",
            "surface_variant": "#6272a4",
            
            "text_primary": "#f8f8f2",
            "text_secondary": "#f8f8f2",
            "text_muted": "#6272a4",
            
            "accent_user": "#50fa7b",     # Green
            "accent_assistant": "#8be9fd", # Cyan
            "accent_system": "#bd93f9",   # Purple
            "accent_error": "#ff5555",    # Red
            "accent_processing": "#f1fa8c", # Yellow
            
            "border": "#6272a4",
            "border_focus": "#bd93f9",
            "selection": "#44475a",
        }
    }
    
    @classmethod
    def get_theme(cls, variant: ThemeVariant) -> Dict[str, Any]:
        """Get theme definition by variant"""
        themes = {
            ThemeVariant.TOKYO_NIGHT: cls.TOKYO_NIGHT,
            ThemeVariant.NORD: cls.NORD,
            ThemeVariant.DRACULA: cls.DRACULA,
        }
        return themes.get(variant, cls.TOKYO_NIGHT)
```

### 2. Textual CSS Implementation

```css
/* theme/theme.tcss - Main stylesheet */

/* Color variable definitions - injected by Python theme system */
:root {
    --background: #1a1b26;
    --surface: #24283b;
    --surface-variant: #3b4261;
    
    --text-primary: #c0caf5;
    --text-secondary: #9aa5ce;
    --text-muted: #565f89;
    
    --accent-user: #9ece6a;
    --accent-assistant: #7dcfff;
    --accent-system: #bb9af7;
    --accent-error: #f7768e;
    --accent-processing: #e0af68;
    
    --border: #414868;
    --border-focus: #7aa2f7;
    --selection: #364a82;
}

/* Application root */
App {
    background: $background;
    color: $text-primary;
}

/* Main layout containers */
Vertical {
    background: $background;
}

Horizontal {
    background: $background;
}

/* Header styling */
Header {
    background: $surface;
    color: $text-primary;
    text-style: bold;
    padding: 0 1;
    border-bottom: solid $border;
}

/* Footer with keyboard shortcuts */
Footer {
    background: $surface;
    color: $text-secondary;
    padding: 0 1;
    border-top: solid $border;
}

/* Timeline widget */
TimelineWidget {
    background: $background;
    border: round $border;
    padding: 1;
    scrollbar-background: $surface;
    scrollbar-color: $border;
    scrollbar-color-hover: $border-focus;
}

/* Timeline block styling */
.timeline-block {
    margin: 1 0;
    padding: 1;
}

.block-header {
    text-style: bold;
    margin-bottom: 1;
}

.block-content {
    margin-left: 2;
    text-style: none;
}

.block-separator {
    color: $text-muted;
    text-align: center;
    margin: 1 0;
}

/* Block type specific colors */
.user-block .block-header {
    color: $accent-user;
}

.assistant-block .block-header {
    color: $accent-assistant;
}

.system-block .block-header {
    color: $accent-system;
}

.error-block .block-header {
    color: $accent-error;
}

.processing-block .block-header {
    color: $accent-processing;
}

/* Input widget styling */
InputWidget {
    background: $surface;
    border: round $border;
    padding: 1;
    margin: 1 0;
}

/* Terminal-like input field */
Input {
    background: $background;
    color: $text-primary;
    border: solid $border;
    border-title-color: $text-secondary;
    
    /* Terminal cursor styling */
    cursor-blink: true;
    cursor-color: $text-primary;
}

Input:focus {
    border: solid $border-focus;
    border-title-color: $border-focus;
}

/* Button styling - minimal, terminal-like */
Button {
    background: $surface;
    color: $text-primary;
    border: solid $border;
    text-style: none;
    margin: 0 1;
}

Button:hover {
    background: $surface-variant;
    border: solid $border-focus;
}

Button:focus {
    background: $surface-variant;
    border: solid $border-focus;
    text-style: bold;
}

/* Primary button (Send) */
Button.-primary {
    background: $accent-user;
    color: $background;
    border: solid $accent-user;
}

Button.-primary:hover {
    background: $accent-user;
    color: $background;
    text-style: bold;
}

/* Status indicators */
.status-ready {
    color: $accent-user;
}

.status-processing {
    color: $accent-processing;
    text-style: italic;
}

.status-error {
    color: $accent-error;
    text-style: bold;
}

/* Responsive design for different terminal sizes */
@media (max-width: 80) {
    InputWidget {
        padding: 0;
    }
    
    TimelineWidget {
        padding: 0 1;
    }
}

@media (max-height: 24) {
    Header, Footer {
        display: none;
    }
}
```

### 3. Dynamic Theme Loading

```python
# theme/loader.py
import os
from typing import Optional
from textual.app import App

class ThemeLoader:
    """Dynamic theme loading and application"""
    
    @staticmethod
    def detect_terminal_theme() -> Optional[ThemeVariant]:
        """Attempt to detect terminal theme from environment"""
        
        # Check common terminal theme environment variables
        if os.getenv("COLORTERM"):
            colorterm = os.getenv("COLORTERM", "").lower()
            if "tokyo" in colorterm or "night" in colorterm:
                return ThemeVariant.TOKYO_NIGHT
            elif "nord" in colorterm:
                return ThemeVariant.NORD
            elif "dracula" in colorterm:
                return ThemeVariant.DRACULA
        
        # Check terminal background color (if available)
        # This is terminal-specific and may not work everywhere
        bg_color = os.getenv("TERM_BACKGROUND_COLOR")
        if bg_color:
            if bg_color.startswith("#1a1b26"):  # Tokyo Night
                return ThemeVariant.TOKYO_NIGHT
            elif bg_color.startswith("#2e3440"):  # Nord
                return ThemeVariant.NORD
                
        return None
    
    @staticmethod
    def apply_theme(app: App, variant: ThemeVariant) -> None:
        """Apply theme to Textual app"""
        theme_def = TerminalTheme.get_theme(variant)
        
        # Generate CSS variables from theme
        css_vars = ThemeLoader._generate_css_variables(theme_def["colors"])
        
        # Update app CSS with new variables
        app.stylesheet.set_variables(css_vars)
        app.refresh()
    
    @staticmethod
    def _generate_css_variables(colors: Dict[str, str]) -> Dict[str, str]:
        """Convert theme colors to CSS variables"""
        css_vars = {}
        for key, value in colors.items():
            css_key = key.replace("_", "-")
            css_vars[css_key] = value
        return css_vars
```

### 4. Terminal Integration Features

```python
# theme/terminal_integration.py
import subprocess
import os
from typing import Tuple, Optional

class TerminalIntegration:
    """Integration with terminal features"""
    
    @staticmethod
    def supports_transparency() -> bool:
        """Check if terminal supports transparency"""
        term = os.getenv("TERM", "")
        return any(x in term for x in ["alacritty", "kitty", "wezterm", "foot"])
    
    @staticmethod
    def get_terminal_size() -> Tuple[int, int]:
        """Get current terminal size"""
        try:
            result = subprocess.run(
                ["stty", "size"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            lines, cols = result.stdout.strip().split()
            return int(lines), int(cols)
        except:
            return 24, 80  # Default fallback
    
    @staticmethod
    def is_sway_environment() -> bool:
        """Check if running under Sway window manager"""
        return os.getenv("SWAYSOCK") is not None
    
    @staticmethod
    def get_font_info() -> Optional[str]:
        """Try to detect terminal font"""
        # This is very terminal-specific and may not work
        # Most terminals don't expose font info to applications
        term_program = os.getenv("TERM_PROGRAM", "")
        if term_program == "Alacritty":
            # Could parse alacritty config, but that's complex
            pass
        return None
```

### 5. Block-Specific Styling

```python
# widgets/styled_blocks.py
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from core.blocks import TimelineBlock, BlockType

class BlockRenderer:
    """Render timeline blocks with terminal aesthetics"""
    
    def __init__(self, theme: Dict[str, str]):
        self.theme = theme
    
    def render_user_block(self, block: TimelineBlock) -> Panel:
        """Render user input block"""
        header = Text(f"❯ {block.title}", style=f"bold {self.theme['accent_user']}")
        content = Text(f"  {block.content}", style=self.theme['text_primary'])
        
        return Panel(
            Align.left(Text.assemble(header, "\\n", content)),
            border_style=self.theme['accent_user'],
            padding=(0, 1),
            title="[dim]User[/dim]",
            title_align="left"
        )
    
    def render_assistant_block(self, block: TimelineBlock) -> Panel:
        """Render assistant response block"""
        header = Text(f"🤖 {block.title}", style=f"bold {self.theme['accent_assistant']}")
        content = Text(block.content, style=self.theme['text_primary'])
        
        return Panel(
            Align.left(Text.assemble(header, "\\n", content)),
            border_style=self.theme['accent_assistant'],
            padding=(0, 1),
            title="[dim]Assistant[/dim]",
            title_align="left"
        )
    
    def render_system_block(self, block: TimelineBlock) -> Panel:
        """Render system check block"""
        header = Text(f"⚙️  {block.title}", style=f"bold {self.theme['accent_system']}")
        content = Text(block.content, style=self.theme['text_secondary'])
        
        return Panel(
            Align.left(Text.assemble(header, "\\n", content)),
            border_style=self.theme['accent_system'],
            padding=(0, 1),
            title="[dim]System[/dim]",
            title_align="left"
        )
```

## Implementation Strategy

### Phase 1: Basic Theme Infrastructure
1. Create theme definition system
2. Implement CSS variable injection
3. Create basic Textual CSS
4. Test with Tokyo Night theme

### Phase 2: Advanced Theming
1. Add multiple theme variants
2. Implement theme detection
3. Add terminal integration features
4. Create responsive design rules

### Phase 3: Polish & Optimization
1. Fine-tune typography
2. Optimize for different terminal sizes
3. Add accessibility features
4. Performance optimization

This styling system will create a truly terminal-native aesthetic that seamlessly integrates with Sway's tiled environment while respecting user's terminal theming choices.