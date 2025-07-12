"""
Tests for enhanced configuration system
"""

import pytest
import tempfile
import yaml
from pathlib import Path
from unittest.mock import patch

from src.config.enhanced_config import (
    EnhancedConfigLoader,
    V3Config,
    get_config,
    get_animation_config,
    get_ui_config,
    get_theme_config,
)
from src.core.animation_clock import AnimationClock


class TestEnhancedConfigLoader:
    """Test the enhanced configuration loader"""

    def test_default_config_creation(self):
        """Test that default configuration can be created"""
        config = V3Config()
        assert config.app.title == "LLM REPL V3-minimal"
        assert config.animation.fps.production == 60
        assert config.animation.typewriter_speeds.initial == 1500

    def test_config_validation(self):
        """Test configuration validation with custom values"""
        config_dict = {
            "app": {"title": "Custom Title", "default_theme": "gruvbox"},
            "animation": {"fps": {"production": 30, "development": 90}},
        }

        config = V3Config(**config_dict)
        assert config.app.title == "Custom Title"
        assert config.app.default_theme == "gruvbox"
        assert config.animation.fps.production == 30
        assert config.animation.fps.development == 90
        # Should use defaults for missing values
        assert config.animation.fps.testing == 1000

    def test_invalid_config_validation(self):
        """Test that invalid configuration raises ValidationError"""
        with pytest.raises(Exception):  # Pydantic ValidationError
            config_dict = {
                "animation": {"fps": {"production": "invalid"}}  # Should be int
            }
            V3Config(**config_dict)

    def test_config_loader_with_file(self):
        """Test configuration loading from file"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            config_data = {
                "app": {"title": "Test App", "default_theme": "tokyo_night"},
                "animation": {"fps": {"production": 45}},
            }
            yaml.dump(config_data, f)
            temp_path = Path(f.name)

        try:
            loader = EnhancedConfigLoader(temp_path)
            config = loader.load_config()

            assert config.app.title == "Test App"
            assert config.app.default_theme == "tokyo_night"
            assert config.animation.fps.production == 45
        finally:
            temp_path.unlink()

    def test_config_loader_missing_file(self):
        """Test configuration loader with missing file generates default"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.yaml"
            loader = EnhancedConfigLoader(config_path)
            config = loader.load_config()

            # Should create default config
            assert config.app.title == "LLM REPL V3-minimal"
            assert config_path.exists()

    def test_environment_fps_detection(self):
        """Test environment-based FPS detection"""
        loader = EnhancedConfigLoader()
        loader.config = V3Config()

        # Test production mode (default)
        with patch.dict("os.environ", {}, clear=True):
            fps = loader.get_fps_for_environment()
            assert fps == 60

        # Test development mode
        with patch.dict("os.environ", {"V3_ENV": "development"}):
            fps = loader.get_fps_for_environment()
            assert fps == 120

        # Test testing mode
        with patch.dict("os.environ", {"V3_ENV": "testing"}):
            fps = loader.get_fps_for_environment()
            assert fps == 1000


class TestConfigurationIntegration:
    """Test integration with other components"""

    def test_animation_clock_config_integration(self):
        """Test AnimationClock uses configuration values"""
        # Reset animation clock to ensure fresh state
        AnimationClock._config_loaded = False

        # Test production mode uses config values
        AnimationClock.set_production_mode()
        fps = AnimationClock.get_fps()

        # Should use config value (60) not hardcoded default
        assert fps == 60

        # Test mode detection
        mode_info = AnimationClock.get_mode_info()
        assert mode_info["mode"] == "production"
        assert mode_info["fps"] == 60

    def test_config_helper_functions(self):
        """Test configuration helper functions"""
        config = get_config()
        assert isinstance(config, V3Config)

        animation_config = get_animation_config()
        assert animation_config.fps.production == 60

        ui_config = get_ui_config()
        assert ui_config.timeline.max_content_preview == 50

        theme_config = get_theme_config("nord")
        assert theme_config.primary == "#88c0d0"

        # Test fallback theme
        theme_config = get_theme_config("nonexistent")
        assert theme_config.primary == "#88c0d0"  # Falls back to nord

    def test_config_theme_access(self):
        """Test theme configuration access"""
        # Test available themes
        config = get_config()
        assert hasattr(config.themes, "nord")
        assert hasattr(config.themes, "gruvbox")
        assert hasattr(config.themes, "tokyo_night")

        # Test theme properties
        nord = config.themes.nord
        assert nord.primary == "#88c0d0"
        assert nord.dark is True

        gruvbox = config.themes.gruvbox
        assert gruvbox.primary == "#83a598"
        assert gruvbox.dark is True


class TestYAMLConfigMigration:
    """Test migration of hardcoded values to YAML"""

    def test_preserves_existing_config_values(self):
        """Test that existing config.yaml values are preserved"""
        config = get_config()

        # These values should be preserved from existing config.yaml
        assert config.animation.typewriter_speeds.initial == 200
        assert config.animation.typewriter_speeds.progress == 200
        assert config.animation.typewriter_speeds.completion == 200
        assert config.animation.typewriter_speeds.summary == 200

        # UI values should be preserved
        assert config.ui.timeline.max_content_preview == 50

    def test_new_config_values_available(self):
        """Test that new configuration values are available"""
        config = get_config()

        # New animation values should be available
        assert hasattr(config.animation, "transitions")
        assert config.animation.transitions.live_to_inscribed == 0.3

        # Theme configurations should be available
        assert hasattr(config, "themes")
        assert hasattr(config.themes, "nord")

        # Mock scenario configs should be available
        assert hasattr(config, "mock_scenarios")
        assert hasattr(config.mock_scenarios, "cognition")

        # Dev config should be available
        assert hasattr(config, "dev")
        assert config.dev.hot_reload is True
