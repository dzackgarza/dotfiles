from pydantic import BaseModel, Field
from textual.design import ColorSystem
import yaml

from elia_chat.locations import theme_directory


class Theme(BaseModel):
    name: str = Field(exclude=True)
    primary: str
    secondary: str | None = None
    background: str | None = None
    surface: str | None = None
    panel: str | None = None
    warning: str | None = None
    error: str | None = None
    success: str | None = None
    accent: str | None = None
    dark: bool = True

    def to_color_system(self) -> ColorSystem:
        """Convert this theme to a ColorSystem."""
        return ColorSystem(
            **self.model_dump(
                exclude={
                    "text_area",
                    "syntax",
                    "variable",
                    "url",
                    "method",
                }
            )
        )


def load_user_themes() -> dict[str, Theme]:
    """Load user themes from "~/.config/elia/themes".

    Returns:
        A dictionary mapping theme names to theme objects.
    """
    themes: dict[str, Theme] = {}
    for path in theme_directory().iterdir():
        path_suffix = path.suffix
        if path_suffix == ".yaml" or path_suffix == ".yml":
            with path.open() as theme_file:
                theme_content = yaml.load(theme_file, Loader=yaml.FullLoader) or {}
                try:
                    themes[theme_content["name"]] = Theme(**theme_content)
                except KeyError:
                    raise ValueError(
                        f"Invalid theme file {path}. A `name` is required."
                    )
    return themes


