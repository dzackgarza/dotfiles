"""
Enhanced Configuration System for V3-minimal

Provides comprehensive YAML configuration with validation, hot-reload,
and schema-driven configuration management.
"""

import os
import time
from pathlib import Path
from typing import Any, Callable, List, Optional

import yaml
from pydantic import BaseModel, ValidationError, Field
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class ConfigurationError(Exception):
    """Raised when configuration loading or validation fails"""

    pass


class AppConfig(BaseModel):
    """Application-level configuration"""

    title: str = "LLM REPL V3-minimal"
    subtitle: str = "Sacred Timeline • Elegant Typography"
    default_theme: str = "nord"
    welcome_message: str = (
        "🔮 **Welcome to LLM REPL V3-minimal**\n\n"
        "Sacred Timeline • Live Blocks • Elegant Typography\n"
        "*Ask anything to begin your research session...*"
    )


class FPSConfig(BaseModel):
    """FPS configuration for different environments"""

    production: int = 60
    development: int = 120
    testing: int = 1000


class TypewriterSpeedsConfig(BaseModel):
    """Character-per-second rates for different animation types"""

    initial: int = 1500
    progress: int = 2000
    completion: int = 2500
    summary: int = 1800
    default: int = 1800


class TransitionsConfig(BaseModel):
    """Animation transition durations in seconds"""

    live_to_inscribed: float = 0.3
    progress_bar: float = 0.2
    token_counter: float = 0.5
    fade_in: float = 0.2
    fade_out: float = 0.15


class AnimationConfig(BaseModel):
    """Animation system configuration"""

    fps: FPSConfig = Field(default_factory=FPSConfig)
    typewriter_speeds: TypewriterSpeedsConfig = Field(
        default_factory=TypewriterSpeedsConfig
    )
    transitions: TransitionsConfig = Field(default_factory=TransitionsConfig)


class ThemeColorConfig(BaseModel):
    """Theme color configuration"""

    primary: str
    secondary: str
    accent: str
    warning: str
    error: str
    success: str
    dark: bool = True


class ThemesConfig(BaseModel):
    """Configuration for all available themes"""

    nord: ThemeColorConfig = Field(
        default_factory=lambda: ThemeColorConfig(
            primary="#88c0d0",
            secondary="#b48ead",
            accent="#81a1c1",
            warning="#ebcb8b",
            error="#bf616a",
            success="#a3be8c",
            dark=True,
        )
    )
    gruvbox: ThemeColorConfig = Field(
        default_factory=lambda: ThemeColorConfig(
            primary="#83a598",
            secondary="#d3869b",
            accent="#fabd2f",
            warning="#fe8019",
            error="#fb4934",
            success="#b8bb26",
            dark=True,
        )
    )
    tokyo_night: ThemeColorConfig = Field(
        default_factory=lambda: ThemeColorConfig(
            primary="#7aa2f7",
            secondary="#bb9af7",
            accent="#7dcfff",
            warning="#e0af68",
            error="#f7768e",
            success="#9ece6a",
            dark=True,
        )
    )


class TimelineUIConfig(BaseModel):
    """Timeline UI configuration"""

    margin_bottom: int = 1
    padding: List[int] = Field(default_factory=lambda: [0, 1])
    max_content_preview: int = 50


class LiveBlockUIConfig(BaseModel):
    """Live block widget configuration"""

    border_radius: str = "round"
    padding: int = 1
    min_height: int = 0


class TimelineBlockUIConfig(BaseModel):
    """Timeline block widget configuration"""

    margin_bottom: int = 1
    padding: List[int] = Field(default_factory=lambda: [0, 1])


class WidgetsConfig(BaseModel):
    """Widget-specific configuration"""

    live_block: LiveBlockUIConfig = Field(default_factory=LiveBlockUIConfig)
    timeline_block: TimelineBlockUIConfig = Field(default_factory=TimelineBlockUIConfig)


class UIConfig(BaseModel):
    """UI-related configuration"""

    timeline: TimelineUIConfig = Field(default_factory=TimelineUIConfig)
    widgets: WidgetsConfig = Field(default_factory=WidgetsConfig)


class CognitionStepConfig(BaseModel):
    """Configuration for a cognition step"""

    time_range: List[float] = Field(default_factory=lambda: [0.5, 1.5])
    tokens_in_range: List[int] = Field(default_factory=lambda: [10, 20])
    tokens_out_range: List[int] = Field(default_factory=lambda: [50, 100])


class MockCognitionConfig(BaseModel):
    """Mock cognition scenario configuration"""

    route_query: CognitionStepConfig = Field(
        default_factory=lambda: CognitionStepConfig(
            time_range=[0.3, 0.8], tokens_in_range=[5, 15], tokens_out_range=[1, 5]
        )
    )
    call_tool: CognitionStepConfig = Field(
        default_factory=lambda: CognitionStepConfig(
            time_range=[1.5, 3.0],
            tokens_in_range=[10, 20],
            tokens_out_range=[1000, 1500],
        )
    )
    format_output: CognitionStepConfig = Field(
        default_factory=lambda: CognitionStepConfig(
            time_range=[0.8, 1.5],
            tokens_in_range=[400, 600],
            tokens_out_range=[200, 300],
        )
    )


class MockScenariosConfig(BaseModel):
    """Mock scenarios configuration"""

    cognition: MockCognitionConfig = Field(default_factory=MockCognitionConfig)


class DevConfig(BaseModel):
    """Development-specific configuration"""

    hot_reload: bool = True
    validation: str = "strict"
    auto_save_theme: bool = True
    debug_mode: bool = False


