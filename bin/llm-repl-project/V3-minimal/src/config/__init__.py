"""
Configuration system for V3-minimal

Provides both legacy compatibility and enhanced YAML configuration.
"""

# Legacy imports for backward compatibility
from .config import (
    AppConfig as LegacyAppConfig,
    ThemeConfig as LegacyThemeConfig,
    RoleConfig,
    TimelineConfig,
    ConfigLoader,
    UIConfig,
    AnimationConfig,
)

# Enhanced configuration system
from .enhanced_config import (
    V3Config,
    EnhancedConfigLoader,
    ConfigurationError,
    get_config,
    get_config_loader,
    reload_config,
    get_animation_config,
    get_ui_config,
    get_theme_config,
    # Configuration models
    AppConfig as EnhancedAppConfig,
    AnimationConfig as EnhancedAnimationConfig,
    ThemesConfig,
    UIConfig as EnhancedUIConfig,
    MockScenariosConfig,
    DevConfig,
)

# Expose legacy interface for backward compatibility
AppConfig = LegacyAppConfig
ThemeConfig = LegacyThemeConfig

__all__ = [
    # Legacy compatibility
    "AppConfig",
    "ThemeConfig",
    "RoleConfig",
    "TimelineConfig",
    "ConfigLoader",
    "UIConfig",
    "AnimationConfig",
    # Enhanced system
    "V3Config",
    "EnhancedConfigLoader",
    "ConfigurationError",
    "get_config",
    "get_config_loader",
    "reload_config",
    "get_animation_config",
    "get_ui_config",
    "get_theme_config",
    # Enhanced configuration models
    "EnhancedAppConfig",
    "EnhancedAnimationConfig",
    "ThemesConfig",
    "EnhancedUIConfig",
    "MockScenariosConfig",
    "DevConfig",
]
