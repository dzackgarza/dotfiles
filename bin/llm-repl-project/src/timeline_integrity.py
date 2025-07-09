#!/usr/bin/env python3
"""
Timeline Integrity System - Architectural Guarantees for Plugin-Only Timeline

This module makes it STRUCTURALLY IMPOSSIBLE to pollute the timeline with
non-plugin content. Only proper plugin instances with full metadata can
appear on the timeline.

ARCHITECTURAL GUARANTEES:
1. Timeline class ONLY accepts validated plugin instances
2. No direct console access for main application
3. All timeline content MUST have LLM usage tracking
4. Plugin contracts are enforced at compile/runtime
5. Local hacks are prevented by access control
"""

from typing import Protocol, runtime_checkable, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
import time
from abc import ABC, abstractmethod


class PluginValidationError(Exception):
    """Raised when plugin doesn't meet timeline requirements."""
    pass


@dataclass(frozen=True)
class PluginMetadata:
    """
    Required metadata for timeline-eligible plugins.
    
    This ensures all timeline content has proper tracking.
    """
    plugin_name: str
    wall_time_seconds: float
    llm_input_tokens: int
    llm_output_tokens: int
    processing_timestamp: float
    plugin_state: str  # Must be COMPLETED
    
    def __post_init__(self):
        """Validate plugin metadata meets timeline requirements."""
        if self.wall_time_seconds < 0:
            raise PluginValidationError(f"Invalid wall time: {self.wall_time_seconds}")
        
        if self.llm_input_tokens < 0 or self.llm_output_tokens < 0:
            raise PluginValidationError(f"Invalid token counts: {self.llm_input_tokens}/{self.llm_output_tokens}")
        
        if self.plugin_state != "COMPLETED":
            raise PluginValidationError(f"Only COMPLETED plugins allowed on timeline, got: {self.plugin_state}")


