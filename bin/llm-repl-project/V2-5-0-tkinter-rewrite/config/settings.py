"""
Application Configuration Settings

Manages configuration for different environments and use cases.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class AppConfig:
    """Application configuration."""
    name: str
    description: str
    cognition_delay: float  # Delay per cognitive step
    max_input_length: int
    theme: str
    window_size: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'description': self.description,
            'cognition_delay': self.cognition_delay,
            'max_input_length': self.max_input_length,
            'theme': self.theme,
            'window_size': self.window_size
        }


# Configuration presets
CONFIGURATIONS = {
    'debug': AppConfig(
        name='debug',
        description='Debug configuration with detailed logging',
        cognition_delay=0.5,  # Slower for debugging
        max_input_length=10000,
        theme='light',
        window_size='1200x800'
    ),
    'fast': AppConfig(
        name='fast',
        description='Fast configuration for quick interactions',
        cognition_delay=0.1,  # Faster processing
        max_input_length=5000,
        theme='light',
        window_size='1000x700'
    ),
    'demo': AppConfig(
        name='demo',
        description='Demo configuration for presentations',
        cognition_delay=0.8,  # Slower for demo visibility
        max_input_length=2000,
        theme='light',
        window_size='1400x900'
    ),
    'test': AppConfig(
        name='test',
        description='Test configuration for automated testing',
        cognition_delay=0.05,  # Very fast for tests
        max_input_length=1000,
        theme='light',
        window_size='800x600'
    )
}


def get_config(config_name: str) -> AppConfig:
    """Get configuration by name."""
    if config_name not in CONFIGURATIONS:
        print(f"Warning: Unknown configuration '{config_name}', using 'debug'")
        config_name = 'debug'
    
    return CONFIGURATIONS[config_name]


def list_configurations() -> Dict[str, str]:
    """List available configurations."""
    return {name: config.description for name, config in CONFIGURATIONS.items()}