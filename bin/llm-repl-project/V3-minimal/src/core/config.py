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

    # Debug mode - pause responses in staging for inspection before inscription
    DEBUG_MODE = True  # When True, use \inscribe command to commit responses

    # Legacy alias for backward compatibility
    MANUAL_INSCRIBE_MODE = DEBUG_MODE

    # Use simple debug mode for now (not processing queue)
    USE_PROCESSING_QUEUE = False

    @classmethod
    def set_cognition_duration(cls, duration: float):
        """Set the cognition processing duration."""
        cls.COGNITION_PROCESSING_DURATION = duration

    @classmethod
    def set_submodule_duration(cls, duration: float):
        """Set the sub-module processing duration."""
        cls.SUBMODULE_PROCESSING_DURATION = duration

    @classmethod
    def enable_debug_mode(cls):
        """Enable debug mode - responses pause in staging for inspection."""
        cls.DEBUG_MODE = True
        cls.MANUAL_INSCRIBE_MODE = True

    @classmethod
    def disable_debug_mode(cls):
        """Disable debug mode - responses auto-inscribe as normal."""
        cls.DEBUG_MODE = False
        cls.MANUAL_INSCRIBE_MODE = False