BUILTIN_THEMES: dict[str, Theme] = {
    "textual": Theme(
        name="textual",
        primary="#004578",
        secondary="#0178D4",
        warning="#ffa62b",
        error="#ba3c5b",
        success="#4EBF71",
        accent="#ffa62b",
        dark=True,
    ),
    "monokai": Theme(
        name="monokai",
        primary="#F92672",  # Pink
        secondary="#66D9EF",  # Light Blue
        warning="#FD971F",  # Orange
        error="#F92672",  # Pink (same as primary for consistency)
        success="#A6E22E",  # Green
        accent="#AE81FF",  # Purple
        background="#272822",  # Dark gray-green
        surface="#3E3D32",  # Slightly lighter gray-green
        panel="#3E3D32",  # Same as surface for consistency
        dark=True,
    ),
    "nautilus": Theme(
        name="nautilus",
        primary="#0077BE",  # Ocean Blue
        secondary="#20B2AA",  # Light Sea Green
        warning="#FFD700",  # Gold (like sunlight on water)
        error="#FF6347",  # Tomato (like a warning buoy)
        success="#32CD32",  # Lime Green (like seaweed)
        accent="#FF8C00",  # Dark Orange (like a sunset over water)
        dark=True,
        background="#001F3F",  # Dark Blue (deep ocean)
        surface="#003366",  # Navy Blue (shallower water)
        panel="#005A8C",  # Steel Blue (water surface)
    ),
    "galaxy": Theme(
        name="galaxy",
        primary="#5A67D8",  # Subtle Accent 2 (Dark) for Assistant/Cognition
        secondary="#333333", # Neutral/Base (Dark) for System
        warning="#FFD700",  # Gold, more visible than orange
        error="#FF4500",  # OrangeRed, vibrant but less harsh than pure red
        success="#4A5568",  # Subtle Accent 1 (Dark) for User
        accent="#38A169",  # Subtle Accent 3 (Dark) for Processing/Tool
        dark=True,
        background="#0F0F1F",  # Very Dark Blue, almost black
        surface="#1E1E3F",  # Dark Blue-Purple
        panel="#2D2B55",  # Slightly Lighter Blue-Purple
    ),
    "nebula": Theme(
        name="nebula",
        primary="#4169E1",  # Royal Blue, more vibrant than Midnight Blue
        secondary="#9400D3",  # Dark Violet, more vibrant than Indigo Dye
        warning="#FFD700",  # Kept Gold for warnings
        error="#FF1493",  # Deep Pink, more nebula-like than Crimson
        success="#00FF7F",  # Spring Green, slightly more vibrant
        accent="#FF00FF",  # Magenta, for a true neon accent
        dark=True,
        background="#0A0A23",  # Dark Navy, closer to a night sky
        surface="#1C1C3C",  # Dark Blue-Purple
        panel="#2E2E5E",  # Slightly Lighter Blue-Purple
    ),
    "alpine": Theme(
        name="alpine",
        primary="#4A90E2",  # Clear Sky Blue
        secondary="#81A1C1",  # Misty Blue
        warning="#EBCB8B",  # Soft Sunlight
        error="#BF616A",  # Muted Red
        success="#A3BE8C",  # Alpine Meadow Green
        accent="#5E81AC",  # Mountain Lake Blue
        dark=True,
        background="#2E3440",  # Dark Slate Grey
        surface="#3B4252",  # Darker Blue-Grey
        panel="#434C5E",  # Lighter Blue-Grey
    ),
    "cobalt": Theme(
        name="cobalt",
        primary="#334D5C",  # Deep Cobalt Blue
        secondary="#4878A6",  # Slate Blue
        warning="#FFAA22",  # Amber, suitable for warnings related to primary
        error="#E63946",  # Red, universally recognized for errors
        success="#4CAF50",  # Green, commonly used for success indication
        accent="#D94E64",  # Candy Apple Red
        dark=True,
        surface="#27343B",  # Dark Lead
        panel="#2D3E46",  # Storm Gray
        background="#1F262A",  # Charcoal
    ),
    "twilight": Theme(
        name="twilight",
        primary="#367588",
        secondary="#5F9EA0",
        warning="#FFD700",
        error="#FF6347",
        success="#00FA9A",
        accent="#FF7F50",
        dark=True,
        background="#191970",
        surface="#3B3B6D",
        panel="#4C516D",
    ),
    "hacker": Theme(
        name="hacker",
        primary="#00FF00",  # Bright Green (Lime)
        secondary="#32CD32",  # Lime Green
        warning="#ADFF2F",  # Green Yellow
        error="#FF4500",  # Orange Red (for contrast)
        success="#00FA9A",  # Medium Spring Green
        accent="#39FF14",  # Neon Green
        dark=True,
        background="#0D0D0D",  # Almost Black
        surface="#1A1A1A",  # Very Dark Gray
        panel="#2A2A2A",  # Dark Gray
    ),
    "tokyo_night": Theme(
        name="tokyo_night",
        primary="#7dcfff",      # Cyan
        secondary="#bb9af7",    # Purple  
        background="#1a1b26",   # Dark blue-gray
        surface="#24283b",      # Lighter blue-gray
        panel="#3b4261",        # Block background
        warning="#e0af68",      # Orange
        error="#f7768e",        # Red
        success="#9ece6a",      # Green
        accent="#7aa2f7",       # Blue
        dark=True
    ),
    "nord": Theme(
        name="nord",
        primary="#88c0d0",      # Frost cyan
        secondary="#b48ead",    # Aurora purple
        background="#2e3440",   # Polar night
        surface="#3b4252",      # Darker polar night
        panel="#434c5e",        # Block background
        warning="#ebcb8b",      # Aurora yellow
        error="#bf616a",        # Aurora red
        success="#a3be8c",      # Aurora green
        accent="#81a1c1",       # Frost blue
        dark=True
    ),
    "dracula": Theme(
        name="dracula",
        primary="#8be9fd",      # Cyan
        secondary="#bd93f9",    # Purple
        background="#282a36",   # Dark background
        surface="#44475a",      # Current line
        panel="#6272a4",        # Comment gray
        warning="#f1fa8c",      # Yellow
        error="#ff5555",        # Red
        success="#50fa7b",      # Green
        accent="#ffb86c",       # Orange
        dark=True
    ),
    "rose_pine": Theme(
        name="rose_pine",
        primary="#9ccfd8",      # Foam cyan
        secondary="#c4a7e7",    # Iris purple
        background="#191724",   # Base dark
        surface="#1f1d2e",     # Surface
        panel="#26233a",       # Overlay
        warning="#f6c177",     # Gold
        error="#eb6f92",       # Love pink
        success="#31748f",     # Pine teal
        accent="#ebbcba",      # Rose
        dark=True
    ),
    "kanagawa": Theme(
        name="kanagawa",
        primary="#7e9cd8",      # Crystal blue
        secondary="#938aa9",    # Violet
        background="#1f1f28",   # Dark background
        surface="#2a2a37",     # Surface
        panel="#363646",       # Block background
        warning="#ffa066",     # Orange
        error="#e82424",       # Red
        success="#76946a",     # Green
        accent="#dca561",      # Yellow
        dark=True
    ),
}
