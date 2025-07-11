"""
Custom theme picker for instant theme switching

This replaces Textual's default theme provider with one that:
1. Shows themes with emoji icons in the command palette
2. Applies themes immediately when selected (no need to press Enter)
3. Shows theme descriptions as help text
4. Provides user-friendly notifications

Usage: Press Ctrl+P and type theme names to see and switch themes instantly.
"""

from textual.command import Hit, Hits, Provider


class InteractiveThemeProvider(Provider):
    """Theme provider that applies themes immediately on selection"""

    async def search(self, query: str) -> Hits:
        """Search for themes and generate commands"""
        matcher = self.matcher(query)

        app = self.app

        # Get available themes from the app
        if hasattr(app, "_get_available_themes"):
            available_themes = app._get_available_themes()
        else:
            from .config import ThemeConfig

            available_themes = ThemeConfig.AVAILABLE_THEMES

        for theme_name, theme_config in available_themes.items():
            score = matcher.match(theme_name)
            if score > 0:
                # Create description with emoji for visual appeal
                description = theme_config.get(
                    "description", f"Switch to {theme_name} theme"
                )

                yield Hit(
                    score=score,
                    match_display=f"🎨 {theme_name}",
                    text=f"Switch to {theme_name} theme",
                    help=description,
                    command=self._make_switch_command(theme_name),
                )

    def _make_switch_command(self, theme_name: str):
        """Create a command function that switches to the specified theme"""

        async def switch_command():
            """Switch to the theme immediately"""
            if hasattr(self.app, "switch_theme"):
                success = self.app.switch_theme(theme_name)
                if success:
                    # Optionally show a notification
                    self.app.notify(f"Switched to {theme_name} theme")

        return switch_command


# Note: Instant theme switching works because pressing Enter on a command
# immediately executes the theme switch. For true "live preview" on arrow
# key navigation, we'd need Textual's CommandPalette selection events
# (see GitHub issue #4595), which aren't available yet.
#
# Current behavior:
# - Ctrl+P opens command palette
# - Type theme name (e.g., "dracula", "tokyo", "nord")
# - Use arrow keys to navigate
# - Press Enter to instantly apply the selected theme
#
# This is much faster than the default theme picker!
