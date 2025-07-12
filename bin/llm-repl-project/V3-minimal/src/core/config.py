"""Configuration for LLM REPL application.

This module contains global configuration parameters that can be adjusted
for debugging and testing purposes.

Usage:
    from src.core.config import Config
    
    # Set processing durations for debugging
    Config.set_cognition_duration(10.0)  # 10 seconds for cognition
    Config.set_submodule_duration(3.0)   # 3 seconds per sub-module

Note: These settings are global and affect all processing in the app.
"""

class Config:
    """Global configuration for the application."""
    
    # Processing durations for debugging
    COGNITION_PROCESSING_DURATION = 5.0  # seconds
    SUBMODULE_PROCESSING_DURATION = 5.0  # seconds per sub-module
    
    # Manual inscribe mode - user must trigger inscription
    MANUAL_INSCRIBE_MODE = False  # Set to True to require manual inscription
    
    @classmethod
    def set_cognition_duration(cls, duration: float):
        """Set the cognition processing duration."""
        cls.COGNITION_PROCESSING_DURATION = duration
    
    @classmethod
    def set_submodule_duration(cls, duration: float):
        """Set the sub-module processing duration."""
        cls.SUBMODULE_PROCESSING_DURATION = duration