class V3Config(BaseModel):
    """Complete V3-minimal configuration"""

    app: AppConfig = Field(default_factory=AppConfig)
    animation: AnimationConfig = Field(default_factory=AnimationConfig)
    themes: ThemesConfig = Field(default_factory=ThemesConfig)
    ui: UIConfig = Field(default_factory=UIConfig)
    mock_scenarios: MockScenariosConfig = Field(default_factory=MockScenariosConfig)
    dev: DevConfig = Field(default_factory=DevConfig)


class ConfigFileHandler(FileSystemEventHandler):
    """Handles configuration file change events for hot-reload"""

    def __init__(
        self,
        config_loader: "EnhancedConfigLoader",
        callback: Callable[[V3Config], None],
    ):
        self.config_loader = config_loader
        self.callback = callback
        self.last_modified = 0.0

    def on_modified(self, event):
        if event.is_directory:
            return

        if event.src_path == str(self.config_loader.config_path):
            # Debounce rapid file changes
            current_time = time.time()
            if current_time - self.last_modified < 0.5:
                return
            self.last_modified = current_time

            try:
                new_config = self.config_loader.load_config()
                self.callback(new_config)
            except ConfigurationError:
                # Ignore errors during hot-reload to prevent crashes
                pass


class EnhancedConfigLoader:
    """Enhanced configuration loader with validation and hot-reload"""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or self._find_config_file()
        self.config: V3Config = V3Config()
        self._observers: List[Any] = []  # Observer instances
        self._callbacks: List[Callable[[V3Config], None]] = []

    def _find_config_file(self) -> Path:
        """Find configuration file in order of preference"""
        search_paths = [
            Path.cwd() / "config.yaml",  # Current directory
            Path.home() / ".config" / "llm-repl" / "config.yaml",  # User config
            Path(__file__).parent.parent.parent / "config.yaml",  # Project default
        ]

        for path in search_paths:
            if path.exists():
                return path

        # Return default location for config generation
        return Path.home() / ".config" / "llm-repl" / "config.yaml"

    def _generate_default_config(self) -> None:
        """Generate default configuration file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        default_config = V3Config()
        config_dict = default_config.model_dump()

        with open(self.config_path, "w") as f:
            yaml.dump(
                config_dict, f, default_flow_style=False, sort_keys=False, indent=2
            )

    def load_config(self) -> V3Config:
        """Load and validate configuration from YAML file"""
        if not self.config_path or not self.config_path.exists():
            self._generate_default_config()

        try:
            with open(self.config_path, "r") as f:
                yaml_data = yaml.safe_load(f) or {}

            self.config = V3Config(**yaml_data)
            return self.config

        except ValidationError as e:
            raise ConfigurationError(f"Invalid configuration: {e}")
        except yaml.YAMLError as e:
            raise ConfigurationError(f"YAML parsing error: {e}")
        except Exception as e:
            raise ConfigurationError(f"Configuration loading error: {e}")

    def save_config(self, config: Optional[V3Config] = None) -> None:
        """Save configuration to YAML file"""
        config_to_save = config or self.config

        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            config_dict = config_to_save.model_dump()

            with open(self.config_path, "w") as f:
                yaml.dump(
                    config_dict, f, default_flow_style=False, sort_keys=False, indent=2
                )

        except Exception as e:
            raise ConfigurationError(f"Configuration saving error: {e}")

    def enable_hot_reload(self, callback: Callable[[V3Config], None]) -> None:
        """Enable hot-reload of configuration changes"""
        if not self.config_path or not self.config_path.exists():
            return

        self._callbacks.append(callback)

        handler = ConfigFileHandler(self, self._on_config_changed)
        observer = Observer()
        observer.schedule(handler, str(self.config_path.parent), recursive=False)
        observer.start()
        self._observers.append(observer)

    def _on_config_changed(self, new_config: V3Config) -> None:
        """Handle configuration changes"""
        self.config = new_config
        for callback in self._callbacks:
            callback(new_config)

    def stop_hot_reload(self) -> None:
        """Stop hot-reload observers"""
        for observer in self._observers:
            observer.stop()
            observer.join()
        self._observers.clear()
        self._callbacks.clear()

    def get_environment_mode(self) -> str:
        """Get current environment mode"""
        return os.getenv("V3_ENV", "production")

    def get_fps_for_environment(self) -> int:
        """Get FPS setting for current environment"""
        env_mode = self.get_environment_mode()
        fps_config = self.config.animation.fps

        if env_mode == "development":
            return fps_config.development
        elif env_mode == "testing":
            return fps_config.testing
        else:
            return fps_config.production


# Global configuration instance
_config_loader: Optional[EnhancedConfigLoader] = None
_current_config: Optional[V3Config] = None


def get_config_loader() -> EnhancedConfigLoader:
    """Get global configuration loader instance"""
    global _config_loader
    if _config_loader is None:
        _config_loader = EnhancedConfigLoader()
        _config_loader.load_config()
    return _config_loader


def get_config() -> V3Config:
    """Get current configuration"""
    global _current_config
    if _current_config is None:
        loader = get_config_loader()
        _current_config = loader.config
    return _current_config


def reload_config() -> V3Config:
    """Reload configuration from file"""
    global _current_config
    loader = get_config_loader()
    _current_config = loader.load_config()
    return _current_config


# Configuration access helpers
def get_animation_config() -> AnimationConfig:
    """Get animation configuration"""
    return get_config().animation


def get_ui_config() -> UIConfig:
    """Get UI configuration"""
    return get_config().ui


def get_theme_config(theme_name: Optional[str] = None) -> ThemeColorConfig:
    """Get theme configuration"""
    config = get_config()
    theme_name = theme_name or config.app.default_theme

    themes = config.themes
    if hasattr(themes, theme_name):
        return getattr(themes, theme_name)
    else:
        return themes.nord  # Fallback to nord theme
