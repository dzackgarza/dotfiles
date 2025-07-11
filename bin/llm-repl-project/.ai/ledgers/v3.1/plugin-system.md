# Ledger: Plugin System

**Goal:** To implement a robust, extensible, and secure plugin system that allows for dynamic discovery, validation, and management of tools, including support for Model Context Protocol (MCP) servers, and to orchestrate the core application flow, *with a critical focus on transparent data aggregation, nesting, and interaction with the 'live' vs. 'inscribed' block lifecycle*.

## 1. Core Philosophy

- **Extensibility:** Allow users to integrate any tool that can describe itself in JSON, without needing to write Python code.
- **Security:** Enforce architectural and UI contracts through a validation process, *including external validation of plugin integrity*.
- **Dynamic Discovery:** Automatically find and register new tools from various sources.
- **User-Friendly Management:** Provide a clear and consistent interface for managing plugins and MCP servers.
- **Structured Turn Orchestration:** Explicitly manage the `User -> Cognition -> Assistant` turn flow through a dedicated orchestrator.
- **Transparency & Aggregation:** Ensure all intermediate data, wall times, and token usage from nested plugins are transparently aggregated and presented at the parent block level.
- **Live vs. Inscribed Interaction:** Plugins must seamlessly interact with the `LiveBlockManager` and `TimelineManager` to manage the lifecycle of blocks from transient 'live' states to permanent 'inscribed' states.

### Implementation Plan
1. **Phase 1: Planning** - Review and plan implementation
2. **Phase 2: Implementation** - Core development work
3. **Phase 3: Testing** - Testing and validation
4. **Phase 4: UX Polish** - Final polish and user experience improvements
5. **Phase 5: Integration** - Integrate ledger into the main system

## 2. Core Functionality

### 2.1. Generic `BasePlugin` and `PluginManager`

To enable a truly extensible system, a generic `BasePlugin` abstract class will define the interface for all plugins. A `PluginManager` will be responsible for registering, managing, and providing instances of these plugins.

#### `src/plugins/base.py`
```python
from abc import ABC, abstractmethod
from typing import Any, Dict

class BasePlugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def process(self, input_data: Any, context: Dict[str, Any]) -> Any:
        pass

    # Optional: for rendering plugin-specific content if not handled by TimelineBlock
    # async def render(self, context: Dict[str, Any]) -> Any:
    #     pass
```

#### `src/plugins/manager.py`
```python
from typing import Dict, Type
from src.plugins.base import BasePlugin

class PluginManager:
    def __init__(self):
        self._plugins: Dict[str, Type[BasePlugin]] = {}

    def register_plugin(self, plugin_class: Type[BasePlugin]):
        if not issubclass(plugin_class, BasePlugin):
            raise TypeError(f"{plugin_class.__name__} must inherit from BasePlugin.")
        self._plugins[plugin_class.name] = plugin_class

    def get_plugin_instance(self, name: str, *args, **kwargs) -> BasePlugin:
        plugin_class = self._plugins.get(name)
        if not plugin_class:
            raise ValueError(f"Plugin '{name}' not registered.")
        return plugin_class(*args, **kwargs)

plugin_manager = PluginManager() # Singleton instance
```

### 2.2. `TurnOrchestrator` for Core Application Flow

The `TurnOrchestrator` will explicitly manage the `User -> Cognition -> Assistant` sequence, ensuring that each stage of the application's core loop is handled by the appropriate plugin. It will also be responsible for initiating and completing 'live' blocks and ensuring their proper inscription.

