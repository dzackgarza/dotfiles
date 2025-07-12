"""Cognition Manager

Manages hot-swappable cognition modules and routes events.
"""

from typing import Optional, Callable, Awaitable, Dict, Any
from .base import CognitionModule, CognitionEvent, CognitionResult
from .noop_module import NoOpCognitionModule
from .mock_module import MockCognitionModule


class CognitionManager:
    """Manages cognition modules and event routing"""

    def __init__(self):
        self.current_module: Optional[CognitionModule] = None
        self.available_modules: Dict[str, CognitionModule] = {}

        # Callbacks for UI integration
        self.staging_callback: Optional[Callable[[CognitionEvent], Awaitable[None]]] = (
            None
        )
        self.timeline_callback: Optional[
            Callable[[CognitionResult], Awaitable[None]]
        ] = None

        # Register default modules
        self._register_default_modules()

    def _register_default_modules(self):
        """Register built-in modules"""
        noop = NoOpCognitionModule()
        mock = MockCognitionModule()

        self.available_modules[noop.get_name()] = noop
        self.available_modules[mock.get_name()] = mock

        # Set Mock as default for better demonstration
        self.set_module(mock.get_name())

    def set_staging_callback(
        self, callback: Callable[[CognitionEvent], Awaitable[None]]
    ):
        """Set callback for staging area updates"""
        self.staging_callback = callback
        if self.current_module:
            self.current_module.set_staging_callback(callback)

    def set_timeline_callback(
        self, callback: Callable[[CognitionResult], Awaitable[None]]
    ):
        """Set callback for timeline inscription"""
        self.timeline_callback = callback
        if self.current_module:
            self.current_module.set_timeline_callback(callback)

    def register_module(self, module: CognitionModule):
        """Register a new cognition module"""
        self.available_modules[module.get_name()] = module

    def set_module(self, module_name: str) -> bool:
        """Set active cognition module by name"""
        if module_name not in self.available_modules:
            return False

        self.current_module = self.available_modules[module_name]

        # Wire callbacks
        if self.staging_callback:
            self.current_module.set_staging_callback(self.staging_callback)
        if self.timeline_callback:
            self.current_module.set_timeline_callback(self.timeline_callback)

        return True

    def get_current_module_name(self) -> str:
        """Get name of current module"""
        return self.current_module.get_name() if self.current_module else "None"

    def get_available_modules(self) -> Dict[str, str]:
        """Get available modules with descriptions"""
        return {
            name: module.get_description()
            for name, module in self.available_modules.items()
        }

    async def process_query(
        self, query: str, context: Optional[Dict[str, Any]] = None
    ) -> CognitionResult:
        """Process query through current cognition module"""
        if not self.current_module:
            raise ValueError("No cognition module set")

        # Process through module (it will emit events via callbacks)
        result = await self.current_module.process(query, context)

        # Inscribe result to timeline
        await self.current_module.inscribe_to_timeline(result)

        # Return result for any additional processing
        return result
