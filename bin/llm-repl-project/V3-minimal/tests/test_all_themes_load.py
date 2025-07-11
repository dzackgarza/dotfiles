"""Test that validates ALL Textual themes can be loaded without errors"""

import pytest
from src.config import ThemeConfig
from src.main import LLMReplApp


class TestTextualThemes:
    """Test that all Textual themes can be registered and used without errors"""

    def test_all_themes_load_in_app(self):
        """Test that every theme can be registered and loaded by the app"""

        async def test_themes():
            app = LLMReplApp()

            async with app.run_test() as pilot:
                # Themes should be registered during on_mount
                for theme_name in ThemeConfig.AVAILABLE_THEMES.keys():
                    # Try to switch to each theme
                    success = app.switch_theme(theme_name)
                    assert success, f"Failed to switch to theme: {theme_name}"
                    assert app.theme == theme_name, f"Theme not applied: {theme_name}"

        import asyncio
        import os

        # Clean up any saved theme preference to avoid test pollution
        try:
            asyncio.run(test_themes())
        finally:
            try:
                os.remove(os.path.expanduser("~/.config/llm-repl/theme"))
            except FileNotFoundError:
                pass

    def test_default_theme_loads_without_error(self):
        """Test that the default theme loads correctly"""

        async def test_default():
            app = LLMReplApp()
            async with app.run_test() as pilot:
                # Default theme should be applied
                assert app.theme == ThemeConfig.DEFAULT_THEME

        import asyncio

        asyncio.run(test_default())

    def test_theme_config_completeness(self):
        """Test that all themes have complete Textual theme configuration"""
        required_keys = {
            "name",
            "description",
            "primary",
            "secondary",
            "accent",
            "warning",
            "error",
            "success",
            "dark",
        }

        for theme_name, theme_config in ThemeConfig.AVAILABLE_THEMES.items():
            missing_keys = required_keys - set(theme_config.keys())
            assert (
                not missing_keys
            ), f"Theme '{theme_name}' missing keys: {missing_keys}"

            # Verify color values are valid hex colors
            color_keys = {
                "primary",
                "secondary",
                "accent",
                "warning",
                "error",
                "success",
            }
            for key in color_keys:
                color = theme_config[key]
                assert isinstance(
                    color, str
                ), f"Theme '{theme_name}' {key} is not a string"
                assert color.startswith(
                    "#"
                ), f"Theme '{theme_name}' {key} is not a hex color: {color}"
                assert len(color) in [
                    4,
                    7,
                ], f"Theme '{theme_name}' {key} invalid hex length: {color}"

            # Verify dark mode is boolean
            assert isinstance(
                theme_config["dark"], bool
            ), f"Theme '{theme_name}' dark is not boolean"

    def test_theme_creation_from_config(self):
        """Test that Theme objects can be created from all configurations"""
        app = LLMReplApp()

        for theme_name, theme_config in ThemeConfig.AVAILABLE_THEMES.items():
            try:
                theme = app._create_theme_from_config(theme_name, theme_config)
                assert theme.name == theme_name
                assert theme.primary == theme_config["primary"]
                assert theme.dark == theme_config["dark"]
            except Exception as e:
                pytest.fail(f"Failed to create theme '{theme_name}': {e}")

    def test_saved_theme_persistence(self):
        """Test that theme preferences are saved and loaded correctly"""
        app = LLMReplApp()

        # Test saving and loading
        test_theme = "tokyo_night"
        app._save_theme_preference(test_theme)
        loaded_theme = app._load_saved_theme()
        assert loaded_theme == test_theme

        # Clean up
        import os

        try:
            os.remove(os.path.expanduser("~/.config/llm-repl/theme"))
        except FileNotFoundError:
            pass