#### `src/core/turn_orchestrator.py`
```python
from src.core.timeline_manager import timeline
from src.core.timeline_block import TimelineBlock
from src.plugins.manager import plugin_manager
import time

class TurnOrchestrator:
    async def process_turn(self, user_input: str):
        # Assume LiveBlockManager is available and initialized
        # from src.core.live_block_manager import live_block_manager

        try:
            # 1. User Input Plugin (starts a live block)
            user_block_id = "user_" + str(uuid.uuid4()) # Example ID
            live_block_manager.start_live_block(user_block_id, "user")
            user_plugin = plugin_manager.get_plugin_instance("user_input")
            user_output = await user_plugin.process(user_input, {})
            inscribed_user_block = await live_block_manager.complete_live_block(user_block_id, user_output, {"tokens": len(user_input.split())}) # Example metadata
            timeline.add_block(inscribed_user_block)

            # 2. Cognition Plugin (starts a live block, potentially nested)
            cognition_block_id = "cognition_" + str(uuid.uuid4())
            live_block_manager.start_live_block(cognition_block_id, "cognition")
            cognition_plugin = plugin_manager.get_plugin_instance("cognition")
            cognition_output = await cognition_plugin.process(user_output, {})
            inscribed_cognition_block = await live_block_manager.complete_live_block(cognition_block_id, cognition_output, {"wall_time": 5.5, "tokens_in": 525, "tokens_out": 1455}) # Example metadata
            timeline.add_block(inscribed_cognition_block)

            # 3. Assistant Plugin (starts a live block)
            assistant_block_id = "assistant_" + str(uuid.uuid4())
            live_block_manager.start_live_block(assistant_block_id, "assistant")
            assistant_plugin = plugin_manager.get_plugin_instance("assistant_response")
            assistant_output = await assistant_plugin.process(cognition_output, {})
            inscribed_assistant_block = await live_block_manager.complete_live_block(assistant_block_id, assistant_output, {"tokens": len(assistant_output.split())}) # Example metadata
            timeline.add_block(inscribed_assistant_block)

        except Exception as e:
            # 4. Error Plugin (if any stage fails)
            error_plugin = plugin_manager.get_plugin_instance("error_reporter")
            error_details = await error_plugin.process(e, {"user_input": user_input})
            error_block_id = "error_" + str(uuid.uuid4())
            live_block_manager.start_live_block(error_block_id, "error")
            inscribed_error_block = await live_block_manager.complete_live_block(error_block_id, error_details, {})
            timeline.add_block(inscribed_error_block)
```

### 2.3. Plugin Nesting and Data Aggregation

Plugins, especially the `CognitionPlugin`, will support nesting of sub-plugins or modules. The parent plugin will be responsible for aggregating metrics (wall time, token usage) and intermediate outputs from its nested components. This aggregated data will be included in the parent's `TimelineBlock` metadata.

### 2.4. Command-Based Plugin Discovery

#### Feature

- Implement a mechanism to discover plugins by running a user-configurable shell command.
- The command will be expected to return a JSON array of `FunctionDeclaration`-like objects.

#### Implementation Details

-   **Configuration:** Add a `plugin_discovery_command` setting to `settings.yaml`.
-   **Discovery Process:** Execute the `plugin_discovery_command` to parse JSON output and create `DiscoveredPlugin` instances.
-   **`DiscoveredPlugin` Class:** A wrapper class that executes the configured tool-call command, passing arguments as JSON on stdin and parsing stdout as the result.

### 2.5. Plugin Validator and External Validation

#### Feature

- A `PluginValidator` class that enforces our architectural and UI contracts for all plugins, *including mechanisms for external validation of plugin integrity and trustworthiness*.

#### Validation Rules

-   **Transparency Contract:** Ensure the plugin provides all required metadata (name, description, parameters, expected data types for live updates).
-   **UI Contract:** For plugins with UI components, ensure they adhere to our theming and aesthetic guidelines.
-   **Safety Contract:** Disallow plugins that attempt to perform unsafe operations (e.g., modifying the timeline, accessing unauthorized system resources).
-   **External Validation:** Implement a mechanism to verify the source, checksum, or digital signature of external plugins to prevent malicious code injection.

### 2.6. MCP (Model Context Protocol) Server Support and Management

#### Feature

- Add support for discovering and interacting with tools from MCP servers, and provide a user-friendly command interface for managing MCP server configurations.

#### Implementation Details

1.  **MCP Server Management Commands (`/mcp`):
    -   **`/mcp list`:** Displays a formatted table of all configured MCP servers.
    -   **`/mcp add <name> <url>`:** Adds a new MCP server to the configuration.
    -   **`/mcp remove <name>`:** Removes an MCP server by name.
    -   **`/mcp edit <name> [new_name] [--url <new_url>]`:** Edits MCP server properties.
    -   **`/mcp connect [name]`:** Attempts to connect to a specific MCP server (or all).
2.  **Configuration File Management:**
    -   Manage MCP server configurations in a YAML file (e.g., `mcp_servers.yaml`).
    -   Include a one-time migration from `mcp_servers.json` to `mcp_servers.yaml` on startup.
3.  **MCP Architecture:**
    -   Implement `MCPManager` for server discovery, connection, and tool integration.
    -   Support dynamic tool registration from MCP servers, schema validation, and tool execution routing.

## 3. Advanced Features

-   **Interactive Mode:** An `/mcp edit --interactive` command for guided editing of server properties.
-   **Health Checks:** Include latency and other health check information for connected servers in `/mcp list`.
-   **MCP Server Marketplace:** Explore integration with a marketplace for discovering and installing MCP servers.
-   **Tool Recommendation Engine:** Develop a system to recommend relevant tools based on user context.