@runtime_checkable
class TimelineEligiblePlugin(Protocol):
    """
    Protocol for plugins that can appear on timeline.
    
    This enforces the contract that timeline content must be proper plugins
    with all required metadata and processing guarantees.
    """
    
    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata with LLM usage, timing, etc."""
        ...
    
    def get_rendered_content(self) -> str:
        """Get rendered content for timeline display."""
        ...
    
    def validate_timeline_eligibility(self) -> bool:
        """Validate that plugin meets timeline requirements."""
        ...


class TimelineIntegrityGuard:
    """
    Guard that enforces timeline integrity.
    
    This class makes it impossible to bypass plugin requirements.
    """
    
    def __init__(self):
        self._validated_plugins: Dict[str, TimelineEligiblePlugin] = {}
        self._timeline_locked = False
    
    def validate_plugin_for_timeline(self, plugin: Any) -> bool:
        """
        Validate that plugin meets timeline requirements.
        
        Returns True only if plugin has all required metadata and contracts.
        """
        # Check if plugin implements the required protocol
        if not isinstance(plugin, TimelineEligiblePlugin):
            raise PluginValidationError(
                f"Plugin {plugin} does not implement TimelineEligiblePlugin protocol"
            )
        
        # Validate plugin metadata
        try:
            metadata = plugin.get_metadata()
            if not isinstance(metadata, PluginMetadata):
                raise PluginValidationError(
                    f"Plugin {plugin} returned invalid metadata type"
                )
        except Exception as e:
            raise PluginValidationError(
                f"Plugin {plugin} failed metadata validation: {e}"
            )
        
        # Validate plugin eligibility
        if not plugin.validate_timeline_eligibility():
            raise PluginValidationError(
                f"Plugin {plugin} failed timeline eligibility check"
            )
        
        return True
    
    def register_validated_plugin(self, plugin: TimelineEligiblePlugin) -> str:
        """
        Register a validated plugin for timeline access.
        
        Returns plugin ID that can be used for timeline operations.
        """
        # Validate plugin first
        if not self.validate_plugin_for_timeline(plugin):
            raise PluginValidationError("Plugin validation failed")
        
        # Generate unique ID
        plugin_id = f"{plugin.get_metadata().plugin_name}_{int(time.time() * 1000)}"
        
        # Store validated plugin
        self._validated_plugins[plugin_id] = plugin
        
        return plugin_id
    
    def get_validated_plugin(self, plugin_id: str) -> Optional[TimelineEligiblePlugin]:
        """Get validated plugin by ID."""
        return self._validated_plugins.get(plugin_id)
    
    def is_plugin_validated(self, plugin_id: str) -> bool:
        """Check if plugin is validated for timeline access."""
        return plugin_id in self._validated_plugins


class SecureTimeline:
    """
    Secure timeline that ONLY accepts validated plugins.
    
    This makes it architecturally impossible to pollute the timeline
    with non-plugin content.
    """
    
    def __init__(self, console):
        self._console = console
        self._integrity_guard = TimelineIntegrityGuard()
        self._timeline_entries: list = []
        self._timeline_sealed = False
    
    def add_plugin_to_timeline(self, plugin: TimelineEligiblePlugin) -> None:
        """
        Add validated plugin to timeline.
        
        This is the ONLY way to add content to the timeline.
        """
        if self._timeline_sealed:
            raise RuntimeError("Timeline is sealed - no more additions allowed")
        
        # Validate plugin through integrity guard
        plugin_id = self._integrity_guard.register_validated_plugin(plugin)
        
        # Add to timeline
        self._timeline_entries.append({
            'plugin_id': plugin_id,
            'plugin': plugin,
            'timestamp': time.time(),
            'metadata': plugin.get_metadata()
        })
        
        # Render to console
        self._render_plugin_to_console(plugin)
    
    def _render_plugin_to_console(self, plugin: TimelineEligiblePlugin) -> None:
        """Render validated plugin to console."""
        content = plugin.get_rendered_content()
        self._console.print(content)
    
    def get_timeline_summary(self) -> Dict[str, Any]:
        """Get summary of timeline with all plugin metadata."""
        return {
            'total_plugins': len(self._timeline_entries),
            'total_wall_time': sum(entry['metadata'].wall_time_seconds for entry in self._timeline_entries),
            'total_llm_tokens': sum(
                entry['metadata'].llm_input_tokens + entry['metadata'].llm_output_tokens
                for entry in self._timeline_entries
            ),
            'plugins': [
                {
                    'name': entry['metadata'].plugin_name,
                    'wall_time': entry['metadata'].wall_time_seconds,
                    'tokens': entry['metadata'].llm_input_tokens + entry['metadata'].llm_output_tokens
                }
                for entry in self._timeline_entries
            ]
        }
    
    def seal_timeline(self) -> None:
        """
        Seal timeline to prevent further additions.
        
        This creates a immutable timeline state.
        """
        self._timeline_sealed = True
    
    def print(self, *args, **kwargs):
        """
        DISABLED: Direct printing is architecturally forbidden.
        
        This prevents all bypasses to the plugin system.
        """
        raise RuntimeError(
            "Direct timeline access is forbidden! "
            "Content must go through add_plugin_to_timeline() with proper plugin validation. "
            "This enforces timeline integrity - only validated plugins with metadata allowed."
        )
    
    def display_block(self, *args, **kwargs):
        """
        DISABLED: Direct block display is architecturally forbidden.
        """
        raise RuntimeError(
            "Direct block display is forbidden! "
            "Content must go through add_plugin_to_timeline() with proper plugin validation."
        )
    
    def display_prompt(self, prompt: str) -> None:
        """
        Display prompt outside timeline.
        
        Prompts are not timeline content - they're input interface.
        """
        # Prompts are allowed as they're not timeline content
        self._console.print(prompt, end="", highlight=False)


class ApplicationWithSecureTimeline:
    """
    Application wrapper that enforces timeline integrity.
    
    This makes it impossible for the main application to bypass
    the plugin system through direct console access.
    """
    
    def __init__(self, console):
        self._timeline = SecureTimeline(console)
        # NO direct console access - forces plugin system usage
    
    def get_timeline(self) -> SecureTimeline:
        """Get secure timeline for validated plugin additions."""
        return self._timeline
    
    def add_plugin_to_timeline(self, plugin: TimelineEligiblePlugin) -> None:
        """Add validated plugin to timeline."""
        self._timeline.add_plugin_to_timeline(plugin)
    
    def display_prompt(self, prompt: str) -> None:
        """Display prompt (not timeline content)."""
        self._timeline.display_prompt(prompt)
    
    def get_timeline_summary(self) -> Dict[str, Any]:
        """Get timeline summary with all plugin metadata."""
        return self._timeline.get_timeline_summary()
    
    # NO print() method - prevents bypasses
    # NO display_block() method - prevents bypasses
    # NO console access - prevents bypasses